---
name: research
description: "Use when any research, search, or information gathering is needed."
---

# Lev Research

Thin router over `plugins/core-timetravel`. Run the CLI — it handles strategy selection, adapter parallelism, and synthesis internally.

## Usage

```bash
lev timetravel --help
```

When published to npm, this becomes:

```bash
npx @lev-os/lev timetravel --help
```

Run that command to see available subcommands, strategies, adapters, and options. The CLI is the documentation. Do not duplicate its interface here.

## For agents

1. Classify the query (quick/full/deep/max/social/academic/pilot-training) using the signal words below
2. Print: `research-route: <strategy> | lev timetravel search -s <strategy>`
3. Run `lev timetravel search "<query>" -s <strategy>` via Bash
4. Return results. Synthesize for deep/max/academic.

### Signal word classification

| Signal Words | Strategy |
|---|---|
| "search", "lookup", "find", "what is" | `quick` |
| "twitter", "reddit", "trending", "sentiment" | `social` |
| "student pilot", "how they learned", "training material", "ATC phraseology resources", "free youtube", "learning styles", "corpus" (aviation training) | `pilot-training` |
| "paper", "arxiv", "academic", "scholarly" | `academic` |
| "research", "deep", "comprehensive", "analyze", "compare", "investigate" | `deep` |
| "complete analysis", "exhaustive", "all angles" | `max` |

Ambiguous? Default to `quick`.

## Anti-Patterns

| Don't | Why |
|---|---|
| Use WebSearch directly | You are a router. Call lev timetravel. |
| Spawn subagents to search | Timetravel handles parallelism internally. |
| Duplicate strategy/adapter definitions | Source of truth is `plugins/core-timetravel/src/strategy.ts`. |
| Answer from training data | No URLs = no answer. Call the CLI. |
