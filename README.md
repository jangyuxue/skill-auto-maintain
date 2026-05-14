# Skill Auto Maintain

Find, organise, and clean up your Hermes Agent skills — automatically.

```bash
git clone https://github.com/jangyuxue/skill-auto-maintain.git
cp -r skill-auto-maintain ~/.hermes/skills/user-created/

~/.hermes/hermes-agent/venv/bin/python \
  ~/.hermes/skills/user-created/skill-auto-maintain/scripts/maintain.py
```

No dependencies. No configuration. Standard library only.

## What It Does

```
[Scan]     Walk every directory under ~/.hermes/skills/
           Skip system bundled (.bundled_manifest)
           Move orphans to user_skills/ and register

[Compare]  Pairwise similarity scoring (name, keywords, headings, cross-refs)
           Flag merge candidates ≥ 0.30 for manual review

[Optimise] Fix SKILL.md formatting and check quality
           Report warnings (missing tags, triggers, short descriptions)

[Report]   Professional summary of everything done
```

## Files

```
skill-auto-maintain/
├── SKILL.md                   # Agent skill document
├── scripts/maintain.py        # The script
├── README.md
├── CHANGELOG.md
└── LICENSE
```

## License

MIT
