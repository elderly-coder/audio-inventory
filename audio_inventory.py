#!/usr/bin/env python3
"""audio-inventory: scan a folder of audio files and write a size/duration report.

Usage:
    python audio_inventory.py ~/voiceovers --format md --out report.md
    python audio_inventory.py . --format json

Requires Python 3.8+. If ffprobe is installed, durations are probed;
otherwise only file sizes are reported.
"""
import argparse
import csv
import io
import json
import os
import subprocess
import sys

AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac", ".wma", ".opus"}


def probe_duration(path):
    """Return audio duration in seconds via ffprobe, or None if unavailable."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, timeout=20)
        return round(float(out.stdout.strip()), 2)
    except Exception:
        return None


def scan(root):
    rows = []
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if os.path.splitext(name)[1].lower() in AUDIO_EXTS:
                full = os.path.join(dirpath, name)
                rows.append({
                    "path": os.path.relpath(full, root),
                    "size_bytes": os.path.getsize(full),
                    "duration_sec": probe_duration(full),
                })
    return rows


def fmt_duration(sec):
    if sec is None:
        return "n/a"
    mins, secs = divmod(int(sec), 60)
    return f"{mins}:{secs:02d}"


def render(rows, fmt):
    if fmt == "json":
        return json.dumps(rows, indent=2) + "\n"
    if fmt == "csv":
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=["path", "size_bytes", "duration_sec"])
        w.writeheader()
        w.writerows(rows)
        return buf.getvalue()
    lines = ["| File | Size | Duration |", "| --- | --- | --- |"]
    total_size = 0
    total_dur = 0.0
    for r in rows:
        total_size += r["size_bytes"]
        if r["duration_sec"]:
            total_dur += r["duration_sec"]
        lines.append(f"| `{r['path']}` | {r['size_bytes']:,} B | "
                     f"{fmt_duration(r['duration_sec'])} |")
    lines.append(f"\n**{len(rows)} files, {total_size:,} bytes total, "
                 f"{fmt_duration(total_dur)} total audio**")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Scan audio files and report size/duration.")
    ap.add_argument("root", help="Folder to scan (searched recursively)")
    ap.add_argument("--format", choices=["md", "json", "csv"], default="md")
    ap.add_argument("--out", help="Write report to this file instead of stdout")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.root):
        sys.exit(f"error: not a folder: {args.root}")

    rows = scan(args.root)
    report = render(rows, args.format)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"wrote {args.out} ({len(rows)} files)")
    else:
        sys.stdout.write(report)


if __name__ == "__main__":
    main()
