---
type: design
created: YYYY-MM-DDTHH:MM:SS
updated: YYYY-MM-DDTHH:MM:SS
status: draft | in_review | approved | superseded
domain: core | product | ux | plugin | platform | research
confidence: 0.0-1.0
author: agent-name
related_tasks: [task-id-1, task-id-2]
related_docs: [path/to/doc1.md, path/to/doc2.md]
related_specs: [path/to/spec1.md]
---

# Design: Title

## How To Fill This Out

Use this template when shaping system behavior, UX, interaction flows, or architecture before locking a spec. Designs can reference specs, but they are broader and can hold multiple candidate paths.

Use uncertainty markers when needed:
- `[tbd]`
- `[unknown]`
- `[theory]`
- `[maybe: ..., confidence: ##%]`

Good:
- "This design compares two interaction surfaces and recommends one."
- "This design references two specs but is not itself a spec."

Bad:
- "This is basically an implementation plan."
- "This is a spec with vague drawings."

## Executive Summary

Briefly describe the design problem, the proposed direction, and why it is the right next step.

## Problem Framing

### Current State

What exists today? What is awkward, unclear, or incomplete?

### Desired Experience

What should the user, operator, or system experience look like when this design succeeds?

## Product Requirements

These sections capture PRD-style content inside the design. Do not create a
separate PRD unless the user explicitly asks for one.

### Problem Statement

Describe the problem from the user, operator, or system perspective.

### Solution Direction

Describe the proposed solution from the user, operator, or system perspective.

### User / Operator Stories

1. As a `<role>`, I want `<capability>`, so that `<benefit>`.

### Implementation Decisions

- Modules or surfaces to build or modify
- Interfaces, schemas, contracts, or interactions to clarify
- Domain vocabulary and ADRs that must shape the design
- Deep-module candidates with simple, testable interfaces

### Testing Decisions

- External behavior that proves success
- Modules, flows, or contracts that need tests
- Prior-art tests, validators, fixtures, or replay checks to reuse
- QA/Pentagon proof design when applicable:
  - promotion decision
  - highest-risk behavioral claim
  - fail-closed acceptance criterion
  - owner-local test/probe/fixture placement
  - Pentagon axes required
  - UltraQA scenario classes required
  - ai-slop-cleaner review gate for cleanup/refactor/fallback/boundary risk

### Out of Scope

- Explicit non-goal 1
- Explicit non-goal 2

## Constraints

- Constraint 1
- Constraint 2
- Constraint 3

## Design Direction

### Core Idea

Describe the main design direction in plain language.

### Key Elements

1. Element 1
2. Element 2
3. Element 3

## Alternatives Considered

### Option A

- Strengths
- Weaknesses
- Why chosen or rejected

### Option B

- Strengths
- Weaknesses
- Why chosen or rejected

## Interaction / Information Model

Describe the main user flow, operator flow, or system interaction model.

```text
[Optional ASCII flow]
```

## Spec Touchpoints

List the specs this design informs or depends on.

| Spec | Relationship | Notes |
|------|--------------|-------|
| path/to/spec.md | informs | Why |

## Risks and Unknowns

- Risk 1
- Risk 2
- `[tbd]`

## Recommendation

State the preferred design direction and why.

## Promotion Readiness

- [ ] Ready to promote to `docs/_inbox`
- [ ] Needs spec follow-up
- [ ] Needs prototype or examples
