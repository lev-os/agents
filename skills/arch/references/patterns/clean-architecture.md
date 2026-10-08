# Clean architecture (and onion)

**Plain words:** concentric rings; source code dependencies point only inward, toward the domain. Entities in the middle, use cases around them, frameworks and I/O outside.

Onion architecture (Palermo, 2008) is the same dependency rule with different ring names; treat them as one pattern.

## Fits when
- Framework or transport churn must not touch business rules.
- Several packages need one direction of import, checkable by a tool.
- Domain objects carry real behavior worth protecting.

## Hurts when
- Applied in full: request DTO, response DTO, presenter, view model, mapper per ring. Four copies of one shape and a mapper for each boundary. This is the cruft JP rejects.
- CRUD-shaped code with no rules: the rings hold nothing.
- "Use case" classes that are one-line pass-throughs.

## Cost
- Lines: the dependency rule is free; every extra ring with its own model costs a type plus a mapper per crossing.
- Concepts: 4 rings in the book; keep 2 (domain, everything else).

## Take / leave
- Take: the dependency rule; rich domain objects; ports owned by the inner ring.
- Leave: per-boundary DTOs, presenters, interactor-per-verb. Pass the domain type across the boundary unless a wire format forces a different shape, then parse at the edge once.

## Tiny example
```ts
// inner: domain type, no imports from outer rings
export type Workstream = { id: WorkstreamId; stage: Stage; tasks: TaskId[] };
// outer: adapter imports inward, never the reverse
import type { Workstream } from '@lev-os/domain';
export const toYaml = (w: Workstream) => yaml.stringify(w);
```

## Pairs with / fights
- Pairs: ports-and-adapters (same idea, fewer rings), ddd-tactical (what lives in the center), modular-monolith (enforces the rule between packages).
- Fights: vertical-slice when rings are imposed inside every slice; DTO-per-layer fights conciseness.

## In Lev
Import edges point inward: surfaces → exec/orchestration → effect/eval/ledger → ... → domain → utils/uri (AGENTS.md). Allowlist lives in `dna/architecture/core-boundaries/concept.yaml`, whose derivation names clean-architecture dependency direction.

Sources: Robert C. Martin, "The Clean Architecture" (2012) and *Clean Architecture* (2017); Jeffrey Palermo, "The Onion Architecture" (2008).
