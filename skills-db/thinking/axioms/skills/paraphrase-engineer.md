---
name: paraphrase-engineer
description: This skill should be used when a belief statement is ambiguous or could be interpreted multiple ways. It helps agents systematically reframe claims across five distinct lenses (knowledge transfer, tool augmentation, pattern recognition, cultural transmission, capability emergence) to expose hidden axioms and select the interpretation that most accurately captures user intent.
---

# paraphrase-engineer

**Framework used:** THINK Paradigm

**Purpose:** Generate 3-5 variations of a belief statement, each exposing different axiom implications to reveal how framing affects underlying assumptions.

**When to use:**
- Starting axiom exploration with a user's belief
- Uncovering hidden assumptions through reframing
- Identifying which interpretation is most accurate
- Clarifying ambiguous or multi-faceted beliefs

---

## Input Contract

**Required:**
- `00-input.md` - User's original belief statement

**Format:**
```markdown
# Input Belief

[User's belief statement]
```

---

## Execution Steps

### Step 1: Extract Core Belief
Read the input belief statement and identify the core claim being made.

### Step 2: Generate 5 Variations
Create exactly 5 paraphrased variations, each revealing different axiom implications:

**Variation types to include:**
1. **Knowledge Transfer Framing** - Focus on how knowledge moves between entities
2. **Tool Augmentation Framing** - Focus on enhancement vs transformation
3. **Pattern Recognition Framing** - Focus on learning mechanisms
4. **Cultural Transmission Framing** - Focus on social/memetic aspects
5. **Capability Emergence Framing** - Focus on emergent properties

### Step 3: Document Axiom Implications
For each variation, explicitly list the axiom implications:
- What assumptions does this framing make?
- What view of cognition/learning does it imply?
- What mechanisms are assumed?
- What's the implied causal chain?

### Step 4: Select Primary Variation
Choose the variation that:
- Most accurately captures the original intent
- Has the clearest axiom implications
- Aligns with observable mechanisms
- Provides strongest foundation for deeper analysis

Document rationale for selection and note secondary considerations.

### Step 5: Engineer Refined Statement
Create a refined belief statement based on the selected variation that:
- Clarifies key concepts to track
- Makes implicit assumptions explicit
- Sets up cleanly for steelman enhancement

---

## Output Contract

**File:** `01-paraphrase.md`

**Required sections:**
1. Original Belief (quoted verbatim)
2. Paraphrased Variations (5 total, numbered 1a-1e)
   - Each with "Axiom implications:" subsection (4-5 bullet points)
3. Selected Variation for Next Steps (with rationale)
4. Engineered Prompt for Subsequent Processing
5. Metadata (variations count, selection, confidence, readiness)

**Template:**
```markdown
# Paraphrase & Engineer Output

**Analysis ID:** axiom-<YYYYMMDD-HHMMSS>
**Timestamp:** <ISO timestamp>
**Previous step:** 00-input.md
**Next step:** 02-steelman.md
**Framework used:** THINK Paradigm

---

## Original Belief

"[verbatim quote]"

---

## Paraphrased Variations

### 1a. **[Framing Name]**
"[paraphrased version]"

**Axiom implications:**
- [assumption 1]
- [assumption 2]
- [assumption 3]
- [assumption 4]

---

[Repeat for 1b through 1e]

---

## Selected Variation for Next Steps

**Primary:** **1[x]. [Framing Name]**

**Rationale:**
- [why this captures intent best]
- [what it reveals about assumptions]
- [how it sets up next steps]

**Secondary consideration:** [other variations worth tracking]

---

## Engineered Prompt for Subsequent Processing

**Refined belief statement:**
"[selected variation text]"

**Key concepts to track:**
- [concept 1]
- [concept 2]
- [concept 3]
- [concept 4]
- [concept 5]

---

## Metadata

- Variations generated: 5
- Selection: 1[x] ([Framing Name])
- Confidence in paraphrase accuracy: [60-95]%
- Ready for steelman-enhance: Yes
```

---

## Quality Checks

Before completing:
- [ ] All 5 variations capture different aspects of the belief
- [ ] Each variation has 4-5 explicit axiom implications
- [ ] Selection is clearly justified
- [ ] Refined statement is clearer than original
- [ ] Key concepts for tracking are identified

---

## Example from Live Execution

**Input:**
> "By encoding all the skills in the domains folder, hidden gems, and axioms, we can make AI think and teach humans how to think and grow by osmosis."

**Generated variations:**
1. Knowledge Transfer Framing
2. Tool Augmentation Framing
3. **Pattern Recognition Framing** (selected)
4. Cultural Transmission Framing
5. Capability Emergence Framing

**Selected (1c):**
> "Cataloging decision-making patterns allows AI to recognize and suggest relevant frameworks in context, training humans to see these patterns independently over time."

**Axiom implications exposed:**
- Frameworks = patterns to be recognized
- AI's role is suggestion/guidance, not teaching
- Human learning = pattern recognition training
- Independence as goal (scaffolding that removes itself)

**Result:** Clearer mechanism, explicit assumptions, ready for steelman enhancement.
