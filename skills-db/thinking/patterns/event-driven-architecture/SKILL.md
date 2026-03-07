---
name: event-driven-architecture
description: Design systems that react to state changes through asynchronous events, enabling loose coupling and scalability
---

# Event-Driven Architecture

## Overview

Event-Driven Architecture (EDA) is an architectural pattern where system components communicate by producing and consuming events representing state changes. An event is an immutable fact about something that happened (e.g., "OrderPlaced", "PaymentReceived"), and components react to these events asynchronously rather than through direct, synchronous calls.

EDA enables loose coupling between services - producers don't know who consumes their events, and consumers don't need to know event sources. This decoupling makes systems more scalable, resilient, and easier to evolve. Common implementations use message brokers (Kafka, RabbitMQ, AWS EventBridge) to handle event routing, persistence, and delivery guarantees.

The pattern gained prominence with microservices architectures where synchronous HTTP calls create tight coupling and cascading failures. Modern EDA implementations combine patterns like event sourcing, CQRS, sagas, and the outbox pattern to build distributed systems that can handle millions of events per second while maintaining reliability.

## When to Use

- Building microservices that need to communicate without tight coupling
- Systems requiring high scalability and ability to add new consumers without modifying producers
- Real-time data processing pipelines (IoT, analytics, monitoring)
- Workflows requiring asynchronous processing (order fulfillment, payment processing)
- Systems needing event replay, audit trails, or time-travel debugging
- Integrating disparate systems that shouldn't directly depend on each other
- Replacing polling-based architectures with reactive push-based models

## The Process

### Step 1: Identify Events and Bounded Contexts

Map domain state changes to events using past-tense naming conventions. Define clear event schemas with versioning strategy.

**Ask:** "What significant state changes occur in this domain? Who needs to know about them?"

**Output:** Event catalog with schemas (e.g., `OrderPlaced`, `PaymentProcessed`, `InventoryReserved`). Use JSON Schema or Protocol Buffers for contracts.

**Pattern:** Event names should be past-tense facts, not commands. `OrderPlaced` not `PlaceOrder`.

### Step 2: Choose Event Delivery Guarantees

Select delivery semantics based on business requirements: at-most-once (fire-and-forget), at-least-once (retries, possible duplicates), or exactly-once (transactional, expensive).

**Ask:** "Can we tolerate duplicate events? Can we tolerate lost events? What's the cost of processing an event twice?"

**Implementation:** Most systems use at-least-once with idempotent consumers (check `event_id` before processing). Exactly-once requires distributed transactions or outbox pattern.

**Trade-off:** At-least-once balances reliability and performance - exactly-once adds latency and complexity.

### Step 3: Implement Event Producers with Outbox Pattern

Avoid dual-write problem where database update succeeds but event publish fails. Write events to database table in same transaction, then async process publishes to broker.

**Ask:** "How do we guarantee event publishing when database transaction commits?"

**Implementation:**
1. Update application state in database
2. Insert event to `outbox` table in same transaction
3. Background process polls outbox and publishes to event broker
4. Mark events as published

**Pattern:** Solves atomicity problem - event only published if database commit succeeds.

### Step 4: Design Event Consumers with Idempotency

Build consumers that produce same result when processing duplicate events. Store processed `event_id` to detect duplicates.

**Ask:** "What happens if this consumer processes the same event twice?"

**Implementation:** Check `processed_events` table for `event_id` before processing. Use database constraints to enforce uniqueness.

**Anti-pattern:** Assuming exactly-once delivery without building defensive consumers.

### Step 5: Handle Distributed Transactions with Sagas

For workflows spanning multiple services, use saga pattern - sequence of local transactions with compensating actions for rollback.

**Ask:** "How do we maintain consistency across services without distributed transactions?"

**Types:** Choreography (services react to events autonomously) or Orchestration (central coordinator manages workflow).

**Example:** Order saga: Reserve inventory → Charge payment → Ship order. If payment fails, compensating event releases inventory reservation.

### Step 6: Implement Dead Letter Queues and Error Handling

Route failed events to dead letter queue (DLQ) after retry attempts exhausted. Monitor DLQ for systematic failures.

**Ask:** "What happens when an event consumer repeatedly fails?"

**Implementation:** Configure retry policy (exponential backoff, max attempts), route to DLQ, alert on DLQ depth threshold. Manual intervention or automated replay after fix.

**Pattern:** Separate transient errors (network) from permanent errors (schema mismatch) - different retry strategies.

### Step 7: Enable Observability and Event Tracing

Implement distributed tracing across event flows using correlation IDs. Log event production, consumption, and processing outcomes.

**Ask:** "How do we debug a failed workflow spanning 10 services?"

**Tools:** OpenTelemetry for tracing, structured logging with `correlation_id`, metrics for event lag and consumer throughput.

**Metric:** Consumer lag (events produced vs consumed) indicates bottlenecks.

## Example Application

**Situation:** E-commerce platform with tightly-coupled monolith causing deployment bottlenecks and cascading failures.

**Migration to EDA:**
- Identified 15 core events (`OrderPlaced`, `PaymentProcessed`, `InventoryUpdated`, `ShipmentDispatched`)
- Implemented Kafka with 3 partitions per topic for parallel processing
- Used outbox pattern in Order Service - events published only after database commit
- Built idempotent consumers - Email Service checks `sent_emails` table before sending
- Implemented choreography saga for order fulfillment - each service reacts to events and publishes next state
- Configured DLQ with 3 retry attempts and exponential backoff
- Added distributed tracing with correlation IDs for debugging

**Outcome:** Services independently deployable (deployment frequency 2x/day → 20x/day). Failures isolated (payment service down doesn't break inventory). New feature (fraud detection) added by consuming existing events - zero changes to producers. System handles 10x traffic spikes without degradation.

## Anti-Patterns

- Tight coupling through event chains where Consumer A requires event from Consumer B (use orchestration instead)
- Event schemas with breaking changes without versioning strategy
- Synchronous request-response disguised as events (use RPC/REST instead)
- Events containing full entity state instead of deltas (bloated payloads, hard to reason about)
- No DLQ or monitoring - failed events disappear silently
- Assuming event ordering across partitions without partition keys
- Over-engineering simple CRUD apps with EDA (use when complexity justified)

## Related

- cqrs (command-query separation complements EDA)
- event-sourcing (events as source of truth)
- saga-pattern (distributed transactions in EDA)
- microservices-architecture (common EDA use case)
- outbox-pattern (reliable event publishing)
- domain-driven-design (bounded contexts inform event design)
