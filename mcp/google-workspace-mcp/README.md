# google-workspace-mcp

MCP server that gives Claude (Claude Code, the Claude desktop app, any MCP client) access to
one Google account's **Gmail, Calendar, Drive, Docs, Sheets, Slides and Chat** through
Google's REST APIs. Python, stdio transport.

It signs in with an OAuth **refresh token** and mints short-lived access tokens itself. Every
call runs as the account behind that token, limited to the scopes it was granted. Writes are
enabled; the tool annotations mark them so the client can ask before running them.

**Several accounts:** one running server = one Google account. To use, say, a private Gmail and
a work account together, register the server twice with different credential files and labels
([below](#two-accounts-side-by-side)).

## Requirements

- Python 3.10+ and [`uv`](https://docs.astral.sh/uv/) (or pip).
- A Google Cloud project with an OAuth client of type **Desktop app** and the APIs you need
  enabled — see [Google Cloud setup](#google-cloud-setup).
- A credential file per account, made once with `google-workspace-mcp auth`.

## Google Cloud setup

Done once; one OAuth client can serve all your accounts. Menu names are those of the Google
Cloud console at the time of writing.

1. **Project.** Open <https://console.cloud.google.com/>, project picker → **New project**, any
   name (e.g. `claude-google-workspace`).
2. **APIs.** **APIs & Services → Library**, enable what you will use: **Gmail API** (required for
   mail), and optionally Google Calendar API, Google Drive API, Google Docs API, Google Sheets API,
   Google Slides API, Google Chat API. With the `gcloud` CLI:

   ```bash
   gcloud services enable gmail.googleapis.com calendar-json.googleapis.com drive.googleapis.com \
       docs.googleapis.com sheets.googleapis.com slides.googleapis.com chat.googleapis.com \
       --project <project-id>
   ```
3. **Consent screen.** **Google Auth Platform → Get started** (older consoles: *OAuth consent
   screen*). App name, your support email, **Audience: External** (needed for a personal
   `@gmail.com` account), contact email → **Create**.
4. **Publish it.** **Audience → Publish app** (status *In production*). While an External app is
   in *Testing*, Google expires its refresh tokens after **7 days** and you would have to sign in
   again every week. A published app that Google has not verified still works for you: the
   sign-in page shows *"Google hasn't verified this app"* → **Advanced → Go to … (unsafe)**. That
   warning is about your own app; unverified apps are limited to 100 users.
5. **Scopes.** **Data Access → Add or remove scopes**: add the ones you will request — for mail
   `…/auth/gmail.modify` (or `…/auth/gmail.readonly`), plus `openid` and `…/auth/userinfo.email`.
6. **Client.** **Clients → Create client → Application type: Desktop app** → **Create** →
   **Download JSON**. Keep the file private (it holds the client secret); move it out of
   `~/Downloads`, e.g. to `~/.config/google-workspace-mcp/client.json` with `chmod 600`.

**Work (Google Workspace) accounts.** Your Workspace admin may block third-party apps. If sign-in
says the app is blocked, ask the admin to trust your client ID (Admin console → Security →
Access and data control → API controls → App access control). Alternatively, create a second
project inside your work organisation with **Audience: Internal**: internal apps need no
publishing or verification and their tokens do not expire weekly, but they only accept accounts
of that organisation — so the private account keeps using the External client.

## Sign in (once per account)

Run on the computer with the browser. The command opens Google's sign-in page, catches the
redirect on `127.0.0.1`, and writes an *authorized user* file with mode 600. It never prints the
client secret or the refresh token.

```bash
cd /path/to/mcp/google-workspace-mcp
uv run google-workspace-mcp auth --client-file ~/.config/google-workspace-mcp/client.json \
    --out ~/.config/google-workspace-mcp/private.json --login-hint me@gmail.com
uv run google-workspace-mcp auth --client-file ~/.config/google-workspace-mcp/client.json \
    --out ~/.config/google-workspace-mcp/work.json --login-hint me@company.com
```

`--scopes` picks what the account may do: `gmail-read` (read mail, save attachments), `gmail`
(default: read, label, draft, send), `all` (everything this server supports — enable the
matching APIs first). Without `--client-file`, it asks for the client ID and secret (hidden).
`--force` replaces an existing file. "No refresh token" means Google already granted this
client once: remove it at <https://myaccount.google.com/permissions> and run `auth` again.

Check a file without starting MCP — prints the source, account and scopes, never the secrets:

```bash
GOOGLE_CREDENTIALS_FILE=~/.config/google-workspace-mcp/private.json uv run google-workspace-mcp check
```

## Configuration

`client_id`, `client_secret` and `refresh_token` come from **one** source — the first complete one of:

| # | Source |
|---|---|
| 1 | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` environment variables |
| 2 | The JSON file named by `GOOGLE_CREDENTIALS_FILE` (what `auth` writes, or `gws auth export --unmasked`) |
| 3 | The `google` section of `$GOOGLE_WORKSPACE_CONFIG`, else `~/.config/google-workspace-mcp/config.json` |
| 4 | `~/.config/gws/work.json` |

Optional:

| Variable | Default | Meaning |
|---|---|---|
| `GOOGLE_ACCOUNT_LABEL` | — | Name shown by `google_whoami` and `check`, e.g. `private` / `work` |
| `GOOGLE_TIMEOUT` | `60` | Request timeout in seconds |
| `GOOGLE_MAX_TEXT_CHARS` | `50000` | Cap on message, document and file text returned in one call |
| `GOOGLE_DOWNLOAD_DIR` | `~/Downloads` | Where downloads, exports, attachments and slide images go when no path is given |

Downloads, exports and uploads use the file system of the machine the server runs on.

## Two accounts side by side

Register the server twice. Each copy reads its own credential file and answers only for its own
account; the label makes it obvious which one a result came from.

**Claude desktop app** — Settings → Developer → Edit Config (`claude_desktop_config.json`), then
restart the app. Use the absolute path of `uv` (`which uv`), because the app does not use your
shell's `PATH`:

```json
{
  "mcpServers": {
    "google-private": {
      "command": "/opt/homebrew/bin/uv",
      "args": ["run", "--directory", "/path/to/mcp/google-workspace-mcp", "google-workspace-mcp"],
      "env": {
        "GOOGLE_CREDENTIALS_FILE": "/Users/me/.config/google-workspace-mcp/private.json",
        "GOOGLE_ACCOUNT_LABEL": "private"
      }
    },
    "google-work": {
      "command": "/opt/homebrew/bin/uv",
      "args": ["run", "--directory", "/path/to/mcp/google-workspace-mcp", "google-workspace-mcp"],
      "env": {
        "GOOGLE_CREDENTIALS_FILE": "/Users/me/.config/google-workspace-mcp/work.json",
        "GOOGLE_ACCOUNT_LABEL": "work"
      }
    }
  }
}
```

**Claude Code:**

```bash
claude mcp add google-private --scope user \
  -e GOOGLE_CREDENTIALS_FILE=$HOME/.config/google-workspace-mcp/private.json -e GOOGLE_ACCOUNT_LABEL=private \
  -- uv run --directory /path/to/mcp/google-workspace-mcp google-workspace-mcp
claude mcp add google-work --scope user \
  -e GOOGLE_CREDENTIALS_FILE=$HOME/.config/google-workspace-mcp/work.json -e GOOGLE_ACCOUNT_LABEL=work \
  -- uv run --directory /path/to/mcp/google-workspace-mcp google-workspace-mcp
```

The config holds only file paths, no secrets. Then ask Claude to run `google_whoami` on each.

## Other ways to run it

### As an installed package

```bash
uv tool install /path/to/mcp/google-workspace-mcp     # or: pipx install /path/to/mcp/google-workspace-mcp
google-workspace-mcp --version
```

Re-run with `--force` after pulling changes. Releases also attach a wheel
(`google_workspace_mcp-<version>-py3-none-any.whl`) for `pip install`. Use `"command":
"google-workspace-mcp"` (absolute path if not on `PATH`; `uv tool install` puts it in
`~/.local/bin`) in the configs above instead of `uv run --directory …`.

### Docker

```bash
docker build -t google-workspace-mcp /path/to/mcp/google-workspace-mcp
docker run -i --rm -e GOOGLE_CREDENTIALS_FILE=/creds/private.json -e GOOGLE_ACCOUNT_LABEL=private \
    -v "$HOME/.config/google-workspace-mcp:/creds:ro" google-workspace-mcp check
```

The container runs as user `google`. `-i` keeps stdin open for the MCP stream; do not add `-t`.
Mount a folder for downloads if you use them (e.g. `-v "$HOME/Downloads:/home/google/Downloads"`).
Sign in (`auth`) on the host, not in the container: it needs your browser.

## Tools

| Tool | What it does |
|---|---|
| `google_whoami` | Verify the sign-in; account email, granted scopes, which services they cover |
| `google_api_request` | Call any `https://*.googleapis.com` endpoint (Tasks, People, permissions, …) |
| `gmail_search_messages` | Search with Gmail query syntax; summary per message |
| `gmail_get_message` | One message: headers, text body, attachment list |
| `gmail_get_thread` | Whole conversation |
| `gmail_list_labels` | Label ids and names |
| `gmail_download_attachment` | Save one attachment to a local file (up to 25 MB); returns path, size, sha256 — never the bytes |
| `gmail_modify_labels` | Mark read, archive, star, trash, apply labels |
| `gmail_create_draft` | Draft, optionally as a reply in a thread |
| `gmail_send_message` | Send now, optionally as a reply |
| `calendar_list_calendars` | Calendars with access role and time zone |
| `calendar_list_events` | Events in a window (bare dates use the calendar's time zone), recurring expanded |
| `calendar_get_event` | One event with attendee responses |
| `calendar_create_event` | Create, optionally with attendees and invitations |
| `calendar_update_event` | Change fields, or RSVP to an invitation |
| `calendar_delete_event` | Delete |
| `drive_search_files` | Find files by name, content, type, folder, date |
| `drive_get_file` | File metadata |
| `drive_read_file` | Content as text: Docs/Slides exported, Sheets as CSV, text files downloaded |
| `drive_create_folder` | New folder |
| `drive_upload_file` | Upload a local file, optionally converting to Doc/Sheet/Slides |
| `drive_download_file` | Save a regular file (PDF, image, Office, zip) to disk |
| `drive_export_file` | Save a Doc/Sheet/Slides/Drawing as pdf, docx, xlsx, pptx, md, csv, … |
| `drive_copy_file` | Copy a file |
| `drive_update_file` | Rename, move, describe, star |
| `drive_trash_file` | Move to trash, or restore |
| `drive_delete_file` | Delete permanently |
| `drive_list_permissions` | Who has access |
| `drive_share_file` | Share with a person, a domain, or anyone with the link |
| `drive_unshare_file` | Remove one permission |
| `drive_list_shared_drives` | Shared drives the account belongs to |
| `docs_get_document` | A Doc as plain text |
| `docs_get_outline` | Headings with their character positions |
| `docs_export_text` | A Doc as Markdown or plain text |
| `docs_create_document` | New Doc with optional text |
| `docs_append_text` | Append text |
| `docs_insert_text` | Insert text at a position |
| `docs_replace_text` | Find and replace |
| `docs_batch_update` | Raw Docs API requests: styles, headings, bullets, tables, images |
| `sheets_get_spreadsheet` | Title and tabs |
| `sheets_read_values` | Read a range |
| `sheets_batch_read` | Read several ranges at once |
| `sheets_update_values` | Overwrite a range |
| `sheets_append_values` | Append rows |
| `sheets_clear_values` | Clear a range |
| `sheets_create_spreadsheet` | New spreadsheet |
| `sheets_add_sheet` / `sheets_rename_sheet` / `sheets_delete_sheet` | Manage tabs |
| `sheets_batch_update` | Raw Sheets API requests: formatting, sorting, filters, charts |
| `slides_get_presentation` | Every slide's elements (ids, placeholders, text) and speaker notes |
| `slides_create_presentation` | New presentation |
| `slides_add_slide` | Add a slide with a layout, optionally filling title and body |
| `slides_duplicate_slide` | Duplicate a slide |
| `slides_delete_object` | Delete a slide or an element |
| `slides_replace_text` | Find and replace across slides (template markers) |
| `slides_set_text` | Replace or append the text of a shape |
| `slides_get_thumbnail` | Render a slide to PNG |
| `slides_batch_update` | Raw Slides API requests: shapes, images, tables, styles, notes |
| `chat_list_spaces` | Chat spaces, group chats, direct messages |
| `chat_list_messages` | Messages of a space in a time window |
| `chat_send_message` | Post to a space or thread |

A tool whose scope the refresh token lacks fails with a message naming the
granted scopes. Other errors carry a hint: a dead refresh token (re-login), an
API not enabled in the Cloud project (`gcloud services enable …`), rate limits.

## Development

```bash
cd mcp/google-workspace-mcp
uv sync --group dev
uv run pytest
uv run mcp dev src/google_workspace_mcp/server.py     # MCP Inspector
```

Tests run against a mocked HTTP transport and the SDK's in-memory client; nothing reaches Google.

## License

MIT — see the repository [LICENSE](../../LICENSE).
