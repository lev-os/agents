# TLAPS and Apalache

## TLAPS

TLAPS is the TLA+ proof system.

- It is centered on the `tlapm` proof manager and backend provers.
- It is strongest today on safety-oriented proof work.
- Current official docs say it does not perform full temporal reasoning.
- Start with `tlapm --help` and the simple example `examples/Euclid.tla` in the TLAPS repo.

Use TLAPS when:
- the model has stabilized
- you need mechanically checked proofs
- the remaining obligation is no longer best explored by explicit counterexample search

## Apalache

Apalache is a symbolic model checker for TLA+.

- It translates verification problems to SMT constraints.
- It is good for bounded executions and inductive invariants over fixed finite parameters.
- It assumes finite data and bounded executions, much like TLC's finiteness assumptions.
- It is still experimental compared with TLC.

Use Apalache when:
- explicit-state exploration is the bottleneck
- the model has integer-heavy or constraint-heavy structure
- you need symbolic bounded checking rather than standard TLC exploration

## Practical split

- Start with TLC unless symbolic checking clearly buys something.
- Move to TLAPS after the checker has already burned down the obvious design mistakes.
- Do not treat TLAPS or Apalache as a substitute for a small, clear base model.
