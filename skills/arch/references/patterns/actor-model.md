# Actor model and supervision

**Plain words:** each long-lived worker owns its own state and a mailbox; others talk to it only by message. A supervisor restarts workers that crash, under a restart budget.

## Fits when
- Many concurrent long-running things (sessions, runs, panes, workers) each with private state.
- Crashes are expected and recovery should be a policy, not try/catch everywhere.
- You need "call with timeout" vs "fire and forget" to be explicit.

## Hurts when
- Short request/response code; actors add mailboxes to a function call.
- Shared state is the real need (a cache); actors serialize every access.
- Building an actor runtime in TS from scratch; Node's single thread already serializes.

## Cost
- Lines: a handle type, typed messages, a supervisor policy per worker kind.
- Concepts: 4 (actor, mailbox, call vs cast, supervisor + restart budget).

## Tiny example
```ts
type Msg = { kind: 'call'; q: 'status'; reply: (s: string) => void } | { kind: 'cast'; input: string };
export function spawnSession() {
  let state = 'idle';
  const inbox: Msg[] = [];
  const tick = () => { const m = inbox.shift(); if (!m) return;
    if (m.kind === 'call') m.reply(state); else state = `busy:${m.input}`; };
  return { send: (m: Msg) => { inbox.push(m); queueMicrotask(tick); } };
}
```

## Pairs with / fights
- Pairs: event-driven, state-machines (actor state is a machine), capability-based (a handle is an authority).
- Fights: functional-core when every rule moves into actor bodies; keep the rules pure and the actor thin.

## In Lev
`code-quality.yaml#otp_actor_lens` maps BEAM ideas to Lev as control-plane semantics, not a runtime dependency: SessionHandle/RunHandle, call vs cast, supervisor child_spec → owner contract with restart budget. Process supervision belongs to `core/daemon*` and `core/substrate`.

Sources: Carl Hewitt et al., "A Universal Modular ACTOR Formalism" (1973); Joe Armstrong, *Making reliable distributed systems in the presence of software errors* (2003).
