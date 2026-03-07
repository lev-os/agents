---
name: thinking-parliament
description: |
  Multi-modal multi-agent deliberation for complex problems. Each parliament seat uses a DIFFERENT
  model (Claude, Gemini, Llama, DeepSeek) for genuine perspective diversity. Includes `lev get`
  pre-step for context injection. CDO 5-stage cycle, confidence-based routing, and anti-groupthink
  safeguards. Triggers on "parliament", "deliberate", "multi-perspective", or strategic decisions.
version: 2.0.0
skill_type: playbook
category: process-thinking
triggers:
  - parliament
  - deliberate
  - multi-perspective
  - thinking parliament
  - multi-model
  - diverse perspectives
---

# Thinking Parliament

## Overview

Orchestrates multi-agent deliberation for problems that exceed single-perspective capacity. Combines CDO cognitive design patterns with axiom-style multi-turn thinking and skill catalog discovery.

## Quick Decision Tree

```
Problem presented?
│
├─→ Confidence < 40%?
│   └─→ FULL PARLIAMENT - Multi-agent deliberation (see below)
│
├─→ Confidence 40-60%?
│   └─→ RESONANCE MODE - Skill discovery + power combos
│
├─→ Confidence 60-85%?
│   └─→ STANDARD - Single-agent with skill hints
│
└─→ Confidence > 85%?
    └─→ DIRECT EXECUTION - No deliberation needed
```

## Confidence Assessment

Before routing, assess problem confidence:

```
CONFIDENCE FACTORS:
├─ Domain familiarity (have I solved this before?)
├─ Information completeness (are requirements clear?)
├─ Risk level (what happens if wrong?)
├─ Reversibility (can we iterate?)
└─ Stakeholder alignment (shared understanding?)

Score: Sum factors 0-100%
```

## Full Parliament Mode (<40% confidence)

**When:** Strategic decisions, system architecture, multi-stakeholder impact.

### Phase 0: Context Gathering (lev-get pre-step)

Before dispatching agents, gather context with semantic search:

```bash
# Extract keywords from problem statement
KEYWORDS=$(echo "$PROBLEM" | grep -oE '\b[A-Za-z]{4,}\b' | sort -u | head -10 | tr '\n' ' ')

# Search across all relevant indexes
lev get "$KEYWORDS" --indexes codebase,documentation,memory,skills > "$SESSION_DIR/00-context.md"

# Include prior art and related decisions
lev get "decision $KEYWORDS" --indexes memory,sessions >> "$SESSION_DIR/00-context.md"
```

**Why pre-step:** Agents deliberate with shared context, not in a vacuum. Memory index surfaces past decisions. Skills index finds relevant frameworks.

**Fallback (if lev get slow/unavailable):**
```bash
# Timeout after 30 seconds, proceed with reduced context
timeout 30s lev get "$KEYWORDS" --indexes codebase,memory > "$SESSION_DIR/00-context.md" 2>/dev/null || {
  echo "# Context gathering timed out - proceeding with problem statement only" > "$SESSION_DIR/00-context.md"
  echo "Note: Parliament will deliberate with less context. Results may need manual validation." >> "$SESSION_DIR/00-context.md"
}
```

### Phase 1: Workspace Setup
```bash
SESSION_DIR="./tmp/parliament-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$SESSION_DIR"
echo "Parliament session: $SESSION_DIR"
```

### Phase 2: Multi-Modal Agent Dispatch

Deploy 5 agents with **distinct models** for genuine perspective diversity:

| Agent | Role | Perspective | Model | Rationale |
|-------|------|-------------|-------|-----------|
| A1 | Advocate | Strongest case FOR | `openrouter/openai/gpt-5.2-pro` | Frontier reasoning, "think hard" support |
| A2 | Critic | Strongest case AGAINST | `openrouter/google/gemini-3-flash-preview` | 1M context, different training data |
| A3 | Systems | Second-order effects | `openrouter/x-ai/grok-4-fast` | 2M context (!), fast inference |
| A4 | Pragmatist | Implementation reality | `claude-opus-4-5` | Deep reasoning for edge cases |
| A5 | Wild Card | Unconsidered alternatives | `openrouter/deepseek/deepseek-v3.2` | Value king, unconventional reasoning |

**Dispatch Pattern (parallel via AI SDK):**
```bash
# All agents dispatch simultaneously with shared context
CONTEXT=$(cat "$SESSION_DIR/00-context.md")

# Using lev exec with different providers
lev exec "Role: Advocate. $PROBLEM\n\nContext:\n$CONTEXT" --model=openai/gpt-5.2-pro --adapter=ai-sdk > "$SESSION_DIR/advocate.md" &
lev exec "Role: Critic. $PROBLEM\n\nContext:\n$CONTEXT" --model=google/gemini-3-flash-preview --adapter=ai-sdk > "$SESSION_DIR/critic.md" &
lev exec "Role: Systems. $PROBLEM\n\nContext:\n$CONTEXT" --model=x-ai/grok-4-fast --adapter=ai-sdk > "$SESSION_DIR/systems.md" &
lev exec "Role: Pragmatist. $PROBLEM\n\nContext:\n$CONTEXT" --model=claude-opus-4-5-20251101 --adapter=claude-agent-sdk > "$SESSION_DIR/pragmatist.md" &
lev exec "Role: Wild Card. $PROBLEM\n\nContext:\n$CONTEXT" --model=deepseek/deepseek-v3.2 --adapter=ai-sdk > "$SESSION_DIR/wildcard.md" &

wait # All 5 run in parallel
```

**Why multi-modal:** Synthetic diversity from one model creates correlated blind spots. Different training data = genuinely different failure modes. Claude catches what Gemini misses and vice versa.

### Phase 3: Devil's Advocate Trigger

**At >70% agreement → Trigger devil's advocate:**

```
IF all agents agree on direction:
  └─→ Spawn contrarian agent
  └─→ Must argue opposite with full conviction
  └─→ Document in $SESSION_DIR/devils-advocate.md
```

### Phase 4: Synthesis

Read all agent artifacts, produce:
- Common ground (where all agree)
- Genuine tensions (where experts differ)
- Decision framework (when to use which approach)
- Confidence calibration (typically lower than initial)

## Resonance Mode (40-60% confidence)

**When:** Problem is scoped but approach unclear.

### Skill Discovery
```bash
# Search 568-skill catalog
node ~/lev/workshop/poc/lookup/cli.js find "<problem keywords>"

# Browse by domain
node ~/lev/workshop/poc/lookup/cli.js list --tag=strategy
node ~/lev/workshop/poc/lookup/cli.js list --tag=systems
```

### Power Combo Discovery

Skills have `complementsWell` metadata. Chain them:

```yaml
# Example combo: Strategic Decision
decision-matrix + rice-scoring + reversibility-check

# Example combo: Systems Analysis
systems-thinking + first-principles + cognitive-parliament
```

**See:** `references/power-combos.md`

## CDO 5-Stage Cycle

All parliament work follows:

```
┌─────────────────────────────────────────────┐
│ 1. PLAN    │ Define problem, scope, success │
│ 2. THINK   │ Multi-agent exploration        │
│ 3. EXECUTE │ Synthesize findings            │
│ 4. REVIEW  │ Validate against criteria      │
│ 5. LEARN   │ Update patterns, calibrate     │
└─────────────────────────────────────────────┘
```

**See:** `references/cdo-patterns.md`

## Axiom Workflow (Anti-Groupthink)

Multi-turn thinking with disk-based artifacts:

```
./tmp/parliament-{timestamp}/
├── 00-input.md           # Original problem
├── 01-perspectives.md    # Initial agent views
├── 02-debate.md          # FOR vs AGAINST
├── 03-synthesis.md       # Integration
├── 04-decision.md        # Framework
└── FINAL.md              # Actionable output
```

**Why disk-based:** Forces deliberation, prevents premature consensus, creates audit trail.

**See:** `references/axiom-workflow.md`

## References

- **references/cdo-patterns.md** - CDO 5-stage cycle, merge strategies
- **references/power-combos.md** - Skill graph, complementsWell network
- **references/axiom-workflow.md** - Disk-based anti-groupthink
- **references/parliamentary-protocol.md** - Multi-agent deliberation rules
- **references/confidence-routing.md** - Routing thresholds and calibration

## Quick Start Examples

### Strategic Decision
```
User: "Should we migrate to microservices?"

1. Assess confidence → 35% (high impact, unclear path)
2. Route → Full Parliament
3. Dispatch: Advocate, Critic, Systems, Pragmatist, Wild Card
4. Synthesize: Boundary conditions, phased approach
5. Output: Decision framework with when-to-migrate criteria
```

### Skill Discovery
```
User: "Help me evaluate these 5 vendors"

1. Assess confidence → 55% (scoped, approach unclear)
2. Route → Resonance Mode
3. Search: "evaluation comparison decision"
4. Find: decision-matrix, weighted-scoring, negotiation-leverage
5. Chain: decision-matrix → weighted-scoring → final-recommendation
```

### Hidden Nugget Extraction
```
User: "What patterns am I missing in this design?"

1. Assess confidence → 45% (unknown unknowns)
2. Route → Resonance Mode + Parliament elements
3. Random skill sampling: lookup random --limit=10
4. Pattern matching against design
5. Surface unconsidered alternatives
```

Load references as needed based on problem complexity.

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
You are the prompt-architect-enhanced specialist for lev-orch-thinking-parliament, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
