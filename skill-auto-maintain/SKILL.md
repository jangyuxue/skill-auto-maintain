---
name: skill-auto-maintain
description: "Automated lifecycle management for non-bundled Hermes skills. Scans all skill directories, migrates orphans to user_skills/, registers in user_skills.json, detects merge candidates via multi-dimensional similarity, and optimises SKILL.md format. No SOUL framework dependency — works on any standard Hermes Agent installation."
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [maintenance, skills, cleanup, registry, standalone]
    triggers:
      - "run skill auto maintenance"
      - "run skill auto maintain"
      - "技能自动维护"
      - "整理技能"
      - "清理技能"
      - "maintain skills"
      - "clean up skills"
---

# Skill Auto Maintain

A standalone tool for managing non-bundled Hermes skills — works on any standard Hermes Agent installation without additional framework dependencies.

## What It Does

Scans all skill directories under `~/.hermes/skills/` and runs four phases:

| Phase | Description |
|-------|-------------|
| [Scan] | Identifies non-bundled skills, migrates misplaced ones to `user_skills/`, registers them in `user_skills.json`, **marks registry entries as `deleted` when their skill directory no longer exists on disk** |
| [Compare] | Pairwise multi-dimensional similarity scoring to detect merge candidates |
| [Optimise] | Fixes SKILL.md formatting and checks content quality (triggers, tags, description, structure) |
| [Report] | Generates a comprehensive professional summary of all actions taken |

## How to Execute

This skill requires running `maintain.py` via the Hermes venv Python. When the user asks to run skill auto maintenance:

1. **Determine the script path:**
   - First run (before self-migration): `~/.hermes/skills/skill-auto-maintain/maintain.py`
   - After self-migration (subsequent runs): `~/.hermes/skills/user_skills/skill-auto-maintain/maintain.py`
   - Try the `user_skills/` path first since most users will already have run it once
2. **Run the script:**
   ```
   ~/.hermes/hermes-agent/venv/bin/python <script_path>
   ```
3. **Return the full report output** to the user — it contains all scan, migration, comparison, and optimisation results.

> **Note on self-migration:** The first run automatically moves the tool's own directory from `skills/skill-auto-maintain/` to `user_skills/skill-auto-maintain/`. This is expected — after one run, the tool lives in `user_skills/` permanently. Subsequent runs should use the `user_skills/` path.

## Scan Scope

The tool scans **all** directories under `~/.hermes/skills/` — including `user_skills/` itself. This means:

- **New skills placed directly into `user_skills/`** get auto-detected and registered on the next run.
- **Skills deleted from `user_skills/`** get their registry entry marked as `deleted` (not removed — preserves audit trail).
- The tool's own directory (`skill-auto-maintain/`) is a regular skill directory and gets processed like any other.

## Directory Structure

```
~/.hermes/skills/
├── .bundled_manifest              ← System built-in skill whitelist
├── creative/                      ← Bundled skill category (read-only)
├── devops/                        ← Bundled skill category (read-only)
├── ...                            ← Any other category directories
├── user_skills/                   ← Created by this tool
│   ├── <skill-name>/              ← Migrated or registered skills
│   │   └── SKILL.md
│   └── user_skills.json           ← Registry (name, description, status, origin, optimised, modification_count)
```

## Usage

Run directly via Hermes venv Python:

```bash
# First run (before self-migration):
~/.hermes/hermes-agent/venv/bin/python \
  ~/.hermes/skills/skill-auto-maintain/maintain.py

# Subsequent runs (after self-migration to user_skills/):
~/.hermes/hermes-agent/venv/bin/python \
  ~/.hermes/skills/user_skills/skill-auto-maintain/maintain.py
```

Or tell your Hermes Agent: *"Run skill auto maintenance"* — the agent will handle it automatically.

## Scan Scope Change (v1.1.0)

Unlike earlier versions that excluded `user_skills/` from scanning, **v1.1.0 now includes it**. This means:

- **New skills placed directly into `user_skills/`** get auto-detected and registered in `user_skills.json` on the next run.
- **Skills deleted from `user_skills/`** get their registry entry marked as `deleted` (not removed — audit trail preserved).
- The tool no longer skips its own directory, so self-migration from root → `user_skills/` is expected and handled correctly.

## Registration Format

| Field | Description |
|-------|-------------|
| `name` | Skill directory name |
| `description` | Description from SKILL.md frontmatter |
| `status` | `active` (on disk + registered), `merged` (absorbed into another), or `deleted` (directory removed) |
| `origin` | Migration source path or `merged: [skill-a, skill-b]` |
| `optimized` | Whether SKILL.md has been format-optimised |
| `modification_count` | Number of times the entry has been modified |
| `created` | ISO timestamp of first registration |
| `last_updated` | ISO timestamp of last modification |

## Merge Detection

Skills are compared using multi-dimensional similarity scoring:
- Name token overlap (+0.20)
- Content keyword overlap (+0.10/keyword, max +0.30)
- Heading structure similarity (+0.10)
- Related-skills cross-reference (+0.20)

Pairs scoring ≥ 0.30 across at least 2 evidence axes are reported as merge candidates. The tool only detects and reports — merging is a manual decision.

## SKILL.md Optimisation

For newly added skills, the tool automatically:
1. Fixes missing or malformed frontmatter (name, description, version, author)
2. Adds missing H1 heading
3. Checks content quality:
   - Short or generic descriptions
   - Missing tags or triggers
   - No structural sections
   - Suspiciously short files (placeholders)

All format changes and quality warnings are reported in the final summary.

## Requirements

- Hermes Agent installed at `~/.hermes/`
- `~/.hermes/hermes-agent/venv/bin/python` (standard library only)
- No other framework dependencies

## Files

| File | Purpose |
|------|---------|
| `maintain.py` | The maintenance script (v2.0.0) |
| `SKILL.md` | This file — skill documentation for the agent |
