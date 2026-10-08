# Parse, don't validate (schema at the boundary)

**Plain words:** turn untrusted input into a typed value once, at the edge. Inside, the type itself proves validity, so nobody re-checks.

## Fits when
- `unknown`, `any` or raw YAML/JSON flows past the first function.
- The same `if (!x.id)` check appears in several places.
- Config, task specs, LLM output or event payloads enter the system.

## Hurts when
- Parsing every internal call, not just the boundary: double cost, no gain.
- Schemas duplicated beside hand-written types; they drift. Derive the type from the schema (or the reverse), never both.
- Over-precise schemas for data you only forward.

## Cost
- Lines: one schema per boundary shape; types are derived.
- Concepts: 1 (boundary parse). Uses a validator already in the repo (zod in TS, serde in Rust).

## Tiny example
```ts
const TaskSpec = z.object({
  id: z.string().min(1),
  lifecycle_stage: z.enum(['ephemeral', 'captured', 'crystallizing', 'crystallized',
    'manifesting', 'completed']).optional(),
});
export type TaskSpec = z.infer<typeof TaskSpec>;
export const parseTaskSpec = (raw: unknown) => TaskSpec.safeParse(raw); // Result at the edge
```

## Pairs with / fights
- Pairs: result-types (`safeParse` returns one), ddd-tactical (value objects are parsed values), ports-and-adapters (adapters parse, core trusts).
- Fights: DTO-per-boundary: parse into the domain type directly, do not parse into a DTO and then map.

## In Lev
`code-quality.yaml#type_safety` asks that untyped values stay at boundaries; `any_count` gate soft 10 / hard 25. Task readiness and the workstream zod schema (`core/workstream/src/schema.ts`) are the live boundary parsers. LLM output is an observation until parsed and judged (translator boundary).

Source: Alexis King, "Parse, don't validate" (lexi-lambda.github.io, 2019).
