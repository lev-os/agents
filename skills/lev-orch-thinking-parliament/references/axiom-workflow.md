# Axiom Workflow Reference

Disk-based multi-turn thinking that prevents groupthink through artifact isolation.

## Philosophy

**Problem:** When reasoning happens entirely in context, positions can converge prematurely. Each turn is influenced by previous turns, creating echo chambers.

**Solution:** Write each perspective to disk BEFORE reading others. Forces genuine independence.

## Workspace Structure

```
./tmp/parliament-{YYYYMMDD-HHMMSS}/
├── 00-input.md              # Original problem (immutable)
├── 01a-advocate.md          # Agent 1 output (isolated)
├── 01b-critic.md            # Agent 2 output (isolated)
├── 01c-systems.md           # Agent 3 output (isolated)
├── 01d-pragmatist.md        # Agent 4 output (isolated)
├── 01e-wildcard.md          # Agent 5 output (isolated)
├── 02-synthesis.md          # Reads all 01x files
├── 03-devils-advocate.md    # If >70% agreement
├── 04-decision.md           # Final framework
└── FINAL.md                 # Actionable output
```

## Naming Convention

- `{step}{letter}-{role}.md` for parallel agents (01a, 01b, 01c...)
- `{step}-{name}.md` for sequential synthesis steps
- `00-input.md` always contains original problem
- `FINAL.md` always contains actionable output

## Multi-Turn Execution

### Turn 1: Problem Framing

**Input:** User's problem statement
**Output:** `00-input.md`

```markdown
# Parliament Input

**Problem:** {user's problem}
**Context:** {relevant background}
**Constraints:** {known limitations}
**Success Criteria:** {measurable outcomes}
**Confidence Assessment:** {initial confidence %}
```

### Turn 2: Independent Perspectives (PARALLEL)

**Input:** `00-input.md` (ONLY)
**Output:** `01a-advocate.md`, `01b-critic.md`, etc.

**Critical:** Each agent reads ONLY `00-input.md`. No cross-reading.

```markdown
# {Role} Perspective

**Agent:** {archetype name}
**Timestamp:** {ISO timestamp}
**Input:** 00-input.md

## Position Statement
[2-3 sentences, clear thesis]

## Key Arguments (3-5)
1. **Argument Name**
   [Supporting evidence and reasoning]
   [Implications if correct]

2. **Argument Name**
   [...]

## Risks/Concerns
- [Risk 1]
- [Risk 2]

## Blind Spots (Self-Acknowledged)
[What might this perspective miss?]

## Confidence
[X]% - [Rationale]
```

### Turn 3: Synthesis

**Input:** ALL `01x-*.md` files
**Output:** `02-synthesis.md`

```markdown
# Synthesis

**Timestamp:** {ISO timestamp}
**Inputs:** 01a-advocate.md, 01b-critic.md, 01c-systems.md, ...

## Agreement Analysis

### High Agreement (>70%)
[Points where most agents agree]

### Moderate Agreement (40-70%)
[Points with mixed views]

### Low Agreement (<40%)
[Genuine disagreements]

## Common Ground
[What all perspectives share]

## Genuine Tensions
| Dimension | Advocate | Critic | Systems | Resolution |
|-----------|----------|--------|---------|------------|
| {aspect}  | {view}   | {view} | {view}  | {how to decide} |

## Integrated Position
[Synthesis statement that acknowledges all perspectives]

## Boundary Conditions
**Works when:**
- Condition 1
- Condition 2

**Fails when:**
- Condition 1
- Condition 2
```

### Turn 4: Devil's Advocate (CONDITIONAL)

**Trigger:** Agreement > 70% on core direction
**Input:** `02-synthesis.md`
**Output:** `03-devils-advocate.md`

```markdown
# Devil's Advocate Challenge

**Trigger:** Synthesis shows >70% agreement on: {direction}
**Purpose:** Prevent premature consensus

## Counter-Position
[The opposite of the emerging consensus, argued with full conviction]

## Evidence Against Consensus
1. [Counter-evidence 1]
2. [Counter-evidence 2]
3. [Counter-evidence 3]

## Unconsidered Scenarios
- What if {assumption} is wrong?
- What if {external factor} changes?
- What if {stakeholder} disagrees?

## Revised Confidence
Original consensus confidence: {X}%
After devil's advocate: {Y}%
Delta: {X-Y}% (healthy = 5-15% decrease)
```

### Turn 5: Decision Framework

**Input:** `02-synthesis.md`, `03-devils-advocate.md` (if exists)
**Output:** `04-decision.md`

```markdown
# Decision Framework

## Summary
[1-2 paragraph executive summary]

## Recommendation
[Clear recommendation with confidence level]

## Decision Tree
```
Problem: {description}
│
├─ IF {condition A}:
│   └─ THEN {approach 1}
│
├─ IF {condition B}:
│   └─ THEN {approach 2}
│
└─ ELSE:
    └─ {default approach}
```

## Success Metrics
- Metric 1: {measurable}
- Metric 2: {measurable}

## Risk Mitigation
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {risk} | {L/M/H} | {L/M/H} | {action} |

## Next Steps
1. [Immediate action]
2. [Short-term action]
3. [Medium-term action]
```

### Turn 6: Final Output

**Input:** All previous files
**Output:** `FINAL.md`

```markdown
# Parliament Decision: {Problem Title}

**Session ID:** parliament-{timestamp}
**Deliberation Time:** {duration}
**Agents Consulted:** {count}
**Final Confidence:** {%}

## Executive Summary
[3-5 sentences capturing the decision and rationale]

## Decision
{Clear, actionable decision}

## Key Considerations
- [Consideration 1]
- [Consideration 2]
- [Consideration 3]

## Dissenting Views
[Any minority perspectives that should be noted]

## Implementation
[How to execute this decision]

## Review Trigger
[When to revisit this decision]
```

## Anti-Groupthink Safeguards

### 1. Isolation Enforcement
- Agents cannot read each other's outputs
- Each agent reads ONLY the input file
- File system enforces isolation

### 2. Devil's Advocate Trigger
- Automatic at >70% agreement
- Must argue opposite with full conviction
- Typically reduces confidence by 5-15%

### 3. Blind Spot Acknowledgment
- Each agent must state what they might miss
- Synthesis specifically addresses blind spots
- Unknown unknowns explicitly surfaced

### 4. Confidence Calibration
- Track confidence throughout process
- Expect confidence to DECREASE as complexity revealed
- Final confidence lower than initial = healthy deliberation

## Resumability

Parliament sessions can be paused and resumed:

```bash
# Resume from last completed step
ls ./tmp/parliament-{timestamp}/
# Shows: 00-input.md, 01a-advocate.md, 01b-critic.md (stopped here)

# Continue from next step
# Read existing files, continue chain
```

## Cleanup

After session:

```bash
# Archive for reference
tar -czf parliament-{timestamp}.tar.gz ./tmp/parliament-{timestamp}/
mv parliament-{timestamp}.tar.gz ./archive/

# Or delete if not needed
rm -rf ./tmp/parliament-{timestamp}/
```
