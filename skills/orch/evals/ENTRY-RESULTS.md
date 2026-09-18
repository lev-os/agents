# Historical entry-mode evaluation: rejected

Current disposition: the user rejected rollback. The intended modes remain
installed, and g019 passed all 18 live sandbox cases plus 33 local tests after
forward iteration. This document records the previous failed campaign, not the
current qualification. See FEEDBACK-ITERATIONS.yaml and
runs/feedback-current-summary.json for current evidence and scope.

Exactly 20 new Claude Haiku 4.5 launches ran after the entry-mode update.
All ran in the restricted three-tool MCP fixture environment; no additional
model calls were made after the cap. The counter is shared across revisions.

| Candidate | Runs | Pass | Fail |
|---|---:|---:|---:|
| g006, first bare/auto smoke | 2 | 1 | 1 |
| g007, strengthened verifier wording | 18 | 6 | 12 |
| Total | 20 | 7 | 13 |

The eight invocation cases cover bare discovery, auto goal creation, until-human
goal reuse and immediate dependent progress, once, watch reuse, unavailable
watch capability, conflicting modes, and new watch creation. The final revision
also ran all ten existing core scenarios once. Only those named fixtures and
effects were tested; no universal or production-scheduler claim is supported.

## Observed failures

- Auto ran and accepted jobs without invoking their declared verifiers.
- Bare discovery produced an incomplete report/recommendation contract.
- Once omitted its verifier/report obligations.
- Until-human skipped inspection of the existing goal.
- Watch dispatched a job already marked running.
- Missing watch capability and conflicting mode controls did not stop effects.
- The expanded candidate also regressed four existing core cases.

## Disposition

At this historical checkpoint, the mode candidate was not promoted and SKILL.md was restored to the exact
g005 digest 3bac1540e6a7d5fff49300f29a8179d16438f6df258d6be582350cf1a7169e70.
Its earlier 20/20 result remains limited to its earlier core test environment;
it does not imply that the proposed invocation modes work.

The full failed candidate is preserved in
../references/invocation-controls.candidate.md. Every run, command, prompt,
model/session identity, actual tool stream, output and controller verdict is
indexed in runs/entry-mode-summary.json. The tested evaluator snapshot in
runs/e005/run_trials.py matches the digest recorded by all twenty runs.

The queued matrix had consumed all 20 reservations before the controller added
the fail-before-next-launch guard. That guard now prevents another same-revision
launch after a failed result; it did not improve this campaign's results.

## Recommended next iteration

Keep the proven execution loop compact. Resolve invocation modes in a small
deterministic startup adapter that returns the selected mode, action limit,
goal policy and watch policy, rather than asking a larger prompt to enforce
every distinction. Keep actual effect and verifier checks in the execution
owner. Then re-run the same frozen invocation fixtures and core regressions
under a newly authorized run budget. Do not call that next design implemented
or qualified: this campaign produced evidence and a rejection, not a working
entry-mode release. No FlowMind evaluator changes were made.
