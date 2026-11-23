"""`google-workspace-mcp auth`: sign in to a Google account once and save its credential.

Runs Google's OAuth flow for installed (desktop) apps: PKCE, a one-shot HTTP listener on
127.0.0.1, the browser for the consent screen. The result is an *authorized user* JSON file
(client_id, client_secret, refresh_token), written with mode 600, that the server reads via
GOOGLE_CREDENTIALS_FILE. Neither the client secret nor the refresh token is ever printed.

    google-workspace-mcp auth --out ~/.config/google-workspace-mcp/private.json \\
        --client-file ~/Downloads/client_secret_XXXX.json [--scopes gmail] [--login-hint me@gmail.com]

Run it on the computer with the browser, once per Google account.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import json
import os
import secrets
import sys
import threading
import webbrowser
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Callable
from urllib.parse import parse_qs, urlencode, urlsplit

import httpx

from google_workspace_mcp.client import TOKEN_URL, USERINFO_URL

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
G = "https://www.googleapis.com/auth/"
IDENTITY = ["openid", "email"]
PRESETS: dict[str, list[str]] = {
    "gmail-read": [G + "gmail.readonly"],
    "gmail": [G + "gmail.modify"],
    "all": [G + "gmail.modify", G + "calendar", G + "drive", G + "documents", G + "spreadsheets",
            G + "presentations", G + "chat.spaces.readonly", G + "chat.messages"],
}
TIMEOUT_SECONDS = 300


class AuthError(Exception):
    """A failure safe to show: never contains a secret."""


def scopes_for(preset: str) -> list[str]:
    if preset not in PRESETS:
        raise AuthError(f"unknown scope preset {preset!r}; choose one of: {', '.join(PRESETS)}")
    return IDENTITY + PRESETS[preset]


def read_client_file(path: Path) -> tuple[str, str]:
    """client_id and client_secret from the JSON Google Cloud lets you download for an OAuth client."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AuthError(f"cannot read OAuth client file {path}: {exc}") from exc
    block = data.get("installed") or data.get("web") or data if isinstance(data, dict) else {}
    cid, sec = str(block.get("client_id") or ""), str(block.get("client_secret") or "")
    if not cid or not sec:
        raise AuthError(f"{path} has no client_id/client_secret (download it from Google Cloud: "
                        "APIs & Services > Credentials > your Desktop client > Download JSON)")
    if "web" in data:
        raise AuthError(f"{path} is a 'Web application' client; create a 'Desktop app' client instead")
    return cid, sec


def pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)[:96]
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


def build_auth_url(client_id: str, redirect_uri: str, scopes: list[str], state: str, challenge: str,
                   login_hint: str | None = None) -> str:
    params = {
        "client_id": client_id, "redirect_uri": redirect_uri, "response_type": "code",
        "scope": " ".join(scopes), "state": state, "code_challenge": challenge,
        "code_challenge_method": "S256", "access_type": "offline", "prompt": "consent",
        "include_granted_scopes": "true",
    }
    if login_hint:
        params["login_hint"] = login_hint
    return AUTH_URL + "?" + urlencode(params)


def wait_for_code(server: HTTPServer, state: str, timeout: float) -> str:
    """Serve one browser redirect on the loopback listener; return the authorization code."""
    result: dict[str, str] = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 (http.server naming)
            q = {k: v[0] for k, v in parse_qs(urlsplit(self.path).query).items()}
            if q.get("state") != state:
                result["error"] = "state mismatch (the sign-in did not come from this run)"
            elif "error" in q:
                result["error"] = f"Google returned: {q['error']}"
            elif "code" in q:
                result["code"] = q["code"]
            else:
                result["error"] = "no authorization code in the redirect"
            ok = "code" in result
            self.send_response(200 if ok else 400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            msg = ("Signed in. You can close this tab and return to the terminal." if ok
                   else "Sign-in failed. Return to the terminal for details.")
            self.wfile.write(f"<!doctype html><title>google-workspace-mcp</title><p>{msg}</p>".encode())

        def log_message(self, *_args: Any) -> None:  # keep the terminal quiet (the URL holds the code)
            return

    server.RequestHandlerClass = Handler
    server.timeout = timeout
    server.handle_request()
    if "code" not in result:
        raise AuthError(result.get("error") or f"no sign-in within {int(timeout)} seconds")
    return result["code"]


def exchange_code(session: httpx.Client, client_id: str, client_secret: str, code: str,
                  redirect_uri: str, verifier: str) -> dict[str, Any]:
    resp = session.post(TOKEN_URL, data={
        "code": code, "client_id": client_id, "client_secret": client_secret,
        "redirect_uri": redirect_uri, "grant_type": "authorization_code", "code_verifier": verifier,
    })
    payload = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
    if resp.status_code != 200:
        raise AuthError(f"token exchange failed (HTTP {resp.status_code}): "
                        f"{payload.get('error', '')} {payload.get('error_description', '')}".strip())
    if not payload.get("refresh_token"):
        raise AuthError("Google returned no refresh token; remove the app's access at "
                        "https://myaccount.google.com/permissions and run auth again")
    return payload


def account_email(session: httpx.Client, access_token: str) -> str | None:
    resp = session.get(USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"})
    return resp.json().get("email") if resp.status_code == 200 else None


def write_credential(path: Path, data: dict[str, str], force: bool) -> None:
    if path.exists() and not force:
        raise AuthError(f"{path} already exists; pass --force to replace it")
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)


def run(out: Path, client_id: str, client_secret: str, preset: str, login_hint: str | None, force: bool,
        open_browser: Callable[[str], object] = webbrowser.open, session: httpx.Client | None = None,
        timeout: float = TIMEOUT_SECONDS, announce: Callable[[str], None] = lambda m: print(m, file=sys.stderr)) -> dict[str, Any]:
    scopes = scopes_for(preset)
    if out.exists() and not force:
        raise AuthError(f"{out} already exists; pass --force to replace it")
    verifier, challenge = pkce_pair()
    state = secrets.token_urlsafe(24)
    server = HTTPServer(("127.0.0.1", 0), BaseHTTPRequestHandler)
    redirect_uri = f"http://127.0.0.1:{server.server_address[1]}/"
    url = build_auth_url(client_id, redirect_uri, scopes, state, challenge, login_hint)
    announce("Opening the Google sign-in page. If it does not open, paste this URL into your browser:\n" + url)
    holder: dict[str, Any] = {}

    def serve() -> None:
        try:
            holder["code"] = wait_for_code(server, state, timeout)
        except AuthError as exc:
            holder["error"] = exc

    worker = threading.Thread(target=serve, daemon=True)
    worker.start()
    open_browser(url)
    worker.join(timeout + 5)
    server.server_close()
    if "error" in holder:
        raise holder["error"]
    if "code" not in holder:
        raise AuthError(f"no sign-in within {int(timeout)} seconds")

    own = session is None
    client = session or httpx.Client(timeout=30)
    try:
        tokens = exchange_code(client, client_id, client_secret, holder["code"], redirect_uri, verifier)
        email = account_email(client, str(tokens.get("access_token", "")))
    finally:
        if own:
            client.close()
    write_credential(out, {"type": "authorized_user", "client_id": client_id, "client_secret": client_secret,
                           "refresh_token": str(tokens["refresh_token"]), "account": email or ""}, force)
    return {"saved_to": str(out), "account": email, "scopes": str(tokens.get("scope", "")).split()}


def cli(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="google-workspace-mcp auth",
                                 description="Sign in to one Google account and save its credential file (mode 600).")
    ap.add_argument("--out", required=True, help="credential file to write, e.g. ~/.config/google-workspace-mcp/private.json")
    ap.add_argument("--client-file", help="OAuth client JSON downloaded from Google Cloud (Desktop app); "
                                          "without it, the client id and secret are asked for")
    ap.add_argument("--scopes", default="gmail", choices=sorted(PRESETS), help="what the account may do (default: gmail)")
    ap.add_argument("--login-hint", help="email address to preselect on the Google sign-in page")
    ap.add_argument("--force", action="store_true", help="replace an existing credential file")
    a = ap.parse_args(argv)
    try:
        if a.client_file:
            cid, sec = read_client_file(Path(os.path.expanduser(a.client_file)))
        else:
            cid = input("OAuth client ID: ").strip()
            sec = getpass.getpass("OAuth client secret (hidden): ").strip()
            if not cid or not sec:
                raise AuthError("client ID and secret are both required")
        result = run(Path(os.path.expanduser(a.out)), cid, sec, a.scopes, a.login_hint, a.force)
    except AuthError as exc:
        print(f"auth failed: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("auth cancelled", file=sys.stderr)
        return 130
    print(json.dumps(result, indent=2))
    return 0
