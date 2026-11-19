# Long-Horizon Planning and Execution

What a plan adds beyond the eight parts; the References table of
[`../SKILL.md`](../SKILL.md) says when this file is read. The eight parts of every plan are in
[Plan parts](plan-parts.md); this file adds no mode, command, task field,
scheduler or runtime implementation. The material is adapted work: see
[the notice](notice.md) when you copy or publish it.

## Contents

- [Which blocks a run takes](#which-blocks-a-run-takes)
- [Long-Run Blocks](#long-run-blocks): worker contracts, portfolio, solvability, effort, contamination
- [Filling Notes](#filling-notes)
- [Pre-Launch Check](#pre-launch-check)
- [Run the authorized effort](#run-the-authorized-effort): the loop through `skill://orch`
- [Return and resume across slices](#return-and-resume-across-slices)

## Which blocks a run takes

Keep one plan, one slice map and one claim list. Planning-only Compile,
Deepen, Review and Map requests stop at their requested artifact.

| Run | Takes |
|---|---|
| Any plan with a delegated slice, bounded chains included | Worker Contracts and the per-spawn spec |
| Any run where result independence matters, short and undelegated runs included | Contamination |
| Any run whose question may have no solution | Solvability (Filling Notes) |
| Long | The above when delegated; the full resume frontier; Effort only when early abandonment is a real risk |
| Parallel search | Portfolio, and the rest as for a long run |

A run that needs none of these loads nothing from this file.

## Long-Run Blocks

Add only the blocks the run needs to the plan, under its `long_run` key, one
key for each block. In a reply, render the Markdown; do not print the tags.

<long-run-blocks>
### Worker Contracts (any delegated slice)
{slice}: role {one line}; workspace {absolute path}; one bounded deliverable {artifact}; returns {artifacts + report: files written, commands run with results, known problems}; claims {ids}; proof {program | reviewer | acceptance owner}; uses {earlier artifacts by path}; boundaries {write scope, tools, sources}; stops {done condition and finite run bound}
Launch a worker only when its input claims pass; verify its output before building on it; re-delegate a narrower recall instead of fixing it yourself.
Repair support: {reviser capability, tools and prompt support that meet Review and Repair in Plan parts | the exact gap that holds the repair}

### Portfolio (parallel search)
Families: {approach families grouped by underlying idea, not wording}
Independence: early workers do not see the favored approach; cross-pollinate after routes develop
Crowding: redirect workers from crowded families to underexplored ones
Allocation: vary effort with evidence; use no fixed strategy quota or default worker count
Rounds: preserve incompatible routes while viable; synthesize, challenge and open new rounds as evidence warrants
Blocked routes: {route}: stalled at {gap as hard as the goal}; reopen only for a materially new mechanism
Dominance: an elegant reduction that ends at a goal-strength subproblem is not progress

### Solvability (when framing is warranted; see Filling Notes)
{Assume a complete solution exists. | Either a complete solution or a complete demonstration of impossibility counts; nothing in between.}

### Effort (long runs with real abandonment risk)
Spend at least {floor} before considering return; new rounds and fresh formulations come before giving up. The floor never overrides a user stop, hard budget, or unavailable required evidence. An effort floor only removes permission to quit early.

### Contamination (when result independence matters)
External search only for {background}; never for {the answer or its benchmark}.
</long-run-blocks>

## Filling Notes

- **Contracts carry the task.** Keep roles to one line and spend words on what
  a slice returns and how it is checked, never on how to do the work.
- **Per-spawn spec.** Every delegated worker gets objective, output format,
  tool and source guidance, and boundaries; a worker sees only its prompt and
  the workspace.
- **Solvability is a scalpel.** Use "assume a solution exists" only when
  existence is plausible; on open or ill-posed questions use the two-sided form
  or a counterexample track, or the run will fabricate.
- **Floors are permissions.** A floor neither guarantees nor bounds runtime;
  the budget is re-injected from outside the loop with verified progress
  rather than stated once.

## Pre-Launch Check

Before launching a long or parallel run, judge the plan's readiness
([Plan parts](plan-parts.md#readiness)) and add the two lines below. For this
launch `sufficient` is not enough on readiness dimensions 2, 4, 8, 12 and 13
and on these two lines: each must be `strong`, which here means an adversary
cannot game it. Fix every one that is absent or present but gameable. Mark an
inapplicable line with its reason instead of forcing a block into a run that
does not need it.

- **Portfolio**: early independence, idea-keyed registry, blocked-route rule,
  late cross-pollination.
- **Contamination**: retrieval scope stated where independence matters.

For delegated runs also confirm: each worker contract names claims that
downstream work waits on; every part of the success sentence that a
command can decide is a program claim; and the plan meets each rule of
[Review and Repair](plan-parts.md#review-and-repair). Judge a plan across
several runs, never one.

## Run the authorized effort

When the user authorizes delivery, hand the same plan, tracker, current frontier,
effect scope, limits and evidence to [Orch](../../orch/SKILL.md). Its mode and
branch-authority rules still apply; planning grants no additional effects.
The controller coordinates these owners without asking the caller to move
between skills:

1. **Select.** Reload the bound tracker, plan, current source/dependency revisions
   and accepted evidence. Choose one coherent dependency-ready unit. Route an
   unresolved decision to its owner; continue other independent authorized work.
2. **Prepare.** For coding or a selected SDLC overlay, use lev-plan Emit and
   [Execution Packet](execution-packet.md) to create or refresh exactly one
   existing-contract task packet. Validate before dispatch. Reuse a current
   packet; regenerate stale inputs. Non-coding uses its domain execution
   contract without a mandatory SDLC packet.
3. **Execute, verify, accept.** Use [Exec](../../exec/SKILL.md) or the domain
   owner within the permitted scope. Record the actual worker handle and
   artifacts. Run the declared verifier, including known-bad sensitivity checks
   before relying on program checks. Accept only after each claim passes as the
   return gate of [Plan parts](plan-parts.md#return-and-resume) says. A
   dispatch, preview or worker report is not acceptance.
4. **Repair or advance.** Recall blocking failures to their responsible slice
   as [Review and Repair](plan-parts.md#review-and-repair) says.
   Preserve failed attempts. Invalidate affected downstream acceptance after a
   changed or failed input; unrelated ready branches can continue. Update the
   bound tracker through its owner and the plan's evidence/resume projection.
   Continue with the next ready unit only within the authorized scope and budget.

In the existing project report, summarize each actual worker call: handle,
role, bounded ask, artifact, status and independently verified evidence. For
parallel search only, Orch also maintains the idea-keyed approach registry,
falsified hypotheses, blocked routes and reopening evidence in the existing
acceptance map or its owner-managed state. The plan states the policy and
points to that state; it is not a second changing tracker.

## Return and resume across slices

The return gate and the stops that win over it are in
[Plan parts](plan-parts.md#return-and-resume). Across slices
it means: completing a slice advances the frontier; it does not complete the
effort. A branch's repair cap, missing authority or unavailable evidence holds
that branch and its affected consumers; continue independent authorized ready
work. Return the whole effort at a global user stop or exhausted budget, the
selected mode's boundary, or when no eligible work remains. If any required
branch is unresolved, label that return incomplete with the strongest verified
result, exact gaps and owners.
Do not turn an unavailable execution surface into a prose claim that the loop ran.

Save the last accepted slice and evidence, exact source/task/worker revisions,
open requirements and decisions, invalidated dependents, remaining limits and
one next ready unit in existing owner-managed state and its Markdown handoff.
On resume, recheck evidence freshness before choosing that unit. Runtime state
uses its existing JSON contract; no new parallel tracker or status file is added.
