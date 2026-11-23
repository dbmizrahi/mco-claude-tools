"""Credentials and settings for the Google Workspace MCP server.

The server signs in with an OAuth *refresh token* (an "authorized user"
credential) and mints short-lived access tokens from it. The three values
client_id, client_secret and refresh_token always come from ONE source, the
first complete one in this order:

  1. $GOOGLE_CLIENT_ID + $GOOGLE_CLIENT_SECRET + $GOOGLE_REFRESH_TOKEN
  2. the JSON file named by $GOOGLE_CREDENTIALS_FILE
  3. the `google` section of a settings file: $GOOGLE_WORKSPACE_CONFIG, else
     ~/.config/google-workspace-mcp/config.json
  4. ~/.config/gws/work.json  (what `gws auth export --unmasked` writes)

`google-workspace-mcp auth --out <file>` creates the file for source 2.

Mixing sources is refused: a client_id from one place and a refresh_token from
another fail at Google with a misleading `unauthorized_client`.

Other settings:
  label     $GOOGLE_ACCOUNT_LABEL       -> none   (e.g. "private" / "work" when several accounts run side by side)
  timeout   $GOOGLE_TIMEOUT (seconds)  -> 60
  max text  $GOOGLE_MAX_TEXT_CHARS     -> 50000  (cap on file/message bodies returned)
  downloads $GOOGLE_DOWNLOAD_DIR       -> ~/Downloads  (where downloads/exports go when no path is given)

Nothing here ever logs or returns a secret; `describe()` reports only where the
credential came from.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

SETTINGS_FILE = Path(".config") / "google-workspace-mcp" / "config.json"
DEFAULT_TIMEOUT = 60.0
DEFAULT_MAX_TEXT_CHARS = 50_000
DEFAULT_DOWNLOAD_DIR = "~/Downloads"
GWS_EXPORT = Path(".config") / "gws" / "work.json"
PLACEHOLDERS = {""}
FIELDS = ("client_id", "client_secret", "refresh_token")
ENV_NAMES = {"client_id": "GOOGLE_CLIENT_ID", "client_secret": "GOOGLE_CLIENT_SECRET", "refresh_token": "GOOGLE_REFRESH_TOKEN"}


class ConfigError(Exception):
    """Raised when no usable Google credential can be found."""


@dataclass(frozen=True)
class GoogleConfig:
    client_id: str
    client_secret: str
    refresh_token: str
    timeout: float
    max_text_chars: int
    credential_source: str
    account_hint: str | None
    download_dir: str = "~/Downloads"
    account_label: str | None = None

    def describe(self) -> dict[str, object]:
        """Diagnostics safe to show: never includes a secret."""
        return {
            "account_label": self.account_label,
            "credential_source": self.credential_source,
            "client_id": self.client_id,  # not secret; identifies the OAuth client
            "configured_account": self.account_hint,
            "timeout_seconds": self.timeout,
            "max_text_chars": self.max_text_chars,
            "download_dir": self.download_dir,
        }


def settings_file_candidates(env: Mapping[str, str], home: Path) -> list[Path]:
    override = env.get("GOOGLE_WORKSPACE_CONFIG", "").strip()
    if override:
        return [Path(os.path.expanduser(override))]
    return [home / SETTINGS_FILE]


def _clean(value: object) -> str:
    text = str(value or "").strip()
    return "" if text in PLACEHOLDERS else text


def _read_json(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot read {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"{path} does not hold a JSON object")
    return data


def _complete(values: Mapping[str, object]) -> dict[str, str] | None:
    cleaned = {f: _clean(values.get(f)) for f in FIELDS}
    return cleaned if all(cleaned.values()) else None


def _partial(values: Mapping[str, object]) -> list[str]:
    return [f for f in FIELDS if _clean(values.get(f))]


def _number(env: Mapping[str, str], name: str, default: float) -> float:
    raw = env.get(name, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be a number, got {raw!r}") from exc
    if value <= 0:
        raise ConfigError(f"{name} must be positive, got {value:g}")
    return value


def load_config(env: Mapping[str, str] | None = None, home: Path | None = None) -> GoogleConfig:
    """Resolve the credential or raise ConfigError naming everything that was searched."""
    env = os.environ if env is None else env
    home = Path.home() if home is None else home
    searched: list[str] = []
    found: dict[str, str] | None = None
    source = ""
    account: str | None = None

    # 1. environment
    env_values = {f: env.get(ENV_NAMES[f], "") for f in FIELDS}
    found = _complete(env_values)
    if found:
        source = "$GOOGLE_CLIENT_ID / $GOOGLE_CLIENT_SECRET / $GOOGLE_REFRESH_TOKEN"
    elif _partial(env_values):
        missing = [ENV_NAMES[f] for f in FIELDS if not _clean(env_values[f])]
        raise ConfigError(
            f"Google credential env vars are incomplete: {', '.join(missing)} not set. "
            "Set all three, or none to fall back to a credentials file."
        )
    searched.append("$GOOGLE_CLIENT_ID/$GOOGLE_CLIENT_SECRET/$GOOGLE_REFRESH_TOKEN")

    # 2. explicit credentials file
    if not found:
        named = env.get("GOOGLE_CREDENTIALS_FILE", "").strip()
        if named:
            path = Path(os.path.expanduser(named))
            if not path.is_file():
                raise ConfigError(f"$GOOGLE_CREDENTIALS_FILE points to {path}, which does not exist")
            data = _read_json(path)
            found = _complete(data)
            if not found:
                raise ConfigError(
                    f"{path} lacks {', '.join(f for f in FIELDS if not _clean(data.get(f)))}; "
                    "expected an authorized-user JSON with client_id, client_secret, refresh_token"
                )
            source = str(path)
        searched.append("$GOOGLE_CREDENTIALS_FILE")

    # 3. settings file, google section
    if not found:
        for cand in settings_file_candidates(env, home):
            searched.append(f"{cand} (google section)")
            if not cand.is_file():
                continue
            section = _read_json(cand).get("google")
            if not isinstance(section, dict):
                continue
            found = _complete(section)
            if found:
                source = f"{cand} (google section)"
                account = _clean(section.get("account")) or None
                break

    # 4. gws export
    if not found:
        path = home / GWS_EXPORT
        searched.append(str(path))
        if path.is_file():
            found = _complete(_read_json(path))
            if found:
                source = str(path)

    if not found:
        raise ConfigError(
            "no Google credential found. Searched: " + "; ".join(searched) + ". Provide an OAuth "
            "client_id, client_secret and refresh_token for the Google account (e.g. the output of "
            "`gws auth export --unmasked`), through any one of those."
        )

    return GoogleConfig(
        client_id=found["client_id"],
        client_secret=found["client_secret"],
        refresh_token=found["refresh_token"],
        timeout=_number(env, "GOOGLE_TIMEOUT", DEFAULT_TIMEOUT),
        max_text_chars=int(_number(env, "GOOGLE_MAX_TEXT_CHARS", DEFAULT_MAX_TEXT_CHARS)),
        credential_source=source,
        account_hint=account,
        download_dir=env.get("GOOGLE_DOWNLOAD_DIR", "").strip() or DEFAULT_DOWNLOAD_DIR,
        account_label=env.get("GOOGLE_ACCOUNT_LABEL", "").strip() or None,
    )
