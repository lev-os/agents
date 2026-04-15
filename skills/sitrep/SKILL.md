---
name: sitrep
description: "Situation report — live dashboard when things are flowing. Shows all entities, their lifecycle mode, gate scores, and what's next. The /lev dashboard for mid-execution. Invoke as /sitrep (alias: /siterep)."
triggers:
  - sitrep
  - siterep
  - status
---

# /sitrep — Situation Report

Quick live dashboard. Use mid-flow when multiple things are executing. Shows what every entity is doing RIGHT NOW.

## When to Use

- Mid-execution: multiple items flowing through lifecycle
- After a /ll tick: what changed?
- When you lose track: "what's happening?"
- Before /interview: what decisions are collected?

## Protocol

### 1. Scan Active State

Read from (in order, stop when you have enough):
1. TaskList (in-session tasks)
2. `.lev/pm/workstreams/*/state/workstream.yaml` (active workstreams)
3. `.lev/pm/handoffs/` (latest handoff for current workstream)
4. `git log --oneline -5` (what just shipped)

### 2. Classify Each Entity

Every item is in exactly ONE mode:

| Mode | Symbol | Meaning |
|------|--------|---------|
| /capture | `📥` | Shape→Plan: classifying, routing, scoring fidelity |
| /exec | `⚡` | Executing: code, flows, agents running |
| /work | `🔄` | Router: deciding what to do next |
| /hygiene | `🧹` | Maintenance: drift check, orphan scan, footer check |
| /pause | `⏸️` | Waiting: needs human decision or external input |
| /done | `✅` | Completed this session |

### 3. Render Dashboard

```
## /sitrep — {workstream} — {timestamp}

### Active ({count})
⚡ {item} — gate: {gate_name} = {score} — next: {verb}
⚡ {item} — gate: {gate_name} = {score} — next: {verb}
📥 {item} — fidelity: {score} — route: {target}

### Paused ({count})
⏸️ {item} — needs: {what_decision} — since: {when}

### Done This Session ({count})
✅ {item} — {one_line_result}

### Queue ({count} remaining)
Next 3: {item1}, {item2}, {item3}

### Loop
🔁 /ll: tick {N} — next: {delay} — mode: {self-pacing|fixed}

---
🧬 {workstream} | 📐 {overlays} | 🎯 {stage}
⏭️  Next: {next_verb}
🚦 Gate: {gate} = {state}
🌀 Decision: {decision}
---
```

### 4. Decision Collector

If any items are paused, show the **decision collector** at the bottom:

```
### Decisions Needed ({count})
1. {item}: {question} — options: a) {opt_a} b) {opt_b}
2. {item}: {question} — options: a) {opt_a} b) {opt_b}

→ Answer inline or /interview for guided mode
```

When ALL items are paused → auto-trigger: `flowmind://arch-interview-brief → /interview`

### 5. Metrics Bar (optional, when data available)

```
📊 Session: {commits} commits | +{added}/-{deleted} LOC | {files} files | {duration}
```

## Rules

- **Fast**: /sitrep should complete in < 5 seconds. No research, no prior-art.
- **Live**: Show current state, not historical. Read TaskList + git, not handoff archaeology.
- **Graph footer**: ALWAYS present (UX drift enforcement).
- **Bucketed**: Max 5 active items shown. Rest in queue count.
- **Actionable**: Every item shows what's next. No items without a next action.

## Aliases

- `/sitrep` = full dashboard (canonical name)
- `/siterep` = same thing (legacy spelling)
- `/status` = same thing
- `/sitrep --brief` = just the active items + loop state (3 lines max)
