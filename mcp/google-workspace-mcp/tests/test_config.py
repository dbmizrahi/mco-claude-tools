"""Credential resolution: env, named file, settings file, gws export — one source at a time."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from google_workspace_mcp.config import ConfigError, load_config

CRED = {"client_id": "cid.apps.googleusercontent.com", "client_secret": "GOCSPX-s", "refresh_token": "1//r"}


def write(path: Path, data: object) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data) if not isinstance(data, str) else data, encoding="utf-8")
    return path


def test_env_wins_and_describe_hides_secrets(tmp_path: Path):
    write(tmp_path / ".config" / "gws" / "work.json", {**CRED, "refresh_token": "1//other"})
    cfg = load_config({"GOOGLE_CLIENT_ID": "a", "GOOGLE_CLIENT_SECRET": "secretsecret", "GOOGLE_REFRESH_TOKEN": "1//tok"}, home=tmp_path)
    assert (cfg.client_id, cfg.client_secret, cfg.refresh_token) == ("a", "secretsecret", "1//tok")
    assert cfg.credential_source.startswith("$GOOGLE_CLIENT_ID")
    shown = json.dumps(cfg.describe())
    assert "secretsecret" not in shown and "1//tok" not in shown
    assert cfg.timeout == 60.0 and cfg.max_text_chars == 50_000


def test_partial_env_is_refused(tmp_path: Path):
    with pytest.raises(ConfigError, match="GOOGLE_REFRESH_TOKEN"):
        load_config({"GOOGLE_CLIENT_ID": "a", "GOOGLE_CLIENT_SECRET": "b"}, home=tmp_path)


def test_named_credentials_file(tmp_path: Path):
    path = write(tmp_path / "creds.json", {**CRED, "type": "authorized_user"})
    cfg = load_config({"GOOGLE_CREDENTIALS_FILE": str(path)}, home=tmp_path)
    assert cfg.refresh_token == "1//r" and cfg.credential_source == str(path)


def test_named_file_missing_or_incomplete(tmp_path: Path):
    with pytest.raises(ConfigError, match="does not exist"):
        load_config({"GOOGLE_CREDENTIALS_FILE": str(tmp_path / "nope.json")}, home=tmp_path)
    path = write(tmp_path / "half.json", {"client_id": "x"})
    with pytest.raises(ConfigError, match="client_secret, refresh_token"):
        load_config({"GOOGLE_CREDENTIALS_FILE": str(path)}, home=tmp_path)


def test_settings_file_google_section(tmp_path: Path):
    write(tmp_path / ".config" / "google-workspace-mcp" / "config.json", {"google": {**CRED, "account": "me@example.com"}})
    write(tmp_path / ".config" / "gws" / "work.json", {**CRED, "refresh_token": "1//gws"})
    cfg = load_config({}, home=tmp_path)
    assert cfg.refresh_token == "1//r"
    assert cfg.credential_source.endswith("google-workspace-mcp/config.json (google section)")
    assert cfg.account_hint == "me@example.com"


def test_settings_file_from_env_var(tmp_path: Path):
    path = write(tmp_path / "elsewhere.json", {"google": CRED})
    cfg = load_config({"GOOGLE_WORKSPACE_CONFIG": str(path)}, home=tmp_path)
    assert cfg.credential_source == f"{path} (google section)"


def test_empty_section_falls_through_to_gws_export(tmp_path: Path):
    write(tmp_path / ".config" / "google-workspace-mcp" / "config.json",
          {"google": {"account": "", "client_id": "", "client_secret": "", "refresh_token": ""}})
    write(tmp_path / ".config" / "gws" / "work.json", CRED)
    cfg = load_config({}, home=tmp_path)
    assert cfg.credential_source.endswith(".config/gws/work.json")
    assert cfg.account_hint is None


def test_account_label_is_reported(tmp_path: Path):
    path = write(tmp_path / "private.json", CRED)
    cfg = load_config({"GOOGLE_CREDENTIALS_FILE": str(path), "GOOGLE_ACCOUNT_LABEL": "private"}, home=tmp_path)
    assert cfg.account_label == "private" and cfg.describe()["account_label"] == "private"
    assert load_config({"GOOGLE_CREDENTIALS_FILE": str(path)}, home=tmp_path).account_label is None


def test_nothing_found_lists_every_place(tmp_path: Path):
    with pytest.raises(ConfigError) as exc:
        load_config({}, home=tmp_path)
    msg = str(exc.value)
    assert "$GOOGLE_CREDENTIALS_FILE" in msg and "google-workspace-mcp/config.json" in msg and "gws/work.json" in msg


def test_bad_numbers(tmp_path: Path):
    env = {"GOOGLE_CLIENT_ID": "a", "GOOGLE_CLIENT_SECRET": "b", "GOOGLE_REFRESH_TOKEN": "c"}
    with pytest.raises(ConfigError, match="GOOGLE_TIMEOUT"):
        load_config({**env, "GOOGLE_TIMEOUT": "fast"}, home=tmp_path)
    with pytest.raises(ConfigError, match="positive"):
        load_config({**env, "GOOGLE_MAX_TEXT_CHARS": "0"}, home=tmp_path)
    assert load_config({**env, "GOOGLE_TIMEOUT": "7"}, home=tmp_path).timeout == 7.0
