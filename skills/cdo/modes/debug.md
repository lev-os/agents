---
name: cdo-debug
description: 7-step Root Cause Analysis workflow — REPRODUCE → ISOLATE → TRACE → HYPOTHESIZE → VERIFY → FIX → VALIDATE
---

# CDO Debug — Root Cause Analysis Workflow

7-step systematic debugging. Fixed turn count. No scope creep.

```
REPRODUCE → ISOLATE → TRACE → HYPOTHESIZE → VERIFY → FIX → VALIDATE
```

## Artifact Structure

```
tmp/debug-rca-<timestamp>/
├── 00-input.md
├── 01-reproduce.md
├── 02-isolate.md
├── 03a-call-path.md        # parallel agent A
├── 03b-working-code.md     # parallel agent B
├── 04-hypotheses.md
├── 05-verified.md
├── 06-fix.md
└── FINAL-validation.md
```

---

## T1: REPRODUCE

**Goal**: Define the exact failure condition. No ambiguity.

**Agent Prompt**:
> You are a reproduction specialist. Your ONLY job is to define the exact steps that trigger this bug.
> Output: exact command/action sequence, expected result, actual result, environment details.
> Do NOT theorize about causes. Do NOT suggest fixes. Just reproduce.

**Output Format** (`01-reproduce.md`):
```markdown
## Reproduction Steps
1. [exact step]
2. [exact step]
...

## Expected Result
[what should happen]

## Actual Result
[what actually happens — include error messages verbatim]

## Environment
- OS/runtime: ...
- Versions: ...
- Config: ...

## Reproduction Confidence
- [ ] Reproduces 100% of the time
- [ ] Reproduces intermittently (~X%)
- [ ] Could not reproduce (STOP — need more info)
```

---

## T2: ISOLATE

**Goal**: Narrow to the smallest failing case.

**Agent Prompt**:
> You are an isolation specialist. Given the reproduction from T1, strip away everything unnecessary.
> Find the MINIMAL reproduction case. Remove dependencies, simplify inputs, reduce scope.
> Output: the smallest possible failing case and what you eliminated.

**Output Format** (`02-isolate.md`):
```markdown
## Minimal Reproduction
[smallest case that still fails]

## Eliminated Variables
- [thing removed that didn't affect the bug]
- ...

## Isolation Boundary
[the specific module/function/layer where the bug lives]
```

---

## T3: TRACE (Parallel)

Two agents run simultaneously:

### Agent A — Call Path Tracer

**Agent Prompt**:
> Trace the exact execution path from the isolated reproduction case. Follow the call stack
> through every function, module boundary, and data transformation. Document the path where
> behavior diverges from expectation.

**Output Format** (`03a-call-path.md`):
```markdown
## Call Path
1. [entry point] → [function] → [function] → ...
2. Divergence point: [where actual != expected]
3. Data state at divergence: [values, types, shapes]
```

### Agent B — Working Code Comparison

**Agent Prompt**:
> Find the nearest WORKING code path — similar functionality that doesn't have this bug.
> Compare: what's different? Different inputs? Different guards? Different data flow?
> Focus on structural differences, not cosmetic ones.

**Output Format** (`03b-working-code.md`):
```markdown
## Working Comparison
- Working path: [file:line — what works]
- Broken path: [file:line — what fails]

## Structural Differences
1. [difference]
2. [difference]

## Likely Significance
[which difference most likely explains the bug]
```

---

## T4: HYPOTHESIZE

**Goal**: Form 2-3 theories with evidence. Not guesses — theories backed by trace data.

**Agent Prompt**:
> Given the trace (T3a) and comparison (T3b), form exactly 2-3 hypotheses about the root cause.
> Each hypothesis MUST cite specific evidence from the trace. Rank by likelihood.
> Do NOT propose fixes yet.

**Output Format** (`04-hypotheses.md`):
```markdown
## Hypothesis 1 (most likely): [name]
- Evidence: [cite from 03a/03b]
- Mechanism: [how this would cause the observed failure]
- Testable prediction: [if this is the cause, then X should also be true]

## Hypothesis 2: [name]
...

## Hypothesis 3 (if applicable): [name]
...
```

---

## T5: VERIFY

**Goal**: Test each hypothesis. Confirm or eliminate.

**Agent Prompt**:
> Test each hypothesis from T4. For each one:
> 1. Check the testable prediction — is it true?
> 2. If possible, temporarily modify the suspected cause — does the bug go away?
> 3. Mark as CONFIRMED, ELIMINATED, or INCONCLUSIVE.
> Exactly ONE hypothesis should be CONFIRMED. If zero or multiple, go back to T4.

**Output Format** (`05-verified.md`):
```markdown
## Hypothesis 1: [CONFIRMED / ELIMINATED / INCONCLUSIVE]
- Prediction test: [result]
- Modification test: [result]
- Conclusion: [why confirmed/eliminated]

## Hypothesis 2: [CONFIRMED / ELIMINATED / INCONCLUSIVE]
...

## Root Cause (confirmed)
[single clear statement of the root cause]
```

---

## T6: FIX

**Goal**: Apply the MINIMAL fix. No scope creep. No refactoring. No "while we're here."

**Agent Prompt**:
> Apply the smallest possible fix for the confirmed root cause. Rules:
> - Fix ONLY the root cause. Nothing else.
> - No refactoring.
> - No "improvements."
> - No touching files unrelated to the fix.
> - If the fix is more than ~20 lines, justify why.

**Output Format** (`06-fix.md`):
```markdown
## Fix Applied
- File(s): [paths]
- Change: [description]
- Lines changed: [count]

## Fix Rationale
[why this fix addresses the root cause, not just the symptom]

## Scope Check
- [ ] Fix touches ONLY the root cause
- [ ] No refactoring included
- [ ] No unrelated changes
```

---

## T7: VALIDATE

**Goal**: Adversarial validation. PASS or FAIL — no "looks good."

**Agent Prompt** (ralph role):
> You are an adversarial validator. Your job is to BREAK this fix. Try:
> 1. Does the original reproduction case pass?
> 2. Edge cases — what inputs could still trigger the bug?
> 3. Regression — did the fix break anything else?
> 4. Root cause — does the fix address the CAUSE or just the SYMPTOM?
>
> Verdict: PASS or FAIL. No "partial pass." No "looks good enough."

**Output Format** (`FINAL-validation.md`):
```markdown
## Validation Verdict: [PASS / FAIL]

## Original Reproduction: [PASS / FAIL]
[evidence]

## Edge Cases Tested
1. [case] → [result]
2. [case] → [result]

## Regression Check: [PASS / FAIL]
[evidence]

## Root Cause Addressed: [YES / NO]
[evidence — fix targets cause, not symptom]

## If FAIL
[what specifically failed and what T-step to return to]
```

---

## Convergence

- **Turn count**: Fixed at 7. No negotiation.
- **Final verdict**: Must be PASS from adversarial validator.
- **If FAIL at T7**: Return to the T-step indicated by the validator. Do not restart from T1.

## Anti-Patterns

- **Don't fix symptoms** — If the fix is "add a null check" but the root cause is "data shouldn't be null here," you're fixing the symptom.
- **Don't refactor while debugging** — Refactoring changes the system under observation. Debug first, refactor later.
- **Don't skip hypothesis testing** — "I'm pretty sure it's X" is not verification. Test it.
- **Don't expand scope** — "While I'm in here, I might as well..." No. Fix the bug. File a separate issue for improvements.
