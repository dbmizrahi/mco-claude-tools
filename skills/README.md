# Standalone skills

Skills that are not part of any plugin: one directory per skill, holding a
`SKILL.md` whose frontmatter `name` equals the directory name.

A Claude Code marketplace serves plugins only, so these are not installed with
`/plugin`. Copy the directory instead:

```bash
cp -R skills/<name> ~/.claude/skills/<name>            # personal: every project
cp -R skills/<name> <project>/.claude/skills/<name>    # one project
```

`scripts/ci/validate_repo.py` parses every `skills/*/SKILL.md` here (frontmatter
must be valid YAML with `name` and `description`). A skill that needs
versioning, releases or bundled scripts belongs in a plugin under `plugins/`.
