# Mode Selection Matrix

## Goal -> Mode

| Goal | Recommended Command Pattern | Why |
|------|-----------------------------|-----|
| Validate empty-state visual fidelity | `--profile analytics-empty` | Removes data variability from diagnosis |
| Validate data-backed rendering | `--profile analytics-seeded --seed-required` | Forces real data path and explicit seeding success |
| Validate message list behavior | `--profile messages-seeded --seed-required` | Focuses list/detail rendering with seeded inbox traffic |
| Validate cross-screen stability | `--profile tour-seeded` or suite mode | Exercises navigation and transitions |
| Validate environment sanity before deep runs | `doctor_tui_inspector.sh` | Catches dependency/wiring issues early |

## Strictness Levels

1. Exploratory:
   no required flags; fastest iteration.
2. Verification:
   add `--seed-required`.
3. Release-gate:
   add both `--seed-required` and `--snapshot-required` and run suite mode.

## Timing Tuning

- If startup races happen:
  increase `--boot-sleep`.
- If snapshots miss state:
  increase `--snapshot-second`.
- If keyflow seems rushed:
  increase waits in `--keys`.
