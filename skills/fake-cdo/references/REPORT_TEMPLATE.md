# Report Template

Use this template for `MODES_OF_REASONING_REPORT_AND_ANALYSIS_OF_PROJECT.md`.

---

```markdown
# Modes of Reasoning: Project Analysis Report

**Project:** [PROJECT_NAME]
**Date:** [DATE]
**Modes Used:** [N] of 80 available
**Agents:** [N_CC] Claude Code + [N_COD] Codex
**Lead Agent:** [YOUR_IDENTITY]

---

## 1. Executive Summary

[1 page max. What did this multi-perspective analysis reveal? What are the 3-5 most important findings? What is the overall health/quality assessment?]

### Key Takeaways
1. [Most important finding]
2. [Second most important]
3. [Third most important]

### Overall Confidence: [0.0-1.0]
[Brief justification for the aggregate confidence score]

---

## 2. Methodology

### Why These 10 Modes?

| # | Mode | Code | Category | Selection Rationale |
|---|------|------|----------|-------------------|
| 1 | [Mode Name] | [Code] | [Category] | [Why this mode was chosen for this project] |
| 2 | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |
| 10 | ... | ... | ... | ... |

### Category Coverage

| Category | Modes Selected | Coverage |
|----------|---------------|----------|
| A: Formal | [count] | [which modes] |
| B: Ampliative | [count] | [which modes] |
| ... | ... | ... |

### Modes Considered But Not Selected
- [Mode]: [why it was excluded]
- ...

---

## 3. Convergent Findings (High Confidence)

These findings were independently reached by multiple reasoning modes. Convergence across
diverse analytical perspectives is the strongest signal this analysis produces.

### Finding C1: [Title]
**Supporting modes:** [Mode1], [Mode2], [Mode3]
**Confidence:** [0.0-1.0]

[Detailed description of the finding]

**Evidence from each mode:**
- **[Mode1]:** [What this mode found and how]
- **[Mode2]:** [What this mode found and how]
- **[Mode3]:** [What this mode found and how]

**Why convergence matters here:** [Why independent discovery strengthens this finding]

**Evidence methodology diversity:** [Did the supporting modes use different search/analysis methodologies, or did they all use the same approach? If same methodology, note: "methodological convergence — confidence may be inflated"]
**Known vs Novel:** [Is this finding genuinely novel, or does it restate something already documented in README/AGENTS.md?]

**Recommended action:** [What to do about it]

### Finding C2: [Title]
[Same structure]

...

---

## 4. Divergent Findings (Points of Disagreement)

These are areas where different reasoning modes reached different or contradictory conclusions.
Disagreements are NOT failures -- they reveal genuine tensions, tradeoffs, or areas where
the answer depends on which values or assumptions you prioritize.

### Disagreement D1: [Title]

**Position A:** [Mode(s)] argue that [position]
- Evidence: [what supports this view]
- Reasoning: [the logical chain]

**Position B:** [Mode(s)] argue that [position]
- Evidence: [what supports this view]
- Reasoning: [the logical chain]

**Analysis of the disagreement:**
[Why these modes disagree. Is it different values, different evidence, different assumptions, or different analytical frameworks? Can the disagreement be resolved, or is it a genuine tradeoff?]

**Lead agent assessment:**
[Your synthesis: which position is stronger, or is this a legitimate tradeoff that the project owner should weigh?]

### Disagreement D2: [Title]
[Same structure]

...

---

## 5. Unique Insights by Mode

Findings that only ONE mode surfaced. These are the distinctive contributions of each
analytical perspective -- the things that would be missed without epistemological diversity.

### [Mode Name] ([Code]) -- Unique Contributions
- **[Insight]:** [Description and why only this mode caught it]
- ...

### [Mode Name] ([Code]) -- Unique Contributions
- ...

[Repeat for each mode that produced genuinely unique findings]

---

## 6. Risk Assessment

Aggregated risks from all modes, ranked by combined severity and agreement level.

| # | Risk | Severity | Likelihood | Modes Flagging | Confidence |
|---|------|----------|------------|---------------|------------|
| 1 | [Risk description] | Critical/High/Med/Low | High/Med/Low | [Mode1, Mode2, ...] | [0.0-1.0] |
| 2 | ... | ... | ... | ... | ... |

### Critical Risks (require immediate attention)
[Detail on any critical-severity risks]

### Strategic Risks (long-term concerns)
[Detail on risks that compound over time]

---

## 7. Recommendations

Prioritized by impact, confidence, and number of supporting modes.

| Priority | Recommendation | Supporting Modes | Effort | Impact |
|----------|---------------|-----------------|--------|--------|
| 1 | [Recommendation] | [Mode1, Mode2, ...] | Low/Med/High | High/Med/Low |
| 2 | ... | ... | ... | ... |

### Top 5 Recommendations (Detailed)

#### Recommendation 1: [Title]
**Supporting modes:** [list]
**Dissenting modes:** [list, if any, with their objection]
**What:** [specific action]
**Why:** [justification from multiple perspectives]
**Expected benefit:** [what improves]
**Effort:** [realistic assessment]
**Risks of NOT doing this:** [what happens if ignored]

**Actionability check:** Given [TEAM_SIZE] developers, [USER_COUNT] users, [DEVELOPMENT_STAGE] — can this be acted on in 30 days? [Yes/No — if No, move to Exploratory Ideas]
**Next-Day Action:** [What specifically would change tomorrow if this recommendation is accepted?]

[Repeat for top 5]

---

## 8. New Ideas and Extensions

Creative proposals aggregated across all modes, deduplicated and assessed.

### High-Potential Ideas

#### Idea 1: [Title]
**Originating mode(s):** [which modes suggested this]
**Description:** [the idea in detail]
**How it connects to project goals:** [alignment]
**Feasibility:** Low/Med/High
**Potential impact:** Low/Med/High
**Cross-mode support:** [do other modes endorse or challenge this idea?]

[Repeat for each high-potential idea]

### Exploratory Ideas (lower confidence, worth investigating)
- [Idea]: [brief description] (from [Mode])
- ...

---

## 9. Open Questions

Questions raised by the analysis that cannot be answered from the project artifacts alone.
These are questions for the project owner or stakeholders.

| # | Question | Raised By | Why It Matters |
|---|----------|-----------|----------------|
| 1 | [Question] | [Mode(s)] | [Why the answer affects the analysis] |
| 2 | ... | ... | ... |

---

## 10. Confidence Matrix

Per-finding confidence with supporting and dissenting modes.

| Finding | Confidence | Supporting Modes | Dissenting Modes | Notes |
|---------|-----------|-----------------|-----------------|-------|
| [Finding title] | [0.0-1.0] | [list] | [list] | [calibration notes] |
| ... | ... | ... | ... | ... |

### Confidence Calibration Notes
[Discussion of where this analysis is most/least reliable and why. Honest uncertainty
assessment is more valuable than false confidence.]

---

## 11. Mode Performance Notes

Assessment of how well each reasoning mode performed on THIS project.

| Mode | Code | Productivity | Unique Value | Applicability | Notes |
|------|------|-------------|-------------|--------------|-------|
| [Mode] | [Code] | High/Med/Low | High/Med/Low | High/Med/Low | [brief note] |
| ... | ... | ... | ... | ... | ... |

### Most Productive Modes
[Which modes found the most and why]

### Least Applicable Modes
[Which modes struggled and why -- useful for future mode selection]

### Mode Selection Retrospective
[If you were to redo this analysis, would you select different modes? Which and why?]

---

## 12. Appendix: Individual Mode Outputs

### A. [Mode Name] ([Code])
**Agent:** [cc/cod pane N]
**Confidence:** [score]
**Thesis:** [one-paragraph thesis from the mode's output]
**Key findings:** [numbered summary]

[Repeat for each mode, or include full MODE_OUTPUT_*.md contents]

---

## 13. Taxonomy Axis Analysis

For each of the 7 taxonomy axes, summarize what the swarm revealed:

### Ampliative vs Non-Ampliative
[What did the ampliative modes discover that the non-ampliative modes couldn't, and vice versa?]

### Monotonic vs Non-Monotonic
[Were there findings that would be retracted if new information arrived? How fragile are the conclusions?]

### Uncertainty vs Vagueness
[Which project aspects have crisp uncertainty (probability) vs genuinely vague boundaries?]

### Descriptive vs Normative
[Where did the analysis describe facts vs where did it make value judgments? Were values laundered as facts?]

### Belief vs Action
[What should we BELIEVE about this project vs what should we DO about it?]

### Single-Agent vs Multi-Agent
[Where does strategic behavior from other agents (users, competitors, attackers) matter?]

### Truth vs Adoption
[Which findings are correct but hard to act on? Which are actionable but uncertain?]

---

## 14. Assumptions Ledger

Aggregated from all mode outputs. Assumptions the project makes (stated and unstated).

| # | Assumption | Surfaced By | Justified? | Risk if Wrong |
|---|-----------|-------------|-----------|---------------|
| 1 | [Assumption] | [Mode(s)] | Yes/No/Partially | [Consequence] |
| ... | ... | ... | ... | ... |

---

## 15. Contribution Scoreboard

| Mode | Code | Score | Findings | Unique | Evidence Quality | Velocity | Notes |
|------|------|-------|----------|--------|-----------------|----------|-------|
| [Mode] | [Code] | [0-100] | [N] | [N] | [High/Med/Low] | [High/Normal/Low] | [brief] |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Diversity Score:** [0.0-1.0] — [interpretation]

---

## 16. Mode Selection Retrospective

### Would You Choose Different Modes?
[With hindsight, which modes were most/least valuable? Which omitted modes would have added significant value?]

### Axis Coverage Assessment
[Which axes were well-covered? Which had blind spots? How did this affect findings?]

### Recommendations for Future Runs
[Specific mode selection advice for analyzing this type of project again]

---

## 17. Appendix: Provenance Index

| Finding ID | Source Mode(s) | Source §F IDs | Tier | Confidence | Report Section |
|------------|---------------|---------------|------|-----------|----------------|
| §C1 | [Mode1, Mode2, Mode3] | [§F3, §F7, §F2] | KERNEL | [0.88] | [Section ref] |
| §C2 | [Mode1, Mode2] | [§F1, §F4] | SUPPORTED | [0.72] | [Section ref] |
| §D1 | [Mode1 vs Mode2] | [§F5 vs §F8] | DISPUTED | [0.60] | [Section ref] |
| §U1 | [Mode1 only] | [§F9] | HYPOTHESIS | [0.55] | [Section ref] |
| ... | ... | ... | ... | ... | ... |

---

## 18. Appendix: Explanation Layer (for key findings)

### §C1: [Finding Title]
**Type:** finding
**Source modes:** [list with §F references]
**Confidence basis:** [why this level]
**Supporting evidence:** [list]
**Counter-evidence:** [list, if any]
**Conflict resolution:** [method, if applicable]
**Reasoning chain:** [the logical path from evidence to conclusion]

[Repeat for all KERNEL and HIGH-severity findings]
```

---

## Synthesis Guidelines

When compiling this report, follow these principles:

1. **Convergence is signal, not noise.** When 3+ modes independently reach the same conclusion via different reasoning paths, that finding is almost certainly real.

2. **Disagreement is information.** Don't paper over tensions. Analyze WHY modes disagree and present both sides fairly.

3. **Unique insights justify the approach.** If every mode found the same things, the multi-perspective approach didn't add value. Highlight what only ONE mode caught.

4. **Confidence must be calibrated.** A finding with high confidence and low support count is suspicious. A finding with moderate confidence but 6-mode support is very reliable.

5. **Recommendations need cross-mode validation.** A recommendation supported by only one mode is a hypothesis. One supported by 5+ modes across different categories is actionable.

6. **New ideas need feasibility grounding.** Creative suggestions from option-generation or conceptual-blending modes should be reality-checked against practical modes.

7. **Questions are output, not failure.** Questions the analysis raises but cannot answer are valuable deliverables -- they point the project owner to blind spots.

## Concise Report Variant (--concise flag)

When `--concise` is specified, use this compressed 7-section template instead of the full 18-section version. This is the recommended format for solo developers, early-stage projects, or when the full report would be disproportionate to the project's size.

```markdown
# Modes of Reasoning: Project Analysis (Concise)

**Project:** [PROJECT_NAME] | **Date:** [DATE] | **Modes:** [N] | **Agents:** [AGENT_MIX]

---

## 1. Executive Summary
[Same as full report — 1 page max, 3-5 key takeaways, overall confidence]

## 2. Convergent Findings (max 5)
[KERNEL findings only. For each: title, supporting modes, evidence summary, recommended action.
Flag any that are "Confirmed Known Risk" (restating documented limitations) vs genuinely novel.]

## 3. Critical Disagreements (max 3)
[DISPUTED findings only. Both positions, diagnosis of why they disagree, lead agent assessment.]

## 4. Security & Risk Findings
[Aggregated risks calibrated against actual deployment context. Include threat model reference.]

## 5. Top Recommendations (max 5)
[Each must pass the actionability gate: "Could this team act on this in 30 days?"
For each: what, why, effort, supporting modes, and "Next-Day Action" — what specifically changes tomorrow.]

## 6. Open Questions
[Questions the analysis raises that need the project owner's input.]

## 7. Provenance Summary
[Compact table: Finding → Source Modes → Tier → Confidence. No full explanation layer.]
```

### What Gets Dropped in Concise Mode
- Individual mode outputs (appendix) — keep the files, don't inline them
- Contribution scoreboard and mode performance notes
- Taxonomy axis analysis
- Full explanation layer (provenance summary replaces it)
- Mode selection retrospective
- Assumptions ledger (fold critical assumptions into findings)
