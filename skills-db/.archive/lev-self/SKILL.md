---
name: lev-self
description: |
  [WHAT] Self-improvement system transforming event streams into actionable system improvements
  [HOW] Analyze events.jsonl for patterns, generate proposals with confidence scores, human-approve, apply to skills/config/daemons
  [WHEN] Use when asking what lev can learn, proposing improvements, or conducting fail-forward root cause analysis
  [WHY] Enables proactive system evolution based on observed failures and patterns instead of reactive fixes

  Triggers: "what can lev learn", "propose improvements", "self-learn", "why did X fail", "improve lev", "fail-forward"
version: 1.0.0
storage:
  events: ~/lev/.lev/events.jsonl
  proposals: ~/.config/lev/proposals/
  patterns: ~/.config/lev/patterns.jsonl

lifecycle_integration:
  stage: all stages (meta-improvement)
  input_artifact: events.jsonl + patterns
  output_artifact: improvement-proposals.md
---

# Lev Self-Improvement

Transform event streams into actionable system improvements. Proactive learning (not just reactive fixes).

## Quick Reference

| Trigger | Action |
|---------|--------|
| "what can lev learn?" | Full analysis cycle |
| "propose improvements" | Generate proposals from patterns |
| "why did X fail?" | Root cause analysis (fail-forward) |
| "self-learn" | Automated improvement cycle |

## Architecture

```
events.jsonl → Analyze → Patterns → Proposals → Human Review → Apply
                 ↑                                              │
                 └──────────── feedback loop ──────────────────┘
```

## Core Workflows

### 1. Event Analysis
```bash
lev learn analyze              # Detect patterns in events.jsonl
lev learn analyze --since 24h  # Last 24 hours only
```

See: `references/event-analysis.md`

### 2. Fail-Forward Protocol
When something fails, extract learning:
1. Capture: What happened? (exact error, context)
2. Root Cause: Why? (5 whys, dependencies)
3. Proposal: How to prevent? (skill patch, config change)
4. Confidence: How sure? (low/medium/high)

See: `references/fail-forward.md`

### 3. Proposal Workflow
```yaml
# ~/.config/lev/proposals/{id}.yaml
id: prop-abc123
type: skill-patch | config-change | new-workflow
target: ~/.claude/skills/lev/SKILL.md
confidence: 0.85
description: "Add timeout handling"
diff: |
  + timeout: 30s
status: pending | approved | rejected | applied
```

See: `references/proposals.md`

## Evolution Targets

| Target | Location | When |
|--------|----------|------|
| Skills | ~/.claude/skills/*/SKILL.md | Behavior improvements |
| Config | ~/lev/.lev/config.yaml | Settings optimization |
| Daemons | ~/.config/lev/daemons.yaml | Process tuning |
| Workflows | ~/lev/workflows/*.yaml | Pattern codification |

## Relationship to Other Skills

- **skill-evolver** (absorbed): Reactive skill fixes
- **lev** (sibling): Behavior definition (lev-self improves it)
- **bd** (integration): Track proposals as issues

## Storage Schema

```
~/.config/lev/
├── proposals/           # Pending proposals
│   └── {id}.yaml
├── memory/
│   ├── patterns.jsonl   # Detected patterns
│   ├── proposals.jsonl  # Proposal history
│   └── applied.jsonl    # Applied changes + outcomes
└── patterns.jsonl       # Active patterns for matching
```

## Confidence Thresholds

| Confidence | Action |
|------------|--------|
| ≥90% | Auto-apply (after notification) |
| 70-89% | Propose with recommendation |
| 50-69% | Propose, request review |
| <50% | Log only, don't propose |

See: `references/tracking-schema.md`

## CLI Quick Reference

```bash
# Analysis
lev learn analyze             # Full event analysis
lev learn patterns            # Show detected patterns

# Proposals
lev learn propose             # Generate proposals from patterns
lev learn review              # Interactive proposal review
lev learn apply <id>          # Apply approved proposal

# Tracking
lev learn status              # Show pending proposals
lev learn history             # Show applied changes
```

## Human-in-the-Loop

**All changes require confirmation:**
1. Proposal generated → notification
2. Human reviews diff
3. Approve/reject/modify
4. Applied changes logged with outcome

**Rollback:**
```bash
lev learn rollback <id>       # Revert applied proposal
```

---

*For detailed schemas and protocols, see references/*
