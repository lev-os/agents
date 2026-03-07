---
name: exa-plus
version: 1.0.0
description: Neural web search via Exa AI. Search people, companies, news, research, code. Supports deep search, domain filters, date ranges.
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["curl","jq"]}}}
---

# Exa - Neural Web Search

Powerful AI-powered search with LinkedIn, news, research papers, and more.

## Setup

Set `EXA_API_KEY` in your environment (e.g. `~/.env.local`):
```bash
export EXA_API_KEY="your-exa-api-key"
```

Fallback: `~/.clawdbot/credentials/exa/config.json` with `{"apiKey": "..."}`

## Commands

### General Search
```bash
bash scripts/search.sh "query" [options]
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
bash scripts/search.sh "AI agents 2024"

# LinkedIn people search
CATEGORY=people bash scripts/search.sh "software engineer Amsterdam"

# Company search
CATEGORY=company bash scripts/search.sh "fintech startup Netherlands"

# News from specific domain
CATEGORY=news DOMAINS="reuters.com,bbc.com" bash scripts/search.sh "Netherlands"

# Research papers
CATEGORY="research paper" bash scripts/search.sh "transformer architecture"

# Deep search (comprehensive)
TYPE=deep bash scripts/search.sh "climate change solutions"

# Date-filtered news
CATEGORY=news SINCE="2026-01-01" bash scripts/search.sh "tech layoffs"
```

### Get Content
Extract full text from URLs:
```bash
bash scripts/content.sh "url1" "url2"
```

## Related Search Tools

**exa-plus specializes in neural search (people, companies, research). For other needs:**

| Tool | Specialty | Use When |
|------|-----------|----------|
| **exa-plus** (this) | Neural web, GitHub, LinkedIn, papers | People/company search, academic research |
| **valyu** | Recursive turn-based research | `valyu research "query" --turns 5` |
| **deep-research** | Multi-query Tavily synthesis | `deep-research "query" --deep` |
| **lev-research** | Multi-perspective orchestration | `lev-research "query"` |
| **lev-find** | Unified local + external | `lev find "query" --scope=research` |
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
- ❌ General web (use brave-search or tavily-search)
- ❌ Turn-based refinement (use valyu)

**Integration pattern:**
```bash
# 1. Find people/companies with Exa
CATEGORY=people exa search "ML engineer Amsterdam"

# 2. Deep research on findings
valyu research "machine learning hiring trends" --turns 5
```

See `skill://lev-research` for comprehensive research workflows.
