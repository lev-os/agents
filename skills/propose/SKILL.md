---
name: propose
description: Use when compiling aligned simple intent or a source-faithful Lev plan into a reviewable slice map or one execution-ready Lev task. Compatibility alias for lev-plan; it does not create or repair broad plans.
---

# /propose - Compatibility Alias

`/propose` and `skill://propose` are kept for existing callers. Their review,
map, and emit semantics live in `skill://lev-plan`; this file holds no workflow.

## Forward Once

Load `skill://lev-plan` and run the mode below, passing the caller's arguments,
flags, source refs, workstream, and authorization unchanged.

| Invocation | lev-plan mode | Result |
|---|---|---|
| `/propose` | Review | Reviews alignment and recommends one vertical slice |
| `/propose map`, `/propose all slices` | Map | Compact slice map only; never creates task folders |
| `/propose emit <slice-id>` | Emit | Exactly one `{dna.yaml,execution.yaml}` task packet |

`--full` and the `emit`, `apply`, `edit`, and `patch` authorizations keep their
meaning there.

`lev-plan` runs `lev find` first for existing plans, designs, decisions and
ideas on the topic; pass the topic words along.

The forward happens once and in one direction. `lev-plan` answers the caller
directly, and its verdict, output, and next route are final: a `needs_plan` or
`needs_interview` result continues inside `lev-plan` or its named route, never
back through `/propose`.

## Work Link

Lifecycle lane: Plan (alias of `/lev-plan`)
Entity movement: `captured | designed | planned | aligned -> proposed | execution_ready | needs_interview | needs_plan`, performed by `/lev-plan`
Workstream: resolved by `/lev-plan` before task writes
Upstream: any caller of `/propose`
Downstream: `/lev-plan`
Router: `/work`
