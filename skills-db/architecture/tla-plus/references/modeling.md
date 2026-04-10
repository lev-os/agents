# Modeling Notes

## Core modeling posture

- TLA+ models systems above the code level.
- A behavior is a sequence of states.
- A step is a pair of consecutive states.
- The spec describes a set of possible behaviors.

## PlusCal vs raw TLA+

- Use PlusCal for algorithm-centric work, especially concurrent or distributed algorithms with explicit control flow.
- Use raw TLA+ when the model is more relational, modular, mathematical, or refinement-heavy.
- PlusCal translates to TLA+ and that translation is the thing you actually check.

## Keep the model smaller than the code

- Omit runtime plumbing and type detail that do not change the behavioral question.
- Fix parameters to finite values first.
- Prefer one clear bug-revealing model over a realistic but intractable one.

## Local state warning

In distributed models, all variables are global. If one variable represents many processes' local states, add locality-style properties when accidental cross-process updates would be a bug.

## Useful starter structure

```tla
VARIABLES vars

Init == ...
Next == ...
Spec == Init /\ [][Next]_vars

TypeOK == ...
Safety == ...
```
