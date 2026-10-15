---
name: better-interface
description: Review a Figma interface across UI polish, accessibility, layout, typography, and writing, then pin findings as cards beside the frame. Use in Figma Agent or Figma Make when asked to critique, polish, or audit a screen.
---

# Review the interface as one system

A strong interface is not five independent audits stapled together. Position and spacing carry hierarchy before a word is read, the words themselves do the explaining, type makes them legible, and polish is what makes the result feel deliberate rather than assembled. Review the whole experience, then consolidate into one prioritized verdict.

When reviewing, slow the interface down. Walk it as a keyboard-only user first — every flow must complete without a mouse. Read the page instead of scanning the code: squint to check the hierarchy holds, read one full paragraph for comfort, resize the viewport to catch bad wrapping and truncation at real content lengths. Replay motion at 10% speed in the browser's Animations panel and walk every state: hover, focus, active, loading, empty. What feels off at 10% speed is what's subtly wrong at full speed.

**Match the project's styling system.** Before writing any fix, check how the codebase styles things and express every change in that system: Tailwind utilities in a Tailwind project, plain declarations in CSS, CSS Modules, styled-components or StyleX. Preserve the project's component library, tokens, and density, and its established motion language except where a principle below prescribes an exact interaction pattern. Never introduce a second styling approach just to apply a fix.

Treat numeric values as starting points for interfaces without an established density or spacing system. Preserve deliberate platform chrome, compact professional tools, and project tokens when they remain usable under hit-area, zoom, localization, and viewport stress tests.

Color notation, palette construction, and gamut are out of scope; this skill measures and reports contrast but does not repaint the project.

## How to run a review

### Resolve scope and mode first

Infer the screen, flow, feature, or repository scope from the request and current workspace. State the resolved scope in the output. Use `full` when no mode is supplied.

| Mode | Coverage | Finding cap |
| --- | --- | --- |
| `quick` | Primary user path and highest-traffic states; report only `HIGH` and `MEDIUM` issues | 5 |
| `full` | Entire requested scope across all five domains, including empty, loading, error, and narrow-width states when present | 15 |

If the requested scope is too large to inspect credibly, narrow it to the highest-traffic complete flow and state the boundary. Never imply uninspected surfaces were reviewed.

### Recon before judgment

Identify the framework, styling system, component library, design tokens, supported viewports, and available preview or test commands. For copy, inspect nearby interface text, the product's terminology, localization conventions, and any voice or content style guide before proposing a change.

### Review in this order

Foundational failures must not be hidden by polish:

1. Accessibility
2. Layout
3. Writing
4. Typography
5. UI polish

When two domains appear to cover the same issue, assign it to the one that owns the underlying rule and mention secondary effects in the **Why** cell. Report it once.

### Require evidence

Every finding cites `path/to/file:line` and shows the current implementation. If the review artifact has no source files, cite the exact screen and component. Do not report a code-level finding from visual appearance alone, or a visual finding from source code alone when runtime behavior determines the result.

### Review without mutating by default

Treat a review request as read-only. Do not edit source code unless the user also asks to implement the findings. When implementation is requested, preserve the consolidated report as the change scope and re-run the relevant verification afterward.

## Accessibility

Accessibility is not a compliance checkbox bolted on at the end; it is the floor for interface craft. Most of it is free if you use the platform: native elements ship with keyboard support, real labels announce themselves, and a visible focus ring is one CSS rule. When unsure, prefer the platform default over a custom rebuild, and remove ARIA rather than add it.

### 1. Native Elements First

The first rule of ARIA: don't use ARIA when a native element exists. `<button>` for actions, `<a href>` for navigation (it must support Cmd/Ctrl/middle-click), never `<div onClick>`. No ARIA is better than bad ARIA.

### 2. Visible Focus Rings

Style `:focus-visible`, not bare `:focus`, so keyboard users get a ring and mouse users usually don't. Prefer the browser's unmodified focus indicator. If the design needs a custom ring, use a project focus token or another explicit color and verify the complete indicator against every adjacent color it crosses; `currentColor` is acceptable only after the same check. Use at least a `2px` solid perimeter or an equivalent visible area. Never use `outline: none` without a verified replacement, and preserve system colors in forced-colors mode.

### 3. Full Keyboard Support

Every pointer interaction needs a keyboard path, following the ARIA APG patterns: Escape closes overlays, arrow keys move within composite widgets (tabs, menus, listboxes), Tab moves between widgets, Enter and Space activate. Only `tabindex="0"` (join the natural tab order) and `tabindex="-1"` (programmatic focus), never positive values, which break the natural order. Composite widgets use roving tabindex: the active item is `0`, all others `-1`.

### 4. Trap and Restore Focus

Modals set `inert` on the background content, move focus inside on open, and return focus to the trigger on close. Add `overscroll-behavior: contain` so background content doesn't scroll.

### 5. Minimum Hit Area

WCAG 2.5.8's Level AA baseline is a 24×24 CSS-pixel target or one of its defined spacing, equivalent-control, inline, user-agent, or essential exceptions. For easier activation, aim for 44×44px in touch contexts and 40×40px in desktop interfaces when density permits. Extend with a pseudo-element if the visible element should stay smaller. Never let extended hit areas overlap.

### 6. Label and Type Every Control

Every input gets a `<label for>` or wrapping `<label>`; a placeholder is never a label, and label and control share one hit target: no dead zones between a checkbox and its text. Add `autocomplete` with a meaningful `name`, and the correct `type` and `inputmode` for the keyboard. Never block paste; users paste passwords and one-time codes.

### 7. Accessible Names Everywhere

Icon-only buttons need a descriptive `aria-label`. Visible label text must appear in the accessible name. Decorative elements get `aria-hidden="true"`, never on a focusable element.

### 8. Don't Rely on Color Alone

Status needs a redundant cue: icon, text, or underline alongside the color. Determine which WCAG contrast requirement applies from the content and state, then measure the rendered foreground/background pair. When contrast fails, report the pair and the requirement it misses; do not change the project's colors unless asked.

### 9. Honor prefers-reduced-motion

Wrap motion in `@media (prefers-reduced-motion: no-preference)` so it is opt-in. Under reduced motion, replace slides and scales with opacity crossfades; kill parallax and autoplay entirely. Independent of the preference: autoplaying media needs a visible pause control, and toasts carrying actions or errors stay until dismissed.

## Layout

Layout communicates before a single word is read: position, spacing, and alignment carry hierarchy on their own, and generous space beats decoration. A good layout also survives stress: resize it, translate it, mirror it for RTL, and it should still hold together.

### 1. Group with Space, Not Lines

Negative space is the primary grouping tool; background shapes second; separator lines last, only where space alone can't carry the structure. The gap between groups must be at least 2× the gap within a group (`8px` intra-group → `16px`+ inter-group), or the grouping reads as noise.

### 2. Keep Controls Distinct from Content

Interactive elements must look interactive: a background shape, a border, or a consistent placement zone. Never style a control identically to adjacent static text.

### 3. Align to Shared Edges

Pick alignment edges and stick to them; every stray edge reads as noise. Use one project spacing step for each level of subordination (`16px` is a useful default). Use logical properties (`padding-inline-start`, `margin-inline-end`) for direction-dependent layout; reserve physical left/right for genuinely physical geometry.

### 4. Order by Importance

The most important content sits near the top and the leading edge; reading order flows top-to-bottom, leading-to-trailing. Think in leading/trailing, not left/right.

### 5. Breathing Room Between Targets

Without an established density system, start with `12px` between adjacent bordered or filled controls and `24px` of clearance around borderless text- and icon-only controls. Compact layouts may use less when the hit areas above do not overlap and the controls remain visually distinct.

### 6. Hold Structure Until It Breaks

Breakpoints come from the content, not device presets. Keep the expanded layout as long as it genuinely fits and collapse late; prefer container queries for component-level adaptation. Test the smallest and largest sizes first.

### 7. Plan for Growth and Clipping

Plan for substantial and language-dependent string growth rather than relying on a universal percentage: no fixed widths or heights on text containers, and let rows wrap. Never park critical actions where resizing or scrolling clips them; keep them reachable in the normal flow or stable chrome appropriate to the product.

## Writing

Clear and brief beats clever, consistency beats variety, and the best error message is the interaction redesigned so the error can't happen. Preserve intentional brand character when it remains clear and appropriate to the stakes: treat a difference from generic plain language as a finding only when it creates inconsistency, ambiguity, translation risk, or an inappropriate tone.

### 1. One Voice, Flexible Tone

The product has one voice, established by its existing system rather than invented during a local edit. Keep terms consistent: if it's "Archive" in the menu, it isn't "Move to storage" in the toast. Tone flexes with the stakes:

| Context | Tone |
| --- | --- |
| Success, onboarding, empty states | Warm, can be light |
| Routine actions, settings | Neutral, minimal |
| Errors, destructive confirmations | Calm, plain, zero playfulness |
| Data loss, security | Serious, explicit |

### 2. Plain Words Over Clever Ones

Choose easily understood words and delete every word that isn't needed. No idioms, colloquialisms, or humor that won't translate. Skip unnecessary gender: "Subscribers can post recipes", not "each subscriber can post his or her recipes". Match the input device: "tap" on touch, "click" with a pointer, "select" when both are possible. Never build sentences by concatenating fragments around variables (`"You have " + n + " new messages"`); word order changes per language, so use full templated strings with proper pluralization.

### 3. Verb-First Buttons

Button labels start with a verb naming the specific action: "Send", "Save draft", "Delete project". Never "OK!", "Let's go!", or bare "Yes"/"No" on consequential actions. Confirmation buttons repeat the consequence so the dialog is answerable without reading the body: "Delete this project?" offers `Delete project` and `Cancel`, not `Yes` and `No`.

### 4. Links Describe Their Destination

Link text makes sense out of context; screen-reader users navigate by a list of the page's links. "Read the billing docs", never "Click here" (which also fails the device-verb rule on touch), and never a bare "Learn more" when several appear on one page. Suffix each: "Learn more about exports".

### 5. One Capitalization Policy

Pick title case or sentence case per element type (all buttons, all headings) and apply it consistently; sentence case is the safer default: calmer, no per-word case rules, localizes cleanly. "Save Changes" beside "Discard changes" reads as sloppiness.

### 6. Errors Say How to Fix, Next to Where It Broke

An error is an instruction, adjacent to the failing field:

| Bad | Good |
| --- | --- |
| That password is too short | Choose a password with at least 8 characters |
| Invalid name | Use only letters for your name |
| Oops! Something went wrong. | Unable to save. Check your connection and try again. |

No blame, no "oops", no exclamation marks. Phrase hints positively ("Use only letters", not "Don't use numbers or symbols") and show them before the mistake, not after. If the same error keeps firing for many users, redesign the interaction instead of rewording it.

### 7. Empty States Point Forward

An empty state says what this place is and how to fill it, with one clear next action:

```html
<!-- Bad: a shrug -->
<p>No results.</p>

<!-- Good: orientation plus a next step -->
<p class="font-medium">No projects yet</p>
<p class="text-sm text-zinc-500">Projects keep your tasks and files together.</p>
<button class="mt-4">Create a project</button>
```

Search and filter empty states name the query and offer an exit: "No results for 'quarterly'. Clear filters". Never park crucial persistent information in an empty state; it disappears the moment content exists.

## Typography

Good typography is mostly restraint. A sensible scale, comfortable spacing and enough contrast beat any clever effect. A label, a table cell, a marketing headline and an article paragraph should not share one set of rules.

### 1. Fewer Fonts, Sizes and Weights

Rarely use more than three fonts. Weight and size define hierarchy, but overusing them hurts readability quickly. Pair for contrast, not similarity: a serif headline with a sans body reads as deliberate, two near-identical sans-serifs read as a mistake. Below `18px`, stay at weight `400`+; weights under `300` are display-only (`28px`+), they disappear at text sizes.

### 2. Use a Type Scale with Semantic Names

Define a small set of sizes and deviate from it as little as possible. Hard-coded sizes without a system break down at scale. For solo projects, default names like `text-sm` work fine as long as the usage rules are clear. On a team, name sizes by use (`text-body-sm`), not by size, so the rules stay consistent.

### 3. Heading Sizes Descend with Level

Within a coherent page hierarchy, map heading levels to descending steps of the type scale: a visually subordinate heading should not accidentally overpower its parent. Adjacent levels may share a size toward the small end of the scale as long as weight or spacing keeps them distinct. Pick semantic heading elements per the Accessibility principles above; this section controls only their visual treatment.

### 4. Line-Height by Role

Headings tighter, around `1.1`. Body copy `1.5` to `1.6`. Prefer unitless values so line-height scales with the font size; fixed values like `24px` do not. Tight line-height is for short text: anything that wraps to three or more lines needs at least `1.4`, even in height-constrained rows.

### 5. Cap the Measure

Long lines make it hard for the eye to find the next line. Cap long-form text around 60–75 characters per line. Any unit works: `65ch` measures characters directly, and a pixel or rem cap is just as good: at a `16px` body size the range lands roughly between `560px` and `680px` depending on the font, so Tailwind's `max-w-xl` or `max-w-2xl` fit. What matters is that a cap exists and the resulting line length sits in range.

### 6. Wrap Deliberately

`text-wrap: balance` distributes text evenly across lines: use it on headings. `text-wrap: pretty` avoids leaving a single short word on the final line: use it on descriptions. Skip both in long-form text: browsers ignore `balance` past a few lines anyway, and evening out a whole paragraph wastes space and makes it harder to read. `overflow-wrap: break-word` where long words, links or IDs could escape the container. `white-space: nowrap` on labels and badges where a line break looks broken.

### 7. Tabular Numbers on Changing Values

Digits have different widths by default, so timers, counters and prices shift layout as they update. Apply `font-variant-numeric: tabular-nums` to any value that changes.

### 8. Truncate Without Losing Content

Single line: `text-overflow: ellipsis` with `overflow: hidden` and `white-space: nowrap`. Multiple lines: `line-clamp`. Truncation hides content, so if the missing text matters, keep the full value reachable in a tooltip or expanded view.

### 9. Inputs at 16px on Mobile

iOS Safari zooms the whole page when an input's text is smaller than `16px`. Keep input text at `16px` on mobile viewports (`text-base sm:text-sm`). Avoid the `maximum-scale=1` viewport meta: Safari ignores it for pinch zoom, but every other browser honors it and blocks zooming, which fails WCAG.

## UI polish

Great interfaces rarely come from a single thing. It's usually a collection of small details that compound into a great experience. This section assumes an animation belongs; deciding whether it belongs at all, and what it costs the user at its trigger frequency, is a separate question worth asking before reaching for the recipes below.

### 1. Concentric Border Radius

Outer radius = inner radius + padding. Mismatched radii on nested elements is the most common thing that makes interfaces feel off.

### 2. Optical Over Geometric Alignment

When geometric centering looks off, align optically. Buttons with icons, play triangles, and asymmetric icons all need manual adjustment.

### 3. Shadows for Elevation, Borders for Structure

For buttons, cards, and containers whose border exists only to create depth, prefer layered transparent `box-shadow` values. Keep borders that communicate structure or state: dividers, layout separators, and selected or focus states.

### 4. Interruptible Animations

Use CSS transitions for interactive state changes: they can be interrupted mid-animation. Reserve keyframes for staged sequences that run once.

### 5. Split and Stagger Enter Animations

For an infrequent staged entrance where sequence helps communicate hierarchy, break content into semantic chunks and stagger them by ~100ms instead of animating one container. Confirm the entrance is infrequent enough to earn a stagger; anything the user triggers often should not stagger at all.

### 6. Subtle Exit Animations

Use a small fixed `translateY` instead of full height. Exits should be softer than enters. Use `ease-out` for both enter and exit transitions.

### 7. Contextual Icon Animations

Animate icons with `opacity`, `scale`, and `blur` instead of toggling visibility. Use exactly these values: scale from `0.25` to `1`, opacity from `0` to `1`, blur from `4px` to `0px`. If the project has `motion` or `framer-motion` in `package.json`, match that package's import path (or the established nearby imports when both exist) and use `transition: { type: "spring", duration: 0.3, bounce: 0 }`; bounce must always be `0`. If no motion library is installed, keep both icons in the DOM (one absolute-positioned) and cross-fade with CSS transitions using `cubic-bezier(0.2, 0, 0, 1)`; this gives both enter and exit animations without any dependency.

### 8. Image Outlines

Add a subtle `1px` outline with low opacity to images for consistent depth. The color must be pure black in light mode (`oklch(0 0 0 / 0.1)`) and pure white in dark mode (`oklch(1 0 0 / 0.1)`), never a near-black like slate, zinc, or any tinted neutral. A tinted outline picks up the surface color underneath it and reads as dirt on the image edge.

### 9. Scale on Press

A subtle `scale(0.96)` on click gives buttons tactile feedback. Always use `0.96`. Never use a value smaller than `0.95`: anything below feels exaggerated. Add a `static` prop to disable it when motion would be distracting.

### 10. Skip Animation on Page Load

Use `initial={false}` on `AnimatePresence` to prevent enter animations on first render. Verify it doesn't break intentional entrance animations.

### 11. Never Use `transition: all`

Always specify exact properties: `transition-property: scale, opacity`. Tailwind's `transition-transform` covers `transform, translate, scale, rotate`.

### 12. Use `will-change` Sparingly

Only for `transform`, `opacity`, `filter`, the properties the GPU can composite. Never use `will-change: all`. Only add when you notice first-frame stutter.

### 13. Match Icon Stroke to Text Weight

An icon next to text carries the text's optical weight: `1.5px` stroke beside regular (400) text, `2px` beside semibold (600). One stroke weight per icon set; never mix libraries on one surface.

### 14. One SVG, Recolored per State

Icons use `currentColor` and get their states (hover, selected, disabled) from CSS color and opacity, never from separate assets. Outline variant is the default; fill variant marks the active state.

### UI polish: common mistakes

| Mistake | Fix |
| --- | --- |
| Same border radius on closely nested parent and child | Calculate `outerRadius = innerRadius + padding` |
| Icons look off-center | Adjust optically with padding or fix SVG directly |
| Border used only to fake elevation | Use layered `box-shadow` with transparency; keep structural and state borders |
| Jarring staged entrance or contextual exit | Stagger infrequent entrances and keep context-preserving exits subtle |
| Stateful icon or toggle animates its default state on page load | Add `initial={false}` to that `AnimatePresence`; preserve intentional page entrances |
| `transition: all` on elements | Specify exact properties |
| First-frame animation stutter | Add `will-change: transform` (sparingly) |
| Hairline icon beside bold text | Match the stroke width to the text weight |
| Separate icon assets per state | One `currentColor` SVG, states via CSS |
| Filled icons everywhere | Outline as default, fill only for the active state |

## Review Output Format

Always use the following sections.

### Scope and Coverage

State the mode, exact scope, stack and styling conventions, and any review boundary. Then show coverage:

| Domain | Evidence inspected | Result |
| --- | --- | --- |
| Accessibility | Files, components, states, or checks | Findings count or `Clear` |

Include all five domains. `Clear` means inspected with no actionable finding; `Not reviewed` must explain why.

### Findings

Use one table ordered by severity, then reach and leverage:

| # | Severity | Domain | Location | Before | After | Why |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | HIGH | Accessibility | `src/Dialog.tsx:42` | ` ` | Add `aria-label="Close"` and hide the icon from the accessibility tree | The icon-only control has no accessible name |

Severity is one shared scale:

- `HIGH`: blocks a task, misleads the user, hides content or controls, causes data-loss risk, or creates a repeated systemic failure.
- `MEDIUM`: meaningfully harms comprehension, efficiency, adaptability, or consistency.
- `LOW`: isolated polish with limited task impact. Include only in `full` mode.

Within a severity, rank by reach and leverage. A token or shared-component fix outranks the same symptom in one leaf component.

Each row is one root cause: list every confirmed location in the same row rather than producing a row per occurrence. Respect the mode's finding cap, and never pad the report to reach it. If there are no findings, omit the table and state "No actionable interface findings."

### Annotate the frame

Every row in the findings table also lands on the canvas as a card. Cards go on one top-level layer named `Interface review`, in the empty space to the left and right of the frame — never on top of the design, and never overlapping the frame's own titles or chrome.

Never reparent, edit, lock, or restyle the frames under review. Annotations are additive; the review is otherwise read-only.

#### Card anatomy

Each card is a vertical auto-layout frame: `280px` fixed width, height hugging its contents, `12px` padding, `8px` item spacing, `8px` corner radius, `oklch(1 0 0)` fill, `1px` `oklch(0 0 0 / 0.08)` stroke.

Three stacked children, in order:

1. **Severity pill** — hug-width rounded rect, `4px` radius, `2px` vertical and `6px` horizontal padding, filled with the severity color below. Label is the severity word in uppercase, `9px`, weight `600`, `0.04em` letter-spacing.
2. **Title** — `#4 CTA contrast`. The finding number, then a three-to-five-word summary. `12px`, weight `600`, `oklch(0.15 0 0)`.
3. **Body** — one or two sentences: what is wrong, then what to do. `11px`, weight `400`, line-height `1.4`, `oklch(0.45 0 0)`. Cap at `240` characters; the full reasoning stays in the findings table.

| Severity | Pill fill | Pill text |
| --- | --- | --- |
| `HIGH` | `oklch(0.577 0.245 27.325)` red | `oklch(1 0 0)` white |
| `MEDIUM` | `oklch(0.705 0.213 47.604)` orange | `oklch(0.15 0 0)` near-black |
| `LOW` | `oklch(0.852 0.199 91.936)` yellow | `oklch(0.15 0 0)` near-black |

White on orange and yellow measures below 4.5:1; use the near-black. The pill names the severity in words, so color never carries it alone and no separate legend is needed.

#### Building the card

Hug sizing is not the default, and children only participate in auto-layout once appended. Follow this sequence exactly:

```js
await figma.loadFontAsync({ family: "Inter", style: "Semi Bold" });
await figma.loadFontAsync({ family: "Inter", style: "Regular" });

const card = figma.createFrame();
card.layoutMode = "VERTICAL";            // must come before any sizing property
card.primaryAxisSizingMode = "AUTO";     // hug height
card.counterAxisSizingMode = "FIXED";    // fixed width
card.resize(280, card.height);
card.verticalPadding = 12;
card.horizontalPadding = 12;
card.itemSpacing = 8;

// Children must be appended to the card. Creating a node and setting its
// x/y puts it on the canvas as a sibling: the card then hugs to nothing
// and its contents float outside the frame.
card.appendChild(pill);
card.appendChild(title);
card.appendChild(body);

// Text wraps to the card width and grows downward
for (const text of [title, body]) {
  text.layoutAlign = "STRETCH";
  text.textAutoResize = "HEIGHT";
}

// The pill hugs its own label instead of stretching
pill.layoutMode = "HORIZONTAL";
pill.primaryAxisSizingMode = "AUTO";
pill.counterAxisSizingMode = "AUTO";
pill.layoutAlign = "INHERIT";
pillLabel.textAutoResize = "WIDTH_AND_HEIGHT";

// x and y are ignored on auto-layout children. Position the card only.
card.x = gutterX;
card.y = stackY;
```

Load every font with `figma.loadFontAsync` before setting `characters`. Text set with an unloaded font measures at zero, so the card hugs to nothing.

Gate on the result before positioning anything else:

```js
if (card.children.length !== 3 || card.height < 56) {
  throw new Error(
    `Finding ${n}: card built empty — ${card.children.length} children, ${card.height}px tall`
  );
}
```

A correctly built card is at least `56px` tall. Anything near `26px` is padding with no content in between.

| Symptom | Cause |
| --- | --- |
| Card hugs to ~`26px` with contents floating outside it | Children created but never `appendChild`ed to the card |
| Every card is the same height | `primaryAxisSizingMode` left at `FIXED` |
| Card is as wide as its longest line | `counterAxisSizingMode` left at `AUTO` |
| Body text runs off the card on one line | Text missing `layoutAlign = "STRETCH"` and `textAutoResize = "HEIGHT"` |
| Pill spans the full card width | Pill missing `AUTO` sizing on both axes |
| Children ignore the positions you set | Expected — auto-layout owns child position; set `x`/`y` on the card only |

#### Placement

Cards sit in two gutters: one starting `80px` to the left of the frame, one `80px` to the right. Assign each card to the gutter nearer its target node, then within a gutter sort by the target's vertical position and stack top to bottom with `16px` between cards. If a stack would run past the frame's bottom edge, move the overflow to the other gutter rather than shrinking cards or letting them overlap.

Position cards only after all children are appended and sized; a card's final height is not known until then.

Draw a `1.5px` dashed connector from the card's inner edge to the target node's nearest edge, stroked in that finding's severity color, routed as a single elbow: horizontal out of the card, then horizontal into the node. End it with a `4px` dot on the node, not an arrowhead. A finding that spans the whole flow gets no connector.

Card and connector for one finding are grouped together and named `#4 MEDIUM Layout`.

#### Scale

The values above assume a frame between `1000px` and `1600px` wide. Outside that range, multiply every annotation dimension and type size by `frameWidth / 1400` so cards stay readable at the zoom level where the whole frame fits on screen.

#### Re-running

Delete the existing `Interface review` layer before drawing the new one. Annotations replace; they never stack. If the file is view-only or the user asked for the report only, output the table alone and say the frame was not annotated.

### Considered but Rejected

Record candidates considered but deliberately rejected. A candidate is rejected when the principle above permits the current implementation, evidence is insufficient, the project convention is intentional, or the proposed change would add complexity without user benefit.

Include 1–3 candidates in `quick` mode and 2–5 in `full` mode:

| Location | Candidate | Rejected because |
| --- | --- | --- |
| `src/Card.tsx:28` | Increase the shadow | Existing depth matches the shared surface token; changing one card would reduce consistency |

These are real candidates inspected during the review, not invented filler. If the scope genuinely contains fewer borderline candidates, include the ones that exist and say so.

### Verification

Run safe, relevant checks available in the project. Inspect the rendered interface when runtime behavior or visual judgment matters. List each check or interaction, the exact command or steps, and the observed result. Separate checks that passed from checks marked **Not verified**; never convert a verification gap into a finding.

### Verdict

End with exactly one:

- `Block` — one or more `HIGH` findings remain.
- `Needs changes` — only `MEDIUM` or `LOW` findings remain.
- `Approve` — no actionable findings remain and the claimed coverage was verified.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| `outline: none` to remove the focus ring | Style `:focus-visible` instead; mouse clicks won't show it |
| ` ` for a button or link | ` ` for actions, ` ` for navigation |
| Placeholder used as the only label | Add a visible ` `; placeholders disappear on input |
| Positive `tabindex` to fix focus order | Fix the DOM order; only use `0` and `-1` |
| `aria-hidden="true"` on a focusable element | Remove it or make the element non-focusable |
| Submit disabled until the form is valid | Keep it enabled; validate on submit and focus the first error |
| Separator line where spacing would do | Remove the line, double the gap between groups |
| `margin-left` / `padding-right` in a localizable layout | `margin-inline-start` / `padding-inline-end` |
| Breakpoints at 768/1024 because they're the defaults | Break where the content actually stops fitting |
| Fixed-width text container sized to one language | `max-width` + wrapping; test pseudo-localization and representative locales |
| `OK` / `Yes` confirming a destructive dialog | Repeat the consequence: "Delete project" |
| "Click here" or bare "Learn more" link | Describe the destination: "Read the billing docs" |
| "Oops! Something went wrong." | Say what to do, next to the failing field |
| "Save Changes" beside "Discard changes" | One capitalization policy per element type |
| Hard-coded one-off font sizes | Use the type scale |
| `line-height: 24px` on scalable text | Unitless value (`1.5`) |
| Full-width paragraphs | Cap around 60–75 characters per line |
| Numbers cause layout shift | `tabular-nums` |
| Truncated text with no way to read it | Tooltip or expanded view for the full value |
| Inputs below `16px` zoom on iOS | `text-base sm:text-sm` |
| Six disconnected domain reports | Consolidate into one ranked findings table |
| Visual claim inferred only from source | Inspect the rendered state or mark it not verified |
| Review silently edits code | Stay read-only unless implementation was requested |
| "Approve" with pending actionable findings | Use `Needs changes` or `Block` |

---

## Surfaces

Border radius, optical alignment, shadows, and image outlines.

### Concentric Border Radius

When nesting rounded elements, the outer radius must equal the inner radius plus the padding between them:

```
outerRadius = innerRadius + padding
```

This rule is most useful when nested surfaces are close together. If padding is larger than `24px`, treat the layers as separate surfaces and choose each radius independently instead of forcing strict concentric math.

#### Example

```css
/* Good: concentric radii */
.card {
  border-radius: 20px; /* 12 + 8 */
  padding: 8px;
}
.card-inner {
  border-radius: 12px;
}

/* Bad: same radius on both */
.card {
  border-radius: 12px;
  padding: 8px;
}
.card-inner {
  border-radius: 12px;
}
```

#### Tailwind Example

```tsx
// Good: outer radius accounts for padding
<div className="rounded-2xl p-2">       {/* 16px radius, 8px padding */}
  <div className="rounded-lg">          {/* 8px radius = 16 - 8 ✓ */}
    ...
  </div>
</div>

// Bad: same radius on both
<div className="rounded-xl p-2">
  <div className="rounded-xl">          {/* same radius, looks off */}
    ...
  </div>
</div>
```

Mismatched border radii on closely nested surfaces is a common source of visual tension. Calculate concentrically when the layers share a visible, even inset; preserve an established component token when the layers are independent or the padding is intentionally asymmetric.

### Optical Alignment

When geometric centering looks off, align optically instead.

#### Buttons with Text + Icon

When an icon makes otherwise symmetric padding look unbalanced, use slightly less padding on the icon side. A useful starting point is:
`icon-side padding = text-side padding - 2px`.

```css
/* Good: less padding on icon side */
.button-with-icon {
  padding-inline-start: 16px;
  padding-inline-end: 14px; /* trailing icon side = text side - 2px */
}

/* Bad: equal padding looks like icon is pushed too far right */
.button-with-icon {
  padding-inline: 16px;
}
```

```tsx
// Tailwind
<button className="ps-4 pe-3.5 flex items-center gap-2">
  <span>Continue</span>
  <ArrowRightIcon />
</button>
```

#### Play Button Triangles

Play icons are triangular and their geometric center is not their visual center. Shift slightly right:

```css
/* Good: optically centered */
.play-button svg {
  transform: translateX(2px); /* physical correction to the glyph itself */
}

/* Bad: geometrically centered but looks off */
.play-button svg {
  /* no adjustment */
}
```

#### Asymmetric Icons (Stars, Arrows, Carets)

Some icons have uneven visual weight. The best fix is adjusting the SVG directly so no extra margin/padding is needed in the component code.

```tsx
// Best: fix in the SVG itself
// Adjust the viewBox or path to visually center the icon

// Fallback: adjust with margin
<span className="translate-x-px">
  <StarIcon />
</span>
```

### Shadows Instead of Borders

For **buttons, cards, and containers** that use a border for depth or elevation, prefer replacing it with a subtle `box-shadow`. Shadows adapt to any background since they use transparency; solid borders don't. This also helps when using images or multiple colors as backgrounds: solid border colors don't work well on backgrounds other than the ones they were designed for.

**Do not apply this to dividers** (`border-b`, `border-t`, side borders) or any border whose purpose is layout separation rather than element depth. Those should stay as borders.

#### Shadow as Border (Light Mode)

The shadow is comprised of three layers. The first acts as a 1px border ring, the second adds subtle lift, and the third provides ambient depth:

```css
:root {
  --shadow-border:
    0px 0px 0px 1px oklch(0 0 0 / 0.06),
    0px 1px 2px -1px oklch(0 0 0 / 0.06),
    0px 2px 4px 0px oklch(0 0 0 / 0.04);
  --shadow-border-hover:
    0px 0px 0px 1px oklch(0 0 0 / 0.08),
    0px 1px 2px -1px oklch(0 0 0 / 0.08),
    0px 2px 4px 0px oklch(0 0 0 / 0.06);
}
```

#### Shadow as Border (Dark Mode)

In dark mode, simplify to a single white ring, since layered depth shadows aren't visible on dark backgrounds:

```css
/* Dark mode: adapt to whatever setup the project uses
   (prefers-color-scheme, class, data attribute, etc.) */
--shadow-border: 0 0 0 1px oklch(1 0 0 / 0.08);
--shadow-border-hover: 0 0 0 1px oklch(1 0 0 / 0.13);
```

#### Usage with Hover Transition

Apply the variable and add `transition-[box-shadow]` for a smooth hover:

```css
.card {
  box-shadow: var(--shadow-border);
  transition-property: box-shadow;
  transition-duration: 150ms;
  transition-timing-function: ease-out;
}

.card:hover {
  box-shadow: var(--shadow-border-hover);
}
```

#### When to Use Shadows vs. Borders

| Use shadows | Use borders |
| --- | --- |
| Cards, containers with depth | Dividers between list items |
| Buttons with bordered styles | Table cell boundaries |
| Elevated elements (dropdowns, modals) | Form input outlines (for accessibility) |
| Elements on varied backgrounds | Hairline separators in dense UI |
| Hover/focus states for lift effect | |

### Image Outlines

Add a subtle `1px` outline with low opacity to images. This creates consistent depth, especially in design systems where other elements use borders or shadows.

#### Color rules (non-negotiable)

- **Light mode**: pure black, `oklch(0 0 0 / 0.1)`.
- **Dark mode**: pure white, `oklch(1 0 0 / 0.1)`.
- Never use a near-black or near-white from the project palette (e.g. slate-900, zinc-900, `#0a0a0a`, `#111827`, `#f5f5f7`). Tinted outlines pick up the surrounding surface color and read as dirt on the image edge.
- Never match the outline to the project's accent or ink color. The outline is a neutral separator, not a themed element.

#### Light Mode

```css
img {
  outline: 1px solid oklch(0 0 0 / 0.1);
  outline-offset: -1px; /* draw the ring just inside the image edge */
}
```

#### Dark Mode

```css
img {
  outline: 1px solid oklch(1 0 0 / 0.1);
  outline-offset: -1px;
}
```

#### Tailwind with Dark Mode

```tsx
<img
  className="outline outline-1 -outline-offset-1 outline-black/10 dark:outline-white/10"
  src={src}
  alt={alt}
/>
```

Use `outline-black/10` and `outline-white/10` specifically, not `outline-slate-*`, `outline-zinc-*`, `outline-neutral-*`, or any tinted scale.

**Why outline instead of border?** `outline` never affects layout (no added width or height at any offset), and `outline-offset: -1px` draws the ring just inside the image edge so it hugs the corner radius instead of sitting outside it.

---

## Animations

Interruptible animations, enter/exit transitions, contextual icon animations and scale on press.

### Interruptible Animations

Users change intent mid-interaction. If animations aren't interruptible, the interface feels broken.

#### CSS Transitions vs. Keyframes

| | CSS Transitions | CSS Keyframe Animations |
| --- | --- | --- |
| **Behavior** | Interpolate toward latest state | Run on a fixed timeline |
| **Interruptible** | Yes, retargets mid-animation | No, restarts from beginning |
| **Use for** | Interactive state changes (hover, toggle, open/close) | Staged sequences that run once (enter animations, loading) |
| **Duration** | Fixed; retargets the value mid-flight, not the timeline | Fixed timeline, restarts from the beginning |

```css
/* Good: interruptible transition for a toggle */
.drawer {
  transform: translateX(-100%);
  transition: transform 200ms ease-out;
}
.drawer.open {
  transform: translateX(0);
}

/* Clicking again mid-animation smoothly reverses, no jank */
```

```css
/* Bad: keyframe animation for interactive element */
.drawer.open {
  animation: slideIn 200ms ease-out forwards;
}

/* Closing mid-animation snaps or restarts, feels broken */
```

**Rule:** Always prefer CSS transitions for interactive elements. Reserve keyframes for one-shot sequences.

### Enter Animations: Split and Stagger

Use this pattern for infrequent staged entrances where sequence helps communicate hierarchy, such as the first load of a page hero, success state, or empty state. Break a large container into semantic chunks and animate each individually. Stagger only where the entrance is infrequent; anything the user triggers often should animate as one container, or not at all.

#### Step by Step

1. **Split** into logical groups (title, description, buttons)
2. **Stagger** with ~100ms delay between groups
3. **For titles**, consider splitting into individual words with ~80ms stagger
4. **Combine** `opacity`, `blur`, and `translateY` for the enter effect

#### Code Example

```tsx
// Motion (Framer Motion): staggered enter
function PageHeader() {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{
        visible: { transition: { staggerChildren: 0.1 } },
      }}
    >
      <motion.h1
        variants={{
          hidden: { opacity: 0, y: 12, filter: "blur(4px)" },
          visible: { opacity: 1, y: 0, filter: "blur(0px)" },
        }}
      >
        Welcome
      </motion.h1>

      <motion.p
        variants={{
          hidden: { opacity: 0, y: 12, filter: "blur(4px)" },
          visible: { opacity: 1, y: 0, filter: "blur(0px)" },
        }}
      >
        A description of the page.
      </motion.p>

      <motion.div
        variants={{
          hidden: { opacity: 0, y: 12, filter: "blur(4px)" },
          visible: { opacity: 1, y: 0, filter: "blur(0px)" },
        }}
      >
        <Button>Get started</Button>
      </motion.div>
    </motion.div>
  );
}
```

#### CSS-Only Stagger

```css
.stagger-item {
  opacity: 0;
  transform: translateY(12px);
  filter: blur(4px);
  animation: fadeInUp 400ms ease-out forwards;
}

.stagger-item:nth-child(1) { animation-delay: 0ms; }
.stagger-item:nth-child(2) { animation-delay: 100ms; }
.stagger-item:nth-child(3) { animation-delay: 200ms; }

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}
```

### Exit Animations

Exit animations should be softer and less attention-grabbing than enter animations. The user's focus is moving to the next thing; don't fight for attention.

#### Subtle Exit (Recommended)

```tsx
// Small fixed translateY: indicates direction without drama
<motion.div
  exit={{
    opacity: 0,
    y: -12,
    filter: "blur(4px)",
    transition: { duration: 0.15, ease: "easeOut" },
  }}
>
  {content}
</motion.div>
```

#### Full Exit (When Context Matters)

```tsx
// Slide fully out: use when spatial context is important
// (e.g., a card returning to a list, a drawer closing)
<motion.div
  exit={{
    opacity: 0,
    x: "-100%",
    transition: { duration: 0.2, ease: "easeOut" },
  }}
>
  {content}
</motion.div>
```

#### Good vs. Bad

```css
/* Good: subtle exit */
.item-exit {
  opacity: 0;
  transform: translateY(-12px);
  transition: opacity 150ms ease-out, transform 150ms ease-out;
}

/* Bad: dramatic exit that steals focus */
.item-exit {
  opacity: 0;
  transform: translateY(-100%) scale(0.5);
  transition: all 400ms ease-out;
}

/* Sometimes correct: remove immediately when motion adds no context */
.item-exit {
  display: none;
}
```

**Key points:**
- Use a small fixed `translateY` (e.g., `-12px`) instead of the full container height
- Keep some directional movement to indicate where the element went
- Exit duration should be shorter than enter duration (150ms vs 300ms)
- Use a subtle exit when it preserves spatial context. Remove immediately when motion adds no information, the interaction repeats frequently, or reduced motion is requested.

### Contextual Icon Animations

When icons appear or disappear contextually (on hover, on state change), animate them with `opacity`, `scale`, and `blur` rather than just toggling visibility.

#### Motion Example

This example uses the `motion` package. If the project instead has `framer-motion`, import the same APIs from `"framer-motion"`; never mix an installed package with the other package's import path.

```tsx
import { AnimatePresence, motion } from "motion/react";

function IconButton({ isActive, icon: Icon }) {
  return (
    <button>
      <AnimatePresence mode="popLayout">
        <motion.span
          key={isActive ? "active" : "inactive"}
          initial={{ opacity: 0, scale: 0.25, filter: "blur(4px)" }}
          animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
          exit={{ opacity: 0, scale: 0.25, filter: "blur(4px)" }}
          transition={{ type: "spring", duration: 0.3, bounce: 0 }}
        >
          <Icon />
        </motion.span>
      </AnimatePresence>
    </button>
  );
}
```

#### CSS Transition Approach (No Motion)

If the project doesn't use Motion (Framer Motion), keep both icons in the DOM and cross-fade them with CSS transitions. Because neither icon unmounts, both enter and exit animate smoothly.

The trick: one icon is absolutely positioned on top of the other. Toggling state cross-fades them: the entering icon scales up from `0.25` while the exiting icon scales down to `0.25`, both with opacity and blur.

```tsx
function IconButton({ isActive, ActiveIcon, InactiveIcon }) {
  return (
    <button>
      <div className="relative">
        <div
          className={cn(
            "absolute inset-0 flex items-center justify-center",
            "transition-[opacity,filter,scale] duration-300",
            "ease-[cubic-bezier(0.2,0,0,1)]",
            isActive
              ? "scale-100 opacity-100 blur-0"
              : "scale-[0.25] opacity-0 blur-[4px]"
          )}
        >
          <ActiveIcon />
        </div>
        <div
          className={cn(
            "transition-[opacity,filter,scale] duration-300",
            "ease-[cubic-bezier(0.2,0,0,1)]",
            isActive
              ? "scale-[0.25] opacity-0 blur-[4px]"
              : "scale-100 opacity-100 blur-0"
          )}
        >
          <InactiveIcon />
        </div>
      </div>
    </button>
  );
}
```

The non-absolute icon (InactiveIcon) defines the layout size. The absolute icon (ActiveIcon) overlays it without affecting flow.

#### Choosing Between Motion and CSS

| | Motion (Framer Motion) | CSS transitions (both icons in DOM) |
| --- | --- | --- |
| **Enter animation** | Yes | Yes |
| **Exit animation** | Yes (via `AnimatePresence`) | Yes (cross-fade, icon never unmounts) |
| **Spring physics** | Yes | No, use `cubic-bezier(0.2, 0, 0, 1)` as approximation |
| **When to use** | Project already uses `motion` or `framer-motion` | No motion dependency, or keeping bundle small |

**Rule:** Check the project's `package.json`. Import from `"motion/react"` when `motion` is installed, or from `"framer-motion"` when `framer-motion` is installed. If both exist, follow the imports already used by the component or its nearest peers. If neither is present, use the CSS cross-fade pattern; don't add a dependency just for icon transitions.

#### When to Animate Icons

| Animate | Don't animate |
| --- | --- |
| Icons that appear on hover (action buttons) | Static navigation icons |
| State change icons (play → pause, like → liked) | Decorative icons |
| Icons in contextual toolbars | Icons that are always visible |
| Loading/success state indicators | Icon labels (text next to icon) |

**Important:** Always use exactly these values for contextual icon animations; do not deviate:
- `scale`: `0.25` → `1` (never use `0.5` or `0.6`)
- `opacity`: `0` → `1`
- `filter`: `"blur(4px)"` → `"blur(0px)"`
- `transition`: `{ type: "spring", duration: 0.3, bounce: 0 }`; **bounce must always be `0`**, never `0.1` or any other value

### Scale on Press

A subtle scale-down on click gives buttons tactile feedback. Always use `scale(0.96)`. Never use a value smaller than `0.95`: anything below feels exaggerated. Use CSS transitions for interruptibility, so that if the user releases mid-press, it smoothly returns.

Not every button needs this. Add a `static` prop to your button component that disables the scale effect when the motion would be distracting.

#### CSS Example

```css
.button {
  transition-property: scale;
  transition-duration: 150ms;
  transition-timing-function: ease-out;
}

.button:active {
  scale: 0.96;
}
```

#### Tailwind Example

```tsx
<button className="transition-transform duration-150 ease-out active:scale-[0.96]">
  Click me
</button>
```

#### Motion Example

```tsx
<motion.button whileTap={{ scale: 0.96 }}>
  Click me
</motion.button>
```

#### Static Prop Pattern

Extract the scale class into a variable and conditionally apply it based on a `static` prop:

```tsx
const tapScale = "active:not-disabled:scale-[0.96]";

function Button({ static: isStatic, className, children, ...props }) {
  return (
    <button
      className={cn(
        "transition-transform duration-150 ease-out",
        !isStatic && tapScale,
        className,
      )}
      {...props}
    >
      {children}
    </button>
  );
}

// Usage
<Button>Click me</Button>           {/* scales on press */}
<Button static>Submit</Button>       {/* no scale */}
```

### Skip Animation on Page Load

Use `initial={false}` on `AnimatePresence` to prevent enter animations from firing on first render. Elements that are already in their default state shouldn't animate in on page load, only on subsequent state changes.

#### When It Works

```tsx
// Good: icon doesn't animate in on mount, only on state change
<AnimatePresence initial={false} mode="popLayout">
  <motion.span
    key={isActive ? "active" : "inactive"}
    initial={{ opacity: 0, scale: 0.25, filter: "blur(4px)" }}
    animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
    exit={{ opacity: 0, scale: 0.25, filter: "blur(4px)" }}
  >
    <Icon />
  </motion.span>
</AnimatePresence>
```

Works well for: icon swaps, toggles, tabs, segmented controls: anything that has a default state on page load.

#### When It Breaks

Don't use `initial={false}` when the component relies on its `initial` prop to set up a first-time enter animation, like a staggered page hero or a loading state. In those cases, removing the initial animation skips the entire entrance.

```tsx
// Bad: initial={false} would skip the staggered page enter entirely
<AnimatePresence initial={false}>
  <motion.div initial="hidden" animate="visible" variants={...}>
    ...
  </motion.div>
</AnimatePresence>
```

Verify the component still looks right on a full page refresh before applying this.

### Scope

Everything in this section assumes the animation belongs. Whether it belongs at all — what it costs the user at its trigger frequency, and whether it should be shortened, made one-sided, or deleted — is a separate question, and the answer defaults to no.

Honoring `prefers-reduced-motion` is covered by the Accessibility principles above; apply it to every animation in this section.

---

## Icons

Icon weight, states, sizing, and direction: the details that make icons sit naturally in an interface.

### Match Icon Stroke to Text Weight

An icon next to text should carry the same optical weight as the text, or the pair looks mismatched: a hairline icon beside semibold text reads as broken, a heavy icon beside regular text shouts.

| Adjacent text | Icon stroke width (24px grid) |
| --- | --- |
| Regular (400), 14–16px | `1.5px` |
| Medium/Semibold (500–600) | `2px` |
| Bold (700), or emphasized standalone | `2.5px` |

```html
<!-- Good: stroke tuned to the label weight -->
<button class="flex items-center gap-2 font-semibold">
  <PlusIcon stroke-width="2" class="size-4" />
  New project
</button>

<!-- Bad: default 1.5px stroke against a bold label -->
<button class="flex items-center gap-2 font-bold">
  <PlusIcon stroke-width="1.5" class="size-4" />
  New project
</button>
```

Two related consistency rules:

- **One optical strategy per surface.** Do not mix icon libraries with incompatible stroke conventions on one toolbar. If the chosen library intentionally supports stroke variants, match them to adjacent text as above; otherwise preserve the set's native stroke and use size or color for emphasis.
- **Size icons relative to the text's cap height**, typically `1em`–`1.25em` when inline with text, so the pair scales together.

### One SVG, Recolored per State

Never ship separate icon assets for default/hover/selected/disabled states. Use a single SVG drawn with `currentColor` and let CSS state drive the color:

```html
<!-- Good: one asset, states are CSS -->
<svg fill="none" stroke="currentColor" stroke-width="2">…</svg>
```

```css
.icon-button { color: oklch(0.552 0.016 285.938); }
.icon-button:hover { color: oklch(0.21 0.006 285.885); }
.icon-button[aria-pressed="true"] { color: oklch(0.623 0.188 259.815); }
.icon-button:disabled { opacity: 0.4; }
```

```html
<!-- Tailwind -->
<button class="text-zinc-500 hover:text-zinc-900 aria-pressed:text-blue-600 disabled:opacity-40">
  <BookmarkIcon />
</button>
```

Hardcoded fills inside the SVG (`fill="#666"`) break this; strip them to `currentColor` when importing icons.

### Outline Default, Fill Active

When an icon set offers outline and filled variants, use them as a state pair, not interchangeably:

| Variant | Use for |
| --- | --- |
| Outline | Default state: toolbars, list rows, inline with text |
| Fill | Selected/active state: the active tab, a toggled bookmark, a liked heart |

```tsx
// Good: variant communicates state
<TabIcon variant={isActive ? "solid" : "outline"} />

// Bad: filled icons everywhere, so the active tab has no state signal
<TabIcon variant="solid" />
```

The swap between variants is a contextual icon animation; use the exact cross-fade values in [Animations](#animations).

### Design at Render Size

An icon that looks great at 48px can collapse into mush at 16px. Details that read at large sizes (thin interior lines, tight counters, fine texture) blur or alias when small.

- Test every icon at the smallest size it will render (often `16px`); it must stay recognizable there.
- Prefer simplified glyphs for small contexts over scaling down detailed artwork.
- Keep icons on the pixel grid at their render size: a 16px icon drawn on a 24px grid with fractional scaling renders soft. Use the icon set's native grid sizes (`16`, `20`, `24`) rather than arbitrary scales.
- Always SVG, never raster, so the same asset stays crisp at every density.

### Icons in RTL

Under `dir="rtl"`, flip icons whose meaning is tied to reading direction, and leave the rest alone:

| Flip | Don't flip |
| --- | --- |
| Back/forward arrows, chevrons in navigation | Logos and brand marks |
| Text-block glyphs (alignment, lists, indent) | Checkmarks |
| Speaker/volume waves (emanate in reading direction) | Physical objects: clocks, cups, pencils |
| "Send" style directional glyphs | Media playback (play/rewind refer to tape direction, convention keeps them LTR) |

```css
/* Good: mirror only direction-dependent icons */
[dir="rtl"] .icon-directional {
  scale: -1 1;
}
```

```html
<!-- Tailwind -->
<ChevronRightIcon class="icon-directional rtl:-scale-x-100" />
```

Analyze composite icons part by part: a badge or slash overlay may keep its position even when the base glyph flips. Accessible names for icon-only buttons are covered by the Accessibility principles above.

---

## Performance

Transition specificity and GPU compositing hints.

### Transition Only What Changes

Never use `transition: all` or Tailwind's `transition-all`. Always specify the exact properties that change. (Tailwind's bare `transition` maps to a curated default list of colors, opacity, shadow and transforms, not to `all`; still prefer naming exactly what changes.)

#### Why

- `transition: all` forces the browser to watch every property for changes
- Causes unexpected transitions on properties you didn't intend to animate (colors, padding, shadows)
- Prevents browser optimizations

#### CSS Example

```css
/* Good: only transition what changes */
.button {
  transition-property: scale, background-color;
  transition-duration: 150ms;
  transition-timing-function: ease-out;
}

/* Bad: transition everything */
.button {
  transition: all 150ms ease-out;
}
```

#### Tailwind

```tsx
// Good: explicit properties
<button className="transition-[scale,background-color] duration-150 ease-out">

// Bad: transition all
<button className="transition-all duration-150 ease-out">
```

#### Tailwind `transition-transform` Note

`transition-transform` in Tailwind maps to `transition-property: transform, translate, scale, rotate`, so it covers all transform-related properties, not just `transform`. Use this when you're only animating transforms. For multiple non-transform properties, use the bracket syntax: `transition-[scale,opacity,filter]`.

### Use `will-change` Sparingly

`will-change` hints the browser to pre-promote an element to its own GPU compositing layer. Without it, the browser promotes the element only when the animation starts; that one-time layer promotion can cause a micro-stutter on the first frame.

This particularly helps when an element is changing `scale`, `rotation`, or moving around with `transform`. For other properties, it doesn't help much: the browser can't composite them on the GPU anyway.

#### Rules

```css
/* Good: specific property that benefits from GPU compositing */
.animated-card {
  will-change: transform;
}

/* Good: multiple compositor-friendly properties */
.animated-card {
  will-change: transform, opacity;
}

/* Bad: never use will-change: all */
.animated-card {
  will-change: all;
}

/* Bad: properties that can't be GPU-composited anyway */
.animated-card {
  will-change: background-color, padding;
}
```

#### Useful Properties

| Property | GPU-compositable | Worth using `will-change` |
| --- | --- | --- |
| `transform` | Yes | Yes |
| `opacity` | Yes | Yes |
| `filter` (blur, brightness) | Yes | Yes |
| `clip-path` | Newer Chromium only | Rarely; not reliable cross-browser |
| `top`, `left`, `width`, `height` | No | No |
| `background`, `border`, `color` | No | No |

#### When to Skip

Modern browsers are already good at optimizing on their own. Only add `will-change` when you notice first-frame stutter; Safari in particular benefits from it. Don't add it preemptively to every animated element; each extra compositing layer costs memory.
