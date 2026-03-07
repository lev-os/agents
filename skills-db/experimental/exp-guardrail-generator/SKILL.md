---
name: guardrail-generator
description: Create flexible boundaries for projects - not rules or requirements, but bumpers that guide without constraining. Use when starting projects, when feeling overwhelmed by possibilities, or when needing structure without suffocation.
skill_evolver:
  enabled: true
  version: 1.0.0
  log_path: ~/.config/lev/logs/skills.jsonl
  hooks:
    - on_invoke
    - on_fail
    - on_success
---

# Guardrail Generator

This skill provides specialized support for creating flexible boundaries that guide work without constraining it - edges that nudge rather than walls that contain.

## Purpose

To generate soft boundaries, decision filters, and momentum channels that provide structure for neurodivergent work patterns without imposing rigid constraints that kill energy and creativity.

## When to Use This Skill

Use this skill when:
- Starting a new project and needing edges (not plans)
- Feeling overwhelmed by infinite possibilities
- Needing structure without feeling suffocated
- Traditional planning feels constraining or deadening
- Work needs direction but not rigid paths

## How to Use This Skill

### Philosophy: Guardrails vs. Rules

**Guardrails are NOT**
- Milestones with dates
- Requirements to check off
- Linear step-by-step processes
- Success criteria to meet

**Guardrails ARE**
- "If you drift here, nudge back"
- "This zone is fertile"
- "That edge drops off"
- "Here's where energy flows"

### Three Types of Guardrails

#### 1. Soft Boundaries (Not Walls, Membranes)

**Characteristics**
- Parameters that flex but signal when crossed
- "This probably isn't the thing" indicators
- Energy conservation zones
- Permeable edges that alert rather than block

**Example guardrails**
- "When complexity exceeds this feel, pause and simplify"
- "If it starts requiring these dependencies, question direction"
- "When you're explaining/justifying this part, it might not be core"
- "If this stops feeling playful, something's wrong"

#### 2. Decision Filters (Not Rules, Questions)

Create questions that guide choices without prescribing answers:

**Core alignment filters**
- "Does this pull toward or away from the strange attractor?"
- "Am I adding complexity or revealing simplicity?"
- "Is this the signal or is this anxiety?"
- "Does this preserve or dilute the essential weirdness?"

**Energy direction filters**
- "Does this feel downstream or upstream?"
- "Am I forcing or flowing?"
- "Is this energizing or draining?"
- "Does this generate tangents (signal) or obligations (noise)?"

**Scope hygiene filters**
- "Is this core or elaboration?"
- "Does removing this kill it or just change it?"
- "Am I building the thing or building around the thing?"

#### 3. Momentum Channels (Not Paths, Attractors)

Identify zones and directions rather than specific routes:

**Flow zones**
- Areas where work naturally feels downstream
- Contexts that generate productive tangents
- Topics that maintain energy over sessions
- Directions that feel inevitable rather than forced

**Fertile ground indicators**
- Where curiosity is highest
- Where "just checking this" leads to hours of flow
- Where tangents tend to circle back valuably
- Where messiness feels productive

**Dilution warning zones**
- Where tangents scatter rather than enrich
- Where more detail creates less clarity
- Where "improving" drains energy
- Where professionalization kills the idea

## Guardrails This Skill Will NOT Create

**Do not create**
- Fixed deadlines (unless external accountability explicitly needed)
- Feature checklists that become prisons
- "Professional standards" that flatten work
- Requirements to explain/justify weird parts
- Metrics for measuring "productivity"
- Linear roadmaps with gates
- Comparison to "how it's usually done"

**Why**: These impose external validation over felt sense and constrain neurodivergent strengths.

## Output Format: Felt Sense Made Visible

**Not**: A project plan document

**Not**: Requirements specification

**Not**: Timeline with milestones

**Instead**: Guardrails expressed as felt sense:

```markdown
## Soft Boundaries
- When this starts feeling like work, pause
- If explaining it requires >3 dependencies, simplify
- When tangents outnumber progress for >2 sessions, refocus

## Decision Filters
Ask before adding features:
- Does this reveal or obscure the core?
- Does this feel inevitable or optional?
- Am I building or justifying?

Ask when stuck:
- Is this complexity or confusion?
- Am I solving or avoiding?
- What would the simplest version be?

## Momentum Channels
Fertile zones:
- [Areas where energy flows naturally]
- [Tangents that tend to circle back valuably]

Dilution zones:
- [Where more detail creates less clarity]
- [Where professional polish kills energy]

Firm edges (but notice if they want to move):
- [This specific scope boundary]
- [This particular constraint that's load-bearing]
```

## Guardrail Evolution

**Guardrails are living boundaries**
- They can move if they want to
- Notice when a firm edge feels wrong
- Trust when a soft boundary wants to harden
- Let channels emerge through experience

**Check-in questions**
- "Do these guardrails still serve?"
- "Which ones feel dead or constraining?"
- "Which new edges are emerging?"
- "What's changed about where energy flows?"

## Philosophical Foundation

This skill treats project boundaries as **energy guidance systems**, not control mechanisms.

Neurodivergent work patterns need edges - total freedom creates overwhelm. But rigid structures kill the very strengths (curiosity, tangential thinking, pattern recognition) that make neurodivergent builders effective.

**Core principle**: You need edges, not cages.

Guardrails create containers that guide energy without constraining it - membranes, not walls.

Validation is felt sense: Do these guardrails help energy flow, or do they create friction?
## Technique Map

- **Soft boundaries over walls** — Parameters that flex and signal when crossed; because neurodivergent work needs edges, not cages, and rigid constraints kill energy.
- **Decision filters as questions** — "Does this pull toward the strange attractor?" not "Do this"; because questions guide without prescribing and preserve agency.
- **Momentum channels over paths** — Identify flow zones and dilution zones; because predetermined routes constrain; attractors guide.
- **Energy direction filters** — "Am I forcing or flowing?" "Does this generate tangents or obligations?"; because downstream/upstream sensing trumps task logic.
- **Living guardrail evolution** — Check-in questions; boundaries can move if they want to; because guardrails that feel dead create friction.

## Technique Notes

Never create milestones, feature checklists, linear roadmaps, or "professional standards." Guardrails are membranes, not walls. Trust when soft boundaries want to harden. Notice when firm edges feel wrong.

---

## Prompt Architect Overlay

**Role Definition:** Guardrail generator for neurodivergent work patterns. Creates flexible boundaries (soft boundaries, decision filters, momentum channels) that guide without constraining. Energy guidance, not control.

**Input Contract:** Accepts new project start, overwhelm by possibilities, "need structure without suffocation," or traditional planning feeling deadening. No project plan required.

**Output Contract:** Markdown with Soft Boundaries, Decision Filters, Momentum Channels. Felt-sense language (e.g., "When this starts feeling like work, pause"). No timelines, milestones, or requirements. Includes evolution check-in questions.

**Edge Cases & Fallbacks:** If user requests fixed deadlines→note external accountability; keep other guardrails soft. If output feels like a plan→reframe as questions and zones. If guardrails feel constraining→suggest moving or removing; validate through felt sense.
