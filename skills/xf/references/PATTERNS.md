# jq Extraction Patterns

> **Copy-paste reference** for parsing xf output.

---

## Quick Reference Card

| Goal | Pattern |
|------|---------|
| All text | `'.[].text'` |
| Text with date | `'.[] \| {text, date: .created_at}'` |
| High engagement | `'[.[] \| select(.metadata.favorite_count > 10)]'` |
| Filter by type | `'[.[] \| select(.result_type == "Tweet")]'` |
| Count results | `'length'` |
| Unique values | `'[.[].field] \| unique'` |
| Sort descending | `'sort_by(-.field)'` |
| Group and count | `'group_by(.field) \| map({key: .[0].field, count: length})'` |
| Safe access | `'.field // "default"'` |
| First N | `'.[0:N]'` |

---

## Basic Extraction

### Text and Content

```bash
# Just text
| jq '.[].text'

# Text without quotes (raw)
| jq -r '.[].text'

# Text with date
| jq '.[] | {text, date: .created_at}'

# Text with engagement
| jq '.[] | {text: .text[0:80], likes: .metadata.favorite_count, rts: .metadata.retweet_count}'

# Truncated text preview
| jq '.[] | .text[0:100]'
```

### Counting and Limiting

```bash
# Count total results
| jq 'length'

# First N results
| jq '.[0:5]'

# Last N results
| jq '.[-5:]'

# Random sample (shuffle + take)
| jq 'to_entries | sort_by(.key | tostring | explode | add) | .[0:10] | map(.value)'
```

---

## Filtering Patterns

### By Field Value

```bash
# High engagement
| jq '[.[] | select(.metadata.favorite_count > 10)]'

# Low engagement
| jq '[.[] | select(.metadata.favorite_count <= 5)]'

# Contains text
| jq '[.[] | select(.text | contains("rust"))]'

# Case-insensitive contains
| jq '[.[] | select(.text | ascii_downcase | contains("rust"))]'

# Regex match
| jq '[.[] | select(.text | test("rust|python"; "i"))]'

# Date range
| jq '[.[] | select(.created_at >= "2024-01" and .created_at < "2024-07")]'

# Non-null field
| jq '[.[] | select(.metadata.in_reply_to != null)]'

# Is reply
| jq '[.[] | select(.metadata.in_reply_to_status_id != null)]'

# Not a reply
| jq '[.[] | select(.metadata.in_reply_to_status_id == null)]'
```

### By Result Type

```bash
# Tweets only
| jq '[.[] | select(.result_type == "Tweet")]'

# DMs only
| jq '[.[] | select(.result_type == "DirectMessage")]'

# Likes only
| jq '[.[] | select(.result_type == "Like")]'

# Grok messages only
| jq '[.[] | select(.result_type == "GrokMessage")]'
```

### Combining Filters

```bash
# High engagement + contains keyword
| jq '[.[] | select(.metadata.favorite_count > 5 and (.text | contains("rust")))]'

# Date + engagement
| jq '[.[] | select(.created_at >= "2024-01" and .metadata.favorite_count > 10)]'

# Type + text filter
| jq '[.[] | select(.result_type == "Tweet" and (.text | test("^@"; "i") | not))]'
```

---

## Aggregation Patterns

### Counting

```bash
# Count by year
| jq -r '.[].created_at[:4]' | sort | uniq -c

# Count by month
| jq -r '.[].created_at[:7]' | sort | uniq -c

# Count by result type
| jq 'group_by(.result_type) | map({type: .[0].result_type, count: length})'

# Count by day of week (requires external date command)
| jq -r '.[].created_at' | xargs -I{} date -d {} +%A | sort | uniq -c
```

### Grouping

```bash
# Group by month
| jq 'group_by(.created_at[:7]) | map({month: .[0].created_at[:7], count: length})'

# Group by conversation (DMs)
| jq 'group_by(.metadata.conversation_id) | map({conv: .[0].metadata.conversation_id, count: length})'

# Group by Grok chat
| jq 'group_by(.metadata.chat_id) | map({chat: .[0].metadata.chat_id, count: length})'

# Group with summary stats
| jq 'group_by(.created_at[:7]) | map({
    month: .[0].created_at[:7],
    count: length,
    avg_likes: (map(.metadata.favorite_count // 0) | add / length)
  })'
```

### Top N

```bash
# Top by engagement
| jq 'sort_by(-.metadata.favorite_count) | .[0:10]'

# Top hashtags
| jq -r '.[].text' | grep -oE '#\w+' | sort | uniq -c | sort -rn | head -20

# Top mentions
| jq -r '.[].text' | grep -oE '@\w+' | sort | uniq -c | sort -rn | head -20

# Top by retweets
| jq 'sort_by(-.metadata.retweet_count) | .[0:10]'
```

---

## DM Patterns

### Basic DM Extraction

```bash
# All DM text
xf search "query" --types dm --format json | jq '.[].text'

# With sender info
| jq '.[] | {sender: .metadata.sender_id, text}'

# Unique conversation IDs
| jq '[.[].metadata.conversation_id] | unique'
```

### Conversation Context (with --context flag)

```bash
# Full conversations
xf search "query" --types dm --context --format json \
  | jq '.conversations[]'

# Conversation messages
| jq '.conversations[] | .messages[] | {sender: .sender_id, text, date: .created_at}'

# Conversation summary
| jq '.conversations | map({id: .conversation_id, message_count: (.messages | length)})'

# Specific conversation
| jq '.conversations[] | select(.conversation_id == "CONV_ID") | .messages[]'
```

### DM Analytics

```bash
# Messages per conversation
| jq 'group_by(.metadata.conversation_id) | map({conv: .[0].metadata.conversation_id, count: length}) | sort_by(-.count)'

# Unique conversation partners
| jq '[.[].metadata.conversation_id] | unique | length'

# Message frequency by date
| jq -r '.[].created_at[:10]' | sort | uniq -c

# Most active conversations
| jq 'group_by(.metadata.conversation_id) | sort_by(-length) | .[0:5] | .[] | {conv: .[0].metadata.conversation_id, messages: length}'
```

---

## Grok Patterns

### Basic Grok Extraction

```bash
# All Grok messages
xf search "" --types grok --format json | jq '.[].text'

# With metadata
| jq '.[] | {text, chat_id: .metadata.chat_id, sender: .metadata.sender}'

# User messages only
| jq '[.[] | select(.metadata.sender == "user")]'

# Grok responses only
| jq '[.[] | select(.metadata.sender == "grok")]'

# By Grok mode
| jq '[.[] | select(.metadata.grok_mode == "fun")]'
```

### Chat Reconstruction

```bash
# Group by chat
| jq 'group_by(.metadata.chat_id)'

# Reconstruct Q&A pairs
| jq 'group_by(.metadata.chat_id) | map({
    chat_id: .[0].metadata.chat_id,
    messages: (sort_by(.created_at) | map({sender: .metadata.sender, text: .text[0:100]}))
  })'

# Count chats
| jq 'group_by(.metadata.chat_id) | length'
```

### Grok Analytics

```bash
# Messages per chat
| jq 'group_by(.metadata.chat_id) | map({chat: .[0].metadata.chat_id, count: length}) | sort_by(-.count)'

# Question count
| jq '[.[] | select(.metadata.sender == "user")] | length'

# Mode distribution
| jq 'group_by(.metadata.grok_mode) | map({mode: .[0].metadata.grok_mode, count: length})'
```

---

## Analytics Patterns

### Engagement Analytics

```bash
# Total engagement
| jq 'map(.metadata.favorite_count + .metadata.retweet_count) | add'

# Average engagement
| jq 'map(.metadata.favorite_count) | add / length'

# Engagement percentiles
| jq 'map(.metadata.favorite_count) | sort | {
    min: .[0],
    p50: .[length/2 | floor],
    p90: .[length*0.9 | floor],
    max: .[-1]
  }'

# Top performing content
| jq 'sort_by(-.metadata.favorite_count) | .[0:10] | .[] | {text: .text[0:60], likes: .metadata.favorite_count}'
```

### Content Analytics

```bash
# Average tweet length
| jq 'map(.text | length) | add / length'

# URL sharing rate
| jq '[.[] | select(.text | contains("http"))] | length'

# Reply rate
| jq '[.[] | select(.metadata.in_reply_to_status_id != null)] | length'

# Media rate
| jq '[.[] | select(.metadata.has_media == true)] | length'
```

### Temporal Analytics

```bash
# Activity by hour (requires date command)
| jq -r '.[].created_at' | cut -c12-13 | sort | uniq -c

# Posting frequency
| jq 'group_by(.created_at[:10]) | map({date: .[0].created_at[:10], count: length}) | sort_by(.date)'

# Monthly engagement trend
| jq 'group_by(.created_at[:7]) | map({
    month: .[0].created_at[:7],
    tweets: length,
    total_likes: (map(.metadata.favorite_count) | add)
  }) | sort_by(.month)'
```

---

## Export Patterns

### Format Conversion

```bash
# JSON to JSONL
| jq -c '.[]' > output.jsonl

# JSON to CSV
| jq -r '["id","date","text"], (.[] | [.id, .created_at[:10], .text]) | @csv' > output.csv

# Extract specific fields
| jq '[.[] | {id, date: .created_at[:10], text, likes: .metadata.favorite_count}]' > simplified.json
```

### Filtered Export

```bash
# Export high engagement only
| jq '[.[] | select(.metadata.favorite_count > 10)]' > high_engagement.json

# Export date range
| jq '[.[] | select(.created_at >= "2024-01" and .created_at < "2024-07")]' > 2024_h1.json

# Export non-replies
| jq '[.[] | select(.metadata.in_reply_to_status_id == null)]' > original_tweets.json
```

---

## Debugging jq

### The Golden Rule: Simplify Rather Than Debug

When a complex jq command fails silently:

**Don't:** Spend time debugging the complex filter.
**Do:** Simplify to basics, verify data exists, then rebuild.

```bash
# Complex filter fails silently:
| jq '[.[] | select(.metadata.favorite_count > 10 and (.text | contains("rust")))] | ...'
# No output, no error. Now what?

# SIMPLIFY FIRST:
| jq 'length'                    # Do we have results?
| jq '.[0]'                      # What does a result look like?
| jq '.[0] | keys'               # What fields exist?
| jq '.[0].metadata | keys'      # What's in metadata?

# THEN rebuild step by step
```

### Build Up Incrementally

```bash
# Start simple
| jq '.[0:5]'

# Add projection
| jq '[.[] | {text, date: .created_at}]'

# Add filter
| jq '[.[] | select(.metadata.favorite_count > 5)]'

# Combine (last)
| jq '[.[] | select(.metadata.favorite_count > 5) | {text: .text[0:80], likes: .metadata.favorite_count}]'
```

### Check Intermediate Counts

```bash
| jq 'length'                                      # Total results
| jq '[.[] | select(.metadata.favorite_count > 10)] | length'  # After engagement filter
| jq '[.[] | select(.result_type == "Tweet")] | length'        # After type filter
```

---

## Safe Access Patterns

### Avoid Null Errors

```bash
# With default
| jq '.field // "default"'
| jq '.metadata.favorite_count // 0'

# Check before access
| jq 'if length == 0 then "no results" else .[0:5] end'

# Safe iterate
| jq '(. // [])[]'
```

### Check Structure

```bash
# Top-level keys
| jq 'keys'

# First result structure
| jq '.[0] | keys'

# Metadata structure
| jq '.[0].metadata | keys'

# Check field exists
| jq '.[0] | has("metadata")'
```

---

## One-Liners

| Task | One-Liner |
|------|-----------|
| All text | `jq '.[].text'` |
| Text + date | `jq '.[] \| {text, date: .created_at}'` |
| Count results | `jq 'length'` |
| First 5 | `jq '.[0:5]'` |
| Top by likes | `jq 'sort_by(-.metadata.favorite_count) \| .[0:5]'` |
| Unique IDs | `jq '[.[].id] \| unique'` |
| Hashtags | `jq -r '.[].text' \| grep -oE '#\w+' \| sort -u` |
| Mentions | `jq -r '.[].text' \| grep -oE '@\w+' \| sort -u` |
| Date range | `jq '[.[] \| select(.created_at >= "2024-01")]'` |
| High engagement | `jq '[.[] \| select(.metadata.favorite_count > 10)]'` |
| Tweets only | `jq '[.[] \| select(.result_type == "Tweet")]'` |
| Count by month | `jq -r '.[].created_at[:7]' \| sort \| uniq -c` |
| Conversation IDs | `jq '[.[].metadata.conversation_id] \| unique'` |
| Grok chats | `jq 'group_by(.metadata.chat_id) \| length'` |
