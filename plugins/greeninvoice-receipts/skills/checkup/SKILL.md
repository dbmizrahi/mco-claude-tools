---
name: checkup
description: Produces a read-only bookkeeping check-up of a Morning (GreenInvoice) account - expense drafts waiting, open and overdue invoices, missing allocation numbers on large invoices, expenses without a category, and failed receipt uploads. Use when the user asks for a "Morning check-up", "bookkeeping check", "what's pending in GreenInvoice", "VAT check", or when a scheduled check-up runs.
---

# Read-only Morning check-up

Read `${CLAUDE_PLUGIN_ROOT}/docs/running-the-script.md` first. Run only the `checkup`
command; this skill never writes anything, in Morning or on disk.

## Steps

1. Run `checkup`.
2. Report, short, in the user's language, in this order. One line when a section is empty.
   - **Drafts waiting** for approval (`drafts.drafts_waiting`, oldest).
   - **Open invoices**: number, client, amount, due date; overdue ones first.
   - **Allocation numbers** (only when `charges_vat` is true): expenses in the current VAT
     period from Israeli suppliers with net amount over ₪5,000 dated from 1 June 2026 and no
     allocation number. State that the input VAT of such an invoice should not be claimed
     until the supplier issues one. Entries with state `not_in_api_reply_check_manually`
     mean the API reply did not include the field: say they need a manual check, do not
     call them missing.
   - **Expenses without a category**, and how many expenses in the period are still open
     (not yet reported).
   - **Upload problems**: files that failed three times or are over 16 MB.
   - Any `credential_warnings`.
3. End with at most three concrete next actions.

Amounts in ₪ with two decimals. This report is not tax advice; if the user asks what to do
about a VAT question, suggest confirming with their bookkeeper or accountant.

In an unattended run, deliver the report with `SendUserMessage` when that tool exists.
