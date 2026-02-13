# Description Quality Guide
**Purpose**: Descriptions are semantic prompts that determine skill discoverability

## The Critical Role of Descriptions

**Descriptions are NOT summaries** - they are **trigger-based prompts** that help users (and AI) know WHEN to reach for this framework.

**Bad (summary)**: "A framework for strategic decision-making"
**Good (trigger)**: "Escape competitive bloodbaths by creating uncontested market space when margins eroding in red oceans"

## Format Template

```
{WHAT it does} when {TRIGGER condition}
```

OR

```
{ACTION verb} to {OUTCOME} when {SITUATION}
```

## Quality Checklist

- [ ] **Specific action/insight** (not "framework for X")
- [ ] **Trigger condition** (when/where to use)
- [ ] **Self-contained** (no context needed)
- [ ] **20-150 characters** (one breath, one thought)
- [ ] **Avoids generic terms** (strategy, framework, thinking, important)
- [ ] **Captures essence** (someone unfamiliar can grasp it)

## Examples by Domain

### Mental Models
- ✅ "Break down to fundamental truths when existing approaches too expensive or inefficient"
- ✅ "Identify failure modes instead of optimizing success when stakes are high and downside catastrophic"
- ❌ "A thinking framework for problem-solving"

### Strategy
- ✅ "Cycle OODA faster than opponents when competing in dynamic markets where speed beats resources"
- ✅ "Escape red ocean competition by creating uncontested market space where rules don't apply"
- ❌ "A strategic framework for competitive advantage"

### Product
- ✅ "Discover unmet needs through weekly customer interviews when building products people actually want"
- ✅ "Map opportunities to solutions visually when aligning teams on what to build next"
- ❌ "A product management methodology"

### Technical
- ✅ "Write tests first to drive design when building features that must work correctly"
- ✅ "Decouple read and write models when they have different scaling or consistency needs"
- ❌ "An architectural pattern for applications"

## Common Mistakes

### Too Vague
- ❌ "Helps with decisions"
- ❌ "Useful for strategy"
- ❌ "Important framework"

### No Trigger
- ❌ "Explains how systems work"
- ❌ "A model for understanding"
- ❌ "Framework for analysis"

### Too Generic
- ❌ "Systematic approach to problem-solving"
- ❌ "Method for strategic thinking"
- ❌ "Tool for decision-making"

### Too Academic
- ❌ "Theoretical framework for analyzing competitive dynamics"
- ❌ "Conceptual model of organizational behavior"
- ❌ "Paradigm for understanding complex systems"

## The Trigger Test

**Ask:** "When would someone search for this framework?"

**Good descriptions answer:**
- "I'm stuck in competitive bloodbath" → Blue Ocean Strategy
- "Need to know if idea will last" → Lindy Effect
- "Hiring bias keeps happening" → Base Rate Fallacy
- "System keeps reverting despite changes" → Attractors

**Bad descriptions miss the search:**
- "Strategic framework" could be 50 different things
- "Decision-making tool" doesn't narrow it down
- "Helps with X" doesn't capture when/why

## Quality Spectrum

**⭐⭐⭐⭐⭐ Excellent** (Use as template)
"Cycle through observe-orient-decide-act faster than opponents, operating inside their decision-making tempo when competing in dynamic markets"
- Specific action: cycle OODA
- Comparative: faster than opponents
- Trigger: dynamic competitive markets
- Outcome: decision tempo advantage

**⭐⭐⭐⭐ Good**
"Break down to fundamental truths when existing approaches are prohibitively expensive"
- Specific action: break down to truths
- Trigger: existing approaches expensive
- Outcome: novel solutions

**⭐⭐⭐ Acceptable**
"Identify root causes by asking why five times"
- Specific action: ask why 5x
- Missing: when/trigger condition
- Fix: Add "when encountering persistent problems"

**⭐⭐ Poor**
"Framework for root cause analysis"
- Generic: "framework for X"
- No action verb
- No trigger
- Rewrite completely

**⭐ Unacceptable**
"Important mental model"
- Meaningless
- No action, no trigger, no specificity
- Delete and start over

## Agent Workflow

When you encounter missing/poor description:

1. **Read** the entire SKILL.md file
2. **Identify:**
   - What specific action/insight does it provide?
   - What trigger conditions indicate it's needed?
   - What outcome does it produce?
3. **Write** using template:
   - "{ACTION} when {TRIGGER}" OR
   - "{WHAT it does} to {OUTCOME} when {CONDITION}"
4. **Validate:**
   - Would someone searching for this trigger find it?
   - Is it specific enough to differentiate from similar frameworks?
   - Can someone unfamiliar understand when to use it?

## Co-Dependent Validation

**CLI's job:**
- Detect structural issues (missing fields, format problems)
- Report what needs fixing
- Provide decision tree for each issue type

**Agent's job:**
- Read frameworks with intelligence
- Write quality trigger-based descriptions
- Make judgment calls on edge cases
- Ensure descriptions enable discoverability

**NOT automated extraction** - requires understanding and judgment.
