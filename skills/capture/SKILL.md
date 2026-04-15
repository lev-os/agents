---
name: capture
description: "Inventory + route + auto-research + durable dispatch. Use /capture for standard sweep, /capture --deep for full auto mode: shovel-ready -> /exec, everything else concrete -> /propose. Nothing should remain in memory."
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

**HARD RULE**: /capture INVENTORIES → AUTO-SAVES → shows /sitrep. It does NOT list and wait.
If you have confidence ≥ 0.7 OR ambiguity ≤ 0.3, write the item to disk immediately.
No items should be left "in-memory" — that's what /capture is FOR.

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

**Order: SAVE first, THEN show. Never show a list the user has to acknowledge with "ok save it."**

Sequence:
1. Write every in-memory item to disk (Step 3 routes)
2. Update the handoff (Step 5)
3. Show the delta

Output ONLY three buckets:
1. **In-memory** — items that could not be written (needs disambiguation)
2. **Blocked** — waiting on human/agent/external
3. **Crystallizing** — actively transitioning stages right now

Do NOT show:
- Done items (they're done, they're in git)
- Captured+stable items (filed, not moving)
- Lists of "things to do" (that's /sitrep's job)

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

### /capture vs /sitrep (read this before adding steps)

- **/sitrep** = read-only dashboard. Shows current lifecycle state. Never writes.
- **/capture** = writes then shows delta (in-mem + blocked + crystallizing only).

They are **different zoom levels** on the same underlying state. Future consolidation possible once /capture has full-fidelity auto-save during every verb (see proposal: lifecycle auto-captures, /capture becomes redundant). Not now.

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
| `--deep` | `/capture --deep` or `/dump` | Full auto: inventory + prior-art per topic + research if needed + route shovel-ready work to `/exec` and the rest to `/propose`. Was a separate /dump skill — now merged. |

### Deep Mode Pipeline (was /dump)

**HARD RULE: /capture NEVER leaves items in-memory.** Every item gets written to disk.
The pipeline is a convergence loop — it writes, checks, enriches, rewrites until stored
fidelity matches or exceeds in-memory fidelity.

```yaml
# The Capture Convergence Loop
while:
  condition: "any item where fidelity(stored) < fidelity(in_memory)"
  do:
    - classify: "tokenize conversation into topics, assign route per topic"
    - write: "dump each topic to its route at current best fidelity"
    - score: "score stored fidelity vs in-memory fidelity per item"
    - enrich: "for items where stored < in_memory:"
        - prior_art: "search repo + web for evidence (3 queries max)"
        - expand: "add details, relationships, attributions from context"
        - rewrite: "update the stored file with enriched content"
    - recheck: "re-score. if stored >= in_memory, item is done"
  exit: "all items: fidelity(stored) >= fidelity(in_memory)"
  circuit_breaker: "3 iterations without improvement → halt, note gap"
```

Key insight: `/capture --deep` PRODUCES higher fidelity than the original conversation
because prior-art enriches each topic beyond what was said. The capture is enrichment,
not just recording.

### Bucketed Queue Display

**HARD RULE: Show max 3-5 items at a time.** The rest queue behind.

```
Bucket 1 (NOW — highest priority, most actionable):
  3-5 items with full dashboard lines

Queue (NEXT — visible as count only):
  "12 more items queued (3 P1, 5 P2, 4 P3)"

Completed (collapsed):
  "7 items captured and written"
```

Bucketing rules:
- Sort by: priority (P0 first), then % to next stage (highest first)
- Show the top 3-5 that are actionable RIGHT NOW
- When an item completes, the next queued item promotes to the bucket
- This IS /work queue mode — the capture dashboard is a work queue

### Aggregate Next-Actions Bucket (Step 4.5)

After classifying all items, add an **ephemeral next-actions bucket** that:
1. Scans all "next steps" / "recommended actions" from the session (yours + user's)
2. Deduplicates against already-captured items
3. Shows as its own section — the backlog of "things we said we'd do but haven't filed"
4. Samurai-light: rank by what unblocks the most, max 5 shown

```
### Next Actions (deduplicated, 5 of N)
1. [unblocks: 3, 7] Wire gate formulas to DefaultGateEvaluator
2. [unblocks: 2] Ship 15 tribunal absorption edits
...
```

### Durable Capture Artifacts

Captures are NOT ephemeral. Every capture sweep produces a **durable artifact** near its workstream:

```
.lev/pm/workstreams/<ws-id>/captures/
  YYYYMMDD-capture-sweep.yaml    # machine-readable (stats, items, scores, routes)
  YYYYMMDD-capture-sweep.md      # human-readable (rendered by /now if needed)
```

The YAML capture report is the source of truth for what was discussed and where it went.
Auto-flows to: beads (task tracking), templated reports, plans, specs, /now pages.

```yaml
# capture report schema
date: YYYY-MM-DD
session: N
items:
  - id: 1
    topic: "..."
    stage: captured
    fidelity: 0.85
    route: "dna/standards/agentic-search.yaml"
    skill: "/propose"
    priority: P0
    subtasks: [...]
    unblocks: [3, 7]
```

### Volume Meta-Gate

| Volume | Behavior |
|---|---|
| < 5 items | Show all in one bucket |
| 5-15 items | Bucket top 5, queue rest |
| 15-25 items | Bucket top 3, queue rest (tighter focus) |
| > 25 items | Auto-suggest: split into workstreams before capturing |

## Fidelity Scoring (REQUIRED)

Every captured item gets a fidelity score before it can advance to durable execution planning.

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
fidelity ≥ 0.8 → if shovel-ready, proceed to /exec; otherwise proceed to /propose
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
  FIDELITY: 0.84 — PASS → route to /exec if verifier + write scope are clear, else /propose
```

### Relationship to Graph Zoom Levels

Fidelity score IS a zoom level measurement:
- L0 (overview) = fidelity ~0.2 — "we talked about X"
- L1 (structure) = fidelity ~0.5 — "X has components A, B, C"
- L2 (details) = fidelity ~0.8 — "A connects to B because of reason R, with constraint C"
- L3 (runtime) = fidelity ~0.95 — "here's the exact formula, exact path, exact sequence"

Source: `dna/gates.yaml` fidelity_gate, `dna/vernacular.yaml` fidelity section.

## Exec Menu (Step 6 — after capture + fidelity loop)

After all items are persisted (fidelity loop complete), present an **exec menu**.
This IS the bridge between /capture and /exec. Samurai-style critical path.

### Rules

- **Max 5 items** in the active bucket (critical path)
- **Max 3 subtasks** per item (detail level)
- **15-point plan** at max depth (5 × 3)
- Critical path ordering via dependency analysis (what unblocks the most?)
- Each item shows: **which skill/flowmind to use** for execution
- Items can be **bundled** when they share a skill/flow

### Format

```
## Exec Menu (5 of N)

1. **[Item Name]** → skill: /exec | flow: ralph | adapter: scout
   a. [Subtask 1] — write_scope: path/to/file
   b. [Subtask 2] — write_scope: path/to/other
   c. [Subtask 3] — verifier: test command
   ⏱ unblocks: #3, #7 | effort: S

2. **[Item Name]** → skill: /propose | flow: none | adapter: opus
   a. [Subtask] — write_scope: dna/graph.yaml
   ⏱ unblocks: #5 | effort: XS

... (max 5)

Queue: N more items (breakdown by priority)
```

### How the Menu is Built

1. **Scan all captured items** — from handoff + proposals + plans + this session
2. **Filter shovel-ready** — has enough fidelity (≥0.8), clear scope, known verifier, and no unresolved blocker
3. **Critical path sort** — items that unblock the most other items rank first
4. **Assign skill/flow** — classify each item:
   | Item Type | Skill | Flow | Adapter |
   |-----------|-------|------|---------|
| DNA/standard write | /propose | none | direct |
| Code implementation with verifier | /exec | ralph | scout/pi |
   | Design decision | /interview or /tribunal | none | opus |
   | Research needed | /prior-art | scout.flow | haiku |
   | Sweep/audit | /exec | lev-ralph | scout |
   | Skill update | /skill-builder | none | direct |
5. **Bundle where possible** — items sharing a skill/flow become one menu entry with subtasks
6. **Present the bucket** — top 5, rest queued

### Dispatch

When user selects items (or "all"):
- Create tasks for the batch
- Dispatch via /exec protocol (classify → verify surface → batch → review)
- If /levloop is active, schedule as tick sequence
- Each completed item promotes the next queued item into the bucket

## Entry Point for lifecycle.flow.yaml

`/capture` enters `lifecycle.flow.yaml` at the `router` node with `entry_verb: capture`. The router branches to the Plan lane. /capture resolves the decision_point (keep\|monitor\|execute\|reject).

## Graph Footer

After every /capture, append the shared graph footer from `~/.claude/skills/_shared/graph-footer.md`.

## Related

- `/work` — the lifecycle router (calls /capture internally)
- `/exec` — dispatch from exec menu (Step 6)
- `/interview` — for items with ambiguity > 0.2
- `/propose` — for items ready to crystallize into dna.yaml
- `/prior-art` — evidence search (called per-topic in deep mode)
- `/levloop` — recurring execution of the exec queue
