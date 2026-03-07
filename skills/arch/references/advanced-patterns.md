# Advanced Architecture Patterns

## Architecture vs Agility Balance

The core tension: upfront planning avoids costly mistakes vs racing to MVP may render early architecture irrelevant.

### When to Invest in Architecture

| Condition | Architecture Investment | Rationale |
|-----------|------------------------|-----------|
| Quality failure is catastrophic | HIGH | Safety-critical, financial, reputation |
| High change cost after deployment | HIGH | Embedded systems, distributed data |
| Large team (>5 developers) | MEDIUM-HIGH | Coordination cost dominates |
| Uncertain requirements | LOW | Defer decisions, keep options open |
| Prototype/MVP stage | LOW | Validate market before scaling |
| Proven domain, stable requirements | MEDIUM | Apply known patterns efficiently |

**Heuristic**: Invest in architecture proportional to the cost of getting it wrong multiplied by the difficulty of changing it later.

### Information Hiding Principle

Anticipate change and encapsulate it:

1. **Identify likely changes** - What will evolve? (ML models, integrations, UI, data schemas)
2. **Encapsulate behind interfaces** - Define stable contracts around volatile implementations
3. **Isolate teams** - Changes within a module don't ripple across teams

**Example**: Anticipating ML model evolution:
```
❌ Tight coupling: Business logic calls model.predict() directly
✅ Loose coupling: Business logic calls PredictionService interface
   - Model can be swapped (v1 → v2, TensorFlow → PyTorch)
   - A/B testing via routing at interface level
   - Fallback strategies encapsulated
```

---

## Architectural Views as Maps

Different abstractions reveal different qualities. Like maps of the same city (neighborhoods, cycle paths, tourist attractions), architectural views serve different reasoning purposes.

### View Catalog

| View | Shows | Useful For | Quality Attributes |
|------|-------|------------|-------------------|
| **Functional** | Components, data flow, interfaces | Understanding what system does | Correctness, completeness |
| **Process** | Processes, threads, synchronization | Performance, concurrency analysis | Performance, scalability |
| **Development** | Modules, packages, build dependencies | Team organization, build time | Maintainability, modularity |
| **Deployment** | Nodes, networks, containers | Infrastructure planning | Availability, security, cost |
| **Data** | Entities, relationships, flows | Consistency, storage decisions | Integrity, privacy, compliance |
| **Security** | Trust boundaries, attack surfaces | Threat modeling | Confidentiality, integrity |

**Principle**: Create only the views that help you reason about the qualities you care about. Don't create views for documentation completeness.

---

## ML-Specific Architectural Patterns

### Pattern: Feature Store

**Intent**: Decouple feature engineering from model training/serving

**Problem**:
- Same features computed twice (training vs inference) → training-serving skew
- Feature code duplicated across projects
- Expensive features recomputed unnecessarily

**Solution**:
```
┌─────────────────┐      ┌──────────────┐      ┌────────────────┐
│  Raw Data       │ ──── │ Feature      │ ──── │ Feature Store  │
│  Sources        │      │ Engineering  │      │ (cache + catalog)│
└─────────────────┘      └──────────────┘      └───────┬────────┘
                                                       │
                    ┌──────────────────────────────────┤
                    │                                  │
                    ▼                                  ▼
           ┌───────────────┐              ┌────────────────────┐
           │ Training      │              │ Inference          │
           │ Pipeline      │              │ Service            │
           └───────────────┘              └────────────────────┘
```

**Trade-offs**:
- ✅ Eliminates training-serving skew
- ✅ Feature reuse across projects
- ✅ Central versioning and lineage
- ❌ Infrastructure complexity
- ❌ Latency for real-time features

**Fitness function**: `training_features == inference_features` for all feature vectors

---

### Pattern: Model-as-Service

**Intent**: Deploy ML model as independent, scalable service

**Solution**:
```
┌──────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Application  │────▶│ Model Service   │────▶│ Model Registry  │
│ (consumer)   │     │ (inference API) │     │ (versioned models)│
└──────────────┘     └─────────────────┘     └─────────────────┘
                            │
                     Load balancer
                            │
               ┌────────────┼────────────┐
               │            │            │
          ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
          │ Model   │  │ Model   │  │ Model   │
          │ v2.1    │  │ v2.1    │  │ v2.0    │  ← canary
          └─────────┘  └─────────┘  └─────────┘
```

**Trade-offs**:
- ✅ Independent scaling
- ✅ Independent deployment/rollback
- ✅ A/B testing, canary deployments
- ❌ Network latency
- ❌ Serialization overhead
- ❌ Operational complexity

**Fitness functions**:
- Inference latency p99 < threshold
- Model version consistency across replicas
- Canary error rate < baseline + margin

---

### Pattern: Retrieval-Augmented Generation (RAG)

**Intent**: Ground generative model responses in retrieved context

**Problem**: LLMs hallucinate, lack recent/proprietary knowledge, expensive to retrain

**Solution**:
```
User Query
    │
    ▼
┌─────────────────┐
│ Query Encoder   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ Vector Search   │────▶│ Document Store  │
│ (retriever)     │     │ (embeddings)    │
└────────┬────────┘     └─────────────────┘
         │
         ▼
   Retrieved Context
         │
         ▼
┌─────────────────┐
│ Prompt Assembly │  ← "Context: {docs}\nQuestion: {query}"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ LLM Generation  │
└────────┬────────┘
         │
         ▼
    Response
```

**Trade-offs**:
- ✅ Grounds responses in facts
- ✅ No retraining for new knowledge
- ✅ Auditability (can cite sources)
- ❌ Retrieval quality bounds generation quality
- ❌ Added latency (search + generation)
- ❌ Context window limits
- ⚠️ Privacy: model may leak retrieved content

**Sensitivity points**:
- Chunk size for embedding
- Top-K retrieval count
- Embedding model quality

---

### Pattern: Heartbeat/Dead-Man Timer

**Intent**: Detect component unavailability to trigger failover

**Solution**:
```
┌─────────────────┐                    ┌─────────────────┐
│ Observed        │ ──heartbeat──────▶ │ Monitor         │
│ Component       │    (every Ns)      │ Component       │
└─────────────────┘                    └────────┬────────┘
                                                │
                                    No heartbeat for N×2s?
                                                │
                                                ▼
                                       Trigger recovery
```

**Parameters**:
- Heartbeat interval (N): Lower = faster detection, higher network cost
- Missed threshold: 1 = aggressive, 3 = conservative

**ML application**: Monitor model inference service health, trigger fallback to simpler model or cached predictions.

---

## Common System Structures for ML

| Structure | ML Integration Pattern | When to Use |
|-----------|----------------------|-------------|
| **Client-Server** | Model inference as server | Single model, many clients |
| **Multi-tier (3-tier)** | Model in logic tier | Traditional enterprise + ML enhancement |
| **Microservices** | Model-as-service per capability | Multiple models, independent scaling |
| **Event-driven** | Model subscribes to data topics | Real-time streaming predictions |
| **Data-flow/Pipeline** | ML pipeline as DAG | Batch training, ETL with ML |
| **Monolithic** | Model as library import | Simple deployments, latency-critical |

---

## Design Pattern Communication Protocol

When discussing patterns, use this structure for efficient communication:

```
PATTERN: [Name]
INTENT: [1 sentence]
PROBLEM: [What quality attribute is unsatisfied]
SOLUTION: [Structural sketch]
TRADE-OFFS: [+/- quality impacts]
ALTERNATIVES: [Other patterns addressing same problem]
```

This raises discussion to pattern-level abstraction, avoiding re-explanation of well-known solutions.
