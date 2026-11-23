# greeninvoice-receipts

Upload receipt files from a folder on your computer to **Morning** (formerly
GreenInvoice / חשבונית ירוקה) as expense drafts, and get a read-only bookkeeping
check-up — from Claude Code or the Claude desktop app.

> **Unofficial.** Not affiliated with, endorsed by or supported by Morning / GreenInvoice.
> **Not tax or accounting advice** — confirm VAT questions with your bookkeeper.
> The file-upload flow is based on third-party documentation
> ([D1DX/morning-skill](https://github.com/D1DX/morning-skill)) and may change without notice.

## What it does

| Skill | Ask Claude | Writes to Morning? |
|---|---|---|
| `setup` | "set up greeninvoice-receipts" | No |
| `upload-receipts` | "upload my receipts" | Yes — **drafts only**; you approve them in Morning |
| `checkup` | "Morning check-up" | No (read-only) |
| `gmail-receipts` | "get receipts from my email" | No — saves attachments into the receipts folder |

- Finds new files (PDF, PNG, JPG, GIF, SVG, up to 16 MB) anywhere in your receipts folder.
- Skips files already handled and files with the same content under another name.
- Shows the list and waits for your OK before uploading (scheduled runs upload directly).
- Morning reads each file and creates an expense draft. Nothing becomes a final expense
  until you approve it in the Morning app.
- Never moves, renames or deletes your files. It only adds `upload-log.csv` and
  `.greeninvoice-receipts.json` (settings, no secrets) to the folder.
- Check-up: drafts waiting, open and overdue invoices, invoices over ₪5,000 net without an
  allocation number (businesses that charge VAT only), expenses without a category,
  failed uploads. Monthly or bi-monthly VAT period is read from your account.

## Requirements

- Optional, for `gmail-receipts`: a Gmail MCP server per account with `gmail_search_messages`,
  `gmail_get_message` and `gmail_download_attachment` (e.g. `google-workspace-mcp` from this
  marketplace), running on the computer that holds the receipts folder.

- A Morning account with API access and an API key.
- Python 3.9+ on the computer that holds the receipts (standard library only).
- Claude Code, or the Claude desktop app with this task linked to your computer.

## Install

Claude Code:

```
/plugin marketplace add dbmizrahi/mco-claude-tools
/plugin install greeninvoice-receipts@mco-claude-tools
```

Claude desktop app: download `greeninvoice-receipts.plugin` from the latest
[release](https://github.com/dbmizrahi/mco-claude-tools/releases) and open it.

## Set up

1. In Morning: Settings → Developer tools (כלים למפתחים) → API keys → create a key.
2. Save the key ID and secret in two files, readable only by you:

   ```bash
   mkdir -p ~/.greeninvoice && chmod 700 ~/.greeninvoice
   printf '%s' 'YOUR_KEY_ID'  > ~/.greeninvoice/apikey
   printf '%s' 'YOUR_SECRET'  > ~/.greeninvoice/secret
   chmod 600 ~/.greeninvoice/apikey ~/.greeninvoice/secret
   ```

   (Or create the two files in a text editor, which keeps the secret out of your shell
   history.) In Claude Code you can use the environment variables `GREENINVOICE_API_ID` and
   `GREENINVOICE_API_SECRET` instead. Never paste the secret into a chat.
3. Ask Claude: **"set up greeninvoice-receipts"**. It checks the connection, shows your
   business name, and offers to mark the files already in the folder as handled so they are
   never uploaded twice.

## Scheduling

Ask Claude to create scheduled tasks, for example:

- every day: "upload my receipts"
- every Sunday morning: "Morning check-up"

With the desktop app, your computer must be on and the app open when they run.

## The upload log

`upload-log.csv` in the receipts folder records every file handled:
`path, size_bytes, md5, sha256, logged_at, status, detail`.

| Status | Meaning |
|---|---|
| `baseline` | existed before setup; never uploaded |
| `uploaded` | sent to Morning; a draft is created |
| `duplicate` | same content already handled |
| `failed` | upload failed; retried on later runs, 3 attempts in total |
| `too_large` | over 16 MB; upload manually in Morning |

## Running the script directly

```bash
python3 scripts/greeninvoice_receipts.py verify   --folder ~/Receipts
python3 scripts/greeninvoice_receipts.py baseline --folder ~/Receipts --dry-run
python3 scripts/greeninvoice_receipts.py upload   --folder ~/Receipts --dry-run
python3 scripts/greeninvoice_receipts.py checkup  --folder ~/Receipts
```

Add `--creds-dir <folder>` when the key files are not in `~/.greeninvoice`.

## Development

```bash
cd plugins/greeninvoice-receipts
python3 -m unittest discover -s tests
```

Tests use a fake network layer; they never call Morning.
