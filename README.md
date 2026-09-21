# audio-inventory

<!-- toc -->
- [audio-inventory](#audio-inventory)
  - [Requirements](#requirements)
  - [Usage](#usage)
<!-- /toc -->


Scan a folder of audio files and get a size/duration report. Built for keeping
voiceover folders honest — point it at a directory, get a table.

## Requirements

Python 3.8+. `ffprobe` is optional but recommended for durations (ships with
[ffmpeg](https://ffmpeg.org)).

## Usage

```bash
python audio_inventory.py ~/voiceovers --format md --out report.md
python audio_inventory.py . --format json
python audio_inventory.py . --format csv --out report.csv
```

Output formats: `md` (Markdown table, default), `json`, `csv`.

Files are found recursively. Durations show `n/a` when ffprobe is missing.
