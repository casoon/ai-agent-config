#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="$HOME/.vibe/config.toml"

if [ ! -f "$TARGET" ]; then
  echo "skip: $TARGET not found — Vibe CLI not installed or not yet configured."
  exit 0
fi

# Inject skill_paths and agent_paths into ~/.vibe/config.toml using stdlib only.
# Idempotent: skips entries that are already present.
#
# codex-agents/ TOML format is reused for Vibe agents as a best-effort assumption.
# If Vibe ships an incompatible agent schema, introduce a dedicated vibe-agents/ target
# and update the agents_path variable accordingly.
python3 - "$BASE" "$TARGET" <<'PY'
import sys, pathlib, re

base   = pathlib.Path(sys.argv[1])
target = pathlib.Path(sys.argv[2])

skills_path = str(base / "skills")
agents_path = str(base / "codex-agents")

text = target.read_text()

def inject(text, key, value):
    # Match:  key = [ ... ]  (single or multi-line)
    pattern = rf'({re.escape(key)}\s*=\s*\[)(.*?)(\])'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        inner = m.group(2)
        if f'"{value}"' in inner or f"'{value}'" in inner:
            print(f"  {key} already contains {value!r} — skipped")
            return text
        if inner.strip():
            replacement = m.group(1) + inner.rstrip() + f',\n  "{value}"\n' + m.group(3)
        else:
            replacement = m.group(1) + f'"{value}"' + m.group(3)
        print(f"  added {value!r} to {key}")
        return text[:m.start()] + replacement + text[m.end():]
    # Key not present — append it
    text = text.rstrip("\n") + f'\n{key} = ["{value}"]\n'
    print(f"  created {key} = [{value!r}]")
    return text

text = inject(text, "skill_paths", skills_path)
text = inject(text, "agent_paths", agents_path)
target.write_text(text)
PY

echo "Vibe config updated: $TARGET"
