---
name: lev-cdo-workflows
description: |
  [WHAT] Four complexity levels of CDO workflows: Quick, Base, Deep, Epic
  [HOW] Graph-based agent dispatch with disk-based artifact passing (no groupthink)
  [WHEN] After classification determines complexity level
  [WHY] Different problems need different depth - prevents over/under-engineering

  Triggers: Called by lev-cdo router based on complexity classification
skill_type: playbook
category: process-thinking

lifecycle_integration:
  stage: crystallizing
  input_artifact: classification metadata + user query
  output_artifact: FINAL-synthesis.md (workflow output)

related_skills:
  - skill://lev-cdo/router           # Receives routing from classification
  - skill://lev-cdo/skill-discovery  # Skills attached to workflow nodes
  - skill://bd                       # Epic workflows create BD structure

plankton: false
---

# CDO Workflows - Complexity-Based Execution Patterns

## Lev Concept

**What is this?**
CDO workflows are graph-based execution patterns where agents read/write to disk in sequence. Each complexity level (Quick/Base/Deep/Epic) defines agent count, turn structure, and convergence criteria.

**Why does it exist?**
Graph structure + disk I/O prevents groupthink. Agents never see each other's work during execution - only the FINAL synthesis step reads all artifacts together.

**When to use it:**
- **Quick**: Simple questions, 1-2 agents, single perspective
- **Base**: Multi-perspective analysis, 2-3 agents, fan-out/merge
- **Deep**: Root cause analysis, 3-5 agents, multi-turn chains
- **Epic**: Strategic decisions, 5+ agents, BD-tracked multi-session

---

## Core Principle

**Graph-based layouts + Agentic execution = CDO**

NOT: streaming, parallel, adaptive "properties" (fever dream)
YES: YAML describes structure → Agents read/write disk → No groupthink

### The Pattern That Works

```
./tmp/<workflow>-<timestamp>/
├── 00-input.md           # Original prompt/belief
├── 01-step-one.md        # Agent A output (reads: 00)
├── 02-step-two.md        # Agent B output (reads: 01)
├── 03a-turn-1.md         # Multi-turn: Agent C turn 1
├── 03b-turn-2.md         # Multi-turn: Agent C turn 2
├── 03c-turn-3.md         # Multi-turn: Agent C turn 3
├── 03-step-three.md      # Agent C synthesis
└── FINAL-synthesis.md    # ONLY this reads ALL files
```

**Critical rules:**
1. Each agent reads from DISK (previous step file)
2. Each agent writes to DISK (its output file)
3. Agents NEVER see each other's work during execution
4. Orchestrator ONLY launches agents—never synthesizes itself
5. Only FINAL step reads all artifacts together

---

## CLI Commands

### Primary Commands

```bash
# Execute workflow by complexity (called by router)
lev cdo execute --complexity=quick --input="00-input.md"
lev cdo execute --complexity=base --input="00-input.md"
lev cdo execute --complexity=deep --input="00-input.md"
lev cdo execute --complexity=epic --bd-epic=clawd-xxx

# Resume interrupted workflow
lev cdo resume --workflow-dir=tmp/analysis-20260128-143022
```

### Execution Protocol

```bash
# 1. Create artifact directory
mkdir -p tmp/<workflow>-$(date +%Y%m%d-%H%M%S)

# 2. Write input file
echo "User's question or belief" > tmp/<workflow>-*/00-input.md

# 3. Launch agents per turn (use Task tool)
# Each agent reads previous step, writes its step

# 4. Final synthesis reads all
```

---

## Workflows

### Level 1: Quick (1-2 agents, 1 turn)

**Use case:** Simple question, single perspective, known answer pattern

**Complexity factors:** 0-2
- Single question
- Known answer pattern
- No dependencies

**Pattern:** Sequential execution, direct answer

**Example:**

Prompt: "Summarize this document"

```yaml
workflow: quick-summary
agents:
  - step: 01
    skill: summarize
    input: "00-input.md"
    output: "FINAL-summary.md"
```

**Execution:**
```
Agent: Read 00-input.md → Write FINAL-summary.md
Done.
```

**Convergence:** N/A (single agent, single output)

---

### Level 2: Base (2-3 agents, 2 turns)

**Use case:** Need 2+ perspectives, then synthesis

**Complexity factors:** 3-5
- Multiple perspectives needed
- 2-3 related domains
- Some prior art exists

**Pattern:** Fan-out/merge (parallel perspectives → synthesis)

**Example:**

Prompt: "Analyze pros and cons of X"

```yaml
workflow: pros-cons-analysis
turns:
  - turn: 1
    parallel: true
    agents:
      - step: 01a
        skill: argue-for
        input: "00-input.md"
        output: "01a-pros.md"
      - step: 01b
        skill: argue-against
        input: "00-input.md"
        output: "01b-cons.md"

  - turn: 2
    agents:
      - step: 02
        skill: synthesize
        input: ["01a-pros.md", "01b-cons.md"]
        output: "FINAL-analysis.md"
```

**Execution:**
```
Turn 1 (parallel):
  Agent A: Read 00-input.md → Write 01a-pros.md
  Agent B: Read 00-input.md → Write 01b-cons.md
  ⏱ Sync

Turn 2:
  Agent C: Read 01a + 01b → Write FINAL-analysis.md
Done.
```

**Convergence:** Synthesis agent reads all Turn 1 outputs, no iteration needed

---

### Level 3: Deep (3-5 agents, 3-5 turns)

**Use case:** Root cause analysis, debate, drilling into assumptions

**Complexity factors:** 6-9
- Root cause unknown
- Multiple hypotheses
- Cross-domain analysis
- 5+ agents needed

**Pattern:** Multi-turn chains with optional resonance loops

**Example: Axiom Exploration Pattern**

Prompt: "Explore foundational assumptions behind belief X"

```yaml
workflow: axiom-exploration
skill_ref: workshop/poc/skills/domains/axioms/
turns:
  - turn: 1
    agents:
      - step: 01
        skill: paraphrase-engineer
        input: "00-input.md"
        output: "01-paraphrase.md"

  - turn: 2
    agents:
      - step: 02
        skill: steelman-enhance
        input: "01-paraphrase.md"
        output: "02-steelman.md"

  - turn: 3  # MULTI-TURN AGENT
    agents:
      - step: 03
        skill: dig-axioms
        input: "02-steelman.md"
        sub_turns:
          - "03a-level1.md"
          - "03b-level2.md"
          - "03c-level3.md"
        output: "03-dig-axioms.md"

  - turn: 4
    agents:
      - step: 04
        skill: map-elements
        input: "03-dig-axioms.md"
        output: "04-map-elements.md"

  - turn: 5  # MULTI-TURN AGENT
    parallel: false
    agents:
      - step: 05
        skill: multi-devils-debate
        input: "04-map-elements.md"
        sub_turns:
          - "05a-devils-advocate.md"  # FOR
          - "05b-anti-devils.md"       # AGAINST
          - "05c-synthesis.md"         # INTEGRATE
        output: "05-multi-devils.md"

  - turn: 6
    agents:
      - step: 06
        skill: synthesize-apply
        input: "all"  # Reads 00-05
        output: "06-synthesize.md"

  - turn: 7
    agents:
      - step: final
        skill: reflection-loop
        input: "all"
        output: "FINAL-synthesis.md"
```

**Convergence criteria:**
- All 7 turns complete
- FINAL-synthesis.md exists
- Optional: Reflection-loop includes confidence score ≥0.80

---

### Level 4: Epic (5+ agents, 5-10 turns, BD-tracked)

**Use case:** Strategic analysis, multi-session work, unknown unknowns

**Complexity factors:** 10+
- Strategic decision
- Multi-session work
- Unknown unknowns
- BD epic required

**Pattern:** BD-tracked phases with dependencies

**Example: Strategic Bet Analysis**

Prompt: "Should we bet on technology X? Full strategic analysis."

```yaml
workflow: strategic-bet-analysis
bd_epic: true  # Track in BD with dependencies
phases:
  - phase: research
    turns: 2
    bd_milestone: "clawd-xxx.1"
    agents:
      - skill: "hidden-gems/ergodicity"
      - skill: "hidden-gems/lindy-effect"
      - skill: "hidden-gems/cynefin"
      - skill: "domains/systems-thinking/*"
      - skill: "axioms/paraphrase-engineer"

  - phase: analysis
    turns: 3
    bd_milestone: "clawd-xxx.2"
    depends_on: research
    agents:
      - skill: "axioms/dig-axioms"  # 3-turn
      - skill: "axioms/multi-devils-debate"  # 3-turn
      - skill: "hidden-gems/morphological"
      - skill: "hidden-gems/triz-40"

  - phase: synthesis
    turns: 3
    bd_milestone: "clawd-xxx.3"
    depends_on: analysis
    agents:
      - resonance_loop: true
      - convergence_threshold: 0.85

  - phase: output
    turns: 2
    bd_milestone: "clawd-xxx.4"
    depends_on: synthesis
    agents:
      - skill: "axioms/synthesize-apply"
      - skill: "axioms/reflection-loop"
```

**BD Structure:**
```
bd://clawd-xxx (Epic: Strategic Bet Analysis)
├── clawd-xxx.1 (Research phase) ✅
├── clawd-xxx.2 (Analysis phase) - blocked by clawd-xxx.1
├── clawd-xxx.3 (Synthesis phase) - blocked by clawd-xxx.2
└── clawd-xxx.4 (Output phase) - blocked by clawd-xxx.3
```

**Convergence criteria:**
- All 4 phases complete (BD milestones closed)
- Synthesis phase reaches convergence threshold (0.85)
- Output phase produces actionable recommendation

---

## Convergence Criteria (CRITICAL)

### When to Stop a Deep Workflow

**Problem:** Without clear exit criteria, Deep workflows can loop infinitely.

**Solution:** Define convergence criteria per workflow type.

---

### Criteria Type 1: Turn Count (Fixed Structure)

**Use for:** Workflows with defined structure (e.g., axiom exploration)

**Rule:** Stop when all defined turns complete

**Example:**
```yaml
workflow: axiom-exploration
turns: 7  # Fixed structure
convergence:
  type: turn_count
  required_turns: 7
  exit_condition: "All turns complete"
```

**Validation:** Check that output files exist for all 7 turns

---

### Criteria Type 2: Confidence Threshold (Iterative)

**Use for:** Root cause analysis, hypothesis testing

**Rule:** Stop when confidence ≥ threshold OR max iterations reached

**Example:**
```yaml
workflow: root-cause-analysis
convergence:
  type: confidence
  threshold: 0.85
  max_iterations: 5
  evaluator_skill: "evaluate-confidence"
```

**Execution:**
```
Turn 1: Generate hypotheses → confidence = 0.60
Turn 2: Test hypotheses → confidence = 0.75
Turn 3: Refine top hypothesis → confidence = 0.88 ✅ STOP
```

**Safety:** Always include `max_iterations` to prevent infinite loops

---

### Criteria Type 3: Perspective Coverage (Fan-out)

**Use for:** Multi-perspective analysis (Base workflows)

**Rule:** Stop when all requested perspectives have been collected + synthesis complete

**Example:**
```yaml
workflow: pros-cons-analysis
convergence:
  type: perspective_coverage
  required_perspectives: ["pros", "cons", "synthesis"]
```

**Validation:** Check that all perspective files exist (01a-pros.md, 01b-cons.md, 02-synthesis.md)

---

### Criteria Type 4: Resonance Loop Convergence (Epic)

**Use for:** Strategic decisions requiring consensus

**Rule:** Stop when consecutive iterations show <10% change in output OR max iterations

**Example:**
```yaml
workflow: strategic-decision
convergence:
  type: resonance
  max_iterations: 5
  convergence_threshold: 0.85
  delta_threshold: 0.10  # <10% change = converged

  loop:
    - skill: synthesize-current
    - skill: critique-synthesis
    - skill: integrate-critique
    - check: |
        delta < 0.10 AND confidence >= 0.85?
          yes: exit_loop
          no: continue (up to max_iterations)
```

**Anti-pattern:** Orchestrator synthesizing → Groupthink
**Pattern:** Separate critique + integrate agents → No groupthink

---

### Convergence Validation Checklist

Before declaring a Deep workflow complete, verify:

- [ ] **Exit criteria met** (turn count, confidence, perspective coverage, or resonance)
- [ ] **All artifact files exist** (no missing turn outputs)
- [ ] **FINAL-synthesis.md exists** (final step completed)
- [ ] **Max iterations not exceeded** (safety check)
- [ ] **Confidence score documented** (if applicable)

**If criteria NOT met:** Report blocker and either:
1. Add more turns (if under max_iterations)
2. Lower threshold (if unrealistic)
3. Escalate to human (if truly stuck)

---

## Resonance Loops (When Needed)

For convergence on complex questions:

```yaml
resonance:
  enabled: true
  max_iterations: 5
  convergence_threshold: 0.85
  check_skill: "evaluate-confidence"

  loop:
    - skill: synthesize-current
    - skill: critique-synthesis
    - skill: integrate-critique
    - check: confidence >= threshold?
      yes: exit_loop
      no: continue
```

**Anti-pattern:** Orchestrator synthesizing → Groupthink
**Pattern:** Separate critique + integrate agents → No groupthink

---

## Agent Dispatch Pattern

```
For each turn:
  If parallel:
    Launch all agents simultaneously (Task tool, multiple calls)
    Wait for all to complete
  Else:
    Launch sequentially

  Sync: Verify outputs exist before next turn
```

---

## BD Integration (Epic Workflows)

### Before Starting Epic Workflow

```bash
# Create BD epic
bd create --title="Workflow: <name>" --type=epic --priority=P1

# Example: Strategic bet analysis
bd create --title="Epic: Evaluate GraphQL migration" --type=epic
# Returns: clawd-xxx
```

### Per Phase

```bash
# Create phase task
bd create --title="Phase: Research" --type=task --parent=clawd-xxx
# Returns: clawd-xxx.1

# Add dependency to previous phase
bd dep add clawd-xxx.2 clawd-xxx.1  # Analysis depends on Research
```

### On Phase Complete

```bash
# Close phase milestone
bd close clawd-xxx.1

# Check if next phase unblocked
bd show clawd-xxx.2  # Should show: unblocked
```

### On Workflow Complete

```bash
# Close epic
bd close clawd-xxx

# Archive artifacts (optional)
mv tmp/strategic-bet-* ~/.lev/pm/reports/clawd-xxx-strategic-bet.md
```

---

## Anti-Patterns to Avoid

| Don't | Do Instead |
|-------|------------|
| Orchestrator reads all context and synthesizes | Dispatch separate synthesis agent |
| Agents share context during execution | Each agent only reads assigned input files |
| Single mega-agent doing everything | Break into focused single-responsibility agents |
| Pseudo-code functions that can't execute | Reference real skills that exist |
| Over-engineer CDO "properties" | Graph structure + file I/O + agent dispatch |
| No max_iterations on loops | Always set safety limit (5-10 iterations) |
| Vague convergence criteria | Define explicit exit conditions |

---

## Relates

### Depends On
- `skill://lev-cdo/router` - Provides classification and routing
- `skill://lev-cdo/skill-discovery` - Finds skills to attach to workflow nodes
- `skill://bd` - Tracks Epic workflows

### Works With
- `skill://planning` - CDO outputs feed into planning
- `skill://work` - Validates CDO outputs via lifecycle ALIGN gate

### Blocks/Enables
- Blocks: Execution if convergence criteria not met
- Enables: Multi-perspective analysis without groupthink

### Lifecycle Position
- **Before:** Classification + routing decision
- **After:** FINAL-synthesis.md → proposal.md or report.md
- **Parallel:** None (sequential execution per turn)

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
You are the prompt-architect-enhanced specialist for workflows, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
