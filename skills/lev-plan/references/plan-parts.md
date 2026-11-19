# Plan Parts

What every plan holds, for `lev-plan` Compile, Deepen, and Review. The steps
are in [`../SKILL.md`](../SKILL.md); this file adds no step. Slices are in
[Slices](slices.md) and claims in [Proof](proof.md).

## Contents

- [The eight parts](#the-eight-parts): what a plan holds, and what depth changes
- [Depth](#depth): light, standard, deep; and when a run is long, delegated, or a parallel search
- [Source](#source): the alignment handoff, intake by source, the fidelity table
- [Outcome](#outcome): the success sentence, Does Not Count, definitions
- [Current to target](#current-to-target): evidence, options, design from intent
- [Review and Repair](#review-and-repair): the reviewer, blocking findings, recalls, run budget, auto-enrich
- [Return and Resume](#return-and-resume): the return gate, the stops that win, the frontier
- [Readiness](#readiness): dimensions, verdicts, blocker classes
- [Plan Form](#plan-form): where the one plan form is

## The eight parts

| # | Part | Holds | Home |
|---|---|---|---|
| 1 | Source | Source context and the fidelity table | [Source](#source) |
| 2 | Outcome | The success sentence, observable done, scope, non-goals, authority, forbidden moves, Does Not Count, definitions | [Outcome](#outcome) |
| 3 | Current to target | Current state with evidence and freshness, target state, decision drivers, options, tradeoffs, rejected alternatives, ownership boundaries where architecture matters | [Current to target](#current-to-target) |
| 4 | Vertical slices | Dependency and slice DAG with critical path; per-slice outcome, artifact, proof, status, covered intent IDs, open decisions; the first executable slice | [Slices](slices.md) |
| 5 | Claims and proof | The claim-to-proof map: program, agent, or person for each claim, and its guard | [Proof](proof.md) |
| 6 | Review and repair | Checklist, blocking conditions, recall and cap, run budget | [Review and Repair](#review-and-repair) |
| 7 | Return and resume | Return gate, stops, frontier, the next lifecycle route | [Return and Resume](#return-and-resume) |
| 8 | Risk and rollback | Risks, pre-mortem where required, mitigation, detection, residual risk, rollback, architecture review triggers | the `design_failure_and_rollback` step of [`../SKILL.md`](../SKILL.md) |

The eight keys are fixed; adapt what each part says to the domain. A plan is
not complete merely because the eight keys exist.

Deep evidence targets, borrowed from demonstrated planning practice:

- At least 80% of load-bearing current-state claims cite exact files, lines, commands,
  or external authority refs.
- At least 90% of acceptance criteria are observable/testable.

## Depth

| Depth | Use when | What each part holds |
|---|---|---|
| `light` | One obvious bounded change | Each part in a line or two: the source ref; the goal as the success sentence with its scope; what changes; the steps as one or more slices; one claim with its proof; what a review must not find; the stop; the way back. Suggest skipping the plan if execution is clearer |
| `standard` | One feature or coherent multi-step change | Every part in full except options and pre-mortem, which stay short |
| `deep` | Migration, architecture, security, destructive work, 3+ authorities, or multi-slice roadmap | Every part in full, with options/tradeoffs, DAG, pre-mortem, rollback, review |

Do not inflate a light plan. Do not compress deep work into a list of activities.

Depth is about risk. Apart from it, say how the run goes:

- **bounded**: one coherent outcome in one slice or a short sequential chain.
  No resume frontier beyond the next unit, no portfolio, no effort floor.
- **long**: multi-slice across sessions, or autonomous. The resume frontier is
  written in full.
- **parallel search**: two or more independent approach families are genuinely
  open and the budget covers parallel workers.

What a long, delegated, or parallel run adds is in
[long-horizon planning](long-horizon.md); the References table of
[`../SKILL.md`](../SKILL.md) says when to read it, and it is read before the
slices are written.

## Source

### Alignment handoff

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

Resolve or fetch every explicitly supplied local path, issue number, tracker URL,
or external URL through its owning source, then read the full artifact/body and
all accessible comments. Report inaccessible material instead of reconstructing
it. Preserve settled decisions about changed modules/interfaces, developer
clarifications, architecture, schemas, API contracts and interactions when
applicable. Additional notes belong only when they change execution or explain
a constraint; do not fill irrelevant headings.

### Source Fidelity Gate

Reuse the five capture components:

```
fidelity = 0.30*detail_preservation
         + 0.25*relationship_preservation
         + 0.20*source_attribution
         + 0.15*neighbor_context
         + 0.10*actionability
```

The plan must contain the `source.rows` list of the
[plan form](plan-form.md), with one row for every material
capture/design row: a goal, constraint, non-goal, decision boundary,
acceptance, or relationship. Each row names its source ref, its destination
(section, slice, decision, or deferment), its claim id or `pending`, a
fidelity of 0.00-1.00, what changed and who approved it, and its route or
blocker class. Its preservation is one of `preserved`, `narrowed-approved`,
`deferred-explicit`, `conflict`, `lost`.

Rules:

- `lost` blocks planning, mapping, and emission.
- `narrowed-approved` requires an explicit source/user decision; the planner
  never narrows a row on its own.
- Every material relationship and non-goal gets its own coverage, not just goals.
- Overall fidelity must be at least 0.90 and must not be lower than the source capture.
- An average cannot hide one missing material row.
- For a map or packet, every material source intent ID is covered by a slice,
  preserved as a plan-level constraint/non-goal, or explicitly deferred with
  owner approval.
- A row counts as `preserved` only when its decision-bearing constraints,
  cross-owner boundaries, and unresolved options appear in the plan or behind
  an exact source retrieval pointer. Copy full stable IDs, session identity,
  and other opaque refs exactly.

## Outcome

The success sentence is written first (the `frame_outcome` step). Every part
of it that a command can decide becomes a program claim.

### Does Not Count

Name the near misses the plan refuses. Start every list here, then add the
problem's own; a light plan keeps only the lines that could happen to it:

- a result that holds only for a narrowed scope or special case
- a reduction to an unvalidated assumption, unavailable dataset, or another
  open question, including the domain's circular form: assuming something
  equivalent to the goal
- bounded or anecdotal verification presented as the whole
- approximate satisfaction where exact satisfaction is specified
- a plan, survey, status report, or explanation of difficulty in place of the
  artifact
- a slice reported done by an orchestrator that wrote the worker's output in
  its own turn
- a rendered plan or packet presented as validated or executed
- a check that passes on its known-bad input, or a degenerate value (NaN,
  empty, placeholder, too good to be true) treated as passing
- a weak or invented command standing in for a claim it cannot decide
- evidence produced before the last edit to the artifact it describes
- output of a long run that is read through a format changed after that run
  started
- agreement among workers offered as proof

When a counterexample or impossibility result is an allowed outcome, require
its complete certificate; an unverified candidate does not satisfy that branch.

## Current to target

**Design from intent** (JP 2026-10-28). Read captures, decisions and designs as
evidence of an intent, not as the answer. Name the shared intent, then plan what
should happen from first principles; an explicit ruling still stands, and a better
ideal becomes a new decision. Every design or plan choice includes "What experts
would do:" with one line for each domain that fits (`- {domain}: {what they would do}`).

Reference current owner paths for executable handoff, with freshness context;
source advice to omit all paths is superseded by Lev's evidence-backed ownership.
When a prototype's state machine, reducer, schema or type shape expresses a
decision more precisely than prose, retain only that decision-rich snippet and
its prototype provenance, not the whole demo.

When uncertainty needs a prototype, route the question to `skill://poc`. Preserve
only its explicit question, selected logic/UI branch, stated assumptions, validated
answer, and provenance in the plan or packet; prototype construction details
remain owned by `skill://poc`.

## Review and Repair

The reviewer works in fresh context, did not build the artifact, and hunts the
checklist: the domain's failure modes, its circularity analogue, degenerate
values, and Does Not Count. The review load itself is the `judge_readiness`
step. Treat fast unanimity as a diversity warning, not corroboration.

Use `pre_mortem`, `reverse_brainstorm`, `falsification` and the attacker stance
(`skill://review`), Pentagon or LFD by plan depth. Keep that reasoning transient.
Persist only information that changes execution: a unique failure mode, the
claim it threatens, and the verifier that can falsify it.

A finding **blocks** only when it shows, with evidence (a failing check, a
counterexample, a reproduction), that the artifact violates the success
sentence, a claim, or a named checklist item. Name each blocking condition in
the plan. Log every other finding, preferences included, as non-blocking; it
never delays convergence.

Each blocking finding becomes a **recall** to the responsible slice: failed
claim IDs, the evidence, a narrowed scope, acceptance (those claims satisfied),
and a retry cap. Give the reviser the same context the reviewer had. The
reviser needs capability, tools and task-specific prompt support suitable for
the findings and comparable to the reviewer, as well as the same relevant
evidence. If that support is unavailable, hold the repair and report the gap;
a stronger audit alone does not repair it. Repair support grants no model,
account or permission change. At the cap, stop with the exact gap and route
it: a decision to `/interview`, a missing contract as a `code_blocker`,
anything else to the operator.

A review finding becomes a separate slice only when it has a distinct operator
outcome, owner, independently verifiable boundary, and reversible delivery unit.
Otherwise repair the existing slice's claims or dependencies. Review cycles do
not authorize additional task emission.

Every slice carries a **run budget**: the worker runs it may spend on builds,
reviews and repairs together, set when the slice is defined; the owner's rerun
is counted apart. A light plan states it in one line for the whole plan. At the budget, stop, report runs spent against runs left, and
take the **narrow exit** first: a smaller success sentence that holds now, with
the rest as one open claim. A wider exit goes to the operator.

Every choice shown to the operator, and every change of approach, names its
**size**: worker runs, machine hours, and what stays unproven.

`auto-enrich` works after source fidelity exists. It is a hardener, not a capture
replacement.

- Existing deep/high-risk plan: enrich the named plan in place, preserving fidelity.
- Existing design without a plan: enrich decisions, then compile a plan before
  slicing when work is multi-slice or cross-authority.
- Raw conversation: run `/capture` first.
- After every auto-enrich edit, recompute the plan fidelity table; no material row may
  disappear while architecture quality improves.
- Approval by an Architect/Critic loop is semantic evidence, not execution authority.

## Return and Resume

Return when the success sentence holds, no blocking finding is open, and every
claim is satisfied by its own proof with evidence produced after the last
edit: core/eval passes each program claim, the review agent answers each agent
claim, and each named owner accepts their claim. A claim with unresolved proof
keeps return closed and is reported in the gap. Pair every persistence
instruction with this gate.

An explicit user stop, a hard budget, or unavailable required evidence always
wins over return rules and effort floors. Then return the strongest verified
state and the exact remaining gap, labeled incomplete. Reports carry artifacts
and evidence pointers; a status line without a pointer counts as no progress.

The resume frontier names the last passing slice and its evidence ref, the
open claims, and one next ready coherent unit, so the outer loop reloads state
from the plan and runtime JSON instead of chat.

Prepare long-running efforts for one coherent unit per future Ralph iteration:
name the next ready chunk, its acceptance/claim checks, dependencies, permitted
effects and stopping condition. Prompt: "Do the next bit of work on this effort;
select ONE ready coherent unit, finish that single thing, record the result and
remaining frontier, then stop." One thing may be a substantial vertical chunk,
not the full effort. The outer loop reloads state and chooses whether to
continue; `lev-ralph` adds a worker/reviewer-fixer cycle within that unit.
Runtime adoption is deferred: creating a plan or preparing a packet does not
run the loop, dispatch, or prove Ralph.

Hard budgets, permissions, and stops belong to the operator and runtime; the
plan restates them for planning. One run neither validates nor refutes a plan;
trials belong to the eval owner.

## Readiness

The LLM judges semantic readiness from current intent, source artifacts, code,
and verifier evidence. Deterministic validation supplies facts and hard
preconditions; it does not determine plan or slice quality.

Judge each dimension `insufficient`, `sufficient`, or `strong`; use the weakest
dimension for the verdict:

1. source fidelity, from capture through plan to slices
2. operator outcome and demonstrability: an adversarial reader decides pass or
   fail from the success sentence; load-bearing terms are defined; this
   problem's plausible near misses are excluded by name
3. current-state evidence and freshness risk
4. scope, non-goal, boundary, and authority clarity; budgets, permissions, and
   stops are enforced by operator or runtime, not by prose
5. option and tradeoff quality (plans only)
6. ownership and dependency quality
7. slice verticality and DAG coherence
8. verifier relevance: each claim's proof can fail, and reports carry evidence
   produced after the last edit
9. rollback and failure handling (plans only)
10. cold-start context sufficiency
11. implementation simplicity
12. return and resume (plans only): every persistence instruction has a
    matching return gate; incomplete return only on user stop, hard budget, or
    unavailable evidence
13. review checklist (plans only): the domain's failure modes, its circularity
    analogue, and degenerate values are named

A slice is judged on the dimensions not marked plans-only. A long or parallel
run also takes long-horizon planning's
[Pre-Launch Check](long-horizon.md#pre-launch-check), which raises the bar
for launch above `sufficient`.

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
or task rewrite. A green schema check, `lev entity task validate`, or existing verifier
is not semantic approval.

## Plan Form

The one plan form is the [plan form](plan-form.md): a YAML record with one
key for each part, declared by the plan record type. Read it
before you write or patch a plan, and before you render a plan in the response
when no write is authorized.
