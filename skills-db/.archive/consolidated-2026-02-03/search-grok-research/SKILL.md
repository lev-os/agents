---
name: grok-research
description: Real-time research via Grok (xAI) with X/Twitter search and web access. Use when Brave fails or you need current events, social sentiment, or real-time data.
homepage: https://x.ai
metadata: {"clawdbot":{"emoji":"🔬","requires":{"env":["XAI_API_KEY"]}}}
---

# Grok Research

Use Grok (xAI) for real-time research when:
- Brave search is down or rate-limited
- You need X/Twitter search
- Current events or real-time data
- Social sentiment analysis

## Quick Usage

```bash
# Via curl (env: XAI_API_KEY)
curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-3",
    "messages": [{"role": "user", "content": "What are people saying about X topic on Twitter right now?"}]
  }' | jq -r '.choices[0].message.content'
```

## Models

| Model | Use Case | Speed |
|-------|----------|-------|
| `grok-3` | Deep research, complex queries | Slower |
| `grok-3-mini` | Quick lookups, simple facts | Fast |

## When to Use vs Brave

| Scenario | Use |
|----------|-----|
| Documentation lookup | Brave |
| API references | Brave |
| Current events | **Grok** |
| Twitter/X sentiment | **Grok** |
| Real-time data | **Grok** |
| Brave 429/down | **Grok** |

## Script

For complex research, use the helper:

```bash
~/.claude/skills/grok-research/scripts/grok-search.sh "your query"
```

## Integration

The skill exposes:
- `grok_search(query)` - Returns research results
- `grok_sentiment(topic)` - Returns X/Twitter sentiment
- `grok_facts(question)` - Quick fact lookup

## API Handoff Pattern (Fabric-style)

```json
{
  "command": "research",
  "query": "...",
  "callback": "https://...",
  "runId": "uuid"
}
```

Returns:
```json
{
  "runId": "uuid",
  "status": "ok",
  "output": "...",
  "sources": ["x.com/...", "..."]
}
```

## Related Search Tools

**grok-research specializes in real-time X/Twitter and current events. For other needs:**

| Tool | Specialty | Use When |
|------|-----------|----------|
| **grok-research** (this) | Real-time X/Twitter, current events | Social sentiment, trending topics, breaking news |
| **valyu** | Recursive turn-based research | `valyu research "query" --turns 5` |
| **deep-research** | Multi-query Tavily synthesis | `deep-research "query" --deep` |
| **lev-research** | Multi-perspective orchestration | `lev-research "query"` |
| **lev-find** | Unified local + external | `lev find "query" --scope=research` |
| **brave-search** | Quick web search | `brave-search "query"` |
| **tavily-search** | AI-optimized snippets | `tavily-search "query"` |
| **exa-plus** | Neural search, LinkedIn, papers | `exa search "query"` |
| **firecrawl** | Web scraping | `firecrawl scrape <url>` |
| **qmd** | Local session search | `qmd query "query"` |

**Grok's unique capabilities:**
- ✅ Real-time X/Twitter search
- ✅ Social sentiment analysis
- ✅ Current events (fresher than other tools)
- ✅ Breaking news
- ✅ Fallback when Brave is down/rate-limited
- ❌ Academic research (use exa-plus)
- ❌ Documentation (use brave-search)
- ❌ Multi-query synthesis (use deep-research)

**Integration pattern:**
```bash
# 1. Check social sentiment with Grok
grok-research "what are people saying about X on Twitter"

# 2. Deep dive with other tools
valyu research "X trends and analysis" --turns 5
```

See `skill://lev-research` for comprehensive research workflows.
