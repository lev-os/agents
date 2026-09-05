---
name: goal-exec
description: Use when converting a user request into a Codex goal that will use `/exec`, Lev exec, or Lev Ralph as bounded execution tools.
skill_type: workflow
category: lifecycle
output_template: hud
---

# /goal-exec - Goal Prompt Wrapper For Exec Work

Use this before `create_goal` when the user says "set a goal to `/exec`",
"goal-exec", "run this with Lev Ralph", or similar.

## Rule

The goal objective is the domain outcome, not the exec workflow. `/exec`, Lev,
Ralph, agents, profiles, and runtime surfaces belong in a short `Tools:`
clause.

Do not hardcode a model in this skill or in the goal prompt unless the user
explicitly names a current-run override. Model choice varies by day, project,
adapter, profile, and FlowMind topology. Prefer the project's execution profile
or FlowMind settings over any skill-level recommendation.

## Long-Horizon Goal Navigation

When the user explicitly creates a long-horizon or multi-session goal, read
[recursive wayfinding](../lev/references/recursive.md) and arrange exactly one
navigation heartbeat bound to that goal. Ordinary discussion, planning, or a
bounded goal does not create one. The default cadence is 30 minutes unless
resolved project configuration supplies another interval.

Before creating the goal or heartbeat, resolve and freeze the navigation packet:

```yaml
goal_ref: <stable goal identity; finalize after create_goal>
outcome_ref: <stable outcome>
outcome_map_ref: <durable outcome map>
workstream_ref: <durable workstream>
tracker_binding: <one configured backend and identity>
policy_provenance: <source refs and digest or revision>
tick_policy: outcome_navigation
heartbeat_idempotency_key: <derive from goal_ref + tick_policy>
rolling_horizon_ref: <current projection>
allowed_effects: []
stop_conditions:
  - goal_paused
  - goal_cancelled
  - outcome_confirmed_complete
  - budget_exhausted
  - blocker_requires_human_or_external_change
```

If the tracker is unconfigured, ask once among the mechanically supported
Markdown, Beads, and GitHub choices, then persist the selection. Resume reuses
that binding. An unavailable backend blocks tracker effects; it never causes a
write to another backend. Do not create the goal until this required choice is
resolved.

Before creating the goal, confirm the host exposes a callable thread-heartbeat
automation surface. After goal creation succeeds, finalize `goal_ref`, derive a
stable automation idempotency key from `goal_ref + tick_policy`, then inspect
existing automations by that key. Update the matching heartbeat when present or
create one when absent. Never use a display name alone as identity. If the host
cannot create or update a heartbeat, report that capability gap; never invent
an automation ID or claim scheduling succeeded.

Deduplicate timer and worker-return wakes so only one tick can advance a given
navigation revision. Pause, cancellation, and confirmed completion disable the
heartbeat through the same host surface. Repeated unchanged blocked or
live-worker states stay quiet; surface only a changed failure, a required
decision, or a meaningful route update.

Use this heartbeat meta-prompt with the resolved packet injected by the host.
The heartbeat must consume the packet; it does not look up project config:

```text
Reconcile current evidence against the bound outcome. Retrieve relevant prior
learning. If the selected step is vague or its assumptions failed, run the
recursive wayfinding procedure. Refresh the rolling horizon after material
changes, keeping steps 1-3 actionable and steps 4-10 appropriately coarse.
Select one eligible tick and resume at most one coherent unit within the
supplied authority. Do not duplicate a live worker or infer release, publishing,
or marketing permission. If waiting remains correct, stay quiet. Stop when the
goal is paused, cancelled, or confirmed complete.
```

The heartbeat is a navigation wake, not a second worker. It reconciles evidence
before choosing one deterministic tick: required review, wayfind/research,
authorized execution, due hygiene, or separately authorized release/publish.
It must not rediscover arbitrary config, rewrite an unchanged plan, or treat no
eligible work as completion.

## SDD Variant
If the user passes `--sdd`, use $subagent-driven-development instead of
`/exec`. Model selection stays out of the goal prompt unless the user gives an
explicit current-run override. Use the domain-outcome template, but include the
SDD batch, review, and verification guardrails because subagent runs need a
clear controller contract.

## REQUIRED PRE-CREATE GOAL GATE

Before calling `create_goal`, the agent MUST construct and display the complete
goal prompt and, for a long-horizon goal, its resolved navigation packet.

Together they MUST contain:

1. `Hard refs:` exact absolute paths to every governing plan/spec.
2. `Outcome:` the stable observable domain result.
3. `Plan:` the known outcome-map reference plus an ordered rolling horizon of
   at most ten stable-ID steps; unresolved future work remains explicit fog.
4. `Acceptance:` explicit hard-cut completion criteria.
5. `Batch gates:` tests/checks required after each SDD batch.
6. `Stop rules:` blocker, reviewer, timeout, and dirty-work protections.

The agent MUST NOT call `create_goal`, dispatch a subagent, or modify code when
any required section is absent.

A summary of the plan is not sufficient. Referring to “the hard cutover,”
“the existing plan,” conversation history, or an unnamed plan is invalid. The
stable goal prompt may point to the resolved packet instead of copying its
evolving horizon, but the packet must be displayed and durably referenced.

For `--sdd`, the goal prompt must define:

- PR-sized batch policy.
- Controller-run gate-before-review rule.
- One checkpoint reviewer that covers both spec/drift detection and code
  quality.
- Commit/push policy after approval when the user wants the controller to land
  batches.
- Timeout/no-result handling for subagents.
- Scoped staging rule to preserve unrelated dirty work.

Do not split ordinary review into separate spec and code-quality reviewers.
Do not launch reviewers on partial diffs unless the user explicitly asks for
diagnosis of a known-failing batch.

## Coding standards
The goal prompt is the perfect place to put coding standards. Source repo conventions from:
- dna/* if available
- docs
- .lev/validation-gates.yaml
- if none of that exists, KISS, YAGNI, SRP, and identifying the best programming pattern for the task at hand are good in general
- do not make variable names conversation shaped. For example if the user said "this is the canonical implementation", it doesn't mean you should name classes, variables, or files "CanonicalThing"
- Use first-principles analysis, systems thinking, pre-mortem, reverse
  brainstorming, or a multi-expert lens only when an unresolved design decision
  or material risk benefits from it. Do not repeat these exercises for settled,
  bounded implementation.
- Source DDD, hex architecture, or clean-code patterns only when the task or
  repository already requires them. Do not add architecture ceremony to a goal
  prompt.

Keep the goal packet compact: outcome, owned scope, exclusions, accepted source
refs, acceptance checks, and stop conditions. Point to accepted artifacts instead
of restating them. Name work owned by another task so the goal cannot absorb it.

## Template

```text
<domain task>.
Tools: /exec and <surface/profile> as bounded execution surfaces.
Guardrails: one slice at a time; stop on reviewer advice, blocker, failed
declared gate, or no-op/advice loop; report diagnostics instead of retrying.
```

The goal objective carries the domain outcome and hard references. Put the
ordered rolling horizon, acceptance, and workflow guardrails in the resolved
navigation packet so they can evolve without rewriting the stable objective.
Do not invent acceptance criteria or hide workflow mechanics inside the outcome.

## Good

```text
Billing webhook idempotency hardening for production checkout events.
Tools: /exec and the project-selected Lev exec profile or FlowMind topology as
bounded execution surfaces.

Task: ensure payment, refund, and subscription webhook handlers can safely
receive duplicate, retried, and out-of-order provider events without
double-writing ledger rows, double-sending customer notifications, or hiding
failed reconciliation states.

Refs: billing webhook router, ledger write path, provider event fixtures,
existing reconciliation tests, production incident notes if present.

Cross-cutting concerns: preserve auditability of every received event; keep
provider-specific parsing separate from domain reconciliation; maintain
backwards compatibility for existing ledger records; avoid schema churn unless
the current model cannot represent idempotency state clearly.

Out of scope: provider migration, billing UI changes, historical data
backfills, notification copy changes, broad ledger refactors, and performance
work unrelated to duplicate-event safety.

Model policy: resolve adapter/model from the selected execution artifact,
FlowMind file, or project `.lev/exec-profiles/`; do not override from the goal
prompt unless the user explicitly gives a current-run model.

Guardrails: one slice at a time; declare the gate before each dispatch; stop on
reviewer advice, blocker, failed declared gate, or no-op/advice loop; report
diagnostics instead of retrying.

Escalation policy: if the same blocker appears twice, tests show ambiguous
money movement, or implementation requires a schema/backfill decision, stop and
return the smallest evidence packet needed for human review.
```

## SDD Prompt Shape

When using `--sdd`, keep the objective domain-shaped and put the subagent
mechanics in guardrails:

```text
<domain task> through PR-sized implementation batches.
Tools: subagent-driven-development as the implementation lane; project task
validation, package tests/typechecks, and real runtime/e2e gates as bounded
verification surfaces.

Batch policy: choose the largest safe, coherent batch in dependency order. A
batch may be one risky slice or several small compatible slices. Review
immediately if the batch touches public API, lifecycle/session/process
management, cross-package boundaries, more than the declared changed-line cap,
a growing or unfocused file, or any failed/changed verifier.

Controller policy: one coding subagent completes one coherent batch. The
controller then runs declared gates locally. Only after gates pass does one
checkpoint reviewer review the final batch for spec drift, boundaries, code
quality, tests, and naming. If declared gates fail, return to implementation or
fix directly before review.

Landing policy: when the project goal says pass = commit/push, stage only
scoped files, follow the repo commit protocol, push, and preserve unrelated
dirty work.

Escalation policy: stop on blocker, same blocker twice, unusable subagent result
after one retry, reviewer finding that changes architecture/public contract, or
runtime evidence that cannot support the claimed behavior.
```

## Model Selection

Model selection belongs to the execution surface, not this wrapper.

Before dispatching, follow `/exec` discipline:

1. Run `lev exec --help` in the target project before using model, profile,
   flow, or binding flags. Never guess current CLI flags or aliases.
2. Read the selected task `execution.yaml`, FlowMind file, and/or exec profile.
   Prefer `--flow=<path>` or `--profile=<id>` when the project declares one.
3. Let the exec profile carry adapter/model policy. Project
   `.lev/exec-profiles/` overlays plugin profiles; explicit CLI flags override
   profile values only when the user or current execution artifact requires it.
4. If no profile or FlowMind policy exists, do not invent a model in
   `goal-exec`. Route to `/propose` or diagnostics for a profile/policy
   decision, or use the current `lev exec --help`/binding output as the only
   live authority.
5. Dogfood binding resolution before real dispatch when practical:
   `lev exec "binding smoke" --profile=<id> --dry-run --dry-run-resolve-binding`.

## Bad

- "Execute all slices through the Exec lane."
- "Validate readiness, run slices in dependency order, collect receipts, route
  blockers, and close with verified status."
- "Keep working until all slices are done."
- "Run with composer-2.5-fast because this skill says so."

Those prompts make the workflow itself the objective and encourage spin.

## Dispatch Discipline

- Create a goal only when the user explicitly asks for a goal.
- Do not set a token budget unless the user gives one.
- Use one slice per dispatch unless the user explicitly asks for a batch and
  the execution artifact marks the slices parallel-safe.
- Reviewer advice is terminal for that dispatch. Route to diagnostics/propose,
  not another implementation worker.
- Same blocker twice is a stop condition.
