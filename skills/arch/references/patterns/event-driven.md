# Event-driven architecture (publish/subscribe)

**Plain words:** a module announces "this happened" as a typed event; other modules react without the announcer knowing who they are.

## Fits when
- Two modules import each other only so one can tell the other something happened.
- Many reactions hang off one fact (log it, update a view, trigger a flow, notify a surface).
- Work crosses process or machine boundaries.

## Hurts when
- You need an answer back: request/reply over events is a slow, hidden function call.
- Ordering, retries and duplicates are not designed; consumers must be idempotent and they are not.
- "Event spaghetti": nobody can trace cause to effect without a tracer.

## Cost
- Lines: one event type, one emit, one handler each side.
- Concepts: 3 (event, bus, idempotent handler) plus delivery semantics (at-least-once, ordering).

## Tiny example
```ts
type LevEvent =
  | { type: 'task.stage.changed'; task_id: string; from: Stage; to: Stage }
  | { type: 'gate.failed'; gate_id: string };

bus.on('task.stage.changed', async (e) => {
  if (e.to === 'completed') await projections.refresh(e.task_id); // idempotent
});
bus.emit({ type: 'task.stage.changed', task_id: 't1', from: 'manifesting', to: 'completed' });
```

## Pairs with / fights
- Pairs: state-machines (transitions emit), event-sourcing (events become the record), cqrs (events feed read models), actor-model.
- Fights: simple direct calls inside one module; using events there adds indirection for nothing.

## In Lev
Cross-module communication is `LevEvent` only (AGENTS.md conventions); event types are kebab.dot. `core/event-dispatch` projects durable events into idempotent actions and cannot import `core/exec` (`core-boundaries/concept.yaml#event_projection`).

Sources: Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns* (2003); Martin Fowler, "What do you mean by Event-Driven?" (2017).
