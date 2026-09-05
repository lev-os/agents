---
name: lev
description: Use when routing intent into Lev lifecycle work, clarifying an uncertain next step, or invoking and diagnosing the Lev CLI and runtime.
skill_type: router
category: lifecycle
sub_skills:
  - work
  - exec
  - stack
  - autodev-lev
---

# lev - Semantic Router and Runtime CLI

## Entity Reconciliation

After authorized material progress, reconcile touched and causally affected
artifacts before routing, handoff, or final response. Track entity ref,
island/provider locator (a path for file storage), basis/evidence, and the
reason/action due. Update through the verified owning CLI/adapter; use a
write-authorized skill fallback only when that operation is unavailable.
Record updated, no_change(reason), or blocked(reason), preserving unresolved
refs. Reading or mentioning a path alone creates no update obligation.
Read-only work reports pending changes only. Reminders grant no write authority;
task status stays with the bound tracker. Update only artifacts whose content
or evidence changed; do not rewrite every referenced document.

## Next Route Contract

`$lev next` executes the next eligible bounded action in the active workstream;
it does not merely describe the next action. Revalidate its entity/source basis,
authority, dependencies and budget first. If blocked, name the exact prerequisite.

Project the selected action as one line: `Next: skill://<name>`,
`Next: cli://<registered-operation>`, or `Next: trigger://<registered-trigger>`.
These are typed route references, never shell text. Skill routes load the named
skill; CLI routes resolve a real command and inspect help; trigger routes resolve
an existing registered event/flow. Unknown routes remain blocked. This skill
contract does not create a `lev next` CLI command.

For this session's Codex POC, before emitting an automatic Next line, register
the current turn and current entity digest with
`python3 /Users/jean-patricksmith/ops/pocs/lev-codex-hud/auto.py recommend --route <route> --entity <absolute-path> --turn <current-turn-id>`.
Only configured read-only skill routes are currently admitted automatically;
CLI/trigger references require their existing resolver and authority.
On explicit `$lev next` or `$lev --auto`, rearm a paused episode if no attempt
is outstanding. Never reset its consumed budget. An injected `Call $lev next`
with a continuation ID requires `auto.py start --id <id>` before work and
`auto.py settle --id <id> --evidence <path>` after reporting evidence. These
controller bookkeeping writes are permitted; they do not authorize task effects.
Queue → start → settle the reported result → review against the bounded claim →
`auto.py accept --id <id> --evidence <review-evidence>` before another auto route.
Controller acceptance permits routing; it is not canonical lifecycle acceptance.
After 10 automatic turns, pause for mandatory human review. Ordinary rearm must
not clear that limit or reset counters; explicit human authorization is required
for another episode.
Do not assume Stop continuation emits UserPromptSubmit. Never claim native
continuation until its delivery/start evidence is present.

## First Move: Route OR Operate the Runtime

First interpret the requested outcome. Choose one path:

| Path | When | First action |
|---|---|---|
| Skill or specific FlowMind | An existing method or verified flow fits the request | Load the matching `skill://<name>` or resolve the concrete flow; follow its contract |
| Clarify the route | Missing intent or a decision changes which method applies | Inspect discoverable facts, ask one to three focused questions, then show a numbered 1–n route table |
| Direct runtime operation | The user needs CLI operation/diagnosis, or no specialized method fits an otherwise clear runtime request | Follow Runtime First Move below |

Do not run the generic CLI tour before every skill-routed request. Help-first
applies when actually using a CLI surface, including execution of a selected
FlowMind. A missing required flow is a routing gap, not permission to silently
substitute a generic loop. Resolve current paths, profiles and available flags;
do not invent flow identifiers from names such as Ralph or architecture review.

## Recursive Wayfinding

All LLM work follows alignment (problem/solution shaping) → propose → act →
verify at the granularity of a coherent work unit. A proposal is a graph patch
offer; code is one possible manifestation. Normal progression visits the next
stage only after its conditions hold. Gate rejection stays or returns to an
earlier stage; it never skips forward or certifies a later stage.

For graph proposals, recursive depth/density requests, or `--auto --recursive`,
load [references/recursive.md](references/recursive.md). It defines breadth-first
simulation, candidate graph deltas, durable capture, and existing-to-proposed
visualization. These are skill semantics, not newly implemented CLI flags.
`--auto` performs eligible shaping/projection within scope; applying proposed
effects still requires their existing authority. The current `propose` skill
implements SDLC packet specialization; generic patch-offer routing does not
silently rename that skill or claim a new runtime API.

For long-horizon or multi-session work, or when the user invokes
`$lev --recursive`, read [references/recursive.md](references/recursive.md)
before charting or materially revising the route. Also load it when a selected
step becomes vague, an assumption is invalidated, a dependency changes, or a
structural failure changes the path to the outcome. `$lev --recursive` is skill
syntax that force-loads this procedure; it is not a `lev` CLI flag. Skip the
reference for a clear bounded request whose route and acceptance are already
known.
Do not finish a user-facing recursive pass until the reference's required
steps 1-3 and steps 4-10 tables are rendered with the active session HUD.
For this artifact, those tables replace any generic follow-up menu or bullet
limit: do not render `🪄 Next steps`. Mark user-provided facts `(supplied)`, not
`(observed)`, and place the exact active-session HUD as the final line.

## Domain Overlay Simulation

Lev routes domain/manifestation overlays; software delivery is the `plugins/sdlc`
overlay, not the universal lifecycle. Simulate this distinction in the runbook
until config-driven routing is available; this prose does not enable a plugin.

| Task domain / missing state | Route |
|---|---|
| Coding; architecture or domain boundaries unresolved | `skill://arch` → `skill://interview` if a human decision remains → `skill://lev-plan` for broad work |
| Coding; decisions settled | `skill://propose` for a selected SDLC execution packet → `skill://exec` |
| Non-coding; broad effort | `skill://lev-plan` → the matching domain skill or `skill://exec` with sufficient scope and acceptance |
| Non-coding; clear bounded request | Matching domain skill; no mandatory proposal packet or coding loop |

Skip already-satisfied stages. Preserve read-only intent and the current
workstream. A plan can supply non-coding execution context without `propose`;
it still needs a named outcome, permitted effects, acceptance and stop condition.
SDLC's future default is a Ralph loop over one coherent next chunk, using
`lev-ralph` worker/reviewer cycles. Runtime adoption is deferred; route through
currently available authorized methods without claiming Ralph ran.

## Intent Routes

| Intent or state | Route | Result |
|---|---|---|
| Development with a bounded implementation outcome | `skill://exec` | Select the declared flow/profile; use a bounded Ralph-style loop when iteration is relevant |
| Development still missing decisions or scope | `skill://interview` or `skill://lev-plan` | Resolve design choices or produce a broad runbook before execution |
| Architecture review | `skill://arch` | Evidence-backed boundaries, alternatives and findings; use a matching verified review flow when available |
| Capture conversation intent | `skill://capture` | Durable source-fidelity ledger |
| Find or resume work | `skill://ws` | Existing workstream and next entity |
| Prior decisions or implementation precedent | `skill://prior-art` | Local evidence and provenance |
| External facts | `skill://research` | Sourced findings |
| Bounded feasibility or prototype | `skill://poc` | Evidence resolving one uncertainty |
| Broad implementation route | `skill://lev-plan` | Runbook, delivery DAG, proof and rollback |
| Harden a planning artifact | `skill://auto-enrich` | Bounded independent review and planning repair |
| Slice readiness or task emission | `skill://propose` | Review, map or authorized single packet |
| Accept verified work | `skill://close` | Acceptance and learnings |
| Pause or transfer context | `skill://handoff` | Durable continuity and resume pointer |
| Create or consolidate a skill | `skill://skill-builder` | Skill instructions and behavioral checks |
| Prompt-stack operation | `skill://stack` | Inspect or run the selected stack |

## Routing Examples

| Request | First move |
|---|---|
| "Implement this agreed parser fix and iterate until the tests pass." | `skill://exec`; resolve the bounded Ralph-style execution contract and verifier |
| "Review the architecture of this module. Read only." | `skill://arch`; inspect and report without implementation |
| "Use this specific FlowMind to review the change." | Resolve and validate that flow, then run it through `skill://exec` within the requested review scope |
| "Help me with authentication." | Clarify the missing intent; present numbered design, diagnosis, planning or execution routes that fit the evidence |
| "Why did lev exec fail to resolve this profile?" | Runtime First Move; inspect live help, binding and diagnostics |

For an uncertain route, use columns `#`, `Route`, `Expected result` with
`skill://<name>` values and contiguous numbers. Recommend one only when supported
by the available context. Clear requests proceed without a compulsory menu.

## Semantic Lifecycle Router

`lev` is the semantic entry point for lifecycle work. "Take over" was a metaphor,
not a command, mode, trigger phrase, or new grant of execution authority. `/work`
remains the compatibility entry point to the same lifecycle procedure.

Interpret the requested outcome and verb class, reuse the active workstream,
inspect its state and relevant sources, then select the next useful lifecycle
owner. Incorporate Wayfinder's destination, precise questions, fog, exclusions,
dependency frontier and resolution delta. Keep the frontier derived from current
state; do not create another tracker or claim cross-session exclusivity.

If the route is clear, proceed within the user's authorized scope. If uncertainty
changes the route, look up discoverable facts first, ask one to three focused
questions, and present the viable routes as a numbered 1–n menu. Each entry names
the owner, intended result and consequence; recommend one and allow free-text
correction. Do not invent options to fill a quota or infer approval from silence.

Use the Intent Routes above. The planning pair shares substantive rules while
differing in scope/output and emission authority. Runtime CLI operations remain
help-first; do not turn skill routes into invented CLI flags.

Validation: a clear request reaches the correct owner without needless menus;
ambiguous intent produces a small grounded question set and numbered routes;
read-only intent causes no write or dispatch; the original workstream persists.

Lev is the project CLI and runtime surface. Treat it as a live local interface,
not a remembered API.

## Decision Frontier Procedure

Resolve artifact references using their declared base. For an unqualified local
reference, check its exact project-root path and the referring artifact's
directory within authorized scope. If both exist with different content, expose
the ambiguity rather than choosing silently. If neither exists, use a bounded
filename inventory; searching file contents for a filename does not establish
that the file is absent. Report the locations actually checked and distinguish
missing, unreadable and ambiguous references before declaring the frontier blocked.

For an effort spanning sessions, orient to its destination and standing
constraints before choosing work. Load the workstream index first, then follow
named artifact pointers only as needed. Use human-readable names linked to stable
IDs; avoid presenting a wall of bare IDs. Keep decision detail in its owning
artifact, with a short pointer in the workstream rather than duplicate prose.

Distinguish three sets: precise open questions (including blocked questions),
in-scope fog that cannot yet be phrased precisely, and explicit exclusions.
Inability to answer a precise question is a dependency, not fog. Derive the
ready frontier from open questions whose dependencies are satisfied and whose
assignment permits this session to work; a local assignment is not a proven
cross-session lock. An explicitly selected blocked item stays blocked until
its prerequisite or authority changes.

Chart broadly before deep-diving one branch. If the route is already clear,
use the existing bounded plan/task instead of manufacturing a decision map.
Research routes to evidence gathering; feasibility to `skill://poc`; live human
decisions to `skill://interview`. The agent cannot answer for the human.
Provisioning or other prerequisite effects require their own authorized scope.
Planning resolves decisions; it does not silently start delivering the outcome.

After a bounded decision unit, record the answer at its owner, update the
workstream pointer and dependency status, and revisit affected questions.
Graduate fog only when a precise question can now be stated; remove its old fog
entry so it is represented once. Keep exclusions off the ready frontier with
their rationale. Reopening excluded work requires an explicit scope decision.
Invalidate stale dependent assumptions rather than silently carrying them on.
Stop or hand off when the planned decision is resolved; another unit needs to
remain within the authorized effort and budget. No new tracker, automatic
research branch creation or fixed token/session quota is implied.

## Runtime First Move

1. Run help before using a surface: `lev --help`, then `lev <command> --help`.
2. If `lev` is not on `PATH`, run from the Leviathan source tree:
   `node core/poly/bin/lev --help`.
3. Some current commands treat `--help` as execution or are discoverable but not
   runnable. Record that exact behavior instead of assuming the surface works.
4. If `node core/poly/bin/lev` fails, capture the failure in a diagnostics
   report before guessing a fallback.
5. For lifecycle work, resolve the workstream through `/work` or `lev work`
   before dispatching `lev exec`.

Help-first is mandatory for CLI operations. Do not invent flags, aliases, flow names, or receipt
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

After semantic routing selects runtime work, use this CLI procedure. It does
not precede a skill-only architecture review, interview, or other routed method.

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
| SDLC plugin | `plugins/sdlc/` |
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
