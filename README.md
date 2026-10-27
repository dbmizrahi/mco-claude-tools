# mco-claude-tools

A public Claude plugin marketplace, `mco-claude-tools`: plugins, connectors
(Claude desktop extensions) and standalone skills for Claude Code and Cowork,
hosted at
[dbmizrahi/mco-claude-tools](https://github.com/dbmizrahi/mco-claude-tools)
and served from its `main` branch.

## Plugins

| Plugin | What it does | Docs |
|---|---|---|
| `tech-llm-council` | Pressure-tests a software, infrastructure or SaaS business decision with 5 technical, product and business advisors, anonymous peer review and a chairman verdict; with the optional `subq-snap-mcp` connector, SubQ Snap picks each advisor's answer and the chairman's verdict from fixed answer options, improving them until one is a clear winner | [plugins/tech-llm-council](plugins/tech-llm-council/README.md) |

## Connectors

MCP servers released as Claude desktop extensions (`.mcpb`). They are not
served by the plugin marketplace: download the `.mcpb` from the release and
open it in the Claude desktop app, which asks for the connector's settings and
stores secrets securely.

| Connector | What it does | Docs |
|---|---|---|
| `subq-snap-mcp` | SubQ Snap decision model as one tool, `decide`: fixed-choice questions about content, a probability per answer | [mcp/subq-snap-mcp](mcp/subq-snap-mcp/README.md) |

## Installing

Inside Claude Code (or `claude plugin …` in a terminal):

```
/plugin marketplace add dbmizrahi/mco-claude-tools
/plugin install <plugin>@mco-claude-tools
```

The repo is public, so no access is needed. A plugin is pinned to the version
in its `plugin.json`; `/plugin update <plugin>` therefore only changes
something after a release.

Cowork: every GitHub release carries `<plugin>.plugin` — download it and open it
in the Claude desktop app. The same archive is published as
`<plugin>-<version>.zip`, which Claude Code loads for one session with
`claude --plugin-dir <zip>`.

Each plugin's README says what to do after installing it.

## Layout

```
.claude-plugin/marketplace.json     the catalogue: one entry per plugin
plugins/<name>/                     a plugin: .claude-plugin/plugin.json, skills/, agents/, …
mcp/<name>/                         a connector: manifest.json (MCPB), package.json, src/, test/
skills/<name>/SKILL.md              standalone skills, used outside any plugin (see below)
scripts/ci/validate_repo.py         repo validator, run in CI and locally
.github/workflows/                  validation and release automation
release-please-config.json          one release-please package per plugin
.release-please-manifest.json       the released version of each plugin
```

One rule holds everything together: **a plugin's directory name is its name
everywhere** — the marketplace entry, `plugin.json`, the release-please
`package-name`, and the prefix of its release tag `<name>-v<version>`. The
validator fails on any mismatch. Versions live in `plugin.json` only; the
marketplace entry carries none. The same rule holds for a connector: its
directory name is the `name` in `manifest.json` and `package.json`, the
release-please `package-name` and the tag prefix.

## Standalone skills

`skills/<name>/SKILL.md` holds skills that are not part of any plugin. A
marketplace can only serve plugins, so these are used by copying:

```bash
cp -R skills/<name> ~/.claude/skills/<name>            # personal: every project
cp -R skills/<name> <project>/.claude/skills/<name>    # one project
```

They are validated (frontmatter parses, `name` equals the directory) but not
released. A skill that should be installable or versioned belongs in a plugin.

## Adding a plugin

1. Create `plugins/<name>/` with `.claude-plugin/plugin.json` (`name`, `version`,
   `description`), the `skills/`, `agents/` and other component directories, and
   a `README.md`. Ship no credentials: keys are read from environment variables
   or from a file outside the repo.
2. Add an entry to `.claude-plugin/marketplace.json`: `name`,
   `"source": "./plugins/<name>"`, `description`, optionally `category`.
   No `version`.
3. Add a package to `release-please-config.json`:
   ```json
   "plugins/<name>": {
     "package-name": "<name>",
     "changelog-path": "CHANGELOG.md",
     "extra-files": [
       { "type": "json", "path": ".claude-plugin/plugin.json", "jsonpath": "$.version" }
     ]
   }
   ```
   and seed `.release-please-manifest.json` with `"plugins/<name>": "<version>"`,
   the same value as in `plugin.json`.
4. Run the validation below; it checks all of the above against each other.

## Adding a connector

1. Create `mcp/<name>/` with a `manifest.json` (MCPB, `server.type: node`), a
   `package.json` with the same `name` and `version`, a committed
   `package-lock.json`, strict TypeScript sources and tests, and a `README.md`
   that says what data the connector sends where. Secrets come only from
   `user_config` fields marked `sensitive: true`, passed to the server as
   `${user_config.<field>}` in `mcp_config.env`.
2. Add a package to `release-please-config.json`:
   ```json
   "mcp/<name>": {
     "release-type": "node",
     "package-name": "<name>",
     "changelog-path": "CHANGELOG.md",
     "extra-files": [
       { "type": "json", "path": "manifest.json", "jsonpath": "$.version" }
     ]
   }
   ```
   and seed `.release-please-manifest.json` with `"mcp/<name>": "<version>"`.
3. The package must provide `npm run typecheck`, `npm test` and `npm run build`
   (output in `dist/`); `validate.yml` runs them on every pull request, then
   validates the manifest and packs a test bundle.

## Releases

Versions come from [conventional commits](https://www.conventionalcommits.org/)
that touch a plugin's or connector's directory — nothing is bumped by hand, and
nobody merges release PRs by hand either:

| Commit prefix | Effect on that package |
|---|---|
| `fix: …` | patch |
| `feat: …` | minor |
| `feat!: …` or a `BREAKING CHANGE:` footer | major |
| `docs:`, `chore:`, `refactor:`, `test:`, `ci:` | no release |

On each push to `main`, `release-please.yml` runs the whole release with no
manual step:

1. release-please opens or updates **one combined Release PR** with every
   package that has releasable commits: it bumps each plugin's `plugin.json` (or
   each connector's `package.json`, `package-lock.json` and `manifest.json`) and
   writes its `CHANGELOG.md`.
2. The Release PR's exact head commit is validated with `validate.yml` — the
   same checks as any other PR.
3. If the checks pass, the workflow squash-merges exactly that commit. It merges
   only PRs opened by `github-actions` with the `autorelease: pending` label and
   bot-only commits, and only while the PR contains the current `main`.
4. It then creates each package's tag `<name>-v<version>` and GitHub release,
   and builds and attaches the assets.

Your own PRs are never merged automatically. If someone pushes to a Release
PR's branch, that PR is left for review too. If validation fails, nothing is
released; the next push to `main` rebuilds the Release PR and tries again.

A plugin release attaches `<name>-<version>.zip`, `<name>.plugin` (identical
bytes, the Cowork name) and `SHA256SUMS`. The archive is the plugin directory
alone, with `plugin.json` at its root, and is validated again after extraction
before it is published.

A commit that does not follow the convention produces no version bump, so if no
release follows a merge, check the commit message first.
Commits outside `plugins/<name>/` and `mcp/<name>/` never release anything.

A connector release attaches `<name>-<version>.mcpb` and `SHA256SUMS`. The
bundle holds the manifest, the compiled server, the README and production
dependencies only, and is unpacked and checked again before it is published.

To release by hand — the first release of a new plugin, or recovering from a
broken bot run — push the tag and `release.yml` runs the same build:

```bash
git tag tech-llm-council-v0.1.0 && git push origin tech-llm-council-v0.1.0
```

The tag must equal `<name>-v<version in plugin.json>`, or the build refuses.

### Repository settings the automation needs

- **Settings → Actions → General → Workflow permissions → "Allow GitHub Actions
  to create and approve pull requests"**. Without it release-please fails with
  "GitHub Actions is not permitted to create or approve pull requests";
  `permissions: pull-requests: write` in the workflow is necessary but not
  sufficient.
- `main` is the default branch: `/plugin marketplace add owner/repo` follows
  the default branch, so merging to `main` is what publishes.
- Branch rules on `main` that require reviews or status checks would block the
  automatic merge of Release PRs unless GitHub Actions may bypass them.
  Release PRs get no status checks of their own (PRs opened with
  `GITHUB_TOKEN` don't trigger workflows); they are validated inside
  `release-please.yml` instead.

## Validation

Runs on every push and pull request to `main` and `develop` (`validate.yml`):
the repo validator, the official plugin validator, and a build of every
connector (typecheck, tests, build, `mcpb validate`, test pack). Run it
locally before pushing, from the repo root:

```bash
pip install pyyaml
python3 scripts/ci/validate_repo.py        # the gate
claude plugin validate .                   # official validator: marketplace manifest
claude plugin validate plugins/<name>      # official validator: one plugin manifest
(cd mcp/<name> && npm ci && npm run typecheck && npm test && npm run build && npx mcpb validate manifest.json)
```

`validate_repo.py` is the gate. It catches what the official validator accepts
without complaint: a marketplace `source` pointing at a directory that does not
exist, malformed YAML frontmatter in a `SKILL.md` or agent file (which breaks
installation at load time), an unlisted plugin directory, drift between
`marketplace.json`, `plugin.json` and the release-please files, and committed
credentials or token-shaped strings. `--plugin <dir>` validates one plugin on
its own; the release build runs it on the extracted archive.
