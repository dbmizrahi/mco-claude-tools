# tech-llm-council

Pressure-tests a software or infrastructure decision, or the business value of a
software product or SaaS, with a council of 5 professionals. They answer
independently, review each other anonymously, and a chairman writes the verdict:
where they agree, where they clash, blind spots, the recommendation and the one
thing to do first. Adapted from Andrej Karpathy's LLM Council.

Optional: [SubQ Snap](https://docs.subq.ai/endpoints/decisions-api/), a decision
model that answers fixed-choice questions with probabilities, adds measured
signals to the council through the separate `subq-snap-mcp` connector. Without
it the council runs unchanged.

Part of the `mco-claude-tools` marketplace
([dbmizrahi/mco-claude-tools](https://github.com/dbmizrahi/mco-claude-tools)).
This directory is the plugin itself; paths below are relative to it.

## Installation

### A. From the marketplace — normal use

```
/plugin marketplace add dbmizrahi/mco-claude-tools
/plugin install tech-llm-council@mco-claude-tools
```

Terminal equivalent:

```bash
claude plugin marketplace add dbmizrahi/mco-claude-tools
claude plugin install tech-llm-council@mco-claude-tools
```

The plugin is pinned to the version in its `plugin.json`; `/plugin update
tech-llm-council` picks up a new release.

### B. From a release archive — Cowork

Each release on the
[Releases](https://github.com/dbmizrahi/mco-claude-tools/releases) page
(tag `tech-llm-council-v<version>`) ships this directory under two names:

- `tech-llm-council.plugin` — open it in the Claude desktop app and accept the
  plugin from the card.
- `tech-llm-council-<version>.zip` — the same bytes, for Claude Code:

  ```bash
  shasum -a 256 -c SHA256SUMS          # optional; published alongside
  claude --plugin-dir tech-llm-council-<version>.zip
  ```

  `--plugin-dir` loads the plugin for that session only.

## Usage

Say "council this: …", "war-room this", "pressure-test this" or describe a
decision you're torn on. The skill is `tech-llm-council:tech-llm-council`.

The roster depends on the question:

| Question type | Advisors |
|---|---|
| Technical decision | Software Architect, Infrastructure Engineer, Security Engineer, Product Manager, CTO |
| Business value of a software product or SaaS | CMO, CFO, CTO, Product Manager, one technical advisor |

## SubQ Snap (optional)

Snap comes from a separate connector in this marketplace,
[`subq-snap-mcp`](../../mcp/subq-snap-mcp/README.md): a Claude desktop
extension with one tool, `decide`. Install it from the
[Releases](https://github.com/dbmizrahi/mco-claude-tools/releases) page
(`subq-snap-mcp-<version>.mcpb`), open it in the Claude desktop app and enter
your SubQ API key there. The app stores the key securely; this plugin never
sees or asks for it.

Without the connector, or when a call fails (no key, timeout, HTTP error), the
council runs unchanged. The verdict ends with one line saying whether Snap was
used or skipped.

Where Snap works: the Claude desktop app, including Cowork sessions linked to
that computer. Not in Claude Code or web-only sessions, which don't load
desktop extensions.

What Snap adds:

| Step | Snap question | Used for |
|---|---|---|
| 1. Roster | worth a council? / technical or business / which technical advisor | advice on the roster; Claude still decides |
| 1. Facts | per file: relevant? draft? | picking context files, excluding drafts |
| 3. Peer review | which response is strongest (A–E, run twice with shuffled letters) | a signal for the chairman |
| 4. Chairman | do these two advisors reach the same recommendation? (10 pairs) | checking agreement and clashes |

The five advisors, the five text reviewers and the chairman stay as they are.
Snap answers are signals, not votes.

Data sent to SubQ: the user's question, the framed question, the advisor
responses and, in step 1, the contents of candidate project files. SubQ
bills per input token; output is free. A council session makes 4 Snap calls,
plus one or more in step 1 when it pre-selects files.
