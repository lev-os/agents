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

## Protocol

```yaml
steps:
  - id: load_context
    action: Read source design, capture, workstream, existing task, and repo evidence.
    validation: "Context includes intent, acceptance, constraints, entity_kind, lifecycle_target, refs, and confidence."
    on_failure: "Route missing product/design framing to /interview."

  - id: score_frame
    action: Score frame completeness, slice readiness, determinism, verification, and DNA awareness.
    validation: "Metrics rollup is visible before asking or emitting."
    on_failure: "Do not write task artifacts."

  - id: align_slice
    action: Propose one recommended vertical slice with alternatives unless auto-emit gates pass.
    validation: "One slice-shape decision is resolved or auto_emit evidence is present."
    on_failure: "Render <proposal-turn-one>."

  - id: build_contract
    action: Draft dna.yaml and execution.yaml with claims, slices, verifiers, write scope, and forbidden moves.
    validation: "A fresh agent can execute using only the task folder."
    on_failure: "Ask the smallest missing operator-context question."

  - id: validate_task
    action: Run `lev task validate <task-id|task-path>`.
    validation: "Validation exits 0 before execution_ready is claimed."
    on_failure: "Route back through proposal graph; do not offer /exec."

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
execution_yaml:
  required:
    - topology
    - runtime_profile
    - validation_chain
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
```

## Gates

| Gate | Pass condition |
|---|---|
| frame_complete_gate | intent, acceptance, constraints, entity_kind, lifecycle_target, topology present |
| slice_verticality_gate | every slice proves a demoable behavior path |
| feedback_loop_gate | each slice has one verifier or HITL capture path |
| cold_start_context_gate | fresh agent can execute from task folder |
| behavior_coverage_gate | every acceptance/source-design claim is covered |
| execution_ready_gate | weighted score >= 0.90 and all hard gates pass |

## Determinism Repair

Resolve "either/or", option lists, quantity hedges, mechanism hedges, and
executor-choice ambiguity by repo evidence or one alignment question. Never emit
while the fork remains.

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

### Execution
- {topology_and_profile}
- {critical_stage_or_verifier}
- {exit_condition}

Next: run `/exec {task_id}`, queue via `/capture`, or ask for the full exec menu.
</final-proposal>

## Red Flags

- "The executor can pick."
- "Both options are valid."
- "I'll show all slices now."
- "These slices are execution_ready."
- "Rules inline are faster."
- "Verifier exists, so it is safe to execute."

## Related

- `/work` routes lifecycle lanes.
- `/capture` provides captured entities and fidelity.
- `/exec` runs execution-ready slices.
