---
name: propose
description: "Write or update a task's dna.yaml + execution.yaml. The Plan lane verb."
triggers:
  - propose
  - define
  - frame
---

# /propose — Lifecycle Transition: Plan Lane

Write the authored root for a task: `dna.yaml` (what) + `execution.yaml` (how).
Pattern: **cascade** (ordered derivation chain). Gate: **frame_complete_gate**.

## When to Use

- After `/capture` or `/interview` converges (ambiguity <= 0.2)
- When crystallizing a discussed idea into an executable task
- To update an existing task's definition or execution plan

## Protocol

### Step 1: Detect Mode

```
target = .lev/tasks/<task-id>/
if target/dna.yaml exists → UPDATE mode (read existing, merge delta)
else → CREATE mode (gather from scratch)
```

### Step 2: Gather Context (CREATE) or Load Existing (UPDATE)

For CREATE, extract from conversation / captured artifacts:
- **intent** — one sentence: what does this task accomplish?
- **acceptance** — list of concrete pass/fail criteria (minimum 1)
- **constraints** — list of boundaries, budget limits, scope fences
- **entity_kind** — from `dna/entities.yaml` types
- **lifecycle_target** — target state after completion

For UPDATE, read existing `dna.yaml`, identify the delta, merge.

### Step 3: Write dna.yaml

```yaml
# .lev/tasks/<task-id>/dna.yaml
ontology: <from dna/graph.yaml>
intent: "<one-sentence purpose>"
entity_kind: <type from dna/entities.yaml>
lifecycle_target: <target state>
acceptance:
  - "<criterion 1>"
  - "<criterion 2>"
local_refs: [<paths to related specs, designs, plans>]
local_constraints:
  - "<constraint 1>"
```

### Step 4: Write execution.yaml

```yaml
# .lev/tasks/<task-id>/execution.yaml
topology: <one of 8 patterns — see below>
runtime_profile: <profile name>
validation_chain:
  - gate: frame_complete_gate
  - gate: convergence_gate
receipt_policy: append_only
checkpoint_policy: forward_only
budget:
  max_iterations: <N>
  timeout: <duration>
exit_conditions:
  - "<condition>"
```

**8 topology patterns** (from `dna/standards/metrics.yaml`):
`sequence` | `protocol` | `strategy` | `judgment` | `cascade` | `loop` | `fan_out` | `reducer`

### Step 5: Validate — frame_complete_gate

```
PASS if: dna.yaml.acceptance.length >= 1 AND execution.yaml.topology != null
FAIL: re-run /propose to complete the missing fields
```

### Step 6: Advance

If gate passes, task state advances to `proposed` (next: `/capture` resolves decision_point).
If gate fails, stay in Plan lane. Report which field is missing.

## KPIs (from dna/lifecycle-kpis.yaml)

| KPI | Weight | Move On |
|-----|--------|---------|
| frame_completeness | 0.40 | = 1.0 |
| acceptance_specificity | 0.35 | >= 0.8 |
| execution_readiness | 0.25 | >= 0.75 |

## HUD

End every `/propose` with the HUD line from `~/.claude/skills/_shared/graph-footer.md`.

## Related

- `/capture` — upstream (resolves decision_point after propose)
- `/interview` — upstream (reduces ambiguity before propose)
- `/exec` — downstream (runs execution.yaml topology)
- `/work` — lifecycle router (may call /propose internally)
