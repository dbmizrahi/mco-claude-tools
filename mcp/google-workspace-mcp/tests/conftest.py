"""Shared fixtures: a fake Google behind httpx.MockTransport, and an in-memory MCP client."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable
from urllib.parse import parse_qs

import httpx
import pytest
from mcp import Client

from google_workspace_mcp.client import GoogleClient
from google_workspace_mcp.config import GoogleConfig
from google_workspace_mcp.server import mcp, set_client

REFRESH_TOKEN = "1//test-refresh-token-not-real"
CLIENT_SECRET = "test-client-secret-not-real"  # not GOCSPX-shaped: the repo's secret scanner flags those
ACCESS_TOKEN = "ya29.test-access-token"
SCOPES = "https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/calendar openid"


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@dataclass
class FakeGoogle:
    """Routes '<METHOD> <host><path>' to canned responders and records requests."""

    responders: dict[str, Callable[[httpx.Request], Any]] = field(default_factory=dict)
    requests: list[httpx.Request] = field(default_factory=list)
    token_calls: int = 0
    token_response: Callable[[], httpx.Response] | None = None

    def on(self, method: str, url: str, responder: Callable[[httpx.Request], Any] | Any) -> None:
        fn = responder if callable(responder) else (lambda request: responder)
        key = url.split("://", 1)[-1]
        self.responders[f"{method} {key}"] = fn

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        key = f"{request.method} {request.url.host}{request.url.raw_path.decode().split('?')[0]}"
        if key == "POST oauth2.googleapis.com/token":
            self.token_calls += 1
            if self.token_response:
                return self.token_response()
            return httpx.Response(200, json={"access_token": f"{ACCESS_TOKEN}-{self.token_calls}", "expires_in": 3599,
                                             "scope": SCOPES, "token_type": "Bearer"})
        responder = self.responders.get(key)
        if responder is None:
            return google_error(404, f"no responder for {key}", "notFound")
        result = responder(request)
        if isinstance(result, httpx.Response):
            return result
        return httpx.Response(200, json=result)

    def last(self, method: str, url: str) -> httpx.Request:
        key = url.split("://", 1)[-1]
        for r in reversed(self.requests):
            if f"{r.method} {r.url.host}{r.url.raw_path.decode().split('?')[0]}" == f"{method} {key}":
                return r
        raise AssertionError(f"no request {method} {url}")


def body(request: httpx.Request) -> Any:
    return json.loads(request.content or b"null")


def form(request: httpx.Request) -> dict[str, str]:
    return {k: v[0] for k, v in parse_qs(request.content.decode()).items()}


def google_error(status: int, message: str, reason: str = "", detail_reason: str = "") -> httpx.Response:
    err: dict[str, Any] = {"code": status, "message": message, "errors": [{"reason": reason, "message": message}]}
    if detail_reason:
        err["details"] = [{"@type": "type.googleapis.com/google.rpc.ErrorInfo", "reason": detail_reason}]
    return httpx.Response(status, json={"error": err})


@pytest.fixture
def config() -> GoogleConfig:
    return GoogleConfig(
        client_id="123-test.apps.googleusercontent.com",
        client_secret=CLIENT_SECRET,
        refresh_token=REFRESH_TOKEN,
        timeout=5.0,
        max_text_chars=1000,
        credential_source="$GOOGLE_CLIENT_ID / $GOOGLE_CLIENT_SECRET / $GOOGLE_REFRESH_TOKEN",
        account_hint=None,
    )


@pytest.fixture
def google() -> FakeGoogle:
    return FakeGoogle()


@pytest.fixture
async def client(config: GoogleConfig, google: FakeGoogle):
    gclient = GoogleClient(config, transport=httpx.MockTransport(google.handler))
    set_client(gclient)
    try:
        async with Client(mcp, raise_exceptions=True) as c:
            yield c
    finally:
        set_client(None)
        await gclient.aclose()
