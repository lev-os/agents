# FrankenSuite Design System — Full Reference

> "Stripe-Grade Monster Technical" — dark, technical, premium.

---

## Color Palette

### Core Colors (CSS Custom Properties in globals.css)
```css
:root {
  --color-bg: #020a02;           /* Near-black with green tint */
  --color-surface: #051205;       /* Card/surface backgrounds */
  --color-border: rgba(34, 197, 94, 0.1);  /* Subtle green borders */
  --color-green-prime: #22c55e;   /* Primary accent */
  --color-green-glow: #4ade80;    /* Lighter green for glows */
  --color-lime-prime: #a3e635;    /* Secondary accent (lime) */
}
```

### Text Colors
| Use | Color | Tailwind |
|-----|-------|----------|
| Body text | `#f1f5f9` | slate-100 |
| Muted text | — | slate-400, slate-500 |
| Micro-labels | — | slate-500, slate-600, green-500/80 |
| Links/active | `#22c55e` | green-500 |

### Spectrum Colors (Deterministic Card Accents)
```ts
const SPECTRUM = ["#38bdf8", "#a78bfa", "#f472b6", "#ef4444", "#fb923c", "#fbbf24", "#34d399", "#22d3ee"];
// Assigned via character code hash of title — NOT random
const idx = title.split("").reduce((a, c) => a + c.charCodeAt(0), 0) % SPECTRUM.length;
```

### Swapping Accent for a New Project
Update these locations when changing from green to another accent:
1. `globals.css` — CSS custom properties
2. `globals.css` — scrollbar thumb hover color
3. `globals.css` — glass-modern border color
4. Component accent prop defaults (FrankenBolt, NeuralPulse, etc.)
5. Tailwind classes: `green-400`, `green-500`, `green-500/10`, `green-500/20` throughout components

---

## Typography

### Font Loading (app/layout.tsx)
```tsx
import { Inter, JetBrains_Mono } from "next/font/google";
const inter = Inter({ variable: "--font-inter", subsets: ["latin"], display: "swap" });
const jetbrainsMono = JetBrains_Mono({ variable: "--font-jetbrains", subsets: ["latin"], display: "swap" });
// Body: className={`${inter.variable} ${jetbrainsMono.variable} font-sans antialiased`}
```

### Font Feature Settings
```css
body { font-feature-settings: "cv02", "cv03", "cv04", "cv11"; }
```
Enables alternate glyphs for Inter (better readability).

### Scale
| Element | Size | Weight | Tracking | Leading |
|---------|------|--------|----------|---------|
| Hero title | `clamp(3.5rem,10vw,7rem)` | 900 (font-black) | -0.02em (tracking-tighter) | 1.1 |
| Section title | text-4xl to text-5xl | 900 | -0.02em | 1.1 |
| Body | text-base to text-lg | 500 (font-medium) | -0.01em (tracking-tight) | 1.6 |
| Micro-labels | `text-[10px]` | 900 | `tracking-[0.3em]` or widest | — |
| Eyebrow | text-xs | 900 | `tracking-[0.4em]` | — |
| Code | font-mono text-sm | — | — | — |

### Micro-Label Pattern (Signature)
```html
<span class="text-[10px] font-black uppercase tracking-[0.3em] text-green-500/80">
  SYSTEM_ALIVE
</span>
```
Used for: nav labels, status indicators, section eyebrows, mobile tab labels.

---

## Spacing System

| Context | Value |
|---------|-------|
| Section vertical padding | `py-16 md:py-32 lg:py-48` |
| Content max-width | `max-w-7xl` (1280px) |
| Hero max-width | `max-w-screen-2xl` |
| Card padding | `p-8 md:p-10` to `p-10 md:p-16` |
| Grid gap | `gap-4` to `gap-12` (contextual) |
| Content grid | `grid-cols-1 lg:grid-cols-12` (4+8 split) |

---

## Glass Morphism

```css
.glass-modern {
  background: rgba(5, 18, 5, 0.8);
  backdrop-filter: blur(12px) saturate(120%);
  border: 1px solid rgba(34, 197, 94, 0.12);
  box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.4),
              inset 0 1px 1px rgba(255, 255, 255, 0.05);
}
```
Used for: header (on scroll), footer, cards, lightbox controls, mobile drawer, modals.

---

## Noise Overlay

Inline SVG noise via `body::before` — no external image request:
```css
body::before {
  content: "";
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,...feTurbulence...");
  opacity: 0.03;
  pointer-events: none;
  z-index: 9999;
  contain: strict; /* limits paint cost */
}
```
The full SVG data URI is in `lib/utils.ts` as `NOISE_SVG_DATA_URI`.

---

## Custom Scrollbar

```css
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #010501; }
::-webkit-scrollbar-thumb {
  background: #1a2e1a;
  border-radius: 4px;
  border: 2px solid #010501;
}
::-webkit-scrollbar-thumb:hover { background: var(--color-green-prime); }
```

---

## CSS Custom Properties — Full List (globals.css)

### Easing & Duration
```css
--ease-stripe: cubic-bezier(0.19, 1, 0.22, 1);
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
--duration-fast: 200ms;
--duration-normal: 400ms;
--duration-slow: 700ms;
```

### Shadows
```css
--shadow-sm: /* standard small shadow */;
--shadow-md: /* standard medium shadow */;
--shadow-lg: /* standard large shadow */;
--shadow-franken: 0 0 40px -10px rgba(34, 197, 94, 0.2);
--shadow-glow: 0 0 20px rgba(34, 197, 94, 0.15);
--shadow-glow-lg: 0 0 40px rgba(34, 197, 94, 0.2);
```

### Letter Spacing
```css
--tracking-tightest: -0.04em;
--tracking-tighter: -0.02em;
--tracking-tight: -0.01em;
--tracking-normal: 0;
--tracking-wide: 0.025em;
--tracking-wider: 0.05em;
--tracking-widest: 0.1em;
```

---

## Utility CSS Classes

### `.kinetic-card`
```css
.kinetic-card {
  transition: all 400ms var(--ease-stripe);
}
.kinetic-card:hover {
  transform: translateY(-4px) scale(1.01);
  border-color: rgba(34, 197, 94, 0.3);
  box-shadow: var(--shadow-franken);
}
```

### `.text-animate-green`
Animated gradient text that cycles colors:
```css
.text-animate-green {
  background: linear-gradient(90deg, #4ade80, #bef264, #22c55e, #4ade80);
  background-size: 300% auto;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: textGradient 8s linear infinite;
}
```

### `.text-gradient-franken`
Static gradient text (no animation):
```css
.text-gradient-franken {
  background: linear-gradient(135deg, #4ade80, #bef264, #34d399);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### `.glow-green`
```css
.glow-green { box-shadow: 0 0 40px rgba(34, 197, 94, 0.15); }
```

### `.skip-link`
Accessibility skip-to-content link:
```css
.skip-link {
  position: absolute;
  /* hidden off-screen by default, appears on :focus */
  background: green;
}
```

---

## Keyframe Animations

### `textGradient`
Background-position shift from 0% to 300% center — creates flowing color effect.

### `float`
```css
@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0); }
  50% { transform: translateY(-10px) rotate(1.5deg); }
}
/* 6s ease-in-out infinite */
```

### `borderBeam`
```css
@keyframes borderBeam {
  from { top: -100%; left: -100%; }
  to { top: 100%; left: 100%; }
}
/* 4s linear infinite — compositor-thread, auto-pauses off-screen */
```

### Scanline (Anatomy Mode)
Repeating gradient creating horizontal scan lines for debug overlay.

---

## Selection & Focus

```css
::selection {
  background: rgba(34, 197, 94, 0.3);
}

:focus-visible {
  outline: 2px solid green;
  outline-offset: 4px;
}
```

---

## React-Tweet Theme Override

Complete color system remapping via `--tweet-*` CSS variables:
```css
.react-tweet-theme {
  --tweet-bg-color: transparent;
  --tweet-border: rgba(255, 255, 255, 0.08);
  --tweet-font-color: #f1f5f9;
  --tweet-font-color-secondary: #94a3b8;
  --tweet-color-blue-primary: #22c55e;     /* green instead of blue */
  --tweet-color-blue-secondary: #4ade80;
  --tweet-quoted-bg-color: transparent;
  --tweet-quoted-border: rgba(255, 255, 255, 0.08);
  --tweet-color-red-primary: #dc2626;       /* for quotes */
  --tweet-img-border-radius: 0.75rem;
}
```

---

## Highlight.js Franken Theme

All `.hljs-*` classes mapped to the green palette:
```css
.hljs-keyword, .hljs-selector-tag { color: #4ade80; font-weight: 800; }
.hljs-string, .hljs-doctag        { color: #a3e635; }
.hljs-number, .hljs-type          { color: #fbbf24; }
.hljs-title, .hljs-section        { color: #4ade80; font-weight: 900; }
.hljs-name, .hljs-addition        { color: #bef264; }
.hljs-comment                     { color: #475569; font-style: italic; }
.hljs-attr, .hljs-attribute       { color: #34d399; }
.hljs-deletion                    { color: #f87171; }
```

---

## Spectral Background Layers

`SpectralBackground` component adds film-grain analog feel:

1. **Film Grain**: SVG `feTurbulence` with animated `baseFrequency` (0.65→0.68), opacity 0.04, mix-blend-mode: overlay
2. **Vertical Scanlines**: Linear gradient at 90deg, opacity pulse [0.05, 0.08], 4s duration
3. **Horizontal Interference**: 1px line, blur, Y motion -10vh→110vh over 8s, 2s delay
4. **Light Leaks**: Two blobs (green top-left, blue bottom-right) with pulse opacity

---

## Scanline Overlay Pattern

Used on video players, hero video, spec-evolution-lab:
```css
background-image: linear-gradient(
  rgba(0, 0, 0, 0) 50%,
  rgba(0, 0, 0, 0.1) 50%
);
background-size: 100% 4px;
opacity: 0.3;
pointer-events: none;
```

---

## Dark Mode

Always-on: `<html class="dark">`. No light mode toggle.
Theme color in viewport meta: `#020a02`.

---

## Performance Considerations

1. Noise overlay uses `contain: strict` to limit repaint cost
2. Glass morphism `backdrop-filter` is GPU-accelerated but expensive — use sparingly on mobile
3. Font display: swap for both fonts prevents FOIT
4. Easing functions use compositor-friendly cubic-bezier curves
5. Custom scrollbar styles are webkit-only (Firefox falls back to default)
6. `will-change: auto` on noise overlay (not `will-change: transform` to avoid memory waste)
7. `content-visibility: auto` on long lists for deferred rendering
8. `transform: translateZ(0)` for GPU layer promotion in glitch component
9. `backfaceVisibility: "hidden"` in motion.div for smoother animations
10. Passive event listeners: `{ passive: true }` for all scroll/mousemove handlers
