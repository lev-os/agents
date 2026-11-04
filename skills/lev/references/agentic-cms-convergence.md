# Lev agentic CMS / wiki / publisher convergence

Use this reference when Lev work drifts between `autowiki`, `cms`, `publisher`, `writer`, and `wiggum-marketer` concepts.

## Session learning

The durable architecture correction is: do **not** treat the center as a generic marketing/content-generation pipeline. Treat the center as an agent-operable structured knowledge and publishing substrate:

```text
sources / inbox
  -> canonical records
  -> graph / entity model
  -> wiki or internal CMS projection
  -> operator control plane
  -> publisher targets
  -> optional creation agents
```

Wiggum is a producer/operator in this system, not the system itself.

## Current Lev concept map

- `plugins/wiggum-marketer` owns creation loops: voice, research, ideation, draft, critique, iteration, publish-intent.
- `plugins/autowiki` owns internal structured wiki projection: raw sources, wiki pages, schema/conventions, refinement/lint/query.
- `plugins/publisher` owns downstream materialization: filesystem, Notion, site/blog/social targets, publish logs.
- `cms-control-plane` / `plugins/cms` should mean lifecycle control: approvals, schedules, routing, operator UI, state transitions. It should not own prose generation.
- `plugins/writer` is only useful if it becomes a generic WRITE primitive or thin shared interface; avoid inventing a parallel content engine without reconciling Wiggum first.

## Recommended canonical loop

```text
source change
  -> LevEvent / storage record
  -> graph projection
  -> autowiki refinement
  -> review / approval state
  -> publisher materialization
  -> measurement / feedback
```

For marketing/content generation:

```text
content need / comm / trend / research
  -> Wiggum DISCOVER / LEARN / RESEARCH / IDEATE / WRITE / CRITIQUE / ITERATE
  -> draft artifact
  -> CMS review state
  -> publisher target
```

## Practical guidance

1. Before designing a new content plugin, inspect `wiggum-marketer`, `autowiki`, `publisher`, and any `cms`/`writer` stubs.
2. Separate generation from lifecycle:
   - LLM: synthesis, voice extraction, drafting, critique, wiki refinement.
   - Code: records, IDs/slugs, schemas, provenance, events, approvals, schedules, publishing adapters, metrics.
3. Keep raw capture separate from analysis/refinement so provenance survives.
4. Do not over-normalize `.lev/` prematurely; propose the smallest dogfoodable slice first.
5. Good first slice: Telegram/input dump -> internal wiki record -> Wiggum draft -> review state -> filesystem/blog publish target.

## Pitfalls

- Do not rename `publisher` back into a full CMS just because publishing is involved.
- Do not let `writer` compete with Wiggum unless the desired abstraction is explicitly a shared primitive/interface.
- Do not confuse an internal LLM wiki, a Notion projection, and an agentic CMS control plane; they share primitives but have different responsibility boundaries.
- Do not start by installing marketing tools; start by mapping existing Lev primitives and dogfooding one end-to-end loop.
