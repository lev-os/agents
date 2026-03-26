# xf Command Reference

> **Freedom Key:** LOW = exact syntax required | MEDIUM = some flexibility | HIGH = multiple approaches

---

## Lifecycle Commands [LOW freedom]

```bash
xf doctor                       # Health check — is index current?
xf index ~/x-archive            # Index archive (first time)
xf index --force                # Full rebuild (when stale)
xf stats --format json          # Archive overview
xf stats --detailed             # Full analytics dashboard
```

### Stats Output

```json
{
  "tweets": 12847,
  "likes": 45231,
  "dms": 3421,
  "grok_messages": 892,
  "followers": 1543,
  "following": 892
}
```

---

## Search Command [MEDIUM freedom]

### Basic Form

```bash
xf search "QUERY" --format json --limit N
```

**Every search needs:** `--format json` for parsing, `--limit N` for control.

### Filtering

| Filter | Example |
|--------|---------|
| By type | `--types tweet`, `dm`, `like`, `grok` |
| By mode | `--mode hybrid` (default), `lexical`, `semantic` |
| By date | `--since "2024-01"`, `--until "last week"` |
| Multiple types | `--types tweet,like` |

### Output Control

| Flag | Effect | Use When |
|------|--------|----------|
| `--format json` | Machine-readable | Always for jq |
| `--format text` | Human-readable | Manual review |
| `--limit N` | Max results | Always set explicitly |
| `--offset N` | Skip first N | Pagination |
| `--sort engagement` | By likes+RTs | Finding best content |
| `--sort date` | Chronological | Timeline view |

### DM-Specific [LOW freedom]

```bash
xf search "QUERY" --types dm --context --format json
```

**CRITICAL:** `--context` only works with `--types dm`. Shows full conversation around matches.

### Search Modes

| Mode | Algorithm | Best For |
|------|-----------|----------|
| `hybrid` (default) | BM25 + vectors | General exploration |
| `lexical` | BM25 only | Exact terms, `"quoted phrases"` |
| `semantic` | Vector similarity | Conceptual, varied wording |

### Query Syntax (Lexical Mode)

```bash
"exact phrase"              # Phrase match
term1 AND term2             # Both required
term1 OR term2              # Either matches
term1 NOT term2             # Exclude term2
rust*                       # Wildcard prefix
```

---

## Tweet Command [LOW freedom]

```bash
xf tweet <ID> [OPTIONS]
```

| Flag | Effect |
|------|--------|
| `--thread, -t` | Show thread context |
| `--engagement, -e` | Show likes/RTs/replies |
| `--format json` | Machine-readable |

### Examples

```bash
xf tweet 1234567890 --thread --format json
xf tweet 1234567890 --engagement --format json
```

### Thread Output

```json
{
  "tweet": {...},
  "thread": {
    "parent": {...},
    "replies": [...]
  }
}
```

---

## List Command [MEDIUM freedom]

```bash
xf list WHAT [OPTIONS]
```

| WHAT | Content |
|------|---------|
| `conversations` | DM conversation list |
| `tweets` | Recent tweets |
| `likes` | Recent likes |
| `followers` | Your followers |
| `following` | Who you follow |

### Examples

```bash
xf list conversations --format json --limit 50
xf list tweets --limit 100 --format json
```

---

## Export Command [LOW freedom]

```bash
xf export WHAT --format FMT -o FILE
```

| WHAT | Content |
|------|---------|
| `tweets` | All your tweets |
| `likes` | All likes |
| `dms` | All DMs (privacy-sensitive!) |
| `all` | Everything |

| Format | Use |
|--------|-----|
| `json` | Array for jq processing |
| `jsonl` | Streaming, large exports |
| `csv` | Spreadsheet import |

### Examples

```bash
xf export tweets --format jsonl -o tweets.jsonl
xf export dms --format json -o dms.json
```

**Note:** For large exports, prefer `jsonl` format.

---

## Stats Command [MEDIUM freedom]

```bash
xf stats [OPTIONS]
```

| Flag | Output |
|------|--------|
| `--format json` | Machine-readable |
| `--detailed, -d` | Full analytics |
| `--hashtags` | Top hashtags |
| `--mentions` | Top mentioned users |
| `--temporal` | Activity patterns, gaps |
| `--engagement` | Likes/RTs distribution |
| `--top N` | Number of top items |

### Detailed Stats Output

```json
{
  "tweets": 12847,
  "likes": 45231,
  "temporal": {
    "first_tweet": "2015-03-14",
    "last_tweet": "2026-01-17",
    "active_days": 2847,
    "longest_gap_days": 45
  },
  "engagement": {
    "total_likes_received": 89234,
    "total_retweets": 12453,
    "avg_likes_per_tweet": 6.9
  }
}
```

---

## Config Command [LOW freedom]

```bash
xf config --show                    # Display current config
xf config --set archive=~/x-archive # Set default archive
xf config --archive ~/x-archive     # Set archive path
```

---

## Global Options

| Flag | Effect |
|------|--------|
| `--format, -f FMT` | Output format |
| `--verbose, -v` | Debug output |
| `--quiet, -q` | Suppress non-error output |
| `--no-color` | Disable colors |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `XF_DB` | Path to SQLite database |
| `XF_INDEX` | Path to Tantivy index |
| `NO_COLOR` | Disable colored output |

---

## Output Schemas

### Search Result

```json
{
  "id": "1234567890",
  "result_type": "Tweet",
  "text": "The tweet content...",
  "created_at": "2024-06-15T10:30:00Z",
  "score": 15.234,
  "highlights": ["matched <em>term</em>"],
  "metadata": {
    "favorite_count": 42,
    "retweet_count": 7
  }
}
```

### DM Result (with --context)

```json
{
  "conversations": [{
    "conversation_id": "abc123",
    "messages": [
      {"sender_id": "123", "text": "...", "created_at": "..."},
      {"sender_id": "456", "text": "...", "created_at": "..."}
    ]
  }]
}
```

### Grok Result

```json
{
  "id": "grok-msg-123",
  "result_type": "GrokMessage",
  "text": "The message content...",
  "created_at": "2024-06-15T10:30:00Z",
  "metadata": {
    "chat_id": "chat-456",
    "sender": "user",
    "grok_mode": "fun"
  }
}
```

---

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | Continue |
| `1` | Error (index, query) | Check `xf doctor`, re-index |
| `2` | Invalid args | Check command syntax |
