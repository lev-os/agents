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
    action: Extract topology, runtime_profile, verifier_contract, write_scope, dependencies, and forbidden_moves.
    validation: "Every slice has verifier, write scope, and dependency status."
    on_failure: "Treat as not execution-ready."

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
    on_failure: "Return to the same execution surface for fixes."

  - id: review_quality
    action: Review interfaces, maintainability, tests, complexity, and correctness risks.
    validation: "Quality approval and declared verifier both pass."
    on_failure: "Do not mark verified."

  - id: final_verify
    action: Run declared verifiers, inspect changed files, and collect receipt/trace evidence.
    validation: "All verifiers pass and evidence supports the claims."
    on_failure: "Emit diagnostics and continue the failing slice."
```

## Dogfood Rules

- While working on Lev, use Lev surfaces first when reasonable.
- Fix simple local errors discovered by the verified path when scoped,
  reversible, and covered by the same verifier.
- Always try `--help` before unfamiliar Lev commands or flags.
- Prefer short evidence chains: `--help`, `--dry-run`, verifier, then trace.
- After failed or interesting `lev exec`, inspect receipt/trace lookup before
  summarizing.

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
