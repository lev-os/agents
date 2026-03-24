---
name: cdo-presets
description: Full preset configurations, modifier docs, and arg parse examples
---

# CDO Presets & Modifiers

Complete reference for preset configurations, stackable modifiers, and argument parsing.

---

## Preset Defaults

| Setting | `quick` | `think` | `deep` | `full` | `debug` |
|---------|---------|---------|--------|--------|---------|
| **Width** | 1-2 | 2-4 | 3-8 | 5-20 | 1-3 |
| **Max Turns** | 1 | 2-3 | 3-5 | 5-10 | 7 (fixed) |
| **BD Tracking** | No | No | Yes | Yes | No |
| **Skill Discovery** | No | Optional | Yes | Yes | No |
| **Team Mode** | Subagents | Subagents | TeamCreate | TeamCreate | Subagents |
| **Dashboard** | No | No | Yes | Yes | No |
| **Adaptive** | No | No | No | Yes | No |
| **Convergence** | N/A | Perspective | Confidence | Resonance | Turn Count |
| **Default Threshold** | N/A | N/A | 0.80 | 0.85 | 7 turns |

### Preset Descriptions

**`quick`** — Fast parallel query. 1 turn, 1-2 agents, no overhead. For questions with known structure.

**`think`** — Light deliberation. 2-3 turns, multiple perspectives. Good for design questions, trade-off analysis.

**`deep`** — Full analysis with tracking. TeamCreate for persistent agents, BD tracking for accountability, skill discovery for capability expansion.

**`full`** — Maximum depth. Adaptive width, resonance-based convergence, parliament protocol available. For high-stakes decisions.

**`debug`** — Fixed 7-turn RCA workflow. See `skill://cdo/modes/debug` for the full protocol.

---

## Modifiers

Modifiers stack on any preset. They override specific settings without changing the rest.

### `hitl` — Human in the Loop

User involved in every turn's planning phase. Enables:
- Interactive DAG visualization before each turn
- Skill selection approval
- Power combo suggestions
- Redirect/abort at any turn boundary

**Effect**: Adds user checkpoint between turns. Does not change width or depth.

### `bd` — BD Tracking

Force beads issue tracking even for `quick`/`think` presets.

**Effect**: Creates BD task at start, updates on completion, links discovered work.

### `team` — TeamCreate Mode

Force persistent team creation even for `quick`/`think` presets.

**Effect**: Uses TeamCreate instead of subagents. Agents persist across turns with shared context.

### `adaptive` — Dynamic Width

Width varies per turn based on results. Auto-enabled for `full` preset.

**Effect**: Turn engine evaluates after each turn — expand width if confidence is low, narrow if converging.

### `lev-exec` — Multi-Model Dispatch

Route different roles to different models via codex CLI or OpenRouter.

**Effect**: Enables model diversity. Analytical roles get reasoning-optimized models, creative roles get generation-optimized models.

---

## Arg Parse

### Format

```
/cdo [modifiers,]<preset> [domain] "question or task"
```

- **Modifiers**: Comma-separated, before preset
- **Preset**: Required (or inferred from modifiers)
- **Domain**: Optional team domain (`dev`, `arch`, etc.)
- **Question**: The actual task/question in quotes

### Examples

```
/cdo think "question"
```
Think preset, no modifiers, no domain.

```
/cdo hitl "question"
```
Deep preset (inferred — hitl implies deliberation), hitl modifier active.

```
/cdo bd,full "question"
```
Full preset with explicit BD tracking.

```
/cdo adaptive,team,full "question"
```
Full preset with adaptive width and TeamCreate.

```
/cdo exec dev "task"
```
Deep preset (inferred), dev domain team, lev-exec dispatch.

```
/cdo lev-exec,full "compare frameworks"
```
Full preset with multi-model dispatch.

```
/cdo debug "why is X broken"
```
Debug preset — fixed 7-turn RCA. No modifiers apply (debug has its own protocol).

### Inference Rules

- If no preset specified but modifiers present → infer `deep`
- `debug` ignores all modifiers (fixed protocol)
- Domain can appear with any preset
- Conflicting modifiers: last one wins

### Inline Overrides

Users can always override width and turns inline:

```
/cdo deep "question" — 3 turns, 5 wide
/cdo full "question" — just 2 agents
/cdo think "question" — 1 turn only
```

Inline overrides take precedence over preset defaults.
