---
name: capture
description: Use when inventorying conversation state into durable artifacts with an operator-visible source-fidelity table, routing faithful items toward interview, planning, proposal, or execution, or deep-processing a brain dump.
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

## Entity Reconciliation

After authorized material progress, reconcile touched and causally affected
artifacts before routing, handoff, or final response. Track entity ref,
island/provider locator (a path for file storage), basis/evidence, and the
reason/action due. Update through the verified owning CLI/adapter; use a
write-authorized skill fallback only when that operation is unavailable.
Record updated, no_change(reason), or blocked(reason), preserving unresolved
refs. Reading or mentioning a path alone creates no update obligation.
Read-only work reports pending changes only. Reminders grant no write authority;
task status stays with the bound tracker. Update only artifacts whose content
or evidence changed; do not rewrite every referenced document.

## Work Link

Lifecycle lane: Shape -> Plan
Entity movement: `memory -> captured | proposed | blocked`
Workstream: resolve active workstream before writing capture artifacts
Upstream: conversation, `/dump`, `/work`
Downstream: `/prior-art`, `/interview`, `/lev-plan`, `/propose`, `/exec`
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
    action: Score each new or materially changed captured row against its source before advancement. Reuse an accepted score and source mapping when neither the source nor compiled intent changed.
    validation: "Every material row has fidelity_components, fidelity_note, and fidelity >= 0.8; no material constraint, non-goal, decision boundary, relationship, or acceptance condition is silently lost."
    on_failure: "Re-capture at higher zoom or route to /interview."

  - id: reconcile_capture_ledger
    action: Build or update only changed lifecycle ledger rows before routing or final output; preserve accepted unchanged rows by reference.
    validation: "Every changed item has the full ledger fields; unchanged accepted items retain a valid referenced row."
    on_failure: "Do not advance routes. Show unresolved ledger rows under In Memory or Blocked."

  - id: show_delta
    action: Always show the source-fidelity table plus the compact lifecycle delta. The table is the operator proof that conversation intent reached disk; it is not optional response detail.
    validation: "The user can see every material intent row, destination, fidelity score, loss/narrowing note, route state, and next owner without opening the durable artifact."
    on_failure: "Rewrite output as <capture-results> with the fidelity table present."
```

## Routes

Select routes using the active domain overlay. These are next-owner suggestions,
not permission to execute. Show only applicable rows as a numbered table when a
choice is needed; otherwise name the single next route using `skill://<name>`.

| Item | Route |
|---|---|
| Constraint, invariant, gate, policy | `skill://lev-plan` for broad changes; `skill://propose` for a bounded SDLC change |
| Brief or design framing | `skill://interview`; preserve the resulting design before choosing the next owner |
| Broad, multi-slice, migration, architecture, or roadmap work | `skill://lev-plan`; preserve the whole effort before task slicing |
| Runtime, agentic, promotion, cleanup, fallback, or boundary-risk item | `skill://interview` or SDLC `skill://propose` with `qa_seed` |
| Coding slice ready for contract review | `skill://propose` |
| Authorized execution with sufficient scope, claims, and checks | `skill://exec`; non-coding may use a sufficient plan without `propose` |
| Provenance or duplicate check needed | `skill://prior-art` |
| Ambiguous intent or boundary | `skill://interview` |
| Workstream identity missing | `skill://ws` |
| Different domain or no matching owner | `skill://lev` |

## Deep Mode

`/capture --deep` and `/dump` add a convergence loop:

```yaml
deep_capture:
  repeat_until: "all writable items have stored fidelity >= in-memory fidelity and every material source row has a visible destination"
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

`fidelity >= 0.8` clears the capture preservation floor; `plan_required` still
controls the next route. Broad work advances to `/lev-plan`, not directly to
proposal or execution. Lower scores stay in capture, prior-art, or interview.

Fidelity is a weak-link gate, not permission to average away a missing material
constraint. A row with a silent loss in scope, non-goals, decision boundaries,
acceptance, relationships, or authority stays captured even if its weighted
number is above 0.8.

## Source Fidelity Table

Render this table in every non-trivial capture response. One row may summarize
several sentences only when they share one destination and lifecycle route.

| Field | Meaning |
|---|---|
| `intent_id` | Stable identity carried into plans, proposals, and tasks |
| `source_refs` | Conversation turn, file, URL, or prior durable artifact supporting the row |
| `source_intent` | Concise statement of the user's goal, constraint, non-goal, decision, or acceptance requirement |
| `destination_ref` | Exact durable destination, or `memory` with a blocker |
| `preservation` | `preserved`, `narrowed-approved`, `deferred-explicit`, `conflict`, or `lost` |
| `fidelity_components` | Detail, relationships, attribution, neighbor context, and actionability scores |
| `fidelity` | Weighted score from the formula above |
| `fidelity_note` | What changed, narrowed, remains absent, or needs human confirmation |

No row marked `lost` advances. `narrowed-approved` requires an explicit user or
source decision; agent simplification alone is not approval.

## Lifecycle Ledger Contract

The lifecycle ledger is the core visibility primitive at lifecycle trigger
points. `/capture`, `/capture --deep`, and `/dump` all build the same ledger
before claiming route advancement. The default human response renders its
delta; `--full`, audit, and debug may render the complete table.

| Field | Meaning |
|---|---|
| `intent_id` | Stable row id for this lifecycle turn |
| `topic` | Short label for the source material |
| `source_refs` | Conversation/file/artifact anchors used to re-derive the row |
| `source_intent` | Concise source-faithful goal, constraint, non-goal, decision, acceptance, or relationship |
| `compiled_intent` | Agent-operational interpretation, not raw user prose |
| `relationships` | Dependencies, conflicts, supersession, grouping, and ordering that must survive routing |
| `current_location` | `disk`, `memory`, `both`, `external`, or `unknown` |
| `artifact_ref` | Path or durable id; `none` if only in memory |
| `destination_ref` | Next durable design, plan, proposal, task, or existing authority |
| `route_state` | `in_memory`, `captured`, `planned`, `proposed`, `execution_ready`, `blocked`, `done`, or `rejected` |
| `fidelity` | Preservation score plus reason if below 0.8 |
| `fidelity_components` | Five component scores used to derive fidelity |
| `fidelity_note` | Explicit preservation, narrowing, conflict, deferment, or loss note |
| `plan_required` | True for broad/multi-slice/migration/architecture/roadmap work |
| `next_route` | `/interview`, `/prior-art`, `/lev-plan`, `/propose`, `/exec`, `/close`, or `none` |
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
      source_refs: []
      source_intent: "<source-faithful requirement>"
      compiled_intent: "<agent-operational interpretation>"
      relationships: []
      current_location: disk | memory | both | external | unknown
      artifact_ref: "<path, durable id, or none>"
      destination_ref: "<path, durable id, memory, or none>"
      route_state: in_memory | captured | planned | proposed | execution_ready | blocked | done | rejected
      fidelity: 0.0
      fidelity_components:
        detail_preservation: 0.0
        relationship_preservation: 0.0
        source_attribution: 0.0
        neighbor_context: 0.0
        actionability: 0.0
      fidelity_note: "<preserved, narrowed, deferred, conflict, or loss note>"
      plan_required: true | false
      next_route: "<skill/path/none>"
      blocker: "<reason or null>"
  items:
    - topic: "<summary>"
      stage: captured | planned | proposed | blocked | executing | rejected
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

Render the Markdown inside this template; do not print the XML wrapper tags.

<capture-results>
## /capture results

### Source Fidelity

| ID | Source intent | Durable destination | Preservation | Detail | Relations | Attribution | Context | Action | Fidelity | Gap / decision |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| {intent_id} | {source_intent} | {destination_ref} | {preservation} | {detail} | {relationships} | {attribution} | {context} | {actionability} | {fidelity_pct} | {fidelity_note} |

### Lifecycle Delta

Saved: {count_and_artifact_refs_or_none}
Still in memory: {count_and_topics_or_none}
Blocked or decision needed: {count_and_highest_leverage_decision_or_none}
Ready next: {count_and_route_or_none}
Next: {one_primary_action}

Ledger: {ledger_artifact_ref}
</capture-results>

## Red Flags

- "I'll show the list first and save after approval."
- "This follow-up is obvious enough to leave in chat."
- "Done items should be listed again."
- "Prior art can wait until proposal."
- "The table is optional because I wrote the artifact."
- "The fidelity score is enough; the user does not need to see the row mapping."
- "I can route broad work directly to propose; the task slices will preserve the roadmap."
- "A routed item can stay only in chat memory."
- "Copying user prose is the same as compiling intent."
- "What would you edit means patch it now."

## Related

- `/work` routes lifecycle lanes.
- `/dump` is a focused alias for `/capture --deep`.
- `/brief` turns conversation context into a lifecycle artifact via `/interview --auto`.
- `/prior-art` finds existing homes.
- `/lev-plan` compiles captured/design intent into a fidelity-checked human runbook and slice DAG.
- `/propose` turns captured/aligned items into task DNA.
- `/exec` runs shovel-ready items.
