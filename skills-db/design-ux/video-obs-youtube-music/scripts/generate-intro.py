#!/usr/bin/env python3
"""
Generate intro video for screen recordings.

Creates a stunning intro with:
- Animated smeared_life WebGL background
- Three.js 3D particle effects
- Animated text overlays with title, description, author info
- Smooth fade in/out transitions

Usage:
    ./generate-intro.py --title "My Video" --description "What this video is about" --output intro.mp4
"""

import argparse
import html
import random
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def escape_js_template(s: str) -> str:
    """Escape a string for safe use inside JavaScript template literals.

    Handles: backslashes, backticks, and ${} interpolation sequences.
    Should be applied AFTER html.escape() for strings going into HTML.
    """
    # Order matters: escape backslashes first
    s = s.replace('\\', '\\\\')
    s = s.replace('`', '\\`')
    s = re.sub(r'\$\{', r'\\${', s)
    return s


# Effect types available (new bright effects: fire, electric, ocean)
EFFECT_TYPES = ['cosmic', 'plasma', 'aurora', 'neon', 'nebula', 'fire', 'electric', 'ocean']

# Bright effects recommended for better visibility
BRIGHT_EFFECTS = ['fire', 'electric', 'neon', 'plasma']

# Default author info
DEFAULT_NAME = "Jeffrey Emanuel"
DEFAULT_TWITTER = "@doodlestein"
DEFAULT_GITHUB = "Dicklesworthstone"

# Duration constants
MIN_DURATION = 6.0   # Minimum intro duration in seconds
MAX_DURATION = 15.0  # Maximum intro duration in seconds
BASE_DURATION = 8.0  # Base duration for short descriptions


def calculate_dynamic_duration(description: str, title: str) -> float:
    """
    Calculate appropriate intro duration based on text length.

    Longer descriptions need more time to be read/appreciated.
    Returns duration in seconds (6-15 second range).
    """
    # Count total text that viewer needs to process
    total_chars = len(title) + len(description)

    # Estimate words (rough: 5 chars per word average)
    word_count = total_chars / 5

    # Reading speed: ~3 words per second for on-screen text
    # But we also want the visual effect to shine
    read_time = word_count / 3.0

    # Add base time for visual appreciation
    duration = max(BASE_DURATION, read_time + 4.0)

    # Clamp to valid range
    return min(MAX_DURATION, max(MIN_DURATION, duration))


def generate_html(
    title: str,
    description: str,
    name: str = DEFAULT_NAME,
    twitter: str = DEFAULT_TWITTER,
    github: str = DEFAULT_GITHUB,
    date: Optional[str] = None,
    width: int = 1920,
    height: int = 1080,
    duration_ms: int = 5000,
    fps: int = 60,
    effect_type: str = 'cosmic',
    output_path: Path = None
) -> Path:
    """Generate intro HTML file from template."""

    script_dir = Path(__file__).parent
    template_path = script_dir / "intro-template.html"

    if not template_path.exists():
        print(f"Error: Template not found at {template_path}", file=sys.stderr)
        sys.exit(1)

    template = template_path.read_text()

    # Use current date if not provided
    if date is None:
        date = datetime.now().strftime("%B %d, %Y")

    # Escape for HTML safety, then for JS template literal safety
    # (the template uses JS template literals with backticks)
    safe_title = escape_js_template(html.escape(title))
    safe_description = escape_js_template(html.escape(description))
    safe_name = escape_js_template(html.escape(name))
    safe_twitter = escape_js_template(html.escape(twitter))
    safe_github = escape_js_template(html.escape(github))
    safe_date = escape_js_template(html.escape(date))

    # Replace placeholders
    html_content = template.replace("{{TITLE}}", safe_title)
    html_content = html_content.replace("{{DESCRIPTION}}", safe_description)
    html_content = html_content.replace("{{NAME}}", safe_name)
    html_content = html_content.replace("{{TWITTER}}", safe_twitter)
    html_content = html_content.replace("{{GITHUB}}", safe_github)
    html_content = html_content.replace("{{DATE}}", safe_date)
    html_content = html_content.replace("{{WIDTH}}", str(width))
    html_content = html_content.replace("{{HEIGHT}}", str(height))
    html_content = html_content.replace("{{DURATION}}", str(duration_ms))
    html_content = html_content.replace("{{FPS}}", str(fps))
    html_content = html_content.replace("{{EFFECT_TYPE}}", effect_type)

    # Write to output path
    if output_path is None:
        output_path = script_dir / "intro-generated.html"

    output_path.write_text(html_content)
    return output_path


def record_intro(
    html_path: Path,
    output_path: Path,
    fps: int = 60,
    width: int = 1920,
    height: int = 1080
) -> None:
    """Record the intro HTML to video using the recording script."""

    script_dir = Path(__file__).parent
    record_script = script_dir / "record-intro.js"

    if not record_script.exists():
        print(f"Error: Recording script not found at {record_script}", file=sys.stderr)
        sys.exit(1)

    cmd = [
        "node", str(record_script),
        str(html_path.absolute()),
        str(output_path.absolute()),
        str(fps),
        str(width),
        str(height)
    ]

    print("Recording intro video...")
    print(f"Command: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error recording intro: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate intro video for screen recordings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Effect types available: {', '.join(EFFECT_TYPES)}

Examples:
    # Basic usage
    ./generate-intro.py --title "Building a CLI Tool" --output intro.mp4

    # With description and custom effect
    ./generate-intro.py --title "React Tutorial" \\
        --description "Learn hooks and state management" \\
        --effect plasma --output intro.mp4

    # Full customization
    ./generate-intro.py --title "My Project" \\
        --description "A deep dive into the architecture" \\
        --name "John Doe" --twitter "@johndoe" --github "johndoe" \\
        --duration 6 --width 3840 --height 2160 --effect aurora \\
        --output intro.mp4
"""
    )

    parser.add_argument("--title", "-t", required=True, help="Video title")
    parser.add_argument("--description", "-d", default="", help="Video description")
    parser.add_argument("--name", default=DEFAULT_NAME, help=f"Author name (default: {DEFAULT_NAME})")
    parser.add_argument("--twitter", default=DEFAULT_TWITTER, help=f"Twitter/X handle (default: {DEFAULT_TWITTER})")
    parser.add_argument("--github", default=DEFAULT_GITHUB, help=f"GitHub username (default: {DEFAULT_GITHUB})")
    parser.add_argument("--date", help="Date to display (default: today)")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Output video file path")
    parser.add_argument("--width", type=int, default=1920, help="Video width (default: 1920)")
    parser.add_argument("--height", type=int, default=1080, help="Video height (default: 1080)")
    parser.add_argument("--duration", type=float, default=None,
                        help="Duration in seconds (default: auto-calculated 6-15s based on text)")
    parser.add_argument("--fps", type=int, default=60, help="Frames per second (default: 60)")
    parser.add_argument("--effect", choices=EFFECT_TYPES, default=None,
                        help="Background effect type (default: random bright effect)")
    parser.add_argument("--random-effect", action="store_true",
                        help="Choose a random effect (any type)")
    parser.add_argument("--html-only", action="store_true",
                        help="Only generate HTML, don't record video")
    parser.add_argument("--keep-html", action="store_true",
                        help="Keep the generated HTML file after recording")

    args = parser.parse_args()

    # Choose effect: specified > random > random bright effect (default)
    if args.effect:
        effect_type = args.effect
    elif args.random_effect:
        effect_type = random.choice(EFFECT_TYPES)
        print(f"Selected random effect: {effect_type}")
    else:
        # Default: choose from bright effects for better visibility
        effect_type = random.choice(BRIGHT_EFFECTS)
        print(f"Selected bright effect: {effect_type}")

    # Calculate duration: specified > auto-calculated
    if args.duration is not None:
        duration = args.duration
    else:
        duration = calculate_dynamic_duration(args.description, args.title)
        print(f"Auto-calculated duration: {duration:.1f}s (based on text length)")

    duration_ms = int(duration * 1000)

    print("Generating intro video:")
    print(f"  Title: {args.title}")
    print(f"  Description: {args.description or '(none)'}")
    print(f"  Author: {args.name}")
    print(f"  Twitter: {args.twitter}")
    print(f"  GitHub: {args.github}")
    print(f"  Resolution: {args.width}x{args.height}")
    print(f"  Duration: {duration:.1f}s @ {args.fps}fps")
    print(f"  Effect: {effect_type}")
    print()

    # Generate HTML
    script_dir = Path(__file__).parent
    html_path = script_dir / f"intro-{args.output.stem}.html"

    html_path = generate_html(
        title=args.title,
        description=args.description,
        name=args.name,
        twitter=args.twitter,
        github=args.github,
        date=args.date,
        width=args.width,
        height=args.height,
        duration_ms=duration_ms,
        fps=args.fps,
        effect_type=effect_type,
        output_path=html_path
    )

    print(f"Generated HTML: {html_path}")

    if args.html_only:
        print("HTML-only mode, skipping video recording")
        return

    # Record video
    record_intro(
        html_path=html_path,
        output_path=args.output,
        fps=args.fps,
        width=args.width,
        height=args.height
    )

    # Cleanup HTML unless keeping
    if not args.keep_html:
        html_path.unlink()
        print(f"Cleaned up: {html_path}")

    print(f"\nIntro video created: {args.output}")


if __name__ == "__main__":
    main()
