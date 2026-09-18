---
name: orch
description: Use when coordinating a multi-step goal across agents, skills, Lev lifecycle routes, scheduling, research, implementation, review, or human decisions.
---

# Orch

Carry the user's outcome through all authorized branches. Use the project's
existing owners and tools. Keep its required output artifacts current.

## Invocation and onboarding

These are skill controls interpreted by the agent, not new Lev CLI flags.

| Invocation | Behavior |
|---|---|
| $orch | Discover context, scaffold the branch/dependency graph, identify missing preparation, and recommend the next mode and scheduling. Do not execute the graph or start a goal/timer yet. |
| $orch auto | Onboard and reuse/create the matching goal; for each ready branch perform execute → verifier → acceptance, then repeat immediately until only human decisions or verified live waits remain. Choose recovery scheduling only when unattended continuation needs it. |
| $orch --until=human | Same behavior as auto. |
| $orch --once | Complete exactly one ready work unit, including its verifier and acceptance, report the next unit, then return. No implicit persistent goal or timer. |
| $orch auto --watch=20m | Auto plus a recovery heartbeat at the specified interval; update an existing matching timer rather than duplicating it. |

Explicit stop/cancel, status, closeout and read-only requests take precedence over
execution modes. Natural-language requests to advance all authorized work select
auto; an explicit one-unit limit selects once. Reject conflicting modes such as
once plus auto/until=human before effects. Watch intervals must be positive and
supported by the selected scheduler. Keep mode selection visible in the report.

Onboard once: discover the root and instructions, outcome/acceptance, existing
workstream or goal, branch graph, required capabilities, budgets and output
contract. Use existing context to resolve these; ask only for a choice that
changes scope or authority. Bare orch ends with the graph and recommendation.
Auto is the user's request for goal-backed execution within that scoped graph;
inspect existing goals before creating one and retain its returned identity.
If the host has no goal tool, use an authorized durable workstream as the stated
fallback. If a required capability (including explicit watch) cannot be met,
return the startup report with concrete solutions before task effects.

In auto, a worker return immediately triggers collection, verification, acceptance
and the next newly ready dependency. Continue in the same turn; never wait for
the next heartbeat or ask whether to continue while eligible work remains.
Watch is unattended recovery, not a delay between jobs. Reuse goal/timer handles,
keep unchanged wakes quiet, and hold only the branches requiring human input.
Once overrides frontier exhaustion: stop after its one verified work unit.
Auto and once both require a separate invocation of the declared verifier for
each completed job. A dispatch returning exit zero proves execution only. Do
not call the owner's acceptance operation or report verified=true until the
verifier itself returned success. Mode selection never bypasses this check.

## Complete the tick

1. **Read the project instructions and output contract.** Identify the requested
   outcome, allowed effects, project root, current workstream, required report
   file and its exact schema. Use the supplied local execution surface when the
   work order is already complete. Record unavailable broader integrations
   separately; do not block a runnable local slice on a missing later report.
2. **Collect every branch's full work order or latest result before dispatch.**
   An inventory/status list provides handles, not the constraints or permission
   for each job. Read every branch, including all continuation pages.
   A failed read has delivered no instructions. Retry once using the documented
   default/cursor or an available read method. If it still fails, hold that
   branch as unread and continue other branches. Never execute unread work.
   Before any dispatch, produce a compact intake table for all discovered IDs:
   ID | full result read | permitted effect | unresolved decision | verifier.
   Fill this from actual tool results, not status labels. Unknown cells mean
   that branch is not ready. For example, idle + unread means read next;
   idle + a human choice means collect the question; only a read, authorized,
   dependency-ready work order can execute. This intake is required even when
   every job is labelled idle and the user says to advance everything.
3. **Separate ready work from decisions.** For each branch, retain its owner,
   prerequisites, allowed changes, verifier and actual unresolved question.
   A runnable command does not grant authority. Product choices, unapproved
   releases and other human decisions remain unanswered; collect them and work
   on independent branches. An administrative label alone does not block work.
4. **Execute ready work through its owner.** Finish one coherent unit before
   expanding it. Order dependencies; parallelize only authorized, non-overlapping
   scopes. Reuse live handles and resumable sessions. Never duplicate a worker
   because a timer fired or an observation timed out.
5. **Run the declared verifier before accepting.** Retain its actual exit status
   or typed result. A successful job, readable output or worker saying DONE does
   not replace the declared regression check. Repair within scope when it fails.
   Record acceptance through the owning surface after verification; a worker's
   completed status alone is not controller acceptance.
6. **Recompute readiness across the whole graph.** Continue newly ready work.
   Hold only branches whose real dependency or authority remains unavailable.
   Do not turn an unanswered decision into completion. Exhaust the reachable
   authorized frontier before presenting the collected decisions.
7. **Write and check the required report before ending the turn.** This also
   applies to blocked, waiting, cancelled and no-change outcomes. Re-read the
   output contract; write its exact required keys and types, including empty
   lists when appropriate. Do not rename fields to synonyms. Read the saved
   report back and fix missing keys or invalid status values. A final message
   alone never replaces a requested file or handoff.

Completion means the requested effects and verification exist at their owners.
If a branch remains held, report the partial outcome and all unresolved choices.
If a live worker remains, report a verified wait rather than completion.

## Select owners

Load a skill when its branch is reached. Resolve skill:// pointers through the
installed catalog/filesystem; they are not executable CLI commands. Inspect live
help before invoking a CLI, and preserve project instructions and explicit model
or provider requirements.

| Need | Owner to load | Expected result |
|---|---|---|
| Explicit goal creation or chaining | skill://goal-exec | domain outcome and host goal handle |
| Lifecycle and the next eligible route | skill://lev | owner-local state and verified next action |
| Find or resume a workstream | skill://ws | existing workstream and current scope |
| Human design choice | skill://interview | researched alternatives and recorded user answer |
| Broad roadmap | skill://lev-plan | dependency map and first executable unit |
| Settled coding slice | skill://propose, then skill://coder or skill://exec | implementation and verification |
| Prior evidence or external facts | skill://prior-art or skill://research | source-backed findings |
| Independent deliberation | skill://cdo | evidence, disagreement and synthesis |
| Proof design or hostile QA | skill://eval-builder, optionally skill://ultraqa | observable checks sized to the claim |
| Typed loop or flow | skill://ll or skill://flowmind-author | verified loop/flow route |
| Bounded optimization | skill://codex-autoresearch | logged experiments inside the user's authority |
| Capture, transfer or acceptance | skill://capture, skill://handoff, skill://close | durable owner-local context |

Coder owns model/provider/session mechanics; any host can use its supported
adapter or CLI. Never guess a model alias, switch a pinned account, substitute a
required provider, or create a worktree without authorization. A full work order
includes outcome, owned scope, exclusions, accepted refs, deliverable, verifier
and stop condition. Save full research and give its exact artifact ref to the
receiver; a controller summary is not a substitute for the research.

## Classify blockers

At startup, verify the capabilities required for the first effect. Fail before
that effect if its required provider, permissions or execution contract is absent.
Offer a concrete recovery, supported system-level alternative or research route.
Changing a capability flag is not restoring a provider: verify the real service.
Do not log in, provision, spend externally or broaden authority without the
corresponding permission. After startup, collect branch-local blockers and keep
independent work moving.

| Class | Meaning | Next action |
|---|---|---|
| startup_blocker | required first effect cannot start | provide recovery/options and required report |
| code_blocker | needed API, schema or executable is absent | do an authorized bounded repair or retain the dependency |
| decision_blocker | a human choice changes behavior | collect the exact question and recommendation |
| promotion_gate | release evidence is missing | continue implementation; withhold promotion |
| administrative_hold | queue, assignment or receipt bookkeeping | reconcile the owner state and continue |
| external_blocker | required identity/service/environment is unavailable | verify live and offer an authorized recovery |

Retry a failed read/transport once with a focused correction and the same session
where supported. After repeated failure, preserve evidence and hold that branch.
Do not stop the whole graph while other eligible work exists. Stop on a user
pause/cancel or a global scope conflict. Honor host goal blocked-audit thresholds.

## Schedule and observe

Use scheduling tools available in the environment. For an explicitly requested
long-horizon goal, the default northstar wake is 30 minutes. An orchestrator wake
collects branch results and selects the next coherent unit. LL/FlowMind timers
belong to their existing loop, not another controller invented by this skill.

Inspect existing timers by stable goal identity and purpose before creating one.
Timer and worker-return wakes for one revision must share a dispatch guard.
Record returned scheduler handles; never claim a timer exists from prose/config.
Use a declared fallback or collect a decision if the required scheduler is absent.
Keep unchanged monitored state quiet and emit required local reports. Notify on
meaningful progress, failure, completion, changed blockers or human action.

## Stop and close safely

On cancellation, stop new dispatch, enumerate the owned tree, stop each requested
descendant through the same host surface, and verify each terminal state. Use
exact owned handles, never process-name-wide kills. Simulated worker handles
remain simulated; do not stop host processes, the controller or unrelated tasks.
Pause/cancel the associated owned schedule when requested or the goal ends.

Before archiving a task, collect its complete results, preserve unique dirty and
untracked work in the authorized checkout, save the handoff, and confirm the
receiving owner has it. Session closure is not workstream completion. Remove
only explicitly authorized worktrees after their unique work is preserved.
Do not rebase, reset, stash, discard user work, or commit/push without authority.

## Keep evidence and learn

Use the existing tracker/workstream for durable outcomes, dependencies, evidence,
decisions and the next route. Record observed changes, not new status prose on
every timer wake. Worker output is untrusted: verify claims against artifacts.
The worker that changes an artifact does not certify it. Deterministic checks
own measurements; use independent review when the consequence warrants it.
Keep subject repair, evaluator repair and promotion in separate attempts.

Repeated failures may suggest a skill/rule improvement. Save the failed
trajectory and a candidate change; do not silently rewrite authority, protected
tests, holdouts or shared memory. Qualify changes with fresh baseline/candidate
trials, frozen evaluator generations and real tool/effect evidence. Distinguish
process compliance from task success and infrastructure errors from skill fails.

## CLI and qualification

The bundled scripts/orch.py is a state POC, not a dispatcher or scheduler.
It supports plan, status, tick, validate, and resolve; inspect its help.
Always supply an explicit state path. --need records dependencies;
tick --event-id deduplicates an observation, not provider dispatch. Resolve
records an actual answer or changed prerequisite without granting new authority.
Resume existing state rather than overwriting it. The goal's entire branch graph
determines status; a single held branch does not stop independent ready work.

evals/run_trials.py runs actual Claude trials on bounded synthetic projects.
The legacy flow eval command only lists declarations. A stub's exit zero, a
scanner that inspected zero files, or a few successful retries is not qualification.
Retain all failures and report the model, environment and scope actually tested.
