# Result types and railway-oriented flow

**Plain words:** a function that can fail returns `{ ok: true, value } | { ok: false, error }` instead of throwing. Steps chain on the success track; the first failure switches to the error track and carries a typed reason.

## Fits when
- Failure is expected and part of the domain (validation, gate fail, provider refused).
- Callers must handle each failure kind differently; `catch (e: unknown)` loses that.
- Silent fallbacks keep hiding errors.

## Hurts when
- Wrapping truly exceptional faults (out of memory, programmer bugs); let those throw.
- Deep generic combinator stacks (`flatMap(mapErr(andThen(...)))`) in a team that reads plain `if`.
- Mixing styles in one module: half throw, half Result.

## Cost
- Lines: one union type, an early-return `if (!r.ok) return r` per step.
- Concepts: 1-2 (discriminated union; optional chaining helpers). No library needed in TS; Rust has it built in.

## Tiny example
```ts
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
type GateError = { kind: 'hollow' } | { kind: 'failed'; check: string };

function runGate(c: Check): Result<Verdict, GateError> {
  if (c.shouldFailPasses) return { ok: false, error: { kind: 'hollow' } };
  return c.pass ? { ok: true, value: 'pass' } : { ok: false, error: { kind: 'failed', check: c.id } };
}
```

## Pairs with / fights
- Pairs: parse-dont-validate, functional-core, state-machines (a transition returns a Result), effect-systems (a typed error channel generalized).
- Fights: exception-heavy frameworks at the edge; translate once in the adapter.

## In Lev
`EvalDecision` is a two-arm union and the error arm carries no verdict field (AGENTS.md failure mode 6). `code-quality.yaml#explicit_failure_policy` and the `discriminated_result_union` playbook entry ask for this shape.

Sources: Scott Wlaschin, "Railway Oriented Programming" (fsharpforfunandprofit.com, 2014); Rust `std::result`.
