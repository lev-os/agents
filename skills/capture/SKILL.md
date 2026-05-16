---
name: capture
description: Use when inventorying conversation state into durable artifacts, routing shovel-ready items toward exec, or deep-processing a brain dump.
skill_type: workflow
category: lifecycle
output_template: hud
triggers:
  - capture
  - dump
---

# /capture - Shape to Plan

Inventory conversation state, write durable artifacts, and route each entity to
its next lifecycle owner. `/dump` is `capture --deep`.

## Work Link

Lifecycle lane: Shape -> Plan
Entity movement: `memory -> captured | proposed | blocked`
Workstream: resolve active workstream before writing capture artifacts
Upstream: conversation, `/dump`, `/work`
Downstream: `/prior-art`, `/propose`, `/exec`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Protocol

```yaml
steps:
  - id: inventory
    action: List ideas, decisions, follow-ups, artifacts, blockers, and promises.
    validation: "Every item has a topic and provisional lifecycle state."
    on_failure: "If the thread is too large, bucket by topic and continue."

  - id: classify
    action: Assign state and route.
    validation: "Each item is memory, captured, transitioning, blocked, done, or rejected."
    on_failure: "Unknown state stays in memory and becomes the first output bucket."

  - id: prior_art_probe
    action: For non-trivial items, search existing work before creating new files.
    validation: "Existing home found, or 'no prior art found' is stated."
    on_failure: "Route to /prior-art before proposing new artifacts."

  - id: write_artifacts
    action: Save in-memory items to the selected workstream or .lev/pm route.
    validation: "No writable item remains only in conversation memory."
    on_failure: "List only the unwritten items under In Memory with blocker."

  - id: score_fidelity
    action: Score captured fidelity before advancement.
    validation: "fidelity >= 0.8 for /propose or /exec routing."
    on_failure: "Re-capture at higher zoom or route to /interview."

  - id: show_delta
    action: Show only in-memory, blocked, and crystallizing items plus stats.
    validation: "Stable captured/done items are omitted from the visible delta."
    on_failure: "Rewrite output as the three buckets."
```

## Routes

| Item | Route |
|---|---|
| Constraint, invariant, gate, policy | DNA-backed task via `/propose` |
| Design-grade framing | `.lev/pm/designs/` then `/propose` |
| Execution-ready task with verifier and write scope | `/exec` |
| Provenance or duplicate check needed | `/prior-art` |
| Ambiguous intent or boundary | `/interview` |
| Workstream identity missing | `/ws` |

## Deep Mode

`/capture --deep` and `/dump` add a convergence loop:

```yaml
deep_capture:
  repeat_until: "all writable items have stored fidelity >= in-memory fidelity"
  loop:
    - inventory by topic
    - prior-art per topic
    - write or update durable route
    - score fidelity
    - enrich weak captures
  circuit_breaker: "3 iterations without fidelity improvement"
```

## Fidelity Gate

```
fidelity = 0.30*detail_preservation
         + 0.25*relationship_preservation
         + 0.20*source_attribution
         + 0.15*neighbor_context
         + 0.10*actionability
```

`fidelity >= 0.8` can advance to `/propose` or `/exec`; lower scores stay in
capture, prior-art, or interview.

## Durable Artifact

Write capture reports near the workstream:

```yaml
path: .lev/pm/workstreams/<ws-id>/captures/YYYYMMDD-capture-sweep.yaml
schema:
  date: YYYY-MM-DD
  workstream: <ws-id>
  items:
    - topic: "<summary>"
      stage: captured | proposed | blocked | executing | rejected
      fidelity: 0.0
      route: "<path or skill>"
      priority: P0 | P1 | P2 | P3
      unblocks: []
```

Markdown capture reports are projections only when useful.

## Output

<capture-results>
## /capture results

### In Memory
{items_that_could_not_be_written}

### Blocked
{blocked_items}

### Crystallizing
{transitioning_items}

### Stats
- Total inventoried: {n}
- In memory captured: {n}
- Transitioning: {n}
- Blocked: {n}
</capture-results>

## Red Flags

- "I'll show the list first and save after approval."
- "This follow-up is obvious enough to leave in chat."
- "Done items should be listed again."
- "Prior art can wait until proposal."

## Related

- `/work` routes lifecycle lanes.
- `/dump` is a focused alias for `/capture --deep`.
- `/prior-art` finds existing homes.
- `/propose` turns captured/aligned items into task DNA.
- `/exec` runs shovel-ready items.
