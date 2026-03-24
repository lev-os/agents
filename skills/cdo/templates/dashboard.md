---
name: cdo-dashboard-template
description: Planning dashboard format — auto view + HITL interactive DAG
---

**Auto Dashboard** (shown for deep+, non-interactive):
```
═══════════════════════════════════════════════════════════
  CDO DELIBERATION — {PROBLEM}
═══════════════════════════════════════════════════════════
  Preset: {preset}  |  Modifiers: {flags}  |  Domain: {domain}
───────────────────────────────────────────────────────────
  PROPOSED DAG

  Turn 1 ({width} agents):
    ├─ {Role 1} [skills: {s1}, {s2}]
    ├─ {Role 2} [skills: {s1}, {s2}]
    └─ {Role 3} [skills: {s1}, {s2}]
    → Synthesizer

  Turn 2-N: Shaped by Turn 1 synthesis (adaptive)
───────────────────────────────────────────────────────────
  BD: {epic-id} ({status})
  Team: {team-name} ({mode})
  Max Turns: {max}  |  Convergence: {type} @ {threshold}
───────────────────────────────────────────────────────────
  Estimated: {N} turns, {M} total agents
═══════════════════════════════════════════════════════════
```

**HITL Dashboard** (interactive, when hitl flag set):
Same as above PLUS:
```
───────────────────────────────────────────────────────────
  SKILL SELECTION

  Discovered skills for this problem:
  1. {skill-name} (relevance: {score}) — {1-line description}
  2. {skill-name} (relevance: {score}) — {1-line description}
  ...

  Power combos available:
  • {combo-name}: {skill1} → {skill2} → {skill3}
  • {combo-name}: {skill1} → {skill2}
───────────────────────────────────────────────────────────

🪄 Configure Turn 1:
1. Accept proposed DAG as-is
2. Add/remove agent roles
3. Swap skills on agents
4. Change width (more/fewer agents)
5. Select power combo for this turn
6. Change preset
7. All of the above: customize everything
8. ⬅️ Back
```

**Per-Turn Status Update** (shown after each synthesis):
```
───────────────────────────────────────────────────────────
  TURN {N} COMPLETE — Confidence: {X}%
───────────────────────────────────────────────────────────
  Common Ground: {brief}
  Tensions: {count} unresolved
  Gaps: {count} remaining

  Next Turn Directive:
    Width: {N} agents
    Focus: {summary}
───────────────────────────────────────────────────────────
```
