# Aesthetic DNA — Visual Physics for Premium Visualizations

> **Purpose:** A generative visual design system — not a static token list. Given ONE accent color, derive the complete aesthetic: dark canvas, glass surfaces, shadows, glows, typography, containers, and kinetic effects. Every recipe extracted from production code across all 4 sites.

<!-- TOC: Dark Canvas | Material System | Luminance Hierarchy | Elevation System | Typography Physics | Color Derivation | Kinetic Surfaces | Texture Library | Container Grammar | The Premium Test | Worked Example -->

---

## 1. The Dark Canvas

Every visualization sits on a layered dark canvas. The base is never pure black — it carries an undertone of the accent color.

### Base Color Derivation

| Site | Accent | Base BG | Surface | Pattern |
|------|--------|---------|---------|---------|
| Jeffrey Emanuel | Cyan `#38bdf8` | `#020617` | `#0f172a` | `#02` + blue undertone |
| FrankenSQLite | Teal `#14b8a6` | `#020a05` | `#051210` | `#02` + green undertone |
| FrankenTUI | Green `#22c55e` | `#020a02` | `#051205` | `#02` + green undertone |
| Asupersync | Blue `#3B82F6` | `#020a14` | `#0A1628` | `#02` + blue undertone |

**Rule:** Base is always `#02XXYY` where XX/YY carry a hint of the accent hue at near-zero saturation. Surface is ~2-3 steps lighter in the same hue family.

### The Background Stack (3 Layers)

```css
/* Layer 1: Base color on body */
body {
  background-color: var(--color-bg); /* e.g. #020a05 */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Layer 2: Ambient radial gradients (optional — adds colored atmosphere) */
body::after {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -2;
  pointer-events: none;
  background:
    radial-gradient(circle at 15% 15%, rgba(ACCENT_1, 0.04), transparent 45%),
    radial-gradient(circle at 85% 25%, rgba(ACCENT_2, 0.04), transparent 45%),
    linear-gradient(to bottom, var(--color-bg), var(--color-bg-deep));
}

/* Layer 3: Noise texture (adds sophistication) */
body::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: 9999;
  pointer-events: none;
  contain: strict;
  opacity: 0.03;
  background-image: url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20width%3D%27120%27%20height%3D%27120%27%3E%3Cfilter%20id%3D%27n%27%3E%3CfeTurbulence%20type%3D%27fractalNoise%27%20baseFrequency%3D%270.85%27%20numOctaves%3D%272%27%20stitchTiles%3D%27stitch%27%20seed%3D%272%27/%3E%3C/filter%3E%3Crect%20width%3D%27120%27%20height%3D%27120%27%20filter%3D%27url(%23n)%27/%3E%3C/svg%3E");
}
```

**Key values:**
- Noise: `baseFrequency='0.85'`, `numOctaves='2'`, opacity `0.03`, z-index `9999`
- Radial accents: `0.04` opacity, `45%` spread, positioned at corners (15%/15%, 85%/25%)
- Linear gradient: subtle darkening from top to bottom

---

## 2. Material System

Four materials, each with a specific recipe. Choose by context.

### Glass (Interactive Cards, Panels)

The primary surface material. Used for any container the user interacts with.

```css
.glass-modern {
  background: rgba(SURFACE, 0.8);
  backdrop-filter: blur(12px) saturate(120%);
  -webkit-backdrop-filter: blur(12px) saturate(120%);
  border: 1px solid rgba(ACCENT, 0.12);
  box-shadow:
    0 4px 24px -1px rgba(0, 0, 0, 0.4),
    inset 0 1px 1px rgba(255, 255, 255, 0.05);
}
```

| Property | Value | Why |
|----------|-------|-----|
| Background opacity | `0.8` | Enough to read text, transparent enough to show depth |
| Blur | `12px` | Crisp enough to see shapes, blurry enough to feel glass |
| Saturate | `120%` | Compensates for blur washing out colors |
| Border | accent at `0.12` | Barely visible, defines edges without harshness |
| Inset highlight | white at `0.05` | Simulates light catching the top edge |
| Drop shadow | black at `0.4` | Grounds the card in space |

**Blur scale:** `8px` (subtle) → `12px` (standard) → `16px` (panels) → `24px` (HD/hero)

**Opacity tiers:**
- Minimal: `0.3` — overlay panels, barely-there surfaces
- Standard: `0.8` — interactive cards, primary containers
- Maximum: `0.9` — sticky headers, must-read content

### Metal (Navigation, Toolbars)

Solid, grounding surfaces. No blur, higher opacity, stronger borders.

```css
.metal {
  background: var(--color-surface);
  border: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: 0 2px 8px -2px rgba(0, 0, 0, 0.4),
              0 0 0 1px rgba(255, 255, 255, 0.04);
}
```

### Glow (Active/Selected States)

Emissive material — the element itself becomes a light source.

```css
.glow {
  background: rgba(ACCENT, 0.08);
  border: 1px solid rgba(ACCENT, 0.3);
  box-shadow: 0 0 40px -10px rgba(ACCENT, 0.2);
}
```

### Paper (Content, Readability)

Maximum contrast for long-form text. Minimal decoration.

```css
.paper {
  background: var(--color-bg);
  border: 1px solid rgba(255, 255, 255, 0.05);
}
```

---

## 3. Luminance Hierarchy

A page has a "lighting model" — consistent light direction creates spatial coherence.

### The Three Light Sources

1. **Primary (Hero):** The brightest element on the page. Usually a gradient headline or key visualization. Draws the eye first.
2. **Secondary (Interactive):** Elements that glow on interaction — buttons, cards, active states. They "emit" accent-colored light via box-shadow.
3. **Ambient (Background):** The noise texture and radial gradients. Barely visible but prevents flat, dead backgrounds.

### Rules

- **Light travels downward:** Top elements are brighter. Hero sections use full-opacity gradients; footer sections use muted colors.
- **Interactive elements emit:** Hover/active states add glow shadows, not just color changes. The element becomes a light source.
- **Background absorbs:** The dark canvas absorbs light — it's never a competing element.
- **One hero per viewport:** Only one element at maximum brightness in any scroll position. Multiple bright elements compete and create visual noise.

---

## 4. Elevation System

Multi-layer shadows with accent-colored glows at higher elevations.

### The 4-Tier Stack

```css
/* Level 0: Flush — resting state */
--elevation-0: 0 1px 2px rgba(0,0,0,0.3),
               0 0 0 1px rgba(0,0,0,0.2);

/* Level 1: Raised — cards, panels */
--elevation-1: 0 2px 8px -2px rgba(0,0,0,0.4),
               0 0 0 1px rgba(255,255,255,0.04);

/* Level 2: Floating — hover states, dropdowns */
--elevation-2: 0 12px 32px -8px rgba(0,0,0,0.5),
               0 4px 12px -4px rgba(ACCENT, 0.08),
               0 0 0 1px rgba(255,255,255,0.06);

/* Level 3: Overlay — modals, popovers */
--elevation-3: 0 24px 48px -12px rgba(0,0,0,0.6),
               0 8px 24px -8px rgba(ACCENT, 0.12),
               0 0 0 1px rgba(255,255,255,0.08);
```

**Pattern:** Each level adds:
- Larger dark shadow spread (2px → 8px → 32px → 48px)
- Accent glow appears at level 2+ (0.08 → 0.12 opacity)
- White ring border brightens (0.04 → 0.06 → 0.08)

### Brand Glow Shadow

Every site has a large-area glow shadow using its accent color:

```css
--shadow-brand: 0 0 40px -10px rgba(ACCENT, 0.2);
```

Used on: hero containers, featured cards, primary CTAs.

---

## 5. Typography Physics

Larger text = tighter tracking = bolder weight. This creates visual density that reads as "premium."

### Fluid Type Scale

```css
--type-hero:    clamp(2.5rem, 8vw, 6rem);     /* 40px → 96px */
--type-h1:      clamp(2rem, 5vw, 3.75rem);    /* 32px → 60px */
--type-h2:      clamp(1.5rem, 4vw, 2.5rem);   /* 24px → 40px */
--type-h3:      clamp(1.25rem, 3vw, 1.875rem); /* 20px → 30px */
--type-h4:      clamp(1.125rem, 2vw, 1.5rem); /* 18px → 24px */
--type-body-lg: clamp(1rem, 1.5vw, 1.25rem);  /* 16px → 20px */
--type-body:    1rem;                           /* 16px */
--type-body-sm: 0.875rem;                       /* 14px */
--type-caption: 0.75rem;                        /* 12px */
```

### Weight × Tracking Relationships

| Size | Weight | Tracking | Leading |
|------|--------|----------|---------|
| Hero / H1 | `900` (black) | `-0.04em` | `1.1` |
| H2 / H3 | `800` (extrabold) | `-0.02em` | `1.2` |
| H4 / Body-lg | `600` (semibold) | `-0.01em` | `1.375` |
| Body | `400` (regular) | `0em` | `1.5-1.6` |
| Caption | `500` (medium) | `0.025em` | `1.5` |
| Code/mono | `400` | `0em` | `1.6` |

**Rule:** As text gets larger, tracking gets tighter and weight gets heavier. This prevents large text from looking loose and airy.

### Font Stacks

```css
--font-sans: "Inter", var(--font-inter), ui-sans-serif, system-ui, sans-serif;
--font-mono: "JetBrains Mono", var(--font-jetbrains), ui-monospace, monospace;
```

**Usage:** Sans for all narrative text. Mono for code, data values, technical labels, step counters.

### Font Smoothing (Required)

```css
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

Without this, text looks fuzzy on dark backgrounds.

---

## 6. Color Derivation Engine

Given ONE accent color, derive every color you need.

### The Opacity Ladder

From a single accent color (e.g., `#14b8a6` teal), derive by opacity:

| Purpose | Opacity | Example (Teal) | Tailwind |
|---------|---------|-----------------|----------|
| Background tint | `0.04` | `rgba(20,184,166, 0.04)` | `bg-teal-500/[0.04]` |
| Code background | `0.08` | `rgba(20,184,166, 0.08)` | `bg-teal-500/[0.08]` |
| Border (rest) | `0.1-0.12` | `rgba(20,184,166, 0.12)` | `border-teal-500/[0.12]` |
| Code border | `0.15` | `rgba(20,184,166, 0.15)` | `border-teal-500/15` |
| Shadow glow | `0.2` | `rgba(20,184,166, 0.2)` | shadow custom |
| Border (hover) | `0.3` | `rgba(20,184,166, 0.3)` | `border-teal-500/30` |
| Selection bg | `0.3` | `rgba(20,184,166, 0.3)` | `selection:bg-teal-500/30` |
| Text (muted) | `0.4` | `rgba(20,184,166, 0.4)` | `text-teal-500/40` |
| Drop-shadow (hover) | `0.5` | `rgba(20,184,166, 0.5)` | filter custom |
| Glow (small element) | `0.6-0.8` | `rgba(20,184,166, 0.8)` | shadow custom |
| Text (full) | `1.0` | `#14b8a6` | `text-teal-500` |

### Three-Color Gradient System

Each site uses 3 related colors for gradients:

| Site | Light | Mid | Dark |
|------|-------|-----|------|
| Jeffrey Emanuel | `#38bdf8` (sky) | `#a78bfa` (violet) | `#34d399` (emerald) |
| FrankenSQLite | `#5eead4` (light teal) | `#2dd4bf` (teal) | `#14b8a6` (dark teal) |
| FrankenTUI | `#bef264` (lime) | `#4ade80` (green) | `#22c55e` (dark green) |
| Asupersync | `#60A5FA` (light blue) | `#3B82F6` (blue) | `#F97316` (orange contrast) |

**Static gradient:** `linear-gradient(135deg, LIGHT 0%, MID 50%, DARK 100%)`
**Animated gradient:** `linear-gradient(to right, MID, LIGHT, DARK, MID)` with `background-size: 300% auto`

### CSS Custom Properties Template

```css
:root {
  --color-bg: #020a05;
  --color-surface: #051210;
  --color-border: rgba(ACCENT, 0.1);
  --color-prime: #14b8a6;
  --color-glow: #2dd4bf;
  --color-light: #5eead4;
}
```

### Semantic Colors (Unchanged)

These are invariant across all sites — never change them:

| Meaning | Color | Hex |
|---------|-------|-----|
| Success | Emerald | `#10b981` |
| Error | Red | `#ef4444` |
| Warning | Amber | `#f59e0b` |
| Active/info | Cyan | `#06b6d4` |
| Info | Sky | `#0ea5e9` |
| Accent | Violet | `#8b5cf6` |
| Muted | Slate | `#64748b` |

---

## 7. Kinetic Surfaces

How surfaces respond to interaction. Every interactive element has a kinetic response.

### The Stripe Easing Curve

```css
--ease-stripe: cubic-bezier(0.19, 1, 0.22, 1);
```

This is THE shared timing function across all 4 production sites. Used for all hover transitions, card lifts, and state changes. It's snappy with a smooth deceleration — the "Stripe feel."

### Duration Scale

```css
--duration-fast: 200ms;    /* Micro-interactions, toggles */
--duration-normal: 400ms;  /* Card hovers, state transitions */
--duration-slow: 700ms;    /* Page transitions, reveals */
```

### Kinetic Card (Copy-Paste)

The universal hover pattern for interactive cards:

```css
.kinetic-card {
  transition: all var(--duration-normal) var(--ease-stripe);
}
.kinetic-card:hover {
  transform: translateY(-4px) scale(1.01);
  border-color: rgba(ACCENT, 0.3);
  box-shadow: var(--shadow-brand); /* 0 0 40px -10px rgba(ACCENT, 0.2) */
}
```

**The effect stack:**
1. **Lift:** `translateY(-4px)` — subtle upward motion
2. **Scale:** `scale(1.01)` — barely perceptible zoom
3. **Border brightens:** accent from `0.12` → `0.3` opacity
4. **Glow activates:** brand shadow appears

### Mouse-Tracked Radial Spotlight

For feature cards that follow the cursor:

```tsx
const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

<div
  onMouseMove={(e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setMousePos({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  }}
  style={{
    background: `radial-gradient(600px circle at ${mousePos.x}px ${mousePos.y}px, rgba(ACCENT, 0.06), transparent 80%)`
  }}
/>
```

### Border Beam Sweep

Diagonal light sweep across card edges:

```css
@keyframes borderBeam {
  0% { top: -100%; left: -100%; }
  100% { top: 100%; left: 100%; }
}

/* Apply via pseudo-element or absolute div inside overflow-hidden container: */
.border-beam {
  background: conic-gradient(from 0deg, transparent 0deg, rgba(ACCENT, 0.1) 180deg, transparent 360deg);
  animation: borderBeam 4s linear infinite;
}
```

### Top-Border Reveal

Animated line that scales in on hover:

```html
<div class="absolute inset-x-0 top-0 h-px origin-center scale-x-0
            bg-gradient-to-r from-ACCENT via-ACCENT to-ACCENT
            transition-transform group-hover:scale-x-100" />
```

### Glow Effects

| Size | Box-shadow | Use for |
|------|------------|---------|
| Small (dots, icons) | `0 0 8px rgba(ACCENT, 0.8)` | Status dots, small indicators |
| Medium (text, buttons) | `0 0 15-20px rgba(ACCENT, 0.5)` | Hover text, button glow |
| Large (cards, areas) | `0 0 40px -10px rgba(ACCENT, 0.2)` | Featured cards, hero sections |
| Extra large (hero) | `0 0 60px rgba(ACCENT, 0.3)` | Primary CTA, lightbox images |

**Filter alternative** (for SVG/text):
```css
filter: drop-shadow(0 0 8px rgba(ACCENT, 0.6));
```

### Pulse Ring

```css
@keyframes pulse-gentle {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
.pulse-gentle { animation: pulse-gentle 2s ease-in-out infinite; }
```

### Float Animation

```css
@keyframes float {
  0%   { transform: translateY(0px) rotate(0deg); }
  50%  { transform: translateY(-10px) rotate(1.5deg); }
  100% { transform: translateY(0px) rotate(0deg); }
}
.animate-float { animation: float 6s ease-in-out infinite; }
```

### Focus & Selection States

```css
/* Focus: accent-colored outline */
:focus-visible {
  outline: 2px solid var(--color-prime);
  outline-offset: 4px;
}

/* Selection: accent tint */
::selection {
  background: rgba(ACCENT, 0.3);
  color: #fff;
}
```

---

## 8. Texture Library

### SVG Fractal Noise (Copy-Paste)

Applied as `body::before`. Creates subtle grain that adds sophistication.

```css
body::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: 9999;
  pointer-events: none;
  contain: strict;
  opacity: 0.03;
  background-image: url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20width%3D%27120%27%20height%3D%27120%27%3E%3Cfilter%20id%3D%27n%27%3E%3CfeTurbulence%20type%3D%27fractalNoise%27%20baseFrequency%3D%270.85%27%20numOctaves%3D%272%27%20stitchTiles%3D%27stitch%27%20seed%3D%272%27/%3E%3C/filter%3E%3Crect%20width%3D%27120%27%20height%3D%27120%27%20filter%3D%27url(%23n)%27/%3E%3C/svg%3E");
}
```

**Parameters:** `baseFrequency='0.85'` (fine grain), `numOctaves='2'` (moderate complexity), opacity `0.03` (barely visible).

### Dot Grid

Technical-feeling grid pattern for visualization containers:

```tsx
<div style={{
  backgroundImage: `radial-gradient(circle at 1px 1px, rgba(ACCENT, 0.15) 1px, transparent 0)`,
  backgroundSize: '40px 40px',
}} />
```

### Stitch Grid (SVG Pattern)

Cross-hatch pattern used on Franken-branded containers:

```tsx
<div style={{
  backgroundImage: `url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h40v40H0z' fill='none'/%3E%3Cpath d='M10 0v5M10 15v10M10 35v5M30 0v5M30 15v10M30 35v5M0 10h5M15 10h10M35 10h5M0 30h5M15 30h10M35 30h5' stroke='%23ffffff' stroke-width='1'/%3E%3C/svg%3E")`,
  backgroundSize: '80px 80px',
  opacity: 0.05,
}} />
```

---

## 9. Container Grammar

### Border-Radius Scale

| Element | Radius | Tailwind |
|---------|--------|----------|
| Small buttons, badges | `6px` | `rounded-md` |
| Inputs, small cards | `8px` | `rounded-lg` |
| Code blocks, inner panels | `12px` | `rounded-xl` |
| Cards, icon containers | `16-24px` | `rounded-xl` to `rounded-2xl` |
| Feature cards, sections | `32px` | `rounded-[2rem]` |
| Pills, tags | `9999px` | `rounded-full` |

**Rule:** Larger containers get larger radii. Inner containers use smaller radii than their parent.

### Padding Scale

| Container | Padding | Tailwind |
|-----------|---------|----------|
| Inline code | `0.15em 0.4em` | custom |
| Badges, tags | `4px 12px` | `px-3 py-1` |
| Code block content | `1.25rem 1.5rem` | `p-5 px-6` |
| Cards (mobile) | `32px` | `p-8` |
| Cards (desktop) | `40px` | `md:p-10` |
| Section vertical | `clamp(4rem, 10vw, 7rem)` | custom |

### Container Recipes

**Card:**
```css
.card {
  background: rgba(SURFACE, 0.8);
  backdrop-filter: blur(12px) saturate(120%);
  border: 1px solid rgba(ACCENT, 0.12);
  border-radius: 2rem;
  padding: 2rem;
  box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.4),
              inset 0 1px 1px rgba(255, 255, 255, 0.05);
}
```

**Code Block:**
```css
.code-block {
  background: rgba(BG, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}
.code-block-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.02);
}
.code-block-content {
  padding: 2rem;
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.6;
}
```

**Tooltip:**
```css
.tooltip {
  background: var(--color-surface);
  border: 1px solid rgba(ACCENT, 0.15);
  border-radius: 0.75rem;
  padding: 0.5rem 0.75rem;
  box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.5);
  font-size: 0.875rem;
}
```

**Inline Code:**
```css
code {
  background: rgba(ACCENT, 0.08);
  border: 1px solid rgba(ACCENT, 0.15);
  border-radius: 0.375rem;
  padding: 0.15em 0.4em;
  font-size: 0.85em;
  color: ACCENT_LIGHT; /* lighter variant of accent */
}
```

### Nesting Rule

Inner containers are more transparent than outer:
- Outer card: `rgba(SURFACE, 0.8)`
- Inner panel: `rgba(255, 255, 255, 0.02)`
- Inner panel hover: `rgba(255, 255, 255, 0.04)`

### Scrollbar Styling

```css
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: var(--color-bg); }
::-webkit-scrollbar-thumb {
  background: SURFACE_LIGHT;
  border: 2px solid var(--color-bg);
  border-radius: 10px;
  transition: background 0.3s;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--color-prime);
}
```

---

## 10. The Premium Test

Five checks that separate premium tech product from developer side project. Run before shipping any visualization.

### The 5 Checks

| # | Check | What to Look For | Pass |
|---|-------|------------------|------|
| 1 | **Noise texture** | Does the background have subtle grain? | `body::before` with fractal noise at ≤0.03 opacity |
| 2 | **Colored shadows** | Do elevated elements cast accent-tinted shadows? | Box-shadow includes `rgba(ACCENT, 0.08-0.12)` at levels 2+ |
| 3 | **Fluid typography** | Do headings use `clamp()` for smooth scaling? | No fixed `px` sizes on any heading |
| 4 | **Kinetic hover** | Do interactive cards lift + scale + glow on hover? | `translateY(-4px) scale(1.01)` + border brighten + shadow enhance |
| 5 | **Glass surfaces** | Do card backgrounds use `backdrop-filter: blur`? | At least one glass surface with `blur(12px) saturate(120%)` |

### Quick Self-Audit

```
□ Base background is NOT pure black (#000) — has accent undertone
□ Font smoothing is enabled (antialiased)
□ Inter for text, JetBrains Mono for code
□ Letter-spacing is negative on headings (-0.02em to -0.04em)
□ All transitions use Stripe easing, not linear/ease
□ Border colors use accent at 0.12 opacity, not white/gray
□ At least one element has a glow shadow
□ Selection color matches accent at 0.3 opacity
□ Focus-visible uses accent-colored 2px outline with 4px offset
□ Scrollbar thumb uses accent color on hover
```

---

## Worked Example: Deriving Full Aesthetic from Accent Color

**Given:** A new visualization site with accent color **Amber** `#f59e0b`.

### Step 1: Derive Base Colors

```css
--color-bg: #0a0802;      /* #0a + amber undertone (warm dark) */
--color-surface: #1a1408;  /* surface: warmer, slightly lighter */
--color-border: rgba(245, 158, 11, 0.1);
--color-prime: #f59e0b;
--color-glow: #fbbf24;     /* lighter amber for glow */
--color-light: #fde68a;    /* lightest amber */
```

### Step 2: Apply the Background Stack

```css
body { background-color: #0a0802; }

body::after {
  background:
    radial-gradient(circle at 15% 15%, rgba(245, 158, 11, 0.04), transparent 45%),
    radial-gradient(circle at 85% 25%, rgba(251, 191, 36, 0.04), transparent 45%),
    linear-gradient(to bottom, #0a0802, #060400);
}

body::before { /* noise — identical every time */ }
```

### Step 3: Apply Glass Material

```css
.glass-modern {
  background: rgba(26, 20, 8, 0.8);          /* surface at 0.8 */
  backdrop-filter: blur(12px) saturate(120%);
  border: 1px solid rgba(245, 158, 11, 0.12); /* accent at 0.12 */
  box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.4),
              inset 0 1px 1px rgba(255, 255, 255, 0.05);
}
```

### Step 4: Apply Kinetic Hover

```css
.kinetic-card {
  transition: all 400ms cubic-bezier(0.19, 1, 0.22, 1);
}
.kinetic-card:hover {
  transform: translateY(-4px) scale(1.01);
  border-color: rgba(245, 158, 11, 0.3);
  box-shadow: 0 0 40px -10px rgba(245, 158, 11, 0.2);
}
```

### Step 5: Apply Text Gradient

```css
.text-gradient-amber {
  background: linear-gradient(to right, #fbbf24, #fde68a, #f59e0b, #fbbf24);
  background-size: 300% auto;
  -webkit-background-clip: text;
  color: transparent;
  animation: textGradient 8s linear infinite;
}
```

### Step 6: Selection, Focus, Scrollbar

```css
::selection { background: rgba(245, 158, 11, 0.3); color: #fff; }
:focus-visible { outline: 2px solid #f59e0b; outline-offset: 4px; }
::-webkit-scrollbar-thumb:hover { background: #f59e0b; }
```

**Result:** A complete, cohesive amber-themed dark aesthetic that matches the premium quality of all 4 production sites, derived entirely from a single accent color.

---

## Quick Reference Card

| Need | Recipe |
|------|--------|
| Dark background | `#02XXYY` with accent undertone + noise at 0.03 |
| Glass card | `blur(12px) saturate(120%)` + accent border at 0.12 + inset white 0.05 |
| Shadow with glow | Standard shadow + `rgba(ACCENT, 0.08-0.12)` layer |
| Heading style | `font-weight: 900; letter-spacing: -0.04em; line-height: 1.1` |
| Hover effect | `translateY(-4px) scale(1.01)` on `cubic-bezier(0.19, 1, 0.22, 1)` 400ms |
| Border at rest | `1px solid rgba(ACCENT, 0.12)` |
| Border on hover | `1px solid rgba(ACCENT, 0.3)` |
| Small glow | `box-shadow: 0 0 8px rgba(ACCENT, 0.8)` |
| Large glow | `box-shadow: 0 0 40px -10px rgba(ACCENT, 0.2)` |
| Text gradient | 3-color linear + `background-size: 300% auto` + 8s animation |
| Noise texture | feTurbulence fractalNoise 0.85 freq, 2 octaves, 0.03 opacity |
| Code background | `rgba(ACCENT, 0.08)` bg + `rgba(ACCENT, 0.15)` border |
| Selection | `rgba(ACCENT, 0.3)` background, white text |
| Focus ring | `2px solid ACCENT`, `4px offset` |
