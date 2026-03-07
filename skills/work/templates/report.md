---
type: report
created: YYYY-MM-DDTHH:MM:SS
updated: YYYY-MM-DDTHH:MM:SS
status: draft | in_progress | complete
scope: codebase | research | audit | analysis | scan
confidence: 0.0-1.0
agent: agent-name
session_id: session-uuid
tags: [tag1, tag2, tag3]
related_tasks: [task-id-1, task-id-2]
related_docs: [path/to/doc1.md, path/to/doc2.md]
---

# Report Title

## How To Fill This Out

Use this template for research findings, audits, scans, and analysis. Reports capture what you learned and what should happen next. They are evidence artifacts, not plans.

Use uncertainty markers when needed:
- `[tbd]`
- `[unknown]`
- `[theory]`
- `[maybe: ..., confidence: ##%]`

Good:
- "This report summarizes findings with evidence and next actions."
- "This report clearly separates facts from theory."

Bad:
- "This is an implementation plan disguised as a report."
- "This claims certainty without evidence."

<!--
PURPOSE: Frontmatter fields for indexing, filtering, and cross-referencing reports across sessions
PROCESS: Fill in all fields before marking status beyond "draft". Update `updated` timestamp on every edit.
GOOD: scope: audit, confidence: 0.85, tags: [nats, daemon-wiring, p0]
BAD: scope: stuff, confidence: 1.0, tags: [misc]
-->

**Generated:** YYYY-MM-DD HH:MM TZ
**Agent:** agent-name
**Scope:** Brief scope description

---

## Executive Summary

<!--
PURPOSE: Give a decision-maker everything they need in 30 seconds — what, so what, now what
PROCESS: Write LAST, after all findings are complete. Distill to 3-5 sentences max. Lead with the most critical finding.
GOOD: "Audit of 8 NATS streams found 3 dead (NLU, TTS, LOGS) consuming resources with zero subscribers. Recommend immediate teardown — estimated 15% memory recovery on Thor."
BAD: "We looked at a lot of things and found some issues that might need attention at some point."
-->

High-level overview of findings. Keep to 3-5 sentences covering:
- What was analyzed/scanned
- Key findings summary
- Critical issues (if any)
- Recommended next actions

### Quick Stats

<!--
PURPOSE: Quantitative snapshot — lets readers gauge scale and confidence at a glance
PROCESS: Fill after analysis. Every number must trace back to evidence in Section 2.
GOOD: Items Scanned: 33 daemon tests | Issues Found: 6 (2 P0, 4 P2) | Confidence: 0.9
BAD: Items Scanned: some | Issues Found: a few | Confidence: high
-->

| Metric | Value | Notes |
|--------|-------|-------|
| Items Scanned | N | Description |
| Issues Found | N | Severity breakdown |
| Confidence | 0.0-1.0 | Confidence in findings |

---

## 1. Findings

### 1.1 Category A

<!--
PURPOSE: One discrete finding with full evidence chain — assessment, proof, and actionable next steps
PROCESS: (1) State the finding clearly in Assessment. (2) Paste concrete evidence — code, logs, metrics. (3) List specific next actions as checkboxes. Each finding should be independently actionable.
GOOD: "Status: FAILING | Location: modules/transcription/config.py:92-99 | Assessment: ValidationConfig defined but never injected into any daemon constructor. Evidence: grep -r 'ValidationConfig' shows zero imports outside config.py."
BAD: "Status: Needs review | Location: somewhere in modules/ | Assessment: Config might not be wired up. Evidence: (none provided)"
-->

**Status:** Status indicator
**Relevance:** Priority/severity
**Location:** File path or system location

**Assessment:**
- Key finding point 1
- Key finding point 2
- Key finding point 3

**Evidence:**
```
Code snippets, logs, or data supporting findings
```

**Next Actions:**
- [ ] Action item 1
- [ ] Action item 2
- [ ] Action item 3

---

### 1.2 Category B

<!--
PURPOSE: Additional finding with cross-references to related work — shows how this finding connects to the broader system
PROCESS: Same as 1.1 for the finding itself. Add cross-references to any doc, task, or epic this finding touches. If it blocks something, say so explicitly.
GOOD: "Cross-References: Related to docs/architecture/00-actual-architecture.md (pipes-and-filters pattern) | Blocks: bd-uav-jo0u (hex adapter wiring)"
BAD: "Cross-References: see other docs"
-->

**Status:** Status indicator
**Relevance:** Priority/severity
**Location:** File path or system location

**Assessment:**
- Key finding point 1
- Key finding point 2

**Cross-References:**
- Related to: path/to/related/doc.md
- Implements: path/to/design/doc.md
- Blocks: task-id or epic-id

---

## 2. Detailed Analysis

### 2.1 Area of Investigation

<!--
PURPOSE: Deep-dive that backs up the findings — this is where the proof lives
PROCESS: (1) Describe what you investigated and why. (2) Show quantitative data first (metrics, counts, benchmarks). (3) Then show qualitative evidence (code snippets, log excerpts). Every claim in Section 1 must have supporting data here.
GOOD: "Ran `pytest modules/daemon/ -v --tb=short` — 33 pass, 0 fail. But coverage report shows 0% on asr_daemon.py, intent_daemon.py, response_daemon.py. All 33 tests hit infrastructure code only."
BAD: "The code looks like it works but we're not sure about coverage."
-->

Detailed analysis with supporting data, metrics, code examples.

**Data/Metrics:**
```
Quantitative data, measurements, benchmarks
```

**Code Examples:**
```typescript
// Code snippets demonstrating findings
```

---

## 3. Recommendations

<!--
PURPOSE: Prioritized, actionable recommendations — what to do, in what order, and why
PROCESS: (1) Immediate = do today, blocks other work. (2) Short-term = this week, high value. (3) Long-term = this month, strategic. Every recommendation must trace to a finding in Section 1. Include effort estimates.
GOOD: "Wire hex adapters (P0, S effort, High impact) — unblocks all daemon unit testing, ~300 LOC change"
BAD: "Fix things (High priority, unknown effort, probably important)"
-->

### 3.1 Immediate Actions
| Action | Priority | Effort | Impact |
|--------|----------|--------|--------|
| Action 1 | P0/P1/P2 | S/M/L | High/Med/Low |
| Action 2 | P0/P1/P2 | S/M/L | High/Med/Low |

### 3.2 Short-term Actions (This Week)
1. Action with rationale
2. Action with rationale

### 3.3 Long-term Actions (This Month)
1. Action with rationale
2. Action with rationale

---

## 4. Validation Checklist

<!--
PURPOSE: Self-review gate — ensures the report meets quality standards before sharing
PROCESS: Check every box before marking report status as "complete". If a box can't be checked, add a note explaining why. This is your quality gate — treat it seriously.
GOOD: All boxes checked, or unchecked boxes have explicit "[SKIP: no code examples in this report]" annotations
BAD: Boxes left unchecked with no explanation, or all boxes checked without actually verifying
-->

### Report Quality
- [ ] All findings have supporting evidence
- [ ] Recommendations are actionable and specific
- [ ] Priority/severity consistently applied
- [ ] Cross-references accurate and up-to-date
- [ ] Confidence level justified

### Technical Validation
- [ ] Code examples tested/verified
- [ ] File paths validated
- [ ] Metrics/data accurate
- [ ] Dependencies identified
- [ ] Blockers documented

### Integration
- [ ] Related tasks linked
- [ ] BD issues created (if needed)
- [ ] Handoff docs updated (if needed)
- [ ] Team notified of critical findings

---

## 5. References

<!--
PURPOSE: Traceable source chain — every claim should be verifiable from these links
PROCESS: Add references as you write, not after. Each reference needs a brief "why referenced" note so future readers know its relevance without clicking through.
GOOD: "[Architecture Reality Doc](docs/architecture/00-actual-architecture.md) - Confirms pipes-and-filters pattern used in daemon assessment"
BAD: "[some doc](doc.md)" or bare URLs with no context
-->

### Source Documents
- [Document Title](path/to/doc.md) - Why referenced
- [Design Doc](path/to/design.md) - Relationship

### Related Work
- Task ID: Brief description
- Epic ID: Brief description

### External References
- [External Resource](URL) - Why relevant

---

## Audit Trail

<!--
PURPOSE: Change log for accountability — who touched what and when
PROCESS: Append a row every time the report is created, updated, or reviewed. Never delete rows. Use ISO timestamps.
GOOD: "2026-03-05 14:30 | Updated | Section 2 — added coverage data | claude-opus"
BAD: "today | changed stuff | me"
-->

| Timestamp | Action | File/Entity | Agent |
|-----------|--------|-------------|-------|
| YYYY-MM-DD | Created | report.md | agent-name |
| YYYY-MM-DD | Updated | Section 2 | agent-name |

---

## Appendix

### A. Raw Data

<!--
PURPOSE: Full unprocessed output that backs the analysis — enables independent verification
PROCESS: Paste complete command output, test results, or log dumps. Do NOT cherry-pick lines. If output exceeds 200 lines, truncate with "[truncated — full output at path/to/file]".
GOOD: Full `pytest -v` output with pass/fail counts, or complete `grep -rn` results
BAD: Hand-edited excerpts that omit inconvenient failures, or "see terminal output" with no actual data
-->

```
Raw data, logs, full output that supports findings
```

### B. Methodology

<!--
PURPOSE: Reproducibility — another agent or human should be able to re-run your analysis and get the same results
PROCESS: List every tool, command, and parameter used. State scope boundaries (what was included/excluded and why). Document assumptions that could invalidate findings if wrong.
GOOD: "Tools: pytest 8.1, grep, ast analysis. Scope: modules/ and poc/ directories. Excluded: vendor/ (third-party). Assumption: test fixtures in conftest.py are representative of production config."
BAD: "Used standard tools to look at the code."
-->

Describe approach used for analysis/scan:
- Tools used
- Parameters/configuration
- Scope/limitations
- Assumptions made

---

## Next Steps in Workflow

<!--
PURPOSE: Route the reader to the correct next action based on report outcomes
PROCESS: Select the most relevant workflow option based on findings severity. If P0 issues exist, escalation should be option 1.
GOOD: Choosing "Escalate" as first option when report contains P0 findings with active data loss risk
BAD: Always defaulting to "Archive findings" regardless of severity
-->

**This report is at the "captured" stage.** Here's what typically comes next:

1. **Design a solution** -> `work "design {solution} based on report"` -> generates proposal.md
2. **Do more research** -> `work "research {specific topic}"` -> generates additional report.md
3. **Create implementation plan** -> `work "plan implementation of {solution}"` -> generates `plan-{kind}-{slug}.md`
4. **Archive findings** -> If no action needed, document rationale and archive
5. **Escalate** -> If critical, create BD epic: `bd create --type=epic --title="{title}"`

**Lifecycle position:** ephemeral -> **captured** -> crystallizing -> crystallized -> manifesting -> completed

---

*Generated by {agent-name} via work skill (captured stage)*
