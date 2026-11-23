"""Thin async client for Google's REST APIs, signed in with a refresh token.

Access tokens are minted at https://oauth2.googleapis.com/token, cached until a
minute before they expire, and minted again once if Google answers 401.

Errors become GoogleError with a message that says what Google said and what to
do about it: re-login for a dead refresh token, add a scope, enable an API in the
OAuth client's Cloud project, or retry later for rate limits.
"""

from __future__ import annotations

import json
import time
from typing import Any, Mapping
from urllib.parse import parse_qsl, urlsplit, urlunsplit

import httpx

from google_workspace_mcp import __version__
from google_workspace_mcp.config import GoogleConfig

TOKEN_URL = "https://oauth2.googleapis.com/token"
TOKENINFO_URL = "https://oauth2.googleapis.com/tokeninfo"
USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
BODY_PREVIEW = 400
EXPIRY_MARGIN = 60.0
# Token-endpoint error codes that mean "a human must log in again", not "retry".
REAUTH_ERRORS = {"invalid_grant", "invalid_rapt", "unauthorized_client", "invalid_client"}


class GoogleError(Exception):
    """An error reported by Google or by the transport, with an actionable message."""

    def __init__(self, message: str, *, status: int | None = None, reason: str | None = None) -> None:
        super().__init__(message)
        self.status = status
        self.reason = reason


def allowed_url(url: str) -> bool:
    """Only https Google API hosts; keeps the bearer token from leaving Google."""
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    return parts.scheme == "https" and (host == "googleapis.com" or host.endswith(".googleapis.com"))


class GoogleClient:
    def __init__(self, config: GoogleConfig, *, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self.config = config
        self._http = httpx.AsyncClient(
            timeout=config.timeout,
            transport=transport,
            headers={"User-Agent": f"google-workspace-mcp/{__version__} python-httpx/{httpx.__version__}"},
        )
        self._token: str | None = None
        self._expires_at = 0.0
        self.granted_scopes: list[str] = []

    async def aclose(self) -> None:
        await self._http.aclose()

    # ------------------------------------------------------------------ token
    async def access_token(self, *, force: bool = False) -> str:
        if not force and self._token and time.monotonic() < self._expires_at:
            return self._token
        data = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "refresh_token": self.config.refresh_token,
            "grant_type": "refresh_token",
        }
        try:
            response = await self._http.post(TOKEN_URL, data=data)
        except httpx.HTTPError as exc:
            raise GoogleError(f"cannot reach Google's token endpoint: {exc}") from exc
        payload = _json_or_none(response)
        if response.status_code >= 400 or not isinstance(payload, dict) or "access_token" not in payload:
            raise self._token_error(response, payload)
        self._token = str(payload["access_token"])
        lifetime = float(payload.get("expires_in") or 3600)
        self._expires_at = time.monotonic() + max(lifetime - EXPIRY_MARGIN, 0.0)
        scope = payload.get("scope")
        if isinstance(scope, str):
            self.granted_scopes = sorted(scope.split())
        return self._token

    def _token_error(self, response: httpx.Response, payload: Any) -> GoogleError:
        code = subtype = detail = ""
        if isinstance(payload, dict):
            code = str(payload.get("error") or "")
            subtype = str(payload.get("error_subtype") or "")
            detail = str(payload.get("error_description") or "")
        if not detail:
            detail = response.text[:BODY_PREVIEW].strip() or response.reason_phrase
        said = f"{code}{'/' + subtype if subtype else ''}: {detail}" if code else detail
        if code in REAUTH_ERRORS or subtype in REAUTH_ERRORS:
            return GoogleError(
                f"Google refused the refresh token ({said}). It is expired, revoked, or belongs to a "
                f"different OAuth client than client_id. This needs an interactive re-login that "
                f"produces a new refresh token for the same client; the credential in use came from "
                f"{self.config.credential_source}. If it recurs about weekly, the OAuth consent "
                f"screen is in Testing mode, where Google expires refresh tokens after 7 days.",
                status=response.status_code, reason=code,
            )
        return GoogleError(f"Google token endpoint HTTP {response.status_code} ({said})", status=response.status_code, reason=code)

    # ------------------------------------------------------------------ calls
    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_body: Any = None,
        raw: bool = False,
        content: bytes | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        """Call a Google API. Returns decoded JSON, or the httpx.Response when raw=True.

        `content` sends raw bytes (uploads) instead of a JSON body; `headers` adds headers.
        """
        if not allowed_url(url):
            raise GoogleError(f"refusing {url!r}: only https://*.googleapis.com URLs are allowed")
        # httpx replaces a URL's own query string when params are given, which would drop
        # e.g. the upload_id of a resumable-upload session URL. Merge them instead.
        parts = urlsplit(url)
        clean_params: dict[str, Any] = dict(parse_qsl(parts.query, keep_blank_values=True))
        clean_params.update({k: v for k, v in (params or {}).items() if v is not None})
        url = urlunsplit((parts.scheme, parts.netloc, parts.path, "", parts.fragment))
        extra = dict(headers or {})
        response = await self._send(method, url, clean_params, json_body, content, extra, force_token=False)
        if response.status_code == 401:
            # The cached access token may have been revoked early: mint once more.
            response = await self._send(method, url, clean_params, json_body, content, extra, force_token=True)
        if response.status_code >= 400:
            raise self._api_error(response, method, url)
        if raw:
            return response
        if not response.content.strip():
            return {}
        try:
            return response.json()
        except ValueError as exc:
            raise GoogleError(
                f"{method} {_short(url)} returned a non-JSON body (HTTP {response.status_code}): "
                f"{response.text[:BODY_PREVIEW]!r}"
            ) from exc

    async def get(self, url: str, **params: Any) -> Any:
        return await self.request("GET", url, params=params)

    async def fetch_public(self, url: str) -> bytes:
        """GET a URL WITHOUT the bearer token (e.g. a Slides thumbnail contentUrl).

        Restricted to Google's content hosts so it cannot be pointed elsewhere.
        """
        parts = urlsplit(url)
        host = (parts.hostname or "").lower()
        if parts.scheme != "https" or not (host.endswith(".googleusercontent.com") or host.endswith(".googleapis.com")):
            raise GoogleError(f"refusing to fetch {url!r}: not a Google content URL")
        try:
            response = await self._http.get(url)
        except httpx.HTTPError as exc:
            raise GoogleError(f"cannot fetch {_short(url)}: {exc}") from exc
        if response.status_code >= 400:
            raise GoogleError(f"GET {_short(url)} failed with HTTP {response.status_code}", status=response.status_code)
        return response.content

    async def _send(
        self, method: str, url: str, params: dict, json_body: Any, raw_content: bytes | None,
        extra_headers: dict[str, str], *, force_token: bool,
    ) -> httpx.Response:
        token = await self.access_token(force=force_token)
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        content: bytes | str | None = raw_content
        if json_body is not None:
            headers["Content-Type"] = "application/json; charset=utf-8"
            content = json.dumps(json_body, ensure_ascii=False)
        headers.update(extra_headers)
        try:
            return await self._http.request(method, url, params=params, headers=headers, content=content)
        except httpx.TimeoutException as exc:
            raise GoogleError(
                f"timeout after {self.config.timeout:g}s on {method} {_short(url)}; raise $GOOGLE_TIMEOUT "
                f"or narrow the request"
            ) from exc
        except httpx.HTTPError as exc:
            raise GoogleError(f"cannot reach {_short(url)}: {exc}") from exc

    def _api_error(self, response: httpx.Response, method: str, url: str) -> GoogleError:
        status = response.status_code
        payload = _json_or_none(response)
        message, reason = "", ""
        err = payload.get("error") if isinstance(payload, dict) else None
        if isinstance(err, dict):
            message = str(err.get("message") or "")
            for item in err.get("details") or []:
                if isinstance(item, dict) and item.get("reason"):
                    reason = str(item["reason"])
                    break
            if not reason:
                for item in err.get("errors") or []:
                    if isinstance(item, dict) and item.get("reason"):
                        reason = str(item["reason"])
                        break
        elif isinstance(err, str):
            message = str(payload.get("error_description") or err)
        if not message:
            message = response.text[:BODY_PREVIEW].strip() or response.reason_phrase
        where = f"{method} {_short(url)}"
        said = f"{reason}: {message}" if reason else message
        lowered = f"{reason} {message}".lower()

        if status == 401:
            text = f"Google rejected the access token on {where} (HTTP 401, {said}) even after minting a fresh one."
        elif status == 403 and ("scope" in lowered or reason in {"insufficientPermissions", "ACCESS_TOKEN_SCOPE_INSUFFICIENT"}):
            scopes = ", ".join(self.granted_scopes) or "unknown"
            text = (
                f"The refresh token lacks the OAuth scope for {where} (HTTP 403, {said}). Granted scopes: "
                f"{scopes}. Re-login with the needed scope added; nothing else will fix it."
            )
        elif status == 403 and ("has not been used" in lowered or "disabled" in lowered or reason in {"SERVICE_DISABLED", "accessNotConfigured"}):
            text = (
                f"The API behind {where} is not enabled in the OAuth client's Google Cloud project "
                f"(HTTP 403, {said}). Enable it with `gcloud services enable <api>.googleapis.com "
                f"--project=<project>` and retry after a minute."
            )
        elif reason == "exportSizeLimitExceeded":
            text = (
                f"The file is too large for Google's export ({where}, {said}). Google caps exports at "
                f"10 MB of output: try a lighter format (pdf instead of pptx, csv per tab), or open "
                f"the file's link and download it from the Google UI."
            )
        elif status == 403:
            text = f"Google denied {where} (HTTP 403, {said}). The account lacks access to this resource."
        elif status == 404:
            text = f"{where}: not found (HTTP 404, {said}). Check the id, or that the account can see it."
        elif status == 429 or reason in {"rateLimitExceeded", "userRateLimitExceeded", "RATE_LIMIT_EXCEEDED"}:
            text = f"Google rate limit on {where} (HTTP {status}, {said}). Wait and retry with smaller pages."
        elif status >= 500:
            text = f"Google server error on {where} (HTTP {status}, {said}). Usually transient; retry."
        else:
            text = f"{where} failed (HTTP {status}, {said})"
        return GoogleError(text, status=status, reason=reason or None)


def _json_or_none(response: httpx.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return None


def _short(url: str) -> str:
    return url.split("?", 1)[0]
