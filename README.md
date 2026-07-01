# ai-agent-config

A shared baseline for global AI-assistant configuration across Claude Code,
Codex, and Mistral Vibe.

The repo holds one neutral tree. At install time, each tool-specific link
script symlinks the shared files into the tool's config directory
(`~/.claude/` resp. `~/.codex/`) under the names that tool expects — so once
you adopt it, an edit here is instantly live for every tool.

> **Status: public snapshot.**
> This is a **sanitized, one-time export** of a personal AI-assistant config:
> global instructions, reusable skills, and subagent prompts. Business-specific
> skills, real machine config, and internal identifiers are kept out. It is
> maintained in a separate private repo and re-exported here periodically, so
> it is not continuously in sync — treat it as a reusable baseline to copy from,
> not a live feed. Expect occasional breaking changes.

## How it's wired

`install/link-all.sh` symlinks this tree into `~/.claude/` and `~/.codex/`.
Existing non-symlink targets are moved to `<path>.bak` first, so nothing is
lost. Once linked, editing a file here changes the live config directly —
there is no copy step or sync to remember.

Machine-specific and secret-bearing files are **not** tracked:

- `codex-config.toml` — the live Codex config. Git-ignored; seeded from
  `codex-config.example.toml` on first install, then written to at runtime
  by Codex. Edit `codex-config.example.toml` for the shareable baseline.
- The **private section** of `GLOBAL.md` (see below) — personal specifics.

## Layout

```
./
├── GLOBAL.md              # global instructions (→ CLAUDE.md / AGENTS.md)
├── agents/                # subagent sources (Markdown + YAML frontmatter)
├── codex-agents/          # generated from agents/ — do not edit by hand
├── skills/                # reusable skills (one folder with SKILL.md each)
├── codex-config.example.toml  # Codex baseline profiles (tracked)
├── codex-config.toml      # live Codex config (git-ignored, seeded from example)
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

`codex-config.toml` is git-ignored and seeded from `codex-config.example.toml`
on first install; on a fresh clone the link script creates it automatically.

If a target path exists and is not already a symlink, it is moved to
`<path>.bak` before the new symlink is created. Already-existing symlinks
are replaced silently.

## Zed

There is no `link-zed.sh` — Zed needs no separate wiring. When you run
**Claude Code inside Zed** as an external agent (ACP: *Agent Panel → New
Thread → Claude Code*), it reads the same `~/.claude/` that the Claude link
script already sets up. So `GLOBAL.md`, `agents/`, and `skills/` are live in
Zed automatically once `install/link-claude.sh` has run.

Zed's *native* Agent (the built-in assistant, not Claude Code) does not have
a skills concept and uses its own rules files under
`~/.config/zed/`; this repo does not target it. Use the Claude Code / ACP
path to get this configuration in Zed.

## Supported platforms

The install scripts use plain portable Bash (`ln -sfn`, `mkdir -p`, `mv`)
and do not depend on macOS-specific tooling.

| Platform      | Status                                                      |
| ------------- | ----------------------------------------------------------- |
| **macOS**     | Tested.                                                     |
| **Linux**     | Expected to work — not actively tested. Please open an issue if something breaks. |
| **Windows**   | Not supported natively. Use **WSL2** (Ubuntu / Debian) — from inside WSL the Linux path applies. |

Requirements on any platform: `bash`, `python3` (for the codex-agent
renderer), and `git`. `nosecrets` is optional but recommended — see
below.

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

### Pre-commit hook

`.githooks/pre-commit` does two things on every commit:

1. Regenerates `codex-agents/*.toml` from `agents/*.md` and stages the
   result, so the Codex-side prompts can never drift out of sync with
   the Markdown sources.
2. Runs [`nosecrets`](https://github.com/casoon/nosecrets) against the
   staged files and aborts the commit on findings.

If `nosecrets` is not installed, the hook prints a visible error and
**continues** — the commit is not blocked, but nothing was scanned.
Install one-off per machine:

```sh
# curl (macOS / Linux, installs a prebuilt binary)
curl -fsSL https://raw.githubusercontent.com/casoon/nosecrets/main/install.sh | sh

# or via npm
npm install -g @casoon/nosecrets

# or via cargo
cargo install nosecrets-cli
```

## Memory scope

This repo manages the **global** layer of Claude Code's memory system — the
per-user `CLAUDE.md` (and Codex's `AGENTS.md`), plus reusable skills and
subagent prompts. It deliberately does **not** cover:

- **Project memory** — each project's own `CLAUDE.md` lives in that
  project's repo, not here.
- **Conversational memory** — Claude Code's per-session auto-memory under
  `~/.claude/projects/…` is machine-local, often personal, and must never
  be committed to a shared baseline.

## Private additions

`GLOBAL.md` ends with a marked "private section". Personal specifics —
preferred package managers, daily languages, commit conventions, project
quirks — belong there. Since this repo is private, that section can be
committed here directly; keep genuine secrets (API keys, tokens) out of it
regardless.

## Change workflow

- Edit `GLOBAL.md`, `agents/*.md`, or `skills/*/SKILL.md` — symlinks make
  the change immediately live for Claude. For Codex, the pre-commit hook
  regenerates `codex-agents/` before the change is committed.
- Keep the global instruction file short. Stack-specific knowledge belongs
  in skills; role prompts belong in agents.

## License

[MIT](LICENSE) — do whatever you like with it, attribution appreciated but
not required.
