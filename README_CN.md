<p align="center">
  <br>
  <b>Skill Auto Maintain</b><br>
  <i>自动查找、整理和清理你的 Hermes Agent 技能。</i>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python 3.8+"></a>
  <a href="README.md">English</a> · <strong>中文</strong>
</p>

> **你的 `~/.hermes/skills/` 一团乱麻。** Agent 创建的技能散落在 `creative/`、`devops/`、`auto-generated/` 等各个目录——没有注册表、没有重复检测、没有质量控制。  
> Skill Auto Maintain 扫描一切，将走丢技能搬到 `user_skills/`，注册登记，检测重复，修复异常的 SKILL.md。一条命令，零配置。

## 快速上手

```bash
git clone https://github.com/jangyuxue/skill-auto-maintain.git
cp -r skill-auto-maintain/skill-auto-maintain ~/.hermes/skills/user-created/
```

然后在 `hermes` 里：

- 输入 `/skill` 从列表选择 **skill-auto-maintain**
- 或者告诉 agent：*"运行技能自动维护"*

## 功能

- 扫描 `~/.hermes/skills/` 下所有目录
- 跳过系统内置技能（通过 `.bundled_manifest` 识别）
- 将走丢技能搬到 `user_skills/` 并注册
- 通过相似度评分检测重复/重叠技能
- 修复 SKILL.md 格式，检查内容质量

## 前后对比

```
❌ 之前                                 ✅ 之后
~/.hermes/skills/                      ~/.hermes/skills/
├── creative/                          ├── creative/  (仅保留内置)
│   ├── architecture-diagram/          ├── devops/     (仅保留内置)
│   └── my-scraper/        ← 走丢     └── user_skills/
├── devops/                                ├── my-scraper/
│   └── my-pipeline/          ← 走丢        ├── my-pipeline/
└── auto-generated/                       └── user_skills.json
    └── old-tool/
```

## 文件结构

```
skill-auto-maintain/                 ← 克隆此仓库
├── README.md
├── README_CN.md                     ← 中文版
├── LICENSE
├── CHANGELOG.md
└── skill-auto-maintain/             ← 将此文件夹复制到 skills/
    ├── SKILL.md
    └── maintain.py
```

## 许可证

MIT
