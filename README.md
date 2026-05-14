<p align="center">
  <br>
  <b>Skill Auto Maintain</b><br>
  <i>Find, organise, and clean up your Hermes Agent skills — automatically.</i>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python 3.8+"></a>
  <a href="#"><img src="https://img.shields.io/badge/status-stable-brightgreen" alt="Status"></a>
  <strong>English</strong> · <a href="README_CN.md">中文</a>
</p>

> **Your `~/.hermes/skills/` is a mess.** Agent-created skills are scattered across `creative/`, `devops/`, `auto-generated/` — with no registry, no duplicate detection, no quality control.  
> Skill Auto Maintain scans everything, moves orphans to `user_skills/`, registers them, detects duplicates, and fixes broken SKILL.md files. One command, zero config. **Zero external dependencies — pure Python 3 standard library.**

<br>

```mermaid
flowchart LR
    A[Scan] --> B[Compare]
    B --> C[Optimise]
    C --> D[Report]
    
    A -.-> A1["Walk all skill dirs<br>Skip bundled skills"]
    B -.-> B1["Similarity scoring<br>Flag merge candidates"]
    C -.-> C1["Fix SKILL.md format<br>Check content quality"]
    D -.-> D1["Professional summary<br>of all actions"]
    
    style A fill:#1e3a5f,stroke:#3b82f6,color:#fff
    style B fill:#1e3a5f,stroke:#3b82f6,color:#fff
    style C fill:#1e3a5f,stroke:#3b82f6,color:#fff
    style D fill:#1e3a5f,stroke:#3b82f6,color:#fff
    style A1 fill:#1e293b,stroke:#475569,color:#94a3b8
    style B1 fill:#1e293b,stroke:#475569,color:#94a3b8
    style C1 fill:#1e293b,stroke:#475569,color:#94a3b8
    style D1 fill:#1e293b,stroke:#475569,color:#94a3b8
```

<br>

<table>
<tr>
<td width="50%" valign="top">

### ❌ Before

```
~/.hermes/skills/
├── creative/
│   ├── architecture-diagram/
│   └── my-scraper        
├── devops/
│   ├── kanban-worker/
│   └── my-pipeline       
└── auto-generated/
    └── old-tool/
```

_Orphans scattered everywhere. No registry. No quality checks._

</td>
<td width="50%" valign="top">

### ✅ After

```
~/.hermes/skills/
├── creative/
│   └── architecture-diagram/
├── devops/
│   └── kanban-worker/
└── user_skills/
    ├── my-scraper/
    ├── my-pipeline/
    ├── old-tool/
    └── user_skills.json
```

_All orphans in one place. Registered. Tracked._

</td>
</tr>
</table>

<br>

## Quick Start

```bash
git clone https://github.com/jangyuxue/skill-auto-maintain.git
cp -r skill-auto-maintain/skill-auto-maintain ~/.hermes/skills/user-created/
```

Then in `hermes`:

- Type `/skill` and select **skill-auto-maintain** from the list, or
- Tell the agent: *"Run skill auto maintenance"*

<br>

## Features

<table>
<tr>
<td width="33%" align="center">

**🔍 Scan**

Walk every directory.  
Skip bundled skills.  
Migrate orphans.

</td>
<td width="33%" align="center">

**📊 Compare**

4-dimension similarity.  
Merge candidate detection.  
Manual review only.

</td>
<td width="33%" align="center">

**✨ Optimise**

Fix SKILL.md format.  
Quality checks.  
Professional report.

</td>
</tr>
</table>

<br>

## Project Structure

```
skill-auto-maintain/
├── README.md
├── README_CN.md
├── LICENSE
├── CHANGELOG.md
└── skill-auto-maintain/         ← Copy this folder to skills/
    ├── SKILL.md
    └── maintain.py
```

<br>

## License

MIT
