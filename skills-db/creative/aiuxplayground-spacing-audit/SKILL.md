---
name: spacing-audit
description: Audit a Figma layout against a 4/8pt spacing system and flag or snap off-grid padding, gaps, and margins. Use in Figma Agent or Figma Make when spacing looks inconsistent, before developer handoff, or when asked to check, align, or standardize spacing.
---

# Spacing Audit

Check a layout against a 4/8pt spacing scale, report every value that is off the grid, and snap it to the nearest correct step. The goal is consistent, predictable rhythm that is easy to hand off and maintain.

## The scale

Base unit is 8. Use 4 only as a half-step for tight, component-internal spacing.

Allowed values: 0, 4, 8, 12, 16, 24, 32, 40, 48, 56, 64, 80, 96.

- 8, 16, 24, 32, 48, 64: structural spacing (section gaps, card padding, layout margins).
- 4, 12, 20: fine spacing inside a component (icon-to-label, chip padding, tight stacks).
- Anything not a multiple of 4 is off-grid and should be flagged.
- A multiple of 4 that is not a multiple of 8 at the layout level (e.g. section gap of 20 or 28) should be flagged as "consider 8pt step" but is not a hard error.

## What to check

Inspect auto-layout frames and spacing between elements:
- Padding inside frames (top, right, bottom, left).
- Item spacing / gap between children.
- Gaps between sections and between grouped blocks.
- Margins around content within a frame.

## How to audit

1. Walk the selected frame (or the whole page if nothing is selected) top-down.
2. For each spacing value, compare it against the allowed scale.
3. For each off-grid value, choose the nearest allowed step. When exactly between two steps, round to the one closer to the surrounding rhythm of that group.
4. Prefer consistency within a group over per-element correctness. If three cards use 14, 16, 16, align all three to 16.

## Rules

- Do not change layout structure, sizing behavior (hug/fill), content, or styling. Only adjust spacing values.
- Preserve intentional exceptions and do not flag them: 1px borders and hairlines, optical alignment offsets, values driven by hug/fill, and spacing set by a variable or token.
- If spacing is already bound to a variable or token, leave it and note it instead of overwriting.
- Round icon-to-label and other fine gaps to 4 or 8, not to larger steps.
- When a whole group is uniformly off-grid on purpose (e.g. a deliberate 6pt system), flag it once and ask before mass-changing.

## Output

1. Return an audit summary first, before changing anything:
   - Total elements checked.
   - A before / after list of every off-grid value, grouped by frame, in the form `Card padding: 14 -> 16`.
   - Any values you left untouched, with the reason (token, hairline, optical).
2. Apply the fixes only after showing the summary.
3. End with a one-line rhythm note: the dominant step the layout now uses (e.g. "layout now on an 8pt rhythm, fine spacing on 4pt").

## Do not

- Do not resize elements or reflow content to hit a number.
- Do not invent a new scale. Stick to the 4/8pt steps above.
- Do not touch corner radius, stroke, or type unless the user explicitly asks.
