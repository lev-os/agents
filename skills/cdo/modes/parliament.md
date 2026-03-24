---
name: cdo-parliament
description: Full 5-role parliament protocol with multi-model diversity and anti-groupthink safeguards
---

# CDO Parliament Protocol

Multi-agent deliberation with enforced independence, protected dissent, and groupthink detection.

---

## Core Principles

1. **Independence First** — Each agent forms views BEFORE seeing others' positions. No anchoring bias.
2. **Full Conviction** — No hedging. Every agent commits to a clear position. "It depends" is banned.
3. **Synthesis Second** — Integration happens ONLY after all perspectives are collected. Never during.
4. **Dissent Protected** — Minority views are documented, never suppressed. A lone dissenter may be the only one who's right.
5. **Confidence Calibrated** — Expect uncertainty to INCREASE as you learn more. If confidence only goes up, you're doing it wrong.

---

## Parliament Sizes

### Minimum (3 roles)

| Role | Focus | Bias Direction |
|------|-------|----------------|
| **Advocate** | Best case for the proposal | Optimistic |
| **Critic** | Failure modes, risks, costs | Pessimistic |
| **Synthesizer** | Integration, trade-offs, decision | Neutral |

### Standard (5 roles)

Adds to minimum:

| Role | Focus | Bias Direction |
|------|-------|----------------|
| **Systems Thinker** | Second-order effects, coupling, feedback loops | Systemic |
| **Pragmatist** | What actually ships, total cost of ownership | Practical |

### Extended (7-10 roles)

Additional specialists drawn from:

| Role | Focus | When to Include |
|------|-------|-----------------|
| **Wild Card** | Unconventional framing, lateral thinking | Always useful, especially when stuck |
| **Security Expert** | Attack surface, threat modeling | Security-sensitive decisions |
| **Economist** | Resource allocation, opportunity cost | Budget/staffing decisions |
| **Domain Specialist** | Deep expertise in the specific area | Technical depth needed |
| **Devil's Advocate** | Forced opposition to majority | When agreement comes too fast |

---

## Deliberation Rounds

### Round 1: Position Papers (Parallel)

All agents write position papers simultaneously. No visibility into others' work.

**Agent Prompt Template**:
> You are the [ROLE]. Analyze this question independently:
> "[QUESTION]"
>
> Write a position paper with:
> 1. Your clear position (no hedging)
> 2. Key evidence/reasoning (3-5 points)
> 3. Biggest risk if your position is wrong
> 4. Confidence level (0-100%)
>
> You have NOT seen anyone else's position. Form your own view first.

### Round 2: Cross-Examination (Optional)

Each agent reads all position papers and responds to the strongest counter-argument.

**Agent Prompt Template**:
> You've read all position papers. The strongest challenge to your view is [AGENT]'s point about [X].
> Respond: Does this change your position? If yes, how? If no, why not?
> Update your confidence level.

**When to skip**: If time-constrained or positions are already well-differentiated.

### Round 3: Synthesis

The Synthesizer (or designated integrator) produces a unified analysis.

**Synthesizer Prompt**:
> Given all position papers and cross-examination:
> 1. Where is there genuine agreement? (not just similar words — same reasoning)
> 2. Where is there genuine disagreement? (not resolvable by more information)
> 3. What are the key trade-offs?
> 4. What is the recommended decision and why?
> 5. What conditions would reverse this recommendation?

### Round 4: Devil's Advocate (Triggered)

**Trigger**: >70% agreement after Round 3.

**Devil's Advocate Prompt**:
> The parliament has reached strong agreement on [POSITION].
> Your job: find the strongest possible argument AGAINST this consensus.
> Consider: What are we all missing? What assumption are we all making?
> What would make this decision catastrophically wrong?
>
> You must argue against the consensus even if you personally agree with it.

### Round 5: Decision Framework

Final output with actionable decision.

```markdown
## Decision: [CLEAR STATEMENT]

## Confidence: [X%]

## Key Arguments For
1. ...
2. ...

## Key Arguments Against
1. ...
2. ...

## Dissenting Views
- [ROLE]: [position] — [reasoning]

## Conditions That Would Reverse This Decision
1. ...

## Recommended Next Actions
1. ...
```

---

## Voting & Consensus

| Consensus Level | Range | Interpretation | Action |
|----------------|-------|----------------|--------|
| **Unanimous** | 100% | Check for groupthink | Trigger Devil's Advocate round |
| **Strong** | 80-99% | Good signal | Proceed, document dissent |
| **Majority** | 51-79% | Proceed with caution | Flag risks, set review triggers |
| **Split** | ~50% | Need more deliberation | Add Round 2, bring in specialists |
| **No Majority** | <50% | Genuine uncertainty | Escalate or defer decision |

---

## Dissent Management

**Rules**:
- Dissenting views MUST be documented in the final output. Non-negotiable.
- Dissent CANNOT be overridden by vote — it persists as a risk flag.
- Dissent creates an automatic review trigger: revisit the decision when new evidence arrives.
- The dissenter's reasoning must be captured, not just their position.

**Dissent Template**:
```markdown
## Dissent Record
- **Who**: [role]
- **Position**: [what they argued]
- **Reasoning**: [why — the important part]
- **Trigger**: [what would prove them right]
- **Review Date**: [when to revisit]
```

---

## Groupthink Detection

### Warning Signs

- Unanimous agreement reached in Round 1 (too fast)
- No blind spots identified by any agent
- Confidence increasing every round (should fluctuate)
- All agents using the same framing/language
- No agent changed their position after cross-examination
- Risk assessment is uniformly low

### Response Protocol

When 2+ warning signs detected:

1. **Force Devil's Advocate** — Even if agreement is below 70%
2. **Reframe the Question** — Ask the same question from a completely different angle
3. **Add a Wild Card** — Bring in an agent with no domain context for fresh eyes
4. **Steelman the Opposition** — Each agent must argue the strongest case AGAINST their own position
5. **Inversion** — "What would have to be true for the OPPOSITE decision to be correct?"

---

## Multi-Model Diversity

For maximum perspective diversity, assign different models to different roles when available:

- Analytical roles (Critic, Systems Thinker) → models strong at reasoning
- Creative roles (Wild Card, Advocate) → models strong at generation
- Integration roles (Synthesizer, Pragmatist) → models strong at summarization

Model diversity reduces correlated blind spots. Same model, same training data, same biases.
