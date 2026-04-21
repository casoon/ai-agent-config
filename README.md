# ai-agent-config

Shareable baseline configuration for Claude Code and Codex.

The repo holds a single neutral tree. At install time, each tool-specific
link script symlinks the shared files into the tool's config directory
(`~/.claude/` resp. `~/.codex/`) under the names that tool expects.

> **Status: example, being validated in practice.**
> This repo is a first cut at sharing a global AI-assistant configuration
> across tools (Claude Code, Codex, eventually Mistral Vibe). I am currently
> using it on my own machine to see whether the approach holds up — where
> the rough edges are, what needs to be simplified, and which parts are
> actually worth sharing. Expect breaking changes. Feedback and issues are
> welcome.

## Intended use

This repo is a **template**, not a ready-to-link personal config. Running
`install/link-all.sh` directly from a clone of this repository will
replace your existing `~/.claude/CLAUDE.md`, `~/.claude/skills/`,
`~/.codex/AGENTS.md`, `~/.codex/config.toml`, and `~/.codex/skills/` with
the generic content here. Existing non-symlink targets are moved to
`<path>.bak`, so nothing is lost, but your real personal config stops
being active until you restore it.

**Recommended workflow:**

1. Fork or clone this repo into a **private** copy.
2. In the private copy, manually merge your existing files from
   `~/.claude/` and `~/.codex/` into `GLOBAL.md`, `skills/`, and
   `codex-config.toml`.
3. Run `install/link-all.sh` from the **private** copy only.
4. Pull updates from this template into the private copy via
   `git merge` or cherry-pick as needed.

## Layout

```
./
├── GLOBAL.md              # global instructions (→ CLAUDE.md / AGENTS.md)
├── agents/                # subagent sources (Markdown + YAML frontmatter)
├── codex-agents/          # generated from agents/ — do not edit by hand
├── skills/                # reusable skills (one folder with SKILL.md each)
├── codex-config.toml      # Codex-only runtime profiles
├── scripts/
│   └── render-codex-agents.py
├── .githooks/
│   └── pre-commit         # regenerates codex-agents/ on commit
└── install/
    ├── link-claude.sh
    ├── link-codex.sh
    └── link-all.sh
```

## Install

```sh
./install/link-all.sh
```

The scripts create symlinks under `~/.claude/` and `~/.codex/`:

| Source                  | Claude target            | Codex target              |
| ----------------------- | ------------------------ | ------------------------- |
| `GLOBAL.md`             | `~/.claude/CLAUDE.md`    | `~/.codex/AGENTS.md`      |
| `agents/`               | `~/.claude/agents`       | — (uses `codex-agents/`)  |
| `codex-agents/`         | —                        | `~/.codex/agents`         |
| `skills/`               | `~/.claude/skills`       | `~/.codex/skills`         |
| `codex-config.toml`     | —                        | `~/.codex/config.toml`    |

If a target path exists and is not already a symlink, it is moved to
`<path>.bak` before the new symlink is created. Already-existing symlinks
are replaced silently.

## Single source of truth

`agents/*.md` is the **only** place to edit agent prompts.
`codex-agents/*.toml` is generated and should never be edited directly:

```sh
python3 scripts/render-codex-agents.py
```

This is run automatically on commit via `.githooks/pre-commit`. Enable the
hook once per clone:

```sh
git config core.hooksPath .githooks
```

The same hook also runs [`nosecrets`](https://github.com/casoon/nosecrets)
against the staged files and aborts the commit on findings. If `nosecrets`
is not on `PATH` the scan is skipped with a warning.

## Private additions

`GLOBAL.md` ends with a marked "private section". Personal specifics —
preferred package managers, daily languages, commit conventions, project
quirks — belong there and should live in a **private fork** of this repo,
not in the shared baseline.

## Change workflow

- Edit `GLOBAL.md`, `agents/*.md`, or `skills/*/SKILL.md` — symlinks make
  the change immediately live for Claude. For Codex, the pre-commit hook
  regenerates `codex-agents/` before the change is committed.
- Keep the global instruction file short. Stack-specific knowledge belongs
  in skills; role prompts belong in agents.

## License

[MIT](LICENSE) — do whatever you like with it, attribution appreciated but
not required.
