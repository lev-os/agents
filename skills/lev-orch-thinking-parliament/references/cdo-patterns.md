# CDO Patterns Reference

CDO (Cognitive Design Orchestration) provides the 5-stage cycle that governs all parliament deliberation.

## The 5-Stage Cycle

```
┌─────────────────────────────────────────────────────────────┐
│  STAGE 1: PLAN                                              │
│  ──────────────────────────────────────────────────────────│
│  • Define the problem precisely                             │
│  • Identify stakeholders and constraints                    │
│  • Set success criteria (measurable)                        │
│  • Estimate complexity → route to appropriate mode          │
│                                                             │
│  Output: problem-statement.md                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 2: THINK                                             │
│  ──────────────────────────────────────────────────────────│
│  • Spawn polymorph agents (3-5 perspectives)                │
│  • Each agent explores solution space independently         │
│  • Parallel execution, no cross-contamination               │
│  • Disk-based artifacts prevent groupthink                  │
│                                                             │
│  Output: perspectives/*.md (one per agent)                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 3: EXECUTE (Synthesis)                               │
│  ──────────────────────────────────────────────────────────│
│  • Read all perspective artifacts                           │
│  • Identify common ground                                   │
│  • Surface genuine disagreements                            │
│  • Propose integrated position                              │
│                                                             │
│  Output: synthesis.md                                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 4: REVIEW                                            │
│  ──────────────────────────────────────────────────────────│
│  • Validate synthesis against success criteria              │
│  • Check for missed perspectives                            │
│  • Verify anti-groupthink (devil's advocate triggered?)     │
│  • Confidence calibration (typically decreases)             │
│                                                             │
│  Output: review.md                                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 5: LEARN (Self-Improvement)                          │
│  ──────────────────────────────────────────────────────────│
│  • What worked in this deliberation?                        │
│  • What perspectives were missing?                          │
│  • Update skill catalog with new patterns                   │
│  • Log for future session resumption                        │
│                                                             │
│  Output: learnings.md                                       │
└─────────────────────────────────────────────────────────────┘
```

## Merge Strategies

When synthesizing agent outputs, use appropriate merge strategy:

### Strategy 1: Consensus Merge
**When:** Most agents agree on core approach.
```
Common ground → Primary recommendation
Minor differences → Noted as implementation options
```

### Strategy 2: Conditional Merge
**When:** Agents agree solution depends on context.
```
IF condition_A:
  → Approach from Agent1
ELSE IF condition_B:
  → Approach from Agent2
ELSE:
  → Hybrid approach
```

### Strategy 3: Tension Preserve
**When:** Genuine disagreement reflects real trade-offs.
```
Tension: Speed vs Quality
├─ Agent1 (Speed): Ship fast, iterate
├─ Agent2 (Quality): Get it right first time
└─ Framework: Decision matrix for each case
```

### Strategy 4: Staged Resolution
**When:** Different approaches suit different phases.
```
Phase 1 (0-6mo):  Agent1 approach (quick wins)
Phase 2 (6-18mo): Agent2 approach (scale)
Phase 3 (18mo+):  Agent3 approach (optimize)
```

## Agent Archetypes

Standard parliament composition:

| Archetype | Role | Bias (Intentional) |
|-----------|------|-------------------|
| Advocate | Build strongest FOR case | Optimistic, sees opportunity |
| Critic | Build strongest AGAINST case | Skeptical, sees risk |
| Systems | Second-order effects | Interconnection, feedback loops |
| Pragmatist | Implementation reality | Resource constraints, execution |
| Wild Card | Unconsidered alternatives | Lateral thinking, reframes |

### Specialized Archetypes (add as needed)

| Archetype | When to Add |
|-----------|-------------|
| User Advocate | Consumer-facing decisions |
| Security | High-risk systems |
| Economist | Cost/benefit analysis |
| Historian | Decisions with precedent |
| Futurist | Long-term strategic |

## Polymorph Agent Dispatch

Each agent receives:

```markdown
## Agent Brief

**Role:** {archetype}
**Perspective:** {intentional bias}
**Problem:** {problem statement}

## Instructions

1. Argue your perspective with FULL CONVICTION
2. Do not hedge or balance - that's synthesis's job
3. Surface evidence that supports YOUR view
4. Identify risks/opportunities others might miss
5. Write findings to {output_file}

## Output Format

### Position Statement
[2-3 sentences, clear thesis]

### Key Arguments (3-5)
[Numbered, with evidence]

### Implications
[What happens if this view is correct?]

### Blind Spots
[What might this perspective miss?]
```

## Cycle Iteration

If review reveals gaps:

```
REVIEW finds missing perspective
    │
    ▼
Return to THINK stage
    │
    ▼
Spawn additional agent with missing perspective
    │
    ▼
Re-run EXECUTE with expanded input
    │
    ▼
Continue to REVIEW
```

**Max iterations:** 3 (prevent infinite loops)

## Integration with BD

For multi-session deliberation:

```bash
# Create epic for parliament session
bd create --type=epic --title="Parliament: {problem summary}"

# Each agent becomes a task
bd create --type=task --parent={epic} --title="[A1] Advocate perspective"
bd create --type=task --parent={epic} --title="[A2] Critic perspective"
# ... etc

# Synthesis becomes final task
bd create --type=task --parent={epic} --title="[SYN] Synthesis and decision"
```
