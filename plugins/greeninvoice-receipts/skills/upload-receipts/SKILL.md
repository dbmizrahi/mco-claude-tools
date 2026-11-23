---
name: upload-receipts
description: Uploads new receipt files from the user's receipts folder to Morning (GreenInvoice) as expense drafts that Morning reads automatically. Use when the user says "upload my receipts", "send receipts to Morning", "add my spendings to GreenInvoice", "upload expenses", or when a scheduled receipts task runs.
---

# Upload receipts to Morning as drafts

Read `${CLAUDE_PLUGIN_ROOT}/docs/running-the-script.md` first. Morning reads each uploaded
file (OCR) and creates an expense draft; the user approves drafts in the Morning app. This
skill never creates final expenses.

If the receipts folder has no `.greeninvoice-receipts.json`, run the `setup` skill instead
(interactive) or stop and report that setup is needed (unattended).

## Steps

1. **Preview.** Run `upload --dry-run`. Nothing in `to_upload` → report that there are no new
   receipts, then stop.
2. **Approval.**
   - Interactive: show the list of files and wait for the user's go-ahead. Point out names
     that do not look like receipts or invoices (bank statements, payment summaries,
     clearing reports, tax forms) and suggest moving them out of the folder.
   - Unattended (scheduled run): continue without asking.
3. **Upload.** Run `upload`. Collect `uploaded`, `failed`, `duplicates`, `too_large`,
   `credential_warnings`.
4. **Confirm drafts.** If anything was uploaded, wait about 60 seconds, then run `drafts`.
   Morning parses files asynchronously; fewer drafts than uploads means "still processing",
   not an error.
5. **Report**, short, in the user's language:
   - Uploaded N files (names) and drafts now waiting.
   - Skipped duplicates (same content already handled).
   - Failed files with the reason. A failed file is retried on later runs, three attempts
     in total; after that it must be uploaded manually in Morning.
   - Files over 16 MB: upload manually.
   - Any credential warnings.
   - Reminder to approve drafts in the Morning app (Expenses → Drafts).
   In an unattended run, deliver the report with `SendUserMessage` when that tool exists.

## Troubleshooting

- Token error (HTTP 401/403) → the API key is wrong or revoked; the user creates a new one
  in Morning. Do not try other endpoints.
- Presign or storage errors for every file → Morning may have changed its upload flow;
  report the HTTP status and message (they never contain secrets) and stop.
