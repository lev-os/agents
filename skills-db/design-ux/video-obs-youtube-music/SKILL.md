---
name: video-obs-youtube-music
description: >-
  Remux OBS recordings to MP4, add YouTube music, generate intro/outro videos with WebGL shaders, and song credit overlays. Use when preparing screen recordings for YouTube or X/Twitter upload.
---

# video-obs-youtube-music — OBS YouTube Music

Remux OBS MKV → MP4, add stunning intro/outro videos with WebGL shaders (FloquetTopoCA, smeared_life, SpinGlassCA), replace audio with YouTube music, and overlay animated song credits.

## Quick Start

```bash
# Basic: remux with single song
ffmpeg -i "recording.mkv" -i "song.mp3" \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k \
  -movflags +faststart "output.mp4"
```

## Workflow

- [ ] Get video path, title, description, and song names from user
- [ ] Probe video duration: `ffprobe -v error -show_entries format=duration -of csv=p=0 "file"`
- [ ] Download songs: `yt-dlp -x --audio-format mp3 "ytsearch1:Song Name"`
- [ ] Check total music duration covers video
- [ ] **Optional**: Generate intro/outro videos with WebGL shaders (see below)
- [ ] **Optional**: Generate animated song credit cards (see below)
- [ ] **Optional**: Use remote machines for parallel rendering (see below)
- [ ] Concatenate intro + recording + outro, add audio and overlays
- [ ] Audio should start at intro (t=0), not when screen recording starts
- [ ] **Encode platform-specific versions** (see Platform Export section)

## Platform Export Requirements

### YouTube (Maximum Quality)
- Resolution: Up to 8K
- Frame rate: Up to 60fps
- Codec: H.264 or HEVC
- No special requirements beyond `-movflags +faststart`

### X/Twitter (CRITICAL - Different Limits!)

| Spec | Limit |
|------|-------|
| **Resolution** | Max 1920x1200 (NOT 4K!) |
| **Frame rate** | Up to 60fps |
| **Bitrate** | Max 25 Mbps |
| **Duration** | 2:20 regular, 4 hours Premium |
| **File size** | 512MB regular, 16GB Premium |
| **Codec** | H.264 + AAC only |

**X-Compatible Encoding Command:**
```bash
ffmpeg -i source_4k.mp4 \
  -vf "scale=1920:1080:flags=lanczos" \
  -c:v libx264 -preset medium -crf 18 \
  -profile:v high -level:v 4.2 -pix_fmt yuv420p \
  -b:v 20M -maxrate 25M -bufsize 25M \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  output_for_x.mp4
```

### QuickTime Compatibility
- HEVC may not play - always provide H.264 version
- Use standard resolutions (3840x2160, 1920x1080)
- Avoid non-standard aspect ratios like 4096x2304

## Intro Video

Generate stunning 5-second intro videos with:
- **WebGL Background**: Animated cellular automata (cosmic, plasma, aurora, neon, nebula effects)
- **3D Particle Effects**: Three.js floating particles with additive blending
- **Animated Text**: Title, description, author info with smooth fade transitions
- **Professional Layout**: Date in corner, social handles at bottom

### Generate Intro

```bash
# Basic intro
./scripts/generate-intro.py \
  --title "Building a CLI Tool in Rust" \
  --output intro.mp4

# Full customization
./scripts/generate-intro.py \
  --title "React Performance Deep Dive" \
  --description "Optimizing renders and reducing bundle size" \
  --effect plasma \
  --duration 5 \
  --width 1920 --height 1080 \
  --output intro.mp4
```

### Effect Types

| Effect | Description |
|--------|-------------|
| `cosmic` | Default - deep purples and blues, organic flow |
| `plasma` | Warm oranges and reds, energetic movement |
| `aurora` | Greens and cyans, smooth northern lights feel |
| `neon` | High contrast pinks and cyans, electric vibe |
| `nebula` | Rich colors with energy glow, space-like |

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--title` | required | Video title (large, centered) |
| `--description` | "" | Subtitle text |
| `--name` | Jeffrey Emanuel | Author name |
| `--twitter` | @doodlestein | X/Twitter handle |
| `--github` | Dicklesworthstone | GitHub username |
| `--date` | today | Date displayed |
| `--effect` | cosmic | Background effect type |
| `--random-effect` | false | Choose random effect |
| `--duration` | 5 | Duration in seconds |
| `--width` | 1920 | Video width |
| `--height` | 1080 | Video height |
| `--fps` | 60 | Frames per second |

### Prepend Intro to Recording

```bash
# Concatenate intro + recording (same resolution/codec)
ffmpeg -i intro.mp4 -i recording.mp4 \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v]" \
  -map "[v]" \
  -c:v libx264 -preset fast -crf 18 \
  "with_intro.mp4"

# With audio from songs
ffmpeg -i intro.mp4 -i recording.mp4 -i song.mp3 \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v]" \
  -map "[v]" -map 2:a \
  -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k \
  -shortest \
  "final.mp4"
```

## Song Credit Cards

Animated "now playing" cards with polished visual effects:
- **Scale animation**: Cards grow from 85% with overshoot bounce on entry/exit
- **Floating motion**: Subtle up/down floating while displayed
- **Pulsing music icon**: Rhythmic scale animation on the music note
- **Shimmer highlight**: Animated gradient sweep across top edge
- **Glow pulse**: Subtle ambient glow that pulses
- **Custom branding**: "Doodlestein's Choice" text with Pacifico font

### Card Dimensions

| Use Case | Width | Height | Notes |
|----------|-------|--------|-------|
| Standard | 2280px | 480px | Full-width overlay |
| Narrow (transparent) | 1900px | 480px | Avoids white rectangle artifacts |
| 4K compatible | 1900px | 480px | Scales well at any resolution |

**Important**: Use narrower cards (1900px) to avoid visible white rectangles on sides.

### Generate Cards with Playwright

```javascript
// render_cards.js - Render card animation to PNG frames
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

async function renderCard(cardNum) {
  const cardPath = "./cards/0" + cardNum + "_card.html";
  const outDir = "./cards/frames_0" + cardNum;

  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.setViewportSize({ width: 1900, height: 480 });
  await page.goto("file://" + path.resolve(cardPath));
  await page.waitForTimeout(500);

  const FPS = 60, DURATION = 6, TOTAL = FPS * DURATION;

  for (let f = 0; f < TOTAL; f++) {
    const framePath = path.join(outDir, "frame_" + String(f).padStart(4, "0") + ".png");
    await page.screenshot({ path: framePath, omitBackground: true }); // Alpha!
    await page.evaluate(() => window.stepFrame());
  }

  await browser.close();
}

renderCard(process.argv[2] || "1");
```

### Encode Cards with Alpha (WebM VP9)

```bash
# Encode PNG frames to WebM with transparency
ffmpeg -framerate 60 -i "frames/frame_%04d.png" \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 2M \
  card.webm
```

### Card Overlay FFmpeg

Position cards in **upper-right corner** (not bottom-right) for better visibility:

```bash
# Single song with animated card (6s video, card at t=10s after intro)
ffmpeg -i "video.mp4" -i "song.mp3" -i "card.webm" \
  -filter_complex \
    "[0:v][2:v]overlay=x=W-w-50:y=50:enable='between(t,10,16)'[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k \
  -movflags +faststart "output.mp4"

# With intro + multiple songs (audio starts at intro)
ffmpeg -i intro.mp4 -i recording.mp4 -i outro.mp4 -i songs.m4a \
  -i card1.webm -i card2.webm \
  -filter_complex "
    [0:v][1:v][2:v]concat=n=3:v=1:a=0[base];
    [4:v]setpts=PTS+10/TB[c1];
    [5:v]setpts=PTS+205/TB[c2];
    [base][c1]overlay=x=W-w-50:y=50:enable='between(t,10,16)'[tmp1];
    [tmp1][c2]overlay=x=W-w-50:y=50:enable='between(t,205,211)'[vout]
  " \
  -map "[vout]" -map 3:a \
  -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k \
  final.mp4
```

### Card Timing Formula

| Song | Card Appears | Card Duration | Animation |
|------|--------------|---------------|-----------|
| 1 | 0s | 6s | Baked into video |
| 2 | song1_duration | 6s | Baked into video |
| 3 | song1 + song2 duration | 6s | Baked into video |

Overlay pattern: `enable='between(t,{start},{start+6})':eof_action=pass`

## Multi-Song (No Cards)

```bash
# Concat audio, copy video
ffmpeg -i "video.mkv" -i "s1.mp3" -i "s2.mp3" \
  -filter_complex "[1:a][2:a]concat=n=2:v=0:a=1[music]" \
  -map 0:v -map "[music]" \
  -c:v copy -c:a aac -b:a 192k \
  -movflags +faststart "output.mp4"
```

## Core Commands

| Task | Command |
|------|---------|
| Duration | `ffprobe -v error -show_entries format=duration -of csv=p=0 "file"` |
| Download song | `yt-dlp -x --audio-format mp3 "ytsearch1:Artist Song"` |
| Get metadata | `yt-dlp --print-json --no-download "ytsearch1:query"` |
| Download thumbnail | `yt-dlp --write-thumbnail --convert-thumbnails jpg "URL"` |

## Dependencies

- `ffmpeg` + `ffprobe`
- `yt-dlp`
- `node` + `playwright` npm package (for intro and card video recording)

Install dependencies:
```bash
cd /path/to/video-obs-youtube-music
npm install playwright
npx playwright install chromium
```

Check: `./scripts/check-deps.sh`

## Remote Machine Parallel Rendering

For complex projects with long intro/outro sequences, distribute rendering across multiple machines.

### Available Machines

| Host | CPU | GPU | Best For |
|------|-----|-----|----------|
| `trj` | High core | Dual 4090 | NVENC encoding |
| `jain` | High core | None | CPU encoding, fast |
| `csd` | Medium | None | Frame rendering |
| `css` | Medium | None | Frame rendering |
| `fmd` | Medium | None | Frame rendering |

### Setup Remote Machines

```bash
# Each machine needs: node, playwright, chromium
ssh machine "npm install playwright && npx playwright install chromium"

# Copy HTML files to remote
scp intro.html machine:/tmp/
scp render_script.js machine:/tmp/
```

### Robust Render Script (with timeouts)

```javascript
// render-frames.js - Distributed rendering with retries
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const START_FRAME = parseInt(process.argv[2]) || 0;
const END_FRAME = parseInt(process.argv[3]) || 100;
const HTML_FILE = process.argv[4] || '/tmp/intro.html';
const OUTPUT_DIR = process.argv[5] || '/tmp/frames';
const WIDTH = parseInt(process.argv[6]) || 1920;
const HEIGHT = parseInt(process.argv[7]) || 1080;

async function render() {
  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const browser = await chromium.launch({
    headless: true,
    timeout: 120000  // 2 minute browser launch timeout
  });

  const page = await browser.newPage();
  page.setDefaultTimeout(60000);  // 60s for page operations

  await page.setViewportSize({ width: WIDTH, height: HEIGHT });
  await page.goto('file://' + path.resolve(HTML_FILE), { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // Jump to start frame
  for (let i = 0; i < START_FRAME; i++) {
    await page.evaluate(() => window.stepFrame && window.stepFrame());
  }

  console.log(`Rendering frames ${START_FRAME} to ${END_FRAME}...`);
  const startTime = Date.now();

  for (let f = START_FRAME; f < END_FRAME; f++) {
    const framePath = path.join(OUTPUT_DIR, `frame_${String(f).padStart(5, '0')}.png`);

    // Retry logic for flaky screenshots
    for (let retry = 0; retry < 3; retry++) {
      try {
        await page.screenshot({ path: framePath });
        break;
      } catch (e) {
        if (retry === 2) throw e;
        await page.waitForTimeout(500);
      }
    }

    await page.evaluate(() => window.stepFrame && window.stepFrame());

    if ((f - START_FRAME) % 100 === 0) {
      const elapsed = (Date.now() - startTime) / 1000;
      const fps = (f - START_FRAME) / elapsed;
      console.log(`Frame ${f}/${END_FRAME} (${fps.toFixed(1)} fps)`);
    }
  }

  await browser.close();
  console.log(`Done! Rendered ${END_FRAME - START_FRAME} frames.`);
}

render().catch(e => { console.error(e); process.exit(1); });
```

### Parallel Frame Rendering

Split frame ranges across machines and render in parallel:

```bash
# Calculate total frames: duration_seconds * fps
TOTAL_FRAMES=5430  # 90.5 seconds at 60fps

# Distribute across 5 machines
ssh css "node /tmp/render.js 0 1086 /tmp/intro.html /tmp/frames" &
ssh csd "node /tmp/render.js 1086 2172 /tmp/intro.html /tmp/frames" &
ssh jain "node /tmp/render.js 2172 3258 /tmp/intro.html /tmp/frames" &
ssh fmd "node /tmp/render.js 3258 4344 /tmp/intro.html /tmp/frames" &
ssh trj "node /tmp/render.js 4344 5430 /tmp/intro.html /tmp/frames" &

wait  # Wait for all to complete
```

### Reallocating Slow Machines

If a machine is too slow, stop it and redistribute:

```bash
# Check progress
ssh slow_machine 'ls /tmp/frames/*.png | wc -l'

# Stop slow machine at frame N, redistribute to faster machines
ssh slow_machine 'pkill -f node'

# Give remaining frames to faster machines
ssh fast1 "node /tmp/render.js $STOPPED_AT $MIDPOINT /tmp/intro.html /tmp/frames" &
ssh fast2 "node /tmp/render.js $MIDPOINT $END /tmp/intro.html /tmp/frames" &
```

### Collect and Assemble Frames

```bash
# Download frames from each machine
rsync -avz css:/tmp/frames/ ./frames/
rsync -avz csd:/tmp/frames/ ./frames/
rsync -avz jain:/tmp/frames/ ./frames/
rsync -avz fmd:/tmp/frames/ ./frames/
rsync -avz trj:/tmp/frames/ ./frames/

# Verify frame count
ls frames/*.png | wc -l  # Should match TOTAL_FRAMES

# Assemble into video
ffmpeg -framerate 60 -i "frames/frame_%05d.png" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 \
  output.mp4
```

### GPU-Accelerated Encoding on Remote

For machines with NVIDIA GPUs (e.g., dual 4090s), use NVENC:

```bash
# HEVC for 4K - fast encoding
ssh trj 'ffmpeg -i input.mp4 -c:v hevc_nvenc -preset p4 -b:v 20M output.mp4'

# H.264 for max compatibility
ssh trj 'ffmpeg -i input.mp4 \
  -c:v h264_nvenc -preset p4 -profile:v high -b:v 20M output.mp4'
```

### Frame Rate Matching

**Critical**: When concatenating videos, all inputs must have the same frame rate:

```bash
# Convert 30fps source to 60fps before concat
ffmpeg -i source_30fps.mkv -r 60 -c:v libx264 -crf 18 source_60fps.mp4

# Now concat with 60fps intro/outro
ffmpeg -i intro_60fps.mp4 -i source_60fps.mp4 -i outro_60fps.mp4 \
  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]" \
  -map "[v]" output.mp4
```

## 4K Video Production

### Resolution Considerations

| Resolution | H.264 Support | HEVC Support | QuickTime | X/Twitter |
|------------|---------------|--------------|-----------|-----------|
| 1920x1080 | Yes | Yes | Yes | Yes |
| 3840x2160 | Yes (level 5.2) | Yes | Yes | **NO** |
| 4096x2304 | No (exceeds level) | Yes | Maybe | **NO** |

### Recommended 4K Workflow

```bash
# 1. Render intro/outro at desired resolution and 60fps
# 2. Convert source to 60fps (matching)
ffmpeg -i source.mkv -r 60 -c:v libx264 -crf 18 source_60fps.mp4

# 3. Assemble master at full resolution
ffmpeg -i intro.mp4 -i source_60fps.mp4 -i outro.mp4 -i audio.m4a \
  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]" \
  -map "[v]" -map 3:a \
  -c:v libx264 -crf 18 -c:a aac -b:a 192k \
  master.mp4

# 4. Export platform-specific versions
# YouTube (keep 4K):
cp master.mp4 youtube_4k.mp4

# X/Twitter (MUST downscale to 1080p):
ffmpeg -i master.mp4 \
  -vf "scale=1920:1080:flags=lanczos" \
  -c:v libx264 -preset medium -crf 18 \
  -profile:v high -level:v 4.2 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  x_twitter_1080p60.mp4
```

## Gotchas

### Encoding
- `ytsearch1:` returns first result — include artist name for accuracy
- Cards/intros require video re-encode (`-c:v libx264`), basic remux can use `-c:v copy`
- `-movflags +faststart` required for YouTube/X streaming
- **Frame rate mismatch**: Concat of different fps causes bitrate/quality issues - convert first!
- **H.264 level limits**: 4096x2304 exceeds level 5.2, use HEVC or scale to 3840x2160

### Platform Compatibility
- **X/Twitter rejects 4K** - Always encode 1080p version for X, even if video plays in preview
- **QuickTime HEVC**: May not play - provide H.264 version for compatibility
- **X Premium** allows 4 hour videos, but still max 1920x1200 resolution

### Card Overlays
- Card overlay position: `x=W-w-50:y=50` = upper-right corner (50px margins)
- Card videos are 6 seconds with animation baked in (no ffmpeg fade needed)
- WebM format supports transparency for clean overlay compositing
- **Card transparency**: Use narrower cards (1900px) to avoid white rectangle artifacts

### Audio
- **Audio timing**: Start audio at intro (t=0), cards appear when screen recording starts

### Remote Rendering
- Remote machines may need SwiftShader for software WebGL rendering
- Always use timeout and retry logic in render scripts
- Monitor render speed - reallocate slow machines' work to faster ones
- Check disk space on remote machines before large frame transfers
