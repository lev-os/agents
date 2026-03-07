---
name: lev-cdo-router
description: |
  [WHAT] Classification engine and complexity-based routing for CDO workflows
  [HOW] Analyzes input intent, confidence, complexity → routes to Quick/Base/Deep/Epic
  [WHEN] First step of every CDO invocation - determines execution strategy
  [WHY] Right-sized workflows prevent over/under-engineering

  Triggers: Called automatically by lev-cdo main skill
skill_type: playbook
category: process-thinking

lifecycle_integration:
  stage: crystallizing
  input_artifact: raw query or problem statement
  output_artifact: classification metadata + routing decision

related_skills:
  - skill://lev-cdo/workflows  # Routes to appropriate workflow
  - skill://lev-find           # Legacy skill name (`lev get` backend used in prior art check)
  - skill://work               # Architecture/lifecycle compliance validation

plankton: false
---

# CDO Router - Classification & Routing

## Lev Concept

**What is this?**
The CDO router is the entry point for all graph-based thinking workflows. It analyzes input to determine intent, confidence level, and complexity, then routes to the appropriate execution pattern.

**Why does it exist?**
Without classification, every problem gets the same heavyweight treatment. The router ensures quick questions get quick answers, while complex problems get multi-agent graph exploration.

**When to use it:**
- Automatically called by `lev cdo` command
- Can be invoked standalone for classification-only: `lev cdo classify "{input}"`

---

## CLI Commands

### Primary Command

```bash
# Auto-classify and route (called by parent skill)
lev cdo classify "{input}"
```

### Output Format

```yaml
classify:
  intent: "{question|command|idea|status|research}"
  confidence: 0.0-1.0
  complexity: "{quick|base|deep|epic}"
  tags: [auto-detected, keywords]
  capture: "{bd|idea|scratchpad|none}"
  route_to: "{workflows/quick|workflows/base|workflows/deep|workflows/epic}"
```

---

## Workflows

### Workflow 1: Classification

**Use case:** Every CDO invocation starts here

**Steps:**
1. Parse input for intent signals
2. Assess confidence (how well-understood is the problem?)
3. Determine complexity (scope, interdependencies, unknowns)
4. Tag with keywords for context
5. Decide capture destination (BD epic, idea file, scratch, none)
6. Route to appropriate workflow sub-skill

**Input:** Raw user query or problem statement
**Output:** Classification metadata + routing decision

**Example:**
```bash
# Input: "Should we use GraphQL or REST?"
# Output:
classify:
  intent: question
  confidence: 0.85
  complexity: base
  tags: [api, architecture, design-decision]
  capture: idea
  route_to: workflows/base
```

---

### Workflow 2: DoR Validation

**Use case:** Before executing Deep or Epic workflows

**Steps:**
1. **Sanity Check** - Verify problem/solution alignment
2. **Prior Art Check** - Search for existing implementations
3. **Architecture Compliance** - Validate YAML-first, LLM-first principles
4. **Scope Validation** - User approval for high-effort work

**Input:** Classification metadata + user query
**Output:** PASS/FAIL + validation notes

**Example:**
```bash
# Complexity: deep
# Triggers: Sanity check + prior art + architecture compliance

DoR Validation:
  sanity_check: PASS
  prior_art: FOUND (3 existing patterns in ~/lev/ideas/)
  architecture_compliance: PASS
  scope_validation: PENDING (requires user approval for 500+ LOC)
  verdict: BLOCKED until scope approved
```

---

## Classification Logic

### Intent Detection

| Pattern | Intent |
|---------|--------|
| "how", "what", "why", "when" | question |
| "do X", "create Y", "implement Z" | command |
| "we should", "what if", "consider" | idea |
| "show status", "what's blocked" | status |
| "find out", "investigate", "explore" | research |

### Confidence Scoring

```yaml
confidence_rules:
  - known_solution_exists: +0.30
  - clear_requirements: +0.20
  - prior_art_found: +0.15
  - single_domain: +0.10
  - vague_requirements: -0.20
  - unknown_domain: -0.30
  - conflicting_constraints: -0.25
```

### Complexity Scoring

```yaml
complexity_factors:
  quick:  # 0-2 factors
    - Single question
    - Known answer pattern
    - No dependencies

  base:   # 3-5 factors
    - Multiple perspectives needed
    - 2-3 related domains
    - Some prior art exists

  deep:   # 6-9 factors
    - Root cause unknown
    - Multiple hypotheses
    - Cross-domain analysis
    - 5+ agents needed

  epic:   # 10+ factors
    - Strategic decision
    - Multi-session work
    - Unknown unknowns
    - BD epic required
```

---

## DoR Validation Gates

### Gate 1: Sanity Check (Deep/Epic only)

**Questions:**
- What's the ACTUAL problem being solved?
- What's the simplest solution?
- Is this a 10-line fix or 1000-line system?
- Does the request match the solution complexity?

**Validation:**
```yaml
checks:
  - estimated_loc > 500 AND request_length < 100: SCOPE_MISMATCH
  - user_says "simple|just|quick": EXPECTATION_MISMATCH
  - solution_simpler_than_problem: OVER_ENGINEERING
```

**Action on FAIL:** Use AskUserQuestion to clarify scope

---

### Gate 2: Prior Art Check (ALWAYS)

**Search locations:**
```bash
# Codebase search
lev get "{keywords}" --indexes codebase

# Documentation search
lev get "{keywords}" --indexes documentation

# BD beads search
bd list --title-contains "{keywords}"
bd list --desc-contains "{keywords}"

# PM artifacts search
find ~/.lev/pm/handoffs -name "*{keywords}*.md"
find ~/.lev/pm/designs -name "*{keywords}*.md"
```

**Required output:**
- Existing implementations found: [yes/no]
- Can we reuse/compose: [yes/no]
- Why we're NOT reusing: [reason if applicable]

**Action on FOUND:** Propose reuse/composition before new implementation

---

### Gate 3: Architecture Compliance (Deep/Epic design)

**YAML-first, LLM-first principles:**

**Questions:**
- Is behavior in YAML or hardcoded?
- Can users customize without code changes?
- Where's the LLM in this design?
- If using FlowMind: YAML compiler or runtime consumer?

**Anti-patterns to catch:**
```yaml
violations:
  - hardcoded_routing: "if factorCount <= 2 then quick else deep"
  - pattern_matching: "regex instead of LLM reasoning"
  - locked_behavior: "users can only tweak threshold numbers"
  - flowmind_misuse: "LLM analyzes → hardcoded if/else executes"
```

**Required:**
- Behavior defined in YAML (customizable)
- LLM reasoning drives decisions
- FlowMind compiles YAML → behavior (not just analysis)

**Action on FAIL:** Reject design, propose YAML-first refactor

---

### Gate 4: Scope Validation (Deep/Epic only)

**Triggers:**
- Estimated effort > 4 hours
- LOC > 500
- Multi-session work required
- BD epic recommended

**Action:**
1. Present effort estimate to user
2. Confirm BD epic creation
3. Require justification if NOT reusing existing solutions
4. Get explicit approval before proceeding

---

## Message Footer Protocol

Every CDO response ends with structured footer:

```yaml
---
🆔 **Session:** {session_id} | 📋 {status} | 🏷️ [{tags}]

**Synths Active:** [{running_ephemeral_workflows}]

**Queued:**
- [ ] {pending_bd_update}
- [ ] {pending_idea_capture}

**Confirmed:** [x] {just_committed}

🪄 **Next:**
1. {action_verb} {target} [skill://...]
2. {action_verb} {target} [skill://...]
3. All | 4. ⬅️ Back
---
```

**Variables:**
| Variable | Source | Example |
|----------|--------|---------|
| session_id | Hook/UUID | `69C2-1408` |
| status | Classification | `crystallizing` |
| tags | Auto-detect | `[cdo, planning]` |
| synths | Active loops | `[research-spike, design-poc]` |
| queued | Pending commits | BD/idea updates |
| next_steps | Context-generated | Skill invocations |

---

## Routing Decision Table

| Confidence | Complexity | Route To | Notes |
|------------|-----------|----------|-------|
| ≥0.90 | quick | workflows/quick | Direct execution, 1-2 agents |
| ≥0.80 | base | workflows/base | Fan-out/merge, 2-3 agents |
| ≥0.60 | deep | workflows/deep | Multi-turn chains, 3-5 agents |
| <0.60 | epic | workflows/epic | BD-tracked, 5+ agents, multi-session |

**Override:** User can force complexity level with `--complexity={level}` flag

---

## Relates

### Depends On
- `skill://lev-find` - Prior art search (legacy skill name for `lev get` backend)
- `skill://bd` - Epic tracking for complex work

### Works With
- `skill://lev-cdo/workflows` - Receives routing decisions
- `skill://work` - Architecture/lifecycle compliance validation (ALIGN gate)

### Blocks/Enables
- Blocks: Execution until DoR passes
- Enables: Right-sized workflow execution

### Lifecycle Position
- **Before:** Raw user input
- **After:** Workflow execution (quick/base/deep/epic)
- **Parallel:** None (sequential gate)

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
You are the prompt-architect-enhanced specialist for router, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
