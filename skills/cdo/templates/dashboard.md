---
name: cdo-dashboard-template
description: Planning dashboard format — auto view, HITL interactive DAG, and the wave plan
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

**Wave Plan Dashboard** (plan modifier; shown before T1, re-rendered after every edit):
```
═══════════════════════════════════════════════════════════
  CDO WAVE PLAN — {PROBLEM}
═══════════════════════════════════════════════════════════
  Goal: {goal}
  Acceptance: A1 {criterion}  |  A2 {criterion}  |  ...
  Judge: {fresh judge agent | + plugin completion_gate receipt}
  Budget: {max_waves} waves  |  {n} without progress  |  {wall_clock}
───────────────────────────────────────────────────────────
  W1 {purpose}                                  targets: A1
    ├─ W1N1 {role} [skills: {s1}]
    ├─ W1N2 {role} [skills: {s1}, {s2}, {s3}]
    └─ → Synthesizer → Judge
  W2 {purpose}                                  targets: A1, A2
    ├─ W2N1 {role} [skills: {s1}, {s2}, {s3}, {s4}, {s5}]
    └─ → Synthesizer → Judge
  ...
  W{N} {purpose}                                targets: A{k}
───────────────────────────────────────────────────────────
  {S} distinct skills across {M} nodes (1-5 per node)
  Backend: {Agent tool | TeamCreate | Lev plugin | Workflow (opt-in)}
═══════════════════════════════════════════════════════════

🪄 Edit the plan:
1. Approve and run
2. Add, remove or reorder waves
3. Add or remove nodes in a wave
4. Swap skills on a node, or change its count (1-5)
5. Re-run skill discovery for a node
6. Change acceptance criteria, judge or budget
7. All of the above: edit everything
8. ⬅️ Back
```

**Wave Progress** (plan or judge; shown after each judge verdict):
```
───────────────────────────────────────────────────────────
  WAVE {N} JUDGED — {satisfied | not satisfied}
───────────────────────────────────────────────────────────
  Criteria: A1 met  |  A2 unmet ({evidence})  |  ...
  Planned W{N+1}: {purpose} [{nodes} nodes]
  Actual  W{N+1}: {kept | amended: {change} | replaced: {why}}
  Budget: {used}/{max} waves  |  {n} without progress
───────────────────────────────────────────────────────────
```
