---
name: streaming-inference
description: Process unbounded data streams with sub-100ms predictions when real-time ML inference is required
---

# Streaming Inference Pattern

## What It Is
A real-time machine learning architecture where models continuously process unbounded data streams, generating predictions with low latency (typically <100ms) as events arrive. The system ingests events from message queues or stream processors, applies feature transformation and model inference in-flight, and emits predictions to downstream consumers - all without persisting the raw event data. This pattern prioritizes low latency and high throughput for event-driven applications.

## When to Use It
- Predictions must be generated within milliseconds of event arrival
- Processing continuous streams of data (clickstreams, IoT sensors, transaction logs)
- Real-time personalization or content ranking required
- Fraud detection or anomaly detection on live transactions
- Monitoring systems that trigger alerts based on ML predictions
- Systems where data volume makes batch processing infeasible (millions of events per second)

## Execution Steps

### 1. Design Stream Processing Architecture
Define how events flow from source to prediction to action. Stream architecture determines latency characteristics and failure modes.

**Action**: Choose message broker: Kafka (high throughput, durability), Kinesis (AWS-native, auto-scaling), Pub/Sub (GCP-native, exactly-once), or Pulsar (multi-tenancy). Design data flow: Source → Stream → Feature Computation → Model Inference → Prediction Stream → Consumer. Define partitioning strategy: partition by user_id for stateful processing, random for stateless. Document: "Events from {source} via {broker} with {partitions} partitions processing {events/sec} with {latency_target} latency."

### 2. Implement Real-Time Feature Engineering
Transform raw events into model-ready features with minimal latency. Feature computation must be stateless or maintain minimal state for fast processing.

**Action**: Identify stateless features (computed from single event: log transformations, categorization). Implement stateful features using windowed aggregations (last 5 minutes average, count in last hour). Use feature store for pre-computed features (user demographics, historical statistics). Cache frequently accessed features in Redis/Memcached. Measure feature computation latency separately to identify bottlenecks.

### 3. Deploy Model for Low-Latency Inference
Optimize model serving for sub-100ms prediction latency. Model size and complexity directly impact latency.

**Action**: Choose deployment: Model server (TensorFlow Serving, TorchServe, Triton) for complex models, In-process inference (load model in stream processor) for simple models (<100MB), ONNX Runtime for cross-framework optimization. Implement batching: micro-batching (collect 10-100 events, infer in batch) if latency allows. Use GPU for deep learning models processing >1K events/sec. Profile inference: measure p50, p95, p99 latency under load.

### 4. Handle Backpressure and Flow Control
Prevent system overload when event rate exceeds processing capacity. Backpressure mechanisms protect downstream services.

**Action**: Implement rate limiting: max events per second per partition. Configure buffer sizes: balance between memory usage and absorbing spikes. Set up consumer lag monitoring: alert when lag exceeds threshold. Design overflow behavior: drop events (acceptable for some use cases), sample events (process every Nth), or scale out processing. Implement graceful degradation: use cached predictions when system overloaded.

### 5. Ensure Exactly-Once Semantics
Prevent duplicate predictions or missed events in face of failures. Streaming systems must handle broker restarts, network partitions, and process crashes.

**Action**: Choose consistency guarantee: At-most-once (fast but can lose data), At-least-once (duplicates possible, need deduplication), Exactly-once (slowest but no duplicates). Implement idempotent prediction writes: use unique event IDs to deduplicate. Checkpoint processing offsets: commit offset only after prediction successfully emitted. Design retry logic: transient errors retry with exponential backoff, permanent errors send to dead-letter queue.

### 6. Monitor Streaming Pipeline Health
Track end-to-end latency, throughput, and error rates in real-time. Streaming systems fail in complex ways requiring comprehensive observability.

**Action**: Instrument metrics: events ingested/sec, predictions emitted/sec, processing latency (p50/p95/p99), consumer lag, error rate. Set up alerts: latency exceeds SLA, consumer lag growing, error rate spike, throughput dropped. Implement distributed tracing: correlate events across stream processors, feature stores, model servers. Create dashboards: visualize pipeline health, identify bottlenecks, capacity planning.

## Real-World Applications

**Fraud Detection and Risk**
- Credit card companies detect fraudulent transactions within milliseconds of swipe
- Payment processors (Stripe, PayPal) score transaction risk in real-time before authorization
- E-commerce platforms identify account takeovers as suspicious login events occur

**Content Personalization**
- TikTok/Instagram adjust feed ranking based on every like, skip, and watch duration in real-time
- Spotify updates "Daily Mix" recommendations as listening patterns change throughout the day
- News sites personalize article feeds based on real-time clickstream analysis

**Monitoring and Alerting**
- DataDog/New Relic detect anomalies in infrastructure metrics (CPU spikes, error rates)
- Security systems identify intrusion attempts from log streams (SIEM platforms)
- Healthcare monitors predict patient deterioration from continuous vital sign streams

**Real-Time Bidding and Advertising**
- Ad exchanges score ad relevance and bid in <10ms during programmatic auctions
- Marketing platforms adjust campaign budgets based on real-time conversion signals
- Recommendation engines personalize product suggestions as user browses e-commerce site

**IoT and Edge Computing**
- Manufacturing systems predict equipment failure from sensor data streams
- Autonomous vehicles process camera/lidar streams for object detection
- Smart home devices classify audio events (glass breaking, smoke alarm) locally

## Anti-Patterns

**Processing streams in batch-style loops** → High latency and resource waste; use stream processing frameworks (Flink, Spark Streaming) optimized for continuous processing.

**Loading model on every prediction** → Extreme latency; load model once at startup and keep in memory.

**No backpressure handling** → System crashes under load; implement rate limiting and graceful degradation.

**Stateful operations without checkpointing** → Lost state on failures; use distributed state management (RocksDB, Redis).

**Synchronous blocking calls in stream pipeline** → Pipeline stalls waiting for external services; use async I/O or cache aggressively.

**Insufficient partitioning** → Single partition becomes bottleneck; partition data to enable horizontal scaling.

## Success Metrics
- End-to-end latency meets SLA (e.g., p95 < 100ms from event arrival to prediction)
- Throughput handles peak load (e.g., 100K events/sec with headroom)
- Consumer lag stays near zero (<1 minute even during spikes)
- Prediction accuracy matches offline evaluation (no train-serve skew)
- Uptime exceeds target (e.g., 99.9% availability)
- Cost per prediction acceptable (inference cost + infrastructure cost per 1M predictions)

## Related Frameworks
- **Batch Serving Pattern**: High-throughput alternative when latency tolerance allows
- **Online Learning Pattern**: Continuous model updates from streaming data
- **Feature Store Pattern**: Pre-compute and serve features for low-latency inference
- **Lambda Architecture**: Combining batch and streaming for comprehensive analytics

## Common Pitfalls
- Underestimating latency budget for feature computation (often dominates inference time)
- Not testing under realistic load leading to production performance surprises
- Ignoring network latency between stream processor and model server
- Complex feature engineering that works offline but too slow for real-time
- No capacity planning for traffic spikes (Black Friday, breaking news)
- Lack of feature parity between training and serving causing model degradation
- Insufficient monitoring making incident response difficult

## Tools & Resources
- **Stream Processing**: Apache Flink, Kafka Streams, Spark Structured Streaming, AWS Kinesis Analytics
- **Message Brokers**: Apache Kafka, AWS Kinesis, Google Cloud Pub/Sub, Apache Pulsar
- **Model Serving**: TensorFlow Serving, TorchServe, NVIDIA Triton, Seldon Core, KServe
- **Feature Stores**: Feast, Tecton, AWS SageMaker Feature Store, Databricks Feature Store
- **Monitoring**: Prometheus + Grafana, Datadog, New Relic, custom metrics in CloudWatch
- **References**: "Streaming Systems" (Akidau et al.), Kafka streams documentation, Flink ML tutorials

## Latency Budget Breakdown

**Target: <100ms end-to-end latency**

Typical allocation:
- Message broker ingestion: 5-10ms
- Feature computation: 20-40ms (often the bottleneck)
- Model inference: 10-30ms
- Prediction write/emit: 5-10ms
- Network overhead: 10-20ms
- Buffer: 10-20ms

**Optimization priorities:**
1. Feature caching (avoid expensive DB lookups)
2. Model optimization (quantization, pruning, ONNX)
3. Micro-batching (amortize overhead across events)
4. Vertical scaling (faster CPUs/GPUs)
5. Horizontal scaling (more partitions/workers)

---
*Framework Type*: ML System Design Pattern
*Domain*: Machine Learning Operations, Real-Time Systems
*Practitioner Score*: 9/10 - Critical for user-facing ML applications requiring low latency
*Complexity*: High - Requires distributed systems expertise, stream processing, performance optimization
*Prerequisites*: Stream processing fundamentals, model serving, distributed systems, performance profiling
