---
name: ml-batch-processing
description: Batch processing decouples prediction from real-time requests by pre-computing predictions on scheduled intervals
---

# ML Batch Processing Pattern

## Classification
- **Domain**: Computer Science, AI/ML
- **Category**: ML System Design Patterns
- **Novelty**: 6/10 (established pattern with modern evolution)
- **Practitioner Evidence**: 10/10 (Google, industry standard)

## Mental Model
Batch processing decouples prediction from real-time requests by pre-computing predictions on scheduled intervals. Like meal prep for the week instead of cooking each meal on-demand—you process predictions in bulk during off-peak hours, store results, and serve them instantly when requested.

## When to Use
- Predictions needed for all users/items at regular intervals (daily recommendations, weekly reports)
- Training data arrives in batches rather than continuously
- Cost optimization prioritized over real-time freshness (batch = cheaper compute)
- Predictions can tolerate staleness (hours/days old acceptable)
- High-throughput scenarios where latency isn't critical

## Core Framework

### 1. Schedule Determination
**Identify prediction cadence based on business requirements**
- Daily batch: Nightly recommendation refresh for morning users
- Hourly batch: Stock predictions updating each trading hour
- Weekly batch: Monthly subscription churn predictions
- Event-triggered: Batch after data warehouse ETL completion

### 2. Data Ingestion Setup
**Configure batch data pipeline from sources to ML system**
- Extract from data warehouse/data lake (BigQuery, Snowflake, S3)
- Apply feature transformations matching training pipeline
- Validate schema consistency with model expectations
- Handle missing values using same imputation as training

### 3. Distributed Processing Architecture
**Parallelize prediction computation across infrastructure**
- Use MapReduce/Spark for horizontal scaling across datasets
- Partition data by entity (user_id, product_id) for independent processing
- Configure batch size based on memory constraints (1K-100K records/batch)
- Implement checkpointing for fault tolerance on long-running jobs

### 4. Model Serving Configuration
**Deploy model in batch-optimized inference mode**
- Load model once per batch job (avoid reload overhead)
- Use batch prediction APIs (TensorFlow batch_predict, PyTorch batch inference)
- Enable GPU batching for deep learning models (32-512 samples/batch)
- Leverage model compilation (TensorRT, ONNX) for throughput optimization

### 5. Prediction Storage Design
**Store pre-computed predictions for fast lookup**
- Key-value store for individual lookups (Redis, DynamoDB: user_id → prediction)
- Columnar storage for analytics (Parquet, BigQuery: all predictions for analysis)
- Include metadata (model_version, prediction_timestamp, confidence_score)
- Set TTL based on batch frequency (1.5x batch interval for overlap)

### 6. Keyed Predictions Pattern
**Enable distributed batch prediction with result matching**
- Attach unique keys to input records (primary keys, composite keys)
- Preserve keys through prediction pipeline (input → features → predictions)
- Join predictions back to original entities using keys
- Handle missing predictions (timeouts, errors) with fallback logic

### 7. Monitoring & Alerting
**Track batch job health and prediction quality**
- Job completion metrics (duration, throughput, failure rate)
- Data quality checks (null rate, distribution shifts, schema violations)
- Model performance monitoring (prediction distribution, confidence intervals)
- Alerting on batch failures or stale predictions (SLA breaches)

## Practical Application

### E-commerce Recommendation System
**Problem**: Generate personalized product recommendations for 10M users
**Batch Solution**:
1. Nightly job extracts user behavior (purchases, views, clicks) from data warehouse
2. Spark cluster processes 10M users in parallel (10K users/partition × 1K partitions)
3. Recommendation model generates top-100 products per user (batch size: 256 users)
4. Predictions stored in Redis with 36-hour TTL (user_id → [product_ids + scores])
5. Web app reads pre-computed recommendations in <5ms (vs. 200ms real-time inference)

### Credit Card Fraud Detection (Batch Component)
**Problem**: Update fraud risk scores for all accounts daily
**Batch Solution**:
1. Daily batch (3am) processes all 50M accounts using last 30 days transactions
2. Feature engineering pipeline computes aggregates (transaction velocity, geography patterns)
3. XGBoost model scores all accounts (1M accounts/minute on 100-node cluster)
4. Risk scores stored in Aurora DB (account_id, risk_score, score_date)
5. Real-time transactions query batch scores + apply real-time rules for final decision

## Edge Cases & Nuances

**Cold Start Problem**: New users/items without predictions
- Fallback to popularity-based or demographic-based defaults
- Trigger on-demand prediction for high-value new entities
- Include new entities in next batch cycle with minimal features

**Prediction Staleness**: Batch predictions lag reality
- Hybrid approach: batch for stable predictions + real-time updates for high-velocity features
- Monitor staleness impact on business metrics (click-through rate decay over time)
- Decrease batch interval if staleness hurts performance (daily → hourly)

**Batch Job Failures**: Incomplete or failed batch runs
- Implement idempotent batch jobs (can safely re-run without duplicates)
- Use transactional writes to prediction store (all-or-nothing semantics)
- Maintain previous batch predictions as fallback until new batch succeeds

**Cost vs. Freshness Tradeoff**: More frequent batches = higher cost
- Profile actual prediction change rate (how often do top-10 recommendations shift?)
- A/B test batch frequencies to measure impact on engagement metrics
- Use event-triggered batches for critical updates (product catalog changes)

## Anti-Patterns

**Batch for Latency-Critical Applications**: Using batch for fraud detection that must block transactions in real-time
**Over-Engineering Batch Infrastructure**: Building distributed system for 10K records processable on single machine
**Ignoring Data Freshness Requirements**: Daily batches for inventory predictions when stock changes hourly
**No Fallback Strategy**: System breaks when batch job fails with no stale predictions

## Trade-offs

**Batch vs. Online Inference**:
- Batch: Lower cost (bulk processing), higher latency (stale predictions), simpler ops (scheduled jobs)
- Online: Higher cost (per-request compute), lower latency (fresh predictions), complex ops (SLA-driven)

**Batch Frequency**:
- More frequent (hourly): Fresher predictions, higher compute cost, more operational complexity
- Less frequent (daily): Stale predictions, lower cost, simpler ops, higher storage requirements

**Distributed vs. Single-Node**:
- Distributed: Scales to billions of records, complex infrastructure, slower for small datasets
- Single-node: Simple, fast for <10M records, memory/compute constraints, no fault tolerance

## Related Frameworks
- **Streaming ML Pattern**: Continuous prediction updates from streaming data (complements batch)
- **Online Learning Pattern**: Incremental model updates as new data arrives (batch retraining alternative)
- **Lambda Architecture**: Batch layer + speed layer for hybrid batch/streaming systems
- **Feature Store Pattern**: Centralized feature computation for batch and online consistency

## Practitioner Sources
- **Google ML Design Patterns** (Lakshmanan et al.): Batch Serving pattern (#17), Keyed Predictions pattern
- **ML System Design**: Batch vs. online prediction serving tradeoffs, architecture patterns
- **Apache Spark MLlib**: Distributed batch prediction at scale, best practices
- **AWS SageMaker Batch Transform**: Managed batch inference service, cost optimization
