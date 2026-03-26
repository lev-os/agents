# Adapting for a New FrankenSuite Project

> Step-by-step guide to create a website for any FrankenSuite project,
> using frankentui.com as the reference implementation.

---

## Phase 1: Scaffold

```bash
bunx create-next-app@latest <project>-website --ts --tailwind --app --src-dir=false
cd <project>-website

# Core dependencies
bun add framer-motion lucide-react clsx tailwind-merge

# Optional (add as needed)
bun add highlight.js marked dompurify react-tweet
```

### package.json — Enforce BUN
```json
{
  "engines": { "bun": ">=1.0.0" },
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "lint": "next lint"
  }
}
```

---

## Phase 2: Copy Design System

### From frankentui_website, copy:
```
app/globals.css          → Full CSS vars, glass-modern, noise overlay, scrollbar
lib/utils.ts             → cn(), NOISE_SVG_DATA_URI, formatDate helpers
lib/site-state.tsx       → SiteProvider (anatomy, terminal, audio context)
hooks/                   → use-body-scroll-lock, use-intersection-observer, use-haptic-feedback
```

### app/layout.tsx — Set up fonts
```tsx
import { Inter, JetBrains_Mono } from "next/font/google";

const inter = Inter({ variable: "--font-inter", subsets: ["latin"], display: "swap" });
const jetbrainsMono = JetBrains_Mono({ variable: "--font-jetbrains", subsets: ["latin"], display: "swap" });

// html: className="dark"
// body: className={`${inter.variable} ${jetbrainsMono.variable} font-sans antialiased`}
```

### next.config.ts — Standard settings
```ts
const nextConfig: NextConfig = {
  images: { formats: ["image/webp"] },
  compress: true,
  poweredByHeader: false,
  reactStrictMode: true,
};
```

---

## Phase 3: Copy Shared Components

### Required (brand consistency):
```
components/franken-elements.tsx   → FrankenBolt, FrankenStitch, FrankenContainer, NeuralPulse
components/franken-glitch.tsx     → FrankenGlitch
components/motion-wrapper.tsx     → Magnetic, BorderBeam, Portal
components/section-shell.tsx      → SectionShell layout primitive
components/client-shell.tsx       → ClientShell (app wrapper)
components/site-header.tsx        → Desktop pill + mobile bottom nav
components/site-footer.tsx        → Glassmorphic footer
components/custom-cursor.tsx      → Desktop cursor system
```

### Optional (copy if the project needs them):
```
components/franken-eye.tsx          → Mouse-tracking eye (hero element)
components/stats-grid.tsx           → Animated number counters
components/animated-number.tsx      → easeOutExpo counter animation
components/screenshot-gallery.tsx   → Lightbox gallery with spring slides
components/rust-code-block.tsx      → Syntax-highlighted code blocks
components/tweet-wall.tsx           → Social proof wall
components/glow-orbits.tsx          → Parallax background orbs (Web Animation API)
components/terminal-demo.tsx        → Typing animation terminal
components/decoding-text.tsx        → Character-reveal text animation
components/spectral-background.tsx  → Film grain + scanlines + light leaks
components/video-player.tsx         → Video with play overlay + scanlines
components/comparison-table.tsx     → Framework comparison with ✓/✗/⚠
components/timeline.tsx             → Vertical timeline with animated nodes
components/error-boundary.tsx       → Kernel_Panic styled error UI
components/motion/index.tsx         → Spring presets + reusable variants
components/motion/magnetic.tsx      → Magnetic cursor attraction
```

### Also copy from lib/:
```
lib/lru-cache.ts                    → Generic LRU cache (if using spec-evolution-lab)
lib/wasm-loader.ts                  → WASM singleton loader (if using WASM demos)
```

---

## Phase 4: Create Content

### lib/content.ts — Central data file

Every project needs at minimum:
```ts
// Site identity
export const siteConfig = {
  name: "FrankenXYZ",
  title: "FrankenXYZ — One-line description",
  description: "SEO description...",
  url: "https://frankenxyz.com",
  github: "https://github.com/user/frankenxyz",
};

// Navigation
export const navItems = [
  { href: "/", label: "Home" },
  { href: "/showcase", label: "Showcase" },
  { href: "/architecture", label: "Architecture" },
  { href: "/getting-started", label: "Get Started" },
];

// Hero stats
export const heroStats = [
  { label: "Lines of Code", value: "50K+", helper: "Pure Rust" },
  { label: "Build Time", value: "<2s", helper: "Release mode" },
];

// Feature grid
export const features = [
  { title: "Feature Name", description: "...", icon: "zap" },
  // ...
];

// Screenshots
export const screenshots = [
  { src: "/screenshots/demo.webp", alt: "Demo", caption: "..." },
];
```

**Rule**: ALL content in this one file. Types co-located. Never create separate data files.

---

## Phase 5: Customize Theme

### Change accent color (if not green)
The default accent is green (#22c55e). To change:

1. **globals.css** — Update CSS custom properties:
   ```css
   --color-green-prime: #3b82f6;  /* e.g., blue */
   --color-green-glow: #60a5fa;
   ```

2. **globals.css** — Update glass-modern border:
   ```css
   border: 1px solid rgba(59, 130, 246, 0.12);  /* match accent */
   ```

3. **globals.css** — Update scrollbar hover color

4. **Component defaults** — Search-and-replace accent references:
   - `green-400` → `blue-400`
   - `green-500` → `blue-500`
   - `green-500/10` → `blue-500/10`
   - `#22c55e` → `#3b82f6`

5. **FrankenBolt/NeuralPulse** — Update default `color` prop values

---

## Phase 6: Build Pages

### Minimum page set:
| Page | Purpose | Key sections |
|------|---------|-------------|
| `/` (homepage) | Overview + CTA | Hero, Features, Screenshots, Code, Get Started |
| `/showcase` | Visual gallery | Screenshot gallery with lightbox |
| `/architecture` | Technical depth | SectionShell sections for each subsystem |
| `/getting-started` | Onboarding | Installation, configuration, first steps |

### Optional pages (add as relevant):
| Page | When to include |
|------|----------------|
| `/glossary` | Project has domain-specific terminology |
| `/how-it-was-built` | Project has an interesting build story |
| `/beads` | Project uses beads for task tracking |

### Homepage structure (follow this order):
```
1. Hero — Big title, subtitle, CTA buttons, stats grid, optional video/eye
2. Features — SectionShell + FeatureCard grid
3. Screenshots — Gallery section
4. Code Example — RustCodeBlock or similar
5. Comparison — Table vs alternatives (optional)
6. Timeline — Changelog/milestones (optional)
7. Social Proof — Tweet wall (optional)
8. Get Started CTA — Final conversion section
9. Author/Credit — Footer section
```

---

## Phase 7: Mobile Navigation

### Update site-header.tsx:
1. **navItems**: Ensure the first 5 items work as bottom tab icons
2. **getIcon()**: Map each nav label to a lucide icon
3. **shortLabel**: Map labels to abbreviated versions for mobile
4. **Drawer**: Full nav list in slide-out menu

```tsx
const shortLabel: Record<string, string> = {
  "Home": "Home",
  "Showcase": "Show",
  "Architecture": "Arch.",
  "Get Started": "Start",
};
```

---

## Phase 8: OG Image & Metadata

### OG Image (`app/opengraph-image.tsx`)
```tsx
import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "FrankenXYZ";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    <div style={{ display: "flex", /* ... */ }}>
      {/* Grid pattern + vignette + screenshot bg at 0.1 opacity */}
      {/* Corner bolts + dashed stitches */}
      {/* Logo + title + description */}
      {/* Stats footer */}
      {/* HUD labels */}
    </div>,
    { ...size }
  );
}
```

**Satori constraints (CRITICAL)**:
- PNG only — WebP causes "TypeError: u2 is not iterable"
- No `<br />` tags — use separate `<span>` elements
- No `borderRadius: "full"` — use `"9999px"` instead
- Every element MUST have `display: "flex"`
- Base64-encode background images as data URIs
- Pre-convert WebP → PNG with sharp if needed

### Per-Page Metadata
```tsx
export const metadata: Metadata = {
  title: "Page Title",                    // Uses template from layout
  description: "SEO description for page",
};
```

### Root Metadata Template
```tsx
title: { default: siteConfig.title, template: `%s | ${siteConfig.name}` },
openGraph: { title, description, url, locale: "en_US", type: "website" },
twitter: { card: "summary_large_image" },
robots: { index: true, follow: true },
icons: { icon: "/favicon.ico", apple: "/apple-icon.png" },
viewport: { themeColor: "#020a02" },
```

---

## Phase 9: Special Features (Choose Which to Include)

| Feature | Required? | Description |
|---------|-----------|-------------|
| Anatomy Mode | Recommended | Debug wireframe overlay (Ctrl+Shift+X) |
| Site Terminal | Optional | Backtick toggles terminal overlay |
| Audio SFX | Optional | Web Audio API oscillator sounds |
| Custom Cursor | Recommended | Desktop-only cursor system with data attributes |
| Signal HUD | Optional | Diagnostic overlay |

### Data Attributes to Add
When building pages, add these attributes to relevant elements:
```html
<div data-technical="true">    <!-- code/technical areas: shows data debris -->
<section data-flashlight="true"> <!-- atmospheric sections: enables vignette -->
<button data-magnetic="true">  <!-- buttons/links: attracts cursor -->
<a data-cursor="pointer">      <!-- clickables: shows crosshair -->
```

---

## Phase 10: Deploy

```bash
# Build and validate
bun run build
bun tsc --noEmit
bun lint

# Deploy to Vercel
vercel deploy --prod

# DNS: Add A record → 76.76.21.21 on Cloudflare
# Add domain in Vercel dashboard
```

---

## Checklist

### Infrastructure
- [ ] BUN enforced in package.json engines
- [ ] Inter + JetBrains Mono fonts loaded with `display: "swap"`
- [ ] Font feature settings: `"cv02", "cv03", "cv04", "cv11"`
- [ ] PostCSS: only `@tailwindcss/postcss` (no tailwind.config)
- [ ] TypeScript strict mode, bundler resolution, `@/*` path alias
- [ ] `<html class="dark">` — always-on dark mode

### Design System
- [ ] CSS custom properties in globals.css match reference
- [ ] Glass-modern class renders correctly
- [ ] Noise overlay visible at 3% opacity
- [ ] Custom scrollbar themed
- [ ] Selection color is green

### Components
- [ ] FrankenBolt/Stitch/Container render correctly
- [ ] SectionShell icons: all string keys in sectionIcons map
- [ ] ErrorBoundary wraps ClientShell
- [ ] Portal component used for modals/lightboxes

### Navigation
- [ ] Mobile bottom nav works with 5 items + MORE
- [ ] Desktop pill nav shows glass-modern on scroll
- [ ] Active link indicator animated via `layoutId`
- [ ] Mobile drawer has body scroll lock
- [ ] Short labels mapped for mobile nav items

### Content & SEO
- [ ] All content in lib/content.ts (no separate data files)
- [ ] OG image generates correctly (PNG, no WebP)
- [ ] Root metadata with title template
- [ ] Per-page metadata with title + description
- [ ] Favicon and apple-icon in public/

### Responsive
- [ ] 1→2→3 column grids at sm/lg breakpoints
- [ ] Hero text uses fluid clamp()
- [ ] Custom cursor: visible desktop, hidden mobile
- [ ] FrankenEye hidden on mobile, visible lg+
- [ ] Code blocks horizontal scroll on mobile

### Accessibility
- [ ] Skip link present
- [ ] Reduced motion respected in ALL animations
- [ ] Focus visible: green outline
- [ ] Dialog/modal roles with aria attributes
- [ ] aria-hidden on decorative SVGs
- [ ] Proper heading hierarchy

### Performance
- [ ] Passive event listeners on scroll/mouse handlers
- [ ] RAF batching for cursor/scroll
- [ ] IntersectionObserver for lazy animations
- [ ] `loading="lazy"` on below-fold images
- [ ] `contain: strict` on noise overlay

### Build & Deploy
- [ ] `bun run build` — zero errors
- [ ] `bun tsc --noEmit` — zero type errors
- [ ] `bun lint` — zero warnings
- [ ] Vercel deployment successful
- [ ] Domain DNS configured
