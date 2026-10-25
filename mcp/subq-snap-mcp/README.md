# subq-snap-mcp

A Claude desktop extension (`.mcpb`) for the
[SubQ Snap](https://docs.subq.ai/endpoints/decisions-api/) decision model. It
adds one tool, `decide`: you give it a piece of content and fixed-choice
questions, and it returns a probability per answer instead of generated text.

The [`tech-llm-council`](../../plugins/tech-llm-council/README.md) plugin uses
it for optional checks; it works with any other prompt or skill too.

Part of the `mco-claude-tools` marketplace
([dbmizrahi/mco-claude-tools](https://github.com/dbmizrahi/mco-claude-tools)).

## Install

1. Download `subq-snap-mcp-<version>.mcpb` from the
   [Releases](https://github.com/dbmizrahi/mco-claude-tools/releases) page
   (tag `subq-snap-mcp-v<version>`). Optional: check it against `SHA256SUMS`.
2. Open the file in the Claude desktop app and confirm the install.
3. Enter your SubQ API key when the app asks for it. The app stores it securely;
   it is not written to any file in this repository.

Where it works: the Claude desktop app, including Cowork sessions linked to
that computer. It does not load in Claude Code or in web-only sessions.

## Settings

| Setting | Default | Purpose |
|---|---|---|
| SubQ API key | — (required) | Bearer token for the SubQ API |
| API endpoint | `https://api.subq.ai/v1/systemone` | Decisions API endpoint |
| Model | `subq-snap-1.1` | Decision model ID |
| Timeout (seconds) | `30` (1–120) | After this, the tool reports `skipped` |

## Data sent to SubQ

Everything passed to `decide` — the `state` (text, objects, file contents a
skill chose to include), the questions and any images — is sent over HTTPS to
SubQ at the configured endpoint, with your API key. Nothing else from your
computer is sent. SubQ bills per input token; output tokens are free. Read
SubQ's own terms for how they handle request data.

## The `decide` tool

Input:

```json
{
  "state": "text, an object or an array",
  "questions": {
    "worthy": { "type": "noul", "instructions": "Is this a real decision?" },
    "kind":   { "type": "choice", "criteria": { "technical": "how to build", "business_value": null } },
    "risk":   { "type": "score", "criteria": ["low", "medium", "high"] }
  },
  "images": [{ "mediaType": "image/png", "base64": "..." }]
}
```

Limits, checked before anything is sent: 1–128 questions, names up to 100
characters, `choice` 2–255 options, `score` 2–10 levels, up to 4 PNG, JPEG or
WebP images. A `noul` question needs `instructions` or `criteria`.

Output (text content, JSON):

- `{"status": "ok", "model": "...", "answers": {...}, "usage": {...}}` —
  `noul` answers carry `noul` (probability of yes); `choice` answers carry
  `choice`, `probabilities` and `confidence`; `score` answers carry `score`,
  `legend`, `probabilities` and `confidence`.
- `{"status": "skipped", "reason": "...", "http_status": 401, "detail": {...}}`
  with `isError: true` — no key, timeout, HTTP error, network error or an
  invalid request. The caller should continue without it.

## Development

```bash
npm ci
npm run typecheck      # strict TypeScript, no `any`
npm test               # node:test with a stubbed fetch, no network
npm run build          # dist/
npx mcpb validate manifest.json
```

The version lives in `package.json` and `manifest.json`; release-please bumps
both. Releases are built by the repository's release workflow, which packs the
bundle with production dependencies only.
