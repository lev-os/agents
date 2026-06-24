---
name: codex-runner
description: Use when dispatching Codex CLI (`codex exec`) as a bounded background worker with subagent ergonomics — fire a scoped prompt, harvest the final message, verify independently before reporting.
skill_type: workflow
category: execution
output_template: hud
---

# /codex-runner - Codex CLI as a Bounded Worker

`codex exec` is a non-interactive one-shot agent run. Treat it exactly like a
subagent dispatch: bounded prompt in, final message out, controller verifies.
The default worker harness is **lazycodex/OmO** via an isolated `CODEX_HOME` —
it adds discipline the raw CLI lacks: explorer/planner subagent fan-out, a
notepad bootstrap that pins acceptance criteria before work starts, and a
momus/reviewer pass that rejects weak evidence before the worker may report
DONE.

Iron Law: **a worker's prose is a claim, not evidence.** Replay the declared
verifier yourself before reporting any result as done — even after the OmO
reviewer approves.

## Surface Selection

- Inside a Lev project: prefer `lev exec --profile=<id>` — it adds transport,
  receipts, per-iteration gate proofs, and `--until`/`--verifier` loops. See
  `/exec`. Exec profiles are the ONLY model/policy brain.
- Default standalone worker: lazycodex/OmO home —
  `CODEX_HOME="${LAZYCODEX_HOME:-$HOME/.codex-lazycodex-trial}"`. Use it when
  no Lev runtime exists in the target repo or you need a single bounded worker
  outside the receipt pipeline.
- Drop to raw `codex exec` (default `~/.codex`) only when the OmO hooks or
  subagent fan-out would interfere (e.g. measuring the bare model, or token
  budget is tight — OmO costs more per run).
- Never use `codex -p <overlay>` to carry policy for Lev work — that is a
  split-brain with exec profiles. Profile-v2 overlays are for raw interactive
  sessions only.

## Dispatch Protocol (subagent ergonomics)

1. **Write the prompt to a file** — avoids shell-quoting corruption:
   `/tmp/<task-id>-prompt.md`.
2. **Launch in the background** from the repo root:

   ```bash
   CODEX_HOME="${LAZYCODEX_HOME:-$HOME/.codex-lazycodex-trial}" codex exec \
     -s workspace-write \
     --output-last-message /tmp/<task-id>-last.txt \
     "$(cat /tmp/<task-id>-prompt.md)" < /dev/null
   ```

   - `< /dev/null` is MANDATORY for background runs. A backgrounded codex
     inherits a non-TTY stdin with no EOF and blocks forever on
     "Reading additional input from stdin..." — looks launched, does nothing.
   - Use `-s workspace-write` for ordinary code-mutating workers. For trusted
     local macOS workers that must run canonical `uv` verifiers, use
     `-s danger-full-access`: Codex `workspace-write` can make `uv` fail before
     Python starts with `~/.cache/uv` permission errors or a
     `system-configuration` panic. Keep the prompt write scope bounded and the
     controller replay mandatory.
   - If a worker was already launched under `workspace-write` and `uv` fails
     before invoking Python, the worker may run the equivalent
     `.venv/bin/python -m ...` verifier as a local fallback. Report both the
     failed `uv` command and the fallback command. The controller still reruns
     the canonical `uv` gate where its shell permits it.
   - Auth lives in `<CODEX_HOME>/auth.json`. A managed/trial home holds its OWN
     copy, so a token rotation in `~/.codex` staleds it → `401 token
     invalidated`. Refresh: `cp ~/.codex/auth.json <CODEX_HOME>/auth.json`.

   When dispatching the REVIEW lane through `lev exec` instead of raw codex,
   the prompt cannot be a bare argv positional — `lev exec` rejects a
   multiline/>2KiB positional. Use `lev exec --prompt-file=<path>
   --profile=<reviewer> --until=... --verifier=... < /dev/null`.

3. **Harvest** `--output-last-message` — that file IS the subagent return
   value. Do not parse progress chatter.
4. **Verify independently**: re-run the worker's claimed commands, inspect the
   diff, then stage files yourself.

## Prompt Contract

Every dispatch prompt must declare, like a subagent brief:

- The bounded task (one slice; domain outcome, not workflow mechanics).
- Hard constraints and explicit write scope (paths the worker may touch).
- Verification commands the worker must run, with exit codes reported.
- Final message format: files created, commands + exit codes, then `DONE` or
  `CONTINUE` + exactly what remains.
- If the worker's harness has subagents (multi_agent enabled), say when to fan
  out (inventory/review), not whether it may.

## Flags That Matter

| Flag | Role |
|---|---|
| `--output-last-message <file>` | the return value — always set it |
| `-c key=value` | config override (`model_reasoning_effort`, feature toggles) |
| `-s <mode>` | sandbox mode; use `danger-full-access` only for trusted local workers that must run `uv` |
| `--json` | JSONL event stream for machine harvesting |
| `--cd <dir>` | working directory |
| `-m <model>` | ONLY on an explicit current-run user override |
| `CODEX_HOME=<dir>` env | isolated config/harness (sandboxed trials) |

Model policy follows `/goal-exec`: never hardcode a model in this skill or a
goal prompt. The `CODEX_HOME` config or the Lev exec profile carries
adapter/model/effort policy.

## Sandbox Rules

- Default `-s workspace-write`.
- Trusted local macOS exception: if the worker must run `uv`, use
  `-s danger-full-access` at launch. Do not use this exception for untrusted
  repositories, remote checkouts, or broad exploratory workers. It only changes
  the OS sandbox needed for `uv`; it does not relax the prompt's write scope,
  proof duties, or controller verification.
- Known gotcha: if the repo is reached via a symlink, the git index can resolve
  outside the writable root and the worker's `git add` fails silently-late.
  The controller stages files after harvest — always.
- Stage new files immediately after harvest; untracked files in synced trees
  can be wiped by background tooling.

## Guardrails (from /goal-exec)

- One slice per dispatch. The goal is the domain outcome; codex is a `Tools:`
  clause.
- Stop on: same blocker twice, no-op result, or a failed declared gate. Report
  diagnostics (command, exit code, stderr path); do not silently retry.
- Reviewer-shaped dispatches must emit machine-checkable
  `VERDICT <id>: PASS|FAIL` lines so a grep can gate them — never prose
  approval.

## Red Flags

- "The worker said DONE, so it's done."
- "I'll pass the prompt inline; quoting is probably fine."
- "danger-full-access is okay without a trusted local `uv` verifier need."
- "The worker already staged/committed its files."
- "I'll hardcode the model so it's reproducible."

## Rationalization Table

| Excuse | Reality |
|---|---|
| "Exit 0 means the work is correct." | Exit 0 means the process ended. Replay the verifier. |
| "Its final summary lists green tests." | Prose. Re-run the commands yourself. |
| "Profile-v2 keeps codex settings tidy." | Split-brain. Exec profiles / CODEX_HOME config own policy. |
| "One big prompt can do all slices." | One slice per dispatch; loops belong to `lev exec --until`. |

## Related

- `/exec` — Lev exec lane (preferred inside Lev projects).
- `/goal-exec` — goal prompt shape for exec work.
- `$subagent-driven-development` — same controller contract, Claude-native lane.
