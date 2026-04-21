#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="$HOME/.claude"

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

link "$BASE/GLOBAL.md" "$TARGET/CLAUDE.md"
link "$BASE/agents"    "$TARGET/agents"
link "$BASE/skills"    "$TARGET/skills"

echo "Claude config linked from $BASE"
