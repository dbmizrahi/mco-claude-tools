"""`google-workspace-mcp auth`: PKCE loopback sign-in, credential file mode 600, no secret printed."""

from __future__ import annotations

import json
import os
import stat
import threading
import urllib.request
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit

import httpx
import pytest

from google_workspace_mcp import auth

CID = "123-test.apps.googleusercontent.com"
SECRET = "test-client-secret-not-real"
REFRESH = "1//test-refresh-from-auth"


def fake_google(refresh: str | None = REFRESH) -> tuple[httpx.Client, list[httpx.Request]]:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.host == "oauth2.googleapis.com":
            payload = {"access_token": "ya29.x", "expires_in": 3599, "scope": "openid email https://www.googleapis.com/auth/gmail.modify"}
            if refresh:
                payload["refresh_token"] = refresh
            return httpx.Response(200, json=payload)
        if request.url.host == "openidconnect.googleapis.com":
            return httpx.Response(200, json={"email": "me@example.com"})
        return httpx.Response(404, json={})

    return httpx.Client(transport=httpx.MockTransport(handler)), seen


def browser(code: str = "the-code", tamper_state: bool = False):
    """Plays the user's browser: follows the consent URL straight to the loopback redirect."""
    opened: dict[str, str] = {}

    def open_browser(url: str) -> None:
        opened["url"] = url
        q = {k: v[0] for k, v in parse_qs(urlsplit(url).query).items()}
        state = "wrong" if tamper_state else q["state"]
        target = q["redirect_uri"] + "?" + urlencode({"code": code, "state": state})

        def hit() -> None:
            try:
                urllib.request.urlopen(target, timeout=5).read()
            except Exception:  # noqa: BLE001 - a 400 page is expected when tampering
                pass

        threading.Thread(target=hit, daemon=True).start()

    return open_browser, opened


def test_sign_in_writes_private_file_and_hides_secrets(tmp_path: Path):
    out = tmp_path / "creds" / "private.json"
    session, seen = fake_google()
    open_browser, opened = browser()
    result = auth.run(out, CID, SECRET, "gmail", "me@example.com", False, open_browser=open_browser,
                      session=session, timeout=10, announce=lambda m: None)

    assert result["account"] == "me@example.com" and result["saved_to"] == str(out)
    assert SECRET not in json.dumps(result) and REFRESH not in json.dumps(result)
    assert stat.S_IMODE(os.stat(out).st_mode) == 0o600
    data = json.loads(out.read_text())
    assert data == {"type": "authorized_user", "client_id": CID, "client_secret": SECRET,
                    "refresh_token": REFRESH, "account": "me@example.com"}

    q = {k: v[0] for k, v in parse_qs(urlsplit(opened["url"]).query).items()}
    assert q["code_challenge_method"] == "S256" and q["access_type"] == "offline" and q["prompt"] == "consent"
    assert q["redirect_uri"].startswith("http://127.0.0.1:") and q["login_hint"] == "me@example.com"
    assert "gmail.modify" in q["scope"] and "openid" in q["scope"]
    token = parse_qs(seen[0].content.decode())
    assert token["grant_type"] == ["authorization_code"] and token["code"] == ["the-code"]
    assert token["code_verifier"][0] and token["redirect_uri"] == [q["redirect_uri"]]


def test_state_mismatch_is_rejected(tmp_path: Path):
    session, _ = fake_google()
    open_browser, _ = browser(tamper_state=True)
    with pytest.raises(auth.AuthError, match="state mismatch"):
        auth.run(tmp_path / "c.json", CID, SECRET, "gmail", None, False, open_browser=open_browser,
                 session=session, timeout=10, announce=lambda m: None)
    assert not (tmp_path / "c.json").exists()


def test_missing_refresh_token_explains_fix(tmp_path: Path):
    session, _ = fake_google(refresh=None)
    open_browser, _ = browser()
    with pytest.raises(auth.AuthError, match="myaccount.google.com/permissions"):
        auth.run(tmp_path / "c.json", CID, SECRET, "gmail", None, False, open_browser=open_browser,
                 session=session, timeout=10, announce=lambda m: None)


def test_existing_file_needs_force(tmp_path: Path):
    out = tmp_path / "c.json"
    out.write_text("{}")
    with pytest.raises(auth.AuthError, match="--force"):
        auth.run(out, CID, SECRET, "gmail", None, False, open_browser=lambda u: None, timeout=1, announce=lambda m: None)


def test_client_file_desktop_ok_web_refused(tmp_path: Path):
    desktop = tmp_path / "desktop.json"
    desktop.write_text(json.dumps({"installed": {"client_id": CID, "client_secret": SECRET}}))
    assert auth.read_client_file(desktop) == (CID, SECRET)
    web = tmp_path / "web.json"
    web.write_text(json.dumps({"web": {"client_id": CID, "client_secret": SECRET}}))
    with pytest.raises(auth.AuthError, match="Desktop app"):
        auth.read_client_file(web)


def test_scope_presets():
    assert auth.scopes_for("gmail-read")[-1].endswith("gmail.readonly")
    assert len(auth.scopes_for("all")) > 4
    with pytest.raises(auth.AuthError, match="gmail-read"):
        auth.scopes_for("everything")
