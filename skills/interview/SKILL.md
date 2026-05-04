---
name: interview
description: Use when guiding decision interviews that produce a design artifact in .lev/pm/designs before proposal or implementation planning.
---

# Interview

<goal>
Run a design interview. Ask one researched question at a time, recommend an answer, and walk the decision tree until a design artifact is ready under `.lev/pm/designs/`.

The interview output is a design, not a spec. It should carry the product
framing normally expected from a PRD, but inside the design artifact.
`propose` is the next lifecycle step after design alignment.
</goal>

<commands>

```bash
/interview                      # compact mode, default
/interview --compact            # explicit compact mode
/interview --full               # rich mode for complex or agent-driven flows
/interview --framework=SCAMPER  # use this lens internally; show only the tag unless --full
```

</commands>

<operational-contract>

```yaml
rules:
  - "Compact vs full changes only the amount of text shown to the user."
  - "Both modes must walk the same design tree, inspect the same codebase context, and maintain the same design artifact."
  - "Walk one branch of the design tree at a time; resolve dependencies between decisions instead of dumping all questions."
  - "If a branch can be answered by exploring the codebase, docs, workstream state, or existing artifacts, inspect those first and answer it without asking the user."
  - "Ask the user only for decisions that remain judgment-bound after lookup."
  - "For every asked question, provide the recommended answer and the design consequence of each option."
  - "Carry resolved and deferred branches forward so the design tree stays explicit."
validation: "Every interview turn has a current branch, lookup result or lookup gap, one recommended answer, and an updated unresolved branch count."
on_failure: "Do not ask another broad question. Inspect context or split the branch."
```

</operational-contract>

<process-contract>

```yaml
steps:
  - id: select_mode
    action: Choose output mode
    instruction: |
      Default to compact mode unless the user passes --full.
      Mode controls output verbosity only, not operational behavior.
      Compact mode fits roughly half a page.
      Full mode shows richer evidence and trade-offs.
    validation: "Mode is compact or full."
    on_failure: "Default to compact and state that full detail is available with --full or d. Deep dive."

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
      Before each branch question, inspect the local workspace when the answer may be discoverable.
      Search code, docs, designs, proposals, workstreams, validation gates, and existing task artifacts as relevant.
      Pull one useful artifact fact, one implementation/doc fact, and one constraint or gate when available.
      If lookup resolves the branch, update the design and move to the next branch without asking.
      If lookup cannot resolve the branch, ask the smallest human judgment question that remains.
    validation: "Each question is grounded in lookup evidence or an explicit lookup gap."
    on_failure: "Do not ask a generic question. Search files/docs first or say what evidence is missing."

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
    on_failure: "Ask one compact design question for the missing product/design requirement."

  - id: synthesize_lenses
    action: Think through perspectives silently
    instruction: |
      Consider systems thinking, first principles, trade-off analysis, Thinking Hats, and other useful lenses internally.
      Print only one compact lens tag, such as (systems thinking), near the question title or recommendation.
      Do not print a framework essay unless the user asks for d. Deep dive or uses --full.
    validation: "Output contains at most one visible lens tag in compact mode."
    on_failure: "Remove framework prose and leave only the tag."

  - id: walk_tree
    action: Resolve one decision branch
    instruction: |
      Ask one question that resolves the next meaningful branch in the design tree.
      Name the current branch and the dependency it unblocks.
      Provide three researched answers when viable; use two only if a third branch would be fake.
      Recommend one answer and name the design consequence of each option.
      Carry unresolved branches forward instead of dumping all branches at once.
    validation: "Question has current branch, lookup result or gap, one decision, 2-3 options, one recommendation, and unresolved branch count."
    on_failure: "Split the question or collapse fake options."

  - id: update_design
    action: Update the design artifact
    instruction: |
      Treat interview as a design loop, not a generic planning loop.
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

<compact-template>
## q{n}) {decision_title} ({lens_tag})

Design target: `.lev/pm/designs/{design_slug}.md` -> {design_section}
Decision: {one_sentence_decision}

Recommended: {a|b|c} - {short_reason}

a. {researched_answer_a} -> {design_consequence}
b. {researched_answer_b} -> {design_consequence}
c. {researched_answer_c} -> {design_consequence}
d. Deep dive: evidence, gates, trade-offs, codebase exploration, or alternate lens

Progress: ambiguity {0.xx}; alignment {xx%}; unresolved branches {n}
Next: answer a/b/c, ask d, or say "propose" if the design is aligned.
</compact-template>

<full-template>
## q{n}) {decision_title} ({lens_tag})

<decision-context>

- Design artifact: `.lev/pm/designs/{design_slug}.md`
- Design section: {design_section}
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

Progress: ambiguity {0.xx}; alignment {xx%}; unresolved branches {n}; design target `.lev/pm/designs/{design_slug}.md`
</full-template>

<ambiguity-contract>

```yaml
score:
  formula: "ambiguity = 1 - sum(clarity_i * weight_i)"
  dimensions:
    intent: 0.30
    outcome: 0.25
    scope: 0.20
    constraints: 0.15
    success_criteria: 0.10
  gate: "ambiguity <= 0.20 means the design is clear enough to propose."
  compact_output: "Progress: ambiguity {0.xx}; alignment {xx%}; unresolved branches {n}"
```

</ambiguity-contract>

<guardrails>

```yaml
rules:
  - "Interview output is always a design artifact under .lev/pm/designs/."
  - "Load /Users/jean-patricksmith/.agents/skills/work/templates/design.md before creating or updating the design."
  - "Do not create spec artifacts from interview output."
  - "Do not create a separate PRD artifact; PRD-style product content lives inside the design."
  - "Never ask ingredient-only option prompts; every option needs a design consequence."
  - "Do not print hidden chain-of-thought or full framework analysis in compact mode."
  - "Do not mention stale provenance, deprecated project names, or internal origin stories."
  - "Use YAML for workflow, contracts, scoring, validation, and state."
  - "Use live XML sections for reusable output templates; do not wrap active XML templates in fenced Markdown blocks."
  - "Use d. Deep dive for evidence, gates, trade-offs, codebase exploration, and alternate lenses."
  - "When the user says propose, stop interviewing and route the aligned design to propose."
validation: "Output is a compact design question by default, full only behind --full or d. Deep dive."
on_failure: "Rewrite the response using the compact live XML section template."
```

</guardrails>
