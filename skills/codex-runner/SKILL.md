---
name: codex-runner
description: Dispatch Codex CLI (`codex exec`) as a trusted-local bounded background worker with isolated artifacts, explicit session resume, watchdog recovery, parallel exploration, controller verification, and merge-only landing. Use for implementation, fixes, refactors, exploration, review, or landing while Lev exec is unavailable or not yet the right runtime.
---

# Codex Runner

Treat `codex exec` like a subagent: send one bounded task, preserve its session
and artifacts, then verify its claims independently. This is a stopgap until
Lev exec owns the same lifecycle end to end.

Iron law: a worker's prose is a claim, not evidence.

## Route

- Use this skill only for trusted local repositories. The default launch is
  unsandboxed `--yolo`; use another runner for untrusted code.
- Use Lev exec when its profile and receipt path already cover the task. Do not
  rebuild Lev transport, receipts, or retry loops here.
- Use the isolated lazycodex/OmO home by default:
  `CODEX_HOME="${LAZYCODEX_HOME:-$HOME/.codex-lazycodex-trial}"`.
- Use raw `~/.codex` only when the isolated hooks or subagent fan-out would
  interfere with the task.
- Let `CODEX_HOME` or a Lev profile own model and reasoning policy. Add `-m`
  only for an explicit one-run user override.

## Prepare

Before launch:

1. Resolve the real repository root and inspect its instructions and status.
2. Create a unique task directory and write the frozen prompt to
   `<task-dir>/prompt.txt`.
3. Give the worker one outcome, an explicit write scope, hard constraints,
   verifier commands, and this final format: changed files; commands with exit
   codes; `DONE` or `CONTINUE` with exactly what remains.
4. Record the pre-run diff/status so controller verification can distinguish
   worker changes from existing user work.
5. Tell the worker it must never `git stash` or `git stash pop`: the checkout
   is shared with other sessions and lanes, and a stash reverts their files
   mid-run. Compare against HEAD with `git diff` or `git show HEAD:path`.

## Launch

Run from the repository root. Use `command codex` to bypass shell aliases,
`--yolo` for the trusted-local worker, and `--disable fast_mode` because this
runner's policy keeps fast mode off.

```bash
runner_repo=/absolute/repository/root
runner_task_dir="$(mktemp -d "${TMPDIR:-/tmp}/codex-runner.XXXXXX")"
runner_home="${LAZYCODEX_HOME:-$HOME/.codex-lazycodex-trial}"

(
  cd "$runner_repo"
  CODEX_HOME="$runner_home" command codex exec \
    --yolo \
    --disable fast_mode \
    -C "$runner_repo" \
    --json \
    --output-last-message "$runner_task_dir/last.txt" \
    "$(cat "$runner_task_dir/prompt.txt")" \
    </dev/null \
    >"$runner_task_dir/events.jsonl" \
    2>"$runner_task_dir/stderr.log"
) &
runner_pid=$!
```

Keep stdin closed for every background run. Keep JSONL events, stderr, and the
final message in separate files; progress chatter is not the return value.

## Preserve and Resume the Session

Extract the first `thread.started.thread_id` from `events.jsonl` as soon as it
appears and save it with the task artifacts. Never use `--last`: parallel runs
make it race-prone.

Resume an interrupted or incomplete worker from the same repository root with
the explicit thread ID. `resume` has no `-C`, and its documented bypass flag is
the long form:

```bash
cd "$runner_repo"
CODEX_HOME="$runner_home" command codex exec resume \
  --dangerously-bypass-approvals-and-sandbox \
  --disable fast_mode \
  --json \
  --output-last-message "$runner_task_dir/resume-last.txt" \
  "$runner_thread_id" \
  "$(cat "$runner_task_dir/resume-prompt.txt")" \
  </dev/null \
  >"$runner_task_dir/resume-events.jsonl" \
  2>"$runner_task_dir/resume-stderr.log"
```

Resume with the smallest useful correction or remaining slice. Do not restate
the full task or start a replacement session.

## Watchdog and Recovery

- Poll the recorded PID and artifact growth at least once per minute. Read the
  latest JSONL event and stderr before deciding a worker is stuck.
- No growth across two checks is a diagnostic trigger, not proof of failure.
  Inspect the process; do not launch a duplicate worker.
- If the process exited, harvest its exit status and artifacts. If it is truly
  wedged, terminate only that recorded PID, then resume the explicit thread.
- Stop after the same blocker occurs twice, a declared gate fails, or the run
  is a no-op. Report the command, exit status, and stderr artifact.

## Parallel Exploration

Parallelize only independent discovery or review lanes. Give every lane a
non-overlapping scope and its own task directory, prompt, event stream, stderr,
final message, PID, and thread ID. Exploration lanes are read-only. Never share
artifact paths and never resume by recency.

## Verify and Land

1. Harvest the final-message file; do not infer success from process exit `0`.
2. Inspect the actual diff and replay every claimed verifier from the
   controller shell.
3. Review the diff for scope creep, weakened tests, wrong-home fixes, and
   unverified claims before authorizing landing.
4. The controller retains landing authorization, pre-land gates, and final
   review. A worker may perform landing mechanics only after that authorization.
5. Once authorized, the worker may stage, commit, merge, resolve merge
   conflicts, and run the repository-native land command. Never rebase. Never
   run `git rebase` or `git pull --rebase`; when freshness is required, merge
   the target branch without rewriting history. Re-run gates after the merge.

## Fixed Policy

- Trusted local launch: `--yolo`.
- Resume: `--dangerously-bypass-approvals-and-sandbox` with an explicit thread.
- Fast mode: always disabled with `--disable fast_mode`.
- Current isolated default: `gpt-5.6-sol` with
  `model_reasoning_effort = "high"`; change the effective `CODEX_HOME` config,
  not each dispatch.
- Auth lives in `<CODEX_HOME>/auth.json`; diagnose that isolated copy when a
  worker reports token invalidation.
