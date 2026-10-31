---
name: now
description: "Compose evidence-backed pages (lessons, technical explainers, run reviews, sales letters, dashboards, feedback surfaces, document collections) as single-file HTML in the lev.now shell. By default, write a content-specific GenUI page, inspect it in light and dark at desktop and phone, and on request save it as a typed template. Render existing RenderSpec JSON, Markdown reader folders and live showcases on their own routes, and publish or attach pages to here.now."
allowed-tools: Read Write Bash Glob Grep
---

# /now — Evidence-backed pages

`/now <topic>` writes a GenUI page by default. You write body HTML whose structure comes from the content, and the CLI puts it in the lev.now page shell (theme preset, fonts, light/dark toggle, nav and footer). Every render gets visual QA before you report it. Fonts and optional diagram/chart runtimes may load from configured CDNs.

RenderSpec is the deterministic route: one canonical component graph rendered to single-file HTML. Never route content to a separate lesson, brief, reader, sales or feedback schema; those are recipes assembled from the same components. The live `--showcase` adapter uses Lev UI components without compiling through RenderSpec.

## Commands

| Pattern | Operation |
|---|---|
| `/now <topic>` | GenUI: plan the content, write a content-specific page, render, visual QA, open |
| `/now --genui <topic>` | The same as `/now <topic>`; kept for compatibility |
| `/now --genui --template <name> <data>` | Render a saved template with new data, checked against its contract |
| `/now publish <topic>` | Compose (GenUI unless the request picks RenderSpec), visual QA, publish to here.now |
| `/now attach <topic> --path <path>` | Compose, visual QA, publish, and link to a handle path |
| `/now render <file.json>` | Render an existing RenderSpec deterministically |
| `/now reader <dir> [-o out]` | Materialize Markdown files, compile them into ordinary document/navigation components, and render compatibility paths |
| `/now --showcase <topic>` | Build and prove a live reference implementation using Lev UI components |

**Choose the route.** Use the RenderSpec route when the user gives RenderSpec JSON, asks for a RenderSpec, a catalog component or a named recipe (for example explain diff), updates an existing `.lev/now/<slug>.json` page, or needs a RenderSpec-only feature: the `feedback` component with the answer poller, `--export`, or `--lev`. Use `reader` for a Markdown folder and `--showcase` for a live reference implementation. Every other request takes the GenUI route.

## Plan the content

Both routes start here. Decompose the request into independently testable content requirements before you choose a structure or components:

- Who is the audience, what do they already know, and what must change after reading?
- What are the load-bearing claims, and what source or repo evidence supports each?
- What is the object, and how does it work? The answer is the page's structure. For example, a run may be a loop and a change a diff; the content decides the form.
- What must be read in sequence, what should be scannable, and what is optional depth?
- Which interactions are required: navigation, pager, feedback, link, or capability-backed action?
- Is each piece of data real, reference (shaped from real source) or synthetic? The page labels it.

Apply Teach-quality authoring:

- Ground teaching in the user's mission and current ability; do not reteach what they already know.
- Keep a lesson focused on one tangible win. Teach only the knowledge needed to perform the skill.
- Prefer high-trust primary sources and cite load-bearing claims.
- Build storage strength, not recognition: add retrieval practice, a real task, or feedback when learning is the goal.
- Keep reference material compressed and scannable; use full documents for durable reading and compact blocks for orientation.

## GenUI route (default)

Run every command from the project root; files live under `.lev/now/genui/`.

1. **Choose.** Run `genui list` and name any saved templates in one line. If the user supplies `--template <name>`, or picks a saved template, read its contract and go to step 8. Otherwise write a new page.
2. **Design.** Read [references/genui-craft.md](references/genui-craft.md). It holds the house type, spacing, scoped-CSS and phone-layout rules, and the visual QA routine. Name the object and its mechanism, and draw that shape. Put the observed evidence first and keep dense execution detail behind tabs, drill-downs and `<details>`.
3. **Write.** Pick a lower-kebab slug. Write the page body to `.lev/now/genui/drafts/<slug>/source.html`: one `<style>` block, every selector under one page class, resets inside `:where()`, theme variables only (`var(--color-accent)`, `--color-accent-text`, `--color-surface-alt`, `--color-border`, `--color-text`, `--color-text-muted`, `--font-display`, `--font-mono`), so light and dark both work. Leave about 5.5rem of top space for the fixed nav.
4. **Render.**
   ```bash
   npx tsx plugins/now/src/cli.ts genui render <slug> --title "<title>" --theme <preset>
   ```
5. **Visual QA.** Run the routine in the reference on every distinct view and state, in light and dark at 1440 and 390. Fix `source.html`, re-render with the same `--title` and `--theme`, and compare the new images with the old ones until the gate passes. Then open the page:
   ```bash
   open -a "Brave Browser" .lev/now/<slug>.html
   ```
6. **Iterate.** Edit the saved `source.html` in place for each change the user asks for; do not start over. Re-run the original `genui render <slug>` command with the same `--title` and `--theme`, then the visual QA for the views the change touched. Once the draft has a contract, its title and theme come from that contract.
7. **Make it a template** (only when the user says so). Turn the content that should change into slots in the same `source.html`: `{{field}}` for one value, `{{#each list}}…{{/each}}` with `{{.}}` (list of values) or `{{column}}` (list of rows) inside. Put slots only in element text, such as `<h1>{{headline}}</h1>`. A slot inside a tag or any attribute, a comment, `<script>`, `<style>`, `<title>` or `<textarea>`, or right after a literal `<` is refused before anything is written. Keep links, data-basis labels and other attributes fixed in the template. Write beside it:
   - `contract.json`: `{ "title": "...", "theme": "<preset>", "fields": { "<name>": { "type": "string" | "number" | "boolean" } | { "type": "list", "items": "string" | { "<column>": "string" | "number" | "boolean" } } } }`
   - `data.json`: the current page's values, which must pass the contract.

   Re-render to check that the page looks the same, then promote. A name that already exists is refused; ask the user for a new name, never delete the old template.
   ```bash
   npx tsx plugins/now/src/cli.ts genui render <slug>
   npx tsx plugins/now/src/cli.ts genui promote <slug> <template-name>
   ```
8. **Render a template with new data.** Keep the template the user already supplied or chose in step 1, and read its fields from `genui list`, which prints every saved template with its fields as JSON. Only when no template is chosen yet, show the names and fields and let the user pick. Write the user's data as JSON that matches the contract. Do not invent values the user did not give; ask for missing fields. The CLI checks the data before it writes anything. New values change lengths, so run the visual QA on the output.
   ```bash
   npx tsx plugins/now/src/cli.ts genui use <template-name> --data <data.json> --output .lev/now/<page>.html
   ```

Every value is HTML-escaped. A contract is data only and never runs code. `sh plugins/now/examples/genui/demo.sh` shows the whole path in a scratch project.

## RenderSpec route

1. Read `plugins/now/src/prompts/spec-generator.md` every time. Treat `plugins/now/src/openlang/component-catalog.ts` as source truth when the prose and catalog disagree.
2. Plan the content (above), then choose the component that satisfies each requirement. A `document` may live anywhere, including inside a lesson, brief, sales page, or mixed visual explainer.
3. Create the RenderSpec at `.lev/now/{topic-slug}.json` under the target project root, with rendered HTML beside it. Honor explicit output paths; use the task workspace for projectless work. Do not create `{ mode: "reader" }`; that shape is compatibility intake only.
4. Render:
   ```bash
   npx tsx plugins/now/src/cli.ts .lev/now/{slug}.json --output .lev/now/{slug}.html
   ```
   Use `--show-source` only for explicit renderer debugging.
5. Run the Visual QA gate, then open the page locally. If the page has a `feedback` element, start the answer poller in the background right after opening it (see Collect Feedback Answers) instead of asking the user to paste JSON back.

### Composition recipes

| Intent | Typical requirements and components |
|---|---|
| Sales letter / visual explainer | Claim sequence, differentiation, proof, objections, action; usually hero + document/text + cards/tables/diagrams + testimonial + action |
| Teach-style content | Mission, current knowledge, one win, explanation, worked example, retrieval or practice, feedback, primary source; usually document + code/diagram + action or feedback |
| Explainer brief / technical | Verdict, boundaries, evidence, mechanics, risks, next move; usually document + diagram/code/table + callout, optionally navigation |
| Explain diff (code change) | Background (deep, skippable) → intuition with toy data → literate code tour ordered by dependency → the change's own open ends → 5-question quiz; usually document + mermaid diagram + one `custom-html` interactive figure + stacked code-block steps + `feedback` variant `quiz` (every option gets `why`; wrong ones explain why not after the reveal) + source-list. No colored left-border accents. Reference: `plugins/now/examples/explain-diff.json` |
| Feedback | Context beside the decision, stable response IDs, explicit choices, optional action; use existing content components + feedback rather than a feedback-only page type |
| Multi-document browsing | Sidebar section + navigation list + routed documents + pager; folder intake compiles exactly this graph |

Recipes may be mixed. A technical lesson can include a sales-quality value proposition; a feedback surface can include a full document; a sales letter can include technical evidence.

### Component and runtime boundaries

- `RenderSpec` is the canonical static IR. `document`, `navigation`, `action`, feedback, and existing visual/layout elements are peers in its flat element map.
- Teach workspace artifacts such as a mission, annotated resources, learning record, and glossary are source/state files, not render schemas or routes. Materialize their relevant content into `objective`, `source-list`, `exercise`, `evidence`, `document`, or other ordinary components.
- Use `objective` for one observable learning outcome, `source-list` for annotated sources, and `exercise` for retrieval or real-world practice. Use `evidence` for claim-level provenance, `decision` for a ruling and next condition, `proof` for bounded support plus limitations, and `testimonial` for attributed document voice.
- Use `feedback` with `variant: "quiz"` when recommendations would reveal an answer before the learner attempts it; the renderer reveals recommendations only after a choice.
- OpenLang is a compact authoring projection: OpenLang -> typed AST -> RenderSpec. Its catalog drives kind admission, allowed attributes, and prompt help; OpenUI concepts are used without adding an OpenUI runtime.
- An `action` with `capabilityRef` is declarative. The renderer emits `lev:action`; it never invokes tools, evaluates code, or performs network requests.
- FlowMind/Poly and the interaction host resolve capability references. Oracle Open Agent Spec inputs compile behind this boundary into capability cards/operations; they are not a renderer dependency.
- AgentPing may render live packet surfaces. Do not move Lev DNA semantics or execution policy into AgentPing components.

## Visual explainers

For architecture maps and technical flows, read [Archify](../archify/SKILL.md). For interactive charts and visual explanations, read the [visualization package](../../skills-db/creative/interactive-visualization-creator/SKILL.md). Bring the selected output back into the page: inline it in a GenUI `source.html`, or use RenderSpec diagrams, charts, tables and sections. In RenderSpec, use `custom-html` only when the component graph cannot express the required visual.

## Showcase route

Use `--showcase` for an investor demonstration, live debugger, or working reference implementation. This adapter uses Lev UI components and does not compile through RenderSpec or target Storybook. Propose missing components explicitly; do not present them as already shipped.

1. Resolve audience, observable behavior, input provenance, live effects, and design model. Interview only for missing choices: live data, realistic source-backed reference data, or synthetic data? Which actions must actually execute? Reuse answers already supplied. Reference shaping is allowed; fabricated successful inference and fake live status are not.
2. Research current libraries for the requested medium using primary sources. Choose for visible impact and functional fit. Use actual graph engines and Archify rather than imitating a requested library with hand-drawn markup. Honor requested quality tiers for other media.
3. Use the requested design model through an available authenticated route and retain model/session evidence. Follow the applicable system prompt. Keep private repository context local unless its export is authorized; a generic design-only brief may guide presentation. Do not silently substitute a required model.
4. Reuse `plugins/now/showcase/` as the live React adapter; keep case source and provenance under `.lev/now/showcase/<slug>/`. Use `@lev-os/lev-ui` components and theme around real visualization engines. Record missing component proposals with behavior, reuse, and proof required; do not create another component catalog.
5. Route CLI inference through `core/exec`; use the existing FlowMind execution graph and typed observation/policy boundaries. Keep credentials server-side. WebSocket events must be actual ordered observations with run references. Reference simulations own isolated state; they do not mutate canonical work by implication.
6. Verify desktop/mobile layout, keyboard interaction, selection and drill-down, disconnection, cancellation, provider error/unknown, and the complete click-to-inference-to-observation-to-declared-branch path. Label snapshots, reference projections, replay, and live execution separately. Preserve exact checks, run references, screenshots, and remaining integration gaps.

Run the current reference adapter from the target project with `npx tsx plugins/now/src/cli.ts --showcase`.

A working showcase proves its inspected behavior, not every product integration. Report the accessible demo, selected libraries, requested-model evidence, verified interactions, and residual limits.

## Visual QA gate

Every `/now` render passes this gate before you report it, on both routes. Follow the routine and probe in [references/genui-craft.md](references/genui-craft.md#visual-qa-routine): every distinct view and state, light and dark, 1440 and 390 wide (plus 1024, 900 and 768 for layout changes), measured, then read image by image. A screenshot you have not read is not evidence. When a check cannot run, say which one and why, and keep it as a gap.

Authored graphs, GenUI drafts, RenderSpec JSON, and rendered HTML stay with the project in `.lev/now/`. Run commands from the target project root (resolve the renderer executable separately when it belongs to another checkout). QA screenshots and manifests go to a fresh system-temp directory via `LEV_NOW_QA_DIR`, including the probe, watch/refresh and other browser screenshot tools. Never place QA screenshots in `.lev/tmp/now`. Retain QA evidence only when needed, through the existing XDG artifact route with a project/task reference. The built-in screenshot pass is a quick width check for any rendered HTML; it does not switch themes:

```bash
now_qa_dir="$(mktemp -d "${TMPDIR:-/tmp}/lev-now-qa.XXXXXX")"
LEV_NOW_QA_DIR="$now_qa_dir" npx tsx plugins/now/src/cli.ts --qa .lev/now/{slug}.html --qa-width 1440
LEV_NOW_QA_DIR="$now_qa_dir" npx tsx plugins/now/src/cli.ts --qa .lev/now/{slug}.html --qa-width 390
```

Fail and revise when:

- The first viewport hides the page's useful content, or hierarchy is unclear.
- Prose, labels, code, navigation, tables, diagrams, or actions clip, collide, become illegible, or overflow at any target width or in either theme.
- The document or any box other than a code or diff block scrolls sideways; text is under 13px; a circle is not round; the console has errors; or keyboard focus has no visible ring.
- Boxes lack inner padding, the header is crowded, or the structure is an interchangeable card grid instead of the object's own shape.
- Routed documents, tabs, dialogs, sidebar links, previous/next, feedback persistence, or action declarations do not work under real interaction.
- The page has visual polish but cannot trace each audience requirement and load-bearing claim to what is rendered.

## Publish

QA a clean build, then run:

```bash
bash ~/.claude/skills/here-now/scripts/publish.sh .lev/now/{slug}.html --title "lev.now — {topic}" --client lev-now
```

Add `--handle-path {path}` for attach.

## Collect Feedback Answers

The feedback component saves answers in browser localStorage under `lev-now-feedback-<pageId>`. Brave, Chrome and Chromium persist that to a per-profile LevelDB, and `scripts/feedback-answers.py` (in this skill directory, Python standard library only) reads it from disk. It needs no server, debugging port or pasted JSON, and it covers `file://` pages and published here.now pages alike. It reads RenderSpec pages, so a page that collects answers takes the RenderSpec route.

```bash
python3 scripts/feedback-answers.py .lev/now/{slug}.json --wait   # run as a background job
python3 scripts/feedback-answers.py .lev/now/{slug}.json          # read the current answers once
```

- `--wait` exits 0 once every feedback item has a choice or note and the answers have stayed unchanged for `--settle` seconds (default 20). The job's completion is the signal to continue: act on the answers without asking the user where they are.
- On `--timeout` (default 3600 s), it prints the partial answers and exits 2.
- Output lists each item's `choice` label, whether it was the `recommended` option, and any `note`. Treat notes as questions or constraints to answer before acting on that item's choice.
- The browser writes to disk a few seconds after a click, so a one-shot read immediately after the user answers can miss the last change.
- Stable `pageId`s matter: answers persist per `pageId`, and a re-rendered page with the same ID restores and reports earlier answers.

## Quick Reference

- Themes (both routes, `--theme`): deep-blue-gold, terracotta-sage, teal-slate, rose-cranberry, amber-emerald, midnight-ink, matrix-temple, obsidian-monolith, fleet-deck, moat.
- RenderSpec components: hero, section, card, text, document, navigation, action, feedback, objective, source-list, exercise, evidence, decision, proof, testimonial, data-table, code-block, timeline, diagram, chart, custom-html, inline.
- RenderSpec section layouts: default, card-grid, kpi-row, pipeline, comparison, diff-panels, collapsible, full-width, sidebar, asymmetric, stacked, deck, stepper.
- RenderSpec effects: grid-dots, grid-lines, card-glow, glass, hero-gradient, noise, title-underline.

## Report

After non-published output, give the local HTML path, a brief mapping from requirements to the page's parts, and the QA evidence: the views and images you read, the measured values, the fixes, and the gaps you could not check. For published output, report only the published URL.
