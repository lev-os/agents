---
name: lev
description: Use when invoking, debugging, or dogfooding the Lev CLI; choosing between work, exec, stack, FlowMind, validation, traces, receipts, or runtime health commands.
skill_type: how-to
category: cli
sub_skills:
  - work
  - exec
  - stack
  - autodev-lev
---

# lev - Agent Runtime CLI

Lev is the project CLI and runtime surface. Treat it as a live local interface,
not a remembered API.

## First Move

1. Run help before using a surface: `lev --help`, then `lev <command> --help`.
2. If `lev` is not on `PATH`, run from the Leviathan source tree:
   `node core/poly/bin/lev --help`.
3. Some current commands treat `--help` as execution or are discoverable but not
   runnable. Record that exact behavior instead of assuming the surface works.
4. If `node core/poly/bin/lev` fails, capture the failure in a diagnostics
   report before guessing a fallback.
5. For lifecycle work, resolve the workstream through `/work` or `lev work`
   before dispatching `lev exec`.

Help-first is mandatory. Do not invent flags, aliases, flow names, or receipt
commands from memory.

## Source Wrapper

Use this pattern when working inside the Leviathan repo:

```bash
LEV=lev
command -v lev >/dev/null 2>&1 || LEV="node core/poly/bin/lev"
$LEV --help
$LEV exec --help
```

If that wrapper fails because `node`, `tsx`, dependencies, or project root
resolution are broken, fix only the simple local issue when it is scoped,
reversible, and verified by the same command. Otherwise emit diagnostics and
route to `/exec` or `/propose`.

## Core Surfaces

Observed current surfaces:

| Need | Command |
|---|---|
| Show command registry | `$LEV --help` |
| Route workflow stage | `$LEV work --help` |
| Dispatch agent work | `$LEV exec --help` |
| Validate task contract | `$LEV task --help`, then `$LEV task validate <task-id|task-path>` |
| General validation | `$LEV validate <path>`; note that `$LEV validate --help` currently runs validation against cwd |
| Runtime health | `$LEV doctor --help` currently runs doctor; `$LEV health --help` is discoverable but root-router unimplemented |
| FlowMind work | `$LEV flowmind --help`, `$LEV flowmind-debug --help` |
| Trace/receipt lookup | `$LEV trace --help`, `$LEV receipt --help` |
| Broken trace aliases | `$LEV exec-trace --help` and `$LEV exec-receipt --help` currently return `UNIMPLEMENTED_COMMAND_SURFACE` |
| Prompt stacks | `$LEV stack --help` or `/stack` |

`lev work` currently supports `auto`, `find`, `review`, and `contract`, plus
`--dry-run` and `--json`. Use it for routing, not as a substitute for workstream
continuity.

`lev exec` currently supports `--workstream`, `--flow`, `--dna`, `--dry-run`,
`--status`, `--verifier`, `--until`, `--concurrency`, `--max-iterations`,
`--max-turns`, `--budget`, retry flags, and `--knob/--with` overrides.

`lev exec --flow` validates the resolved FlowMind graph before provider or tmux
dispatch by default. Use `--no-validate` only for deliberate diagnostics; failed
FlowMind validation must block dispatch and should be reported with receipt or
trace evidence when available.

## Dogfood Loop

Use Lev surfaces first when working on Lev, unless the CLI is itself the thing
being repaired.

```yaml
steps:
  - id: help
    action: Run `$LEV <surface> --help`.
    validation: "Command exists and flags are copied from live help."
    on_failure: "Emit diagnostics with command-not-found or help failure."

  - id: route
    action: Resolve lifecycle stage and workstream.
    validation: "Workstream id is known or `/work` is the next skill."
    on_failure: "Do not dispatch execution."

  - id: dry_run
    action: Prefer `--dry-run` or `--json` when the command supports it.
    validation: "Planned command, write scope, and verifier are visible."
    on_failure: "Route to diagnostics or `/propose`."

  - id: execute
    action: Run the smallest command that proves or advances the entity.
    validation: "Exit code, stdout/stderr, changed files, and artifacts are known."
    on_failure: "Fix simple scoped errors or emit diagnostics."

  - id: inspect
    action: Check receipt, trace, events, or status after failures and interesting runs.
    validation: "Report cites trace/receipt refs or says none exist."
    on_failure: "Do not summarize as complete."
```

## Command Chaining Practice

Build evidence chains, not opaque one-liners:

1. Help: `$LEV <command> --help`
2. Preview: `$LEV <command> ... --dry-run` or `--json`
3. Gate: validator, verifier, or targeted test
4. Inspect: trace, receipt, status, or event log
5. Summarize: command, exit code, evidence, next route

When a shell chain is useful, keep it auditable: use `set -euo pipefail`, keep
the chain short, and do not hide failing commands behind pipes that always exit
0. In agent tool calls, prefer separate commands when the output needs review.

## Exec Prompt Shape

Every `lev exec` prompt should answer:

1. What does passing look like?
2. What is failing now?
3. What specifically changes?
4. What must not change?
5. How is completion verified?

Example:

```bash
$LEV exec "Fix config validation for core/exec.

Current failure:
- namespace_is_lev rejects namespace: exec.

Reference:
- plugins/browser-cascade/config.yaml uses namespace: \"@lev-os/browser-ops\".

Scope:
- Touch only core/exec/config.yaml.

Done:
- $LEV validate core/exec exits 0.
- git diff shows only core/exec/config.yaml." \
  --workstream=<ws-id> \
  --verifier="$LEV validate core/exec"
```

## Diagnostics Report

Use this for broken commands, failed dispatch, uncertain flags, missing traces,
or runtime-health issues:

<lev-diagnostics-report>
## Lev Diagnostics: {surface_or_command}

- command: `{command}`
- cwd: `{cwd}`
- path_resolution: `{lev_path_or_source_wrapper}`
- help_checked: `{yes|no}` `{help_command}`
- exit_code: `{exit_code}`
- stdout: `{stdout_path_or_excerpt}`
- stderr: `{stderr_path_or_excerpt}`
- config_scope: `{system|project|module|env|unknown}`
- workstream: `{ws_id_or_none}`
- dry_run: `{command_or_none}`
- verifier: `{command_or_none}`
- receipt: `{receipt_id_or_none}`
- trace: `{trace_ref_or_none}`
- suspected_layer: `{path|dependency|config|flow|adapter|verifier|implementation|environment}`
- simplest_next_fix: `{one_action}`
- route: `{retry|/work|/propose|/exec|blocked}`
</lev-diagnostics-report>

## Trace and Event Follow-Ups

Try help first, then inspect the relevant surface:

```bash
$LEV exec --status
$LEV trace --help
$LEV receipt --help
```

Known root-router gaps from dogfood on 2026-05-09:

- `$LEV exec-trace --help`: `UNIMPLEMENTED_COMMAND_SURFACE`
- `$LEV exec-receipt --help`: `UNIMPLEMENTED_COMMAND_SURFACE`
- `$LEV health --help`: `UNIMPLEMENTED_COMMAND_SURFACE`
- `$LEV validate --help`: executes validator against cwd instead of showing help

Useful files when present:

```text
~/.local/share/lev/events.jsonl
~/.local/share/lev/exec/traces/traces.jsonl
.lev/agentfs/exec/events.jsonl
```

For failed or surprising executions, do not stop at stderr. Look for receipt,
trace, event, and workstream state before deciding the next route.

## FlowMind and Lifecycle

- Use `/work` for lifecycle routing and HUD discipline.
- Use `/propose` when the entity is not execution-ready.
- Use `/exec` when `dna.yaml` and `execution.yaml` exist with verifier and write
  scope.
- Use FlowMind commands when the work is a graph/topology/runtime issue.
- Use `/close` after verified work to checkpoint, learn, and update state.

## Source Map

| Domain | Path |
|---|---|
| CLI binary | `core/poly/bin/lev` |
| CLI dispatch | `core/poly/src/surfaces/cli/` |
| Exec engine | `core/harness/src/` |
| Orchestration | `core/orchestration/src/` |
| FlowMind | `core/flowmind/src/` |
| SDLC plugin | `plugins/core-sdlc/` |
| Prompt stack | `plugins/prompt-stack/` |
| Domain types | `core/domain/` |
| Config | `core/config/` |

Read `dna/graph.yaml` before touching core runtime behavior. Preserve bounded
loops, append-only receipts, explicit scope, and deterministic validation gates.

## Red Flags

- "I remember the flag."
- "The alias probably still exists."
- "The command failed, so I'll use shell directly."
- "No need for a dry-run."
- "Trace lookup can wait."
- "This tiny fix can skip the workstream."
- "stderr is enough diagnostics."
