---
name: Batch Serving
description: Machine learning inference pattern where predictions are generated for large datasets at scheduled intervals rather than in real-time
---

# Batch Serving Pattern

## What It Is
A machine learning inference pattern where predictions are generated for large datasets at scheduled intervals rather than in response to individual real-time requests. The model processes accumulated data in bulk batches, writing results to storage for later consumption by downstream applications. This pattern decouples prediction generation from prediction consumption, optimizing for throughput over latency.

## When to Use It
- Predictions don't require immediate (sub-second) responses
- Processing millions of predictions daily (recommendation feeds, email campaigns, report generation)
- Compute costs matter more than latency (batch jobs run during off-peak hours)
- Input data naturally accumulates in batches (daily transactions, overnight data pipelines)
- High-throughput requirements where parallelization across many records is possible
- Predictions consumed by scheduled processes (daily dashboards, weekly reports, nightly ETL jobs)

## Execution Steps

### 1. Define Batch Cadence and Scope
Determine how frequently batches run and what data each batch processes. Cadence balances freshness requirements against computational efficiency.

**Action**: Answer: How fresh do predictions need to be? (Real-time, hourly, daily, weekly?) What triggers a batch? (Schedule, data threshold, manual trigger?) What's the input data source? (Database table, data warehouse, object storage?) Document: "Run batch {cadence} processing {data_volume} records from {source} writing to {destination}."

### 2. Design Data Partitioning Strategy
Split large datasets into processable chunks to enable parallel processing and failure recovery. Partitioning prevents memory overflow and allows retrying failed partitions without reprocessing everything.

**Action**: Choose partitioning scheme: Time-based (process records by date/hour), ID-based (partition by user_id ranges), Size-based (fixed chunks of N records), or Hybrid (time + size). Implement partition tracking to record which partitions completed successfully. Write partition metadata to enable idempotent retries.

### 3. Implement Batch Inference Pipeline
Build the ETL pipeline that loads data, applies the model, and writes predictions. Optimize for throughput using vectorization and parallelization.

**Action**: Load batch data efficiently (use columnar formats like Parquet, query only needed columns). Apply model inference using batch prediction APIs (model.predict(batch) not model.predict(record) in loop). Vectorize operations using NumPy/Pandas for 10-100x speedup. Write predictions with batch writes (bulk inserts, not row-by-row).

### 4. Configure Resource Allocation
Size compute resources for batch workload. Batch jobs typically use large instances for short durations rather than small instances continuously.

**Action**: Estimate memory needs: model_size + batch_size * record_size + overhead. Choose instance type: CPU for tree-based models, GPU for deep learning. Implement parallelization: multiple workers processing different partitions simultaneously. Monitor resource utilization to right-size instances (target 70-90% CPU/GPU usage).

### 5. Handle Failures and Monitoring
Build robustness for multi-hour batch jobs where transient failures are inevitable. Track progress to enable resumption and debugging.

**Action**: Implement checkpointing: save progress after each partition completes. Design retry logic: exponential backoff for transient errors, skip and log for data errors. Log metrics per batch: records processed, predictions generated, processing time, error count. Set up alerts: batch didn't complete within expected window, error rate exceeds threshold.

### 6. Optimize Prediction Storage and Access
Structure prediction output for efficient consumption by downstream systems. Consider storage format, indexing, and access patterns.

**Action**: Choose storage: Database (PostgreSQL, MySQL) for relational queries, Data warehouse (BigQuery, Redshift) for analytics, Object storage (S3, GCS) for large-scale dumps, Cache (Redis) for high-frequency access. Add indexes on query patterns (user_id, timestamp). Include metadata: prediction timestamp, model version, confidence scores. Implement retention policy: delete predictions older than N days.

## Real-World Applications

**Recommendation Systems**
- Netflix generates personalized video recommendations nightly for 200M+ users
- Spotify creates "Discover Weekly" playlists every Monday using batch inference
- Amazon pre-computes product recommendations for browsing pages

**Marketing and Communication**
- Email service providers score engagement probability for millions of recipients before campaign send
- Ad platforms pre-generate audience targeting scores overnight for next-day campaign optimization
- CRM systems batch-score lead quality for sales team prioritization

**Risk and Fraud**
- Credit card companies generate daily fraud risk scores for all active accounts
- Insurance providers batch-calculate claim fraud likelihood for overnight review queues
- Banks compute credit risk scores monthly for portfolio monitoring

**Business Intelligence**
- Retailers forecast demand for thousands of SKUs across hundreds of locations daily
- Healthcare systems predict patient readmission risk for care management programs
- Financial services generate customer churn predictions weekly for retention campaigns

## Anti-Patterns

**Using batch serving for time-sensitive decisions** → User experiences stale predictions; if decision impacts immediate user experience (fraud detection, search ranking), use real-time inference.

**Processing entire dataset when only subset changed** → Wastes compute on unchanged records; implement incremental processing to predict only new/updated records.

**No partition tolerance** → Single record failure kills entire batch; implement partition-level error handling to skip bad records without reprocessing millions.

**Ignoring model versioning** → Can't reproduce predictions or diagnose issues; always tag predictions with model version and timestamp.

**Writing predictions without indexes** → Downstream queries are slow; add indexes on access patterns before batch completes.

**Running batch during peak hours** → Competes with user-facing workloads for resources; schedule during off-peak windows (nights, weekends).

## Success Metrics
- Batch completes within scheduled window (e.g., 4-hour job finishes in 3 hours with buffer)
- Cost per prediction decreases vs real-time serving (typically 10-100x cheaper)
- Throughput meets business requirements (millions of predictions per hour)
- Error rate under threshold (<0.1% of predictions fail)
- Downstream systems consume predictions successfully (no data quality issues)
- Resource utilization efficient (70-90% CPU/GPU usage during processing)

## Related Frameworks
- **Streaming Inference Pattern**: Real-time alternative when low latency required
- **Online Learning Pattern**: Continuous model updates as new data arrives
- **Lambda Architecture**: Combining batch and streaming for comprehensive processing
- **Feature Store Pattern**: Managing feature computation for batch inference

## Common Pitfalls
- Not accounting for data growth leading to batch duration exceeding window
- Lack of idempotency causing duplicate predictions on retries
- Insufficient monitoring making debugging failures difficult
- No gradual rollout when deploying new model versions
- Overwriting previous predictions without audit trail
- Not partitioning large batches leading to memory issues
- Forgetting to version control prediction schemas causing breaking changes

## Tools & Resources
- **Batch Processing Frameworks**: Apache Spark, Dask, Ray for distributed processing
- **Workflow Orchestration**: Airflow, Prefect, Kubeflow for scheduling and monitoring
- **Model Serving**: TensorFlow Batch Prediction, PyTorch inference, Scikit-learn joblib
- **Storage Solutions**: PostgreSQL, BigQuery, Redshift, S3, Parquet files
- **Monitoring**: Datadog, Prometheus, CloudWatch for job observability
- **References**: "Machine Learning Design Patterns" (Lakshmanan et al.), Google's "Rules of Machine Learning", Databricks ML guides

## Batch vs Real-Time Decision Matrix

**Choose Batch Serving When:**
- Latency tolerance > 1 hour
- Processing millions of predictions per job
- Predictions consumed by scheduled processes
- Cost optimization is priority
- Input data arrives in natural batches

**Choose Real-Time Serving When:**
- Latency requirement < 100ms
- Predictions drive immediate user actions
- Request-response pattern required
- Input data arrives as individual events
- Freshness critical (fraud, content ranking)

**Hybrid Approach:**
Many production systems use both patterns - batch for base recommendations/scores, real-time for personalization adjustments.

---
*Framework Type*: ML System Design Pattern
*Domain*: Machine Learning Operations, System Design
*Practitioner Score*: 9/10 - Foundational pattern for production ML, used by all major platforms
*Complexity*: Medium - Requires understanding of distributed systems, ETL pipelines, model deployment
*Prerequisites*: ML model deployment basics, batch processing frameworks, data pipeline design
