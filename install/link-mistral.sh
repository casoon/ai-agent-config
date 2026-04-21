#!/usr/bin/env bash
set -euo pipefail

# Placeholder for Mistral Vibe CLI integration.
#
# Vibe config lives at ~/.vibe/config.toml and uses array fields for skill and
# agent directories (skill_paths, agent_paths, tool_paths). Unlike Claude and
# Codex, Vibe does not consume a top-level instructions file (no CLAUDE.md /
# AGENTS.md analogue in the schema as of now), and the agent file format is
# unconfirmed.
#
# When activating this script in the future:
#   1. Decide whether codex-agents/ (TOML) is compatible with Vibe, or whether
#      a separate vibe-agents/ target is needed.
#   2. Replace the exit below with a TOML edit that appends the repo paths to
#      skill_paths and agent_paths in ~/.vibe/config.toml (idempotent — skip
#      entries that already exist).
#   3. Update README.md install table and install/link-all.sh.

echo "link-mistral.sh: placeholder — Mistral Vibe integration not yet wired up."
echo "  See comments in this file for the intended approach."
exit 0

# --- Sketch for later ------------------------------------------------------
#
# BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# TARGET="$HOME/.vibe/config.toml"
#
# if [ ! -f "$TARGET" ]; then
#   echo "error: $TARGET not found — is Vibe CLI installed?" >&2
#   exit 1
# fi
#
# python3 - "$BASE" "$TARGET" <<'PY'
# import sys, tomllib, pathlib
# base, target = sys.argv[1], pathlib.Path(sys.argv[2])
# cfg = tomllib.loads(target.read_text())
# # TODO: inject "$base/skills" into cfg["skill_paths"] and
# #       "$base/codex-agents" (or a dedicated vibe-agents/) into
# #       cfg["agent_paths"], write back preserving comments (tomllib
# #       does not — consider tomlkit).
# PY
