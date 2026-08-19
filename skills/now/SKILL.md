---
name: now
description: "Compose evidence-backed sales pages, lessons, technical explainers, feedback surfaces, dashboards, and document collections as one deterministic RenderSpec component graph, then render, QA, publish, or attach the HTML."
allowed-tools: Read Write Bash Glob Grep
---

# /now — Composable Deterministic Pages

Build one canonical RenderSpec component graph and render it to single-file HTML with lev.now. Fonts and optional diagram/chart runtimes may load from configured CDNs. Never route content to a separate lesson, brief, reader, sales, or feedback schema. Those are recipes assembled from the same components.

## Commands

| Pattern | Operation |
|---|---|
| `/now <topic>` | Research/decompose, compose RenderSpec, render, open, QA |
| `/now publish <topic>` | Compose, QA, and publish to here.now |
| `/now attach <topic> --path <path>` | Compose, publish, and link to a handle path |
| `/now render <file.json>` | Render an existing RenderSpec deterministically |
| `/now reader <dir> [-o out]` | Materialize Markdown files, compile them into ordinary document/navigation components, and render compatibility paths |

## Required Workflow

1. Read `plugins/now/src/prompts/spec-generator.md` every time. Treat `plugins/now/src/openlang/component-catalog.ts` as source truth when the prose and catalog disagree.
2. Decompose the request into independently testable content requirements before selecting components:
   - Who is the audience, what do they already know, and what must change after reading?
   - What are the load-bearing claims, and what source or repo evidence supports each?
   - What must be read in sequence, what should be scannable, and what is optional depth?
   - Which interactions are required: navigation, pager, feedback, link, or capability-backed action?
   - Which component satisfies each requirement? A `document` may live anywhere, including inside a lesson, brief, sales page, or mixed visual explainer.
3. Apply Teach-quality authoring:
   - Ground teaching in the user's mission and current ability; do not reteach what they already know.
   - Keep a lesson focused on one tangible win. Teach only the knowledge needed to perform the skill.
   - Prefer high-trust primary sources and cite load-bearing claims.
   - Build storage strength, not recognition: add retrieval practice, a real task, or feedback when learning is the goal.
   - Keep reference material compressed and scannable; use full documents for durable reading and cards/callouts for orientation.
4. Select components per requirement, then create the RenderSpec at `~/.agents/levnow/{topic-slug}.json`. Do not create `{ mode: "reader" }`; that shape is compatibility intake only.
5. Render:
   ```bash
   npx tsx plugins/now/src/cli.ts ~/.agents/levnow/{slug}.json --output ~/.agents/levnow/{slug}.html
   ```
   Use `--show-source` only for explicit renderer debugging.
6. Open and QA locally. For shared, published, attached, or visually judged pages, use browser inspection at desktop and mobile sizes.
7. For publish, QA a clean build and run:
   ```bash
   bash ~/.claude/skills/here-now/scripts/publish.sh ~/.agents/levnow/{slug}.html --title "lev.now — {topic}" --client lev-now
   ```
   Add `--handle-path {path}` for attach.

## Composition Recipes, Not Routes

| Intent | Typical requirements and components |
|---|---|
| Sales letter / visual explainer | Claim sequence, differentiation, proof, objections, action; usually hero + document/text + cards/tables/diagrams + testimonial + action |
| Teach-style content | Mission, current knowledge, one win, explanation, worked example, retrieval or practice, feedback, primary source; usually document + code/diagram + action or feedback |
| Explainer brief / technical | Verdict, boundaries, evidence, mechanics, risks, next move; usually document + diagram/code/table + callout, optionally navigation |
| Feedback | Context beside the decision, stable response IDs, explicit choices, optional action; use existing content components + feedback rather than a feedback-only page type |
| Multi-document browsing | Sidebar section + navigation list + routed documents + pager; folder intake compiles exactly this graph |

Recipes may be mixed. A technical lesson can include a sales-quality value proposition; a feedback surface can include a full document; a sales letter can include technical evidence.

## Visual Explainer Link

When visual encoding is load-bearing—architecture maps, dense comparisons, causal flows, spatial explanations, or custom interaction—also read [`../visual-explainer/SKILL.md`](../visual-explainer/SKILL.md). That skill supplies visual research and art-direction methods. Bring its output back into this same RenderSpec graph using diagrams, charts, tables, sections, and other catalog components. Use `custom-html` only when the component graph cannot express the required visual.

## Component and Runtime Boundaries

- `RenderSpec` is the canonical static IR. `document`, `navigation`, `action`, feedback, and existing visual/layout elements are peers in its flat element map.
- Teach workspace artifacts such as a mission, annotated resources, learning record, and glossary are source/state files, not render schemas or routes. Materialize their relevant content into `objective`, `source-list`, `exercise`, `evidence`, `document`, or other ordinary components.
- Use `objective` for one observable learning outcome, `source-list` for annotated sources, and `exercise` for retrieval or real-world practice. Use `evidence` for claim-level provenance, `decision` for a ruling and next condition, `proof` for bounded support plus limitations, and `testimonial` for attributed document voice.
- Use `feedback` with `variant: "quiz"` when recommendations would reveal an answer before the learner attempts it; the renderer reveals recommendations only after a choice.
- OpenLang is a compact authoring projection: OpenLang -> typed AST -> RenderSpec. Its catalog drives kind admission, allowed attributes, and prompt help; OpenUI concepts are used without adding an OpenUI runtime.
- An `action` with `capabilityRef` is declarative. The renderer emits `lev:action`; it never invokes tools, evaluates code, or performs network requests.
- FlowMind/Poly and the interaction host resolve capability references. Oracle Open Agent Spec inputs compile behind this boundary into capability cards/operations; they are not a renderer dependency.
- AgentPing may render live packet surfaces. Do not move Lev DNA semantics or execution policy into AgentPing components.

## Visual QA Gate

For professional or shared output, render and inspect at 1440px and 390px; for layout changes also check 1024, 900, and 768px.

```bash
npx tsx plugins/now/src/cli.ts ~/.agents/levnow/{slug}.json --output ~/.agents/levnow/{slug}.html --qa --qa-width 1440
npx tsx plugins/now/src/cli.ts ~/.agents/levnow/{slug}.json --output ~/.agents/levnow/{slug}.html --qa --qa-width 390
```

Fail and revise when:

- The first viewport hides the page's useful content or hierarchy is unclear.
- Prose, labels, code, navigation, tables, diagrams, or actions clip, collide, become illegible, or overflow at any target width.
- Routed documents, sidebar links, previous/next, feedback persistence, or action declarations do not work under real interaction.
- The page has visual polish but cannot trace each audience requirement and load-bearing claim to a rendered component.

## Quick Reference

- Components: hero, section, card, text, document, navigation, action, feedback, objective, source-list, exercise, evidence, decision, proof, testimonial, data-table, code-block, timeline, diagram, chart, custom-html, inline.
- Section layouts: default, card-grid, kpi-row, pipeline, comparison, diff-panels, collapsible, full-width, sidebar, asymmetric, stacked, deck, stepper.
- Themes: deep-blue-gold, terracotta-sage, teal-slate, rose-cranberry, amber-emerald, midnight-ink, matrix-temple, obsidian-monolith, fleet-deck, moat.
- Effects: grid-dots, grid-lines, card-glow, glass, hero-gradient, noise, title-underline.

## Report

After non-published output, provide the local HTML path plus a brief mapping from requirements to components and the QA evidence. For published output, report only the published URL.
