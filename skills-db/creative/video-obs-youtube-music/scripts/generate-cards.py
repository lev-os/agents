#!/usr/bin/env python3
"""
Generate animated song credit card overlays for OBS recordings.

Downloads songs with metadata, creates animated HTML cards, records them as
WebM videos with transparency, and outputs ffmpeg overlay commands.

Usage:
    ./generate-cards.py --songs "Artist - Song 1" "Artist - Song 2" --output-dir ./cards
"""

import argparse
import html
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path


# Card dimensions (6x original for better visibility)
CARD_WIDTH = 2280
CARD_HEIGHT = 480

# Video card duration (animations baked into video)
CARD_VIDEO_DURATION = 6.0  # seconds

CARD_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 2280px;
      height: 480px;
      background: transparent;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }

    @keyframes cardEntry {
      0% {
        transform: scale(0.85) translateY(20px);
        opacity: 0;
      }
      8% {
        transform: scale(1.02) translateY(-5px);
        opacity: 1;
      }
      15% {
        transform: scale(1) translateY(0);
        opacity: 1;
      }
      85% {
        transform: scale(1) translateY(0);
        opacity: 1;
      }
      92% {
        transform: scale(1.02) translateY(-5px);
        opacity: 1;
      }
      100% {
        transform: scale(0.85) translateY(20px);
        opacity: 0;
      }
    }

    @keyframes float {
      0%, 100% { transform: translateY(0px); }
      50% { transform: translateY(-8px); }
    }

    @keyframes pulse {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.15); }
    }

    @keyframes shimmer {
      0% { background-position: -200% center; }
      100% { background-position: 200% center; }
    }

    @keyframes glowPulse {
      0%, 100% { box-shadow: 0 24px 120px rgba(0, 0, 0, 0.4), 0 0 60px rgba(255, 255, 255, 0.05); }
      50% { box-shadow: 0 24px 120px rgba(0, 0, 0, 0.4), 0 0 80px rgba(255, 255, 255, 0.12); }
    }

    .card-wrapper {
      animation: cardEntry 6s ease-in-out forwards;
    }

    .card {
      display: flex;
      align-items: center;
      gap: 72px;
      padding: 60px 84px;
      background: linear-gradient(135deg, rgba(30, 30, 40, 0.9) 0%, rgba(10, 10, 15, 0.95) 100%);
      backdrop-filter: blur(20px);
      border-radius: 72px;
      border: 2px solid rgba(255, 255, 255, 0.1);
      height: 456px;
      animation: glowPulse 3s ease-in-out infinite, float 4s ease-in-out infinite;
      position: relative;
      overflow: hidden;
    }

    .card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
      background-size: 200% 100%;
      animation: shimmer 3s ease-in-out infinite;
    }

    .thumbnail {
      width: 336px;
      height: 336px;
      border-radius: 48px;
      object-fit: cover;
      flex-shrink: 0;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
      border: 3px solid rgba(255, 255, 255, 0.15);
    }

    .info {
      flex: 1;
      min-width: 0;
      color: white;
    }

    .now-playing {
      font-size: 48px;
      text-transform: uppercase;
      letter-spacing: 8px;
      color: rgba(255, 255, 255, 0.5);
      margin-bottom: 24px;
      font-weight: 500;
    }

    .title {
      font-size: 84px;
      font-weight: 700;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      line-height: 1.2;
      text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }

    .icon-container {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 140px;
      height: 140px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 50%;
      flex-shrink: 0;
    }

    .icon {
      width: 80px;
      height: 80px;
      fill: rgba(255, 255, 255, 0.7);
      animation: pulse 1.5s ease-in-out infinite;
    }
  </style>
</head>
<body>
  <div class="card-wrapper">
    <div class="card">
      <img class="thumbnail" src="THUMBNAIL_URL" alt="">
      <div class="info">
        <div class="now-playing">Now Playing</div>
        <div class="title">SONG_TITLE</div>
      </div>
      <div class="icon-container">
        <svg class="icon" viewBox="0 0 24 24">
          <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
        </svg>
      </div>
    </div>
  </div>
</body>
</html>"""


def download_song_with_metadata(query: str, output_dir: Path) -> dict:
    """Download song and return metadata including title, duration, thumbnail."""
    # Get metadata first
    result = subprocess.run(
        ["yt-dlp", "--print-json", "--no-download", f"ytsearch1:{query}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error getting metadata for '{query}'", file=sys.stderr)
        return None

    try:
        meta = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error parsing metadata for '{query}': {e}", file=sys.stderr)
        return None

    # Download audio
    # Build output template: use .%(ext)s so yt-dlp fills in the extension
    audio_template = output_dir / f"{meta['id']}.%(ext)s"
    audio_path = output_dir / f"{meta['id']}.mp3"
    try:
        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "mp3",
            "-o", str(audio_template),
            meta["webpage_url"]
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio for '{query}': {e}", file=sys.stderr)
        return None

    # Download thumbnail
    thumb_path = output_dir / f"{meta['id']}_thumb.jpg"
    thumb_url = meta.get("thumbnail", "")
    thumb_downloaded = False
    if thumb_url:
        try:
            urllib.request.urlretrieve(thumb_url, thumb_path)
            thumb_downloaded = True
        except Exception as e:
            print(f"Warning: Could not download thumbnail: {e}", file=sys.stderr)

    return {
        "id": meta["id"],
        "title": meta.get("title", query),
        "duration": meta.get("duration", 0),
        "audio_path": str(audio_path),
        "thumbnail_path": str(thumb_path) if thumb_downloaded else None,
        "thumbnail_url": thumb_url
    }


def generate_card_html(song: dict, output_dir: Path) -> Path:
    """Generate HTML file for the song card."""
    html_content = CARD_TEMPLATE

    # Replace THUMBNAIL_URL first (before inserting user content that might contain this string)
    # Note: file:// URLs require absolute paths and URL encoding for special chars
    if song.get("thumbnail_path") and Path(song["thumbnail_path"]).exists():
        abs_thumb_path = Path(song["thumbnail_path"]).absolute()
        # URL-encode the path (safe='/' preserves path separators)
        encoded_path = urllib.parse.quote(str(abs_thumb_path), safe='/')
        html_content = html_content.replace("THUMBNAIL_URL", f"file://{encoded_path}")
    else:
        # HTML-escape the URL in case it contains special characters
        safe_url = html.escape(song.get("thumbnail_url", ""))
        html_content = html_content.replace("THUMBNAIL_URL", safe_url)

    # Replace SONG_TITLE last (user content could theoretically contain placeholder strings)
    # Escape HTML special characters to prevent XSS/broken HTML
    safe_title = html.escape(song["title"])
    html_content = html_content.replace("SONG_TITLE", safe_title)

    html_path = output_dir / f"{song['id']}_card.html"
    html_path.write_text(html_content)
    return html_path


def record_card_video(html_path: Path, output_path: Path, duration_ms: int = 6000):
    """Use Playwright to record an animated video of the HTML card."""
    # Use the helper script in the same directory
    script_dir = Path(__file__).parent
    screenshot_script = script_dir / "screenshot-html.js"

    if not screenshot_script.exists():
        raise FileNotFoundError(f"Screenshot script not found: {screenshot_script}")

    subprocess.run([
        "node", str(screenshot_script),
        str(html_path.absolute()),
        str(output_path),
        str(CARD_WIDTH), str(CARD_HEIGHT),
        str(duration_ms)
    ], check=True)


def generate_ffmpeg_overlay_args(songs: list, num_audio_inputs: int = 1,
                                  margin: int = 40, card_video_duration: float = 6.0) -> tuple:
    """
    Generate ffmpeg input args and filter_complex for overlaying animated video cards.

    Since card animations (fade, scale, effects) are baked into the video,
    ffmpeg only needs to position and time the overlay.

    Args:
        songs: List of song dicts with 'card_path' and 'duration' keys
        num_audio_inputs: Number of audio inputs (to calculate correct input indices)
        margin: Pixels from edge for card positioning (default 40 for larger cards)
        card_video_duration: Duration of each card video in seconds

    Returns:
        (input_args, filter_complex, final_video_label)
    """
    input_args = []
    filters = []

    cumulative_time = 0.0
    prev_overlay = "0:v"
    card_input_count = 0  # Track actual number of card inputs added

    for song in songs:
        card_path = song.get("card_path")
        if not card_path:
            cumulative_time += song.get("duration", 0)
            continue

        input_args.extend(["-i", card_path])
        # Input index = 1 (video) + num_audio_inputs + card_input_count
        input_idx = 1 + num_audio_inputs + card_input_count
        card_input_count += 1

        start = cumulative_time
        end = start + card_video_duration

        overlay_name = f"v{card_input_count}"

        # Overlay the animated video card (animations already baked in)
        # Use ffmpeg's dynamic W (width) and H (height) for positioning
        # eof_action=pass means continue main video after card ends
        # shortest=0 ensures the main video isn't cut short
        overlay = (
            f"[{prev_overlay}][{input_idx}:v]overlay="
            f"x=W-w-{margin}:y=H-h-{margin}:"
            f"enable='between(t,{start:.2f},{end:.2f})':"
            f"eof_action=pass[{overlay_name}]"
        )
        filters.append(overlay)
        prev_overlay = overlay_name

        cumulative_time += song.get("duration", 0)

    filter_complex = ";".join(filters) if filters else None
    final_video = prev_overlay

    return input_args, filter_complex, final_video


def main():
    parser = argparse.ArgumentParser(description="Generate song credit cards for video overlay")
    parser.add_argument("--songs", nargs="+", required=True, help="Song search queries")
    parser.add_argument("--output-dir", type=Path, default=Path("./cards"), help="Output directory")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    songs = []
    video_duration_ms = int(CARD_VIDEO_DURATION * 1000)

    for query in args.songs:
        print(f"Processing: {query}")
        song = download_song_with_metadata(query, args.output_dir)
        if song:
            # Generate HTML card with animations
            html_path = generate_card_html(song, args.output_dir)

            # Record animated video card
            card_path = args.output_dir / f"{song['id']}_card.webm"
            try:
                print(f"  Recording animated card video ({CARD_VIDEO_DURATION}s)...")
                record_card_video(html_path, card_path, video_duration_ms)
                song["card_path"] = str(card_path)
            except Exception as e:
                print(f"Warning: Could not record card video: {e}", file=sys.stderr)

            songs.append(song)

    # Output song info as JSON
    manifest = args.output_dir / "songs.json"
    manifest.write_text(json.dumps(songs, indent=2))
    print(f"\nSong manifest written to: {manifest}")

    # Generate ffmpeg overlay hint
    num_audio = len(songs)  # Assuming one audio input per song
    input_args, filter_complex, final_video = generate_ffmpeg_overlay_args(songs, num_audio_inputs=num_audio)

    if filter_complex:
        print("\n--- ffmpeg overlay filter ---")
        print(f"Additional inputs: {' '.join(input_args)}")
        print(f"Filter complex: {filter_complex}")
        print(f"Map final video: [{final_video}]")


if __name__ == "__main__":
    main()
