---
name: synthesize-apply
description: This skill should be used after completing deep analysis across multiple perspectives to move from understanding to action. It helps agents integrate findings using the Cynefin framework to classify problem complexity, generate 5-7 concrete applications with realistic timelines, and prioritize a research agenda—transforming analysis into executable strategy.
---

# synthesize-apply

**Framework used:** Cynefin Framework

**Purpose:** Integrate all previous findings (axioms, emotions, debate) into coherent synthesis, classify problem complexity, and generate concrete applications with timeline.

**When to use:**
- After multi-devils debate synthesis
- Before reflection loop
- Need to move from analysis to action
- Want to classify problem type for appropriate response

---

## Input Contract

**Required:**
- `00-input.md` through `05c-synthesis.md` - All previous analysis files

**Minimum required:**
- `03-dig-axioms.md` - Root axioms
- `05c-synthesis.md` - Integrated position from debate

**Format:**
```markdown
## Integrated Position: [Name]

[Synthesis statement]

### Key Qualifications
[Boundary conditions]
```

---

## Execution Steps

### Step 1: Read All Artifacts
Systematically read all previous files:
- 00-input.md (original belief)
- 01-paraphrase.md (variations)
- 02-steelman.md (enhanced belief)
- 03-dig-axioms.md (axiom hierarchy)
- 04-map-elements.md (emotional/tribal landscape)
- 05a-devils-advocate.md (FOR position)
- 05b-anti-devils.md (AGAINST position)
- 05c-synthesis.md (integrated position)

### Step 2: Extract Integrated Findings

**Root Discovery:**
- What root axiom was found?
- How does it support/undermine belief?

**Confidence Evolution:**
- Track: Original → Steelman → FOR → AGAINST → Synthesis
- Note trend (increasing/decreasing/stable)

**Key Insight:**
- What's the core realization from synthesis?
- Single sentence summary

### Step 3: Classify Problem with Cynefin

Assess which Cynefin domain:

**Clear (Simple):**
- Best practice applies
- Cause-effect obvious
- Sense → Categorize → Respond

**Complicated:**
- Expert analysis needed
- Cause-effect discoverable
- Sense → Analyze → Respond

**Complex:**
- Emergent patterns
- Cause-effect retrospective only
- Probe → Sense → Respond

**Chaotic:**
- No patterns
- Cause-effect unclear
- Act → Sense → Respond

**Rationale:**
- Why this classification?
- What evidence supports it?
- What does this mean for approach?

**Implication:**
- How should we respond given this classification?
- What methods fit this domain?

### Step 4: Generate Applications (5-7 practical applications)

For each application:
- **Clear title** describing what to do
- **Timeline** (Next 3 months / Architecture decision / Product feature / etc.)
- **Description** (2-4 bullet points explaining the application)
- Why this follows from the analysis

**Application categories:**
1. Immediate MVP/pilot (0-3 months)
2. Architecture/design decisions
3. Product features to build
4. Community/social components
5. Market/domain segmentation
6. Quality assurance / monitoring
7. Additional domain-specific applications

### Step 5: Create Research Agenda (3-5 priorities)

For each research priority:
- **Clear question** to investigate
- **Timeline** estimate
- **Why this matters** for validating/refining belief

**Priority ordering:**
1. Most critical for validation
2. Medium-term investigations
3. Long-term studies

### Step 6: Write Integrated Findings Section
Synthesize:
- Root discovery (1-2 sentences)
- Confidence evolution (trajectory)
- Key insight (synthesis core finding)

---

## Output Contract

**File:** `06-synthesize.md`

**Required sections:**
1. Integrated Findings (root discovery, confidence evolution, key insight)
2. Cynefin Classification (domain, rationale, implication)
3. Applications (5-7 practical applications with timelines)
4. Research Agenda (3-5 priorities with timelines)
5. Metadata

**Template:**
```markdown
# Synthesize & Apply Output

**Analysis ID:** axiom-<YYYYMMDD-HHMMSS>
**Timestamp:** <ISO timestamp>
**Inputs:** All previous files (00 through 05)
**Next step:** 07-reflection.md
**Framework used:** Cynefin

---

## Integrated Findings

### Root Discovery
**[Root axiom name]** ([brief description]) → enables [intermediate] → enables [surface belief].

### Confidence Evolution
[Original]% (start) → [Steelman]% (enhanced) → [FOR]% (optimistic) → [AGAINST]% (skeptical) → **[Synthesis]% (realistic)**

### Key Insight
**[Core realization from synthesis]:** [1-2 sentence explanation]

---

## Cynefin Classification

**Domain:** **[CLEAR/COMPLICATED/COMPLEX/CHAOTIC]** ([not X, Y, or Z])

**Rationale:**
- [Evidence point 1]
- [Evidence point 2]
- [Evidence point 3]
- [Evidence point 4]

**Implication:** [How to approach given this classification]

---

## Applications

### 1. **[Application Name]** ([Timeline])
- [Description point 1]
- [Description point 2]
- [Description point 3]
- [Why this follows from analysis]

---

[Repeat for 5-7 applications]

---

## Research Agenda

**Priority 1:** [Research question] ([Timeline])
**Priority 2:** [Research question] ([Timeline])
**Priority 3:** [Research question] ([Timeline])
[Optional Priority 4-5]

---

## Metadata

- Cynefin domain: [domain]
- Applications generated: [count]
- Timeline: [shortest] - [longest]
- Ready for reflection: Yes
```

---

## Quality Checks

Before completing:
- [ ] All previous files read and integrated
- [ ] Root discovery clearly stated
- [ ] Confidence trajectory documented
- [ ] Cynefin classification justified
- [ ] 5-7 applications generated
- [ ] Applications have clear timelines
- [ ] Applications follow from analysis (not arbitrary)
- [ ] 3-5 research priorities identified
- [ ] Research agenda addresses critical gaps

---

## Example from Live Execution

**Integrated Findings:**
- Root: Functionalism (mental states = functional role, substrate-independent)
- Confidence: 70% → 80% → 70% → 60-65%
- Key Insight: "Bounded Pragmatism"—works in specific contexts, not universally

**Cynefin Classification:**
- Domain: COMPLEX (not Complicated, Clear, or Chaotic)
- Rationale: No linear cause-effect, emergent properties, context-dependent, requires probe-sense-respond
- Implication: Can't engineer solution, must experiment and adapt

**Applications (6 generated):**
1. **Build Scoped MVP** (Next 3 months) - ONE bounded domain, 50-user pilot, measure outcomes
2. **Design for Scaffold Fading** (Architecture decision) - Track user independence, reduce suggestions
3. **Add Practice Layer** (Product feature) - Don't just suggest, provide exercises and case studies
4. **Community Integration** (Hybrid model) - AI for retrieval, humans for mentoring
5. **Domain Segmentation** (Market strategy) - Target management/software, avoid philosophy/art
6. **Goodhart Monitoring** (Quality assurance) - Measure outcomes not process

**Research Agenda (4 priorities):**
1. Transfer experiment (3-6 months)
2. Expertise stage interaction (6-12 months)
3. AI vs human scaffolding (6-12 months)
4. Domain boundary test (12 months)

**Result:** Clear action plan with 3-18 month timeline, grounded in Cynefin's "Complex" classification requiring probe-sense-respond approach.
