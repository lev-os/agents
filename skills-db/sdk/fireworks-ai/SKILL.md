---
name: fireworks-ai
description: |
  [WHAT] Fast, cost-effective inference and fine-tuning for open-source LLMs via OpenAI-compatible APIs
  [HOW] Serverless inference, on-demand GPU deployments, LoRA fine-tuning (SFT, RFT, DPO), firectl CLI
  [WHEN] Use when deploying open-source models, fine-tuning for custom use cases, or migrating from OpenAI
  [WHY] 100+ models, prompt caching, batch inference, multi-LoRA deployments, reinforcement fine-tuning

  Triggers: "fireworks", "fireworks ai", "fireworks.ai", "firectl", "fireworks api",
            "fine-tune llama", "fine-tune qwen", "fine-tune deepseek", "LoRA fine-tuning",
            "reinforcement fine-tuning", "RFT", "SFT", "DPO", "serverless inference",
            "on-demand deployment", "multi-lora", "prompt caching", "batch inference",
            "openai compatible", "migrate from openai"
---

# Fireworks AI Skill

Fast, cost-effective access to 100+ open-source models with OpenAI-compatible APIs, LoRA fine-tuning, and advanced deployment options.

## When to Use This Skill

| Scenario | Example | Relevant Section |
|----------|---------|------------------|
| Query text models | "Chat completion with Llama" | Quick Reference → Chat Completion |
| Fine-tune a model | "Train model on my data" | Fine-Tuning Overview |
| Deploy custom model | "On-demand GPU deployment" | Deployments |
| Migrate from OpenAI | "Use OpenAI SDK with Fireworks" | OpenAI Compatibility |
| Batch processing | "Process 10K prompts offline" | Batch Inference |
| Image generation | "FLUX Kontext image editing" | Image Generation |
| Embeddings/RAG | "Generate embeddings for search" | Embeddings & Reranking |
| CLI operations | "firectl commands" | firectl Reference |

## Quick Reference

### Chat Completion (OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key="<YOUR_FIREWORKS_API_KEY>",
)

chat_completion = client.chat.completions.create(
    model="accounts/fireworks/models/llama-v3p1-8b-instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say this is a test"},
    ],
)
print(chat_completion.choices[0].message.content)
```

### Chat Completion (curl)

```bash
curl --request POST \
     --url https://api.fireworks.ai/inference/v1/chat/completions \
     --header "accept: application/json" \
     --header "authorization: Bearer $FIREWORKS_API_KEY" \
     --header "content-type: application/json" \
     --data '{
       "model": "accounts/fireworks/models/llama-v3p1-8b-instruct",
       "messages": [{"role": "user", "content": "Hello!"}]
     }'
```

### Supervised Fine-Tuning Job

```bash
firectl supervised-fine-tuning-job create \
  --base-model accounts/fireworks/models/llama-v3p1-8b-instruct \
  --dataset my-training-dataset \
  --output-model my-fine-tuned-model \
  --epochs 3 \
  --learning-rate 1e-4 \
  --lora-rank 8
```

### Create Dataset for Fine-Tuning

```python
from fireworks.client import Dataset

dataset = Dataset.from_file(
    "path/to/training_data.jsonl",
    name="my-training-dataset"
)
# Dataset is now available on Fireworks for fine-tuning
```

### Monitor Training Progress

```python
while not job.is_completed:
    job.raise_if_bad_state()
    print(f"Training state: {job.state}")
    time.sleep(10)
    job = job.get()

print(f"Training completed! New model: {job.output_model}")
```

### Deploy Fine-Tuned Model (Multi-LoRA)

```python
from fireworks import LLM

base_model = LLM(
    model="accounts/fireworks/models/llama-v3p2-3b-instruct",
    deployment_type="on-demand",
    id="shared-base-deployment",
    enable_addons=True
)
```

### Generate Embeddings

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key="<YOUR_FIREWORKS_API_KEY>",
)

response = client.embeddings.create(
    model="fireworks/qwen3-embedding-8b",
    input="Your text to embed"
)
embeddings = response.data[0].embedding
```

### Export Billing Metrics

```bash
firectl billing export-metrics \
  --start-time "2025-01-01" \
  --end-time "2025-01-31" \
  --filename january_metrics.csv
```

### Create Deployment

```bash
firectl deployment create accounts/fireworks/models/deepseek-v3 \
  --deployment-shape throughput
```

## Key Concepts

### Fine-Tuning Methods

| Method | Use Case | When to Use |
|--------|----------|-------------|
| **SFT** (Supervised) | Classification, extraction | Large labeled dataset (~1000+ examples) |
| **RFT** (Reinforcement) | Complex reasoning, agents | Small dataset, verifiable outputs, multi-step tasks |
| **DPO** (Preference) | Alignment, style | Pairwise preference comparisons |

**Decision Tree:**
- Have 1000+ labeled examples? → **SFT**
- Task is verifiable but lacks golden outputs? → **RFT**
- Want to align with preferences? → **DPO**

### LoRA (Low-Rank Adaptation)

Fireworks uses LoRA for efficient fine-tuning:
- **Faster & cheaper** - Train in hours, not days
- **Easy to deploy** - Instant deployment on Fireworks
- **Flexible** - Run multiple LoRAs on single base deployment

### Deployment Types

| Type | Use Case | Scaling |
|------|----------|---------|
| **Serverless** | Variable traffic, cost optimization | Auto-scale to zero |
| **On-Demand** | Consistent performance, high throughput | Dedicated GPUs |
| **Reserved** | Predictable workloads, discounts | Pre-purchased capacity |

### Agent Tracing (RFT)

For reinforcement fine-tuning with agents:
1. Use `model_base_url` from trainer (points to `tracing.fireworks.ai`)
2. Attach `FireworksTracingHttpHandler` for structured logging
3. Log `Status.rollout_finished()` or `Status.rollout_error()` on completion
4. Trainer joins traces + logs via `rollout_id`

## API Compatibility

Fireworks is **OpenAI-compatible**. Key differences:

| Feature | OpenAI | Fireworks |
|---------|--------|-----------|
| `max_tokens` overflow | Error | Auto-truncate (configurable) |
| Streaming usage stats | Not returned | Returned in final chunk |
| Model names | `gpt-4` | `accounts/fireworks/models/llama-v3p1-8b-instruct` |

Set `context_length_exceeded_behavior: "error"` for OpenAI-like behavior.

## firectl CLI Quick Reference

```bash
# Authentication
firectl login

# Account operations
firectl account list

# Dataset operations
firectl dataset download <dataset-id>
firectl dataset list

# Fine-tuning jobs
firectl supervised-fine-tuning-job create --help
firectl supervised-fine-tuning-job list
firectl dpo-job resume <job-id>

# Deployments
firectl deployment create <model> --deployment-shape <shape>
firectl deployment scale <deployment-id> --replicas <n>

# Evaluators
firectl evaluator-revision get <evaluator-id>

# Billing
firectl billing export-metrics
```

## Available Models (Highlights)

**Text Models:**
- DeepSeek V3, DeepSeek R1
- Llama 3.1/3.2/3.3 (8B, 70B, 405B)
- Qwen 2.5 family
- Kimi K2

**Embedding Models:**
- `fireworks/qwen3-embedding-8b` (serverless)
- `fireworks/qwen3-embedding-4b`
- `nomic-ai/nomic-embed-text-v1.5`

**Reranking Models:**
- `fireworks/qwen3-reranker-8b` (serverless)

**Image Models:**
- FLUX Kontext Pro/Max
- SDXL ControlNet

Browse all: https://fireworks.ai/models

## Reference Files

| File | Content | Use For |
|------|---------|---------|
| `references/llms-txt.md` | Complete API reference (410 pages) | Detailed API docs, all CLI commands, parameters |

**Navigation tips:**
- Search for specific CLI commands: `firectl <command>`
- API endpoints follow pattern: `/v1/accounts/{account_id}/<resource>`
- Fine-tuning docs under `#fine-tuning-*` sections
- Deployment docs under `#deployment-*` sections

## Working with This Skill

### For Beginners

1. Start with Chat Completion example above
2. Get API key from https://app.fireworks.ai
3. Use OpenAI SDK (familiar interface)
4. Try serverless models first (no deployment needed)

### For Fine-Tuning

1. Prepare JSONL dataset with `messages` format
2. Upload with `Dataset.from_file()` or `firectl`
3. Choose fine-tuning method (SFT/RFT/DPO)
4. Monitor with `firectl supervised-fine-tuning-job list`
5. Deploy LoRA or merge into base model

### For Production

1. Consider on-demand deployments for consistent performance
2. Enable prompt caching for repeated prefixes
3. Use batch inference for offline processing
4. Monitor usage via billing export or dashboard
5. Set up service accounts for CI/CD

## Common Patterns

### Streaming with Usage Stats

```python
for chunk in client.chat.completions.create(stream=True, ...):
    if chunk.usage:  # Available in final chunk
        print(f"Tokens: {chunk.usage.total_tokens}")
```

### Variable-Length Embeddings

```python
response = client.embeddings.create(
    model="fireworks/qwen3-embedding-8b",
    input="Your text",
    dimensions=128  # Reduce from default for faster similarity
)
```

### Reranking Documents

```python
# Using /rerank endpoint
response = client.post("/rerank", json={
    "model": "fireworks/qwen3-reranker-8b",
    "query": "search query",
    "documents": ["doc1", "doc2", "doc3"]
})
```

## Resources

- **Model Library:** https://fireworks.ai/models
- **Playground:** https://app.fireworks.ai/playground
- **Usage Dashboard:** https://app.fireworks.ai/account/usage
- **API Reference:** https://docs.fireworks.ai/api-reference
- **firectl Docs:** https://docs.fireworks.ai/tools-sdks/firectl

## Notes

- Generated from official Fireworks AI documentation (410 pages)
- OpenAI SDK examples work directly with Fireworks
- Model names use `accounts/fireworks/models/<model-name>` format
- Fine-tuning uses LoRA by default (set `--lora-rank 0` for full parameter)
