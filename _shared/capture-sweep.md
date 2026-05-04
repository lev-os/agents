<!--
  Shared capture-sweep subroutine — single source of truth.
  @include'd by: ~/.claude/skills/capture/SKILL.md and ~/.claude/skills/close/SKILL.md (Step 0)
  Source: .lev/tasks/lifecycle-trigger-substrate/execution.yaml N4b
  CDO Q2 verdict: SHIP-PR-1-2 (2/3 tribunal — 2026-04-15)
  Drift check: tmp/capture-sweep-diff-test.sh — CI-enforced post-PR2
-->

# capture.sweep — shared inventory protocol

**Single source of truth for the capture/close inventory sweep.**

Both `/capture` (standalone + deep modes) and `/close` (Step 0 gate mode) execute this
exact sequence. Prose drift between the two is the failure this file prevents.

## Contract

```yaml
capture.sweep:
  inputs:
    mode: standalone | gate | deep
    conversation_context: [session turns]
    workstream_id: string
    fidelity_threshold: 0.8 (default)
  outputs:
    items: [...]
    stats:
      total_inventoried: int
      in_memory_captured: int   # items written this sweep
      transitioning: int        # items moving between lifecycle stages
      blocked: int              # items waiting on external
      fidelity_avg: float
    durable_artifact_path: string   # path to captures/YYYYMMDD-*.yaml
    in_memory_count: int            # 0 required in gate mode
    exit_code: int                  # 0 = clean, >0 = items still in memory
  side_effects:
    - Writes .lev/pm/workstreams/<ws-id>/captures/YYYYMMDD-capture-sweep.yaml
    - Routes in-memory items to the canonical routes below
    - In mode=gate: fails if in_memory_count > 0 after sweep
    - In mode=deep: runs convergence loop with prior-art enrichment
```

## The Sweep (sequence)

### 1. Inventory

Scan the conversation for:
- Ideas mentioned but not filed anywhere
- Decisions made but not persisted
- Follow-ups promised but not tracked
- Artifacts discussed but not created

### 2. Classify Each Item

| State | Meaning | Where It Lives |
|---|---|---|
| **done** | Shipped, pushed, published | handoff / git log / published URL |
| **captured** | Filed in .lev/ or pushed | .lev/pm/, .lev/scratch/, parity YAML |
| **in-memory** | Discussed but NOT filed | only in context — MUST capture now |
| **transitioning** | Moving between lifecycle stages | show prominently |
| **blocked** | Waiting on another agent/human | note the blocker |

### 3. Route (canonical route list — identical across /capture + /close)

For each in-memory item, route by type:

| Item type | Route |
|---|---|
| Constraint / behavioral contract | `.lev/scratch/feature-dna-drafts/` |
| Plan / task | `.lev/pm/plans/` |
| Decision | `.lev/pm/decisions/` |
| Parity observation | `.lev/pm/parity/` |
| Design insight | `.lev/pm/designs/` |
| Proposal (pre-spec) | `.lev/pm/proposals/` |
| Report (audit/research/status/etc) | `.lev/pm/reports/` |
| Agent coordination item | `.lev/mail/` |
| Captured sweep artifact (always) | `.lev/pm/workstreams/<ws>/captures/` |
| Trace entry (trigger emission) | `.lev/pm/workstreams/<ws>/trace/` |
| Needs deliberation | suggest `/cdo` or `/think` |
| Needs evidence search | suggest `/prior-art` or `/lev-research` |
| Needs clarity | suggest `/interview` |

**Routes MUST match between /capture and /close byte-for-byte.** CI enforced via
`tmp/capture-sweep-diff-test.sh`.

### 4. Fidelity Scoring (REQUIRED before advancing)

```
fidelity = 0.30 · detail_preservation
         + 0.25 · relationship_preservation
         + 0.20 · source_attribution
         + 0.15 · neighbor_context
         + 0.10 · actionability
```

| Dimension | Weight | Scoring |
|---|---|---|
| detail_preservation | 30% | Did numbers/names/paths/formulas survive? |
| relationship_preservation | 25% | Did dependencies + cross-references survive? |
| source_attribution | 20% | Can each point trace to where/when it was said? |
| neighbor_context | 15% | Are related topics cross-referenced? |
| actionability | 10% | Can someone act WITHOUT reading the original convo? |

**Gate:**
- `fidelity ≥ 0.8` → shovel-ready (advance to `/exec` or `/propose`)
- `fidelity < 0.8` → re-capture at higher zoom level (L2→L3)

Zoom levels: L0 overview (~0.2) / L1 structure (~0.5) / L2 details (~0.8) / L3 runtime (~0.95).

### 5. Durable Artifact (ALWAYS — per mode)

Write to `.lev/pm/workstreams/<ws-id>/captures/YYYYMMDD-capture-sweep.yaml`:

```yaml
date: YYYY-MM-DD
session: N
mode: standalone | gate | deep
items:
  - id: 1
    topic: "..."
    stage: captured
    fidelity: 0.85
    route: "path/to/destination"
    skill: "/propose" | "/exec" | "/interview" | "/prior-art"
    priority: P0-P3
    neighbors: [...]
    unblocks: [...]
stats:
  total_inventoried: N
  in_memory_captured: N
  fidelity_avg: 0.xx
  in_memory_count: 0   # MUST be 0 in gate mode
```

## Mode-specific Behavior

| Mode | Caller | Extra steps | Exit condition |
|---|---|---|---|
| `standalone` | `/capture` (default) | Standard sweep → exec menu | items written to disk |
| `gate` | `/close` Step 0 | Fast sweep; no enrichment | **MUST** have `in_memory_count == 0` or /close halts |
| `deep` | `/capture --deep` or `/dump` | Convergence loop: prior-art + research per-topic + rewrite until `fidelity(stored) ≥ fidelity(in_memory)` | max 3 convergence iterations |

### Deep-mode convergence loop

```yaml
while:
  condition: "any item where fidelity(stored) < fidelity(in_memory)"
  do:
    - classify: "tokenize conversation into topics"
    - write: "dump each topic at current best fidelity"
    - score: "fidelity per item"
    - enrich: "for items below target — prior_art search (3 queries max)"
    - rewrite: "update stored file with enrichment"
    - recheck: "re-score"
  exit: "all items: fidelity(stored) >= fidelity(in_memory)"
  circuit_breaker: "3 iterations without improvement → halt, note gap"
```

## Output Shape (bucketed — max 3-5 visible)

After sweep, show ONLY:

```
### In Memory (MUST file now — should be empty post-sweep)
1. [ROUTE → path] Description

### Transitioning (crystallizing — ≤5 items)
1. [stage-from → stage-to] Description — trigger: X

### Blocked (waiting)
1. [blocked on A1] Description — since: date

### Stats
- Total inventoried: N
- In memory → captured: N
- Transitioning: N
- Blocked: N
- Fidelity avg: 0.xx
```

Do NOT show done items (git log has them) or captured+stable items (that's /sitrep's job).

## Volume Meta-Gate

| Volume | Behavior |
|---|---|
| < 5 items | Show all in one bucket |
| 5-15 items | Bucket top 5, queue rest |
| 15-25 items | Bucket top 3, queue rest |
| > 25 items | Auto-suggest: split into workstreams before capturing |

## Exec Menu (deferred to caller)

The **exec menu** (top 5 of N shovel-ready items with skill/flow/adapter/model)
is caller-specific. `/capture` renders it; `/close` does not (close is terminal).

Adapter/model rules (from /propose skill convergence):
- **adapter** (execution lane): `direct | scout | pi` — `pi` is scout-only
- **model** (reasoning tier): `haiku | sonnet | opus`
- **flow** (orchestration): `ralph | lev-ralph | none`
- Same adapter across every menu entry = smell — vary by work shape.

## Drift-Proof Mechanism

1. **This file** is the single source of truth
2. Both skills `@include` it (not copy)
3. CI enforced via `tmp/capture-sweep-diff-test.sh`
4. Future: `plugins/sdlc/tests/capture-sweep-parity.test.ts` fixture-based

Any change to sweep behavior lands in this file FIRST. Both skills pick it up on next load.
