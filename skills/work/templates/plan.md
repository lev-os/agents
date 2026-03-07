---
type: plan
plan_kind: impl | bugfix | chore | research
created: YYYY-MM-DDTHH:MM:SS
updated: YYYY-MM-DDTHH:MM:SS
status: draft | ready | in_progress | blocked | complete
domain: core | product | ux | plugin | platform | research
confidence: 0.0-1.0
author: agent-name
related_tasks: [task-id-1, task-id-2]
related_docs: [path/to/doc1.md, path/to/doc2.md]
related_specs: [path/to/spec1.md]
---

# Plan: Title

## How To Fill This Out

Use this template for the current execution slice. A plan is not the long-term roadmap; it is the concrete execution artifact for the slice that is active now. The long-term roadmap stays in the handoff.

Plan file naming should follow the family:
- `plan-impl-{slug}.md`
- `plan-bugfix-{slug}.md`
- `plan-chore-{slug}.md`
- `plan-research-{slug}.md`

Use uncertainty markers when needed:
- `[tbd]`
- `[unknown]`
- `[theory]`
- `[maybe: ..., confidence: ##%]`

Good:
- "This plan covers the current implementation slice only."
- "This plan links back to the spec and validation gates."

Bad:
- "This is the full multi-session roadmap."
- "This is a dumping ground for ideas."

## Executive Summary

Briefly describe the current slice, why it exists now, and what success looks like.

## Goal

One-sentence goal for this execution slice.

## Done Condition

Deterministic completion test for this slice.

## Why This Slice Now

Explain why this is the right slice to execute next.

## Inputs and Preconditions

- Input artifact 1
- Input artifact 2
- Precondition 1

## Execution Steps

1. Step 1
2. Step 2
3. Step 3

## Validation

### Gates

- Gate 1
- Gate 2

### Checks

- [ ] Check 1
- [ ] Check 2
- [ ] Check 3

## Dependencies

| Dependency | Type | Notes |
|------------|------|-------|
| path/to/spec.md | spec | Why |

## Risks and Unknowns

- `[tbd]`
- `[maybe: ..., confidence: ##%]`

## Next Promotion or Closeout Step

What happens when this plan completes?

