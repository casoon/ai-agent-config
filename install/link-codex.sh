#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="$HOME/.codex"

mkdir -p "$TARGET"

link() {
  local src="$1"
  local dst="$2"
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    echo "warning: $dst exists and is not a symlink — moving to $dst.bak"
    mv "$dst" "$dst.bak"
  fi
  ln -sfn "$src" "$dst"
  echo "  linked $dst -> $src"
}

if [ ! -d "$BASE/codex-agents" ]; then
  echo "note: codex-agents/ missing — running renderer once"
  python3 "$BASE/scripts/render-codex-agents.py"
fi

link "$BASE/GLOBAL.md"         "$TARGET/AGENTS.md"
link "$BASE/codex-config.toml" "$TARGET/config.toml"
link "$BASE/codex-agents"      "$TARGET/agents"
link "$BASE/skills"            "$TARGET/skills"

echo "Codex config linked from $BASE"
