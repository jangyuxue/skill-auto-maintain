# Skill Auto Maintain

Find, organise, and clean up your Hermes Agent skills — automatically.

```bash
git clone https://github.com/jangyuxue/skill-auto-maintain.git
cp -r skill-auto-maintain ~/.hermes/skills/user-created/

~/.hermes/hermes-agent/venv/bin/python \
  ~/.hermes/skills/user-created/skill-auto-maintain/scripts/maintain.py
```

One command scans everything, migrates orphans to `user_skills/`, registers them, detects duplicates, and fixes SKILL.md formatting. Zero config, zero dependencies.

[Changelog](CHANGELOG.md)

## License

MIT
