#!/usr/bin/env python3
"""Structural and safety checks for the mco-claude-tools marketplace repo.

Runs in CI and locally, from the repo root:

    python3 scripts/ci/validate_repo.py                  # the whole marketplace
    python3 scripts/ci/validate_repo.py --root <dir>     # a checkout somewhere else
    python3 scripts/ci/validate_repo.py --plugin <dir>   # one plugin on its own
                                                         # (an extracted release archive)

Why this exists alongside `claude plugin validate`
--------------------------------------------------
The official validator is the authority on manifest shape and is run separately
in CI, on the marketplace root and on every plugin directory. Measured against
CLI 2.1.274, it does NOT catch things that ship a broken or unsafe plugin:

  * a marketplace `source` pointing at a directory that does not exist
  * a SKILL.md or agent file whose YAML frontmatter is malformed (this has
    broken a real install before: bare `<example>` blocks placed directly in
    frontmatter)
  * drift between the marketplace, plugin.json and the release-please files —
    a release-please package key that no longer matches a plugin directory
    silently means "this plugin never releases again"
  * committed credentials

All of that is covered below, plus the connectors in mcp/<name>/ (MCP servers
released as Claude desktop extensions, .mcpb). The layout rule the checks enforce:

    directory name == marketplace entry name == plugin.json name
                   == release-please package-name == release tag prefix

and, for a connector, directory name == manifest.json name == package.json name
== release-please package-name == release tag prefix.

so that `plugins/<name>/` releases as `<name>-v<version>` and nothing has to
be looked up twice.

Exit code 0 = all checks passed, 1 = at least one failure.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment problem, not a repo problem
    print("FATAL: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

PLUGINS_DIR = "plugins"          # where marketplace plugins live
SKILLS_DIR = "skills"            # standalone skills, outside any plugin
MCP_DIR = "mcp"                  # connectors: MCP servers released as .mcpb
RP_CONFIG = "release-please-config.json"
RP_MANIFEST = ".release-please-manifest.json"

KEBAB_RE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
SEMVER_RE = re.compile(r"\d+\.\d+\.\d+")

# Files that must never be committed: .mcp.json is rendered with live tokens,
# *.bak-* is editor/script scratch. Matched anywhere in the tree.
FORBIDDEN_GLOBS = [
    "**/.mcp.json", "**/*.bak-*",
]

# Credential shapes. Kept deliberately narrow to avoid false positives on docs.
SECRET_PATTERNS = [
    (r"xox[baprs]-[0-9A-Za-z-]{10,}", "Slack token"),
    (r"GOCSPX-[0-9A-Za-z_-]{10,}", "Google OAuth client secret"),
    (r"1//0[0-9A-Za-z_-]{20,}", "Google refresh token"),
    (r"[0-9]{10,}-[0-9a-z]{20,}\.apps\.googleusercontent\.com", "Google client id"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"\b[a-f0-9]{40}\b", "40-hex secret"),
]

# Scanned for secrets. Binary, vendored and build paths are skipped.
SCAN_SUFFIXES = {".py", ".sh", ".json", ".md", ".yml", ".yaml", ".txt", ".cfg", ".toml"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "dist", "dist-test", "build-check"}

# Placeholders that legitimately sit where a secret would go. A line containing
# one is not scanned. Empty until a plugin ships a template with placeholders.
PLACEHOLDER_TOKENS: set[str] = set()

# A git SHA is 40 hex characters, exactly like the 40-hex pattern above,
# and SHAs are all over a repo's generated content: release-please changelogs
# link every commit, actions are SHA-pinned for supply-chain safety, docs cite
# revisions. Flagging those is noise, and blanket-exempting whole files would
# hide a real leak sitting next to them.
#
# So instead of skipping such lines, cut the SHA-bearing *substrings* out and
# scan what remains. A commit link stops matching; a key hardcoded elsewhere on
# the same line still does.
GIT_SHA_CONTEXT_RE = re.compile(
    r"uses:\s*[\w.\-]+/[\w.\-/]+@[0-9a-f]{40}"                 # SHA-pinned action
    r"|/(?:commit|commits|compare|tree|blob|raw)/"             # git hosting paths
    r"[^\s)\"'<>]*[0-9a-f]{40}"
)


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.checks = 0

    def check(self, ok: bool, label: str, detail: str = "") -> bool:
        self.checks += 1
        if ok:
            print(f"  ok    {label}")
        else:
            print(f"  FAIL  {label}" + (f"\n          {detail}" if detail else ""))
            self.failures.append(label)
        return ok


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def load_json(path: Path, rep: Report, label: str):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        rep.check(False, label, f"missing file: {path}")
    except json.JSONDecodeError as exc:
        rep.check(False, label, f"invalid JSON in {path}: {exc}")
    return None


def parse_frontmatter(path: Path):
    """Return (data, error). Mirrors how the plugin loader reads frontmatter."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None, "no YAML frontmatter (file must start with '---')"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "frontmatter is never closed with '---'"
    try:
        data = yaml.safe_load(text[3:end])
    except yaml.YAMLError as exc:
        return None, f"frontmatter is not valid YAML: {str(exc).splitlines()[0]}"
    if not isinstance(data, dict):
        return None, f"frontmatter parsed as {type(data).__name__}, expected a mapping"
    return data, None


def inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


# ------------------------------------------------------------ plugin checks
def check_skill_frontmatter(path: Path, rel: str, rep: Report) -> None:
    data, err = parse_frontmatter(path)
    if err:
        rep.check(False, f"{rel} frontmatter", err)
        return
    if not rep.check(
        bool(data.get("name")) and bool(data.get("description")),
        f"{rel} has name + description",
    ):
        return
    if path.name == "SKILL.md":
        rep.check(
            data["name"] == path.parent.name,
            f"{rel} name matches its directory",
            f"frontmatter name {data['name']!r} vs directory {path.parent.name!r}",
        )


def check_plugin(plugin_dir: Path, tag: str, rep: Report) -> dict | None:
    """Everything that must hold inside one plugin directory.

    `tag` prefixes the check labels (the plugin name, or the directory in
    --plugin mode). Returns the parsed plugin.json, or None if it is unusable.
    """
    plugin = load_json(plugin_dir / ".claude-plugin" / "plugin.json", rep,
                       f"{tag} plugin.json parses")
    if plugin is None:
        return None

    for field in ("name", "version", "description"):
        rep.check(bool(plugin.get(field)), f"{tag} plugin.json has {field}")
    name = str(plugin.get("name", ""))
    rep.check(bool(KEBAB_RE.fullmatch(name)), f"{tag} plugin name is kebab-case", f"got {name!r}")
    version = str(plugin.get("version", ""))
    rep.check(bool(SEMVER_RE.fullmatch(version)), f"{tag} plugin version is semver", f"got {version!r}")

    # The official validator does not parse these. A bad one breaks installation.
    targets = sorted(plugin_dir.glob("skills/*/SKILL.md")) + sorted(plugin_dir.glob("agents/*.md"))
    rep.check(bool(targets), f"{tag} has skills or agents to check")
    for path in targets:
        check_skill_frontmatter(path, f"{tag}/{path.relative_to(plugin_dir)}", rep)

    return plugin


# ------------------------------------------------------- marketplace checks
def resolve_source(root: Path, marketplace: dict, source: str) -> Path:
    """Relative sources resolve against the marketplace root; bare names
    resolve under metadata.pluginRoot, as Claude Code does."""
    plugin_root = (marketplace.get("metadata") or {}).get("pluginRoot")
    if "/" not in source and plugin_root:
        return root / plugin_root / source
    return root / source


def check_marketplace(root: Path, rep: Report) -> tuple[dict | None, dict[str, dict]]:
    """Validate the catalogue. Returns (marketplace, plugins) where plugins maps
    each local plugin name to {"dir": Path, "rel": str, "manifest": dict|None}."""
    marketplace = load_json(root / ".claude-plugin" / "marketplace.json", rep,
                            "marketplace.json parses")
    if marketplace is None:
        return None, {}

    rep.check(bool(marketplace.get("name")), "marketplace has a name")
    owner = marketplace.get("owner")
    rep.check(
        isinstance(owner, dict) and bool(owner.get("name")),
        "marketplace has owner.name",
        "owner must be an object with a name",
    )
    entries = marketplace.get("plugins")
    if not rep.check(isinstance(entries, list) and bool(entries), "marketplace lists plugins"):
        return marketplace, {}

    plugins: dict[str, dict] = {}
    for i, entry in enumerate(entries):
        name = str(entry.get("name", ""))
        tag = f"plugins[{i}] ({name or '?'})"
        rep.check(bool(KEBAB_RE.fullmatch(name)), f"{tag} name is kebab-case", f"got {name!r}")
        # The version is pinned in plugin.json only. Claude Code always prefers
        # the plugin.json value, so a copy here can only ever be stale or wrong.
        rep.check(
            "version" not in entry,
            f"{tag} has no version field",
            "the version lives in plugin.json only; release-please bumps it there",
        )

        src = entry.get("source")
        if not isinstance(src, str):
            rep.check(True, f"{tag} source is remote (not path-checked)")
            continue
        target = resolve_source(root, marketplace, src)
        label = f"{tag} source resolves"
        if not inside(target, root):
            rep.check(False, label, f"{src!r} escapes the marketplace root")
            continue
        if not target.is_dir():
            rep.check(False, label, f"{src!r} is not a directory")
            continue
        if not rep.check((target / ".claude-plugin" / "plugin.json").is_file(), label,
                         f"{src!r} has no .claude-plugin/plugin.json"):
            continue
        rel = str(target.resolve().relative_to(root.resolve()))
        rep.check(
            target.name == name,
            f"{tag} directory name equals the entry name",
            f"source {src!r} vs name {name!r}",
        )
        plugins[name] = {"dir": target, "rel": rel, "manifest": None}
    return marketplace, plugins


def check_orphans(root: Path, plugins: dict[str, dict], rep: Report) -> None:
    """A plugin directory that is not in the catalogue is a mistake, not a draft."""
    listed = {info["dir"].resolve() for info in plugins.values()}
    orphans = [
        str(p.parent.parent.relative_to(root))
        for p in sorted((root / PLUGINS_DIR).glob("*/.claude-plugin/plugin.json"))
        if p.parent.parent.resolve() not in listed
    ]
    rep.check(
        not orphans,
        f"every {PLUGINS_DIR}/* plugin is listed in marketplace.json",
        "unlisted: " + ", ".join(orphans) if orphans else "",
    )


def check_standalone_skills(root: Path, rep: Report) -> None:
    """skills/<name>/SKILL.md — shipped outside any plugin, copied by hand."""
    skills_dir = root / SKILLS_DIR
    if not skills_dir.is_dir():
        return
    targets = sorted(skills_dir.glob("*/SKILL.md"))
    if not targets:
        rep.check(True, f"{SKILLS_DIR}/ has no standalone skills yet")
        return
    for path in targets:
        check_skill_frontmatter(path, str(path.relative_to(root)), rep)


# --------------------------------------------------------- connector checks
MANIFEST_REQUIRED = ("manifest_version", "name", "version", "description", "author", "server")
SECRET_NAME_RE = re.compile(r"(key|token|secret|password)", re.IGNORECASE)
USER_CONFIG_REF_RE = re.compile(r"^\$\{user_config\.[A-Za-z_][A-Za-z0-9_]*\}$")
BUILD_OUTPUT_RE = re.compile(r"(^|/)(node_modules|dist|dist-test)/|\.mcpb$")


def tracked_files(root: Path, rel: str) -> list[str] | None:
    """Files git tracks under `rel`, or None when git cannot tell (no repo)."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--", rel],
            capture_output=True, text=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return [line for line in out.stdout.splitlines() if line]


def check_connectors(root: Path, rep: Report) -> dict[str, dict]:
    """mcp/<name>/ — MCP servers released as Claude desktop extensions (.mcpb).

    The same naming rule as plugins: directory == manifest.json name ==
    package.json name == release-please package-name == tag prefix. Returns
    name -> {"dir", "rel", "version"} for the release-please checks."""
    connectors: dict[str, dict] = {}
    mcp_dir = root / MCP_DIR
    if not mcp_dir.is_dir():
        return connectors
    dirs = sorted(p for p in mcp_dir.iterdir() if p.is_dir() and p.name not in SKIP_DIRS)
    if not dirs:
        rep.check(True, f"{MCP_DIR}/ has no connectors yet")
        return connectors

    for cdir in dirs:
        name = cdir.name
        tag = f"{MCP_DIR}/{name}"
        manifest = load_json(cdir / "manifest.json", rep, f"{tag} manifest.json parses")
        if manifest is None:
            continue
        missing = [f for f in MANIFEST_REQUIRED if not manifest.get(f)]
        rep.check(not missing, f"{tag} manifest has required fields", "missing: " + ", ".join(missing))
        author = manifest.get("author")
        rep.check(isinstance(author, dict) and bool(author.get("name")), f"{tag} manifest has author.name")
        rep.check(bool(KEBAB_RE.fullmatch(name)), f"{tag} directory name is kebab-case", f"got {name!r}")
        rep.check(manifest.get("name") == name, f"{tag} manifest name equals the directory name",
                  f"manifest says {manifest.get('name')!r}")
        version = str(manifest.get("version", ""))
        rep.check(bool(SEMVER_RE.fullmatch(version)), f"{tag} manifest version is semver", f"got {version!r}")

        server = manifest.get("server") if isinstance(manifest.get("server"), dict) else {}
        entry = str(server.get("entry_point", ""))
        rep.check(bool(entry), f"{tag} server.entry_point is set")
        mcp_config = server.get("mcp_config") if isinstance(server.get("mcp_config"), dict) else {}
        env = mcp_config.get("env") if isinstance(mcp_config.get("env"), dict) else {}
        literal = [k for k, v in env.items()
                   if SECRET_NAME_RE.search(k) and not USER_CONFIG_REF_RE.match(str(v))]
        rep.check(not literal, f"{tag} secret env vars come from user_config",
                  "literal values for: " + ", ".join(literal))
        user_config = manifest.get("user_config") if isinstance(manifest.get("user_config"), dict) else {}
        unmasked = [k for k, v in user_config.items()
                    if SECRET_NAME_RE.search(k) and isinstance(v, dict) and v.get("sensitive") is not True]
        rep.check(not unmasked, f"{tag} secret user_config fields are sensitive",
                  "not sensitive: " + ", ".join(unmasked))

        package = load_json(cdir / "package.json", rep, f"{tag} package.json parses")
        if package is not None:
            rep.check(package.get("name") == name, f"{tag} package.json name equals the directory name",
                      f"package.json says {package.get('name')!r}")
            rep.check(package.get("version") == version, f"{tag} package.json version equals manifest version",
                      f"package.json {package.get('version')!r} vs manifest {version!r}")
        rep.check((cdir / "package-lock.json").is_file(), f"{tag} has package-lock.json",
                  "npm ci needs it; run npm install and commit the lock file")

        rel = str(cdir.resolve().relative_to(root.resolve()))
        files = tracked_files(root, rel)
        if files is None:
            rep.check(True, f"{tag} build output check skipped (not a git checkout)")
        else:
            built = [f for f in files if BUILD_OUTPUT_RE.search(f)]
            rep.check(not built, f"{tag} commits no node_modules, dist or .mcpb",
                      "tracked: " + ", ".join(built[:5]))
        connectors[name] = {"dir": cdir, "rel": rel, "version": version}
    return connectors


# ---------------------------------------------------- release-please checks
def check_release_please(root: Path, plugins: dict[str, dict], connectors: dict[str, dict],
                         rep: Report) -> None:
    """The three files must describe the same set of plugins and connectors,
    or one silently stops releasing. Verified against release-please 17.x behaviour:
    package keys are matched verbatim against commit paths (a leading `./`
    never matches), and extra-files paths are relative to the package
    directory unless they start with `/`."""
    config = load_json(root / RP_CONFIG, rep, f"{RP_CONFIG} parses")
    manifest = load_json(root / RP_MANIFEST, rep, f"{RP_MANIFEST} parses")
    if config is None or manifest is None:
        return

    packages = config.get("packages")
    if not rep.check(isinstance(packages, dict) and bool(packages), f"{RP_CONFIG} declares packages"):
        return
    rep.check(isinstance(manifest, dict), f"{RP_MANIFEST} is an object")

    bad_keys = [k for k in packages if k == "." or k.startswith(("./", "/")) or k.endswith("/")]
    rep.check(
        not bad_keys,
        "release-please package keys are plain relative paths",
        "release-please matches these verbatim against commit paths: " + ", ".join(bad_keys)
        if bad_keys else "",
    )

    expected = {info["rel"] for info in plugins.values()} | {info["rel"] for info in connectors.values()}
    rep.check(
        set(packages) == expected,
        "release-please packages == plugin and connector directories",
        f"config has {sorted(packages)}, repo has {sorted(expected)}",
    )
    rep.check(
        set(packages) == set(manifest),
        f"{RP_MANIFEST} keys == release-please packages",
        f"manifest has {sorted(manifest)}, config has {sorted(packages)}",
    )

    by_rel = {info["rel"]: (name, info) for name, info in plugins.items()}
    conn_by_rel = {info["rel"]: info for info in connectors.values()}
    for key, pkg in packages.items():
        pkg = pkg or {}
        rep.check(
            bool(pkg.get("release-type") or config.get("release-type")),
            f"{key} has a release-type",
        )
        component = pkg.get("package-name")
        rep.check(
            component == Path(key).name,
            f"{key} package-name equals the directory name",
            f"package-name {component!r} — the tag prefix must be the directory name",
        )
        if key in by_rel:
            name, info = by_rel[key]
            plugin_version = (info["manifest"] or {}).get("version")
            rep.check(
                manifest.get(key) == plugin_version,
                f"{key} manifest version equals plugin.json version",
                f"manifest says {manifest.get(key)!r}, plugin.json says {plugin_version!r}",
            )
        if key in conn_by_rel:
            info = conn_by_rel[key]
            rep.check(
                manifest.get(key) == info["version"],
                f"{key} manifest version equals the connector version",
                f"{RP_MANIFEST} says {manifest.get(key)!r}, manifest.json says {info['version']!r}",
            )
            rep.check(
                (pkg.get("release-type") or config.get("release-type")) == "node",
                f"{key} uses release-type node",
                "release-type node is what bumps package.json and package-lock.json",
            )
            ef_paths = {
                (ef if isinstance(ef, str) else str((ef or {}).get("path", "")))
                for ef in pkg.get("extra-files") or []
            }
            rep.check(
                "manifest.json" in ef_paths,
                f"{key} extra-files bump manifest.json",
                "without it the .mcpb manifest keeps the old version",
            )
        for ef in pkg.get("extra-files") or []:
            ef_path = ef if isinstance(ef, str) else str((ef or {}).get("path", ""))
            label = f"{key} extra-file {ef_path!r} resolves"
            if not ef_path:
                rep.check(False, label, "extra-files entry has no path")
                continue
            if re.search(r"(^|/)\.\.?(/|$)", ef_path):
                rep.check(False, label, "contains ./ or ../ — release-please rejects it "
                                        "(paths are relative to the package directory; "
                                        "a leading / means the repo root)")
                continue
            target = root / ef_path.lstrip("/") if ef_path.startswith("/") else root / key / ef_path
            rep.check(target.is_file(), label, f"{target.relative_to(root)} does not exist")


# ------------------------------------------------------------ safety checks
def check_forbidden(root: Path, rep: Report) -> None:
    present: list[str] = []
    for pattern in FORBIDDEN_GLOBS:
        for hit in root.glob(pattern):
            if not any(part in SKIP_DIRS for part in hit.parts):
                present.append(str(hit.relative_to(root)))
    rep.check(
        not present,
        "no credential or scratch files present",
        "found: " + ", ".join(sorted(set(present))) if present else "",
    )


def check_secrets(root: Path, rep: Report) -> None:
    hits: list[str] = []
    for path in iter_files(root):
        if path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if any(tok in line for tok in PLACEHOLDER_TOKENS):
                continue
            # Remove commit references, then scan the remainder.
            scrubbed = GIT_SHA_CONTEXT_RE.sub(" ", line)
            for pattern, kind in SECRET_PATTERNS:
                if re.search(pattern, scrubbed):
                    hits.append(f"{path.relative_to(root)}:{lineno} looks like a {kind}")
    rep.check(not hits, "no secrets in tracked content", "\n          ".join(hits[:10]))


def check_python(root: Path, rep: Report) -> None:
    """Compile in-memory so no .pyc is written into the repo or the runner."""
    bad: list[str] = []
    for path in sorted(iter_files(root)):
        if path.suffix != ".py":
            continue
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            bad.append(f"{path.relative_to(root)}:{exc.lineno}: {exc.msg}")
        except OSError as exc:
            bad.append(f"{path.relative_to(root)}: unreadable ({exc})")
    rep.check(not bad, "all python files compile", "\n          ".join(bad))


# -------------------------------------------------------------------- main
def validate_marketplace(root: Path, rep: Report) -> None:
    print("marketplace")
    marketplace, plugins = check_marketplace(root, rep)
    if marketplace is None:
        return
    check_orphans(root, plugins, rep)

    for name, info in plugins.items():
        print(f"\nplugin {name}")
        manifest = check_plugin(info["dir"], name, rep)
        info["manifest"] = manifest
        if manifest is not None:
            rep.check(
                manifest.get("name") == name,
                f"{name} plugin.json name equals the marketplace entry name",
                f"plugin.json says {manifest.get('name')!r} — agents and skills are "
                f"namespaced by this field",
            )

    if (root / SKILLS_DIR).is_dir():
        print("\nstandalone skills")
        check_standalone_skills(root, rep)

    print("\nconnectors")
    connectors = check_connectors(root, rep)

    print("\nrelease-please")
    check_release_please(root, plugins, connectors, rep)

    print("\nsafety")
    check_forbidden(root, rep)
    check_secrets(root, rep)

    print("\npython")
    check_python(root, rep)


def validate_plugin(plugin_dir: Path, rep: Report) -> None:
    print(f"plugin {plugin_dir.name}")
    check_plugin(plugin_dir, plugin_dir.name, rep)
    rep.check(
        not (plugin_dir / ".claude-plugin" / "marketplace.json").exists(),
        "no marketplace.json inside the plugin",
        "a plugin archive is a plugin, not a marketplace",
    )
    print("\nsafety")
    check_forbidden(plugin_dir, rep)
    check_secrets(plugin_dir, rep)
    print("\npython")
    check_python(plugin_dir, rep)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="marketplace repo root (default: current directory)")
    ap.add_argument("--plugin", metavar="DIR",
                    help="validate a single plugin directory instead of the marketplace "
                         "(used on the extracted release archive)")
    args = ap.parse_args()

    rep = Report()
    if args.plugin:
        target = Path(args.plugin).resolve()
        print(f"Validating plugin {target}\n")
        validate_plugin(target, rep)
    else:
        target = Path(args.root).resolve()
        print(f"Validating marketplace {target}\n")
        validate_marketplace(target, rep)

    print()
    if rep.failures:
        print(f"FAILED — {len(rep.failures)} of {rep.checks} checks:")
        for f in rep.failures:
            print(f"  - {f}")
        return 1
    print(f"PASSED — {rep.checks} checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
