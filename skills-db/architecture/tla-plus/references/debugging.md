# Debugging Failures

## First rule

Minimize the model before theorizing about the bug.

## Property failure triage

If a `PROPERTY` fails:
1. Remove the property from the `.cfg`.
2. Rerun invariants only.
3. Fix any invariant failure first.
4. Return to the temporal property only after the safety floor is stable.

## Failure worksheet

```text
Check type:
Smallest failing configuration:
Trace story:
Likely modeling mistake:
Next change:
```

## TLC-specific debugging habits

- Keep constants small until the failure is understandable.
- Use one worker on small models when deterministic depth reporting matters.
- Dump traces when you need to inspect an implementation-facing artifact.
- Use `ALIAS` or differential traces to improve readability, not to hide structure.

## Common causes

- wrong variable updated
- missing `UNCHANGED`
- invariant expressed at the wrong semantic level
- property checked as an invariant or vice versa
- configuration constants not aligned with the intended model
