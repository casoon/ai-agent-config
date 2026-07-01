#!/usr/bin/env python3
"""
Convert PNG/JPG images to WebP.
Usage: python3 convert.py <input> [<input> ...] [--max-width 1200] [--quality 85] [--out-dir .]
"""
import sys
import os
import argparse
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow not installed. Run: pip3 install Pillow")


def convert(src: Path, out_dir: Path, max_width: int, quality: int) -> tuple[int, int, str]:
    img = Image.open(src)
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")
    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        img = img.resize((max_width, round(h * ratio)), Image.LANCZOS)
    dst = out_dir / src.with_suffix(".webp").name
    img.save(dst, "WEBP", quality=quality, method=6)
    return os.path.getsize(src), os.path.getsize(dst), str(dst)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("inputs", nargs="+")
    p.add_argument("--max-width", type=int, default=1200)
    p.add_argument("--quality", type=int, default=85)
    p.add_argument("--out-dir", default=None)
    args = p.parse_args()

    for inp in args.inputs:
        src = Path(inp)
        out_dir = Path(args.out_dir) if args.out_dir else src.parent
        orig, new, dst = convert(src, out_dir, args.max_width, args.quality)
        saving = round((1 - new / orig) * 100)
        w, h = Image.open(dst).size
        print(f"{src.name} → {Path(dst).name}  {orig//1024}KB → {new//1024}KB  (-{saving}%)  {w}x{h}")


if __name__ == "__main__":
    main()
