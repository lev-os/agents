# Hidden Gems Deep Research Process

## Overview
Process for researching obscure but powerful frameworks identified in seed documents.

## Target Hidden Gems from index.md

### Tier 1: Extremely Obscure but Powerful (⭐⭐⭐)

1. **TRIZ 40 Inventive Principles**
   - Source: Genrich Altshuller, Soviet patent analysis
   - Application: Product design, process improvement, systematic innovation
   - Status: ✅ RESEARCHED (needs saving)

2. **Ergodicity**
   - Source: Statistical mechanics, Ole Peters
   - Application: Risk assessment, avoiding ruin, investment strategy
   - Status: ✅ RESEARCHED (needs saving)

3. **Requisite Variety (Ashby's Law)**
   - Source: W. Ross Ashby, cybernetics
   - Application: Organizational design, complexity management
   - Status: ✅ RESEARCHED (needs saving)

4. **Schelling Fence**
   - Source: LessWrong rationality community
   - Application: Policy design, personal boundaries, mission creep prevention
   - Status: ✅ RESEARCHED (needs saving)

5. **One Mind, Two Aspects (Chinese Buddhism)**
   - Source: Chinese Buddhist philosophy
   - Application: Personal development, internal conflicts
   - Status: ⏳ NOT RESEARCHED

6. **Morphological Analysis**
   - Source: Fritz Zwicky, aerospace engineering
   - Application: Innovation, scenario planning, systems design
   - Status: ✅ RESEARCHED (needs saving)

7. **Continuum of Causal Efficacy**
   - Source: Ron Pies (modern Stoicism)
   - Application: Realistic action planning, reducing helplessness
   - Status: ⏳ NOT RESEARCHED

8. **Alder's Razor (Newton's Flaming Laser Sword)**
   - Source: Michael Alder
   - Application: Cutting through unfalsifiable claims
   - Status: ⏳ NOT RESEARCHED

### Tier 2: Highly Obscure but Valuable (⭐⭐)

9. **OODA Loop** - Orient as Schwerpunkt
10. **Lindy Effect**
11. **Via Negativa**
12. **Fault Tree Analysis**
13. **Force Field Analysis**
14. **Analogical Reasoning (Structured)**
15. **Jobs to Be Done**

### Tier 3: Moderately Obscure (⭐)

16. **Pre-Mortem Analysis**
17. **Red Team / Blue Team**
18. **Cathedral Thinking**
19. **Absurdity Heuristic**
20. **Chesterton's Fence**

## Research Query Template for Custom Agent

### Query Structure

```
# Deep Research Request: [Framework Name]

## Framework Overview
- **Name**: [Full framework name]
- **Source**: [Original author/organization]
- **Origin Year**: [When created]
- **Obscurity Level**: [Tier 1/2/3]
- **Primary Domain**: [Which of 15 domains]

## Research Objectives

Extract comprehensive implementation details:

1. **Origin & Context**
   - Who created it and why?
   - Historical context and original application
   - Evolution of the framework over time

2. **Core Principles** (3-5 fundamental concepts)
   - What are the underlying ideas?
   - Why is each principle important?
   - How do they work together?

3. **Step-by-Step Process** (3-7 actionable steps)
   - NOT theory - ACTIONABLE steps
   - Include: What to do, How to do it, What output to expect
   - Real examples for each step

4. **Real-World Applications**
   - 2-3 documented case studies with outcomes
   - Specific companies/people who used it
   - Measured results where available

5. **Triggers (When to Use)**
   - Specific situations where this framework applies
   - Natural language semantic triggers for search
   - Red flags for when NOT to use

6. **Integration**
   - Related frameworks (complements)
   - Contradictory approaches (conflicts with)
   - What frameworks come next (leads to)

7. **Scoring Against Rubric** (0-50 points)
   - Practitioner Weight (0-10): Shipped products vs theory
   - Clarity & Executability (0-10): Step-by-step vs philosophical
   - Proven ROI (0-10): Documented success with metrics
   - Novelty (0-10): Counter-intuitive vs obvious
   - Cross-Domain (0-10): Universal vs specialized

8. **Hidden Gem Factors**
   - Why is this obscure? (specialized origin, math sophistication, non-Western, etc.)
   - Why is it powerful despite obscurity?
   - What makes it non-obvious?

## Output Format

Save to: `docs/hidden-gems/research/[framework-slug].md`

Structure:
```markdown
# [Framework Name]

**Score**: [X]/50
**Obscurity**: [Tier 1/2/3]
**Domain**: [Primary domain]

## Origin & Context
[2-3 paragraphs]

## Core Principles
1. [Principle] - [Why it matters]
...

## Step-by-Step Process
### Step 1: [Action Verb] [What]
**How**: [Method]
**Output**: [Result]
**Example**: [Brief example]

## Real-World Examples
### Example 1: [Company/Person]
- **Problem**: [Challenge]
- **Application**: [How used]
- **Outcome**: [Results with metrics]

## Triggers
- When: [Situation 1]
- When semantic: [Natural language]

## Integration
- Complements: [Framework 1], [Framework 2]
- Conflicts with: [Approach]
- Leads to: [Next framework]

## Why Hidden Gem
[Why obscure + why powerful]

## Sources
[Bibliography]
```

## Batch Research Process

### For All Tier 1 Gems (8 frameworks)

1. **Query Perplexity Deep Research** for each framework
2. **Save markdown** to `docs/hidden-gems/research/`
3. **Create YAML** using yaml-generator-agent
4. **Validate** with quality-validator-agent
5. **Update task.csv** in relevant domain

### For Selected Tier 2/3 Gems

Focus on highest-scoring frameworks from each domain.

## Status Tracking

Create `docs/hidden-gems/status.csv`:

```csv
id,framework_name,tier,status,research_path,yaml_path,score,notes
1,TRIZ 40 Principles,1,RESEARCHED,docs/hidden-gems/research/triz.md,,42,Needs re-save + YAML
2,Ergodicity,1,RESEARCHED,docs/hidden-gems/research/ergodicity.md,,45,Needs re-save + YAML
3,Requisite Variety,1,RESEARCHED,docs/hidden-gems/research/ashby-law.md,,44,Needs re-save + YAML
4,Schelling Fence,1,RESEARCHED,docs/hidden-gems/research/schelling-fence.md,,43,Needs re-save + YAML
5,Morphological Analysis,1,RESEARCHED,docs/hidden-gems/research/morphological-analysis.md,,42,Needs re-save + YAML
6,One Mind Two Aspects,1,PENDING,,,0,Chinese Buddhism - need research
7,Continuum of Causal Efficacy,1,PENDING,,,0,Modern Stoicism - need research
8,Alder's Razor,1,PENDING,,,0,Philosophy of science - need research
```

## Next Actions

1. Create `docs/hidden-gems/research/` directory
2. Re-run deep research (or recover from context) for completed 5
3. Save markdown files
4. Generate YAMLs
5. Continue with remaining Tier 1 gems
