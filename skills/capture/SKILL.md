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

## Canon Write Gate

If the user asks "what would you edit", "show me", "audit", "plan", "pass2",
"recommend", or "how would you", do not mutate canon files. Render the ledger
and proposed changes only. Write artifacts only when the user explicitly asks
to apply, edit, patch, emit, or create a durable capture.

## Protocol

```yaml
steps:
  - id: inventory
    action: Inventory ideas, decisions, follow-ups, artifacts, blockers, promises, and proof/QA risks.
    validation: "Every item has a topic and provisional lifecycle state."
    on_failure: "If the thread is too large, bucket by topic and continue."

  - id: classify
    action: Compile user/source prose into agent-operational intent, state, and route.
    validation: "Each item has compiled_intent, route_state, and next_route."
    on_failure: "Unknown state stays in memory and becomes the first output bucket."

  - id: prior_art_probe
    action: For non-trivial items, search existing work before creating new files.
    validation: "Existing home found, or 'no prior art found' is stated."
    on_failure: "Route to /prior-art before proposing new artifacts."

  - id: seed_qa_contract
    action: For non-trivial items, create a QA seed before route advancement.
    validation: "Runtime, agentic, promotion, cleanup, fallback, or boundary-risk items name proof_required, highest_risk_claim, scenario_classes, and owner-local placement."
    on_failure: "Keep the item captured and route to /interview or /propose before /exec."

  - id: write_artifacts
    action: Save in-memory items to the selected workstream or .lev/pm route.
    validation: "No writable item remains only in conversation memory."
    on_failure: "List only the unwritten items under In Memory with blocker."

  - id: score_fidelity
    action: Score captured fidelity before advancement.
    validation: "fidelity >= 0.8 for /propose or /exec routing."
    on_failure: "Re-capture at higher zoom or route to /interview."

  - id: reconcile_capture_ledger
    action: Build the lifecycle ledger before routing or final output.
    validation: "Every item has intent_id, compiled_intent, current_location, artifact_ref, route_state, fidelity, next_route, and blocker."
    on_failure: "Do not advance routes. Show unresolved ledger rows under In Memory or Blocked."

  - id: show_delta
    action: Show the full ledger table plus in-memory, blocked, and crystallizing buckets.
    validation: "The user can see what is truly on disk, what remains only in memory, and what changed this turn."
    on_failure: "Rewrite output as the shared <capture-results> ledger."
```

## Routes

| Item | Route |
|---|---|
| Constraint, invariant, gate, policy | DNA-backed task via `/propose` |
| Brief/document-artifact framing | `/brief` -> `/interview --auto` -> `.lev/pm/designs/` then `/propose` |
| Design-grade framing | `/interview --auto` -> `.lev/pm/designs/` then `/propose` |
| Runtime, agentic, promotion, cleanup, fallback, or boundary-risk item | `/interview` or `/propose` with `qa_seed` |
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

## Lifecycle Ledger Contract

The lifecycle ledger is the core visibility primitive at lifecycle trigger
points. `/capture`, `/capture --deep`, and `/dump` all render the same table
before claiming route advancement.

| Field | Meaning |
|---|---|
| `intent_id` | Stable row id for this lifecycle turn |
| `topic` | Short label for the source material |
| `compiled_intent` | Agent-operational interpretation, not raw user prose |
| `current_location` | `disk`, `memory`, `both`, `external`, or `unknown` |
| `artifact_ref` | Path or durable id; `none` if only in memory |
| `route_state` | `in_memory`, `captured`, `proposed`, `execution_ready`, `blocked`, `done`, or `rejected` |
| `fidelity` | Preservation score plus reason if below 0.8 |
| `next_route` | `/interview`, `/prior-art`, `/propose`, `/exec`, `/close`, or `none` |
| `blocker` | `null` or the reason this row cannot advance |

No route can advance if a row has `current_location: memory` without a blocker
or planned destination. This prevents hidden in-chat state from being mistaken
for durable work.

## Durable Artifact

Write capture reports near the workstream:

```yaml
path: .lev/pm/workstreams/<ws-id>/captures/YYYYMMDD-capture-sweep.yaml
schema:
  date: YYYY-MM-DD
  workstream: <ws-id>
  ledger:
    - intent_id: "<stable row id>"
      topic: "<summary>"
      compiled_intent: "<agent-operational interpretation>"
      current_location: disk | memory | both | external | unknown
      artifact_ref: "<path, durable id, or none>"
      route_state: in_memory | captured | proposed | execution_ready | blocked | done | rejected
      fidelity: 0.0
      next_route: "<skill/path/none>"
      blocker: "<reason or null>"
  items:
    - topic: "<summary>"
      stage: captured | proposed | blocked | executing | rejected
      fidelity: 0.0
      route: "<path or skill>"
      priority: P0 | P1 | P2 | P3
      unblocks: []
      qa_seed:
        proof_required: true | false
        proof_gate_state: needs_proof_design | needs_proof_gates | needs_runtime_qa | needs_quality_review | needs_close_verdict | proof_blocked | none
        highest_risk_claim: "<claim or null>"
        scenario_classes: []
        owner_local_test_placement: "<module path or null>"
        shared_testing_boundary: "core/testing is a library/evaluator source, not the home for module-specific tests"
```

Markdown capture reports are projections only when useful.

## Output

<capture-results>
## /capture results

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

### Stats
- Total inventoried: {n}
- In memory captured: {n}
- Transitioning: {n}
- Blocked: {n}
- Ledger rows: {n}
</capture-results>

## Red Flags

- "I'll show the list first and save after approval."
- "This follow-up is obvious enough to leave in chat."
- "Done items should be listed again."
- "Prior art can wait until proposal."
- "The table is optional because I wrote the artifact."
- "A routed item can stay only in chat memory."
- "Copying user prose is the same as compiling intent."
- "What would you edit means patch it now."

## Related

- `/work` routes lifecycle lanes.
- `/dump` is a focused alias for `/capture --deep`.
- `/brief` turns conversation context into a lifecycle artifact via `/interview --auto`.
- `/prior-art` finds existing homes.
- `/propose` turns captured/aligned items into task DNA.
- `/exec` runs shovel-ready items.
