---
name: dump
description: Use when a long brainstorm or brain dump needs deep capture, prior-art routing, and durable next states.
skill_type: alias
category: lifecycle
output_template: hud
---

# /dump - Action Wrapper for /capture --deep

`/dump` is not a separate capture engine. It invokes `/capture --deep`, renders
the shared lifecycle ledger, then takes the obvious next lifecycle action only
when the ledger proves the row is durable and write-authorized.

## Work Link

Lifecycle lane: Shape -> Plan
Entity movement: `memory -> captured | proposed | execution_ready | blocked`
Workstream: resolve active workstream before writing capture artifacts
Upstream: conversation, `/work`
Downstream: `/capture --deep`, `/prior-art`, `/propose`, `/exec`
Router: `/work`
HUD: end with `🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}`

## Protocol

```yaml
steps:
  - id: invoke_capture_deep
    action: Run the /capture deep-mode inventory and fidelity loop.
    validation: "Every topic has a durable route or blocker and appears in the shared capture ledger."
    on_failure: "Return to /capture with the unresolved bucket."

  - id: render_capture_ledger
    action: Render the same <capture-results> lifecycle ledger used by /capture.
    validation: "The table shows compiled_intent, current_location, artifact_ref, route_state, fidelity, next_route, and blocker for every item."
    on_failure: "Do not route. Show the missing ledger fields."

  - id: probe_prior_art
    action: Search existing work per topic before creating new artifacts.
    validation: "Each new proposal has no better existing home."
    on_failure: "Route to /prior-art and stop proposal creation for that topic."

  - id: route_next
    action: Take the next action for shovel-ready rows: /exec for execution_ready, /propose for aligned captured work, /interview for ambiguous rows.
    validation: "No routed item has current_location=memory without artifact_ref, blocker, or explicit write authorization."
    on_failure: "Show the blocked items and missing gate."
```

## Output

First render the exact `/capture --deep` ledger block:

<capture-results>
## /dump results

### Ledger
| ID | Topic | Compiled Intent | Current Location | Artifact | Route State | Fidelity | Next Route | Blocker |
|---|---|---|---|---|---|---:|---|---|
| {intent_id} | {topic} | {compiled_intent} | {current_location} | {artifact_ref} | {route_state} | {fidelity_pct} | {next_route} | {blocker} |

### In Memory
{items_that_could_not_be_written}

### Blocked
{blocked_items}

### Crystallizing
{transitioning_items}
</capture-results>

Then show action stats:

| Metric | Count |
|---|---|
| Total inventoried | N |
| Routed to existing files | N |
| New proposals created | N |
| Ready for /exec | N |
| Needs /interview | N |
| Blocked | N |

## Red Flags

- "Dump can skip prior-art."
- "This is just a list."
- "We can leave low-priority items in memory."
- "Dump should implement its own capture protocol."
- "Dump can skip the shared ledger because it routes immediately."
- "A metric table is enough to prove what is on disk."
- "Dump can turn proposal language into writes without a canon write gate."

## Related

- `/capture --deep` owns inventory, fidelity, durable artifact writes, the canon write gate, and the shared ledger.
- `/prior-art` avoids duplicate artifacts.
- `/propose` creates task DNA and execution plans.
- `/exec` handles execution-ready entities.
