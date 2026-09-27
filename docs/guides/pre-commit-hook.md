---
title: The pre-commit hook
description: What .githooks/pre-commit does on every commit, and how to install the secret scanner it calls.
order: 2
---

Enable the hook once per clone:

```sh
git config core.hooksPath .githooks
```

On every commit it then does two things:

1. Runs `scripts/render-codex-agents.py`. If `codex-agents/` changed, the result is staged, so
   the Codex prompts cannot drift from the Markdown sources.
2. Runs `nosecrets scan --staged` and aborts the commit on findings.

If `nosecrets` is not on `PATH`, the hook prints an error explaining how to install it and lets
the commit proceed without a scan.

## Install nosecrets

```sh
# prebuilt binary (macOS / Linux)
curl -fsSL https://raw.githubusercontent.com/casoon/nosecrets/main/install.sh | sh

# or via npm
npm install -g @casoon/nosecrets

# or via cargo
cargo install nosecrets-cli
```

## Known false positives

Some Cloudflare reference files in `skills/cloudflare/references/` contain placeholder
connection strings. They are listed with their finding IDs in `.nosecretsignore`, so the scan
passes without disabling it.
