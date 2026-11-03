# Plan-first SDLC discovery and adapter convergence

Session source: 2026-07-12 Plan-vs-Task deliberation for Lev SDLC file + Beads adapters.

## Durable decision

Use a **Plan-first complexity router** for SDLC discovery and execution routing.

- `Plan` is the canonical operator-facing first-discovery entity.
- `Task` is not canonical at the planning edge; it survives as a legacy compatibility alias for an Act-ready `ExecutionPacket`.
- `ExecutionPacket` is the compiled Act-ready leaf handed to Act/runtime surfaces.
- `Proposal` / intake is pre-plan intent or transition material, not execution authority.
- `Workstream` is grouping/campaign/projection, not the first actionable work noun.
- Core invariant stays `Plan → Act → Verify`.
- Domain plugins such as `plugins/sdlc`, video, etc. extend the loop with domain overlays instead of replacing it.

## Recommended overlay shape

```text
Proposal / Intake → Design → Spec → Plan → ExecutionPacket → Run → Receipt
```

Simple work can remain a one-file plan. Complex work can splinter Plan into Design → Spec → Plan, FlowMind graphs, execution packets, runs, receipts, and projections.

## Planning workflow

When the user is debating `task` vs `plan`, do not immediately rename all surfaces or hard-cut existing task bundles.

1. Run a small discovery eval before changing canon:
   - basic + task framing
   - advanced + task framing
   - basic + plan framing
   - advanced + plan framing
2. Synthesize using a CDO/architecture lens.
3. Reduce with POV/forced-framing into one governing axiom.
4. Write the result as:
   - ADR/decision
   - eval artifact
   - entity contract sketch
   - router spec sketch
   - updated workstream/plan state
5. Keep compatibility shims until file adapter and Beads adapter parity are proven.

## Pitfalls

- Do not treat `task` as the domain root just because existing directories or Beads use the word task.
- Do not hard-rename `task → proposal`; proposal is earlier than the Act-ready leaf.
- Do not make plan markdown-only. `Plan` is a facade that can escalate into richer bundles and proofs.
- Do not let SDLC plugin work duplicate core loop/proof authority. Core owns the loop/proof substrate; SDLC owns domain nouns and adapter semantics.
