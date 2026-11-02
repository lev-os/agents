---
name: creative
skill_type: router
description: Use when work is about how something looks, moves or is shown: UI, screens, landing pages, AI-looking UI to unslop, mock product shots, motion, video, diagrams, charts, pages, slides or images. Also when a UX task reaches visual design.
---

# Creative

Creative is the design hub. Name the artifact the user wants, pick **one** owner
from the table, load that skill, and produce the artifact. Add a second skill
only when the work crosses into its row (for example, a landing page that also
needs a hero film). The hub routes; the owner does the work.

Top-level skills load by name. Packages live in `skills-db/creative/` and load
by path; the full list is the [package index](../../skills-db/creative/README.md).

## Route

| The user wants | Owner | Load |
| --- | --- | --- |
| Research, personas, journeys, flows, wireframes, page structure, onboarding audit, CLI UX | ux | [ux](../ux/SKILL.md) |
| Build, review, polish or harden product UI; design systems and DESIGN.md; native screens | impeccable | [impeccable](../impeccable/SKILL.md) |
| A screen that looks vibecoded or AI-made, made into a designed screen | unslop | [unslop](../../skills-db/creative/unslop/SKILL.md) |
| A new landing page or portfolio with a strong visual direction | taste-skill | [taste-skill](../taste-skill/SKILL.md) |
| Mock product UI for marketing: hero stills, feature cards, cursor demos, bento grids | stageshow | [stageshow](../../skills-db/creative/stageshow/SKILL.md) |
| Product films, launch videos, explainers, logo stings, kinetic type | motion-graphics | [motion-graphics](../motion-graphics/SKILL.md) |
| Video in React code | remotion | [remotion-best-practices](../../skills-db/creative/remotion-best-practices/SKILL.md) |
| Architecture, workflow, sequence, data-flow or state diagrams | archify | [archify](../archify/SKILL.md) |
| Charts, stat tiles, dashboards of data | dataviz | the host's `dataviz` skill |
| An evidence page, lesson, run review or dashboard page in lev.now, and publishing it | now | [now](../now/SKILL.md) |
| A `.pen` file or Pencil canvas | pencil | [pencil](../../skills-db/creative/pencil/SKILL.md) |
| Slides | pptx | [pptx presentations](../../skills-db/creative/aiuxplayground-pptx-presentations/SKILL.md) |
| Generated or edited images | nano-banana-pro | [nano-banana-pro](../../skills-db/creative/nano-banana-pro/SKILL.md) |
| Social share images | og-share-images | [og-share-images](../../skills-db/creative/og-share-images/SKILL.md) |
| Anything else (shaders, SwiftUI patterns, TUI, prompt libraries) | package index | [README](../../skills-db/creative/README.md) |

## Where two rows meet

- **Landing page.** taste-skill sets the direction for a new page. impeccable
  owns an existing product's page, using its persuade mode.
- **Slop.** unslop owns AI-looking screens. AI-looking code goes to
  `ai-slop-cleaner`, AI-sounding prose goes to `writing`; neither is design.
- **Animation.** Motion inside a screen (hover, transitions, micro-interactions)
  is impeccable `animate`. A film or a loop someone watches is motion-graphics.
  A mock product demo with a cursor is stageshow.
- **Audit.** A product-quality or onboarding scorecard is ux `--craft`. A visual
  and code audit of screens is impeccable `audit` or `critique`.
- **Page versus chart versus diagram.** now owns the page; it loads dataviz for
  each chart and archify for each diagram it contains.

## Keep

Keep the user's brief, authority and product evidence. Produce the requested
artifact, not only a report. Keep each package's license, credit and source
status. A package listed here is routed, not qualified: imported packages stay
unaudited until checked. Run no installer or outside change without its own
authorization; state a missing tool or source as a gap.
