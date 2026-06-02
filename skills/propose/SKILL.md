---
name: propose
description: Use when turning an aligned design or captured idea into task DNA and execution YAML through the Plan lane.
skill_type: workflow
category: lifecycle
output_template: hud
---

# /propose - Plan Lane

`/propose` compiles aligned context into
`.lev/pm/tasks/<task-id>/{dna.yaml,execution.yaml}`. It does not execute. It
prepares a cold-startable entity for `/exec`.

## Work Link

Lifecycle lane: Plan
Entity movement: `captured | aligned -> proposed | execution_ready | needs_interview`
Workstream: resolve active workstream before writing task artifacts
Upstream: `/capture`, `/interview`, `.lev/pm/designs/*`
Downstream: `/exec`, `/capture`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Adversarial Contract

FlowMind plus deterministic Lev SDK validation is the authority:

1. Run or emulate `plugins/sdlc/flows/propose-adversarial-contract.flow.yaml`.
2. Author claim ledger, reverse brainstorm, failure hypotheses, falsifying
   fitness functions, verifier adequacy critique, and artifact rewrite.
3. Run `lev task validate <task-id|task-path>` before marking execution-ready.
4. Never treat `execution_ready`, unit tests, no-regression, or verifier
   existence as proof of behavior without claim evidence.

Hard rule: important source-design claims must map to `claim_coverage`,
`verifier_contract`, reverse false-green hypotheses, falsifying fitness
functions, and production trace fields: `receipt_id`, `exec_id`, `flow`,
`task`, `slice`, `node_id`, `branch_taken`, `verifier_command`,
`stdout_path`, `stderr_path`, `exit_code`, `files_touched`,
`claim_verdicts`, and `evidence_ref`.

## Capture Ledger Intake

If the proposal came from `/capture` or `/dump`, load the source ledger row
before writing task artifacts. Preserve `intent_id`, `topic`,
`compiled_intent`, `artifact_ref`, `route_state`, `fidelity`, `next_route`, and
`blocker` in `source_context.capture_ledger`. If no ledger exists, create a
proposal-local ledger row and mark `current_location: memory` until the task
folder is written.

## Canon Write Gate

If the user asks what would be proposed, edited, or planned, render
`<proposal-turn-one>` or `<slice-review>` only. Write task artifacts only after
explicit apply/edit/emit/patch authorization or an existing approved capture
row with `next_route: /propose`.

## Proposal Readout

After emitting or updating a task from a design, render a short readout. This is
for human sanity, not an exec gate:

- run `bash -lc 'sleep 2'` when a shell is available, then do one separate
  compare pass against the source design/capture before rendering the readout
- key boundaries and where they came from
- user story or operator outcome
- acceptance criteria
- test strategy or preflight checks
- open decisions or known blockers

If the readout exposes an obvious proposal mistake, fix the task before calling
it proposed, then run `bash -lc 'sleep 2'` once more and reread the final
readout. Keep executable-readiness policy in Lev validation/SDK, not in this
skill prose.

## Protocol

```yaml
steps:
  - id: load_context
    action: Read source design, capture, workstream, existing task, and repo evidence.
    validation: "Context includes intent, acceptance, constraints, entity_kind, lifecycle_target, refs, and confidence."
    on_failure: "Route missing product/design framing to /interview."

  - id: load_capture_ledger
    action: Reconcile source capture/dump ledger rows before proposal emission.
    validation: "Captured sources have a ledger row with compiled_intent, artifact_ref, route_state, fidelity, next_route, and blocker."
    on_failure: "Route to /capture before writing task artifacts."

  - id: score_frame
    action: Score frame completeness, slice readiness, determinism, verification, and DNA awareness.
    validation: "Metrics rollup is visible before asking or emitting."
    on_failure: "Do not write task artifacts."

  - id: align_slice
    action: Propose one recommended vertical slice with alternatives unless auto-emit gates pass.
    validation: "One slice-shape decision is resolved or auto_emit evidence is present."
    on_failure: "Render <proposal-turn-one>."

  - id: build_contract
    action: Draft dna.yaml and execution.yaml with claims, slices, proof_gates, verifiers, write scope, and forbidden moves.
    validation: "A fresh agent can execute using only the task folder and source_context.capture_ledger preserves the source row."
    on_failure: "Ask the smallest missing operator-context question."

  - id: validate_task
    action: Run `lev task validate <task-id|task-path>`.
    validation: "Validation exits 0 before execution_ready is claimed."
    on_failure: "Route back through proposal graph; do not offer /exec."

  - id: proposal_readout
    action: Run `bash -lc 'sleep 2'` when available, compare proposal to source design/capture, then render the short human readout after proposal emission or update.
    validation: "Critical boundaries, story, acceptance, tests/preflight, and open decisions are visible."
    on_failure: "Fix obvious proposal mistakes before offering /exec."

  - id: offer_exec
    action: Offer the single best next exec slice.
    validation: "Exec offer appears only when unresolved == 0 and execution_ready_gate passes."
    on_failure: "Show next alignment question instead."
```

## Auto Emit Gate

Only write or mark execution-ready when all are true:

- `frame_completeness == 1.0`
- `slice_readiness >= 0.9`
- `determinism == 1.0`
- `verification_strength >= 0.9`
- `cold_start_context_gate == pass`
- `proof_gate_design == pass | not_applicable_with_rationale`
- `unresolved == 0`
- `approval_source != null` or `auto_alignment_evidence != []`

## Required Task Shape

```yaml
dna_yaml:
  required:
    - ontology
    - intent
    - entity_kind
    - lifecycle_target
    - acceptance
    - local_refs
    - local_constraints
    - source_context
source_context:
  capture_ledger:
    - intent_id
    - topic
    - compiled_intent
    - artifact_ref
    - route_state
    - fidelity
    - next_route
    - blocker
execution_yaml:
  required:
    - topology
    - runtime_profile
    - validation_chain
    - proof_gates
    - receipt_policy: append_only
    - checkpoint_policy: forward_only
    - budget
    - exit_conditions
    - slices
slice_required:
  - id
  - title
  - behavior_coverage
  - what_to_build
  - why_this_slice
  - acceptance_criteria
  - operator_context
  - verifier_contract
  - write_scope
  - constraints
  - failure_modes
  - review_status
  - approval_source
proof_gates_required_when:
  - non_trivial
  - runtime_or_agentic_behavior
  - promotion_decision
  - cleanup_or_refactor
  - fallback_or_boundary_risk
proof_gates_shape:
  pentagon:
    target: "<task or product surface>"
    promotion_decision: "<decision this proof gates>"
    highest_risk_claim: "<claim that costs money, trust, safety, or architecture integrity if false>"
    axes:
      contract_unit: { proof: "...", gates: [] }
      integration: { proof: "...", gates: [] }
      surface_e2e: { proof: "...", gates: [] }
      harness_ratchet: { proof: "...", gates: [] }
      adversarial_eval: { proof: "...", gates: [] }
    receipts: []
  ultraqa:
    mode: dynamic_e2e_inside_pentagon
    goal: "<hostile runtime QA goal>"
    required_scenario_classes: [normal_path, malformed_input, prompt_injection, cancel_resume, stale_state, dirty_worktree, hung_command, flaky_or_retried, misleading_success_output]
    baseline: []
    scenario_matrix: []
  quality:
    ai_slop_cleaner:
      required: true | false
      reason: "<cleanup/refactor/fallback/boundary risk>"
      scope: []
      review_gate: "<verifier or N/A>"
```

## Gates

| Gate | Pass condition |
|---|---|
| frame_complete_gate | intent, acceptance, constraints, entity_kind, lifecycle_target, topology present |
| slice_verticality_gate | every slice proves a demoable behavior path |
| feedback_loop_gate | each slice has one verifier or HITL capture path |
| cold_start_context_gate | fresh agent can execute from task folder |
| behavior_coverage_gate | every acceptance/source-design claim is covered |
| proof_gate_design | required proof gates exist, or task explains why QA/Pentagon is not applicable |
| execution_ready_gate | weighted score >= 0.90 and all hard gates pass |

## Determinism Repair

Resolve "either/or", option lists, quantity hedges, mechanism hedges, and
executor-choice ambiguity by repo evidence or one alignment question. Never emit
while the fork remains.

## Output Templates

<proposal-turn-one>
## Proposal Alignment: {task_id}

Current stage: {stage_name}
Ledger: {intent_id_or_none}; fidelity {fidelity_pct_or_unknown}; artifact {artifact_ref_or_none}; state {route_state}; blocker {blocker_or_none}

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
Ledger: {intent_id_or_none}; source {artifact_ref_or_none}; fidelity {fidelity_pct_or_unknown}; state {route_state}; blocker {blocker_or_none}

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

### Ledger
- source: {intent_id_or_none} from {artifact_ref_or_none}
- compiled_intent: {compiled_intent}
- fidelity: {fidelity_pct_or_unknown}; state: {route_state}; route: {next_route}; blocker: {blocker_or_none}

### Execution
- {topology_and_profile}
- {critical_stage_or_verifier}
- {exit_condition}

### Readout
- boundaries: {critical_boundaries_and_sources}
- story: {operator_outcome}
- acceptance: {acceptance_summary}
- tests/preflight: {test_or_preflight_summary}
- open decisions: {none_or_decisions}

Next: run `/exec {task_id}`, queue via `/capture`, or ask for the full exec menu.
</final-proposal>

## Red Flags

- "The executor can pick."
- "Both options are valid."
- "I'll show all slices now."
- "These slices are execution_ready."
- "Rules inline are faster."
- "Verifier exists, so it is safe to execute."
- "QA can be figured out after implementation."
- "Pentagon means put the test in core/testing."
- "The capture ledger can be dropped once task DNA exists."
- "What would you propose means write task DNA."

## Related

- `/work` routes lifecycle lanes.
- `/capture` provides captured entities and fidelity.
- `/exec` runs execution-ready slices.
