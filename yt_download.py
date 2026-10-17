#!/usr/bin/env python3
"""
yt_download.py - Download YouTube videos (or just the audio) by pasting a URL.

Usage:
    python yt_download.py                 # interactive: paste a URL, then pick MP4 or MP3
    python yt_download.py <URL>           # asks whether you want MP4 or MP3
    python yt_download.py <URL> --mp4     # skip the question, keep the video
    python yt_download.py <URL> --mp3     # skip the question, convert to MP3

Requirements:
    pip install -U yt-dlp
    ffmpeg installed on your system (needed to merge video+audio and make MP3s)
"""

import sys
from pathlib import Path
from typing import Optional

try:
    import yt_dlp
except ImportError:
    sys.exit("yt-dlp is not installed. Run:  pip install -U yt-dlp")

# Where files are saved: a "YouTube" folder inside your Downloads folder
DOWNLOAD_DIR = Path.home() / "Downloads" / "YouTube"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def progress_hook(d):
    """Print a simple one-line progress indicator."""
    if d["status"] == "downloading":
        pct = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        print(f"\r  Downloading... {pct}  at {speed}  ETA {eta}     ", end="", flush=True)
    elif d["status"] == "finished":
        print("\n  Download finished, processing file...")


def build_options(audio_only: bool) -> dict:
    opts = {
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s [%(id)s].%(ext)s"),
        "progress_hooks": [progress_hook],
        "noplaylist": True,          # only the video in the URL, not the whole playlist
        "continuedl": True,          # resume partially downloaded files
        "retries": 10,               # retry on network hiccups (useful for long videos)
        "fragment_retries": 10,
        "quiet": True,
        "no_warnings": True,
    }
    if audio_only:
        opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        opts.update({
            # best video + best audio, merged into one MP4
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        })
    return opts


def download(url: str, audio_only: bool = False) -> None:
    url = url.strip()
    if not url:
        return
    print(f"\nFetching: {url}")
    try:
        with yt_dlp.YoutubeDL(build_options(audio_only)) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "video")
            print(f"  Saved: {title}")
            print(f"  Folder: {DOWNLOAD_DIR}")
    except yt_dlp.utils.DownloadError as e:
        print(f"\n  Could not download: {e}")
    except KeyboardInterrupt:
        print("\n  Cancelled. Run again with the same URL to resume.")


def ask_format() -> Optional[bool]:
    """Ask whether to keep the video (MP4) or convert to MP3.
    Returns True for MP3, False for MP4, None if cancelled."""
    print("  Choose format:")
    print("    1) MP4  - keep the video")
    print("    2) MP3  - convert to audio only")
    while True:
        try:
            choice = input("  Enter 1 or 2: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if choice in {"1", "mp4", "video", "v"}:
            return False
        if choice in {"2", "mp3", "audio", "a"}:
            return True
        print("  Please type 1 or 2.")


def interactive() -> None:
    print("YouTube Downloader")
    print(f"Files are saved to: {DOWNLOAD_DIR}")
    print("Paste a URL and press Enter. Type 'q' to quit.\n")
    while True:
        try:
            url = input("URL> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if url.lower() in {"q", "quit", "exit"}:
            print("Bye!")
            break
        if not url:
            continue
        audio = ask_format()
        if audio is None:
            print("  Skipped.")
            continue
        download(url, audio_only=audio)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        interactive()
    else:
        urls = [a for a in args if not a.startswith("--")]
        if "--audio" in args or "--mp3" in args:
            audio_flag = True
        elif "--video" in args or "--mp4" in args:
            audio_flag = False
        else:
            audio_flag = ask_format()
            if audio_flag is None:
                sys.exit("Cancelled.")
        for u in urls:
            download(u, audio_only=audio_flag)
