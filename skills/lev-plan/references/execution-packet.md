# Execution Packet

Detail for `lev-plan` Emit mode: what `emit_slice` and `validate_structure`
need. The workflow and the Write Gate live in [`../SKILL.md`](../SKILL.md);
the claims, their checks, the admission loop, and the TDD rules live in
[Proof](proof.md). This file adds no step.

## Contents

- [Packet Location and Timing](#packet-location-and-timing): where the one packet goes and when it is written
- [Requirements Ledger](#requirements-ledger): where the claims are written in the task
- [Flow and Launch](#flow-and-launch): where the flow is chosen and named, launch instructions
- [Emitted Task Shape](#emitted-task-shape): required fields of `dna.yaml` and `execution.yaml`, `lifecycle_stage` values
- [Emission Gate](#emission-gate): conditions that all hold before a packet is written
- [Final Output](#final-output): the `<final-proposal>` template

## Packet Location and Timing

Emit writes exactly one `{dna.yaml,execution.yaml}` packet in the task folder
of the workstream that owns the slice:
`.lev/pm/workstreams/<workstream-id>/tasks/<task-id>/`. Use
`.lev/pm/tasks/<task-id>/` only when no workstream owns it. Both places are
declared in `core/workstream/config.yaml` (`entity_definitions.task`).

Materialize a task just before it enters the ready set. Regenerate from the
current source when a design, dependency, or boundary has changed. The other
slices stay in the map until their turn.

## Requirements Ledger

The slice's claims are written as one `requirements:` list in the task's
`dna.yaml` (`schema: lev.task.v2`). The three passes, the row and `check:`
shape, and the guards are in [Proof](proof.md); read it before you write a
row. Carry each plan claim in with its `source_ref` and its stable id.

When the list outgrows `dna.yaml`, move rows to `evals/<name>.yaml` in the
task folder under the same `requirements:` key. That file holds overflow
rows of the one ledger; it defines no evaluator.

## Flow and Launch

The packet does not select the flow; the launch does.

- **`topology` stays a slice classification** (for example
  `single_vertical_slice`). It never names a flow.
- **Selected current flow.** Choose it under
  [Proof and Evaluator Selection](proof.md#proof-and-evaluator-selection),
  which says what the eval gate reads; the packet needs no flow or evaluator
  field.
- **Launch instructions.** State them in the final output with the flow passed
  explicitly: `lev entity task validate <task>`, then
  `lev sdlc exec <task> --flow <flow>`. Planning writes the instructions; Exec
  runs them.
- **Unresolved binding.** When no current flow fits, the slice is a hold under
  "Hold, never drop" in that section; a default flow is never chosen in its
  place.

## Emitted Task Shape

```yaml
dna_yaml.required:
  [schema (lev.task.v2), ontology, intent, entity_kind, lifecycle_target, lifecycle_stage, requirements, local_refs, source_context]

source_context.required:
  [capture_refs, plan_ref_or_not_required, plan_digest_or_na, covered_intent_ids, source_fidelity]

execution_yaml.required:
  [topology, runtime_profile_ref, dependencies, structural_preconditions, slices, exit_conditions]

slice.required:
  [id, operator_outcome, what_to_build, write_scope]

shared_contract_refs:
  [standards_ref, execution_evidence_profile_ref, proof_profile_ref]
```

`topology` is the slice classification. `shared_contract_refs` in this listing
names the three existing individual refs (`standards_ref`,
`execution_evidence_profile_ref`, `proof_profile_ref`); it is not a container
key.

`lifecycle_stage` uses the current domain enum: `ephemeral`, `captured`,
`crystallizing`, `crystallized`, `manifesting`, `completed`, `discarded`. A
prepared, validated packet is `crystallized`. `proposed` and `execution_ready`
are route and readiness states, not values of that enum, and they never mean
implemented or completed.

Add an existing field only when this slice needs it; the packet keeps its
current keys. A fresh executor must be able to resolve references and act
without reading the originating chat.

## Emission Gate

Emit only when all are true:

- one slice is selected
- semantic readiness is `ready`
- no semantic dimension is `insufficient`
- no blocking decision remains
- deterministic structural preconditions pass
- write authorization exists
- source and dependency references are current
- every material intent ID is covered or explicitly deferred without loss
- the selected flow exists and validates today, and the packet uses only
  current keys with no inline evaluator definition
- the task has a definition of done and its `check:` rows are admitted
  ([Proof](proof.md#admit-a-check-before-you-trust-it))

## Final Output

<final-proposal>
## Proposal: {task_id}

Verdict: {ready|needs_review|blocked}
Outcome: {operator_visible_result}
When done: {observable_effect}
Source: {plan_ref_or_capture_ref}; fidelity {score}; slice covers {intent_ids}
Code and rules: {owner_paths}; {rules_index_refs}
First slice: {slice_id}; write scope {paths}
Proof: local {check}; integration {check_or_na}; field {check_or_na}
Launch: `lev entity task validate {task}`, then `lev sdlc exec {task} --flow {selected_flow}`; route `skill://exec`
Open decisions: {none_or_decisions}
Next: {run_exec|repair|interview}
</final-proposal>
