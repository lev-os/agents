---
name: propose
description: Use when turning an aligned design or captured idea into .lev/pm/tasks dna.yaml and execution.yaml through a Plan-lane alignment loop.
---

# Propose

`/propose` is the Plan-lane alignment loop. It compiles an aligned design or
captured idea into `.lev/pm/tasks/<task-id>/dna.yaml` and `execution.yaml`, but
it should not one-shot the whole plan unless the metrics and approval source
justify it.

Default posture: walk one vertical-slice decision at a time, like `/interview`
walks design decisions. A vertical slice is a narrow end-to-end behavior path
that proves the system trajectory across all required layers.

```yaml
role_contract:
  target: ".lev/pm/tasks/<task-id>/{dna.yaml,execution.yaml}"
  lane: plan
  pattern: cascade
  primary_gate: execution_ready_gate
  source_modes:
    - design
    - conversation
    - capture
    - plan
    - exploration
  upstream:
    - "/capture"
    - "/interview"
    - ".lev/pm/designs/<design>.md"
  downstream:
    - "/exec"
    - "/capture decision_point"
  hard_rule: "Do not mark a slice execution_ready without user approval or explicit auto-alignment evidence."
```

## Process

```yaml
proposal_fsm:
  steps:
    - id: load_context
      action: Read source design, conversation, captured context, existing task, workstream, and relevant repo evidence.
      validation: "Context includes intent, acceptance, constraints, entity_kind, lifecycle_target, source refs, and source_context or a named gap."
      on_failure: "Route missing product/design framing back to /interview."

    - id: score_plan
      action: Score frame, slices, determinism, verification, DNA awareness, and unresolved decisions.
      validation: "Metrics rollup is visible before asking or emitting."
      on_failure: "Do not emit artifacts."

    - id: ask_first_slice
      action: Propose one recommended vertical slice with 2-3 alternatives.
      validation: "First turn asks one slice-shape decision unless auto_emit_allowed is true."
      on_failure: "Rewrite as <proposal-turn-one>."

    - id: apply_alignment
      action: Apply each approved answer immediately to draft dna/execution state.
      validation: "Approved facts are reflected in dna source_context/acceptance/constraints or execution.slices."
      on_failure: "Ask the smallest missing alignment question."

    - id: review_slices
      action: Review slice granularity, dependencies, HITL/AFK labels, coverage, and verifiers.
      validation: "Each slice has approval_source or auto_alignment_evidence before execution_ready."
      on_failure: "Keep review_status draft or aligned."

    - id: cold_start_check
      action: Check whether a fresh agent with only the task folder can execute safely.
      validation: "Each slice has what_to_build, acceptance_criteria, operator_context, verifier_contract, and forbidden_moves."
      on_failure: "Ask for or infer the missing operator context before emit."

    - id: emit_artifacts
      action: Write or update dna.yaml and execution.yaml only after gates pass.
      validation: "execution_ready_gate and cold_start_context_gate pass; no unresolved proposal-level decisions remain."
      on_failure: "Show next alignment action, not an exec menu."

    - id: offer_exec
      action: Show one compact execution offer, with more only on request.
      validation: "Exec menu appears only after execution_ready_gate passes."
      on_failure: "Replace exec menu with the next proposal alignment question."
```

```yaml
auto_emit_allowed_when:
  - frame_completeness == 1.0
  - slice_readiness >= 0.9
  - determinism == 1.0
  - verification_strength >= 0.9
  - cold_start_context_gate == pass
  - unresolved == 0
  - approval_source != null or auto_alignment_evidence != []
otherwise:
  first_turn: ask_first_slice
```

## Contracts

```yaml
dna_yaml:
  path: ".lev/pm/tasks/<task-id>/dna.yaml"
  required:
    ontology: "<from dna/graph.yaml>"
    intent: "<one-sentence purpose>"
    entity_kind: "<type from dna/entities.yaml>"
    lifecycle_target: "<target state>"
    acceptance:
      - "<pass/fail criterion>"
    local_refs:
      - "<designs, specs, docs, plans, code refs>"
    local_constraints:
      - "<scope fence or invariant>"
    source_context:
      mode: "design | conversation | capture | plan | exploration"
      summary: "<what source material established>"
      refs:
        - "<file path, transcript marker, plan path, screenshot note, or workstream ref>"
      confidence: 0.0-1.0
      inferred_without_design_file: false
  when_from_design:
    source_design: ".lev/pm/designs/<design-slug>.md"
    execution_slice_map: "execution.yaml:slices"
    grouping_reason: "<why this effort can live in one task folder>"

execution_yaml:
  path: ".lev/pm/tasks/<task-id>/execution.yaml"
  required:
    topology: "sequence | protocol | strategy | judgment | cascade | loop | fan_out | reducer"
    runtime_profile: "<profile>"
    validation_chain:
      - frame_complete_gate
      - plan_alignment_gate
      - convergence_gate
      - slice_verticality_gate
      - slice_alignment_gate
      - feedback_loop_gate
      - cold_start_context_gate
      - adversarial_constraint_gate
      - execution_ready_gate
    receipt_policy: append_only
    checkpoint_policy: forward_only
    budget:
      max_iterations: "<N>"
      timeout: "<duration>"
    exit_conditions:
      - "<deterministic done condition>"
    slices:
      - id: "<slice-id>"
        title: "<demoable behavior slice>"
        focus: "<one behavior path this slice proves>"
        type: "AFK | HITL"
        blocked_by: []
        what_to_build: "<issue-body level description of the vertical slice>"
        why_this_slice: "<why this is the right next behavioral cut>"
        acceptance_criteria:
          - "<slice-level pass/fail criterion>"
        operator_context:
          exact_inputs:
            - "<fixtures, turns, commands, source artifacts, env assumptions>"
          known_reds:
            - "<allowed honest-red failures>"
          forbidden_moves:
            - "<boundaries a cold agent must not cross>"
          hitl_protocol: "<what human verifies, if HITL>"
        verifier_contract:
          command: "<command or HITL capture path>"
          inputs:
            - "<required input>"
          outputs:
            - "<required output/receipt>"
          pass_fail: "<plain rule>"
        stages:
          - id: "<stage-id>"
            action: "<implementation or validation step inside this slice>"
            verify: "<stage-level command, check, or receipt>"
        design_refs:
          - ".lev/pm/designs/<design-slug>.md#<section>"
        write_scope:
          - "<concrete path or glob>"
        constraints:
          - "<scope fence or invariant>"
        failure_modes:
          - "<what this slice must not break>"
        verify: "<one command or structured HITL capture path>"
        gates:
          - slice_verticality_gate
          - feedback_loop_gate
          - adversarial_constraint_gate
```

```yaml
slice_rules:
  vertical_slice: "A thin end-to-end path that proves the whole system trajectory."
  prefer: "3-5 thin slices for medium work; 1 only when the design is one behavior path."
  forbidden:
    - "schema-only slice"
    - "API-only slice"
    - "UI-only slice"
    - "docs-only slice"
    - "tests-only slice"
  required_per_slice:
    - id
    - title
    - type
    - blocked_by
    - behavior_coverage
    - acceptance
    - what_to_build
    - why_this_slice
    - acceptance_criteria
    - operator_context
    - verifier_contract
    - stages
    - focus
    - constraints
    - failure_modes
    - verify
    - review_status
    - approval_source
```

## Gates

```yaml
metrics:
  frame_completeness:
    weight: 0.25
    pass: "intent, acceptance, constraints, entity_kind, lifecycle_target, topology are present"
  slice_readiness:
    weight: 0.25
    pass: "slices are vertical, covered, dependency-ordered, reviewed, and execution_ready"
  determinism:
    weight: 0.20
    pass: "zero unresolved forks, hedges, or executor choices"
  verification_strength:
    weight: 0.15
    pass: "each slice has exactly one deterministic verifier or structured HITL path"
  dna_awareness:
    weight: 0.15
    pass: "rule sets land in DNA-backed registries with schema and index when applicable"
  execution_ready_gate: "weighted score >= 0.90 and all hard gates pass"
  compact_output: "Plan: frame {xx%}; slices {xx%}; determinism {xx%}; verify {xx%}; unresolved {n}"

hard_gates:
  frame_complete_gate: "dna.acceptance.length >= 1 and execution.topology exists"
  plan_alignment_gate: "first-turn or slice-review alignment happened, or auto_emit_allowed_when is proven"
  slice_verticality_gate: "every slice cuts through required layers and is demoable/verifiable"
  slice_alignment_gate: "granularity, dependencies, HITL/AFK, coverage, verifier reviewed"
  feedback_loop_gate: "each slice has one verifier or one HITL capture path"
  cold_start_context_gate: "a fresh agent can execute from the task folder without this conversation"
  adversarial_constraint_gate: "each slice lists constraints, failure modes, and out-of-scope boundaries"
  behavior_coverage_gate: "each acceptance target or source design decision is covered"
  dna_execution_gate: "execution.slices cover dna.acceptance, constraints, and source_context"
```

```yaml
determinism_gate:
  forbidden_patterns:
    proposal_level_or: ["either X or Y", "A or B", "one of X/Y/Z"]
    acceptance_options: ["pick one", "options: a, b, c"]
    quantity_hedges: ["at minimum", "at least", "possibly including", "and more"]
    mechanism_hedges: ["via X, build step, or Y"]
    name_level_or: ["stage ids containing unresolved 'or'"]
  allowed_patterns:
    predicate_or: "Boolean OR inside an eval expression."
    exhaustive_list: "Exact enumerated list."
    default_with_overrides: "Default plus explicit override set."
  repair_loop:
    - "Research with shell/rg/read to resolve by evidence."
    - "If evidence resolves, update draft and rescore."
    - "If evidence does not resolve, ask /interview-style alignment question."
    - "Never emit while the fork remains."
```

```yaml
dna_awareness_gate:
  applies_when: "proposal ships rule sets, invariants, gates, constraints, policies, standards, or validation semantics"
  discover_roots:
    - ".lev/config.yaml paths.dna"
    - ".lev/config.yaml contracts.<name>.source"
    - ".lev/config.yaml flows.roots[]"
    - "fallback: dna/, .lev/dna/, data/dna/, plugins/dna/"
  rules:
    - "Extend existing registry before creating a new one."
    - "If creating a registry, include schema and meta-contract."
    - "Index new registries in canonical_contracts[] when the project has an index."
    - "Keep rules in DNA/data; code is the runner, not the holder."
    - "Backrefs both ways: prompts/tests/fixtures cite DNA ids and meta-contract asserts parity."
  fail_examples:
    - "Python literals holding semantic invariants."
    - "Bespoke config yaml instead of DNA conventions."
    - "Unindexed registry."
```

## Output Templates

<proposal-turn-one>
## Proposal Alignment: {task_id}

Current stage: {stage_name}

Recommended vertical slice: {recommended_slice}

Why this first: {short_reason}

a. {option_a} -> {consequence}
b. {option_b} -> {consequence}
c. {option_c} -> {consequence}
d. Deep dive: dependencies, gates, alternatives, or codebase evidence

Progress: frame {xx%}; slices {xx%}; determinism {xx%}; verify {xx%}; unresolved {n}
Next: answer a/b/c, ask d, or say "emit" if this is already aligned.
</proposal-turn-one>

<slice-review>
## Slice Review: {task_id}

Plan: frame {xx%}; slices {xx%}; determinism {xx%}; verify {xx%}; unresolved {n}

1. {title} -- {AFK|HITL}; blocked_by {ids|None}; covers {target}; verify {check}; cold-start {pass|gap}; {draft|aligned|execution_ready}

Missing operator context: {fixtures_commands_known_reds_contracts_or_none}

Review question: {one_question_needed_to_advance}
</slice-review>

<final-proposal>
## Proposal: {task_id}

### DNA
- {intent_or_end_state}
- {acceptance_highlight}
- {constraint_or_boundary}

### Plan Alignment
Plan: frame {xx%}; slices {xx%}; determinism {xx%}; verify {xx%}; unresolved 0

### Slice Review
1. {title} -- {AFK|HITL}; blocked_by {ids|None}; covers {target}; verify {check}; cold-start pass; execution_ready via {approval_source}

### Execution
- {topology_and_profile}
- {critical_stage_or_verifier}
- {exit_condition}

### Operator Context
- Inputs: {fixtures_commands_artifacts}
- Known reds: {allowed_failures_or_none}
- Forbidden moves: {boundaries}
- Verifier contract: {command_inputs_outputs_pass_fail}

Next: run `/exec {task_id}`, queue via `/capture`, or ask for the full exec menu.
</final-proposal>

<exec-menu>
## Exec Offer: {task_id}

Best next slice: {slice_title}

INTENT: {one_sentence_end_state}
STRATEGY: {approach_not_file_list}
VERIFY: {plain_english_done_proof}

Route: /exec -> {adapter} -> {model}; unblocks {stage_ids}

More: say "full menu" to see remaining slices.
</exec-menu>

## Rendering Rules

```yaml
rendering:
  default_before_ready: proposal-turn-one
  during_review: slice-review
  after_ready: final-proposal
  exec_menu: "single best next slice by default; full menu only when requested"
  max_visible_slices: 5
  never_show:
    - raw file path lists in exec cards
    - git diff verbs
    - nested option dumps
    - exec menu when unresolved > 0
```

```yaml
exec_routing:
  adapter_guidance:
    scout: "inventory, audit, evidence, prior-art"
    pi: "scout-only prior-art/evidence; never implementation"
    direct: "small deterministic artifact update"
    codex: "code implementation or integration"
    claude-agent-sdk: "review, verification, boundary enforcement"
  model_guidance:
    haiku: "fast evidence gathering"
    sonnet: "standard implementation"
    codex-5.4-xhigh: "complex coding/integration"
    opus: "deep design/tradeoff resolution"
    default: "small deterministic update"
  hard_rules:
    - "Adapter is execution mechanism; model is reasoning tier."
    - "Do not put opus/haiku/sonnet in adapter."
    - "Do not default every item to the same adapter."
```

## Anti-Patterns

| Rationalization | Correction |
|---|---|
| "The executor can pick." | Then `/propose` did not finish; ask or research first. |
| "Both options are valid." | Evidence decides, or the user decides. |
| "I'll show all slices now." | First turn is one vertical slice unless auto_emit_allowed_when is proven. |
| "These slices are execution_ready." | Need approval_source or explicit auto-alignment evidence. |
| "Leaving flexibility for future." | Flexibility at propose time becomes ambiguity at exec time. |
| "Rules inline are faster." | Rule sets belong in DNA-backed registries when applicable. |
| "The task is too complex." | Shard it; each shard still needs deterministic execution. |

## Related

- `/interview` reduces ambiguity and produces `.lev/pm/designs/`.
- `/capture` inventories, routes, and queues.
- `/exec` runs execution-ready stages.
- `/work` routes lifecycle lanes and reports HUD state.
