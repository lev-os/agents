---
type: proposal
created: YYYY-MM-DDTHH:MM:SS
updated: YYYY-MM-DDTHH:MM:SS
status: draft | proposed | approved | rejected | superseded
complexity_score: 0-12
tier: inline | light | full
confidence: 0.0-1.0
author: agent-name
reviewers: [reviewer1, reviewer2]
tags: [architecture, feature, refactor, etc]
related_tasks: [task-id-1, task-id-2]
supersedes: [old-proposal-id]
superseded_by: null | new-proposal-id
validation_gates:
  dor_complete: false
  prior_art_check: false
  alignment_check: false
  approval_received: false
---

# Proposal: Title

**Created:** YYYY-MM-DD HH:MM TZ
**Author:** agent-name
**Status:** draft | proposed | approved
**Complexity:** Tier (inline/light/full) - Score X/12

---

## Executive Summary

Brief 2-3 sentence overview of what this proposal recommends and why.

**Problem:** One sentence describing the problem being solved
**Solution:** One sentence describing the proposed solution
**Impact:** Who benefits and how

---

## 1. Problem Statement

### 1.1 Current State

Describe the current situation, pain points, limitations.

**Pain Points:**
- Pain point 1 with impact
- Pain point 2 with impact
- Pain point 3 with impact

**Affected Users/Systems:**
- User/system 1: How affected
- User/system 2: How affected

---

### 1.2 Why Now?

Why is this problem urgent/important to solve now?
- Blocker for: X
- Technical debt impact: Y
- User impact: Z

---

## 2. Proposed Solution

### 2.1 High-Level Approach

Describe the solution approach conceptually (not implementation details yet).

**Key Components:**
1. Component 1 - What it does
2. Component 2 - What it does
3. Component 3 - What it does

**Architecture Diagram (if applicable):**
```
[Visual representation or ASCII diagram]
```

---

### 2.2 Design Principles

What principles guide this solution?
- Principle 1: Rationale
- Principle 2: Rationale
- Principle 3: Rationale

**Constraints:**
- Constraint 1: Why it matters
- Constraint 2: Why it matters

---

### 2.3 Integration Points

How does this integrate with existing systems?

| System/Component | Integration Type | Changes Required |
|------------------|------------------|------------------|
| System A | API | New endpoint |
| System B | Event | Subscribe to events |
| System C | Config | Add config values |

---

## 3. Implementation Plan

### 3.1 Phases

**Phase 1: Foundation (Effort: S/M/L)**
- Task 1: Description
- Task 2: Description
- **Deliverable:** What's complete after this phase
- **Validation:** How to verify phase completion

**Phase 2: Integration (Effort: S/M/L)**
- Task 1: Description
- Task 2: Description
- **Deliverable:** What's complete after this phase
- **Validation:** How to verify phase completion

**Phase 3: Polish (Effort: S/M/L)**
- Task 1: Description
- Task 2: Description
- **Deliverable:** What's complete after this phase
- **Validation:** How to verify phase completion

---

### 3.2 Technology Stack

**Required Technologies:**
- Technology A: Version, purpose
- Technology B: Version, purpose

**Stack Rationale:**
Why these technologies over alternatives?
- Choice A vs Alternative: Reasoning
- Choice B vs Alternative: Reasoning

**Stack Risks:**
- Risk 1: Mitigation strategy
- Risk 2: Mitigation strategy

---

### 3.3 File Structure

```
Desired codebase tree after implementation:

path/to/new/
├── component-a.ts    # Purpose/responsibility
├── component-b.ts    # Purpose/responsibility
├── tests/
│   ├── component-a.test.ts
│   └── component-b.test.ts
└── docs/
    └── component-guide.md
```

---

## 4. Graph Patch (Filesystem Changes)

### 4.1 Dependency Graph

**Current State (Lookup):**
```yaml
# skill://lev-find?query={module-name}&scope=codebase  # legacy skill name (backend for lev get)
dependencies:
  reads_from:
    - path/to/module-a.ts
    - path/to/module-b.ts

  writes_to:
    - path/to/output.ts

  imports:
    - skill://skill-name  # Skill dependency
    - flowmind://protocol-name  # FlowMind protocol
```

**Proposed Updates (Patch):**
```yaml
# Graph changes this proposal introduces
add_nodes:
  - id: new-module
    path: path/to/new-module.ts
    type: module
    exports: [functionA, functionB]

add_edges:
  - from: new-module
    to: existing-module
    type: imports

modify_nodes:
  - id: existing-module
    path: path/to/existing.ts
    changes:
      - add_export: newFunction
      - update_interface: IExisting

remove_nodes:
  - id: deprecated-module
    path: path/to/old.ts
    migration: "Use new-module instead"
```

**Skill Dependencies:**
```yaml
# skill:// protocol references
required_skills:
  - skill://lev-find      # Legacy skill name (context backend for lev get)
  - skill://lev-align     # Architecture validation
  - skill://planning      # Plan generation (if approved)

optional_skills:
  - skill://lev-research  # Additional research
  - skill://lev-test      # E2E validation
```

**FlowMind Protocols:**
```yaml
# flowmind:// or lev:// protocol handlers
protocols:
  - lev://get?query=auth&scope=code
  - flowmind://entity-lifecycle?state=crystallizing
  - workshop://intake/github
```

---

## 5. Validation Gates

### 5.1 DoR Validation

**Complexity Score:** X/12 (Effort: X + Confidence: X + Risk: X + Scope: X)

**Required DoR Elements:**
```yaml
DoR:
  entry: path/to/entry/point
  done: observable_completion_state
  validation: command_to_verify_success
  prior_art_check: checked | not_checked
  stack: "Tech A + Tech B + Tech C"
  stack_rationale: "Why this stack"
  confidence: 0.0-1.0
```

**DoR Completion Checklist:**
- [ ] Entry point defined and exists
- [ ] Done state observable and testable
- [ ] Validation command specified and tested
- [ ] Prior art checked (no duplicate work)
- [ ] Technology stack justified
- [ ] Confidence level justified

---

### 4.2 Prior Art Check

**Existing Solutions Evaluated:**
| Solution | Location | Pros | Cons | Decision |
|----------|----------|------|------|----------|
| Solution A | path/to/code | Pro 1, Pro 2 | Con 1 | Rejected: Reason |
| Solution B | path/to/code | Pro 1, Pro 2 | Con 1 | Adopted: Reason |

**Related Work:**
- Epic ID: Relationship (supersedes/complements/depends on)
- Task ID: Relationship
- Proposal ID: Relationship

---

### 4.3 Alignment Check

**North Star Alignment:**
- [ ] Aligns with project vision
- [ ] No architecture drift introduced
- [ ] Follows established patterns
- [ ] Maintains consistency

**Drift Assessment:**
- Drift Type: none | pivot | gap
- If drift: Justification for deviation

---

### 4.4 Approval Gate

**Approvers:**
- [ ] Technical Lead: Name
- [ ] Product/PM: Name
- [ ] Team Lead: Name

**Approval Criteria:**
- [ ] Proposal complete and clear
- [ ] Implementation plan feasible
- [ ] Validation gates defined
- [ ] No unresolved concerns

**Concerns Raised:**
1. Concern: Resolution
2. Concern: Resolution

---

## 5. Alternatives Considered

### 5.1 Alternative A: Title

**Description:** Brief description of alternative approach

**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Decision:** Rejected/Accepted
**Rationale:** Why this decision was made

---

### 5.2 Alternative B: Title

**Description:** Brief description of alternative approach

**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Decision:** Rejected/Accepted
**Rationale:** Why this decision was made

---

## 6. Risk Assessment

### 6.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Risk 1 | High/Med/Low | High/Med/Low | Strategy |
| Risk 2 | High/Med/Low | High/Med/Low | Strategy |

---

### 6.2 Dependencies

**Internal Dependencies:**
- Depends on Epic/Task ID: Why, status
- Blocks Epic/Task ID: Why, status

**External Dependencies:**
- External service/tool: Why, risk if unavailable

---

## 7. Success Metrics

### 7.1 Acceptance Criteria

- [ ] Criterion 1: Specific, measurable outcome
- [ ] Criterion 2: Specific, measurable outcome
- [ ] Criterion 3: Specific, measurable outcome

---

### 7.2 Performance Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Metric 1 | Value | How to measure |
| Metric 2 | Value | How to measure |

---

### 7.3 User Impact Metrics

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| User metric 1 | Current | Goal | Method |
| User metric 2 | Current | Goal | Method |

---

## 8. References

### Research Documents
- [Research Title](path/to/research.md) - Key findings used
- [Analysis Title](path/to/analysis.md) - Data referenced

### Design Documents
- [Design Title](path/to/design.md) - Architecture patterns
- [C4 Diagram](path/to/diagram.md) - System context

### Related Proposals
- [Proposal Title](path/to/proposal.md) - Relationship

### External References
- [External Resource](URL) - Why relevant
- [Documentation](URL) - Specification used

---

## 9. Open Questions

1. **Question 1?**
   - Context: Why this matters
   - Options: A, B, C
   - Decision needed by: Date/milestone

2. **Question 2?**
   - Context: Why this matters
   - Options: A, B, C
   - Decision needed by: Date/milestone

---

## 10. Decision Log

| Date | Decision | Rationale | Approver |
|------|----------|-----------|----------|
| YYYY-MM-DD | Decision text | Why | Name |
| YYYY-MM-DD | Decision text | Why | Name |

---

## 11. Next Steps

### Immediate (Before Approval)
1. Action item 1
2. Action item 2

### After Approval
1. Create BD epic/tasks
2. Schedule implementation phases
3. Set up validation infrastructure

### Follow-up
1. Schedule review checkpoints
2. Document lessons learned

---

## Appendix

### A. Detailed Technical Specs

```typescript
// Code examples, type definitions, interfaces
// that support the proposal
```

### B. Research Data

```
Supporting data, metrics, benchmarks
that informed the proposal
```

### C. Prototype/POC

**Location:** path/to/poc
**Status:** working | needs_fixes | abandoned
**Findings:** Key learnings from POC

---

## 🪄 Next Steps in Workflow

**This proposal is at the "crystallizing" stage.** Here's what typically comes next:

1. **Design validation gates** → Define test strategy, DoR, acceptance criteria
2. **Create implementation plan** → `work "plan implementation of {this proposal}"` → generates plan.md with full DoR
3. **Run spike/POC** → Test technical unknowns: `work "POC for {specific aspect}"`
4. **Get alignment** → Run `lev-align` to check for architecture drift
5. **Refine proposal** → Update based on feedback, more research if needed
6. **Scaffold BD epic** → Once approved: `bd create --type=epic --title="{title}"` with plan.md

**Lifecycle position:** ephemeral → captured → **crystallizing** → crystallized → manifesting → completed

---

*Proposal created via work skill (crystallizing stage)*
