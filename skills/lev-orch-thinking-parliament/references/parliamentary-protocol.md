# Parliamentary Protocol Reference

Rules and procedures for multi-agent deliberation.

## Core Principles

1. **Independence First:** Each agent forms views before seeing others
2. **Full Conviction:** Agents argue their perspective without hedging
3. **Synthesis Second:** Integration only after all perspectives collected
4. **Dissent Protected:** Minority views documented, not suppressed
5. **Confidence Calibrated:** Expect uncertainty to increase, not decrease

## Agent Composition

### Minimum Parliament (3 agents)
- Advocate (FOR)
- Critic (AGAINST)
- Synthesizer (INTEGRATE)

### Standard Parliament (5 agents)
- Advocate
- Critic
- Systems Thinker
- Pragmatist
- Wild Card

### Extended Parliament (7-10 agents)
Add specialized perspectives as needed:
- User Advocate
- Security Expert
- Economist
- Historian
- Futurist
- Domain Specialist
- Devil's Advocate (auto-triggered)

## Deliberation Rounds

### Round 1: Position Papers
Each agent writes independent position paper.

**Duration:** 1 turn per agent (parallel)
**Output:** Numbered position files

**Requirements:**
- Clear thesis statement
- 3-5 supporting arguments
- Evidence for each argument
- Self-acknowledged blind spots
- Confidence percentage

### Round 2: Cross-Examination (Optional)
Agents can challenge each other.

**Duration:** 1-2 turns
**Output:** Challenge/response files

**Format:**
```markdown
## Challenge to {Agent}

**From:** {challenging agent}
**Re:** {specific argument}

### Challenge
[Why this argument may be weak]

### Response Required
[Specific question to answer]
```

### Round 3: Synthesis
Read all position papers, integrate.

**Duration:** 1 turn
**Output:** synthesis.md

**Must include:**
- Common ground
- Genuine tensions
- Proposed resolution
- Confidence assessment

### Round 4: Devil's Advocate (Conditional)
Triggered when agreement > 70%.

**Duration:** 1 turn
**Output:** devils-advocate.md

**Rules:**
- MUST argue opposite of consensus
- MUST argue with full conviction
- MUST provide counter-evidence
- Cannot hedge or qualify

### Round 5: Decision Framework
Create actionable output.

**Duration:** 1 turn
**Output:** decision.md, FINAL.md

## Voting and Consensus

### Formal Vote (when needed)
```
Motion: {proposed decision}

Votes:
├─ Agent 1 (Advocate): FOR / AGAINST / ABSTAIN
├─ Agent 2 (Critic): FOR / AGAINST / ABSTAIN
├─ Agent 3 (Systems): FOR / AGAINST / ABSTAIN
├─ Agent 4 (Pragmatist): FOR / AGAINST / ABSTAIN
└─ Agent 5 (Wild Card): FOR / AGAINST / ABSTAIN

Result: {majority} / {unanimous} / {split}
```

### Consensus Levels

| Level | Agreement | Interpretation |
|-------|-----------|----------------|
| Unanimous | 100% | Strong signal, check for groupthink |
| Strong Consensus | 80-99% | Good signal, note dissent |
| Majority | 51-79% | Proceed with caution |
| Split | ~50% | Need more deliberation or decision framework |
| Minority | <50% | Significant opposition, explore why |

## Dissent Management

### Recording Dissent
```markdown
## Dissenting Opinion

**Agent:** {name}
**Position:** AGAINST majority on {issue}

### Rationale
[Why this agent disagrees]

### Conditions for Revisiting
[When majority should reconsider]

### Risk if Majority Proceeds
[What could go wrong]
```

### Dissent Rights
- Dissenting views MUST be documented
- Dissent cannot be overridden, only noted
- Dissent creates automatic review trigger
- Dissenter can request devil's advocate round

## Time Management

### Quick Parliament (30-60 min)
- 3 agents
- 1 round of position papers
- Direct to synthesis
- Skip cross-examination

### Standard Parliament (1-2 hours)
- 5 agents
- Position papers
- Optional cross-examination
- Full synthesis
- Devil's advocate if triggered

### Deep Parliament (2-4 hours)
- 7-10 agents
- Full position papers
- Cross-examination
- Multiple synthesis rounds
- Devil's advocate
- Decision framework iteration

## Emergency Protocols

### Deadlock Resolution
If parliament cannot reach decision:

1. **Reframe Problem:** Maybe question is wrong
2. **Add Agent:** Bring new perspective
3. **Time Box:** Decide with available info
4. **Escalate:** Human decision maker

### Groupthink Detection
Warning signs:
- Unanimous agreement too quickly
- No blind spots identified
- Confidence increasing
- No devil's advocate triggered

**Response:** Force devil's advocate round

### Agent Failure
If an agent produces low-quality output:

1. **Re-prompt:** Clarify requirements
2. **Replace:** Spawn new agent with same role
3. **Continue:** Proceed with remaining agents

## Integration with BD

### Task Tracking
```bash
# Each agent = BD task
bd create --type=task --title="[A1] Advocate position"
bd create --type=task --title="[A2] Critic position"
# ... etc

# Synthesis = task
bd create --type=task --title="[SYN] Parliament synthesis"

# Decision = task
bd create --type=task --title="[DEC] Decision framework"
```

### Session Persistence
For multi-session parliaments:

```bash
# Save session state
bd update {epic-id} --description="
## Parliament State
- Completed: Agents 1-3
- Pending: Agents 4-5
- Next: Cross-examination
- Files: ./tmp/parliament-{timestamp}/
"
```

## Quality Checks

Before finalizing:

- [ ] All agents submitted position papers
- [ ] Each paper has clear thesis
- [ ] Each paper has 3+ arguments
- [ ] Blind spots acknowledged
- [ ] Synthesis covers all perspectives
- [ ] Dissent documented
- [ ] Confidence calibrated (should be lower than start)
- [ ] Decision is actionable
- [ ] Next steps are clear
