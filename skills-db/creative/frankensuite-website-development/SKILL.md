---
name: frankensuite-website-development
description: >-
  Build FrankenSuite project websites matching frankentui.com quality. Use when
  creating a new FrankenSuite website, adding pages/sections, or adapting the
  design system for a different project.
---

<!-- TOC: Brand | Quick Start | Architecture | Gotchas | Adaptation | References -->

# FrankenSuite Website Development

> **Reference implementation:** `/data/projects/frankentui_website` (frankentui.com)
> Read the source files AND [DESIGN-PHILOSOPHY.md](references/DESIGN-PHILOSOPHY.md) before building.

---

## Brand Essence

**"Laboratory of Beautiful Monsters"** — industrial horror meets Stripe-grade polish.

- Bolts = fasteners, Stitches = sutures, Glitches = electrical surges, Eye = the monster watching, Green = life force
- Every heading uses the **"One Green Word"** pattern: `"Get [Started]."` — green word is the most evocative, period makes it declarative
- **Micro-labels** (`text-[10px] font-black uppercase tracking-[0.3em]`) appear everywhere — eyebrows, status indicators, nav badges, stats. This is what makes it feel like an instrument dashboard, not a blog
- The site **breathes** through 4 atmospheric layers: GlowOrbits (background) → SpectralBackground noise/grain (atmosphere) → glass-modern cards (content) → custom cursor (interactive)
- Homepage is a **scroll narrative** — each section is a story chapter from "Here's what this is" (hero) through "Others love it" (tweets) to "The machine is alive" (footer)

Full philosophy, anti-patterns, visual language: [DESIGN-PHILOSOPHY.md](references/DESIGN-PHILOSOPHY.md)

---

## Quick Start

```bash
bunx create-next-app@latest <project>-website --ts --tailwind --app --src-dir=false
cd <project>-website
bun add framer-motion lucide-react clsx tailwind-merge highlight.js marked dompurify
```

Copy from `frankentui_website`:
```
# Required (brand consistency)
components/  franken-elements.tsx franken-glitch.tsx franken-eye.tsx
             motion-wrapper.tsx section-shell.tsx client-shell.tsx
             site-header.tsx site-footer.tsx custom-cursor.tsx
lib/         utils.ts site-state.tsx
hooks/       use-body-scroll-lock.ts use-intersection-observer.ts
app/         globals.css

# Optional (copy as needed)
components/  glow-orbits.tsx spectral-background.tsx terminal-demo.tsx
             screenshot-gallery.tsx rust-code-block.tsx comparison-table.tsx
             timeline.tsx tweet-wall.tsx video-player.tsx stats-grid.tsx
             animated-number.tsx decoding-text.tsx error-boundary.tsx
             motion/index.tsx motion/magnetic.tsx
```

Then: create `lib/content.ts` → update `app/layout.tsx` (Inter + JetBrains Mono) → build pages.

Full step-by-step: [ADAPTATION-GUIDE.md](references/ADAPTATION-GUIDE.md)

---

## Workflow

- [ ] Scaffold Next.js 16 + BUN
- [ ] Copy design system + shared components
- [ ] Create `lib/content.ts` (ALL content in this one file)
- [ ] Build homepage following scroll narrative order
- [ ] Build subpages: Showcase, Architecture, Getting Started (minimum)
- [ ] Verify mobile: bottom nav, responsive grids, touch interactions
- [ ] `bun run build && bun tsc --noEmit` — zero errors
- [ ] Deploy to Vercel

---

## Tech Stack

Next.js 16 (App Router, Turbopack) · React 19 · Tailwind CSS 4 (`@tailwindcss/postcss`, no tailwind.config) · Framer Motion 12 · lucide-react · Inter + JetBrains Mono via `next/font/google`

**BUN only** — never npm/yarn/pnpm. TypeScript strict, bundler resolution, `@/*` path alias.

---

## Architecture

```
RootLayout (server) → ClientShell ("use client" boundary)
  ├── SiteProvider (context: anatomy, terminal, audio)
  ├── SiteHeader (desktop pill nav + mobile bottom nav)
  ├── AnimatePresence page transitions
  │   └── {children}
  ├── SiteFooter
  └── CustomCursor (desktop only)
```

**SectionShell** — core layout primitive (4/8 col grid, sticky sidebar):
```tsx
<SectionShell id="features" icon="sparkles" eyebrow="Why" title="Built Different" kicker="...">
  {/* content */}
</SectionShell>
```

**Content centralization**: ALL data in `lib/content.ts` — `siteConfig`, `navItems`, `heroStats`, `features`, `screenshots`, `codeExample`, `comparisonData`, `changelog`, `tweets`. Types co-located. Never separate data files.

Component details: [COMPONENTS.md](references/COMPONENTS.md) · Motion system: [EXACT-VALUES.md](references/EXACT-VALUES.md)

---

## Key Design Patterns

| Pattern | Implementation | Details in |
|---------|---------------|------------|
| Glass morphism | `rgba(5,18,5,0.8)` + `blur(12px)` + green/12% border | [DESIGN-SYSTEM.md](references/DESIGN-SYSTEM.md) |
| Micro-labels | `text-[10px] font-black uppercase tracking-[0.3em]` | [DESIGN-PHILOSOPHY.md](references/DESIGN-PHILOSOPHY.md) |
| Viewport entry | `opacity:0,y:40` → `1,0`, ease `[0.19,1,0.22,1]` | [COMPONENTS.md](references/COMPONENTS.md) |
| Spring presets | smooth/snappy/gentle/quick | [COMPONENTS.md](references/COMPONENTS.md) |
| Custom cursor | `data-technical` / `data-flashlight` / `data-magnetic` / `data-cursor` | [COMPONENTS.md](references/COMPONENTS.md) |
| Desktop nav | Floating pill, transparent → glass-modern on scroll | [RESPONSIVE.md](references/RESPONSIVE.md) |
| Mobile nav | Bottom tab bar (not hamburger), slide-out drawer | [RESPONSIVE.md](references/RESPONSIVE.md) |
| CTAs | Primary `bg-green-500 rounded-2xl`, never `rounded-full` | [DESIGN-PHILOSOPHY.md](references/DESIGN-PHILOSOPHY.md) |
| Section spacing | `py-16 md:py-32 lg:py-48` — extreme breathing room | [DESIGN-PHILOSOPHY.md](references/DESIGN-PHILOSOPHY.md) |
| Hero formula | Eyebrow → big title (green word + period) → subtitle → CTAs → stats → FrankenEye | [DESIGN-PHILOSOPHY.md](references/DESIGN-PHILOSOPHY.md) |
| Decorative system | FrankenBolt/Stitch/Container/Glitch/Eye — shared brand chrome | [COMPONENTS.md](references/COMPONENTS.md) |
| OG images | Satori/next/og — PNG only, no `<br/>`, `display:"flex"` everywhere | [ADAPTATION-GUIDE.md](references/ADAPTATION-GUIDE.md) |

---

## Gotchas

1. **SectionShell icon**: String key, not component ref. Add to BOTH import AND `sectionIcons` map
2. **Server/Client boundary**: No `next/dynamic` with `ssr: false` in Server Components (Next.js 16). Import `"use client"` components directly
3. **React 19**: No ref writes during render. No synchronous setState in effects
4. **Satori (next/og)**: No WebP, no `<br />`, no `borderRadius: "full"` (use "9999px"). Pre-convert with sharp
5. **Linter auto-modifies**: Re-read files before editing — ESLint may have changed imports
6. **.next/cache**: `rm -r .next/cache` fixes phantom type errors
7. **BUN only**: `bun dev`, `bun run build`, `bun lint`, `bun tsc --noEmit`
8. **Content**: ALL data in `lib/content.ts` — never separate data files
9. **RustCodeBlock**: Uses `title` prop, NOT `filename`
10. **GlowOrbits**: Native Web Animation API — don't convert to Framer Motion
11. **Portal**: Fixed-position inside transform parents breaks — use Portal from motion-wrapper.tsx
12. **Body scroll lock**: Must compensate scrollbar width — use `useBodyScrollLock`
13. **Event listeners**: Always `{ passive: true }` for scroll/mouse. RAF batching for cursor.
14. **Font loading**: Both fonts need `display: "swap"` to prevent FOIT

---

## Adapting for a New Project

1. **Read [DESIGN-PHILOSOPHY.md](references/DESIGN-PHILOSOPHY.md) first** — absorb the aesthetic soul
2. **Fork structure, not code** — same tech stack, same visual language
3. **Replace content** — new `siteConfig`, `navItems`, `features`, etc.
4. **Swap accent color** — update `--color-green-prime` in CSS vars + component defaults
5. **Keep decorative system** — FrankenBolt/Stitch/Container/Glitch for brand unity
6. **Follow the scroll narrative** — homepage tells a story, each section is a chapter
7. **Maintain micro-labels** — every section needs the 10px uppercase eyebrow
8. **Preserve atmosphere** — GlowOrbits + noise + glass-modern + breathing space
9. **Test the "alive" feeling** — if the page feels static, something is missing

Full 10-phase guide + checklist: [ADAPTATION-GUIDE.md](references/ADAPTATION-GUIDE.md)

---

## References

| I need to... | Read |
|--------------|------|
| Understand the brand, visual language, anti-patterns | [DESIGN-PHILOSOPHY.md](references/DESIGN-PHILOSOPHY.md) |
| Look up CSS vars, glass-modern, typography, utility classes | [DESIGN-SYSTEM.md](references/DESIGN-SYSTEM.md) |
| Understand a component's API, behavior, or props | [COMPONENTS.md](references/COMPONENTS.md) |
| Get exact values (SVG paths, spring configs, magic numbers) | [EXACT-VALUES.md](references/EXACT-VALUES.md) |
| See page-by-page implementation patterns | [PAGES.md](references/PAGES.md) |
| Check responsive/mobile behavior | [RESPONSIVE.md](references/RESPONSIVE.md) |
| Follow step-by-step new project setup | [ADAPTATION-GUIDE.md](references/ADAPTATION-GUIDE.md) |
