# Long-running goals: finish the outcome

Read when composing a persistent goal or supervising multi-turn execution.
This is shared by goal-exec (objective authoring) and orch (execution control).
It does not create a goal, grant effects, change modes, or authorize scheduling.

## Write a finishable goal

Define the observable end state first, then the required behaviors, exclusions,
source refs, acceptance checks and real stopping conditions. Be exhaustive about
requirements, not prescriptive about every tool call. Separate required work
from optional improvements; a discovered adjacent problem is not automatically
another deliverable. Carry accepted user decisions forward without re-interviewing.

Show the complete proposed goal in a Markdown code block when creating or
revising it; do not make the user ask another turn to see the replacement text.
If creation is already authorized, displaying it is not another approval gate.
Inspect the host goal first. Reuse the matching active goal; change its objective
only through a supported operation. If the host cannot replace an unfinished
objective, disclose that limitation—never mark unfinished work complete to
unlock creation or claim that a displayed prompt was saved.

Use this content structure, adapting detail to the task:

```text
Outcome: What must work, for whom, through which real entry point.
Required scope: Every requested behavior and deliverable, including integration.
Non-goals/authority: What may change and which effects remain prohibited.
Hard refs: Exact project, governing sources and existing state artifacts.
Accepted decisions: Settled product/architecture choices and explicit overrides.
Plan: Dependency-ordered milestones; start at the current unfinished critical path.
Acceptance: Requirement -> falsifying check -> evidence needed -> completion criterion.
Execution: Tools/providers, verification, recovery and review constraints.
Continuation: Keep implementing and verifying authorized ready work after milestones.
Stop rules: Completion, explicit pause/cancel, exhausted configured budget, or a
genuine unresolved authority/product/dependency blocker requiring outside action.
Closeout: Current evidence for every requirement, changed files, remaining risks.
```

## Maintain state without creating another project

Reuse the bound plan/workstream/tracker for a compact acceptance map: requirement,
owner/entry point, dependencies, implementation status, verifier, latest evidence
and remaining gap. Prefer the existing artifact format; Markdown is not required.
Record failed attempts and decisions as well as successes. Update only changed
facts and invalidate evidence when its code, inputs or policy changes. Preserve
this state before compaction or a required yield; do not rewrite an unchanged
plan on every turn or build a new tracker just to run the goal.

## Execute vertical slices

Prioritize a connected user/runtime path over accumulating disconnected helpers.
Test the real entry point, dispatch, effect, verification and result wherever the
claim crosses those boundaries. A reducer, pack, API, dry run or fixture can finish
its own milestone; it cannot stand in for the integrated outcome.

After a milestone passes, immediately continue to the next authorized dependency.
Use concise commentary for progress; a successful small patch is not a reason to
ask “continue?” or stop the overall effort. ONCE remains exactly one unit;
read-only, pause and cancellation retain their authority limits. If a host forces
a turn boundary, checkpoint the exact next action and retain the unfinished goal.

Investigate the first failed verifier, repair within scope, and rerun that check
before widening. Do not weaken assertions, skip a required negative case, or
shrink the requested scope to obtain green. Separate pre-existing/unrelated
failures with current evidence; repair only authorized dependencies. A missing
test is implementation work, not automatically a blocker.

Use coder's provider/session and bounded-recovery policy rather than inventing a
second retry limit here. A live worker's observation timeout is not termination;
inspect and resume the same handle. Distinguish transport retries, product-repair
attempts and evaluation errors. Preserve failure evidence for the next attempt.

## Detect stalls and close honestly

Classify a continuation as progress (code/artifact or decision-changing evidence),
verified wait (a confirmed live handle), or no progress. Repeated status prose,
unchanged searches, unexecuted plans and another disconnected helper do not
close integration gaps. When progress stalls, change the tactic or reduce the
dependency problem; do not reduce the promised outcome. Use host blocked-state
rules and report the exact evidence and smallest outside action when truly stuck.

Before claiming complete, audit every original requirement against current
evidence. Include negative cases, restart/concurrency where relevant, and actual
provider or UI behavior when required. Label unit, integration, live/provider and
promotion evidence separately. Review the integrated change, not just each helper.
Missing required evidence means unfinished. An authorized deferral is recorded as
a scope decision, never silently counted as delivered. Mark complete through the
host only after the entire accepted outcome passes; report blockers honestly.

## Goals are not schedules

Prefer native goal continuation when available. A long-running goal does not
automatically require a timer. Add one only for an explicit watch/schedule request
or an already-authorized continuation policy that needs it, deduplicated against
goal/worker wakes. Respect “no schedules”; unavailable optional scheduling does
not block goal creation. Never activate unrelated automations or new chats.

## Source basis

Adapted from official OpenAI guidance, consulted 2026-09-21:

- [Follow a goal](https://learn.chatgpt.com/use-cases/follow-goals): durable objectives, bounded scope and verifiable stopping conditions.
- [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex): durable specifications/state, milestones, repeated validation and repair.
- [Prompting Codex](https://learn.chatgpt.com/docs/prompting#prompting-codex): desired behavior, relevant context, constraints and verification.

The concrete execution and authority rules above are local skill guidance, not
claims that OpenAI requires a particular tracker, model, retry count or timer.
