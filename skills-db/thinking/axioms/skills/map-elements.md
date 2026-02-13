---
name: map-elements
description: This skill should be used when understanding the full landscape of non-rational influences on a belief. It helps agents systematically map emotional drivers, tribal affiliations, political orientation, personality traits, and physiological states to identify bias risks and hidden motivations, creating a complete profile of how identity and embodiment shape reasoning.
---

# map-elements

**Framework used:** Polyvagal Theory

**Purpose:** Map the emotional drivers, tribal affiliations, political spectrum position, and autonomic nervous system states influencing a belief to identify potential biases and motivations.

**When to use:**
- After axioms have been identified
- Before multi-perspective debate
- Understanding non-rational drivers of belief
- Identifying bias risks and mitigation strategies

---

## Input Contract

**Required:**
- `03-dig-axioms.md` - Complete axiom hierarchy with root axioms identified

**Format:**
```markdown
## Complete Axiom Hierarchy
[Hierarchy showing BELIEF → LEVEL 1 → LEVEL 2 → ROOT]
```

---

## Execution Steps

### Step 1: Summarize Core Axioms
Extract from dig-axioms:
- Original belief
- Level 1 axiom
- Level 2 axiom (if present)
- Root axiom
- Critical vulnerabilities

### Step 2: Map Primary Emotions (4-6 emotions)

For each emotion, document:
- **Name:** Hope, Anxiety, Pride, Curiosity, etc.
- **Intensity:** (0-100% scale)
- **Nature:** Brief description
- **Manifestations:** How it appears in the belief/reasoning (2-3 examples)
- **Underlying need:** What this emotion is serving
- **Polyvagal state:** Ventral vagal / Sympathetic / Dorsal vagal / Fawn

**Categories to consider:**
- Positive anticipation (hope, excitement, wonder)
- Negative anticipation (anxiety, fear, doubt)
- Investment (pride, attachment, defensiveness)
- Exploration (curiosity, fascination, playfulness)

### Step 3: Identify Emotional Pattern
Synthesize into cluster label:
- What's the dominant emotional driver?
- How do emotions interact?
- Is the balance healthy or biased?

### Step 4: Map Tribal/Political Alignments (4-6 tribes)

For each tribal affiliation:
- **Tribe name** (AI Optimists, Rationalists, etc.)
- **Alignment strength:** (0-100%)
- **Characteristics:** What defines this tribe (3-4 points)
- **Tribal markers:** Language, references, narratives used
- **Political compass:** Economic left/right, social auth/lib
- **Big 5 correlation:** Which personality traits correlate

**Tribes to consider:**
- Technology philosophy (AI optimists/skeptics, open source, etc.)
- Intellectual movements (Rationalists, Effectiviology, etc.)
- Political orientation (left/right, libertarian/authoritarian)
- Epistemological stance (empiricists, intuitionists, etc.)

### Step 5: Identify Tribal Tensions
Document 2-3 tensions where tribal affiliations conflict:
- Which tribes pull in different directions?
- What identity conflicts might arise?
- Where do values compete?

### Step 6: Map Political Spectrum

**Haidt's Moral Foundations:**
Create table scoring 1-10 on each foundation:
- Care/Harm
- Fairness/Cheating
- Loyalty/Betrayal
- Authority/Subversion
- Sanctity/Degradation
- Liberty/Oppression

Identify pattern (e.g., "Libertarian-Left")

**Political Compass:**
- Economic axis (-10 left to +10 right)
- Social axis (-10 libertarian to +10 authoritarian)
- Position estimate with rationale

### Step 7: Create Big 5 Profile

Score percentile (0-100) on:
- **Openness:** Novelty-seeking, abstract thinking
- **Conscientiousness:** Organization, systematic work
- **Extraversion:** Social energy, assertiveness
- **Agreeableness:** Cooperation, empathy
- **Neuroticism:** Emotional stability, anxiety

Include evidence from analysis for each score.

### Step 8: ANS Quadrant Mapping (Polyvagal)

Map current autonomic state:

**States to assess:**
- **Ventral Vagal (Safe & Social):** Curiosity, exploration, connection
- **Sympathetic (Mobilization):** Anticipation, vigilance, energy
- **Dorsal Vagal (Shutdown):** Despair, freeze, disconnect
- **Fawn (Appeasement):** Over-accommodation, people-pleasing

Assign percentages and create quadrant chart.

Document latent triggers (what would activate shutdown/fawn states).

### Step 9: Optional Correlations
If relevant, include:
- Hormonal/neurochemical correlations (dopamine, oxytocin, etc.)
- Time perception (future/present/past focus)
- Determinism/free will beliefs
- Other relevant psychological dimensions

### Step 10: Identify Bias Warnings
List 3-5 potential biases:
- Confirmation bias (in-group)
- Sunk cost (investment)
- Motivated reasoning (emotional drivers)
- Tribal epistemology (echo chambers)

Include mitigation evidence (e.g., "This exploration demonstrates bias awareness").

---

## Output Contract

**File:** `04-map-elements.md`

**Required sections:**
1. Core Axioms Summary (from dig-axioms)
2. Emotional Drivers (4-6 emotions with full breakdown)
3. Emotional Pattern (synthesis/cluster label)
4. Tribal/Political Alignments (4-6 tribes)
5. Tribal Tensions (2-3 conflicts)
6. Political Spectrum Mapping (Haidt + Compass)
7. Big 5 Personality Profile (table with evidence)
8. ANS Quadrant Mapping (percentages + chart)
9. Summary: Emotional & Tribal Landscape (synthesis)
10. Potential Bias Warnings (3-5 with mitigation)
11. Metadata

**Template:**
```markdown
# Map Elements Output

**Analysis ID:** axiom-<YYYYMMDD-HHMMSS>
**Timestamp:** <ISO timestamp>
**Previous step:** 03-dig-axioms.md
**Next step:** 05a-devils-advocate.md
**Framework used:** Polyvagal Theory

---

## Core Axioms Summary

[Brief list of belief → axiom chain from dig-axioms]

---

## Emotional Drivers

### Primary Emotions

#### 1. **[Emotion Name]** (Dominant - [60-100]%)
**Nature:** [Brief description]

**Manifestations:**
- [Example 1]
- [Example 2]
- [Example 3]

**Underlying need:** [What this serves]

**Polyvagal state:** [Ventral vagal / Sympathetic / Dorsal / Fawn]

---

[Repeat for 4-6 emotions]

---

### Emotional Pattern

**Cluster:** **[Pattern Name]**

[2-4 sentence synthesis of how emotions interact]

**Healthy balance:** [Assessment of emotional influence]

---

## Tribal / Political Alignments

### Technology & Philosophy Tribes

#### 1. **[Tribe Name]** (Strong Alignment - [60-100]%)
**Characteristics:**
- [Characteristic 1]
- [Characteristic 2]
- [Characteristic 3]

**Tribal markers:**
- Language: [Examples]
- References: [Who/what cited]
- Narrative: [Core story]

**Political Compass:** [Position]

**Big 5 Correlation:** [Which traits]

---

[Repeat for 4-6 tribes]

---

### Tribal Tensions

#### Tension 1: **[Tribe A] vs [Tribe B]**
[Description of conflict and implications]

---

[Repeat for 2-3 tensions]

---

## Political Spectrum Mapping

### Haidt's Moral Foundations
| Foundation | Score (1-10) | Evidence |
|------------|--------------|----------|
| **Care/Harm** | [score] | [evidence] |
| **Fairness/Cheating** | [score] | [evidence] |
| **Loyalty/Betrayal** | [score] | [evidence] |
| **Authority/Subversion** | [score] | [evidence] |
| **Sanctity/Degradation** | [score] | [evidence] |
| **Liberty/Oppression** | [score] | [evidence] |

**Pattern:** **[Pattern Name]**

---

### Political Compass
```
      Authoritarian
            |
    Left ---|--- Right
            |
      Libertarian
```
**Position:** **[Position]** ([economic score], [social score])

**Rationale:**
- **[Axis]:** [Why positioned here]
- **[Axis]:** [Why positioned here]

---

## Big 5 Personality Profile

| Trait | Score (Percentile) | Evidence from Analysis |
|-------|-------|---------------------|
| **Openness** | [0-100]th | [evidence] |
| **Conscientiousness** | [0-100]th | [evidence] |
| **Extraversion** | [0-100]th | [evidence] |
| **Agreeableness** | [0-100]th | [evidence] |
| **Neuroticism** | [0-100]th | [evidence] |

**Profile:** **[Profile description]**

---

## ANS Quadrant Mapping (Polyvagal Analysis)

### Autonomic Nervous System States

#### Current Dominant State: **[State Name]**
**Indicators:**
- [Indicator 1]
- [Indicator 2]
- [Indicator 3]

**Percentage:** [0-100]%

---

[Repeat for all active states]

---

### ANS Quadrant Chart

```
        Ventral Vagal (Safe & Social)
              |  ← [%]
              |
    Fawn ----+---- Fight
    ([%])    |      ([%])
              |
              |
    Freeze --+---- Flight
    ([%])    |      ([%])
              |
        Dorsal Vagal (Shutdown)
```

**Current position:** [Description]

---

## Summary: Emotional & Tribal Landscape

### Emotional Core:
**[1-2 sentence synthesis]**

### Tribal Alignment:
**[List key tribes]**
- Political: [Position]
- Personality: [Key traits]
- Morality: [Key foundations]

### ANS State:
**[Description of current state]**

### Critical Insight:
[How emotional/tribal factors influence belief - supportive or biased?]

---

## Potential Bias Warnings

1. **[Bias name]:** [Description]
2. **[Bias name]:** [Description]
3. **[Bias name]:** [Description]

**Mitigation:** [Evidence of bias awareness and correction]

---

## Metadata

- Emotional drivers identified: [count]
- Tribal alignments: [count]
- Political compass: [position]
- Big 5 profile: [summary]
- ANS quadrant: [percentages]
- Framework used: Polyvagal Theory
- Ready for multi-devils debate: Yes
```

---

## Quality Checks

Before completing:
- [ ] 4-6 emotions mapped with full breakdown
- [ ] 4-6 tribal affiliations with characteristics
- [ ] Haidt foundations scored with evidence
- [ ] Political compass position justified
- [ ] Big 5 profile has evidence for each trait
- [ ] ANS quadrant percentages total ~100%
- [ ] Bias warnings identified with mitigation
- [ ] Summary synthesizes landscape

---

## Example from Live Execution

**Emotional drivers:**
1. Hope/Optimism (80%) - dominant
2. Anxiety/Doubt (40%) - secondary
3. Pride/Investment (60%) - moderate
4. Curiosity/Wonder (75%) - strong

**Pattern:** "Hopeful Builder with Intellectual Humility"

**Tribal alignments:**
1. AI Optimists (85%)
2. Rationalists (70%)
3. Open Source (80%)
4. Computationalists (65%)

**Political:** Left-Libertarian (-3, -5)

**Big 5:** O95 C80 E40 A65 N35

**ANS:** 60% ventral vagal, 30% sympathetic, 10% latent

**Bias warnings:**
- Confirmation (in-group)
- Sunk cost (months invested)
- Motivated reasoning (hope)

**Mitigation:** Exploration itself shows bias awareness

**Result:** Clear map of non-rational influences, bias risks identified, intellectual honesty preserved.
