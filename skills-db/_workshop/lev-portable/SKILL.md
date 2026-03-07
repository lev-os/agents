---
name: lev-portable
description: |
  Portable architectural thinking toolkit. Spec guard, shearing layers classifier,
  multi-perspective deliberation, cross-IDE skill search, and lightweight lifecycle router.
  No framework dependencies — works on any AI IDE.

  Triggers: "guard", "layers", "think portable", "find portable", "work portable",
  "spec check", "classify", "perspectives", "lev-portable"
version: 1.0.0
triggers:
  - guard
  - layers
  - think portable
  - find portable
  - work portable
  - spec check
  - classify
  - perspectives
  - lev-portable
compatibility:
  - claude-code
  - cursor
  - windsurf
  - continue-dev
  - cline
  - roo-code
---

# lev-portable — Architectural Thinking Toolkit

**One skill, five capabilities.** Portable spec guard, shearing layers classifier, multi-perspective deliberation, cross-IDE skill search, and lightweight lifecycle router. Zero framework dependencies.

## Quick Decision Tree

```
Input received →
│
├─ Vague / underspecified?
│  └─→ GUARD — Detect gaps, ask structured questions
│
├─ Need to classify where this fits architecturally?
│  └─→ LAYERS — Brand shearing layers × L0-L3 depth
│
├─ Need multiple perspectives before deciding?
│  └─→ THINK — 5 CDO roles deliberate sequentially
│
├─ Need to find existing skills / prior art?
│  └─→ FIND — rg across IDE skill paths
│
└─ Ready to execute structured work?
   └─→ WORK — 3-phase FSM: Plan → Execute → Validate
```

## Sub-Route Overview

| Route | Purpose | Trigger Keywords | Ref |
|-------|---------|-----------------|-----|
| **guard** | Detect underspecified inputs | "guard", "spec check", "vague" | `references/guard.md` |
| **layers** | Classify by velocity/depth/persistence | "layers", "classify", "shearing" | `references/layers.md` |
| **think** | Multi-perspective deliberation | "think", "perspectives", "deliberate" | `references/think.md` |
| **find** | Cross-IDE skill search | "find portable", "search skills" | `references/find.md` |
| **work** | Lifecycle FSM router | "work portable", "execute" | `references/work.md` |

---

## guard — Spec Guard

Detects underspecified inputs using 6 categories from the Trail of Bits audit checklist merged with structured interview frameworks.

### 6 Detection Categories

| # | Category | Question Pattern | Weight |
|---|----------|-----------------|--------|
| 1 | **Objective** | What specific outcome is expected? | 20% |
| 2 | **Scope** | What's included/excluded? Boundaries? | 20% |
| 3 | **Constraints** | Time, tech, budget, compatibility limits? | 15% |
| 4 | **Environment** | Where does this run? What exists already? | 15% |
| 5 | **Dependencies** | What must exist first? What breaks? | 15% |
| 6 | **Success Criteria** | How do we know it's done and correct? | 15% |

### Underspec Score

```
For each category:
  MISSING (no info)     → +full weight
  PARTIAL (implied)     → +half weight
  PRESENT (explicit)    → +0

Score = sum of weights → 0-100%
```

### Auto-Trigger Rules

```
Score > 30%  → Trigger guard automatically
Score > 60%  → Block execution until resolved
Score ≤ 30%  → Pass through (sufficient spec)
```

### Fast-Path Questions

When triggered, ask **only missing categories** using this format:

```
🛡️ Guard detected gaps in: {list missing categories}

q{n}) {Category}: {Specific question}
   Context: {Why this matters for the task}
   Default: {Reasonable assumption if user skips}
```

### Skip Conditions

- Explicit file paths provided → skip (scope is clear)
- Multi-turn conversation with established context → skip
- User flag: `--no-guard` → skip
- Score ≤ 30% → skip

**Full reference:** `references/guard.md`

---

## layers — Shearing Layers Classifier

Classifies changes using Stewart Brand's "How Buildings Learn" framework crossed with the L0-L3 depth model. Answers: *where does this change live, how fast does it move, and how permanent is it?*

### 3-Question Classifier

```
Q1 — VELOCITY: How often does this change?
     Site (decades) | Structure (years) | Skin (seasons) |
     Services (months) | Space Plan (weeks) | Stuff (daily)

Q2 — DEPTH: What level of detail?
     L0 Overview | L1 Structure | L2 Details | L3 Runtime

Q3 — PERSISTENCE: System or ephemeral?
     System Graph (permanent, infrastructure) |
     CDO Graph (ephemeral, thinking artifact)
```

### Decision Matrix

| Change Type | Layer | Depth | Persistence | Example |
|------------|-------|-------|-------------|---------|
| Database schema | Site | L1 | System | Add users table |
| Auth system | Structure | L1-L2 | System | JWT → OAuth migration |
| API versioning | Structure | L1 | System | v1 → v2 endpoint |
| UI framework | Skin | L1-L2 | System | React → Svelte |
| Component styling | Skin | L2 | CDO→System | Button redesign |
| Monitoring setup | Services | L2 | System | Add Datadog |
| CI/CD pipeline | Services | L2 | System | GitHub Actions config |
| Feature flag | Space Plan | L2-L3 | CDO | A/B test toggle |
| Route configuration | Space Plan | L2 | System | Add /settings page |
| Error message text | Stuff | L2-L3 | CDO | "Login failed" wording |
| Log format | Stuff | L3 | CDO | JSON → structured |
| Env variable | Stuff | L3 | CDO | Set DEBUG=true |

### Architecture Implications

```
Site/Structure changes    → Need design review, migration plan
Skin changes              → Need visual review, backward compat
Services changes          → Need ops review, rollback plan
Space Plan changes        → Need user flow review, feature flags
Stuff changes             → Ship fast, iterate, minimal review
```

**Full reference:** `references/layers.md`

---

## think — Multi-Perspective Deliberation

5 CDO roles applied sequentially to any problem. Portable version of the Thinking Parliament — single model, multiple perspectives, no external dispatch.

### 5 Roles

| Role | Lens | Asks |
|------|------|------|
| **Advocate** | Strongest case FOR | "Why is this the right move? What strengths does it build on?" |
| **Critic** | Strongest case AGAINST | "What could go wrong? What are we not seeing?" |
| **Systems** | Second-order effects | "What else does this touch? What emerges from the interaction?" |
| **Pragmatist** | Implementation reality | "Can we actually build this? What constraints matter?" |
| **Wild Card** | Unconsidered alternatives | "What if we're asking the wrong question entirely?" |

### Application Pattern

```
For each role (sequential):
  1. State the role explicitly
  2. Apply role lens to the problem
  3. Produce 2-3 key insights
  4. Rate confidence (0-1) in those insights

After all 5 roles:
  → Synthesize: common ground + genuine tensions
  → If >70% agreement → trigger devil's advocate (re-run Critic harder)
  → Output: decision framework, not just recommendation
```

### Layer-Weighted Application

The layers classifier influences which roles get emphasis:

```
Site/Structure  → Emphasize: Systems, Critic (high stakes)
Skin/Services   → Emphasize: Pragmatist, Advocate (execution focus)
Space Plan      → Balanced across all roles
Stuff           → Emphasize: Pragmatist, Wild Card (speed + creativity)
```

**Full reference:** `references/think.md`

---

## find — Cross-IDE Skill Search

Searches for skills across all major AI IDE skill locations using `rg` (with `grep` fallback).

### IDE Skill Paths

```bash
SKILL_PATHS=(
  "$HOME/.claude/commands"          # Claude Code commands
  "$HOME/.claude/skills"            # Claude Code skills
  "$HOME/.agents/skills"            # Agent skills (canonical)
  "$HOME/.agents/skills-db"         # Skills database
  "$HOME/.cursor/rules"             # Cursor rules
  "$HOME/.cursor/skills"            # Cursor skills
  "$HOME/.windsurf/rules"           # Windsurf rules
  "$HOME/.continue"                 # Continue.dev
  "$HOME/.cline/rules"              # Cline rules
  "$HOME/.roo/rules"                # Roo Code rules
)
```

### Search Patterns

```bash
# By name
rg -l -i "{query}" --glob="SKILL.md" --glob="*.md" ${SKILL_PATHS[@]}

# By trigger
rg -i "triggers?.*{query}" --glob="*.md" --glob="*.yaml" ${SKILL_PATHS[@]}

# By description
rg -i "description.*{query}" --glob="SKILL.md" ${SKILL_PATHS[@]}
```

### Output Format

```
📂 {skill-name}
   Path: {full path}
   Description: {first line of description}
   Triggers: {trigger list}
---
Found {n} skills matching "{query}" across {m} IDE locations.
```

### Fallback

When `rg` unavailable:
```bash
find ${SKILL_PATHS[@]} -name "*.md" -exec grep -li "{query}" {} \; 2>/dev/null
```

**Full reference:** `references/find.md`

---

## work — Lightweight Lifecycle Router

3-phase FSM that chains guard → layers → think → execute. Portable version of the full work skill — no BD tracking, no lev CLI.

### FSM States

```
┌──────────┐    ┌───────────┐    ┌────────────┐
│ PLANNING │───▶│ EXECUTION │───▶│ VALIDATION │
└──────────┘    └───────────┘    └────────────┘
 guard            apply output     verify against
 layers           create artifacts guard criteria
 think            write files      check completeness
```

### PLANNING Phase

```
1. GUARD   — Score input (0-100% underspec)
             Skip if score ≤ 30% or --no-guard
             Ask questions for missing categories

2. LAYERS  — Classify the work
             Determine: velocity, depth, persistence
             Informs review requirements

3. THINK   — Deliberate (if complexity warrants)
             Apply 5 roles sequentially
             Skip if trivial (Site/Stuff + L3 + CDO)
             Output: decision framework
```

### EXECUTION Phase

```
Apply thinking output:
  - Simple (Stuff/L3)   → Direct execution, no artifact
  - Medium (Skin-Space)  → Create brief plan, then execute
  - Complex (Site-Struct) → Create full proposal, get approval, then execute
```

### VALIDATION Phase

```
Check against guard criteria:
  ✓ Objective met?
  ✓ Scope respected?
  ✓ Constraints honored?
  ✓ Success criteria satisfied?

If validation fails → loop back to PLANNING with learned context
If validation passes → emit completion summary
```

### Confidence Routing

```
Confidence ≥ 0.90 → Direct execution (skip think)
Confidence ≥ 0.80 → Light think (Advocate + Critic only)
Confidence ≥ 0.60 → Full think (all 5 roles)
Confidence < 0.60 → Full think + extended guard + human review
```

### Session Management

```
On interrupt: save state to ./tmp/lev-portable-{timestamp}.md
On resume: detect saved state, offer to continue
State includes: FSM phase, guard score, layer classification, think output
```

**Full reference:** `references/work.md`

---

## Integration Notes

### Cross-IDE Compatibility

This skill uses **zero framework dependencies**:
- No `lev` CLI required
- No `bd` (beads) required
- No custom daemons or services
- Search uses `rg` with `grep` fallback
- All state is markdown files in `./tmp/`

### Installation

```bash
# Via skills marketplace
npx skills add lev-os/lev-portable

# Manual: copy to any IDE skill location
cp -r lev-portable/ ~/.claude/commands/lev-portable/   # Claude Code
cp -r lev-portable/ ~/.cursor/skills/lev-portable/     # Cursor
cp -r lev-portable/ ~/.agents/skills/lev-portable/     # Universal
```

### Escape Hatches

| Situation | Escape |
|-----------|--------|
| Guard too aggressive | `--no-guard` or provide explicit file paths |
| Layers classification wrong | Override manually: "treat this as {layer}" |
| Think taking too long | "just Advocate + Critic" for fast deliberation |
| Find not finding skills | Provide path directly: "search in {path}" |
| Work FSM stuck | "skip to execution" to bypass planning |

### Composability

Each sub-route works standalone:
```
/guard "add auth"           → Just run spec guard
/layers "migrate database"  → Just classify the change
/think "add caching"        → Just run 5 perspectives
/find "interview"           → Just search for skills
/work "add dark mode"       → Full chain: guard → layers → think → execute
```

### Relationship to Full Lev

This is the **thinking model** extracted from Lev, without the runtime:

| lev-portable | Full Lev Equivalent |
|-------------|-------------------|
| guard | `lev-cdo` DoR gates + `interview` framework |
| layers | `docs/01-architecture.md` L0-L3 + Brand theory |
| think | `thinking-parliament` (single-model portable) |
| find | `lev-find` (rg-only, no vector index) |
| work | `work` skill (no BD, no team dispatch) |

---

**Status:** v1.0.0
**Source:** Shearing layers audit → 75% alignment, 3 coupling inversions
**License:** MIT
