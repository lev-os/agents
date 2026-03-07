# Proposal Workflow

How proposals are created, reviewed, and applied.

## Proposal Schema

```yaml
# ~/.config/lev/proposals/{id}.yaml
id: prop-abc123
created: "2026-01-17T00:00:00Z"
type: skill-patch | config-change | new-workflow | daemon-tune
target: ~/.claude/skills/lev/SKILL.md
source: event-analysis | fail-forward | manual
confidence: 0.85
description: "Add timeout handling to prevent hangs"

diff: |
  @@ -10,3 +10,4 @@
   config:
     retry: 3
  +  timeout: 30s

rationale: |
  Observed 5 timeout events in last 24h.
  Adding explicit timeout prevents indefinite hangs.

verification: |
  1. Load skill
  2. Trigger timeout scenario
  3. Confirm graceful failure

status: pending | approved | rejected | applied
applied_at: null
outcome: null
```

## Lifecycle

```
Created → Pending → [Approved/Rejected] → Applied → Outcome Tracked
              ↑                              │
              └────── Rollback ──────────────┘
```

## Review Commands

```bash
lev learn review                    # Interactive review all pending
lev learn review <id>               # Review specific proposal
lev learn approve <id>              # Approve
lev learn reject <id> --reason "x"  # Reject with reason
```

## Auto-Apply Rules

| Confidence | Behavior |
|------------|----------|
| ≥90% + low risk | Auto-apply after 24h notification |
| ≥90% + high risk | Require explicit approval |
| <90% | Always require approval |

## Tracking

All proposals logged to `~/.config/lev/memory/proposals.jsonl`:
```jsonl
{"id":"prop-abc","status":"applied","outcome":"success","impact":"reduced timeouts 100%"}
```
