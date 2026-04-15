# Workflow Recipes

> **Priority:** Iterate fast. Sub-millisecond search enables exploration loops.

---

## Recipe Index

| Recipe | When |
|--------|------|
| [Archive Bootstrap](#archive-bootstrap) | First-time setup |
| [Topic Mining](#topic-mining) | Find everything about a subject |
| [Conversation Recovery](#conversation-recovery) | Reconstruct DM threads |
| [Grok Archaeology](#grok-archaeology) | Mine AI conversations |
| [Engagement Analysis](#engagement-analysis) | What resonated |
| [Timeline Reconstruction](#timeline-reconstruction) | Chronological view |
| [Cross-Reference Discovery](#cross-reference-discovery) | Connect topics |
| [Full Export Pipeline](#full-export-pipeline) | Bulk extraction |

---

## Archive Bootstrap

**First-time setup after downloading X archive:**

```bash
# 1. Import from zip (extracts + indexes)
xf import ~/Downloads/twitter-2026-01-09-*.zip

# 2. Or index existing extraction
xf index ~/my_x_history

# 3. Verify health
xf doctor

# 4. Overview
xf stats --format json | jq '{tweets, likes, dms, grok_messages}'
```

**Expected output:**
```json
{
  "tweets": 12847,
  "likes": 45231,
  "dms": 3421,
  "grok_messages": 892
}
```

---

## Topic Mining

**Goal:** Find everything you said/saved about a topic.

### Step-by-Step

```bash
# 1. Broad search (hybrid mode = best coverage)
xf search "machine learning" --format json --limit 100 | jq 'length'
# Found: 47 results

# 2. Your public thoughts
xf search "machine learning" --types tweet --format json --limit 100 \
  | jq '.[] | {text: .text[0:100], date: .created_at[:10], likes: .metadata.favorite_count}'

# 3. What you curated (liked)
xf search "machine learning" --types like --format json --limit 100 \
  | jq '.[] | .text[0:150]'

# 4. Private discussions
xf search "machine learning" --types dm --context --format json

# 5. AI conversations
xf search "machine learning" --types grok --format json
```

### Topic Mining with Dates

```bash
# Focus on specific period
xf search "project X" --since "2024-06" --until "2024-09" --format json

# Recent only
xf search "rust" --since "last month" --format json
```

### One-Command Topic Report

```bash
./scripts/topic_miner.py "machine learning"
```

---

## Conversation Recovery

**Goal:** Reconstruct DM discussions on a topic.

```bash
# 1. Find messages mentioning topic
xf search "meeting notes" --types dm --format json --limit 50 \
  | jq 'length'
# Found: 12 messages

# 2. Get conversation IDs
xf search "meeting notes" --types dm --format json \
  | jq '[.[].metadata.conversation_id] | unique'
# ["conv-123", "conv-456"]

# 3. View full conversation with context
xf search "meeting notes" --types dm --context --format json \
  | jq '.conversations[] | {id: .conversation_id, count: (.messages | length)}'

# 4. Extract specific conversation
xf search "meeting notes" --types dm --context --format json \
  | jq '.conversations[0].messages[] | {sender: .sender_id, text: .text[0:100], date: .created_at}'
```

### List All Conversations

```bash
xf list conversations --format json \
  | jq '.[] | {id: .conversation_id, participants: .participant_ids, last_message: .last_message_at}'
```

---

## Grok Archaeology

**Goal:** Find questions you asked Grok and answers received.

```bash
# 1. How many Grok messages?
xf stats --format json | jq '.grok_messages'

# 2. Search Grok history
xf search "how do I" --types grok --format json --limit 50

# 3. Find by topic
xf search "python" --types grok --format json --limit 100 \
  | jq '.[] | {text: .text[0:100], mode: .metadata.grok_mode}'

# 4. Group by chat
xf search "" --types grok --format json --limit 1000 \
  | jq 'group_by(.metadata.chat_id) | map({chat: .[0].metadata.chat_id, count: length}) | sort_by(-.count)'

# 5. Reconstruct a chat conversation
CHAT_ID="chat-123"
xf search "" --types grok --format json --limit 1000 \
  | jq --arg id "$CHAT_ID" '[.[] | select(.metadata.chat_id == $id)] | sort_by(.created_at) | .[] | {sender: .metadata.sender, text: .text[0:200]}'
```

### Grok Q&A Extraction

```bash
# Your questions (user messages)
xf search "" --types grok --format json \
  | jq '[.[] | select(.metadata.sender == "user")] | .[] | .text[0:100]'

# Grok's responses
xf search "" --types grok --format json \
  | jq '[.[] | select(.metadata.sender == "grok")] | .[] | .text[0:200]'
```

---

## Engagement Analysis

**Goal:** Find what content resonated.

```bash
# 1. Top engaging tweets
xf search "" --types tweet --sort engagement --limit 20 --format json \
  | jq '.[] | {text: .text[0:80], likes: .metadata.favorite_count, rts: .metadata.retweet_count}'

# 2. Engagement over threshold
xf export tweets --format json \
  | jq '[.[] | select(.favorite_count > 50)] | sort_by(-.favorite_count) | .[0:10]'

# 3. Most liked by topic
xf search "rust" --types tweet --sort engagement --format json \
  | jq '.[] | {text: .text[0:80], likes: .metadata.favorite_count}'

# 4. Engagement timeline by month
xf export tweets --format json \
  | jq 'group_by(.created_at[:7]) | map({month: .[0].created_at[:7], total_likes: (map(.favorite_count) | add), count: length}) | sort_by(.month)'

# 5. Viral tweets (top 1%)
xf export tweets --format json \
  | jq 'sort_by(-.favorite_count) | .[0:(length/100 | floor + 1)]'
```

---

## Timeline Reconstruction

**Goal:** Chronological view of your activity.

```bash
# 1. Activity by month
xf export tweets --format json \
  | jq -r '.[].created_at[:7]' | sort | uniq -c

# 2. Activity by year
xf export tweets --format json \
  | jq -r '.[].created_at[:4]' | sort | uniq -c

# 3. Full temporal stats
xf stats --temporal --format json

# 4. Specific period deep dive
xf search "*" --since "2024-01" --until "2024-03" --format json --limit 500 \
  | jq 'sort_by(.created_at) | .[] | "\(.created_at[:10]): \(.text[0:80])"' -r

# 5. Find gaps in activity
xf stats --temporal --format json \
  | jq '.temporal | {first: .first_tweet, last: .last_tweet, longest_gap: .longest_gap_days}'
```

---

## Cross-Reference Discovery

**Goal:** Find connections between topics.

```bash
# 1. Co-occurring terms with topic
xf search "rust" --types tweet --format json \
  | jq -r '.[].text' | tr '[:upper:]' '[:lower:]' | grep -oE '\b\w+\b' | sort | uniq -c | sort -rn | head -30

# 2. Hashtag co-occurrence
xf search "#rust" --types tweet --format json \
  | jq -r '.[].text' | grep -oE '#\w+' | sort | uniq -c | sort -rn

# 3. People you mention with topic
xf search "machine learning" --types tweet --format json \
  | jq -r '.[].text' | grep -oE '@\w+' | sort | uniq -c | sort -rn

# 4. Topics by DM conversation
xf search "project" --types dm --format json \
  | jq 'group_by(.metadata.conversation_id) | map({conv: .[0].metadata.conversation_id, topics: [.[].text[0:50]] | unique})'

# 5. Liked authors (who you engage with)
xf search "" --types like --format json --limit 1000 \
  | jq -r '.[].metadata.author_handle // empty' | sort | uniq -c | sort -rn | head -20
```

---

## Full Export Pipeline

**Goal:** Extract data for external analysis.

```bash
# 1. Export all tweets (JSONL for large archives)
xf export tweets --format jsonl -o tweets.jsonl

# 2. Export DMs (privacy-sensitive!)
xf export dms --format json -o dms.json

# 3. Export filtered subset
xf search "rust" --types tweet --format json --limit 10000 > rust_tweets.json

# 4. Export for spreadsheet
xf export tweets --format csv -o tweets.csv

# 5. Extract just text for NLP
xf export tweets --format json | jq -r '.[].text' > tweet_texts.txt

# 6. Build topic corpus
for topic in "rust" "python" "machine learning"; do
  xf search "$topic" --types tweet --format json --limit 1000 > "corpus_${topic// /_}.json"
done

# 7. Full archive backup
xf export all --format jsonl -o full_archive.jsonl
```

---

## Full Example: Research Workflow

**Scenario:** Research what you knew about "distributed systems" for a new project.

```bash
# 1. Initial scope
echo "=== Scope ==="
xf search "distributed systems" --format json | jq 'length'
# Found: 47 results

# 2. Your public thoughts
echo "=== Your Tweets ==="
xf search "distributed systems" --types tweet --format json \
  | jq '.[] | {date: .created_at[:10], text: .text[0:100], likes: .metadata.favorite_count}' | head -20

# 3. What you curated
echo "=== Liked Content ==="
xf search "distributed systems" --types like --format json \
  | jq '.[] | .text[0:120]' | head -10

# 4. Private discussions
echo "=== DM Threads ==="
xf search "distributed systems" --types dm --context --format json \
  | jq '.conversations | length'
# Found: 3 conversations

# 5. Grok conversations
echo "=== Grok Q&A ==="
xf search "distributed systems" --types grok --format json \
  | jq '.[] | {q: .text[0:80], mode: .metadata.grok_mode}'

# 6. Timeline
echo "=== Timeline ==="
xf search "distributed systems" --types tweet --format json \
  | jq -r '.[].created_at[:7]' | sort | uniq -c

# 7. Related topics
echo "=== Related Hashtags ==="
xf search "distributed systems" --format json \
  | jq -r '.[].text' | grep -oE '#\w+' | sort | uniq -c | sort -rn | head -10
```

---

## Pro Tips

### Parallel Searches for Coverage

Different phrasings = different hits. Run in parallel:

```bash
xf search "distributed systems" --format json &
xf search "microservices" --format json &
xf search "service mesh" --format json &
wait
```

### Save Common Queries

```bash
# ~/.bashrc
alias xf-tweets='xf search --types tweet --format json'
alias xf-dms='xf search --types dm --context --format json'
alias xf-grok='xf search --types grok --format json'
alias xf-likes='xf search --types like --format json'
```

### Quick Stats Check

```bash
xf stats --format json | jq 'to_entries | .[] | "\(.key): \(.value)"' -r
```
