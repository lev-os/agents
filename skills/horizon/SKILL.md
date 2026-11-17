---
name: horizon
description: Use when the operator explicitly invokes /horizon or skill://horizon for a long-horizon planning brief.
---

# /horizon - Compatibility Alias

`/horizon` and `skill://horizon` are kept for existing callers. The horizon
method is now part of every plan of `skill://lev-plan`; this file holds no
workflow.

## Forward Once

Load `skill://lev-plan` (the Skill tool with `lev-plan`; a host with no Skill
tool opens `../lev-plan/SKILL.md`) and run the mode below, passing the caller's arguments,
topic words, flags, source refs, workstream, and authorization unchanged.

| Invocation | lev-plan mode |
|---|---|
| `/horizon` with no write authorized | Review; render the plan body of lev-plan's plan template in the response as the brief |
| `/horizon` with plan writes authorized | Compile, or Deepen when a matching plan exists |
| A packet preview | Review, with the preview rendered from lev-plan's packet reference, labeled unvalidated and unemitted |

Treat the run as long: read lev-plan's long-horizon planning reference when
its conditions hold.

The forward happens once and in one direction. `lev-plan` answers the caller
directly, and its verdict, output, and next route are final.

## Work Link

Lifecycle lane: Plan (alias of `/lev-plan`)
Entity movement: performed by `/lev-plan`
Workstream: resolved by `/lev-plan` before any durable write
Upstream: any caller of `/horizon`
Downstream: `/lev-plan`
Router: `/work`
