---
title: Customising the baseline
description: Where personal specifics go, how to add skills and subagents, and how to keep your copy in step with new snapshots.
order: 1
---

## Personal specifics in GLOBAL.md

`GLOBAL.md` ends with a marked private section, an HTML comment listing what belongs there:
preferred package manager, languages and tools you use daily, projects that need special
handling, personal code style, commit and PR conventions. Keep it in your own copy, not in a
shared repository, and keep genuine secrets out of it either way.

Keep the rest of the file short. It is loaded for every project, so stack-specific knowledge
belongs in skills and role prompts belong in agents.

## Add or change a skill

Create `skills/<name>/SKILL.md` with `name` and `description` in the frontmatter, and put longer
material in files next to it. Because `skills/` is linked as a whole, the new skill is
available to Claude Code and Codex immediately. The [skill reference](../../reference/skills/)
lists what the snapshot ships with.

## Add or change a subagent

Edit or create `agents/<name>.md` only. `codex-agents/` is generated; with the hook enabled it
is regenerated on commit, otherwise run:

```sh
python3 scripts/render-codex-agents.py
```

The renderer stops with an error if a file has no frontmatter block or if its body contains
`"""`, which cannot be expressed in the TOML output.

## Change the Codex profiles

Edit `codex-config.example.toml` for anything that belongs in the shared baseline. The live
`codex-config.toml` is only seeded once; after that, copy changes over by hand or delete it and
re-run `link-codex.sh`.

## Keep up with new snapshots

The public repository is re-exported from a private one from time to time. If you use a fork,
pull the upstream changes and resolve conflicts in the files you customised; the symlinks do not
need to be recreated. The [changelog](../../../changelog/) summarises each change.
