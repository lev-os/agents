# Event sourcing (append-only log as the record)

**Plain words:** store every change as an event appended to a log; current state is a fold over the log. You never update in place, so you can replay, audit and rebuild.

## Fits when
- "What happened, in what order, and why" is a product requirement (receipts, audit, proof).
- You must rebuild views or recover after a crash by replay.
- Writes are naturally events already (runs, effects, verdicts).

## Hurts when
- Applied to plain records nobody audits; you pay for replay you never use.
- Event schemas change and old events must still replay: versioning and upcasting are forever work.
- Reads need the current state fast and you have no snapshot or projection.

## Cost
- Lines: append function, fold function, snapshot (later).
- Concepts: 4 (event, stream, fold/projection, schema version). High lifetime cost per stream; use it for few streams.

## Tiny example
```ts
type RunEvent = { seq: number; kind: 'started' | 'step' | 'sealed'; at: string; data?: unknown };
export const append = (log: RunEvent[], e: Omit<RunEvent, 'seq'>) =>
  [...log, { ...e, seq: log.length }];
export const status = (log: RunEvent[]) =>
  log.reduce<'running' | 'sealed' | 'none'>(
    (s, e) => (e.kind === 'sealed' ? 'sealed' : e.kind === 'started' ? 'running' : s), 'none');
```

## Pairs with / fights
- Pairs: cqrs (log is the write side, views the read side), event-driven, functional-core (fold is pure), state-machines.
- Fights: hand-edited state files; mutable YAML that is also called the record.

## In Lev
`core/execution-ledger` is an append-only JSONL run store, and only `core/exec` writes the ledger (`dna/index.yaml` catalog; AGENTS.md). Keep event sourcing to the ledger; work entities (task, workstream YAML) are state files, and that is fine.

Sources: Martin Fowler, "Event Sourcing" (2005); Greg Young, "CQRS Documents" (2010).
