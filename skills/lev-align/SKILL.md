---
name: lev-align
description: |
  [WHAT] Standalone alignment auditor for north-star drift.
  [HOW] Scans codebase state, compares to canonical docs, classifies drift, proposes corrections.
  [WHEN] Use only for explicit deep-dive alignment audits.
  [WHY] Default alignment should run inside `work`; this remains for focused audit sessions.

  Triggers: "align lev", "check north star", "what's our direction", "audit alignment", "detect drift", "product pivot"
version: 3.0.0
skill_type: reference
category: process-alignment
status: legacy-standalone

lifecycle_integration:
  stage: crystallizing
  input_artifact: codebase state + north star docs
  output_artifact: alignment-report.md + proposed doc updates
---

# Lev Align

> Preferred path: run alignment via `work` (`align/check/scan` routes). Use this skill directly only when you want a dedicated alignment audit.

Strategic alignment. North star management + drift detection + pivot adoption.

## Core Loop

```
1. NORTH STAR EXISTS?
   ├─ NO  → Deep research codebase → Define north star → Save to docs/
   └─ YES → Continue

2. CURRENT STATE ALIGNED?
   ├─ YES → Report "aligned" → Done
   └─ NO  → Detect drift type → Continue

3. DRIFT TYPE?
   ├─ STALE DOCS     → Propose doc updates
   ├─ PRODUCT PIVOT  → Propose north star update OR adopt new direction
   └─ COVERAGE GAP   → Propose additions to north star docs
```

## North Star Discovery

If no canonical north star found, trigger deep research:

```
# Check for north star docs
Expected locations:
- README.md (vision section)
- pm/00-roadmap.md (north star vision)
- docs/vision.md or docs/north-star.md
- NORTH_STAR.md at root

If missing or stale (>30 days):
1. Deep research codebase:
   - Recent git commits (direction of work)
   - BD issues (what's prioritized)
   - ADRs (architectural decisions)
   - Session artifacts (what's being built)

2. Synthesize north star:
   - Vision statement (1 sentence)
   - Key priorities (3-5 items)
   - Success metrics
   - Current phase

3. Propose location + content
4. Save on approval
```

## Drift Types

| Type              | Signal                           | Action                            |
| ----------------- | -------------------------------- | --------------------------------- |
| **Stale Docs**    | Dates old, refs outdated         | Update docs to match reality      |
| **Product Pivot** | Work diverged from stated vision | Update north star OR realign work |
| **Coverage Gap**  | New artifacts not in north star  | Add to north star docs            |
| **Status Drift**  | BD closed but docs say open      | Update doc refs                   |
| **Path Drift**    | Refs point to moved files        | Fix refs                          |

## Pivot Detection

When work diverges from north star:

```
# Signs of pivot
- Recent ADRs contradict roadmap priorities
- BD work doesn't match stated "critical path"
- New concepts emerged not in vision docs
- Energy going to unlisted areas

# Response options
1. ADOPT PIVOT → Update north star to reflect new direction
2. REALIGN WORK → Flag divergent work, recommend refocus
3. SPLIT → Some work is pivot, some is drift - handle separately
```

## Process

### 1. Locate North Star

```
# Primary sources (check in order)
1. README.md - "Vision" or "North Star" section
2. docs/

# Extract
- Vision statement
- Key priorities
- Current phase
- Success metrics
- Last updated date
```

### 2. Gather Current State

```
# What's actually happening
- git log --since="14 days" (recent work)
- bd list --open (active issues)
- bd list --closed --since 14d (recent completions)
- docs/adr/*.md (recent decisions)
- skills/ (what capabilities exist)
- Recent session handoffs
```

### 3. Compare & Classify

```
For each north star priority:
  - Is there active work? (BD issues, commits)
  - Is it blocked? (dependencies, decisions)
  - Is it abandoned? (no activity, superseded)

For each recent artifact:
  - Does it advance north star?
  - Does it pivot from north star?
  - Is it coverage gap?
```

### 4. Generate Alignment Report

```markdown
## Alignment Report - {date}

### North Star Status

**Vision**: "{vision statement}"
**Source**: {file} (last updated: {date})
**Freshness**: {fresh|stale|missing}

### Priority Alignment

| Priority           | Status     | Evidence          |
| ------------------ | ---------- | ----------------- |
| LEANN integration  | ⏸️ Stalled | No commits in 30d |
| Dashboard shell    | 🔄 Active  | lev-h7rq open     |
| Prose architecture | ✅ Done    | ADR-060 merged    |

### Drift Detected

1. **Product Pivot**: ADR-060 introduces "Prose Architecture" not in roadmap
   - Recommend: Add to north star as new priority
2. **Stale Docs**: pm/00-roadmap.md dated 2025-12-04 (35 days)

   - Recommend: Update with recent completions

3. **Status Drift**: lev-2598 closed but referenced as open
   - Recommend: Update refs to "superseded by ADR-060"

### Proposed Actions

1. [ ] Update docs/epics
2. [ ] Add "Prose Architecture" to north star priorities
3. [ ] Mark lev-2598 as closed/superseded in docs
4. [ ] Update state-of-the-union with recent work

Execute? [Y/n]
```

### 5. Execute Updates

With human approval:

- Update doc dates
- Add new priorities to north star
- Fix status refs
- Create BD issues for large changes

### 6. Validate

Re-run audit. North star should be current, drift minimal.

## When North Star Missing

If no canonical north star found:

```
Agent: No canonical north star found.

Initiating deep research to define one...

[Analyzing 14 days of commits...]
[Scanning 194 open BD issues...]
[Reading recent ADRs...]
[Checking session handoffs...]

## Proposed North Star

**Vision**: "Autonomous agents that learn, reason, and self-improve
through persistent memory"

**Key Priorities**:
1. Poly-Bridge architecture (performance foundation)
2. LEANN integration (semantic search)
3. Memory activation (learning loop)
4. Dashboard shell (user interface)
5. Prose architecture (system prompt generation)

**Current Phase**: Infrastructure + Alignment

**Save to**: docs/NORTH_STAR.md

Create this north star doc? [Y/n]
```

## Quick Commands

```
"align lev"           → Full alignment audit
"check north star"    → Just verify north star exists and is fresh
"what's drifted"      → Show drift without proposing fixes
"adopt pivot"         → Update north star to match current work direction
"update roadmap"      → Sync pm/00-roadmap.md with current state
```

## Related

- `bd` - Source of truth for issue status
- `lev get` - Deep codebase research
- `lev-learn` - Triggers align on patterns

## Relates

### Master Router
- **Lev Master Router** (`lev/SKILL.md`) - Routes all lev-* skills
  Parent skill that dispatches to this skill based on keywords/context

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-align, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
