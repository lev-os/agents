---
name: proactive-guessing
description: This skill should be used when asking a user why they hold a belief and want to surface unconsidered alternatives. It helps agents generate categorized hypotheses (emotional, tribal, rational, philosophical, unconceived) that reduce cognitive load and reveal blind spots by offering a recognition menu rather than forcing open-ended generation.
---

# proactive-guessing

**Supporting skill - used within dig-axioms**

**Purpose:** Generate 5-8 categorized hypotheses for why someone holds a belief, reducing cognitive load and revealing unconsidered alternatives.

**When to use:**
- During Socratic questioning (dig-axioms)
- When asking "why do you believe X?"
- User might not have articulated reasons
- Want to surface emotional/tribal drivers

---

## Core Principle

**Anti-pattern:** Ask open-ended "why?" and wait for user to generate answer.
- High cognitive load
- Easy to miss unconsidered alternatives
- Tends toward post-hoc rationalization

**Pattern:** Offer categorized menu of plausible reasons.
- Low cognitive load (recognition vs generation)
- Surfaces alternatives user hadn't considered
- Organized by type (emotional, tribal, rational, philosophical)

---

## Execution Steps

### Step 1: Frame the Belief
Identify the specific belief/axiom being questioned.

### Step 2: Generate 5-8 Hypotheses

**Required categories to cover:**
1. **Emotional** (1-2 options) - Hope, fear, pride, anxiety, excitement
2. **Tribal** (1-2 options) - Identity, in-group alignment, signaling
3. **Rational** (2-3 options) - Personal experience, analogical reasoning, logical inference
4. **Philosophical** (1-2 options) - Epistemological or ontological assumptions
5. **Unconceived** (1 option) - Alternative that undermines the premise
6. **Other** (1 option) - Blank for user's own answer

**Format for each hypothesis:**
```markdown
### [Number]. ([Category]) **[Short Name]**
[2-4 sentence explanation covering:]
- What this reason is
- How it would support the belief
- What it assumes about reality/cognition
- Why someone might hold this
```

### Step 3: Make Hypotheses Specific
Each hypothesis should:
- Reference the actual belief content
- Use concrete examples where possible
- Avoid vague abstractions
- Be genuinely plausible (not strawmen)

### Step 4: Ensure Coverage
Check that hypotheses cover:
- Positive emotions (hope, pride) and negative (fear, anxiety)
- Different tribal identities (multiple in-groups)
- Both personal experience and abstract reasoning
- Mainstream and alternative philosophical positions
- At least one "what if you're wrong?" unconceived alternative

### Step 5: Present with Numbering
Number 1-8, clearly mark categories in parentheses.

### Step 6: Include Blank Option
Always end with:
```markdown
### 8. (Other/Insert Own)**_______________________________**
```

---

## Output Format

**Embedded within dig-axioms file:**

```markdown
## Proactive Guessing: [5-8] Possible Presumptions

### 1. (Emotional) **[Short Name]**
[Explanation]

### 2. (Tribal) **[Short Name]**
[Explanation]

### 3. (Rational) **[Short Name]**
[Explanation]

### 4. (Rational) **[Short Name]**
[Explanation]

### 5. (Philosophical) **[Short Name]**
[Explanation]

### 6. (Philosophical) **[Short Name]**
[Explanation]

### 7. (Unconceived) **[Short Name]**
[Explanation]

### 8. (Other/Insert Own)**_______________________________**
```

---

## Quality Checks

Before presenting:
- [ ] 5-8 options total
- [ ] Categories labeled: (Emotional), (Tribal), (Rational), (Philosophical), (Unconceived), (Other)
- [ ] Each hypothesis has 2-4 sentence explanation
- [ ] Hypotheses reference specific belief content
- [ ] At least one unconceived alternative
- [ ] Blank option for user's own answer
- [ ] No strawmen (all plausible)

---

## Example from Live Execution

**Belief being questioned:**
> "Structured framework catalogs enable AI to pattern-match and humans to learn through cognitive apprenticeship"

**Proactive guesses generated:**

1. **(Emotional) Hope for Leverage** - Want months of cataloging to have multiplicative impact
2. **(Tribal) AI-Optimist Identity** - Aligns with "AI will transform education" narrative
3. **(Rational) Personal Experience** - Observed this in own learning with Perplexity/Claude
4. **(Rational) Analogical Reasoning from Expertise Research** - Chess masters = pattern recognition
5. **(Philosophical) Knowledge Externalization Assumption** - Thinking can be decomposed into teachable components
6. **(Philosophical) Learning-by-Exposure Assumption** - Humans learn implicitly through immersion
7. **(Unconceived) What if thinking ISN'T pattern-matching?** - Thinking might be generative/embodied
8. **(Other/Insert Own)**

**User selected:** #4 (Analogical Reasoning from Expertise Research)

**Result:** Revealed core axiom was analogy to chess/medical diagnosis expertise, which became Level 1 axiom for further drilling.

---

## Anti-Patterns to Avoid

**❌ Too few options** (less than 5)
- Doesn't cover enough space
- User may feel constrained

**❌ Too many options** (more than 8)
- Cognitive overload
- Decision paralysis

**❌ All same category**
- Missing emotional/tribal drivers
- Incomplete picture

**❌ Vague abstractions**
- "You believe in progress"
- Not specific enough to belief

**❌ Strawmen**
- Obviously implausible reasons
- User won't select them
- Breaks trust

**❌ No unconceived alternative**
- Doesn't challenge premise
- Misses opportunity for insight

---

## Why This Works

**Cognitive load:**
- Recognition easier than generation
- Menu of options vs blank slate

**Blind spots:**
- Users don't spontaneously consider emotional/tribal drivers
- Unconceived alternatives surface what's missing

**Honesty:**
- Seeing emotional reasons explicitly helps acknowledge them
- Tribal alignment becomes visible rather than invisible

**Depth:**
- Each category probes different type of presumption
- Systematic coverage of reasoning space

**Flexibility:**
- "Other" allows user to provide own answer
- Not forced into options if none fit

---

## Relation to Other Skills

**Used primarily in:**
- dig-axioms (each turn uses proactive guessing)

**Could be used in:**
- Any Socratic questioning context
- Debugging reasoning processes
- Collaborative belief exploration
- Teaching critical thinking

**Complements:**
- ACH (Analysis of Competing Hypotheses) - systematic evaluation
- Second-Order Thinking - considering multiple perspectives
- Polyvagal Theory - emotional state awareness
