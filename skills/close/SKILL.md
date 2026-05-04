---
name: close
description: "Close lane verb. QA + accept + commit + hygiene + learn + recommend."
triggers:
  - close
  - ok
  - done
  - accept
output_template: hud
---

# /close — Lifecycle Transition: Close Lane

Close the active task: verify, ratify, checkpoint, clean, learn, recommend.
Pattern: **sequence** (linear, no branching). Gate: **drift_gate** (drift < 0.3).
Flow ref: `plugins/sdlc/flows/close-and-learn.flow.yaml`

## When to Use

- After `/exec` converges (convergence >= 0.95)
- When acceptance criteria are met and work is ready to seal
- Triggers: `/close`, `/ok`, `/done`, `/accept`

## Protocol

### Step 0: Absorb /capture (HARD GATE — day-1 scope)

**/close subsumes /capture.** Before anything else: run the shared inventory sweep in **gate mode**.

**Protocol**: `@include ~/.claude/skills/_shared/capture-sweep.md` with `mode=gate`.

This reads the canonical sweep protocol (inventory → classify → route → fidelity score → durable artifact write) from the single source of truth. No prose re-implementation — prior drift between /capture and /close proved that path fails (see `tmp/capture-sweep-diff-test.sh`).

**Gate requirement:** the shared sweep returns `in_memory_count`. It MUST be 0 to proceed to Step 1. If > 0, either file the remaining items or /close halts.

Rationale: bg agents should be able to apply the trigger output without NLP on prose. If /close seals a session with items still floating in conversation context, those items die at compact.

Canonical routes + fidelity formula + durable artifact schema: see `~/.claude/skills/_shared/capture-sweep.md` — NOT duplicated here.

### Step 1: QA

Validate task output against acceptance criteria.
```
Read .lev/pm/tasks/<task-id>/dna.yaml → acceptance field
Check each criterion. Report pass/fail per criterion.
ALL must pass to proceed. Any fail → rework (back to /exec).
```

### Step 2: Accept

Human ratification checkpoint.
```
Present QA results to human.
Auto-accept if confidence >= 0.85 (from idle-exec-policy default_threshold).
Otherwise, present results and wait for explicit human approval.
Destructive/publish/deploy actions ALWAYS require human confirmation.
```

### Step 3: Commit

Git checkpoint — forward-only.
```
git add . → git commit → git pull → git push
Message references task-id. No rebase. No amend.
```

### Step 4: Hygiene

Post-commit cleanup and drift check.
```
1. Run /lev-align on touched files
2. Check for stale references in modified files
3. Verify no orphaned imports
4. Compute drift: drift = 0.5*goal_drift + 0.3*constraint_drift + 0.2*ontology_drift
5. drift >= 0.5 → circuit breaker halt
6. drift >= 0.3 → rework (max 2 rework cycles)
7. drift < 0.3 → proceed
```

### Step 5: Learn (TYPED, not prose)

Extract learnings as STRUCTURED objects. Prose learnings cannot be applied by background agents.

Each learning MUST have:
```yaml
- id: L-<slug>
  claim: "<concrete assertion, one sentence>"
  evidence: "<path:line | commit:sha | conversation:turn>"
  applies_to: [<audience tags>]  # e.g. [skill_authors, bg_agents, schema_authors]
  propagates: [<concrete places that should adopt this>]  # file paths, skill refs
```

Prose summaries are fine in handoff.md, but the TYPED list goes in the trigger (Step 6.5).

### Step 6: Recommend

Propose next action for related entities.
```
For each graph neighbor: keep / monitor / execute / reject
Are there more tasks ready in this workstream?
```

### Step 6.5: Emit trigger (REQUIRED — day-1 scope of lifecycle_trigger.v1)

Write the canonical structured record of this close to the trigger stream.

```
Path: .lev/pm/workstreams/<ws-id>/triggers/<YYYYMMDDThhmm>-close.yaml
Schema: lifecycle_trigger.v1 (see .lev/pm/proposals/20260415-lifecycle-trigger-envelope.yaml)

Required fields:
  schema: lifecycle_trigger.v1
  verb: close
  entity_ref: ws://<ws-id>  OR task://<task-id>
  timestamp: <ISO 8601 UTC>
  agent: <session id>
  commit_before: <sha pre-close>
  commit_after: <sha post-close>
  outputs:
    items: []                   # MUST be empty (Step 0 gate)
    learnings: [...]            # typed entries from Step 5
    gates: [...]                # {id, score, threshold, pass} per hygiene check
    artifacts: [...]            # commits, files, ids
    decisions: [...]            # if any decisions ratified this close
  metrics:
    drift: <number>
    in_memory_count: 0
  cursor:
    last_verb: close
    last_at: <timestamp>
    last_commit: <sha>
    next_verb: null              # sealed; or next session's verb if chaining
    blocker: null
  recommend:
    - { entity: <uri>, verdict: <keep|monitor|execute|reject>, note: "..." }
```

A worked example lives at `.lev/pm/workstreams/lifecycle-engine/triggers/20260415T0220-propose.yaml`.
The trigger file is the structured counterpart to the handoff.md — bg agents read triggers, humans read handoffs.

### Step 7: Handoff (REQUIRED — do not skip)

Invoke the /handoff skill to update the workstream and pbcopy the resume prompt.
This is not optional — a /close that doesn't /handoff leaves the workstream stale.

/handoff writes `.lev/pm/workstreams/<id>/state/workstream.yaml` + commits + pushes + pbcopy.
Workstreams are the durable identity (not markdown files in handoffs/).

## KPIs (from dna/lifecycle-kpis.yaml)

| KPI | Weight | Move On |
|-----|--------|---------|
| drift_score | 0.45 | < 0.3 |
| hygiene_pass_rate | 0.30 | >= 0.95 |
| learning_extracted | 0.25 | >= 1 (mandatory) |

Max rework: 2. Circuit breaker: 3 consecutive failures.

## HUD

End every `/close` with the HUD line from `~/.claude/skills/_shared/graph-footer.md`.

## Related

- `/exec` — upstream (runs until convergence, then hands to /close)
- `/handoff` — downstream (session boundary after close)
- `/work` — lifecycle router (may call /close internally)
- `/lev-align` — used in hygiene step
