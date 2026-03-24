---
name: cdo-domain-arch
description: Architecture team preset — ATAM, C4, ADR framework analysis
---

# CDO Domain: Architecture

Architecture team preset for design analysis, trade-off evaluation, and decision documentation.

---

## Team Shape

| Role | Agent Type | Skills | Focus |
|------|-----------|--------|-------|
| **Architect** | architecture-advisor | /arch, ATAM, C4, quality attributes | System design, trade-offs |
| **Critic** | general-purpose | risk-assessment, failure-modes | Attack surface, what breaks |
| **Systems Thinker** | general-purpose | systems-thinking, feedback-loops | Coupling, emergent behavior |
| **Pragmatist** | general-purpose | total-cost-ownership, implementation | What actually ships |

---

## Source Files (Auto-Read for Context)

The Architect auto-loads these at session start:

- `docs/specs/` — Existing specifications
- `docs/design/` — Design documents
- `docs/ARCHITECTURE.md` — Architecture overview
- `.lev/pm/designs/` — Design proposals
- `AGENTS.md` — Ownership map and module boundaries

---

## Workflow

```
T1: Architect proposes, all roles analyze in parallel
    - Architect frames the problem: drivers, constraints, quality attributes
    - Critic identifies failure modes and risks (independent)
    - Systems Thinker maps coupling and second-order effects (independent)
    - Pragmatist evaluates implementation cost and timeline (independent)
    - Output: 4 independent position papers

T2: Cross-examination of architectural drivers vs quality attributes
    - Each role challenges the others' assumptions
    - Focus: where do quality attributes conflict? (e.g., performance vs maintainability)
    - Output: trade-off matrix with clear tensions identified

T3: Synthesis + ADR generation
    - Architect integrates all perspectives into a decision
    - Output: Architecture Decision Record (ADR)
    - Output: Updated C4 diagrams if structural changes proposed

Adaptive: bring in domain experts if specific subsystems need attention
    - Security-sensitive → add Security Expert
    - Data-intensive → add Data Architect
    - Cross-team impact → add Stakeholder Proxy
```

---

## ADR Output Format

```markdown
# ADR-NNN: [Decision Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the issue we're deciding on?]

## Drivers
- [Quality attribute 1]
- [Quality attribute 2]
- [Constraint]

## Decision
[What we decided and why]

## Alternatives Considered
### Option A: [name]
- Pros: ...
- Cons: ...
- Trade-offs: ...

### Option B: [name]
...

## Consequences
- [Positive consequence]
- [Negative consequence / accepted risk]
- [Trade-off accepted]

## Dissent
[Any dissenting views from the architecture team — preserved, not suppressed]
```

---

## Quality Attribute Analysis

The team evaluates proposals against these attributes (ATAM-style):

| Attribute | Question | Measured By |
|-----------|----------|-------------|
| **Modifiability** | How hard is it to change later? | Files touched per feature |
| **Testability** | Can we verify it works? | Test coverage, isolation |
| **Performance** | Does it meet latency/throughput needs? | Benchmarks |
| **Security** | What's the attack surface? | Threat model |
| **Deployability** | How does it ship? | Pipeline complexity |
| **Operability** | How do we monitor/debug it? | Observability surface |

---

## C4 Diagram Levels

When structural changes are proposed, the Architect produces:

- **L1 (Context)**: System boundaries and external actors
- **L2 (Container)**: Major runtime components and data flows
- **L3 (Component)**: Internal module structure (only for affected areas)
- **L4 (Code)**: Only if the decision affects specific class/function design
