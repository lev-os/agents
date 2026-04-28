# statline — reusable KPI row

Theme-agnostic 4-cell KPI component with variants. Auto-renders from a JSON `data-stats` attribute.

## Contract

```html
<div class="statline" data-stats='[{"k":"Key","v":"Value","unit":"sub-label"}, ...]'></div>
```

Each stat object: `k` (label, uppercase mini-caps), `v` (value, mono), `unit` (optional sub-label).

## Variants

| Class | Behavior |
|-------|----------|
| `.statline` | Default 4-col. Wraps to 2×2 at `<640px`, 1-col at `<375px`. |
| `.statline.statline--2col` | Always 2 columns. |
| `.statline.statline--inline` | Single-line pipe-separated mini. |

## Animated counters

Add `data-animate="true"`. Integer `v` values tween `0 → target` over 800ms once the element enters viewport (IntersectionObserver, fires once).

## Theme tokens

Inherits from host. No hardcoded colors:
- `--primary` — accent (unused directly; available for host overrides)
- `--on-surface` — labels + numeric values
- `--on-surface-variant` — units + separators
- `--outline` — cell dividers (falls back to `color-mix` of `--on-surface`)

Proven under Obsidian dark and Daybreak light palettes (demo 4 shows both).

## Files

- `statline.css` — component styles (no reset)
- `statline.js` — renderer + scroll-animate (IIFE, no deps)
- `index.html` — 4-demo harness
