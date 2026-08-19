#!/usr/bin/env python3
"""
Assemble final workflow video with:
- FloquetTopoCA intro (10s)
- 2x speed screen recording with timer (673s)
- FloquetTopoCA outro with scrolling text (45s)
- Ashra music tracks
- Song credit card overlays
"""

import subprocess
import os
import sys
from pathlib import Path

# Paths
HOME = Path.home()
MOVIES_DIR = Path(os.environ.get("MOVIES_DIR", str(HOME / "Movies")))
MUSIC_DIR = Path(os.environ.get("MUSIC_DIR", str(MOVIES_DIR / "ashra_music")))
CARDS_DIR = Path(os.environ.get("CARDS_DIR", str(MUSIC_DIR / "cards")))

# Input files
INTRO_VIDEO = MOVIES_DIR / "intro_floquet_4k.mp4"
MAIN_VIDEO = MOVIES_DIR / "screen_recording_2x_with_timer.mp4"
OUTRO_VIDEO = MOVIES_DIR / "floquet_outro.mp4"
SONG_1 = MUSIC_DIR / "01_dont_trust_the_kids.mp3"
SONG_2 = MUSIC_DIR / "02_pas_de_trois.mp3"
CARD_1 = CARDS_DIR / "01_card.mp4"
CARD_2 = CARDS_DIR / "02_card.mp4"

# Output
OUTPUT = Path(os.environ.get("OUTPUT_FILE", str(MOVIES_DIR / "multi_agent_workflow_final.mp4")))

# Durations (in seconds)
INTRO_DURATION = 10.0
MAIN_DURATION = 673.4
OUTRO_DURATION = 45.0
SONG_1_DURATION = 194.87
SONG_2_DURATION = 537.77
CARD_DURATION = 6.0

# Card overlay timing (relative to start of video)
CARD_1_START = 2.0  # Show first card 2s after video starts
CARD_2_START = SONG_1_DURATION + 2.0  # Show second card 2s after song 2 starts

def check_files():
    """Check that all required files exist."""
    missing = []
    for f in [MAIN_VIDEO, SONG_1, SONG_2, CARD_1, CARD_2]:
        if not f.exists():
            missing.append(f)

    # These may still be rendering
    optional_missing = []
    for f in [INTRO_VIDEO, OUTRO_VIDEO]:
        if not f.exists():
            optional_missing.append(f)

    if missing:
        print("Missing required files:")
        for f in missing:
            print(f"  - {f}")
        sys.exit(1)

    if optional_missing:
        print("Still rendering (will wait):")
        for f in optional_missing:
            print(f"  - {f}")
        return False

    return True

def get_duration(path):
    """Get video duration in seconds."""
    result = subprocess.run([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'csv=p=0', str(path)
    ], capture_output=True, text=True)
    return float(result.stdout.strip())

def assemble():
    """Assemble the final video."""
    print("=" * 60)
    print("Assembling Multi-Agent Workflow Video")
    print("=" * 60)

    # Get actual durations
    intro_dur = get_duration(INTRO_VIDEO)
    main_dur = get_duration(MAIN_VIDEO)
    outro_dur = get_duration(OUTRO_VIDEO) if OUTRO_VIDEO.exists() else OUTRO_DURATION

    total_video_dur = intro_dur + main_dur + (outro_dur if OUTRO_VIDEO.exists() else 0)

    print("\nVideo components:")
    print(f"  Intro: {intro_dur:.1f}s")
    print(f"  Main:  {main_dur:.1f}s")
    if OUTRO_VIDEO.exists():
        print(f"  Outro: {outro_dur:.1f}s")
    print(f"  Total: {total_video_dur:.1f}s ({total_video_dur/60:.1f} min)")

    # Calculate card overlay positions (relative to concatenated video)
    card_1_pos = intro_dur + CARD_1_START
    card_2_pos = intro_dur + SONG_1_DURATION + 2.0

    print("\nCard overlays:")
    print(f"  Card 1 at: {card_1_pos:.1f}s")
    print(f"  Card 2 at: {card_2_pos:.1f}s")

    # Step 1: Concatenate videos
    print("\n[Step 1] Concatenating video segments...")

    concat_list = Path("/tmp/concat_list.txt")
    with open(concat_list, 'w') as f:
        f.write(f"file '{INTRO_VIDEO}'\n")
        f.write(f"file '{MAIN_VIDEO}'\n")
        if OUTRO_VIDEO.exists():
            f.write(f"file '{OUTRO_VIDEO}'\n")

    concat_output = Path("/tmp/concat_video.mp4")
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', str(concat_list),
        '-c', 'copy', str(concat_output)
    ], check=True)

    # Step 2: Add card overlays
    print("\n[Step 2] Adding song credit card overlays...")

    # Card overlay dimensions and position (bottom right with padding)
    # Cards are 2280x480, need to scale down for 4K video
    scale_factor = 0.4  # Scale to about 912x192
    card_w = int(2280 * scale_factor)
    card_h = int(480 * scale_factor)
    margin = 48

    overlay_output = Path("/tmp/overlay_video.mp4")

    # Complex filter for overlaying both cards
    filter_complex = f"""
[1:v]scale={card_w}:{card_h}[card1];
[2:v]scale={card_w}:{card_h}[card2];
[0:v][card1]overlay=W-w-{margin}:{margin}:enable='between(t,{card_1_pos},{card_1_pos + CARD_DURATION})'[v1];
[v1][card2]overlay=W-w-{margin}:{margin}:enable='between(t,{card_2_pos},{card_2_pos + CARD_DURATION})'[vout]
"""

    subprocess.run([
        'ffmpeg', '-y',
        '-i', str(concat_output),
        '-i', str(CARD_1),
        '-i', str(CARD_2),
        '-filter_complex', filter_complex,
        '-map', '[vout]',
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
        '-pix_fmt', 'yuv420p',
        str(overlay_output)
    ], check=True)

    # Step 3: Concatenate and mix audio
    print("\n[Step 3] Adding music tracks...")

    # Calculate music fade points
    music_end = total_video_dur
    fade_start = music_end - 5.0  # 5 second fade out

    audio_filter = f"""
[0:a]asetpts=PTS-STARTPTS[a1];
[1:a]asetpts=PTS-STARTPTS,adelay={int(SONG_1_DURATION * 1000)}[a2];
[a1][a2]amix=inputs=2:duration=longest,afade=t=out:st={fade_start}:d=5[aout]
"""

    subprocess.run([
        'ffmpeg', '-y',
        '-i', str(SONG_1),
        '-i', str(SONG_2),
        '-filter_complex', audio_filter,
        '-map', '[aout]',
        '-c:a', 'aac', '-b:a', '192k',
        '-t', str(total_video_dur),
        '/tmp/mixed_audio.m4a'
    ], check=True)

    # Step 4: Combine video and audio
    print("\n[Step 4] Combining video and audio...")

    subprocess.run([
        'ffmpeg', '-y',
        '-i', str(overlay_output),
        '-i', '/tmp/mixed_audio.m4a',
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-shortest',
        str(OUTPUT)
    ], check=True)

    # Get final file info
    final_dur = get_duration(OUTPUT)
    final_size = OUTPUT.stat().st_size / (1024 * 1024)

    print("\n" + "=" * 60)
    print("Final Video Created!")
    print("=" * 60)
    print(f"  File: {OUTPUT}")
    print(f"  Duration: {final_dur:.1f}s ({final_dur/60:.1f} min)")
    print(f"  Size: {final_size:.1f} MB")

    # Cleanup
    print("\nCleaning up temp files...")
    for f in [concat_list, concat_output, overlay_output, Path('/tmp/mixed_audio.m4a')]:
        if f.exists():
            f.unlink()

if __name__ == "__main__":
    if not check_files():
        print("\nWaiting for rendering to complete...")
        print("Run this script again once intro/outro are ready.")
        sys.exit(0)

    assemble()
