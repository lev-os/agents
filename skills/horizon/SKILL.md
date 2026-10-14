---
name: horizon
description: Use when the operator explicitly invokes /horizon or skill://horizon for an experimental long-horizon launch brief over aligned Lev intent; without that explicit request, planning, maps, and packets stay with lev-plan.
---

# /horizon - Long-Horizon Launch Brief (Experiment)

`horizon` turns aligned intent into one source-faithful Markdown launch brief:
a full success predicate, what does not count, per-stage artifacts and checks,
named review blocking conditions, bounded repair, and a resume point. The brief
is progressive: core blocks always, long-run blocks only when the run needs
them, and later branches stay open until their stage.

It runs beside `skill://lev-plan` and its `propose` alias and replaces neither;
`skill://poc` stays the proof lane. The method is adapted from Muratcan's
`long-horizon-prompting` (MIT); OMX is a later secondary review/state
reference, not a source of the method. See [NOTICE](NOTICE.md).

For non-trivial project work, load [Project Context](../lev/references/project-context.md)
before project-specific lookup.

## Fit Check

Run horizon when one operator outcome, its boundaries, and a relevant verifier
can be named. Aligned intent goes straight to the brief: synthesize settled
decisions and ask only about an unresolved choice that changes scope or
acceptance. Otherwise route once:

| Signal | Route |
|---|---|
| Conversation-only intent, no source ledger | `/capture` |
| Unresolved product, architecture, or authority decision | `/interview` (`skill://arch` for a technical boundary) |
| Unknown answer that a prototype would settle | `skill://poc` |
| Broad, migration, or cross-authority work with no plan | lev-plan Compile with the [plan template](../work/templates/plan.md); the brief cites that plan |
| Packet preview | Render it in this run through the packet reference below; no repeated shaping hop |
| Slice map or task-folder emission | lev-plan Map or Emit directly, passing the brief; emission stays with Emit |

Size the run before writing:

- **bounded**: one coherent outcome in one stage or a short sequential chain.
  Core blocks only, plus Worker Contracts when a stage is delegated; no
  portfolio, effort floor, or contamination block.
- **long**: multi-stage or multi-session. Add the resume frontier; add an
  effort floor only when early abandonment is a real risk.
- **parallel search**: two or more independent approach families are genuinely
  open and the budget covers parallel workers; add the portfolio block.

Read [worker contracts and long-run blocks](references/task-brief.md) before
writing stages whenever any stage is delegated to a worker, including in a
bounded sequential chain, and whenever the run needs a portfolio, solvability,
effort, or contamination block. A delegated bounded run takes only the Worker
Contracts and per-spawn guidance from it.

## Workflow

```yaml
steps:
  - id: bind_source
    action: Resolve the workstream, capture/design/plan/task refs, and any existing plan or task; freeze the intent in lev-plan's transition packet; list every material intent ID with its source ref, including later branches that are still unresolved.
    validation: "Every material intent has an intent_id and source_ref in the Fidelity and route table; an existing plan or task is reused; unresolved later branches are open rows, neither resolved nor dropped."
    on_failure: "Route per Fit Check; do not draft around missing intent."

  - id: write_predicate
    action: Write the full success predicate first - one sentence about the returned artifact with quantifiers, scope, and the narrowing assumptions it may not make. Work backward from what a complete answer lets the operator do.
    validation: "An adversarial reader can decide from the predicate alone whether a given artifact passes; every mechanically decidable part is named as a stage check."
    on_failure: "Not ready for a long run: decompose to a smaller predicate, send the decision to /interview, or the unknown to skill://poc."

  - id: exclude_near_misses
    action: Write Does Not Count with the refusal list - every result you would send back from a capable collaborator under pressure - starting from the defaults below. Then define each load-bearing term with its degenerate cases.
    validation: "Each predictable near miss is excluded by name and mapped to a row, an invalid_proof entry, or the review checklist; terms settle the empty, trivial, duplicate, and boundary cases the predicate must survive."

  - id: stage_checks
    action: Split the work into stages that each end in a named artifact stating its premises and conclusion locally. For each failure a stage can introduce, choose proof credible for that claim - a command check with a known-bad input where a command decides it; otherwise review from the diff, or named independent evidence or human review with its acceptance owner - and name the stage that waits on it.
    validation: "Every check is named after the failure it rules out and maps to one ledger row ID; command checks exist only where a command decides the claim, each naming an input on which it must go red; every other row names its reviewer or acceptance owner or is listed as unresolved proof; no stage starts before its input rows are satisfied."

  - id: set_review
    action: Write the checklist, named blocking conditions, and bounded repair from Review and Repair.
    validation: "The brief states which findings block and the evidence each needs; every recall has a finite cap."

  - id: set_return_and_resume
    action: Write the return predicate, the incomplete-return exits, and the resume frontier from Return, Stops, and Resume.
    validation: "Return depends on rows and open blocking findings, never on confidence, effort, or elapsed time; a fresh session can resume from the frontier without the originating chat."

  - id: red_team
    action: Ask a fresh instance for the cheapest way to make the artifact look done without satisfying the predicate; patch each answer the brief would accept with a Does Not Count line or a check.
    validation: "The last pass finds only near misses already excluded or caught."

  - id: render_and_route
    action: Render the brief from the template, plus a packet preview when asked, and name the next route. horizon writes no task folder and dispatches nothing.
    validation: "The brief cites ledger row IDs and carries no second executable ledger; any packet preview is labeled unvalidated and unemitted; Next names exactly one route."
```

## Does Not Count Defaults

Start every list here, then add the problem's own near misses:

- a result that holds only for a narrowed scope or special case
- a reduction to an unvalidated assumption, unavailable dataset, or another
  open question, including the domain's circular form: assuming something
  equivalent to the goal
- bounded or anecdotal verification presented as the whole
- approximate satisfaction where exact satisfaction is specified
- a plan, survey, status report, or explanation of difficulty in place of the
  artifact
- a stage reported done by an orchestrator that wrote the worker's output in
  its own turn
- a rendered brief or packet presented as validated or executed
- a check that passes on its known-bad input, or a degenerate value (NaN,
  empty, placeholder, too good to be true) treated as passing
- a weak or invented command standing in for a claim it cannot decide
- evidence produced before the last edit to the artifact it describes
- agreement among workers offered as proof

## Review and Repair

The reviewer works in fresh context, did not build the artifact, and hunts the
checklist: the domain's failure modes, its circularity analogue, degenerate
values, and Does Not Count. Decisive claims need proof from outside the model
loop that is credible for the claim: a command row where a command decides it;
otherwise named independent evidence (a field or external-owner verifier, or
human review) and its acceptance owner. When neither exists yet, list the proof
as unresolved rather than manufacturing a weak command to fill the slot. Treat
fast unanimity as a diversity warning, not corroboration.

A finding **blocks** only when it shows, with evidence (a failing check, a
counterexample, a reproduction), that the artifact violates the predicate, a
ledger row, or a named checklist item. Name each blocking condition in the
brief. Log every other finding, preferences included, as non-blocking; it never
delays convergence.

Each blocking finding becomes a **recall** to the responsible stage: failed row
IDs, the evidence, a narrowed scope, acceptance (those rows satisfied), and a
retry cap. Give the reviser the same context the reviewer had. Repair edits the
existing slice's rows or dependencies; a review cycle authorizes no new task.
At the cap, stop with the exact gap and route it: a decision to `/interview`,
a missing contract as a `code_blocker`, anything else to the operator.

## Return, Stops, and Resume

Return when the predicate holds, no blocking finding is open, and every stage
row is satisfied by its own proof with evidence produced after the last edit:
core/eval passes each command row, the review agent answers each review row,
and each named owner accepts their independent-evidence row. A row with
unresolved proof keeps return closed and is reported in the gap. Pair every
persistence instruction with this gate. An effort floor only removes
permission to quit early.

An explicit user stop, a hard budget, or unavailable required evidence always
wins over return rules and effort floors. Then return the strongest verified
state and the exact remaining gap, labeled incomplete. Reports carry artifacts
and evidence pointers; a status line without a pointer counts as no progress.

Resume follows lev-plan iteration planning: the frontier names the last passing
stage and its evidence ref, the open rows, and one next ready coherent unit, so
the outer loop reloads state from the ledger and runtime JSON instead of chat.

## Authority and Formats

- **One ledger.** Requirements and checks live in the task's `dna.yaml`
  `requirements:` (overflow in `evals/<name>.yaml` under the same key). Before
  a task exists, the plan's `steps[].validation` and acceptance criteria are
  the claim source; proposed rows appear once, in the packet preview when one
  is rendered or else as one sentence per proposed ID in the brief, and
  lev-plan Emit makes them canonical. The brief otherwise cites IDs.
- **Existing v2 rows.** The success predicate is the operator's
  `type: acceptance` row; a stage exit is an acceptance row with `owner_slice`;
  constraints and checkable exclusions are `type: constraint` rows or
  `invalid_proof` entries on the row they threaten. A typed check such as
  `no_future_leakage: bool` becomes a row named after the failure whose
  `check:` exit decides it. A claim proven by independent evidence or human
  review is a row without `check:` whose sentence names the evidence and the
  acceptance owner.
- **Proof is not launch.** Proof is rows and their `check:`. Launch is
  `lev task validate <task>`, then `lev sdlc exec <task> --flow <flow>`, with
  the flow chosen under lev-plan's Proof and Evaluator Selection; `topology`
  stays a slice classification.
- **core/eval decides; Exec acts.** Verdict ownership is unchanged: core/eval
  decides `check:` rows, Exec performs effects, and horizon states no verdict
  or effect in advance. Current keys only: when a stage would need
  `eval_packs`, a proof-gate container, a flow field, an inline evaluator, or a
  boolean packet field, hold it as a `code_blocker` naming the missing
  contract.
- **Limits live outside the prose.** Hard budgets, permissions, and stops
  belong to the operator and runtime; the brief restates them for planning.
  One run neither validates nor refutes a brief; trials belong to the eval
  owner.
- **Holdouts stay out.** Holdout answers, scorer internals, and calibration
  fixtures never enter the brief or authoring scope; cite the policy by ref.
- **Formats.** Brief and plans are Markdown, machine declarations current YAML,
  runtime state the JSON its runtime owns.

When a stage check must become, or be checked against, a requirement row, or
the operator wants a packet preview, read
[Execution Packet](../lev-plan/references/execution-packet.md) in the same run
before writing those checks or the preview. Render the preview from its row
shape and emitted task shape, labeled preview: not validated, executed, or
emitted. Task-folder emission stays with lev-plan Emit.

## Write Gate

Render by default. Persist only into an existing artifact inside authorized
scope: a broad brief as a section of its plan under `.lev/pm/plans/`, a
bounded brief in the response or, when authorized, as a light plan. Packet
previews stay in the response; task folders come only from lev-plan Emit with
explicit authorization.

## Brief Template

Render the Markdown inside; do not print the wrapper tags. Delete blocks that
do not apply; a bounded run keeps the core blocks only. A `lost` fidelity row
blocks a ready brief, and `narrowed-approved` needs the operator's decision.

<horizon-brief>
## Horizon Brief: {brief_id}

Intent: {one_sentence_intent}
Source: {capture|design|plan|task refs}; intent IDs {ids}
Plan: {plan_ref | plan_not_required: one_sentence_rationale}
Ledger: {task_ref requirements | plan_ref steps | proposed rows pending Emit}
Run: {bounded|long|parallel search}; limits {user stops, hard budgets, permissions}
State: {memory|disk:ref}; confidence {low|medium|high}; blocker {none|code_blocker|decision_blocker: reason}

### Definitions
- {term}: {meaning}; degenerate cases {empty|trivial|duplicate|boundary}

### Success Predicate
{One sentence: what must be true of the returned artifact, with quantifiers, scope, and the narrowing assumptions it may not make.}

### Does Not Count
- {near miss}: excluded by {row_id | invalid_proof on row_id | review checklist}

### Stages
| Stage | Artifact | Rows (proof) | Rules out | Known-bad input | Waits on |
|---|---|---|---|---|---|
| {S1} | {path} | {row_id: command | review | owner} | {failure} | {fixture or n/a} | {none or stage} |

### Review
Checklist: {domain failure modes; circularity analogue; degenerate values}
Blocks when: {named condition}; evidence {failing check | counterexample | reproduction}
Non-blocking: logged; never delays return
Outside-loop proof: {command row_id | independent evidence or human review: row_id, owner}; unresolved {none | row_ids}

### Repair
Recall: {stage}; failed rows {ids}; evidence {ref}; narrowed scope {scope}; acceptance {rows satisfied}; cap {n}
At cap: stop with the exact gap; route {/interview | code_blocker | operator}

### Return
Return when: predicate holds, every stage row is satisfied by its proof with evidence after the last edit, and no blocking finding is open.
Incomplete only on: explicit user stop, hard budget, or unavailable required evidence; strongest verified state plus exact gap.

### Resume
Frontier: last passing stage {id} at {evidence_ref}; open rows {ids}; next unit {one ready coherent unit}

### Open Branches
- {later branch}: {intent_id}; open because {reason}; owner {route}

### Fidelity and Route
| Intent ID | Source ref | Brief destination | Ledger row | Preservation | Route / blocker |
|---|---|---|---|---|---|
| {INT-*} | {ref} | {block or stage} | {row_id or pending} | {preserved|narrowed-approved|deferred-explicit|conflict|lost} | {route or blocker class} |

Proof: commands {row_ids}; review-answered {row_ids}; independent or human {row_id: owner}; unresolved {none | row_ids}
Packet: {preview from the packet reference, unvalidated and unemitted | not requested}; emission via lev-plan Emit
Launch: `lev task validate {task}`, then `lev sdlc exec {task} --flow {selected_flow}` | none until Emit
Next: {lev-plan emit {slice_id} | /exec | skill://poc | /interview | resume {unit}}
</horizon-brief>

## Work Link

Lifecycle lane: Plan (experiment beside `/lev-plan`)
Entity movement: `aligned | planned -> proposed | needs_interview | needs_plan`; execution readiness stays with lev-plan Emit
Workstream: resolved as `/lev-plan` does before any durable write
Upstream: `/capture`, `/interview`, `.lev/pm/designs/*`, `.lev/pm/plans/*`, aligned bounded intent
Downstream: `/lev-plan` (Compile, Map, Emit), `skill://poc`, `/interview`, `/exec` after a validated packet
Router: `/work`
