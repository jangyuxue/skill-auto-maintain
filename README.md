<p align="center">
  <br>
  <b>Skill Auto Maintain</b><br>
  <i>Find, organise, and clean up your Hermes Agent skills — automatically.</i>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python 3.8+"></a>
</p>

> **Your `~/.hermes/skills/` is a mess.** Agent-created skills land everywhere — `creative/`, `devops/`, `auto-generated/` — with no registry, no duplicate detection, and no quality control.  
> Skill Auto Maintain scans everything, moves orphans to `user_skills/`, registers them, detects duplicates, and fixes broken SKILL.md files. One command, zero config.

## Quick Start

```bash
git clone https://github.com/jangyuxue/skill-auto-maintain.git
cp -r skill-auto-maintain/skill-auto-maintain ~/.hermes/skills/user-created/
```

Then in `hermes`:

- Type `/skill` and select **skill-auto-maintain** from the list, or
- Tell the agent: *"Run skill auto maintenance"*


## What It Does

- Scans every directory under `~/.hermes/skills/`
- Skips system-bundled skills (via `.bundled_manifest`)
- Moves orphans to `user_skills/` and registers them
- Detects duplicate/overlapping skills via similarity scoring
- Fixes SKILL.md formatting and checks content quality

## Before vs After

```
❌ Before                              ✅ After
~/.hermes/skills/                      ~/.hermes/skills/
├── creative/                          ├── creative/  (bundled only)
│   ├── architecture-diagram/          ├── devops/     (bundled only)
│   └── my-scraper/        ← 走丢     └── user_skills/
├── devops/                                ├── my-scraper/
│   └── my-pipeline/          ← 走丢        ├── my-pipeline/
└── auto-generated/                       └── user_skills.json
    └── old-tool/
```

## Files

```
skill-auto-maintain/                 ← Clone this repo
├── README.md
├── LICENSE
├── CHANGELOG.md
└── skill-auto-maintain/             ← Copy this folder to skills/
    ├── SKILL.md
    └── maintain.py
```

## License

MIT
