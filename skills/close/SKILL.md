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

### Step 1: QA

Validate task output against acceptance criteria.
```
Read .lev/tasks/<task-id>/dna.yaml → acceptance field
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

### Step 5: Learn

Extract learnings and update graph neighbors.
```
1. Which skill/flow was used? Did it work first try?
2. Record execution pattern that succeeded
3. Update cm (procedural memory) with lessons
4. Emit receipt (append-only, C2)
```

### Step 6: Recommend

Propose next action for related entities.
```
For each graph neighbor: keep / monitor / execute / reject
Are there more tasks ready in this workstream?
```

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
