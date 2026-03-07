---
name: ml-streaming-inference
description: Streaming inference processes predictions on events as they arrive in real-time data streams with sub-second latency
---

# ML Streaming Inference Pattern

## Classification
- **Domain**: Computer Science, AI/ML
- **Category**: ML System Design Patterns
- **Novelty**: 7/10 (modern pattern for real-time systems)
- **Practitioner Evidence**: 10/10 (Kafka, Flink, production-validated)

## Mental Model
Streaming inference processes predictions on events as they arrive in real-time data streams, rather than batching or waiting for requests. Like a conveyor belt factory where each item gets inspected immediately as it passes, versus collecting items into boxes for later inspection. Data flows continuously through the model with sub-second latency.

## When to Use
- Real-time event processing (fraud detection, anomaly detection, IoT sensor monitoring)
- Predictions must happen on data in motion before storage (filter/route/enrich streams)
- Low-latency requirements (milliseconds to seconds) with high throughput (thousands/second)
- Continuous data streams from Kafka, Kinesis, Pub/Sub, or IoT sources
- Predictions inform downstream stream processing (feature engineering, alerting, routing)

## Core Framework

### 1. Streaming Architecture Selection
**Choose deployment pattern for model in stream processing pipeline**

**Option A: Embedded Model Pattern**
- Deploy model directly inside stream processor (Kafka Streams, Flink)
- Load model in-memory within application code (TensorFlow, PyTorch, ONNX)
- Process events using stream processing DSL with model calls
- Best for: Simple models, low latency requirements, tight coupling needs

**Option B: Model Server Pattern**
- Deploy dedicated model serving infrastructure (TensorFlow Serving, Seldon, KServe)
- Stream processor makes RPC calls to model server (HTTP/REST or gRPC)
- Model server handles versioning, A/B testing, scaling independently
- Best for: Complex models, shared across services, versioning needs

### 2. Stream Processor Setup
**Configure stream processing engine for real-time inference**

**Kafka Streams Approach**:
- Define topology: source topic → transform → model inference → sink topic
- Configure processing guarantees (at-least-once vs. exactly-once)
- Set parallelism (number of stream threads = topic partitions)
- Implement stateful processing if predictions need context (windowed aggregations)

**Apache Flink Approach**:
- Create DataStream from Kafka/Kinesis source
- Map/FlatMap functions call model for predictions
- Configure checkpointing for fault tolerance (every 60-300 seconds)
- Use AsyncIO for non-blocking model server calls (maintain throughput)

### 3. Model Loading & Initialization
**Optimize model deployment for streaming performance**
- Load model once during processor initialization (avoid per-event loading)
- Use model serialization formats optimized for inference (ONNX, TorchScript, SavedModel)
- Pre-warm model with dummy predictions (avoid cold-start latency on first event)
- Configure batch inference within streams (micro-batches of 10-100 events for throughput)

### 4. Feature Engineering in Streams
**Extract features from streaming events for model input**
- Parse event payload into feature vector (JSON → numerical/categorical features)
- Enrich events with lookup data (joins with reference tables, caches, feature stores)
- Apply stateful transformations (rolling windows, session aggregations, counters)
- Handle missing features with defaults/imputation matching training pipeline

### 5. Inference Execution
**Perform prediction on streaming events with low latency**
- For embedded models: Direct function call within stream processor
- For model servers: Async HTTP/gRPC request with timeout (100-500ms)
- Implement micro-batching: Accumulate 10-50 events, batch predict, distribute results
- Handle prediction failures with fallback logic (default scores, retry, dead letter queue)

### 6. Output & Downstream Integration
**Route predictions to consumers and storage**
- Publish predictions to output Kafka topic (prediction_id, features, score, timestamp)
- Trigger actions based on prediction thresholds (fraud alert if score > 0.9)
- Enrich original event with prediction (merge input + output streams)
- Sink to databases for serving (low-latency KV stores) or analytics (data warehouse)

### 7. Monitoring & Observability
**Track streaming inference performance and model health**
- Latency metrics: End-to-end latency (event arrival → prediction output), model inference time
- Throughput metrics: Events/second processed, predictions/second generated
- Model metrics: Prediction distribution, confidence scores, drift detection
- Error handling: Prediction failures, timeout rate, dead letter queue size

## Practical Application

### Real-Time Fraud Detection (Credit Card Transactions)
**Problem**: Detect fraudulent transactions within 100ms to block before authorization
**Streaming Solution**:
1. Transaction events stream into Kafka topic (card_id, amount, merchant, location, timestamp)
2. Flink job enriches with stateful features (transaction velocity last 5 min, merchant history)
3. XGBoost model embedded in Flink scores each transaction (fraud_score: 0-1)
4. High-risk transactions (score > 0.85) published to fraud_alerts topic → blocks authorization
5. All predictions logged to data warehouse for model monitoring and retraining
**Result**: 50ms p99 latency, 100K transactions/second throughput

### IoT Anomaly Detection (Manufacturing Sensors)
**Problem**: Detect machine failures from 10K sensor streams in real-time
**Streaming Solution**:
1. Sensor data streams from devices to AWS Kinesis (temperature, vibration, pressure every 1 second)
2. Kafka Streams aggregates 10-second windows per machine (mean, std, max, min)
3. Isolation Forest model (embedded ONNX) scores each window for anomaly (anomaly_score)
4. Anomalies (score > threshold) trigger alerts to maintenance team via SNS
5. Normal predictions stored in TimescaleDB for trend analysis
**Result**: 2-second end-to-end latency, early detection 30 minutes before failure

### Content Recommendation (Social Media Feed)
**Problem**: Score feed posts in real-time as users scroll
**Streaming Solution**:
1. User scroll events stream to Kafka (user_id, post_id, scroll_position, timestamp)
2. Kafka Streams calls TensorFlow Serving via gRPC (async) with user/post embeddings
3. Ranking model returns relevance scores for candidate posts
4. Top-scored posts returned to client within 200ms
5. User interactions (clicks, likes) feedback to training pipeline via Kafka

## Edge Cases & Nuances

**Backpressure & Rate Limiting**: Inference slower than event arrival rate
- Use micro-batching to increase throughput (trade small latency for higher QPS)
- Scale horizontally: Add stream processor instances (Kafka partitions, Flink parallelism)
- Implement load shedding: Drop low-priority events during overload (sample 10% of events)

**Model Update Without Downtime**: Deploying new model version
- Blue-green deployment: Run old + new versions, gradually shift traffic (canary release)
- For embedded models: Rolling restart stream processors with new model binary
- For model servers: Update server behind load balancer, test before full rollout

**Event Ordering & Exactly-Once Processing**: Preventing duplicate predictions
- Use Kafka exactly-once semantics (EOS) with transactional producers/consumers
- Implement idempotent predictions with deduplication keys (event_id tracking)
- Handle late-arriving events with watermarks (Flink) or grace periods

**Cold Start & Stateful Processing**: New stream processor instance initialization
- Restore state from checkpoints (Flink savepoints, Kafka changelog topics)
- Pre-populate caches/lookup tables before processing events (initialization phase)
- Use state TTL to prevent unbounded state growth (expire old entries after N hours)

## Anti-Patterns

**Synchronous Blocking Calls**: Calling slow external APIs synchronously in stream processing
**Stateless Processing of Temporal Patterns**: Ignoring event history when model needs context
**Over-Sized Models**: Running 10GB deep learning model with 500ms latency in millisecond-latency streams
**No Backpressure Handling**: Letting event queue grow unbounded during processing slowdowns

## Trade-offs

**Embedded Model vs. Model Server**:
- Embedded: Lower latency (no RPC), tighter coupling, harder to version/update, duplicated models
- Model Server: Higher latency (network call), loose coupling, easy versioning, centralized serving

**Micro-Batching vs. Per-Event Inference**:
- Micro-batching: Higher throughput (batch efficiency), slightly higher latency (accumulation delay)
- Per-event: Lower latency (immediate processing), lower throughput (overhead per event)

**At-Least-Once vs. Exactly-Once**:
- At-least-once: Simpler, higher throughput, possible duplicate predictions (idempotency needed)
- Exactly-once: Complex, lower throughput (coordination overhead), no duplicates

## Related Frameworks
- **Batch Processing Pattern**: Pre-compute predictions offline (complements streaming for hybrid systems)
- **Online Learning Pattern**: Update model continuously from streaming data (streaming training)
- **Lambda Architecture**: Batch layer + speed layer combining batch and streaming predictions
- **Kappa Architecture**: Pure streaming architecture (stream processing for all data)
- **Feature Store**: Consistent feature engineering for batch and streaming (avoid training/serving skew)

## Practitioner Sources
- **Kafka ML Systems** (Kai Waehner): Real-time inference with Kafka + Flink, architecture patterns
- **Google ML Design Patterns**: Streaming inference patterns, deployment strategies
- **Confluent ML Blog**: Machine learning in Kafka applications, best practices
- **Apache Flink ML**: Streaming ML pipelines, stateful inference, checkpointing strategies
- **TensorFlow Serving**: Model serving for production inference, gRPC APIs, versioning
