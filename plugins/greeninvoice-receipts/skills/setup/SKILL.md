---
name: setup
description: Sets up greeninvoice-receipts for a Morning (GreenInvoice) account - chooses the receipts folder and the API key location, verifies the connection, and marks receipts already in the folder as handled. Use when the user says "set up greeninvoice-receipts", "connect my receipts folder to Morning", "configure GreenInvoice receipts", or before the first upload when the folder has no .greeninvoice-receipts.json.
---

# Set up greeninvoice-receipts

Read `${CLAUDE_PLUGIN_ROOT}/docs/running-the-script.md` first; it says which shell to use
and how to run the script. Explain each step in plain language before doing it, and ask
before writing anything.

## Steps

1. **Receipts folder.** Ask where receipt files are kept (any layout; month folders such as
   `2026-11/` work well). Confirm the folder exists.
2. **API key.** Ask whether the user already has a Morning API key.
   - If not, explain: in Morning, open Settings → Developer tools (כלים למפתחים) → API keys,
     create a key, and copy the key ID and the secret.
   - Recommend storing them in two files, `apikey` (key ID) and `secret`, in a private folder
     (default `~/.greeninvoice/`), readable only by the user (`chmod 600`). The user creates
     these files themselves; never ask them to paste the secret into the chat. If they paste
     it anyway, do not repeat it, and suggest they create a new key later.
   - In Claude Code, the environment variables `GREENINVOICE_API_ID` and
     `GREENINVOICE_API_SECRET` are an alternative.
3. **Verify.** Run `verify`. Show the business name, whether it charges VAT, and the VAT
   period. Relay any `credentials.warnings` (for example, loose file permissions). On error,
   explain it and stop.
4. **Existing files.** Run `baseline --dry-run` and show how many files are already in the
   folder. Explain that marking them as handled means they are never uploaded (because they
   were most likely already recorded). Ask for confirmation, then run `baseline`. If the user
   wants some existing files uploaded, tell them to move those out of the folder before the
   baseline and back in afterwards.
5. **Settings.** Add to `<receipts>/.greeninvoice-receipts.json`, with a small
   read-modify-write that keeps the keys `baseline` wrote:
   - `receipts_dir`: the receipts folder's real path on the user's computer (e.g.
     `/Users/me/Documents/Receipts`), never a `$HOME/mnt/...` mount path. Other tools that run
     on the computer, such as a Gmail server saving attachments, need it.
   - `credentials_dir`: the credentials folder as it is on the user's computer (omit when
     environment variables are used).
   - `language`: the user's language.
6. **Next steps.** Explain:
   - New receipts: drop files into the folder, then ask "upload my receipts".
   - Drafts must be approved in the Morning app (Expenses → Drafts).
   - Scheduling: the user can ask Claude to create scheduled tasks, for example a daily
     "upload my receipts" and a weekly "Morning check-up". With a linked computer, the
     computer must be on with the Claude desktop app open when they run.
