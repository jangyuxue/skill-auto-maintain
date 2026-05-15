## v2.0.0 — Standalone Orphan Detection (2026-05-15)

### Overview

v2.0.0 adds detection of standalone skills placed directly at `skills/<name>/`
(e.g. `skills/soul-governance/` with its own `SKILL.md`), which were previously
silently ignored by the scanner.

### What Changed

`scan_all_directories()` now runs two checks per top-level directory:

1. **Sub-skill scan** (existing): `scan_skills_in_dir()` looks for subdirectories
   that contain a `SKILL.md` — e.g. `creative/my-skill/SKILL.md`

2. **Standalone check** (new): after the sub-skill scan, checks if the directory
   itself has a `SKILL.md` directly inside — e.g. `skills/soul-governance/SKILL.md`

Both results are merged into the same `{skill_name: skill_path}` dict, so existing
migration, registration, and merge detection logic handles standalone skills
without any additional changes.

### Why

Hermes Agent sometimes creates skills directly under `~/.hermes/skills/<name>/`
instead of placing them inside `auto-generated/` or a category directory. The
old scanner only found skills nested inside category subdirectories, so these
standalone skills were completely invisible to the tool.

### Before vs After

| Scenario | Before v2.0.0 | After v2.0.0 |
|----------|---------------|--------------|
| `skills/creative/my-skill/SKILL.md` | ✅ Detected | ✅ Detected |
| `skills/soul-governance/SKILL.md` | ❌ Silently ignored | ✅ Migrated to `user_skills/` |
| `skills/auto-generated/my-skill/SKILL.md` | ✅ Detected (sub-skill scan) | ✅ Detected (both scans) |

### Upgrade

Re-clone or copy the updated `maintain.py`:

```bash
git pull
cp -r skill-auto-maintain/skill-auto-maintain ~/.hermes/skills/user-created/
```

### License

MIT
