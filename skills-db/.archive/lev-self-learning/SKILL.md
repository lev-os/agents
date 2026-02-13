---
name: lev-learn
description: |
  [WHAT] Event-driven learning system analyzing events.jsonl streams to propose system improvements
  [HOW] Polars-based pattern detection, proposal generation with confidence scores, human-in-the-loop confirmation, targets skills/daemons/config/workflows
  [WHEN] Use when analyzing events, detecting patterns, proposing improvements, or conducting post-mortem analysis
  [WHY] Extends skill-evolver from reactive fixes to proactive platform evolution based on observed patterns

  Triggers: "what can lev learn", "analyze events", "propose improvements", "self-learn", "optimize lev", "pattern detection", "event analysis"
version: 1.0.0
extends: skill-evolver
tools:
  - lev-learn (Python CLI via uv)
  - jq (JSONL queries)
  - polars (DataFrame analysis)
storage:
  events: ~/lev/.lev/events.jsonl
  proposals: ~/.config/lev/proposals/
  memory: ~/.config/lev/memory/
  patterns: ~/.config/lev/patterns.jsonl

lifecycle_integration:
  stage: all stages (meta-improvement)
  input_artifact: events.jsonl stream
  output_artifact: actionable proposals + pattern database
---

# Lev Self-Learning

Transform event streams into actionable system improvements. Extends skill-evolver to evolve the entire platform, not just skills.

## Relationship to skill-evolver

This skill **extends** skill-evolver:
- skill-evolver: Reactive (user reports failure → fix skill)
- lev-learn: Proactive (analyze events → propose improvements)

Both use the same:
- Proposal format
- Version store (`~/lev/.lev/store/`)
- Shared memory (`~/.config/lev/memory/`)
- Human-in-the-loop confirmation

## When to Use

| Trigger | Mode |
|---------|------|
| "what can lev learn?" | Full analysis cycle |
| "analyze events" | Pattern detection only |
| "propose improvements" | Generate proposals |
| "why did X fail?" | Root cause analysis |
| "optimize lev" | Performance-focused |
| "self-learn" | Automated improvement cycle |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    EVENT-DRIVEN LEARNING                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ~/lev/.lev/events.jsonl                                       │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐   │
│   │  Analyze    │───►│   Patterns   │───►│    Proposals    │   │
│   │  (polars)   │    │   (.jsonl)   │    │    (.yaml)      │   │
│   └─────────────┘    └──────────────┘    └─────────────────┘   │
│                                                   │             │
│                                                   ▼             │
│                                          ┌───────────────┐      │
│                                          │ Human Review  │      │
│                                          │  (confirm)    │      │
│                                          └───────────────┘      │
│                                                   │             │
│         ┌─────────────────────────────────────────┘             │
│         ▼                                                       │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              EVOLUTION TARGETS                          │   │
│   ├─────────────────────────────────────────────────────────┤   │
│   │  Skills     │ ~/.claude/skills/*/SKILL.md               │   │
│   │  Daemons    │ ~/.config/lev/daemons.yaml                │   │
│   │  Config     │ ~/lev/.lev/config.yaml                    │   │
│   │  Workflows  │ ~/lev/workflows/*.yaml                    │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   Shared Memory: ~/.config/lev/memory/                          │
│   - patterns.jsonl (detected patterns)                          │
│   - proposals.jsonl (pending proposals)                         │
│   - applied.jsonl (applied changes + outcomes)                  │
└─────────────────────────────────────────────────────────────────┘
```

## Shared Memory Store

Location: `~/.config/lev/`

```
~/.config/lev/
├── memory/
│   ├── patterns.jsonl      # Detected patterns across sessions
│   ├── proposals.jsonl     # Pending improvement proposals
│   └── applied.jsonl       # Applied changes + validation results
├── proposals/
│   ├── prop-001.yaml       # Individual proposal files
│   └── prop-002.yaml
└── config.yaml             # Global lev configuration
```

### Pattern Memory Schema

```jsonl
{"id":"pat-001","type":"error_cluster","signature":"mcp-adapter:timeout","count":12,"first_seen":"2026-01-01T00:00:00Z","last_seen":"2026-01-07T12:00:00Z","sessions":["ses-a","ses-b"],"proposed":false}
```

### Proposal Schema

```yaml
id: prop-001
type: skill_evolution | daemon_config | workflow_optimization | config_change
confidence: 0.85
impact: high | medium | low
effort: 5min | 30min | 2hr
status: pending | approved | applied | rejected | validated

observation: |
  Detected 12 instances of /codifier failing when GitHub rate-limited.
  
recommendation: |
  Add exponential backoff to codifier's GitHub fetcher.
  
implementation:
  target: skill | daemon | config | workflow
  file: ~/.claude/skills/codifier/SKILL.md
  changes:
    - section: "## Guardrails"
      action: append
      content: |
        - [ ] Check GitHub rate limit before fetch
        - [ ] Implement 1s/2s/4s backoff on 429
        
validation:
  metric: codifier_github_success_rate
  baseline: 0.73
  target: 0.92
  window: 7d
```

## Analysis Modes

### 1. Pattern Detection

```bash
uv run ~/lev/tools/lev-learn/main.py analyze --since 24h
```

Detects:
| Pattern | Method | Action |
|---------|--------|--------|
| Error Clusters | Same error type in 5min window | Propose fix |
| Skill Chains | Sequential skill invocations | Propose workflow |
| Duration Anomalies | >2x median duration | Investigate bottleneck |
| Retry Storms | 3+ retries same action | Propose guardrail |
| **Drift Signals** | ENOENT clusters, ref churn | **Trigger `lev-align`** |

### Drift Detection Integration

When lev-learn detects drift signals, it triggers `lev-align`:

```yaml
# Drift signal patterns
drift_triggers:
  - pattern: "ENOENT|Cannot find module|missing file"
    threshold: 3 occurrences in 1h
    action: invoke_lev_align
    
  - pattern: "ref.*not found|broken link"
    threshold: 5 occurrences in 24h
    action: invoke_lev_align
    
  - pattern: high_path_churn
    threshold: 10+ path changes in 1 session
    action: invoke_lev_align
```

See `skills/lev-align/SKILL.md` for the full alignment workflow (north star + drift + pivot adoption).

### 2. Proposal Generation

```bash
uv run ~/lev/tools/lev-learn/main.py propose --top 5
```

Generates proposals sorted by:
1. Confidence (pattern strength)
2. Impact (frequency × severity)
3. Effort (implementation cost)

### 3. Application (Human-in-the-Loop)

```bash
# Show proposal
uv run ~/lev/tools/lev-learn/main.py show prop-001

# Apply with confirmation
uv run ~/lev/tools/lev-learn/main.py apply prop-001

# Dry run
uv run ~/lev/tools/lev-learn/main.py apply prop-001 --dry-run
```

## Evolution Targets

### Skills (via skill-evolver)
- Path: `~/.claude/skills/*/SKILL.md`
- Versioned in: `~/lev/.lev/store/skill-versions/`
- Changes: Add guardrails, update examples, fix triggers

### Daemons
- Path: `~/.config/lev/daemons.yaml` or registry
- Changes: Tune polling intervals, add health checks, adjust resources

### Config
- Path: `~/lev/.lev/config.yaml`
- Changes: Adjust lifecycle settings, hook configurations, proxy settings

### Workflows
- Path: `~/lev/workflows/*.yaml`
- Changes: Optimize step ordering, add error handling, parallelize

## CLI Reference

### `lev-learn analyze`

```bash
# Full analysis
uv run ~/lev/tools/lev-learn/main.py analyze

# Time-bounded
uv run ~/lev/tools/lev-learn/main.py analyze --since 1h

# Specific event types
uv run ~/lev/tools/lev-learn/main.py analyze --type "lev.error,lev.tool"

# Output to file
uv run ~/lev/tools/lev-learn/main.py analyze --output ~/.config/lev/memory/patterns.jsonl
```

### `lev-learn propose`

```bash
# Generate from patterns
uv run ~/lev/tools/lev-learn/main.py propose

# Filter by target
uv run ~/lev/tools/lev-learn/main.py propose --target skill

# Minimum confidence
uv run ~/lev/tools/lev-learn/main.py propose --min-confidence 0.8
```

### `lev-learn apply`

```bash
# Interactive apply
uv run ~/lev/tools/lev-learn/main.py apply prop-001

# Auto-apply low-risk
uv run ~/lev/tools/lev-learn/main.py apply --auto --max-effort 5min
```

### `lev-learn stats`

```bash
# Event statistics
uv run ~/lev/tools/lev-learn/main.py stats

# By skill
uv run ~/lev/tools/lev-learn/main.py stats --group-by skill

# Time series
uv run ~/lev/tools/lev-learn/main.py stats --resolution hourly
```

## Self-Learning Loop

```
Daily (automated):
  1. Analyze last 24h events
  2. Update pattern memory
  3. Generate new proposals
  
Weekly (human review):
  1. Review pending proposals
  2. Approve/reject with feedback
  3. Apply approved proposals
  4. Validate applied changes
  
Monthly (retrospective):
  1. Review validation results
  2. Adjust confidence weights
  3. Archive stale patterns
```

## Guardrails

**Before analysis**:
- [ ] events.jsonl exists and has >100 events
- [ ] Sufficient time range for patterns (>1h)

**Before proposing**:
- [ ] Pattern has 3+ occurrences
- [ ] Confidence > 0.6

**Before applying**:
- [ ] User confirmation received
- [ ] Backup created (skill-evolver handles)
- [ ] Dry-run shown

**After applying**:
- [ ] Validation metric baseline recorded
- [ ] Follow-up check scheduled

## References

- `references/pattern-algorithms.md` - Detection algorithms
- `references/proposal-templates.md` - YAML templates
- `references/validation-metrics.md` - Success measurement
