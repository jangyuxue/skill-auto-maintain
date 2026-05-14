<p align="center">
  <br>
  <b>Skill Auto Maintain</b><br>
  <i>Find, organise, and clean up your Hermes Agent skills — automatically.</i>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python 3.8+"></a>
</p>

---

**Before — skills scattered everywhere, no registry, no quality control:**

```
~/.hermes/skills/
├── creative/
│   ├── architecture-diagram/    ← system bundled (safe)
│   └── my-scraper/              ← orphan — agent put it here
├── devops/
│   ├── kanban-worker/           ← system bundled (safe)
│   └── my-pipeline/             ← orphan — user put it here
├── auto-generated/
│   └── old-tool/                ← unregistered, quality unknown
└── .hub/
```

**After — one command, everything organised:**

```
~/.hermes/skills/
├── creative/architecture-diagram/  ← bundled, untouched
├── devops/kanban-worker/           ← bundled, untouched
└── user_skills/                    ← created by maintain.py
    ├── my-scraper/SKILL.md
    ├── my-pipeline/SKILL.md
    ├── old-tool/SKILL.md
    └── user_skills.json            ← registry
```

**What changed:**
- `my-scraper` migrated from `creative/` → `user_skills/`
- `my-pipeline` migrated from `devops/` → `user_skills/`
- `old-tool` registered with quality check
- All orphan skills detected, moved, and tracked
- Merge candidates flagged for review

---

## Quick Start

```bash
git clone https://github.com/jangyuxue/skill-auto-maintain.git
cd skill-auto-maintain

mkdir -p ~/.hermes/skills/user-created/skill-auto-maintain
cp scripts/maintain.py ~/.hermes/skills/user-created/skill-auto-maintain/
cp SKILL.md ~/.hermes/skills/user-created/skill-auto-maintain/

~/.hermes/hermes-agent/venv/bin/python \
  ~/.hermes/skills/user-created/skill-auto-maintain/scripts/maintain.py
```

No dependencies. No config. Standard library only.

---

## How It Works

```
Phase 1: [Scan]     ──→  Walk every directory under ~/.hermes/skills/
                  │        Skip bundled (via .bundled_manifest)
                  │        Migrate orphans to user_skills/
                  └─→      Register in user_skills.json

Phase 2: [Compare]  ──→  Pairwise similarity scoring
                  │        4 axes: name, keywords, headings, cross-refs
                  └─→      Report merge candidates (score ≥ 0.30)

Phase 3: [Optimise] ──→  Fix SKILL.md frontmatter, headings
                  │        Check quality: tags, triggers, description length
                  └─→      Flag issues for review

Phase 4: [Report]   ──→  Professional summary of everything done
```

---

## Registry (`user_skills.json`)

```json
{
  "name": "prompt-optimiser",
  "description": "Analyse and rewrite prompts for clarity",
  "status": "active",
  "origin": "auto-generated/prompt-optimiser",
  "optimized": true,
  "modification_count": 1
}
```

---

## Files

```
skill-auto-maintain/
├── README.md                       # This file
├── LICENSE                         # MIT
├── CHANGELOG.md                    # Version history
├── SKILL.md                        # Agent skill doc
├── scripts/
│   └── maintain.py                 # v1.0.0
└── .github/
    ├── workflows/syntax-check.yml  # CI
    └── PULL_REQUEST_TEMPLATE.md    # PR template
```

---

## License

MIT
