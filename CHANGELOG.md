# Changelog

## v1.0.0 — 2026-05-14

Initial release.

### Features

- **Scan**: Walks all directories under `~/.hermes/skills/`, identifies non-bundled skills, migrates misplaced ones to `user_skills/`, registers them in `user_skills.json`
- **Compare**: Pairwise multi-dimensional similarity scoring across name tokens, content keywords, heading structure, and cross-references. Reports merge candidates above threshold for manual review
- **Optimise**: Auto-fixes missing frontmatter, empty fields, missing H1 in SKILL.md. Checks content quality (short descriptions, missing tags/triggers, placeholder files)
- **Report**: Professional summary of all actions taken

### Technical

- Zero external dependencies — standard library only
- Single-file script (`scripts/maintain.py`)
- Compatible with any standard Hermes Agent installation
- Idempotent — safe to run multiple times
