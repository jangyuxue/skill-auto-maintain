# Changelog

## v2.0.0 — 2026-05-15

### Added

- **Standalone orphan detection**: `scan_all_directories()` now also detects skills
  placed directly at `skills/<name>/` with their own SKILL.md (e.g. agent-created
  standalone skills that bypassed category directories). Previously only sub-skills
  inside category dirs were found.

### Fixed

- Skills like `skills/my-custom-tool/` with SKILL.md at the top level were
  silently ignored because `scan_skills_in_dir()` only looks for subdirectories.
  Now each directory is checked for its own SKILL.md after the sub-skill scan.

## v1.0.0 — 2026-05-14

Initial release.

- **Scan**: walks all skill directories, migrates orphans to `user_skills/`, registers in `user_skills.json`
- **Compare**: pairwise similarity scoring, reports merge candidates
- **Optimise**: fixes SKILL.md format, checks content quality
- **Report**: professional summary of all actions
