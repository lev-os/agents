---
name: tavily
description: AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents.
homepage: https://tavily.com
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["node"],"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---

# Tavily Search

AI-optimized web search using Tavily API. Designed for AI agents - returns clean, relevant content.

## Search

```bash
node {baseDir}/scripts/search.mjs "query"
node {baseDir}/scripts/search.mjs "query" -n 10
node {baseDir}/scripts/search.mjs "query" --deep
node {baseDir}/scripts/search.mjs "query" --topic news
```

## Options

- `-n <count>`: Number of results (default: 5, max: 20)
- `--deep`: Use advanced search for deeper research (slower, more comprehensive)
- `--topic <topic>`: Search topic - `general` (default) or `news`
- `--days <n>`: For news topic, limit to last n days

## Extract content from URL

```bash
node {baseDir}/scripts/extract.mjs "https://example.com/article"
```

Notes:
- Needs `TAVILY_API_KEY` from https://tavily.com
- Tavily is optimized for AI - returns clean, relevant snippets
- Use `--deep` for complex research questions
- Use `--topic news` for current events

## Related Search Tools

**tavily-search is for single-query AI-optimized search. For more:**

| Tool | Use When | Example |
|------|----------|---------|
| **deep-research** | Multi-query Tavily synthesis | `deep-research "query" --deep` (uses this + more) |
| **valyu** | Turn-based recursive research | `valyu research "query" --turns 5` |
| **lev-research** | Multi-perspective orchestration | `lev-research "query"` |
| **lev-find** | Unified local + external | `lev get "query" --scope=research` |
| **brave-search** | Quick web lookups | `brave-search "query"` |
| **exa-plus** | Neural search, GitHub, papers | `exa search "query"` |
| **grok-research** | Real-time X/Twitter | `grok-research "query"` |
| **firecrawl** | Content extraction | `firecrawl scrape <url>` |
| **qmd** | Local session search | `qmd query "query"` |

**Tavily hierarchy:**
- **tavily-search** (this) - Single query, clean snippets
- **deep-research** - Multi-query orchestration using Tavily backend

**When to use tavily-search:**
- ✅ Quick AI-optimized results
- ✅ Clean snippets for LLM context
- ✅ Current events with `--topic news`
- ❌ Multi-query synthesis (use deep-research)
- ❌ Turn-based refinement (use valyu)

See `skill://deep-research` for comprehensive Tavily workflows.
