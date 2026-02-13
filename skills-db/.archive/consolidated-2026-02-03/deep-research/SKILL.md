---
name: deep-research
description: Multi-mode research agent using Tavily. Quick searches, query expansion, and deep multi-query synthesis with smart stopping. **MANDATE:** Always load exa + valyu for comprehensive research.
homepage: https://tavily.com
metadata: {"clawdbot":{"emoji":"🔬","requires":{"bins":["bun"],"env":["TAVILY_API_KEY","EXA_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---

# Deep Research

**MANDATE:** All research queries MUST load **exa** + **valyu** backends for comprehensive discovery.

Intelligent research agent with three modes: quick search, query expansion, and deep multi-query synthesis. Uses Tavily's AI-optimized search with smart stopping.

## Required Backends

**Before starting any research:**
1. Load `skill://exa-plus` - Neural web + GitHub search
2. Load `skill://valyu` - Deep research + time travel analysis
3. Use `lev find --scope=research` for integrated search

**Example:**
```bash
# Load exa + valyu
lev find "authentication patterns 2026" --scope=research

# Augment with Tavily deep search
bun {baseDir}/scripts/research.mjs "authentication patterns 2026" --deep
```

## Usage

```bash
# Quick mode - single query, fast results
bun {baseDir}/scripts/research.mjs "query" --quick

# Expand mode - iterative query refinement (default)
bun {baseDir}/scripts/research.mjs "query" --expand

# Deep mode - multi-query synthesis with comprehensive analysis
bun {baseDir}/scripts/research.mjs "query" --deep
```

## Modes

### Quick Mode (`--quick`)
Single Tavily search. Fast, returns top results with AI-generated answer.
- Best for: Simple factual questions, quick lookups
- Iterations: 1

### Expand Mode (`--expand`) [default]
Iterative query refinement. Analyzes initial results and generates follow-up queries.
- Best for: Exploratory research, learning about a topic
- Iterations: 2-3 (stops when confident or no new info)

### Deep Mode (`--deep`)
Multi-query parallel search with synthesis. Generates multiple angle queries, searches in parallel, and synthesizes findings.
- Best for: Comprehensive research, due diligence, complex topics
- Iterations: Up to 5 (configurable)

## Options

- `--quick`: Quick single-query mode
- `--expand`: Iterative expansion mode (default)
- `--deep`: Deep multi-query synthesis mode
- `--max-iter <n>`: Maximum iterations (default: 5)
- `--confidence <n>`: Confidence threshold 0-100 (default: 85)
- `--results <n>`: Results per query (default: 5, max: 20)
- `--topic <t>`: Search topic - `general` (default) or `news`
- `--json`: Output raw JSON instead of markdown

## Smart Stopping

The agent stops early when:
1. **Confidence threshold reached** - Sources consistently agree
2. **No new information** - Follow-up queries return redundant results
3. **Max iterations hit** - Safety limit reached

## Output Format

```markdown
# Research: [Query]

## Summary
[Synthesized findings with confidence score]

## Key Findings
- Finding 1
- Finding 2
...

## Sources
- [Title](url) - relevance%
...

## Research Trace
- Iteration 1: [query] → [n] results
- Iteration 2: [follow-up] → [n] new results
...
```

## Configuration

API key is read from (in order):
1. `TAVILY_API_KEY` environment variable
2. `~/.clawdbot/clawdbot.json` → `skills.entries["tavily-search"].apiKey`

## Examples

```bash
# Quick fact check
bun {baseDir}/scripts/research.mjs "What is the current population of Tokyo?" --quick

# Explore a topic
bun {baseDir}/scripts/research.mjs "How does CRISPR gene editing work?"

# Deep research for decision making
bun {baseDir}/scripts/research.mjs "Best practices for Kubernetes autoscaling in production" --deep

# News research
bun {baseDir}/scripts/research.mjs "AI regulation updates 2024" --topic news --deep
```

## Related Search Tools

**Choose the right tool for your task:**

| Tool | Best For | When to Use |
|------|----------|-------------|
| **deep-research** (this) | Multi-query synthesis, iterative refinement | Complex research, topic exploration |
| **valyu** | Turn-based recursive research (1-10 turns) | Confidence-driven research, automatic query refinement |
| **lev-research** | Multi-perspective orchestration | Architecture analysis, gap detection |
| **lev-find** | Unified search (local + external) | Cross-domain search, finding related work |
| **brave-search** | Quick web search | Documentation, API references |
| **tavily-search** | Single-query AI search | Fast lookups, clean snippets |
| **exa-plus** | Neural search, GitHub, LinkedIn | People/company search, research papers |
| **grok-research** | Real-time X/Twitter, current events | Social sentiment, trending topics |
| **firecrawl** | Web scraping, site mapping | Content extraction, structured data |
| **qmd** | Local session/doc search | Conversation history, markdown collections |

**Integration pattern:**
```bash
# 1. Quick lookup
brave-search "keyword" --num 5

# 2. Deeper research
deep-research "keyword context" --deep

# 3. Recursive refinement
valyu research "keyword context" --turns 5 --threshold 0.85

# 4. Multi-perspective
lev-research "keyword" --template=technology_assessment
```

---

## Notes

- Uses Tavily's `advanced` search depth for better results in expand/deep modes
- Deduplicates sources across iterations
- Tracks information density to detect diminishing returns
- Outputs structured markdown optimized for AI consumption
