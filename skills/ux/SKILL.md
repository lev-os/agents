---
name: ux
description: "Routes UX/product design runs, user research/persona synthesis, wireframes, flows, IA, pencil visuals, and agentic CLI UX. Infers full run vs research vs CDO-backed persona mode from context, asking one question only when ambiguous."
skill_type: hub
category: design-ux
related_skills:
  - work
  - lev-cdo
  - lev-research
hub_routes:
  ux-pipeline: "wireframe, flow, IA, journey, interaction, JTBD, task graph"
  ux-research: "user research, synthetic research, personas, study design, persona matrix"
  cdo-persona-insights: "cdo insights, deliberation artifacts, persona base, synthesis-informed research"
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
+-- User research / personas / study design?
|   -> Run UX research mode:
|      Step 1 persona detection + Step 2 persona fanout + domain exploration + problem framing + synthetic user research
|      Optional: use CDO persona agents if CDO artifacts or "$cdo insights" are present
|
+-- UX pipeline (wireframes, flows, IA, JTBD)?
|   -> Run 7-step pipeline (this skill body)
|
+-- CDO insights / persona base / deliberation synthesis?
|   -> Run persona detection, compose one CDO agent per situation-specific persona,
|      then use those findings as persona seed material
|      Continue into research mode or full pipeline depending on context
|
+-- "What design skills exist?" / browse?
|   -> Query: ls ~/.agents/skills-db/design-ux/
|      Deep:  ~/.agents/lev-skills.sh discover "{query}" --json --category=design
|
+-- Ambiguous?
    -> Infer from local/contextual signals first. If confidence < 0.75, ask one
       clarifying question with these options:
       1. Full UX run
       2. User research/personas only
       3. Persona base from CDO insights
       4. Spike/wireframes only
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
| (w) | Run UX pipeline | Persona-first steps + downstream UX phases below |
| (f) | Full UX run | Step 1 persona detection + Step 2 persona fanout + full downstream pipeline |
| (r) | User research/personas | Step 1 persona detection + Step 2 persona fanout + research synthesis |
| (d) | CDO-backed persona base | Step 1 persona detection + Step 2 CDO persona fanout + research synthesis |
| (v) | Visual design / .pen | Pencil MCP tools |
| (c) | CLI/agentic UX patterns | Phase 0.5 lev-ref |
| (b) | Browse design skills | lev-skill resolve |

---

# UX Pipeline

## Mode Parsing

Treat the user's message (including any `/ux ...` text) as the input.

- First run the **Intent Resolver** below. Do not default to AUTO until context
  has been inspected.

- If the input or nearby context contains `cdo`, `$cdo`, `CDO insights`,
  `persona base`, `deliberation`, `synthesis`, `multi-agent`, or paths under
  `tmp/cdo-*`, set mode to `cdo-research` unless the user explicitly asks for
  only wireframes or only full pipeline.

- If the input or nearby context contains `user research`, `synthetic research`,
  `persona`, `study`, `interview`, `JTBD research`, or `research matrix`, set
  mode to `research` unless the user explicitly requests full pipeline.

- If it contains `full` or `interactive`: ask a small set of clarifying questions first, then run step-by-step.

- If it contains `step N`: in persona-first modes, `step 1` means Persona
  Detection and `step 2` means Persona Fanout. Otherwise, match the named
  downstream phase if provided.

- If it contains `continue`: resume the most recent run folder under `.lev/ux/`.

- If it contains `spike`: skip directly to the Wireframes phase. Sketch the interface based on the request alone — no analysis, no artifacts, just wireframes. After wireframes, optionally back-fill analysis from what was drawn. This is prototype-first design.

- If no mode is explicit:
  - Infer `continue` if the user is referring to an existing `.lev/ux/` run.
  - Infer `cdo-research` if CDO artifacts are attached, cited, or present as the
    declared source of persona insight.
  - Infer `research` if the request asks who the users are, what personas need,
    what interviews/research should happen, or how to validate a UX/product
    premise.
  - Infer `full` if the request asks for an end-to-end product/UX package,
    flows, IA, research, and wireframes together.
  - Infer `spike` if the request asks to sketch, mock, wireframe, or make screens
    quickly with little analysis.

- If inference confidence is below `0.75`, ask exactly one clarifying question:
  `Should I run the full UX pipeline, user research/personas only, persona base from CDO insights, or spike/wireframes only?`

- In any non-auto mode except `spike`, `continue`, or explicit `step N`, use
  the persona-first sequence:
  - Step 1: Persona Detection.
  - Step 2: Persona Fanout.
  - Step 3: Synthesis into problem framing, research, JTBD, or full UX pipeline.
  Do not skip straight to problem framing unless the user explicitly says to.

- Otherwise: AUTO mode. Run the downstream UX pipeline end-to-end and produce wireframes.

## Intent Resolver

Before Phase -1, compile a small routing record:

```yaml
ux_intent:
  inferred_mode: full | auto | interactive | research | cdo-research | spike | continue | step
  confidence: 0.0
  evidence:
    - "explicit token, nearby context, artifact path, user correction, or prior run"
  ask_if_below_confidence: 0.75
  clarification_question: "Should I run the full UX pipeline, user research/personas only, persona base from CDO insights, or spike/wireframes only?"
```

Context signals to inspect:

- Current user message and the last few user corrections.
- Files or attachments named by the user.
- Existing `.lev/ux/` runs.
- CDO outputs under `tmp/cdo-*`, `.lev/pm/`, or paths named by the user.
- Product/domain artifacts already on disk.
- Whether the user is asking to design the product, validate the users, create
  personas, or draw screens.

Routing rules:

- `research`: run Step 1 Persona Detection, Step 2 Persona Fanout, Problem
  Framing, Synthetic User Research, then write `summary.md` and
  `constraint_bundle.yaml` if the signal is strong enough. Do not continue into
  wireframes unless the user asked for full pipeline or the gate decision is
  `proceed` and AUTO mode is active.
- `cdo-research`: run Step 1 Persona Detection, Step 2 CDO Persona Fanout, then
  Synthetic User Research using CDO findings as persona seed material. Continue
  into full UX only if requested or inferred with high confidence.
- `full`: run Step 1 Persona Detection, Step 2 Persona Fanout, Step 0b, then
  continue through the full downstream UX pipeline.
- `auto`: run Step 0b through the full downstream UX pipeline unless self-invalidation aborts.
- `spike`: run Wireframes only.
- `continue`: resume latest or explicitly named run.

Do not ask the clarifying question if the user already selected a mode in plain
English. "Let's do research first" means `research`; "base personas on CDO" means
`cdo-research`; "full run" means `full`.

## Persona Detection Gate

In `full`, `interactive`, `research`, and `cdo-research` modes, persona
detection is the first step unless the user explicitly bypasses it.

Naming rule: in non-auto mode this is Step 1. Step 2 is Persona Fanout. Problem
framing happens after fanout synthesis. In AUTO mode, keep the existing pipeline
numbering but still run this gate when research/persona context is relevant.

Write `persona_detection.yaml`:

```yaml
persona_detection:
  source_context:
    - "user request, attachments, prior artifacts, CDO outputs, repo/product docs"
  situation: "{what situation these personas are reacting to}"
  domain: "{domain or market}"
  likely_persona_axes:
    - axis: "{role, authority, risk tolerance, domain expertise, buyer/user, technical literacy, urgency, trust posture}"
      why_it_matters: "{why this axis changes UX/research response}"
  candidate_personas:
    - id: "{persona-id}"
      role: "{domain-specific role}"
      personality_type: "{behavioral archetype specific to the situation, not MBTI by default}"
      context: "{what they know, need, fear, control, and misunderstand}"
      primary_question: "{what this persona needs answered}"
      likely_objection: "{what would make them reject the product/design}"
      source: named_person | role | investor | consumer | buyer | operator | gatekeeper | synthetic
      named_person: "{name if persona is based on a specific stakeholder, else null}"
  confidence: 0.0
  ask_user_if_below: 0.75
```

Persona source rule:

- If local context names people, each named person plus their role becomes a
  candidate persona unless the user excludes them. Example: founder, COO,
  CEO-track, marketing lead, UX researcher.
- Always consider outside-market personas when relevant: investors, consumers,
  buyers/customers, operators, compliance/risk gatekeepers, and strategic
  partners.
- Do not flatten named people into generic roles. "Steve as Argo/Kingly COO" and
  "Lewis as Argo CEO-track" are different personas because their incentives,
  authority, risk, and objections differ.
- For Argo/Kingly-style venture work, default persona pool is:
  - each named team member + role;
  - sponsor founders;
  - investors;
  - customers/buyers;
  - consumers/end users;
  - strategic partners;
  - risk/legal/compliance gatekeepers.

If confidence is below `0.75`, ask one question:

```text
Which persona base should I use: real users/buyers, internal operators, CDO-derived personality agents, or all of the above?
```

If confidence is high, continue without asking and explain the inferred persona
base in `summary.md`.

## Step 2: Persona Fanout

Persona Fanout turns `persona_detection.yaml` into parallel persona responses.
Use it in `research`, `cdo-research`, `full`, and `interactive` modes after
Step 1.

Write `persona_fanout.md`:

```md
# Persona Fanout

## Fanout Matrix

| Persona | Source | Role | Question Asked | Output Artifact |
|---|---|---|---|---|

## Cross-Persona Synthesis

- Convergent needs:
- Divergent needs:
- Objections:
- Trust signals:
- Language that resonates:
- UX/research implications:
- Cap table/package/product implications, if relevant:
```

Fanout prompt for each persona:

```text
You are {persona_id}, a {role} in this situation: {situation}.
Respond from your own incentives, authority, fears, and practical constraints.
Do not optimize for what the product team wants to hear.

Return:
1. What you need.
2. What you distrust.
3. What would make you engage.
4. What would make you reject this.
5. What language sounds credible to you.
6. What evidence or milestone would change your mind.
7. UX/product/research implications.
```

If CDO is not requested, fanout may be run as synthetic persona responses. If
CDO is requested or inferred, use CDO Persona Agent Mode below.

## CDO Persona Agent Mode

When mode is `cdo-research`, each CDO agent should be a
situation-specific personality/persona, not a generic expert role.

The agent set should be derived from `persona_detection.yaml`. Each agent brief
must include:

- Persona role and authority.
- Situation they are responding to.
- Personality/archetype in practical UX terms, not default MBTI labels.
- What they want.
- What they distrust.
- What evidence would change their mind.
- What they would do if confused.
- Output format: needs, objections, trust signals, language that resonates,
  failure modes, and design/research implications.

Examples:

- Skeptical enterprise buyer.
- Time-starved operator.
- Status-sensitive executive sponsor.
- Domain expert who distrusts generic AI.
- Novice user with high anxiety.
- Compliance/risk gatekeeper.
- Growth/marketing opportunist.

CDO composition rule:

```yaml
cdo_persona_agents:
  source: persona_detection.yaml
  composition: "one agent per candidate persona/personality type; include each named person + role, investors, and consumers/customers when relevant"
  synthesis_goal: "convert persona reactions into research constraints, JTBD inputs, anti-patterns, and UX risks"
  output_artifacts:
    - persona_fanout.md
    - cdo_insights.md
    - persona_source_map.yaml
```

If actual CDO/agent dispatch is unavailable, create the proposed CDO persona
matrix and ask before substituting single-model synthetic responses. Do not
pretend a multi-agent run occurred.

## Output Location

Create a run folder:

- `RUN_DIR=.lev/ux/{YYYYMMDD-HHMMSS}-{slug}/`

Write artifacts below. If resuming, reuse the existing `RUN_DIR`.

Artifacts (expected):

- `domain_exploration.md`

- `problem_spec.yaml`

- `study_design.yaml`

- `user_and_agent_research.md`

- `cdo_insights.md` (only in `cdo-research` or when CDO artifacts are used)

- `persona_detection.yaml` (required for non-auto `full`, `interactive`,
  `research`, and `cdo-research`)

- `persona_fanout.md` (required after `persona_detection.yaml` in non-auto
  research/full/cdo-research)

- `persona_source_map.yaml` (only in `research` or `cdo-research`)

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
   - If match -> load that skill, optionally resume after persona fanout or at the named downstream phase.

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

After collecting responses, compare their unprompted concerns with the problem you planned to frame in the Problem Framing phase.

- **Strong overlap**: Your problem framing is grounded. Proceed.
- **Partial overlap**: Adjust problem_spec to incorporate concerns you missed.
- **Significant divergence**: Reconsider your problem framing entirely. The domain personas surfaced problems you didn't consider — maybe you're solving the wrong thing.

Write `domain_exploration.md` with personas, responses, and comparison.

**Why this exists**: Synthetic User Research constructs personas FROM the problem_spec, which means they can't say "you're solving the wrong problem." Step 0b breaks that circular validation by exploring the domain before committing to a problem frame.

## Problem Framing

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

## Synthetic User Research

**Depends on**: `problem_spec.yaml` must exist.
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

Feed into JTBD:

- Convergent concerns → constraints for job statements

- Convergent excitement → motivation language

- Divergent reactions → separate `user_types` in `jobs.graph.json`

- Edge cases → risk register or scope exclusions

### 1b.4: Self-Invalidation Gate

After collecting results, evaluate whether the pipeline should continue:

- **gate_decision: proceed** — Clear signal. Personas differentiated. Convergence/divergence is actionable. Continue to JTBD.
- **gate_decision: reframe** — Step 0b concerns diverge significantly from `problem_spec.yaml`, OR personas surfaced a better problem. Go back to Problem Framing and revise `problem_spec.yaml`.
- **gate_decision: abort** — ALL personas across ALL models say "just build and iterate" or equivalent. OR convergence is below useful threshold (too much noise, no clear signal). Recommend a different approach: rapid prototyping, traditional user interviews, design sprint, or just-build-it.

A pipeline that can't recommend against itself isn't honest. If the research says this tool is wrong for this problem, say so and stop.

Append `gate_decision` to `user_and_agent_research.md`. If `abort`, write `summary.md` with the recommendation to NOT continue the pipeline, and why.

### Artifacts

- `study_design.yaml` (study design with personas, matrix, rationale)

- `user_and_agent_research.md` (results, convergence/divergence analysis, gate decision, JTBD integration notes)

- `domain_exploration.md` (Step 0b output, if run)

## JTBD: Jobs To Be Done

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

## Task Decomposition

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

## Information Architecture (IA)

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

## Interaction Models

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

## Components

Write `components.md`:

- Reusable components list (name, purpose, props/data).

- Screens-to-components mapping.

Rules:

- Prefer composable components over mega-views.

- Name components after user intent (not implementation).

## Wireframes

Write `wireframes.md`:

- A short global nav map.

- For each screen:

- Purpose (one line).

- Primary actions (1-3).

- Layout: header/body/footer sections.

- State variants: idle/loading/empty/error/success.

If the user asks for a design-file deliverable, propose using the `pencil` tool to generate a `.pen` wireframe and confirm the target path under `.lev/ux/`.

## Constraint Bundle

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

relationships:
  - from: "{Entity}"
    to: "{Entity}"
    cardinality: "1:1 | 1:N | N:M"
    ownership: contains | references
  # From ia_schema.json — how entities compose. Agents guess without this.

modes:
  auto:
    description: "Full pipeline, no stops. Default."
    gates: [self_invalidation]  # only this gate pauses auto
    output: constraint_bundle.yaml
  interactive:
    description: "Pause at each step for review."
    gates: [study_design, tribunal_dispatch, analysis, self_invalidation]
    output: all artifacts + constraint_bundle.yaml
  spike:
    description: "Straight to wireframes. No research."
    gates: []
    output: wireframes.md
  # From research divergence — user_types map to modes differently

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
    default_mode: auto | interactive | spike
  # From research divergence — different users want different things
  # default_mode maps each user type to its natural pipeline mode

research_signal:
  convergence: ["{what all personas agreed on}"]
  tensions: ["{where personas split — the tradeoffs}"]
  gate_decision: proceed | reframe | abort

validation_rubric:
  # Two tiers: bundle_checks (verify against this YAML now) and run_checks (verify after pipeline execution)
  bundle_checks:
    # Verifiable right now against this file's structure
    - check: "{what to verify}"
      pass_if: "{concrete condition checkable in this YAML}"
      severity: must | should | nice
    # Must = hard fail. Should = flag. Nice = bonus.
    # Min 3 bundle_checks. Derive from anti_patterns + layout_constraints.
  run_checks:
    # Verifiable after pipeline execution against RUN_DIR artifacts
    - check: "{what to verify}"
      pass_if: "{condition requiring pipeline output files}"
      severity: must | should | nice
    # Min 2 run_checks. Validates actual execution quality.
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
