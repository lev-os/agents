---
name: steelman-enhance
description: This skill should be used after identifying a belief's primary framing to strengthen it before critical analysis. It helps agents resolve internal contradictions, ground abstract claims in research evidence, and classify claims by confidence level, resulting in a maximally defensible version that reveals which parts are solid and which need validation.
---

# steelman-enhance

**Framework used:** ARIZ (Algorithm for Inventive Problem Solving)

**Purpose:** Build the strongest charitable version of a belief by resolving internal contradictions and grounding claims in empirical correlations.

**When to use:**
- After paraphrase-engineer has selected primary framing
- Before digging into deeper axioms
- When belief has internal tensions that need resolving
- To ground abstract claims in research evidence

---

## Input Contract

**Required:**
- `01-paraphrase.md` - Selected variation and refined belief statement

**Format:**
```markdown
## Selected Variation for Next Steps

**Primary:** **1[x]. [Framing Name]**

**Refined belief statement:**
"[statement]"
```

---

## Execution Steps

### Step 1: Identify Internal Contradictions
Analyze the refined belief for tensions:
- Conflicting claims within the statement
- Vague terms that could mean different things
- Implicit assumptions that conflict
- Overstated vs understated elements

Document 2-4 major contradictions with clear framing:
- What's the tension?
- Why does it matter?

### Step 2: Resolve Each Contradiction
For each contradiction, apply ARIZ problem-solving:
- Reframe as "levels of processing" or "both/and"
- Distinguish necessary vs sufficient conditions
- Clarify mechanism or causal chain
- Find synthesis that preserves both aspects

Document the resolution clearly.

### Step 3: Find Supporting Empirical Correlations
Identify 5 empirical correlations from research literature:
- Use correlation language ("X correlates with Y")
- Cite actual research (author, year)
- Assess relevance to the belief
- Rate evidence quality (Strong/Moderate/Weak)
- Assign confidence (40-95%)

**Coverage:**
- At least 2 with 80%+ confidence
- At least 1 identified as "weakest link"
- Mix of strong and moderate evidence

### Step 4: Classify Claims by Strength
Organize all claims into three tiers:

**Strong Claims (80%+ confidence):**
- Well-established in literature
- Multiple replications
- Clear mechanisms

**Moderate Claims (60-80% confidence):**
- Some evidence but context-dependent
- Fewer studies or mixed results
- Plausible but not proven

**Weak Claims (40-60% confidence):**
- Speculative or untested
- Analogies without direct evidence
- Requires empirical validation

### Step 5: Identify Gaps in Evidence
Document what's missing:
- Critical missing evidence (what would validate/invalidate)
- Questions needing empirical test
- Confounds not controlled for
- Alternative explanations not ruled out

### Step 6: Write Enhanced Belief Statement
Synthesize into strongest charitable version that:
- Resolves all contradictions
- Grounds claims in correlations
- Acknowledges gaps
- Uses precise language
- Makes assumptions explicit

### Step 7: Assess Overall Confidence
Provide confidence estimate with breakdown:
- Mechanism plausibility
- AI capability assessment
- Human learning assessment
- Superiority to alternatives
- Overall confidence (weighted)

---

## Output Contract

**File:** `02-steelman.md`

**Required sections:**
1. Strongest Charitable Version (opening synthesis)
2. Internal Contradictions Resolved (2-4 contradictions)
3. Supporting Empirical Correlations (5 correlations with citations)
4. Strengthened Claims (organized by confidence tier)
5. Gaps in Evidence (critical missing + questions)
6. Enhanced Belief Statement (final synthesis)
7. Confidence Assessment (breakdown + overall)
8. Metadata

**Template:**
```markdown
# Steelman & Enhance Output

**Analysis ID:** axiom-<YYYYMMDD-HHMMSS>
**Timestamp:** <ISO timestamp>
**Previous step:** 01-paraphrase.md (Selected: [variation])
**Next step:** 03a-level1.md
**Framework used:** ARIZ (Algorithm for Inventive Problem Solving)

---

## Strongest Charitable Version

"[3-5 sentence synthesis incorporating contradictions resolved and empirical grounding]"

---

## Internal Contradictions Resolved

### Contradiction 1: [Name] vs [Name]
**Original tension:** [What's the conflict?]

**Resolution:** [How ARIZ resolves it - levels, necessary/sufficient, both/and, etc.]

---

[Repeat for 2-4 contradictions]

---

## Supporting Empirical Correlations

### 1. [Research Area] ([Authors, Year])
**Correlation:** [What correlates with what]
- **Relevance:** [How it applies to belief]
- **Evidence quality:** [Strong/Moderate/Weak] ([why])
- **Confidence:** [60-95]%

---

[Repeat for 5 correlations]

---

## Strengthened Claims

### Strong Claims (80%+ confidence):
1. [Claim] - [Why strong]
2. [Claim] - [Why strong]
3. [Claim] - [Why strong]

### Moderate Claims (60-80% confidence):
1. [Claim] - [Why moderate]
2. [Claim] - [Why moderate]

### Weak Claims (40-60% confidence):
1. [Claim] - [Why weak]
2. [Claim] - [Why weak]

---

## Gaps in Evidence

### Critical Missing Evidence:
1. [What's missing]
2. [What's missing]

### Questions Needing Empirical Test:
- [Question 1]
- [Question 2]
- [Question 3]

---

## Enhanced Belief Statement

"[2-4 sentence final synthesis]"

---

## Confidence Assessment

- **Mechanism plausibility:** [60-95]% ([rationale])
- **AI capability to X:** [60-95]% ([rationale])
- **Human learning via Y:** [60-95]% ([rationale])
- **Superior to alternatives:** [40-95]% ([rationale])
- **Overall confidence:** [60-95]% → [maintained/increased/decreased], [why]

---

## Metadata

- Framework used: ARIZ for contradiction resolution
- Correlations added: 5 (with confidence scores)
- Internal contradictions resolved: [2-4]
- Gaps identified: [number] critical
- Ready for axiom drilling: Yes
```

---

## Quality Checks

Before completing:
- [ ] All contradictions have clear resolutions
- [ ] 5 empirical correlations with proper citations
- [ ] Claims organized by evidence strength
- [ ] Gaps explicitly acknowledged
- [ ] Enhanced statement is stronger than original
- [ ] Confidence assessment includes breakdown

---

## Example from Live Execution

**Input belief:**
> "Cataloging decision-making patterns allows AI to recognize and suggest relevant frameworks in context, training humans to see these patterns independently over time."

**Contradictions resolved:**
1. "Make AI think" vs "AI suggests" → Levels of processing
2. "Osmosis" vs "Training" → Cognitive apprenticeship model
3. "Encoding makes" vs "Encoding enables" → Necessary but not sufficient

**Correlations added:**
1. Cognitive Apprenticeship (Collins et al., 1987) - 85% confidence
2. Chunk Theory (Chase & Simon, 1973) - 90% confidence
3. Spaced Repetition (Bjork & Bjork, 2011) - 88% confidence
4. Externalized Cognition (Clark & Chalmers, 1998) - 70% confidence
5. Transfer of Learning (Barnett & Ceci, 2002) - 65% confidence (weakest link)

**Enhanced statement:**
> "A structured catalog of thinking frameworks enables AI to pattern-match and suggest contextually relevant reasoning approaches. Through cognitive apprenticeship—where AI provides explicit scaffolding that fades as skill develops—humans can potentially internalize these patterns via repeated exposure in authentic contexts. This mechanism aligns with established theories of expertise development (chunking, deliberate practice) and externalized cognition, though empirical validation of the osmotic learning claim and far transfer effects remains necessary."

**Result:** Maintained 70% confidence but now evidence-based, contradictions resolved, gaps acknowledged.
