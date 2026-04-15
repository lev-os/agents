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
- you need social/academic/pilot-training adapters

Implementation surface: `plugins/core-timetravel`. Run the CLI — it handles strategy selection, adapter parallelism, and synthesis internally.

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

0. First decide whether the task is local retrieval or real research.
   - Local repo/docs/tasks/session recall → `lev find` / agent-native tools, not this skill
   - Current/deep/external question → continue here
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
| Use this skill for ordinary repo search | `lev find` is the local retrieval primitive |
| Use WebSearch directly | You are a router. Call lev timetravel. |
| Spawn subagents to search | Timetravel handles parallelism internally. |
| Duplicate strategy/adapter definitions | Source of truth is `plugins/core-timetravel/src/strategy.ts`. |
| Answer from training data | No URLs = no answer. Call the CLI. |
