---
title: How it works
description: Which file ends up where, why every target is a symlink, and how Codex, Mistral Vibe and Zed are covered.
order: 2
---

## One tree, several names

Each tool expects its configuration under its own names. The link scripts map the neutral
tree onto them:

| Source | Claude Code | Codex |
| --- | --- | --- |
| `GLOBAL.md` | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` |
| `agents/` | `~/.claude/agents` | – (uses `codex-agents/`) |
| `codex-agents/` | – | `~/.codex/agents` |
| `skills/` | `~/.claude/skills` | `~/.codex/skills` |
| `codex-config.toml` | – | `~/.codex/config.toml` |

Only these paths are linked. Everything else in the repository, including this site's `site/`
and `docs/` folders, stays out of the tools' config directories.

## Symlinks, not copies

Every link is created with `ln -sfn`. Once linked, editing `GLOBAL.md`, a file in `agents/` or
a `SKILL.md` changes the live configuration directly; there is no copy step or sync to remember.
Pulling a new snapshot with `git pull` updates all tools at once.

Before linking, each script checks the target: if it exists and is not a symlink, it is moved
to `<path>.bak`. Existing symlinks are replaced without a backup.

## Subagents for Codex

Claude Code reads subagents as Markdown with YAML frontmatter (`name`, `description`) and the
prompt as body. Codex expects TOML. `scripts/render-codex-agents.py` renders each
`agents/<name>.md` into `codex-agents/<name>.toml` with `name`, `description` and the body as a
triple-quoted `prompt`, and deletes TOML files whose Markdown source is gone. The
[showcase](../../../showcase/) shows every pair.

`codex-agents/` is committed, so a fresh clone works without running Python; `link-codex.sh`
only runs the renderer if the folder is missing.

## Codex config

Codex writes runtime state such as marketplaces and project trust levels into its
`config.toml`. That file is therefore machine-specific: `codex-config.toml` is git-ignored and
seeded from the tracked `codex-config.example.toml` on first install. The example defines three
profiles, `default` (medium reasoning effort), `deep` (high) and `fast` (low), and the
`context7` MCP server. Edit the example file for changes that belong in the shared baseline.

## Mistral Vibe

Vibe is configured by paths rather than symlinks. `link-mistral.sh` edits `~/.vibe/config.toml`
in place and adds the repository's `skills/` to `skill_paths` and `codex-agents/` to
`agent_paths`. Reusing the Codex TOML format for Vibe agents is a best-effort assumption noted
in the script.

## Zed

There is no Zed script, because none is needed: Claude Code running inside Zed as an external
agent (*Agent Panel → New Thread → Claude Code*) reads the same `~/.claude/` that
`link-claude.sh` sets up. Zed's built-in agent is not targeted.
