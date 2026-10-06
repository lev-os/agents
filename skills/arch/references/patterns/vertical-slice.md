# Vertical slice

**Plain words:** organize code by feature (one folder holds the handler, its rules, its adapter calls and its tests), not by technical layer (all controllers here, all services there).

## Fits when
- A change touches one behavior but today edits five layer folders.
- Helpers were promoted to a shared folder with a single caller.
- Agents work in parallel; a slice keeps one change inside one context window.

## Hurts when
- Real shared rules get copied into every slice (now three versions drift).
- Slices reach into each other's internals instead of a shared domain type.
- Used as an excuse for no domain model at all in a rule-heavy area.

## Cost
- Lines: often negative; removes pass-through layers.
- Concepts: 1 (slice). The discipline is when to promote a helper (2+ independent callers).

## Tiny example
```text
plugins/sdlc/src/handlers/
  close-task.ts        # handler: parse args, call rules, write
  close-task.rules.ts  # pure rules for this one behavior
  close-task.test.ts
# shared only after a second slice needs it -> core/domain or core/utils
```

## Pairs with / fights
- Pairs: functional-core (inside a slice), modular-monolith (slices inside modules), result-types.
- Fights: clean-architecture rings imposed per slice; utility gravity (premature shared helpers).

## In Lev
Default by standard: `code-quality.yaml#vertical_slice_locality` and `#helper_promotion_rule` (promote only with 2+ callers), smells `utility_gravity`, `god_object`. Handler LOC soft 250 / hard 400 forces slices to stay small.

Sources: Jimmy Bogard, "Vertical Slice Architecture" (jimmybogard.com, 2018).
