---
name: lev-plan
description: Use when compiling captured or designed intent into a Lev plan (human runbook, migration, architecture plan, multi-slice roadmap), deepening or reviewing a plan, changing plan state under `.lev/pm/plans/`, reviewing slice readiness, rendering a slice map, or emitting one execution-ready Lev task.
---

# /lev-plan - Plan, Slice Map, and Execution Packet

`lev-plan` is one workflow from aligned intent to the next executable unit. A
run moves through these stages in order and stops at the one the request asked
for:

1. **Alignment handoff**: bind the source and freeze the intent with its
   fidelity.
2. **Broad plan, when the work needs one**: compile, deepen, or review the
   human runbook under `.lev/pm/plans/` and manage its FSM.
3. **Review or map**: judge readiness and render a compact slice map.
4. **One execution packet**: write a single just-in-time task packet for a
   selected slice.

A plan preserves the source fidelity table, explains current and target state,
resolves architecture and ownership, builds a dependency/slice map, and records
human-readable execution and rollback. It is not merely a frontmatter
generator: a schema-valid shallow plan is still a failed plan. The workflow
does not implement, dispatch, or pre-create a backlog of task folders.

For multi-stage or multi-session planning, long autonomous work, or a request
to use Horizon, read [long-horizon planning](references/long-horizon.md) before
framing the outcome or judging readiness. It loads Horizon as a method reference
inside this workflow; the caller does not need a separate `/horizon` invocation.
A planning-only request stops at its selected mode. When the user also authorizes
delivery, pass the same plan and next ready slice to `skill://orch`, which runs
the referenced execution loop through the existing owners.

Plans, maps, reviews, and specs are Markdown for humans. The task packet keeps
its established YAML payloads, and runtime state stays in the JSON its runtime
owns.

For any non-trivial direct or routed invocation, load [Project Context](../lev/references/project-context.md) before project-specific lookup. It resolves the active project and its declared breadcrumbs.

`skill://lev-plan` loads this contract. Plans, workstreams, and emitted tasks
use durable `lev://entity/work/plan/<plan-id>`,
`lev://entity/work/workstream/<workstream-id>`, and
`lev://entity/work/task/<task-id>` identities; later execution is addressed
separately as `lev://exec/<flow>`. Load `skill://lev` before introducing
another URI family.

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

Lifecycle lane: Plan
Entity movement: `captured | designed | draft_plan -> planned | needs_interview | needs_review`, then `planned | aligned -> proposed | execution_ready | needs_interview | needs_plan`
Workstream: resolve the active workstream before plan writes, and the workstream that owns the slice (the `ws` skill) before task writes; the task folder goes under it
Upstream: `/capture`, `/interview`, `/prior-art`, `.lev/pm/designs/*`, existing plan under `.lev/pm/plans/*`, aligned simple-slice intent
Downstream: `/auto-enrich`, `/exec` for a ready SDLC packet, `/exec` or domain skill for non-coding, `/interview`, `/capture`, `/lev`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Modes

| Mode | Trigger | Result |
|---|---|---|
| Compile | Captured/design intent or explicit `create` | One new plan, or update the existing matching plan |
| Deepen | `deepen <plan>` or an existing shallow plan | Patch the named plan in place; never create a parallel version |
| Review | `review <plan>`, “is this plan ready?”, or a slice or aligned bounded intent with no other mode | Fidelity/readiness verdict; a slice review recommends one vertical slice; no write unless authorized |
| Lifecycle | list/show/transition/validate | FSM operation only |
| Map | `map` or `all slices` | Compact slice map only; never creates task folders |
| Emit | `emit <slice-id>` | Exactly one `{dna.yaml,execution.yaml}` task packet |

The `propose` alias forwards `/propose` to Review, `/propose map` and
`/propose all slices` to Map, and `/propose emit <slice-id>` to Emit, with
arguments, flags, and authorization unchanged. This skill answers the caller
directly and never routes back to `propose`.

Default to review without writing when the user asks what the plan should
contain, requests an audit, or has not authorized a durable edit.

## Which Stage

Classify the domain and the scope before applying software-delivery mechanics.
Map and Emit simulate the SDLC overlay; they are not a mandatory gate for all
Lev work.

- **Broad work plans first.** Broad, multi-slice, migration, architecture,
  security, or cross-authority work needs a plan source before any slice is
  mapped or emitted. A Map or Emit request never authors or deepens that plan
  as a side effect: leave the entity at `needs_plan`, name Compile or Deepen as
  the next step, and continue into it only when the request and its
  authorization cover plan writes.
- **A bounded slice goes direct.** A capture or design goes straight to Review,
  Map, or Emit only when one bounded vertical outcome is already clear. Record
  `plan_not_required` with a one-sentence rationale in the transition packet
  and, on Emit, in the packet's existing `source_context` plan field.
- **Non-coding work skips the packet.** With a sufficient plan, scope,
  acceptance, and authority it routes to its domain skill or `skill://exec`;
  Map and Emit apply only to coding or an overlay that requires a packet.
- **Open decisions leave first.** Coding with unresolved architecture goes to
  `skill://arch`; an unresolved product or architecture decision goes to
  `/interview`.

## Workflow

```yaml
steps:
  - id: bind_source
    action: Resolve workstream, capture/design/plan refs, existing matching plan or task, source digests, and allowed write scope; freeze the aligned intent as the transition packet before broad lookup or writes.
    validation: "Every material intent has an intent_id and source_ref; an existing plan or task is reused when present; one operator outcome, its boundaries, and a relevant verifier can be named."
    on_failure: "Route conversation-only work to /capture; unresolved product or architecture framing to /interview."

  - id: select_mode
    action: Apply Which Stage, then select compile, deepen, review, lifecycle, map, or emit from the command. A lifecycle request performs only its FSM operation and then route_forward.
    validation: "Exactly one mode is selected; broad work has a plan source before map or emit; a direct bounded slice records plan_not_required with its rationale."
    on_failure: "Default to review without writing."

  - id: rehydrate_fidelity
    action: Load the capture source-fidelity table and map every material row to a plan section, decision, deferment, or explicit conflict. For map and emit, map every material intent_id to a plan-level constraint or proposed slice and reject lost rows.
    validation: "Source fidelity is current; no material row is lost; plan fidelity is >= 0.90 and not lower than capture fidelity; every slice names covered intent IDs."
    on_failure: "Route missing capture fidelity to /capture or ask one decision question; a shallow broad plan is needs_plan. Do not draft around missing intent."

  - id: inspect_current_state
    action: Identify the owning code areas, then inspect only what this run needs - current code, docs, plans, dependencies, dirty work, external authority, the source capture/design/plan, workstream, existing task, verifier evidence, and the applicable entries from the project's rules index.
    validation: "Current-state claims are observed or labeled stale/assumed; load-bearing claims cite exact refs."
    on_failure: "Route to /prior-art or keep the claim unknown; mark stale or missing authority as an open decision."

  - id: choose_depth
    when: mode is compile or deepen
    action: Select light, standard, or deep from risk and topology; state the selection in the plan.
    validation: "Depth matches the real blast radius and does not use length as a proxy for rigor."

  - id: frame_outcome
    when: mode is compile or deepen
    action: Define operator outcome, observable done state, scope, non-goals, authority boundaries, and human decisions.
    validation: "A teammate can tell what changes, what stays unchanged, and what done looks like."

  - id: analyze_options
    when: mode is compile or deepen
    action: For standard/deep plans, compare at least two meaningful approaches or record evidence that alternatives are invalid.
    validation: "Decision drivers, tradeoffs, sacrificed attributes, and chosen approach are explicit; newly derived behavior is labeled proposed or left as an open decision, never promoted into settled source intent."

  - id: build_topology
    when: mode is compile or deepen
    action: Build current-to-target map, ownership boundaries, dependencies, slices, critical path, promotion gates, and administrative holds.
    validation: "Every slice has an outcome, owner, depends_on, proof, status, open decisions, and covered intent_ids; each promotion verifier is satisfiable by that slice plus completed dependencies; a slice with incomplete or blocked dependencies is blocked, not ready or merely promotion-gated."

  - id: design_proof
    when: mode is compile or deepen
    action: Map each acceptance claim to the smallest relevant local, integration, field, or external-owner verifier, chosen under Proof and Evaluator Selection.
    validation: "At least 90% of acceptance criteria are concrete/testable; each verifier is attached to the first slice whose scope can satisfy it; every claimed preserved boundary or compatibility form is exercised directly; missing future tests are slice work, not false blockers."

  - id: design_failure_and_rollback
    when: mode is compile or deepen
    action: Record credible failure mechanisms, prevention/detection, residual risk, rollback, and architecture review triggers.
    validation: "High-risk/deep plans include a three-scenario pre-mortem and unit/integration/e2e/observability test shape where applicable; rollback returns to the latest dependency-compatible state and cannot remove compatibility still required by incomplete slices."

  - id: write_or_patch
    when: mode is compile or deepen
    action: Write one plan under .lev/pm/plans/ only inside authorized scope, preserving unrelated plan history and current dirty work.
    validation: "Exactly one plan is created or updated; source refs and fidelity table are durable."

  - id: judge_readiness
    action: Run deterministic structure/ref checks, then the semantic weak-link review - score the readiness dimensions, classify blockers, and issue the verdict. Use /auto-enrich for explicit or deep/high-risk plan hardening when available.
    validation: "No readiness dimension is insufficient; deterministic success is reported separately from semantic approval."
    on_failure: "If no slice is runnable, simplify the DAG; block only on a concrete code or decision blocker."

  - id: map_slices
    when: mode is map
    action: Render compact slice records without creating task folders.
    validation: "Every record has an outcome, owner, dependencies, proof, status, and open decisions; at least one approved-map slice is runnable."

  - id: prove_requirements
    when: mode is emit and semantic readiness is ready
    action: Read references/execution-packet.md, write the slice's requirements list with its three passes (think, write, prove), then run every check once on today's tree.
    validation: "Every row is a prompt (often one sentence, never forced) that a check or the review agent can answer; at least one check is red today when the slice adds or fixes behaviour."
    on_failure: "Sharpen a row nothing can prove, or route its open question to /interview."

  - id: emit_slice
    when: mode is emit and semantic readiness is ready
    action: Write one lean task packet for the selected vertical slice, using only current packet keys.
    validation: "Exactly one task folder is created or updated, and every Emission Gate condition holds."

  - id: validate_structure
    when: mode is emit
    action: Run `lev task validate <task-id|task-path> --json`; it validates every `check:` through core/eval. Report deterministic failures separately.
    on_failure: "Keep the task proposed; do not offer /exec."

  - id: compare_source
    action: Recompare intent, boundaries, requirements and their proof, dependencies, and freshness with the source.
    on_failure: "Repair and rejudge before offering the next route."

  - id: route_forward
    action: Name the next stage or route - an approved SDLC plan to map or slice review, a ready slice to emit, a validated packet to /exec, a sufficient non-coding plan to the domain skill or /exec. Outside emit this workflow writes no task folder, and it never dispatches execution.
    validation: "The first executable slice is named and the broad plan, when one exists, remains its source."
```

In Emit mode, read [Execution Packet](references/execution-packet.md) before
`prove_requirements`; also read it to review or repair an existing task packet.
It carries the requirements ledger, check rules, flow and launch detail, the
emitted task shape, and the Emission Gate.

## Alignment Handoff

Freeze the aligned intent before broad lookup. Keep this packet internal by
default; render it only for `--full` or when a missing field explains a
`needs_review` verdict. If one operator outcome, its boundaries, and a relevant
verifier cannot be named, route to `/interview`.

<transition-packet>
## Transition: {plan_slug_or_proposal_id}

Intent: {one_sentence_intent}
Source: {chat|capture|design|task}; refs {known_refs_or_none}
Plan: {plan_ref | plan_not_required: one_sentence_rationale}; source fidelity {score_or_unknown}; lost rows {count_or_unknown}
Requirements: {known_requirements_or_gap}
Constraints: {write_scope_boundaries_forbidden_moves}
Open decisions: {none_or_blocking_decisions}
Recommended slice: {one_vertical_slice_or_gap}
Proof: {relevant_verifier_or_gap}
Mode: {compile|deepen|review|lifecycle|map|emit}
</transition-packet>

Where relevant, establish the product outcome, owning code areas, applicable
rules/index refs, real-world critical path, observable done state, and smallest
local/integration/field proof. Identify code areas first, then use the nearest
project rules index to load only the standards that govern those areas. If an
item is unknown, expose the gap; if it is irrelevant, say why.

Intake by source:

- **Capture or dump.** Preserve the source ledger identity and artifact
  reference. Do not duplicate session notes or the full capture row into plan
  or task canon. If the source lacks compiled intent, return it to `/capture`.
  If non-trivial source rows lack the visible/durable fidelity components and
  loss notes, return them to `/capture` before judging readiness.
- **Design.** A design's `Design-to-Propose Handoff` section is the handoff
  for a bounded slice; its suggested profile and validation chain are inputs
  to verify, not settled choices.
- **Plan.** Load its source-fidelity table, current/target boundary, decisions,
  dependency DAG, first slice, open decisions, and freshness state. Preserve
  the plan ref and covered `intent_id` values in every slice record. The plan
  stays the broad runbook; maps and task packets select execution units without
  rewriting or shrinking it. A plan that lacks fidelity coverage,
  current/target evidence, or a coherent slice DAG is `needs_plan`: repair it
  in Deepen rather than reconstructing it in a map. If auto-enrich revised the
  plan, require its final digest/fidelity state rather than an older snapshot.

## Source Fidelity Gate

Reuse the five capture components:

```
fidelity = 0.30*detail_preservation
         + 0.25*relationship_preservation
         + 0.20*source_attribution
         + 0.15*neighbor_context
         + 0.10*actionability
```

The plan must contain this table for every material capture/design row:

| Intent ID | Source requirement | Plan destination | Preservation | Fidelity | Note / approval |
|---|---|---|---|---:|---|
| `INT-*` | Goal, constraint, non-goal, decision boundary, acceptance, or relationship | Section/slice/decision/deferment | `preserved`, `narrowed-approved`, `deferred-explicit`, `conflict`, `lost` | 0.00-1.00 | What changed and who approved it |

Rules:

- `lost` blocks planning, mapping, and emission.
- `narrowed-approved` requires an explicit source/user decision.
- Every material relationship and non-goal gets its own coverage, not just goals.
- Overall fidelity must be at least 0.90 and must not be lower than the source capture.
- An average cannot hide one missing material row.
- For a map or packet, every material source intent ID is covered by a slice,
  preserved as a plan-level constraint/non-goal, or explicitly deferred with
  owner approval.

## Plan Depth

| Depth | Use when | Required shape |
|---|---|---|
| `light` | One obvious bounded change | Goal, scope, steps, proof; suggest skipping the plan if execution is clearer |
| `standard` | One feature or coherent multi-step change | Source fidelity, current/target, boundaries, steps, risks, verification |
| `deep` | Migration, architecture, security, destructive work, 3+ authorities, or multi-slice roadmap | Full contract below, options/tradeoffs, DAG, pre-mortem, rollback, review |

Do not inflate a light plan. Do not compress deep work into a list of activities.

## Plan Contract

Every standard/deep plan includes, adapting headings to the domain:

1. Source context and fidelity table.
2. Outcome and observable done condition.
3. Current state with evidence and freshness.
4. Target state and current-to-target map.
5. Scope, non-goals, authority, and forbidden moves.
6. Decision drivers, options, tradeoffs, and rejected alternatives.
7. Ownership/container/component boundaries where architecture matters.
8. Dependency and slice DAG with critical path.
9. Per-slice outcome, proof, status, covered intent IDs, and open decisions.
10. Acceptance/claim-to-verifier map.
11. Risks, pre-mortem where required, mitigation, detection, and residual risk.
12. Rollback and architecture review triggers.
13. First executable slice and next lifecycle route.

Deep evidence targets, borrowed from demonstrated planning practice:

- At least 80% of load-bearing current-state claims cite exact files, lines, commands,
  or external authority refs.
- At least 90% of acceptance criteria are observable/testable.
- A plan is not complete merely because required headings exist.

## Shared Planning and TDD Contract

The plan and the packet share problem/behavior, domain vocabulary, decisions,
constraints, acceptance examples, test seams, delivery slices, dependencies,
evidence and authority. The plan projects the broad runbook; a map or packet
projects a selected slice for review or execution. Preserve source IDs and
decisions across both. Use tracer bullets for independently demonstrable
end-to-end behavior and expand–migrate–contract for wide compatibility changes.
Reuse existing public test seams; prefactoring needs a concrete scoped reason.

### Iteration planning

Prepare long-running efforts for one coherent unit per future Ralph iteration:
name the next ready chunk, its acceptance/claim checks, dependencies, permitted
effects and stopping condition. Prompt: "Do the next bit of work on this effort;
select ONE ready coherent unit, finish that single thing, record the result and
remaining frontier, then stop." One thing may be a substantial vertical chunk,
not the full effort. The outer loop reloads state and chooses whether to
continue; `lev-ralph` adds a worker/reviewer-fixer cycle within that unit.
Runtime adoption is deferred: creating a plan or preparing a packet does not
run the loop, dispatch, or prove Ralph.

Use existing plan `steps[].validation` / acceptance criteria and task
`claim_verifier_map` as claim sources. Carry each plan claim into a packet as a
requirement row with its `source_ref` and its proof, preserving stable claim
references; keep dependencies, scope and stop conditions explicit. Dedicated
`claim.yaml` and direct runtime ingestion of plan claims are future work, not
newly supported schema or CLI behavior.

### Shared substance

Resolve or fetch every explicitly supplied local path, issue number, tracker URL,
or external URL through its owning source, then read the full artifact/body and
all accessible comments. Report inaccessible material instead of reconstructing
it. Preserve settled decisions about changed modules/interfaces, developer
clarifications, architecture, schemas, API contracts and interactions when
applicable. Additional notes belong only when they change execution or explain
a constraint; do not fill irrelevant headings.

Reference current owner paths for executable handoff, with freshness context;
source advice to omit all paths is superseded by Lev's evidence-backed ownership.
When a prototype's state machine, reducer, schema or type shape expresses a
decision more precisely than prose, retain only that decision-rich snippet and
its prototype provenance, not the whole demo.

When uncertainty needs a prototype, route the question to `skill://poc`. Preserve
only its explicit question, selected logic/UI branch, stated assumptions, validated
answer, and provenance in the plan or packet; prototype construction details
remain owned by `skill://poc`.

For wide mechanical changes that cannot land as independent vertical slices,
expand alongside the old form, migrate bounded caller batches while preserving
compatibility, then contract only after every migration dependency is satisfied
and no old caller remains. If batches cannot stay green independently, explicitly
plan a shared integration boundary and final integrate-and-verify gate; do not
promise per-batch green. Branch creation still requires the task's authority.
A behavior-changing slice at a shared seam must preserve the old caller contract
immediately or remain unexposed until compatibility proof passes; never put an
incompatible baseline before a blocked or unavailable expansion slice.
Prefactoring is justified only by a concrete dependency, with its own scope/check.

Present slice name, genuine blockers and delivered behavior when reviewing the
breakdown. Ask about granularity or merging/splitting only when unresolved; prior
approval need not be repeated. A source parent remains unchanged unless that
mutation is authorized. A map is not task emission or tracker publication.

When a selected slice needs an SDLC spec projection, load and render the
canonical [`../work/templates/spec.md`](../work/templates/spec.md), which this
skill owns as a lane. Do not fork the template inline or invent another spec
format. A spec cites requirement rows by id; the rows stay in the task's
`dna.yaml`.

### Conditional TDD

When TDD is relevant to a plan step or a packet, read
[TDD rules](references/execution-packet.md#tdd-rules) before designing its
proof. They cover test design, the RED-to-GREEN cycle, the single worker
batch, and the isolated-TDD exception.

## Proof and Evaluator Selection

Planning chooses the proof before anything runs, from contracts that exist
today.

- **Current contracts only.** The current eval gate reads two inputs: the node
  packs of the selected FlowMind flow and the task's `requirements:`. Choosing
  evaluators is therefore choosing the flow: resolve it from the project's
  current FlowMind contracts (flow files that exist and validate today). A
  flow or evaluator recalled from memory, a filename, or an older plan is
  unverified until live help and the current files confirm it.
- **Record the selection for humans.** Name the selected flow and the proof it
  supplies in the plan's proof section, in the `Proof:` and `Launch:` lines of
  the output, and in existing source refs such as a row's `source_ref`. The
  task packet keeps its current keys and carries its own proof only as
  requirement rows and their `check:`.
- **Hold, never drop.** Hold the slice that carries the claim when a source
  brings an `eval_packs` key or an inline evaluator definition, when no current
  contract declares the evaluator a claim needs, or when binding the selection
  would need a packet key that does not exist. A contract hold is a
  `code_blocker` naming the missing owner contract; an interview hold is a
  `decision_blocker` routed to `/interview` when choosing the proof is a human
  decision. A claim weakened to a check that happens to exist is a lost row.
- **Shared profiles by ref.** Reference shared runtime, standards, evidence,
  and proof profiles through their existing individual refs. When the
  repository has DNA standards or boundary laws, load the applicable files
  before judging readiness and persist only their refs. Do not copy their
  generic receipt fields, test taxonomies, or review checklists into every
  plan or task.
- **Protected holdouts stay with their owner.** Cite a holdout policy by ref;
  holdout answers, scorer internals, private lint details, and calibration
  fixtures never enter a plan, map, spec, or packet.

## Semantic Readiness

The LLM judges semantic readiness from current intent, source artifacts, code,
and verifier evidence. Deterministic validation supplies facts and hard
preconditions; it does not determine plan or slice quality.

Judge each dimension `insufficient`, `sufficient`, or `strong`; use the weakest
dimension for the verdict:

1. source fidelity, from capture through plan to slices
2. operator outcome and demonstrability
3. current-state evidence and freshness risk
4. scope, non-goal, boundary, and authority clarity
5. option and tradeoff quality (plans only)
6. ownership and dependency quality
7. slice verticality and DAG coherence
8. verifier relevance
9. rollback and failure handling (plans only)
10. cold-start context sufficiency
11. implementation simplicity

A slice is judged on the nine dimensions not marked plans-only.

Verdicts:

- `ready`: every dimension is at least sufficient, fidelity passes, and no decision
  blocker remains.
- `needs_review`: a dimension is insufficient but a focused revision of the
  named plan or slice can repair it.
- `needs_interview` (plans): a human product, architecture, authority, or
  irreversible decision is unresolved.
- `implementation_handoff` (plans): the next uncertainty requires a spike/runtime
  proof, not more plan prose.
- `blocked` (slices): execution depends on an unresolved product, architecture,
  or authority decision, or on an unavailable code contract.

Classify alleged blockers before issuing the verdict:

- `code_blocker`: required executable, API, schema, or owner contract is unavailable
- `decision_blocker`: unresolved product, architecture, or authority choice
- `promotion_gate`: proof required for cutover, merge, release, or certification
- `administrative_hold`: queue or assignment state

Only the first two may make a slice `blocked`. Missing tests and harnesses are
slice work. Missing receipts require checking the live dependency; receipts are
post-execution outputs. Promotion gates and administrative holds must be shown
separately from implementation readiness.

Do not average weak dimensions into a passing score. Rejudge after every plan
or task rewrite. A green schema check, `lev task validate`, or existing verifier
is not semantic approval.

## Code, LLM, and Human Authority

- Deterministic code owns schema validation, reference existence, graph cycles,
  path policy, write-scope enforcement, and reproducible command results.
- core/eval decides whether a `check:` or evaluator passed; Exec performs
  effects and collects evidence. Planning authors requirement text and
  references, and states neither a verdict nor an effect in advance.
- The LLM owns intent interpretation, slice verticality, semantic readiness,
  verifier relevance, unnecessary complexity, and stale-context judgment.
- A human owns unresolved product tradeoffs and explicit approval where policy
  requires it.

## Adversarial Review

Use premortem, reverse brainstorming, falsification, Pentagon, LFD, or UltraQA
as reasoning tools when risk warrants them. Keep that reasoning transient.
Persist only information that changes execution: a unique failure mode, the
claim it threatens, and the verifier that can falsify it.

A review finding becomes a separate slice only when it has a distinct operator
outcome, owner, independently verifiable boundary, and reversible delivery unit.
Otherwise repair the existing slice's requirement rows or dependencies. Review
cycles do not authorize additional task emission.

## Write Gate

Render review output by default. Write a plan only inside authorized planning
scope. Write task artifacts only after explicit `emit`, `apply`, `edit`, or
`patch` authorization, or an approved capture row routed to Emit. `all slices`
is map authorization, not task-emission authorization. Emit must also pass the
[Emission Gate](references/execution-packet.md#emission-gate).

## Slice Map

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
proof boilerplate, or claims that all slices are execution-ready. A map does
not dispatch by itself, but every approved map must identify at least one
executable slice.

## Auto-Enrich Integration

`auto-enrich` works after source fidelity exists. It is a hardener, not a capture
replacement.

- Existing deep/high-risk plan: enrich the named plan in place, preserving fidelity.
- Existing design without a plan: enrich decisions, then compile a plan before
  slicing when work is multi-slice or cross-authority.
- Raw conversation: run `/capture` first.
- After every auto-enrich edit, recompute the plan fidelity table; no material row may
  disappear while architecture quality improves.
- Approval by an Architect/Critic loop is semantic evidence, not execution authority.

## Plan Types and Files

| Type | Pattern | Purpose |
|---|---|---|
| `plan-impl` | `plan-impl-*` | Feature or capability delivery |
| `plan-bugfix` | `plan-bugfix-*` | Defect investigation and resolution |
| `plan-chore` | `plan-chore-*` | Maintenance, cleanup, docs, tooling |
| `plan-research` | `plan-research-*` | Investigation with knowledge output |
| `plan-migration` | `plan-migration-*` | Transition between well-defined system shapes |

Required frontmatter remains backward-compatible:

```yaml
---
type: plan-impl
status: draft
priority: 2
slug: stable-kebab-name
created_at: YYYY-MM-DD
done_condition: "observable deterministic completion"
steps:
  - description: "claim-shaped step"
    validation: "check that can prove the claim"
acceptance_criteria: []
gates: []
---
```

New or materially updated standard/deep plans should also include:

```yaml
plan_depth: standard | deep
source_refs: []
fidelity_score: 0.0
review_state: unreviewed | needs_review | approved | implementation_handoff
first_slice: stable-slice-id | null
open_decisions: []
```

## Lifecycle FSM

```text
draft -> ready -> in_progress -> needs_validation -> validated -> done -> archived
                         |              |
                         +-> blocked    +-> ready on failed validation
```

Transitions:

- `draft -> ready`: source fidelity and semantic readiness pass; first slice exists.
- `ready -> in_progress`: an executor claims the plan or an emitted task references it.
- `in_progress -> needs_validation`: implementation is complete, not merely attempted.
- `needs_validation -> validated`: fitness functions and acceptance pass.
- `validated -> done`: move to `_done/` when no remaining plan work exists.
- `in_progress -> blocked`: concrete code/decision dependency prevents progress.
- `done -> archived`: historical reference only.

## Operations

```bash
lev loop --json
bd show <bd_id>
bd create --title="Implement feature X" --type=task -p 2
bd close <bd_id> --reason "completed per plan"
```

Update `status` in frontmatter for transitions. On validated completion, move the
plan to `.lev/pm/plans/_done/`. Do not create a second plan to represent a state
transition.

## Output

Render the Markdown inside live templates; do not print the XML wrapper tags.
Plan modes render `<plan-review>`, a slice review renders `<proposal-review>`,
Map renders `<slice-map>`, and Emit renders `<final-proposal>` from the
packet reference.

<plan-review>
## Plan: {slug}

Verdict: {ready|needs_review|needs_interview|implementation_handoff}
Depth: {light|standard|deep}
Source fidelity: {score}; lost rows {count}; narrowed rows {count}
Outcome: {operator_visible_result}
Current -> target: {one_sentence_transition}
First slice: {slice_id}; {outcome}; proof {verifier}
Weakest point: {dimension}; {reason}
Open decisions: {none_or_list}
Artifact: {plan_ref}
Next: {/auto-enrich|map|emit <slice-id>|/interview|implementation spike}
</plan-review>

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

## Next-Step Mini-Router

Offer only eligible next items using a numbered `#`, `Route`, `Expected result`
table when there is a real choice. Clear authorized transitions proceed
directly. Planning approval is not execution authority.

| Result | Route | Expected result |
|---|---|---|
| Decision unresolved | `skill://interview` or `skill://arch` | Resolve product choice or technical boundary before emission |
| Plan needs hardening | `skill://auto-enrich` | Improve the same plan |
| Broad plan missing, stale, or incomplete | Compile or Deepen | Repair the source plan before slicing |
| SDLC slice ready | Map or Emit | Map, or prepare the selected packet |
| Ready authorized SDLC packet | `skill://exec` | Execute the selected unit |
| Non-coding plan sufficient | `skill://exec` or selected domain skill | Execute within explicit scope; no SDLC packet |
| Pause / transfer / deferred | `skill://handoff` | Persist frontier, packet state, and resumption condition |

## Red Flags

- "The frontmatter validates, so the plan is ready."
- "The conversation was long; the plan can summarize aggressively."
- "The task list preserves the roadmap."
- "The first slice is clear, so other source requirements can stay in chat."
- "Smaller blast radius means a migration plan is higher quality."
- "Auto-enrich can recover details that capture omitted."
- "Architect approval means execution is authorized."
- "Every alternative is shallow, so I do not need to name why."
- "The executor can decide the open product or architecture decision."
- "All slices means emit all tasks."
- "A generated backlog is a roadmap."
- "Task validation passed, so semantic quality is proven."
- "More proof metadata makes the task more ready."
- "A task generated from an older design is still current."
- "Verifier exists, so the behavior is proven."
- "Session notes belong in task canon."
- "The proposal exists, so implementation can start."
- "The broad plan is optional; the slice map can recover it from chat."
- "A 95% fidelity average is fine even though one material constraint disappeared."
- "Emit can deepen a shallow migration plan while writing the first task."
- "The harness or receipt is missing, so implementation is blocked."
- "Every slice is held, but the map is still approved."
- "No current contract declares that evaluator, so the packet can define it inline or drop the claim."
