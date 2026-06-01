---
name: interview
description: Use when guiding decision interviews that produce a design artifact in .lev/pm/designs before proposal or implementation planning.
output_template: footer
---

# Interview

<goal>
Run a design-acquisition interview. First reduce ambiguity until the subject, intent, outcome, scope, constraints, and success criteria are clear enough to know the decision space. Then walk one researched design branch at a time until a design artifact is ready under `.lev/pm/designs/`.

The interview output is a design, not a spec. It should carry the product
framing normally expected from a PRD, but inside the design artifact.
`propose` is the next lifecycle step after design alignment.
</goal>

<commands>

```bash
<<<<<<< HEAD
/interview                      # --standard --compact by default
/interview --auto               # synthesize/update artifact from context; ask only on blocking ambiguity
=======
/interview                      # --standard by default
>>>>>>> b8982ad246b55b1f9c1643f387b5f88a6e606123
/interview --quick              # lower rigor, ambiguity gate <= 0.30
/interview --standard           # default rigor, ambiguity gate <= 0.20
/interview --deep               # high rigor, ambiguity gate <= 0.15
/interview --auto               # continue lookup-resolvable turns; stop for human judgment or propose handoff
/interview --framework=SCAMPER  # use this lens internally; show only the tag unless d. Deep dive is requested
```

</commands>

<operational-contract>

```yaml
rules:
<<<<<<< HEAD
  - "Depth and verbosity are separate controls: quick/standard/deep changes ambiguity threshold; compact/full changes visible text volume only."
  - "--auto performs lookup and scoring first; if ambiguity is at or below threshold, update the artifact instead of interviewing."
  - "Start in the orientation loop unless ambiguity is already at or below the active depth threshold."
  - "Do not walk design branches until the orientation loop identifies the subject and ambiguity is at or below threshold."
  - "Run codebase/docs/artifact lookup before asking in both loops; do not ask the user what files can answer."
  - "When ambiguity is above threshold, ask one Socratic question targeting the weakest clarity dimension."
=======
  - "Depth controls rigor: quick/standard/deep changes ambiguity threshold. Visible output always uses the guided interview format."
  - "Start in the orientation phase unless ambiguity is already at or below the active depth threshold."
  - "Do not walk design branches until the orientation phase identifies the subject and ambiguity is at or below threshold."
  - "Run codebase/docs/artifact lookup before asking in both phases; do not ask the user what files can answer."
  - "When ambiguity is above threshold, ask one Socratic question targeting the weakest clarity dimension, with three concrete ways to answer and one recommendation."
>>>>>>> b8982ad246b55b1f9c1643f387b5f88a6e606123
  - "When ambiguity is at or below threshold, discover the candidate branch map and walk one design branch at a time."
  - "For design-branch questions, provide three researched options, one recommendation, and the consequence of each option."
  - "Persist subject, source context, depth, ambiguity, resolved branches, deferred branches, and next branch."
  - "`--auto` may answer lookup-resolvable branches without pausing, but it must stop for human product judgment, irreversible decisions, or when the design is ready for propose."
validation: "Every turn declares phase, active depth threshold, ambiguity score, lookup result or gap, and the next state transition."
on_failure: "Do not ask another broad question. Re-score ambiguity, inspect context, or switch to the orientation template."
```

</operational-contract>

<process-contract>

```yaml
steps:
  - id: select_controls
    action: Choose depth and cadence
    instruction: |
<<<<<<< HEAD
      Default to --standard --compact.
      --auto inherits --standard --compact unless quick/standard/deep/full is also supplied.
      User-passed quick/standard/deep overrides complexity inference.
      If not passed, infer depth from complexity: quick for low blast radius and reversible choices, standard for normal product/architecture design, deep for cross-module, high-risk, or irreversible design.
      In --auto, ask only when lookup cannot reduce ambiguity below the selected threshold.
      Compact/full controls presentation only; it never changes lookup, scoring, or branch coverage.
    validation: "Depth is quick, standard, or deep; output mode is compact or full."
    on_failure: "Default to --standard --compact and state that more detail is available with --full or d. Deep dive."
=======
      Default to --standard.
      User-passed quick/standard/deep overrides complexity inference.
      If not passed, infer depth from complexity: quick for low blast radius and reversible choices, standard for normal product/architecture design, deep for cross-module, high-risk, or irreversible design.
      Auto controls cadence only; it never changes lookup, scoring, branch coverage, or artifact quality.
    validation: "Depth is quick, standard, or deep; auto is true or false."
    on_failure: "Default to --standard and state that more detail is available with d. Deep dive."
>>>>>>> b8982ad246b55b1f9c1643f387b5f88a6e606123

  - id: load_design_template
    action: Load the canonical design template
    instruction: |
      Before creating or updating the design artifact, load:
      /Users/jean-patricksmith/.agents/skills/work/templates/design.md
      Use it as the artifact skeleton under .lev/pm/designs/.
      Do not create a spec artifact from interview output.
    validation: "Design template loaded and target artifact path is under .lev/pm/designs/."
    on_failure: "Stop and load the design template before writing interview artifacts."

  - id: discover_context
    action: Lookup before asking
    instruction: |
      Before each orientation or branch question, inspect the local workspace when the answer may be discoverable.
      Search code, docs, designs, proposals, workstreams, validation gates, and existing task artifacts as relevant.
      Pull one useful artifact fact, one implementation/doc fact, and one constraint or gate when available.
      If lookup resolves the ambiguity dimension or branch, update state and move to the next unresolved dimension or branch without asking.
      If lookup cannot resolve it, ask the smallest human judgment question that remains.
    validation: "Each question is grounded in lookup evidence or an explicit lookup gap."
    on_failure: "Do not ask a generic question. Search files/docs first or say what evidence is missing."

  - id: orient_subject
    action: Reduce ambiguity before branch walking
    instruction: |
      Establish the current subject, likely design artifact, source context, and whether this is a design problem at all.
      Score intent, outcome, scope, constraints, and success criteria after lookup.
      If ambiguity is above the active depth threshold, ask one Socratic question against the weakest dimension.
      Do not invent the whole decision tree while the subject is still unclear.
    validation: "Subject, candidate design target, source context, ambiguity score, weakest dimension, and next orientation question are known."
    on_failure: "Use the orientation template and ask for the missing dimension."

  - id: discover_design_branches
    action: Discover candidate branches after orientation
    instruction: |
      After ambiguity is at or below threshold, derive the candidate branch map from the clarified subject and lookup evidence.
      Name dependencies between branches so the next question resolves the highest-leverage design uncertainty.
      Keep the branch map concise; store resolved/deferred branches in state rather than dumping all of them.
    validation: "Candidate branches exist only after ambiguity is at or below the active depth threshold."
    on_failure: "Return to orient_subject; the decision space is not ready for branch walking."

  - id: shape_product_requirements
    action: Fold PRD-style content into the design
    instruction: |
      The design artifact should include the PRD-derived content needed for later slicing:
      problem statement, solution direction, user/operator stories, implementation decisions,
      testing decisions, and out-of-scope boundaries.

      Before asking the user, inspect repo/docs for domain vocabulary, ADRs, major modules,
      deep-module candidates, and test prior art. Ask only for product or design judgment
      that lookup cannot answer.
    validation: "Design artifact has product framing, stories, implementation decisions, testing decisions, and out-of-scope boundaries when relevant."
    on_failure: "Ask one focused design question for the missing product/design requirement."

  - id: shape_proof_design
    action: Design QA/Pentagon proof before proposal
    instruction: |
      For non-trivial, runtime, agentic, promotion, cleanup, fallback, or boundary-risk work,
      add proof design to the Testing Decisions section before handing off to propose.
      Name the promotion decision, highest-risk behavioral claim, fail-closed acceptance,
      required Pentagon axes, UltraQA scenario classes, owner-local test placement, and
      any ai-slop-cleaner review gate.

      Keep ownership explicit: module-specific tests, probes, fixtures, and harness suites
      live with the owning module and use shared testing/eval helpers. Do not put
      module-specific tests into core/testing just because Pentagon is involved.
      This is internal design hygiene unless the user asks for d. Deep dive.
    validation: "Testing Decisions include proof design or explicitly mark proof gates N/A with rationale."
    on_failure: "Ask one focused proof-design question before proposing."

  - id: shape_semantic_controls
    action: Shape semantic KPIs and ontology boundaries
    instruction: |
      During design, name the semantic control signals the later proposal can harden:
      ambiguity, alignment, convergence, semantic drift, proof readiness, and unresolved branch count.
      These are design-stage KPIs until propose converts them into concrete proof metrics, gate
      thresholds, fixtures, receipts, or validation commands.

      When the design depends on vocabulary, ownership categories, graph entities, lifecycle states,
      or authority boundaries, run an ontological taxonomy exploration before branch closure. Keep it
      practical: identify the taxonomy axis, the drift risk, the canonical owner, and the proof signal
      that would catch bad drift.
      This is internal design hygiene unless the user asks for d. Deep dive.
    validation: "Non-trivial designs name semantic KPIs, taxonomy/drift risk, and whether each proof signal is design-stage or propose-hardened."
    on_failure: "Ask one focused semantic-control or taxonomy question before proposing."

  - id: synthesize_lenses
    action: Think through perspectives silently
    instruction: |
      Consider systems thinking, first principles, trade-off analysis, Thinking Hats, and other useful lenses internally.
      Print only one lens tag, such as (systems thinking), near the question title or recommendation.
      Do not print a framework essay unless the user asks for d. Deep dive.
    validation: "Output contains at most one visible lens tag."
    on_failure: "Remove framework prose and leave only the tag."

  - id: walk_tree
    action: Resolve one decision branch
    instruction: |
      Only run this step after ambiguity is at or below the active depth threshold.
      Ask one question that resolves the next meaningful branch in the design tree.
      Name the current branch and the dependency it unblocks.
      Provide three researched answers when viable; use two only if a third branch would be fake.
      Recommend one answer and name the design consequence of each option.
      Carry unresolved branches forward instead of dumping all branches at once.
    validation: "Question has current branch, lookup result or gap, one decision, 2-3 options, one recommendation with rationale, and unresolved branch count."
    on_failure: "Split the question or collapse fake options."

  - id: update_design
    action: Update the design artifact
    instruction: |
      Treat interview as a design phase, not a generic planning phase.
      The output target is a design artifact: problem framing, constraints, direction, alternatives, interaction model, PRD-style product sections, risks, and recommendation.
      Write or update the design under .lev/pm/designs/ using the canonical design template.
      When the user says propose, stop interviewing and hand the aligned design to propose.
    validation: "A design artifact path under .lev/pm/designs/ is named or updated."
    on_failure: "Add a concrete design artifact target before asking."
```

</process-contract>

<lifecycle-contract>

```yaml
steps:
  - id: lifecycle_sync
    action: Keep work artifacts current when .lev/pm/ exists
    instruction: |
      If .lev/pm/ exists, treat interview as part of the work lifecycle.
      Prefer updating active workstream state, handoff, and .lev/pm/designs/ artifacts.
      Update proposals only when the user enters proposition mode or asks to run propose.
    validation: "Relevant lifecycle artifact is updated or explicitly not needed for read-only/trivial work."
    on_failure: "Pause and create or resume lifecycle continuity before continuing substantial work."
```

</lifecycle-contract>

<format-contract>

```yaml
rules:
  - "There is one visible interview format. Do not branch into alternate display modes."
  - "Use hard line breaks between sections; do not combine multiple metadata fields into dense status prose."
  - "Orientation output uses: Question, Recommended, Ways to answer, Progress line, emoji HUD."
  - "Design output uses: Decision, Recommended, Options, Progress line, emoji HUD."
  - "Recommended must explain why the option is recommended, not just restate the option."
  - "Each a/b/c answer gets its own mini-block with a consequence after ->."
  - "Orientation a/b/c choices are answer frames, not final design-branch alternatives."
  - "Design a/b/c choices are researched branch options."
  - "Progress is exactly one line. Do not render progress as bullets."
  - "Keep the emoji HUD. It is the fast status surface."
  - "Use d. Deep dive as the only expansion mode for evidence, gates, trade-offs, codebase exploration, or alternate lenses."
  - "Use plain ASCII arrows like => in templates."
validation: "Output has a question or decision, one recommendation, three a/b/c choices when viable, d. Deep dive, one Progress line, and one emoji HUD."
on_failure: "Rewrite using the orientation or design template. Remove progress bullet lists and display-mode wording."
```

</format-contract>

<orientation-template>
## q{n}) Clarify {weakest_dimension} ({lens_tag})

**Question**
{smallest_socratic_question}

**Recommended**
`{a|b|c}` because {why_this_answer_frame_best_reduces_ambiguity}

**Ways to answer**
`a` {answer_frame_a} -> {what_this_clarifies}

`b` {answer_frame_b} -> {what_this_clarifies}

`c` {answer_frame_c} -> {what_this_clarifies}

`d` Deep dive

Progress: `.lev/pm/designs/{design_slug}.md` | orientation | ambiguity {0.xx}/{threshold} | next: choose `a`, `b`, `c`, `d`, or `propose`

🧭 orientation | 🎯 ambiguity {0.xx}/{threshold} | ✅ alignment {xx}% | 🌿 branches {resolved}/{total} | 🧪 proof {proof_state} | ⏭️ {next_action}
</orientation-template>

<design-template>
## q{n}) {decision_title} ({lens_tag})

**Decision**
{one_sentence_decision}

**Recommended**
`{a|b|c}` because {why_recommended}

**Options**
`a` {researched_answer_a} -> {design_consequence}

`b` {researched_answer_b} -> {design_consequence}

`c` {researched_answer_c} -> {design_consequence}

`d` Deep dive

Progress: `.lev/pm/designs/{design_slug}.md` | {design|proof-shaping|ready-to-propose} | ambiguity {0.xx}/{threshold} | branches {resolved}/{total} | next: choose `a`, `b`, `c`, `d`, or `propose`

🧭 {phase} | 🎯 ambiguity {0.xx}/{threshold} | ✅ alignment {xx}% | 🌿 branches {resolved}/{total} | 🧪 proof {proof_state} | ⏭️ {next_action}
</design-template>

<deep-dive-template>
## q{n}) {decision_title} ({lens_tag})

<decision-context>
- Design artifact: `.lev/pm/designs/{design_slug}.md`
- Design section: {design_section}
- Phase: {orientation|design|proof-shaping|ready-to-propose}
- Depth threshold: {depth} / {ambiguity_threshold}
- Decision: {design_decision}
- Needed now: {why_now}
- Unblocks: {what_unblocks}
- Risk if wrong: {failure_mode}
</decision-context>

<analysis lens="{framework}">
{framework_read_of_pressure_points}
</analysis>

<decision-tree>
- Current branch: {branch_under_test}
- Resolved branches: {resolved}
- Deferred branches: {deferred}
</decision-tree>

<evidence>
- {artifact_fact_with_path}
- {code_or_doc_fact_with_path}
- {constraint_or_gate}
- {assumption_check}
</evidence>

<tradeoffs>

| Option | Benefits | Costs/Risks | Gate Impact | Side Effects |
|---|---|---|---|---|
| a | ... | ... | ... | ... |
| b | ... | ... | ... | ... |
| c | ... | ... | ... | ... |

</tradeoffs>

<options>
a. {researched_option_a} -> {design_consequence}
b. {researched_option_b} -> {design_consequence}
c. {researched_option_c} -> {design_consequence}
d. Deep dive / branch expansion
</options>

Recommended: {a|b|c} ({lens_tag}) - {why}
Progress: `.lev/pm/designs/{design_slug}.md` | {phase} | ambiguity {0.xx}/{threshold} | branches {resolved}/{total} | next: choose `a`, `b`, `c`, `d`, or `propose`

🧭 {phase} | 🎯 ambiguity {0.xx}/{threshold} | ✅ alignment {xx}% | 🌿 branches {resolved}/{total} | 🧪 proof {proof_state} | ⏭️ {next_action}
</deep-dive-template>

<ambiguity-contract>

```yaml
score:
  formula: "ambiguity = 1 - sum(clarity_i * weight_i)"
  depth_thresholds:
    quick: 0.30
    standard: 0.20
    deep: 0.15
  phase_gate: "If ambiguity is above the active depth threshold, stay in orientation. If ambiguity is at or below threshold, enter the design phase."
  dimensions:
    intent: 0.30
    outcome: 0.25
    scope: 0.20
    constraints: 0.15
    success_criteria: 0.10
  complexity_default_depth:
    formula: "complexity = novelty*.25 + blast_radius*.25 + cross_module_scope*.20 + irreversibility*.15 + evidence_gap*.15"
    quick: "complexity < 0.35"
    standard: "0.35 <= complexity < 0.70"
    deep: "complexity >= 0.70"
  design_readiness_gate: "The design is ready to propose when ambiguity is at or below the active threshold, major branches are resolved or explicitly deferred, and the design artifact can name acceptance horizon and constraints."
  progress_fields:
    design_entity: "The .lev/pm/designs artifact path or slug. It identifies the durable design, not process state."
    phase: "orientation until ambiguity is below threshold, design while resolving branches, proof-shaping while naming gates/KPIs, ready-to-propose when propose can harden it."
    ambiguity: "Weighted uncertainty. It should fall as intent, outcome, scope, constraints, and success criteria become clear."
    alignment: "Operator/design confidence that the selected branch matches the desired direction. It should rise as branches resolve."
    branches: "Resolved branch count over known branch count. It should move toward all resolved or explicitly deferred."
    proof: "Proof-design maturity. Keep details internal unless d. Deep dive is requested."
    next: "The smallest valid transition: answer, deep dive, continue auto, or propose."
  visible_output: "One recommendation, three a/b/c choices when viable, d. Deep dive, one Progress line, and one emoji HUD."
```

</ambiguity-contract>

<guardrails>

```yaml
rules:
  - "Interview output is always a design artifact under .lev/pm/designs/."
  - "Load /Users/jean-patricksmith/.agents/skills/work/templates/design.md before creating or updating the design."
  - "Do not create spec artifacts from interview output."
  - "Do not create a separate PRD artifact; PRD-style product content lives inside the design."
  - "Do not walk design branches until ambiguity is at or below the active depth threshold."
  - "If the subject or decision space is unclear, use the orientation template with three ways to answer."
  - "Quick/standard/deep controls rigor. Do not introduce alternate output modes."
  - "Never ask ingredient-only option prompts; every a/b/c answer must include a consequence after ->."
  - "Do not print hidden chain-of-thought or framework analysis unless d. Deep dive is requested."
  - "Do not mention stale provenance, deprecated project names, or internal origin stories."
  - "Use YAML for workflow, contracts, scoring, validation, and state."
  - "Use live XML sections for reusable output templates; do not wrap active XML templates in fenced Markdown blocks."
  - "Use d. Deep dive for evidence, gates, trade-offs, codebase exploration, and alternate lenses."
  - "When the user says propose, stop interviewing and route the aligned design to propose."
validation: "Output is an orientation question while ambiguity is high, then a design question after branch discovery. Both use recommendation, a/b/c choices, Progress line, and emoji HUD. Deep detail appears only after d. Deep dive."
on_failure: "Rewrite the response using the orientation or design live XML section template."
```

</guardrails>
