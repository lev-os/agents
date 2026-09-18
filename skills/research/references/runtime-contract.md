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

When a request clearly names people, companies, leads, markets, technical sources, or news, use the matching proposed routine in `references/domain-routines.md`. Execute its fixed stages with existing CLIs. Do not claim it is a native `lev research` strategy.

Ambiguous? Default to `quick`.

## Anti-Patterns

| Don't | Why |
|---|---|
| Use this skill for ordinary repo search | `lev find` is the local retrieval primitive |
| Use direct internet search as the first step when `lev research` is healthy | Keep the router as the primary path so adapter logs and strategy selection remain consistent. |
| Spawn subagents to search | Timetravel handles parallelism internally. |
| Duplicate strategy/adapter definitions | Source of truth is `plugins/research/src/strategy.ts`. |
| Choose providers opportunistically | The selected routine fixes stage order and preferred/fallback tools. |
| Stop after `Sources: 0` | No URLs from the router means use internet-search fallback, not no answer. |
| Answer from training data | No URLs = no answer. Call the CLI, then internet-search fallback if needed. |
| Treat synthesis-only output as sourced | Some providers synthesize without URLs; verify with source-bearing adapters or fallback search. |
