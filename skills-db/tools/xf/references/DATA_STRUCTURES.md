# X Archive Data Structures

> **Critical knowledge for understanding xf output and raw archive files.**

---

## Quick Reference

| Content Type | `result_type` | Key Metadata Fields |
|--------------|---------------|---------------------|
| Your tweets | `Tweet` | `favorite_count`, `retweet_count`, `in_reply_to_status_id` |
| Liked tweets | `Like` | `author_handle`, `author_id` |
| DMs | `DirectMessage` | `conversation_id`, `sender_id` |
| Grok chats | `GrokMessage` | `chat_id`, `sender`, `grok_mode` |

---

## Archive Structure

When you download your X archive, it contains:

```
your-archive/
├── data/
│   ├── tweets.js              # Your tweets
│   ├── like.js                # Liked tweets
│   ├── direct-messages.js     # DM conversations
│   ├── grok-conversation.js   # Grok AI chats (if available)
│   ├── follower.js            # Your followers
│   ├── following.js           # Who you follow
│   ├── block.js               # Blocked accounts
│   ├── mute.js                # Muted accounts
│   └── ...
├── assets/
│   └── ...                    # Media files
└── Your archive.html          # Web viewer
```

**Note:** xf indexes the `data/` directory and creates its own index files.

---

## Search Result Structure

### Common Fields (All Types)

```json
{
  "id": "1234567890123456789",
  "result_type": "Tweet",
  "text": "The content text...",
  "created_at": "2024-06-15T10:30:00Z",
  "score": 15.234,
  "highlights": ["matched <em>term</em>"],
  "metadata": { ... }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `result_type` | string | `Tweet`, `Like`, `DirectMessage`, `GrokMessage` |
| `text` | string | The content |
| `created_at` | ISO 8601 | Timestamp |
| `score` | float | Search relevance score |
| `highlights` | array | Matched terms with `<em>` tags |
| `metadata` | object | Type-specific additional data |

---

## Tweet Structure

### Search Result

```json
{
  "id": "1234567890",
  "result_type": "Tweet",
  "text": "Just shipped a new feature! #rust #programming",
  "created_at": "2024-06-15T10:30:00Z",
  "score": 12.5,
  "metadata": {
    "favorite_count": 42,
    "retweet_count": 7,
    "reply_count": 3,
    "in_reply_to_status_id": null,
    "in_reply_to_user_id": null,
    "is_retweet": false,
    "has_media": true,
    "urls": ["https://example.com/link"],
    "hashtags": ["rust", "programming"],
    "user_mentions": ["@someone"]
  }
}
```

### Key Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `favorite_count` | int | Number of likes received |
| `retweet_count` | int | Number of retweets |
| `reply_count` | int | Number of replies |
| `in_reply_to_status_id` | string/null | If reply, the parent tweet ID |
| `in_reply_to_user_id` | string/null | If reply, the user being replied to |
| `is_retweet` | bool | Whether this is a retweet |
| `has_media` | bool | Has images/video |
| `urls` | array | Extracted URLs |
| `hashtags` | array | Extracted hashtags (without #) |
| `user_mentions` | array | Mentioned @usernames |

### Detecting Tweet Types

```bash
# Original tweets (not replies)
| jq '[.[] | select(.metadata.in_reply_to_status_id == null)]'

# Replies only
| jq '[.[] | select(.metadata.in_reply_to_status_id != null)]'

# Tweets with media
| jq '[.[] | select(.metadata.has_media == true)]'

# Tweets with links
| jq '[.[] | select((.metadata.urls | length) > 0)]'
```

---

## Like Structure

### Search Result

```json
{
  "id": "9876543210",
  "result_type": "Like",
  "text": "Great article on distributed systems!",
  "created_at": "2024-06-14T15:20:00Z",
  "score": 8.3,
  "metadata": {
    "author_handle": "techwriter",
    "author_id": "111222333",
    "original_tweet_id": "9876543210",
    "liked_at": "2024-06-14T15:20:00Z"
  }
}
```

### Key Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `author_handle` | string | Original tweet author's handle |
| `author_id` | string | Original tweet author's ID |
| `original_tweet_id` | string | The liked tweet's ID |
| `liked_at` | ISO 8601 | When you liked it |

### Common Like Queries

```bash
# Find liked content by specific author
| jq '[.[] | select(.metadata.author_handle == "techwriter")]'

# Most liked authors
| jq -r '.[].metadata.author_handle' | sort | uniq -c | sort -rn | head -20
```

---

## DM Structure

### Search Result (without --context)

```json
{
  "id": "dm-msg-123",
  "result_type": "DirectMessage",
  "text": "Hey, can you send me that link?",
  "created_at": "2024-06-13T09:15:00Z",
  "score": 6.7,
  "metadata": {
    "conversation_id": "conv-abc123",
    "sender_id": "123456789",
    "recipient_id": "987654321",
    "message_type": "text"
  }
}
```

### Search Result (with --context)

```json
{
  "conversations": [{
    "conversation_id": "conv-abc123",
    "participant_ids": ["123456789", "987654321"],
    "messages": [
      {
        "id": "dm-msg-122",
        "text": "Do you have that article link?",
        "sender_id": "987654321",
        "created_at": "2024-06-13T09:10:00Z"
      },
      {
        "id": "dm-msg-123",
        "text": "Hey, can you send me that link?",
        "sender_id": "123456789",
        "created_at": "2024-06-13T09:15:00Z"
      }
    ]
  }]
}
```

### Key Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `conversation_id` | string | Unique conversation identifier |
| `sender_id` | string | Who sent this message |
| `recipient_id` | string | Who received this message |
| `message_type` | string | `text`, `media`, `reaction` |

### Common DM Queries

```bash
# List all conversations
| jq '[.[].metadata.conversation_id] | unique'

# Messages from specific conversation
| jq --arg id "conv-abc123" '[.[] | select(.metadata.conversation_id == $id)]'

# Group by conversation
| jq 'group_by(.metadata.conversation_id) | map({conv: .[0].metadata.conversation_id, count: length})'
```

---

## Grok Message Structure

### Search Result

```json
{
  "id": "grok-msg-456",
  "result_type": "GrokMessage",
  "text": "How do I implement a binary search tree in Rust?",
  "created_at": "2024-06-12T14:00:00Z",
  "score": 5.2,
  "metadata": {
    "chat_id": "grok-chat-789",
    "sender": "user",
    "grok_mode": "regular",
    "model_version": "grok-2"
  }
}
```

### Key Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `chat_id` | string | Unique chat session identifier |
| `sender` | string | `user` or `grok` |
| `grok_mode` | string | `regular`, `fun`, etc. |
| `model_version` | string | Grok model version used |

### Common Grok Queries

```bash
# Your questions only
| jq '[.[] | select(.metadata.sender == "user")]'

# Grok's responses only
| jq '[.[] | select(.metadata.sender == "grok")]'

# Reconstruct chat conversation
| jq 'group_by(.metadata.chat_id) | map({
    chat: .[0].metadata.chat_id,
    messages: (sort_by(.created_at) | map({sender: .metadata.sender, text: .text[0:100]}))
  })'

# Count by mode
| jq 'group_by(.metadata.grok_mode) | map({mode: .[0].metadata.grok_mode, count: length})'
```

---

## Export vs Search Differences

Field names differ between search results and raw exports:

### Tweet Fields

| Field | Search Result Path | Export Path |
|-------|-------------------|-------------|
| Likes | `.metadata.favorite_count` | `.favorite_count` |
| Retweets | `.metadata.retweet_count` | `.retweet_count` |
| Reply to | `.metadata.in_reply_to_status_id` | `.in_reply_to_status_id` |

### Handling Both Formats

```bash
# Universal engagement extraction
| jq '.[] | {
    likes: (.metadata.favorite_count // .favorite_count // 0),
    rts: (.metadata.retweet_count // .retweet_count // 0)
  }'
```

---

## Date Formats

All dates are ISO 8601 format:

```
2024-06-15T10:30:00Z
│    │  │  │  │  │ └─ UTC timezone
│    │  │  │  │  └─── Seconds
│    │  │  │  └────── Minutes
│    │  │  └───────── Hours (24h)
│    │  └──────────── Day
│    └─────────────── Month
└──────────────────── Year
```

### Date Extraction Patterns

```bash
# Extract year
| jq -r '.[].created_at[:4]'

# Extract month (YYYY-MM)
| jq -r '.[].created_at[:7]'

# Extract date (YYYY-MM-DD)
| jq -r '.[].created_at[:10]'

# Extract hour
| jq -r '.[].created_at[11:13]'
```

---

## File Locations

### xf Database Files

After indexing, xf creates:

```
~/.xf/                          # Default location
├── db.sqlite                   # SQLite database
└── index/                      # Tantivy search index

# Or within archive directory:
~/x-archive/.xf/
├── db.sqlite
└── index/
```

### Environment Variables

```bash
export XF_DB=~/.xf/db.sqlite
export XF_INDEX=~/.xf/index
```

---

## Type Detection

### From Search Results

```bash
# Check result type
| jq '.[0].result_type'

# Group by type
| jq 'group_by(.result_type) | map({type: .[0].result_type, count: length})'
```

### From Raw Archive Files

```bash
# tweets.js starts with:
# window.YTD.tweets.part0 = [...]

# Parse raw archive file
tail -n +2 data/tweets.js | jq '.[].tweet'
```

---

## Quick Structure Exploration

When unsure about structure:

```bash
# Top-level keys
| jq 'keys'

# First item structure
| jq '.[0] | keys'

# Metadata structure
| jq '.[0].metadata | keys'

# Full first item
| jq '.[0]'

# Sample of each type
| jq 'group_by(.result_type) | map(.[0])'
```
