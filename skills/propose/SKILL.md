---
name: propose
description: Use when compiling an aligned design, capture, or chat intent into execution-ready task DNA and execution YAML.
skill_type: workflow
category: lifecycle
output_template: hud
---

# /propose - Execution Packet Lane

`/propose` first freezes aligned context into a compact execution transition
packet, then compiles one vertical slice into
`.lev/pm/tasks/<task-id>/{dna.yaml,execution.yaml}`. It does not plan broadly
and it does not execute. It prepares a cold-startable entity for `/exec`.

Use either `/plan` or `/propose` for a given turn. `/plan` creates or reviews a
human runbook. `/propose` emits executable task artifacts from already-aligned
intent. If alignment is missing, route to `/interview`, not `/plan`.

## Work Link
Lifecycle lane: Execution preparation
Entity movement: `captured | aligned -> proposed | execution_ready | needs_interview`
Workstream: resolve active workstream before writing task artifacts
Upstream: `/capture`, `/interview`, `.lev/pm/designs/*`, aligned chat intent
Downstream: `/exec`, `/capture`
Adjacent: `/plan` is a standalone planning lane, not a prerequisite
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Adversarial Contract

Do not run a broad evidence sweep before the transition packet exists. The
first turn preserves the current alignment so compaction or handoff cannot turn
proposal work into generic planning. If the packet cannot name one executable
slice, one verifier path, and write boundaries, route to `/interview`.

<transition-packet>
## Proposal Transition: {task_id}

Intent: {one_sentence_intent}
Source: {chat|capture|design|task}; refs {known_refs_or_none}
Acceptance: {known_acceptance_or_gap}
Constraints: {write_scope_boundaries_forbidden_moves}
Open forks: {none_or_smallest_unresolved_decisions}
Recommended first slice: {one_vertical_slice_or_gap}
Execution proof: {known_verifier_or_gap}
Next: answer one question, say `emit`, route to `/interview`, or use `/plan` only if the user asked for a runbook/review.
</transition-packet>

## Execution-Readiness Contract

FlowMind plus deterministic Lev SDK validation is the authority after `emit`:

1. Run or emulate `plugins/sdlc/flows/propose-adversarial-contract.flow.yaml`.
2. Author claim ledger, reverse brainstorm, failure hypotheses, falsifying
   fitness functions, verifier adequacy critique, and artifact rewrite.
3. For non-trivial, runtime, agentic, promotion, cleanup, fallback, or boundary-risk
   work, run the Pentagon-LFD design pass: target, constraints, instruments,
   forced entropy, dev/holdout policy, cheap-path cheats, and preflight
   calibration.
4. Run `lev task validate <task-id|task-path>` before marking execution-ready.
5. Never treat `execution_ready`, unit tests, no-regression, or verifier
   existence as proof of behavior without claim evidence.

Hard rule: important source-design claims map to `claim_coverage`,
`verifier_contract`, false-green hypotheses, falsifying fitness functions, and
receipt fields for command, exit code, files touched, verdicts, and evidence.
If LFD-shaped proof is required, include a scoreable loss-function target,
constraints, instruments, eval split, cheap-path fences, and preflight
calibration. If that cannot be designed from current evidence, ask one
alignment question instead of emitting task artifacts.

Execution focus rule: proposal output must be the smallest executable slice that
proves a behavior or receipt. Do not output a multi-option work plan when the
design, capture, or chat already chooses a direction.

## Capture Ledger Intake

If the proposal came from `/capture` or `/dump`, load the source ledger row
before writing task artifacts. Preserve `intent_id`, `topic`,
`compiled_intent`, `artifact_ref`, `route_state`, `fidelity`, `next_route`, and
`blocker` in `source_context.capture_ledger`. If no ledger exists, create a
proposal-local ledger row and mark `current_location: memory` until the task
folder is written.

## Canon Write Gate

If the user asks what would be proposed, edited, or planned, render
`<transition-packet>`, `<proposal-turn-one>`, or `<slice-review>` only. Write
task artifacts only after explicit apply/edit/emit/patch authorization or an
existing approved capture row with `next_route: /propose`. Never interpret a
proposal artifact as permission to implement.

## Proposal Readout

After emitting or updating a task from a design, render a short readout. This is
for human sanity, not an exec gate:

Do one separate compare pass against the source design/capture before readout.
Cover boundaries, operator outcome, acceptance, verifier/preflight, and open decisions.

If the readout exposes an obvious proposal mistake, fix the task before calling
it proposed. Keep executable-readiness policy in Lev validation/SDK, not in this
skill prose.

## Protocol

```yaml
steps:
  - id: transition_freeze
    action: Render the compact transition packet before broad lookup or task writes.
    validation: "Intent, source, known refs, acceptance or gap, constraints, open forks, first slice, and next action are visible."
    on_failure: "Stop and render <transition-packet>; do not gather more context yet."

  - id: load_context
    action: After transition_freeze, read only source design, capture, workstream, existing task, and repo evidence needed for unresolved fields.
    validation: "Context includes intent, acceptance, constraints, entity_kind, lifecycle_target, refs, confidence, and any design-to-propose handoff."
    on_failure: "Route missing product/design framing to /interview."

  - id: load_capture_ledger
    action: Reconcile source capture/dump ledger rows before proposal emission.
    validation: "Captured sources have a ledger row with compiled_intent, artifact_ref, route_state, fidelity, next_route, and blocker."
    on_failure: "Route to /capture before writing task artifacts."

  - id: score_frame
    action: Score frame completeness, slice readiness, determinism, verification, and DNA awareness.
    validation: "Metrics rollup is visible before asking or emitting."
    on_failure: "Do not write task artifacts."

  - id: design_pentagon_lfd
    action: Generate the Pentagon-LFD proof target when proof risk requires it.
    validation: "Target, constraints, instruments, forced entropy, eval cases, cheap paths, and preflight calibration are present or explicitly not applicable."
    on_failure: "Render <proposal-turn-one>; do not emit execution-ready artifacts."

  - id: align_slice
    action: Select exactly one recommended vertical execution slice unless auto-emit gates pass.
    validation: "One executable slice-shape decision is resolved or auto_emit evidence is present."
    on_failure: "Render <proposal-turn-one>."

  - id: build_contract
    action: Draft dna.yaml and execution.yaml with topology, runtime profile, claims, proof_gates, receipts, write scope, and forbidden moves.
    validation: "A fresh agent can execute using only the task folder and source_context.capture_ledger preserves the source row."
    on_failure: "Ask the smallest missing operator-context question."

  - id: validate_task
    action: Run `lev task validate <task-id|task-path>`.
    validation: "Validation exits 0 before execution_ready is claimed."
    on_failure: "Route back through proposal graph; do not offer /exec."

  - id: proposal_readout
    action: Compare proposal to source design/capture, then render the short human readout after proposal emission or update.
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
- `pentagon_lfd_preflight == pass | not_applicable_with_rationale`
- `unresolved == 0`
- `approval_source != null` or `auto_alignment_evidence != []`

## Required Task Shape

```yaml
dna_yaml.required:
  [ontology, intent, entity_kind, lifecycle_target, acceptance, local_refs, local_constraints, source_context]
source_context.capture_ledger:
  [intent_id, topic, compiled_intent, artifact_ref, route_state, fidelity, next_route, blocker]
source_context.design_handoff_required_when_from_design:
  [recommendation, first_slice, acceptance_horizon, proof_design, forbidden_moves, unresolved_forks]
execution_yaml.required:
  [topology, runtime_profile, validation_chain, proof_gates, receipt_policy, checkpoint_policy, budget, exit_conditions, slices]
slice.required:
  [id, title, behavior_coverage, what_to_build, why_this_slice, acceptance_criteria, operator_context, verifier_contract, write_scope, constraints, failure_modes, review_status, approval_source]
proof_gates.required_when:
  [non_trivial, runtime_or_agentic_behavior, promotion_decision, cleanup_or_refactor, fallback_or_boundary_risk]
proof_gates.shape:
  pentagon: { target, promotion_decision, highest_risk_claim, axes, receipts, lfd? }
  lfd: { target, constraints, instruments, eval_split, cheap_path_fences, preflight }
  ultraqa: { mode: dynamic_e2e_inside_pentagon, goal, required_scenario_classes, baseline, scenario_matrix }
  quality: { ai_slop_cleaner: { required, reason, scope, review_gate } }
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
| pentagon_lfd_preflight | loss-function target and cheap-path preflight exist for proof-risk work, or N/A is justified |
| execution_ready_gate | weighted score >= 0.90 and all hard gates pass |

## Determinism Repair

Resolve "either/or", option lists, quantity hedges, mechanism hedges, and
executor-choice ambiguity by repo evidence or one alignment question. Never emit
while the fork remains.

## Output Templates

<proposal-turn-one>
## Execution Alignment: {task_id}

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

Readiness: frame {xx%}; slices {xx%}; determinism {xx%}; verify {xx%}; unresolved {n}
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

### Execution Packet
Readiness: frame {xx%}; slices {xx%}; determinism {xx%}; verify {xx%}; unresolved 0

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

- "I'll gather the repo first, then summarize the proposal."
- "Compaction can recover the plan from chat."
- "The proposal task exists, so implementation can start."
- "The executor can pick."
- "I'll run plan first."
- "Both options are valid."
- "I'll show all slices now."
- "These slices are execution_ready."
- "Rules inline are faster."
- "Verifier exists, so it is safe to execute."
- "QA can be figured out after implementation."
- "Pentagon means put the test in core/testing."
- "Pentagon means scenario list only; no target, instruments, or cheap-path preflight."
- "A generated eval design is enough without known-good/known-bad calibration."
- "The capture ledger can be dropped once task DNA exists."
- "What would you propose means write task DNA."
- "The plan exists, so propose is automatic."
