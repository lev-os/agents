---
name: qmd
description: Quick Markdown Search - Full-text and vector search for markdown and JSONL files. Use for searching conversation history, documentation, and any text-based collections. Triggers on "search for", "find in sessions", "query history".
version: 1.0.0
repository: https://github.com/tobi/qmd
skill_type: tool
category: process-get-local
---

# qmd - Quick Markdown Search

Full-text (BM25) and vector similarity search with query expansion and reranking.

## Overview

qmd provides semantic search across collections of text files (markdown, JSONL, etc.) using:
- **BM25 full-text search** - Fast keyword matching
- **Vector embeddings** - Semantic similarity (embeddinggemma-300M)
- **Reranking** - Quality filtering (qwen3-reranker-0.6b)
- **Query expansion** - Automatic query refinement

**Installation:**
```bash
bun install -g https://github.com/tobi/qmd
```

**Binary location:** `~/.bun/bin/qmd`

## When to Use

Use qmd for:
- Searching conversation history across Claude Code, claudesp, Clawdbot
- Finding discussions about specific topics
- Semantic similarity search (similar concepts, different words)
- Documentation search
- Any large text corpus search

**Session Retention Policy:**
- Only keep sessions < 2 months old in qmd index
- Older sessions: grep on demand from raw JSONL files
- Keeps index size manageable, search fast

## Core Commands

### Search Commands

```bash
# Combined search (BM25 + vector + reranking) - BEST
qmd query "{text}" -c <collection>

# Full-text search only - FAST
qmd search "{text}" -c <collection>

# Vector similarity only - SEMANTIC
qmd vsearch "{text}" -c <collection>
```

### Collection Management

```bash
# Create/index collection
qmd collection add <path> --name <name> --mask <pattern>

# List all collections
qmd collection list

# Remove collection
qmd collection remove <name>

# Rename collection
qmd collection rename <old> <new>
```

### Index Management

```bash
# Update index (re-scan for changes)
qmd update

# Update with git pull
qmd update --pull

# Generate embeddings (required for vsearch)
qmd embed -f

# Check index status
qmd status

# Clean up and vacuum
qmd cleanup
```

### File Operations

```bash
# Get specific document
qmd get <file>[:line] [-l N] [--from N]

# Get multiple documents by pattern
qmd multi-get <pattern> [-l N] [--max-bytes N]

# List files in collection
qmd ls [collection[/path]]
```

### Context Management

```bash
# Add context for path
qmd context add [path] "text"

# List all contexts
qmd context list

# Remove context
qmd context rm <path>
```

## Search Options

```bash
# Limit results
-n <num>                   # Number of results (default: 5)

# Scoring thresholds
--min-score <num>          # Minimum similarity score
--all                      # Return all matches

# Output formats
--full                     # Full document instead of snippet
--line-numbers            # Add line numbers
--json                    # JSON output
--csv                     # CSV output
--md                      # Markdown output
--xml                     # XML output
--files                   # Output docid,score,filepath,context

# Collection filtering
-c <name>                 # Filter to specific collection

# Multi-get options
-l <num>                  # Maximum lines per file
--max-bytes <num>         # Skip files larger than N bytes
```

## Common Patterns

### Search All Collections

```bash
qmd query "authentication" \
  -c claude-sessions \
  -c claudesp-sessions \
  -c clawdbot-sessions \
  --full -n 10
```

### Search with Score Threshold

```bash
qmd query "deployment bug" --min-score 0.7 --json
```

### Get Recent Files

```bash
qmd ls claude-sessions | head -20
```

### Semantic Search

```bash
# Find similar concepts (not just keywords)
qmd vsearch "how do we handle errors in the gateway"
```

### Bulk Retrieval

```bash
# Get all files matching pattern
qmd multi-get "2026-01-28*.jsonl" --json
```

## Output Formats

### Default (Snippet)

```
Result 1 (score: 0.85):
File: ~/.claude/sessions/abc123.jsonl:42
Snippet: ...relevant text around match...
```

### Full Document

```bash
qmd query "text" --full --line-numbers
```

### JSON

```bash
qmd query "text" --json | jq '.results[] | {score, file: .docid}'
```

### Files Only

```bash
qmd query "text" --files
# Output: docid,score,filepath,context
```

## MCP Server

qmd includes an MCP server for agent integration:

```bash
# Start MCP server
qmd mcp

# Add to claude_desktop_config.json:
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

**MCP tools exposed:**
- `search` - Full-text search
- `vsearch` - Vector search
- `query` - Combined search
- `get` - Get document
- `multi-get` - Get multiple documents
- `collection_*` - Collection operations

## Index Details

**Location:** `~/.cache/qmd/index.sqlite`

**Models (auto-downloaded from HuggingFace):**
- Embedding: embeddinggemma-300M-Q8_0
- Reranking: qwen3-reranker-0.6b-q8_0
- Generation: Qwen3-0.6B-Q8_0

**Collection structure:**
```sql
CREATE TABLE collections (
  name TEXT PRIMARY KEY,
  path TEXT,
  mask TEXT
);

CREATE TABLE documents (
  docid TEXT PRIMARY KEY,
  collection TEXT,
  path TEXT,
  hash TEXT,
  content TEXT
);

CREATE TABLE embeddings (
  hash TEXT PRIMARY KEY,
  embedding BLOB
);
```

## Troubleshooting

### "Collection not found"

```bash
qmd collection list  # Check what exists
qmd collection add <path> --name <name> --mask "*.md"
```

### "No embeddings found"

```bash
qmd embed -f  # Generate embeddings
```

### No results

```bash
# Try broader search
qmd search "keyword" --all --min-score 0.3

# Check collection has files
qmd ls <collection>

# Re-index
qmd update
```

### Large index

```bash
qmd cleanup  # Vacuum DB
```

## Examples

### Example 1: Find Authentication Discussions

```bash
qmd query "authentication jwt middleware" \
  -c claude-sessions \
  -c clawdbot-sessions \
  --full --line-numbers -n 5
```

### Example 2: Search Clawdbot Only

```bash
qmd search "gateway bug" -c clawdbot-sessions --files
```

### Example 3: Semantic Search

```bash
# Find conceptually similar content
qmd vsearch "deploying containers to production" \
  --full -n 3
```

### Example 4: Get Session by ID

```bash
# If you know the session ID
qmd get ~/.clawdbot/agents/main/sessions/abc-123.jsonl --full
```

### Example 5: Search Recent Sessions

```bash
# Find files, then search within them
find ~/.clawdbot/agents/main/sessions -name "*.jsonl" -mtime -7 | \
  xargs qmd multi-get --json | \
  jq -r '.[] | select(.content | contains("voice"))'
```

## Related Search Tools

**qmd specializes in local markdown/JSONL search. For external search:**

| Tool | Specialty | Use When |
|------|-----------|----------|
| **qmd** (this) | Local session/doc search (BM25 + vector) | Conversation history, markdown collections |
| **lev-find** | Unified local + external search | Cross-domain discovery, default choice |
| **lev-research** | Multi-perspective orchestration | Architecture analysis, research workflows |
| **valyu** | Recursive turn-based research | `valyu research "query" --turns 5` |
| **deep-research** | Multi-query Tavily synthesis | `deep-research "query" --deep` |
| **brave-search** | Quick web search | `brave-search "query"` |
| **tavily-search** | AI-optimized snippets | `tavily-search "query"` |
| **exa-plus** | Neural search, GitHub, papers | `exa search "query"` |
| **grok-research** | Real-time X/Twitter | `grok-research "query"` |
| **firecrawl** | Web scraping | `firecrawl scrape <url>` |

**QMD's unique capabilities:**
- ✅ Local-only (no external API calls)
- ✅ BM25 full-text + vector embeddings + reranking
- ✅ Conversation history across Claude Code/claudesp/Clawdbot
- ✅ Fast markdown collection search
- ✅ MCP server for agent integration
- ❌ External web search (use brave/tavily/exa)
- ❌ Multi-perspective (use lev-research)

**Integration pattern:**
```bash
# 1. Search local history
qmd query "authentication discussion" -c claude-sessions --full

# 2. If not found locally, search external
valyu research "authentication patterns 2026" --turns 5

# 3. Or use unified search
lev get "authentication" --scope=all  # Searches both local + external
```

## Integration with Other Skills

### lev-clwd

lev-clwd uses qmd for conversation history search across all 3 session stores.

### lev-find

Future: lev-find will abstract qmd collections with unified interface.

See `skill://lev-research` for comprehensive research workflows.

## Claudesp Variant (~/dcs)

The **claudesp** variant lives at `~/.claude-sneakpeek/claudesp/config/` with shortcut:

```bash
~/dcs → ~/.claude-sneakpeek/claudesp/config/
```

### Directory Structure

```
~/.claude-sneakpeek/
└── claudesp/
    └── config/              # ← ~/dcs points here
        ├── CLAUDE.md        # Variant-specific instructions
        ├── .claude.json     # Variant settings + hooks
        ├── settings.json    # Variant hook configuration
        ├── commands/        # Commands (copies, allow variant edits)
        ├── skills/          # Skills (symlinked from ~/.claude/skills/)
        ├── hooks/           # Same hooks as ~/.claude/hooks/
        ├── plans/           # Session plans
        ├── history.jsonl    # Claudesp-specific command history
        ├── projects/        # Project session indexes
        └── session-env/     # Session environments
```

### Session Collections

| Collection | Path | Files |
|-----------|------|-------|
| `claude-sessions` | `~/.claude/transcripts/` | ~1558 |
| `claudesp-sessions` | `~/dcs/transcripts/` (or `~/.claude-sneakpeek/claudesp/config/transcripts/`) | ~163 |
| `clawdbot-sessions` | `~/.clawdbot/agents/main/sessions/` | ~1165 |

### Searching Claudesp History

```bash
# Search claudesp sessions specifically
qmd query "entity dashboard" -c claudesp-sessions --full -n 5

# Cross-variant search (all 3 session stores)
qmd query "lev cms" -c claude-sessions -c claudesp-sessions -c clawdbot-sessions -n 10
```

---

## Auto-Refresh (Staleness Detection)

### How qmd Handles Incremental Updates

qmd tracks file hashes in the index. On `qmd update`:
- **New files** → indexed and added
- **Changed files** (hash differs) → re-indexed
- **Unchanged files** → skipped (fast)
- **Deleted files** → removed from index

This means `qmd update` is always safe and incremental.

### XDG Cache Staleness Check

Index lives at `~/.cache/qmd/index.sqlite` (XDG-compliant).

**Auto-refresh pattern for hooks/session start:**

```bash
#!/bin/bash
# qmd-auto-refresh.sh - Run on SessionStart or as needed
# Checks if index is stale and refreshes incrementally

QMD_INDEX="$HOME/.cache/qmd/index.sqlite"
STALENESS_THRESHOLD=86400  # 1 day in seconds

if [ ! -f "$QMD_INDEX" ]; then
  echo "qmd index missing, creating..."
  qmd update
  exit 0
fi

# Check last modified time
INDEX_MTIME=$(stat -f %m "$QMD_INDEX" 2>/dev/null || stat -c %Y "$QMD_INDEX" 2>/dev/null)
NOW=$(date +%s)
AGE=$(( NOW - INDEX_MTIME ))

if [ "$AGE" -gt "$STALENESS_THRESHOLD" ]; then
  echo "qmd index stale (${AGE}s old), refreshing..."
  qmd update  # Incremental: skips unchanged files via hash
else
  echo "qmd index fresh (${AGE}s old)"
fi
```

### Hook Integration

Add to `~/.claude/settings.json` SessionStart hooks:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/qmd-auto-refresh.sh"
          }
        ]
      }
    ]
  }
}
```

### Session Retention Policy

- **< 2 months old**: Keep in qmd index (fast semantic search)
- **> 2 months old**: Grep on demand from raw JSONL files
- **Cleanup**: `qmd cleanup` removes orphaned data, vacuums DB

### Collection-Level Staleness

```bash
# Check which collections need refresh
qmd status | grep "updated" | awk '{print $1, $NF}'

# Force refresh specific collection
qmd update -c claude-sessions
qmd update -c claudesp-sessions

# Refresh all (incremental, safe)
qmd update
```

---

## Maintenance

### Daily Update

Add to jared cron or SessionStart hook:

```bash
# Incremental update (skips unchanged files)
qmd update

# Generate embeddings for new files
qmd embed -f
```

### Weekly Cleanup

```bash
qmd cleanup  # Remove orphaned data, vacuum DB
```

## Reference

**Repository:** https://github.com/tobi/qmd
**Models:** HuggingFace (auto-downloaded)
**Index:** `~/.cache/qmd/index.sqlite`
**Binary:** `~/.bun/bin/qmd`
**Shortcut:** `~/dcs` → `~/.claude-sneakpeek/claudesp/config/`

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-find-qmd, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
