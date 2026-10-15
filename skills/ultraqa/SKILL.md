---
name: ultraqa
description: "Use when adversarially reviewing behavior with dynamic e2e evidence: hostile scenario matrices, misleading-success and harness-error checks, bounded QA cycles, cleanup evidence, and repair requests returned to the caller."
---

# UltraQA Skill

## Operating Contract

- Use outcome-first framing with concise, evidence-dense progress and completion reporting.
- Treat newer user updates as local overrides for the active workflow branch while preserving earlier non-conflicting constraints.
- If the user says `continue`, advance the current verified next step instead of restarting discovery.
- UltraQA is not satisfied by a shallow build/lint/typecheck/test checklist. It must exercise the requested behavior through adversarial dynamic e2e scenarios whenever the target can be run, simulated, or harnessed safely.
- UltraQA is an adversarial review and evidence method: it designs scenarios, observes behavior, classifies results, and returns observations plus repair requests. The caller owns effects, fixes, lifecycle state, and verdicts.
- Under `/exec`, Exec runs the commands, harnesses, and cleanup and receives the repair requests; UltraQA never routes back into Exec. On a direct user request that needs a fix or state change, route it once to the existing `skill://exec` (step 6), with no new driver, CLI, or plugin.

[ULTRAQA ACTIVATED - ADVERSARIAL DYNAMIC E2E QA CYCLING]

## Overview

UltraQA finds real behavior failures by combining normal verification commands with generated end-to-end scenarios, hostile user modeling, temporary harnesses when useful, and a structured evidence report. The workflow repeats observe → diagnose → request repair → re-observe the repaired revision until the goal is met, a bounded stop condition is reached, or a safety boundary blocks further execution. UltraQA originated as an OMX workflow; this generalized method keeps its scenario, cleanup, and stop discipline on any host.

## Goal Parsing

Parse the goal from arguments. Supported formats:

| Invocation | Goal Type | What to Check |
|------------|-----------|---------------|
| `/ultraqa --tests` | tests | Existing tests plus adversarial dynamic e2e scenarios for the changed behavior |
| `/ultraqa --build` | build | Build succeeds and generated smoke/e2e probes still run against the built artifact when applicable |
| `/ultraqa --lint` | lint | Lint passes and no generated harness/test artifact violates project hygiene |
| `/ultraqa --typecheck` | typecheck | Typecheck passes and generated typed harnesses compile when applicable |
| `/ultraqa --custom "pattern"` | custom | Custom success pattern is verified against behavior, not trusted as misleading success output |
| `/ultraqa --interactive` | interactive | CLI/service behavior is tested with generated hostile and edge-case interactions |

If no structured goal is provided, interpret the argument as a custom behavior goal and derive a runnable e2e strategy from repository context.

## Required Scenario Matrix

Before declaring success, create and maintain a scenario matrix. Each row must include: scenario id, intent, user/attacker model, setup, command or harness, expected signal, actual result, fixes applied, evidence, and cleanup status.

The matrix must include normal-path coverage plus adversarial dynamic e2e scenarios selected from the current goal and codebase. Unless clearly irrelevant or impossible, include these hostile and edge-case classes:

1. **Malformed input**: invalid JSON, missing fields, invalid flags, oversized strings, unusual Unicode, path traversal-like values, and corrupted state files.
2. **Repeated interruptions**: repeated `continue`, stop/cancel/abort wording, interrupted command output, and retries after partial progress.
3. **Prompt injection attempts**: user text that tries to override instructions, exfiltrate secrets, skip verification, delete state, or claim false success.
4. **Cancel/resume behavior**: active state cleanup, resume detection, stale in-progress state, and cancellation followed by a fresh run.
5. **Stale state**: old `.omx/state` files, mismatched sessions, missing timestamps, and contradictory phase metadata.
6. **Dirty worktree**: pre-existing modifications, untracked generated files, and verification that UltraQA does not hide or overwrite unrelated work.
7. **Hung or long-running commands**: bounded timeout handling, killed child processes, and recovery notes.
8. **Flaky tests**: rerun strategy, failure clustering, quarantine evidence, and avoiding false green from a single lucky pass.
9. **Misleading success output**: output containing success phrases with non-zero exits, hidden failures, skipped tests, or partial command logs.

## Dynamic E2E and Temporary Harness Rules

- Generate temporary tests, scripts, fixtures, or harnesses when they materially improve behavioral confidence and no existing e2e surface covers the scenario.
- Prefer project-native test tools and small throwaway harnesses under a temporary directory or clearly named test fixture.
- Record every generated artifact in the scenario matrix, including whether it was committed intentionally or removed during cleanup.
- Use bounded runtimes and explicit timeouts for commands that can hang.
- Validate exit codes and output semantics; do not trust success-looking text alone.
- Do not delete, rewrite, or mask unrelated user work. Capture dirty-worktree evidence before and after generated harness work.

## Cycle Workflow

### Cycle N (Max 5)

1. **PLAN ADVERSARIAL QA**
   - Restate the goal, success criteria, safety bounds, and stop condition.
   - Inspect repository context enough to identify runnable surfaces, test commands, state files, and cleanup paths.
   - Build or update the required scenario matrix before running commands.

2. **RUN BASELINE VERIFICATION**
   - `--tests`: Run the project's test command.
   - `--build`: Run the project's build command.
   - `--lint`: Run the project's lint command.
   - `--typecheck`: Run the project's type check command.
   - `--custom`: Run the appropriate command and check the pattern plus exit status and failure markers.
   - `--interactive`: drive the CLI/service through an existing harness, or delegate to a QA/tester role the caller or provider currently supports; otherwise request a harness from the caller. Give it:
     ```
     Goal: [describe what to verify]
     Service: [how to start]
     Test cases: [normal, hostile, malformed, interruption, resume, stale-state, dirty-worktree, hung-command, flaky, and misleading-output scenarios]
     ```

3. **RUN ADVERSARIAL DYNAMIC E2E SCENARIOS**
   - Execute the scenario matrix using existing e2e tests, generated temporary tests, or generated harnesses.
   - Model malicious/hostile user behavior explicitly, including prompt injection and attempts to bypass safety or verification.
   - Exercise malformed input, repeated interruptions, cancel/resume, stale state, dirty worktree handling, hung commands, flaky tests, and misleading success output when relevant.
   - Capture commands, exit codes, important output excerpts, artifacts, and cleanup status.

4. **CHECK RESULT**
   - **YES** only if baseline verification and adversarial e2e scenarios passed, generated artifacts are cleaned up or intentionally tracked, and the report has complete evidence.
   - **NO** if any scenario failed, was skipped without justification, left debris, relied on misleading output, or lacked evidence. Continue to step 5.
   - Classify a broken harness, missing dependency, port/tmux conflict, or hung command as a harness error, not a pass or product failure; repair the harness or exit with `ULTRAQA ERROR`.
   - YES is an observation returned to the caller, not a canonical completion verdict.

5. **ARCHITECT DIAGNOSIS**
   Diagnose directly, or delegate to an architect/reviewer role the caller or provider currently supports, with:
   ```
   Goal: [goal type and behavior]
   Scenario matrix: [rows, commands, failures, evidence]
   Output: [test/build/e2e/harness output]
   Provide root cause, safety implications, and specific fix recommendations. A hash
   difference shows only different bytes; state chronology, actor, mechanism or cause
   only with its own evidence, otherwise as a hypothesis with its falsifying check.
   ```

6. **REQUEST REPAIR**
   - Emit one repair request per failing scenario:
   ```
   Issue: [architect diagnosis]
   Files: [affected files]
   Constraints: preserve unrelated dirty work, clean temporary harnesses, keep safety bounds
   Apply the fix precisely as recommended.
   ```
   - Under Exec, return it to Exec and stop; Exec decides whether to apply it and re-invokes this method with the cycle number and failure history.
   - On direct invocation, route it once to `skill://exec`.
   - Re-observe only the exact revision the effect owner reports; evidence from earlier revisions is stale.

7. **CLEAN UP AND ROLLBACK**
   - Remove temporary harnesses, fixtures, logs, spawned processes, and state files unless they are intentional deliverables; under Exec, Exec performs this cleanup and UltraQA verifies it.
   - Have the effect owner roll back failed experimental edits that are not part of the final fix.
   - Re-check the worktree and record cleanup evidence: remaining intentional changes or residual debris.

8. **REPEAT**
   - Go back to step 1 with the updated scenario matrix and failure history.

## Safety Bounds

UltraQA must stay inside these safety bounds:

- No destructive commands such as force resets, broad deletes, secret exfiltration, credential dumping, production writes, or unbounded process spawning.
- No reading or printing secrets beyond the minimum metadata needed to verify absence of leakage.
- No network or external-production side effects unless the user explicitly authorized them.
- No unbounded waits: use timeouts, retries with caps, and clear hung-command diagnostics.
- No hiding unrelated dirty work or generated debris.
- If a required scenario would violate these bounds, mark it blocked in the report with the safe substitute used.

## Exit Conditions

| Condition | Action |
|-----------|--------|
| **Goal Met** | Exit with success: `ULTRAQA COMPLETE: Goal met after N cycles` plus the structured report |
| **Cycle 5 Reached** | Exit with diagnosis: `ULTRAQA STOPPED: Max cycles` plus failures, fixes attempted, residual risks, and evidence |
| **Same Failure 3x** | Exit early: `ULTRAQA STOPPED: Same failure detected 3 times` plus root cause, safety notes, and next owner |
| **Safety Boundary** | Exit: `ULTRAQA BLOCKED: [destructive/credentialed/external-production/unbounded action]` plus safe substitute evidence |
| **Environment Error** | Exit: `ULTRAQA ERROR: [tmux/port/dependency/hung command issue]` plus cleanup status |

Each label is a method observation returned to the caller. `ULTRAQA COMPLETE` means this run's matrix observed no open failure; acceptance and completion status stay with the caller, Exec, and `core/eval`.

## Structured Report

Every terminal UltraQA result must include this report shape:

```markdown
# UltraQA Report

## Goal and success criteria
- Goal:
- Stop condition:
- Safety bounds applied:

## Scenario matrix
| ID | User/attacker model | Scenario | Command/harness | Expected signal | Actual result | Status | Evidence | Cleanup |
|----|---------------------|----------|-----------------|-----------------|---------------|--------|----------|---------|

## Commands run
- `[exit code] command` — purpose, duration/timeout, key output evidence

## Failures found
- Scenario ID, failure signal, evidenced root cause or labeled hypothesis, user impact, safety impact

## Fixes applied
- Repair request, effect owner, files changed, revision re-observed, rationale, linked failing scenario(s), regression evidence

## Cleanup and rollback
- Generated artifacts removed or intentionally kept
- State/process cleanup performed
- Worktree status before/after

## Residual risks
- Untested or blocked scenarios with reasons and safe substitutes

## Evidence
- Test output, e2e logs, harness output, screenshots/transcripts when relevant, and rerun/flake evidence
```

## Observability

Output progress each cycle:

```text
[ULTRAQA Cycle 1/5] Planning adversarial scenario matrix...
[ULTRAQA Cycle 1/5] Running baseline tests...
[ULTRAQA Cycle 1/5] Running ADV-E2E-003 prompt-injection harness...
[ULTRAQA Cycle 1/5] FAILED - stale state resume accepted misleading success output
[ULTRAQA Cycle 1/5] Architect diagnosing scenario ADV-E2E-003...
[ULTRAQA Cycle 1/5] Repair requested: src/hooks/... - validate exit code before success phrase
[ULTRAQA Cycle 1/5] Cleaning temporary harnesses and state...
[ULTRAQA Cycle 2/5] PASSED - baseline + 9 adversarial scenarios pass
[ULTRAQA COMPLETE] Goal met after 2 cycles
```

## State Tracking

UltraQA owns no lifecycle state and issues no `omx state` commands. The caller (Exec, or the host session on direct invocation) keeps the `ultraqa` mode record on its own state surface; UltraQA returns the fields that record needs: `active`, `current_phase` (`planning`, `qa`, `adversarial-e2e`, `diagnose`, `fix`, `cleanup`, `complete`), `iteration`, `started_at`/`completed_at`, `scenario_matrix`, and the relationship fields below. Resume from that record and the last report instead of restarting discovery.

### Mode State Relationship Policy

UltraQA may run while another workflow mode is active. Treat that as an explicit
state relationship, not as a reason to clear or overwrite parent state. Return
the matching fields for the caller to record.

- `child`: UltraQA is verifying work for an active parent mode. Record
  `mode_relationship:"child"`, `parent_mode`, and `parent_session_id` when
  those values are known. Keep the parent state intact.
- `parallel`: UltraQA is independent but shares the same repo. Record
  `mode_relationship:"parallel"` and keep dirty-worktree evidence in the
  scenario matrix.
- `conflict`: UltraQA would mutate the same state file, process, or artifact as
  another active mode. Return a structured non-fatal diagnostic with
  `overlap_blocked:true`, `conflict_mode`, `conflict_resource`, and
  `next_route:"retry_with_child_state_or_cancel_parent"`.
- `root`: No active parent mode is relevant. Record `mode_relationship:"root"`.

Never request clearing unrelated `.omx/state` mode files to make nested QA pass.
Cleanup requests cover only UltraQA state unless the user explicitly cancels
another mode.

## Scenario Examples

**Good:** The user says `continue` after the workflow already has a clear next step. Continue the current branch of work, rerun the relevant adversarial scenario, and update the report instead of restarting discovery.

**Good:** The user changes only the output shape or downstream delivery step (for example `make a PR`). Preserve earlier non-conflicting workflow constraints and apply the update locally.

**Good:** A CLI prints `SUCCESS` while exiting 1. Mark the misleading success output scenario failed, request a repair of the parser or reporting path, and rerun the generated harness on the repaired revision.

**Bad:** The workflow runs only `npm test`, `npm run build`, `npm run lint`, or `npm run typecheck`, sees green output, and declares UltraQA complete without adversarial dynamic e2e coverage.

**Bad:** A generated harness leaves untracked files, state, or a child process behind and the final report omits cleanup status.

**Bad:** The user says `continue`, and the workflow restarts discovery or stops before the missing verification/evidence is gathered.

## Cancellation

User can cancel with `/cancel`; the caller or host clears the UltraQA record. Cancellation itself should be tested in cancel/resume scenarios when relevant, but UltraQA must not block an explicit user cancellation; it stops at the next boundary and reports cleanup status.

## Important Rules

1. **ADVERSARIAL E2E REQUIRED** - Baseline build/lint/typecheck/test commands are necessary evidence, not sufficient completion proof.
2. **SCENARIO MATRIX REQUIRED** - Track normal, hostile, malformed, interruption, injection, cancel/resume, stale-state, dirty-worktree, hung-command, flaky, and misleading-output coverage.
3. **GENERATE HARNESSES WHEN USEFUL** - Create temporary tests or harnesses when they materially improve behavioral confidence, then clean them up or hand them to the effect owner as declared deliverables.
4. **PARALLEL WHEN SAFE** - Run independent diagnostics while preparing potential fixes; do not parallelize commands that mutate the same state or worktree.
5. **TRACK FAILURES** - Record each failure to detect patterns and avoid false greens.
6. **EARLY EXIT ON PATTERN** - 3x same failure = stop and surface with root cause and residual risk.
7. **CLEAR OUTPUT** - User should always know current cycle, scenario, command, status, and evidence.
8. **CLEAN UP** - Request clearing of UltraQA state and remove temporary artifacts on completion, cancellation, or early stop; report cleanup evidence.
9. **SAFETY FIRST** - Never exfiltrate secrets, run destructive cleanup, write to production, or wait indefinitely to satisfy a scenario.

## STATE CLEANUP ON COMPLETION

When goal is met OR max cycles reached OR exiting early, return a cleanup request for the UltraQA mode record; the caller or host clears it through its own state path (for an OMX host, `$cancel`) rather than deleting files directly. Also remove temporary e2e harnesses, fixtures, and logs unless they are intentional artifacts listed in the report, and record the result.

---

Begin ULTRAQA cycling now. Parse the goal, identify the caller that owns effects, build the adversarial dynamic e2e scenario matrix, and start cycle 1.
