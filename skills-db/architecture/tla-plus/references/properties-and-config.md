# Properties and Configuration

## Semantic levels

- `ASSUME` is for constant-level facts about constants and fixed structures.
- `INVARIANT` / `INVARIANTS` in `.cfg` are for state predicates.
- `PROPERTY` / `PROPERTIES` in `.cfg` are for temporal formulas, action properties, and refinement checks.

## Important trap

If you move from `INVARIANT I` to `PROPERTY I` without redefining `I` as `[]I`, TLC only checks the initial states, not all reachable states.

## `.cfg` responsibilities

Put in `.cfg`:
- which specification to check
- constant replacements
- which invariants or properties to check
- optional search controls such as symmetry, view, constraints, alias

Put in `.tla`:
- the actual formulas
- operator definitions
- constants and variables
- the logic of the model

## Minimal recommended structure

```cfg
SPECIFICATION Spec
CONSTANTS
    N <- MC_N
INVARIANTS
    TypeOK
    Safety
PROPERTIES
    Liveness
```

## `SPECIFICATION` vs `INIT` + `NEXT`

- Prefer `SPECIFICATION` for full temporal specs, especially with fairness.
- Use `INIT` + `NEXT` only when you are checking safety and do not need fairness-driven temporal behavior.

## Advanced controls

- `SYMMETRY` can shrink search dramatically but only if the symmetry is real.
- `VIEW` abstracts states and can hide bugs if chosen badly.
- `CONSTRAINT` and `ACTION_CONSTRAINT` prune search without reporting an error.
- `ALIAS` improves trace readability.
