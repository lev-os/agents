---
name: online-learning
description: Online learning updates models continuously as new data arrives, one sample at a time or in mini-batches, without retraining from scratch
---

# Online Learning Pattern

## Classification
- **Domain**: Computer Science, AI/ML
- **Category**: ML System Design Patterns
- **Novelty**: 8/10 (advanced pattern for continuous adaptation)
- **Practitioner Evidence**: 9/10 (Kafka-ML, research-backed, emerging production use)

## Mental Model
Online learning (incremental learning) updates models continuously as new data arrives, one sample at a time or in mini-batches, without retraining from scratch. Like learning a language through daily conversations versus intensive courses—knowledge accumulates gradually through exposure, adapting to new patterns without forgetting fundamentals.

## When to Use
- Data distribution shifts frequently (concept drift, user behavior changes)
- Retraining entire model is too expensive or slow (large datasets, limited compute)
- Fresh predictions critical (stock trading, recommendation systems, personalization)
- Continuous labeled feedback available (user clicks, transaction outcomes, sensor readings)
- Model must adapt to new classes/patterns without catastrophic forgetting

## Core Framework

### 1. Learning Scenario Selection
**Choose appropriate incremental learning paradigm**

**Domain-Incremental Learning (DI)**:
- Data distribution changes over time but task stays same
- Example: Spam detection adapting to new spam tactics
- Use when: Input patterns evolve but output categories fixed

**Task-Incremental Learning (TI)**:
- Multiple related tasks learned sequentially
- Example: Multi-language translation learned one language pair at a time
- Use when: Related tasks arrive incrementally, task ID known at test time

**Class-Incremental Learning (CI)**:
- New output classes added over time
- Example: Product categorization with new product types added monthly
- Use when: Output space grows, must classify new + old classes without task ID

### 2. Catastrophic Forgetting Prevention
**Prevent performance degradation on old data when learning new patterns**

**Regularization-Based Methods**:
- Elastic Weight Consolidation (EWC): Penalize changes to important weights (Fisher information)
- Learning without Forgetting (LwF): Preserve old predictions via knowledge distillation
- Synaptic Intelligence: Track weight importance during learning, protect critical weights

**Replay-Based Methods**:
- Experience Replay: Store subset of old examples, mix with new data during updates
- Generative Replay: Use generative model to synthesize old data patterns for rehearsal
- Hybrid: Combine small memory buffer (1-5% of data) with regularization

**Architecture-Based Methods**:
- Progressive Neural Networks: Add new sub-networks for new tasks, freeze old ones
- Dynamic Expandable Representation: Grow model capacity selectively for new patterns

### 3. Data Stream Processing Architecture
**Configure infrastructure for continuous learning**
- Stream data from Kafka/Kinesis topics (labeled_examples, user_feedback)
- Implement sliding window for mini-batch updates (100-1000 samples per update)
- Use stateful stream processing (Flink, Kafka Streams) for aggregating gradients
- Checkpoint model state periodically (every N updates) for fault tolerance

### 4. Incremental Update Algorithm
**Apply efficient gradient updates without full retraining**

**Stochastic Gradient Descent (SGD) Variants**:
- Process each example: compute loss → gradient → update weights
- Use adaptive learning rates (AdaGrad, RMSprop, Adam) for stability
- Decay learning rate over time (prevent oscillation as knowledge accumulates)

**Mini-Batch Updates**:
- Accumulate 50-500 examples → compute average gradient → update
- Balance: Larger batches = stable updates, smaller batches = faster adaptation
- Use gradient clipping to prevent exploding gradients from outliers

**Second-Order Methods** (for shallow models):
- Online Newton Step, Online AROW for linear/logistic models
- More sample-efficient but higher computational cost per update

### 5. Model Evaluation & Drift Detection
**Monitor performance and detect when retraining needed**
- Track metrics on validation stream (separate from training stream)
- Detect drift: Compare recent performance vs. baseline (sliding window metrics)
- Use statistical tests (Kolmogorov-Smirnov, Page-Hinkley) for distribution shift
- Trigger full retraining if online updates can't recover performance

### 6. Hyperparameter Adaptation
**Adjust learning configuration based on stream characteristics**
- Start with higher learning rate (faster initial adaptation), decay over time
- Increase batch size as data accumulates (more stable updates with more data)
- Adjust regularization strength based on forgetting rate (EWC lambda parameter)
- Use meta-learning to tune hyperparameters online (learn learning rate schedules)

### 7. Production Deployment Strategy
**Safely deploy continuously updating models**
- Shadow mode: Run online learner alongside static model, compare predictions
- Canary deployment: Route 5-10% traffic to online model, monitor metrics
- A/B testing: Compare online learning vs. periodic batch retraining
- Rollback mechanism: Revert to previous checkpoint if performance degrades

## Practical Application

### Personalized News Recommendations
**Problem**: User interests change rapidly, daily retraining too slow
**Online Learning Solution**:
1. User interactions stream to Kafka (user_id, article_id, click, timestamp)
2. Flink aggregates interactions into mini-batches (500 examples per 30 seconds)
3. Neural collaborative filtering model updates via Adam optimizer (lr=0.001, decay=0.999)
4. Experience replay: Buffer 10K recent examples, mix 20% old + 80% new per batch
5. Track click-through rate per user segment, rollback if drops >5% from baseline
**Result**: 15% CTR improvement vs. daily batch retraining, 2-hour adaptation to trending topics

### Fraud Detection with Evolving Tactics
**Problem**: Fraudsters adapt tactics weekly, batch models lag behind
**Online Learning Solution**:
1. Transaction outcomes stream with 24-hour label delay (fraud confirmed/denied)
2. Gradient boosting model (XGBoost) with incremental updates (learning_rate=0.05)
3. Store 5K recent fraud examples in memory buffer for replay (prevent forgetting fraud patterns)
4. Page-Hinkley test monitors false positive rate (alert if statistically significant spike)
5. Full retraining triggered monthly or when drift detector fires
**Result**: 40% faster detection of new fraud patterns, 8% reduction in false positives

### Product Categorization with New Product Types
**Problem**: New product categories added monthly (CI scenario)
**Online Learning Solution**:
1. New products labeled by ops team, streamed to training pipeline
2. Dynamic class-incremental learning: Add output neurons for new categories
3. Knowledge distillation: Freeze old predictions, only update for new classes
4. Balanced sampling: Equal representation of new classes + old classes in mini-batches
5. Evaluate on held-out old classes to detect catastrophic forgetting (>2% drop triggers intervention)
**Result**: Support 50 new categories/month without full retraining, maintain 95% accuracy on old classes

## Edge Cases & Nuances

**Label Delay**: Feedback arrives hours/days after prediction
- Use delayed reward learning: Buffer predictions, apply updates when labels arrive
- Implement temporal credit assignment (which prediction led to outcome?)
- Consider imbalanced delayed feedback (positive outcomes reported faster than negative)

**Outlier Robustness**: Adversarial examples or noise in stream
- Use robust loss functions (Huber loss instead of MSE, focal loss for class imbalance)
- Implement anomaly detection filter before model updates (flag suspicious examples)
- Apply gradient clipping (cap gradient magnitude at 1.0-10.0)

**Cold Start for New Entities**: New users/items without history
- Initialize embeddings with content-based features or cluster averages
- Use meta-learning (MAML) for fast adaptation with few examples
- Fallback to population statistics until entity-specific data accumulates

**Memory Constraints**: Limited storage for replay buffers
- Prioritize examples for replay (reservoir sampling, importance weighting)
- Use coreset construction: Select representative subset of old data
- Compress experiences via generative model (GAN, VAE) for synthetic replay

## Anti-Patterns

**No Forgetting Prevention**: Pure SGD on new data, forgetting old patterns within hours
**Ignoring Data Distribution Shifts**: Blindly updating without drift detection or evaluation
**Over-Aggressive Learning Rates**: High LR causing oscillation and catastrophic forgetting
**No Rollback Strategy**: Deploying continuously updating model without safety nets

## Trade-offs

**Online Learning vs. Batch Retraining**:
- Online: Continuous adaptation, low latency updates, risk of drift/instability
- Batch: Stable performance, expensive retraining, lag in adaptation

**Replay Buffer Size**:
- Larger (10% of data): Better retention, higher memory cost, slower updates
- Smaller (1% of data): Memory-efficient, faster updates, more forgetting risk

**Update Frequency**:
- High (every 100 examples): Fast adaptation, potential instability, high compute
- Low (every 10K examples): Stable updates, slower adaptation, bursty resource usage

## Related Frameworks
- **Streaming Inference Pattern**: Real-time predictions on streaming data (inference side)
- **Batch Processing Pattern**: Full retraining periodically (alternative to online learning)
- **Continual Learning**: Broader field including task-incremental, class-incremental scenarios
- **Transfer Learning**: Pre-train on large dataset, fine-tune on specific task (related adaptation strategy)
- **Active Learning**: Select most informative examples for labeling (complement to online learning)

## Practitioner Sources
- **Kafka-ML Framework**: Online learning infrastructure with Kafka + TensorFlow/PyTorch
- **IBM Continual Learning**: Survey of methods, catastrophic forgetting solutions
- **Nature Machine Intelligence** (2022): Three types of incremental learning taxonomy
- **Flink ML**: Apache Flink for online model training and drift detection
- **Chip Huyen - ML Systems Design**: Online learning in production systems, best practices
