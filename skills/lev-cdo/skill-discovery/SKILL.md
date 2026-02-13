---
name: lev-cdo-skill-discovery
description: |
  [WHAT] Semantic search and discovery of skills for CDO workflow nodes
  [HOW] Uses lev-catalog CLI to browse, search, and load skills from axioms/hidden-gems
  [WHEN] Before building Deep/Epic workflows - discover skills to attach to graph nodes
  [WHY] Don't reinvent patterns - reuse existing decision frameworks and mental models

  Triggers: Called before Deep/Epic workflow construction
skill_type: tool
category: process-get

lifecycle_integration:
  stage: crystallizing
  input_artifact: workflow definition + complexity classification
  output_artifact: skill attachments for workflow nodes

related_skills:
  - skill://lev-cdo/workflows     # Provides skills to workflow nodes
  - skill://lev-find              # Legacy skill name (`lev get` backend, codebase-focused)

plankton: false
---

# CDO Skill Discovery - lev-catalog Integration

## Lev Concept

**What is this?**
A discovery-first workflow that uses semantic search to find existing decision frameworks, mental models, and analysis patterns before building CDO workflows.

**Why does it exist?**
CDO workflows can reference 40+ existing skills (axioms, hidden-gems). Without discovery, you'll:
- Reinvent existing patterns
- Miss powerful frameworks (ergodicity, cynefin, TRIZ-40)
- Build workflows from scratch instead of composing

**When to use it:**
- Before building Deep workflows (3-5 agents)
- Before building Epic workflows (5+ agents)
- When complexity classification triggers skill attachment

---

## CLI Commands

### lev-catalog Commands

```bash
# Browse skills by tag
lev-catalog index --tag=dev           # Software engineering patterns
lev-catalog index --tag=cognitive     # Mental models, biases
lev-catalog index --tag=strategy      # Business strategy frameworks

# Semantic search for skills matching your task
lev-catalog find "belief analysis"
lev-catalog find "risk under uncertainty"

# Load a specific skill for agent dispatch
lev-catalog load dig-axioms
lev-catalog load ergodicity

# Full catalog as JSON (for programmatic use)
lev-catalog catalog --source=axioms
lev-catalog catalog --source=hidden-gems
```

**CLI Location:** `node ~/lev/workshop/poc/lookup/cli.js`

**Alias setup:**
```bash
alias lev-catalog='node ~/lev/workshop/poc/lookup/cli.js'
```

---

## Workflows

### Workflow 1: Discovery-First CDO Construction

**Use case:** Building a Deep or Epic workflow from scratch

**Steps:**
1. **Classify complexity** → Quick / Base / Deep / Epic
2. **Browse by tag** → `lev-catalog index --tag=<tag>`
3. **Search for skills** → `lev-catalog find "<task keywords>"`
4. **Load skill content** → `lev-catalog load <skill-id>`
5. **Attach to graph nodes** → 1-n skills per node based on context
6. **Build workflow YAML** → Reference discovered skills

**Input:** Complexity classification + user query
**Output:** Workflow YAML with skill references

**Example:**
```bash
# Step 1: Classify
# User query: "Explore foundational assumptions behind belief X"
# Classification: complexity=deep, intent=research

# Step 2: Browse by tag
lev-catalog index --tag=cognitive
# → Shows: dig-axioms, steelman, paraphrase-engineer, etc.

# Step 3: Semantic search
lev-catalog find "socratic questioning belief"
# → Results:
#   - dig-axioms (score: 0.92)
#   - reflection-loop (score: 0.87)
#   - paraphrase-engineer (score: 0.81)

# Step 4: Load skill details
lev-catalog load dig-axioms
# → Returns full SKILL.md content

# Step 5: Attach to workflow nodes
# Turn 3: Use dig-axioms (multi-turn drilling)
# Turn 7: Use reflection-loop (final synthesis)

# Step 6: Build workflow YAML
# → See Level 3: Deep example in workflows/SKILL.md
```

---

### Workflow 2: Tag-Based Exploration

**Use case:** Discovering skills by category

**Tag categories:**

| Tag | Content | Example Skills |
|-----|---------|----------------|
| `dev` | Software engineering, patterns, architecture | refactoring-patterns, SOLID-principles |
| `strategy` | Business strategy, competitive analysis | five-forces, blue-ocean, wardley-maps |
| `cognitive` | Mental models, biases, heuristics | ergodicity, cynefin, lindy-effect |
| `decision` | Decision-making frameworks | decision-trees, morphological, TRIZ-40 |
| `systems` | Systems thinking, complexity | causal-loops, feedback-systems, emergence |
| `design` | UI/UX, product design | jobs-to-be-done, design-thinking |

**Example:**
```bash
# Explore cognitive skills
lev-catalog index --tag=cognitive

# Output:
# - ergodicity (probability under path dependence)
# - cynefin (complexity framework)
# - lindy-effect (time-tested resilience)
# - survivorship-bias (selection effects)
# - etc.
```

---

## Skill Catalogs

### Axiom Skills (11 total)

**Location:** `~/lev/workshop/poc/skills/domains/axioms/skills/`

**Skills:**
- **paraphrase-engineer** - Restate belief in clearest form
- **steelman-enhance** - Strengthen argument before critique
- **dig-axioms** - Multi-turn socratic drilling (3 levels)
- **map-elements** - Extract components and relationships
- **multi-devils-debate** - FOR/AGAINST/SYNTHESIS (3-turn)
- **synthesize-apply** - Integrate findings into actionable insight
- **reflection-loop** - Meta-analysis of reasoning process
- **proactive-guessing** - Hypothesis generation
- **ans-quadrant-mapping** - Cynefin-style complexity mapping
- **correlation-grounding** - Separate correlation from causation

**Common patterns:**
- Belief analysis workflows
- Assumption exploration
- Socratic questioning

---

### Hidden Gems (35+ total)

**Location:** `~/lev/workshop/poc/skills/domains/hidden-gems/`

**Categories:**

**Cognitive Frameworks:**
- ergodicity - Probability under path dependence
- cynefin - Complexity classification (simple/complicated/complex/chaotic)
- lindy-effect - Time-tested resilience heuristic

**Strategy Frameworks:**
- five-forces - Industry structure analysis (Porter)
- blue-ocean - Value innovation strategy
- wardley-maps - Strategic landscape mapping

**Decision Frameworks:**
- morphological - Solution space exploration
- TRIZ-40 - Inventive problem-solving principles
- decision-trees - Structured decision analysis

**Systems Thinking:**
- causal-loops - Feedback system analysis
- emergence - Bottom-up complexity
- antifragility - Systems that gain from stress

**Full catalog:** See `~/lev/workshop/poc/skills/domains/hidden-gems/task.csv`

---

## Integration with Workflows

### Attaching Skills to Workflow Nodes

**Pattern:** Each workflow turn can reference 1-n skills

**Example: Axiom Exploration (Deep workflow)**

```yaml
workflow: axiom-exploration
turns:
  - turn: 1
    agents:
      - skill: paraphrase-engineer  # DISCOVERED skill
        input: "00-input.md"
        output: "01-paraphrase.md"

  - turn: 3
    agents:
      - skill: dig-axioms           # DISCOVERED skill (multi-turn)
        input: "02-steelman.md"
        sub_turns: 3
        output: "03-dig-axioms.md"

  - turn: 7
    agents:
      - skill: reflection-loop      # DISCOVERED skill
        input: "all"
        output: "FINAL-synthesis.md"
```

**Discovery flow:**
1. User query: "Explore assumptions behind X"
2. Classification: Deep complexity
3. Search: `lev-catalog find "assumptions beliefs"`
4. Results: paraphrase-engineer, dig-axioms, reflection-loop
5. Load: `lev-catalog load dig-axioms` → read full skill
6. Attach: Add to workflow YAML as shown above

---

## Search Strategies

### Strategy 1: Keyword Search

**Use when:** You know the domain (e.g., "decision making")

```bash
lev-catalog find "decision under uncertainty"
lev-catalog find "root cause analysis"
lev-catalog find "strategic planning"
```

---

### Strategy 2: Tag Browsing

**Use when:** Exploring a category

```bash
lev-catalog index --tag=cognitive
lev-catalog index --tag=strategy
```

---

### Strategy 3: Similar Problems

**Use when:** You have an example problem

```bash
# Example: "Should we adopt GraphQL?"
lev-catalog find "technology adoption risk"
# → ergodicity, lindy-effect, morphological

# Example: "Debug intermittent failure"
lev-catalog find "root cause complex systems"
# → causal-loops, emergence, cynefin
```

---

## Orchestration Patterns

### Pattern 1: Single-Domain Workflow

**Use case:** Problem fits one skill category

**Example:** Belief analysis (all axiom skills)

```yaml
workflow: belief-analysis
skill_sources: [axioms]
turns:
  - paraphrase-engineer
  - steelman-enhance
  - dig-axioms
  - reflection-loop
```

---

### Pattern 2: Multi-Domain Workflow

**Use case:** Problem spans categories (cognitive + strategy)

**Example:** Strategic technology bet

```yaml
workflow: tech-bet-analysis
skill_sources: [axioms, hidden-gems]
turns:
  - turn: research
    skills: [ergodicity, lindy-effect, cynefin]
  - turn: analysis
    skills: [dig-axioms, morphological, TRIZ-40]
  - turn: synthesis
    skills: [synthesize-apply, reflection-loop]
```

---

### Pattern 3: Domain Expansion

**Use case:** Start narrow, expand if stuck

```
Level 1: Axioms only (belief analysis)
  ↓ (if stuck)
Level 2: + Hidden Gems (cognitive frameworks)
  ↓ (if stuck)
Level 3: + Strategy frameworks (business context)
```

**Example:**
```bash
# Level 1: Try axioms
lev-catalog find "assumptions" --source=axioms

# Level 2: Expand to cognitive
lev-catalog find "assumptions" --source=hidden-gems --tag=cognitive

# Level 3: Full catalog
lev-catalog find "assumptions"
```

---

## Related Orchestration Patterns

**Referenced in:**
- `~/.claude/commands/bd-agent.md` - Confidence routing
- `~/.claude/commands/plan.md` - Turn execution

**Complements:**
- `skill://lev-find` - Search codebase/docs (legacy skill name for `lev get` backend; not skill catalog)
- `skill://lev-research` - External research (web search)

---

## Anti-Patterns to Avoid

| Don't | Do Instead |
|-------|------------|
| Build workflows from scratch | Search catalog first |
| Use only familiar skills | Explore tags for new frameworks |
| Attach random skills | Match skill to workflow turn purpose |
| Skip skill loading | Read full SKILL.md before attaching |
| Reinvent decision frameworks | Use TRIZ-40, morphological, etc. |

---

## Relates

### Depends On
- `lev-catalog` CLI - Semantic search engine

### Works With
- `skill://lev-cdo/workflows` - Provides skills to attach
- `skill://lev-cdo/router` - Discovery triggered by Deep/Epic classification

### Blocks/Enables
- Blocks: None (discovery is optional but recommended)
- Enables: Reuse of 40+ existing patterns

### Lifecycle Position
- **Before:** Workflow YAML construction
- **After:** Skill-enriched workflow ready for execution
- **Parallel:** Can run while building workflow structure

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
You are the prompt-architect-enhanced specialist for skill-discovery, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
