---
name: cdo-synthesis-protocol
description: Synthesizer agent prompt template and anti-groupthink safeguards
---

# Synthesis Protocol

## Synthesizer Role

Dedicated agent dispatched AFTER each turn's agents complete. Reads ALL turn artifacts + prior synthesis. The synthesizer is never the orchestrator — always a separate agent.

## Synthesizer Prompt Template

```
# Turn {N} Synthesis

Read all Turn {N} agent artifacts and produce:

1. COMMON GROUND: Where do agents agree? (with evidence)
2. TENSIONS: Where do they genuinely disagree? (not surface disagreements)
3. GAPS: What perspectives or analysis are still missing?
4. SURPRISES: Did any agent surface something unexpected?
5. CONFIDENCE: Overall confidence in current state (0-100%)
6. NEXT TURN DIRECTIVE: (see adaptive-turns.md format)

## Anti-Groupthink Check
- If all agents agree → FLAG as potential groupthink
- If confidence only went UP from last turn → FLAG as suspicious
- Healthy deliberation sees confidence DIP then stabilize

## BD Report (if BD tracking active)
Summary: {2-3 sentences}
Files: {list of artifact paths}
Confidence: {score}
Gaps remaining: {count}

Write to: tmp/cdo-{session}/t{N}-synthesis.md
```

## Devil's Advocate Trigger

If synthesis finds >70% agreement AND confidence is rising, automatically add a devil's advocate agent to the next turn with directive:

> "Argue the opposite of the current consensus with full conviction."

This is not optional. Unanimous agreement is a smell — the system must pressure-test it before accepting convergence.

## BD Integration

After synthesis, update tracking:

```bash
bd close {current-turn-task} --reason "confidence {X}%, {N} gaps, {M} tensions"

# If not converged:
bd create --type=task --title="T{N+1}: {focus from directive}" --parent={epic-id}
```

## Final Synthesis

When convergence is met, the FINAL synthesis agent reads ALL artifacts across ALL turns and produces `FINAL.md` with:

- **Problem restatement** — what was actually asked
- **Key findings** — organized by turn, showing how understanding evolved
- **Recommendations** — with confidence levels per recommendation
- **Dissenting views** — minority opinions preserved, not buried
- **Action items** — concrete next steps
- **Decision log** — what was decided and why, with evidence trail
