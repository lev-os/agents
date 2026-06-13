---
name: exec
description: Use when running execution-ready task slices, dispatching verified `lev exec` flows, or reviewing implementation work in the Exec lane.
skill_type: workflow
category: lifecycle
output_template: hud
---

# /exec - Exec Lane

`/exec` runs execution-ready entities. It does not invent plans, weaken
verifiers, or complete work without review evidence.

## Goal Prompt Discipline

When a user asks to set a goal involving `/exec`, the goal objective must be the
domain task. Name `/exec`, Lev, Ralph, profiles, or runtime surfaces only as
bounded tools/surfaces.

Bad goal objective:
- "Execute all slices through the exec lane, validate readiness, collect
  receipts, route blockers, and close with verified status."

Good goal objective:
- "COPI cutover. Tools: `/exec`/Lev Ralph as bounded execution surfaces. Run one
  slice at a time; stop on reviewer advice, blocker, failed declared gate, or a
  no-op/advice loop; report diagnostics."

Do not turn the workflow mechanics into the goal. The goal is the product or
repo outcome; `/exec` is just the controlled way to attempt it.

## Model Selection Discipline

Model choice is execution policy, not skill prose. It varies by adapter,
project, FlowMind topology, profile, and current local configuration.

Before dispatch:

1. Run `lev exec --help` in the target project before choosing model, profile,
   flow, binding, budget, or loop flags. Do not guess flags or aliases.
2. Prefer the selected task `execution.yaml`, FlowMind `--flow=<path>`, or
   exec `--profile=<id>` over an inline `--model`.
3. Let exec profiles carry adapter/model policy. Project `.lev/exec-profiles/`
   overlays plugin profiles; explicit CLI flags override profile values only
   when the user or execution artifact requires an override.
4. Use `lev exec "binding smoke" --profile=<id> --dry-run --dry-run-resolve-binding`
   before a real dispatch when profile/model selection matters. Treat dry-run
   binding output as resolution evidence, not live provider execution proof.
5. If no project, FlowMind, or exec-profile policy exists, stop and route to
   `/propose` or diagnostics for a policy decision instead of inventing a stale
   model default in the skill.

## Worker / Reviewer Profile Pattern

Exec profiles are the ONLY profile system. Adapter-native profile/config layers
(e.g. `codex -p <overlay>`) are never read by Lev — the provider card passes
explicit model flags. Do not duplicate adapter/model policy into adapter-native
config; that is a split-brain.

Canonical bounded-loop dispatch (ralph shape):

```
lev exec "<bounded slice>" --profile=<worker-profile-id> \
  --until="<completion condition>" --verifier="<shell command>"
```

- Worker and reviewer are separate profiles (separate lanes, separate
  system prompts). Review dispatch reuses the same shape with the reviewer
  profile and a verifier that greps machine-checkable `VERDICT <claim>:` lines.
- Agent iterations outlive the default transport delta timeout; pass
  `--with execution_delta_timeout_ms=180000` (or higher) for loop dispatches
  unless the loop path already defaults it.
- Per-iteration gate proofs land at
  `.lev/agentfs/exec/artifacts/<execId>/loop-verifier/iteration-N/gate-proof.json`;
  cite them as receipt evidence, never the worker's prose claim.
- Discover profile ids with `ls .lev/exec-profiles/` plus plugin-shipped
  profiles; never hardcode model names in prompts or skills.

## Work Link

Lifecycle lane: Exec
Entity movement: `execution_ready -> executing -> verified | blocked | needs_propose`
Workstream: resolve active workstream and task entity before dispatch
Upstream: `/propose`
Downstream: `/close`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Adversarial Exec Contract

When a task has `dna.yaml` and `execution.yaml`, execution readiness is enforced
by Lev SDK, not prose:

1. Resolve the task path.
2. Run `lev task validate <task-id|task-path>` before dispatch.
3. Prefer `plugins/sdlc/flows/exec-adversarial-readiness.flow.yaml` for claim-backed tasks.
4. Review order: source-design claim coverage -> verifier adequacy -> declared gate output -> write scope -> code quality.
5. If readiness fails, stop before worker dispatch and route to `/propose`.

Hard rule: a green command is not enough. Completion needs queryable
receipt/trace evidence: node artifacts, branch decisions, verifier commands,
stdout/stderr paths, exit codes, touched files, and `claim_verdicts` with
`evidence_ref`. Score-lift needs row-level before/after deltas attributed to
selected candidates. Routing and telemetry claims need machine-readable traces.
`execution_ready` is never completion.

## Follow-up Ledger

Every exec follow-up must preserve the artifact ledger from `/propose` and add
runtime evidence: selected slice, command, cwd, verifier, receipt/trace refs,
touched files, result, fidelity/confidence, and next route. Follow-ups are
compiled into agent-operational rows, not copied from final-answer prose. If a
fix, blocker, or follow-up is discovered, write or route it through `/capture`;
do not leave it only in chat memory.

## Protocol

```yaml
steps:
  - id: resolve_context
    action: Identify workstream, task path, execution artifact, and target slice.
    validation: "workstream id, task id/path, and current slice are known."
    on_failure: "Route to /work, /ws, or /propose before executing."

  - id: validate_task
    action: Run `lev task validate <task-id|task-path>`.
    validation: "Task validation exits 0, or failures are captured as proposal work."
    on_failure: "Do not dispatch. Route to /propose with diagnostics."

  - id: read_execution_yaml
    action: Extract topology, runtime_profile, proof_gates, verifier_contract, write_scope, dependencies, and forbidden_moves.
    validation: "Every slice has verifier, write scope, and dependency status."
    on_failure: "Treat as not execution-ready."

  - id: read_proof_gates
    action: Classify Pentagon, UltraQA, and ai-slop-cleaner gates for the selected slice.
    validation: "Each applicable proof gate has commands, scenario classes, expected receipts, owner-local test placement, and cleanup policy."
    on_failure: "Route to /propose for proof-gate repair before dispatch."

  - id: classify_batch
    action: Mark slices parallel_safe or serial_only and lev_exec_first or subagent_required.
    validation: "No batch has overlapping write scope or more than 3 implementation tasks."
    on_failure: "Collapse to serial execution."

  - id: verify_surface
    action: Run `lev exec --help`, confirm flow exists, and confirm command shape before dispatch.
    validation: "No guessed flags or flow names."
    on_failure: "Downgrade to subagent or route to /propose."

  - id: dispatch
    action: Run the selected flow or subagent with bounded prompt, write scope, and verifier.
    validation: "Dispatch records command, cwd, verifier, and expected receipt/trace evidence."
    on_failure: "Emit <diagnostics-report>."

  - id: review_spec
    action: Check requested behavior, no extra behavior, write scope, and runtime contracts.
    validation: "Spec approval occurs before quality review."
    on_failure: "Fail closed as needs_propose/blocked. Do not redispatch a worker from reviewer advice unless the user explicitly asks."

  - id: review_quality
    action: Review interfaces, maintainability, tests, complexity, and correctness risks.
    validation: "Quality approval and declared verifier both pass."
    on_failure: "Do not mark verified."

  - id: run_runtime_qa
    action: Execute declared proof gates before final verification.
    validation: "Baseline verifiers, Pentagon gates, UltraQA runtime scenarios, cleanup, generated-artifact status, and ai-slop-cleaner review pass or produce a blocked verdict."
    on_failure: "Stop the current slice as blocked with diagnostics; do not spin."

  - id: final_verify
    action: Run declared verifiers, inspect changed files, and collect receipt/trace evidence.
    validation: "All verifiers pass and evidence supports the claims."
    on_failure: "Emit diagnostics and stop the failing slice."

  - id: update_followup_ledger
    action: Record verified, blocked, or follow-up rows with disk/memory state and evidence refs.
    validation: "Every new follow-up has compiled_intent, current_location, artifact_ref or blocker, fidelity/confidence, route_state, and next_route."
    on_failure: "Route unresolved rows to /capture before final summary."
```

## QA / Pentagon Runtime Rules

- Treat UltraQA scenario generation as proposal/design input, but runtime
  execution belongs here: commands, exit codes, timeouts, temporary harnesses,
  cleanup, flaky reruns, misleading-output checks, and residual risks.
- Run Pentagon gates from `execution.yaml.proof_gates.pentagon` when present.
  Do not substitute a repo-wide green audit for a feature-local promotion claim.
- Run ai-slop-cleaner review when `proof_gates.quality.ai_slop_cleaner.required`
  is true, or when the exec slice performs cleanup/refactor work or touches
  fallback/boundary-risk code.
- Module-specific tests, probes, fixtures, and harness suites stay with the
  owning module. `core/testing` is a shared testing/eval library and generic
  gate surface, not the destination for module-owned proof code.
- Record generated harnesses, logs, state files, and cleanup status in the
  validation evidence. Remove temporary artifacts unless the task deliberately
  promotes them.

## Dogfood Rules

- While working on Lev, use Lev surfaces first when reasonable.
- Fix simple local errors discovered by the verified path when scoped,
  reversible, and covered by the same verifier.
- Always try `--help` before unfamiliar Lev commands or flags.
- Prefer short evidence chains: `--help`, `--dry-run`, verifier, then trace.
- After failed or interesting `lev exec`, inspect receipt/trace lookup before
  summarizing.

## Fail-Closed Loop Rules

- Multi-slice exec runs are serial by default. Run one slice, review it, then
  decide whether the next slice is still execution-ready.
- Reviewer `advice` is a terminal blocker for the current dispatch. Route to
  diagnostics or `/propose`; do not treat advice as another worker prompt.
- A no-op worker followed by reviewer advice is an immediate stop condition.
- A green command plus reviewer advice means the verifier is insufficient or the
  claim is overbroad. Stop and repair the task/proof, not the code.
- Same blocker twice means stop. Do not spend a third loop unless the user
  explicitly asks for another attempt.

## Diagnostics Report

<diagnostics-report>
## Exec Diagnostics: {task_or_slice}

- command: `{command}`
- cwd: `{cwd}`
- exit_code: `{exit_code}`
- stdout: `{stdout_path_or_excerpt}`
- stderr: `{stderr_path_or_excerpt}`
- receipt_id: `{receipt_id_or_none}`
- exec_id: `{exec_id_or_none}`
- trace: `{trace_ref_or_none}`
- ledger_row: `{capture_or_followup_id}`
- compiled_intent: `{agent_operational_followup}`
- current_location: `{disk|memory|both|external|unknown}`
- artifact_ref: `{path_or_none}`
- route_state: `{captured|execution_ready|blocked|done|rejected}`
- next_route: `{retry_exec|propose|capture|work|blocked|close}`
- suspected_layer: `{plan|surface|adapter|verifier|implementation|environment}`
- simplest_next_fix: `{one_action}`
- route: `{retry_exec|propose|work|blocked}`
</diagnostics-report>

## Flow Routing

| Situation | Surface |
|---|---|
| task has execution.yaml | project-selected FlowMind/topology from execution artifact |
| bounded implementation with verifier | verified `lev exec` flow |
| reviewer loop needed | `lev-ralph` if supported by current CLI |
| no clean verifier or bespoke context | subagent with explicit scope and verifier |
| architecture or tradeoff work | route back to `/propose`, `/interview`, or `/prior-art` |
| weak/missing execution artifact | `/propose` |

For 10x Ralph/proposal expansion, use an outer controller loop. One successful
Ralph run produces one item, not the full list.

## Lev Contracts for Runtime Work

If touching FlowMind, plugin config, scheduler, runtime steering, context
injection, protocols, or graph control flow, load relevant DNA/gates/design
docs and carry explicit notes for:

- `LevEvent` lifecycle emission
- trace context propagation
- structured logging
- bounded budgets, retries, and timeouts
- append-only receipts
- scope and permissions
- structured machine schemas
- resumability and idempotency
- project scheduler use
- protocol/config resolution through the fractal chain

## Red Flags

- "Just ship it."
- "The verifier is small but probably enough."
- "Flow name probably maps to CLI."
- "No execution.yaml, but this is obvious."
- "execution_ready means done."
- "Receipt lookup can wait."
- "I'll summarize the failure without the command and exit code."
- "UltraQA is just a scenario list; no runtime cleanup or evidence needed."
- "A green Pentagon audit proves the feature-local claim."
- "Exec follow-ups can stay in the final answer without a ledger route."
- "Reviewer advice means try the worker again."
- "The goal prompt should describe the exec workflow instead of the actual task."

## Rationalization Table

| Excuse | Reality |
|---|---|
| "Smallest relevant checks." | Declared verifiers and claim evidence are mandatory. |
| "We can infer success from no-regression." | Behavioral claims need direct outcome evidence. |
| "The CLI probably supports that flag." | Run `--help`; never guess. |
| "Trace is optional." | Routing, telemetry, and receipt claims need machine-readable evidence. |
| "The executor can fix the plan." | Weak plans route to `/propose`, not execution. |

## Related

- `/work` routes lifecycle state.
- `/propose` creates execution-ready artifacts.
- `/close` seals verified work.
