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

## SDD Variant
If the user passes `--sdd`, use $subagent-driven-development instead of
`/exec`. Model selection stays out of the goal prompt unless the user gives an
explicit current-run override. Use the domain-outcome template, but include the
SDD batch, review, and verification guardrails because subagent runs need a
clear controller contract.

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
- always think from first principles, systems thinking, do a premortum + reverse brainstorming exercise
- always adopt a multi {domain} expert lens, "what would a team of n {domain} experts say"?
- on naming/patterns: source DDD, hex architecture and clean code primitives, compile user/task intent > ground up design thinking > coding standards / guiding principles that you want to bake in to the guard rails below

## Template

```text
<domain task>.
Tools: /exec and <surface/profile> as bounded execution surfaces.
Guardrails: one slice at a time; stop on reviewer advice, blocker, failed
declared gate, or no-op/advice loop; report diagnostics instead of retrying.
```

The goal objective should carry only the source refs and stop rules. It should
not restate the whole design, invent acceptance criteria, or summarize workflow
mechanics as the objective.

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
