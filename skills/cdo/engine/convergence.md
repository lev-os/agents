---
name: cdo-convergence
description: Four convergence criteria types — when to stop the turn loop
---

# Convergence Criteria

Four types of convergence, chosen per-workflow. Every workflow MUST declare which type it uses.

## Type 1: Turn Count (fixed structure)

For debug workflows and presets with fixed turns. Stop when all defined turns complete.

No confidence tracking needed — the structure IS the convergence. Use when the problem is well-understood and the number of perspectives is known in advance.

## Type 2: Confidence Threshold (iterative)

Stop when `confidence >= threshold` OR `max_iterations` reached. Always include `max_iterations` as a safety valve — never allow unbounded iteration.

```
Turn 1: hypotheses       → confidence 0.60
Turn 2: test hypotheses  → confidence 0.75
Turn 3: refine           → confidence 0.88  STOP
```

The threshold comes from the preset or workflow config. Typical values:

- Quick decisions: `0.75`
- Architecture/design: `0.85`
- Security/compliance: `0.90`

## Type 3: Perspective Coverage (fan-out)

Stop when all requested perspectives collected + synthesis complete.

This is the "gather all viewpoints" mode. The workflow declares which perspectives are required, agents fan out in parallel, and convergence is met when every perspective has been covered and synthesized.

No iterative refinement — one turn of gathering, one synthesis, done.

## Type 4: Resonance Loop (convergence delta)

Stop when consecutive iterations show <10% change in output OR `max_iterations` reached. This is the most sophisticated type — it finds the natural resting point.

```
loop:
  - synthesize-current
  - critique-synthesis
  - integrate-critique
  - check: delta < 0.10 AND confidence >= 0.85?
      yes: exit
      no: continue (up to max)
```

Delta is measured by the synthesizer comparing its current output to the previous iteration. If the substance isn't changing, the system has converged naturally.

## Validation Checklist

Before declaring ANY workflow complete, verify:

- [ ] Exit criteria met (type-specific check above)
- [ ] All artifact files exist on disk
- [ ] `FINAL.md` exists with full synthesis
- [ ] Max iterations not exceeded (or forced-FINAL if they were)
- [ ] Confidence documented in final synthesis
