# Long-Run Blocks and Pre-Launch Score

Load from `horizon` whenever any stage is delegated to a worker, including a
bounded sequential chain, and when a run needs a portfolio, solvability,
effort, or contamination block or an existing brief is scored before launch. A
delegated bounded run uses only Worker Contracts and the per-spawn guidance;
Portfolio, Solvability, Effort, and Contamination stay conditional on the run
needing them; a bounded run still takes contamination guards when independence
matters. A long or parallel brief always loads the Pre-Launch Score. Core blocks,
review, return, and the ledger stay in
[`../SKILL.md`](../SKILL.md); packet mechanics stay in
[Execution Packet](../../lev-plan/references/execution-packet.md).

## Long-Run Blocks

Append only the blocks the run needs to the `horizon-brief`, inside the same
wrapper. Render the Markdown; do not print the tags.

<horizon-long-run>
### Portfolio (parallel search)
Families: {approach families grouped by underlying idea, not wording}
Independence: early workers do not see the favored approach; cross-pollinate after routes develop
Crowding: redirect workers from crowded families to underexplored ones
Allocation: vary effort with evidence; use no fixed strategy quota or default worker count
Rounds: preserve incompatible routes while viable; synthesize, challenge and open new rounds as evidence warrants
Blocked routes: {route}: stalled at {gap as hard as the goal}; reopen only for a materially new mechanism
Dominance: an elegant reduction that ends at a goal-strength subproblem is not progress

### Worker Contracts (any delegated stage)
{stage}: role {one line}; workspace {absolute path}; one bounded deliverable {artifact}; returns {artifacts + report: files written, commands run with results, known problems}; rows {ids}; proof {command row | reviewer | acceptance owner}; uses {earlier artifacts by path}; boundaries {write scope, tools, sources}; stops {done condition and finite run bound}
Launch a worker only when its input rows pass; verify its output before building on it; re-delegate a narrower recall instead of fixing it yourself.
Repair support: reviser capability, tools and task-specific prompt support suitable for the findings and comparable to the reviewer; otherwise hold the repair with the exact gap. This grants no model, account or permission change.

### Solvability (when framing is warranted; see Filling Notes)
{Assume a complete solution exists. | Either a complete solution or a complete demonstration of impossibility counts; nothing in between.}

### Effort (long runs with real abandonment risk)
Spend at least {floor} before considering return; new rounds and fresh formulations come before giving up. The floor never overrides a user stop, hard budget, or unavailable required evidence.

### Contamination (when result independence matters)
External search only for {background}; never for {the answer or its benchmark}.
</horizon-long-run>

## Filling Notes

- **Contracts carry the task.** Keep roles to one line and spend words on what
  a stage returns and how it is checked, never on how to do the work.
- **Per-spawn spec.** Every delegated worker gets objective, output format,
  tool and source guidance, and boundaries; a worker sees only its prompt and
  the workspace.
- **Solvability is a scalpel.** Use "assume a solution exists" only when
  existence is plausible; on open or ill-posed questions use the two-sided form
  or a counterexample track, or the run will fabricate.
- **Floors are permissions.** A floor neither guarantees nor bounds runtime;
  budgets stay with the operator and runtime, re-injected from outside the
  loop with verified progress rather than stated once.
- **Contamination guards** belong wherever result independence matters.

## Pre-Launch Score

Score each line 0 (absent), 1 (present but gameable), or 2 (adversary-proof).
Fix every applicable 0 and 1 before launching a long or parallel run; mark an
inapplicable dimension with its reason instead of forcing a portfolio or
contamination block into a run that does not need it.

| # | Dimension | 2 means |
|---|---|---|
| 1 | Success predicate | An adversarial reader decides pass or fail unambiguously; quantifiers and scope explicit |
| 2 | Definitions | Load-bearing terms defined, degenerate cases settled |
| 3 | Does Not Count | This problem's plausible near misses excluded by name |
| 4 | Checklist | Domain failure modes, circularity analogue, degenerate values |
| 5 | Persistence pairing | Every persistence instruction has a matching return gate |
| 6 | Return | Predicate over the artifact; incomplete return only on user stop, hard budget, or unavailable evidence |
| 7 | Portfolio | Early independence, idea-keyed registry, blocked-route rule, late cross-pollination |
| 8 | Reporting | Artifacts and evidence produced after the last edit; status lines rejected |
| 9 | Contamination | Retrieval scope stated where independence matters |
| 10 | Limits outside the prose | Budgets, permissions, and stops enforced by operator or runtime |

For delegated runs also confirm: each worker contract names rows that
downstream work waits on; every mechanically decidable part of the predicate is
a command check; blocking conditions and recall caps are stated; the reviser
gets as much context as the reviewer; and decisive claims carry credible proof
from outside the model loop (a command row where a command decides, otherwise
named independent evidence or human review with its acceptance owner), with
unresolved proof listed rather than filled by a weak command. Judge a brief
across several runs, never one.
