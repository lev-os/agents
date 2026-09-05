---
name: propose
description: Use when compiling aligned simple intent or a source-faithful Lev plan into a reviewable slice map or one execution-ready Lev task. It does not create or repair broad plans.
---

# /propose - Execution Packet Lane

`/propose` turns aligned intent into either a compact slice map or one vertical
execution slice. It does not implement, create a broad plan, or pre-create a
backlog of task folders.

## Command Modes

- `/propose` reviews alignment and recommends one vertical slice.
- `/propose map` and `/propose all slices` render a compact slice map only.
  They never create child task folders.
- `/propose emit <slice-id>` writes exactly one
  `.lev/pm/tasks/<task-id>/{dna.yaml,execution.yaml}` packet.
- Materialize a task just before it enters the ready set. Regenerate from the
  current source when a design, dependency, or boundary has changed.

Use `/lev-plan` for a human runbook and `/interview` for unresolved product or
architecture decisions. A map does not dispatch by itself, but every approved
map must identify at least one executable slice.

## Entity Reconciliation

After authorized material progress, reconcile touched and causally affected
artifacts before routing, handoff, or final response. Track entity ref,
island/provider locator (a path for file storage), basis/evidence, and the
reason/action due. Update through the verified owning CLI/adapter; use a
write-authorized skill fallback only when that operation is unavailable.
Record updated, no_change(reason), or blocked(reason), preserving unresolved
refs. Reading or mentioning a path alone creates no update obligation.
Read-only work reports pending changes only. Reminders grant no write authority;
task status stays with the bound tracker. Update only artifacts whose content
or evidence changed; do not rewrite every referenced document.

## Work Link

Lifecycle lane: Execution preparation
Entity movement: `captured | designed | planned | aligned -> proposed | execution_ready | needs_interview | needs_plan`
Workstream: resolve the active workstream before writing task artifacts
Upstream: `/capture`, `/interview`, `/lev-plan`, `.lev/pm/designs/*`, `.lev/pm/plans/*`, aligned simple-slice intent
Downstream: `/exec`, `/capture`, `/lev-plan`, `/interview`
Router: `/work`

## Transition Packet

Freeze the aligned intent before broad lookup. Keep this packet internal by
default; render it only for `--full` or when a missing field explains a
`needs_review` verdict. If one operator outcome, its boundaries, and a relevant
verifier cannot be named, route to `/interview`.

<transition-packet>
## Proposal Transition: {proposal_id}

Intent: {one_sentence_intent}
Source: {chat|capture|design|task}; refs {known_refs_or_none}
Plan: {plan_ref_or_not_required}; source fidelity {score_or_unknown}; lost rows {count_or_unknown}
Acceptance: {known_acceptance_or_gap}
Constraints: {write_scope_boundaries_forbidden_moves}
Open decisions: {none_or_blocking_decisions}
Recommended slice: {one_vertical_slice_or_gap}
Proof: {relevant_verifier_or_gap}
Mode: {review|map|emit}
</transition-packet>

## Expectation And Proof Check

Where relevant, establish the product outcome, owning code areas, applicable
rules/index refs, real-world critical path, observable done state, and smallest
local/integration/field proof. Identify code areas first, then use the nearest
project rules index to load only the standards that govern those areas. If an
item is unknown, expose the gap; if it is irrelevant, say why.

For broad, multi-slice, migration, architecture, security, or cross-authority work,
require a `/lev-plan` source before slicing. A capture or design may go directly
to proposal only when one bounded vertical outcome is already clear. `propose`
must not silently become the broad-plan author.

## Shared Planning and TDD Contract

### Overlay and iteration planning

This packet lane simulates the SDLC overlay, not a mandatory gate for all Lev
work. Non-coding work with a sufficient plan, scope, acceptance and authority
can route to its domain skill or `skill://exec` without emitting this packet.
Coding with unresolved architecture goes to `skill://arch`; broad planning gaps
return to `skill://lev-plan`.

Prepare each selected unit for the future loop prompt: "Do the next bit of work
on this effort. Select ONE ready coherent unit, finish that single thing, record
the result and remaining frontier, then stop." A unit may be a substantial
vertical chunk, not the full effort. Preserve plan claim references and map them
to checks in `claim_verifier_map`; keep dependencies, scope and stop conditions
explicit. The outer Ralph loop reloads state between units; `lev-ralph` adds the
worker/reviewer-fixer cycle inside one unit. Runtime adoption and dedicated
`claim.yaml` are deferred; preparing a packet does not dispatch or prove Ralph.

### Shared substance and conditional TDD

Resolve or fetch every explicitly supplied local path, issue number, tracker URL,
or external URL through its owning source, then read the full artifact/body and
all accessible comments. Report inaccessible material instead of reconstructing
it. Preserve settled decisions about changed modules/interfaces, developer
clarifications, architecture, schemas, API contracts and interactions when
applicable. Additional notes belong only when they change execution or explain
a constraint; do not fill irrelevant headings.

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
Treat every rule in this TDD subsection as active in every cycle: check it before
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

Reference current owner paths for executable handoff, with freshness context;
source advice to omit all paths is superseded by Lev's evidence-backed ownership.
When a prototype's state machine, reducer, schema or type shape expresses a
decision more precisely than prose, retain only that decision-rich snippet and
its prototype provenance, not the whole demo.

When uncertainty needs a prototype, route the question to `skill://poc`. Preserve
only its explicit question, selected logic/UI branch, stated assumptions, validated
answer, and provenance in the proposal; prototype construction details remain
owned by `skill://poc`.

For wide mechanical changes that cannot land as independent vertical slices,
expand alongside the old form, migrate bounded caller batches while preserving
compatibility, then contract only after every migration dependency is satisfied
and no old caller remains. If batches cannot stay green independently, explicitly
plan a shared integration boundary and final integrate-and-verify gate; do not
promise per-batch green. Branch creation still requires the task's authority.
Prefactoring is justified only by a concrete dependency, with its own scope/check.

Present slice name, genuine blockers and delivered behavior when reviewing the
breakdown. Ask about granularity or merging/splitting only when unresolved; prior
approval need not be repeated. A source parent remains unchanged unless that
mutation is authorized. A map is not task emission or tracker publication.

Plan and proposal share problem/behavior, domain vocabulary, decisions, constraints,
acceptance examples, test seams, delivery slices, dependencies, evidence and
authority. The plan projects the broad runbook; proposal projects a selected
slice for review or execution. Preserve source IDs and decisions across both.
Use tracer bullets for independently demonstrable end-to-end behavior and
expand–migrate–contract for wide compatibility changes. Reuse existing public
test seams; prefactoring needs a concrete scoped reason.

When this lane needs an SDLC spec projection, load and render the canonical
`../work/templates/spec.md`, which `skill://propose` owns. Do not fork the source
skill's inline template or invent another spec format.

For ordinary TDD, emit one coherent worker batch containing the behavioral
RED-to-GREEN cycle, its write scope, and its verifier. The controller reruns the
check, then one checkpoint reviewer may cover spec drift and code quality on the
completed batch. Do not create separate RED, GREEN, spec-review, and quality-review
agents by default. Use that isolated topology only when the user explicitly asks
for it or a high-assurance contract requires hidden holdouts or enforced role
separation.

## Semantic Readiness

The LLM judges semantic readiness from current intent, source artifacts, code,
and verifier evidence. Deterministic validation supplies facts and hard
preconditions; it does not determine proposal quality.

Score each dimension `insufficient`, `sufficient`, or `strong`:

1. intent fidelity, including source-fidelity coverage from capture through plan to slices
2. operator outcome and demonstrability
3. scope and boundary clarity
4. verticality
5. dependency quality
6. verifier relevance
7. cold-start context sufficiency
8. implementation simplicity
9. freshness risk

Use the weakest dimension for the verdict:

- `ready`: every dimension is at least sufficient and no blocking decision is open.
- `needs_review`: a dimension is insufficient but a focused revision can repair it.
- `blocked`: execution depends on an unresolved product, architecture, or authority decision.

Classify alleged blockers before issuing the verdict:

- `code_blocker`: required executable, API, schema, or owner contract is unavailable
- `decision_blocker`: unresolved product, architecture, or authority choice
- `promotion_gate`: proof required for cutover, merge, release, or certification
- `administrative_hold`: queue or assignment state

Only the first two may make a slice `blocked`. Missing tests and harnesses are
slice work. Missing receipts require checking the live dependency; receipts are
post-execution outputs. Promotion gates and administrative holds must be shown
separately from implementation readiness.

Do not average weak dimensions into a passing score. Rejudge after every task
rewrite. A green schema check, `lev task validate`, or existing verifier is not
semantic approval.

Intent fidelity is sufficient only when every material source intent ID is
covered by a slice, preserved as a plan-level constraint/non-goal, or explicitly
deferred with owner approval. A high average cannot hide one lost material row.

## Code, LLM, And Human Authority

- Deterministic code owns schema validation, reference existence, graph cycles,
  path policy, write-scope enforcement, and reproducible command results.
- The LLM owns intent interpretation, slice verticality, semantic readiness,
  verifier relevance, unnecessary complexity, and stale-context judgment.
- A human owns unresolved product tradeoffs and explicit approval where policy
  requires it.

## Adversarial Review

Use premortem, reverse brainstorming, falsification, Pentagon, LFD, or UltraQA
as reasoning tools when risk warrants them. Keep that reasoning transient.
Persist only task-specific information that changes execution: a unique failure
mode, the claim it threatens, and the verifier that can falsify it.

A review finding becomes a separate slice only when it has a distinct operator
outcome, owner, independently verifiable boundary, and reversible delivery unit.
Otherwise repair the existing slice's constraint, acceptance, dependency, or
verifier mapping. Review cycles do not authorize additional task emission.

Use this compact mapping:

```yaml
claim_verifier_map:
  - claim_ref: <acceptance or design claim>
    failure_mode: <credible false-green path>
    verifier_ref: <command, test, or proof profile>
```

Reference shared runtime, standards, evidence, and proof profiles. When the
repository has DNA standards or boundary laws, load the applicable files before
judging readiness and persist only their refs. Do not copy their generic receipt
fields, test taxonomies, or review checklists into every task.

## Capture Intake

When the proposal comes from `/capture` or `/dump`, preserve the source ledger
identity and artifact reference. Do not duplicate session notes or the full
capture row into task canon. If the source lacks compiled intent, return it to
`/capture`. If non-trivial source rows lack the visible/durable fidelity
components and loss notes, return them to `/capture` before judging readiness.

## Plan Intake

When a source plan exists:

- Load its source-fidelity table, current/target boundary, decisions, dependency
  DAG, first slice, open decisions, and freshness state.
- Preserve the plan ref and covered `intent_id` values in every slice record.
- Treat the plan as the broad runbook; maps and task packets select execution
  units without rewriting or shrinking it.
- If broad work lacks fidelity coverage, current/target evidence, or a coherent
  slice DAG, return it to `/lev-plan` rather than reconstructing it here.
- If auto-enrich revised the plan, require its final digest/fidelity state rather
  than an older snapshot.

## Write Gate

Render review output by default. Write task artifacts only after explicit
`emit`, `apply`, `edit`, or `patch` authorization, or an approved capture row
routed to `/propose`. `all slices` is map authorization, not task-emission
authorization.

## Protocol

```yaml
steps:
  - id: freeze_intent
    action: Build the transition packet before broad lookup or writes; expose it only for --full or a repairable alignment gap.
    failure: Route missing product or architecture framing to /interview.

  - id: load_context
    action: Identify the owning code areas, then read only current source capture/design/plan, workstream, existing task, verifier evidence, and the applicable entries from the project's rules index.
    failure: Mark stale or missing authority as an open decision.

  - id: verify_source_fidelity
    action: For plan-backed work, map every material intent_id to a plan-level constraint or proposed slice and reject lost rows. For direct simple-slice work, record why a plan is not required.
    validation: Source fidelity is current, no material row is lost, and every slice names covered intent IDs.
    failure: Route missing capture fidelity to /capture and shallow broad plans to /lev-plan.

  - id: select_mode
    action: Select review, map, or single-slice emit from the command.
    failure: Default to review without writing.

  - id: judge_readiness
    action: Score the nine semantic dimensions, classify blockers, and issue ready, needs_review, or blocked.
    failure: If no slice is runnable, simplify the DAG; block only on a concrete code or decision blocker.

  - id: map_slices
    when: mode == map
    action: Render compact slice records without creating task folders.
    validation: Every record has an outcome, owner, dependencies, proof, status, and open decisions; at least one approved-map slice is runnable.

  - id: emit_slice
    when: mode == emit and semantic_readiness == ready
    action: Write one lean task packet for the selected vertical slice.
    validation: Exactly one task folder is created or updated.

  - id: validate_structure
    when: mode == emit
    action: Run `lev task validate <task-id|task-path>` and report deterministic failures separately.
    failure: Keep the task proposed; do not offer /exec.

  - id: compare_source
    action: Recompare intent, boundaries, acceptance, verifier, dependencies, and freshness with the source.
    failure: Repair and rejudge before offering /exec.
```

## Slice Map Shape

```yaml
slices:
  - id: <stable-domain-name>
    operator_outcome: <observable result>
    owner: <package or plugin>
    depends_on: []
    covers_intent_ids: []
    proof: <verifier or proof profile>
    status: <ready|needs_review|blocked>
    open_decisions: []
```

The map may show every slice. It must not contain copied task packets, generic
proof boilerplate, or claims that all slices are execution-ready.

## Emitted Task Shape

```yaml
dna_yaml.required:
  [ontology, intent, entity_kind, lifecycle_target, acceptance, local_refs, local_constraints, source_context]

source_context.required:
  [capture_refs, plan_ref_or_not_required, plan_digest_or_na, covered_intent_ids, source_fidelity]

execution_yaml.required:
  [topology, runtime_profile_ref, dependencies, structural_preconditions, slices]

slice.required:
  [id, operator_outcome, claim_verifier_map, what_to_build, acceptance_criteria, write_scope, forbidden_moves]

shared_contract_refs:
  [standards_ref, execution_evidence_profile_ref, proof_profile_ref]
```

Add fields only when this slice needs them. A fresh executor must be able to
resolve references and act without reading the originating chat.

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

## Output Templates

Render the Markdown inside live templates; do not print the XML wrapper tags.

<proposal-review>
## Proposal: {proposal_id}

Verdict: {ready|needs_review|blocked}
Outcome: {operator_visible_result}
When done: {observable_effect}
Source: {plan_or_capture_ref}; fidelity {score}; covered intent {count}/{total}
Code and rules: {owner_paths}; {rules_index_refs}
First testable slice: {slice_id} - {behavior}
Proof: local {check}; integration {check_or_na}; field {check_or_na}
Weakest point: {dimension}: {reason}
Open decisions: {none_or_decisions}
Next: {emit_slice|repair_question|interview}
</proposal-review>

<slice-map>
## Slice Map: {proposal_id}

Source state: {current|stale|in_flux}
Source plan: {plan_ref_or_not_required}; fidelity {score}; coverage {covered}/{total}
Critical path: {slice_ids}
Slices: {compact_slice_records}
Promotion gates: {slice_ids_and_reason}
Administrative holds: {slice_ids_and_reason}
Next slice: {one_slice_id_or_design_decision}
</slice-map>

<final-proposal>
## Proposal: {task_id}

Verdict: {ready|needs_review|blocked}
Outcome: {operator_visible_result}
When done: {observable_effect}
Source: {plan_ref_or_capture_ref}; fidelity {score}; slice covers {intent_ids}
Code and rules: {owner_paths}; {rules_index_refs}
First slice: {slice_id}; write scope {paths}
Proof: local {check}; integration {check_or_na}; field {check_or_na}
Open decisions: {none_or_decisions}
Next: {run_exec|repair|interview}
</final-proposal>

## Next-Step Mini-Router

When a choice is useful, render only eligible items as a numbered table with
`#`, `Route`, `Expected result`. Clear authorized transitions proceed directly.

| Result | Route | Expected result |
|---|---|---|
| Ready authorized SDLC packet | `skill://exec` | Execute the selected unit |
| Broad plan stale / incomplete | `skill://lev-plan` | Repair the source plan |
| Human or architecture decision missing | `skill://interview` or `skill://arch` | Resolve the decision before emission |
| Non-coding packet unnecessary | `skill://exec` or domain skill | Use the sufficient source plan directly |
| Deferred / paused | `skill://handoff` | Preserve packet state and resumption condition |

## Proposal Red Flags

- "All slices means emit all tasks."
- "A generated backlog is a roadmap."
- "Task validation passed, so semantic quality is proven."
- "More proof metadata makes the task more ready."
- "The executor can choose the product or architecture decision."
- "A task generated from an older design is still current."
- "Verifier exists, so the behavior is proven."
- "Session notes belong in task canon."
- "The proposal exists, so implementation can start."
- "The broad plan is optional; the slice map can recover it from chat."
- "A 95% fidelity average is fine even though one material constraint disappeared."
- "Propose can deepen a shallow migration plan while emitting the first task."
- "The harness or receipt is missing, so implementation is blocked."
- "Every slice is held, but the map is still approved."
