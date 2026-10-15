---
name: remotion-best-practices
description: Use whenever dealing with Remotion code to obtain domain-specific knowledge.
---

# Remotion Best Practices

Use this skill whenever you are dealing with Remotion code (programmatic video with React) to obtain domain-specific knowledge.

## Rule Categories

**Composition & Structure:**
* rules/compositions.md - Defining compositions, stills, folders, default props and dynamic metadata
* rules/calculate-metadata.md - Dynamically set composition duration, dimensions, and props
* rules/parameters.md - Make a video parametrizable by adding a Zod schema

**Media Assets:**
* rules/assets.md - Importing images, videos, audio, and fonts into Remotion
* rules/images.md - Embedding images using the Img component
* rules/videos.md - Embedding videos with trimming, volume, speed, looping, pitch
* rules/audio.md - Using audio and sound - importing, trimming, volume, speed, pitch
* rules/fonts.md - Loading Google Fonts and local fonts
* rules/gifs.md - Displaying GIFs synchronized with timeline

**Animation & Timing:**
* rules/animations.md - Fundamental animation skills for Remotion
* rules/timing.md - Interpolation curves - linear, easing, spring animations
* rules/transitions.md - Scene transition patterns
* rules/trimming.md - Trimming patterns - cut beginning or end of animations
* rules/sequencing.md - Sequencing patterns - delay, trim, limit duration of items
* rules/text-animations.md - Typography and text animation patterns

**Visual & Data:**
* rules/3d.md - 3D content using Three.js and React Three Fiber
* rules/charts.md - Chart and data visualization patterns
* rules/maps.md - Add a map using Mapbox and animate it
* rules/lottie.md - Embedding Lottie animations

**Captions & Text:**
* rules/display-captions.md - Displaying captions with TikTok-style pages and word highlighting
* rules/import-srt-captions.md - Importing .srt subtitle files using @remotion/captions
* rules/transcribe-captions.md - Transcribing audio to generate captions
* rules/measuring-text.md - Measuring text dimensions, fitting text to containers, checking overflow
* rules/measuring-dom-nodes.md - Measuring DOM element dimensions

**Utilities (Mediabunny):**
* rules/can-decode.md - Check if a video can be decoded by the browser
* rules/get-video-duration.md - Getting the duration of a video file in seconds
* rules/get-audio-duration.md - Getting the duration of an audio file in seconds
* rules/get-video-dimensions.md - Getting the width and height of a video file
* rules/extract-frames.md - Extract frames from videos at specific timestamps

**Stack Integration:**
* rules/tailwind.md - Using TailwindCSS in Remotion

## How to Use

Read individual rule files for detailed explanations and code examples. Each rule provides specific patterns, best practices, and implementation guidance for its topic area.