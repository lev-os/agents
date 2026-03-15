# Confidence Routing Reference

Systematic confidence assessment to determine appropriate deliberation depth.

## Routing Thresholds

```
┌────────────────────────────────────────────────────────────────┐
│  CONFIDENCE ROUTING MATRIX                                      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  > 85% ────→ DIRECT EXECUTION                                  │
│              • Problem is familiar                             │
│              • Solution is known                               │
│              • Risk is low                                     │
│              • Just do it                                      │
│                                                                │
│  60-85% ───→ STANDARD (Single Agent + Skill Hints)             │
│              • Problem is scoped                               │
│              • Approach is clear-ish                           │
│              • Some uncertainty acceptable                     │
│              • One agent with skill catalog support            │
│                                                                │
│  40-60% ───→ RESONANCE MODE (Skill Discovery + Combos)         │
│              • Problem is defined                              │
│              • Multiple approaches possible                    │
│              • Need pattern matching                           │
│              • Skill catalog exploration                       │
│                                                                │
│  < 40% ────→ FULL PARLIAMENT (Multi-Agent Deliberation)        │
│              • High uncertainty                                │
│              • High stakes                                     │
│              • Multiple stakeholders                           │
│              • Need diverse perspectives                       │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## Confidence Assessment Framework

Score each factor 0-20%, sum for total:

### Factor 1: Domain Familiarity (0-20%)
```
20%: Solved this exact problem before
15%: Solved similar problems multiple times
10%: Solved related problems
5%:  Read about this domain
0%:  Completely new domain
```

### Factor 2: Information Completeness (0-20%)
```
20%: All requirements clear and documented
15%: Most requirements clear, few assumptions
10%: Core requirements clear, details fuzzy
5%:  Vague requirements, many assumptions
0%:  Requirements unclear or contradictory
```

### Factor 3: Solution Clarity (0-20%)
```
20%: Know exactly what to do
15%: Know approach, details to figure out
10%: Have ideas, need to explore
5%:  Multiple competing approaches
0%:  No idea where to start
```

### Factor 4: Risk Tolerance (0-20%)
```
20%: Low risk, easily reversible
15%: Moderate risk, can iterate
10%: Significant risk, some irreversibility
5%:  High risk, hard to undo
0%:  Critical risk, irreversible
```

### Factor 5: Stakeholder Alignment (0-20%)
```
20%: All stakeholders aligned
15%: Most stakeholders aligned
10%: Key stakeholders aligned
5%:  Some stakeholder disagreement
0%:  Major stakeholder conflict
```

## Quick Assessment Template

```markdown
## Confidence Assessment

**Problem:** {description}

| Factor | Score | Notes |
|--------|-------|-------|
| Domain Familiarity | /20 | |
| Information Completeness | /20 | |
| Solution Clarity | /20 | |
| Risk Tolerance | /20 | |
| Stakeholder Alignment | /20 | |
| **TOTAL** | **/100** | |

**Route:** {Direct / Standard / Resonance / Parliament}
```

## Override Rules

### Force Parliament (regardless of score)
- Strategic decision with long-term impact
- Multiple teams affected
- Explicit stakeholder request
- Prior decisions in this area failed

### Force Direct (regardless of score)
- Time constraint < 1 hour
- Reversible experiment
- Low-stakes exploration
- Explicit "just do it" request

## Calibration Guidelines

### Expected Confidence Trajectory

**Healthy Deliberation:**
```
Start:  60% confidence
After THINK: 50% (complexity revealed)
After SYNTHESIS: 55% (some resolution)
After DEVIL'S ADVOCATE: 50% (challenges absorbed)
Final: 55% (calibrated)

Pattern: Initial confidence DROPS, then stabilizes
```

**Warning Sign:**
```
Start:  60% confidence
After THINK: 70%
After SYNTHESIS: 80%
Final: 85%

Pattern: Confidence only goes UP = possible groupthink
```

### Confidence Delta by Mode

| Mode | Expected Delta | Meaning |
|------|----------------|---------|
| Direct | 0% | No deliberation, confidence unchanged |
| Standard | -5 to +5% | Minor adjustment |
| Resonance | -10 to +10% | Moderate adjustment as patterns found |
| Parliament | -20 to -5% | Healthy decrease as complexity revealed |

## Post-Decision Calibration

Track predictions vs outcomes:

```markdown
## Calibration Log

**Decision:** {description}
**Confidence at decision:** {X}%
**Outcome:** {success / partial / failure}
**Actual difficulty:** {easy / as expected / harder}

**Calibration adjustment:**
- If outcome matched confidence: well calibrated
- If easier than expected: underconfident, +5% base
- If harder than expected: overconfident, -5% base
```

## Threshold Tuning

Over time, adjust thresholds based on outcomes:

### Default Thresholds
```
Direct: >85%
Standard: 60-85%
Resonance: 40-60%
Parliament: <40%
```

### After Calibration
If parliament decisions consistently succeed:
```
Direct: >80%
Standard: 55-80%
Resonance: 35-55%
Parliament: <35%
```

If direct execution often fails:
```
Direct: >90%
Standard: 70-90%
Resonance: 50-70%
Parliament: <50%
```

## Integration with Skill Lookup

Confidence affects skill selection:

```bash
# High confidence (>85%): Skip skill lookup
# Just execute

# Standard (60-85%): Quick skill hint
node ~/lev/workshop/poc/lookup/cli.js find "<problem>" --limit=3

# Resonance (40-60%): Full skill exploration
node ~/lev/workshop/poc/lookup/cli.js find "<problem>" --limit=10
node ~/lev/workshop/poc/lookup/cli.js random --limit=5

# Parliament (<40%): Skill-augmented agents
# Each agent gets relevant skills from catalog
```

## Decision Tree Summary

```
Problem Arrives
    │
    ▼
Calculate Confidence Score
    │
    ├─ >85% → DIRECT: Execute immediately
    │
    ├─ 60-85% → STANDARD: Single agent + 3 skill hints
    │
    ├─ 40-60% → RESONANCE: Skill catalog exploration + combos
    │
    └─ <40% → PARLIAMENT: Full multi-agent deliberation
             │
             ├─ Spawn 3-5 agents
             ├─ Run CDO 5-stage cycle
             ├─ Trigger devil's advocate if >70% agreement
             └─ Expect confidence to decrease
```
