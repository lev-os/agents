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

## Pre-create Gate

Before calling `create_goal`, display the complete goal prompt. It must contain:

1. `Hard refs:` exact absolute paths to governing plans/specs.
2. `Plan:` the complete ordered execution sequence.
3. `Acceptance:` hard-cut observable completion criteria.
4. `Batch gates:` controller checks after each applicable batch.
5. `Stop rules:` blockers, review, timeout, identity/session, and dirty-work protections.

Do not create a goal, dispatch a worker, or modify code while one is absent.
Create a goal only with explicit user authorization and set a token budget only
when the user supplies one.

## Goal Prompt

Keep workflow out of the objective and place the resolved flags in one short
tools clause:

```text
<domain outcome>.
Tools: $coder <resolved flags> as the bounded execution surface.

Hard refs: <absolute paths>.
Plan: <ordered 1-N sequence>.
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
