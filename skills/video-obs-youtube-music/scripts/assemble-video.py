#!/usr/bin/env python3
"""
Assemble final video with intro, sped-up screen recording, and timer overlay.

This script:
1. Speeds up screen recording to 2x with frame interpolation to 60fps
2. Adds a stylish timer overlay using ffmpeg drawtext
3. Concatenates intro video with processed recording (with crossfade)
4. Outputs final video ready for upload

Usage:
    ./assemble-video.py --intro intro.mp4 --recording screen.mp4 --output final.mp4
"""

import argparse
import json
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path


def get_video_info(video_path: Path) -> dict:
    """Get video metadata using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        str(video_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")

    data = json.loads(result.stdout)
    video_stream = next(
        (s for s in data.get("streams", []) if s.get("codec_type") == "video"),
        None
    )

    if not video_stream:
        raise RuntimeError(f"No video stream found in {video_path}")

    # Parse frame rate (can be "30/1" or "30000/1001")
    fps_str = video_stream.get("r_frame_rate", "30/1")
    if "/" in fps_str:
        num, den = fps_str.split("/")
        fps = float(num) / float(den)
    else:
        fps = float(fps_str)

    return {
        "width": int(video_stream.get("width", 0)),
        "height": int(video_stream.get("height", 0)),
        "duration": float(data.get("format", {}).get("duration", 0)),
        "fps": fps,
        "codec": video_stream.get("codec_name", "unknown")
    }


def build_timer_filter(
    width: int,
    height: int,
    speed_factor: float,
    font_path: str = None
) -> str:
    """
    Build ffmpeg drawtext filter for animated timer overlay.

    The timer shows elapsed time at the sped-up rate (e.g., 2x).
    Uses a stylish design with a background box and monospace font.
    """
    # Calculate sizes based on video dimensions
    font_size = int(height * 0.028)
    badge_font_size = int(height * 0.020)
    padding_x = int(width * 0.015)
    int(height * 0.012)
    margin = int(width * 0.025)
    margin_top = int(height * 0.03)
    int(height * 0.008)

    # Font - prefer monospace
    font = font_path or "/System/Library/Fonts/SFNSMono.ttf"
    # Fallback to common monospace fonts
    if not Path(font).exists():
        for candidate in [
            "/System/Library/Fonts/Monaco.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/TTF/DejaVuSansMono.ttf"
        ]:
            if Path(candidate).exists():
                font = candidate
                break

    # Timer expression: displays time at speed_factor rate
    # t = current time in seconds, we want to show t * speed_factor
    # Format as MM:SS
    time_expr = (
        f"'%{{eif\\:floor((t*{speed_factor})/60)\\:d\\:2}}\\:"
        f"%{{eif\\:mod(floor(t*{speed_factor})\\,60)\\:d\\:2}}'"
    )

    # Build the filter chain
    # First: draw background box
    # Second: draw "2X" badge
    # Third: draw timer text
    filters = []

    # Background box (semi-transparent black with rounded appearance via padding)
    # Using a filled rectangle
    box_x = margin
    box_y = margin_top
    box_w = int(width * 0.12)
    box_h = int(height * 0.055)

    # Draw semi-transparent background
    filters.append(
        f"drawbox=x={box_x}:y={box_y}:w={box_w}:h={box_h}:"
        f"color=black@0.65:t=fill"
    )

    # Draw border/highlight on top
    filters.append(
        f"drawbox=x={box_x}:y={box_y}:w={box_w}:h=2:"
        f"color=white@0.15:t=fill"
    )

    # Draw "2X" speed badge (orange background)
    badge_x = margin + padding_x
    badge_y = margin_top + int(box_h * 0.25)
    badge_w = int(width * 0.025)
    badge_h = int(height * 0.03)

    filters.append(
        f"drawbox=x={badge_x}:y={badge_y}:w={badge_w}:h={badge_h}:"
        f"color=0xFF6020@0.9:t=fill"
    )

    # Draw "2X" text
    badge_text_x = badge_x + int(badge_w * 0.15)
    badge_text_y = badge_y + int(badge_h * 0.15)
    speed_label = f"{int(speed_factor)}X" if speed_factor == int(speed_factor) else f"{speed_factor}X"

    filters.append(
        f"drawtext=text='{speed_label}':"
        f"fontfile='{font}':"
        f"fontsize={badge_font_size}:"
        f"fontcolor=white:"
        f"x={badge_text_x}:y={badge_text_y}:"
        f"shadowcolor=black@0.5:shadowx=1:shadowy=1"
    )

    # Draw timer text
    timer_x = badge_x + badge_w + int(width * 0.015)
    timer_y = margin_top + int(box_h * 0.28)

    filters.append(
        f"drawtext=text={time_expr}:"
        f"fontfile='{font}':"
        f"fontsize={font_size}:"
        f"fontcolor=white@0.95:"
        f"x={timer_x}:y={timer_y}:"
        f"shadowcolor=0xFF8040@0.5:shadowx=0:shadowy=0:borderw=1:bordercolor=0xFF8040@0.3"
    )

    return ",".join(filters)


def speed_up_with_timer(
    input_path: Path,
    output_path: Path,
    speed_factor: float = 2.0,
    output_fps: int = 60,
    use_interpolation: bool = True,
    add_timer: bool = True,
    video_info: dict = None
) -> None:
    """
    Speed up video with optional frame interpolation and timer overlay.
    """
    if video_info is None:
        video_info = get_video_info(input_path)

    filters = []

    # Speed up video using setpts
    pts_factor = 1.0 / speed_factor
    filters.append(f"setpts={pts_factor}*PTS")

    # Frame interpolation using minterpolate for smoother output
    if use_interpolation:
        # minterpolate creates smooth motion between frames
        # Using blend mode for better quality at high speeds
        filters.append(
            f"minterpolate=fps={output_fps}:mi_mode=blend"
        )
    else:
        # Simple fps filter without interpolation
        filters.append(f"fps={output_fps}")

    # Add timer overlay
    if add_timer:
        timer_filter = build_timer_filter(
            video_info["width"],
            video_info["height"],
            speed_factor
        )
        filters.append(timer_filter)

    filter_complex = ",".join(filters)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-vf", filter_complex,
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-an",  # No audio for now
        str(output_path)
    ]

    print(f"Processing video: {speed_factor}x speed, {output_fps}fps")
    print(f"  Interpolation: {'blend mode' if use_interpolation else 'none'}")
    print(f"  Timer overlay: {'yes' if add_timer else 'no'}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg stderr: {result.stderr}", file=sys.stderr)
            raise subprocess.CalledProcessError(result.returncode, cmd)
    except subprocess.CalledProcessError as e:
        print(f"Error processing video: {e}", file=sys.stderr)
        sys.exit(1)


def concatenate_with_crossfade(
    intro_path: Path,
    recording_path: Path,
    output_path: Path,
    crossfade_duration: float = 1.0
) -> None:
    """
    Concatenate intro and recording with crossfade transition.
    """
    intro_info = get_video_info(intro_path)
    intro_duration = intro_info["duration"]

    # xfade offset = when fade starts (end of intro minus fade duration)
    offset = max(0, intro_duration - crossfade_duration)

    filter_complex = (
        f"[0:v][1:v]xfade=transition=fade:duration={crossfade_duration}:offset={offset}[outv]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(intro_path),
        "-i", str(recording_path),
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output_path)
    ]

    print(f"Concatenating with {crossfade_duration}s crossfade...")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg stderr: {result.stderr}", file=sys.stderr)
            raise subprocess.CalledProcessError(result.returncode, cmd)
    except subprocess.CalledProcessError as e:
        print(f"Error concatenating: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Assemble final video with intro, 2x speed recording, and timer overlay",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Process recording only (2x speed with timer)
    ./assemble-video.py -r screen.mp4 -o output.mp4

    # Full assembly with intro
    ./assemble-video.py -i intro.mp4 -r screen.mp4 -o final.mp4

    # Custom speed and no interpolation (faster processing)
    ./assemble-video.py -r screen.mp4 -o output.mp4 --speed 3 --no-interpolation
"""
    )

    parser.add_argument("--intro", "-i", type=Path,
                        help="Intro video file (optional)")
    parser.add_argument("--recording", "-r", type=Path, required=True,
                        help="Screen recording to process")
    parser.add_argument("--output", "-o", type=Path, required=True,
                        help="Output video file")
    parser.add_argument("--speed", type=float, default=2.0,
                        help="Speed multiplier for recording (default: 2.0)")
    parser.add_argument("--fps", type=int, default=60,
                        help="Output frame rate (default: 60)")
    parser.add_argument("--crossfade", type=float, default=1.0,
                        help="Crossfade duration between intro and recording (default: 1.0s)")
    parser.add_argument("--no-timer", action="store_true",
                        help="Skip timer overlay")
    parser.add_argument("--no-interpolation", action="store_true",
                        help="Skip frame interpolation (faster, less smooth)")
    parser.add_argument("--keep-temp", action="store_true",
                        help="Keep temporary files")

    args = parser.parse_args()

    # Validate inputs
    if not args.recording.exists():
        print(f"Error: Recording not found: {args.recording}", file=sys.stderr)
        sys.exit(1)

    if args.intro and not args.intro.exists():
        print(f"Error: Intro not found: {args.intro}", file=sys.stderr)
        sys.exit(1)

    # Get recording info
    print(f"\nAnalyzing: {args.recording}")
    rec_info = get_video_info(args.recording)
    print(f"  Resolution: {rec_info['width']}x{rec_info['height']}")
    print(f"  Duration: {rec_info['duration']:.2f}s")
    print(f"  Original FPS: {rec_info['fps']:.2f}")

    sped_up_duration = rec_info["duration"] / args.speed
    print("\nOutput will be:")
    print(f"  Duration: {sped_up_duration:.2f}s (at {args.speed}x speed)")
    print(f"  FPS: {args.fps}")

    # Create temp directory
    temp_dir = Path(tempfile.mkdtemp(prefix="video_assembly_"))
    print(f"\nWorking directory: {temp_dir}")

    try:
        # Step 1: Speed up recording with timer
        print("\n[Step 1] Processing screen recording...")
        sped_up_path = temp_dir / "sped_up.mp4"
        speed_up_with_timer(
            args.recording,
            sped_up_path,
            speed_factor=args.speed,
            output_fps=args.fps,
            use_interpolation=not args.no_interpolation,
            add_timer=not args.no_timer,
            video_info=rec_info
        )

        # Step 2: Concatenate with intro (if provided)
        if args.intro:
            print("\n[Step 2] Concatenating with intro...")
            concatenate_with_crossfade(
                args.intro,
                sped_up_path,
                args.output,
                crossfade_duration=args.crossfade
            )
        else:
            print("\n[Step 2] No intro provided, copying output...")
            shutil.copy2(sped_up_path, args.output)

        # Done!
        print(f"\n{'='*50}")
        print(f"Final video created: {args.output}")

        final_info = get_video_info(args.output)
        print(f"  Resolution: {final_info['width']}x{final_info['height']}")
        print(f"  Duration: {final_info['duration']:.2f}s")
        print(f"  FPS: {final_info['fps']:.2f}")

        file_size = args.output.stat().st_size / (1024 * 1024)
        print(f"  Size: {file_size:.1f} MB")

    finally:
        if not args.keep_temp:
            shutil.rmtree(temp_dir, ignore_errors=True)
            print("\nCleaned up temp files")
        else:
            print(f"\nTemp files kept at: {temp_dir}")


if __name__ == "__main__":
    main()
