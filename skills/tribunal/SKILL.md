---
name: tribunal
description: "Run one neutral prompt independently across every discovered model from selected CLI providers, then compare all answers and failures. Use for naming, short judgment questions, sanity checks, and cross-model test matrices; never use it to execute coding work."
---

# Tribunal

Collect independent opinions, not implementation. Run the same short prompt
across the full reachable model roster for the selected providers, preserve the
raw matrix, and summarize convergence without hiding dissent or failed cells.

Read [references/cli-runners.md](references/cli-runners.md) before dispatch. It
defines detection, model discovery, cache provenance, and current headless
invocations.

## 1. Frame One Question

Write a neutral prompt under 200 words. Include the necessary context without
stating a preferred answer. Ask every model for the same compact shape:

```json
{"answer":"candidate or decision","reason":"one short reason"}
```

Do not rephrase per model. Do not ask models to coordinate.

## 2. Resolve the Full Roster

Run `bin/detect-runners --json`. Use `--refresh` when the caller asks for live
state or the cached provenance is stale.

- If the caller names providers or models, use exactly those selections.
- If the caller gives only a provider count `N`, choose `N` installed runners
  with non-empty rosters in stable detector order and disclose the choices.
- If providers are selected without models, dispatch every model returned for
  each provider. Do not sample weakest/middle/strongest and do not apply a budget
  tier.
- If neither providers nor `N` are named, default to three installed runners and
  every model from each. Prefer Claude, Codex, and a Google-capable runner when
  available so small and frontier models are both represented.
- Treat OpenCode and Pi as aggregate catalogs. Select them automatically only
  when needed to fill the requested `N`; when explicitly selected, honor their
  complete discovered roster.
- If an installed runner cannot enumerate models, emit an unavailable roster row
  unless the caller supplied explicit model IDs. Never guess completeness.

## 3. Dispatch in Parallel

Create one process per `(runner, model)` cell with the identical prompt. Use the
read-only or no-tools invocation from the runner reference. Give every cell its
own output and log file. Launch independent cells concurrently when the host can
track them safely.

Tribunal does not edit files, execute implementation tasks, or verify code. Route
that work to a coding-agent workflow instead.

## 4. Collect Every Outcome

Wait for every cell to finish or time out. Record runner, model, answer, reason,
status, and error for every cell. Never drop failed adapters or show only the
first successful answer.

Present:

1. The complete model-by-model answer matrix.
2. Exact answer counts with explicit denominators.
3. A provider-balanced view so a provider exposing more model variants does not
   silently dominate the conclusion.
4. Dissent, unavailable rosters, timeouts, and parse failures.

Classify the result as unanimous, convergent, split, or divergent. Treat
convergence as evidence, not automatic truth.

## Optional Fusion

Only when the caller asks for fusion, anonymize the collected answers and run a
separate synthesizer after the raw matrix is complete. Label synthesis as an LLM
interpretation and keep all source answers visible. Exact normalization, counts,
failures, and provenance remain deterministic.
