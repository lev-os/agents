# Work — Lightweight Lifecycle Router Reference

3-phase FSM that chains guard → layers → think → execute. Portable version of the full Lev work skill — no BD tracking, no lev CLI, no daemon dependencies.

---

## Core Principle

**Think before you act, validate after.** Every piece of work flows through PLANNING → EXECUTION → VALIDATION. The planning phase chains the other lev-portable sub-routes (guard, layers, think) to build context before execution.

---

## FSM Definition

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  ┌──────────┐    ┌───────────┐    ┌────────────┐                    │
│  │ PLANNING │───▶│ EXECUTION │───▶│ VALIDATION │──── DONE           │
│  └──────────┘    └───────────┘    └────────────┘                    │
│       │                                  │                           │
│       │                                  │ FAIL                      │
│       │                                  ▼                           │
│       │                          ┌──────────────┐                   │
│       │◀─────────────────────────│ LOOP BACK    │                   │
│       │   (with learned context) └──────────────┘                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### State Transitions

| From | To | Trigger |
|------|----|---------|
| PLANNING | EXECUTION | Guard passes + layers classified + think completed (or skipped) |
| EXECUTION | VALIDATION | Work artifacts created |
| VALIDATION | DONE | All guard criteria satisfied |
| VALIDATION | PLANNING | Validation fails → loop with learned context |

---

## PLANNING Phase

The planning phase chains three sub-routes from lev-portable:

### Step 1: Guard (Spec Check)

```
INPUT:  User's request / problem statement
PROCESS:
  1. Score against 6 categories (Objective, Scope, Constraints, Environment, Dependencies, Success Criteria)
  2. Calculate underspec score (0-100%)
  3. If score > 30%: ask structured questions for missing categories
  4. If score > 60%: block until critical gaps filled
  5. If score ≤ 30%: pass through

OUTPUT: Enriched context with explicit answers for each category
SKIP:   --no-guard flag, explicit file paths, multi-turn established context
```

### Step 2: Layers (Classification)

```
INPUT:  Guard-enriched context
PROCESS:
  1. Classify velocity (Site → Stuff)
  2. Classify depth (L0 → L3)
  3. Classify persistence (System vs CDO)
  4. Determine review requirements

OUTPUT: Classification tuple { layer, depth, persistence, review_level }
```

### Step 3: Think (Deliberation)

```
INPUT:  Guard-enriched context + layer classification
PROCESS:
  Route by confidence:
    ≥ 0.90 → Skip think entirely (direct execution)
    ≥ 0.80 → Light deliberation (Advocate + Critic only)
    ≥ 0.60 → Full deliberation (all 5 roles)
    < 0.60 → Full deliberation + extended guard + human review

  Apply layer-weighted role emphasis:
    Site/Structure  → Critic + Systems amplified
    Skin/Services   → Advocate + Pragmatist amplified
    Space Plan      → Equal weight
    Stuff           → Pragmatist + Wild Card amplified

OUTPUT: Synthesis (common ground + tensions + decision framework)
SKIP:   Confidence ≥ 0.90, trivial classification (Stuff + L3 + CDO)
```

---

## EXECUTION Phase

Based on the planning output, execute with appropriate rigor:

### Execution Tiers

| Classification | Tier | Pattern |
|---------------|------|---------|
| Stuff + L3 + CDO | **Direct** | Just do it. No artifact. |
| Space Plan + L2 | **Brief** | 5-bullet plan → execute → verify |
| Skin/Services + L1-L2 | **Standard** | Written plan → execute → review |
| Structure + L1 | **Deliberate** | Full proposal → approval → execute → review |
| Site + L0-L1 | **Formal** | Full proposal → approval → phased execution → multi-gate review |

### Artifact Creation

```
DIRECT tier:
  → No planning artifact
  → Just execute and report

BRIEF tier:
  → Inline plan (5-10 bullet points in chat)
  → Execute
  → Brief summary of changes

STANDARD tier:
  → ./tmp/lev-portable-{timestamp}/plan.md
  → Execute according to plan
  → ./tmp/lev-portable-{timestamp}/summary.md

DELIBERATE tier:
  → ./tmp/lev-portable-{timestamp}/proposal.md
  → Wait for user approval
  → Execute according to proposal
  → ./tmp/lev-portable-{timestamp}/summary.md

FORMAL tier:
  → ./tmp/lev-portable-{timestamp}/proposal.md
  → Wait for user approval
  → Execute in phases with gates between each
  → ./tmp/lev-portable-{timestamp}/review.md per phase
  → ./tmp/lev-portable-{timestamp}/summary.md
```

---

## VALIDATION Phase

Validate the executed work against the guard criteria established in planning:

### Validation Checks

```
For each guard category scored in PLANNING:

  ✓ Objective:     Does the result meet the stated objective?
  ✓ Scope:         Did we stay within declared boundaries?
  ✓ Constraints:   Were all constraints honored?
  ✓ Environment:   Does it work in the target environment?
  ✓ Dependencies:  Are dependencies satisfied? Nothing broken?
  ✓ Success:       Do success criteria pass?
```

### Validation Outcomes

```
ALL PASS → DONE
  → Emit completion summary
  → Clean up temp files (or preserve with --keep-artifacts)

ANY FAIL → LOOP BACK to PLANNING
  → Carry forward: what failed and why
  → Guard re-scores with learned context
  → Think re-deliberates with failure knowledge
  → Maximum 3 loops before escalating to user

PARTIAL → DONE with warnings
  → Emit summary with warning section
  → List what passed and what needs attention
```

---

## Confidence Routing

Confidence is a composite of guard score + layer classification + deliberation consensus:

### Confidence Calculation

```
base_confidence = 1.0 - (guard_underspec_score / 100)

layer_modifier:
  Site/Structure  → -0.1 (high stakes = lower confidence)
  Skin/Services   → +0.0 (neutral)
  Space Plan      → +0.05 (well-understood territory)
  Stuff           → +0.1 (low stakes = higher confidence)

think_modifier:
  Agreement > 80% → +0.1
  Agreement 50-80% → +0.0
  Agreement < 50%  → -0.1

final_confidence = base_confidence + layer_modifier + think_modifier
```

### Routing Table

| Confidence | Action | Think Mode | Execution Tier |
|-----------|--------|-----------|---------------|
| ≥ 0.90 | Direct execute | Skip | Direct/Brief |
| 0.80-0.89 | Light deliberation | Advocate + Critic | Brief/Standard |
| 0.60-0.79 | Full deliberation | All 5 roles | Standard/Deliberate |
| < 0.60 | Extended planning | All 5 + devil's advocate | Deliberate/Formal |

---

## Session Management

### Save State on Interrupt

When a session is interrupted (user closes, timeout, context switch):

```markdown
# Save to: ./tmp/lev-portable-{timestamp}/session.md

## Session State
- **Phase:** {PLANNING | EXECUTION | VALIDATION}
- **Step:** {guard | layers | think | executing | validating}
- **Timestamp:** {ISO 8601}
- **Topic:** {brief description}

## Guard State
- **Score:** {underspec_score}%
- **Categories:** {scored categories with values}
- **Questions asked:** {list}
- **Answers received:** {list}

## Layers Classification
- **Layer:** {Brand layer}
- **Depth:** {L0-L3}
- **Persistence:** {System | CDO}

## Think Output
- **Roles completed:** {list}
- **Synthesis:** {if available}
- **Confidence:** {current}

## Execution Progress
- **Files modified:** {list}
- **Files created:** {list}
- **Remaining work:** {list}
```

### Resume from Saved State

```
On start, check for saved sessions:
  1. Look for ./tmp/lev-portable-*/session.md
  2. If found, read latest session
  3. Present to user:
     "Found interrupted session: '{topic}' at {phase}/{step}
      Last active: {timestamp}
      Resume? [y/n]"
  4. If yes: restore state, continue from last step
  5. If no: archive old session, start fresh
```

---

## Chaining Logic

How the sub-routes compose within the work FSM:

```
work "add dark mode"
│
├─ PLANNING:
│  ├─ guard("add dark mode")
│  │  → Score: 55% (Objective: partial, Scope: missing, ...)
│  │  → Ask: "What's included? Just colors, or layout changes too?"
│  │  → User answers: "Colors + component variants, not layout"
│  │  → Re-score: 25% → PASS
│  │
│  ├─ layers("add dark mode with colors + component variants")
│  │  → Layer: Skin (UI framework level)
│  │  → Depth: L2 (implementation details)
│  │  → Persistence: System (goes into codebase)
│  │  → Review: Visual + code review
│  │
│  └─ think("dark mode: colors + component variants, Skin/L2/System")
│     → Advocate: "CSS variables make this clean + themeable"
│     → Critic: "What about images? SVGs? Third-party components?"
│     → Systems: "Affects every component, need systematic approach"
│     → Pragmatist: "Start with CSS variables, iterate on edge cases"
│     → Wild Card: "What about system preference detection (prefers-color-scheme)?"
│     → Synthesis: CSS variables + system detection + phased rollout
│
├─ EXECUTION:
│  → Tier: Standard (Skin + L2 + System)
│  → Plan: 8-bullet implementation plan
│  → Execute: Create theme tokens, update components, add toggle
│
└─ VALIDATION:
   → Objective: Dark mode works ✓
   → Scope: Colors + variants only ✓ (no layout changes)
   → Constraints: No new dependencies ✓
   → Success: Toggle works, system preference detected ✓
   → DONE
```

---

## Error Recovery

### Loop-Back Pattern

When validation fails, the FSM loops back with enriched context:

```
Loop 1: Standard re-planning
  → Guard re-scores with failure context
  → Layers classification unchanged (usually)
  → Think re-deliberates with "what failed" as input
  → Execute with corrected approach

Loop 2: Escalated re-planning
  → Full guard (all 6 categories re-evaluated)
  → Think with all 5 roles + devil's advocate
  → Execute with more conservative approach

Loop 3: Human escalation
  → Present: "After 3 attempts, validation still failing."
  → Show: what passed, what failed, what was tried
  → Ask: "How should we proceed?"
  → Options: retry, simplify scope, abandon, manual fix
```

### Maximum Loop Count

Default: 3 loops before human escalation.
Override: `--max-loops={n}` to change threshold.

---

## Integration Points

| Sub-Route | Input From | Output To |
|-----------|-----------|----------|
| guard | User input | layers, validation |
| layers | Guard-enriched context | think, execution tier |
| think | Guard + layers output | execution approach |
| find | User query (on demand) | Any phase (context enrichment) |

---

## Quick Reference Card

```
⚙️ WORK — 3 phases, structured execution

PLANNING:
  1. Guard  → Score spec (0-100%), ask if gaps
  2. Layers → Classify (velocity × depth × persistence)
  3. Think  → Deliberate (5 roles, skip if trivial)

EXECUTION:
  Direct | Brief | Standard | Deliberate | Formal
  (based on classification)

VALIDATION:
  Check against guard criteria
  Pass → Done | Fail → Loop back (max 3)

Confidence routing: 0.90+ skip think | 0.60-0.90 full | <0.60 extended
```
