# State machines (FSM, statecharts, typestate)

**Plain words:** name every state a thing can be in and every allowed move between states. A move not on the list is impossible, not just discouraged. Statecharts add nesting and parallel regions; typestate puts the state in the type so the compiler rejects illegal calls.

## Fits when
- A lifecycle exists (captured → crystallized → manifesting → completed) and bugs come from illegal jumps.
- Booleans multiply (`isRunning && !isDone && hasError`); 2^n combos, few legal.
- Humans need to see the flow; the table or diagram is the spec.

## Hurts when
- Two states and one transition: a boolean or enum is enough.
- Deeply nested statecharts nobody can read; the chart becomes the god object.
- State lives in two places (a `stage:` field and a derived stage); pick one owner.

## Cost
- Lines: a transition table (data) plus one pure `next(state, event)` function.
- Concepts: 2 (state, event). Statecharts add 3 (hierarchy, parallel, history). Library optional; a table is often enough.

## Tiny example
```ts
const moves = {
  captured: ['crystallizing', 'discarded'],
  crystallizing: ['crystallized', 'captured'],
  crystallized: ['manifesting'],
  manifesting: ['completed', 'crystallized'],
} as const satisfies Record<string, readonly string[]>;
export const canMove = (from: keyof typeof moves, to: string) =>
  (moves[from] as readonly string[]).includes(to);
```
Rust typestate: `Task<Draft>::approve(self) -> Task<Approved>`; `run()` exists only on `Task<Approved>`.

## Pairs with / fights
- Pairs: functional-core (`next` is pure), event-driven (transitions emit events), result-types (illegal move = typed error), ddd-tactical (aggregate guards transitions).
- Fights: free-form status strings (`stringly_typed_namespace` smell).

## In Lev
Entity lifecycle is declared in `dna/graph.yaml#lifecycle_domains.entity` and exported from `core/domain/src/entity-lifecycle.ts` (plan revision 9, slice 1). The idea machine revival is a statechart whose guards become checks. Playbook names `state_machine` for orchestration.

Sources: David Harel, "Statecharts: A Visual Formalism for Complex Systems" (1987); XState docs (stately.ai).
