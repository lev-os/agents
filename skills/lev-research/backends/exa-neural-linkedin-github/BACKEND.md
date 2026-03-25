---
name: exa
version: 1.1.1
description: Exa AI wrapper for search, contents extraction, and answers with citations. Use when you need semantic search, direct page contents, or grounded answer synthesis.
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["curl","jq"]}}}
---

# Exa

Powerful Exa AI wrapper covering search, contents, and answers.

## Setup

Set `EXA_API_KEY` in your environment (e.g. `~/.env.local`):
```bash
export EXA_API_KEY="your-exa-api-key"
```

Fallback: `~/.clawdbot/credentials/exa/config.json` with `{"apiKey": "..."}`

Use the stable wrapper installed at `~/.local/bin/exa`.

## Commands

### General Search
```bash
exa search "query" [options]
```

Options (as env vars):
- `NUM=10` - Number of results (max 100)
- `TYPE=auto` - Search type: auto, neural, fast, deep
- `CATEGORY=` - Category: news, company, people, research paper, github, tweet, pdf, financial report
- `DOMAINS=` - Include domains (comma-separated)
- `EXCLUDE=` - Exclude domains (comma-separated)
- `SINCE=` - Published after (ISO date)
- `UNTIL=` - Published before (ISO date)
- `LOCATION=NL` - User location (country code)

### Examples

```bash
# Basic search
exa search "AI agents 2024"

# LinkedIn / people search
exa search "software engineer Amsterdam" --category people

# Company search
exa search "fintech startup Netherlands" --category company

# News from specific domain
exa search "Netherlands" --category news --domains "reuters.com,bbc.com"

# Research papers
exa search "transformer architecture" --category "research paper"

# Deep search
exa search "climate change solutions" --type deep

# Date-filtered news
exa search "tech layoffs" --category news --since 2026-01-01
```

### Get Content
Extract full text from URLs:
```bash
exa contents "url1" "url2"
```

### Answer

Get an answer grounded in Exa search results:
```bash
exa answer "What is the latest valuation of SpaceX?"
```

## Related Search Tools

**Exa specializes in semantic search plus answer/contents. For orchestration, use Timetravel via the skill router.**

| Tool | Specialty | Use When |
|------|-----------|----------|
| **exa** (this) | Semantic search, contents, answer | Direct Exa API access |
| **valyu** | Recursive turn-based research | `valyu research "query" --turns 5` |
| **deep-research** | Multi-query Tavily synthesis | `deep-research "query" --deep` |
| **lev-research** | Multi-perspective orchestration | `lev-research "query"` |
| **lev-find** | Unified local + external | `lev get "query" --scope=research` |
| **brave-search** | Quick web search | `brave-search "query"` |
| **tavily-search** | AI-optimized snippets | `tavily-search "query"` |
| **grok-research** | Real-time X/Twitter | `grok-research "query"` |
| **firecrawl** | Web scraping | `firecrawl scrape <url>` |
| **qmd** | Local session search | `qmd query "query"` |

**Exa's unique capabilities:**
- ✅ LinkedIn people search (`CATEGORY=people`)
- ✅ Company research (`CATEGORY=company`)
- ✅ Research papers (`CATEGORY="research paper"`)
- ✅ GitHub code search (`CATEGORY=github`)
- ✅ Neural semantic search (not just keywords)
- ✅ Full page contents extraction
- ✅ Answer generation with citations

**Integration pattern:**
```bash
# 1. Search
exa search "ML engineer Amsterdam" --category people

# 2. Pull contents
exa contents "https://example.com/profile"

# 3. Ask a grounded question
exa answer "What patterns show up across these sources?"
```

See `skill://lev-research` for comprehensive research workflows.
