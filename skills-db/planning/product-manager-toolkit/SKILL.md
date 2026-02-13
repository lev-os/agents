# Product Manager Toolkit

Essential tools and frameworks for modern product management, from discovery to delivery.

## Quick Start

### For Feature Prioritization

```bash
python scripts/rice_prioritizer.py sample  # Create sample CSV
python scripts/rice_prioritizer.py sample_features.csv --capacity 15
```

### For Interview Analysis

```bash
python scripts/customer_interview_analyzer.py interview_transcript.txt
```

### For PRD Creation

1. Choose template from `references/prd_templates.md`
2. Fill in sections based on discovery work
3. Review with stakeholders
4. Version control in your PM tool

## Core Workflows

### Feature Prioritization Process

1. **Gather Feature Requests** - Customer feedback, sales requests, technical debt, strategic initiatives
2. **Score with RICE**
   - **Reach**: Users affected per quarter
   - **Impact**: massive/high/medium/low/minimal
   - **Confidence**: high/medium/low
   - **Effort**: xl/l/m/s/xs (person-months)
3. **Analyze Portfolio** - Quick wins vs big bets, effort distribution, strategy validation
4. **Generate Roadmap** - Quarterly capacity planning, dependency mapping, stakeholder alignment

### Customer Discovery Process

1. **Conduct Interviews** - Semi-structured format, focus on problems not solutions
2. **Analyze Insights** - Pain points, feature requests, jobs to be done, sentiment
3. **Synthesize Findings** - Group similar pain points, identify patterns, map to opportunities
4. **Validate Solutions** - Create hypotheses, test with prototypes, measure actual vs expected

### PRD Development Process

Templates available:
- **Standard PRD**: Complex features (6-8 weeks)
- **One-Page PRD**: Simple features (2-4 weeks)
- **Feature Brief**: Exploration phase (1 week)
- **Agile Epic**: Sprint-based delivery

## Prioritization Frameworks

### RICE Framework

```
Score = (Reach x Impact x Confidence) / Effort

Reach: # of users/quarter
Impact: Massive=3x, High=2x, Medium=1x, Low=0.5x, Minimal=0.25x
Confidence: High=100%, Medium=80%, Low=50%
Effort: Person-months
```

### Value vs Effort Matrix

```
           Low Effort    High Effort
High       QUICK WINS    BIG BETS
Value      [Prioritize]  [Strategic]

Low        FILL-INS      TIME SINKS
Value      [Maybe]       [Avoid]
```

### MoSCoW Method

- **Must Have**: Critical for launch
- **Should Have**: Important but not critical
- **Could Have**: Nice to have
- **Won't Have**: Out of scope

## Discovery Frameworks

### Customer Interview Guide

1. Context Questions (5 min) - Role, workflow, tools
2. Problem Exploration (15 min) - Pain points, frequency, workarounds
3. Solution Validation (10 min) - Reaction to concepts, value, willingness to pay
4. Wrap-up (5 min) - Other thoughts, referrals, follow-up

### Hypothesis Template

```
We believe that [building this feature]
For [these users]
Will [achieve this outcome]
We'll know we're right when [metric]
```

## Metrics & Analytics

### Feature Success Metrics

- **Adoption**: % of users using feature
- **Frequency**: Usage per user per time period
- **Depth**: % of feature capability used
- **Retention**: Continued usage over time
- **Satisfaction**: NPS/CSAT for feature

### Funnel Analysis

```
Acquisition -> Activation -> Retention -> Revenue -> Referral
```

## Best Practices

### Writing Great PRDs
1. Start with the problem, not solution
2. Include clear success metrics upfront
3. Explicitly state what's out of scope
4. Use visuals (wireframes, flows)
5. Keep technical details in appendix

### Effective Prioritization
1. Mix quick wins with strategic bets
2. Consider opportunity cost
3. Account for dependencies
4. Buffer for unexpected work (20%)
5. Revisit quarterly

### Customer Discovery Tips
1. Ask "why" 5 times
2. Focus on past behavior, not future intentions
3. Avoid leading questions
4. Look for emotional reactions
5. Validate with data

## Common Pitfalls to Avoid

1. **Solution-First Thinking**: Jumping to features before understanding problems
2. **Analysis Paralysis**: Over-researching without shipping
3. **Feature Factory**: Shipping features without measuring impact
4. **Ignoring Technical Debt**: Not allocating time for platform health
5. **Stakeholder Surprise**: Not communicating early and often
6. **Metric Theater**: Optimizing vanity metrics over real value
