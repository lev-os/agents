#!/usr/bin/env python3
"""Generate a 1280x640 GitHub social preview image for a repository.

Usage:
    python3 generate_og_image.py /path/to/repo
    python3 generate_og_image.py /path/to/repo --output custom_name.png
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import textwrap
from glob import glob
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 640
BORDER = 24
FONT_PATH = "/System/Library/Fonts/HelveticaNeue.ttc"


def get_repo_metadata(repo_path: str) -> dict:
    """Fetch repo description and topics via gh CLI."""
    result = subprocess.run(
        ["gh", "repo", "view", "--json", "name,description,repositoryTopics,owner"],
        capture_output=True, text=True, cwd=repo_path,
    )
    if result.returncode != 0:
        # Fallback: derive name from directory
        return {
            "name": Path(repo_path).name,
            "description": "",
            "topics": [],
            "owner": "",
        }
    data = json.loads(result.stdout)
    topics = [t["name"] for t in (data.get("repositoryTopics") or [])]
    return {
        "name": data.get("name", Path(repo_path).name),
        "description": data.get("description", "") or "",
        "topics": topics,
        "owner": data.get("owner", {}).get("login", ""),
    }


def find_hero_image(repo_path: str) -> str | None:
    """Search for a hero/illustration image in the repo."""
    search_dirs = ["", "docs", "images", "assets", "img", ".github"]
    extensions = ["*.webp", "*.png", "*.jpg", "*.jpeg"]

    # Search common directories for images
    for subdir in search_dirs:
        search_path = os.path.join(repo_path, subdir)
        if not os.path.isdir(search_path):
            continue
        for ext in extensions:
            matches = glob(os.path.join(search_path, ext))
            for match in matches:
                basename = os.path.basename(match).lower()
                # Skip tiny icons, favicons, badges
                if any(skip in basename for skip in [
                    "favicon", "icon-", "badge", "shield", "logo-small",
                    "gh_share_image", "gh_og_share_image",
                ]):
                    continue
                # Prefer images that look like hero/illustration images
                try:
                    with Image.open(match) as img:
                        w, h = img.size
                        # Skip very small images (icons/badges)
                        if w < 200 or h < 200:
                            continue
                        return match
                except Exception:
                    continue

    # Parse README for first image reference
    readme_path = find_readme(repo_path)
    if readme_path:
        try:
            with open(readme_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            # Match ![alt](path) or <img src="path">
            md_match = re.search(r'!\[.*?\]\(([^)]+)\)', content)
            if not md_match:
                md_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
            if md_match:
                img_ref = md_match.group(1)
                # Skip external URLs, badges, shields
                if not img_ref.startswith(("http://", "https://")):
                    img_path = os.path.join(repo_path, img_ref)
                    if os.path.isfile(img_path):
                        try:
                            with Image.open(img_path) as img:
                                w, h = img.size
                                if w >= 200 and h >= 200:
                                    return img_path
                        except Exception:
                            pass
        except Exception:
            pass

    return None


def find_readme(repo_path: str) -> str | None:
    """Find the README file in the repo root."""
    for name in ["README.md", "readme.md", "Readme.md", "README.rst", "README"]:
        path = os.path.join(repo_path, name)
        if os.path.isfile(path):
            return path
    return None


def name_to_colors(name: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """Generate a deterministic gradient color pair from a repo name."""
    h = hashlib.sha256(name.encode()).hexdigest()
    # Use different parts of the hash for two colors
    r1, g1, b1 = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r2, g2, b2 = int(h[6:8], 16), int(h[8:10], 16), int(h[10:12], 16)
    # Darken colors to ensure text readability (max ~60% brightness)
    factor = 0.45
    c1 = (int(r1 * factor), int(g1 * factor), int(b1 * factor))
    c2 = (int(r2 * factor), int(g2 * factor), int(b2 * factor))
    return c1, c2


def create_gradient_background(name: str) -> Image.Image:
    """Create a gradient background based on repo name hash."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    c1, c2 = name_to_colors(name)
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img


def create_hero_background(hero_path: str) -> Image.Image:
    """Resize/crop hero image to fill canvas with dark gradient overlay."""
    hero = Image.open(hero_path).convert("RGBA")

    # Resize to cover the canvas (maintain aspect ratio, crop excess)
    hero_ratio = hero.width / hero.height
    canvas_ratio = WIDTH / HEIGHT

    if hero_ratio > canvas_ratio:
        # Hero is wider — scale by height, crop width
        new_height = HEIGHT
        new_width = int(HEIGHT * hero_ratio)
    else:
        # Hero is taller — scale by width, crop height
        new_width = WIDTH
        new_height = int(WIDTH / hero_ratio)

    hero = hero.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Top-aligned crop: keep the top of the image, crop from bottom
    left = (new_width - WIDTH) // 2
    top = 0
    hero = hero.crop((left, top, left + WIDTH, top + HEIGHT))

    # Convert to RGB
    bg = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    bg.paste(hero, mask=hero.split()[3] if hero.mode == "RGBA" else None)

    # No gradient overlay — let the illustration speak for itself.
    return bg


def draw_vignette(img: Image.Image, strength: int = 60) -> None:
    """Draw a smooth gradient vignette around the edges."""
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))

    # Build a per-pixel alpha map based on distance from edges
    # For each pixel, alpha = strength * how close it is to the nearest edge
    import numpy as np

    # Create distance fields from each edge (0 at edge, 1 at vignette_radius inward)
    vignette_radius = 80  # how deep the vignette fades inward
    alpha = np.zeros((HEIGHT, WIDTH), dtype=np.float64)

    # Horizontal distance from left/right edges
    for x in range(min(vignette_radius, WIDTH // 2)):
        t = 1.0 - (x / vignette_radius)
        alpha[:, x] = np.maximum(alpha[:, x], t)
        alpha[:, WIDTH - 1 - x] = np.maximum(alpha[:, WIDTH - 1 - x], t)

    # Vertical distance from top/bottom edges
    for y in range(min(vignette_radius, HEIGHT // 2)):
        t = 1.0 - (y / vignette_radius)
        alpha[y, :] = np.maximum(alpha[y, :], t)
        alpha[HEIGHT - 1 - y, :] = np.maximum(alpha[HEIGHT - 1 - y, :], t)

    # Smooth with quadratic falloff for a natural vignette feel
    alpha = alpha ** 1.5
    alpha = (alpha * strength).clip(0, 255).astype(np.uint8)

    # Apply to overlay
    overlay_array = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    overlay_array[:, :, 3] = alpha  # black with varying alpha
    overlay = Image.fromarray(overlay_array, "RGBA")

    img_rgba = img.convert("RGBA")
    composited = Image.alpha_composite(img_rgba, overlay)
    img.paste(composited.convert("RGB"))


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Load Helvetica Neue at the given size. Index 0 = regular, 1 = bold."""
    try:
        index = 1 if bold else 0
        return ImageFont.truetype(FONT_PATH, size, index=index)
    except Exception:
        # Fallback to default
        return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = font.getbbox(test)
        if bbox[2] <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def draw_text_centered(
    draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
    y: int, max_width: int, fill: str = "white", shadow: bool = True,
) -> int:
    """Draw centered, word-wrapped text with drop shadow. Returns Y after last line."""
    lines = wrap_text(text, font, max_width)
    for line in lines:
        bbox = font.getbbox(line)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        x = (WIDTH - line_width) // 2
        if shadow:
            # Draw shadow for readability
            for dx, dy in [(2, 2), (1, 1), (2, 1), (1, 2)]:
                draw.text((x + dx, y + dy), line, font=font, fill=(0, 0, 0))
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height + 8
    return y


def draw_topic_badges(
    draw: ImageDraw.Draw, img: Image.Image, topics: list[str],
    y: int, font: ImageFont.FreeTypeFont,
) -> None:
    """Draw pill-shaped topic badges centered at y."""
    if not topics:
        return

    badge_padding_x = 18
    badge_padding_y = 8
    badge_gap = 12
    badge_height = 36

    # Calculate total width to center the row
    badge_widths = []
    for topic in topics:
        bbox = font.getbbox(topic)
        w = bbox[2] - bbox[0] + badge_padding_x * 2
        badge_widths.append(w)

    total_width = sum(badge_widths) + badge_gap * (len(badge_widths) - 1)

    # If too wide, truncate topics
    while total_width > WIDTH - BORDER * 2 - 40 and len(badge_widths) > 1:
        badge_widths.pop()
        topics = topics[:-1]
        total_width = sum(badge_widths) + badge_gap * (len(badge_widths) - 1)

    x = (WIDTH - total_width) // 2

    # Draw each badge — solid dark background, bright white text
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    for i, topic in enumerate(topics):
        bw = badge_widths[i]
        radius = badge_height // 2
        overlay_draw.rounded_rectangle(
            [(x, y), (x + bw, y + badge_height)],
            radius=radius,
            fill=(0, 0, 0, 180),
            outline=(255, 255, 255, 200),
            width=2,
        )
        bbox = font.getbbox(topic)
        tw = bbox[2] - bbox[0]
        tx = x + (bw - tw) // 2
        ty = y + badge_padding_y
        overlay_draw.text((tx, ty), topic, font=font, fill=(255, 255, 255, 255))
        x += bw + badge_gap

    # Composite overlay onto image
    img_rgba = img.convert("RGBA")
    composited = Image.alpha_composite(img_rgba, overlay)
    img.paste(composited.convert("RGB"))


def generate(repo_path: str, output_path: str | None = None) -> str:
    """Generate the social preview image. Returns the output file path."""
    repo_path = os.path.abspath(repo_path)

    if not os.path.isdir(repo_path):
        print(f"Error: {repo_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Get metadata
    meta = get_repo_metadata(repo_path)
    repo_name = meta["name"]
    description = meta["description"]
    topics = meta["topics"]

    print(f"Generating social preview for: {repo_name}")
    if description:
        print(f"  Description: {description[:80]}...")
    print(f"  Topics: {', '.join(topics) if topics else '(none)'}")

    # Find hero image
    hero_path = find_hero_image(repo_path)
    if hero_path:
        print(f"  Hero image: {hero_path}")
        img = create_hero_background(hero_path)
    else:
        print("  No hero image found, using gradient background")
        img = create_gradient_background(repo_name)

    # Draw border
    draw_vignette(img)

    # Load fonts
    font_name = load_font(48, bold=True)
    font_desc = load_font(32)
    font_tag = load_font(22)
    font_owner = load_font(24)

    draw = ImageDraw.Draw(img)

    # Layout: ALL text lives in the bottom portion so the hero image is visible.
    # For hero images: text in bottom 40%. For gradient-only: text centered.
    text_max_width = WIDTH - BORDER * 2 - 80

    if hero_path:
        # Hero mode: the illustration already contains the project name and
        # description. No text overlay at all — let the art stand alone.
        pass
    else:
        # Gradient-only mode: center text vertically (no hero to speak for us)
        content_top = BORDER + 80
        y_cursor = content_top

        display_name = repo_name.replace("-", " ").replace("_", " ")
        y_cursor = draw_text_centered(draw, display_name, font_name, y_cursor, text_max_width)
        y_cursor += 20

        if description:
            if len(description) > 200:
                description = description[:197] + "..."
            y_cursor = draw_text_centered(
                draw, description, font_desc, y_cursor, text_max_width,
                fill=(230, 230, 230),
            )

        if topics:
            tag_y = HEIGHT - BORDER - 48
            draw_topic_badges(draw, img, topics[:8], tag_y, font_tag)

    # Save
    if output_path is None:
        output_path = os.path.join(repo_path, "gh_og_share_image.png")

    # GitHub limit is 1MB for social preview images.
    TARGET_SIZE = 1_000_000

    # Try optimized PNG first
    img.save(output_path, "PNG", optimize=True, compress_level=9)
    size = os.path.getsize(output_path)

    if size > TARGET_SIZE:
        # Save as high-quality JPEG — visually near-lossless, much smaller
        quality = 95
        while quality >= 75:
            img.save(output_path, "JPEG", quality=quality, optimize=True)
            size = os.path.getsize(output_path)
            if size <= TARGET_SIZE:
                break
            quality -= 5

    size_kb = size / 1024
    print(f"  Saved: {output_path} ({size_kb:.0f}KB)")
    print(f"  Dimensions: {WIDTH}x{HEIGHT}")
    return output_path


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate GitHub social preview image")
    parser.add_argument("repo_path", help="Path to the repository")
    parser.add_argument("--output", "-o", help="Output file path (default: repo_root/gh_share_image.png)")
    args = parser.parse_args()

    generate(args.repo_path, args.output)


if __name__ == "__main__":
    main()
