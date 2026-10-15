---
name: cdo-agent-composition
description: How CDO agents get their roles, skills, and prompts — the agent brief format
---

**Agent Brief Template**: Each agent receives:
1. Role (perspective to take)
2. Skills (2-3 skill contents injected inline)
3. Input files (which artifacts to read)
4. Output: a file to write only when its supplied tools include Write; otherwise the caller persists the text it returns (a return path grants no Write)
5. Constraint: argue with full conviction, no hedging
6. Handoff, for an agent that consumes earlier outputs (Turn 2+, a later wave, synthesis): for each consumed output, its session/turn/role and dispatch handle or task ID, the premises it was given (CANDIDATE unless verified), its exact file path, the judge or claim-audit result that accepted it (or `unchecked` when none is recorded), the tools, effects and sources this agent may use (at most those the caller supplied), and unresolved dependencies

Every agent ends its output with the Handoff Return below. Compose each brief in this order:

1. Inventory each supplied worker record under its own exact identity (dispatch handle or task ID, role): its task, status, revisions, input and return paths, and tools, as recorded. Each fact stays with its own record even when no relationship to another record is established: doubt about a relationship is not doubt that the recorded entity exists, and a supplied field is never reported as unrecorded.
2. Build the requested worker's brief from its own record and the current task. Its requested task stays the job, and its supplied return path stays its return path (a return path grants no Write). An unknown join never removes the record, replaces the job or adds a prerequisite or seat. Unresolved scope never widens authority either: keep each caller restriction that may apply, give the narrower work product that all of them permit when it still advances the task, and otherwise hold only the action that depends on that scope for its owner to resolve.
3. Bind consumed history only through explicit records. Compose each handoff entry only from the dispatch records, check results and Handoff Return that carry its dispatch handle or task ID, not from synthesis prose or recalled history. Join entities, runs or revisions only through an explicit binding in those records; matching spelling is not a binding (a label shared across namespaces establishes neither that the entities are the same nor that they differ). An assumption, a CANDIDATE mark or a request to confirm later does not supply the binding.
4. Without a binding the relationship is UNKNOWN, not an identity or a contradiction. Describe it in Context apart from the worker's own record, and list it under unresolved dependencies as a lookup for the missing binding, never as a consumed output, premise or Problem.
5. Scope each absence to the records searched: a null or missing field means unrecorded there, not that the run or check never happened. A missing field holds only that agent; independent agents in the turn still dispatch.
6. Judge progress and stopping on the combined wave result against the run's actual wave, no-progress and wall-clock budgets. Only actual useful results under the caller's progress test count as progress; a returned message alone does not. One blocked agent is that branch's result, and it does not make the wave a no-progress wave while an independent agent can still advance.
7. When a consumed output fails its check or is superseded, invalidate every output accepted on it directly or transitively, including acceptance based on the superseded version: follow the handoffs, so in A→B→C a failed A invalidates B and C even when C's handoff lists only B. Re-brief and re-run those agents against the current output; outputs outside that chain stand.
8. Agreement between agents is neither independent evidence nor proof of dispatch: treat it as corroboration only when their handoffs show separate sources or checks, and count an agent only from its returned dispatch result.

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
