# Valyu AI - Search API for AI Agents

**Description:** Enterprise search API providing real-time web search, content extraction, AI-powered answers, and deep research capabilities optimized for AI agents.

**Website:** https://docs.valyu.ai/home
**API Base:** https://api.valyu.ai/v1/

---

## Authentication

All API requests require an API key:

```bash
# Header format
x-api-key: your-api-key-here
```

Get your API key at: https://platform.valyu.ai

---

## Core APIs

### 1. Search API

**Endpoint:** `POST https://api.valyu.ai/v1/search`

**Purpose:** Query web, proprietary datasets, and news sources with customizable filters.

**Request Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | **Required** | Search query string |
| `max_num_results` | integer | 10 | Results count (1-20 standard, up to 100 with special key) |
| `search_type` | enum | all | Options: `all`, `web`, `proprietary`, `news` |
| `fast_mode` | boolean | false | Reduced latency but shorter results |
| `max_price` | float | auto | CPM pricing limit in dollars |
| `relevance_threshold` | float | 0.5 | Minimum relevance score (0.0-1.0) |
| `included_sources` | array | [] | Specific sources/domains to include |
| `excluded_sources` | array | [] | Sources/domains to exclude |
| `category` | string | null | Natural language guide phrase |
| `response_length` | int/string | short | `short` (25k), `medium` (50k), `large` (100k), `max`, or custom |
| `country_code` | string | null | 2-letter ISO country code |
| `is_tool_call` | boolean | true | Optimize for AI agent vs. user queries |
| `start_date` | string | null | Start date (YYYY-MM-DD) |
| `end_date` | string | null | End date (YYYY-MM-DD) |
| `url_only` | boolean | false | Return only URLs (web/news only) |

**Response Schema:**

```json
{
  "success": true,
  "tx_id": "string",
  "query": "string",
  "results": [
    {
      "id": "string",
      "title": "string",
      "url": "string",
      "content": "string",
      "source": "string",
      "length": 12345,
      "image_url": "string",
      "publication_date": "string",
      "doi": "string",
      "citation": "string",
      "citation_count": 42,
      "authors": ["string"],
      "references": "string",
      "price": 0.001,
      "data_type": "unstructured",
      "source_type": "general"
    }
  ],
  "results_by_source": {
    "web": 5,
    "proprietary": 3
  },
  "total_deduction_pcm": 1.5,
  "total_deduction_dollars": 0.0015,
  "total_characters": 25000
}
```

**Source Types:** `general`, `website`, `forum`, `paper`, `data`, `report`, `health_data`, `clinical_trial`, `drug_label`, `grants`

---

### 2. Answer API

**Endpoint:** `POST https://api.valyu.ai/v1/answer`

**Purpose:** AI-generated responses grounded in search results. Supports streaming via SSE.

**Request Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | **Required** | Question or query |
| `system_instructions` | string | null | Custom AI directives (max 2000 chars) |
| `structured_output` | object | null | JSON schema for structured responses |
| `search_type` | enum | all | `all`, `web`, `proprietary`, `news` |
| `fast_mode` | boolean | false | Reduced latency mode |
| `data_max_price` | float | 1 | Maximum search cost in dollars |
| `included_sources` | array | [] | Specific domains/URLs/datasets |
| `excluded_sources` | array | [] | Sources to exclude |
| `start_date` | string | null | Date filter (YYYY-MM-DD) |
| `end_date` | string | null | Date filter (YYYY-MM-DD) |
| `country_code` | string | null | 2-letter ISO code |
| `streaming` | boolean | false | Enable SSE streaming |

**Response Schema:**

```json
{
  "success": true,
  "tx_id": "string",
  "original_query": "string",
  "contents": "string or object",
  "data_type": "unstructured",
  "search_results": [
    {
      "title": "string",
      "url": "string",
      "content": "string",
      "source_type": "string",
      "publication_date": "string",
      "relevance_score": 0.95
    }
  ],
  "search_metadata": {
    "tx_id": "string",
    "result_count": 10,
    "total_characters": 50000
  },
  "ai_usage": {
    "input_tokens": 1000,
    "output_tokens": 500
  },
  "cost": {
    "search_dollars": 0.001,
    "ai_dollars": 0.002,
    "total_dollars": 0.003
  }
}
```

**Streaming Mode:** Returns Server-Sent Events with search results first, then content deltas, metadata, and `[DONE]` marker.

---

### 3. Contents API

**Endpoint:** `POST https://api.valyu.ai/v1/contents`

**Purpose:** Extract clean, structured content from web pages with optional AI processing.

**Request Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `urls` | array | **Required** | 1-10 URLs (must start with http/https) |
| `response_length` | string/int | short | `short` (25K), `medium` (50K), `large` (100K), `max`, or custom (1K-1M) |
| `max_price_dollars` | number | auto | Cost limit (defaults to 2x estimated) |
| `extract_effort` | string | normal | `normal`, `high`, or `auto` |
| `screenshot` | boolean | false | Include page screenshots |
| `summary` | boolean/string/object | false | AI processing: `true`, custom instructions, or JSON schema |

**Response Schema:**

```json
{
  "success": true,
  "tx_id": "string",
  "results": [
    {
      "title": "string",
      "url": "string",
      "content": "markdown string or JSON object",
      "description": "string",
      "price": 0.001,
      "length": 25000,
      "data_type": "unstructured",
      "image_url": {
        "image1": "url",
        "image2": "url"
      },
      "screenshot_url": "string",
      "summary_success": true
    }
  ],
  "urls_requested": 5,
  "urls_processed": 5,
  "urls_failed": 0,
  "total_cost_dollars": 0.005,
  "total_characters": 125000
}
```

**Extract Effort:**
- `normal`: Fastest, basic extraction
- `high`: Better quality, slower
- `auto`: Automatic quality selection

**Summary Options:**
- `false`: No AI processing (default)
- `true`: Basic summarization
- `"custom instructions"`: Specific AI task
- `{json_schema}`: Structured data extraction

---

### 4. DeepResearch API

**Endpoint:** `POST https://api.valyu.ai/v1/deepresearch`

**Purpose:** Launch asynchronous research tasks with batch processing and progress monitoring.

**Features:**
- Extended research workflows
- Task status checking
- Batch processing support
- Comprehensive report generation

---

## SDK Support

### Python

```bash
pip install valyu
```

```python
from valyu import ValyuClient

client = ValyuClient(api_key="your-api-key")

# Search
results = client.search(
    query="AI agents",
    max_num_results=10,
    search_type="web"
)

# Answer
answer = client.answer(
    query="What are AI agents?",
    streaming=False
)

# Contents
contents = client.contents(
    urls=["https://example.com"],
    summary="Summarize key points"
)
```

### JavaScript/TypeScript

```bash
npm install valyu-js
```

```javascript
import { ValyuClient } from 'valyu-js';

const client = new ValyuClient({ apiKey: 'your-api-key' });

// Search
const results = await client.search({
  query: 'AI agents',
  max_num_results: 10,
  search_type: 'web'
});

// Answer
const answer = await client.answer({
  query: 'What are AI agents?',
  streaming: false
});

// Contents
const contents = await client.contents({
  urls: ['https://example.com'],
  summary: 'Summarize key points'
});
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 206 | Partial content (some operations failed) |
| 400 | Invalid parameters |
| 401 | Unauthorized/invalid API key |
| 402 | Insufficient credits |
| 403 | API key lacks permissions |
| 422 | All URLs failed processing (Contents API) |
| 500 | Server error |

---

## Pricing Model

- **Pay-per-success:** Charged only for successful operations
- **CPM-based:** Cost per thousand character retrievals
- **$10 starter credits** available
- **Transparent costs:** Response includes detailed cost breakdown
- **No rate limits** documented

---

## Integration Frameworks

**Supported:**
- LangChain
- LlamaIndex
- Vercel AI SDK

**AI Platforms:**
- Claude (Anthropic)
- AWS Bedrock
- Google Gemini

---

## Use Cases

### 1. Real-time Web Search
```python
results = client.search(
    query="latest AI developments 2026",
    search_type="news",
    start_date="2026-01-01",
    max_num_results=20
)
```

### 2. AI-Powered Q&A
```python
answer = client.answer(
    query="How do neural networks work?",
    system_instructions="Explain in simple terms for beginners",
    included_sources=["wikipedia.org", "arxiv.org"]
)
```

### 3. Content Extraction
```python
contents = client.contents(
    urls=["https://docs.example.com"],
    summary={
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "key_features": {"type": "array", "items": {"type": "string"}},
            "pricing": {"type": "string"}
        }
    }
)
```

### 4. Research with Citations
```python
results = client.search(
    query="quantum computing applications",
    search_type="all",
    response_length="large",
    relevance_threshold=0.8
)

# Results include citations, DOIs, authors for academic sources
```

---

## Advanced Features

### Structured Data Extraction

```python
# Extract specific data using JSON schema
answer = client.answer(
    query="https://example.com/product",
    structured_output={
        "type": "object",
        "properties": {
            "product_name": {"type": "string"},
            "price": {"type": "number"},
            "features": {"type": "array", "items": {"type": "string"}},
            "rating": {"type": "number"}
        },
        "required": ["product_name", "price"]
    }
)
```

### Source Filtering

```python
# Include specific domains
results = client.search(
    query="AI safety research",
    included_sources=["arxiv.org", "openai.com", "anthropic.com"]
)

# Exclude domains
results = client.search(
    query="AI news",
    excluded_sources=["reddit.com", "twitter.com"]
)
```

### Cost Control

```python
# Set maximum spending per request
results = client.search(
    query="comprehensive AI report",
    max_price=0.10,  # Max $0.10 per request
    response_length="large"
)
```

---

## Resources

- **Documentation:** https://docs.valyu.ai/
- **API Platform:** https://platform.valyu.ai/
- **LLM-optimized docs:** https://docs.valyu.ai/llms.txt
- **Community:** Discord, GitHub, Twitter
- **Support:** Email contact available

---

## Quick Reference

```bash
# cURL Example - Search
curl -X POST https://api.valyu.ai/v1/search \
  -H "x-api-key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "AI agents",
    "max_num_results": 10,
    "search_type": "web"
  }'

# cURL Example - Answer
curl -X POST https://api.valyu.ai/v1/answer \
  -H "x-api-key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are transformers in AI?",
    "streaming": false
  }'

# cURL Example - Contents
curl -X POST https://api.valyu.ai/v1/contents \
  -H "x-api-key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com"],
    "response_length": "medium",
    "summary": "Extract key information"
  }'
```

---

## CLI Tool (Quick Access)

### Installation

```bash
Use the stable wrapper installed at `~/.local/bin/valyu`.
It reads `VALYU_API_KEY` from `~/.env.local`.
```

### Usage

**Basic Commands:**
```bash
# Search
valyu search "AI agents" --num 10 --type web

# Answer
valyu answer "What are transformers?" --instructions "Technical explanation"

# Contents
valyu contents https://example.com --summary "Extract key points"

# Recursive Research (1-10 turns)
valyu research "quantum computing" --turns 5 --threshold 0.85
```

**Recursive Research Pattern:**

The `valyu research` command implements **turn-based iterative refinement**:

1. **Turn 1**: Initial search → AI answer with confidence score
2. **Refinement**: AI suggests next query based on knowledge gaps
3. **Turns 2-N**: Iterative deepening until confidence >= threshold
4. **Synthesis**: Final comprehensive answer across all turns

**Turn Loop:**
```
Turn 1: "quantum computing applications"
  → Confidence: 65%
  → Next: "What are practical quantum algorithms?"

Turn 2: "What are practical quantum algorithms?"
  → Confidence: 78%
  → Next: "How do quantum error correction codes work?"

Turn 3: "How do quantum error correction codes work?"
  → Confidence: 91%
  → STOP (>= 85% threshold)

Final Synthesis: Comprehensive answer from 3 turns
```

**Research Strategies:**
- `--strategy breadth`: More sources (20), broad coverage
- `--strategy depth`: Fewer sources (10), deep content
- `--strategy balanced`: 15 sources, general-purpose (default)

**Example - 5-Turn Deep Research:**
```bash
valyu research "How does RAG work with vector databases?" \
  --turns 5 \
  --threshold 0.85 \
  --strategy depth \
  --output ./rag-research

# Output:
# ./rag-research/
# ├── turn-1.md       - Initial findings
# ├── turn-2.md       - Refined query results
# ├── turn-3.md       - Continued refinement
# ├── turn-4.md       - Deep dive
# ├── turn-5.md       - Final iteration
# ├── REPORT.md       - Complete synthesis
# └── results.json    - Full data
```

**Cost Control:**
```bash
# Lower cost (fewer results, fast mode)
valyu search "topic" --num 5 --fast

# Higher quality (more turns, deeper research)
valyu research "topic" --turns 10 --strategy depth
```

**See:** `~/.agents/skills/lev-research/backends/valyu-recursive-confidence/cli/README.md` for historical CLI documentation. The stable runtime surface is the `valyu` wrapper in `~/.local/bin`.

---

## Integration Patterns

### From Claude Code / Cursor

```typescript
// Use CLI from agent code
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// Run research
const { stdout } = await execAsync(
  'valyu research "topic" --turns 5 --output ./research'
);

// Parse results
const results = JSON.parse(
  await fs.readFile('./research/results.json', 'utf-8')
);
```

### From Shell Scripts

```bash
#!/bin/bash
# Automated research pipeline

topics=("AI safety" "quantum computing" "neural networks")

for topic in "${topics[@]}"; do
  echo "Researching: $topic"
  valyu research "$topic" \
    --turns 5 \
    --strategy balanced \
    --output "research/$(echo $topic | tr ' ' '-')"
done

# Combine reports
cat research/*/REPORT.md > COMBINED_RESEARCH.md
```

### With lev exec (Future)

**Current:** Quick CLI wrapper (stopgap)

**Future:** Native lev plugin with FlowMind directives

```yaml
# valyu.flow.yaml (planned)
name: valyu-research
type: lev_plugin
cdo_properties:
  - streaming:
      target_confidence: 85-95
      max_iterations: 10
commands:
  research:
    handler: recursive_research
    params:
      query: string
      turns: number
      strategy: breadth|depth|balanced
```

**Tech Debt Ticket:** See BD epic for 1st-class plugin migration

---

---

## Related Search Tools

**valyu specializes in recursive turn-based research. For other approaches:**

| Tool | Specialty | Use When |
|------|-----------|----------|
| **valyu** (this) | Recursive research (1-10 turns, confidence scoring) | Iterative refinement, confidence-driven research |
| **lev-research** | Multi-perspective orchestration | Architecture analysis, research workflows |
| **lev-find** | Unified local + external search | Cross-domain discovery, default choice |
| **deep-research** | Multi-query Tavily synthesis | Complex topics, parallel queries |
| **brave-search** | Quick web search | Fast lookups, documentation |
| **tavily-search** | AI-optimized single search | Clean snippets, factual questions |
| **exa-plus** | Neural search, GitHub, papers | People/company search, academic research |
| **grok-research** | Real-time X/Twitter | Social sentiment, current events |
| **firecrawl** | Web scraping | Content extraction, site mapping |
| **qmd** | Local session search | Conversation history, markdown collections |

**Valyu's unique capabilities:**
- ✅ Turn-based iterative refinement (1-10 turns)
- ✅ Confidence scoring with automatic stopping (85-95% threshold)
- ✅ AI-suggested query refinement between turns
- ✅ Three research strategies (breadth/depth/balanced)
- ✅ Complete turn-by-turn reporting
- ❌ Local search (use qmd or lev-find)
- ❌ Multi-perspective templates (use lev-research)
- ❌ Real-time social (use grok-research)

**Integration pattern:**
```bash
# 1. Quick lookup
brave-search "keyword" --num 5

# 2. If insufficient, escalate to Valyu
valyu research "keyword context" --turns 5 --threshold 0.85

# 3. Or orchestrate through lev-research
lev-research "keyword" --template=technology_assessment
```

**When to use Valyu:**
- Need 85-95% confidence in findings
- Research requires iterative refinement
- Want automatic query expansion
- Prepared for 1-10 turns ($0.01-0.02 typical cost)

**When NOT to use Valyu:**
- Quick lookups (use brave-search or tavily-search)
- Local-only search (use qmd or lev-find)
- Multi-perspective analysis (use lev-research)

See `skill://lev-research` for comprehensive research orchestration.

---

**Last Updated:** 2026-01-28
**Skill Version:** 1.0.0
**API Version:** v1
**CLI Version:** 1.0.0
