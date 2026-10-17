# yt-grab

Paste a YouTube URL, choose **MP4** (video) or **MP3** (audio), and it downloads to your computer. Videos of any length work, and interrupted downloads resume where they stopped.

Built with Python and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Features

- Download any YouTube video as MP4 at the best available quality
- Convert to MP3 (192 kbps) for audio only
- Interactive mode: paste URLs one after another without restarting
- Resumes partial downloads and retries on network errors
- Downloads only the video in the URL, even if the link is part of a playlist

## Requirements

- Python 3.9 or newer
- [ffmpeg](https://ffmpeg.org/), used to merge video and audio and to create MP3s

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/MatthewTuurozeeng/yt-grab.git
   cd yt-grab
   ```

2. Install the Python dependency:
   ```bash
   pip install -r requirements.txt
   ```

3. Install ffmpeg:

   | System  | Command                    |
   |---------|----------------------------|
   | Windows | `winget install ffmpeg`    |
   | macOS   | `brew install ffmpeg`      |
   | Linux   | `sudo apt install ffmpeg`  |

   Check it worked with `ffmpeg -version`.

## Usage

### Interactive mode

```bash
python yt_download.py
```

Paste a URL, then pick a format:

```
URL> https://www.youtube.com/watch?v=xxxxxxx
  Choose format:
    1) MP4  - keep the video
    2) MP3  - convert to audio only
  Enter 1 or 2: 1
```

Type `q` to quit.

### One-line mode

```bash
python yt_download.py "https://www.youtube.com/watch?v=xxxxxxx"          # asks MP4 or MP3
python yt_download.py "https://www.youtube.com/watch?v=xxxxxxx" --mp4    # video
python yt_download.py "https://www.youtube.com/watch?v=xxxxxxx" --mp3    # audio
```

Put the URL in quotes so your terminal doesn't misread characters like `&`.

## Where files are saved

Downloads go to a `YouTube` folder inside your Downloads folder:

- Windows: `C:\Users\<you>\Downloads\YouTube`
- macOS / Linux: `~/Downloads/YouTube`

To change this, edit `DOWNLOAD_DIR` near the top of `yt_download.py`.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Downloads suddenly fail | YouTube changes things often. Update yt-dlp: `pip install -U yt-dlp` |
| `ffmpeg not found` | Install ffmpeg (see above) and restart your terminal |
| `yt-dlp is not installed` | Run `pip install -r requirements.txt` |
| Download stopped halfway | Run the same URL again; it resumes |

## Disclaimer

This tool is for personal use with content you have the right to download, such as your own uploads, Creative Commons videos, or material whose owner permits downloading. Downloading copyrighted content without permission may violate YouTube's Terms of Service and copyright law in your country. You are responsible for how you use it.

## License

MIT
