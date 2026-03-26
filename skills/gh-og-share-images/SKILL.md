---
name: gh-og-share-images
description: >-
  Generate GitHub social preview images (1280x640 PNG) via iterative
  vision-guided refinement. Use when: social preview, GitHub share image,
  OG image for repo, social card, gh_share_image, preview image.
---

# gh-og-share-images

Generate GitHub social preview images (1280x640 PNG) for repositories via an iterative, vision-guided refinement process. Every image requires multiple passes of generation, visual inspection, and parameter tweaking before it's ready.

## Trigger phrases
- "generate social preview", "GitHub share image", "OG image for repo", "social card"
- "gh_share_image", "preview image for this repo"

## Core principle

**This is NOT a fire-and-forget script.** Every repo's illustration has different dimensions, colors, contrast, and composition. Every description has different length. The script `generate_og_image.py` is just the starting-point generator — the real work is the iterative visual review loop. Plan for **at least 5 passes** of generate → view → tweak → regenerate per image.

## Workflow (per repo)

### Step 1: Gather context
1. `gh repo view --json name,description,repositoryTopics,owner` for metadata
2. Find the hero/illustration image. Check:
   - Root: `*illustration*`, `*hero*`, `*banner*` (webp/png/jpg)
   - `docs/`, `images/`, `assets/`, `img/`, `.github/`
   - README.md first `![](...)` reference
3. **View the hero image** with the Read tool. Understand its composition — where the subject is, aspect ratio, color palette, busy vs clean areas.

### Step 2: Generate initial draft
Run `generate_og_image.py` with the repo path. This produces a first draft at `gh_og_share_image.png` (or `--output` path).

```bash
python3 /Users/jemanuel/projects/je_private_skills_repo/.claude/skills/gh-og-share-images/generate_og_image.py /path/to/repo --output /tmp/preview.png
```

### Step 3: Visual review (MANDATORY — at least 5 passes)

**Read the output image** with the Read tool every single time. Inspect for:

- **Hero image cropping**: Is the subject cut off? Is the important part visible? The script defaults to top-aligned crop, but some images need center or custom alignment.
- **Gradient overlay**: Is it too dark/light? Does it kill the illustration or leave text unreadable?
- **Text placement**: Does text overlap the interesting part of the illustration? Is it readable against the background?
- **Text content**: Is the description too long and wrapping awkwardly? Should it be shortened?
- **Topic badges**: Are they visible? Too many? Overlapping?
- **Overall composition**: Does it look good as a small thumbnail (how it appears on social media)?
- **Color harmony**: Does the text color work with the illustration palette?

### Step 4: Tweak and regenerate

Based on visual review, modify `generate_og_image.py` parameters or the script itself. Common adjustments:

| Problem | Fix |
|---------|-----|
| Subject cut off at top/bottom | Change crop alignment (top/center/bottom) in `create_hero_background` |
| Gradient too dark, kills illustration | Reduce alpha values, raise `gradient_start` ratio |
| Gradient too light, text unreadable | Increase alpha values, lower `gradient_start` ratio |
| Text covers the good part of the image | Adjust text Y positions, move text block up or down |
| Description too long, wraps ugly | Truncate description or reduce font size |
| Too many topic badges | Limit `topics[:N]` to fewer |
| Wrong hero image selected | Pass explicit image path or adjust `find_hero_image` priority |
| Image too busy for text overlay | Add text shadow/outline, or increase gradient coverage |
| Colors clash | Adjust text fill colors to complement the illustration |

### Step 5: Repeat Steps 3-4

Keep going until the image looks genuinely good. **Do not stop at "acceptable."** This image represents the repo on every social share.

### Step 6: Save final output
Save as `gh_og_share_image.png` in the repo root. Must be under 1MB (GitHub's limit). The script handles this automatically — it tries optimized PNG first, then falls back to high-quality JPEG (95 down). **Never reduce color depth to shrink file size — always prefer higher JPEG compression over quantization.** The user will manually upload via GitHub Settings > Social preview.

## Script reference

**`generate_og_image.py`** — Pillow-based generator. Key parameters to tweak per-repo:

- Canvas: 1280x640 (GitHub's required dimensions)
- Hero crop alignment (top/center/bottom)
- Gradient overlay start position and opacity range
- Text positions (bottom-anchored for hero images, centered for gradient-only)
- Font sizes: repo name (48px bold), description (32px), tags (20px), owner (24px)
- Border width (currently 24px)

**`batch_generate.sh`** — Iterates all repos in `~/projects/`. Useful for generating initial drafts, but **every output still needs individual visual review and refinement**.

## Dependencies
- Python 3 + Pillow
- `gh` CLI (for repo metadata)
- macOS font: `/System/Library/Fonts/HelveticaNeue.ttc`
- Claude Code with image understanding (for the visual review passes)

## Upload

GitHub has no API for social preview upload. After finalizing each image:
`Settings > Social preview > Edit > Upload an image`
