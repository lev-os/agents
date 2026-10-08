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

### `plan` — Wave Plan

Plan the whole run before T1: up to 10 waves (or the user's number), each with nodes, and 1-5 discovered skills per node. Show the Wave Plan dashboard, let the user edit it, and run only after explicit approval.

**Effect**: Adds a planning phase and the Wave Plan dashboard. Implies `judge`. The plan is a forecast: the previous synthesis directive and the judge's unmet criteria may amend each wave. See `references/wave-planner.md`.

### `judge` — Judged Exit

An independent judge decides whether the run satisfied acceptance criteria frozen before T1.

**Effect**: Replaces the confidence exit with Type 5 convergence (`engine/convergence.md`). Not satisfied and budget remains → another wave aimed at the unmet criteria. Budget exhausted → FINAL.md reports the unmet criteria.

### `modes` — Reasoning Operators

Run reasoning modes as bounded operators on pivotal questions, with an independent claim audit before synthesis.

**Effect**: Turn 0 writes a decision contract and a neutral case file. Synthesis audits claims before it writes the directive. See `references/reasoning-operators.md`.

### `reality` — Reality Check

Measure what is built against the stated vision, then plan, push and refine the bridge.

**Effect**: Turn 0 builds the vision checklist. Later turns run gap analysis, bridge planning, ambition waves and refinement waves. See `references/reality-check.md`.

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

```
/cdo plan,full "design our release process"
```
Full preset. Plan the waves and the skills for each node, approve, then run with a judge.

```
/cdo judge,deep "make the flaky test suite reliable"
```
Deep preset. A judge on frozen criteria decides when to stop.

```
/cdo modes,reality,deep "where does project X stand against its vision?"
```
Deep preset. A vision checklist, then reasoning operators with a claim audit.

### Inference Rules

- If no preset specified but modifiers present → infer `deep`
- `debug` ignores all modifiers (fixed protocol)
- Domain can appear with any preset
- Conflicting modifiers: last one wins
- `plan` implies `judge`

### Inline Overrides

Users can always override width and turns inline:

```
/cdo deep "question" — 3 turns, 5 wide
/cdo full "question" — just 2 agents
/cdo think "question" — 1 turn only
```

Inline overrides take precedence over preset defaults.
