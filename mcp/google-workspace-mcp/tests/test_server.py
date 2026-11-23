"""Tool behaviour through the real MCP layer, against a fake Google."""

from __future__ import annotations

import base64
import email
from urllib.parse import parse_qs

import httpx
import pytest

from tests.conftest import ACCESS_TOKEN, CLIENT_SECRET, REFRESH_TOKEN, FakeGoogle, body, form, google_error

pytestmark = pytest.mark.anyio

GMAIL = "https://gmail.googleapis.com/gmail/v1/users/me"
CAL = "https://www.googleapis.com/calendar/v3"
DRIVE = "https://www.googleapis.com/drive/v3"


def text(result) -> str:
    return "\n".join(block.text for block in result.content if getattr(block, "type", "") == "text")


def query(request: httpx.Request) -> dict[str, list[str]]:
    return parse_qs(request.url.query.decode())


def b64(s: str) -> str:
    return base64.urlsafe_b64encode(s.encode()).decode().rstrip("=")


async def test_tools_are_registered_with_annotations(client):
    tools = {t.name: t for t in (await client.list_tools()).tools}
    assert sorted(tools) == sorted([
        "google_whoami", "google_api_request",
        "gmail_search_messages", "gmail_get_message", "gmail_get_thread", "gmail_list_labels",
        "gmail_download_attachment", "gmail_modify_labels", "gmail_create_draft", "gmail_send_message",
        "calendar_list_calendars", "calendar_list_events", "calendar_get_event",
        "calendar_create_event", "calendar_update_event", "calendar_delete_event",
        "drive_search_files", "drive_get_file", "drive_read_file", "drive_create_folder",
        "drive_upload_file", "drive_download_file", "drive_export_file", "drive_copy_file",
        "drive_update_file", "drive_trash_file", "drive_delete_file", "drive_list_permissions",
        "drive_share_file", "drive_unshare_file", "drive_list_shared_drives",
        "docs_get_document", "docs_get_outline", "docs_export_text", "docs_create_document",
        "docs_append_text", "docs_insert_text", "docs_replace_text", "docs_batch_update",
        "sheets_get_spreadsheet", "sheets_read_values", "sheets_batch_read", "sheets_update_values",
        "sheets_append_values", "sheets_clear_values", "sheets_create_spreadsheet",
        "sheets_add_sheet", "sheets_rename_sheet", "sheets_delete_sheet", "sheets_batch_update",
        "slides_get_presentation", "slides_create_presentation", "slides_add_slide",
        "slides_duplicate_slide", "slides_delete_object", "slides_replace_text", "slides_set_text",
        "slides_get_thumbnail", "slides_batch_update",
        "chat_list_spaces", "chat_list_messages", "chat_send_message",
    ])
    assert tools["gmail_search_messages"].annotations.read_only_hint is True
    assert tools["gmail_send_message"].annotations.destructive_hint is True
    assert tools["calendar_delete_event"].annotations.read_only_hint is False
    assert "\n    " not in tools["google_whoami"].description


async def test_whoami_mints_token_once_and_hides_secrets(client, google: FakeGoogle):
    google.on("GET", "https://oauth2.googleapis.com/tokeninfo",
              {"scope": "https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/calendar openid https://www.googleapis.com/auth/userinfo.email", "email": "d@x.com"})
    google.on("GET", "https://openidconnect.googleapis.com/v1/userinfo", {"email": "d@x.com", "name": "David"})

    result = await client.call_tool("google_whoami", {})

    assert result.is_error is False
    sc = result.structured_content
    assert sc["email"] == "d@x.com" and sc["name"] == "David"
    assert sc["services"]["gmail"] and sc["services"]["calendar"] and not sc["services"]["chat"]
    assert sc["services"]["slides"] is False
    for secret in (REFRESH_TOKEN, CLIENT_SECRET, ACCESS_TOKEN):
        assert secret not in text(result)
    token_req = google.last("POST", "https://oauth2.googleapis.com/token")
    assert form(token_req) == {"client_id": "123-test.apps.googleusercontent.com", "client_secret": CLIENT_SECRET,
                               "refresh_token": REFRESH_TOKEN, "grant_type": "refresh_token"}
    userinfo = google.last("GET", "https://openidconnect.googleapis.com/v1/userinfo")
    assert userinfo.headers["Authorization"].startswith(f"Bearer {ACCESS_TOKEN}")


async def test_dead_refresh_token_says_relogin(client, google: FakeGoogle):
    google.token_response = lambda: httpx.Response(400, json={"error": "invalid_grant", "error_description": "Token has been expired or revoked."})
    result = await client.call_tool("gmail_list_labels", {})
    assert result.is_error is True
    msg = text(result)
    assert "invalid_grant" in msg and "re-login" in msg and "7 days" in msg


async def test_401_triggers_one_fresh_token(client, google: FakeGoogle):
    calls = {"n": 0}

    def labels(request):
        calls["n"] += 1
        if calls["n"] == 1:
            return google_error(401, "Invalid Credentials", "authError")
        return {"labels": [{"id": "INBOX", "name": "INBOX", "type": "system"}]}

    google.on("GET", f"{GMAIL}/labels", labels)
    result = await client.call_tool("gmail_list_labels", {})
    assert result.is_error is False and result.structured_content["count"] == 1
    assert google.token_calls == 2


async def test_missing_scope_names_granted_scopes(client, google: FakeGoogle):
    google.on("GET", "https://chat.googleapis.com/v1/spaces",
              google_error(403, "Request had insufficient authentication scopes.", "insufficientPermissions", "ACCESS_TOKEN_SCOPE_INSUFFICIENT"))
    result = await client.call_tool("chat_list_spaces", {})
    assert result.is_error is True
    assert "lacks the OAuth scope" in text(result) and "gmail.modify" in text(result)


async def test_disabled_api_says_enable_it(client, google: FakeGoogle):
    google.on("GET", f"{DRIVE}/files/abc",
              google_error(403, "Google Drive API has not been used in project 1 before or it is disabled.", "accessNotConfigured", "SERVICE_DISABLED"))
    result = await client.call_tool("drive_get_file", {"file_id": "abc"})
    assert result.is_error is True and "gcloud services enable" in text(result)


async def test_export_size_limit_is_not_reported_as_access_denied(client, google: FakeGoogle):
    google.on("GET", f"{DRIVE}/files/big/export", google_error(403, "This file is too large to be exported.", "exportSizeLimitExceeded"))
    result = await client.call_tool("docs_export_text", {"document_id": "big"})
    assert result.is_error is True
    assert "10 MB" in text(result) and "lacks access" not in text(result)


async def test_gmail_search_fetches_metadata(client, google: FakeGoogle):
    google.on("GET", f"{GMAIL}/messages", {"messages": [{"id": "m1"}, {"id": "m2"}], "resultSizeEstimate": 2, "nextPageToken": "p2"})

    def meta(request):
        mid = request.url.path.rsplit("/", 1)[-1]
        return {"id": mid, "threadId": "t" + mid, "snippet": "hi &amp; bye", "labelIds": ["INBOX"],
                "payload": {"headers": [{"name": "From", "value": "a@x.com"}, {"name": "Subject", "value": f"S {mid}"}]}}

    google.on("GET", f"{GMAIL}/messages/m1", meta)
    google.on("GET", f"{GMAIL}/messages/m2", meta)
    result = await client.call_tool("gmail_search_messages", {"query": "from:a@x.com", "max_results": 2})
    sc = result.structured_content
    assert sc["count"] == 2 and sc["next_page_token"] == "p2"
    assert sc["messages"][0] == {"id": "m1", "thread_id": "tm1", "date": None, "from": "a@x.com", "to": None,
                                 "subject": "S m1", "snippet": "hi & bye", "labels": ["INBOX"]}
    q = query(google.last("GET", f"{GMAIL}/messages"))
    assert q["q"] == ["from:a@x.com"] and q["maxResults"] == ["2"]
    mq = query(google.last("GET", f"{GMAIL}/messages/m2"))
    assert mq["format"] == ["metadata"] and set(mq["metadataHeaders"]) == {"From", "To", "Subject", "Date"}


async def test_gmail_get_message_prefers_plain_and_lists_attachments(client, google: FakeGoogle):
    google.on("GET", f"{GMAIL}/messages/m1", {"id": "m1", "threadId": "t1", "payload": {
        "mimeType": "multipart/mixed", "headers": [{"name": "Subject", "value": "Invoice"}],
        "parts": [
            {"mimeType": "multipart/alternative", "parts": [
                {"mimeType": "text/plain", "body": {"data": b64("Hello plain")}},
                {"mimeType": "text/html", "body": {"data": b64("<p>Hello html</p>")}},
            ]},
            {"mimeType": "application/pdf", "filename": "inv.pdf", "body": {"attachmentId": "att1", "size": 1234}},
        ]}})
    sc = (await client.call_tool("gmail_get_message", {"message_id": "m1"})).structured_content
    assert sc["body"] == "Hello plain" and sc["body_truncated"] is False
    assert sc["attachments"] == [{"filename": "inv.pdf", "mime_type": "application/pdf", "size": 1234, "attachment_id": "att1"}]


async def test_gmail_html_only_body_is_converted_and_truncated(client, google: FakeGoogle):
    html = "<style>x{}</style><p>Line one</p><p>" + "y" * 2000 + "</p>"
    google.on("GET", f"{GMAIL}/messages/m1", {"id": "m1", "payload": {"mimeType": "text/html", "body": {"data": b64(html)}}})
    sc = (await client.call_tool("gmail_get_message", {"message_id": "m1"})).structured_content
    assert sc["body"].startswith("Line one\n") and "x{}" not in sc["body"]
    assert sc["body_truncated"] is True and len(sc["body"]) == 1000


async def test_reply_draft_threads_and_sets_headers(client, google: FakeGoogle):
    google.on("GET", f"{GMAIL}/messages/orig", {"id": "orig", "threadId": "T9", "payload": {"headers": [
        {"name": "Message-ID", "value": "<abc@mail>"}, {"name": "Subject", "value": "Budget"}]}})
    google.on("POST", f"{GMAIL}/drafts", {"id": "d1", "message": {"id": "m9", "threadId": "T9"}})
    result = await client.call_tool("gmail_create_draft", {"to": ["Bob <bob@x.com>"], "subject": "", "body": "Agreed.",
                                                           "reply_to_message_id": "orig"})
    assert result.structured_content == {"draft_id": "d1", "message_id": "m9", "thread_id": "T9"}
    sent = body(google.last("POST", f"{GMAIL}/drafts"))
    assert sent["message"]["threadId"] == "T9"
    mime = email.message_from_bytes(base64.urlsafe_b64decode(sent["message"]["raw"]))
    assert mime["Subject"] == "Re: Budget" and mime["In-Reply-To"] == "<abc@mail>" and mime["To"] == "Bob <bob@x.com>"
    assert mime.get_payload(decode=True).decode().strip() == "Agreed."


async def test_send_rejects_bad_address(client):
    result = await client.call_tool("gmail_send_message", {"to": ["not-an-address"], "subject": "s", "body": "b"})
    assert result.is_error is True and "invalid address" in text(result)


async def test_calendar_list_events_bare_dates_use_calendar_zone(client, google: FakeGoogle):
    google.on("GET", f"{CAL}/calendars/primary", {"id": "d@x.com", "timeZone": "Asia/Jerusalem"})
    google.on("GET", f"{CAL}/calendars/primary/events", {"items": [
        {"id": "e1", "summary": "Standup", "start": {"dateTime": "2026-10-12T09:00:00+03:00"}, "end": {"dateTime": "2026-10-12T09:15:00+03:00"},
         "attendees": [{"email": "d@x.com", "self": True, "responseStatus": "accepted"}], "organizer": {"email": "boss@x.com"}},
        {"id": "e2", "summary": "Skipped", "start": {"date": "2026-10-12"}, "end": {"date": "2026-10-13"},
         "attendees": [{"email": "d@x.com", "self": True, "responseStatus": "declined"}]},
    ]})
    result = await client.call_tool("calendar_list_events", {"time_min": "2026-10-12", "time_max": "2026-10-12", "include_declined": False})
    sc = result.structured_content
    assert sc["time_min"] == "2026-10-12T00:00:00+03:00" and sc["time_max"] == "2026-10-13T00:00:00+03:00"
    assert [e["id"] for e in sc["events"]] == ["e1"] and sc["events"][0]["my_response"] == "accepted"
    q = query(google.last("GET", f"{CAL}/calendars/primary/events"))
    assert q["singleEvents"] == ["true"] and q["orderBy"] == ["startTime"] and q["timeZone"] == ["Asia/Jerusalem"]


async def test_calendar_create_requires_offset_or_zone(client, google: FakeGoogle):
    bad = await client.call_tool("calendar_create_event", {"summary": "x", "start": "2026-10-13T10:00:00", "end": "2026-10-13T11:00:00"})
    assert bad.is_error is True and "no UTC offset" in text(bad)

    google.on("POST", f"{CAL}/calendars/primary/events", lambda r: {"id": "new", **body(r)})
    ok = await client.call_tool("calendar_create_event", {"summary": "Review", "start": "2026-10-13T10:00:00", "end": "2026-10-13T11:00:00",
                                                          "time_zone": "Asia/Jerusalem", "attendees": ["a@x.com"]})
    assert ok.is_error is False and ok.structured_content["id"] == "new"
    sent = body(google.last("POST", f"{CAL}/calendars/primary/events"))
    assert sent["start"] == {"dateTime": "2026-10-13T10:00:00", "timeZone": "Asia/Jerusalem"}
    assert sent["attendees"] == [{"email": "a@x.com"}]


async def test_calendar_rsvp_patches_only_own_attendance(client, google: FakeGoogle):
    url = f"{CAL}/calendars/primary/events/e1"
    google.on("GET", url, {"id": "e1", "attendees": [{"email": "boss@x.com", "responseStatus": "accepted"},
                                                      {"email": "d@x.com", "self": True, "responseStatus": "needsAction"}]})
    google.on("PATCH", url, lambda r: {"id": "e1", **body(r)})
    result = await client.call_tool("calendar_update_event", {"event_id": "e1", "response_status": "declined"})
    assert result.is_error is False
    patch = body(google.last("PATCH", url))
    assert patch == {"attendees": [{"email": "boss@x.com", "responseStatus": "accepted"},
                                   {"email": "d@x.com", "self": True, "responseStatus": "declined"}]}


async def test_drive_search_builds_query(client, google: FakeGoogle):
    google.on("GET", f"{DRIVE}/files", {"files": [{"id": "f1", "name": "Q3 plan", "mimeType": "application/vnd.google-apps.document", "size": "10"}]})
    result = await client.call_tool("drive_search_files", {"name_contains": "Bob's plan", "mime_type": "application/pdf"})
    assert result.structured_content["files"][0]["size"] == 10
    q = query(google.last("GET", f"{DRIVE}/files"))["q"][0]
    assert q == "name contains 'Bob\\'s plan' and mimeType = 'application/pdf' and trashed = false"


async def test_drive_read_exports_docs_and_skips_binaries(client, google: FakeGoogle):
    google.on("GET", f"{DRIVE}/files/doc1", {"id": "doc1", "name": "Plan", "mimeType": "application/vnd.google-apps.document"})
    google.on("GET", f"{DRIVE}/files/doc1/export", lambda r: httpx.Response(200, text="Plan text"))
    sc = (await client.call_tool("drive_read_file", {"file_id": "doc1"})).structured_content
    assert sc["content"] == "Plan text" and sc["content_type"] == "text/plain"
    assert query(google.last("GET", f"{DRIVE}/files/doc1/export"))["mimeType"] == ["text/plain"]

    google.on("GET", f"{DRIVE}/files/pdf1", {"id": "pdf1", "name": "x.pdf", "mimeType": "application/pdf"})
    sc = (await client.call_tool("drive_read_file", {"file_id": "pdf1"})).structured_content
    assert sc["content"] is None and "binary" in sc["note"]


async def test_docs_get_document_flattens_paragraphs_and_tables(client, google: FakeGoogle):
    google.on("GET", "https://docs.googleapis.com/v1/documents/D1", {"documentId": "D1", "title": "Spec", "revisionId": "r", "body": {"content": [
        {"endIndex": 1, "sectionBreak": {}},
        {"endIndex": 7, "paragraph": {"elements": [{"textRun": {"content": "Intro\n"}}]}},
        {"endIndex": 20, "table": {"tableRows": [{"tableCells": [
            {"content": [{"paragraph": {"elements": [{"textRun": {"content": "a\n"}}]}}]},
            {"content": [{"paragraph": {"elements": [{"textRun": {"content": "b\n"}}]}}]}]}]}},
    ]}})
    sc = (await client.call_tool("docs_get_document", {"document_id": "D1"})).structured_content
    assert sc["text"] == "Intro\na | b\n" and sc["end_index"] == 20


async def test_sheets_ranges_are_url_encoded(client, google: FakeGoogle):
    url = "https://sheets.googleapis.com/v4/spreadsheets/S1/values/Hours%202026%21A1%3AB2"
    google.on("GET", url, {"range": "'Hours 2026'!A1:B2", "values": [["a", "b"]]})
    sc = (await client.call_tool("sheets_read_values", {"spreadsheet_id": "S1", "range": "Hours 2026!A1:B2"})).structured_content
    assert sc["values"] == [["a", "b"]]

    google.on("POST", url + ":append", {"updates": {"updatedRange": "x", "updatedRows": 1}})
    sc = (await client.call_tool("sheets_append_values", {"spreadsheet_id": "S1", "range": "Hours 2026!A1:B2", "values": [[1, 2]]})).structured_content
    assert sc["updated_rows"] == 1
    req = google.last("POST", url + ":append")
    assert query(req)["valueInputOption"] == ["USER_ENTERED"] and body(req) == {"values": [[1, 2]]}


async def test_chat_messages_filter_by_local_day(client, google: FakeGoogle):
    google.on("GET", "https://chat.googleapis.com/v1/spaces/AAA/messages", {"messages": [
        {"name": "spaces/AAA/messages/1", "createTime": "2026-10-12T07:00:00Z", "sender": {"name": "users/42", "type": "HUMAN"},
         "text": "deploy done", "thread": {"name": "spaces/AAA/threads/t"}}]})
    sc = (await client.call_tool("chat_list_messages", {"space": "AAA", "after": "2026-10-12", "before": "2026-10-12",
                                                         "time_zone": "Asia/Jerusalem"})).structured_content
    assert sc["space"] == "spaces/AAA" and sc["messages"][0]["sender"] == "users/42"
    flt = query(google.last("GET", "https://chat.googleapis.com/v1/spaces/AAA/messages"))["filter"][0]
    assert flt == 'createTime >= "2026-10-12T00:00:00+03:00" AND createTime < "2026-10-13T00:00:00+03:00"'


async def test_chat_rejects_malformed_space(client):
    result = await client.call_tool("chat_list_messages", {"space": "spaces/../x"})
    assert result.is_error is True and "invalid space" in text(result)


async def test_api_request_only_googleapis(client, google: FakeGoogle):
    bad = await client.call_tool("google_api_request", {"method": "GET", "url": "https://evil.example.com/steal"})
    assert bad.is_error is True and "only https://*.googleapis.com" in text(bad)
    assert google.token_calls == 0  # refused before any token was minted

    google.on("GET", "https://tasks.googleapis.com/tasks/v1/users/@me/lists", {"items": [{"id": "L1"}]})
    ok = await client.call_tool("google_api_request", {"method": "GET", "url": "https://tasks.googleapis.com/tasks/v1/users/@me/lists"})
    assert ok.structured_content == {"status": 200, "result": {"items": [{"id": "L1"}]}}
