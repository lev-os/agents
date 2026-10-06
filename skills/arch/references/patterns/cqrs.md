# CQRS (separate write model and read model)

**Plain words:** the shape you write with differs from the shape you read with. Commands change the record; queries read from a view built for the question.

## Fits when
- Reads and writes have very different shapes or loads (a dashboard over an append-only log).
- Read views can be rebuilt and may lag a little.
- One write record feeds several unrelated views (status line, HUD, report).

## Hurts when
- Applied to the whole system. Fowler: "for most systems CQRS adds risky complexity."
- Users need read-your-write right away and the view is eventually consistent.
- Two models are maintained by hand instead of derived.

## Cost
- Lines: a projection function per view plus a rebuild trigger.
- Concepts: 3 (command, query, projection) plus staleness.

## Tiny example
```ts
// write side: the ledger (see event-sourcing)
// read side: a derived, rebuildable view
export function buildStatusView(log: RunEvent[]): Record<string, 'running' | 'sealed'> {
  const view: Record<string, 'running' | 'sealed'> = {};
  for (const e of log) view[e.run_id] = e.kind === 'sealed' ? 'sealed' : 'running';
  return view; // never written back; deleting it loses nothing
}
```

## Pairs with / fights
- Pairs: event-sourcing, event-driven (events update views).
- Fights: modular-monolith simplicity when one table would do; any case where the "view" becomes a second source of truth (split-brain).

## In Lev
Already present in light form: `core/telemetry` builds rebuildable read models and "a projection never certifies or replaces an authority record" (`core-boundaries/concept.yaml#telemetry_projection`). Use the word only when a view is truly separate; do not add command buses.

Source: Martin Fowler, "CQRS" (martinfowler.com/bliki/CQRS.html, 2011); Greg Young.
