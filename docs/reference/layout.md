---
title: Repository layout
description: What each file and folder in the repository is for, and which of them the install scripts link.
order: 3
---

```text
./
├── GLOBAL.md                  # global instructions (→ CLAUDE.md / AGENTS.md)
├── agents/                    # subagent sources (Markdown + YAML frontmatter)
├── codex-agents/              # generated from agents/ — do not edit by hand
├── skills/                    # one folder with a SKILL.md per skill
├── codex-config.example.toml  # Codex baseline profiles (tracked)
├── codex-config.toml          # live Codex config (git-ignored, seeded from the example)
├── scripts/
│   └── render-codex-agents.py
├── .githooks/
│   └── pre-commit             # renders codex-agents/, runs nosecrets
├── install/
│   ├── link-all.sh
│   ├── link-claude.sh
│   ├── link-codex.sh
│   └── link-mistral.sh
├── .nosecretsignore           # reviewed false positives of the secret scan
├── site/                      # this website (Astro), not linked anywhere
└── docs/                      # the pages you are reading, not linked anywhere
```

| Path | Linked by | Edit by hand |
| --- | --- | --- |
| `GLOBAL.md` | `link-claude.sh`, `link-codex.sh` | yes |
| `agents/` | `link-claude.sh` | yes |
| `codex-agents/` | `link-codex.sh`, `link-mistral.sh` (as path) | no, generated |
| `skills/` | `link-claude.sh`, `link-codex.sh`, `link-mistral.sh` (as path) | yes |
| `codex-config.toml` | `link-codex.sh` | yes, machine-local |
| `codex-config.example.toml` | – (seeds `codex-config.toml`) | yes |
