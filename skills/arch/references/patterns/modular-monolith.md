# Modular monolith

**Plain words:** one repo, one deploy (or a few binaries), many modules with enforced boundaries: public API per module, allowed import directions, checked in CI. Microservice-style separation without the network.

## Fits when
- One team or one person plus agents; no need for independent deploys.
- Boundaries matter but cross-process calls would only add latency and failure modes.
- You want to split later and need the seams proven first.

## Hurts when
- Boundaries are only in folder names; without a checker, they erode within weeks.
- One module needs a different runtime, scale or release cadence; extract it.
- The build graph is so large every change rebuilds everything.

## Cost
- Lines: a boundary checker config plus a public `index.ts` per module.
- Concepts: 3 (module, public API, allowed edge). The checker is the whole pattern.

## Tiny example
```js
// .dependency-cruiser.cjs (excerpt)
module.exports = { forbidden: [{
  name: 'domain-stays-pure',
  from: { path: '^core/domain' },
  to: { path: '^core/(exec|orchestration|daemon)' },
}]};
```

## Pairs with / fights
- Pairs: clean-architecture (direction rule), ddd-tactical (module = bounded context), vertical-slice, microkernel-plugins.
- Fights: microservices by default; shared "common" packages with no owner.

## In Lev
42 core packages plus plugins in one pnpm/turbo monorepo; import allowlist in `dna/architecture/core-boundaries/concept.yaml#dependency_direction`; `pnpm --dir core/orchestration run lint:boundary`; touched-file LOC gate. AGENTS.md notes the dependency-cruiser generator still expects an old key (known gap).

Sources: Shopify Engineering, "Deconstructing the Monolith" (2019) and "Enforcing Modularity with Packwerk" (2020); Simon Brown, "Modular monoliths" (2015).
