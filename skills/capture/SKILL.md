---
name: capture
description: "Inventory + route + auto-research + propose. The Shape→Plan lifecycle trigger. Use /capture for standard sweep, /capture --deep for full auto-research mode (was /dump)."
triggers:
  - capture
  - dump
---

# /capture — Lifecycle Transition: Shape → Plan

Inventory everything discussed. Route to lifecycle state. File what's unfiled. Show only what's in-memory or transitioning.

## When to Use

- End of a brainstorm / brain dump session
- Before `/work` or `/lev exec` — crystallize what exists
- After a long conversation — capture the delta
- When you say "list everything" or "what did we talk about"

## Protocol

### Step 1: Inventory

Scan the conversation for:
- Ideas mentioned but not filed anywhere
- Decisions made but not persisted
- Follow-ups promised but not tracked
- Artifacts discussed but not created

### Step 2: Classify Each Item

| State | Meaning | Where It Lives |
|---|---|---|
| **done** | Shipped, pushed, published | handoff / git log / published URL |
| **captured** | Filed in .lev/ or pushed | .lev/pm/plans/, .lev/scratch/, parity YAML, etc. |
| **in-memory** | Discussed but NOT filed | only in conversation context — MUST capture now |
| **transitioning** | Moving between lifecycle stages | show prominently |
| **blocked** | Waiting on another agent/human | note the blocker |

### Step 3: Route

For each in-memory item:
- If it's a constraint/behavioral contract → `.lev/scratch/feature-dna-drafts/`
- If it's a plan/task → `.lev/pm/plans/`
- If it's a decision → `.lev/pm/decisions/`
- If it's a parity observation → `.lev/pm/parity/`
- If it's a design insight → `.lev/pm/designs/`
- If it's an agent coordination item → `.lev/mail/`
- If it needs deliberation → suggest `/cdo` or `/think`
- If it needs research → suggest `/prior-art` or `/lev-research`

### Step 4: Show the Delta

Output ONLY:
1. **In-memory items** (not yet captured — action required)
2. **Transitioning items** (moving states — awareness required)

Do NOT show done+stable items unless asked.

### Step 5: Handoff Update

Update the active handoff with the capture results:
```yaml
capture_sweep:
  date: YYYY-MM-DD
  in_memory_captured: N
  transitioning: N
  blocked: N
  total_inventoried: N
```

## Output Format

```
## /capture results

### In Memory (MUST file now)
1. [ROUTE → .lev/pm/plans/] Description of unfiled idea
2. [ROUTE → .lev/scratch/] Description of unfiled constraint
...

### Transitioning (awareness)
1. [planned → next] Description — trigger: X
2. [next → executing] Description — started by: agent Y
...

### Blocked (waiting)
1. [blocked on A1] Description — since: date
...

### Stats
- Total inventoried: N
- In memory → captured: N
- Transitioning: N
- Blocked: N
```

## Depth Modes

| Mode | Trigger | What Happens |
|---|---|---|
| `--shallow` | `/capture --shallow` | Inventory only. Classify + stats table. No routing. |
| (default) | `/capture` | Inventory + classify + route to existing files via /prior-art. Standard sweep. |
| `--deep` | `/capture --deep` or `/dump` | Full auto: inventory + prior-art per topic + research if needed + propose if ambiguity ≤ 0.2. Was a separate /dump skill — now merged. |

### Deep Mode Pipeline (was /dump)

```
FOR EACH in-memory item:
  1. /prior-art probe (3 queries max)
     → found existing home? route there
     → no home? continue
  2. /research (if topic needs evidence)
  3. check ambiguity score
     → ≤ 0.2? /propose (write dna.yaml)
     → > 0.2? flag for /interview
```

### Volume Meta-Gate

| Volume | Behavior |
|---|---|
| < 10 items | Normal capture |
| 10-25 items | Standard (warn about volume) |
| > 25 items | Auto-suggest: split into workstreams before capturing |

## Fidelity Scoring (REQUIRED)

Every captured item gets a fidelity score before it can advance to /propose.

### The Formula

```
fidelity = 0.30 × detail_preservation
         + 0.25 × relationship_preservation
         + 0.20 × source_attribution
         + 0.15 × neighbor_context
         + 0.10 × actionability
```

### Dimensions

| Dimension | Weight | What to Score (0-1) |
|---|---|---|
| detail_preservation | 30% | Did specific numbers, names, paths, formulas survive? If conversation said "15 points," did you capture 15? |
| relationship_preservation | 25% | Did connections between ideas survive? If X depends on Y, is that link captured? |
| source_attribution | 20% | Can each point trace to where it was said? (which message, which session, which agent) |
| neighbor_context | 15% | Are related topics cross-referenced? Does this capture link to its graph neighbors? |
| actionability | 10% | Can someone act on this WITHOUT reading the original conversation? |

### Gate

```
fidelity ≥ 0.8 → proceed to /propose
fidelity < 0.8 → re-capture at higher zoom level (L2→L3)
```

### How to Re-Capture at Higher Fidelity

1. Identify which dimension scored lowest
2. Re-read the relevant conversation context
3. Expand the capture with missing details, relationships, or attributions
4. Re-score

### Example

```
Item: "/work rewrite as lifecycle router"
  detail_preservation: 0.4  ← FAIL (15 points discussed, 3 captured)
  relationship_preservation: 0.3  ← FAIL
  source_attribution: 0.6
  neighbor_context: 0.5
  actionability: 0.3  ← FAIL
  FIDELITY: 0.39 — BELOW THRESHOLD → re-capture

After re-capture:
  detail_preservation: 0.9  ← all 15 points expanded
  relationship_preservation: 0.8  ← telemetry + discovery + flow selection linked
  source_attribution: 0.85  ← traced to GPT breakthrough + Opus /think
  neighbor_context: 0.75  ← cross-referenced with 20 promoted flows
  actionability: 0.8  ← someone can rebuild the vision from this alone
  FIDELITY: 0.84 — PASS → proceed to /propose
```

### Relationship to Graph Zoom Levels

Fidelity score IS a zoom level measurement:
- L0 (overview) = fidelity ~0.2 — "we talked about X"
- L1 (structure) = fidelity ~0.5 — "X has components A, B, C"
- L2 (details) = fidelity ~0.8 — "A connects to B because of reason R, with constraint C"
- L3 (runtime) = fidelity ~0.95 — "here's the exact formula, exact path, exact sequence"

Source: `dna/gates.yaml` fidelity_gate, `dna/vernacular.yaml` fidelity section.

## Entry Point for lifecycle.flow.yaml

`/capture` enters `lifecycle.flow.yaml` at the `router` node with `entry_verb: capture`. The router branches to the Plan lane. /capture resolves the decision_point (keep\|monitor\|execute\|reject).

## Graph Footer

After every /capture, append the shared graph footer from `~/.claude/skills/_shared/graph-footer.md`.

## Related

- `/work` — the lifecycle router (calls /capture internally)
- `/interview` — for items with ambiguity > 0.2
- `/propose` — for items ready to crystallize into dna.yaml
- `/prior-art` — evidence search (called per-topic in deep mode)
