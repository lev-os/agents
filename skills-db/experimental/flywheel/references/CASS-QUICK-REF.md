# CASS Quick Reference

> Essential commands for mining session history.

---

## Bootstrap (Always First)

```bash
# Health check + refresh index
cass status --json && cass index --json
```

**Why:** Index must be fresh for accurate results.

---

## The Core Commands

### 1. Project Overview

```bash
# Who did what, when?
cass search "*" --workspace /data/projects/PROJECT \
  --aggregate agent,date --limit 1 --json
```

**Returns:** Counts by agent and date, no content.

### 2. Find Patterns

```bash
# Search with minimal output
cass search "KEYWORD" --workspace /data/projects/PROJECT \
  --json --fields minimal --limit 50
```

**Filter to user prompts:**
```bash
| jq '[.hits[] | select(.line_number <= 3)]'
```

### 3. View Context

```bash
# Line-oriented view (raw)
cass view /path.jsonl -n LINE -C 20

# Message-oriented view (structured)
cass expand /path.jsonl --line LINE --context 3
```

### 4. Find Related Sessions

```bash
# Discover work clusters
cass context /path.jsonl --json
```

### 5. Export for Analysis

```bash
# Always use -o, never pipe
cass export /path.jsonl --format json --include-tools -o /tmp/out.json
```

---

## Ritual Detection

```bash
# Find repeated prompts (rituals)
cass search "*" --workspace /data/projects/PROJECT \
  --json --fields minimal --limit 500 \
  | jq '[.hits[] | select(.line_number <= 3) | .title[0:80]]
        | group_by(.) | map({prompt: .[0], count: length})
        | sort_by(-.count) | map(select(.count >= 5)) | .[0:30]'
```

**Interpretation:**
- `count >= 10` → RITUAL (validated methodology)
- `count 5-9` → Emerging pattern
- `count < 5` → One-off (not generalizable)

---

## Search Modes

| Mode | Use When | Example |
|------|----------|---------|
| `lexical` (default) | Exact strings, filenames | `"AGENTS.md"` |
| `semantic` | Conceptual, unknown wording | `"scope reduction"` |
| `hybrid` | Broad exploration | `"architecture decisions"` |

**Default to lexical.** Only use semantic when exact wording is unknown.

---

## Critical Rules

| Rule | Why |
|------|-----|
| `--limit 1` minimum | `--limit 0` panics |
| `--fields minimal` | 5x smaller output |
| Export to file (`-o`) | Piping causes broken pipe panic |
| Exact workspace paths | Case-sensitive matching |
| `--include-tools` | Tool calls hidden by default |

---

## Key jq Filters

```bash
# User prompts only
| jq '[.hits[] | select(.line_number <= 3)]'

# Extract source paths
| jq '.hits[].source_path' -r

# Count total matches
| jq '.total_matches'

# Get aggregation buckets
| jq '.aggregations.agent.buckets'

# First N results
| jq '.hits[0:10]'
```

---

## Session File Heuristics

| Line Number | Content |
|-------------|---------|
| 1-3 | User prompts |
| `/subagents/` line 2 | THE extraction prompt |
| High line numbers | Assistant responses |

---

## Common Workflows

### Find All Instances of a Pattern

```bash
# 1. Search
cass search "pattern" --workspace /path --json --fields minimal --limit 100 \
  | jq '[.hits[] | select(.line_number <= 3)]'

# 2. Extract source paths
| jq '.[].source_path' -r > /tmp/paths.txt

# 3. View each in context
for p in $(cat /tmp/paths.txt); do
  echo "=== $p ==="
  cass view "$p" -n 1 -C 10
done
```

### Mine a Specific Project

```bash
# Overview
cass search "*" --workspace /data/projects/myproject \
  --aggregate agent,date --limit 1 --json

# Find rituals
cass search "*" --workspace /data/projects/myproject \
  --json --fields minimal --limit 500 \
  | jq '[.hits[] | select(.line_number <= 3) | .title[0:80]]
        | group_by(.) | map({prompt: .[0], count: length})
        | sort_by(-.count) | .[0:20]'
```

### Investigate Specific Topic

```bash
# Search topic
cass search "authentication" --workspace /data/projects/myproject \
  --json --fields minimal --limit 50

# Pick a hit, view context
cass expand /path/from/hit.jsonl --line LINE --context 5

# Find related sessions
cass context /path/from/hit.jsonl --json
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| 0 results but content exists | Check workspace path (case-sensitive) |
| Index stale | Run `cass index --json` |
| Broken pipe panic | Use `-o file.json` instead of piping |
| Missing tool calls | Add `--include-tools` |
| Output too large | Use `--fields minimal` |

---

## Output Fields

### Minimal (`--fields minimal`)

```json
{
  "source_path": "/path/to/session.jsonl",
  "line_number": 2,
  "title": "First 80 chars of content..."
}
```

### Full (default)

```json
{
  "source_path": "/path/to/session.jsonl",
  "line_number": 2,
  "title": "First 80 chars...",
  "content": "Full content...",
  "agent": "claude-code",
  "workspace": "/data/projects/myproject",
  "timestamp": "2026-01-15T10:30:00Z"
}
```

---

## Quick Copy-Paste

```bash
# Health check
cass status --json && cass index --json

# Project overview
cass search "*" --workspace /data/projects/PROJECT --aggregate agent,date --limit 1 --json

# Find user prompts
cass search "KEYWORD" --workspace /data/projects/PROJECT --json --fields minimal --limit 50 | jq '[.hits[] | select(.line_number <= 3)]'

# Ritual detection
cass search "*" --workspace /data/projects/PROJECT --json --fields minimal --limit 500 | jq '[.hits[] | select(.line_number <= 3) | .title[0:80]] | group_by(.) | map({prompt: .[0], count: length}) | sort_by(-.count) | map(select(.count >= 5)) | .[0:30]'

# View context
cass view /PATH.jsonl -n LINE -C 20

# Expand message
cass expand /PATH.jsonl --line LINE --context 3

# Related sessions
cass context /PATH.jsonl --json
```
