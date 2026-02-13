---
name: ans-quadrant-mapping
description: This skill should be used when analyzing the physiological and embodied dimensions of a belief or position. It helps agents map autonomic nervous system states using Polyvagal Theory to expose how threat responses, safety cues, and physiological arousal influence reasoning, enabling identification of when thinking shifts from open exploration to defensive or shutdown modes.
---

# ans-quadrant-mapping

**Supporting skill - used within map-elements**

**Framework used:** Polyvagal Theory

**Purpose:** Map current autonomic nervous system state using Polyvagal Theory to understand physiological drivers of belief and identify potential triggers.

**When to use:**
- During emotional/tribal mapping (map-elements)
- Understanding embodied aspects of belief
- Identifying stress responses influencing reasoning
- Predicting potential threat reactions

---

## Core Theory: Polyvagal

**Three autonomic states:**

### 1. Ventral Vagal (Safe & Social)
- Newest evolutionary system
- Active when feeling safe
- Enables: Curiosity, exploration, connection, learning
- Facial expressions: Open, relaxed, engaged
- Voice: Melodic, varied prosody

### 2. Sympathetic (Mobilization)
- Fight or flight system
- Active under stress or positive arousal
- Enables: Action, energy, vigilance
- Two modes:
  - **Positive:** Excitement, anticipation, enthusiasm
  - **Negative:** Anxiety, panic, aggression

### 3. Dorsal Vagal (Shutdown)
- Oldest evolutionary system
- Active under extreme threat
- Enables: Freeze, collapse, dissociation
- Protective mechanism when fight/flight fails

### 4. Fawn (Appeasement)
- Hybrid state
- Active when power imbalance
- Enables: People-pleasing, over-accommodation
- Attempts to defuse threat through submission

---

## Execution Steps

### Step 1: Assess Indicators for Each State

**Ventral Vagal (Safe & Social) indicators:**
- Curiosity-driven exploration
- Open to challenge without defensiveness
- Prosocial motivation
- Intellectual playfulness
- Collaborative language
- Genuine questions

**Sympathetic (Mobilization) indicators:**
- Hope/anticipation (positive)
- Anxiety/vigilance (negative)
- Urgency
- High energy
- Need to convince or defend
- Investment concern

**Dorsal Vagal (Shutdown) indicators:**
- Despair or hopelessness
- Disconnection from topic
- "Nothing matters" attitude
- Low energy
- Avoidance

**Fawn (Appeasement) indicators:**
- Over-accommodation
- Excessive agreement
- Minimizing own position
- Deferring to authority
- Apologizing unnecessarily

### Step 2: Assign Percentages

Assess what percentage of current state is in each mode:
- Percentages should total ~100%
- Most beliefs involve mixed states
- Document reasoning for each percentage

**Example:**
- Ventral Vagal: 60% (primary - safe exploration)
- Sympathetic: 30% (positive anticipation, mild vigilance)
- Dorsal Vagal: 5% (latent, not active)
- Fawn: 5% (latent, not active)

### Step 3: Document Current Dominant State

**For each active state (>20%):**
- Name the state
- List 3-5 indicators supporting assessment
- Assign percentage
- Note positive vs negative mobilization if sympathetic

### Step 4: Identify Latent States

**For inactive states (<20%):**
- Note they're latent
- Identify potential triggers that would activate them
- What would cause shift to shutdown?
- What would cause shift to fawn?

### Step 5: Create Visual Quadrant Chart

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

### Step 6: Assess Current Position
Describe overall autonomic state in 1-2 sentences:
- Primary mode and why
- Mixed states and balance
- Overall assessment (healthy exploration vs threat-reactive)

---

## Output Format

**Embedded within map-elements file:**

```markdown
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

#### Latent States: **[State Names]**
**Not currently active, but potential triggers:**
- **[State]:** If [trigger] → [response]
- **[State]:** If [trigger] → [response]

**Percentage:** [0-20]% (latent)

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

**Current position:** [1-2 sentence description]
```

---

## Quality Checks

Before completing:
- [ ] All four states assessed (ventral vagal, sympathetic, dorsal vagal, fawn)
- [ ] Indicators listed for active states (3-5 each)
- [ ] Percentages assigned and total ~100%
- [ ] Latent states identified with triggers
- [ ] Quadrant chart created
- [ ] Current position described
- [ ] Assessment reflects evidence from belief exploration

---

## Example from Live Execution

**Assessment:**

#### Current Dominant State: **Ventral Vagal (Safe & Social)**
**Indicators:**
- Curiosity-driven exploration
- Open to challenge without defensiveness
- Prosocial motivation (teach humanity)
- Intellectual playfulness ("amazing," "continue")

**Percentage:** 60%

#### Secondary State: **Sympathetic (Mobilization)**
**Indicators:**
- Hope/anticipation (positive mobilization)
- Mild anxiety about project validity (scanning threats)
- Urgency to validate (3+ months invested)

**Percentage:** 30%

#### Latent States: **Dorsal Vagal (Shutdown) & Fawn (Appeasement)**
**Not currently active, but potential triggers:**
- **Shutdown:** If axiom chain fully collapses (functionalism disproven) → despair, "all work wasted"
- **Fawn:** If criticized by respected authority → over-accommodation, abandoning valid insights

**Percentage:** 10% (latent)

**Quadrant Chart:**
```
        Ventral Vagal (Safe & Social)
              |  ← 60%
              |
    Fawn ----+---- Fight
    (10%)    |      (5%)
              |
              |
    Freeze --+---- Flight
    (5%)     |      (20%)
              |
        Dorsal Vagal (Shutdown)
```

**Current position:** Primarily ventral vagal with sympathetic activation (positive arousal, not threat-based)

**Result:** Clear map of physiological state influencing belief. Mostly safe exploration with some positive anticipation. Low threat response. Identifies what would trigger shutdown/fawn if analysis threatened core assumptions or identity.

---

## Why This Matters

**Embodied cognition:**
- Beliefs aren't just cognitive
- Physiological state influences reasoning
- Threat responses narrow thinking

**Bias awareness:**
- Ventral vagal → open exploration
- Sympathetic (negative) → defensive reasoning
- Dorsal → shutdown, avoidance
- Fawn → excessive agreement, no critical thinking

**Predictive:**
- Knowing latent triggers helps avoid them
- Can recognize when shifting states
- Adjust approach based on ANS state

**Integration:**
- Complements emotional mapping (what you feel)
- Complements tribal mapping (who you align with)
- Adds physiological layer (how your body responds)

---

## Anti-Patterns to Avoid

**❌ Assume single state**
- Most situations are mixed
- Document percentages, not binary

**❌ Ignore positive sympathetic**
- Sympathetic ≠ always threat
- Can be excitement, anticipation, hope

**❌ Pathologize states**
- All states are adaptive
- Context determines appropriateness
- Shutdown/fawn appropriate under real threat

**❌ Guess without indicators**
- Need evidence from exploration
- Language, openness, defensiveness
- Not arbitrary assignment

**❌ Skip latent triggers**
- Identifying what would shift states is valuable
- Helps predict threat responses
- Reveals vulnerabilities

---

## Relation to Other Skills

**Used primarily in:**
- map-elements (emotional/tribal landscape)

**Could be used in:**
- Conflict analysis
- Team dynamics assessment
- Leadership coaching
- Therapy/counseling contexts

**Complements:**
- Polyvagal Theory (framework for ANS states)
- Haidt's Moral Foundations (political/moral drivers)
- Big 5 Personality (trait patterns)
- Emotional intelligence frameworks
