---
name: horizon
description: Use when the operator explicitly invokes /horizon or skill://horizon for a long-horizon planning brief.
---

# /horizon - Long-Horizon Launch Brief (Experiment)

`/horizon` is the direct entry to the horizon method, which lives in the plan
skill. Run the Fit Check below first. When it passes,
load [the horizon method](../lev-plan/references/horizon.md) and follow it
from Run Size to the rendered brief. The method cites rules of the plan skill by link
(sections of `../lev-plan/SKILL.md` and `execution-packet.md`): on this direct
call, read each cited section when you reach its link, before you act on it.

For non-trivial project work, load [Project Context](../lev/references/project-context.md)
before project-specific lookup.

## Fit Check

Run horizon when one operator outcome, its boundaries, and a relevant verifier
can be named. Aligned intent goes straight to the brief: synthesize settled
decisions and ask only about an unresolved choice that changes scope or
acceptance. Otherwise route once:

| Signal | Route |
|---|---|
| Conversation-only intent, no source ledger | `/capture` |
| Unresolved product, architecture, or authority decision | `/interview` (`skill://arch` for a technical boundary) |
| Unknown answer that a prototype would settle | `skill://poc` |
| Broad, migration, or cross-authority work with no plan | lev-plan Compile with the [plan template](../work/templates/plan.md); the brief cites that plan |
| Packet preview | Not a route away: load the method and render it in this run through the method's packet reference; no repeated shaping hop |
| Slice map or task-folder emission | lev-plan Map or Emit directly, passing the brief; emission stays with Emit |

## Work Link

Lifecycle lane: Plan (experiment beside `/lev-plan`)
Entity movement: `aligned | planned -> proposed | needs_interview | needs_plan`; execution readiness stays with lev-plan Emit
Workstream: resolved as `/lev-plan` does before any durable write
Upstream: `/capture`, `/interview`, `.lev/pm/designs/*`, `.lev/pm/plans/*`, aligned bounded intent
Downstream: `/lev-plan` (Compile, Map, Emit), `skill://poc`, `/interview`, `/exec` after a validated packet
Router: `/work`
