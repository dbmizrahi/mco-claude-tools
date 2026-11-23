"""MCP server for Google Workspace: Gmail, Calendar, Drive, Docs, Sheets, Slides and Chat.

Tools:

  account     google_whoami, google_api_request
  gmail       gmail_search_messages, gmail_get_message, gmail_get_thread, gmail_list_labels,
              gmail_download_attachment, gmail_modify_labels, gmail_create_draft, gmail_send_message
  calendar    calendar_list_calendars, calendar_list_events, calendar_get_event,
              calendar_create_event, calendar_update_event, calendar_delete_event
  drive       drive_search_files, drive_get_file, drive_read_file, drive_create_folder,
              drive_upload_file, drive_download_file, drive_export_file, drive_copy_file,
              drive_update_file, drive_trash_file, drive_delete_file, drive_list_permissions,
              drive_share_file, drive_unshare_file, drive_list_shared_drives
  docs        docs_get_document, docs_get_outline, docs_export_text, docs_create_document,
              docs_append_text, docs_insert_text, docs_replace_text, docs_batch_update
  sheets      sheets_get_spreadsheet, sheets_read_values, sheets_batch_read, sheets_update_values,
              sheets_append_values, sheets_clear_values, sheets_create_spreadsheet,
              sheets_add_sheet, sheets_rename_sheet, sheets_delete_sheet, sheets_batch_update
  slides      slides_get_presentation, slides_create_presentation, slides_add_slide,
              slides_duplicate_slide, slides_delete_object, slides_replace_text, slides_set_text,
              slides_get_thumbnail, slides_batch_update
  chat        chat_list_spaces, chat_list_messages, chat_send_message

Every call runs as the Google account behind the refresh token, limited to the
scopes that token was granted. Google's errors come back as tool errors with a hint.

Run:  google-workspace-mcp            (stdio transport, for Claude Code / Claude Desktop)
      google-workspace-mcp check      (no MCP: print the credential source, account and scopes)
      google-workspace-mcp auth ...   (sign in once and save a credential file; see auth.py)
"""

from __future__ import annotations

import asyncio
import base64
import functools
import hashlib
import inspect
import json
import logging
import mimetypes
import os
import re
import sys
import uuid
from datetime import date, datetime, time as dtime, timedelta
from email.message import EmailMessage
from email.utils import getaddresses
from html import unescape
from pathlib import Path
from typing import Annotated, Any, Awaitable, Callable, Literal, TypeVar
from urllib.parse import quote

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import Field

from google_workspace_mcp import __version__
from google_workspace_mcp.client import TOKENINFO_URL, USERINFO_URL, GoogleClient, GoogleError
from google_workspace_mcp.config import ConfigError, load_config

log = logging.getLogger("google_workspace_mcp")

GMAIL = "https://gmail.googleapis.com/gmail/v1/users/me"
CALENDAR = "https://www.googleapis.com/calendar/v3"
DRIVE = "https://www.googleapis.com/drive/v3"
DOCS = "https://docs.googleapis.com/v1/documents"
SHEETS = "https://sheets.googleapis.com/v4/spreadsheets"
CHAT = "https://chat.googleapis.com/v1"
FETCH_CONCURRENCY = 8

INSTRUCTIONS = """\
Google Workspace access (Gmail, Calendar, Drive, Docs, Sheets, Slides, Chat) as one Google account.
Several copies of this server may run side by side, one per account (e.g. private and work);
each answers only for its own account. Start with google_whoami to see the account, its label
and which scopes it has; a tool whose scope
is missing fails with a message naming the granted scopes.
Gmail search uses Gmail query syntax (from:, to:, subject:, after:YYYY/MM/DD, is:unread,
label:, has:attachment). Calendar and Chat times are RFC 3339 (2026-10-12T09:00:00+03:00);
a bare date YYYY-MM-DD is also accepted where noted. Results are paginated: pass the
returned next_page_token back as page_token. Downloads and exports are saved on the machine
running this server. For edits the dedicated tools do not cover, use docs_batch_update,
sheets_batch_update or slides_batch_update. For anything else, google_api_request
calls any https://*.googleapis.com endpoint with the same sign-in.
"""

mcp = MCPServer(
    "google_workspace_mcp",
    title="Google Workspace",
    version=__version__,
    instructions=INSTRUCTIONS,
    log_level="WARNING",  # stderr stays quiet; stdout is the protocol channel
)

# --------------------------------------------------------------------------- client
_client: GoogleClient | None = None


def set_client(client: GoogleClient | None) -> None:
    """Install a client (tests inject one with a mock transport)."""
    global _client
    _client = client


def get_client() -> GoogleClient:
    global _client
    if _client is None:
        try:
            _client = GoogleClient(load_config())
        except ConfigError as exc:
            raise ToolError(f"Google sign-in is not configured: {exc}") from exc
    return _client


F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def google_tool(func: F) -> F:
    """Turn Google/config failures into tool errors the model can read and act on."""

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except (GoogleError, ConfigError) as exc:
            raise ToolError(str(exc)) from exc

    # The docstring becomes the tool description the model reads: strip the indentation.
    wrapper.__doc__ = inspect.cleandoc(func.__doc__ or "")
    return wrapper  # type: ignore[return-value]


READ = ToolAnnotations(read_only_hint=True, idempotent_hint=True, open_world_hint=True)
CREATE = ToolAnnotations(read_only_hint=False, destructive_hint=False, idempotent_hint=False, open_world_hint=True)
CHANGE = ToolAnnotations(read_only_hint=False, destructive_hint=True, idempotent_hint=True, open_world_hint=True)
DESTROY = ToolAnnotations(read_only_hint=False, destructive_hint=True, idempotent_hint=False, open_world_hint=True)

PAGE_TOKEN_DESC = "next_page_token from the previous call, to get the next page."


# ------------------------------------------------------------------- helpers
def _seg(value: str) -> str:
    """An id placed into a URL path segment."""
    value = value.strip()
    if not value:
        raise ToolError("id must not be empty")
    return quote(value, safe="@")


def _truncate(text: str, limit: int) -> tuple[str, bool]:
    return (text, False) if len(text) <= limit else (text[:limit], True)


def _b64url_decode(data: str) -> str:
    raw = base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))
    return raw.decode("utf-8", "replace")


TAG_RE = re.compile(r"<[^>]+>")
STYLE_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)
BREAK_RE = re.compile(r"<(br|/p|/div|/tr|/li|/h[1-6])[^>]*>", re.I)


def _html_to_text(html: str) -> str:
    text = STYLE_RE.sub("", html)
    text = BREAK_RE.sub("\n", text)
    text = unescape(TAG_RE.sub("", text))
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+", " ", text)).strip()


def _check_rfc3339(value: str, name: str) -> str:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ToolError(f"{name} must be RFC 3339 like 2026-10-12T09:00:00+03:00, got {value!r}") from exc
    if not re.search(r"(Z|[+-]\d\d:\d\d)$", value):
        raise ToolError(f"{name} needs a UTC offset (…Z or …+03:00), got {value!r}")
    return value


def _day_start(value: str, tz_name: str) -> str:
    """'YYYY-MM-DD' -> RFC 3339 midnight in tz_name; RFC 3339 passes through (validated)."""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        from zoneinfo import ZoneInfo

        try:
            zone = ZoneInfo(tz_name)
        except Exception as exc:  # noqa: BLE001 - bad name or missing tzdata
            raise ToolError(f"unknown time zone {tz_name!r}: {exc}") from exc
        return datetime.combine(date.fromisoformat(value), dtime(0, 0), zone).isoformat()
    return _check_rfc3339(value, "time")


def _next_day(value: str) -> str:
    """For an inclusive end date 'YYYY-MM-DD', the following day; other values unchanged."""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return (date.fromisoformat(value) + timedelta(days=1)).isoformat()
    return value


# ===================================================================== account
@mcp.tool(name="google_whoami", title="Google: account and granted scopes", annotations=READ)
@google_tool
async def google_whoami() -> dict[str, Any]:
    """Verify the Google sign-in and report the account and the OAuth scopes it was granted.

    Returns {"account_label", "email", "name", "scopes": [...], "services": {"gmail": true, ...},
    "connection": {where the credential came from}}. Call this first when something
    fails: a dead refresh token or a missing scope shows up here.
    """
    client = get_client()
    token = await client.access_token(force=True)
    info = await client.request("GET", TOKENINFO_URL, params={"access_token": token})
    scopes = sorted(str(info.get("scope", "")).split()) or client.granted_scopes
    email = info.get("email")
    name = None
    if any(s.endswith(("userinfo.profile", "userinfo.email")) or s in ("openid", "email", "profile") for s in scopes):
        try:
            user = await client.get(USERINFO_URL)
            email, name = user.get("email", email), user.get("name")
        except GoogleError:
            pass
    if not email and any("gmail" in s or s.endswith("mail.google.com/") for s in scopes):
        try:
            email = (await client.get(f"{GMAIL}/profile")).get("emailAddress")
        except GoogleError:
            pass

    def has(*parts: str) -> bool:
        return any(any(p in s for p in parts) for s in scopes)

    return {
        "account_label": client.config.account_label,
        "email": email,
        "name": name,
        "scopes": scopes,
        "services": {
            "gmail": has("gmail", "mail.google.com"),
            "calendar": has("auth/calendar"),
            "drive": has("auth/drive"),
            "docs": has("auth/documents", "auth/drive"),
            "sheets": has("auth/spreadsheets", "auth/drive"),
            "slides": has("auth/presentations", "auth/drive"),
            "chat": has("auth/chat"),
        },
        "connection": client.config.describe(),
    }


@mcp.tool(name="google_api_request", title="Google: call any Google REST endpoint", annotations=DESTROY)
@google_tool
async def google_api_request(
    method: Annotated[Literal["GET", "POST", "PUT", "PATCH", "DELETE"], Field(description="HTTP method.")],
    url: Annotated[str, Field(description="Full https://*.googleapis.com URL, e.g. https://tasks.googleapis.com/tasks/v1/users/@me/lists")],
    params: Annotated[dict[str, Any] | None, Field(description="Query parameters.")] = None,
    body: Annotated[Any, Field(description="JSON request body for POST/PUT/PATCH.")] = None,
) -> dict[str, Any]:
    """Call any Google REST API endpoint with this account's sign-in — for operations the
    other tools do not cover (Tasks, People, Drive permissions, Calendar ACLs, ...).

    Returns {"status", "result": <decoded JSON>}. Only https://*.googleapis.com URLs are
    accepted. Can change or delete data depending on the method.
    """
    client = get_client()
    response = await client.request(method, url, params=params, json_body=body, raw=True)
    try:
        result: Any = response.json() if response.content.strip() else None
    except ValueError:
        text, cut = _truncate(response.text, client.config.max_text_chars)
        result = {"text": text, "truncated": cut}
    return {"status": response.status_code, "result": result}


# ======================================================================= gmail
def _headers(payload: dict[str, Any]) -> dict[str, str]:
    return {h.get("name", ""): h.get("value", "") for h in payload.get("headers", []) if isinstance(h, dict)}


def _summary(msg: dict[str, Any]) -> dict[str, Any]:
    h = _headers(msg.get("payload", {}))
    return {
        "id": msg.get("id"),
        "thread_id": msg.get("threadId"),
        "date": h.get("Date"),
        "from": h.get("From"),
        "to": h.get("To"),
        "subject": h.get("Subject"),
        "snippet": unescape(msg.get("snippet", "")),
        "labels": msg.get("labelIds", []),
    }


def _walk_parts(part: dict[str, Any], plain: list[str], html: list[str], files: list[dict[str, Any]]) -> None:
    mime = part.get("mimeType", "")
    body = part.get("body", {}) or {}
    filename = part.get("filename") or ""
    if filename:
        files.append({"filename": filename, "mime_type": mime, "size": body.get("size"), "attachment_id": body.get("attachmentId")})
    elif body.get("data"):
        if mime == "text/plain":
            plain.append(_b64url_decode(body["data"]))
        elif mime == "text/html":
            html.append(_b64url_decode(body["data"]))
    for sub in part.get("parts", []) or []:
        _walk_parts(sub, plain, html, files)


def _full_message(msg: dict[str, Any], limit: int) -> dict[str, Any]:
    plain: list[str] = []
    html: list[str] = []
    files: list[dict[str, Any]] = []
    payload = msg.get("payload", {})
    _walk_parts(payload, plain, html, files)
    text = "\n".join(plain).strip() or _html_to_text("\n".join(html))
    body, cut = _truncate(text, limit)
    h = _headers(payload)
    out = _summary(msg)
    out.update({"cc": h.get("Cc"), "message_id_header": h.get("Message-ID") or h.get("Message-Id"),
                "body": body, "body_truncated": cut, "attachments": files})
    return out


@mcp.tool(name="gmail_search_messages", title="Gmail: search messages", annotations=READ)
@google_tool
async def gmail_search_messages(
    query: Annotated[str, Field(description="Gmail search query, e.g. 'from:alice after:2026/10/01 subject:invoice', 'in:sent newer_than:7d', 'is:unread label:inbox'. Empty = all mail.")] = "",
    max_results: Annotated[int, Field(ge=1, le=100, description="Page size.")] = 20,
    page_token: Annotated[str | None, Field(description=PAGE_TOKEN_DESC)] = None,
    include_spam_trash: Annotated[bool, Field(description="Also search Spam and Trash.")] = False,
) -> dict[str, Any]:
    """Search Gmail and return a summary of each matching message: id, thread_id, date,
    from, to, subject, snippet, labels. Newest first.

    Returns {"count", "result_size_estimate", "next_page_token", "messages": [...]}.
    Read a full message with gmail_get_message, a conversation with gmail_get_thread.
    """
    client = get_client()
    listing = await client.get(
        f"{GMAIL}/messages", q=query or None, maxResults=max_results, pageToken=page_token,
        includeSpamTrash=str(include_spam_trash).lower(),
    )
    ids = [m["id"] for m in listing.get("messages", [])]
    sem = asyncio.Semaphore(FETCH_CONCURRENCY)

    async def fetch(mid: str) -> dict[str, Any]:
        async with sem:
            return await client.request(
                "GET", f"{GMAIL}/messages/{_seg(mid)}",
                params={"format": "metadata", "metadataHeaders": ["From", "To", "Subject", "Date"]},
            )

    messages = await asyncio.gather(*(fetch(m) for m in ids))
    return {
        "count": len(messages),
        "result_size_estimate": listing.get("resultSizeEstimate"),
        "next_page_token": listing.get("nextPageToken"),
        "messages": [_summary(m) for m in messages],
    }


@mcp.tool(name="gmail_get_message", title="Gmail: read a message", annotations=READ)
@google_tool
async def gmail_get_message(
    message_id: Annotated[str, Field(description="Message id from gmail_search_messages.")],
) -> dict[str, Any]:
    """Read one message: headers, plain-text body (HTML converted to text when there is no
    plain part) and the list of attachments (name, type, size, attachment_id).

    The body is cut at $GOOGLE_MAX_TEXT_CHARS; "body_truncated" says when.
    """
    client = get_client()
    msg = await client.get(f"{GMAIL}/messages/{_seg(message_id)}", format="full")
    return _full_message(msg, client.config.max_text_chars)


MAX_ATTACHMENT_BYTES = 25 * 1024 * 1024


def _attachment_parts(part: dict[str, Any], out: list[dict[str, Any]]) -> None:
    if part.get("filename"):
        out.append(part)
    for sub in part.get("parts", []) or []:
        _attachment_parts(sub, out)


@mcp.tool(name="gmail_download_attachment", title="Gmail: save an attachment to disk", annotations=READ)
@google_tool
async def gmail_download_attachment(
    message_id: Annotated[str, Field(description="Message id from gmail_search_messages.")],
    attachment_id: Annotated[str | None, Field(description="attachment_id from gmail_get_message. Give this or filename.")] = None,
    filename: Annotated[str | None, Field(description="Exact attachment file name, when there is no attachment_id or it is easier.")] = None,
    save_path: Annotated[str | None, Field(description=(
        "Local file or folder to save to on the machine running this server. A folder keeps the "
        "attachment's name. Omit to save into $GOOGLE_DOWNLOAD_DIR (default ~/Downloads)."))] = None,
    overwrite: Annotated[bool, Field(description="Replace an existing local file.")] = False,
) -> dict[str, Any]:
    """Save one attachment of a Gmail message to a local file. The file's bytes are never
    returned, only where it was saved.

    Returns {"saved_to", "bytes", "filename", "mime_type", "sha256", "message_id"}.
    Attachments over 25 MB are refused. Find attachments with gmail_get_message.
    """
    if not attachment_id and not filename:
        raise ToolError("give attachment_id or filename (see gmail_get_message)")
    client = get_client()
    msg = await client.get(f"{GMAIL}/messages/{_seg(message_id)}", format="full")
    parts: list[dict[str, Any]] = []
    _attachment_parts(msg.get("payload", {}), parts)
    if attachment_id:
        matches = [p for p in parts if (p.get("body") or {}).get("attachmentId") == attachment_id]
    else:
        matches = [p for p in parts if p.get("filename") == filename]
    if not matches:
        names = ", ".join(repr(p.get("filename")) for p in parts) or "none"
        raise ToolError(f"no such attachment in message {message_id}; attachments: {names}")
    if len(matches) > 1:
        raise ToolError(f"{len(matches)} attachments are named {filename!r}; pass attachment_id instead")
    part = matches[0]
    body = part.get("body") or {}
    size = int(body.get("size") or 0)
    if size > MAX_ATTACHMENT_BYTES:
        raise ToolError(f"attachment is {size} bytes; the limit is {MAX_ATTACHMENT_BYTES} (25 MB)")
    name = str(part.get("filename"))
    target = _target_path(save_path, name, overwrite)
    if body.get("attachmentId"):
        att = await client.get(f"{GMAIL}/messages/{_seg(message_id)}/attachments/{_seg(str(body['attachmentId']))}")
        encoded = str(att.get("data", ""))
    else:
        encoded = str(body.get("data", ""))
    data = base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4))
    if len(data) > MAX_ATTACHMENT_BYTES:
        raise ToolError(f"attachment is {len(data)} bytes; the limit is {MAX_ATTACHMENT_BYTES} (25 MB)")
    saved = _write(target, data)
    return {**saved, "filename": name, "mime_type": part.get("mimeType"),
            "sha256": hashlib.sha256(data).hexdigest(), "message_id": message_id}


@mcp.tool(name="gmail_get_thread", title="Gmail: read a conversation", annotations=READ)
@google_tool
async def gmail_get_thread(
    thread_id: Annotated[str, Field(description="Thread id (thread_id from gmail_search_messages).")],
) -> dict[str, Any]:
    """Read every message of a conversation, oldest first, each with headers and body.

    Returns {"thread_id", "count", "messages": [...]}. Bodies share the
    $GOOGLE_MAX_TEXT_CHARS budget evenly.
    """
    client = get_client()
    thread = await client.get(f"{GMAIL}/threads/{_seg(thread_id)}", format="full")
    msgs = thread.get("messages", [])
    per = max(client.config.max_text_chars // max(len(msgs), 1), 500)
    return {"thread_id": thread.get("id"), "count": len(msgs), "messages": [_full_message(m, per) for m in msgs]}


@mcp.tool(name="gmail_list_labels", title="Gmail: list labels", annotations=READ)
@google_tool
async def gmail_list_labels() -> dict[str, Any]:
    """List Gmail labels (system and user) with their ids, for gmail_modify_labels and
    label: searches. Returns {"count", "labels": [{"id", "name", "type"}]}."""
    client = get_client()
    labels = (await client.get(f"{GMAIL}/labels")).get("labels", [])
    rows = sorted(({"id": l.get("id"), "name": l.get("name"), "type": l.get("type")} for l in labels), key=lambda r: r["name"] or "")
    return {"count": len(rows), "labels": rows}


@mcp.tool(name="gmail_modify_labels", title="Gmail: add or remove labels", annotations=CHANGE)
@google_tool
async def gmail_modify_labels(
    message_ids: Annotated[list[str], Field(min_length=1, max_length=1000, description="Message ids to change.")],
    add_label_ids: Annotated[list[str] | None, Field(description="Label ids to add, e.g. ['STARRED'] or a user label id.")] = None,
    remove_label_ids: Annotated[list[str] | None, Field(description="Label ids to remove, e.g. ['UNREAD'] to mark read, ['INBOX'] to archive.")] = None,
) -> dict[str, Any]:
    """Add and/or remove labels on messages: mark read (remove UNREAD), archive (remove
    INBOX), star (add STARRED), trash (add TRASH), or apply user labels.
    Returns {"modified": <count>}."""
    if not add_label_ids and not remove_label_ids:
        raise ToolError("give add_label_ids and/or remove_label_ids")
    client = get_client()
    await client.request("POST", f"{GMAIL}/messages/batchModify", json_body={
        "ids": message_ids, "addLabelIds": add_label_ids or [], "removeLabelIds": remove_label_ids or [],
    })
    return {"modified": len(message_ids), "added": add_label_ids or [], "removed": remove_label_ids or []}


async def _build_raw(
    client: GoogleClient, to: list[str], subject: str, body: str, cc: list[str] | None,
    bcc: list[str] | None, reply_to_message_id: str | None, html: bool,
) -> tuple[str, str | None]:
    msg = EmailMessage()
    thread_id = None
    if reply_to_message_id:
        orig = await client.request(
            "GET", f"{GMAIL}/messages/{_seg(reply_to_message_id)}",
            params={"format": "metadata", "metadataHeaders": ["Message-ID", "References", "Subject"]},
        )
        h = {k.lower(): v for k, v in _headers(orig.get("payload", {})).items()}
        thread_id = orig.get("threadId")
        if h.get("message-id"):
            msg["In-Reply-To"] = h["message-id"]
            msg["References"] = f"{h.get('references', '')} {h['message-id']}".strip()
        if not subject:
            orig_subject = h.get("subject", "")
            subject = orig_subject if orig_subject.lower().startswith("re:") else f"Re: {orig_subject}"
    if to:
        msg["To"] = ", ".join(to)
    if cc:
        msg["Cc"] = ", ".join(cc)
    if bcc:
        msg["Bcc"] = ", ".join(bcc)
    msg["Subject"] = subject
    if html:
        msg.set_content(_html_to_text(body))
        msg.add_alternative(body, subtype="html")
    else:
        msg.set_content(body)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    return raw, thread_id


def _check_addresses(values: list[str] | None, name: str) -> None:
    for addr in values or []:
        parsed = getaddresses([addr])
        if not parsed or "@" not in parsed[0][1]:
            raise ToolError(f"{name} contains an invalid address: {addr!r}")


ADDR_DESC = "Addresses, e.g. ['alice@example.com', 'Bob <bob@example.com>']."


@mcp.tool(name="gmail_create_draft", title="Gmail: create a draft", annotations=CREATE)
@google_tool
async def gmail_create_draft(
    to: Annotated[list[str], Field(description=ADDR_DESC + " May be empty for a draft.")],
    subject: Annotated[str, Field(description="Subject. Leave empty when replying to reuse 'Re: <original>'.")],
    body: Annotated[str, Field(description="Message body, plain text (or HTML when html=true).")],
    cc: Annotated[list[str] | None, Field(description=ADDR_DESC)] = None,
    bcc: Annotated[list[str] | None, Field(description=ADDR_DESC)] = None,
    reply_to_message_id: Annotated[str | None, Field(description="Message id this replies to; threads the draft into that conversation.")] = None,
    html: Annotated[bool, Field(description="Body is HTML.")] = False,
) -> dict[str, Any]:
    """Create a Gmail draft (nothing is sent). Returns {"draft_id", "message_id", "thread_id"}."""
    for name, vals in (("to", to), ("cc", cc), ("bcc", bcc)):
        _check_addresses(vals, name)
    client = get_client()
    raw, thread_id = await _build_raw(client, to, subject, body, cc, bcc, reply_to_message_id, html)
    message: dict[str, Any] = {"raw": raw}
    if thread_id:
        message["threadId"] = thread_id
    draft = await client.request("POST", f"{GMAIL}/drafts", json_body={"message": message})
    return {"draft_id": draft.get("id"), "message_id": draft.get("message", {}).get("id"),
            "thread_id": draft.get("message", {}).get("threadId")}


@mcp.tool(name="gmail_send_message", title="Gmail: send an email", annotations=DESTROY)
@google_tool
async def gmail_send_message(
    to: Annotated[list[str], Field(min_length=1, description=ADDR_DESC)],
    subject: Annotated[str, Field(description="Subject. Leave empty when replying to reuse 'Re: <original>'.")],
    body: Annotated[str, Field(description="Message body, plain text (or HTML when html=true).")],
    cc: Annotated[list[str] | None, Field(description=ADDR_DESC)] = None,
    bcc: Annotated[list[str] | None, Field(description=ADDR_DESC)] = None,
    reply_to_message_id: Annotated[str | None, Field(description="Message id this replies to; keeps the reply in that conversation.")] = None,
    html: Annotated[bool, Field(description="Body is HTML.")] = False,
) -> dict[str, Any]:
    """Send an email immediately from this account. Cannot be undone — prefer
    gmail_create_draft when the user has not explicitly asked to send.
    Returns {"message_id", "thread_id", "labels"}."""
    for name, vals in (("to", to), ("cc", cc), ("bcc", bcc)):
        _check_addresses(vals, name)
    client = get_client()
    raw, thread_id = await _build_raw(client, to, subject, body, cc, bcc, reply_to_message_id, html)
    payload: dict[str, Any] = {"raw": raw}
    if thread_id:
        payload["threadId"] = thread_id
    sent = await client.request("POST", f"{GMAIL}/messages/send", json_body=payload)
    return {"message_id": sent.get("id"), "thread_id": sent.get("threadId"), "labels": sent.get("labelIds", [])}


# ==================================================================== calendar
CAL_ID_DESC = "Calendar id; 'primary' is the account's own calendar. Others come from calendar_list_calendars."


def _event(e: dict[str, Any]) -> dict[str, Any]:
    start, end = e.get("start", {}), e.get("end", {})
    me = next((a for a in e.get("attendees", []) if a.get("self")), None)
    return {
        "id": e.get("id"),
        "summary": e.get("summary"),
        "start": start.get("dateTime") or start.get("date"),
        "end": end.get("dateTime") or end.get("date"),
        "all_day": "date" in start,
        "status": e.get("status"),
        "my_response": me.get("responseStatus") if me else ("owner" if e.get("organizer", {}).get("self") else None),
        "organizer": e.get("organizer", {}).get("email"),
        "attendees": [a.get("email") for a in e.get("attendees", [])],
        "location": e.get("location"),
        "description": e.get("description"),
        "meet_link": e.get("hangoutLink"),
        "recurring_event_id": e.get("recurringEventId"),
        "html_link": e.get("htmlLink"),
    }


def _when(value: str, tz: str | None, name: str) -> dict[str, str]:
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return {"date": value}
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ToolError(f"{name} must be YYYY-MM-DD (all-day) or an ISO date-time, got {value!r}") from exc
    if not re.search(r"(Z|[+-]\d\d:\d\d)$", value) and not tz:
        raise ToolError(f"{name} {value!r} has no UTC offset: add one (…+03:00) or pass time_zone")
    out = {"dateTime": value}
    if tz:
        out["timeZone"] = tz
    return out


@mcp.tool(name="calendar_list_calendars", title="Calendar: list calendars", annotations=READ)
@google_tool
async def calendar_list_calendars() -> dict[str, Any]:
    """List the calendars this account sees, with id, name, access role and time zone.
    Returns {"count", "calendars": [{"id", "summary", "primary", "access_role", "time_zone"}]}."""
    client = get_client()
    rows: list[dict[str, Any]] = []
    token = None
    while True:
        page = await client.get(f"{CALENDAR}/users/me/calendarList", maxResults=250, pageToken=token)
        rows += [{"id": c.get("id"), "summary": c.get("summaryOverride") or c.get("summary"),
                  "primary": bool(c.get("primary")), "access_role": c.get("accessRole"),
                  "time_zone": c.get("timeZone")} for c in page.get("items", [])]
        token = page.get("nextPageToken")
        if not token:
            break
    return {"count": len(rows), "calendars": rows}


@mcp.tool(name="calendar_list_events", title="Calendar: list events", annotations=READ)
@google_tool
async def calendar_list_events(
    time_min: Annotated[str, Field(description="Start of the window: YYYY-MM-DD (midnight in the calendar's time zone) or RFC 3339.")],
    time_max: Annotated[str, Field(description="End of the window, inclusive when a bare date YYYY-MM-DD (the whole day), else exclusive RFC 3339.")],
    calendar_id: Annotated[str, Field(description=CAL_ID_DESC)] = "primary",
    query: Annotated[str | None, Field(description="Free-text filter on title, description, location, attendees.")] = None,
    include_declined: Annotated[bool, Field(description="Keep events this account declined.")] = True,
    max_results: Annotated[int, Field(ge=1, le=2500)] = 250,
    page_token: Annotated[str | None, Field(description=PAGE_TOKEN_DESC)] = None,
) -> dict[str, Any]:
    """List events in a time window, recurring events expanded, ordered by start time.

    Returns {"calendar_id", "time_zone", "time_min", "time_max", "count", "next_page_token",
    "events": [{"id", "summary", "start", "end", "all_day", "status", "my_response",
    "organizer", "attendees", "location", "description", "meet_link", "html_link"}]}.
    """
    client = get_client()
    cal = _seg(calendar_id)
    tz = (await client.get(f"{CALENDAR}/calendars/{cal}")).get("timeZone") or "UTC"
    tmin, tmax = _day_start(time_min, tz), _day_start(_next_day(time_max), tz)
    page = await client.get(
        f"{CALENDAR}/calendars/{cal}/events", timeMin=tmin, timeMax=tmax, q=query, singleEvents="true",
        orderBy="startTime", maxResults=max_results, pageToken=page_token, timeZone=tz,
    )
    events = [_event(e) for e in page.get("items", [])]
    if not include_declined:
        events = [e for e in events if e["my_response"] != "declined"]
    return {"calendar_id": calendar_id, "time_zone": tz, "time_min": tmin, "time_max": tmax,
            "count": len(events), "next_page_token": page.get("nextPageToken"), "events": events}


@mcp.tool(name="calendar_get_event", title="Calendar: get an event", annotations=READ)
@google_tool
async def calendar_get_event(
    event_id: Annotated[str, Field(description="Event id from calendar_list_events.")],
    calendar_id: Annotated[str, Field(description=CAL_ID_DESC)] = "primary",
) -> dict[str, Any]:
    """Read one event with attendees' responses. Returns the event fields plus
    "attendee_responses": [{"email", "response"}]."""
    client = get_client()
    e = await client.get(f"{CALENDAR}/calendars/{_seg(calendar_id)}/events/{_seg(event_id)}")
    out = _event(e)
    out["attendee_responses"] = [{"email": a.get("email"), "response": a.get("responseStatus")} for a in e.get("attendees", [])]
    return out


@mcp.tool(name="calendar_create_event", title="Calendar: create an event", annotations=CREATE)
@google_tool
async def calendar_create_event(
    summary: Annotated[str, Field(description="Event title.")],
    start: Annotated[str, Field(description="YYYY-MM-DD for an all-day event, or a date-time like 2026-10-13T10:00:00+03:00.")],
    end: Annotated[str, Field(description="Same form as start. For all-day events the day AFTER the last day (Google's rule).")],
    calendar_id: Annotated[str, Field(description=CAL_ID_DESC)] = "primary",
    description: Annotated[str | None, Field(description="Event description.")] = None,
    location: Annotated[str | None, Field(description="Location.")] = None,
    attendees: Annotated[list[str] | None, Field(description="Attendee email addresses.")] = None,
    time_zone: Annotated[str | None, Field(description="IANA zone (e.g. Asia/Jerusalem) for date-times without an offset.")] = None,
    send_updates: Annotated[Literal["all", "externalOnly", "none"], Field(description="Who gets invitation emails.")] = "none",
) -> dict[str, Any]:
    """Create a calendar event, optionally inviting attendees. Returns the created event."""
    client = get_client()
    body: dict[str, Any] = {"summary": summary, "start": _when(start, time_zone, "start"), "end": _when(end, time_zone, "end")}
    if description is not None:
        body["description"] = description
    if location is not None:
        body["location"] = location
    if attendees:
        body["attendees"] = [{"email": a} for a in attendees]
    e = await client.request("POST", f"{CALENDAR}/calendars/{_seg(calendar_id)}/events",
                             params={"sendUpdates": send_updates}, json_body=body)
    return _event(e)


@mcp.tool(name="calendar_update_event", title="Calendar: update an event", annotations=CHANGE)
@google_tool
async def calendar_update_event(
    event_id: Annotated[str, Field(description="Event id.")],
    calendar_id: Annotated[str, Field(description=CAL_ID_DESC)] = "primary",
    summary: Annotated[str | None, Field(description="New title.")] = None,
    start: Annotated[str | None, Field(description="New start (same forms as calendar_create_event).")] = None,
    end: Annotated[str | None, Field(description="New end.")] = None,
    description: Annotated[str | None, Field(description="New description.")] = None,
    location: Annotated[str | None, Field(description="New location.")] = None,
    attendees: Annotated[list[str] | None, Field(description="Replaces the whole attendee list.")] = None,
    response_status: Annotated[Literal["accepted", "declined", "tentative"] | None, Field(description="Set THIS account's RSVP on an invitation.")] = None,
    time_zone: Annotated[str | None, Field(description="IANA zone for date-times without an offset.")] = None,
    send_updates: Annotated[Literal["all", "externalOnly", "none"], Field(description="Who gets update emails.")] = "none",
) -> dict[str, Any]:
    """Change fields of an event (only the given ones), or answer an invitation with
    response_status. Returns the updated event."""
    client = get_client()
    url = f"{CALENDAR}/calendars/{_seg(calendar_id)}/events/{_seg(event_id)}"
    patch: dict[str, Any] = {}
    for key, val in (("summary", summary), ("description", description), ("location", location)):
        if val is not None:
            patch[key] = val
    if start is not None:
        patch["start"] = _when(start, time_zone, "start")
    if end is not None:
        patch["end"] = _when(end, time_zone, "end")
    if attendees is not None:
        patch["attendees"] = [{"email": a} for a in attendees]
    if response_status:
        current = await client.get(url)
        people = current.get("attendees", [])
        mine = [a for a in people if a.get("self")]
        if not mine:
            raise ToolError("this account is not an attendee of the event, so it cannot RSVP")
        mine[0]["responseStatus"] = response_status
        patch["attendees"] = people if attendees is None else patch["attendees"]
    if not patch:
        raise ToolError("nothing to change: give at least one field")
    e = await client.request("PATCH", url, params={"sendUpdates": send_updates}, json_body=patch)
    return _event(e)


@mcp.tool(name="calendar_delete_event", title="Calendar: delete an event", annotations=DESTROY)
@google_tool
async def calendar_delete_event(
    event_id: Annotated[str, Field(description="Event id.")],
    calendar_id: Annotated[str, Field(description=CAL_ID_DESC)] = "primary",
    send_updates: Annotated[Literal["all", "externalOnly", "none"], Field(description="Who gets cancellation emails.")] = "none",
) -> dict[str, Any]:
    """Delete an event. For an invitation from someone else, prefer declining with
    calendar_update_event. Returns {"deleted": true, "event_id"}."""
    client = get_client()
    await client.request("DELETE", f"{CALENDAR}/calendars/{_seg(calendar_id)}/events/{_seg(event_id)}",
                         params={"sendUpdates": send_updates})
    return {"deleted": True, "event_id": event_id}


# ======================================================================= drive
FILE_FIELDS = "id,name,mimeType,modifiedTime,createdTime,size,owners(emailAddress),webViewLink,parents,trashed"
EXPORTS = {
    "application/vnd.google-apps.document": "text/plain",
    "application/vnd.google-apps.spreadsheet": "text/csv",
    "application/vnd.google-apps.presentation": "text/plain",
    "application/vnd.google-apps.drawing": "image/svg+xml",
    "application/vnd.google-apps.script": "application/vnd.google-apps.script+json",
}
TEXTUAL = ("text/", "application/json", "application/xml", "application/javascript", "application/x-yaml", "application/yaml")


def _file(f: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f.get("id"), "name": f.get("name"), "mime_type": f.get("mimeType"),
        "modified": f.get("modifiedTime"), "created": f.get("createdTime"),
        "size": int(f["size"]) if f.get("size") else None,
        "owners": [o.get("emailAddress") for o in f.get("owners", [])],
        "link": f.get("webViewLink"), "parents": f.get("parents", []), "trashed": f.get("trashed", False),
    }


@mcp.tool(name="drive_search_files", title="Drive: search files", annotations=READ)
@google_tool
async def drive_search_files(
    name_contains: Annotated[str | None, Field(description="Text the file name contains.")] = None,
    full_text: Annotated[str | None, Field(description="Text anywhere in the file's content or name.")] = None,
    mime_type: Annotated[str | None, Field(description="Exact MIME type, e.g. application/vnd.google-apps.document, application/vnd.google-apps.spreadsheet, application/pdf, application/vnd.google-apps.folder.")] = None,
    folder_id: Annotated[str | None, Field(description="Only files directly inside this folder.")] = None,
    modified_after: Annotated[str | None, Field(description="RFC 3339, e.g. 2026-10-01T00:00:00Z.")] = None,
    query: Annotated[str | None, Field(description="Raw Drive query (q syntax) ANDed with the filters above, e.g. \"'me' in owners\".")] = None,
    include_trashed: Annotated[bool, Field(description="Include files in the trash.")] = False,
    order_by: Annotated[str, Field(description="Sort, e.g. 'modifiedTime desc', 'name'.")] = "modifiedTime desc",
    page_size: Annotated[int, Field(ge=1, le=1000)] = 50,
    page_token: Annotated[str | None, Field(description=PAGE_TOKEN_DESC)] = None,
) -> dict[str, Any]:
    """Find files in My Drive and shared drives the account can see.

    Returns {"count", "next_page_token", "files": [{"id", "name", "mime_type", "modified",
    "size", "owners", "link", ...}]}. Read one with drive_read_file.
    """
    def lit(value: str) -> str:
        return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"

    terms = []
    if name_contains:
        terms.append(f"name contains {lit(name_contains)}")
    if full_text:
        terms.append(f"fullText contains {lit(full_text)}")
    if mime_type:
        terms.append(f"mimeType = {lit(mime_type)}")
    if folder_id:
        terms.append(f"{lit(folder_id)} in parents")
    if modified_after:
        terms.append(f"modifiedTime > {lit(_check_rfc3339(modified_after, 'modified_after'))}")
    if query:
        terms.append(f"({query})")
    if not include_trashed:
        terms.append("trashed = false")
    client = get_client()
    page = await client.get(
        f"{DRIVE}/files", q=" and ".join(terms) or None, orderBy=None if full_text else order_by,
        pageSize=page_size, pageToken=page_token, fields=f"nextPageToken,files({FILE_FIELDS})",
        supportsAllDrives="true", includeItemsFromAllDrives="true", corpora="allDrives",
    )
    files = [_file(f) for f in page.get("files", [])]
    return {"count": len(files), "next_page_token": page.get("nextPageToken"), "files": files}


@mcp.tool(name="drive_get_file", title="Drive: file details", annotations=READ)
@google_tool
async def drive_get_file(
    file_id: Annotated[str, Field(description="Drive file id (also the id in a Docs/Sheets URL).")],
) -> dict[str, Any]:
    """Metadata of one file: name, type, size, owners, dates, link, parents."""
    client = get_client()
    f = await client.get(f"{DRIVE}/files/{_seg(file_id)}", fields=FILE_FIELDS, supportsAllDrives="true")
    return _file(f)


@mcp.tool(name="drive_read_file", title="Drive: read file content", annotations=READ)
@google_tool
async def drive_read_file(
    file_id: Annotated[str, Field(description="Drive file id.")],
    export_mime_type: Annotated[str | None, Field(description="For Google Docs/Sheets/Slides: export format, e.g. text/markdown, text/html, text/csv. Default: Docs and Slides as text/plain, Sheets as text/csv (first sheet only; use sheets_read_values for other tabs).")] = None,
) -> dict[str, Any]:
    """Read a file's content as text: Google Docs, Sheets and Slides are exported;
    text-like files (txt, csv, json, xml, md, code) are downloaded. Binary files (PDF,
    images, Office) are not returned — only their metadata, with a note.

    Returns {"file": {...}, "content_type", "content", "truncated"}. Content is cut at
    $GOOGLE_MAX_TEXT_CHARS.
    """
    client = get_client()
    meta = await client.get(f"{DRIVE}/files/{_seg(file_id)}", fields=FILE_FIELDS, supportsAllDrives="true")
    mime = meta.get("mimeType", "")
    if mime.startswith("application/vnd.google-apps."):
        target = export_mime_type or EXPORTS.get(mime)
        if not target:
            return {"file": _file(meta), "content_type": None, "content": None, "truncated": False,
                    "note": f"{mime} cannot be exported as text"}
        resp = await client.request("GET", f"{DRIVE}/files/{_seg(file_id)}/export", params={"mimeType": target}, raw=True)
        content_type = target
    elif mime.startswith(TEXTUAL) or mime in ("application/x-sh", "application/sql"):
        resp = await client.request("GET", f"{DRIVE}/files/{_seg(file_id)}", params={"alt": "media", "supportsAllDrives": "true"}, raw=True)
        content_type = mime
    else:
        return {"file": _file(meta), "content_type": mime, "content": None, "truncated": False,
                "note": "binary file: content not returned. Open it via the link, or export it from Drive to a text format."}
    text, cut = _truncate(resp.text, client.config.max_text_chars)
    return {"file": _file(meta), "content_type": content_type, "content": text, "truncated": cut}


# ======================================================================== docs
def _doc_text(elements: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for el in elements:
        if "paragraph" in el:
            for pe in el["paragraph"].get("elements", []):
                parts.append(pe.get("textRun", {}).get("content", ""))
        elif "table" in el:
            for row in el["table"].get("tableRows", []):
                cells = [_doc_text(c.get("content", [])).strip().replace("\n", " ") for c in row.get("tableCells", [])]
                parts.append(" | ".join(cells) + "\n")
        elif "tableOfContents" in el:
            parts.append(_doc_text(el["tableOfContents"].get("content", [])))
    return "".join(parts)


@mcp.tool(name="docs_get_document", title="Docs: read a document", annotations=READ)
@google_tool
async def docs_get_document(
    document_id: Annotated[str, Field(description="Document id (from the URL /document/d/<id>/).")],
) -> dict[str, Any]:
    """Read a Google Doc as plain text (tables as 'a | b | c' rows), with title and
    revision. Returns {"document_id", "title", "revision_id", "text", "truncated", "end_index"}."""
    client = get_client()
    doc = await client.get(f"{DOCS}/{_seg(document_id)}")
    content = doc.get("body", {}).get("content", [])
    text, cut = _truncate(_doc_text(content), client.config.max_text_chars)
    end = content[-1].get("endIndex") if content else None
    return {"document_id": doc.get("documentId"), "title": doc.get("title"), "revision_id": doc.get("revisionId"),
            "text": text, "truncated": cut, "end_index": end}


@mcp.tool(name="docs_create_document", title="Docs: create a document", annotations=CREATE)
@google_tool
async def docs_create_document(
    title: Annotated[str, Field(description="Document title.")],
    text: Annotated[str | None, Field(description="Initial plain-text content.")] = None,
) -> dict[str, Any]:
    """Create a Google Doc in My Drive, optionally with initial text.
    Returns {"document_id", "title", "link"}."""
    client = get_client()
    doc = await client.request("POST", DOCS, json_body={"title": title})
    doc_id = doc.get("documentId")
    if text:
        await client.request("POST", f"{DOCS}/{_seg(doc_id)}:batchUpdate", json_body={
            "requests": [{"insertText": {"location": {"index": 1}, "text": text}}]})
    return {"document_id": doc_id, "title": doc.get("title"), "link": f"https://docs.google.com/document/d/{doc_id}/edit"}


@mcp.tool(name="docs_append_text", title="Docs: append text", annotations=CREATE)
@google_tool
async def docs_append_text(
    document_id: Annotated[str, Field(description="Document id.")],
    text: Annotated[str, Field(min_length=1, description="Plain text to add at the end of the document. Start with '\\n' for a new paragraph.")],
) -> dict[str, Any]:
    """Append plain text at the end of a Google Doc. For other edits (replace text,
    styles, tables) use google_api_request with the Docs batchUpdate endpoint.
    Returns {"document_id", "appended_chars"}."""
    client = get_client()
    await client.request("POST", f"{DOCS}/{_seg(document_id)}:batchUpdate", json_body={
        "requests": [{"insertText": {"endOfSegmentLocation": {}, "text": text}}]})
    return {"document_id": document_id, "appended_chars": len(text)}


# ====================================================================== sheets
SHEET_ID_DESC = "Spreadsheet id (from the URL /spreadsheets/d/<id>/)."
RANGE_DESC = "A1 range, e.g. 'Sheet1!A1:D20', 'Sheet1' (whole tab), or 'A:C'."
INPUT_DESC = "USER_ENTERED parses values as if typed (formulas, dates, numbers); RAW stores them as-is."


@mcp.tool(name="sheets_get_spreadsheet", title="Sheets: spreadsheet details", annotations=READ)
@google_tool
async def sheets_get_spreadsheet(
    spreadsheet_id: Annotated[str, Field(description=SHEET_ID_DESC)],
) -> dict[str, Any]:
    """Title, locale, time zone and the list of tabs with their sizes.
    Returns {"spreadsheet_id", "title", "time_zone", "sheets": [{"sheet_id", "title", "rows", "columns"}], "link"}."""
    client = get_client()
    s = await client.get(f"{SHEETS}/{_seg(spreadsheet_id)}", fields="spreadsheetId,properties,sheets.properties,spreadsheetUrl")
    tabs = [{"sheet_id": t["properties"].get("sheetId"), "title": t["properties"].get("title"),
             "rows": t["properties"].get("gridProperties", {}).get("rowCount"),
             "columns": t["properties"].get("gridProperties", {}).get("columnCount")} for t in s.get("sheets", [])]
    return {"spreadsheet_id": s.get("spreadsheetId"), "title": s.get("properties", {}).get("title"),
            "time_zone": s.get("properties", {}).get("timeZone"), "locale": s.get("properties", {}).get("locale"),
            "sheets": tabs, "link": s.get("spreadsheetUrl")}


@mcp.tool(name="sheets_read_values", title="Sheets: read cells", annotations=READ)
@google_tool
async def sheets_read_values(
    spreadsheet_id: Annotated[str, Field(description=SHEET_ID_DESC)],
    range: Annotated[str, Field(description=RANGE_DESC)],
    render: Annotated[Literal["FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA"], Field(description="FORMATTED_VALUE as shown in the UI; UNFORMATTED_VALUE raw numbers; FORMULA the formulas.")] = "FORMATTED_VALUE",
) -> dict[str, Any]:
    """Read a range of cells as rows. Returns {"range", "row_count", "values": [[...], ...]}.
    Trailing empty rows and cells are omitted by Google."""
    client = get_client()
    v = await client.get(f"{SHEETS}/{_seg(spreadsheet_id)}/values/{quote(range, safe='')}", valueRenderOption=render)
    values = v.get("values", [])
    return {"range": v.get("range"), "row_count": len(values), "values": values}


@mcp.tool(name="sheets_update_values", title="Sheets: write cells", annotations=CHANGE)
@google_tool
async def sheets_update_values(
    spreadsheet_id: Annotated[str, Field(description=SHEET_ID_DESC)],
    range: Annotated[str, Field(description="Top-left cell or full A1 range to overwrite, e.g. 'Sheet1!B2'.")],
    values: Annotated[list[list[Any]], Field(min_length=1, description="Rows of cell values, e.g. [['Name','Hours'],['David',8]].")],
    value_input: Annotated[Literal["USER_ENTERED", "RAW"], Field(description=INPUT_DESC)] = "USER_ENTERED",
) -> dict[str, Any]:
    """Overwrite cells starting at range. Returns {"updated_range", "updated_rows", "updated_cells"}."""
    client = get_client()
    r = await client.request("PUT", f"{SHEETS}/{_seg(spreadsheet_id)}/values/{quote(range, safe='')}",
                             params={"valueInputOption": value_input}, json_body={"values": values})
    return {"updated_range": r.get("updatedRange"), "updated_rows": r.get("updatedRows"), "updated_cells": r.get("updatedCells")}


@mcp.tool(name="sheets_append_values", title="Sheets: append rows", annotations=CREATE)
@google_tool
async def sheets_append_values(
    spreadsheet_id: Annotated[str, Field(description=SHEET_ID_DESC)],
    range: Annotated[str, Field(description="The table to append to, e.g. 'Sheet1' or 'Sheet1!A:D'. Rows go after its last row.")],
    values: Annotated[list[list[Any]], Field(min_length=1, description="Rows to append.")],
    value_input: Annotated[Literal["USER_ENTERED", "RAW"], Field(description=INPUT_DESC)] = "USER_ENTERED",
) -> dict[str, Any]:
    """Append rows after the last row of a table. Returns {"updated_range", "updated_rows"}."""
    client = get_client()
    r = await client.request("POST", f"{SHEETS}/{_seg(spreadsheet_id)}/values/{quote(range, safe='')}:append",
                             params={"valueInputOption": value_input, "insertDataOption": "INSERT_ROWS"},
                             json_body={"values": values})
    u = r.get("updates", {})
    return {"updated_range": u.get("updatedRange"), "updated_rows": u.get("updatedRows")}


@mcp.tool(name="sheets_create_spreadsheet", title="Sheets: create a spreadsheet", annotations=CREATE)
@google_tool
async def sheets_create_spreadsheet(
    title: Annotated[str, Field(description="Spreadsheet title.")],
    sheet_titles: Annotated[list[str] | None, Field(description="Tab names. Default: one tab 'Sheet1'.")] = None,
) -> dict[str, Any]:
    """Create a spreadsheet in My Drive. Returns {"spreadsheet_id", "title", "sheets", "link"}."""
    client = get_client()
    body: dict[str, Any] = {"properties": {"title": title}}
    if sheet_titles:
        body["sheets"] = [{"properties": {"title": t}} for t in sheet_titles]
    s = await client.request("POST", SHEETS, json_body=body)
    return {"spreadsheet_id": s.get("spreadsheetId"), "title": s.get("properties", {}).get("title"),
            "sheets": [t["properties"]["title"] for t in s.get("sheets", [])], "link": s.get("spreadsheetUrl")}


# ================================================================ drive: files
UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"
FOLDER_MIME = "application/vnd.google-apps.folder"
EXPORT_FORMATS = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "odt": "application/vnd.oasis.opendocument.text",
    "ods": "application/x-vnd.oasis.opendocument.spreadsheet",
    "odp": "application/vnd.oasis.opendocument.presentation",
    "rtf": "application/rtf",
    "txt": "text/plain",
    "md": "text/markdown",
    "csv": "text/csv",
    "tsv": "text/tab-separated-values",
    "html": "application/zip",
    "epub": "application/epub+zip",
    "png": "image/png",
    "jpg": "image/jpeg",
    "svg": "image/svg+xml",
}
CONVERT_TO = {
    "document": "application/vnd.google-apps.document",
    "spreadsheet": "application/vnd.google-apps.spreadsheet",
    "presentation": "application/vnd.google-apps.presentation",
}
SAVE_PATH_DESC = (
    "Local path to save to on the machine running this server. A directory keeps the "
    "Drive file name. Omit to save into $GOOGLE_DOWNLOAD_DIR (default ~/Downloads)."
)


def _target_path(save_path: str | None, default_name: str, overwrite: bool) -> Path:
    """Where to save: a given file path, a given directory (keeps default_name), or the download dir."""
    if save_path is None:
        path = Path(os.path.expanduser(get_client().config.download_dir)) / _safe_name(default_name)
    else:
        given = Path(os.path.expanduser(save_path))
        is_dir = given.is_dir() or save_path.endswith(("/", os.sep))
        path = given / _safe_name(default_name) if is_dir else given
    if not path.parent.is_dir():
        raise ToolError(f"folder {path.parent} does not exist")
    if path.exists() and not overwrite:
        raise ToolError(f"{path} already exists; pass overwrite=true to replace it")
    return path


def _safe_name(name: str) -> str:
    cleaned = re.sub(r'[/\\:*?"<>|\x00-\x1f]', "_", name).strip(" .")
    return cleaned or "download"


def _write(path: Path, data: bytes) -> dict[str, Any]:
    try:
        path.write_bytes(data)
    except OSError as exc:
        raise ToolError(f"cannot write {path}: {exc}") from exc
    return {"saved_to": str(path), "bytes": len(data)}


@mcp.tool(name="drive_create_folder", title="Drive: create a folder", annotations=CREATE)
@google_tool
async def drive_create_folder(
    name: Annotated[str, Field(min_length=1, description="Folder name.")],
    parent_id: Annotated[str | None, Field(description="Parent folder id (or shared drive id). Omit for My Drive root.")] = None,
) -> dict[str, Any]:
    """Create a folder. Returns the new folder's details (id, name, link)."""
    client = get_client()
    body: dict[str, Any] = {"name": name, "mimeType": FOLDER_MIME}
    if parent_id:
        body["parents"] = [parent_id]
    f = await client.request("POST", f"{DRIVE}/files", params={"fields": FILE_FIELDS, "supportsAllDrives": "true"}, json_body=body)
    return _file(f)


@mcp.tool(name="drive_upload_file", title="Drive: upload a local file", annotations=CREATE)
@google_tool
async def drive_upload_file(
    local_path: Annotated[str, Field(description="Path of the file on the machine running this server.")],
    name: Annotated[str | None, Field(description="Name in Drive. Default: the local file name.")] = None,
    parent_id: Annotated[str | None, Field(description="Destination folder id. Omit for My Drive root.")] = None,
    convert_to: Annotated[Literal["document", "spreadsheet", "presentation"] | None, Field(description="Convert on upload: Word/text/HTML -> document, Excel/CSV -> spreadsheet, PowerPoint -> presentation.")] = None,
    mime_type: Annotated[str | None, Field(description="MIME type of the local file. Default: guessed from the extension.")] = None,
) -> dict[str, Any]:
    """Upload a local file to Drive, optionally converting it to a Google Doc, Sheet or
    Slides. Returns the new file's details."""
    path = Path(os.path.expanduser(local_path))
    if not path.is_file():
        raise ToolError(f"{path} is not a file")
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ToolError(f"cannot read {path}: {exc}") from exc
    source_type = mime_type or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    meta: dict[str, Any] = {"name": name or path.name}
    if parent_id:
        meta["parents"] = [parent_id]
    if convert_to:
        meta["mimeType"] = CONVERT_TO[convert_to]
        if not name:
            meta["name"] = path.stem
    client = get_client()
    start = await client.request(
        "POST", UPLOAD, params={"uploadType": "resumable", "supportsAllDrives": "true"}, json_body=meta, raw=True,
        headers={"X-Upload-Content-Type": source_type, "X-Upload-Content-Length": str(len(data))},
    )
    session = start.headers.get("Location")
    if not session:
        raise ToolError("Drive did not return an upload session URL")
    f = await client.request("PUT", session, content=data, headers={"Content-Type": source_type},
                             params={"fields": FILE_FIELDS})
    return _file(f)


@mcp.tool(name="drive_download_file", title="Drive: download a file to disk", annotations=READ)
@google_tool
async def drive_download_file(
    file_id: Annotated[str, Field(description="Drive file id of a regular (non-Google) file: PDF, image, Office file, zip, ...")],
    save_path: Annotated[str | None, Field(description=SAVE_PATH_DESC)] = None,
    overwrite: Annotated[bool, Field(description="Replace an existing local file.")] = False,
) -> dict[str, Any]:
    """Download a file's bytes to a local path. Google Docs/Sheets/Slides have no bytes
    of their own — use drive_export_file for them. Returns {"file", "saved_to", "bytes"}."""
    client = get_client()
    meta = await client.get(f"{DRIVE}/files/{_seg(file_id)}", fields=FILE_FIELDS, supportsAllDrives="true")
    if str(meta.get("mimeType", "")).startswith("application/vnd.google-apps."):
        raise ToolError(f"{meta.get('name')!r} is a {meta.get('mimeType')}; use drive_export_file to save it as pdf/docx/xlsx/pptx/...")
    target = _target_path(save_path, meta.get("name") or file_id, overwrite)
    resp = await client.request("GET", f"{DRIVE}/files/{_seg(file_id)}", params={"alt": "media", "supportsAllDrives": "true"}, raw=True)
    return {"file": _file(meta), **_write(target, resp.content)}


@mcp.tool(name="drive_export_file", title="Drive: export a Google file", annotations=READ)
@google_tool
async def drive_export_file(
    file_id: Annotated[str, Field(description="Id of a Google Doc, Sheet, Slides or Drawing.")],
    format: Annotated[Literal["pdf", "docx", "xlsx", "pptx", "odt", "ods", "odp", "rtf", "txt", "md", "csv", "tsv", "html", "epub", "png", "jpg", "svg"],
                      Field(description="Docs: pdf, docx, odt, rtf, txt, md, html (zip), epub. Sheets: pdf, xlsx, ods, csv/tsv (first tab), html. Slides: pdf, pptx, odp, txt. Drawings: pdf, png, jpg, svg.")],
    save_path: Annotated[str | None, Field(description=SAVE_PATH_DESC)] = None,
    overwrite: Annotated[bool, Field(description="Replace an existing local file.")] = False,
) -> dict[str, Any]:
    """Export a Google Doc/Sheet/Slides/Drawing to a file format and save it locally.
    Google caps exports at 10 MB. Returns {"file", "format", "saved_to", "bytes"}."""
    client = get_client()
    meta = await client.get(f"{DRIVE}/files/{_seg(file_id)}", fields=FILE_FIELDS, supportsAllDrives="true")
    if not str(meta.get("mimeType", "")).startswith("application/vnd.google-apps."):
        raise ToolError(f"{meta.get('name')!r} is a regular file ({meta.get('mimeType')}); use drive_download_file")
    ext = "zip" if format == "html" else format
    target = _target_path(save_path, f"{meta.get('name') or file_id}.{ext}", overwrite)
    resp = await client.request("GET", f"{DRIVE}/files/{_seg(file_id)}/export", params={"mimeType": EXPORT_FORMATS[format]}, raw=True)
    return {"file": _file(meta), "format": format, **_write(target, resp.content)}


@mcp.tool(name="drive_copy_file", title="Drive: copy a file", annotations=CREATE)
@google_tool
async def drive_copy_file(
    file_id: Annotated[str, Field(description="File to copy.")],
    name: Annotated[str | None, Field(description="Name of the copy. Default: 'Copy of <name>'.")] = None,
    parent_id: Annotated[str | None, Field(description="Folder for the copy. Default: same folder.")] = None,
) -> dict[str, Any]:
    """Copy a file (Docs/Sheets/Slides included; folders cannot be copied). Returns the copy's details."""
    body: dict[str, Any] = {}
    if name:
        body["name"] = name
    if parent_id:
        body["parents"] = [parent_id]
    client = get_client()
    f = await client.request("POST", f"{DRIVE}/files/{_seg(file_id)}/copy",
                             params={"fields": FILE_FIELDS, "supportsAllDrives": "true"}, json_body=body)
    return _file(f)


@mcp.tool(name="drive_update_file", title="Drive: rename or move", annotations=CHANGE)
@google_tool
async def drive_update_file(
    file_id: Annotated[str, Field(description="File or folder id.")],
    name: Annotated[str | None, Field(description="New name.")] = None,
    move_to_folder_id: Annotated[str | None, Field(description="Move into this folder (removed from its current folders).")] = None,
    description: Annotated[str | None, Field(description="New description.")] = None,
    starred: Annotated[bool | None, Field(description="Star or unstar.")] = None,
) -> dict[str, Any]:
    """Rename, move, describe or star a file or folder. Returns the updated details."""
    client = get_client()
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if description is not None:
        body["description"] = description
    if starred is not None:
        body["starred"] = starred
    params: dict[str, Any] = {"fields": FILE_FIELDS, "supportsAllDrives": "true"}
    if move_to_folder_id:
        current = await client.get(f"{DRIVE}/files/{_seg(file_id)}", fields="parents", supportsAllDrives="true")
        params["addParents"] = move_to_folder_id
        old = [p for p in current.get("parents", []) if p != move_to_folder_id]
        if old:
            params["removeParents"] = ",".join(old)
    if not body and not move_to_folder_id:
        raise ToolError("nothing to change: give name, move_to_folder_id, description or starred")
    f = await client.request("PATCH", f"{DRIVE}/files/{_seg(file_id)}", params=params, json_body=body)
    return _file(f)


@mcp.tool(name="drive_trash_file", title="Drive: move to trash or restore", annotations=CHANGE)
@google_tool
async def drive_trash_file(
    file_id: Annotated[str, Field(description="File or folder id.")],
    restore: Annotated[bool, Field(description="true restores the file from the trash.")] = False,
) -> dict[str, Any]:
    """Move a file to the trash (recoverable for 30 days), or restore it with restore=true."""
    client = get_client()
    f = await client.request("PATCH", f"{DRIVE}/files/{_seg(file_id)}",
                             params={"fields": FILE_FIELDS, "supportsAllDrives": "true"}, json_body={"trashed": not restore})
    return _file(f)


@mcp.tool(name="drive_delete_file", title="Drive: delete permanently", annotations=DESTROY)
@google_tool
async def drive_delete_file(
    file_id: Annotated[str, Field(description="File or folder id.")],
) -> dict[str, Any]:
    """Delete a file or folder PERMANENTLY, skipping the trash. Cannot be undone; prefer
    drive_trash_file. Returns {"deleted": true, "file_id"}."""
    client = get_client()
    await client.request("DELETE", f"{DRIVE}/files/{_seg(file_id)}", params={"supportsAllDrives": "true"})
    return {"deleted": True, "file_id": file_id}


# ============================================================= drive: sharing
PERMISSION_FIELDS = "id,type,role,emailAddress,domain,displayName,expirationTime"


@mcp.tool(name="drive_list_permissions", title="Drive: who has access", annotations=READ)
@google_tool
async def drive_list_permissions(
    file_id: Annotated[str, Field(description="File or folder id.")],
) -> dict[str, Any]:
    """List who can access a file. Returns {"file_id", "count", "permissions": [{"id",
    "type", "role", "email", "domain", "name"}]}; the id is what drive_unshare_file takes."""
    client = get_client()
    page = await client.get(f"{DRIVE}/files/{_seg(file_id)}/permissions",
                            fields=f"permissions({PERMISSION_FIELDS})", supportsAllDrives="true")
    rows = [{"id": p.get("id"), "type": p.get("type"), "role": p.get("role"), "email": p.get("emailAddress"),
             "domain": p.get("domain"), "name": p.get("displayName"), "expires": p.get("expirationTime")}
            for p in page.get("permissions", [])]
    return {"file_id": file_id, "count": len(rows), "permissions": rows}


@mcp.tool(name="drive_share_file", title="Drive: share a file", annotations=CREATE)
@google_tool
async def drive_share_file(
    file_id: Annotated[str, Field(description="File or folder id.")],
    role: Annotated[Literal["reader", "commenter", "writer", "fileOrganizer", "organizer"], Field(description="Access level. fileOrganizer/organizer exist only on shared drives.")],
    email: Annotated[str | None, Field(description="Person or Google group to share with.")] = None,
    domain: Annotated[str | None, Field(description="Share with everyone in this Workspace domain, e.g. example.com.")] = None,
    anyone_with_link: Annotated[bool, Field(description="Share with anyone who has the link.")] = False,
    notify: Annotated[bool, Field(description="Email the person (only for email shares).")] = True,
    message: Annotated[str | None, Field(description="Text of the notification email.")] = None,
) -> dict[str, Any]:
    """Grant access to a file: to a person or group (email), a whole domain, or anyone
    with the link. Give exactly one of email, domain, anyone_with_link. Returns the new permission."""
    targets = [bool(email), bool(domain), anyone_with_link]
    if sum(targets) != 1:
        raise ToolError("give exactly one of email, domain or anyone_with_link=true")
    body: dict[str, Any] = {"role": role}
    params: dict[str, Any] = {"supportsAllDrives": "true", "fields": PERMISSION_FIELDS}
    if email:
        _check_addresses([email], "email")
        body.update({"type": "user", "emailAddress": email})
        params["sendNotificationEmail"] = str(notify).lower()
        if notify and message:
            params["emailMessage"] = message
    elif domain:
        body.update({"type": "domain", "domain": domain})
    else:
        body["type"] = "anyone"
    client = get_client()
    p = await client.request("POST", f"{DRIVE}/files/{_seg(file_id)}/permissions", params=params, json_body=body)
    return {"id": p.get("id"), "type": p.get("type"), "role": p.get("role"), "email": p.get("emailAddress"), "domain": p.get("domain")}


@mcp.tool(name="drive_unshare_file", title="Drive: remove access", annotations=DESTROY)
@google_tool
async def drive_unshare_file(
    file_id: Annotated[str, Field(description="File or folder id.")],
    permission_id: Annotated[str, Field(description="Permission id from drive_list_permissions.")],
) -> dict[str, Any]:
    """Remove one permission from a file. Returns {"removed": true, "permission_id"}."""
    client = get_client()
    await client.request("DELETE", f"{DRIVE}/files/{_seg(file_id)}/permissions/{_seg(permission_id)}",
                         params={"supportsAllDrives": "true"})
    return {"removed": True, "permission_id": permission_id}


@mcp.tool(name="drive_list_shared_drives", title="Drive: list shared drives", annotations=READ)
@google_tool
async def drive_list_shared_drives(
    page_size: Annotated[int, Field(ge=1, le=100)] = 100,
    page_token: Annotated[str | None, Field(description=PAGE_TOKEN_DESC)] = None,
) -> dict[str, Any]:
    """List the shared drives this account is a member of. A shared drive's id works as a
    folder id in drive_search_files, drive_create_folder and drive_upload_file.
    Returns {"count", "next_page_token", "drives": [{"id", "name"}]}."""
    client = get_client()
    page = await client.get(f"{DRIVE}/drives", pageSize=page_size, pageToken=page_token)
    rows = [{"id": d.get("id"), "name": d.get("name")} for d in page.get("drives", [])]
    return {"count": len(rows), "next_page_token": page.get("nextPageToken"), "drives": rows}


# ============================================================== docs: editing
def _headings(content: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for el in content:
        para = el.get("paragraph")
        if not para:
            continue
        style = para.get("paragraphStyle", {}).get("namedStyleType", "")
        if style == "TITLE" or style.startswith("HEADING_"):
            text = "".join(pe.get("textRun", {}).get("content", "") for pe in para.get("elements", [])).strip()
            level = 0 if style == "TITLE" else int(style.split("_")[1])
            out.append({"level": level, "style": style, "text": text,
                        "start_index": el.get("startIndex"), "end_index": el.get("endIndex")})
    return out


@mcp.tool(name="docs_get_outline", title="Docs: headings and positions", annotations=READ)
@google_tool
async def docs_get_outline(
    document_id: Annotated[str, Field(description="Document id.")],
) -> dict[str, Any]:
    """The document's structure: title and every heading with its level and character
    positions (start_index/end_index), for docs_insert_text and docs_batch_update.
    Returns {"document_id", "title", "end_index", "headings": [...]}."""
    client = get_client()
    doc = await client.get(f"{DOCS}/{_seg(document_id)}")
    content = doc.get("body", {}).get("content", [])
    return {"document_id": doc.get("documentId"), "title": doc.get("title"),
            "end_index": content[-1].get("endIndex") if content else None, "headings": _headings(content)}


@mcp.tool(name="docs_export_text", title="Docs: export as Markdown, HTML or text", annotations=READ)
@google_tool
async def docs_export_text(
    document_id: Annotated[str, Field(description="Document id.")],
    format: Annotated[Literal["markdown", "text"], Field(description="markdown keeps headings, lists, links, tables; text is plain.")] = "markdown",
) -> dict[str, Any]:
    """Return a Google Doc's content as Markdown (or plain text), produced by Google's own
    export. Cut at $GOOGLE_MAX_TEXT_CHARS. Returns {"document_id", "format", "content", "truncated"}."""
    client = get_client()
    mime = "text/markdown" if format == "markdown" else "text/plain"
    resp = await client.request("GET", f"{DRIVE}/files/{_seg(document_id)}/export", params={"mimeType": mime}, raw=True)
    text, cut = _truncate(resp.text, client.config.max_text_chars)
    return {"document_id": document_id, "format": format, "content": text, "truncated": cut}


async def _docs_batch(document_id: str, requests: list[dict[str, Any]]) -> dict[str, Any]:
    return await get_client().request("POST", f"{DOCS}/{_seg(document_id)}:batchUpdate", json_body={"requests": requests})


@mcp.tool(name="docs_replace_text", title="Docs: find and replace", annotations=CHANGE)
@google_tool
async def docs_replace_text(
    document_id: Annotated[str, Field(description="Document id.")],
    find: Annotated[str, Field(min_length=1, description="Text to find.")],
    replace: Annotated[str, Field(description="Replacement text (empty string deletes).")],
    match_case: Annotated[bool, Field(description="Case-sensitive match.")] = True,
) -> dict[str, Any]:
    """Replace every occurrence of a text in a Google Doc. Returns {"document_id", "occurrences_changed"}."""
    r = await _docs_batch(document_id, [{"replaceAllText": {"containsText": {"text": find, "matchCase": match_case}, "replaceText": replace}}])
    changed = (r.get("replies") or [{}])[0].get("replaceAllText", {}).get("occurrencesChanged", 0)
    return {"document_id": document_id, "occurrences_changed": changed}


@mcp.tool(name="docs_insert_text", title="Docs: insert text at a position", annotations=CREATE)
@google_tool
async def docs_insert_text(
    document_id: Annotated[str, Field(description="Document id.")],
    index: Annotated[int, Field(ge=1, description="Character position to insert at (1 = start of the body). Positions come from docs_get_outline.")],
    text: Annotated[str, Field(min_length=1, description="Plain text to insert. Use '\\n' for new paragraphs.")],
) -> dict[str, Any]:
    """Insert plain text at a character position of a Google Doc. Returns {"document_id", "index", "inserted_chars"}."""
    await _docs_batch(document_id, [{"insertText": {"location": {"index": index}, "text": text}}])
    return {"document_id": document_id, "index": index, "inserted_chars": len(text)}


@mcp.tool(name="docs_batch_update", title="Docs: raw batchUpdate", annotations=DESTROY)
@google_tool
async def docs_batch_update(
    document_id: Annotated[str, Field(description="Document id.")],
    requests: Annotated[list[dict[str, Any]], Field(min_length=1, description="Docs API request objects, e.g. [{\"updateParagraphStyle\": {...}}, {\"insertTable\": {...}}, {\"deleteContentRange\": {...}}]. Applied atomically, in order.")],
) -> dict[str, Any]:
    """Apply Docs API batchUpdate requests for anything the other docs_ tools do not
    cover: text and paragraph styles, headings, bullets, tables, images, deletions.
    See https://developers.google.com/docs/api/reference/rest/v1/documents/request.
    Returns {"document_id", "replies"}."""
    r = await _docs_batch(document_id, requests)
    return {"document_id": document_id, "replies": r.get("replies", [])}


# ============================================================ sheets: editing
async def _sheets_batch(spreadsheet_id: str, requests: list[dict[str, Any]]) -> dict[str, Any]:
    return await get_client().request("POST", f"{SHEETS}/{_seg(spreadsheet_id)}:batchUpdate", json_body={"requests": requests})


@mcp.tool(name="sheets_batch_read", title="Sheets: read several ranges", annotations=READ)
@google_tool
async def sheets_batch_read(
    spreadsheet_id: Annotated[str, Field(description=SHEET_ID_DESC)],
    ranges: Annotated[list[str], Field(min_length=1, max_length=100, description="A1 ranges, e.g. ['Summary!A1:C10', 'Hours!A:F'].")],
    render: Annotated[Literal["FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA"], Field(description="FORMATTED_VALUE as shown; UNFORMATTED_VALUE raw; FORMULA the formulas.")] = "FORMATTED_VALUE",
) -> dict[str, Any]:
    """Read several ranges in one call. Returns {"count", "ranges": [{"range", "values"}]}."""
    client = get_client()
    r = await client.request("GET", f"{SHEETS}/{_seg(spreadsheet_id)}/values:batchGet",
                             params={"ranges": ranges, "valueRenderOption": render})
    out = [{"range": v.get("range"), "values": v.get("values", [])} for v in r.get("valueRanges", [])]
    return {"count": len(out), "ranges": out}


@mcp.tool(name="sheets_clear_values", title="Sheets: clear cells", annotations=CHANGE)
@google_tool
async def sheets_clear_values(
    spreadsheet_id: Annotated[str, Field(description=SHEET_ID_DESC)],
    range: Annotated[str, Field(description=RANGE_DESC)],
) -> dict[str, Any]:
    """Clear the values of a range (formatting stays). Returns {"cleared_range"}."""
    client = get_client()
    r = await client.request("POST", f"{SHEETS}/{_seg(spreadsheet_id)}/values/{quote(range, safe='')}:clear", json_body={})
    return {"cleared_range": r.get("clearedRange")}


@mcp.tool(name="sheets_add_sheet", title="Sheets: add a tab", annotations=CREATE)
@google_tool
async def sheets_add_sheet(
    spreadsheet_id: Annotated[str, Field(description=SHEET_ID_DESC)],
    title: Annotated[str, Field(min_length=1, description="Tab name.")],
    rows: Annotated[int, Field(ge=1, description="Row count.")] = 1000,
    columns: Annotated[int, Field(ge=1, description="Column count.")] = 26,
    index: Annotated[int | None, Field(ge=0, description="Position among the tabs (0 = first). Default: last.")] = None,
) -> dict[str, Any]:
    """Add a tab to a spreadsheet. Returns {"sheet_id", "title", "index"}."""
    props: dict[str, Any] = {"title": title, "gridProperties": {"rowCount": rows, "columnCount": columns}}
    if index is not None:
        props["index"] = index
    r = await _sheets_batch(spreadsheet_id, [{"addSheet": {"properties": props}}])
    p = r["replies"][0]["addSheet"]["properties"]
    return {"sheet_id": p.get("sheetId"), "title": p.get("title"), "index": p.get("index")}


@mcp.tool(name="sheets_rename_sheet", title="Sheets: rename a tab", annotations=CHANGE)
@google_tool
async def sheets_rename_sheet(
    spreadsheet_id: Annotated[str, Field(description=SHEET_ID_DESC)],
    sheet_id: Annotated[int, Field(description="Numeric tab id (sheet_id from sheets_get_spreadsheet), not the tab name.")],
    title: Annotated[str, Field(min_length=1, description="New tab name.")],
) -> dict[str, Any]:
    """Rename a tab. Returns {"sheet_id", "title"}."""
    await _sheets_batch(spreadsheet_id, [{"updateSheetProperties": {"properties": {"sheetId": sheet_id, "title": title}, "fields": "title"}}])
    return {"sheet_id": sheet_id, "title": title}


@mcp.tool(name="sheets_delete_sheet", title="Sheets: delete a tab", annotations=DESTROY)
@google_tool
async def sheets_delete_sheet(
    spreadsheet_id: Annotated[str, Field(description=SHEET_ID_DESC)],
    sheet_id: Annotated[int, Field(description="Numeric tab id from sheets_get_spreadsheet.")],
) -> dict[str, Any]:
    """Delete a tab and everything on it (recoverable only through version history).
    Returns {"deleted": true, "sheet_id"}."""
    await _sheets_batch(spreadsheet_id, [{"deleteSheet": {"sheetId": sheet_id}}])
    return {"deleted": True, "sheet_id": sheet_id}


@mcp.tool(name="sheets_batch_update", title="Sheets: raw batchUpdate", annotations=DESTROY)
@google_tool
async def sheets_batch_update(
    spreadsheet_id: Annotated[str, Field(description=SHEET_ID_DESC)],
    requests: Annotated[list[dict[str, Any]], Field(min_length=1, description="Sheets API request objects, e.g. [{\"repeatCell\": {...}}, {\"sortRange\": {...}}, {\"addChart\": {...}}]. Applied atomically, in order.")],
) -> dict[str, Any]:
    """Apply Sheets API batchUpdate requests for anything the other sheets_ tools do not
    cover: formatting, borders, merges, sorting, filters, conditional formats, charts,
    protected ranges, row/column insert and delete.
    See https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request.
    Returns {"spreadsheet_id", "replies"}."""
    r = await _sheets_batch(spreadsheet_id, requests)
    return {"spreadsheet_id": spreadsheet_id, "replies": r.get("replies", [])}


# ====================================================================== slides
SLIDES = "https://slides.googleapis.com/v1/presentations"
PRES_ID_DESC = "Presentation id (from the URL /presentation/d/<id>/)."


def _shape_text(element: dict[str, Any]) -> str:
    if "shape" in element:
        return "".join(t.get("textRun", {}).get("content", "") for t in element["shape"].get("text", {}).get("textElements", []))
    if "table" in element:
        rows = []
        for row in element["table"].get("tableRows", []):
            cells = ["".join(t.get("textRun", {}).get("content", "") for t in c.get("text", {}).get("textElements", [])).strip()
                     for c in row.get("tableCells", [])]
            rows.append(" | ".join(cells))
        return "\n".join(rows)
    if "elementGroup" in element:
        return "\n".join(_shape_text(c) for c in element["elementGroup"].get("children", []))
    return ""


def _element(element: dict[str, Any]) -> dict[str, Any]:
    kind = next((k for k in ("shape", "table", "image", "video", "line", "sheetsChart", "elementGroup", "wordArt") if k in element), "other")
    out: dict[str, Any] = {"object_id": element.get("objectId"), "kind": kind}
    if kind == "shape":
        ph = element["shape"].get("placeholder")
        if ph:
            out["placeholder"] = ph.get("type")
    text = _shape_text(element).strip()
    if text:
        out["text"] = text
    return out


def _notes(slide: dict[str, Any]) -> str:
    notes_page = slide.get("slideProperties", {}).get("notesPage", {})
    notes_id = notes_page.get("notesProperties", {}).get("speakerNotesObjectId")
    for el in notes_page.get("pageElements", []):
        if el.get("objectId") == notes_id:
            return _shape_text(el).strip()
    return ""


@mcp.tool(name="slides_get_presentation", title="Slides: read a presentation", annotations=READ)
@google_tool
async def slides_get_presentation(
    presentation_id: Annotated[str, Field(description=PRES_ID_DESC)],
) -> dict[str, Any]:
    """Read a presentation slide by slide: each slide's id, its elements (object id,
    kind, placeholder type, text) and speaker notes. Object ids are what the other
    slides_ tools take. Returns {"presentation_id", "title", "slide_count", "slides": [...]}."""
    client = get_client()
    p = await client.get(f"{SLIDES}/{_seg(presentation_id)}")
    slides = []
    budget = client.config.max_text_chars
    for i, s in enumerate(p.get("slides", [])):
        elements = [_element(e) for e in s.get("pageElements", [])]
        slides.append({"index": i, "slide_id": s.get("objectId"), "elements": elements, "notes": _notes(s)})
    text = json.dumps(slides, ensure_ascii=False)
    truncated = len(text) > budget
    if truncated:
        while slides and len(json.dumps(slides, ensure_ascii=False)) > budget:
            slides.pop()
    return {"presentation_id": p.get("presentationId"), "title": p.get("title"),
            "slide_count": len(p.get("slides", [])), "slides": slides, "truncated": truncated,
            "link": f"https://docs.google.com/presentation/d/{p.get('presentationId')}/edit"}


@mcp.tool(name="slides_create_presentation", title="Slides: create a presentation", annotations=CREATE)
@google_tool
async def slides_create_presentation(
    title: Annotated[str, Field(min_length=1, description="Presentation title.")],
) -> dict[str, Any]:
    """Create an empty presentation (one title slide) in My Drive.
    Returns {"presentation_id", "title", "first_slide_id", "link"}."""
    client = get_client()
    p = await client.request("POST", SLIDES, json_body={"title": title})
    pid = p.get("presentationId")
    first = (p.get("slides") or [{}])[0].get("objectId")
    return {"presentation_id": pid, "title": p.get("title"), "first_slide_id": first,
            "link": f"https://docs.google.com/presentation/d/{pid}/edit"}


async def _slides_batch(presentation_id: str, requests: list[dict[str, Any]]) -> dict[str, Any]:
    return await get_client().request("POST", f"{SLIDES}/{_seg(presentation_id)}:batchUpdate", json_body={"requests": requests})


def _new_id(prefix: str) -> str:
    # Slides object ids: 5-50 chars, start with [A-Za-z0-9_], then [A-Za-z0-9_-:].
    return f"{prefix}_{uuid.uuid4().hex[:20]}"


LAYOUTS = Literal["BLANK", "TITLE", "TITLE_AND_BODY", "TITLE_AND_TWO_COLUMNS", "TITLE_ONLY", "SECTION_HEADER",
                  "SECTION_TITLE_AND_DESCRIPTION", "ONE_COLUMN_TEXT", "MAIN_POINT", "BIG_NUMBER", "CAPTION_ONLY"]


@mcp.tool(name="slides_add_slide", title="Slides: add a slide", annotations=CREATE)
@google_tool
async def slides_add_slide(
    presentation_id: Annotated[str, Field(description=PRES_ID_DESC)],
    layout: Annotated[LAYOUTS, Field(description="Predefined layout of the presentation's theme.")] = "TITLE_AND_BODY",
    title: Annotated[str | None, Field(description="Text for the title placeholder (CENTERED_TITLE on layout TITLE, TITLE otherwise).")] = None,
    body: Annotated[str | None, Field(description="Text for the body placeholder (SUBTITLE on layout TITLE, BODY otherwise). Layouts without one reject this.")] = None,
    index: Annotated[int | None, Field(ge=0, description="Position (0 = first). Default: last.")] = None,
) -> dict[str, Any]:
    """Add a slide with a predefined layout, optionally filling its title and body.
    Returns {"slide_id", "title_id", "body_id"} (ids of the filled placeholders)."""
    slide_id = _new_id("slide")
    create: dict[str, Any] = {"objectId": slide_id, "slideLayoutReference": {"predefinedLayout": layout}}
    if index is not None:
        create["insertionIndex"] = index
    title_type, body_type = ("CENTERED_TITLE", "SUBTITLE") if layout == "TITLE" else ("TITLE", "BODY")
    mappings, inserts = [], []
    ids: dict[str, str | None] = {"title_id": None, "body_id": None}
    for key, ph_type, text in (("title_id", title_type, title), ("body_id", body_type, body)):
        if text:
            oid = _new_id(key.split("_")[0])
            ids[key] = oid
            mappings.append({"layoutPlaceholder": {"type": ph_type, "index": 0}, "objectId": oid})
            inserts.append({"insertText": {"objectId": oid, "text": text}})
    if mappings:
        create["placeholderIdMappings"] = mappings
    await _slides_batch(presentation_id, [{"createSlide": create}, *inserts])
    return {"slide_id": slide_id, **ids}


@mcp.tool(name="slides_duplicate_slide", title="Slides: duplicate a slide", annotations=CREATE)
@google_tool
async def slides_duplicate_slide(
    presentation_id: Annotated[str, Field(description=PRES_ID_DESC)],
    slide_id: Annotated[str, Field(description="Slide id from slides_get_presentation.")],
) -> dict[str, Any]:
    """Duplicate a slide; the copy goes right after the original. Returns {"new_slide_id"}."""
    r = await _slides_batch(presentation_id, [{"duplicateObject": {"objectId": slide_id}}])
    return {"new_slide_id": r["replies"][0]["duplicateObject"]["objectId"]}


@mcp.tool(name="slides_delete_object", title="Slides: delete a slide or element", annotations=DESTROY)
@google_tool
async def slides_delete_object(
    presentation_id: Annotated[str, Field(description=PRES_ID_DESC)],
    object_id: Annotated[str, Field(description="Id of a slide, or of an element on a slide, from slides_get_presentation.")],
) -> dict[str, Any]:
    """Delete a slide, or one element (shape, image, table) on a slide.
    Returns {"deleted": true, "object_id"}."""
    await _slides_batch(presentation_id, [{"deleteObject": {"objectId": object_id}}])
    return {"deleted": True, "object_id": object_id}


@mcp.tool(name="slides_replace_text", title="Slides: find and replace", annotations=CHANGE)
@google_tool
async def slides_replace_text(
    presentation_id: Annotated[str, Field(description=PRES_ID_DESC)],
    find: Annotated[str, Field(min_length=1, description="Text to find, e.g. a template marker like {{client}}.")],
    replace: Annotated[str, Field(description="Replacement text.")],
    match_case: Annotated[bool, Field(description="Case-sensitive match.")] = True,
    slide_ids: Annotated[list[str] | None, Field(description="Only these slides. Default: all slides.")] = None,
) -> dict[str, Any]:
    """Replace every occurrence of a text across the presentation (or the given slides).
    Returns {"occurrences_changed"}."""
    req: dict[str, Any] = {"containsText": {"text": find, "matchCase": match_case}, "replaceText": replace}
    if slide_ids:
        req["pageObjectIds"] = slide_ids
    r = await _slides_batch(presentation_id, [{"replaceAllText": req}])
    return {"occurrences_changed": (r.get("replies") or [{}])[0].get("replaceAllText", {}).get("occurrencesChanged", 0)}


@mcp.tool(name="slides_set_text", title="Slides: write text into a shape", annotations=CHANGE)
@google_tool
async def slides_set_text(
    presentation_id: Annotated[str, Field(description=PRES_ID_DESC)],
    object_id: Annotated[str, Field(description="Shape or placeholder id from slides_get_presentation.")],
    text: Annotated[str, Field(min_length=1, description="Text to write.")],
    replace_existing: Annotated[bool, Field(description="true replaces the shape's whole text; false appends at the end.")] = True,
) -> dict[str, Any]:
    """Put text into a shape or placeholder: replace its whole text (default) or append.
    Returns {"object_id", "chars"}."""
    client = get_client()
    p = await client.get(f"{SLIDES}/{_seg(presentation_id)}")
    current = None
    for s in p.get("slides", []):
        for el in s.get("pageElements", []):
            if el.get("objectId") == object_id:
                current = _shape_text(el)
    if current is None:
        raise ToolError(f"no element {object_id!r} on any slide of the presentation")
    requests: list[dict[str, Any]] = []
    if replace_existing:
        if current:  # deleteText fails on a shape that has no text at all
            requests.append({"deleteText": {"objectId": object_id, "textRange": {"type": "ALL"}}})
        requests.append({"insertText": {"objectId": object_id, "text": text, "insertionIndex": 0}})
    else:
        # A shape's text ends with a newline Google keeps; insert before it.
        index = len(current) - 1 if current.endswith("\n") else len(current)
        requests.append({"insertText": {"objectId": object_id, "text": text, "insertionIndex": max(index, 0)}})
    await _slides_batch(presentation_id, requests)
    return {"object_id": object_id, "chars": len(text)}


@mcp.tool(name="slides_get_thumbnail", title="Slides: slide image", annotations=READ)
@google_tool
async def slides_get_thumbnail(
    presentation_id: Annotated[str, Field(description=PRES_ID_DESC)],
    slide_id: Annotated[str, Field(description="Slide id from slides_get_presentation.")],
    size: Annotated[Literal["SMALL", "MEDIUM", "LARGE"], Field(description="SMALL 200px, MEDIUM 800px, LARGE 1600px wide.")] = "LARGE",
    save_path: Annotated[str | None, Field(description="Save the PNG here (file or directory). Omit to only get the temporary image URL.")] = None,
    overwrite: Annotated[bool, Field(description="Replace an existing local file.")] = False,
) -> dict[str, Any]:
    """Render a slide to PNG. Returns {"slide_id", "width", "height", "content_url"} (the URL
    works for about 30 minutes without sign-in), plus "saved_to" and "bytes" when save_path is given."""
    client = get_client()
    t = await client.request("GET", f"{SLIDES}/{_seg(presentation_id)}/pages/{_seg(slide_id)}/thumbnail",
                             params={"thumbnailProperties.mimeType": "PNG", "thumbnailProperties.thumbnailSize": size})
    out: dict[str, Any] = {"slide_id": slide_id, "width": t.get("width"), "height": t.get("height"), "content_url": t.get("contentUrl")}
    if save_path is not None:
        target = _target_path(save_path, f"{slide_id}.png", overwrite)
        out.update(_write(target, await client.fetch_public(t["contentUrl"])))
    return out


@mcp.tool(name="slides_batch_update", title="Slides: raw batchUpdate", annotations=DESTROY)
@google_tool
async def slides_batch_update(
    presentation_id: Annotated[str, Field(description=PRES_ID_DESC)],
    requests: Annotated[list[dict[str, Any]], Field(min_length=1, description="Slides API request objects, e.g. [{\"createShape\": {...}}, {\"createImage\": {...}}, {\"updateTextStyle\": {...}}]. Applied atomically, in order.")],
) -> dict[str, Any]:
    """Apply Slides API batchUpdate requests for anything the other slides_ tools do not
    cover: shapes, images, tables, text and shape styles, moving slides, speaker notes.
    See https://developers.google.com/slides/api/reference/rest/v1/presentations/request.
    Returns {"presentation_id", "replies"}."""
    r = await _slides_batch(presentation_id, requests)
    return {"presentation_id": presentation_id, "replies": r.get("replies", [])}


# ======================================================================== chat
def _space_name(space: str) -> str:
    space = space.strip()
    if not space:
        raise ToolError("space must not be empty")
    name = space if space.startswith("spaces/") else f"spaces/{space}"
    if not re.fullmatch(r"spaces/[A-Za-z0-9_-]+", name):
        raise ToolError(f"invalid space {space!r}: expected 'spaces/AAAA...' from chat_list_spaces")
    return name


@mcp.tool(name="chat_list_spaces", title="Chat: list spaces", annotations=READ)
@google_tool
async def chat_list_spaces(
    space_type: Annotated[Literal["all", "SPACE", "GROUP_CHAT", "DIRECT_MESSAGE"], Field(description="SPACE = named spaces; GROUP_CHAT = unnamed group chats; DIRECT_MESSAGE = 1:1 chats.")] = "all",
    page_size: Annotated[int, Field(ge=1, le=1000)] = 200,
    page_token: Annotated[str | None, Field(description=PAGE_TOKEN_DESC)] = None,
) -> dict[str, Any]:
    """List Google Chat spaces this account belongs to.
    Returns {"count", "next_page_token", "spaces": [{"name", "display_name", "type", "last_active"}]}."""
    client = get_client()
    flt = None if space_type == "all" else f'spaceType = "{space_type}"'
    page = await client.get(f"{CHAT}/spaces", pageSize=page_size, pageToken=page_token, filter=flt)
    rows = [{"name": s.get("name"), "display_name": s.get("displayName"), "type": s.get("spaceType"),
             "last_active": s.get("lastActiveTime")} for s in page.get("spaces", [])]
    return {"count": len(rows), "next_page_token": page.get("nextPageToken"), "spaces": rows}


@mcp.tool(name="chat_list_messages", title="Chat: list messages", annotations=READ)
@google_tool
async def chat_list_messages(
    space: Annotated[str, Field(description="Space name 'spaces/AAAA...' from chat_list_spaces.")],
    after: Annotated[str | None, Field(description="Only messages created at/after this: YYYY-MM-DD (midnight in time_zone) or RFC 3339.")] = None,
    before: Annotated[str | None, Field(description="Only messages created before this: YYYY-MM-DD (inclusive whole day, in time_zone) or RFC 3339 (exclusive).")] = None,
    time_zone: Annotated[str, Field(description="IANA zone for bare dates, e.g. Asia/Jerusalem.")] = "UTC",
    newest_first: Annotated[bool, Field(description="Order newest first instead of oldest first.")] = False,
    page_size: Annotated[int, Field(ge=1, le=1000)] = 100,
    page_token: Annotated[str | None, Field(description=PAGE_TOKEN_DESC)] = None,
) -> dict[str, Any]:
    """List messages of a Chat space in a time window.

    Returns {"space", "count", "next_page_token", "messages": [{"name", "created", "sender",
    "sender_type", "text", "thread"}]}. sender is 'users/<id>'; compare with the id that
    google_whoami's account has in Chat. Bot messages are included and marked sender_type BOT.
    """
    client = get_client()
    name = _space_name(space)
    terms = []
    if after:
        terms.append(f'createTime >= "{_day_start(after, time_zone)}"')
    if before:
        terms.append(f'createTime < "{_day_start(_next_day(before), time_zone)}"')
    page = await client.get(
        f"{CHAT}/{name}/messages", pageSize=page_size, pageToken=page_token,
        filter=" AND ".join(terms) or None, orderBy="createTime desc" if newest_first else "createTime asc",
    )
    limit = client.config.max_text_chars
    rows = []
    for m in page.get("messages", []):
        text, _ = _truncate(m.get("text") or m.get("argumentText") or "", limit)
        rows.append({"name": m.get("name"), "created": m.get("createTime"),
                     "sender": m.get("sender", {}).get("name"), "sender_type": m.get("sender", {}).get("type"),
                     "text": text, "thread": m.get("thread", {}).get("name")})
    return {"space": name, "count": len(rows), "next_page_token": page.get("nextPageToken"), "messages": rows}


@mcp.tool(name="chat_send_message", title="Chat: send a message", annotations=DESTROY)
@google_tool
async def chat_send_message(
    space: Annotated[str, Field(description="Space name 'spaces/AAAA...'.")],
    text: Annotated[str, Field(min_length=1, description="Message text (Chat formatting: *bold*, _italic_, `code`).")],
    thread: Annotated[str | None, Field(description="Thread name 'spaces/…/threads/…' to reply in; omit to start a new thread.")] = None,
) -> dict[str, Any]:
    """Post a message to a Chat space as this account. Visible to the space's members
    immediately. Returns {"name", "created", "thread"}."""
    client = get_client()
    name = _space_name(space)
    body: dict[str, Any] = {"text": text}
    params: dict[str, Any] = {}
    if thread:
        body["thread"] = {"name": thread}
        params["messageReplyOption"] = "REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD"
    m = await client.request("POST", f"{CHAT}/{name}/messages", params=params, json_body=body)
    return {"name": m.get("name"), "created": m.get("createTime"), "thread": m.get("thread", {}).get("name")}


# -------------------------------------------------------------------- entry
async def _check() -> int:
    try:
        config = load_config()
    except ConfigError as exc:
        print(f"config error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"connection": config.describe()}, indent=2))
    client = GoogleClient(config)
    try:
        set_client(client)
        try:
            info = await google_whoami()
        except ToolError as exc:
            print(f"sign-in FAILED: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(info, indent=2, ensure_ascii=False))
        return 0
    finally:
        set_client(None)
        await client.aclose()


def main() -> None:
    logging.basicConfig(level=logging.WARNING, stream=sys.stderr, format="%(name)s %(levelname)s %(message)s")
    args = sys.argv[1:]
    if args == ["check"]:
        sys.exit(asyncio.run(_check()))
    if args and args[0] == "auth":
        from google_workspace_mcp.auth import cli as auth_cli

        sys.exit(auth_cli(args[1:]))
    if args in (["--version"], ["-V"]):
        print(f"google-workspace-mcp {__version__}")
        return
    if args:
        print("usage: google-workspace-mcp [check | auth --out FILE ... | --version]   (no arguments = stdio MCP server)", file=sys.stderr)
        sys.exit(2)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
