# Tracking Schema

JSONL schemas for patterns, proposals, and outcomes.

## patterns.jsonl

```jsonl
{
  "id": "pat-001",
  "type": "frequency|sequence|performance",
  "pattern": "description of detected pattern",
  "events": ["event-id-1", "event-id-2"],
  "first_seen": "2026-01-15T00:00:00Z",
  "last_seen": "2026-01-17T00:00:00Z",
  "count": 15,
  "confidence": 0.85,
  "proposal_id": "prop-abc123"
}
```

## proposals.jsonl

```jsonl
{
  "id": "prop-abc123",
  "created": "2026-01-17T00:00:00Z",
  "type": "skill-patch",
  "target": "~/.claude/skills/lev/SKILL.md",
  "status": "applied",
  "applied_at": "2026-01-17T01:00:00Z",
  "outcome": "success",
  "outcome_notes": "Timeout events reduced to zero"
}
```

## applied.jsonl

```jsonl
{
  "id": "applied-001",
  "proposal_id": "prop-abc123",
  "timestamp": "2026-01-17T01:00:00Z",
  "backup_path": "~/.config/lev/backups/lev-SKILL.md.bak",
  "rollback_available": true,
  "verification_status": "passed",
  "metrics_before": {"timeout_events": 5},
  "metrics_after": {"timeout_events": 0}
}
```

## Confidence Calculation

```
confidence = base_confidence * evidence_weight * recency_factor

base_confidence:
  - Direct observation: 0.9
  - Pattern inference: 0.7
  - Hypothesis: 0.5

evidence_weight:
  - Multiple occurrences: 1.2
  - Single occurrence: 0.8
  - User confirmed: 1.5

recency_factor:
  - Last 24h: 1.0
  - Last week: 0.9
  - Older: 0.7
```

## Storage Locations

| File | Purpose | Retention |
|------|---------|-----------|
| patterns.jsonl | Active patterns | Until resolved |
| proposals.jsonl | All proposals | Forever |
| applied.jsonl | Applied changes | Forever |
| events.jsonl | Raw events | 30 days |
