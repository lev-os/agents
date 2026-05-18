---
name: dump
description: Use when a long brainstorm or brain dump needs deep capture, prior-art routing, and durable next states.
skill_type: alias
category: lifecycle
output_template: hud
---

# /dump - Alias for /capture --deep

`/dump` is not a separate lifecycle engine. It invokes `/capture --deep`, then
routes each captured entity through prior-art, propose, or exec.

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
    validation: "Every topic has a durable route or blocker."
    on_failure: "Return to /capture with the unresolved bucket."

  - id: probe_prior_art
    action: Search existing work per topic before creating new artifacts.
    validation: "Each new proposal has no better existing home."
    on_failure: "Route to /prior-art and stop proposal creation for that topic."

  - id: route_next
    action: Send shovel-ready entities to /exec and the rest to /propose or /interview.
    validation: "No item remains only in memory."
    on_failure: "Show the blocked items and missing gate."
```

## Output

Show the `/capture --deep` three-bucket delta plus routing stats:

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

## Related

- `/capture --deep` owns the implementation.
- `/prior-art` avoids duplicate artifacts.
- `/propose` creates task DNA and execution plans.
- `/exec` handles execution-ready entities.
