# Synthesis Methodology

> How to combine 10 independent mode outputs into a single report with provenance, triangulation, conflict resolution, and contribution scoring.

## The Triangulation Protocol

Adapted from the operationalizing-expertise methodology where 3-model distillation + triangulation produces high-confidence kernels. Applied here to N-mode ensemble reasoning.

### Confidence Tiers

| Tier | Criteria | Label | Report Section |
|------|----------|-------|----------------|
| **KERNEL** | 3+ modes independently reached the same finding via different reasoning paths | High confidence | Convergent Findings |
| **SUPPORTED** | 2 modes agree independently | Moderate confidence | Supported Findings |
| **HYPOTHESIS** | 1 mode only, but with strong evidence | Lower confidence, high uniqueness | Unique Insights by Mode |
| **DISPUTED** | 2+ modes actively disagree | Requires resolution | Divergent Findings |
| **ABSENT** | Expected finding that NO mode produced | Structural blind spot | Blind Spot Analysis |

### What Counts as "Independent Agreement"

True agreement requires:
1. **Same claim** (not just same topic)
2. **Different evidence** (citing different files, patterns, or reasoning chains)
3. **Different analytical framework** (not just two formal modes both finding the same type error)
4. **Different search methodology** (not just multiple modes all grepping for the same imports — if all modes used `grep` to find "zero callers," that is ONE methodology used N times, not N independent confirmations)

**NOT agreement:** Two modes discussing the same topic but drawing different conclusions (that's DISPUTED). Two modes not mentioning something (that's absence, not agreement).

### Triangulation Process

```
FOR each finding §F[N] in any mode output:
  1. Normalize the finding to a canonical claim
  2. Search all OTHER mode outputs for semantically similar findings
  3. If found in 2+ other modes:
     → Mark as KERNEL, record all source modes
     → Boost confidence: confidence = max(individual) * 1.1 (cap at 0.95)
  4. If found in 1 other mode:
     → Mark as SUPPORTED, record both sources
  5. If unique to this mode:
     → Mark as HYPOTHESIS
  6. If contradicted by another mode:
     → Mark as DISPUTED, record both positions

FOR the set of all normalized claims:
  7. Identify claims that SHOULD exist but don't (blind spots)
  8. Check axis coverage: is any axis completely unrepresented?
```

## Conflict Resolution Framework

When modes disagree, diagnosis must precede resolution. The conflict resolution method is recorded in the explanation layer.

### Diagnosis: Why Do They Disagree?

| Diagnosis | How to Detect | Example |
|-----------|--------------|---------|
| **Different evidence** | Modes cite different files/docs | One found a code bug, another found a doc error |
| **Different values** | One uses "should" the other uses "is" | Security mode says "insecure," usability mode says "user-friendly" |
| **Different assumptions** | Modes state different premises | One assumes current scale, another assumes 10x |
| **Different level of abstraction** | One is micro, another macro | Code-level finding vs architecture-level finding |
| **Different axes** | Check taxonomy axis positions | Descriptive mode vs normative mode |
| **Analytical error** | Evidence doesn't support the claim | Mode misread the code or hallucinated a dependency |
| **Genuine contradiction** | Same evidence, same level, opposite claims | "This is thread-safe" vs "This has a race condition" |

### Resolution Strategies

| Strategy | When to Use | How |
|----------|------------|-----|
| **Combine** | Different evidence → both are right | Present as complementary findings that together give fuller picture |
| **Contextualize** | Different assumptions | Present conditionally: "If X then A; if Y then B" |
| **Separate** | Different axes or levels | Present as answering different questions (both valid) |
| **Tradeoff** | Different values | Present as genuine tradeoff the project owner must weigh |
| **Majority** | 3+ modes vs 1 mode, no error identified | Side with majority but note dissent with reasoning |
| **Weighted** | Modes have different applicability to this finding | Weight by mode relevance and evidence quality |
| **Adversarial** | Genuine contradiction | Actively investigate yourself; one side is wrong |
| **Defer** | Can't resolve without external info | Present to project owner with both positions and request clarification |

### Conflict Severity Scoring

From NTM's ensemble conflict detection:

```
severity = f(position_count, average_confidence)

LOW:    average_confidence < 0.45
MEDIUM: average_confidence >= 0.45 OR 3+ distinct positions
HIGH:   4+ positions OR average_confidence >= 0.75
```

High-severity conflicts MUST be individually analyzed in the Divergent Findings section.

## Contribution Scoring

Each mode's contribution is measured across multiple dimensions. This prevents the report from being dominated by the most verbose mode.

### Scoring Weights

| Metric | Weight | What It Measures |
|--------|--------|-----------------|
| Findings produced | 0.40 | Raw analytical output |
| Unique insights | 0.30 | Things ONLY this mode found |
| Evidence quality | 0.20 | Proportion of findings with specific references |
| Calibration quality | 0.10 | Does confidence match evidence strength? |

### Score Calculation

```
For each mode M:
  findings_score = (M.findings_count / total_findings_all_modes)
  unique_score   = (M.unique_insights / total_unique_all_modes)
  evidence_score = (M.findings_with_refs / M.total_findings)
  calibration_score = assess_calibration(M.stated_confidence, M.evidence_quality)

  contribution = 0.40 * findings_score
               + 0.30 * unique_score
               + 0.20 * evidence_score
               + 0.10 * calibration_score

  // Penalty for findings that cite other modes' evidence without independent verification
  dependency_penalty = 0.15 * (findings_citing_other_modes / M.total_findings)
  
  adjusted_contribution = contribution - dependency_penalty
  normalized_score = adjusted_contribution * 100  // 0-100 scale
```

### Diversity Score

Measures whether contributions are evenly distributed or dominated by one mode:

```
diversity = 1.0 / (1.0 + coefficient_of_variation²)
```

- Diversity near 1.0 → modes contributed evenly (good)
- Diversity near 0.0 → one mode dominated (investigate why)

### Velocity Tracking

From NTM's ensemble velocity system:

```
velocity = unique_findings / tokens_estimated * 1000
```

Label:
- HIGH: velocity > average (efficient mode for this project)
- NORMAL: velocity near average
- LOW: velocity < 1.0 (mode was inefficient -- may indicate poor fit)

Report velocity in Mode Performance Notes to inform future mode selection.

## Provenance Tracking

Every finding in the final report must be traceable back to its source.

### Finding ID Scheme

```
§F[N] — finding ID assigned by the originating mode agent
§C[N] — convergent finding ID in the synthesis (may combine multiple §F IDs)
§D[N] — disputed finding ID
§R[N] — recommendation ID
§I[N] — idea/innovation ID
```

### Provenance Chain

For each finding in the report:

```
§C1 ← discovered by [Systems-Thinking §F3, Root-Cause §F7, Adversarial §F2]
     ← deduplicated: Systems-Thinking §F3 and Root-Cause §F7 merged (Jaccard 0.82)
     ← cited in: Section 4 (Convergent Findings), Section 8 (Recommendations §R2)
     ← conflict: none
     ← confidence: 0.88 (3-mode convergence, strong evidence)
```

### Provenance Index

The report appendix contains a complete index:

```
| Finding ID | Source Mode(s) | Source §F IDs | Tier | Confidence | Report Section |
|------------|---------------|---------------|------|-----------|----------------|
| §C1 | F7, F5, H2 | §F3, §F7, §F2 | KERNEL | 0.88 | 4.1 |
| §C2 | A1, A8 | §F1, §F4 | SUPPORTED | 0.72 | 5.2 |
| §D1 | F7 vs H2 | §F5 vs §F8 | DISPUTED | 0.60 | 6.1 |
| §U1 | B5 only | §F9 | HYPOTHESIS | 0.55 | 7.3 |
```

## Explanation Layer

For every conclusion in the report, the explanation layer documents the reasoning chain. This makes the synthesis auditable and debuggable.

### Per-Conclusion Explanation

```markdown
### Conclusion §C[N]: [Title]

**Type:** finding / risk / recommendation
**Source modes:** [Mode1 (§F[N]), Mode2 (§F[M]), ...]
**Confidence:** [score] — Basis: [why this level]
**Supporting evidence:**
- [Evidence 1 from mode output]
- [Evidence 2 from mode output]

**Counter-evidence:**
- [Any evidence against this conclusion]

**Conflict resolution:** [method used, if applicable]
**Confidence impact of resolution:** [how resolution affected confidence]

**Reasoning:**
[The logical chain from evidence to conclusion]
```

### Conflict Resolution Documentation

```markdown
### Conflict §D[N]: [Topic]

**Positions:**
- Position A ([Mode1, Mode2]): [claim] — Evidence: [refs] — Reasoning: [logic]
- Position B ([Mode3]): [claim] — Evidence: [refs] — Reasoning: [logic]

**Diagnosis:** [Why they disagree — which category from the table above]
**Resolution method:** [combine / contextualize / separate / tradeoff / majority / weighted / adversarial / defer]
**Resolution:** [What was decided]
**Confidence impact:** [How this affected the overall confidence]
**Lead agent note:** [Your assessment of this disagreement]
```

## Synthesis Quality Checks

Before finalizing the report, verify:

- [ ] Every convergent finding has 3+ independent source modes
- [ ] Every disputed finding has explicit diagnosis and resolution
- [ ] Every unique insight is flagged as HYPOTHESIS (not presented as proven)
- [ ] Provenance chain is complete for every finding in the report
- [ ] Contribution scores are computed and reported
- [ ] At least one antagonistic pair produced a productive tension
- [ ] No axis is completely unrepresented (or the gap is noted)
- [ ] Confidence scores vary (not all 0.7) and have calibration justifications
- [ ] The report separates descriptive from normative claims
- [ ] Recommendations cite specific supporting findings

## Intra-Mode Contradiction Detection

Before including a mode's findings in synthesis, check whether the mode's own recommendations are internally consistent. In one deployment, a Bayesian agent simultaneously recommended "increase warmup to 50+ commits" (more conservative) and "use dual-rate EMA for faster phase-change detection" (more responsive). These are in tension and the report didn't flag it.

For each mode output:
1. List all recommendations
2. Check: do any recommendations pull in opposite directions?
3. If yes, flag the contradiction and either resolve it or present both with the tension noted

## Novel vs Restated-Known Distinction

During synthesis, classify each finding as:
- **NOVEL:** Not documented anywhere in README, AGENTS.md, issue trackers, or inline comments
- **CONFIRMED-KNOWN:** Restates something the project owner already documented
- **ELABORATED-KNOWN:** Adds new detail or evidence to a known limitation

The contribution scoreboard should weight NOVEL findings 3x higher than CONFIRMED-KNOWN. An insight the developer doesn't know is worth far more than restating a documented limitation.

## Model Diversity Discount

When all agents run on the same underlying model (e.g., all Claude, all GPT), same-model agreement is weaker evidence than cross-model agreement. Apply a discount:

- **Cross-model convergence** (Claude + Codex + Gemini agree): Full KERNEL confidence
- **Same-model convergence** (3 Claude agents agree): Discount confidence by 0.85x

The report should note when all agents are the same model: "All agents used [model]. True triangulation requires model diversity. Same-model agreement may reflect shared training biases rather than independent confirmation."

## Actionability Gate

Before including any recommendation in the final report's main section:
1. State the project's team size, development stage, and user count (from Phase 0 deployment context)
2. Ask: "Could this be acted on in the next 30 days by this team?"
3. If NO → move to an "Exploratory / Future" appendix, not the main recommendations

This prevents reports full of theoretically-correct but practically-impossible recommendations for solo developers or early-stage projects.
