# Effect systems (effects as values)

**Plain words:** instead of doing I/O, a function returns a description of the I/O it wants, with its error types and required services in the type. A runtime runs the description. Effect-TS writes this as `Effect<Success, Error, Requirements>`.

## Fits when
- You must inspect, plan, approve or replay effects before they happen (dry runs, policy checks, receipts).
- Error channels and required services should be checked by the compiler.
- Cancellation, retry and concurrency policy repeat across many call sites.

## Hurts when
- Adopting a whole effect library: new dependency, new idioms, steep reading curve, every stack trace changes. Lev rule: no new dependencies without an explicit ask.
- Small scripts; `async` plus Result types already cover it.
- Half the codebase uses it; two ways to do everything.

## Cost
- Lines: library adoption is large; the light form (an `Effect` data type for the few effects you must govern) is small.
- Concepts: library form 6+ (Effect, Layer, Context, fibers, schedules, scopes); light form 2 (effect description, interpreter).

## Tiny example (light form, no library)
```ts
type Effect =
  | { kind: 'write_file'; path: string; body: string }
  | { kind: 'spawn'; cmd: string[] };
export const plan = (task: Task): Effect[] =>
  [{ kind: 'write_file', path: `${task.id}/exec.yaml`, body: render(task) }];
// a separate, single runner decides, executes and seals each effect
```

## Pairs with / fights
- Pairs: functional-core (core returns effects), capability-based, declarative-interpreter, result-types.
- Fights: ponytail/simplicity when adopted wholesale; ambient `await fs.writeFile` sprinkled in rules.

## In Lev
Light form already exists: `core/effect` declares, observes and settles effects (`core-boundaries/concept.yaml#effect_settlement`); `core/exec` is the blessed effectful entry. Effect-TS itself: not adopted (fit low; dependency rule).

Sources: Effect docs (effect.website); Gordon Plotkin and Matija Pretnar, "Handlers of Algebraic Effects" (2009).
