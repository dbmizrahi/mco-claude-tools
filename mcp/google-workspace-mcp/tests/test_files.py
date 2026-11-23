"""Drive file management, Docs/Sheets editing and Slides, against a fake Google."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import parse_qs

import httpx
import pytest

from tests.conftest import FakeGoogle, body

pytestmark = pytest.mark.anyio

DRIVE = "https://www.googleapis.com/drive/v3"
UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"
DOCS = "https://docs.googleapis.com/v1/documents"
SHEETS = "https://sheets.googleapis.com/v4/spreadsheets"
SLIDES = "https://slides.googleapis.com/v1/presentations"


def text(result) -> str:
    return "\n".join(block.text for block in result.content if getattr(block, "type", "") == "text")


def query(request: httpx.Request) -> dict[str, list[str]]:
    return parse_qs(request.url.query.decode())


# --------------------------------------------------------------------- drive
async def test_upload_uses_resumable_session_and_converts(client, google: FakeGoogle, tmp_path: Path):
    local = tmp_path / "Report Q3.docx"
    local.write_bytes(b"PK\x03\x04 fake docx")
    session = "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&upload_id=XYZ"
    google.on("POST", UPLOAD, lambda r: httpx.Response(200, headers={"Location": session}))
    google.on("PUT", UPLOAD, lambda r: {"id": "new1", "name": "Report Q3", "mimeType": "application/vnd.google-apps.document"})

    result = await client.call_tool("drive_upload_file", {"local_path": str(local), "parent_id": "F1", "convert_to": "document"})

    assert result.is_error is False and result.structured_content["id"] == "new1"
    start = google.last("POST", UPLOAD)
    assert query(start)["uploadType"] == ["resumable"]
    assert body(start) == {"name": "Report Q3", "parents": ["F1"], "mimeType": "application/vnd.google-apps.document"}
    assert start.headers["X-Upload-Content-Type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    assert start.headers["X-Upload-Content-Length"] == str(len(b"PK\x03\x04 fake docx"))
    put = google.last("PUT", UPLOAD)
    assert put.content == b"PK\x03\x04 fake docx" and query(put)["upload_id"] == ["XYZ"]


async def test_upload_missing_file(client, tmp_path: Path):
    result = await client.call_tool("drive_upload_file", {"local_path": str(tmp_path / "nope.pdf")})
    assert result.is_error is True and "is not a file" in text(result)


async def test_download_saves_into_directory_and_refuses_overwrite(client, google: FakeGoogle, tmp_path: Path):
    google.on("GET", f"{DRIVE}/files/p1", lambda r: httpx.Response(200, content=b"%PDF-1.7 bytes")
              if query(r).get("alt") == ["media"] else httpx.Response(200, json={"id": "p1", "name": "inv/oice.pdf", "mimeType": "application/pdf"}))

    first = await client.call_tool("drive_download_file", {"file_id": "p1", "save_path": str(tmp_path)})
    assert first.is_error is False
    saved = Path(first.structured_content["saved_to"])
    assert saved == tmp_path / "inv_oice.pdf" and saved.read_bytes() == b"%PDF-1.7 bytes"

    again = await client.call_tool("drive_download_file", {"file_id": "p1", "save_path": str(tmp_path)})
    assert again.is_error is True and "overwrite=true" in text(again)


async def test_download_refuses_google_native_files(client, google: FakeGoogle, tmp_path: Path):
    google.on("GET", f"{DRIVE}/files/d1", {"id": "d1", "name": "Plan", "mimeType": "application/vnd.google-apps.document"})
    result = await client.call_tool("drive_download_file", {"file_id": "d1", "save_path": str(tmp_path)})
    assert result.is_error is True and "drive_export_file" in text(result)


async def test_export_saves_with_extension(client, google: FakeGoogle, tmp_path: Path):
    google.on("GET", f"{DRIVE}/files/s1", {"id": "s1", "name": "Hours", "mimeType": "application/vnd.google-apps.spreadsheet"})
    google.on("GET", f"{DRIVE}/files/s1/export", lambda r: httpx.Response(200, content=b"xlsx-bytes"))
    result = await client.call_tool("drive_export_file", {"file_id": "s1", "format": "xlsx", "save_path": str(tmp_path) + "/"})
    sc = result.structured_content
    assert sc["saved_to"] == str(tmp_path / "Hours.xlsx") and sc["bytes"] == 10
    assert query(google.last("GET", f"{DRIVE}/files/s1/export"))["mimeType"] == [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]


async def test_export_to_missing_folder(client, google: FakeGoogle, tmp_path: Path):
    google.on("GET", f"{DRIVE}/files/s1", {"id": "s1", "name": "Hours", "mimeType": "application/vnd.google-apps.spreadsheet"})
    result = await client.call_tool("drive_export_file", {"file_id": "s1", "format": "pdf", "save_path": str(tmp_path / "no" / "x.pdf")})
    assert result.is_error is True and "does not exist" in text(result)


async def test_move_replaces_parents(client, google: FakeGoogle):
    def handler(r):
        if r.method == "GET":
            return {"parents": ["OLD1", "OLD2"]}
        return {"id": "f1", "name": body(r).get("name"), "parents": ["NEW"]}

    google.on("GET", f"{DRIVE}/files/f1", handler)
    google.on("PATCH", f"{DRIVE}/files/f1", handler)
    result = await client.call_tool("drive_update_file", {"file_id": "f1", "name": "Renamed", "move_to_folder_id": "NEW"})
    assert result.is_error is False
    q = query(google.last("PATCH", f"{DRIVE}/files/f1"))
    assert q["addParents"] == ["NEW"] and q["removeParents"] == ["OLD1,OLD2"]
    assert body(google.last("PATCH", f"{DRIVE}/files/f1")) == {"name": "Renamed"}


async def test_trash_and_restore(client, google: FakeGoogle):
    google.on("PATCH", f"{DRIVE}/files/f1", lambda r: {"id": "f1", "trashed": body(r)["trashed"]})
    assert (await client.call_tool("drive_trash_file", {"file_id": "f1"})).structured_content["trashed"] is True
    assert (await client.call_tool("drive_trash_file", {"file_id": "f1", "restore": True})).structured_content["trashed"] is False


async def test_share_requires_exactly_one_target_and_sends_notification(client, google: FakeGoogle):
    bad = await client.call_tool("drive_share_file", {"file_id": "f1", "role": "reader", "email": "a@x.com", "anyone_with_link": True})
    assert bad.is_error is True and "exactly one" in text(bad)

    google.on("POST", f"{DRIVE}/files/f1/permissions", lambda r: {"id": "p9", **body(r)})
    ok = await client.call_tool("drive_share_file", {"file_id": "f1", "role": "writer", "email": "a@x.com", "message": "FYI"})
    assert ok.structured_content == {"id": "p9", "type": "user", "role": "writer", "email": "a@x.com", "domain": None}
    q = query(google.last("POST", f"{DRIVE}/files/f1/permissions"))
    assert q["sendNotificationEmail"] == ["true"] and q["emailMessage"] == ["FYI"]


async def test_list_permissions(client, google: FakeGoogle):
    google.on("GET", f"{DRIVE}/files/f1/permissions", {"permissions": [
        {"id": "p1", "type": "user", "role": "owner", "emailAddress": "d@x.com", "displayName": "David"}]})
    sc = (await client.call_tool("drive_list_permissions", {"file_id": "f1"})).structured_content
    assert sc["permissions"][0]["email"] == "d@x.com" and sc["permissions"][0]["role"] == "owner"


# ---------------------------------------------------------------------- docs
async def test_docs_outline_lists_headings(client, google: FakeGoogle):
    google.on("GET", f"{DOCS}/D1", {"documentId": "D1", "title": "Spec", "body": {"content": [
        {"startIndex": 1, "endIndex": 7, "paragraph": {"paragraphStyle": {"namedStyleType": "TITLE"}, "elements": [{"textRun": {"content": "Spec\n"}}]}},
        {"startIndex": 7, "endIndex": 20, "paragraph": {"paragraphStyle": {"namedStyleType": "NORMAL_TEXT"}, "elements": [{"textRun": {"content": "body\n"}}]}},
        {"startIndex": 20, "endIndex": 30, "paragraph": {"paragraphStyle": {"namedStyleType": "HEADING_2"}, "elements": [{"textRun": {"content": "Scope\n"}}]}},
    ]}})
    sc = (await client.call_tool("docs_get_outline", {"document_id": "D1"})).structured_content
    assert sc["end_index"] == 30
    assert sc["headings"] == [
        {"level": 0, "style": "TITLE", "text": "Spec", "start_index": 1, "end_index": 7},
        {"level": 2, "style": "HEADING_2", "text": "Scope", "start_index": 20, "end_index": 30},
    ]


async def test_docs_replace_and_insert(client, google: FakeGoogle):
    google.on("POST", f"{DOCS}/D1:batchUpdate", lambda r: {"replies": [{"replaceAllText": {"occurrencesChanged": 3}}]}
              if "replaceAllText" in body(r)["requests"][0] else {"replies": [{}]})
    sc = (await client.call_tool("docs_replace_text", {"document_id": "D1", "find": "{{x}}", "replace": "y"})).structured_content
    assert sc["occurrences_changed"] == 3
    assert body(google.last("POST", f"{DOCS}/D1:batchUpdate"))["requests"][0]["replaceAllText"]["containsText"] == {"text": "{{x}}", "matchCase": True}

    await client.call_tool("docs_insert_text", {"document_id": "D1", "index": 20, "text": "New\n"})
    assert body(google.last("POST", f"{DOCS}/D1:batchUpdate")) == {"requests": [{"insertText": {"location": {"index": 20}, "text": "New\n"}}]}


async def test_docs_export_markdown(client, google: FakeGoogle):
    google.on("GET", f"{DRIVE}/files/D1/export", lambda r: httpx.Response(200, text="# Spec\n\n- a\n"))
    sc = (await client.call_tool("docs_export_text", {"document_id": "D1"})).structured_content
    assert sc["content"] == "# Spec\n\n- a\n"
    assert query(google.last("GET", f"{DRIVE}/files/D1/export"))["mimeType"] == ["text/markdown"]


# -------------------------------------------------------------------- sheets
async def test_sheets_batch_read_repeats_ranges(client, google: FakeGoogle):
    google.on("GET", f"{SHEETS}/S1/values:batchGet", {"valueRanges": [{"range": "A!A1:B1", "values": [[1, 2]]}, {"range": "B!A1"}]})
    sc = (await client.call_tool("sheets_batch_read", {"spreadsheet_id": "S1", "ranges": ["A!A1:B1", "B!A1"]})).structured_content
    assert sc["ranges"] == [{"range": "A!A1:B1", "values": [[1, 2]]}, {"range": "B!A1", "values": []}]
    assert query(google.last("GET", f"{SHEETS}/S1/values:batchGet"))["ranges"] == ["A!A1:B1", "B!A1"]


async def test_sheets_tab_management(client, google: FakeGoogle):
    def batch(r):
        req = body(r)["requests"][0]
        if "addSheet" in req:
            return {"replies": [{"addSheet": {"properties": {"sheetId": 77, "title": req["addSheet"]["properties"]["title"], "index": 2}}}]}
        return {"replies": [{}]}

    google.on("POST", f"{SHEETS}/S1:batchUpdate", batch)
    sc = (await client.call_tool("sheets_add_sheet", {"spreadsheet_id": "S1", "title": "Oct"})).structured_content
    assert sc == {"sheet_id": 77, "title": "Oct", "index": 2}

    await client.call_tool("sheets_rename_sheet", {"spreadsheet_id": "S1", "sheet_id": 77, "title": "October"})
    assert body(google.last("POST", f"{SHEETS}/S1:batchUpdate")) == {"requests": [
        {"updateSheetProperties": {"properties": {"sheetId": 77, "title": "October"}, "fields": "title"}}]}

    await client.call_tool("sheets_delete_sheet", {"spreadsheet_id": "S1", "sheet_id": 77})
    assert body(google.last("POST", f"{SHEETS}/S1:batchUpdate")) == {"requests": [{"deleteSheet": {"sheetId": 77}}]}


async def test_sheets_clear(client, google: FakeGoogle):
    google.on("POST", f"{SHEETS}/S1/values/Hours%21A2%3AF:clear", {"clearedRange": "Hours!A2:F1000"})
    sc = (await client.call_tool("sheets_clear_values", {"spreadsheet_id": "S1", "range": "Hours!A2:F"})).structured_content
    assert sc == {"cleared_range": "Hours!A2:F1000"}


# -------------------------------------------------------------------- slides
def _text(t: str) -> dict:
    return {"text": {"textElements": [{"textRun": {"content": t}}]}}


PRESENTATION = {
    "presentationId": "P1", "title": "Deck",
    "slides": [{
        "objectId": "s1",
        "pageElements": [
            {"objectId": "t1", "shape": {"placeholder": {"type": "TITLE"}, **_text("Quarterly review\n")}},
            {"objectId": "b1", "shape": {"placeholder": {"type": "BODY"}}},
            {"objectId": "tb1", "table": {"tableRows": [{"tableCells": [_text("a\n"), _text("b\n")]}]}},
            {"objectId": "img1", "image": {}},
        ],
        "slideProperties": {"notesPage": {
            "notesProperties": {"speakerNotesObjectId": "n1"},
            "pageElements": [{"objectId": "n1", "shape": _text("Say hello\n")}]}},
    }],
}


async def test_slides_get_presentation(client, google: FakeGoogle):
    google.on("GET", f"{SLIDES}/P1", PRESENTATION)
    sc = (await client.call_tool("slides_get_presentation", {"presentation_id": "P1"})).structured_content
    assert sc["slide_count"] == 1 and sc["truncated"] is False
    slide = sc["slides"][0]
    assert slide["slide_id"] == "s1" and slide["notes"] == "Say hello"
    assert slide["elements"] == [
        {"object_id": "t1", "kind": "shape", "placeholder": "TITLE", "text": "Quarterly review"},
        {"object_id": "b1", "kind": "shape", "placeholder": "BODY"},
        {"object_id": "tb1", "kind": "table", "text": "a | b"},
        {"object_id": "img1", "kind": "image"},
    ]


async def test_slides_add_title_slide_maps_centered_title(client, google: FakeGoogle):
    google.on("POST", f"{SLIDES}/P1:batchUpdate", {"replies": [{"createSlide": {}}]})
    sc = (await client.call_tool("slides_add_slide", {"presentation_id": "P1", "layout": "TITLE", "title": "Hello", "body": "Sub", "index": 1})).structured_content
    reqs = body(google.last("POST", f"{SLIDES}/P1:batchUpdate"))["requests"]
    create = reqs[0]["createSlide"]
    assert create["objectId"] == sc["slide_id"] and create["insertionIndex"] == 1
    assert [m["layoutPlaceholder"]["type"] for m in create["placeholderIdMappings"]] == ["CENTERED_TITLE", "SUBTITLE"]
    assert reqs[1] == {"insertText": {"objectId": sc["title_id"], "text": "Hello"}}
    assert reqs[2] == {"insertText": {"objectId": sc["body_id"], "text": "Sub"}}
    for oid in (sc["slide_id"], sc["title_id"], sc["body_id"]):
        assert 5 <= len(oid) <= 50


async def test_slides_set_text_skips_delete_on_empty_shape(client, google: FakeGoogle):
    google.on("GET", f"{SLIDES}/P1", PRESENTATION)
    google.on("POST", f"{SLIDES}/P1:batchUpdate", {"replies": []})

    await client.call_tool("slides_set_text", {"presentation_id": "P1", "object_id": "b1", "text": "Points"})
    assert body(google.last("POST", f"{SLIDES}/P1:batchUpdate"))["requests"] == [
        {"insertText": {"objectId": "b1", "text": "Points", "insertionIndex": 0}}]

    await client.call_tool("slides_set_text", {"presentation_id": "P1", "object_id": "t1", "text": "New title"})
    reqs = body(google.last("POST", f"{SLIDES}/P1:batchUpdate"))["requests"]
    assert reqs[0] == {"deleteText": {"objectId": "t1", "textRange": {"type": "ALL"}}}

    await client.call_tool("slides_set_text", {"presentation_id": "P1", "object_id": "t1", "text": " 2026", "replace_existing": False})
    assert body(google.last("POST", f"{SLIDES}/P1:batchUpdate"))["requests"] == [
        {"insertText": {"objectId": "t1", "text": " 2026", "insertionIndex": len("Quarterly review")}}]

    missing = await client.call_tool("slides_set_text", {"presentation_id": "P1", "object_id": "zzz", "text": "x"})
    assert missing.is_error is True and "no element" in text(missing)


async def test_slides_thumbnail_saved_without_bearer(client, google: FakeGoogle, tmp_path: Path):
    google.on("GET", f"{SLIDES}/P1/pages/s1/thumbnail", {"width": 1600, "height": 900, "contentUrl": "https://lh3.googleusercontent.com/abc"})
    google.on("GET", "https://lh3.googleusercontent.com/abc", lambda r: httpx.Response(200, content=b"\x89PNG"))
    sc = (await client.call_tool("slides_get_thumbnail", {"presentation_id": "P1", "slide_id": "s1", "save_path": str(tmp_path)})).structured_content
    assert sc["saved_to"] == str(tmp_path / "s1.png") and (tmp_path / "s1.png").read_bytes() == b"\x89PNG"
    image_req = google.last("GET", "https://lh3.googleusercontent.com/abc")
    assert "Authorization" not in image_req.headers
    thumb_q = query(google.last("GET", f"{SLIDES}/P1/pages/s1/thumbnail"))
    assert thumb_q["thumbnailProperties.thumbnailSize"] == ["LARGE"]


async def test_slides_replace_text_scoped_to_slides(client, google: FakeGoogle):
    google.on("POST", f"{SLIDES}/P1:batchUpdate", {"replies": [{"replaceAllText": {"occurrencesChanged": 2}}]})
    sc = (await client.call_tool("slides_replace_text", {"presentation_id": "P1", "find": "{{client}}", "replace": "Acme", "slide_ids": ["s1"]})).structured_content
    assert sc == {"occurrences_changed": 2}
    req = body(google.last("POST", f"{SLIDES}/P1:batchUpdate"))["requests"][0]["replaceAllText"]
    assert req["pageObjectIds"] == ["s1"] and req["replaceText"] == "Acme"
