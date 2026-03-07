# Valyu CLI - AI-Powered Search & Research

Command-line interface for Valyu AI with recursive deep research capabilities.

## Quick Start

```bash
# Install
cd ~/.claude/skills/valyu/cli
./install.sh

# Configure API key
echo "VALYU_API_KEY=your-key" > ~/.valyu/.env

# Run
valyu search "AI agents"
valyu answer "What are transformers?"
valyu research "quantum computing applications" --turns 5
```

## Installation

```bash
cd ~/.claude/skills/valyu/cli
./install.sh
```

This will:
1. Install dependencies (`valyu-js`, `commander`, `chalk`, `ora`)
2. Build TypeScript to JavaScript
3. Link `valyu` command globally
4. Create `~/.valyu/` config directory

**Requirements:**
- Node.js 18+
- npm or pnpm
- Valyu API key from https://platform.valyu.ai

## Configuration

Create `~/.valyu/.env`:

```bash
VALYU_API_KEY=your-api-key-here
```

Get your API key: https://platform.valyu.ai

## Commands

### `valyu search`

Search web, news, and proprietary sources.

```bash
valyu search "AI agents" \
  --num 20 \
  --type web \
  --start 2026-01-01 \
  --output results.json
```

**Options:**
- `-n, --num <number>` - Results count (default: 10, max: 100)
- `-t, --type <type>` - Search type: `all|web|proprietary|news` (default: all)
- `-f, --fast` - Fast mode (reduced latency)
- `--start <date>` - Start date (YYYY-MM-DD)
- `--end <date>` - End date (YYYY-MM-DD)
- `-o, --output <file>` - Save JSON results

**Example:**
```bash
$ valyu search "Claude AI" --num 15 --type web

📊 Found 15 results
Cost: $0.0012

[1] Claude AI by Anthropic
https://anthropic.com/claude
Claude is a next generation AI assistant...

[2] Claude AI Documentation
https://docs.anthropic.com
Complete documentation for Claude API...
```

---

### `valyu answer`

Get AI-generated answers grounded in search results.

```bash
valyu answer "How do transformers work?" \
  --instructions "Explain in simple terms" \
  --type all \
  --output answer.json
```

**Options:**
- `-t, --type <type>` - Search type: `all|web|proprietary|news`
- `-i, --instructions <text>` - System instructions for AI
- `--stream` - Enable streaming mode (SSE)
- `-o, --output <file>` - Save JSON results

**Example:**
```bash
$ valyu answer "What is RAG?" --instructions "Technical explanation"

💡 Answer:

Retrieval-Augmented Generation (RAG) is an AI architecture that combines...

📚 Sources:
[1] Understanding RAG Systems
    https://example.com/rag-guide
[2] RAG Implementation Patterns
    https://example.com/rag-patterns

Cost: $0.0023
Tokens: 1542
```

---

### `valyu contents`

Extract clean content from web pages.

```bash
valyu contents https://example.com \
  --length medium \
  --summary "Extract key features" \
  --output content.json
```

**Options:**
- `-l, --length <size>` - Response length: `short|medium|large|max`
- `-e, --effort <level>` - Extract effort: `normal|high|auto`
- `-s, --summary <instructions>` - AI summary instructions
- `--screenshot` - Include page screenshots
- `-o, --output <file>` - Save JSON results

**Example:**
```bash
$ valyu contents https://docs.example.com --summary "Summarize API features"

📄 Processed 1/1 URLs
Cost: $0.0015

[1] Example API Documentation
https://docs.example.com
The Example API provides REST endpoints for...
```

---

### `valyu research` (Recursive Deep Research)

**This is the key feature** - Multi-turn iterative research with automatic query refinement.

```bash
valyu research "quantum computing applications" \
  --turns 5 \
  --threshold 0.85 \
  --strategy balanced \
  --output ./research-output
```

**Options:**
- `-n, --turns <number>` - Max research turns (1-10, default: 5)
- `-t, --threshold <number>` - Confidence threshold to stop (0.0-1.0, default: 0.85)
- `-o, --output <dir>` - Output directory (default: ./valyu-research)
- `--strategy <type>` - Research strategy: `breadth|depth|balanced` (default: balanced)

**Strategies:**
- **breadth**: More sources (20), medium depth → broad coverage
- **depth**: Fewer sources (10), deeper content → comprehensive understanding
- **balanced**: 15 sources, medium depth → general-purpose

**How it works:**

1. **Turn 1**: Initial search + answer with confidence scoring
2. **Refinement**: AI suggests next query based on gaps/uncertainty
3. **Turn 2-N**: Iterative deepening until:
   - Confidence >= threshold (e.g., 85%)
   - Max turns reached
   - AI marks research "COMPLETE"
4. **Synthesis**: Final comprehensive answer across all turns

**Output:**
```
./research-output/
├── turn-1.json       # Full API responses
├── turn-1.md         # Human-readable findings
├── turn-2.json
├── turn-2.md
├── ...
├── results.json      # Complete research results
└── REPORT.md         # Final synthesis + timeline
```

**Example:**

```bash
$ valyu research "How does attention mechanism work in transformers?" --turns 3

🔬 Starting Recursive Deep Research

Query: How does attention mechanism work in transformers?
Turns: 3 (max)
Threshold: 0.85
Strategy: balanced

✓ Turn 1 complete: 65% confidence, 15 sources, $0.0034
→ Next turn: What are query, key, and value vectors in attention?

✓ Turn 2 complete: 78% confidence, 12 sources, $0.0029
→ Next turn: How is multi-head attention implemented?

✓ Turn 3 complete: 91% confidence, 14 sources, $0.0031

✓ Confidence threshold reached (91% >= 85%)
✓ Synthesis complete

✓ Research Complete

📊 Summary:
Total turns: 3
Final confidence: 91.0%
Total cost: $0.0112
Results saved: ./research-output/

💡 Final Synthesis:

[Comprehensive answer based on all 3 turns...]

📚 Key Sources:
[1] Attention Is All You Need (cited 5x)
    https://arxiv.org/abs/1706.03762
[2] The Illustrated Transformer (cited 3x)
    https://jalammar.github.io/illustrated-transformer
```

---

## Recursive Research Workflow

The `valyu research` command implements a **turn-based iterative refinement** pattern:

### Turn Loop

```
Turn 1: Initial Query
  ↓
Search (10-20 sources) + Answer (with confidence scoring)
  ↓
Parse: FINDINGS + CONFIDENCE + NEXT_QUERY
  ↓
If confidence < threshold:
  ↓
Turn 2: Refined Query (focus on gaps)
  ↓
Search + Answer (builds on Turn 1)
  ↓
Parse: FINDINGS + CONFIDENCE + NEXT_QUERY
  ↓
If confidence < threshold:
  ↓
Turn 3-N: Continued refinement
  ↓
Stop when:
- Confidence >= threshold
- Max turns reached
- AI marks "COMPLETE"
  ↓
Final Synthesis (across all turns)
```

### Confidence Scoring

Each turn's AI response includes:
```
FINDINGS: [detailed findings from this turn]
CONFIDENCE: 0.78  # How complete the answer is (0.0-1.0)
NEXT_QUERY: [refined query focusing on gaps] OR "COMPLETE"
```

The system automatically refines queries to fill knowledge gaps until confidence threshold is reached.

### Use Cases

**1. Comprehensive Topic Research**
```bash
valyu research "state of AI agents in 2026" --turns 7 --strategy breadth
```
- Broad coverage across multiple sources
- 7 turns for thorough exploration
- Good for landscape analysis

**2. Deep Technical Understanding**
```bash
valyu research "implement RAG with vector databases" --turns 5 --strategy depth
```
- Fewer sources, deeper content
- 5 turns for iterative refinement
- Good for implementation details

**3. Quick Research (3 turns)**
```bash
valyu research "latest GPT-4 features" --turns 3 --threshold 0.75
```
- Fast iteration (3 turns)
- Lower threshold (75%) for speed
- Good for quick summaries

**4. High-Confidence Research**
```bash
valyu research "quantum error correction methods" --turns 10 --threshold 0.95
```
- Max turns (10) for thoroughness
- High threshold (95%) for certainty
- Good for critical decisions

---

## Advanced Patterns

### Piping Results

```bash
# Search and extract specific data
valyu search "AI conferences 2026" --output search.json
cat search.json | jq '.results[].url' | xargs valyu contents

# Chain research to answer
valyu research "transformers architecture" --turns 3 --output research/
cat research/REPORT.md | valyu answer "Summarize in 3 bullet points"
```

### Batch Processing

```bash
# Research multiple topics
topics=("AI safety" "quantum computing" "neural networks")
for topic in "${topics[@]}"; do
  valyu research "$topic" --turns 5 --output "research/$topic"
done
```

### Custom Instructions

```bash
# Domain-specific research
valyu answer "How does photosynthesis work?" \
  --instructions "Explain at high school biology level with diagrams"

# Structured extraction
valyu answer "https://example.com/pricing" \
  --instructions "Extract: features, pricing tiers, and limits as JSON"
```

---

## Cost Management

All commands show cost breakdowns:

```bash
$ valyu search "AI" --num 10
Cost: $0.0012  # Cost for this operation

$ valyu research "topic" --turns 5
Total cost: $0.0156  # Cumulative across 5 turns + synthesis
```

**Typical costs:**
- Search (10 results): ~$0.001-0.002
- Answer: ~$0.002-0.004
- Contents (1 URL): ~$0.001-0.003
- Research (5 turns): ~$0.01-0.02

Control costs with:
- `--num <smaller>` - Fewer search results
- `--turns <lower>` - Fewer research iterations
- `--fast` - Fast mode (lower quality, lower cost)
- `--length short` - Shorter responses

---

## Troubleshooting

**Error: VALYU_API_KEY not found**
```bash
# Solution: Create config file
echo "VALYU_API_KEY=your-key" > ~/.valyu/.env
```

**Error: 402 Insufficient credits**
- Add credits at https://platform.valyu.ai
- $10 free starter credits available

**Command not found: valyu**
```bash
# Re-run installer
cd ~/.claude/skills/valyu/cli
./install.sh
```

**TypeScript errors**
```bash
# Rebuild
npm run build
```

---

## Development

```bash
# Run without building
npm run dev search "query"

# Build
npm run build

# Link globally
npm link
```

---

## Integration with Lev

**Current Status:** Quick CLI implementation (stopgap)

**Future:** Proper lev plugin with:
- FlowMind directives (`valyu.flow.yaml`)
- lev exec CDO properties (streaming research)
- Plugin registry entry
- Native lev skill integration

**Tech Debt Ticket:** See BD epic for 1st-class plugin migration

---

## Examples

### Example 1: Quick Search
```bash
valyu search "Claude Code features" --num 10
```

### Example 2: Technical Q&A
```bash
valyu answer "Explain gradient descent" \
  --instructions "Include mathematical formulas and examples"
```

### Example 3: Content Extraction
```bash
valyu contents \
  https://docs.anthropic.com/claude/docs \
  --summary "Extract API endpoints and parameters"
```

### Example 4: Deep Research (3 turns)
```bash
valyu research "implementing vector search" \
  --turns 3 \
  --strategy depth \
  --output ./vector-search-research
```

### Example 5: High-Confidence Research (10 turns)
```bash
valyu research "AI safety alignment techniques" \
  --turns 10 \
  --threshold 0.95 \
  --strategy balanced \
  --output ./ai-safety-research
```

---

**Version:** 1.0.0
**Last Updated:** 2026-01-28
**License:** MIT
