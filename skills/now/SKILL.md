---
name: now
description: "Deterministic lev.now renders JSON specs to styled HTML with publish and attach. Use when user wants dashboards, reports, timelines, or rich pages instead of large markdown tables."
argument-hint: '[publish|attach|render] <topic or spec.json> [--theme preset] [--path handle-path]'
allowed-tools: Read Write Bash Glob Grep
---

# /now — Fast Deterministic Page Rendering

You generate beautiful self-contained HTML pages from a JSON spec using the lev.now template engine.

## Modes

| Pattern | Mode |
|---|---|
| `/now <topic>` | Generate JSON spec → render → open |
| `/now publish <topic>` | Generate + publish to here.now |
| `/now attach <topic> --path <path>` | Generate + publish + link to handle path |
| `/now render <file.json>` | Render existing spec (pure deterministic) |
| `/now render <file.json> publish` | Render + publish |

## How to Generate

1. **Read the spec generator guide** at `plugins/lev-now/src/prompts/spec-generator.md` EVERY TIME. It has the content-type behavior tree, all 11 element types, 13 section variants, effect knobs, and design principles.

2. **Classify the content** using the behavior tree in the guide:
   - Technical doc → sidebar-toc layout, teal-slate, code blocks
   - Dashboard → kpi-row, charts, teal-slate or deep-blue-gold
   - Sales/marketing → centered hero, CTA, card-glow, warm theme
   - Comparison → full-width tables, status badges, amber-emerald
   - Presentation → deck variant (scroll-snap slides)
   - Walkthrough → stepper variant (prev/next steps)
   - Live monitor → set `meta.refresh: 300` for auto-reload

3. **Generate the RenderSpec JSON** and save to `~/.agents/levnow/{topic-slug}.json`

4. **Render:**
   ```bash
   npx tsx plugins/lev-now/src/cli.ts ~/.agents/levnow/{slug}.json --show-source --output ~/.agents/levnow/{slug}.html
   ```

5. **Open:** `open ~/.agents/levnow/{slug}.html`

6. **If publish:** `bash ~/.claude/skills/here-now/scripts/publish.sh ~/.agents/levnow/{slug}.html --title "lev.now — {topic}" --client lev-now`

7. **If attach:** add `--handle-path {path}` to publish command.

## Quick Reference (read the guide for full details)

**11 Element Types:** hero (with optional CTA buttons), section, card (10 variants incl. testimonial), text, data-table, code-block, timeline, diagram, chart, custom-html, inline

**13 Section Variants:** default, card-grid, kpi-row, pipeline, comparison, diff-panels, collapsible, full-width, sidebar, asymmetric, stacked, deck (slides), stepper (walkthrough)

**2 Page Layouts:** default, sidebar-toc (`meta.layout: "sidebar-toc"`)

**7 Effect Knobs:** grid-dots, grid-lines, card-glow, glass, hero-gradient, noise, title-underline — themes auto-include defaults, override with `meta.effects`

**6 Themes:** deep-blue-gold (dark editorial), teal-slate (dark technical), midnight-ink (dark blueprint), terracotta-sage (light warm), rose-cranberry (light refined), amber-emerald (light data)

**Special Features:**
- Tables with 5+ cols get fullscreen portal toggle (zoom, pan, save)
- Diagrams get fullscreen portal with Ctrl+scroll zoom + drag pan + SVG save
- Cards with children get click-to-expand detail overlays
- `meta.refresh: N` adds auto-reload for live dashboards
- KPI integer values animate from 0 on scroll

## Report

After rendering, describe the **design choices** — not just stats:
- Theme + why it fits the content
- Layout structure and content type classification
- Key visual elements (which of the 11 types used, which variants)
- Render time + element count (brief)

**If the command was a publish:** Report ONLY the published URL. Do NOT show the local `~/.agents/levnow/*.html` path — the local file is an intermediate artifact, not the deliverable. The user follows the published link, not the local file.

**If the command was NOT a publish:** Show the local path (it IS the deliverable).
