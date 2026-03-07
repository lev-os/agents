---
title: "{{TITLE}}"
type: chore
entity: "{{ENTITY_ID}}"
spec_ref: "{{SPEC_PATH}}"
created: "{{DATE}}"
author: "{{AUTHOR}}"
status: draft
priority: "{{PRIORITY}}"
---

# {{TITLE}} — Implementation Chore

> **Ephemeral document.** DELETE this chore when code matches spec. No FMEA here — that lives in the spec.

## Gap Summary
<!--
PURPOSE: 1-2 sentences: what's broken and which spec defines the target.
PROCESS: State the gap, not the solution. Reference the spec by path and section.
GOOD: "ValidationConfig exists (modules/transcription/config.py:92-99) but is never injected
      into the ASR daemon. Target: spec-transcription.md Section 'Processing Step 5'."
BAD:  "Validation needs to be improved."
-->

## Gap Matrix
<!--
PURPOSE: Spec section vs current state. DELETE rows as they're closed.
PROCESS: One row per gap. Severity = how bad is it if this gap stays open.
         When you close a gap, delete the row. When all rows are gone, delete the chore.
GOOD: Specific file:line references for both spec target and current code.
BAD:  Vague descriptions without file references.
-->

| # | Spec Section | Target | Current Reality | Severity | Status |
|---|-------------|--------|-----------------|----------|--------|
| 1 | {{SPEC_SECTION}} | {{WHAT_SPEC_SAYS}} | {{WHAT_CODE_DOES}} | {{P0-P4}} | open |

## Implementation Steps
<!--
PURPOSE: Ordered steps to close the gaps. Check off as completed.
PROCESS: Each step should be independently verifiable. Include the validation command.
         Group by phase if there are natural dependency boundaries.
GOOD: "1. Inject ValidationConfig into ASRDaemon.__init__() — verify: unit test passes
      2. Wire CircuitBreaker to validation pipeline — verify: `just test-asr`
      3. Add run_in_executor wrapper — verify: no event loop blocking in profiler"
BAD:  "1. Fix the validation system"
-->

### Phase 1: {{PHASE_NAME}}
- [ ] {{STEP}} — verify: {{VALIDATION_COMMAND}}
- [ ] {{STEP}} — verify: {{VALIDATION_COMMAND}}

## Dependencies
<!--
PURPOSE: What blocks this chore or what this chore blocks.
PROCESS: Reference BD issue IDs and other chore paths.
-->

| This Chore | Depends On | Reason |
|------------|-----------|--------|
| {{THIS}} | {{BLOCKER}} | {{WHY}} |

## Done When
<!--
PURPOSE: Concrete conditions that make this chore deletable.
PROCESS: List binary (pass/fail) criteria. When ALL are true, delete this file.
GOOD: "All gap matrix rows are closed. `just gate-2` passes. Spec BDD scenarios 1-4 have
      corresponding passing tests."
BAD:  "Code is aligned with spec."
-->

- [ ] All gap matrix rows closed (deleted)
- [ ] {{DONE_CRITERION}}
- [ ] {{DONE_CRITERION}}
