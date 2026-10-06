# Capability-based security (object capabilities, least authority)

**Plain words:** a component can only act on what it was handed a reference to. No ambient authority: no reaching for a global `fs`, `process.env` or network client. Granting = passing the reference.

## Fits when
- Untrusted or semi-trusted code runs: plugins, model-written code, tool calls.
- You must answer "what can this worker possibly touch?" by reading its inputs.
- Effects need sealing and audit (who was allowed to write what).

## Hurts when
- The runtime has ambient authority everywhere (Node `require('fs')`) and nothing enforces the rule; it is then a convention, not security. Pair with a sandbox or a lint.
- Every helper takes ten capability arguments; group them into one narrow port per job.

## Cost
- Lines: same as dependency injection; the difference is discipline (no globals) and narrowing (pass `readOnly(files)`, not `files`).
- Concepts: 2 (capability, attenuation). Enforcement costs more: sandbox, lint rule or process boundary.

## Tiny example
```ts
type ReadCap = { read(path: string): Promise<string> };
const attenuate = (files: FilePort, root: string): ReadCap => ({
  read: (p) => (p.startsWith(root) ? files.read(p) : Promise.reject(new Error('denied'))),
});
await runPlugin(plugin, { files: attenuate(localFileAdapter, '/repo/plugins/x') });
```

## Pairs with / fights
- Pairs: dependency-injection (same mechanism), ports-and-adapters, microkernel-plugins, effect-systems (effects declared up front).
- Fights: service locators and global singletons; "convenience" imports of `child_process`.

## In Lev
Shadow-exec is a named failure: any spawn outside `core/exec`, `core/substrate`, `core/daemon*` is BLOCK (AGENTS.md failure mode 1). `core/orchestration` owns capability-policy evaluation (`core-boundaries/concept.yaml#orchestration_policy`); `core/effect` declares and settles effects.

Sources: Mark S. Miller, *Robust Composition* (PhD thesis, 2006); Jonathan Rees, "A Security Kernel Based on the Lambda-Calculus" (1995).
