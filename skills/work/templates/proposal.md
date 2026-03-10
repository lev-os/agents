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

## How To Fill This Out

Use this template when proposing a non-trivial solution before spec or execution. A proposal explains the problem, compares options, and recommends a direction. It is broader than a plan and less locked than a spec.

Use uncertainty markers when needed:
- `[tbd]`
- `[unknown]`
- `[theory]`
- `[maybe: ..., confidence: ##%]`

Good:
- "This proposal compares two directions and recommends one."
- "This proposal explains what still needs validation before approval."

Bad:
- "This is already the final spec."
- "This is just a task list."

<!--
PURPOSE: Top-level title that uniquely identifies this proposal at a glance
PROCESS: Write a short, specific title — verb-noun format preferred (e.g., "Migrate X to Y", "Add Z Pipeline")
GOOD: "Proposal: Replace Regex Intent Engine with DeBERTa Classifier"
BAD: "Proposal: Intent Improvements"
-->

**Created:** YYYY-MM-DD HH:MM TZ
**Author:** agent-name
**Status:** draft | proposed | approved
**Complexity:** Tier (inline/light/full) - Score X/12

---

## Executive Summary

<!--
PURPOSE: Give any reader a complete picture in 30 seconds — the entire proposal distilled
PROCESS: Write the Problem/Solution/Impact lines first, then compose the 2-3 sentence overview that connects them
GOOD: "The regex-based emergency detector has a 50% false-positive rate, causing unnecessary escalations. We propose replacing it with a scored strategy pattern using DeBERTa, reducing FP to <5%. This unblocks the session FSM from handling false alarms."
BAD: "We want to improve the system and make things better for users by updating some components."
-->

Brief 2-3 sentence overview of what this proposal recommends and why.

**Problem:** One sentence describing the problem being solved
**Solution:** One sentence describing the proposed solution
**Impact:** Who benefits and how

---

## 1. Problem Statement

### 1.1 Current State

<!--
PURPOSE: Establish the concrete reality — what exists today and why it hurts
PROCESS: (1) Describe the current architecture/behavior. (2) List pain points with measurable impact. (3) Identify who or what is affected. Cite files, test results, or metrics.
GOOD: "AudioSplitter (288 LOC, modules/audio/) exists but has zero tests and is not exported. Any change risks silent regressions across the ingest pipeline."
BAD: "The current system has some issues that need to be addressed for better performance."
-->

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

<!--
PURPOSE: Justify urgency — why this can't wait another sprint or quarter
PROCESS: Identify concrete blockers, compounding costs, or time-sensitive triggers. Link to specific tasks or milestones.
GOOD: "Hex adapter wiring (bd-jo0u) is P0 because it blocks all daemon unit testing. Every day without it means more untested daemon code ships."
BAD: "It would be nice to do this soon because it's been on the backlog for a while."
-->

Why is this problem urgent/important to solve now?
- Blocker for: X
- Technical debt impact: Y
- User impact: Z

---

## 2. Proposed Solution

### 2.1 High-Level Approach

<!--
PURPOSE: Describe WHAT the solution does and HOW it works — conceptually, not code-level
PROCESS: (1) State the approach in one sentence. (2) Break into 2-5 key components. (3) Show how they relate with a diagram if the flow isn't obvious.
GOOD: "Wrap each daemon's NATS connection behind a MessageBrokerProtocol adapter injected at construction time. Three components: (1) adapter interface, (2) NATS implementation, (3) in-memory stub for tests."
BAD: "We will refactor the codebase to use better patterns and improve the architecture."
-->

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

<!--
PURPOSE: Make the "why behind the how" explicit so reviewers can challenge trade-offs
PROCESS: List 2-4 principles that drove design decisions. Each principle should connect to a constraint or project value.
GOOD: "Fail-fast on bad params: HARD REJECT + log + clarification. Never silently clamp. Rationale: silent correction in ATC context is a safety hazard."
BAD: "We follow best practices and industry standards for clean code."
-->

What principles guide this solution?
- Principle 1: Rationale
- Principle 2: Rationale
- Principle 3: Rationale

**Constraints:**
- Constraint 1: Why it matters
- Constraint 2: Why it matters

---

### 2.3 Integration Points

<!--
PURPOSE: Map every system boundary this proposal touches — nothing should be a surprise during implementation
PROCESS: Walk the data flow end-to-end and note every system that sends, receives, or transforms data. Fill the table with concrete module names and change types.
GOOD: "modules/session/fsm.py | Event consumer | Add CLARIFICATION_REQUESTED event handler"
BAD: "Various systems | Integration | Some changes needed"
-->

How does this integrate with existing systems?

| System/Component | Integration Type | Changes Required |
|------------------|------------------|------------------|
| System A | API | New endpoint |
| System B | Event | Subscribe to events |
| System C | Config | Add config values |

---

## 3. Implementation Plan

### 3.1 Phases

<!--
PURPOSE: Break implementation into shippable increments with clear exit criteria
PROCESS: (1) Each phase should be independently deployable or testable. (2) Include effort estimate (S/M/L). (3) Define a concrete deliverable and a validation command or test. (4) Phases should be ordered by dependency, not priority.
GOOD: "Phase 1: Foundation (Effort: S) — Create MessageBrokerProtocol adapter + NATSAdapter implementation. Deliverable: `pytest tests/adapters/ -v` passes. Validation: isinstance(NATSAdapter(), MessageBrokerProtocol) == True"
BAD: "Phase 1: Do the main work. Phase 2: Fix bugs. Phase 3: Polish."
-->

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

<!--
PURPOSE: Lock down the stack so implementation doesn't drift into unvetted dependencies
PROCESS: (1) List each technology with its pinned version and role. (2) For each choice, name the alternative you rejected and why. (3) Flag risks per technology (maturity, licensing, maintenance).
GOOD: "pydantic==2.9.2: Config validation. Chosen over dataclasses because we need runtime validation + JSON schema export. Risk: v2 migration broke some v1 patterns — already resolved in our codebase."
BAD: "Python, some ML libraries, standard tools."
-->

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

<!--
PURPOSE: Show the exact filesystem footprint so reviewers can spot conflicts and understand scope
PROCESS: Use a tree diagram with one-line comments per file. Only include new or modified paths. Mark existing files that change with "(modified)".
GOOD: "modules/broker/adapter.py  # MessageBrokerProtocol ABC + NATSAdapter impl\ntests/broker/test_adapter.py  # Unit tests using NATSClientStub"
BAD: "src/\n  stuff/\n    code.py"
-->

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

<!--
PURPOSE: Formalize the dependency changes as a reviewable graph patch — the "diff" for architecture
PROCESS: (1) Query current state with lev-find or grep. (2) Express additions, modifications, and removals as structured YAML. (3) Include skill and protocol dependencies separately.
GOOD: "add_nodes:\n  - id: broker-adapter\n    path: modules/broker/adapter.py\n    exports: [MessageBrokerProtocol, NATSAdapter]\nadd_edges:\n  - from: asr-daemon\n    to: broker-adapter\n    type: imports"
BAD: "add_nodes:\n  - id: new-stuff\n    path: somewhere\n    type: unknown"
-->

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

optional_skills:
  - skill://lev-research  # Additional research
  - skill://workflow      # Workflow scaffolding where relevant
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

<!--
PURPOSE: Define the "Definition of Ready" — the contract that must be met before implementation starts
PROCESS: (1) Calculate complexity score across 4 dimensions (Effort + Confidence + Risk + Scope, each 0-3). (2) Fill the DoR YAML with concrete values. (3) Check every box in the completion checklist or explain why it's N/A.
GOOD: "DoR:\n  entry: modules/broker/adapter.py\n  done: 'pytest tests/broker/ exits 0 AND all 3 daemons construct with injected adapter'\n  validation: 'make test-broker && python -c \"from modules.broker import NATSAdapter\"'"
BAD: "DoR:\n  entry: TBD\n  done: it works\n  validation: manual testing"
-->

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

<!--
PURPOSE: Prove you looked for existing solutions before proposing new work — prevent reinventing wheels
PROCESS: (1) Search the codebase (grep, glob) for similar functionality. (2) Check BD for related issues. (3) Evaluate each candidate in the table with honest pros/cons. (4) Link related epics/tasks/proposals.
GOOD: "Solution: poc/cleanup hallucination filter | Location: poc/cleanup/strategies/ | Pros: 7 strategies, 33 tests, profile system | Cons: Not wired to production config | Decision: Adopt as-is, wire via ValidationConfig"
BAD: "We looked around and didn't find anything relevant."
-->

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

<!--
PURPOSE: Catch architecture drift before it gets baked into the codebase
PROCESS: (1) Check each item against the project's actual architecture (see docs/architecture/00-actual-architecture.md). (2) If any box is unchecked, document the drift type and justify the deviation.
GOOD: "Drift Type: gap — no existing pattern for config-flag-gated bus switching. Justification: interview Q2 locked the decision for `internal_bus: nats|direct` flag; this creates the first instance of that pattern."
BAD: "Everything aligns. No issues."
-->

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

<!--
PURPOSE: Formalize who must sign off and track unresolved concerns
PROCESS: (1) List required approvers by role. (2) Check all approval criteria. (3) Record every concern raised during review with its resolution — even resolved ones, for the decision log.
GOOD: "Concern: 'NATSAdapter adds constructor complexity to all 3 daemons' — Resolution: Factory function handles wiring; daemon constructors gain 1 param."
BAD: "No concerns."
-->

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

<!--
PURPOSE: Show you evaluated other paths — proves the chosen solution isn't just the first idea
PROCESS: (1) Describe the alternative honestly — steel-man it. (2) List real pros (not strawmen). (3) List real cons with evidence. (4) State the decision and the deciding factor.
GOOD: "Alternative: Keep regex-only intent engine. Pros: Zero migration effort, already deployed, sub-1ms latency. Cons: 50% FP rate on emergency detection (measured), no confidence scores, can't handle multi-intent. Decision: Rejected — FP rate is a safety risk per interview Q10."
BAD: "Alternative: Do nothing. Pros: None. Cons: Everything stays bad. Decision: Rejected obviously."
-->

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

<!--
PURPOSE: Second alternative — include at least two for any full-tier proposal
PROCESS: Same as 5.1. If there's genuinely only one alternative, say so and explain why the design space is constrained.
GOOD: "Alternative: Use Qwen instead of DeBERTa. Pros: Higher raw accuracy on general NLU benchmarks. Cons: No ATC-domain training data, 10x inference cost, interview Q5 explicitly deferred Qwen to P3. Decision: Rejected — premature given current data constraints."
BAD: "Alternative: Use a different library. Pros: It's different. Cons: We don't know it. Decision: No."
-->

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

<!--
PURPOSE: Name the things that could go wrong so the team can prepare, not panic
PROCESS: (1) Brainstorm failure modes — what breaks if your assumptions are wrong? (2) Rate likelihood and impact honestly (High/Med/Low). (3) For each risk, write a concrete mitigation, not "we'll handle it."
GOOD: "Risk: DeBERTa inference exceeds 100ms latency budget on CPU | Likelihood: Med | Impact: High | Mitigation: Benchmark on target hardware in Phase 1; fallback to regex-only if p95 > 80ms"
BAD: "Risk: Something might not work | Likelihood: Low | Impact: Low | Mitigation: We'll figure it out"
-->

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Risk 1 | High/Med/Low | High/Med/Low | Strategy |
| Risk 2 | High/Med/Low | High/Med/Low | Strategy |

---

### 6.2 Dependencies

<!--
PURPOSE: Map what blocks you and what you block — prevent surprise cascading delays
PROCESS: (1) List internal deps with their BD issue IDs and current status. (2) List external deps with fallback plans if they become unavailable.
GOOD: "Internal: Depends on bd-jo0u (hex adapters, status: open) — need MessageBrokerProtocol before wiring daemons. Blocks: bd-w1jx (daemon unit tests) — can't write tests without adapter injection."
BAD: "Depends on some other work being done first."
-->

**Internal Dependencies:**
- Depends on Epic/Task ID: Why, status
- Blocks Epic/Task ID: Why, status

**External Dependencies:**
- External service/tool: Why, risk if unavailable

---

## 7. Success Metrics

### 7.1 Acceptance Criteria

<!--
PURPOSE: Define the binary pass/fail conditions — when is this DONE, no ambiguity
PROCESS: Write each criterion as a testable assertion. Use the format "Given X, when Y, then Z" or "X must be true as verified by Z."
GOOD: "pytest tests/broker/ exits 0 with >= 95% line coverage on modules/broker/adapter.py"
BAD: "The system works correctly and users are happy."
-->

- [ ] Criterion 1: Specific, measurable outcome
- [ ] Criterion 2: Specific, measurable outcome
- [ ] Criterion 3: Specific, measurable outcome

---

### 7.2 Performance Metrics

<!--
PURPOSE: Set quantitative targets so you can prove the solution actually improved things
PROCESS: For each metric, define the target value AND how you'll measure it (command, dashboard, test). Include baselines if known.
GOOD: "Emergency detection false-positive rate | Target: < 5% | Measurement: Run eval suite on 500-sample test set, count FP / (FP + TN)"
BAD: "Speed | Fast | Check if it feels fast"
-->

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Metric 1 | Value | How to measure |
| Metric 2 | Value | How to measure |

---

### 7.3 User Impact Metrics

<!--
PURPOSE: Connect technical changes to user-visible outcomes — keeps the proposal grounded in value
PROCESS: Establish current baseline, set a target, and define how you'll measure the delta. If you don't have a baseline, say so and make measuring it part of Phase 1.
GOOD: "False alarm escalations | Baseline: ~12/day (estimated from logs) | Target: < 1/day | Measurement: Count CLARIFICATION_REQUESTED events in telemetry with source=emergency_detector"
BAD: "User satisfaction | Low | High | Surveys"
-->

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| User metric 1 | Current | Goal | Method |
| User metric 2 | Current | Goal | Method |

---

## 8. References

<!--
PURPOSE: Link to all supporting evidence so reviewers can verify claims without asking you
PROCESS: Organize by type (research, design, related proposals, external). Use relative paths for internal docs, full URLs for external. Add a one-line note on what each reference contributes.
GOOD: "docs/architecture/00-actual-architecture.md — Confirms pipes-and-filters pattern (not hexagonal) for daemon wiring decisions"
BAD: "Some docs we looked at"
-->

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

<!--
PURPOSE: Capture unknowns explicitly so they don't become hidden assumptions
PROCESS: For each question: (1) State the question clearly. (2) Explain why the answer matters for this proposal. (3) List the options you see. (4) Set a deadline — open questions without deadlines never close.
GOOD: "Should the bus flag default to 'direct' or 'nats'? Context: Affects whether existing deployments need config changes. Options: (A) default=nats (backward-compatible), (B) default=direct (simpler). Decision needed by: before Phase 2 starts."
BAD: "What should we do about the thing? Context: It's important. Options: yes or no."
-->

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

<!--
PURPOSE: Create an auditable trail of decisions made during this proposal's lifecycle
PROCESS: Add a row every time a decision is made or changed — during drafting, review, or revision. Include WHO decided (even if it's you) and WHY.
GOOD: "2026-03-05 | Reject Qwen for V1, defer to P3 | Interview Q5: no ATC training data yet | JP"
BAD: "Today | We decided stuff | Because | Someone"
-->

| Date | Decision | Rationale | Approver |
|------|----------|-----------|----------|
| YYYY-MM-DD | Decision text | Why | Name |
| YYYY-MM-DD | Decision text | Why | Name |

---

## 11. Next Steps

<!--
PURPOSE: Make the path forward unambiguous — what happens immediately vs. after approval
PROCESS: (1) List pre-approval actions (reviews, spikes, questions to resolve). (2) List post-approval actions (BD epic creation, phase kickoff). (3) List follow-up items (checkpoints, retrospectives).
GOOD: "Before Approval: (1) Run benchmark on target hardware to validate latency assumption. (2) Resolve open question on bus flag default. After Approval: (1) `bd create --type=epic 'Hex Adapter Wiring'` with phases from section 3.1."
BAD: "1. Do the work. 2. Ship it. 3. Celebrate."
-->

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

<!--
PURPOSE: Provide code-level detail that supports the proposal without cluttering the main sections
PROCESS: Include type definitions, interface contracts, config schemas, or algorithm pseudocode. This is the "show me the code" section for skeptical reviewers.
GOOD: "class MessageBrokerProtocol(Protocol):\n    async def publish(self, subject: str, payload: bytes) -> None: ...\n    async def subscribe(self, subject: str, handler: Callable) -> None: ..."
BAD: "// TODO: add code here later"
-->

```typescript
// Code examples, type definitions, interfaces
// that support the proposal
```

### B. Research Data

<!--
PURPOSE: Include raw data, benchmarks, or metrics that informed the proposal's claims
PROCESS: Present data in tables or structured format. Include collection methodology and date. Link to reproducible scripts if possible.
GOOD: "Emergency regex FP test (2026-03-04, n=500):\n  True positives: 47/50 (94%)\n  False positives: 225/450 (50%)\n  Script: scripts/eval_emergency_regex.py"
BAD: "We tested it and it was bad."
-->

```
Supporting data, metrics, benchmarks
that informed the proposal
```

### C. Prototype/POC

<!--
PURPOSE: Link to working code that de-risks the proposal — proof it's not just theory
PROCESS: Point to the POC location, state whether it works, and summarize what you learned. Be honest about POC limitations.
GOOD: "Location: poc/cleanup/ | Status: working (7 strategies, 33 tests pass) | Findings: Profile-based strategy selection works well; config wiring to production ValidationConfig is the remaining gap."
BAD: "Location: somewhere | Status: maybe works | Findings: it seemed fine"
-->

**Location:** path/to/poc
**Status:** working | needs_fixes | abandoned
**Findings:** Key learnings from POC

---

## Next Steps in Workflow

<!--
PURPOSE: Orient the reader on where this proposal sits in the lifecycle and what actions are available
PROCESS: This section is mostly static — update only the lifecycle position line to reflect current state.
GOOD: Leave as-is unless the proposal has moved past "crystallizing" stage.
BAD: Deleting this section or leaving the lifecycle position stale after a stage transition.
-->

**This proposal is at the "crystallizing" stage.** Here's what typically comes next:

1. **Design validation gates** - Define test strategy, DoR, acceptance criteria
2. **Create implementation plan** - `work "plan implementation of {this proposal}"` - generates `plan-{kind}-{slug}.md` for the current execution slice
3. **Run spike/POC** - Test technical unknowns: `work "POC for {specific aspect}"`
4. **Get alignment** - Run `lev-align` to check for architecture drift
5. **Refine proposal** - Update based on feedback, more research if needed
6. **Scaffold tracker epic** - Once approved: create the execution-slice tracker and link the plan artifact

**Lifecycle position:** ephemeral - captured - **crystallizing** - crystallized - manifesting - completed

---

*Proposal created via work skill (crystallizing stage)*
