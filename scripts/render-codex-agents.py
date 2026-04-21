#!/usr/bin/env python3
# Render agents/*.md into codex-agents/*.toml.
#
# Source: Markdown with YAML frontmatter (name, description) + body.
# Target: TOML with name, description, and a prompt triple-quoted block.
#
# Invoked manually or by the .githooks/pre-commit hook; keeps codex-agents/
# in sync with agents/ whenever the source changes.

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "agents"
DST_DIR = ROOT / "codex-agents"

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def render(src: pathlib.Path, dst: pathlib.Path) -> None:
    text = src.read_text()
    match = FRONTMATTER.match(text)
    if not match:
        sys.exit(f"error: {src} has no YAML frontmatter block")

    front, body = match.group(1), match.group(2).strip()

    meta: dict[str, str] = {}
    for line in front.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()

    name = meta.get("name", src.stem)
    description = meta.get("description", "")

    if '"""' in body:
        sys.exit(f"error: {src} body contains triple quotes — cannot render to TOML")

    dst.write_text(
        f'name = "{toml_escape(name)}"\n'
        f'description = "{toml_escape(description)}"\n\n'
        f'prompt = """\n{body}\n"""\n'
    )


def main() -> None:
    if not SRC_DIR.is_dir():
        sys.exit(f"error: {SRC_DIR} not found")

    DST_DIR.mkdir(exist_ok=True)

    sources = sorted(SRC_DIR.glob("*.md"))
    if not sources:
        sys.exit(f"error: no .md files found in {SRC_DIR}")

    rendered = set()
    for src in sources:
        dst = DST_DIR / f"{src.stem}.toml"
        render(src, dst)
        rendered.add(dst.name)
        print(f"  rendered {dst.relative_to(ROOT)}")

    for stale in DST_DIR.glob("*.toml"):
        if stale.name not in rendered:
            stale.unlink()
            print(f"  removed stale {stale.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
