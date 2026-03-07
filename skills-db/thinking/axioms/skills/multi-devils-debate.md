---
name: multi-devils-debate
description: "This skill should be used when a belief requires rigorous testing against its strongest possible counterarguments. It guides agents through multi-turn debate (3 rounds: FOR, AGAINST, synthesis) to argue both positions with full conviction, identify genuine disagreements versus false ones, propose hybrid models, and calibrate confidence based on integrated perspective rather than initial conviction."
---

# multi-devils-debate (MULTI-TURN)

**Framework used:** Second-Order Thinking

**Purpose:** Conduct rigorous multi-perspective debate by arguing FOR (devils advocate), AGAINST (anti-devils), then synthesizing both positions to find common ground and genuine disagreements.

**Multi-turn structure:** Three sequential rounds producing separate files.

**When to use:**
- After emotional/tribal mapping is complete
- Before final synthesis
- When belief has substantive counterarguments
- Testing robustness against strongest critiques

---

## Multi-Turn Structure

This skill executes across 3 turns:
- **Turn 1 (05a-devils-advocate.md):** Argue FOR the belief (strengthen beyond steelman)
- **Turn 2 (05b-anti-devils.md):** Argue AGAINST the belief (strongest critique)
- **Turn 3 (05c-synthesis.md):** Integrate both perspectives (common ground + genuine tensions)
- **Complete (05-multi-devils.md):** Full debate record with decision frameworks

---

## Turn 1: Devils Advocate (FOR) Input Contract

**Required:**
- `04-map-elements.md` - Emotional/tribal landscape

**Format:**
```markdown
## Summary: Emotional & Tribal Landscape

[Synthesis of emotional drivers and tribal affiliations]
```

---

## Turn 1: Execution Steps

### Step 1: Frame Role and Position
- Role: Arguing FOR the belief
- Approach: Strengthen argument beyond steelman
- Strategy: Find overlooked advantages, dismiss critiques

### Step 2: Build Core Argument
Create compelling thesis (1-3 sentences) that:
- Frames belief in strongest possible terms
- Uses compelling metaphor or framing
- Emphasizes transformative potential

### Step 3: Present Strongest Arguments FOR (5-7 arguments)

For each argument:
- Clear subheading
- Detailed explanation (3-6 paragraphs)
- Specific evidence and examples
- Why this argument is compelling

**Argument categories to cover:**
1. Empirical success of related systems
2. Technological breakthrough/readiness
3. Compounding returns / network effects
4. Addresses real problems / failure modes
5. Falsifiable and improvable
6. Additional domain-specific arguments

### Step 4: Preemptively Address Critiques (3-5 critiques)

For each critique:
- State the critique clearly
- Present dismissal or reframing
- Show why critique is orthogonal or misguided

### Step 5: Identify Axioms of This Position

**Core axiom:**
- State the foundational presumption
- Explain implications
- Why this axiom supports the position

**Secondary axioms (1-2):**
- Supporting presumptions
- Evidence for each

### Step 6: Map Emotional Core
What emotions drive this position?
- Primary emotions (hope, optimism, etc.)
- Underlying drivers
- ANS state
- Polyvagal interpretation

### Step 7: Map Tribal Affiliation
Which tribes would endorse this position?
- 3-5 tribal identities
- Political orientation
- Why this position signals belonging

### Step 8: Provide Strongest Version Summary
2-4 sentence synthesis of the absolute strongest case.

### Step 9: Justify Full Endorsement
List 5-7 reasons why this position deserves full endorsement.

### Step 10: Confidence Assessment
Rate confidence in this position (typically higher than balanced view).
Explain why confidence is elevated.

---

## Turn 1: Output Contract

**File:** `05a-devils-advocate.md`

**Required sections:**
1. Role: Arguing FOR the Position
2. Core Argument (thesis)
3. Strongest Arguments FOR (5-7 detailed)
4. Addressing Critiques (3-5 preemptive)
5. Axioms of This Position (core + secondary)
6. Emotional Core of This Position
7. Tribal Affiliation
8. Strongest Version Summary
9. Why This Position Deserves Full Endorsement
10. Confidence Assessment
11. Metadata

**Template in file creation call.**

---

## Turn 2: Anti-Devils (AGAINST) Input Contract

**Required:**
- `05a-devils-advocate.md` - FOR position and confidence

---

## Turn 2: Execution Steps

### Step 1: Frame Role and Position
- Role: Arguing AGAINST the belief
- Approach: Present strongest critique
- Strategy: Identify fatal flaws, find unconsidered alternatives

### Step 2: Build Core Counter-Argument
Create compelling counter-thesis that:
- Directly challenges core claim
- Identifies fundamental flaw or reification fallacy
- Frames alternative view

### Step 3: Present Strongest Arguments AGAINST (5-7 arguments)

For each argument:
- Clear subheading
- Detailed explanation
- Why this undermines the belief
- Evidence and examples

**Argument categories to cover:**
1. Analogies fail (domain differences)
2. Embodiment critique (tacit knowledge)
3. Transfer research (empirical failure)
4. AI limitations (lacks understanding/theory of mind)
5. Measurement problems (Goodhart's Law)
6. Philosophical alternatives (enactivism, etc.)
7. Additional domain-specific critiques

### Step 4: Dismantle FOR Arguments (3-5 rebuttals)

For each major FOR argument:
- Restate it fairly
- Identify hidden assumption or weak link
- Present counter-evidence
- Show why rebuttal is stronger

### Step 5: Identify Axioms of AGAINST Position

**Core axiom:**
- State the foundational presumption (often opposes FOR axiom)
- Explain implications
- Why this axiom undermines belief

**Secondary axioms (1-2):**
- Supporting presumptions

### Step 6: Map Emotional Core
What emotions drive skepticism?
- Primary emotions (caution, humility, etc.)
- Underlying drivers
- ANS state

### Step 7: Map Tribal Affiliation
Which tribes would endorse skeptical position?
- 3-5 tribal identities
- Why skepticism signals intellectual rigor

### Step 8: Provide Strongest Critique Summary
2-4 sentence synthesis of why belief fails.

### Step 9: Present Alternative Framework
If belief is wrong, what's the better model?
- 1-2 alternatives
- Why these work better

### Step 10: Confidence Assessment
Rate confidence in AGAINST position.
Explain reasoning.

---

## Turn 2: Output Contract

**File:** `05b-anti-devils.md`

Similar structure to Turn 1 but arguing AGAINST.

---

## Turn 3: Synthesis Input Contract

**Required:**
- `05a-devils-advocate.md` - FOR arguments and confidence
- `05b-anti-devils.md` - AGAINST arguments and confidence

---

## Turn 3: Execution Steps

### Step 1: Identify Common Ground (4-5 points)

What do both positions agree on?
- State each point of agreement
- Show how both FOR and AGAINST acknowledge it
- Assess level of agreement

### Step 2: Map Genuine Disagreements (3-5 tensions)

For each tension, create detailed comparison:

**Tension format:**
- **Dimension:** What's being debated
- **FOR Position:** What FOR claims
- **AGAINST Position:** What AGAINST claims
- **Resolution:** How to integrate or test

**Common tension types:**
- Ontology of mind (computational vs embodied)
- Learning mechanism (exposure vs practice)
- Analogy validity (works in domain X vs fails)
- AI capability (pattern-matching sufficient vs needs theory of mind)

### Step 3: Craft Integrated Position
Create synthesis statement that:
- Acknowledges both perspectives
- Identifies when/where belief works vs fails
- Proposes bounded/qualified version

### Step 4: Specify Boundary Conditions

**Works when:**
- List 4-6 conditions where belief holds

**Fails when:**
- List 4-6 conditions where belief fails

### Step 5: Propose Hybrid Model
Create model integrating both positions:
- Components from FOR
- Critiques from AGAINST addressed
- Resulting in practical approach

### Step 6: Design Critical Empirical Tests (3-5 tests)

For each test:
- **Design:** What to measure
- **Resolves:** Which tension it addresses
- **Timeline:** How long to run

### Step 7: Axiom Implications

**FOR Position Axiom:**
- Implications for project
- Risk if false

**AGAINST Position Axiom:**
- Implications for project
- Risk if false

**Synthesis Position Axiom:**
- Integrated axiom
- Implications

### Step 8: Map Emotional & Tribal Landscapes

**FOR Perspective:**
- Emotions, tribes, politics, personality

**AGAINST Perspective:**
- Emotions, tribes, politics, personality

**Synthesis Perspective:**
- Integrated emotional stance

### Step 9: Create Decision Tree/Framework
"When to use frameworks" - scoring system with 4-6 questions.

### Step 10: Resolved Confidence Estimate

**Synthesis confidence:**
- Integrate FOR (optimistic) and AGAINST (skeptical)
- Typically lower than FOR, balanced
- Detailed rationale

### Step 11: Provide Actionable Recommendations
Phased approach (3-5 phases) based on synthesis:
- Immediate (0-6 months)
- Medium-term (6-18 months)
- Long-term (18+ months)

---

## Turn 3: Output Contract

**File:** `05c-synthesis.md`

**Required sections:**
1. Integration Task (what we're synthesizing)
2. Common Ground (4-5 points of agreement)
3. Genuine Disagreements (3-5 tensions with detailed comparison)
4. Integrated Position (synthesis statement)
5. Key Qualifications (boundary conditions)
6. Proposed Hybrid Model
7. Resolved Confidence Estimate
8. Actionable Recommendations
9. Empirical Tests to Resolve Remaining Ambiguities
10. Synthesis Summary
11. Metadata

---

## Complete Record Input Contract

**Required:**
- `05a-devils-advocate.md`
- `05b-anti-devils.md`
- `05c-synthesis.md`

---

## Complete Record: Execution Steps

### Step 1: Create Debate Structure Overview
Outline the 3-round structure.

### Step 2: Summarize Each Round (3 summaries)

**For each (FOR, AGAINST, Synthesis):**
- Position statement
- Key arguments (3-5 bullets)
- Confidence level
- Tribal/emotional drivers

### Step 3: Create Comparison Tables

**Common Ground table:**
- List agreements with both positions' views

**Genuine Tensions table:**
- Dimension | FOR | AGAINST | Resolution

### Step 4: Document Refined Belief
Quote synthesis position's integrated belief statement.

### Step 5: Compile Hybrid Model
Detailed description of synthesis approach with all components.

### Step 6: List All Critical Tests
Compile all empirical tests from synthesis.

### Step 7: Create Decision Framework
Full decision tree/scoring system from synthesis.

### Step 8: Map Areas of Disagreement
Separate genuine (empirical test needed) from false (reframing resolves).

### Step 9: Compile Recommendations
All phased recommendations from synthesis.

### Step 10: Final Confidence Assessment
Track confidence trajectory: Original → FOR → AGAINST → Synthesis

### Step 11: Meta-Commentary
What did the debate reveal?
- Key insights
- Strategic implications
- Value of multi-perspective analysis

---

## Complete Record: Output Contract

**File:** `05-multi-devils.md`

**Required sections:**
1. Debate Structure (overview of 3 rounds)
2. Round 1 Summary: Devils Advocate (FOR)
3. Round 2 Summary: Anti-Devils (AGAINST)
4. Round 3 Summary: Synthesis
5. Integrated Findings (common ground + tensions)
6. Refined Belief (synthesis statement)
7. Proposed Hybrid Model
8. Critical Empirical Tests
9. Decision Tree/Framework
10. Areas of Genuine Disagreement
11. Areas of False Disagreement
12. Recommended Next Actions (phased)
13. Final Confidence Assessment
14. Metadata

---

## Quality Checks

**Turn 1 (FOR):**
- [ ] 5-7 strong arguments presented
- [ ] 3-5 critiques preemptively addressed
- [ ] Axioms clearly stated
- [ ] Confidence higher than balanced (typically 75-85%)

**Turn 2 (AGAINST):**
- [ ] 5-7 strong counter-arguments presented
- [ ] FOR arguments directly challenged
- [ ] Alternative axioms presented
- [ ] Confidence reflects skepticism (typically 65-75%)

**Turn 3 (Synthesis):**
- [ ] Common ground identified (4-5 points)
- [ ] Genuine tensions mapped (3-5)
- [ ] Boundary conditions specified
- [ ] Hybrid model practical
- [ ] Empirical tests proposed (3-5)
- [ ] Confidence calibrated down from FOR (typically 55-70%)

**Complete Record:**
- [ ] All 3 rounds summarized
- [ ] Trajectory clear (confidence evolution)
- [ ] Decision framework actionable
- [ ] Recommendations phased and specific

---

## Example from Live Execution

**Round 1: Devils Advocate (FOR)**
- Position: Framework cataloging = cognitive infrastructure
- Key arguments: Medical DSS work, AI breakthrough enables it, network effects compound
- Confidence: 80%
- Axiom: Cognitive pragmatism (outcomes matter, not theory)

**Round 2: Anti-Devils (AGAINST)**
- Position: Framework cataloging commits reification fallacy
- Key arguments: Analogies fail, embodiment matters, transfer research negative, AI lacks understanding
- Confidence: 70%
- Axiom: Enactivism (mind = embodied action)

**Round 3: Synthesis**
- Integrated position: "Bounded Pragmatism"
- Works when: Bounded domains, novice-competent learners, integrated practice, measurable outcomes
- Fails when: Unbounded domains, expert level, no feedback, passive exposure
- Confidence: 60-65% (down from 70% original)
- Key insight: Context determines success, not universal applicability

**Decision framework:**
5 questions scoring when frameworks work:
1. Bounded domain? 2. Novice-competent stage? 3. Practice integrated? 4. Outcomes measurable? 5. Human mentorship available?

**Result:** Nuanced, actionable position that acknowledges both strengths and limitations. Confidence calibrated based on empirical evidence needs.
