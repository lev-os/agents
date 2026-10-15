---
name: desktop-to-mobile
description: Create a 390px mobile version of a selected desktop frame, following responsive best practices — stacking, navigation transforms, type scaling, touch targets, and content prioritization. Use in Figma Agent or Figma Make when asked to make a mobile version, adapt for mobile, or invoke /mobile-from-desktop.
---

# Mobile From Desktop

Create a mobile version of the selected desktop frame. The mobile version must feel natively designed for mobile — not a shrunk desktop. Preserve the brand, content, and visual language exactly; transform only structure, sizing, and interaction patterns.

## Canvas setup

- Target width: **390px** (iPhone 14/15 baseline). If the user names another width, use theirs.
- Height: auto — grows with content. Never crop or hide content to fit an arbitrary height.
- Name the new frame `[original name] — Mobile 390`.
- Place it **120px to the right** of the desktop frame.
- Never modify the original desktop frame.

## Step 1 — Read and map the desktop frame

Before creating anything:

1. Read the full node tree of the selection: sections, their order, grids, components, text styles, spacing values.
2. Identify the section types present (hero, nav, feature grid, pricing, testimonials, gallery, footer, forms, tables, etc.).
3. Note the spacing system (base unit, section paddings) and type scale — mobile values will be derived from these, not invented.
4. If the selection is not a frame, or is a single small component rather than a page/screen, tell the user and stop.

## Step 2 — Global transformation rules

### Layout
- Multi-column grids stack into a single column. Column order = desktop reading order (left→right, top→bottom).
- Content max-width: 390 − 2×20px side margins = **350px** content area. Side padding: 20px (or 16px if the desktop system uses a 4px base).
- Section vertical padding: reduce desktop values by ~40–50% (e.g. 120px → 64px, 96px → 56px, 64px → 40px). Keep the rhythm proportional — bigger desktop gaps stay bigger on mobile.
- Gaps between stacked items: 16–24px, taken from the desktop spacing scale.
- Use auto layout (vertical) for every stacked section so the frame stays editable.

### Typography
- Scale down headings ~30–40%, keep body nearly intact:
  - Desktop 64–72 → 36–40
  - Desktop 48–56 → 30–32
  - Desktop 32–40 → 24–28
  - Desktop 24 → 20
  - Body 16–18 → keep 16 (never below 15 for body)
  - Captions/labels → keep, minimum 12
- Line-height: headings 1.1–1.2, body 1.5–1.6.
- Shorten nothing: keep all copy. If a heading wraps to 4+ lines, flag it in the final report rather than rewriting.
- Left-align long text blocks even if desktop centers them; centered is fine for short heroes and section titles.

### Touch targets
- Every interactive element: minimum **44×44px** hit area.
- Buttons: full-width (350px) for primary CTAs in stacked sections; height 48–56px. Secondary buttons may stay intrinsic width.
- Adjacent tap targets: minimum 8px between them.
- Links inside body text: keep, but ensure surrounding line-height gives enough tap room.

### Imagery
- Full-bleed images may extend edge-to-edge (390px); contained images stay within the 350px content area.
- Preserve aspect ratios; switch wide panoramic crops (e.g., 21:9 hero) to 4:3 or 1:1 crops focused on the subject.
- Decorative background elements that would crowd a small screen: scale down or remove, and list every removal in the final report.

## Step 3 — Section-specific patterns

### Navigation
- Desktop horizontal nav → top bar 64px tall: logo left, hamburger icon right.
- Also create a separate frame `[name] — Mobile Menu` showing the opened menu state: full-screen or dropdown with the nav links stacked, 56px row height each.
- If the desktop nav has a prominent CTA (e.g. "Get started"), keep it visible in the top bar next to the hamburger if space allows, otherwise first item in the opened menu.
- If the page is app-like (dashboard) with 3–5 primary destinations → use a bottom tab bar (56px, icons + labels) instead of a hamburger.

### Hero
- Stack: heading → subheading → CTA(s) → hero image. If the image is the message (product shot), image may go first.
- Two side-by-side CTAs → stack vertically, primary on top, 12px gap.

### Feature grids (3–4 columns)
- Stack into one column, OR use a horizontal swipe carousel if there are 4+ visually rich cards. Default: stack. Use carousel only for card galleries, logos, and testimonials.
- Card internal padding: reduce ~25% from desktop.

### Logo bars / social proof
- Wrap into 2 rows, or single-row horizontal scroll. Shrink logos to max height 28–32px.

### Pricing tables
- Stack plans vertically, recommended plan first (not middle, as on desktop).
- If plans share a long feature-comparison table → each plan card lists its own features; drop the comparison matrix and note it in the report.

### Data tables
- Tables wider than 350px: transform each row into a card (label: value pairs stacked), or make the table horizontally scrollable with the first column pinned. Default: cards for ≤6 columns of simple data, scroll for dense numeric tables.

### Forms
- All fields full-width, stacked. Field height 48–56px. Labels above fields, never placeholder-only.
- Multi-column form rows (First name | Last name) → stacked, unless both fields are short (ZIP | City may stay paired).

### Footer
- Columns stack; link groups become either stacked lists or accordions if there are 4+ groups. Legal line and social icons last.

### Sticky elements
- Desktop sticky sidebar CTAs → sticky bottom bar on mobile (full-width button, 16px padding, above safe area).

## Step 4 — Content prioritization

Mobile users scroll, but attention decays. Without deleting content:
- Keep the desktop section order unless a section is purely decorative filler before the primary CTA — in that case it may move below the CTA section. Report any reordering.
- Collapse long FAQ lists into accordions (first item may be expanded).
- Long testimonial walls → carousel of one testimonial per view.

## Step 5 — Finalize and report

1. Verify: no horizontal overflow anywhere, all text legible (body ≥15px), all touch targets ≥44px, auto layout applied to all stacked sections.
2. Deliver frames: `— Mobile 390` and `— Mobile Menu` (plus any state frames created).
3. Report in chat:
   - Sections transformed and which pattern was used for each
   - Anything removed, cropped, reordered, or converted (e.g., "comparison matrix → per-card feature lists")
   - Flags for human review (headings wrapping 4+ lines, dense tables, ambiguous nav CTA placement)

## Guardrails

- Never invent new content, copy, or imagery — everything comes from the desktop frame.
- Never restyle: colors, fonts, radius, shadows stay identical to the desktop system.
- Use existing components and their mobile variants from the connected library if they exist; only detach or rebuild when no variant fits, and report each case.
- If the desktop frame uses breakpoint-specific components (e.g., `nav/desktop`), check the library for the `nav/mobile` counterpart before building one from scratch.
