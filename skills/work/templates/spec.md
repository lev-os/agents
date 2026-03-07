---
title: "{{TITLE}}"
type: spec
entity: "{{ENTITY_ID}}"
stage: crystallized
created: "{{DATE}}"
author: "{{AUTHOR}}"
status: draft
---

# {{TITLE}} — Behavioral Specification

## Executive Summary
<!-- 2-3 sentences: what this spec defines and why -->

## Context
<!-- System context, architectural constraints, related specs -->

### Existing State
<!-- Current implementation or lack thereof -->

### Target State
<!-- Desired end state with measurable criteria -->

## User Scenarios (BDD)

### Scenario 1: {{SCENARIO_NAME}}
```gherkin
Feature: {{FEATURE_NAME}}
  As a {{ROLE}}
  I want {{GOAL}}
  So that {{BENEFIT}}

  Scenario: {{SCENARIO}}
    Given {{PRECONDITION}}
    When {{ACTION}}
    Then {{EXPECTED_RESULT}}
```

## Behavioral Specification

### Inputs
<!-- Input types, schemas, validation rules -->

### Processing
<!-- Step-by-step processing logic, state transitions -->

### Outputs
<!-- Output types, schemas, side effects -->

### Performance
<!-- Latency, throughput, resource constraints -->

## Contract

### Dependencies
<!-- External services, packages, skills required -->

### Integration Points
<!-- APIs, events, hooks this spec touches -->

### Breaking Changes
<!-- What existing behavior this changes -->

## Implementation Guidance

### Recommended Skills
<!-- Skill IDs discovered during planning phase -->

### Team Structure
<!-- Recommended execution strategy: direct / ephemeral subagents / formal team -->

### Workstreams
<!-- If team/subagents: workstream definitions with assignments -->

## BD Task Decomposition

### Epic Mapping
<!-- List required epics and why they exist -->

| Epic ID | Title | Scope | Success Signal |
|---------|-------|-------|----------------|
| {{EPIC_ID}} | {{EPIC_TITLE}} | {{EPIC_SCOPE}} | {{EPIC_SUCCESS_SIGNAL}} |

### Task Breakdown
<!-- Decompose spec into executable BD tasks; map each task to scenarios/contracts -->

| Task ID | Summary | Linked Scenario(s) | Owner | Acceptance Signal |
|---------|---------|--------------------|-------|-------------------|
| {{TASK_ID}} | {{TASK_SUMMARY}} | {{SCENARIO_REF}} | {{OWNER}} | {{ACCEPTANCE_SIGNAL}} |

### Dependency Ordering
<!-- Explicit prerequisites/dependencies between tasks -->

| Blocking Task | Dependent Task | Reason |
|---------------|----------------|--------|
| {{BLOCKING_TASK}} | {{DEPENDENT_TASK}} | {{DEPENDENCY_REASON}} |

## Test Coverage

### Unit Tests
<!-- Key test cases -->

### Integration Tests
<!-- Cross-boundary test scenarios -->

### E2E Verification
<!-- End-to-end smoke test command -->

## Success Criteria
<!-- Measurable acceptance criteria -->

## Rollback Plan
<!-- How to safely revert this spec's changes if execution fails -->

### Rollback Trigger
<!-- Objective condition that triggers rollback -->

### Rollback Steps
1. {{ROLLBACK_STEP_1}}
2. {{ROLLBACK_STEP_2}}
3. {{ROLLBACK_STEP_3}}

### Data/State Recovery
<!-- How to recover data, state, or config safely -->

## Open Questions
<!-- Unresolved decisions, risks, unknowns -->
