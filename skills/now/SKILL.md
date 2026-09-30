---
name: now
description: "Compose evidence-backed sales pages, lessons, technical explainers, feedback surfaces, dashboards, and document collections as one deterministic RenderSpec component graph, then render, QA, publish, or attach the HTML."
allowed-tools: Read Write Bash Glob Grep
---

# /now — Composable Deterministic Pages

For ordinary pages, build one canonical RenderSpec component graph and render it to single-file HTML with lev.now. The live `--showcase` reference adapter below uses Lev UI components without compiling through RenderSpec. Fonts and optional diagram/chart runtimes may load from configured CDNs. Never route content to a separate lesson, brief, reader, sales, or feedback schema. Those are recipes assembled from the same components.

## Commands

| Pattern | Operation |
|---|---|
| `/now <topic>` | Research/decompose, compose RenderSpec, render, open, QA |
| `/now --showcase <topic>` | Build and prove a live reference implementation using Lev UI components |
| `/now publish <topic>` | Compose, QA, and publish to here.now |
| `/now attach <topic> --path <path>` | Compose, publish, and link to a handle path |
| `/now render <file.json>` | Render an existing RenderSpec deterministically |
| `/now reader <dir> [-o out]` | Materialize Markdown files, compile them into ordinary document/navigation components, and render compatibility paths |

## Showcase route

Use `--showcase` for an investor demonstration, live debugger, or working reference implementation. This adapter uses Lev UI components and does not compile through RenderSpec or target Storybook. Propose missing components explicitly; do not present them as already shipped.

1. Resolve audience, observable behavior, input provenance, live effects, and design model. Interview only for missing choices: live data, realistic source-backed reference data, or synthetic data? Which actions must actually execute? Reuse answers already supplied. Reference shaping is allowed; fabricated successful inference and fake live status are not.
2. Research current libraries for the requested medium using primary sources. Choose for visible impact and functional fit. Use actual graph engines and Archify rather than imitating a requested library with hand-drawn markup. Honor requested quality tiers for other media.
3. Use the requested design model through an available authenticated route and retain model/session evidence. Follow the applicable system prompt. Keep private repository context local unless its export is authorized; a generic design-only brief may guide presentation. Do not silently substitute a required model.
4. Reuse `plugins/now/showcase/` as the live React adapter; keep case source and provenance under `.lev/now/showcase/<slug>/`. Use `@lev-os/lev-ui` components and theme around real visualization engines. Record missing component proposals with behavior, reuse, and proof required; do not create another component catalog.
5. Route CLI inference through `core/exec`; use the existing FlowMind execution graph and typed observation/policy boundaries. Keep credentials server-side. WebSocket events must be actual ordered observations with run references. Reference simulations own isolated state; they do not mutate canonical work by implication.
6. Verify desktop/mobile layout, keyboard interaction, selection and drill-down, disconnection, cancellation, provider error/unknown, and the complete click-to-inference-to-observation-to-declared-branch path. Label snapshots, reference projections, replay, and live execution separately. Preserve exact checks, run references, screenshots, and remaining integration gaps.

Run the current reference adapter from the target project with `npx tsx plugins/now/src/cli.ts --showcase`.

A working showcase proves its inspected behavior, not every product integration. Report the accessible demo, selected libraries, requested-model evidence, verified interactions, and residual limits. Ordinary `/now` requests continue with the RenderSpec workflow below.

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
4. Select components per requirement, then create the RenderSpec at `.lev/now/{topic-slug}.json` under the target project root, with rendered HTML beside it. Honor explicit output paths; use the task workspace for projectless work. Do not create `{ mode: "reader" }`; that shape is compatibility intake only.
5. Render:
   ```bash
   npx tsx plugins/now/src/cli.ts .lev/now/{slug}.json --output .lev/now/{slug}.html
   ```
   Use `--show-source` only for explicit renderer debugging.
6. Open locally. Run QA only when the user passes `publish` or explicitly asks for QA; published pages still require desktop and mobile inspection. If the page has a `feedback` element, start the answer poller in the background right after opening it (see Collect Feedback Answers) instead of asking the user to paste JSON back.
7. For publish, QA a clean build and run:
   ```bash
   bash ~/.claude/skills/here-now/scripts/publish.sh .lev/now/{slug}.html --title "lev.now — {topic}" --client lev-now
   ```
   Add `--handle-path {path}` for attach.

## Composition Recipes, Not Routes

| Intent | Typical requirements and components |
|---|---|
| Sales letter / visual explainer | Claim sequence, differentiation, proof, objections, action; usually hero + document/text + cards/tables/diagrams + testimonial + action |
| Teach-style content | Mission, current knowledge, one win, explanation, worked example, retrieval or practice, feedback, primary source; usually document + code/diagram + action or feedback |
| Explainer brief / technical | Verdict, boundaries, evidence, mechanics, risks, next move; usually document + diagram/code/table + callout, optionally navigation |
| Explain diff (code change) | Background (deep, skippable) → intuition with toy data → literate code tour ordered by dependency → the change's own open ends → 5-question quiz; usually document + mermaid diagram + one `custom-html` interactive figure + stacked code-block steps + `feedback` variant `quiz` (every option gets `why`; wrong ones explain why not after the reveal) + source-list. No colored left-border accents. Reference: `plugins/now/examples/explain-diff.json` |
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

## Collect Feedback Answers

The feedback component saves answers in browser localStorage under `lev-now-feedback-<pageId>`. Brave, Chrome and Chromium persist that to a per-profile LevelDB, and `scripts/feedback-answers.py` (in this skill directory, Python standard library only) reads it from disk. It needs no server, debugging port or pasted JSON, and it covers `file://` pages and published here.now pages alike.

```bash
python3 scripts/feedback-answers.py .lev/now/{slug}.json --wait   # run as a background job
python3 scripts/feedback-answers.py .lev/now/{slug}.json          # read the current answers once
```

- `--wait` exits 0 once every feedback item has a choice or note and the answers have stayed unchanged for `--settle` seconds (default 20). The job's completion is the signal to continue: act on the answers without asking the user where they are.
- On `--timeout` (default 3600 s), it prints the partial answers and exits 2.
- Output lists each item's `choice` label, whether it was the `recommended` option, and any `note`. Treat notes as questions or constraints to answer before acting on that item's choice.
- The browser writes to disk a few seconds after a click, so a one-shot read immediately after the user answers can miss the last change.
- Stable `pageId`s matter: answers persist per `pageId`, and a re-rendered page with the same ID restores and reports earlier answers.

## Visual QA Gate

QA is opt-in. Do not run the QA command or browser inspection for an ordinary
`/now` render. Run this gate for `/now publish`, or when the user explicitly
requests QA, review, or responsive inspection.

For professional or shared output, render and inspect at 1440px and 390px; for layout changes also check 1024, 900, and 768px.

Authored graphs, RenderSpec JSON, and rendered HTML stay with the project in `.lev/now/`. Run commands from the target project root (resolve the renderer executable separately when it belongs to another checkout). QA screenshots and manifests go to a fresh system-temp directory via `LEV_NOW_QA_DIR`, including watch/refresh and other browser screenshot tools. Never place QA screenshots in `.lev/tmp/now`. Retain QA evidence only when needed, through the existing XDG artifact route with a project/task reference.

```bash
now_qa_dir="$(mktemp -d "${TMPDIR:-/tmp}/lev-now-qa.XXXXXX")"
LEV_NOW_QA_DIR="$now_qa_dir" npx tsx plugins/now/src/cli.ts .lev/now/{slug}.json --output .lev/now/{slug}.html --qa --qa-width 1440
LEV_NOW_QA_DIR="$now_qa_dir" npx tsx plugins/now/src/cli.ts .lev/now/{slug}.json --output .lev/now/{slug}.html --qa --qa-width 390
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
