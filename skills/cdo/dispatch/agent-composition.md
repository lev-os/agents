---
name: cdo-agent-composition
description: How CDO agents get their roles, skills, and prompts — the agent brief format
---

**Agent Brief Template**: Each agent receives:
1. Role (perspective to take)
2. Skills (2-3 skill contents injected inline)
3. Input files (which artifacts to read)
4. Output file (where to write)
5. Constraint: argue with full conviction, no hedging

**Standard CDO Roles** (5-role parliament):
| Role | Perspective | Prompt Directive |
|------|------------|-----------------|
| Advocate | Strongest case FOR | "Build the most compelling argument FOR this approach" |
| Critic | Strongest case AGAINST | "Find every weakness, risk, and failure mode" |
| Systems Thinker | Second-order effects | "Map feedback loops, coupling, emergent behaviors" |
| Pragmatist | Implementation reality | "What actually ships? What's the MVP? What breaks?" |
| Wild Card | Unconsidered alternatives | "What if we're solving the wrong problem entirely?" |

**Extended Roles** (add as needed):
- Security Analyst, Financial Analyst, User Advocate, Historian, Domain Specialist

**Agent Output Format**: Each agent MUST write:
```markdown
### Position Statement
[2-3 sentences, clear thesis]

### Key Arguments (3-5)
[Numbered, with evidence]

### Implications
[What happens if this view is correct?]

### Blind Spots
[What might this perspective miss?]

### Confidence
[0-100%, with justification]
```

**BD Notes Submission**: If BD is active, each agent's output path + summary gets stored in the BD turn task notes:
```bash
bd update {turn-task} --notes="Agent {role}: {1-line summary}. File: tmp/cdo-{session}/t{N}-{role}.md"
```
