---
name: Fine-Tuning Strategies
description: Adapt pre-trained foundation models to specific tasks/domains by continuing training on targeted data
---

# Fine-Tuning Strategies for LLMs

## Classification
- **Domain**: Computer Science, AI/ML
- **Category**: Transfer Learning & Model Adaptation
- **Novelty**: 7/10 (rapidly evolving field, new methods emerging)
- **Practitioner Evidence**: 10/10 (industry standard, validated at scale)

## Mental Model
Fine-tuning adapts a pre-trained foundation model to specific tasks/domains by continuing training on targeted data. Like hiring an experienced generalist and providing domain-specific training—the model retains broad knowledge while gaining specialized expertise. Parameter-efficient methods (LoRA, adapters) train tiny modules instead of all weights, like teaching shortcuts rather than rewriting the entire manual.

## When to Use
- Pre-trained model exists but lacks domain-specific knowledge (medical, legal, code)
- Behavior modification needed (instruction-following, safety alignment, style matching)
- Task performance insufficient with prompting alone (complex reasoning, low-resource languages)
- Cost/latency constraints favor smaller specialized model over large general model
- Data privacy requires on-premise model (can't use APIs for sensitive data)

## Core Framework

### 1. Fine-Tuning Method Selection
**Choose appropriate strategy based on resources and requirements**

**Full Fine-Tuning**:
- Update all model parameters during training
- Highest quality, requires most compute (100% parameter updates)
- Use when: Best possible accuracy required, sufficient compute available (multi-GPU)
- Memory: ~4x model size (model + gradients + optimizer states + activations)

**Parameter-Efficient Fine-Tuning (PEFT)**:
- Train small subset of parameters (adapters, LoRA, prefix tuning)
- 50-70% cost reduction vs. full fine-tuning, near-equivalent accuracy
- Use when: Limited GPU memory, need multiple task-specific versions, fast iteration
- Memory: ~1.2x model size (base model frozen, train tiny modules)

**Feature Extraction** (transfer learning baseline):
- Freeze all layers except output head, train only final classifier
- Fastest, cheapest, lowest quality for complex tasks
- Use when: Dataset very small (<1K examples), highly related to pre-training task

### 2. LoRA (Low-Rank Adaptation)
**Most popular PEFT method - inject trainable rank decomposition matrices**

**How LoRA Works**:
- Freeze pre-trained weights W, add trainable matrices A and B: W + AB
- A is (d × r), B is (r × d) where r << d (rank 4-64 typical)
- Only train A, B (0.1-1% of parameters), merge back into W after training

**LoRA Configuration**:
- Rank (r): Higher = more capacity but more parameters (4-8 for simple, 16-64 for complex)
- Alpha: Scaling factor for LoRA updates (typically alpha = 2r or r)
- Target modules: Apply to query/value projections (QV) or all linear layers (QKVO)
- Dropout: 0.05-0.1 on LoRA layers to prevent overfitting

**LoRA Variants**:
- **QLoRA**: Quantize base model to 4-bit (NF4), train LoRA adapters (75% memory reduction)
- **DoRA**: Weight-decomposed LoRA for better convergence
- **AdaLoRA**: Adaptive rank allocation across layers based on importance

### 3. Adapter Methods
**Insert small trainable modules between frozen transformer layers**

**Bottleneck Adapters**:
- Add down-projection (d → r) → activation → up-projection (r → d) after each layer
- Typical bottleneck size: 64-256 dimensions (vs. 4096+ model hidden size)
- 2-5% additional parameters, 30-50% cost reduction vs. full fine-tuning

**Prefix Tuning**:
- Prepend trainable continuous vectors to key/value in each attention layer
- Prefix length: 10-50 tokens worth of virtual "instructions"
- Use when: Few-shot learning, want to condition model without changing weights

**IA3 (Infused Adapter by Inhibiting and Amplifying Inner Activations)**:
- Learn multiplicative scaling vectors for activations (even smaller than LoRA)
- 0.01% parameters, competitive with LoRA on many tasks

### 4. Data Preparation & Quality
**Prepare high-quality training data for effective fine-tuning**

**Data Volume Guidelines**:
- Instruction tuning: 2K-10K diverse examples minimum
- Domain adaptation: 10K-100K domain-specific documents
- Task-specific: 500-5K task examples (depends on task complexity)
- Quality > quantity: 1K high-quality > 10K noisy examples

**Data Format**:
- Instruction-following: (instruction, input, output) triplets
- Conversational: Multi-turn dialogues with system/user/assistant roles
- Domain text: Unstructured documents for continued pre-training
- Ensure format matches target use case (not just Q&A if building chatbot)

**Data Quality Checklist**:
- Diverse coverage of target task variations
- High-quality human-written or carefully filtered outputs
- Balanced representation (avoid demographic/topic biases)
- Decontaminated (remove benchmark test sets from training data)

### 5. Training Configuration
**Set hyperparameters for stable, effective fine-tuning**

**Learning Rate**:
- Full fine-tuning: 1e-5 to 5e-5 (much smaller than pre-training)
- LoRA/PEFT: 1e-4 to 3e-4 (can be higher since fewer parameters)
- Use warmup: 3-10% of steps for gradual ramp-up
- Scheduler: Linear decay or cosine decay to 0

**Batch Size & Gradient Accumulation**:
- Effective batch size: 32-128 for most tasks (instruction tuning)
- Use gradient accumulation if GPU memory limited (micro-batch 1-4, accumulate 8-32 steps)
- Larger batches = more stable but slower adaptation

**Epochs & Early Stopping**:
- 1-5 epochs typical (more = overfitting risk)
- Monitor validation loss/metrics, stop if no improvement for 2-3 evaluations
- Save checkpoints every epoch for best model selection

**Regularization**:
- Dropout: 0.1 on adapters/LoRA, 0.0-0.05 on full fine-tuning
- Weight decay: 0.01-0.1 (L2 regularization on trainable parameters)

### 6. Evaluation & Iteration
**Measure fine-tuning effectiveness and iterate**

**Quantitative Metrics**:
- Task-specific: Accuracy, F1, BLEU, ROUGE depending on task
- Perplexity: Lower = better language modeling (for domain adaptation)
- General capabilities: Test on held-out benchmarks (MMLU, GSM8K) to ensure no regression

**Qualitative Evaluation**:
- Manual review of 50-100 model outputs across diverse inputs
- Check for: Hallucinations, off-topic responses, style inconsistency, safety issues
- A/B test vs. base model with real users when possible

**Iteration Strategy**:
- Start small: 1K examples, LoRA rank 8, 1 epoch → quick baseline
- Scale up: Add data, increase rank/epochs if underfitting
- Diagnose: Overfitting (train high, val low) → reduce epochs/rank; Underfitting (both low) → add capacity/data

### 7. Deployment & Multi-Adapter Serving
**Deploy fine-tuned models efficiently in production**

**Single-Task Deployment**:
- Merge LoRA weights back into base model (no inference overhead)
- Quantize for deployment (GPTQ, AWQ, GGUF) to reduce memory/cost
- Serve via standard inference frameworks (vLLM, TensorRT-LLM, HuggingFace TGI)

**Multi-Adapter Serving**:
- Keep base model in memory, load LoRA adapters dynamically per request
- Serve 10-100+ specialized models with single base model instance
- Use adapter routing: Route requests to appropriate adapter based on task/user
- Tools: Predibase, Replicate, custom vLLM with LoRA support

## Practical Application

### Customer Support Chatbot (Instruction Tuning)
**Problem**: GPT-3.5 too generic, needs company-specific knowledge and tone
**Fine-Tuning Solution**:
1. Collect 5K customer service conversations (historical tickets + human-written responses)
2. Format as instruction-response pairs (query, context, ideal_response)
3. Fine-tune Llama-3-8B with LoRA (rank=16, alpha=32, QV layers)
4. 3 epochs, lr=2e-4, batch=64 (8 micro-batch × 8 accumulation steps)
5. Evaluate on held-out tickets, compare response quality vs. base model
**Result**: 35% reduction in response time, 25% increase in CSAT, 4x cheaper than GPT-4 API

### Medical Report Generation (Domain Adaptation)
**Problem**: General LLM hallucinates medical terminology, misses critical details
**Fine-Tuning Solution**:
1. Curate 50K radiology reports (anonymized clinical data)
2. Continued pre-training (next-token prediction on domain text) for 1 epoch
3. Then instruction fine-tune on 3K (imaging_findings → clinical_report) pairs
4. Use QLoRA (4-bit base, rank=32) to fit 70B model on single A100
5. Validate with radiologist review (accuracy, completeness, safety)
**Result**: 90% clinician acceptance rate (vs. 60% for GPT-4), compliant with privacy requirements

### Code Generation for Internal APIs (Task-Specific)
**Problem**: Copilot doesn't know company's internal APIs and conventions
**Fine-Tuning Solution**:
1. Extract 20K code snippets from company repos (focus on API usage)
2. Generate (docstring → code) pairs using existing well-documented functions
3. Fine-tune CodeLlama-13B with LoRA (rank=8, QKVO layers)
4. 2 epochs, lr=1e-4, add 0.1 dropout to prevent overfitting on API patterns
5. Test on hidden internal functions, measure correctness + style adherence
**Result**: 70% acceptance rate for suggested completions (vs. 35% for base Copilot)

## Edge Cases & Nuances

**Catastrophic Forgetting**: Fine-tuning erases general capabilities
- Use smaller learning rate (1e-5 vs. 1e-4), fewer epochs (1-2 vs. 3-5)
- Mix general instruction data (10-20%) with domain-specific data
- Evaluate on general benchmarks (MMLU) to detect regression
- Consider multi-task fine-tuning: Train on target task + diverse auxiliary tasks

**Overfitting on Small Datasets**: Model memorizes training data
- Strong regularization (dropout 0.2, weight decay 0.1)
- Data augmentation: Paraphrase instructions, back-translate examples
- Use smaller model (7B instead of 70B) if dataset <5K examples
- Early stopping based on validation metrics (not training loss)

**Distribution Mismatch**: Training data doesn't match deployment inputs
- Collect production data samples, manually label subset for validation
- Iterative deployment: Fine-tune → deploy → collect failures → retrain
- Active learning: Identify low-confidence predictions, prioritize for labeling

**Adapter Interference**: Multiple LoRA adapters conflict when combined
- Composition methods: Sequential (adapter1 → adapter2), merged (weighted average)
- Orthogonalization techniques to reduce interference between adapters
- Alternatively: Train multi-task adapter from scratch instead of composing

## Anti-Patterns

**Fine-Tuning When Prompting Sufficient**: Wasting resources when few-shot prompting works
**Using Tiny Datasets**: Attempting fine-tuning with <500 examples (prompt engineering better)
**No Validation Set**: Overfitting without realizing, no way to select best checkpoint
**Copying Benchmark Data**: Training on test sets, inflated metrics, poor generalization

## Trade-offs

**Full Fine-Tuning vs. LoRA**:
- Full: Highest quality (+2-5% on benchmarks), 10x compute cost, single specialized model
- LoRA: 95% of full quality, 10% compute cost, can serve many adapters simultaneously

**LoRA Rank Selection**:
- Low rank (4-8): Faster, less overfitting, sufficient for simple tasks
- High rank (32-64): More capacity, better for complex tasks, higher memory/compute

**Training Duration**:
- 1 epoch: Fast, less overfitting, may underfit complex tasks
- 3-5 epochs: Better fit, overfitting risk, diminishing returns after 3

## Related Frameworks
- **Prompt Engineering**: Zero-shot alternative to fine-tuning (try first)
- **RAG (Retrieval-Augmented Generation)**: Inject knowledge without training (complementary)
- **Distillation**: Compress fine-tuned large model into smaller model
- **RLHF (Reinforcement Learning from Human Feedback)**: Align model to human preferences
- **Continued Pre-training**: Further pre-train on domain corpus before task fine-tuning

## Practitioner Sources
- **Chip Huyen - AI Engineering**: Fine-tuning in production, best practices, cost analysis
- **HuggingFace PEFT Library**: LoRA, adapters, prefix tuning implementations
- **Databricks LoRA Guide**: Optimal parameter selection, efficiency benchmarks
- **Google ML Design Patterns**: Transfer learning patterns, feature extraction strategies
- **Predibase Blog**: Multi-adapter serving, LoRA in production at scale
- **Microsoft DeepSpeed**: Memory-efficient training, ZeRO optimization for fine-tuning
