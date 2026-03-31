---
name: research
description: "Use when any research, search, or information gathering is needed."
---

# Lev Research

Thin router over `plugins/core-timetravel`. Classify, announce, execute via CLI. Done.

## How it works

1. Classify query complexity into a strategy
2. Print the route line
3. Call `timetravel search` or `timetravel flowmind-poc` via Bash
4. Return results (synthesize for deep/max/academic)

## Strategy Classification

Parse signal words from the user's query:

| Signal Words | Strategy |
|---|---|
| "search", "lookup", "find", "what is" | `quick` |
| "twitter", "reddit", "trending", "sentiment" | `social` |
| "paper", "arxiv", "academic", "scholarly" | `academic` |
| "research", "deep", "comprehensive", "analyze", "compare", "investigate" | `deep` |
| `$research` with no override | `deep` |
| "complete analysis", "exhaustive", "all angles" | `max` |

Ambiguous? Default to `quick`. Never ask the user to pick a mode.

## Execution

### Step 1: Announce the route

Print exactly one line before calling any backend:

```
research-route: <strategy> | timetravel search -s <strategy>
```

### Step 2: Execute via timetravel CLI

The CLI lives at `plugins/core-timetravel`. Run from the leviathan repo root:

```bash
# Standard search (quick/full/deep/max/social/academic)
npx timetravel search "<query>" -s <strategy>

# Deep research with recursive fan-out (deep/max only, when depth matters)
npx timetravel flowmind-poc "<query>" -s deep --max-depth 3 --fanout 5 --max-queries 12

# Single adapter override
npx timetravel search "<query>" -a valyu

# Check what adapters are available
npx timetravel status
```

Strategy-to-backend mapping is defined in `plugins/core-timetravel/src/strategy.ts`:

| Strategy | Adapters | Mode |
|---|---|---|
| `quick` | brave, tavily | first-success |
| `full` | brave, firecrawl, perplexity | parallel |
| `deep` | valyu, perplexity, exa | parallel + synthesizer |
| `max` | brave, firecrawl, perplexity, exa, valyu | parallel + synthesizer |
| `academic` | arxiv, exa, perplexity | parallel |
| `social` | grok, hackernews, scrapecreators | parallel |

Do NOT duplicate this mapping. The CLI is the source of truth.

### Step 3: Return results

- `quick`/`social`: Return JSON results directly with URLs
- `full`: Merge results grouped by adapter
- `deep`/`max`/`academic`: Synthesize with this structure:
  1. Executive summary (2-3 sentences)
  2. Key findings (numbered, each with source citation)
  3. Evidence table (claim | source | confidence)
  4. Open questions
  5. Sources (numbered URLs)

Every claim needs a source URL from the timetravel output. No source = no claim.

## Social Research

For social/trending queries, timetravel has a dedicated surface:

```bash
npx timetravel social search "<query>" --platforms reddit,tiktok,x --results 50
```

## Workflow Profiles

For advanced deterministic workflows:

```bash
npx timetravel workflow list          # See available profiles
npx timetravel workflow explain <id>  # Dry-run a workflow
npx timetravel workflow run <id> -q "<query>"
```

## Anti-Patterns

| Excuse | Reality |
|--------|---------|
| "I'll just use WebSearch directly" | You are a router. Call `timetravel search`. |
| "The MCP tool is faster" | There are no MCP fallbacks. Timetravel CLI is the backend. |
| "I'll spawn subagents to search" | Timetravel handles parallelism internally. Call it once. |
| "I already know the answer" | Training data has no URLs. Call timetravel. |
| "Let me search first to understand" | That IS the quick strategy. If classified as deep, run deep. |
| "One source is enough" | quick = first-success is fine. deep/max require the full adapter set. |
| "I need to ask which mode" | Default to quick. The user gave you a query, not a quiz. |

## Adapter Health

Before blaming "no results", check adapter availability:

```bash
npx timetravel status
npx timetravel adapters
```

If adapters are missing API keys, report which ones are down. Don't silently degrade.
