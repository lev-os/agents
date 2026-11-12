# Hostile run

The attacker stance on running behaviour: a bounded cycle that runs the target, attacks it with hostile end-to-end
scenarios, and returns observations and repair requests. It replaces the `ultraqa` skill (JP 2026-11-12: "review
should absorb ultraqa"). It is advice like every review: the caller owns effects, fixes, state and the verdict.

## Contents

- [Who does what](#who-does-what)
- [Goal](#goal)
- [Scenario matrix](#scenario-matrix)
- [Harness rules](#harness-rules)
- [Cycle](#cycle)
- [Safety bounds](#safety-bounds)
- [Stops](#stops)
- [State](#state)
- [Report](#report)

## Who does what

- Build, lint, typecheck and test commands are evidence, never the whole run. The run must exercise the behaviour
  through hostile end-to-end scenarios whenever the target can be run, simulated or harnessed safely.
- Under `skill://exec`, Exec runs the commands, harnesses and cleanup and receives the repair requests. The run never
  routes back into Exec.
- On a direct request that needs a fix or a state change, route the repair once to `skill://exec`; add no new driver,
  CLI or plugin.
- On `continue`, advance the current verified next step; do not restart discovery. A newer user update changes only the
  branch it names.

## Goal

| Goal | Check |
|---|---|
| `--tests` | The test command, plus hostile e2e scenarios for the changed behaviour |
| `--build` | The build, plus smoke and e2e probes against the built artifact |
| `--lint` | Lint, and no generated harness breaks project hygiene |
| `--typecheck` | Typecheck, and generated typed harnesses compile |
| `--custom "pattern"` | The pattern, checked with the exit status and failure markers, never trusted alone |
| `--interactive` | A CLI or service driven with hostile and edge-case input |

With no goal type, treat the argument as a behaviour goal and derive a runnable e2e strategy from the project.

## Scenario matrix

Build the matrix before you run anything, and keep it current. Each row: id, intent, user or attacker model, setup,
command or harness, expected signal, actual result, fixes, evidence, cleanup status.

Cover the normal path, then each class below unless it is clearly irrelevant or impossible (say which and why):

1. **Malformed input**: invalid JSON, missing fields, bad flags, huge strings, unusual Unicode, path-traversal values,
   corrupt state files.
2. **Repeated interruptions**: repeated `continue`, stop or cancel wording, cut-off output, retry after partial
   progress.
3. **Prompt injection**: text that tries to override instructions, leak secrets, skip checks, delete state or claim
   false success.
4. **Cancel and resume**: state cleanup, resume detection, stale in-progress state, cancel then a fresh run.
5. **Stale state**: old state files, mismatched sessions, missing timestamps, contradictory phase data.
6. **Dirty worktree**: existing edits and untracked files; the run must not hide or overwrite unrelated work.
7. **Hung commands**: timeouts, killed child processes, recovery notes.
8. **Flaky tests**: rerun plan, failure clusters, quarantine evidence; one lucky pass is not green.
9. **Misleading success**: success words with a non-zero exit, hidden failures, skipped tests, partial logs.

## Harness rules

- Write a temporary test, script, fixture or harness only when it adds behavioural confidence and no existing e2e
  surface covers the scenario. Prefer project-native tools; put throwaway harnesses in a temporary folder or a clearly
  named fixture.
- Record every generated artifact in the matrix, and whether it was kept on purpose or removed.
- Give every command that can hang a timeout. Check exit codes and output meaning; success-looking text alone proves
  nothing.
- Capture worktree status before and after harness work.

## Cycle

At most 5 cycles. Each cycle:

1. **Plan.** Restate the goal, success criteria, safety bounds and stop. Find the runnable surfaces, test commands,
   state files and cleanup paths. The project's standards (from review's project-load step) apply; a broken rule is a
   finding. Update the matrix.
2. **Baseline.** Run the goal's command. For `--interactive`, drive an existing harness, or give a tester role the
   caller supports this brief: goal, how to start the service, and the test cases (normal plus every class above).
3. **Attack.** Run the matrix with existing e2e tests or generated harnesses. Model the hostile user on purpose. Capture
   commands, exit codes, key output, artifacts and cleanup status.
4. **Check.** Clean only when the baseline and every scenario passed, generated artifacts are removed or tracked on
   purpose, and the evidence is complete. A failed, unjustified-skip, debris-leaving, misleading-output or
   evidence-less scenario is not clean. A broken harness, missing dependency, port or tmux conflict, or hung command is a
   harness error, not a pass and not a product failure: repair the harness or stop with `HOSTILE RUN ERROR`.
5. **Diagnose.** Diagnose directly, or give a reviewer role the goal, the matrix rows, failures and output, and ask for
   root cause, safety impact and fix. A hash difference shows only different bytes; state order, actor, mechanism or
   cause only with its own evidence, else as a hypothesis with the check that would falsify it.
6. **Request repair.** One request per failing scenario: issue, files, constraints (keep unrelated dirty work, clean
   temporary harnesses, keep safety bounds). Under Exec, return it and stop; Exec decides and calls the run again with
   the cycle number and failure history. Re-observe only the exact revision the effect owner reports; older evidence is
   stale.
7. **Clean up.** Remove temporary harnesses, fixtures, logs, processes and state unless they are declared deliverables
   (under Exec, Exec removes them and the run checks). The effect owner rolls back failed experimental edits. Record the
   worktree after.

Print one progress line for each step, for example `[hostile run 1/5] FAILED ADV-003: resume accepted a misleading
success`. Run independent diagnostics in parallel; never parallelize commands that change the same state or worktree.

## Safety bounds

No force resets, broad deletes, secret reads beyond the metadata that proves no leak, credential dumps, production
writes, unbounded process spawns or unbounded waits. No network or production side effect without the user's explicit
permission. When a scenario needs one of these, mark it blocked and record the safe substitute you used.

## Stops

| Condition | Line |
|---|---|
| Matrix clean | `HOSTILE RUN COMPLETE: no open failure after N cycles` |
| Cycle 5 reached | `HOSTILE RUN STOPPED: max cycles`, with failures, fixes tried, residual risk |
| Same failure 3 times | `HOSTILE RUN STOPPED: same failure 3 times`, with root cause and next owner |
| Safety bound | `HOSTILE RUN BLOCKED: <the action>`, with the safe substitute's evidence |
| Environment error | `HOSTILE RUN ERROR: <tmux, port, dependency or hung command>`, with cleanup status |

Each line is an observation for the caller. Acceptance stays with the caller, Exec and the project's checker (in
Leviathan, `core/eval`). A user cancel stops the run at the next boundary; report cleanup status.

## State

The run owns no lifecycle state and issues no host state commands. It returns the fields the caller records:
`active`, `current_phase` (`planning`, `qa`, `adversarial-e2e`, `diagnose`, `fix`, `cleanup`, `complete`),
`iteration`, `started_at`, `completed_at`, `scenario_matrix`, and `mode_relationship`:

- `child`: verifying work for an active parent mode; add `parent_mode` and `parent_session_id` when known; leave the
  parent state alone.
- `parallel`: independent, same repo; keep dirty-worktree evidence in the matrix.
- `conflict`: it would change the same state file, process or artifact as another active mode; return
  `overlap_blocked: true`, `conflict_mode`, `conflict_resource` and
  `next_route: retry_with_child_state_or_cancel_parent`.
- `root`: no relevant parent mode.

Resume from the caller's record and the last report. On any stop, return a cleanup request for the run's record only;
the caller clears it through its own state path. Clear another mode's state only when the user cancels that mode.

## Report

Every stop carries this report, under review's typed first line. Each finding in it is labelled `advice`.

<hostile-run-report>
## Hostile run report

**Goal:** {goal} · **Stop:** {stop line} · **Safety bounds:** {applied}

| ID | User or attacker model | Scenario | Command or harness | Expected | Actual | Status | Evidence | Cleanup |
|---|---|---|---|---|---|---|---|---|

**Commands run:** `[exit] command`: purpose, timeout, key output.
**Failures:** scenario id, signal, cause with evidence or a labelled hypothesis, user impact, safety impact.
**Repairs:** request, effect owner, files, revision re-observed, linked scenarios, regression evidence.
**Cleanup:** artifacts removed or kept, state and processes cleared, worktree before and after.
**Residual risk:** untested or blocked scenarios, with reason and safe substitute.
</hostile-run-report>
