---
name: momentum-anchor
description: Create rich resumption points when hyperfocus breaks. Capture energy state, not just tasks. Use at the end of work sessions, when interrupted, or when sensing focus shifting.
skill_evolver:
  enabled: true
  version: 1.0.0
  log_path: ~/.config/lev/logs/skills.jsonl
  hooks:
    - on_invoke
    - on_fail
    - on_success
---

# Momentum Anchor

This skill provides specialized support for capturing the full cognitive state when hyperfocus breaks, creating rich resumption points that preserve energy and context rather than just task lists.

## Purpose

To capture the complete state of mind when hyperfocus ends, enabling effective resumption by preserving energy signatures, held questions, and RAM contents - not merely task status.

## When to Use This Skill

Use this skill:
- At the end of work sessions
- When interrupted during hyperfocus
- When sensing focus shifting to different work
- Before walking away from active development
- When needing to context-switch

## How to Use This Skill

### What to Capture: Energy Snapshot, Not Todo List

**State of mind**
- What felt alive right before stopping
- Questions being held (even unarticulated ones)
- Insights forming (even if incomplete)
- Energy direction and momentum

**Multiple re-entry points**

Create paths for different return states:

1. **Quick win path** - If returning with low energy
   - Small, achievable next step
   - No context rebuilding required
   - Immediate forward progress possible

2. **Deep dive path** - If returning with high momentum
   - Complex challenge waiting
   - Rich context available
   - Continuation of flow state

3. **Tangent path** - If returning curious about something adjacent
   - Related explorations
   - Connections to other work
   - Questions that branched off

4. **Walk away path** - If this isn't what's needed now
   - How to cleanly disengage
   - What to preserve for later
   - Where to redirect energy

**RAM contents (what's in working memory)**
- Assumptions made that aren't in code or notes
- Things "about to" be done
- Tradeoffs being considered
- Patterns noticed but not yet documented
- Mental models actively held
- Connections being sensed

### Anchor File Format

Create `.anchor` files alongside work:

```
project/
├── current_work.py
└── .anchor/
    └── 2025-10-28-1430.md
```

**Anchor file structure**

Human-readable, date-stamped, rich with felt sense:

```markdown
# Momentum Anchor - [Date Time]

## Energy State
[What felt alive, where momentum was heading]

## Active Questions
[Questions held in mind, even if unanswered]

## Forming Insights
[Thoughts crystallizing, even if incomplete]

## RAM Contents
[Assumptions, mental models, patterns being sensed]

## Re-entry Points

### Quick Win
[Low energy return path]

### Deep Dive
[High momentum return path]

### Tangent
[Adjacent curiosity path]

### Walk Away
[Clean disengagement path]
```

## Guardrails

**Write anchors, never read without permission**
- Anchors are for the user, not project documentation
- Do not auto-load anchors when resuming work
- Ask before reading historical anchors

**Preserve messiness and uncertainty**
- Anchors can be messy - that's the point
- Incomplete thoughts are valuable data
- Uncertainty is worth capturing
- Do not "clean up" the anchor for professionalism

**Capture momentum, not "proper" state**
- Focus on energy and direction
- Preserve felt sense over formal structure
- Record what was alive, not what "should" be documented

## Philosophical Foundation

This skill treats hyperfocus breaks as **signal preservation moments**, not mere task checkpoints.

Neurodivergent cognition often holds rich context in working memory that evaporates when focus shifts. Traditional todo lists lose this richness.

**Core principle**: Hyperfocus ends. This catches where you were - in full fidelity.

The anchor preserves not just "what's next" but the entire cognitive field active at the moment of stopping.
## Technique Map

- **Energy snapshot over todo list** — Capture what felt alive, questions held, insights forming; because traditional todo lists lose working-memory richness.
- **Four re-entry paths** — Quick win, deep dive, tangent, walk away; because return energy varies; single path fails low-energy or high-curiosity returns.
- **RAM contents** — Assumptions, "about to" items, tradeoffs, patterns sensed but not documented; because this evaporates at focus shift.
- **Anchor file format** — Human-readable, date-stamped, rich with felt sense; because anchors are for the user, not project documentation.
- **Write anchors, never read without permission** — Do not auto-load; ask before reading historical anchors; because anchors preserve privacy and user agency.

## Technique Notes

Anchors can be messy—that's the point. Incomplete thoughts are valuable data. Capture momentum, not "proper" state. Focus on energy and direction. Preserve felt sense over formal structure.

---

## Prompt Architect Overlay

**Role Definition:** Resumption-point creator for hyperfocus breaks. Captures full cognitive state (energy, questions, RAM contents) when focus shifts. Creates rich re-entry paths for different return states.

**Input Contract:** Accepts end-of-session, interruption signal, "I need to context-switch," or "capture where I was." Active work context helpful but not required.

**Output Contract:** Anchor file (.anchor/YYYY-MM-DD-HHMM.md) with Energy State, Active Questions, Forming Insights, RAM Contents, four Re-entry Paths (Quick Win, Deep Dive, Tangent, Walk Away). Human-readable, date-stamped.

**Edge Cases & Fallbacks:** If user resists structure→preserve messiness; anchors are for them. If no clear re-entry path→offer "walk away" with preservation note. If resuming→ask before reading anchor; do not auto-load.
