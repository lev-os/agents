---
name: cdo-adaptive-turns
description: Turn composition protocol — how each turn's shape is determined by the previous synthesis
---

# Adaptive Turn Composition

## Turn Composition Protocol

Before each turn, the orchestrator reads the previous synthesis and makes three decisions:

1. **Width**: How many agents? (1-20)
2. **Roles**: What perspectives needed?
3. **Skills**: What 2-3 skills per agent? (via lev-catalog)

For Turn 1, these come from the preset. For Turn N+1, they come from the synthesis directive.

## Synthesis Directive Format

Every synthesis ends with a YAML block that shapes the next turn:

```yaml
## Next Turn Directive
confidence: 0.65
convergence_met: false
gaps:
  - "Security implications unaddressed"
  - "Cost analysis surface-level"
tensions:
  - "Advocate vs Critic on timeline feasibility"
recommended_next_turn:
  width: 3
  agents:
    - role: Security Analyst
      skills: [risk-assessment, threat-modeling]
      focus: "Security implications"
    - role: Financial Analyst
      skills: [total-cost-ownership, rice-scoring]
      focus: "Deep cost analysis"
    - role: Mediator
      skills: [decision-matrix, reversibility-check]
      focus: "Resolve timeline tension"
```

## Adaptation Rules

- `confidence >= threshold` → FINAL synthesis
- All gaps addressed + tensions resolved → FINAL
- Max turns reached → force FINAL
- Single gap dominates → narrow to 1-2 focused agents
- Many gaps → go wide (5-10 agents)
- New problem dimensions found → consider widening beyond preset
- Confidence drops → flag for HITL if not already in HITL mode

## Adaptive Team Sizing

When the `adaptive` flag is set:

- After each synthesis, compare recommended width to current team
- If need MORE roles: spawn additional teammates (TeamCreate members) or subagents
- If roles no longer needed: send `shutdown_request` to those teammates
- Width can expand beyond preset maximum when synthesis justifies it

## Anti-Patterns

- **DO NOT** pre-plan all turns at start. Only compose the current turn.
- **DO NOT** let the orchestrator synthesize. Always dispatch a separate agent.
- **DO NOT** let agents see each other's work during a turn. Disk isolation is mandatory.
- **DO NOT** skip synthesis between turns. Even if only 1 agent ran.
