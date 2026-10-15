# FrankenSuite Component Patterns — Full Reference

---

## Shell Structure

```
app/layout.tsx (Server Component)
  ├── Inter + JetBrains Mono fonts loaded
  ├── metadata + viewport configured
  └── <ClientShell> (single "use client" boundary)
        ├── <SiteProvider> (context: anatomy, terminal, audio)
        ├── <SignalHUD> (diagnostic overlay)
        ├── <SiteTerminal> (backtick toggle)
        ├── <CustomCursor> (desktop only, md+ media query)
        ├── <SiteHeader> (desktop pill + mobile bottom nav)
        ├── <AnimatePresence> + <motion.div> (page transitions)
        │     └── {children} (page content)
        ├── <SiteFooter> (glassmorphic, 12-col grid)
        └── <ScrollToTop>
```

**Key insight**: One `"use client"` boundary (`ClientShell`) wraps everything. Page components are Server Components that import client components directly.

---

## SectionShell — Core Layout Primitive

Every content section uses this wrapper:
```tsx
<SectionShell
  id="features"
  icon="sparkles"          // String key — NOT component ref
  eyebrow="Why FrankenTUI"
  title="Built Different"
  kicker="Description text..."
>
  {/* 8-column content area */}
</SectionShell>
```

**Layout**: `grid-cols-1 lg:grid-cols-12`
- Columns 1-4: Sticky sidebar (icon + eyebrow + title + kicker + decorative stitch)
- Columns 5-12: Scrollable content area

**Icon system**: Icons are string keys mapped to an internal `sectionIcons` record.
Adding a new icon requires:
1. Import from `lucide-react`
2. Add entry to `sectionIcons` map in `section-shell.tsx`

Available icons (21): `sparkles`, `code`, `terminal`, `layers`, `cpu`, `zap`, `eye`, `globe`, `rocket`, `network`, `info`, `book`, `puzzle`, `image`, `git-branch`, `layout`, `database`, `shield`, `film`, `star`, `monitor`

---

## Decorative System (FrankenSuite Brand)

### FrankenBolt
Industrial bolt with electrical arc SVGs on hover.
```tsx
<FrankenBolt color="#22c55e" baseScale={0.5} className="absolute -left-1.5 -top-1.5" />
```
Props: `color`, `baseScale`, `className`. 14px bolt with dark gradient, inner cross, dual SVG arcs on hover.

### FrankenStitch
Cross-stitch SVG decoration.
```tsx
<FrankenStitch orientation="horizontal" length={80} className="..." />
```
Props: `orientation` (horizontal/vertical), `length`, `className`. Hover: scale 1.05, opacity 0.35→0.7.

### FrankenContainer
Primary card wrapper combining all decorative elements (5 layers: outer div → stitched skin → corner bolts → edge stitches → content):
```tsx
<FrankenContainer className="p-8" showStitches={true}>{children}</FrankenContainer>
```

### NeuralPulse
Traveling spark beam along container border. Two beams traverse clockwise over 4s.
```tsx
<NeuralPulse color="#22c55e" className="opacity-40" />
```

### FrankenGlitch
RGB chromatic aberration split/shake effect.
```tsx
<FrankenGlitch trigger="hover" intensity="medium"><h1>Title</h1></FrankenGlitch>
```
- `trigger`: `"hover"` | `"always"` | `"random"` (15% chance every 3s)
- `intensity`: `"low"` (±2px) | `"medium"` (±5px) | `"high"` (±10px)

### Magnetic
Spring-physics cursor-following wrapper.
```tsx
<Magnetic strength={0.1}><button>GITHUB</button></Magnetic>
```
Element leans toward cursor at `(clientX - centerX) * strength`. Default 0.2-0.25.

### BorderBeam
CSS conic-gradient beam rotating around border. Compositor-thread, auto-pauses off-screen.
```tsx
<BorderBeam size={200} duration={8} />
```

Exact SVG paths, keyframes, and animation configs for all decorative components: [EXACT-VALUES.md](EXACT-VALUES.md)

---

## FrankenEye — Mouse-Tracking Animated Eye

```tsx
<FrankenEye />  // Positioned absolutely in hero, hidden lg:block, scale-100 md:scale-150
```
Sclera with blood vessel SVGs (proximity-based opacity), iris with conic gradient pattern, pupil dilation on hover, random blink (~2.5s, 20% chance), RAF-throttled mouse tracking via `atan2`.

Exact SVG paths, tracking math, blink timing: [EXACT-VALUES.md](EXACT-VALUES.md)

---

## DecodingText — Character Reveal Animation

```tsx
<DecodingText text="HELLO WORLD" duration={1000} className="text-green-400" />
```

- Character-by-character reveal using requestAnimationFrame
- Non-revealed chars show random glyphs: `"0123456789ABCDEF$#@&*<>[]{}"`
- Progress: `i / chars.length` threshold per character
- During animation: `text-green-400/80`
- After completion: applies input className

---

## SpectralBackground — Film Grain Analog Effects

4 layers for cinematic feel:
1. **Film grain**: SVG feTurbulence, baseFrequency animated 0.65→0.68, opacity 0.04, `mix-blend-mode: overlay`
2. **Vertical scanlines**: 90deg gradient, opacity pulsing [0.05, 0.08], 4s
3. **Horizontal interference**: 1px line, blur, Y: -10vh→110vh over 8s
4. **Light leaks**: Green blob (top-left) + blue blob (bottom-right), opacity pulse

---

## AnimatedNumber — Counter with easeOutExpo

```tsx
<AnimatedNumber value={50000} suffix="+" />
```

- RAF-based counter from 0 → target over 2000ms
- Easing: `easeOutExpo` formula: `1 - 2^(-10t)`
- Visibility trigger: IntersectionObserver with `once: true`
- Respects `prefers-reduced-motion` (shows final value immediately)

---

## GlowOrbits — Parallax Background Rings

Uses **native Web Animation API** (NOT Framer Motion) for performance. 3 glow rings (blur-120-160px) + 2 accent blobs, parallax via `useTransform`/`useSpring` (±30px offset). IntersectionObserver pauses off-screen. `useReducedMotion()` disables entirely.

Ring sizes, positions, colors, parallax math: [EXACT-VALUES.md](EXACT-VALUES.md)

---

## VideoPlayer

```tsx
<VideoPlayer src="/videos/demo.mp4" poster="/screenshots/demo.webp" />
```

- FrankenContainer wrapper with `withPulse`, border hover effect
- Lazy play button overlay (`data-magnetic="true"` for cursor attraction)
  - 24×24 rounded-full, green-500 with glow shadow
  - Hides after first playback
- Scanline overlay: 4px repeating gradient, opacity 0.3
- `preload="metadata"` optimization
- Video controls appear conditionally post-start

---

## ErrorBoundary

Class component wrapping ClientShell:
```tsx
<ErrorBoundary fallback={<ErrorUI />}>
  <ClientShell>{children}</ClientShell>
</ErrorBoundary>
```

- Styled as "Kernel_Panic" with dump ID (random hex string)
- Error message displayed in `<code>` block
- Retry button (resets state via `setState({ hasError: false })`)
- Reload button (full page reload via `window.location.reload()`)
- `role="alert" aria-live="assertive"` for screen readers

---

## TerminalDemo — Typing Animation

25-line hardcoded command sequence with per-line config:
```ts
{ text: "cargo build --release", speed: 30, delay: 500 }
```

- Character-by-character reveal with color batching (performance)
- IntersectionObserver: starts only when scrolled into view
- Dashboard visualization using box-drawing chars (└─┐│)
- Terminal chrome: traffic light dots + title bar
- Cursor: blinking block at end of current line

---

## FrankenTerminal — WASM Integration

Wraps FrankenTUI WASM module for live terminal demo:
- **WASM loader** (`lib/wasm-loader.ts`): Singleton cache, `new Function()` for native ES module import (bypasses Next.js bundler)
- **Font loading**: Pragmasevka NF via FontFace API
- **Text assets**: Optional 14MB Shakespeare + SQLite source data
- Canvas-based rendering with WebGPU detection
- `ResizeObserver` for responsive terminal sizing
- Cell width/height calculation, zoom level support
- Keyboard capture for terminal input
- Status overlay: cols×rows display
- Error/loading/fallback component slots

---

## ComparisonTable

```tsx
<ComparisonTable data={comparisonData} />
```

- StatusCell helper: ✓ (green-400), ✗ (slate-600), ⚠ (yellow-400/500)
- Row-level hover: background color animation
- FrankenGlitch on feature names and primary column header
- Responsive: `overflow-x-auto` horizontal scroll on mobile

---

## Timeline

```tsx
<Timeline items={changelog} />
```

- Vertical gradient line with animated node dots
- Ping animation on hover (scale pulse, green glow)
- Two-column layout: time label (mono, green) + content block
- Staggered viewport-entry animations per item
- Bullet items with green glow effect on hover

---

## Motion Patterns

### Spring Presets (components/motion/index.tsx)
```ts
springs = { smooth: {200,25}, snappy: {400,35}, gentle: {100,20}, quick: {500,40} }
```

### Key Patterns
- **Viewport entry** (most common): `initial={{opacity:0,y:40}} whileInView={{opacity:1,y:0}} viewport={{once:true,amount:0.05}} transition={{duration:0.8,ease:[0.19,1,0.22,1]}}`
- **Staggered entry**: `delay: (index % 4) * 0.1`
- **Kinetic hover** (CSS): `translateY(-4px) scale(1.01)` with `--ease-stripe`
- **Reduced motion**: ALWAYS check `useReducedMotion()` — skip to final state
- **Page transitions**: `AnimatePresence mode="wait"` with opacity fade in ClientShell
- **Easing**: `cubic-bezier(0.19, 1, 0.22, 1)` (Stripe-like), `cubic-bezier(0.16, 1, 0.3, 1)` (out-expo)

### Reusable Variants
`fadeUp` (y 24→0), `fadeScale` (scale 0.96→1), `staggerContainer` (0.06s children), `staggerFast` (0.04s), `sheetEntrance` (y 100%→0)

Exact variant configs with all values: [EXACT-VALUES.md](EXACT-VALUES.md)

---

## Feature Cards

Deterministic accent from SPECTRUM array via title char hash. Mouse-tracking radial gradient on hover (`useMotionTemplate`). FrankenContainer wrapper. SPECTRUM values and gradient template: [EXACT-VALUES.md](EXACT-VALUES.md), hash formula: [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md)

---

## Custom Cursor (Desktop Only)

Activates on `md+` via `window.matchMedia("(min-width: 768px)")`. All animations use RAF batching.

### Data Attributes
| Attribute | Effect |
|-----------|--------|
| `data-technical="true"` | Data debris particle trail (hex/binary chars) |
| `data-flashlight="true"` | 600px radial vignette darkening |
| `data-magnetic="true"` | Element attracts cursor (60px radius) |
| `data-cursor="pointer"` | Crosshair lines appear |

Visual elements: outer ring (scales 1→1.4 on pointer, 0.7 on click), inner dot (glow, red flash on click), crosshair lines, click glitch burst, flashlight vignette, data debris particles. Spring: `stiffness: 400, damping: 30, mass: 0.5`.

Exact dimensions, DOM walk algorithm, PRNG formula, debris generation: [EXACT-VALUES.md](EXACT-VALUES.md)

---

## Stat Counters (StatsGrid)

Animated number counters triggered by IntersectionObserver:
- Numbers count up from 0 to target over ~2 seconds
- FrankenContainer wrappers with NeuralPulse on hover
- Corner bolts on each stat card

---

## Screenshot Gallery

Lightbox with spring-physics directional slide animations:
- Left/right keyboard navigation (ArrowLeft/ArrowRight, Escape)
- Touch swipe support (60px threshold)
- Portal-based modal for z-index isolation
- Body scroll lock with scrollbar width compensation

---

## Code Blocks (RustCodeBlock)

Custom Rust tokenizer (not highlight.js for inline code):
- Token types: keyword, type, macro, string, comment, number, operator, function
- Terminal chrome header with traffic lights
- Copy-to-clipboard button
- Line numbers
- FrankenBolt corners
- Uses `title` prop (NOT `filename`)

---

## Tweet Wall

react-tweet embeds in glassmorphic card wrappers:
- Masonry layout via CSS `columns: 1` / `columns: 2` at md
- Fallback content cards for non-embedded tweets
- Glass-modern card styling overrides react-tweet defaults

---

## Hooks

| Hook | Purpose | Key detail |
|------|---------|------------|
| `useBodyScrollLock(isLocked)` | Prevents body scroll + compensates scrollbar width | Calculates scrollbar width to prevent layout shift |
| `useIntersectionObserver(ref, options)` | Returns IntersectionObserverEntry | Supports `threshold`, `rootMargin`, `triggerOnce` |
| `useHapticFeedback()` | Vibration API wrapper for mobile | Returns `triggerHaptic(pattern)` function |
| `useResize()` (in web_react) | Pointer-based container resize | Min/max constraints, pointer capture for reliable drag |

---

## Site State (SiteProvider)

### Context Values
| Value | Type | Description |
|-------|------|-------------|
| `isAnatomyMode` | boolean | Wireframe debug overlay active |
| `toggleAnatomyMode` | function | Toggle anatomy mode |
| `isTerminalOpen` | boolean | Terminal overlay visible |
| `setTerminalOpen` | function | Control terminal visibility |
| `isAudioEnabled` | boolean | Audio effects enabled |
| `toggleAudio` | function | Toggle audio on/off |
| `playSfx(type)` | function | Play synthesized sound |

### Keyboard Shortcuts
- **Backtick** (`` ` ``): Toggle terminal (checks `isTextInputLike()` to avoid conflict with text inputs)
- **Ctrl+Shift+X**: Toggle anatomy mode

### Audio SFX (Web Audio API Oscillator Synthesis)
```ts
playSfx("click")  // sine 800→100Hz exponential ramp, short
playSfx("zap")    // sine 600→80Hz with gain ramp, electrical
playSfx("hum")    // triangle 60Hz with 0.5s envelope, low rumble
playSfx("error")  // square 150→100Hz, harsh
```
Audio context initialized lazily (deferred). Non-fatal try-catch on creation.

### Anatomy Mode Effects (CSS)
When active, injects global styles:
- Component outlines with dashed green borders
- Grid overlay via repeating linear gradients
- Scanline animation across entire page
- Grayscale filter on all images
- Components show hex data watermark overlays
- SVG wireframe overlays on feature cards

---

## Utility Functions (lib/utils.ts)

| Function | Purpose |
|----------|---------|
| `cn(...inputs)` | `clsx` + `tailwind-merge` for className composition |
| `isTextInputLike(el)` | Detects input/textarea/contenteditable (for keyboard shortcut guards) |
| `NOISE_SVG_DATA_URI` | Inline SVG feTurbulence noise texture data URI |
| `formatDate(iso)` | ISO → relative time ("5h ago", "3d ago") |
| `formatDateFull(iso)` | ISO → full readable format with time |

---

## LRU Cache (lib/lru-cache.ts)

Generic LRU cache used for expensive computations:
```ts
const cache = new LRUCache<string, string>(16);
cache.get(key);     // returns cached value or undefined
cache.set(key, val); // evicts oldest if at capacity
```

Used in spec-evolution-lab for:
- MarkdownHTMLCache (16 entries) — rendered markdown HTML
- PatchParseCache (32 entries) — parsed diff patches
- SnapshotMdCache (32 entries) — snapshot markdown content

Module-level caches survive re-renders (not in state/refs).

---

## Portal Component (motion-wrapper.tsx)

```tsx
<Portal>{children}</Portal>
```

Renders children into `document.body` via `createPortal`. Essential for:
- Lightbox modals (avoid "fixed inside transform" CSS bugs)
- Bottom sheet dialogs
- Custom cursor layers

---

## WASM Module Loading (lib/wasm-loader.ts)

Singleton cache pattern for WASM modules:
```ts
// Native ES module import to preserve import.meta.url (bypasses Next.js bundler)
const nativeImport = new Function("url", "return import(url)");
```

- Parallel `Promise.all()` for loading multiple modules
- Font loading via `FontFace` API (Pragmasevka NF for terminal)
- Text asset loading with separate cache (Shakespeare + SQLite source, ~14MB)
- Reset capability for cleanup
