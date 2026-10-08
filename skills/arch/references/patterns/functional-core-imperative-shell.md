# Functional core, imperative shell

**Plain words:** decisions are pure functions over plain values; a thin outer layer does the I/O (read, call the core, write what it returned).

## Fits when
- A handler mixes "what should happen" with reading files, spawning, or calling a model.
- Tests need mocks of time, disk or network just to check a rule.
- The same rule must run from CLI, daemon, test and replay.

## Hurts when
- The logic is mostly I/O orchestration (retry, stream, backpressure); the "core" ends up empty and the split is ceremony.
- Data needed by the decision is huge or lazy; loading it all up front to stay pure is wasteful.

## Cost
- Lines: near zero; you move code, you do not add it.
- Concepts: 1 (pure vs effectful). Cheapest pattern in this folder.

## Tiny example
```ts
// core: pure
export function nextStage(task: Task, checks: CheckResult[]): Stage {
  return checks.every((c) => c.pass) ? advance(task.stage) : task.stage;
}
// shell: effects
export async function handler(args: { id: string }) {
  const task = await readTask(args.id);
  const checks = await runChecks(task);
  await writeStage(args.id, nextStage(task, checks));
}
```

## Pairs with / fights
- Pairs: ports-and-adapters (the shell is the adapters), result-types, parse-dont-validate, state-machines (the transition function is the core).
- Fights: nothing directly; it is the default. Overkill only in pure glue code.

## In Lev
Named in `dna/standards/code-quality.yaml#pattern_playbook` for IO-heavy handlers, with humble object. `core/domain` is the pure side by invariant (`dna/architecture/core-boundaries/concept.yaml#pure_domain`).

Source: Gary Bernhardt, "Boundaries" (2012) and the "Functional Core, Imperative Shell" screencast.
