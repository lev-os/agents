---
name: brave-search
description: Web search and content extraction via Brave Search API. Use for searching documentation, facts, or any web content. Lightweight, no browser required.
---

# Brave Search

Headless web search and content extraction using Brave Search. No browser required.

## Setup

Run once before first use:

```bash
cd ~/Projects/agent-scripts/skills/brave-search
npm ci
```

Needs env: `BRAVE_API_KEY`.

## Search

```bash
./search.js "query"                    # Basic search (5 results)
./search.js "query" -n 10              # More results
./search.js "query" --content          # Include page content as markdown
./search.js "query" -n 3 --content     # Combined
```

## Extract Page Content

```bash
./content.js https://example.com/article
```

Fetches a URL and extracts readable content as markdown.

## Output Format

```
--- Result 1 ---
Title: Page Title
Link: https://example.com/page
Snippet: Description from search results
Content: (if --content flag used)
  Markdown content extracted from the page...

--- Result 2 ---
...
```

## When to Use

- Searching for documentation or API references
- Looking up facts or current information
- Fetching content from specific URLs
- Any task requiring web search without interactive browsing

## Related Search Tools

**brave-search is for quick lookups. For deeper research:**

| Tool | Use When | Example |
|------|----------|---------|
| **valyu** | Recursive turn-based research | `valyu research "query" --turns 5` |
| **deep-research** | Multi-query synthesis | `deep-research "query" --deep` |
| **lev-research** | Multi-perspective analysis | `lev-research "query" --template=tech_assessment` |
| **lev-find** | Local + external unified | `lev get "query" --scope=research` |
| **tavily-search** | AI-optimized snippets | `tavily-search "query" --deep` |
| **exa-plus** | Neural search, GitHub, papers | `exa search "query" --category=research` |
| **grok-research** | Real-time X/Twitter | `grok-research "query"` |
| **firecrawl** | Content extraction | `firecrawl scrape <url>` |

**When to use brave-search:**
- ✅ Quick documentation lookups
- ✅ API references
- ✅ Fast fact-checking
- ❌ Deep research (use deep-research or valyu)
- ❌ Multi-perspective (use lev-research)
- ❌ Social sentiment (use grok-research)

See `skill://lev-research` for comprehensive research workflows.
