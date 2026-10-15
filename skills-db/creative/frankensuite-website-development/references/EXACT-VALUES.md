# FrankenSuite Exact Implementation Values — Complete Reference

> Every magic number, every color code, every animation config, every SVG path.
> Use this when building a new FrankenSuite website to match frankentui.com exactly.

---

## FrankenBolt — Exact Implementation

### Dimensions & Styling
- Container: `h-3.5 w-3.5` (14×14px)
- Gradient: `from-slate-700 via-slate-900 to-black`
- Border: `border-white/10`
- Inner cross: two divs `h-[60%] w-[1.5px]`, one at `rotate-45`, one at `-rotate-45`, `bg-slate-800`
- Default color: `#4ade80` (green-400, NOT green-500)

### SVG Electrical Arcs
```tsx
// viewBox="0 0 20 20"
// Path 1 (vertical): "M 10,2 Q 13,5 10,10 T 10,18"
// Path 2 (horizontal): "M 2,10 Q 5,13 10,10 T 18,10"
// strokeWidth="0.75", fill="none"
// filter: drop-shadow(0 0 3px ${color})
```

### Hover Animation
```ts
controls.start({
  opacity: [0, 1, 0.5, 1, 0],
  pathLength: [0, 1],
  transition: { duration: 0.2, repeat: Infinity, repeatType: "reverse", ease: "linear" }
})
// whileHover: scale = baseScale * 1.15
```

---

## FrankenStitch — Exact SVG Paths

### Horizontal
```svg
<svg width="100%" height="12" viewBox="0 0 100 12">
  <path d="M5 6 L15 6 M10 1 L10 11 M25 6 L35 6 M30 1 L30 11 M45 6 L55 6 M50 1 L50 11 M65 6 L75 6 M70 1 L70 11 M85 6 L95 6 M90 1 L90 11"
    strokeWidth="1.5" strokeLinecap="round" />
</svg>
```
5 stitch pairs at x = 10, 30, 50, 70, 90

### Vertical
```svg
<svg width="12" height="100%" viewBox="0 0 12 100">
  <path d="M6 5 L6 15 M1 10 L11 10 M6 25 L6 35 M1 30 L11 30 M6 45 L6 55 M1 50 L11 50 M6 65 L6 75 M1 70 L11 70 M6 85 L6 95 M1 90 L11 90"
    strokeWidth="1.5" strokeLinecap="round" />
</svg>
```
5 stitch pairs at y = 10, 30, 50, 70, 90

### Animation
- Initial: `scale: 1, opacity: 0.35`
- Hover: `scale: 1.05, opacity: 0.7`
- Spring: `stiffness: 400, damping: 15`

---

## NeuralPulse — Exact Keyframes

### Horizontal Beam
- Dimensions: `h-[1.5px] w-12` (1.5px × 48px)
- Gradient: `from-transparent via-[var(--pulse-color)] to-transparent`
- Blur: `blur-[2px]`
- Drop shadow: `drop-shadow(0 0 4px var(--pulse-color))`
- Keyframes:
  ```ts
  top:     ["0%",  "0%",   "100%", "100%", "0%"]
  left:    ["0%",  "100%", "100%", "0%",   "0%"]
  opacity: [0,     1,      1,      1,      0]
  times:   [0,     0.25,   0.5,    0.75,   1]
  // duration: 4s, repeat: Infinity, ease: "linear"
  ```

### Vertical Beam (2s delay)
- Dimensions: `w-[1.5px] h-12`
- Same gradient direction rotated
- Same keyframe pattern, `delay: 2`
- Opacity: `[0, 0.8, 0.8, 0.8, 0]` (slightly dimmer than horizontal)

---

## FrankenContainer — Exact Structure

### Stitched Background Texture SVG
```
data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40'>
  <path d='M10 5 L10 15 M30 5 L30 15 M10 25 L10 35 M30 25 L30 35
           M5 10 L15 10 M25 10 L35 10 M5 30 L15 30 M25 30 L35 30'
    stroke='#ffffff' stroke-width='1' fill='none'/>
</svg>
```
Applied at: `backgroundSize: '80px 80px'`, `opacity-[0.05]`

### Stitch Visibility (hover transitions)
- Top/Bottom stitches: `opacity-20 group-hover/container:opacity-60`
- Left/Right stitches: `opacity-10 group-hover/container:opacity-40`
- NeuralPulse: `opacity-0 group-hover/container:opacity-100 transition-opacity duration-700`

### Bolt Positions
All four corners: `absolute -left-1.5 -top-1.5 z-30` (−6px offset)

---

## FrankenGlitch — Exact Implementation

### Text Shadow Effect
```ts
textShadow: `${offset}px 0 rgba(255,0,0,0.5), -${offset}px 0 rgba(0,255,255,0.5)`
```

### Offset Values by Intensity
- Low: `±2px`
- Medium: `±5px`
- High: `±10px`

### Split Slice ClipPaths
- Top slice: `clipPath: inset(0 0 70% 0)` — red text-shadow
- Bottom slice: `clipPath: inset(70% 0 0 0)` — cyan text-shadow
- Duration: `0.1s`, repeating mirror

### Random Trigger
- Check interval: every `3000ms`
- Probability: `Math.random() < 0.15` (15% chance)
- Active duration: `150 + Math.random() * 200`ms (150-350ms)

---

## FrankenEye — Exact Implementation

### Container
- Size: `h-12 w-12` (48×48px), `rounded-full`
- Border: `border-2 border-slate-900`
- Inner shadow: `inset 0 2px 4px rgba(0,0,0,0.3)`

### Sclera Gradient
```css
bg-[radial-gradient(circle_at_30%_30%, #fff 0%, #e2e8f0 100%)]
```
Highlight at upper-left (30%, 30%)

### Blood Vessel SVG Paths (viewBox 0 0 100 100)
```
Path 1: M 15 15 Q 30 35 45 45  (top-left → center)
Path 2: M 85 15 Q 70 35 55 45  (top-right → center)
Path 3: M 15 85 Q 30 65 45 55  (bottom-left → center)
Path 4: M 85 85 Q 70 65 55 55  (bottom-right → center)
```
All: `stroke="#ef4444" strokeWidth="0.8" fill="none"`
Container opacity: `opacity-30`

### Iris & Pupil
- Iris: `h-6 w-6` (24px), `bg-green-500`, `border border-green-700`
  - Inner shadow: `inset 0 0 10px rgba(0,0,0,0.3)`
  - Pattern: `repeating-conic-gradient(from 0deg, transparent 0deg 10deg, rgba(0,0,0,0.1) 10deg 20deg)` at 40% opacity
  - Spring: `stiffness: 250, damping: 20`
- Pupil: `h-3 w-3` (12px), `bg-slate-950`
  - Hover scale: `1.25`
- Shine: `h-1.5 w-1.5` (6px), `bg-white/60`, position `top-1 left-1`

### Mouse Tracking Math
```ts
const deltaX = clientX - centerX;
const deltaY = clientY - centerY;
const distance = Math.hypot(deltaX, deltaY);
const angle = Math.atan2(deltaY, deltaX);
const moveDist = Math.min(eyeWidth / 4, distance / 15);
// Caps iris at 25% of eye width, divides distance by 15 for damping
const x = Math.cos(angle) * moveDist;
const y = Math.sin(angle) * moveDist;
```

### Proximity
```ts
const proximity = Math.max(0, 1 - distance / 400);
// 0px → 1.0, 200px → 0.5, 400px → 0.0, >400px → 0.0
```

### Blink
- Interval: `2500ms`
- Probability: `Math.random() > 0.8` (20% per tick)
- Duration: `120ms`
- Eyelid animation: `scaleY: isBlinking ? 1 : 0`, `duration: 0.1, ease: "easeInOut"`
- Surface shadow (z-30): `inset 0 4px 12px rgba(0,0,0,0.4)`

---

## Custom Cursor — Exact Implementation

### Element Detection (walks DOM tree upward)
```ts
// Finds first ancestor matching each:
closestButton     // tagName === "BUTTON"
closestLink       // tagName === "A"
closestPre        // tagName === "PRE"
closestCode       // tagName === "CODE"
closestHeader     // tagName === "HEADER"
closestTechnical  // dataset.technical === "true"
closestFlashlight // dataset.flashlight === "true"
magneticElement   // dataset.magnetic === "true"
hasPointerRole    // role === "button" OR dataset.cursor === "pointer"
```

### Clickability Logic
```ts
isClickable = target.tagName === "BUTTON"
  || target.tagName === "A"
  || Boolean(closestButton)
  || Boolean(closestLink)
  || hasPointerRole
```

### Flashlight Guard
```ts
isFlashlight = Boolean(closestFlashlight) && !closestHeader
// Disabled inside <header> elements
```

### Magnetic Attraction
```ts
const centerX = rect.left + rect.width / 2;
const centerY = rect.top + rect.height / 2;
const distance = Math.hypot(clientX - centerX, clientY - centerY);
if (distance < 60) { /* activate magnetic mode */ }
```

### RAF Batching Pattern
```ts
let last: { clientX, clientY, target } | null = null;
let rafId: number | null = null;

function handleMouseMove(e) {
  last = { clientX: e.clientX, clientY: e.clientY, target: e.target };
  if (!rafId) {
    rafId = requestAnimationFrame(flush);
  }
}

function flush() {
  rafId = null;
  if (!last) return;
  // Process accumulated state in single frame
  // ...all element detection and state updates here
}
```

### PRNG for Data Debris (avoids Math.random in render)
```ts
function prng(seed: number): number {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}
```

### Data Debris Particles (5 per cursor)
```ts
// For particle index i:
char:     prng(i * 17.1) > 0.5 ? hexDigit : (prng(i * 43.7) > 0.5 ? "0" : "1")
offsetX:  (prng(i * 59.9) - 0.5) * 40    // range [-20, 20]px
offsetY:  (prng(i * 71.2) - 0.5) * 40    // range [-20, 20]px
duration: 1 + prng(i * 83.1) * 2          // range [1, 3]s
drift1:   (prng(i * 97.3) - 0.5) * 20     // range [-10, 10]px
drift2:   (prng(i * 101.9) - 0.5) * 40    // range [-20, 20]px
```

### Exact Dimensions
| Element | Dimension | Value |
|---------|-----------|-------|
| Outer ring | Size | `h-10 w-10` (40px) |
| Outer ring | Border | `border-green-500/40` → `/80` on pointer |
| Outer ring | Scale normal | 1.0 |
| Outer ring | Scale pointer | 1.4 |
| Outer ring | Scale clicking | 0.7 |
| Outer ring | Click rotation | 45deg |
| Outer ring | Click border-radius | 20% (from 50%) |
| Inner dot | Size | `h-1.5 w-1.5` (6px) |
| Inner dot | Shadow | `0 0 10px rgba(74, 222, 128, 0.8)` |
| Inner dot | Click scale | 3.0 |
| Inner dot | Click color | `bg-red-500` (from green-400) |
| Crosshair lines | Length | `8px` |
| Crosshair lines | Width | `1px` |
| Crosshair lines | Offset | `15px` from center |
| Crosshair lines | Color | `bg-green-500/60` |
| Crosshair lines | Entry rotation | `-45deg` → `0deg` |
| Crosshair lines | Exit rotation | `0deg` → `45deg` |
| Click glitch ring | Inset | `-10px` (outside ring) |
| Click glitch ring | Border | `border-red-500/50` |
| Click glitch ring | Scale | 0.5 → 1.5 |
| Flashlight | Diameter | `600px` |
| Flashlight | Gradient | `transparent 0%` → `rgba(0,0,0,0.9) 70%` |
| Flashlight | Box shadow | `0 0 0 3000px rgba(0,0,0,0.9)` |
| Data debris | Count | 5 particles |
| Data debris | Font | `text-[8px] font-mono text-green-500/40` |
| Data debris | Y travel | `-20px` to `-40px` |
| Spring | Stiffness | 400 |
| Spring | Damping | 30 |
| Spring | Mass | 0.5 |
| Breakpoint | Desktop only | `768px` (md) |

---

## GlowOrbits — Exact Implementation

### Ring Sizes & Positions
| Ring | Position | Size | Color (hex+opacity) | Blur |
|------|----------|------|---------------------|------|
| 1 | `-top-[20%] -left-[10%]` | `h-[60%] w-[60%]` | `${SPECTRUM[0]}33` | `blur-[120px]` |
| 2 | `-bottom-[20%] -right-[10%]` | `h-[70%] w-[70%]` | `${SPECTRUM[2]}22` | `blur-[140px]` |
| 3 | `top-1/2 left-1/2 -translate-x/y-1/2` | `h-[80%] w-[80%]` | `${SPECTRUM[6]}11` | `blur-[160px]` |

### Ring Animation (Web Animation API)
```ts
ring.animate([
  { transform: "rotate(0deg) scale(1)", opacity: 0.1 },
  { transform: "rotate(180deg) scale(1.15)", opacity: 0.25 },
  { transform: "rotate(360deg) scale(1)", opacity: 0.1 }
], {
  duration: 30000 + (index * 8000),  // Ring 0: 30s, Ring 1: 38s, Ring 2: 46s
  easing: "ease-in-out",
  iterations: Infinity
});
```

### Accent Blobs
| Blob | Position | Size | Color | Blur | Animation |
|------|----------|------|-------|------|-----------|
| Emerald | `top-1/4 right-1/4` | `h-64 w-64` (256px) | `bg-emerald-500/20` | `blur-[100px]` | scale [1,1.2,1], opacity [0.1,0.2,0.1], 10s |
| Blue | `bottom-1/4 left-1/3` | `h-80 w-80` (320px) | `bg-blue-500/20` | `blur-[110px]` | scale [1.2,1,1.2], opacity [0.1,0.15,0.1], 12s, delay 2s |

### Parallax Math
```ts
// Spring: damping 50, stiffness 100
const parallaxX = useTransform(mouseX, (val) => (val / window.innerWidth - 0.5) * -60);
const parallaxY = useTransform(mouseY, (val) => (val / window.innerHeight - 0.5) * -60);
// Range: -30px to +30px offset
```

---

## Audio Synthesis — Exact Parameters

### Click
```ts
osc.type = "sine";
osc.frequency.setValueAtTime(800, t);
osc.frequency.exponentialRampToValueAtTime(100, t + 0.1);
gain.gain.setValueAtTime(0.1, t);
gain.gain.exponentialRampToValueAtTime(0.01, t + 0.1);
osc.stop(t + 0.1);
```

### Zap
```ts
osc.type = "sine";
osc.frequency.setValueAtTime(600, t);
osc.frequency.exponentialRampToValueAtTime(80, t + 0.15);
gain.gain.setValueAtTime(0.04, t);
gain.gain.exponentialRampToValueAtTime(0.001, t + 0.15);
osc.stop(t + 0.15);
```

### Hum
```ts
osc.type = "triangle";
osc.frequency.setValueAtTime(60, t);
gain.gain.setValueAtTime(0, t);
gain.gain.linearRampToValueAtTime(0.1, t + 0.1);
gain.gain.linearRampToValueAtTime(0, t + 0.5);
osc.stop(t + 0.5);
```

### Error
```ts
osc.type = "square";
osc.frequency.setValueAtTime(150, t);
osc.frequency.setValueAtTime(100, t + 0.1);
gain.gain.setValueAtTime(0.05, t);
gain.gain.linearRampToValueAtTime(0, t + 0.3);
osc.stop(t + 0.3);
```

---

## Anatomy Mode CSS Injection

### Component Outlines
```css
.anatomy-mode [class*="FrankenContainer"],
.anatomy-mode [class*="glass-modern"],
.anatomy-mode [class*="SiteHeader"],
.anatomy-mode section {
  outline: 1.5px solid rgba(34, 197, 94, 0.3) !important;
  outline-offset: 6px;
  box-shadow: 0 0 20px rgba(34, 197, 94, 0.1) !important;
}
```

### Image Filters
```css
.anatomy-mode img, .anatomy-mode video {
  filter: grayscale(0.6) opacity(0.7) contrast(1.1);
  transition: filter 0.8s ease;
}
```

### Grid Overlay (::before, z-40)
```css
background-image:
  linear-gradient(rgba(34, 197, 94, 0.03) 1px, transparent 1px),
  linear-gradient(90deg, rgba(34, 197, 94, 0.03) 1px, transparent 1px);
background-size: 40px 40px;
opacity: 0.6;
```

### Scanline Sweep (::after, z-41)
```css
background: linear-gradient(to bottom,
  transparent 0%, rgba(34, 197, 94, 0.04) 50%, transparent 100%);
background-size: 100% 15px;
animation: scanline 12s linear infinite;
/* translateY(-100%) → translateY(100%) */
```

---

## Page Transition Animation (ClientShell)

```ts
// Enter
initial: prefersReducedMotion ? { opacity: 1 } : { opacity: 0 }
animate: { opacity: 1, transition: { duration: prefersReducedMotion ? 0 : 0.4, ease: "easeOut", delay: prefersReducedMotion ? 0 : 0.1 } }
// Exit
exit: prefersReducedMotion ? { opacity: 1 } : { opacity: 0, transition: { duration: 0.3, ease: "easeIn" } }
// AnimatePresence mode="wait"
```

---

## SectionShell — Exact Values

### Icon Map (22 icons)
```ts
sectionIcons = {
  barChart3, blocks, bug, clock, cpu, eye, fileText, gitCompare,
  globe, keyboard, layers, monitor, package, play, rocket, shield,
  skull, sparkles, terminal, twitter, zap, activity
}
```

### Layout Classes
- Container: `relative mx-auto max-w-7xl px-6 py-16 md:py-32 lg:py-48`
- Grid: `grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-24 items-start`
- Sidebar: `lg:col-span-4 lg:sticky lg:top-32 space-y-10`
- Content: `lg:col-span-8`
- Bottom border: `bg-gradient-to-r from-transparent via-green-500/10 to-transparent`

### Sidebar Animation
```ts
initial: { opacity: 0, x: -20 }
whileInView: { opacity: 1, x: 0 }
viewport: { once: true, amount: 0.05 }
transition: { duration: 0.8, ease: [0.19, 1, 0.22, 1] }
```

### Content Animation
Same as sidebar but: `initial: { opacity: 0, y: 40 }`, `delay: 0.2`, `duration: 1`

### Eyebrow
- Line: `h-px w-8 bg-green-500/40`
- Text: `text-[10px] font-black uppercase tracking-[0.3em] text-green-500/80`
- Container: `inline-flex items-center gap-3 mb-8`

### Icon Box
- Size: `h-12 w-12 rounded-xl`
- Style: `bg-green-500/5 border border-green-500/20 text-green-400`
- Attribute: `data-magnetic="true"`
- Fallback icon: `Activity`

### Title
- Style: `text-4xl md:text-5xl font-black tracking-tight text-white leading-tight`
- Wrapped in: `FrankenGlitch trigger="hover" intensity="low"`

---

## Screenshot Gallery — Exact Spring Config

```ts
const SLIDE_OFFSET = 400;  // pixels

// Spring for directional slide
x: { type: "spring", stiffness: 260, damping: 28, mass: 0.8 }
opacity: { duration: 0.25, ease: [0.4, 0, 0.2, 1] }
scale: { duration: 0.35, ease: [0.4, 0, 0.2, 1] }

// Touch swipe threshold: 60px
// Image sizes: "(max-width: 640px) 100vw, (max-width: 768px) 50vw, 33vw"
```

---

## Feature Card — Exact Radial Gradient

```ts
const background = useMotionTemplate`
  radial-gradient(600px circle at ${mouseX}px ${mouseY}px, ${accentColor}15, transparent 80%)
`;
// 600px radius, accent at 15% opacity suffix, transparent at 80%
```

### Anatomy Mode Hex Overlay
```ts
// 40 elements, each:
const hex = Math.random().toString(16).substring(2, 40);
// Color: ${accentColor}33 (accent at ~20% opacity)
```

---

## Rust Tokenizer — Exact Regex

```regex
/::|\b(?:format|println|eprintln|dbg|vec|panic|todo|unreachable|cfg|derive)!|
  \b(?:use|fn|let|mut|match|impl|struct|enum|pub|self|type|mod|where|for|in|if|else|return|const|static|trait|derive|cfg|async|await|move|crate|super)\b|
  \b(?:Self|Cmd|Event|Msg|Rect|Frame|Paragraph|App|ScreenMode|Model|u64|u32|u16|u8|usize|i64|i32|isize|bool|str|String|Vec|Box|Option|Result|true|false|None|Some|Ok|Err)\b|
  \b\d+\b|\b[a-z_][a-z0-9_]*\b(?=\s*\()/g
```

### Token Colors
| Token | Tailwind Class |
|-------|---------------|
| string | `text-lime-300` |
| comment | `text-slate-600 italic` |
| keyword | `text-green-400 font-black` |
| type | `text-emerald-300 font-bold` |
| macro | `text-yellow-300 font-bold` |
| number | `text-amber-300` |
| func | `text-blue-300` |
| path | `text-slate-500` |
| special | `text-orange-300` |

---

## Terminal Demo — Exact Typing Sequence

```ts
const LINES = [
  { text: "$ cargo add ftui", style: "command", delay: 400, speed: 1, typed: true },
  { text: "    Updating crates.io index", style: "dim", delay: 600, speed: 2, typed: false },
  { text: "      Adding ftui v0.1.1 to dependencies", style: "green", delay: 400, speed: 2, typed: false },
  { text: "", style: "dim", delay: 300, speed: 1, typed: false },
  { text: "$ cargo run --example dashboard", style: "command", delay: 600, speed: 1, typed: true },
  { text: "    Compiling ftui v0.1.1", style: "dim", delay: 500, speed: 2, typed: false },
  { text: "     Running target/debug/examples/dashboard", style: "dim", delay: 400, speed: 2, typed: false },
  { text: "", style: "dim", delay: 300, speed: 1, typed: false },
  { text: "┌─ Metrics ──────┐ ┌─ Events ──────────┐", style: "dashboard-border", delay: 200, speed: 3 },
  { text: "│ CPU    ██▓░ 54%│ │ 14:32 task.done   │", style: "dashboard-mixed", delay: 100, speed: 3 },
  { text: "│ Memory ███░ 71%│ │ 14:31 deploy.ok   │", style: "dashboard-mixed", delay: 100, speed: 3 },
  { text: "│ Disk   █░░░ 22%│ │ 14:30 build.pass  │", style: "dashboard-mixed", delay: 100, speed: 3 },
  { text: "└────────────────┘ └───────────────────┘", style: "dashboard-border", delay: 100, speed: 3 },
];
// TYPING_SPEED_BASE = 30ms per char
```

---

## DecodingText — Exact Glyph Set

```ts
const GLYPHS = "0123456789ABCDEF$#@&*<>[]{}";
// 28 characters for random replacement
// Reveal threshold per char: i / chars.length
// Default duration: 1000ms
```

---

## Spectral Background — Exact Layer Values

| Layer | Property | Value |
|-------|----------|-------|
| Film grain | Filter | feTurbulence fractalNoise |
| Film grain | Base frequency | 0.65 → 0.68 → 0.65 (animated) |
| Film grain | Octaves | 3 |
| Film grain | Opacity | 0.04 |
| Film grain | Blend mode | overlay |
| Scanlines | Direction | 90deg (vertical) |
| Scanlines | Pattern width | 100px |
| Scanlines | Opacity | [0.05, 0.08, 0.04, 0.07], 4s |
| Interference | Height | 1px |
| Interference | Blur | 1px |
| Interference | Y travel | -10vh → 110vh, 8s, delay 2s |
| Interference | Opacity | [0, 0.3, 0] |
| Green glow | Size | 50% × 50% |
| Green glow | Position | top-0, left-1/4 |
| Green glow | Blur | 120px |
| Blue glow | Size | 40% × 40% |
| Blue glow | Position | bottom-0, right-1/4 |
| Blue glow | Blur | 100px |

---

## AnimatedNumber — Exact Formula

```ts
function easeOutExpo(t: number): number {
  return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
}
// Duration: 2000ms
// IntersectionObserver threshold: 0.3
```

---

## Motion Variants — Exact Configs

### fadeUp
```ts
hidden: { opacity: 0, y: 24 }
visible: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 200, damping: 25 } }
exit: { opacity: 0, y: -12, transition: { duration: 0.2 } }
```

### fadeScale
```ts
hidden: { opacity: 0, scale: 0.96 }
visible: { opacity: 1, scale: 1, transition: { type: "spring", stiffness: 200, damping: 25 } }
exit: { opacity: 0, scale: 0.98, transition: { duration: 0.15 } }
```

### staggerContainer
```ts
visible: { transition: { staggerChildren: 0.06, delayChildren: 0.1 } }
```

### staggerFast
```ts
visible: { transition: { staggerChildren: 0.04, delayChildren: 0.05 } }
```

### sheetEntrance
```ts
hidden: { y: "100%", opacity: 0.8 }
visible: { y: 0, opacity: 1, transition: { type: "spring", stiffness: 300, damping: 30 } }
exit: { y: "100%", opacity: 0.8, transition: { duration: 0.2 } }
```

---

## Site Footer — Exact Structure

### Status Indicators
```ts
// "ALL SYSTEMS OPERATIONAL"
// Dot: h-1.5 w-1.5, bg-green-500, shadow-[0_0_8px_#22c55e]
// Animation: scale [1, 1.5, 1], opacity [0.3, 1, 0.3], duration 1.5s

// "KERNEL v0.1.1 ACTIVE"
// text-[10px] font-black uppercase tracking-[0.3em] text-slate-600
```

### Social Links
- Wrapped in `Magnetic strength={0.3}`
- Size: `h-12 w-12 rounded-2xl`
- Base: `bg-white/5 border border-white/10 text-slate-400`
- Hover: `text-green-400 border-green-500/40 bg-green-500/5`
- Shadow: `shadow-[0_0_20px_rgba(0,0,0,0.2)]`

### Back-to-Top Arrow
```ts
y: [0, -4, 0], duration: 1.5, repeat: Infinity, ease: "easeInOut"
// Tracking expansion on hover: tracking-[0.3em] → tracking-[0.4em]
```

### Attribution
```
"MADE IN 5 DAYS"
text-[10px] font-black text-white/5 uppercase tracking-[0.5em] select-none
```

---

## Global CSS Body Rules

```css
body {
  background-color: #020a02;
  color: #f1f5f9;
  font-family: var(--font-sans);
  font-feature-settings: "cv02", "cv03", "cv04", "cv11";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.6;
  letter-spacing: -0.01em;
  overflow-x: hidden;
}

h1, h2, h3, h4 {
  letter-spacing: -0.02em;
  font-weight: 900;
  line-height: 1.1;
}
```

---

## Complete Shadow Definitions

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.5);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
--shadow-franken: 0 0 40px -10px rgba(34, 197, 94, 0.2);
```
