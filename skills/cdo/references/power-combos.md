# Power Combos Reference

Skills work better in combination. This reference documents the skill graph and high-value combinations.

## Skill Discovery Commands

```bash
# Search by keyword
node ~/lev/workshop/poc/lookup/cli.js find "decision making"

# Browse by tag
node ~/lev/workshop/poc/lookup/cli.js list --tag=strategy
node ~/lev/workshop/poc/lookup/cli.js list --tag=systems
node ~/lev/workshop/poc/lookup/cli.js list --tag=cognitive

# Random sampling (serendipity)
node ~/lev/workshop/poc/lookup/cli.js random --limit=10

# Full catalog
node ~/lev/workshop/poc/lookup/cli.js catalog --json
```

## ComplementsWell Network

Skills declare what they pair well with via `complementsWell` metadata:

```yaml
# Example: decision-matrix
id: decision-matrix
complementsWell: [rice-scoring, 10-10-10-framework, reversibility-check]

# Example: systems-thinking
id: systems-thinking
complementsWell: [first-principles-thinking, second-order-effects, feedback-loops]
```

## High-Value Combos

### Strategic Decision Making

```
decision-matrix
    │
    ├─→ rice-scoring (prioritization)
    │
    ├─→ reversibility-check (risk assessment)
    │
    └─→ 10-10-10-framework (time horizon)

Chain: Evaluate → Prioritize → Risk Check → Temporal View → Decide
```

### Systems Analysis

```
systems-thinking
    │
    ├─→ first-principles-thinking (decompose)
    │
    ├─→ second-order-effects (consequences)
    │
    └─→ feedback-loops (dynamics)

Chain: Map System → Decompose → Project Effects → Identify Loops → Intervene
```

### Problem Solving

```
root-cause-analysis
    │
    ├─→ 5-whys (drill down)
    │
    ├─→ ishikawa-diagram (categorize causes)
    │
    └─→ pareto-principle (focus)

Chain: Surface Issue → Drill Down → Categorize → Focus on 20% → Solve
```

### Multi-Perspective Analysis

```
cognitive-parliament
    │
    ├─→ steelmanning (strengthen positions)
    │
    ├─→ devils-advocate (challenge)
    │
    └─→ red-team-blue-team (adversarial)

Chain: Gather Views → Strengthen Each → Challenge All → Synthesize
```

### Product Strategy

```
jobs-to-be-done
    │
    ├─→ value-proposition-canvas (fit)
    │
    ├─→ blue-ocean-strategy (differentiation)
    │
    └─→ product-market-fit (validation)

Chain: Understand Job → Map Value → Find Blue Ocean → Validate Fit
```

## Combo Discovery Algorithm

When matching skills to a problem:

```
1. KEYWORD EXTRACTION
   Extract keywords from problem description

2. INITIAL MATCH
   Search catalog: node lookup find "<keywords>"
   Take top 3-5 results

3. EXPAND VIA COMPLEMENTSWELLS
   For each matched skill:
     Read complementsWell array
     Add those skills to candidate set

4. FILTER BY COMPLEXITY
   Match skill complexity to problem scope:
   - Quick: Simple, bounded problems
   - Base: Standard implementation
   - Deep: Strategic, high-uncertainty

5. BUILD CHAIN
   Order skills by natural flow:
   Research → Analysis → Decision → Validation
```

## Example Combo Construction

**Problem:** "Should we build this feature in-house or buy?"

```bash
# Step 1: Search
node ~/lev/workshop/poc/lookup/cli.js find "build vs buy decision"

# Results:
# 1. make-vs-buy-analysis (0.85)
# 2. total-cost-ownership (0.72)
# 3. core-competency (0.68)

# Step 2: Check complementsWell
# make-vs-buy-analysis.complementsWell:
#   - total-cost-ownership
#   - vendor-evaluation
#   - risk-assessment

# Step 3: Build chain
COMBO: Build vs Buy Decision
├─ core-competency (is this our focus?)
├─ make-vs-buy-analysis (structured comparison)
├─ total-cost-ownership (full cost view)
├─ vendor-evaluation (if buy, which?)
└─ risk-assessment (what could go wrong?)
```

## Skill Tags (for browsing)

| Tag | Description | Example Skills |
|-----|-------------|----------------|
| strategy | Business/product strategy | blue-ocean, porter-five-forces |
| systems | Systems thinking | feedback-loops, leverage-points |
| cognitive | Mental models | confirmation-bias, anchoring |
| decision | Decision frameworks | decision-matrix, weighted-scoring |
| design | UI/UX, product design | design-thinking, user-journey |
| dev | Software patterns | solid-principles, clean-architecture |

## Parliament + Skill Combos

Parliament agents can each use different skill combos:

```
Parliament Session: Architecture Decision
│
├─ Agent 1 (Advocate)
│  └─ Uses: systems-thinking + blue-ocean-strategy
│
├─ Agent 2 (Critic)
│  └─ Uses: risk-assessment + devils-advocate
│
├─ Agent 3 (Systems)
│  └─ Uses: feedback-loops + second-order-effects
│
├─ Agent 4 (Pragmatist)
│  └─ Uses: total-cost-ownership + resource-constraints
│
└─ Agent 5 (Wild Card)
    └─ Uses: random sampling + unconsidered-alternatives
```

## Skill Lookup Integration

When routing to parliament:

```python
# Pseudo-code for skill-augmented parliament

def parliament_with_skills(problem):
    # 1. Search relevant skills
    skills = lookup_find(problem.keywords)

    # 2. Expand via complementsWell
    expanded = expand_complements(skills)

    # 3. Assign to agents
    for agent in parliament.agents:
        agent.skills = select_for_perspective(expanded, agent.archetype)

    # 4. Run deliberation
    perspectives = [agent.deliberate() for agent in parliament.agents]

    # 5. Synthesize with skill-informed framework
    return synthesize(perspectives, skills)
```
