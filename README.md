<p align="center">
  <img src="assets/banner.webp" alt="audio-inventory banner: audio waveform rising from a folder" width="100%">
</p>

<h1 align="center">audio-inventory</h1>

<p align="center">
  Point it at a folder of audio. Get a size and duration report.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT license">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Cross platform">
</p>

## Why

Voiceover folders get messy fast. This answers "how many files, how much audio, how big" in one command. I built it to keep my own voiceover folders honest.

## Quick start

No dependencies beyond the standard library. `ffprobe` is optional but recommended for durations (it ships with [ffmpeg](https://ffmpeg.org)).

```bash
python audio_inventory.py ~/voiceovers --format md --out report.md
```

## Usage

```bash
python audio_inventory.py <folder> [--format md|json|csv] [--out file]
```

| Option | Default | Description |
|---|---|---|
| `--format` | `md` | Report format: `md` (Markdown table), `json`, or `csv` |
| `--out` | stdout | Write the report to a file instead of printing it |

Scans recursively. Finds `.mp3 .wav .ogg .m4a .flac .aac .wma .opus`. Durations show as `n/a` when ffprobe is missing.

## Example output

```
| File | Size | Duration |
| --- | --- | --- |
| `00-intro.mp3` | 145,030 B | 0:09 |
| `01-main.mp3` | 135,417 B | 0:08 |

**20 files, 2,812,835 bytes total, 2:55 total audio**
```

## License

[MIT](LICENSE)
