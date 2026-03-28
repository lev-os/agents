---
name: ux
description: "UX design hub: 8-step wireframe pipeline (+ constraint_bundle for agents) + product design (design-os) + visual prototyping (pencil) + agentic UX patterns (lev-ref). Use for wireframes, flows, IA, JTBD, product design, CLI design, agentic UX, design systems, or component architecture."
skill_type: hub
category: design-ux
related_skills:
  - work
  - lev-cdo
  - lev-research
hub_routes:
  ux-pipeline: "wireframe, flow, IA, journey, interaction, JTBD, task graph"
  design-os: "product design, vision, roadmap, data model, design system, export"
  pencil-mcp: "visual design, .pen file, mockup, design sweep"
  agentic-ux: "CLI design, progressive disclosure, prompt steering, CLI-as-prompt"
  browse: "design skill, find skill, what skills"
---

# UX Design Hub

Routes to specialist sub-skills or runs the built-in 8-step UX pipeline.

## Hub Decision Tree

```
Request arrives
|
+-- Product planning (vision, roadmap, data model, export)?
|   -> Load: skill://lev-design-os
|      (~/.agents/skills/lev-design-os/SKILL.md + references/)
|
+-- Visual design / .pen file / design sweep?
|   -> Use Pencil MCP tools (batch_design, get_screenshot, style guides)
|      Ref: skillsdb://design-ux/pencil for character/illustration work
|
+-- CLI / agentic UX patterns?
|   -> Load Phase 0.5 lev-ref patterns (below)
|
+-- UX pipeline (wireframes, flows, IA, JTBD)?
|   -> Run 7-step pipeline (this skill body)
|
+-- "What design skills exist?" / browse?
|   -> Query: ls ~/.agents/skills-db/design-ux/
|      Deep:  ~/.agents/lev-skills.sh discover "{query}" --json --category=design
|
+-- Ambiguous?
    -> Ask one clarifying question, then route
```

## Skills-DB Design Catalog (skillsdb://design-ux/*)

| Skill | Load when |
|-------|-----------|
| design-os | Product vision, roadmap, data model, design tokens, export |
| superdesign-prompt-library | AI image prompts, style/layout/component prompts |
| swiftui-* (6 skills) | SwiftUI/iOS/macOS UI work |
| metal-shaders, vfx-spell-effects | GPU graphics, visual effects |

## UX Thinking Patterns (scored, from skills-db)

Load from ~/.agents/skills-db/thinking/patterns/{name}/SKILL.md when reasoning depth needed:

| Pattern | Score | Use when |
|---------|-------|----------|
| nielsen-heuristics | 50 | Usability evaluation |
| design-of-everyday-things | 48 | Affordance/signifier analysis |
| dont-make-me-think | 48 | Simplicity audit |
| laws-of-ux | 45 | Psychology-based design |
| wcag | 45 | Accessibility compliance |
| design-systems | 45 | Component architecture |
| refactoring-ui | 44 | Developer-facing design tactics |

## Hub Shortcuts

| Key | Action | Route |
|-----|--------|-------|
| (p) | Product design wizard | skill://lev-design-os |
| (w) | Run UX pipeline | Steps 1-7 below |
| (v) | Visual design / .pen | Pencil MCP tools |
| (c) | CLI/agentic UX patterns | Phase 0.5 lev-ref |
| (b) | Browse design skills | lev-skill resolve |

---

# UX Pipeline

## Mode Parsing

Treat the user's message (including any `/ux ...` text) as the input.

- If it contains `full` or `interactive`: ask a small set of clarifying questions first, then run step-by-step.

- If it contains `step N` (N=1..7): run only that step and update artifacts.

- If it contains `continue`: resume the most recent run folder under `.lev/ux/`.

- If it contains `spike`: Skip directly to Step 7 (Wireframes). Sketch the interface based on the request alone — no analysis, no artifacts, just wireframes. After wireframes, optionally back-fill Steps 1-6 from what was drawn. This is prototype-first design.

- Otherwise: AUTO mode. Run all 7 steps end-to-end and produce wireframes.

## Output Location

Create a run folder:

- `RUN_DIR=.lev/ux/{YYYYMMDD-HHMMSS}-{slug}/`

Write artifacts below. If resuming, reuse the existing `RUN_DIR`.

Artifacts (expected):

- `domain_exploration.md`

- `problem_spec.yaml`

- `study_design.yaml`

- `user_and_agent_research.md`

- `routed_skills.json`

- `jobs.graph.json`

- `task_graph.json`

- `ia_schema.json`

- `interaction_fsm.json`

- `components.md`

- `wireframes.md`

- `constraint_bundle.yaml`

- `summary.md`

## Phase -1: Setup (Deterministic)

1. Create run dir and establish shell vars:

```bash
TS="$(date +%Y%m%d-%H%M%S)"
SLUG="$(printf '%s' "$USER_MSG" | tr '[:upper:]' '[:lower:]' | rg -o "[a-z0-9]+" | head -n 6 | paste -sd- -)"
RUN_DIR=".lev/ux/${TS}-${SLUG}"
mkdir -p "$RUN_DIR"
```

2. Persist the raw request for traceability:

```bash
printf '%s\n' "$USER_MSG" > "$RUN_DIR/request.txt"
```

## Phase 0: Prior Art (Fast)

1. If `bd` exists and `.beads/` exists:

- `bd list --status=open | rg -n "ux|design|wireframe|ia|flow" -i || true`

2. Scan local UX artifacts:

- `ls -t .lev/ux 2>/dev/null | head -n 10 || true`

3. Scan UI code quickly (keep it cheap):

- `rg -n "struct\\s+.*View\\b|SwiftUI|Navigation(Stack|SplitView)|TabView" apps packages extensions 2>/dev/null | head -n 50 || true`

If you find relevant prior art, cite paths in `summary.md` and either extend it or explicitly supersede it.

## Phase 0.5: Agentic UX Patterns (lev-ref)

Apply lev-ref patterns to all UX outputs (especially `summary.md` and any routed-skill handoff).

This phase doubles as the **agentic-ux** hub route. Load directly when asked about CLI design, progressive disclosure, or prompt steering — no need to run the full 7-step pipeline.

Key patterns:
- **CLI-as-Prompt**: Every CLI surface is a prompt-steering opportunity
- **Progressive Disclosure**: Metadata first, body on trigger, references on demand
- **Every Surface a Steering Attempt**: Follow-ups, related skills, confidence inline
- **Audio Design**: Consider sonic feedback for agent interactions

1. Load lev-ref patterns:

```bash
sed -n '1,220p' docs/_inbox/lev-ref/SKILL.md
```

2. Apply inline conventions (CLI-as-Prompt):

- Add confidence lines like `[85% confident]` for key recommendations.

- Add `→ Next:` and `→ Related:` follow-ups.

- Add a short `💡 Tip:` in `summary.md` if there's a non-obvious UX lesson.

## Phase 0.6: Skills-DB Enrichment

Route to specialized skills using the Hub Decision Tree above.

1. Check hub_routes (frontmatter) for trigger match against request keywords.
   - If match -> load that skill, optionally resume pipeline at Step 3+.

2. If no hub_route match, query skills-db dynamically:

```bash
# Design-ux category first (high-signal, 12 skills)
rg -l -i "{keywords}" ~/.agents/skills-db/design-ux/*/SKILL.md

# Broader search only if design-ux returns empty
lev-skill resolve "{keywords}" --json 2>/dev/null | jq '.results[:5]'
```

3. If curated scores available, prefer higher-scored patterns:

```bash
grep -i "{keyword}" ~/.agents/skills-db/thinking/11-ui-ux/task.csv \
  | sort -t, -k8 -rn | head -3
```

4. Emit routed_skills.json (keep existing schema for compatibility):

```json
{ "request_terms": [...], "candidates": [...], "selected": [...] }
```

5. Present discovered skills:
   - 1 clear match -> propose loading it
   - 2-3 matches -> ranked list, let user choose
   - 0 matches -> continue with built-in UX pipeline

6. Continue pipeline regardless — routing enriches, never blocks.

## Step 0b: Unconstrained Domain Exploration

**Optional. Runs in `full` and `auto` modes. Skip with `step 1` or `spike`.**

Before problem framing, construct 2-3 personas grounded ONLY in the domain — not in any specific problem. These personas don't know what you're building. They know the domain.

### 0b.1: Construct Domain Personas

From the user's request, identify the domain (e.g., "developer tooling", "healthcare scheduling", "social commerce"). Construct 2-3 personas who live in that domain daily — different roles, different frustrations, different expertise levels.

Each persona: ~150 words. Who they are, what they deal with, what drives them crazy. No problem_spec to anchor to — that's the point.

### 0b.2: Open-Ended Exploration

Ask each persona (via tribunal or Agent dispatch):

- "What frustrates you most about [domain] right now?"
- "If you could change one thing about how [domain] works, what would it be?"
- "What's broken that nobody talks about?"

### 0b.3: Compare with Intended Problem

After collecting responses, compare their unprompted concerns with the problem you planned to frame in Step 1.

- **Strong overlap**: Your problem framing is grounded. Proceed.
- **Partial overlap**: Adjust problem_spec to incorporate concerns you missed.
- **Significant divergence**: Reconsider your problem framing entirely. The domain personas surfaced problems you didn't consider — maybe you're solving the wrong thing.

Write `domain_exploration.md` with personas, responses, and comparison.

**Why this exists**: Step 1b (synthetic user research) constructs personas FROM the problem_spec, which means they can't say "you're solving the wrong problem." Step 0b breaks that circular validation by exploring the domain before committing to a problem frame.

## Step 1: Problem Framing

Write `problem_spec.yaml`:

```yaml
problem:
  statement: "{1-2 sentences}"
  for_whom: "{primary user segment}"
  constraints:
    - "{constraint}"
  success_criteria:
    - "{measurable outcome}"
  scope:
    in: ["{in}"]
    out: ["{out}"]
```

Rules:

- Make success criteria measurable.

- Keep scope boundaries crisp.

## Step 1b: Synthetic User Research

**Depends on**: Step 1 (`problem_spec.yaml` must exist)
**Reference**: Load `references/study-construction.md` for methodology.

### 1b.1: Design the Study

Analyze problem_spec. Reason about:

- Who are the real user segments for THIS problem? Not generic archetypes — segments grounded in the problem's `for_whom`, `constraints`, and `success_criteria`.

- What psychological dimensions matter for THIS study? Not always Big 5. Maybe domain expertise. Maybe risk tolerance. Maybe tech literacy. Maybe regulatory burden. Pick the axes that would actually produce different reactions to this specific stimulus.

- How many personas does this study need? Could be 2, could be 6. Depends on user space breadth. More isn't better — more is more permutations.

- What's the stimulus? Problem statement? Feature concept? Wireframe? Could be all three across rounds.

Construct personas using axiom explorer's `map-elements` output format as a scaffold (load `~/.agents/skills-db/thinking/axioms/skills/map-elements.md` for format reference) — but only the dimensions that matter. A developer tool study doesn't need political compass. A healthcare app might need ANS state.

Write `study_design.yaml`:

```yaml
study:
  stimulus:
    type: problem_statement | feature_concept | wireframe
    content: "{from problem_spec}"
  personas:
    - id: "{descriptive-id}"
      description: "{who this person is, grounded in the problem}"
      key_dimensions:
        - "{dimension}: {value + reasoning}"
      prompt_injection: |
        {the actual persona prompt — full worldview, not just traits}
  matrix:
    models: ["{model-ids — reasoning: why these models}"]
    cli_runners: ["{cli names — reasoning: why these CLIs}"]
  rationale: "{why these personas, why this matrix, what signal are we looking for}"
```

**Full mode**: Present study design for review. User can add/remove/modify personas, change the model matrix, adjust dimensions.

**Auto mode**: Construct and run. Explain reasoning for every choice.

### 1b.2: Execute via Tribunal

For each cell in the persona × model matrix:

- Construct the persona-injected prompt (persona prompt + stimulus)

- Dispatch via tribunal (using CLI runner table at `references/cli-runners.md` for cross-CLI runs, or Agent tool for Claude-only)

- Collect structured responses

The same persona runs against every model. The same model runs every persona. The matrix is the point.

### 1b.3: Analyze & Integrate

Write `user_and_agent_research.md`:

- **Per-persona across models**: Does reasoning strength change the reaction? Where do edges appear?

- **Per-model across personas**: Which model surfaces the most differentiated responses?

- **Convergence map**: What do ALL personas agree on regardless of model? This is strong signal.

- **Divergence map**: Where do personas split? Where do models split? These are the tensions worth investigating.

- **Edge cases**: Unexpected reactions at low/high reasoning strength. Insights that only one persona × model combination surfaced.

Feed into Step 2 (JTBD):

- Convergent concerns → constraints for job statements

- Convergent excitement → motivation language

- Divergent reactions → separate `user_types` in `jobs.graph.json`

- Edge cases → risk register or scope exclusions

### 1b.4: Self-Invalidation Gate

After collecting results, evaluate whether the pipeline should continue:

- **gate_decision: proceed** — Clear signal. Personas differentiated. Convergence/divergence is actionable. Continue to Step 2.
- **gate_decision: reframe** — Step 0b concerns diverge significantly from Step 1 problem_spec, OR personas surfaced a better problem. Go back to Step 1 and revise problem_spec.
- **gate_decision: abort** — ALL personas across ALL models say "just build and iterate" or equivalent. OR convergence is below useful threshold (too much noise, no clear signal). Recommend a different approach: rapid prototyping, traditional user interviews, design sprint, or just-build-it.

A pipeline that can't recommend against itself isn't honest. If the research says this tool is wrong for this problem, say so and stop.

Append `gate_decision` to `user_and_agent_research.md`. If `abort`, write `summary.md` with the recommendation to NOT continue the pipeline, and why.

### Artifacts

- `study_design.yaml` (study design with personas, matrix, rationale)

- `user_and_agent_research.md` (results, convergence/divergence analysis, gate decision, JTBD integration notes)

- `domain_exploration.md` (Step 0b output, if run)

## Step 2: Jobs To Be Done (JTBD)

Write `jobs.graph.json`:

```json
{
  "jobs": [
    {
      "id": "job-1",
      "statement": "When I {situation}, I want to {motivation}, so I can {outcome}",
      "type": "functional",
      "triggers": ["{trigger}"],
      "user_types": ["{archetype}"]
    }
  ]
}
```

Rules:

- Prefer progress language over feature language.

- Include at least one emotional or social job if relevant.

## Step 3: Task Decomposition

Write `task_graph.json`:

```json
{
  "tasks": [
    {
      "id": "task-1",
      "name": "{verb} {object}",
      "entry_state": "{precondition}",
      "exit_state": "{postcondition}",
      "happy_path": ["{step}"],
      "failure_modes": ["{failure}"],
      "depends_on": []
    }
  ]
}
```

Rules:

- Include failure modes and recovery paths.

- Keep tasks at a UI-actionable granularity.

## Step 4: Information Architecture (IA)

Write `ia_schema.json`:

```json
{
  "entities": [
    {"name": "{Entity}", "attributes": ["{attr}"], "actions": ["{verb}"]}
  ],
  "relationships": [
    {"from": "{Entity}", "to": "{Entity}", "type": "has_many"}
  ],
  "navigation": {
    "primary": ["{screen}"],
    "secondary": ["{screen}"]
  }
}
```

Rules:

- Avoid navigation that doesn't map to an entity or job.

## Step 5: Interaction Models

Write `interaction_fsm.json`:

```json
{
  "screens": [
    {
      "id": "screen-1",
      "name": "{Screen Name}",
      "states": ["idle", "loading", "empty", "error", "success"],
      "transitions": [
        {"from": "idle", "event": "tap_primary", "to": "loading"}
      ],
      "feedback": ["spinner", "toast"]
    }
  ]
}
```

Rules:

- Explicitly model `loading`, `empty`, and `error` states.

- Call out accessibility considerations if there's complex interaction.

## Step 6: Components

Write `components.md`:

- Reusable components list (name, purpose, props/data).

- Screens-to-components mapping.

Rules:

- Prefer composable components over mega-views.

- Name components after user intent (not implementation).

## Step 7: Wireframes

Write `wireframes.md`:

- A short global nav map.

- For each screen:

- Purpose (one line).

- Primary actions (1-3).

- Layout: header/body/footer sections.

- State variants: idle/loading/empty/error/success.

If the user asks for a design-file deliverable, propose using the `pencil` tool to generate a `.pen` wireframe and confirm the target path under `.lev/ux/`.

## Step 8: Constraint Bundle

Write `constraint_bundle.yaml` — a compressed, agent-optimized summary of the entire run. This is what an agent consumes as context before implementing UI.

**Target: <6K tokens.** If the bundle exceeds 8K tokens, you're not compressing enough. Rank and cut.

```yaml
# constraint_bundle.yaml
meta:
  source: "{RUN_DIR}"
  confidence: synthetic
  pipeline_version: "ux-v1"

problem: |
  {1-2 sentence problem statement from problem_spec.yaml}

primary_jobs:
  - id: job-1
    statement: "{JTBD statement}"
    priority: 1
  # Top 3-5 jobs only, ranked by research signal strength

entities:
  - name: "{Entity}"
    attributes: ["{attr}"]
    primary_action: "{verb}"
  # From ia_schema.json — only entities with user-facing actions

navigation:
  primary: ["{screen}"]
  secondary: ["{screen}"]

layout_constraints:
  # Extracted from research convergence + wireframe patterns
  - "{constraint}: {true|false|value}"

anti_patterns:
  # From research divergence + edge cases — explicit "don't" list
  - "{what not to do and why}"

design_tokens:
  palette: "{name or hex values}"
  fonts: ["{font}"]
  # Only if the pipeline produced design direction

user_types:
  - id: "{type-id}"
    needs: "{what this user type prioritizes}"
  # From research divergence — different users want different things

research_signal:
  convergence: ["{what all personas agreed on}"]
  tensions: ["{where personas split — the tradeoffs}"]
  gate_decision: proceed | reframe | abort
```

Rules:

- **Rank everything.** Jobs by priority. Entities by user-facing importance. Anti-patterns by severity.

- **Anti-patterns are mandatory.** Agents default to training data averages without explicit "don't" signals. Every bundle needs at least 3 anti-patterns.

- **`confidence: synthetic` always present.** This is synthetic research, not real user data.

- **Omit empty sections.** If no design tokens were produced, don't include the key.

- **This replaces nothing.** The full artifacts (13 files) remain the source of truth. The bundle is a compressed handoff for agents who need context, not the complete picture.

**Skip in spike mode** — spike has no research to compress.

## Final Summary

Write `summary.md`:

- Problem + success criteria.

- Key tradeoffs and open questions.

- The wireframe screen list (ordered).

- What to implement first (smallest shippable slice).

- Include lev-ref inline conventions: `[N% confident]`, `→ Next:`, and `💡 Tip:`.

## Technique Map

- **Identify scope** — Determine what the skill applies to before executing.
- **Follow workflow** — Use documented steps; avoid ad-hoc shortcuts.
- **Verify outputs** — Check results match expected contract.
- **Handle errors** — Graceful degradation when dependencies missing.
- **Reference docs** — Load references/ when detail needed.
- **Preserve state** — Don't overwrite user config or artifacts.

## Technique Notes

Skill-specific technique rationale. Apply patterns from the skill body. Progressive disclosure: metadata first, body on trigger, references on demand.

## Prompt Architect Overlay

**Role Definition:** Specialist for ux domain. Executes workflows, produces artifacts, routes to related skills when needed.

**Input Contract:** Context, optional config, artifacts from prior steps. Depends on skill.

**Output Contract:** Artifacts, status, next-step recommendations. Format per skill.

**Edge Cases & Fallbacks:** Missing context—ask or infer from workspace. Dependency missing—degrade gracefully; note in output. Ambiguous request—clarify before proceeding.
