---
name: product-manager-toolkit
description: Essential tools and frameworks for product management, from discovery to delivery.
---

# Product Manager Toolkit

Essential tools and frameworks for modern product management, from discovery to delivery.

## Quick Start

**For Feature Prioritization:**
Run `python scripts/rice_prioritizer.py sample` to create sample CSV, then `python scripts/rice_prioritizer.py sample_features.csv --capacity 15` to prioritize.

**For Interview Analysis:**
Run `python scripts/customer_interview_analyzer.py interview_transcript.txt` to extract insights.

**For PRD Creation:**
Choose template from `references/prd_templates.md`, fill sections based on discovery work, review with stakeholders, version control in PM tool.

## Core Workflows

### Feature Prioritization Process

1. **Gather Feature Requests** from customer feedback, sales requests, technical debt, strategic initiatives.
2. **Score with RICE**: Create CSV with name, reach, impact, confidence, effort. Run `python scripts/rice_prioritizer.py features.csv`. **Reach** = users affected per quarter. **Impact** = massive/high/medium/low/minimal. **Confidence** = high/medium/low. **Effort** = xl/l/m/s/xs (person-months).
3. **Analyze Portfolio**: Review quick wins vs big bets, check effort distribution, validate against strategy.
4. **Generate Roadmap**: Quarterly capacity planning, dependency mapping, stakeholder alignment.

### Customer Discovery Process

1. **Conduct Interviews**: Use semi-structured format, focus on problems not solutions, record with permission.
2. **Analyze Insights**: Run `python scripts/customer_interview_analyzer.py transcript.txt` to extract pain points with severity, feature requests with priority, jobs to be done, sentiment analysis, key themes and quotes.
3. **Synthesize Findings**: Group similar pain points, identify patterns across interviews, map to opportunity areas.
4. **Validate Solutions**: Create solution hypotheses, test with prototypes, measure actual vs expected behavior.

### PRD Development Process

1. **Choose Template**: Standard PRD (complex features, 6-8 weeks), One-Page PRD (simple features, 2-4 weeks), Feature Brief (exploration, 1 week), Agile Epic (sprint-based delivery).
2. **Structure Content**: Problem → Solution → Success Metrics. Always include out-of-scope. Clear acceptance criteria.
3. **Collaborate**: Engineering for feasibility, Design for experience, Sales for market validation, Support for operational impact.

## Key Scripts

**rice_prioritizer.py**: RICE score calculation, portfolio balance analysis (quick wins vs big bets), quarterly roadmap generation, team capacity planning, multiple output formats (text/json/csv). Usage: `python scripts/rice_prioritizer.py features.csv --capacity 20 --output json`

**customer_interview_analyzer.py**: Pain point extraction with severity, feature request identification, JTBD pattern recognition, sentiment analysis, theme extraction, competitor mentions, key quotes. Usage: `python scripts/customer_interview_analyzer.py interview.txt json`

## Prioritization Frameworks

**RICE Framework:**
Score = (Reach × Impact × Confidence) / Effort
Where Impact: Massive = 3x, High = 2x, Medium = 1x, Low = 0.5x, Minimal = 0.25x
Confidence: High = 100%, Medium = 80%, Low = 50%

**Value vs Effort Matrix:**
High Value + Low Effort = QUICK WINS (Prioritize)
High Value + High Effort = BIG BETS (Strategic)
Low Value + Low Effort = FILL-INS (Maybe)
Low Value + High Effort = TIME SINKS (Avoid)

**MoSCoW Method:**
Must Have (critical for launch), Should Have (important but not critical), Could Have (nice to have), Won't Have (out of scope).

## Discovery Frameworks

**Customer Interview Guide:**
Context Questions (5 min): Role, responsibilities, current workflow, tools used.
Problem Exploration (15 min): Pain points, frequency and impact, current workarounds.
Solution Validation (10 min): Reaction to concepts, value perception, willingness to pay.
Wrap-up (5 min): Other thoughts, referrals, follow-up permission.

**Hypothesis Template:**
We believe that [building this feature] for [these users] will [achieve this outcome]. We'll know we're right when [metric].

**North Star Metric Framework:**
Identify core value → Make it measurable → Ensure it's actionable → Check it's a leading indicator.

## Best Practices

**Writing Great PRDs:** Start with problem not solution, include clear success metrics upfront, explicitly state out-of-scope, use visuals (wireframes/flows), keep technical details in appendix, version control changes.

**Effective Prioritization:** Mix quick wins with strategic bets, consider opportunity cost, account for dependencies, buffer for unexpected work (20%), revisit quarterly, communicate decisions clearly.

**Customer Discovery:** Ask "why" 5 times, focus on past behavior not future intentions, avoid leading questions, interview in their environment, look for emotional reactions, validate with data.

## Common Pitfalls to Avoid

Solution-first thinking (jumping to features before understanding problems), analysis paralysis (over-researching without shipping), feature factory (shipping without measuring impact), ignoring technical debt, stakeholder surprise (not communicating early/often), metric theater (optimizing vanity metrics).