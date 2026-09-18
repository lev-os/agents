---
name: research
description: "Use when current external facts, source-backed comparisons, investigations, or recent community evidence are needed."
skill_type: router
---

# Research

Use `lev find` or native retrieval for local code, documents, tasks and sessions.
For external research, select one method, print its route, and follow its stages.
Only this root is the research entry point; child methods load conditionally.

## Select the method

`research --sherlock` and `research --last30` are skill invocation syntax.
They are not `lev research` CLI flags. Inspect live help before runtime calls.

| Request | Load | Accepted output |
|---|---|---|
| Explicit `--sherlock`, dossier, OSINT, multi-round investigation or resume | [Sherlock](references/sherlock/method.md) | Source-bearing investigation state, deductions, gaps and local dashboard |
| Explicit `--last30`, last 30 days, recent community testimony or engagement | [Last30](references/last30.md) | Dated platform evidence, coverage, source URLs and provider gaps |
| Ordinary external question | [Classifier](nodes/classify.md), then its selected node | Source-backed results from the fixed routine |
| Aviation training resources/corpus | [Pilot training](references/pilot-training.md) | Sourced learning resources; no corpus acceptance claim |

Explicit selectors take precedence. If both child selectors are supplied,
resolve which deliverable is required before spending provider calls. A date
mentioned as background alone does not select last30. A code investigation
alone remains local retrieval. Ordinary "deep research" uses the deep routine.

## Execute the ordinary routine

1. Read the selected routine under `nodes/`; domain routines load
   [domain contracts](references/domain-routines.md). These domain contracts
   are not native CLI strategies. Follow fixed stages and fallback order.
2. For deep/max/academic, load [prompt and evidence contracts](references/runtime-contract.md)
   and prepare objective, audience, scope, context, subquestions, evidence and output.
3. Run `lev research --help`. Implementation is `plugins/research`; compatibility
   routing through `lev timetravel` does not change the northbound command.
   Strategies/providers are owned by `plugins/research/src/strategy.ts`.
4. Inspect planned prompts with `lev research "<query>" -s <strategy> --prompt-plan-only`
   when appropriate. Print `research-route: <routine> | lev research -s <strategy>`.
5. Execute `lev research "<query>" -s <strategy>`. Default deep prompt planning
   and AutoWiki raw intake remain in place. Use `--no-wikify` for a no-intake run.
   Raw outputs are evidence, not promoted guidance.
6. If the CLI errors, lacks adapters or yields no URLs, immediately use available
   internet-search tools following [the fallback contract](references/runtime-contract.md).
   Print the failure and fallback; do not substitute an unsourced answer.
7. Return source URLs, findings, uncertainty and remaining gaps. A completed
   process, synthesis without URLs or fixture success does not prove live research.

The existing `--flow=deep-research` route is a prompt-compilation/recursive-search
POC. Do not describe it as execution of arbitrary graph nodes. Sherlock's method
requires its own verified graph route and reports node outcomes.

## Acceptance

Preserve source provenance and observation/inference distinctions. Show requested
versus observed provider coverage and partial failures. Budget or scope expansion
requires a human decision. Save only artifacts authorized by the selected method;
local dashboard creation does not authorize external publication. Evaluation
requirements and current evidence live in [qualification](references/evaluation.json).

Load [tool catalog](references/tool-catalog.md) only when inspecting capability
availability. Catalog discovery does not authorize changing provider order.
