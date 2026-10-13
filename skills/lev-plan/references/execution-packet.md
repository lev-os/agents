# Execution Packet

Detail for `lev-plan` Emit mode: what `prove_requirements`, `emit_slice`, and
`validate_structure` need, plus the TDD rules a plan step or packet follows
when TDD is relevant. The workflow, readiness verdicts, proof selection, and
Write Gate live in [`../SKILL.md`](../SKILL.md); this file adds no step.

## Contents

- [Packet Location and Timing](#packet-location-and-timing): where the one packet goes and when it is written
- [Requirements Ledger](#requirements-ledger): the single `requirements:` list, its three passes, and row shape
- [Checks and False-Green Evidence](#checks-and-false-green-evidence): `check:` rules, fixtures, `invalid_proof`, red checks
- [Flow and Launch](#flow-and-launch): what the eval gate reads, where the flow is named, launch instructions
- [Emitted Task Shape](#emitted-task-shape): required fields of `dna.yaml` and `execution.yaml`, `lifecycle_stage` values
- [Emission Gate](#emission-gate): conditions that all hold before a packet is written
- [Final Output](#final-output): the `<final-proposal>` template
- [TDD Rules](#tdd-rules): test design, the RED-to-GREEN cycle, and batch topology

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

Everything the task must make true is one `requirements:` list in the task's
`dna.yaml` (`schema: lev.task.v2`): operator acceptance, slice exits,
constraints, forbidden moves and source claims are all rows of it. Write it in
three passes:

1. **Think.** For the slice, list what must be true when it is done and what
   must not be true (regressions, forbidden moves, false-green paths, a second
   path left behind). This list is scratch work; only its sentences land.
2. **Write.** Each item becomes one row whose `text` is a plain sentence; a
   negative idea is written into the sentence ("An invalid flow never exits 0").
3. **Prove.** For every row ask "how will we prove it?":
   - a command can show it: give the row a `check:`;
   - only reading the change can show it (one path, no swallowed error, tests
     cover both outcomes): leave `check:` off; the review agent answers it from
     the diff;
   - nothing can show it: sharpen the sentence until something can, or route
     the open question to `/interview`.

Row shape (`core/domain/src/task-requirements.ts`; the task reader is
`core/workstream/src/task-packet.ts`):

```yaml
schema: lev.task.v2
requirements:
  - id: invalid-flow-exits-nonzero    # unique across dna.yaml and evals/
    type: acceptance                   # acceptance | constraint | a claim type
    owner_slice: <slice id>            # set when the row is that slice's exit
    text: An invalid flow makes `lev flowmind validate <file>` exit non-zero.
    source_ref: <plan#section or path:line>   # when a plan or design states it
    risk: high                         # optional: high | medium | low
    invalid_proof: [<evidence that looks like proof and is not>]
    check:                             # omitted when the review agent answers
      command: lev                     # the program
      argv: [flowmind, validate, <known-bad file>]
      expectedExit: nonzero            # zero | nonzero | any
      timeoutMs: 120000
```

- At least one `type: acceptance` row has no `owner_slice`: the operator's
  acceptance. A slice exit is an acceptance row with `owner_slice`; a
  constraint or forbidden move is `type: constraint`.
- A claim type (`behavior_change`, `architecture_boundary`, `no_regression`,
  ...) is for a claim a plan or design states; its slice lists it in
  `claim_coverage` and `verifier_contract.proves_claims`, and
  `lev task validate` names any trace fields its type needs.
- When the list outgrows `dna.yaml`, move rows to `evals/<name>.yaml` in the
  task folder under the same `requirements:` key. That file holds overflow
  rows of the one ledger; it defines no evaluator.

## Checks and False-Green Evidence

- `check:` is a core/eval command case without `id` (the row id is the case
  id; `EvalCommandCase` in `core/eval/src/command-cases.ts`): `command` is the
  program and `argv` its arguments, plus optional `cwd` (inside the project),
  `timeoutMs`, `expectedExit` or `expectedExitCode`, `stdoutContains`,
  `stderrContains`. A shell line is rejected: a pipe or `&&` becomes separate
  rows. A search that must find nothing is `git grep` with
  `expectedExit: nonzero`.
- A check that needs a known input (a bad file, a sample) points at a fixture
  the packet writes in the task folder under `fixtures/`, named so repo-wide
  scans of that kind skip it (a flow fixture is `<name>.yaml`, never
  `<name>.flow.yaml`).
- Run every check once before emitting. A check for what the slice adds or
  fixes is red on today's tree; a check already green is a regression guard. A
  slice whose checks are all green today proves nothing new: add the red check
  or say why the review agent carries the change.
- Record each adversarial finding on the requirement row it threatens: the
  false-green path goes in `invalid_proof`, and the command that falsifies it
  is the row's `check:` (or the review agent answers the row).

## Flow and Launch

The packet does not select the flow; the launch does.

- **`topology` stays a slice classification** (for example
  `single_vertical_slice`). It never names a flow.
- **Selected current flow.** Choose it under
  [Proof and Evaluator Selection](../SKILL.md#proof-and-evaluator-selection).
  The current eval gate reads that flow's node packs and this task's
  `requirements:`, so the packet needs no flow or evaluator field.
- **Launch instructions.** State them in the final output with the flow passed
  explicitly: `lev task validate <task>`, then
  `lev sdlc exec <task> --flow <flow>`. Planning writes the instructions; Exec
  runs them.
- **Unresolved binding.** When no current flow fits, or recording the
  selection would need a packet key that does not exist, hold the slice
  instead of choosing a default or adding a key.

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
Launch: `lev task validate {task}`, then `lev sdlc exec {task} --flow {selected_flow}`; route `skill://exec`
Open decisions: {none_or_decisions}
Next: {run_exec|repair|interview}
</final-proposal>

## TDD Rules

TDD tests describe one logical behavior through the agreed public seam, using
domain vocabulary and independently derived expected values (spec examples,
known literals or a separate oracle). Avoid mirroring the implementation in the
assertion, private-method tests and side-channel checks that bypass the interface.
Prefer real internal collaborators; isolate external APIs, time/randomness and
necessary filesystem/database boundaries with existing adapters or test resources.
Use operation-specific boundary interfaces and injected dependencies where they
already fit; this is not permission to add abstractions solely for mocking.
Prefer an isolated test database when database behavior is the claim; otherwise
state what a boundary fake cannot establish. Each operation fake should expose
its expected response shape and exercised endpoint without conditional catch-all
setup, retaining the interface's type checks. Flag call-count/order assertions
and HOW-named tests when they merely couple to internals; observable protocol
ordering may itself be a legitimate contract. Check that behavior-preserving
internal refactoring would leave the test meaningful and green.
Treat every rule in this TDD section as active in every cycle: check it before
the first RED and again before selecting each next behavior. Work one behavior
through RED then GREEN before selecting another; GREEN adds only the current
cycle's production code needed to pass its test, with no anticipated tests or
features. A coherent Ralph unit may contain several sequential cycles. Keep
unrelated refactoring for review and an authorized follow-up; preserve the existing
frozen-test and isolation contract below.

Before forming a TDD packet, read the relevant `CONTEXT.md` when present and
applicable ADRs; record their refs and require test names plus public-interface
vocabulary to match them. Synthesize settled conversation decisions without
restarting an interview; expose only unresolved
choices that change scope or acceptance. Describe the user problem, intended
behavior, actors, exclusions and testing decisions without padding story counts.
Prefer the highest existing public test seam that actually observes the claim.
If none exists, propose a new seam at the highest viable public boundary; ask
only when that seam's tradeoff needs a user decision.

For ordinary TDD, plan and emit one coherent worker-owned batch: the behavioral
RED-to-GREEN cycle through the agreed public seam, its write scope, and its
verifier, followed by the declared checks and at most one integrated checkpoint
review covering spec drift and code quality. The same worker may write the
failing test and implementation; the controller confirms the failure is
behavioral and reruns the accepted check. Separate RED, GREEN, spec-review,
quality-review, or verifier agents are the isolated topology: use it only when
the user explicitly selects isolated TDD or a high-assurance execution contract
requires hidden holdouts or enforced role separation. Planning records that
exception; it does not dispatch agents.
