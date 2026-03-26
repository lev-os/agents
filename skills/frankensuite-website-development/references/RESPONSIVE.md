# FrankenSuite Responsive Strategy — Full Reference

---

## Breakpoints (Tailwind Defaults)

| Breakpoint | Width | Primary Use |
|------------|-------|-------------|
| `sm` | 640px | Feature grid 2-col |
| `md` | 768px | **Primary mobile/desktop split** |
| `lg` | 1024px | SectionShell grid, 3-col features |
| `xl` | 1280px | Max content width |

---

## Navigation

### Desktop (hidden md:block)
Floating pill navbar centered horizontally:
```
┌─ Logo ─────────┬─ Nav Links ─────────┬─ Tools ──────────┐
│ [F] FrankenTUI  │ Home Showcase Arch  │ [>_] [👁] GITHUB │
└─────────────────┴─────────────────────┴──────────────────┘
```

- **Position**: `fixed top-6 left-1/2 -translate-x-1/2`
- **Size**: `w-[95%] lg:w-[1200px] h-16`
- **Shape**: `rounded-full`
- **Scroll behavior**: Transparent → glass-modern at `scrollY > 20`
- **Active indicator**: `layoutId="nav-underline"` for smooth animated transitions
- **Tools**: Terminal button, Anatomy toggle, GitHub CTA (Magnetic wrapped)

### Mobile (md:hidden)
Bottom tab bar + slide-out drawer:
```
┌─────────────────────────────────────────┐
│  Home  Show  Demo  Arch  Graph  MORE    │
└─────────────────────────────────────────┘
```

- **Position**: `fixed bottom-6 left-1/2 -translate-x-1/2 w-[90%]`
- **Style**: `glass-modern h-16 rounded-2xl`
- **Shows**: First 5 nav items (icon + 7px label) + "MORE" hamburger
- **Short labels**: Map long labels to abbreviations (`"Architecture" → "Arch."`)
- **MORE drawer**: Slide-in from right (`w-[80%]`), spring animation, body scroll lock
- **Drawer extras**: Anatomy toggle, Audio toggle, Shell Interface button

---

## Layout Patterns by Breakpoint

### SectionShell
```
Mobile:  Single column, full width
lg+:     grid-cols-12 → 4-col sidebar (sticky) + 8-col content
```

### Feature Grid
```
Mobile:  grid-cols-1
sm:      grid-cols-2
lg:      grid-cols-3
```

### Hero Section
```
Mobile:  Centered stack, smaller FrankenEye (scale-100)
md+:     Full-width hero, larger eye (scale-150)
Fluid:   text-[clamp(3.5rem,10vw,7rem)] for title
```

### Hero Buttons
```
Mobile:  flex-col (stacked)
sm:      flex-row (side by side)
```

### Tweet Wall
```
Mobile:  columns-1
md:      columns-2
```

### Footer
```
Mobile:  Single column stack
md:      grid-cols-12 (5+4+3 column split)
```

### Code Blocks
```
Mobile:  overflow-x-auto (horizontal scroll)
Desktop: Full width display
```

---

## Touch & Interaction

### Custom Cursor
- **Desktop only**: Activated via `window.matchMedia("(min-width: 768px)")` in JS
- **Mobile**: Hidden entirely, native cursor restored, no RAF overhead

### Screenshot Gallery
- **Desktop**: Arrow key navigation (← → Escape), click to open lightbox
- **Mobile**: Touch swipe support (60px threshold), tap to open
- **Both**: Portal rendering for z-index isolation, body scroll lock

### Mobile Drawer
- **Slide-in**: `x: "100%"` → `x: 0` with spring animation (`damping: 25, stiffness: 200`)
- **Backdrop**: `bg-black/90 backdrop-blur-md`
- **Scroll lock**: `useBodyScrollLock(open)` with scrollbar width compensation
- **Content**: Full nav list + Anatomy toggle + Audio toggle + Shell Interface button

### Bottom Sheet Modal (Glossary)
- Slide-up via Portal, 92vh max height
- `dialog` role, `aria-modal`, keyboard Escape
- `useBodyScrollLock` prevents background scroll
- `sheetEntrance` variant: y 100%→0, opacity 0.8→1, spring physics

### Feature Card Touch Support
- `onTouchMove` / `onTouchStart` / `onTouchEnd` handlers
- Touch position drives radial gradient (same as mouse on desktop)
- Prevents default browser touch behaviors in interactive areas

### Haptic Feedback
`useHapticFeedback()` hook wraps the Vibration API for tactile button feedback on mobile.

---

## Responsive Table Pattern (Module CSS)

For complex data tables on mobile, the spec-evolution-lab uses:
```css
@media (max-width: 640px) {
  table { display: block; }
  tr { display: grid; }
  td::before {
    content: attr(data-label);
    /* Shows label as inline header per cell */
  }
}
```
Tables stack into card-like rows on mobile with `data-label` pseudo-elements.

---

## Mobile-Specific Component Visibility

| Component | Mobile | Desktop |
|-----------|--------|---------|
| FrankenEye | `hidden` | `lg:block`, scale-150 |
| Custom Cursor | Disabled (no RAF) | Full system with debris/flashlight |
| Desktop nav | `hidden md:block` | Floating pill |
| Mobile nav | `md:hidden` | Hidden |
| GlowOrbits | Simplified/disabled if reduced motion | Full parallax + rotation |
| Signal HUD | Smaller scale | Full display |
| Decorative stitches | `hidden md:block` on some | Full display |

---

## Performance on Mobile

1. **Custom cursor disabled** — saves RAF loop entirely
2. **Reduced motion respected** — `useReducedMotion()` skips animations
3. **Lazy loading** — `loading="lazy"` on all images except above-fold
4. **Font display swap** — prevents FOIT on slow connections
5. **Glass morphism** — `backdrop-filter` is GPU-intensive; used sparingly on mobile
6. **Intersection Observer** — animations and heavy components pause off-screen
7. **GlowOrbits** — Web Animation API (not JS animation) reduces main thread work
8. **content-visibility: auto** — Defers off-screen rendering on long list pages
9. **Passive event listeners** — `{ passive: true }` on all scroll/touch handlers
10. **Image optimization** — WebP format, responsive `sizes` attributes

---

## Testing Checklist

- [ ] Desktop nav: pill navbar floats, glass on scroll, active indicators animate
- [ ] Mobile nav: bottom bar visible, 5 items + MORE, drawer slides in
- [ ] Mobile drawer: spring animation, scroll lock, no layout shift
- [ ] Feature grid: 1→2→3 columns at breakpoints
- [ ] Hero: fluid text sizing, buttons stack/row correctly
- [ ] FrankenEye: hidden on mobile, visible and tracking on desktop
- [ ] Lightbox: keyboard (desktop) and swipe (mobile) both work
- [ ] Bottom sheet: slides up, escape closes, scroll lock active
- [ ] Body scroll lock: no layout shift when any modal/drawer opens
- [ ] Custom cursor: visible on desktop, hidden on mobile
- [ ] Reduced motion: all animations respect preference
- [ ] Touch targets: minimum 44×44px for interactive elements
- [ ] Data tables: stack into cards on narrow screens
- [ ] Video player: play button visible, touch-friendly, scanline overlay
