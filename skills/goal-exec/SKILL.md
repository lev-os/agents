---
name: goal-exec
description: Convert an explicit user request into a Codex goal and pass its chosen coder, Lev, LazyCodex, SDD, or Fable execution flags to $coder.
---

# Goal Exec

Use this only before `create_goal` when the user explicitly asks to set or run a
goal. The goal describes the domain outcome. Load `skill://coder`; `$coder` owns
execution mechanics. For `--lev`, also load `skill://exec` and resolve the flow
as `lev://exec/<flow>` rather than treating the skill pointer as a runtime URI.

## Flags

```text
$goal-exec [--coder] [--lev] [--sdd[=checkpoint|pair]] [--lazycodex] [--fable]
```

| Flag | Contract |
|---|---|
| `--coder` | Load `$coder`; use its direct single-worker mode unless another topology flag is present. |
| `--lev` | Pass `--lev`; execution must use `lev exec` and project FlowMind/profile policy. |
| `--sdd` | Pass `--sdd=checkpoint`. |
| `--sdd=checkpoint|pair` | Pass the exact SDD mode. Reject other values. |
| `--lazycodex` | Pass through; use the inline LazyCodex protocol in `$coder`. |
| `--fable` | Pass through; prefer the configured Fable reviewer profile. |

`--coder` selects the execution owner. The remaining flags refine `$coder` and
must be copied unchanged into the goal's `Tools:` clause. `--sdd`, `--lazycodex`,
or `--fable` imply `--coder`. `--fable` requires SDD because it selects the
reviewer, never the coder. Reject contradictions instead of silently dropping
or substituting flags.

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

## Pre-create Gate

Before calling `create_goal`, display the complete goal prompt and, for a
long-horizon goal, its resolved navigation packet. Together they must contain:

1. `Hard refs:` exact absolute paths to governing plans/specs.
2. `Outcome:` the stable observable domain result.
3. `Plan:` the ordered execution sequence; for long-horizon work, the outcome-map
   reference and at most ten stable-ID rolling-horizon steps with unresolved fog.
4. `Acceptance:` hard-cut observable completion criteria.
5. `Batch gates:` controller checks after each applicable batch.
6. `Stop rules:` blockers, review, timeout, identity/session, and dirty-work protections.

Do not create a goal, dispatch a worker, or modify code while one is absent.
Create a goal only with explicit user authorization and set a token budget only
when the user supplies one.

For long-horizon work, the stable objective may reference the displayed durable
navigation packet rather than repeat its evolving horizon. Do not invent
acceptance criteria or replace exact references with conversation shorthand.

For SDD, carry the selected `$coder` topology into the packet: PR-sized batches,
controller gates before review, one reviewer covering spec and code quality,
timeout/no-result handling, and scoped staging with the authorized commit/push
policy. Do not review partial diffs unless diagnosis is explicitly requested.

Keep scope, exclusions, source refs and other tasks' ownership explicit. Use
first-principles analysis, premortems or expert lenses only for unresolved
choices or material risk; architectural patterns come from the task or repo.

## Goal Prompt

Keep workflow out of the objective and place the resolved flags in one short
tools clause:

```text
Outcome: <domain outcome>.
Tools: $coder <resolved flags> as the bounded execution surface.

Hard refs: <absolute paths>.
Plan: <ordered sequence or durable navigation packet and rolling horizon>.
Acceptance: <observable hard cuts>.
Batch gates: <commands and runtime checks>.
Stop rules: stop on a failed gate, material decision, unavailable required
identity/profile, unusable explicit session after one focused retry, the same
blocker twice, or scope conflict with existing work.
```

Source coding standards from the nearest project instructions, DNA/rules,
docs, and `.lev/validation-gates.yaml`. Model selection belongs to the selected
project execution profile or FlowMind binding. The goal may name a model only
for an explicit current-run user override.

Before emitting `--lev`, inspect `lev exec --help`, the selected task
`execution.yaml`, FlowMind file, and project `.lev/exec-profiles/`. Prefer a
declared `--flow` or `--profile`; never guess current flags or model aliases.
