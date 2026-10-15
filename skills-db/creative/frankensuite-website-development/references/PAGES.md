# FrankenSuite Page Patterns — Full Reference

> Each page in frankentui.com demonstrates reusable patterns for building FrankenSuite project websites.

---

## Homepage (`app/page.tsx`)

The homepage is the most complex page. Follow this exact section order:

### 1. Hero Section
- **Title**: `text-[clamp(3.5rem,10vw,7rem)] font-black tracking-tighter leading-[1.1]`
- **Subtitle**: `text-lg md:text-xl text-slate-400 font-medium tracking-tight max-w-2xl`
- **CTA buttons**: Two buttons — primary (green gradient, `active:scale-95`) + secondary (outline)
- **Layout**: `flex-col sm:flex-row` for button stack on mobile
- **GlowOrbits**: Parallax background orbs using Web Animation API, IntersectionObserver pauses off-screen
- **FrankenEye**: Mouse-tracking eye with blood vessels (proximity-based opacity), random blink (2.5s interval), pupil dilation on hover. Hidden on mobile (`hidden lg:block`), scale `100 md:scale-150`
- **Video element**: `autoPlay muted loop playsInline`, poster image, scanline overlay (4px repeating gradient at opacity 0.3)
- **Stats cards**: Floating glass-morphism card at `-bottom-10`, monospace + `tabular-nums` for alignment
- **Lightning arcs**: SVG paths with Framer Motion `pathLength` animation

### 2. Terminal Demo Section
- **TerminalDemo component**: Hardcoded 25-line typing animation sequence
- Per-line `speed` (ms per char) + `delay` (ms before line starts)
- Character-by-character reveal with color batching for performance
- IntersectionObserver visibility trigger (starts only when scrolled into view)
- Dashboard visualization using box-drawing characters (└─┐│ etc.)
- Terminal chrome header with traffic light dots

### 3. Features Section
- **SectionShell** wrapper with icon="sparkles"
- **FeatureCard grid**: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4`
- Each card: deterministic accent color from SPECTRUM via title char hash
- Mouse-tracking radial gradient: `useMotionTemplate` + `useMotionValue`
- Anatomy mode: 40-line hex data matrix overlay + SVG wireframe
- Touch support: `onTouchMove`/`onTouchStart`/`onTouchEnd` handlers

### 4. Browser/WASM Section (Optional)
- Demonstrates WebGPU/WASM capabilities
- `browserAdvantages` and `browserComparisonData` from content.ts
- Comparison cards with advantage/disadvantage markers

### 5. Screenshot Gallery
- **ScreenshotGallery component**: Lightbox with spring-physics directional slide
- Direction-aware: slides enter from left or right (400px offset) based on navigation direction
- Keyboard: Escape closes, ← → navigate
- Touch swipe: 60px threshold
- Portal rendering for z-index isolation
- Body scroll lock with scrollbar width compensation
- `loading="lazy"` on thumbnails, `priority` only on lightbox active image

### 6. Comparison Table
- **ComparisonTable component**: Framework comparison
- StatusCell helper renders ✓ (green-400), ✗ (slate-600), ⚠ (yellow-400/500)
- Row-level hover animation: background color transition
- FrankenGlitch on feature names and FrankenTUI column header
- Responsive: horizontal scroll on mobile via `overflow-x-auto`

### 7. Code Block
- **RustCodeBlock component**: Custom Rust tokenizer (NOT highlight.js)
- Token types: keyword, type, macro, string, comment, number, operator, function
- Terminal chrome header with traffic lights + title
- Copy-to-clipboard: `navigator.clipboard.writeText()`, check icon toggle with 2s timeout
- Line numbers in `text-slate-700 select-none`
- FrankenBolt corners
- **IMPORTANT**: Uses `title` prop, NOT `filename`

### 8. Timeline/Changelog
- **Timeline component**: Vertical line with gradient + node dots
- Ping animation on node hover (scale pulse)
- Two-column layout: time label (mono, green) + content block
- Staggered viewport-entry animations per item
- Bullet items with green glow on hover

### 9. Tweet Wall
- **TweetWall component**: react-tweet embeds + fallback content cards
- CSS columns masonry: `columns-1 md:columns-2`
- GlassFrankenCard wrapper per tweet
- react-tweet theme overrides in globals.css (transparent backgrounds, green accents)
- Fallback cards for tweets without `tweetId`: quote text + attribution

### 10. Get Started CTA
- Final conversion section
- Primary CTA button + secondary GitHub link
- Repeat of key stats or unique selling points

---

## Showcase Page (`app/showcase/page.tsx`)

- **LazyTerminalSection**: Custom IntersectionObserver with 200px rootMargin for lazy loading
- FrankenTerminal wraps WASM module (loaded via singleton cache pattern)
- Fallback loading state while WASM initializes
- **Video Collection**: `Suspense` with fallback states, `preload="metadata"` optimization
- Play button overlay hides after first playback
- Scanline overlay on videos
- **Full Screenshot Gallery**: Same component as homepage but with all screenshots

---

## Architecture Page (`app/architecture/page.tsx`)

- **Deterministic Colors**: Same SPECTRUM hash pattern as FeatureCards
- **Pipeline Stages**: 5-stage render cycle visualization
  - Animated data packets moving between stages (spring animations)
  - Kinetic arrows with blur particle effects traversing between stages
- **16-Byte Cell Model**: Technical spec table with field breakdown
  - Grid layout, hovers activate per-cell background colors
  - Detailed field: grapheme, fg, bg, attributes, reserved
- **Decision Cards**: Dynamic accent colors via title hash
  - Icon rotation on hover
  - Glass-modern containers with spectrum accent borders
- **Crate Grid**: Workspace crate overview (name, description, size)
- **Algorithm Showcase**: Cards with algorithm details + complexity annotations

---

## Getting Started Page (`app/getting-started/page.tsx`)

- **Copy-to-Clipboard Terminal**: `navigator.clipboard` API
  - Toggle between Copy/Check icon with 2s timeout
  - Terminal chrome styling (mini traffic lights, monospace)
  - FrankenContainer wrapper
- **Expandable FAQ**: HTML `<details>` element
  - Marker hidden, custom chevron with `rotate(45deg)` on `[open]`
  - Color transition green-500 → slate-400 on summary text
  - Smooth content reveal
- **Installation Steps**: Two-column layout
  - Left: numbered step with description
  - Right: terminal command block with copy button
- **Prerequisites Checklist**: Green check marks, mono font for version numbers

---

## Glossary Page (`app/glossary/page.tsx`)

- **Dynamic Search**: Input with real-time filtering of `jargon` terms
- **Alphabetical Grouping**: Terms grouped by first letter
  - Count badge per letter group
  - Sticky letter sidebar with `text-7xl opacity-10` giant letter background
- **Bottom Sheet Modal**: Slide-up animation via Portal
  - `useBodyScrollLock` when open
  - Keyboard Escape support
  - 92vh max height
  - `dialog` role with `aria-modal`
- **Term Detail View** (3 columns):
  1. Short definition
  2. Monster Analogy callout (green-tinted box)
  3. Technical Rationale section
  4. Connected Nodes (related terms as clickable chips)
- **Streamdown Component**: Custom markdown renderer for term descriptions

---

## Beads / Project Graph Page (`app/beads/page.tsx`)

- **Dynamic Import**: `next/dynamic` with `ssr: false` (SQL.js can't run server-side)
- **Loading State**: Custom green progress bar spinner
- **BeadsView Component** (`components/beads/beads-view.tsx`):
  - SQL.js: Loads `.beads/beads.db` via fetch, queries with SQL
  - Force-Graph: Canvas-based DAG visualization
  - Node styling: Color by status (open=green, in_progress=yellow, blocked=red, closed=slate)
  - Link particles: Directional animated dots on edges
  - Click: Modal detail pane with Streamdown markdown rendering
  - Priority-based node sizing

---

## How It Was Built Page (`app/how-it-was-built/page.tsx`)

- **Key Stats Grid**: 4-column responsive, group hover states
  - Inline NeuralPulse, gradient top border on hover
- **Dev Process Insights**: Flavor-based styling system
  - `breakthrough`: emerald border/bg
  - `decision`: amber border/bg
  - `crisis`: red border/bg
  - `grind`: slate border/bg
  - `ship`: sky border/bg
- **Git Log Terminal**: Monospace scrollable container
  - Scanline overlay
  - Highlighted publish lines in green
  - Epoch timestamps + author metadata
- **Spec Evolution Lab CTA**: FrankenContainer with monster head image, pulse glow, corner brackets that scale on hover, multi-arc SVG lightning

---

## Spec Evolution Lab (`app/how-it-was-built/spec-evolution-lab/page.tsx`)

Most complex page — 1000+ line component with:
- **Complex State Machine**: BucketMode (day/hour/15m/5m), DiffFormat (unified/sideBySide), TabKey switching
- **LRU Caches** (module-level, survive re-renders):
  - MarkdownHTMLCache (16 entries)
  - PatchParseCache (32 entries)
  - SnapshotMdCache (32 entries)
- **Myers Diff Algorithm**: Line-based diff computation
- **Timeline Scrubber**: Playback speed control (0.5x, 1x, 2x, 4x)
- **Taxonomy Visualization**: 11 bucket categories with assigned colors, stacked bar charts
- **CorpusIndex**: Full-text search indexing
- **Module CSS**: `spec-evolution-lab.module.css` with:
  - `.mdProse`: Full typography customization
  - `content-visibility: auto` on commit rows for virtualization
  - Responsive tables that stack on mobile via `data-label` + `::before` pseudo-elements
  - Scoped highlight.js theme (sky/emerald/amber/violet colors)

---

## Web React Page (`app/web_react/page.tsx`)

- **Resizable Terminal**: Custom `useResize` hook with pointer events
  - Min/max constraints, container-relative drag tracking
  - Pointer capture for reliable dragging
- **Preset Sizes**: Compact (80×24), Standard (120×35), Wide (160×45), Full-width
- **Code Snippet**: Integrated copy button with Check/Copy icon toggle
- **Props Reference Table**: Comprehensive prop documentation with type signatures and defaults

---

## Metadata & SEO Pattern

### Root Layout (`app/layout.tsx`)
```tsx
export const metadata: Metadata = {
  title: { default: siteConfig.title, template: `%s | ${siteConfig.name}` },
  description: siteConfig.description,
  openGraph: { title, description, url, locale: "en_US", type: "website" },
  twitter: { card: "summary_large_image" },
  robots: { index: true, follow: true },
  icons: { icon: "/favicon.ico", apple: "/apple-icon.png" },
};
export const viewport: Viewport = { themeColor: "#020a02" };
```

### Per-Page Metadata
Each route exports its own metadata:
```tsx
export const metadata: Metadata = {
  title: "Architecture",
  description: "Deep dive into the FrankenTUI rendering architecture...",
};
```

### OG Images
Each page can have `opengraph-image.tsx` and `twitter-image.tsx` files that use `ImageResponse` from `next/og`.
