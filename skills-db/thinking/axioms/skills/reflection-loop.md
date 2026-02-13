---
name: reflection-loop
description: This skill should be used after deep analytical work (belief analysis, axiom drilling, multi-perspective debate) to assess what the process revealed and whether further iteration is needed. It helps agents identify methodological strengths/gaps, calibrate confidence, and decide between continuing exploration or proceeding to synthesis using the OODA framework.
---

# reflection-loop

**Framework used:** OODA Loop (Observe-Orient-Decide-Act)

**Purpose:** Provide process feedback, identify what worked/didn't work, suggest refinements, and determine if further iteration is needed.

**When to use:**
- After synthesize-apply step
- Before final synthesis
- Improving the exploration process itself
- Learning what to do differently next time

---

## Input Contract

**Required:**
- `06-synthesize.md` - Applications and integrated findings
- Access to all previous files for process assessment

**Format:**
```markdown
## Applications

[List of 5-7 applications]

## Research Agenda

[List of 3-5 priorities]
```

---

## Execution Steps

### Step 1: Observe - What Worked Well (3-5 points)

Review the entire process and identify successes:
- Which skills/frameworks were most valuable?
- What insights emerged that wouldn't have without the process?
- Where did the methodology shine?
- What exceeded expectations?

Document with specificity.

### Step 2: Orient - What Could Improve (3-5 points)

Identify gaps, weaknesses, or missed opportunities:
- What could have been explored more deeply?
- Which frameworks weren't fully applied?
- What assumptions went unquestioned?
- Where could the process be more rigorous?

Be constructive and specific.

### Step 3: Decide - Key Refinements (2-4 refinements)

Based on observations, propose concrete improvements:

**For each refinement:**
- **Key Realization:** What did we learn?
- **Problem with original:** What was insufficient?
- **Refined approach:** What's better?

### Step 4: Act - Next Exploration Steps (2-4 steps)

If further exploration is warranted, suggest:
- Additional questions to investigate
- Frameworks to apply more deeply
- Alternative perspectives to explore
- Experiments to run

If exploration is complete, note readiness for final synthesis.

### Step 5: Meta-Insights on Process

Reflect on the exploration itself:

**On the process:**
- What did this methodology reveal?
- How did the file-based workflow perform?
- Was multi-turn structure valuable?
- Did frameworks add or detract?

**On thinking:**
- What did we learn about how beliefs are structured?
- What patterns emerged about assumptions?
- How did emotions/tribes influence reasoning?
- Did confidence calibrate appropriately?

### Step 6: Identify Iteration Decision

Should we:
- **Continue refining** (more OODA loops)?
- **Proceed to final synthesis** (exploration complete)?
- **Pivot to different approach** (methodology insufficient)?

Document decision with rationale.

---

## Output Contract

**File:** `07-reflection.md`

**Required sections:**
1. Process Feedback (what worked well, what could improve)
2. Refinements (key realizations and refined approaches)
3. Next Exploration Steps (if continuing) OR Readiness (if complete)
4. Meta-Insights (on the process itself, on thinking)
5. Metadata

**Template:**
```markdown
# Reflection Loop Output

**Analysis ID:** axiom-<YYYYMMDD-HHMMSS>
**Timestamp:** <ISO timestamp>
**Previous step:** 06-synthesize.md
**Next step:** FINAL-synthesis.md [or continue iteration]
**Framework used:** OODA Loop

---

## Process Feedback

**What worked well:**
- [Success point 1]
- [Success point 2]
- [Success point 3]
- [Success point 4]

**What could improve:**
- [Improvement area 1]
- [Improvement area 2]
- [Improvement area 3]

---

## Refinements

### Key Realization [1]
**Original [X] was [problem].**
- [What was insufficient]
- [Why it mattered]

**Refined [X] is more [quality]:**
- [What's better]
- [Why this helps]

---

[Repeat for 2-4 refinements]

---

## Next Exploration Steps

[If continuing:]
1. **[Step name]** ([what to investigate])
2. **[Step name]** ([what to investigate])
3. **[Step name]** ([what to investigate])

[If complete:]
- Ready for final synthesis: Yes
- Exploration complete: [Why]

---

## Meta-Insights

**On the process itself:**
- [Insight about methodology 1]
- [Insight about methodology 2]
- [Insight about methodology 3]

**On thinking:**
- [Insight about belief structure 1]
- [Insight about assumptions 2]
- [Insight about confidence calibration 3]

---

## Metadata

- Framework used: OODA Loop
- Iterations: [count] ([could continue or complete])
- Ready for final synthesis: [Yes/No]
```

---

## Quality Checks

Before completing:
- [ ] 3-5 "what worked well" points identified
- [ ] 3-5 "what could improve" points identified
- [ ] 2-4 refinements with clear before/after
- [ ] Next steps specified (continue or complete)
- [ ] Meta-insights on both process and thinking
- [ ] Decision clear on whether to iterate or synthesize

---

## Example from Live Execution

**What worked well:**
- Axiom drilling revealed hidden assumptions (functionalism as root)
- Multi-devils debate surfaced genuine tensions vs false disagreements
- Emotional/tribal mapping showed bias awareness (not blind spots)
- Confidence calibration improved (70% → 60-65% more realistic)

**What could improve:**
- Could have explored more unconceived alternatives
- ANS quadrant mapping was approximate (need rubric)
- THINK Paradigm not fully applied (missing detailed technique)

**Key Realization:**
- Original belief was overconfident and underspecified
- Refined belief is more actionable (specific contexts, measurable criteria, phased validation)

**Next Exploration Steps:**
1. Empirical validation (run pilot study)
2. Deepen embodiment understanding (read Dreyfus, Varela)
3. Explore hybrid models (computational + enactive integration)

**Meta-Insights:**

**On the process:**
- Socratic drilling works (reached root axioms)
- Steelmanning both sides prevented rationalization
- File-based workflow is auditable and resumable
- Multi-turn structure captured complexity

**On thinking:**
- Most beliefs rest on philosophical commitments (functionalism, empiricism, etc.)
- Emotional/tribal factors present but manageable (intellectual honesty wins)
- Confidence should decrease as assumptions are made explicit (not increase)

**Result:** Clear assessment of methodology strengths/gaps, confidence calibrated appropriately, ready for final synthesis.
