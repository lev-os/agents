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
6. Handoff, for an agent that consumes earlier outputs (Turn 2+, a later wave, synthesis): for each consumed output, its session/turn/role and dispatch handle or task ID, the premises it was given (CANDIDATE unless verified), its exact file path, the judge or claim-audit result that accepted it (or `unchecked`), the tools and sources this agent may use, and unresolved dependencies

Every agent ends its output with the Handoff Return below. Compose the handoff from dispatch records, check results and each upstream Handoff Return, not from synthesis prose. Join entities, runs or revisions only through an explicit binding in those records; matching spelling is not a binding (a label shared across namespaces establishes neither that the entities are the same nor that they differ). Without a binding the relationship is UNKNOWN, not an identity or a contradiction. A missing field holds only that agent; independent agents in the turn still dispatch. When a consumed output fails its check or is superseded, invalidate every output accepted on it directly or transitively, including acceptance based on the superseded version: follow the handoffs, so in A→B→C a failed A invalidates B and C even when C's handoff lists only B. Re-brief and re-run those agents against the current output; outputs outside that chain stand. Agreement between agents is neither independent evidence nor proof of dispatch: treat it as corroboration only when their handoffs show separate sources or checks, and count an agent only from its returned dispatch result.

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

### Handoff Return
[Inputs read with their source/run identity; premises relied on (CANDIDATE unless verified); exact artifacts written; checks run and results, or none; unresolved dependencies]
```

**BD Notes Submission**: If BD is active, each agent's output path + summary gets stored in the BD turn task notes:
```bash
bd update {turn-task} --notes="Agent {role}: {1-line summary}. File: tmp/cdo-{session}/t{N}-{role}.md"
```
