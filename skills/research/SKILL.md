---
name: research
description: "Use when any research, search, or information gathering is needed."
---

# Lev Research

Deep/current/external branch of the unified `lev find` story.

Use `lev find` first for local repo/operator truth.

Use `lev-research` when:
- the answer depends on current web data
- the user asked for deep/comparative/exhaustive research
- you need multi-source synthesis beyond local indexes
- you need social or academic adapters

Implementation surface: `plugins/timetravel` with root Poly bindings over `core-timetravel`.
Use `lev research` as the northbound runtime surface. `lev timetravel` remains the
underlying runtime/compat surface.

## Usage

```bash
lev research --help
```

When published to npm, this becomes:

```bash
npx @lev-os/lev research --help
```

Run that command to see available subcommands, strategies, adapters, and options. The CLI is the documentation. Do not duplicate its interface here.

## For agents

0. First decide whether the task is local retrieval or real research.
   - Local repo/docs/tasks/session recall → `lev find` / agent-native tools, not this skill
   - Current/deep/external question → continue here
1. Classify the query (quick/full/deep/max/social/academic) using the signal words below
2. For `deep`, `max`, and `academic`, first build a short research prompt package:
   objective, audience, scope, known context, sub-questions, evidence contract, and output contract.
   Use the deep research prompt contract below and the runtime strategy metadata
   in `plugins/timetravel/src/strategy.ts`.
   Historical `lev research` outputs and generated results are AutoWiki intake
   material, not canonical guidance. Treat them as raw sources for the wiki
   projection unless they have been source-reviewed and promoted.
3. When you need to inspect the package before spending adapter calls, run:
   `lev research "<query>" -s <strategy> --prompt-plan-only`
4. When the user asks for FlowMind handling or recursive research, run:
   `lev research "<query>" -s <strategy> --flow=deep-research --flow-plan-only`
   first, then remove `--flow-plan-only` when a bounded FlowMind run is desired.
5. Print: `research-route: <strategy> | lev research -s <strategy>`
6. Run `lev research "<query>" -s <strategy>` via Bash. Prompt planning is
   default-on for `deep`, `max`, and `academic`; completed runs wikify by
   default into the project AutoWiki raw layer. Use `--no-prompt-plan` only
   when terse output is required and `--no-wikify` only when the run must not
   touch wiki intake.
7. If the CLI returns sources/URLs, return those results. Synthesize for deep/max/academic.
8. If the CLI returns no sources/URLs, reports no adapters, errors, or otherwise cannot reach the web, immediately fall back to the agent's available internet search tools (`web_search`, `WebSearch`, browser/search MCP, or equivalent). Do not stop at `Sources: 0`.
9. Print the fallback in the route line or next status line:
   - `research-route: <strategy> | lev research -s <strategy> | fallback: internet-search (<reason>)`
10. Return only source-backed results. If both CLI and fallback search fail, say that no live sources could be reached and include the exact failure mode.

### Internet fallback contract

`lev research` is the preferred router, not a blocker. The job of this skill is live research. When the router cannot produce URLs, use whatever internet search capability is available in the current agent runtime.

Minimum fallback behavior:
- Run at least one web search query for quick/full requests and multiple targeted queries for deep/max requests.
- Open or inspect primary sources when accuracy depends on exact wording.
- Include source URLs in the answer.
- Do not answer from training data when the user asked for current or external information.

### Deep research prompt contract

Deep research quality depends on the input contract. Before running `deep`, `max`,
or `academic`, compress the user request into:

```text
Objective: one precise research question.
Audience: who will use the answer and what decision it supports.
Scope: timeframe, geography, domains, source classes, exclusions.
Known context: assumptions, prior decisions, baseline facts, or files.
Sub-questions: 3-7 focused queries that can be searched independently.
Evidence contract: source quality, recency, citation, and contradiction rules.
Output contract: structure, confidence labels, limits, and open questions.
```

Provider-specific rules belong in the runtime strategy metadata and AutoWiki
intake/projection, not in this skill directory. If provider behavior matters,
verify against current provider docs and cite the URLs you used.

### Signal word classification

| Signal Words | Strategy |
|---|---|
| "search", "lookup", "find", "what is" | `quick` |
| "twitter", "reddit", "trending", "sentiment" | `social` |
| "paper", "arxiv", "academic", "scholarly" | `academic` |
| "research", "deep", "comprehensive", "analyze", "compare", "investigate" | `deep` |
| "complete analysis", "exhaustive", "all angles" | `max` |

Ambiguous? Default to `quick`.

## Anti-Patterns

| Don't | Why |
|---|---|
| Use this skill for ordinary repo search | `lev find` is the local retrieval primitive |
| Use direct internet search as the first step when `lev research` is healthy | Keep the router as the primary path so adapter logs and strategy selection remain consistent. |
| Spawn subagents to search | Timetravel handles parallelism internally. |
| Duplicate strategy/adapter definitions | Source of truth is `plugins/timetravel/src/strategy.ts`. |
| Stop after `Sources: 0` | No URLs from the router means use internet-search fallback, not no answer. |
| Answer from training data | No URLs = no answer. Call the CLI, then internet-search fallback if needed. |
| Treat synthesis-only output as sourced | Some providers synthesize without URLs; verify with source-bearing adapters or fallback search. |
