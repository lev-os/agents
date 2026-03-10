---
type: validation-report
created: YYYY-MM-DDTHH:MM:SS
updated: YYYY-MM-DDTHH:MM:SS
status: draft | validated | failed | partial
domain: core | product | ux | plugin | platform | research
confidence: 0.0-1.0
author: agent-name
related_tasks: [task-id-1, task-id-2]
related_docs: [path/to/doc1.md, path/to/doc2.md]
related_specs: [path/to/spec1.md]
---

# Validation Report: Title

## How To Fill This Out

Use this template when validating an implementation, design, spec, or execution slice against explicit requirements. This is not a general report; it is a check against a declared target.

Use uncertainty markers when needed:
- `[tbd]`
- `[unknown]`
- `[theory]`
- `[maybe: ..., confidence: ##%]`

Good:
- "This report validates a spec against implementation."
- "This report shows what passed, what failed, and the evidence."

Bad:
- "This is just another research summary."
- "This guesses pass/fail without evidence."

## Executive Summary

State what was validated, the overall result, and the most important gap or success.

## Validation Results

| Requirement | Status | Evidence | Notes |
|-------------|--------|----------|-------|
| Requirement 1 | PASS | path:line | Why |
| Requirement 2 | FAIL | path:line | Why |

## Detailed Evidence

### Area 1

```text
[Relevant evidence]
```

### Area 2

```text
[Relevant evidence]
```

## Gaps

- Gap 1
- Gap 2

## Recommended Next Actions

1. Action 1
2. Action 2

## Validation Decision

- [ ] Validated
- [ ] Needs follow-up plan
- [ ] Needs spec update
- [ ] Needs design revision
