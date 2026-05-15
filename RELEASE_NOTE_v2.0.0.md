# v2.0.0 — Registry Sync, Extended Scan Scope & Stability Improvements

**Release Date:** 2026-05-15

---

## Overview

v2.0.0 is a maintenance-focused release that addresses four real-world issues discovered during daily use of the skill auto-maintenance tool:

1. **Scan blind spot** — `user_skills/` was silently excluded, so skills placed there were never registered
2. **Stale registry** — deleted skill directories left `"active"` entries forever, disk and registry drifted
3. **Fragile frontmatter parser** — a regex that assumed a specific field order would silently return empty strings when fields were rearranged
4. **No rollback safety** — registry overwrites had no backup, making accidental corruption unrecoverable

---

## What Changed

### 1. Scan Scope: `user_skills/` No Longer Excluded

**Before:** `EXCLUDED_DIRS = {"user_skills", ...}` — any skill placed in `user_skills/` (e.g. `daily-plan-manager`, `image-gen`) was invisible to the scanner and never appeared in `user_skills.json`.

**After:** `EXCLUDED_DIRS` is now an empty set. The scanner traverses every directory under `~/.hermes/skills/`, including `user_skills/` and the tool's own directory. New skills dropped into `user_skills/` are automatically registered on the next run.

---

### 2. Registry Deletion Detection

**Before:** When you removed a skill directory from disk (e.g. `rm -rf user_skills/obsolete-skill/`), the registry entry remained `"status": "active"` forever — a silent inconsistency.

**After:** After each scan, the tool iterates all registry entries with `status = "active"` and checks whether the corresponding directory still exists. If the directory is gone, the entry is automatically marked `"deleted"`.

---

### 3. Description Parser: Regex → Line-by-Line

**Before:** The description was extracted from SKILL.md frontmatter using a regex:

```python
pattern = r'description:\s*["\']?(.*?)["\']?\s*(?:\n|platforms|version|author|tags)'
```

This regex only recognised four specific follow-up field names (`platforms`, `version`, `author`, `tags`). If the frontmatter had a different field order — e.g. `description` followed by `license:` or `category:` — the match would silently fail and return an empty string.

**After:** A line-by-line parser: find the YAML frontmatter block (content between `---` delimiters), scan each line, match on the `description:` prefix. Field order no longer matters. The code is simpler and more robust.

---

### 4. Pre-Run Snapshot Backup

Before overwriting `user_skills.json`, the tool now saves a timestamped copy to:

```
user_skills/.history/user_skills_YYYYMMDD_HHMMSS.json
```

If the registry is accidentally corrupted, you can restore from the latest snapshot manually.

---

### 5. Docs & Version String Cleanup

| Item | Before | After |
|------|--------|-------|
| `scan_all_directories()` docstring | `"excluding hidden and user_skills"` | `"excluding hidden dirs"` |
| Run banner version | `v1.0` | `v1.1.0` (matches SKILL.md) |

---

## Registry Schema

No breaking changes to `user_skills.json`. The new `"deleted"` status value is backward-compatible — older tool versions will preserve it without error.

| Field | Type | v1.x | v2.0 |
|-------|------|------|------|
| `status` | string | `active`, `merged` | `active`, `merged`, `deleted` |
| `origin` | string | migration source path | unchanged |

---

## Upgrade from v1.x

```bash
# Replace the script and run once — that's it
cp skill-auto-maintain/maintain.py ~/.hermes/skills/user_skills/skill-auto-maintain/maintain.py

~/.hermes/hermes-agent/venv/bin/python \
  ~/.hermes/skills/user_skills/skill-auto-maintain/maintain.py
```

Your existing `user_skills.json` is read, new entries are supplemented, and the file is written back. No manual migration needed.

---

## Files Changed

| File | Lines | Role |
|------|-------|------|
| `maintain.py` | 818 | Core maintenance script |
| `SKILL.md` | — | Skill documentation |

---

## License

MIT
