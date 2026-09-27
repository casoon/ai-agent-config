---
title: Overview
description: What ai-agent-config contains, which tools it wires up, and what it deliberately leaves out.
order: 0
---

ai-agent-config is a baseline for the **global** configuration of AI coding assistants. It keeps
three things in one neutral folder tree:

- **Global instructions** in `GLOBAL.md`: working style, validation, scope control, commit and
  output rules that apply to every project.
- **Subagents** in `agents/`: role prompts for an explorer, planner, implementer, reviewer and
  security auditor.
- **Skills** in `skills/`: one folder per skill, each with a `SKILL.md` and optional
  reference files.

The install scripts symlink this tree into `~/.claude/` and `~/.codex/` under the names each
tool expects, and register the skills and agents in Mistral Vibe's config if Vibe is
installed. Because every target is a symlink, an edit in the repository is live immediately.

A short product page lives at [ai-agent-config.casoon.de](https://ai-agent-config.casoon.de).

## Status

The repository is a **public snapshot**: a sanitized export of a personal configuration that is
maintained in a separate private repository and re-exported periodically. Business-specific
skills, real machine config and internal identifiers are kept out. Treat it as a baseline to
copy from rather than a live feed, and expect occasional breaking changes.

## What it does not cover

- **Project memory:** each project's own `CLAUDE.md` or `AGENTS.md` belongs in that project's
  repository.
- **Conversational memory:** Claude Code's per-session auto-memory under `~/.claude/projects/`
  is machine-local and often personal; it never belongs in a shared baseline.
- **Zed's native agent:** it has no skills concept and uses its own rules files. Claude Code
  running inside Zed reads `~/.claude/` and gets everything (see
  [How it works](getting-started/how-it-works/)).

## How the docs are organised

- **Getting started:** [installation](getting-started/installation/) and
  [how the symlinks work](getting-started/how-it-works/).
- **Guides:** [customising the baseline](guides/customizing/) and the
  [pre-commit hook](guides/pre-commit-hook/).
- **Reference:** every [subagent](reference/agents/) and [skill](reference/skills/), read from
  the repository when the site is built, and the [repository layout](reference/layout/).

The [showcase](../showcase/) puts each subagent's Markdown source next to the TOML file
generated from it for Codex.
