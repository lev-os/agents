# Horizon Method: Long-Horizon Launch Brief (Experiment)

The horizon method turns aligned intent into one source-faithful Markdown
launch brief: a full success predicate, what does not count, per-stage
artifacts and checks, named review blocking conditions, bounded repair, and a
resume point. The brief is progressive: core blocks always, long-run blocks
only when the run needs them, and later branches stay open until their stage.

Two entries load this file. `lev-plan` loads it through
[long-horizon planning](long-horizon.md), which says how the brief goes into
the plan. The direct `/horizon` command loads it through
[its entry](../../horizon/SKILL.md), which holds the Fit Check. `skill://poc`
stays the proof lane. The method is adapted work: see
[the notice](horizon-notice.md) when you copy or publish it.

The method cites rules of lev-plan by link. A lev-plan caller has them loaded.
A direct `/horizon` caller reads each cited section when it reaches the link.

## Contents

- [Run Size](#run-size): bounded, long or parallel search, and when to load the long-run blocks
- [Workflow](#workflow): the eight steps from bound source to rendered brief
- [Does Not Count Defaults](#does-not-count-defaults): the near misses every brief excludes
- [Review and Repair](#review-and-repair): the reviewer, blocking findings, recalls, run budget, frozen formats
- [Return, Stops, and Resume](#return-stops-and-resume): the return gate, the stops that win over it, the frontier
- [Authority and Formats](#authority-and-formats): the one ledger, row types, limits, the packet preview
- [Write Gate](#write-gate): where a brief may be saved
- [Brief Template](#brief-template): the `horizon-brief` output

## Run Size

Size the run before writing:

- **bounded**: one coherent outcome in one stage or a short sequential chain.
  Core blocks only, plus Worker Contracts when a stage is delegated; no
  portfolio or effort floor. Add contamination guards if result independence
  matters, even for a short run.
- **long**: multi-stage or multi-session. Add the resume frontier; add an
  effort floor only when early abandonment is a real risk.
- **parallel search**: two or more independent approach families are genuinely
  open and the budget covers parallel workers; add the portfolio block.

Read [worker contracts and long-run blocks](horizon-long-run-blocks.md) before
writing stages whenever any stage is delegated to a worker, including in a
bounded sequential chain, and whenever the run needs a portfolio, solvability,
effort, or contamination block, or a pre-launch review of a long or parallel
brief. Score every long or parallel brief before launch with that file's
Pre-Launch Score. A delegated bounded run
takes Worker Contracts and per-spawn guidance, plus any applicable contamination
guard; it does not need the full long-run score.

## Workflow

```yaml
steps:
  - id: bind_source
    action: Run the prior-art lookup of lev-plan's `inspect_current_state` step first (read that step in [lev-plan's Workflow](../SKILL.md#workflow) for the exact `lev find` call and its fallbacks); when lev-plan already ran it in this work, reuse its cards. Resolve the workstream, capture/design/plan/task refs, and any existing plan or task; freeze the intent in lev-plan's transition packet; list every material intent ID with its source ref, including later branches that are still unresolved.
    validation: "Every material intent has an intent_id and source_ref in the Fidelity and route table; an existing plan or task is reused; unresolved later branches are open rows, neither resolved nor dropped."
    on_failure: "Route as the entry says (direct /horizon: its Fit Check; inside lev-plan: Which Stage and this step's own on_failure there); do not draft around missing intent."

  - id: write_predicate
    action: Write the full success predicate first - one sentence about the returned artifact with quantifiers, scope, and the narrowing assumptions it may not make. Work backward from what a complete answer lets the operator do.
    validation: "An adversarial reader can decide from the predicate alone whether a given artifact passes; every mechanically decidable part is named as a stage check."
    on_failure: "Not ready for a long run: decompose to a smaller predicate, send the decision to /interview, or the unknown to skill://poc."

  - id: exclude_near_misses
    action: Write Does Not Count with the refusal list - every result you would send back from a capable collaborator under pressure - starting from the defaults below. Then define each load-bearing term with its degenerate cases.
    validation: "Each predictable near miss is excluded by name and mapped to a row, an invalid_proof entry, or the review checklist; terms settle the empty, trivial, duplicate, and boundary cases the predicate must survive."

  - id: stage_checks
    action: Split the work into stages that each end in a named artifact stating its premises and conclusion locally. For each failure a stage can introduce, choose proof credible for that claim - a command check with a known-bad input where a command decides it; otherwise review from the diff, or named independent evidence or human review with its acceptance owner - and name the stage that waits on it. Assign a check owner to run each command check against its known-bad control before that check can justify acceptance; planning names the run and required evidence, and authorized execution collects it. Give each stage a run budget, and freeze the format of every artifact a long run reads before that run starts (Review and Repair).
    validation: "Every stage names its run budget, and every artifact a long run reads names its frozen format version; every check is named after the failure it rules out and maps to one ledger row ID; command checks exist only where a command decides the claim, each naming a known-bad control, check owner and sensitivity evidence required before acceptance; every other row names its reviewer or acceptance owner or is listed as unresolved proof; no stage starts before its input rows are satisfied."

  - id: set_review
    action: Write the checklist, named blocking conditions, and bounded repair from Review and Repair.
    validation: "The brief states which findings block and the evidence each needs; every recall has a finite cap."

  - id: set_return_and_resume
    action: Write the return predicate, the incomplete-return exits, and the resume frontier from Return, Stops, and Resume.
    validation: "Return depends on rows and open blocking findings, never on confidence, effort, or elapsed time; a fresh session can resume from the frontier without the originating chat."

  - id: red_team
    action: Load the `review` skill by its name (the Skill tool with `review`; a host with no Skill tool opens ~/.agents/skills/review/SKILL.md) with the attacker stance, naming the brief and horizon as the caller in its arguments; review's fresh reader attacks the predicate. When review routed you here, skip this load and use the stance and lenses it gave. When review already ran on the same brief in this work and the brief has not changed since, cite that run's report file instead of a second run. Patch each answer the brief would accept with a Does Not Count line or a check, and put that review run's chat line (the review skill's Report section) under the review checklist.
    validation: "The last pass finds only near misses already excluded or caught."

  - id: render_and_route
    action: Run the zoom_out read that Review and Repair orders before rendering. Then render the brief from the template, plus a packet preview when asked, and name the next route. The method dispatches nothing (Write Gate).
    validation: "The brief cites ledger row IDs and carries no second executable ledger; any packet preview is labeled unvalidated and unemitted; every preserved row passes the cold-read recall check; Next names exactly one route, and evidence with no available owner stays unresolved. The review checklist holds one chat line of the review skill for each run (the red_team run and the run before rendering; the cited run's line when an earlier run is cited), each with its report file's path, or, when the review skill could not be loaded, the line 'review: could not run ({reason})'. Until then the brief is unreviewed: it stays uncommitted, and no reply calls it finished."
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
- output of a long run that is read through a format changed after that run
  started
- agreement among workers offered as proof

When a counterexample or impossibility result is an allowed outcome, require
its complete certificate; an unverified candidate does not satisfy that branch.

## Review and Repair

The reviewer works in fresh context, did not build the artifact, and hunts the
checklist: the domain's failure modes, its circularity analogue, degenerate
values, and Does Not Count. Decisive claims need proof from outside the model
loop that is credible for the claim: a command row where a command decides it;
otherwise named independent evidence (a field or external-owner verifier, or
human review) and its acceptance owner. When neither exists yet, list the proof
as unresolved rather than manufacturing a weak command to fill the slot. Treat
fast unanimity as a diversity warning, not corroboration.

Before rendering the brief, load the `review` skill by its name (the Skill tool with
`review`; a host with no Skill tool opens ~/.agents/skills/review/SKILL.md); name in its
arguments the brief, lens `zoom_out`, and horizon as the caller. Its findings are advice:
put its chat line (the review skill's Report section) under the review checklist; a blocker from it
becomes a blocking condition only when it meets the rule below.

A finding **blocks** only when it shows, with evidence (a failing check, a
counterexample, a reproduction), that the artifact violates the predicate, a
ledger row, or a named checklist item. Name each blocking condition in the
brief. Log every other finding, preferences included, as non-blocking; it never
delays convergence.

Each blocking finding becomes a **recall** to the responsible stage: failed row
IDs, the evidence, a narrowed scope, acceptance (those rows satisfied), and a
retry cap. Give the reviser the same context the reviewer had. What a repair
may edit, and that a review cycle authorizes no new task, is lev-plan's
[Adversarial Review](../SKILL.md#adversarial-review).
The reviser needs capability, tools and task-specific prompt support suitable
for the findings and comparable to the reviewer, as well as the same relevant evidence. If that support is unavailable,
hold the repair and report the gap; a stronger audit alone does not repair it.
Repair support grants no model, account or permission change.
At the cap, stop with the exact gap and route it: a decision to `/interview`,
a missing contract as a `code_blocker`, anything else to the operator.

A stage also carries a **run budget**: the worker runs it may spend on builds,
reviews and repairs together, set when the stage is defined; the owner's rerun
is counted apart. At the budget, stop, report runs spent against runs left, and
take the **narrow exit** first: a smaller predicate that holds now, with the
rest as one open row. A wider exit goes to the operator.

Every choice shown to the operator, and every change of approach, names its
**size**: worker runs, machine hours, and what stays unproven.

A long run reads only frozen formats. Version the format of each artifact it
reads and settle that version before the run starts; a later format change
makes the run's output stale, and the plan then names the rerun and its size.

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

The brief adds no authority of its own. The plan skill and the packet reference
hold the rules; this section says only how a brief uses them.

- **One ledger.** The ledger is the task's `requirements:` list
  ([Requirements Ledger](execution-packet.md#requirements-ledger)); before a
  task exists, the claim source is the plan, as lev-plan's Iteration planning
  says. Proposed rows appear once, in the packet preview when one is rendered
  or else as one sentence per proposed ID in the brief, and lev-plan Emit makes
  them canonical. The brief otherwise cites IDs.
- **Brief parts as rows.** Use the row shape of the Requirements Ledger. The
  success predicate is the operator's `type: acceptance` row; a stage exit is
  an acceptance row with `owner_slice`; constraints and checkable exclusions
  are `type: constraint` rows or `invalid_proof` entries on the row they
  threaten. A typed check such as
  `no_future_leakage: bool` becomes a row named after the failure whose
  `check:` exit decides it. A claim proven by independent evidence or human
  review is a row without `check:` whose sentence names the evidence and the
  acceptance owner.
- **Proof is not launch.** Proof is rows and their `check:`. The launch
  commands and the flow choice are in
  [Flow and Launch](execution-packet.md#flow-and-launch).
- **Who decides, and holds.** Verdict and effect ownership are lev-plan's
  [Code, LLM, and Human Authority](../SKILL.md#code-llm-and-human-authority);
  the brief states no verdict or effect in advance. A stage that would need a
  key or evaluator outside the current contracts (`eval_packs`, a proof-gate
  container, a flow field, an inline evaluator, a boolean packet field) is a
  hold under "Hold, never drop" and holdouts stay with their owner, both in
  [Proof and Evaluator Selection](../SKILL.md#proof-and-evaluator-selection).
- **Limits live outside the prose.** Hard budgets, permissions, and stops
  belong to the operator and runtime; the brief restates them for planning.
  One run neither validates nor refutes a brief; trials belong to the eval
  owner.
- **Formats.** The brief is Markdown. The format of every other artifact is in
  the intro of [lev-plan](../SKILL.md).

When a stage check must become, or be checked against, a requirement row, or
the operator wants a packet preview, read
[Execution Packet](execution-packet.md) in the same run
before writing those checks or the preview. Render the preview from its row
shape and emitted task shape, labeled preview: not validated, executed, or
emitted.

## Write Gate

lev-plan's [Write Gate](../SKILL.md#write-gate) applies. In addition, a brief persists
only into an existing artifact inside authorized scope: a broad brief as a
section of its plan under `.lev/pm/plans/`, a bounded brief in the response or,
when authorized, as a light plan. Packet previews stay in the response.

## Brief Template

Render the Markdown inside; do not print the wrapper tags. Delete blocks that
do not apply; a bounded run keeps the core blocks only. The preservation states
and what `lost` and `narrowed-approved` do to a brief are the rules of
lev-plan's [Source Fidelity Gate](../SKILL.md#source-fidelity-gate).

A row counts as `preserved` only when its decision-bearing constraints,
cross-owner boundaries, and unresolved options appear in the brief or behind an
exact source retrieval pointer. Copy full stable IDs, session identity, and
other opaque refs exactly. Before marking the brief ready, cold-read it in fresh
context and confirm each row's constraints and unknowns are recoverable from the
brief or its pointers. Next names a route only for a gap its owner can close;
evidence with no available owner stays an unresolved blocker.

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
| Stage | Artifact | Rows (proof) | Rules out | Known-bad input | Waits on | Run budget |
|---|---|---|---|---|---|---|
| {S1} | {path; format {version, frozen} when a long run reads it} | {row_id: command | review | owner} | {failure} | {fixture or n/a} | {none or stage} | {n worker runs} |

### Review
Checklist: {domain failure modes; circularity analogue; degenerate values}
Blocks when: {named condition}; evidence {failing check | counterexample | reproduction}
Non-blocking: logged; never delays return
Outside-loop proof: {command row_id | independent evidence or human review: row_id, owner}; unresolved {none | row_ids}

### Repair
Recall: {stage}; failed rows {ids}; evidence {ref}; narrowed scope {scope}; acceptance {rows satisfied}; cap {n}
At cap or run budget: stop with the exact gap and runs {spent}/{budget}; narrow exit {smaller predicate + one open row}; route {/interview | code_blocker | operator}

### Return
Return when: predicate holds, every stage row is satisfied by its proof with evidence after the last edit, and no blocking finding is open.
Incomplete only on: explicit user stop, hard budget, or unavailable required evidence; strongest verified state plus exact gap.

### Resume
Frontier: last passing stage {id} at {evidence_ref}; open rows {ids}; next unit {one ready coherent unit}

### Open Branches
- {later branch}: {intent_id}; open because {reason}; owner {route}; size {worker runs; machine hours; what stays unproven}

### Fidelity and Route
| Intent ID | Source ref | Brief destination | Ledger row | Preservation | Route / blocker |
|---|---|---|---|---|---|
| {INT-*} | {ref} | {block or stage} | {row_id or pending} | {preserved|narrowed-approved|deferred-explicit|conflict|lost} | {route or blocker class} |

Proof: commands {row_ids}; review-answered {row_ids}; independent or human {row_id: owner}; unresolved {none | row_ids}
Packet: {preview from the packet reference, unvalidated and unemitted | not requested}; emission via lev-plan Emit
Launch: `lev entity task validate {task}`, then `lev sdlc exec {task} --flow {selected_flow}` | none until Emit
Next: {lev-plan emit {slice_id} | /exec | skill://poc | /interview | resume {unit}}
</horizon-brief>
