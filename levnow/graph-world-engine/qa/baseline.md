# GXW Baseline QA — 2026-04-23

**Source**: https://solar-rapids-gcbw.here.now/
**Local**: ~/.agents/levnow/graph-world-engine/
**Original files**: /tmp/gxw/lev-design-system/project/

## Feature Parity Checklist (binary pass/fail — every variant must satisfy)

1. **Masthead** — title, 4-cell statline with unit labels, annotation block
2. **Section 01 Projections** — ROOT card + 5 projection cards with count + examples
3. **Section 02 Flow Grid** — 12 flow cards, lane-tagged
4. **Section 03 Matrix** — 13 impls × 12 flows, 156 cells, 4 states (direct/family/adjacent/none)
   - Hover a cell → binding panel updates with impl×flow label + kind + text
   - Row + column highlight on hover
   - Lane filter chips → filter rows (tested: "near" hides 10 of 13 rows)
5. **Section 04 Ledger** — 13 rows, 5 columns (idx/name/center/owner/lane)
   - Lane filter chips + text search combine
   - Search "eqsat" → 1 row visible
6. **Section 05 Outliers** — 5 rows (uniq ≥4) ranked by uniqueness, star rating
7. **Section 06 Promotion Lanes** — 3-tier columns (NEAR/MID/FAR) with scored items
8. **Section 07 Judgment Calls** — split2: Promote-first vs Do-not-promote
9. **Section 08 Sources** — 8 file-path rows with notes + colophon
10. **Tweaks FAB** — floating bottom-right, opens panel with 3 segmented toggles:
    - density: comfortable/compact → updates body[data-density]
    - font: jb/ibm/berk → updates body[data-font]
    - annot: off/on → updates body[data-annot]

## Breakpoint Observations (screenshots in qa/bp-*.png)

| Viewport | Page height | Verdict |
|---|---|---|
| 320×568 | 19968px | Matrix unusable; flow cards stack 1-col OK; ledger rows wrap awkwardly |
| 375×812 | ~17000px | Same issues as 320, slightly better |
| 640×960 | ~12000px | Flow cards 2-col, matrix cramped, tweaks FAB still visible |
| 768×1024 | ~10000px | Flow cards 2-col OK, matrix dense, ledger rows wrap |
| 1024×768 | ~8000px | 3-col flow grid, matrix still dense but readable |
| 1280×900 | ~7000px | Good density, matrix clean |
| 1440×900 | ~7000px | Ideal — this is the target |
| 1920×1080 | ~6500px | Everything composed; ledger starts looking sparse |

## Known Breaks

- **Matrix < 1024px**: cells compress to unreadable; needs mobile strategy (horizontal scroll + sticky impl column, OR accordion-per-impl with inline flow chips)
- **Ledger < 768px**: 5-col layout collapses; rows need stacked mobile mode
- **Projection-stack < 768px**: 5 children should stack vertically; arrows become vertical connectors
- **Tweaks FAB at 320px**: overlaps footer colophon if not `position: fixed` with safe-area inset

## Target Enhancements for Variants

- Sticky impl column in matrix (both variants)
- Mobile accordion fallback for matrix when viewport < 768px
- Ledger collapses to card-stack mode on mobile
- Projection-stack vertical rail on narrow
- Skip links for keyboard nav (currently none)
