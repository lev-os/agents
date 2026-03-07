# Skills Index

Reusable atomic patterns for axiom exploration. Each skill is standalone and can be composed into commands/workflows.

**Status:** ✅ All skills fully codified from live execution (2025-01-29)

Each skill file now includes:
- Complete input/output contracts
- Step-by-step execution instructions
- Output templates with required sections
- Quality checks for verification
- Examples from working implementation
- Anti-patterns to avoid

---

## Core Sequential Skills (7 skills)

### 1. paraphrase-engineer.md ✅
**What it does:** Generate 5 variations of belief statement, each exposing different axiom implications (Knowledge Transfer, Tool Augmentation, Pattern Recognition, Cultural Transmission, Capability Emergence). Select best variation for analysis.

**When to use:**
- Starting any exploration to clarify intent
- Multiple interpretations possible
- Need to make implicit assumptions explicit
- Uncovering hidden assumptions through reframing

**Framework used:** THINK Paradigm

**Documentation:** Complete with 110-line execution template, quality checks, live execution example

---

### 2. steelman-enhance.md ✅
**What it does:** Build strongest charitable version by resolving 2-4 internal contradictions (using ARIZ) and adding 5 empirical correlations (with citations, confidence scores). Identify gaps in evidence.

**When to use:**
- Weak or unclear argument needs strengthening
- Want most robust version before critique
- Need evidence backing for claims
- Grounding abstract ideas in research

**Framework used:** ARIZ (Algorithm for Inventive Problem Solving) + Humean Skepticism

**Documentation:** Complete with 145-line execution template, correlation-grounding technique integrated

---

### 3. dig-axioms.md ✅ (MULTI-TURN)
**What it does:** Socratic questioning ("why?") across 3 turns to drill from surface belief → Level 1 → Level 2 → Root axiom. Each turn uses proactive-guessing (5-8 categorized options). Synthesis creates axiom hierarchy diagram and identifies vulnerabilities.

**When to use:**
- Need to find foundational assumptions
- Exploring "why" behind beliefs
- Testing logical consistency
- Tracing reasoning chains to philosophical bedrock

**Framework used:** ACH (Analysis of Competing Hypotheses)

**Multi-turn structure:** 03a-level1.md → 03b-level2.md → 03c-level3.md → 03-dig-axioms.md (synthesis)

**Documentation:** Complete with detailed multi-turn workflow, proactive-guessing integration, Mermaid hierarchy template

---

### 4. map-elements.md ✅
**What it does:** Map emotional drivers (4-6 emotions with intensity/manifestations), tribal affiliations (4-6 tribes), political spectrum (Haidt's 6 foundations + compass), Big 5 personality profile, ANS quadrant mapping (Polyvagal). Identify bias warnings.

**When to use:**
- Understanding full belief structure
- Exploring emotional/tribal factors
- Identifying bias risks
- Sensitive or politically charged topics

**Framework used:** Polyvagal Theory

**Documentation:** Complete with 364-line execution template, ANS quadrant chart, bias mitigation

---

### 5. multi-devils-debate.md ✅ (MULTI-TURN)
**What it does:** 3-round debate producing separate files: (1) Devils Advocate argues FOR with 5-7 arguments (80% confidence), (2) Anti-Devils argues AGAINST with 5-7 critiques (70% confidence), (3) Synthesis finds common ground + genuine tensions, creates hybrid model, decision framework (60-65% confidence).

**When to use:**
- Preparing for actual debate
- Want to see strongest counter-arguments
- Need multiple perspectives integrated
- Testing position robustness
- Understanding opposition deeply

**Framework used:** Second-Order Thinking

**Multi-turn structure:** 05a-devils-advocate.md → 05b-anti-devils.md → 05c-synthesis.md → 05-multi-devils.md (complete record)

**Documentation:** Complete with detailed 3-round templates, axiom comparison, decision tree creation

---

### 6. synthesize-apply.md ✅
**What it does:** Read all previous files (00-05), extract integrated findings (root discovery, confidence evolution, key insight), classify problem with Cynefin, generate 5-7 practical applications with timelines, create 3-5 priority research agenda.

**When to use:**
- Completing an exploration
- Need actionable outputs
- Want Cynefin classification for response strategy
- Moving from analysis to action

**Framework used:** Cynefin Framework

**Documentation:** Complete with systematic artifact reading, Cynefin classification guide, application generation

---

### 7. reflection-loop.md ✅
**What it does:** OODA Loop reflection on process (what worked/didn't), identify 2-4 key refinements, propose next exploration steps or declare readiness for final synthesis. Meta-insights on process and thinking.

**When to use:**
- After completing exploration
- Process improvement needed
- Want to iterate on findings
- Meta-analysis of own work

**Framework used:** OODA Loop

**Documentation:** Complete with process feedback template, meta-insights structure

---

## Supporting Technique Skills (3 skills)

These are embedded techniques used by core skills, not standalone workflows.

### proactive-guessing.md ✅
**What it does:** Generate 5-8 categorized hypotheses for why someone holds a belief: (1-2) Emotional, (1-2) Tribal, (2-3) Rational, (1-2) Philosophical, (1) Unconceived alternative, (1) Other/blank. Reduces cognitive load, surfaces blind spots.

**When to use:**
- During Socratic questioning (dig-axioms turns)
- User might not have articulated reasons
- Want to surface emotional/tribal drivers
- Discover unconsidered alternatives

**Used by:** dig-axioms (each turn), unconceived-explorer command

**Anti-pattern:** Open-ended "why?" with no menu (high cognitive load, misses alternatives)

**Documentation:** Complete with category requirements, language patterns, cognitive science rationale

---

### ans-quadrant-mapping.md ✅
**What it does:** Map autonomic nervous system state using Polyvagal Theory: Ventral Vagal (safe/social), Sympathetic (mobilization), Dorsal Vagal (shutdown), Fawn (appeasement). Assign percentages, create quadrant chart, identify latent triggers.

**When to use:**
- During emotional/tribal mapping (map-elements)
- Understanding embodied aspects of belief
- Identifying stress responses influencing reasoning
- Predicting threat reactions

**Used by:** map-elements, emotional-tribal-mapper command

**Note:** Presented as correlations for exploration, not definitive diagnosis.

**Documentation:** Complete with Polyvagal theory overview, indicator assessment, visual quadrant template

---

### correlation-grounding.md ✅
**What it does:** Ground abstract claims in 5 empirical research correlations using Humean skepticism. Cite (Author, Year), assess evidence quality (Strong/Moderate/Weak), rate confidence (40-95%), identify weakest link. Avoid causal language.

**When to use:**
- During steelman-enhance
- Converting intuitions to testable hypotheses
- Acknowledging limits of current knowledge
- Avoiding hallucination and overconfidence

**Used by:** steelman-enhance, multiple commands

**Anti-pattern:** Claiming "X causes Y" without caveat (should be "X correlates with Y")

**Documentation:** Complete with Humean epistemology foundation, correlation language patterns, anti-hallucination protocol

---

## Usage Notes

- **Standalone use:** Any skill can be used independently for focused work
- **Composition:** Commands chain skills together for complete workflows
- **Order matters:** Core skills 1-7 are designed as sequential chain but can skip steps
- **Customization:** Mix and match skills for custom workflows
- **Framework references:** Each skill leverages a hidden gem framework (see dependencies)
