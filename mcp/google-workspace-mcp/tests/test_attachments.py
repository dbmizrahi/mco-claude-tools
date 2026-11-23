"""gmail_download_attachment against a fake Google: bytes go to disk, never to the model."""

from __future__ import annotations

import base64
import hashlib
from pathlib import Path

import pytest

from tests.conftest import FakeGoogle

pytestmark = pytest.mark.anyio

GMAIL = "https://gmail.googleapis.com/gmail/v1/users/me"
PDF = b"%PDF-1.7 receipt bytes"
PNG = b"\x89PNG tiny inline image"


def b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def text(result) -> str:
    return "\n".join(block.text for block in result.content if getattr(block, "type", "") == "text")


def message(*parts: dict) -> dict:
    return {"id": "m1", "payload": {"mimeType": "multipart/mixed", "parts": [
        {"mimeType": "text/plain", "body": {"data": b64(b"hello")}}, *parts]}}


PDF_PART = {"mimeType": "application/pdf", "filename": "Invoice 42.pdf", "body": {"attachmentId": "A1", "size": len(PDF)}}
PNG_PART = {"mimeType": "image/png", "filename": "logo.png", "body": {"data": b64(PNG), "size": len(PNG)}}


async def test_saves_by_attachment_id_into_folder(client, google: FakeGoogle, tmp_path: Path):
    google.on("GET", f"{GMAIL}/messages/m1", message(PDF_PART))
    google.on("GET", f"{GMAIL}/messages/m1/attachments/A1", {"data": b64(PDF), "size": len(PDF)})

    result = await client.call_tool("gmail_download_attachment",
                                    {"message_id": "m1", "attachment_id": "A1", "save_path": str(tmp_path)})

    assert result.is_error is False
    sc = result.structured_content
    assert Path(sc["saved_to"]) == tmp_path / "Invoice 42.pdf"
    assert (tmp_path / "Invoice 42.pdf").read_bytes() == PDF
    assert sc["sha256"] == hashlib.sha256(PDF).hexdigest() and sc["bytes"] == len(PDF)
    assert sc["mime_type"] == "application/pdf"
    assert b64(PDF) not in text(result)


async def test_saves_inline_part_by_filename(client, google: FakeGoogle, tmp_path: Path):
    google.on("GET", f"{GMAIL}/messages/m1", message(PNG_PART))
    result = await client.call_tool("gmail_download_attachment",
                                    {"message_id": "m1", "filename": "logo.png", "save_path": str(tmp_path / "x.png")})
    assert result.is_error is False
    assert (tmp_path / "x.png").read_bytes() == PNG


async def test_refuses_overwrite_unless_asked(client, google: FakeGoogle, tmp_path: Path):
    google.on("GET", f"{GMAIL}/messages/m1", message(PNG_PART))
    (tmp_path / "logo.png").write_bytes(b"old")
    args = {"message_id": "m1", "filename": "logo.png", "save_path": str(tmp_path)}
    first = await client.call_tool("gmail_download_attachment", args)
    assert first.is_error is True and "already exists" in text(first)
    second = await client.call_tool("gmail_download_attachment", {**args, "overwrite": True})
    assert second.is_error is False and (tmp_path / "logo.png").read_bytes() == PNG


async def test_unsafe_name_is_cleaned(client, google: FakeGoogle, tmp_path: Path):
    evil = {**PNG_PART, "filename": "../../etc/passwd"}
    google.on("GET", f"{GMAIL}/messages/m1", message(evil))
    result = await client.call_tool("gmail_download_attachment",
                                    {"message_id": "m1", "filename": "../../etc/passwd", "save_path": str(tmp_path)})
    assert result.is_error is False
    saved = Path(result.structured_content["saved_to"])
    assert saved.parent == tmp_path and "/" not in saved.name


async def test_too_large_is_refused_before_download(client, google: FakeGoogle, tmp_path: Path):
    big = {**PDF_PART, "body": {"attachmentId": "A1", "size": 26 * 1024 * 1024}}
    google.on("GET", f"{GMAIL}/messages/m1", message(big))
    result = await client.call_tool("gmail_download_attachment",
                                    {"message_id": "m1", "attachment_id": "A1", "save_path": str(tmp_path)})
    assert result.is_error is True and "25 MB" in text(result)
    assert all("/attachments/" not in str(r.url) for r in google.requests)


async def test_unknown_or_ambiguous_attachment(client, google: FakeGoogle, tmp_path: Path):
    google.on("GET", f"{GMAIL}/messages/m1", message(PDF_PART, {**PNG_PART, "filename": "Invoice 42.pdf"}))
    missing = await client.call_tool("gmail_download_attachment", {"message_id": "m1", "filename": "nope.pdf", "save_path": str(tmp_path)})
    assert missing.is_error is True and "Invoice 42.pdf" in text(missing)
    twice = await client.call_tool("gmail_download_attachment", {"message_id": "m1", "filename": "Invoice 42.pdf", "save_path": str(tmp_path)})
    assert twice.is_error is True and "attachment_id" in text(twice)
    neither = await client.call_tool("gmail_download_attachment", {"message_id": "m1"})
    assert neither.is_error is True


async def test_whoami_reports_account_label(client, google: FakeGoogle):
    google.on("GET", "https://oauth2.googleapis.com/tokeninfo", {"scope": "https://www.googleapis.com/auth/gmail.modify", "email": "me@example.com"})
    google.on("GET", f"{GMAIL}/profile", {"emailAddress": "me@example.com"})
    sc = (await client.call_tool("google_whoami", {})).structured_content
    assert "account_label" in sc and sc["account_label"] is None
