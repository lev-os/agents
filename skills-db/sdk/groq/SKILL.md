---
name: groq
description: |
  [WHAT] Fast LLM inference via Groq API (chat) + Ollama (embeddings)
  [HOW] Groq for chat completions (llama-3.3-70b-versatile), Ollama nomic-embed-text for embeddings
  [WHEN] Need fast inference, embedding text for RAG, chat completions
  [WHY] Groq provides fastest LLM inference; Ollama handles local embeddings (Groq has no embedding API)

  Triggers: "groq embed", "groq chat", "groq complete", "embed with groq", "fast llm"
---

# groq

Fast LLM inference via Groq API for chat, Ollama for embeddings.

## Setup

**Environment:**
- `GROQ_API_KEY` - Required for chat completions
- Ollama running locally for embeddings (`ollama serve`)

**Install dependencies:**
```bash
cd ~/.claude/skills/groq
pip install groq requests
```

**Pull embedding model (first time):**
```bash
ollama pull nomic-embed-text
```

## Usage

### Chat Completion

```bash
# Simple chat
./scripts/chat.py "Explain quantum computing in 2 sentences"

# With system prompt
./scripts/chat.py "Write a haiku" --system "You are a poet"

# Different model
./scripts/chat.py "Hello" --model llama-3.1-8b-instant

# JSON output
./scripts/chat.py "List 3 colors as JSON array" --json
```

### Embeddings

```bash
# Embed text (returns JSON array of floats)
./scripts/embed.sh "Hello world"

# Embed from stdin
echo "Some text to embed" | ./scripts/embed.sh

# Python direct
./scripts/embed.py "Hello world"
```

## Models

### Chat Models (Groq)
| Model | Context | Speed | Use Case |
|-------|---------|-------|----------|
| `llama-3.3-70b-versatile` | 128k | Fast | Default, general purpose |
| `llama-3.1-8b-instant` | 128k | Fastest | Simple tasks |
| `llama3-70b-8192` | 8k | Fast | Legacy |
| `gemma2-9b-it` | 8k | Fast | Instruction following |

### Embedding Model (Ollama)
| Model | Dimensions | Notes |
|-------|------------|-------|
| `nomic-embed-text` | 768 | Local, fast, good quality |

## Output Format

### Chat
Plain text response to stdout. Errors to stderr.

### Embed
JSON array of floats:
```json
[0.123, -0.456, 0.789, ...]
```

## When to Use

| Scenario | Command |
|----------|---------|
| Quick question | `./scripts/chat.py "What is X?"` |
| Code generation | `./scripts/chat.py "Write Python for Y"` |
| Embed for RAG | `./scripts/embed.sh "document text"` |
| Batch embed | `cat docs.txt \| while read line; do ./scripts/embed.sh "$line"; done` |

## Error Handling

- Missing `GROQ_API_KEY`: Chat fails with clear error
- Ollama not running: Embed falls back to error message
- Rate limits: Groq has generous limits but will return 429 if exceeded

## Related Skills

| Skill | Use When |
|-------|----------|
| **oracle** | Need GPT-5, Claude, multi-model comparison |
| **lev-find** | Unified search with embeddings already indexed |
| **brave-search** | Web search, not embeddings |
