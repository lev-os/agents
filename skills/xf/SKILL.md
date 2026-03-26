---
name: xf
description: >-
  Search X (Twitter) archives for insights, conversations, and knowledge. Use when
  mining tweets, DMs, Grok chats, likes, or extracting information from X data exports.
---

<!-- TOC: Goldmine | THE EXACT PROMPT | Quick Reference | When to Use | Critical Rules | The Heuristics | jq Essentials | References -->

# xf Knowledge Extraction

> **Core Insight:** Your X archive is a goldmine. Sub-millisecond search makes iterative exploration practical. Mine your history before rebuilding context.

## The Goldmine Principle

Your X archive contains:
- **Public thoughts** — Tweets capture your evolving thinking over years
- **Private conversations** — DMs hold detailed discussions, decisions, links shared
- **AI interactions** — Grok chats show what questions you asked and answers received
- **Curated content** — Likes reveal what resonated with you

**The insight:** Mining your X history surfaces forgotten context faster than rebuilding it.

---

## THE EXACT PROMPT — Discovery Workflow

```
1. Bootstrap: Check health, get archive overview
   xf doctor && xf stats --format json | jq '{tweets, likes, dms, grok_messages}'

2. Search: Find content by topic (hybrid mode default = best)
   xf search "KEYWORD" --format json --limit 50

3. Filter by type: Narrow to specific content
   xf search "KEYWORD" --types dm --context --format json    # DMs w/ conversation
   xf search "KEYWORD" --types grok --format json            # AI Q&A

4. Follow hits: Get full context
   xf tweet <ID> --thread --format json                      # Tweet thread
   xf search "KEYWORD" --types dm --context --format json    # Full DM thread

5. Extract: Export for analysis
   xf search "topic" --format json --limit 1000 | jq '[.[] | {text, date: .created_at}]'
```

### Why This Workflow Works

- **Hybrid search first** — Default mode combines keyword + semantic for best coverage
- **`--format json`** — Machine-readable output for piping to jq
- **`--context` for DMs** — Shows full conversation threads around matches
- **Iterate fast** — Sub-millisecond search enables exploration loops

---

## Quick Reference

```bash
# Health + overview (ALWAYS first)
xf doctor && xf stats --format json

# Search modes (hybrid is default = best)
xf search "query" --format json                   # Hybrid (keyword + semantic)
xf search "exact phrase" --mode lexical           # Keyword only (BM25)
xf search "feeling stressed" --mode semantic      # Meaning-based

# Filter by content type
xf search "query" --types tweet --format json     # Your tweets
xf search "query" --types dm --context            # DMs with full conversation
xf search "query" --types like --format json      # Liked tweets
xf search "query" --types grok --format json      # Grok AI chats

# Date filtering
xf search "query" --since "2024-01" --until "2024-06" --format json
xf search "query" --since "last week" --format json

# Output control
xf search "query" --limit 100 --offset 50 --format json
```

---

## When to Use What

| You Want | Use | Why |
|----------|-----|-----|
| Find content by topic | `--mode hybrid` (default) | Best of keyword + semantic |
| Find exact phrase | `--mode lexical` + `"quotes"` | Literal string match |
| Find conceptually related | `--mode semantic` | "feeling overwhelmed" → burnout tweets |
| DM conversations | `--types dm --context` | Shows full thread around matches |
| What you engaged with | `--types like` | Your curation over time |
| AI Q&A history | `--types grok` | What you asked Grok |
| High engagement content | `--sort engagement` | Your best tweets |

---

## Critical Rules

| Rule | Why | Consequence |
|------|-----|-------------|
| **`--format json`** | Machine-readable output | Required for jq pipelines |
| **Index first** | Archive must be indexed | `xf index` before search |
| **`--context` requires `--types dm`** | Only works for DMs | Ignored otherwise |
| **All data local** | Zero network calls | Privacy-first, offline-capable |

---

## The Heuristics

| Signal | Meaning | Action |
|--------|---------|--------|
| Many likes on topic | Topic resonated with you | Search likes for curated content |
| DM mentions project | Detailed private discussion | Use `--context` to get full thread |
| Grok chat on topic | You asked AI about it | May have refined explanations |
| High engagement tweet | Your audience resonated | Check thread for discussion |
| Semantic finds more | Wording varies | Use semantic for broad exploration |

---

## jq Essentials

```bash
# Extract just text
| jq '.[].text'

# Text with dates
| jq '.[] | {text, date: .created_at}'

# Filter by engagement
| jq '[.[] | select(.favorite_count > 10)]'

# Count by year
| jq -r '.[].created_at[:4]' | sort | uniq -c

# DM conversation IDs
| jq '[.[].metadata.conversation_id] | unique'

# Find hashtags
| jq -r '.[].text' | grep -oE '#\w+' | sort | uniq -c | sort -rn
```

---

## References

| Need | Reference |
|------|-----------|
| Full command reference | [COMMANDS.md](references/COMMANDS.md) |
| Workflow recipes | [RECIPES.md](references/RECIPES.md) |
| jq patterns | [PATTERNS.md](references/PATTERNS.md) |
| Pitfalls & fixes | [PITFALLS.md](references/PITFALLS.md) |
| X archive data structures | [DATA_STRUCTURES.md](references/DATA_STRUCTURES.md) |

---

## Scripts

| Script | Usage |
|--------|-------|
| `bash scripts/quick_analysis.sh` | One-command archive overview |
| `python3 scripts/topic_miner.py "topic"` | Deep dive on a topic |
| `bash scripts/validate.sh` | Validate xf is working |

---

## Validation

```bash
# Quick health check
xf doctor

# Should show: all checks pass
```

If issues: run `xf index --force` to rebuild.
