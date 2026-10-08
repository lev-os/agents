# Dependency injection and the composition root

**Plain words:** a function or object receives what it needs as arguments instead of importing a concrete thing. All the real wiring happens once, at the entry point (the composition root).

## Fits when
- Sprawling imports: module A imports B's concrete client, which imports C's config loader, and tests must mock the module graph.
- The same code runs with different adapters (test, CLI, daemon, replay).
- You want one place to read "what is actually plugged in".

## Hurts when
- A container with decorators, string tokens and lifetime scopes for 12 services. Lookup at runtime hides the graph; errors move from compile time to start time.
- Parameters threaded through ten layers ("parameter drilling"): the object graph is too deep, not DI's fault, but it shows up here.
- Pure helpers get injected too; inject effects, call pure functions directly.

## Cost
- Lines: one extra parameter or a `deps` object; one wiring file per entry point.
- Concepts: 2 (inject, composition root). No container needed ("pure DI").

## Tiny example
```ts
type Deps = { files: FilePort; clock: () => Date };
export const makeTaskService = ({ files, clock }: Deps) => ({
  async touch(id: string) { await files.write(`${id}.stamp`, clock().toISOString()); },
});
// composition root (main / handler entry)
const service = makeTaskService({ files: localFileAdapter, clock: () => new Date() });
```

## Pairs with / fights
- Pairs: ports-and-adapters (what gets injected), functional-core (inject only into the shell), capability-based (passing a dep is granting authority).
- Fights: convention-over-configuration discovery when both decide wiring; service locators (a global registry you pull from is DI's opposite).

## In Lev
`core/reconciler` is ports-injected (`dna/index.yaml` catalog). Prefer a `deps` parameter over a new cross-package import edge; every new edge must be in the allowlist (`core-boundaries/concept.yaml`).

Sources: Mark Seemann, *Dependency Injection in .NET* (2011), "Composition Root"; Seemann, "Pure DI" (blog.ploeh.dk, 2014).
