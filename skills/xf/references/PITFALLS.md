# xf Pitfalls & Troubleshooting

> **Quick lookup:** Ctrl+F for your error message or symptom.

---

## Quick Diagnosis

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| 0 results but content exists | Index stale or not built | `xf index --force` |
| `--context` ignored | Not using `--types dm` | Add `--types dm` |
| No Grok messages found | Archive predates Grok | Check `xf stats` for grok_messages count |
| jq returns null | Wrong field path | Use `jq '.[0] \| keys'` to check structure |
| Empty search results | Typo or wrong mode | Try `--mode semantic` for fuzzy matching |
| Slow first search | Vector index loading | Normal on first query, subsequent are fast |
| Date filter not working | Wrong format | Use ISO format: `"2024-01-15"` or natural: `"last week"` |

---

## Index Problems

### "Index not found" / "Please run xf index first"

```bash
xf doctor                       # Check what's wrong
xf index ~/path/to/archive      # Index the archive
xf index --force                # Force rebuild if stale
```

### Index Stale / Missing Recent Content

```bash
# Check index status
xf doctor

# Force full re-index
xf index --force
```

### Wrong Archive Path

```bash
# Check configured path
xf config --show

# Set correct path
xf config --archive ~/correct/path/to/archive

# Or use environment variable
export XF_DB=~/x-archive/.xf/db.sqlite
export XF_INDEX=~/x-archive/.xf/index
```

---

## Search Problems

### 0 Results But Content Exists

1. **Check index health:**
   ```bash
   xf doctor
   xf stats --format json | jq '{tweets, likes}'
   ```

2. **Try different search mode:**
   ```bash
   # Lexical finds exact terms
   xf search "exact phrase" --mode lexical --format json

   # Semantic finds related concepts
   xf search "the concept" --mode semantic --format json

   # Hybrid (default) combines both
   xf search "query" --format json
   ```

3. **Check type filter:**
   ```bash
   # Maybe it's in likes, not tweets
   xf search "query" --types like --format json

   # Search all types
   xf search "query" --format json
   ```

### `--context` Flag Ignored

**Problem:** Using `--context` but not getting conversation threads.

**Fix:** `--context` only works with DMs:
```bash
# WRONG (context ignored):
xf search "query" --context --format json

# RIGHT:
xf search "query" --types dm --context --format json
```

### Date Filter Not Working

**Use proper formats:**
```bash
# ISO format (recommended)
xf search "query" --since "2024-01-15" --until "2024-06-30"

# Natural language
xf search "query" --since "last month"
xf search "query" --since "3 days ago"
xf search "query" --since "2024-01"  # First of month
```

**Common mistakes:**
```bash
# WRONG:
--since "January 2024"
--since "1/15/2024"

# RIGHT:
--since "2024-01"
--since "2024-01-15"
```

### No Grok Messages Found

```bash
# Check if archive has Grok data
xf stats --format json | jq '.grok_messages'

# If 0, your archive predates Grok or doesn't include it
# Request a fresh archive from X that includes Grok conversations
```

---

## Output Problems

### JSON Output Malformed

```bash
# Check you're using --format json
xf search "query" --format json | jq '.'

# If still broken, check for stderr mixing:
xf search "query" --format json 2>/dev/null | jq '.'
```

### Too Much Output

```bash
# Limit results
xf search "query" --format json --limit 20

# Truncate text in jq
| jq '.[] | {text: .text[0:100]}'

# Just count
| jq 'length'
```

### Empty Results Array

```bash
# Check if query matches anything
xf search "query" --format json | jq 'length'

# Try broader search
xf search "" --types tweet --format json --limit 10

# Check stats to confirm data exists
xf stats --format json
```

---

## jq Problems

### jq Returns null

```bash
# Check structure first
| jq '.[0] | keys'

# Check if field exists
| jq '.[0] | has("metadata")'

# Use safe access
| jq '.field // "default"'
```

### Complex Filter Fails Silently

**The golden rule: Simplify rather than debug**

```bash
# Complex filter, no output:
| jq '[.[] | select(.metadata.favorite_count > 10 and ...)]'

# SIMPLIFY:
| jq 'length'                     # Do we have data?
| jq '.[0]'                       # What's in it?
| jq '.[0].metadata | keys'       # What fields?

# Then rebuild step by step
```

### Field Name Mismatch

Field names differ between search results and exports:

| Context | Likes Field | Retweets Field |
|---------|-------------|----------------|
| Search results | `.metadata.favorite_count` | `.metadata.retweet_count` |
| Export | `.favorite_count` | `.retweet_count` |

```bash
# For search results:
| jq '.[] | .metadata.favorite_count'

# For exports:
| jq '.[] | .favorite_count'
```

---

## Type-Specific Issues

### DMs

**Problem:** Can't find DM conversation

**Solutions:**
```bash
# List all conversations first
xf list conversations --format json | jq '.[].conversation_id'

# Search with context
xf search "keyword" --types dm --context --format json

# Get all messages from specific conversation
xf search "" --types dm --format json \
  | jq --arg id "CONV_ID" '[.[] | select(.metadata.conversation_id == $id)]'
```

### Grok

**Problem:** Can't reconstruct Grok chat flow

**Solution:**
```bash
# Group by chat, sort by time
xf search "" --types grok --format json --limit 1000 \
  | jq 'group_by(.metadata.chat_id) | map({
      chat: .[0].metadata.chat_id,
      messages: (sort_by(.created_at) | map({sender: .metadata.sender, text: .text[0:100]}))
    })'
```

### Likes

**Problem:** Can't find original tweet author

**Check metadata:**
```bash
| jq '.[0].metadata | keys'

# Author might be in:
| jq '.[] | .metadata.author_handle'
# or
| jq '.[] | .metadata.author_id'
```

---

## Performance Issues

### Slow First Search

**Normal behavior:** First search loads vector index (~1-2 seconds).
**Subsequent searches:** Sub-millisecond.

### Large Export Timeout

```bash
# Use JSONL for streaming
xf export tweets --format jsonl -o tweets.jsonl

# Process in chunks
split -l 10000 tweets.jsonl chunk_
```

### Memory Issues with Large Results

```bash
# Limit results
xf search "query" --limit 1000 --format json

# Stream with jq
xf export tweets --format jsonl | jq -c 'select(.favorite_count > 10)' > filtered.jsonl
```

---

## Diagnostic Workflow

When xf isn't working:

```bash
# 1. Health check
xf doctor

# 2. Check stats
xf stats --format json | jq '{tweets, likes, dms, grok_messages}'

# 3. Simple search test
xf search "test" --format json --limit 5 | jq 'length'

# 4. Check configuration
xf config --show

# 5. Force re-index if needed
xf index --force
```

---

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | Continue |
| `1` | Error (index, query) | Check `xf doctor`, review query |
| `2` | Invalid args | Check command syntax, quoting |

---

## Pro Tips

### Quote Queries Properly

```bash
# Simple queries
xf search "machine learning" --format json

# Queries with special chars
xf search '"quoted phrase"' --mode lexical --format json

# Queries with shell special chars
xf search 'term1 AND term2' --mode lexical --format json
```

### Check Field Existence Before Filtering

```bash
# Avoid null errors
| jq '[.[] | select(.metadata.favorite_count != null and .metadata.favorite_count > 10)]'

# Or use defaults
| jq '[.[] | select((.metadata.favorite_count // 0) > 10)]'
```

### Parallel Searches for Coverage

```bash
# Different terms = different results
xf search "distributed systems" --format json > results1.json &
xf search "microservices" --format json > results2.json &
xf search "service mesh" --format json > results3.json &
wait
```
