#!/usr/bin/env python3
"""
watch.py — core of the video-watch skill.

Given a URL (anything yt-dlp supports) or a local video file, produces:
  - a sampled, deduplicated set of JPEG frames with timestamps
  - a timestamped transcript (captions if available, Whisper API fallback)
printed to stdout so the calling agent can Read() each frame and the
transcript, then answer grounded in what it actually saw and heard.

No third-party Python packages. Shells out to yt-dlp / ffmpeg / ffprobe
(and curl for the optional Whisper fallback).
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

FRAME_BUDGET_TIERS = [
    (30, 30),
    (60, 40),
    (180, 60),
    (600, 80),
]
FRAME_BUDGET_MAX = 100
FOCUSED_FPS_CAP = 2.0
DEDUP_THRESHOLD = 2.0
FRAME_WIDTH = 512


def die(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def check_deps(need_ytdlp):
    required = ("yt-dlp", "ffmpeg", "ffprobe") if need_ytdlp else ("ffmpeg", "ffprobe")
    missing = [b for b in required if shutil.which(b) is None]
    if not missing:
        return
    hints = {
        "darwin": "brew install yt-dlp ffmpeg",
        "linux": "sudo apt install ffmpeg && pipx install yt-dlp  # or your distro's equivalent",
        "win32": "winget install yt-dlp.yt-dlp Gyan.FFmpeg  # or: choco install yt-dlp ffmpeg",
    }
    hint = hints.get(sys.platform, "install yt-dlp and ffmpeg for your platform")
    die(f"missing required tool(s): {', '.join(missing)}. Install with: {hint}")


def is_url(s):
    return re.match(r"^https?://", s) is not None


def fmt_ts(seconds, decimal=False):
    whole = max(0.0, seconds)
    h, rem = divmod(int(whole), 3600)
    m, s = divmod(rem, 60)
    if decimal:
        s = s + (whole - int(whole))
        sec_str = f"{s:04.1f}"
    else:
        sec_str = f"{s:02d}"
    return f"{h:02d}:{m:02d}:{sec_str}" if h else f"{m:02d}:{sec_str}"


def parse_ts(ts):
    """'00:00:01.000' or '00:01.000' -> seconds (float)."""
    parts = ts.replace(",", ".").split(":")
    parts = [float(p) for p in parts]
    while len(parts) < 3:
        parts.insert(0, 0.0)
    h, m, s = parts
    return h * 3600 + m * 60 + s


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def download(url, workdir, want_video, sub_langs):
    """One combined yt-dlp call: video (optional) + subs (best-effort)."""
    out_tpl = os.path.join(workdir, "source.%(ext)s")
    cmd = ["yt-dlp", "--no-playlist", "-o", out_tpl]
    if want_video:
        cmd += ["-f", "bv*[height<=720]+ba/b[height<=720]"]
    else:
        cmd += ["--skip-download"]
    cmd += [
        "--write-subs", "--write-auto-subs",
        "--sub-format", "vtt", "--sub-langs", sub_langs,
        "--no-warnings", url,
    ]
    res = run(cmd)
    if res.returncode != 0 and want_video:
        die(f"yt-dlp failed:\n{res.stderr.strip()[-2000:]}")

    video_path = None
    vtt_path = None
    for name in sorted(os.listdir(workdir)):
        full = os.path.join(workdir, name)
        if name.startswith("source.") and name.endswith(".vtt") and vtt_path is None:
            vtt_path = full
        elif name.startswith("source.") and not name.endswith(".vtt") and video_path is None:
            video_path = full
    return video_path, vtt_path


def parse_vtt(path):
    """Return [(start_seconds, text), ...], deduped for auto-caption cue-rolling."""
    text = open(path, encoding="utf-8", errors="replace").read()
    blocks = re.split(r"\n\n+", text)
    cues = []
    ts_re = re.compile(r"(\d+:\d{2}(?::\d{2})?\.\d{3})\s*-->\s*(\d+:\d{2}(?::\d{2})?\.\d{3})")
    tag_re = re.compile(r"<[^>]+>")
    for block in blocks:
        m = ts_re.search(block)
        if not m:
            continue
        start = parse_ts(m.group(1))
        lines = block[m.end():].strip().splitlines()
        clean = " ".join(tag_re.sub("", ln).strip() for ln in lines if ln.strip())
        if clean:
            cues.append((start, clean))
    # Auto-captions frequently repeat the same line across consecutive cues
    # (rolling/karaoke style) — drop exact consecutive repeats.
    deduped = []
    for start, txt in cues:
        if deduped and deduped[-1][1] == txt:
            continue
        deduped.append((start, txt))
    return deduped


def whisper_transcript(video_path, workdir):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    audio_path = os.path.join(workdir, "audio.mp3")
    res = run(["ffmpeg", "-y", "-i", video_path, "-vn", "-ac", "1", "-ar", "16000",
               "-b:a", "64k", audio_path])
    if res.returncode != 0 or not os.path.exists(audio_path):
        print(f"WARN: audio extraction failed, no transcript: {res.stderr.strip()[-500:]}",
              file=sys.stderr)
        return None
    res = run(["curl", "-s", "https://api.openai.com/v1/audio/transcriptions",
               "-H", f"Authorization: Bearer {api_key}",
               "-F", f"file=@{audio_path}",
               "-F", "model=whisper-1",
               "-F", "response_format=verbose_json"])
    try:
        data = json.loads(res.stdout)
    except json.JSONDecodeError:
        print(f"WARN: Whisper API returned unparseable response, no transcript",
              file=sys.stderr)
        return None
    segments = data.get("segments")
    if not segments:
        return None
    return [(seg["start"], seg["text"].strip()) for seg in segments if seg.get("text", "").strip()]


def frame_budget(duration, start, end):
    if start is not None and end is not None:
        window = max(0.0, end - start)
        return max(4, min(FRAME_BUDGET_MAX, int(window * FOCUSED_FPS_CAP)))
    for limit, budget in FRAME_BUDGET_TIERS:
        if duration <= limit:
            return budget
    return FRAME_BUDGET_MAX


def get_duration(video_path):
    res = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1:nokey=1", video_path])
    try:
        return float(res.stdout.strip())
    except ValueError:
        die(f"could not read duration from {video_path}")


def extract_frames(video_path, workdir, duration, start, end, budget):
    frame_dir = os.path.join(workdir, "frames")
    os.makedirs(frame_dir, exist_ok=True)
    window = (end - start) if (start is not None and end is not None) else duration
    fps = budget / max(window, 0.1)
    cmd = ["ffmpeg", "-y"]
    if start is not None:
        cmd += ["-ss", str(start)]
    cmd += ["-i", video_path]
    if end is not None and start is not None:
        cmd += ["-t", str(end - start)]
    cmd += ["-vf", f"fps={fps:.6f},scale={FRAME_WIDTH}:-2",
            "-q:v", "3", os.path.join(frame_dir, "frame_%04d.jpg")]
    res = run(cmd)
    if res.returncode != 0:
        die(f"ffmpeg frame extraction failed:\n{res.stderr.strip()[-1500:]}")
    frames = sorted(os.path.join(frame_dir, f) for f in os.listdir(frame_dir)
                     if f.endswith(".jpg"))
    offset = start or 0.0
    timestamps = [offset + i * (window / max(len(frames), 1)) for i in range(len(frames))]
    return list(zip(frames, timestamps))


def thumbnail_bytes(frame_path):
    res = subprocess.run(
        ["ffmpeg", "-y", "-i", frame_path, "-vf", "scale=16:16,format=gray",
         "-f", "rawvideo", "-"],
        capture_output=True,
    )
    return res.stdout  # 256 grayscale bytes on success, b"" on failure


def mean_abs_diff(a, b):
    if not a or not b or len(a) != len(b):
        return 999.0
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def dedup(frames):
    """frames: [(path, ts), ...]. Always keeps first and last."""
    if len(frames) <= 2:
        return frames, 0
    kept = [frames[0]]
    ref = thumbnail_bytes(frames[0][0])
    dropped = 0
    for path, ts in frames[1:-1]:
        thumb = thumbnail_bytes(path)
        if mean_abs_diff(ref, thumb) <= DEDUP_THRESHOLD:
            dropped += 1
            os.remove(path)
            continue
        kept.append((path, ts))
        ref = thumb
    kept.append(frames[-1])
    return kept, dropped


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", help="video URL or local file path")
    ap.add_argument("--start", help="focus window start, HH:MM:SS or seconds")
    ap.add_argument("--end", help="focus window end, HH:MM:SS or seconds")
    ap.add_argument("--no-frames", action="store_true", help="transcript only, skip frames/video download")
    ap.add_argument("--sub-langs", default="en.*,de.*", help="yt-dlp --sub-langs value")
    ap.add_argument("--keep", action="store_true", help="do not print the workdir as a cleanup candidate")
    args = ap.parse_args()

    def to_seconds(v):
        if v is None:
            return None
        return float(v) if re.match(r"^\d+(\.\d+)?$", v) else parse_ts(v)

    start, end = to_seconds(args.start), to_seconds(args.end)
    if (start is None) != (end is None):
        die("--start and --end must be given together")
    check_deps(need_ytdlp=is_url(args.source))
    workdir = tempfile.mkdtemp(prefix="video-watch-")

    if is_url(args.source):
        video_path, vtt_path = download(args.source, workdir, want_video=not args.no_frames,
                                          sub_langs=args.sub_langs)
    else:
        if not os.path.exists(args.source):
            die(f"local file not found: {args.source}")
        video_path, vtt_path = args.source, None

    transcript = parse_vtt(vtt_path) if vtt_path else None
    if transcript is None and video_path and not args.no_frames:
        transcript = whisper_transcript(video_path, workdir)

    print(f"=== SOURCE: {args.source} ===")

    if transcript:
        source = "captions" if vtt_path else "whisper"
        print(f"\n=== TRANSCRIPT ({source}) ===")
        for ts, text in transcript:
            print(f"[{fmt_ts(ts)}] {text}")
    else:
        print("\n=== TRANSCRIPT: none (no captions, no OPENAI_API_KEY for Whisper fallback) ===")

    if not args.no_frames and video_path:
        duration = get_duration(video_path)
        budget = frame_budget(duration, start, end)
        frames = extract_frames(video_path, workdir, duration, start, end, budget)
        kept, dropped = dedup(frames)
        print(f"\n=== FRAMES: {len(kept)} kept from {len(frames)} extracted "
              f"({dropped} near-duplicates dropped) ===")
        for path, ts in kept:
            print(f"{path}  t={fmt_ts(ts, decimal=True)}")
        if duration > 600 and end is None:
            print(f"NOTE: {fmt_ts(duration)} video capped at {FRAME_BUDGET_MAX} frames — "
                  f"sparse coverage. Re-run with --start/--end for a focused, denser pass.",
                  file=sys.stderr)

    if not args.keep:
        print(f"\n=== WORKDIR: {workdir} (rm -rf if no follow-up questions) ===")


if __name__ == "__main__":
    main()
