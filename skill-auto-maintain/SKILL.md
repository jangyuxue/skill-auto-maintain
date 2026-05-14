---
name: skill-auto-maintain
description: "Automated lifecycle management for non-bundled Hermes skills. Scans all skill directories, migrates orphans to user_skills/, registers in user_skills.json, detects merge candidates via multi-dimensional similarity, and optimises SKILL.md format. No SOUL framework dependency — works on any standard Hermes Agent installation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [maintenance, skills, cleanup, registry, standalone]
---

# Skill Auto Maintain

A standalone tool for managing non-bundled Hermes skills — works on any standard Hermes Agent installation without additional framework dependencies.

## What It Does

Scans all skill directories under `~/.hermes/skills/` and runs four phases:

| Phase | Description |
|-------|-------------|
| [Scan] | Identifies non-bundled skills, migrates misplaced ones to `user_skills/`, registers them in `user_skills.json` |
| [Compare] | Pairwise multi-dimensional similarity scoring to detect merge candidates |
| [Optimise] | Fixes SKILL.md formatting and checks content quality (triggers, tags, description, structure) |
| [Report] | Generates a comprehensive professional summary of all actions taken |

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

```bash
~/.hermes/hermes-agent/venv/bin/python \
  ~/.hermes/skills/user-created/skill-auto-maintain/maintain.py
```

## Registration Format

Each skill in `user_skills.json` includes:

| Field | Description |
|-------|-------------|
| `name` | Skill directory name |
| `description` | Description from SKILL.md frontmatter |
| `status` | `active` or `merged` |
| `origin` | Migration source path or `merged: [skill-a, skill-b]` |
| `optimized` | Whether SKILL.md has been format-optimised |
| `modification_count` | Number of times the entry has been modified |

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
| `scripts/maintain.py` | The maintenance script (v1.0.0) |
| `SKILL.md` | This file — skill documentation for the agent |
