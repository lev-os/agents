# Workshop Lifecycle Reference

Full documentation for the INTAKE → ANALYSIS → POC → INTEGRATION lifecycle.

## Phase Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   INTAKE    │ →  │  ANALYSIS   │ →  │     POC     │ →  │ INTEGRATION │
│             │    │             │    │             │    │             │
│ Raw idea or │    │ Understand  │    │ Build       │    │ Production  │
│ requirement │    │ scope &     │    │ working     │    │ deployment  │
│             │    │ approach    │    │ prototype   │    │ & routing   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Phase 1: Intake

**Purpose:** Capture raw ideas, requirements, or problems.

**Input:** Natural language description, error message, feature request.

**Process:**
1. Classify type: skill | workflow | synth | adapter | hook | plugin
2. Create workshop item in ~/clawd/workshop/intake/

**Output:**
```yaml
id: ws-XXX
type: skill
title: "Description"
source: "conversation"
status: intake
raw_input: |
  Original request...
```

## Phase 2: Analysis

**Purpose:** Understand scope, dependencies, approach.

**Questions to answer:**
- What existing entities does this interact with?
- What's the minimal viable implementation?
- What are the edge cases?
- How will we test it?

**Output:**
```yaml
analysis:
  dependencies: [list]
  approach: |
    1. Step one
    2. Step two
  success_criteria:
    - Criterion 1
    - Criterion 2
  estimated_complexity: low | medium | high
  analysis_complete: true
```

## Phase 3: POC

**Purpose:** Build working prototype to validate approach.

**Location:** ~/clawd/workshop/poc/<item-id>/

**Requirements:**
- Must run standalone
- Must have basic tests
- Must document usage
- Must log decisions

**Output:**
```yaml
poc:
  location: ~/clawd/workshop/poc/ws-XXX/
  files: [list]
  test_results:
    passed: N
    failed: N
  poc_complete: true
```

## Phase 4: Integration

**Purpose:** Promote POC to production.

**Integration targets:**
- ~/.claude/skills/ - Skills
- ~/lev/context/workflows/ - Workflows
- ~/clawd/synth/ - Synths
- ~/leviathan/core/ - Adapters

**Output:**
```yaml
integration:
  status: complete
  integrated_to:
    - target: location
  routing_rules: [list]
```

## CLI Commands

```bash
lev workshop intake "description"
lev workshop analyze ws-XXX
lev workshop poc ws-XXX
lev workshop integrate ws-XXX
lev workshop status
lev workshop list --phase poc
```

## Storage

- Workshop items: ~/clawd/workshop/
- POC staging: ~/clawd/workshop/poc/
- Integration queue: ~/clawd/workshop/integration/
