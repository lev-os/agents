---
name: correlation-grounding
description: This skill should be used when abstract belief claims require empirical validation without claiming causation. It guides agents to ground claims in research correlations following Humean epistemology, moving from causal language to observed co-occurrence patterns, enabling intellectual honesty about the limits of evidence and confidence in supporting claims.
---

# correlation-grounding

**Supporting skill - used within steelman-enhance**

**Framework used:** Humean Skepticism / Empiricism

**Purpose:** Ground abstract belief claims in empirical research correlations while explicitly avoiding causal language, following Humean epistemology.

**When to use:**
- During steelman-enhance
- When claims need empirical support
- Converting intuitions to testable hypotheses
- Acknowledging limits of current knowledge

---

## Core Principle: Humean Skepticism

**David Hume's insight:**
- We observe correlations, not causation
- "A causes B" is inference, not observation
- Science reveals what consistently co-occurs
- Causality is metaphysical assumption

**Application to beliefs:**
- Replace "X causes Y" with "X correlates with Y"
- Cite research showing co-occurrence
- Acknowledge correlation ≠ causation
- Rate confidence in correlation

---

## Execution Steps

### Step 1: Identify Claims Needing Support

From enhanced belief statement, extract 3-5 core claims:
- Mechanisms proposed (how X leads to Y)
- Effects predicted (if we do X, Y will happen)
- Assumptions about learning/cognition/behavior

### Step 2: Find Empirical Correlations (5 total)

For each claim, search for research showing:
- **What correlates:** "X is associated with Y"
- **Not:** "X causes Y"

**Correlation types:**
- Observational studies (X and Y co-occur)
- Experimental studies (manipulating X correlates with Y change)
- Meta-analyses (multiple studies find same correlation)
- Theoretical frameworks (model predicts correlation)

### Step 3: Document Each Correlation

For each of 5 correlations:

**Citation:**
- Research area / Theory name
- (Author, Year) or (Authors, Year)

**Correlation statement:**
- What correlates with what
- Use language: "correlates with," "is associated with," "co-occurs with"
- Avoid: "causes," "produces," "creates," "makes"

**Relevance:**
- How this correlation supports the belief
- What mechanism it suggests (tentatively)

**Evidence quality:**
- **Strong:** Multiple replications, large effects, controlled studies
- **Moderate:** Some studies, mixed results, observational
- **Weak:** Single study, small sample, theoretical only

**Confidence:**
- Personal confidence in this correlation (40-95%)
- Why this confidence level?

### Step 4: Identify Weakest Link

Of the 5 correlations, mark which is:
- Lowest evidence quality
- Lowest confidence
- Most critical for belief
- "If this fails, belief weakens substantially"

### Step 5: Assess Coverage

Check that correlations cover:
- Core mechanism of belief
- Supporting evidence
- Alternative explanations
- Boundary conditions

**Target coverage:**
- At least 2 with "Strong" evidence quality
- At least 2 with 80%+ confidence
- At least 1 identified as "weakest link"

### Step 6: Rate Overall Grounding

How well-grounded is the belief given correlations?
- Strong support (80%+): Multiple strong correlations
- Moderate support (60-80%): Some correlations, gaps remain
- Weak support (40-60%): Few correlations, speculative

---

## Output Format

**Embedded within steelman-enhance file:**

```markdown
## Supporting Empirical Correlations

### 1. [Research Area / Theory Name] ([Authors, Year])
**Correlation:** [What correlates with what - explicit correlation language]
- **Relevance:** [How this supports belief]
- **Mechanism:** [What process it suggests] (tentative)
- **Evidence quality:** [Strong/Moderate/Weak] ([why])
- **Confidence:** [40-95]%

---

[Repeat for 5 correlations]

### [Weakest Link Note]
**Note:** This is the **weakest link**—[why this correlation is critical but uncertain]
```

---

## Language Patterns

**✅ CORRECT (Correlation language):**
- "X correlates with Y"
- "X is associated with Y"
- "Studies find X and Y co-occur"
- "Manipulating X corresponds to Y changes"
- "X predicts Y in regression models"
- "Research shows X-Y relationship"

**❌ INCORRECT (Causal language):**
- "X causes Y"
- "X produces Y"
- "X creates Y"
- "X makes Y happen"
- "X leads to Y" (unless qualifying: "appears to lead to")
- "X results in Y"

**⚠️ ACCEPTABLE (Qualified causal):**
- "X may cause Y (correlation observed)"
- "X appears to lead to Y (mechanism unclear)"
- "Causal mechanism proposed: X→Y (not confirmed)"

---

## Quality Checks

Before completing:
- [ ] 5 empirical correlations documented
- [ ] All use correlation language (not causal)
- [ ] Citations include (Author, Year)
- [ ] Relevance to belief explained
- [ ] Evidence quality assessed (Strong/Moderate/Weak)
- [ ] Confidence rated (40-95%)
- [ ] Weakest link identified
- [ ] Coverage adequate (2 strong, 2 high-confidence)

---

## Example from Live Execution

**Belief being grounded:**
> "Framework cataloging enables AI to pattern-match and humans to learn through cognitive apprenticeship"

**5 Correlations identified:**

### 1. Cognitive Apprenticeship (Collins, Brown, Newman, 1987)
**Correlation:** Explicit modeling → guided practice → fading → independent mastery
- **Relevance:** Framework suggestions = modeling step
- **Evidence quality:** Strong (replicated across domains)
- **Confidence:** 85%

### 2. Chunk Theory & Pattern Recognition (Chase & Simon, 1973; Ericsson, 2006)
**Correlation:** Expert performance correlates with recognizing ~50,000-100,000 patterns
- **Relevance:** Frameworks = learnable patterns
- **Mechanism:** Repeated exposure builds pattern library
- **Evidence quality:** Strong (chess, medical diagnosis, programming)
- **Confidence:** 90%

### 3. Spaced Repetition & Contextual Retrieval (Bjork & Bjork, 2011)
**Correlation:** Learning strengthened by varied context + retrieval practice
- **Relevance:** AI suggesting in context = retrieval cue
- **Finding:** Desirable difficulties enhance retention
- **Evidence quality:** Strong (laboratory + field studies)
- **Confidence:** 88%

### 4. Externalized Cognition (Clark & Chalmers, 1998; Hutchins, 1995)
**Correlation:** Tools become part of cognitive system when reliably coupled
- **Relevance:** Framework catalog = cognitive prosthetic
- **Mechanism:** Extended mind thesis
- **Evidence quality:** Moderate (philosophical + anthropological)
- **Confidence:** 70%

### 5. Transfer of Learning (Barnett & Ceci, 2002)
**Correlation:** Near transfer common, far transfer rare without explicit abstraction
- **Relevance:** Framework encoding = explicit abstraction layer
- **Implication:** Structured encoding may enhance far transfer
- **Evidence quality:** Moderate (meta-analysis)
- **Confidence:** 65%
- **Note:** This is the **weakest link**—transfer is hard even with scaffolding

**Result:** Belief well-grounded in empirical correlations, with explicit acknowledgment of weakest evidence (transfer). Avoids claiming causation, maintains epistemic humility.

---

## Why This Matters

**Epistemic humility:**
- Acknowledges limits of knowledge
- Doesn't overstate claims
- Honest about uncertainty

**Falsifiable:**
- Correlations can be tested
- Confidence can be updated
- Weakest link identified for focus

**Anti-hallucination:**
- Cites real research
- Specific authors and years
- Evidence quality assessed

**Intellectual honesty:**
- Hume's insight respected
- No causal leaps
- Correlation ≠ causation explicit

---

## Anti-Patterns to Avoid

**❌ Claim causation without caveat**
- "Frameworks cause learning" → too strong
- Should be: "Framework exposure correlates with learning gains"

**❌ Cite research without specifics**
- "Studies show..." → which studies?
- Need: (Author, Year) citations

**❌ Ignore evidence quality**
- Treat all sources equally
- Need: Strong/Moderate/Weak assessment

**❌ Miss weakest link**
- Present all correlations as equal
- Need: Identify which is most uncertain

**❌ No confidence ratings**
- Binary "true/false"
- Need: Probabilistic confidence (40-95%)

**❌ Cherry-pick supportive evidence**
- Ignore contradicting studies
- Need: Acknowledge gaps and contradictions

---

## Relation to Other Skills

**Used primarily in:**
- steelman-enhance (grounding abstract claims)

**Could be used in:**
- Any empirical claim validation
- Research synthesis
- Literature reviews
- Hypothesis generation

**Complements:**
- ARIZ (resolving contradictions in evidence)
- ACH (comparing competing hypotheses)
- Cynefin (classifying evidence type)
- Scientific method (hypothesis testing)

---

## Philosophical Foundation

**Hume's Problem of Induction:**
- Past correlations don't guarantee future ones
- Causality is habit of mind, not observed fact
- Science progresses by finding correlations, not proving causation

**Karl Popper's Falsificationism:**
- Scientific claims must be falsifiable
- Confidence updates with evidence
- Never "proven," only "not yet falsified"

**Application:**
- State correlations, not laws
- Rate confidence, don't claim certainty
- Identify what would falsify the claim
- Update beliefs with new evidence

**Result:** Intellectually honest, empirically grounded, epistemically humble belief statements.
