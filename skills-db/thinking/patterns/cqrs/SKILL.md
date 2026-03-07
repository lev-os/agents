---
name: cqrs
description: Separate read and write operations into distinct models optimized for their specific purposes
---

# CQRS (Command Query Responsibility Segregation)

## Overview

CQRS is an architectural pattern that segregates operations that modify data (commands) from operations that read data (queries) into separate models. Instead of using the same entity model for both reads and writes, CQRS maintains distinct models optimized for each purpose - write models for consistency and business rules, read models for query performance and presentation.

The pattern originated from Bertrand Meyer's Command-Query Separation (CQS) principle and was popularized by Greg Young in the context of Domain-Driven Design and Event Sourcing. While CQS applies at the method level (methods either change state or return data, never both), CQRS scales this to the architectural level with physically separate models and potentially separate databases.

CQRS shines in complex domains where read and write patterns differ significantly - think dashboards with complex aggregations versus transactional writes with strict business rules. It enables independent scaling of read and write workloads, optimized data models for different access patterns, and eventual consistency trade-offs. However, CQRS adds substantial complexity and should be applied judiciously - most CRUD applications don't need it.

## When to Use

- Read and write workloads have vastly different scaling requirements (1000:1 read-to-write ratio)
- Complex business logic for writes but simple queries for reads (or vice versa)
- Multiple read representations of same data (API, analytics, search, UI)
- Collaborative domains where multiple users work on different aspects of same data
- Combining with Event Sourcing for audit trails and temporal queries
- Performance optimization where denormalized read models improve query speed
- Systems requiring strong write consistency but tolerating eventual read consistency

## The Process

### Step 1: Separate Command and Query Responsibilities

Define commands representing business operations (imperative) and queries representing data requests (interrogative). Commands modify state, queries return DTOs.

**Ask:** "Which operations change state versus retrieve data? Can these be cleanly separated?"

**Commands:** `PlaceOrder`, `CancelOrder`, `UpdateInventory` - return success/failure, no data.

**Queries:** `GetOrderDetails`, `FindOrdersByCustomer`, `GetInventoryReport` - return DTOs, no side effects.

**Principle:** Commands validate business rules and update write model. Queries read from optimized read model without touching write model.

### Step 2: Design Write Model for Consistency

Build normalized write model focused on enforcing business invariants and transactional consistency. Use domain entities with behavior, not anemic data structures.

**Ask:** "What are the consistency boundaries and business rules for each command?"

**Example:** `Order` aggregate validates inventory availability, applies pricing rules, enforces state transitions (Pending → Confirmed → Shipped). Write to normalized tables optimized for ACID transactions.

**Storage:** Typically RDBMS for transactional guarantees. Commands should represent business tasks, not CRUD operations.

### Step 3: Design Read Models for Query Optimization

Create denormalized read models optimized for specific query patterns. One write model can project to multiple read models.

**Ask:** "What are the most common query patterns? How can we pre-compute or denormalize for performance?"

**Example:** Order Dashboard read model combines order, customer, product, shipping data into single denormalized document. Pre-calculate totals, aggregations, and commonly filtered fields.

**Storage:** Can use different database (NoSQL, search engine, cache) optimized for read patterns. One read model per use case (API, reporting, search).

### Step 4: Implement Synchronization Mechanism

Sync write model changes to read models. Choose synchronous (immediate consistency) or asynchronous (eventual consistency) based on requirements.

**Synchronous:** Write model publishes events, read model handler updates in same transaction (complexity, tight coupling).

**Asynchronous:** Write model publishes to message queue/event stream, read model consumes and updates independently (eventual consistency, decoupled).

**Pattern:** Most implementations use asynchronous with event bus - write model publishes `OrderPlaced` event, read model handler updates denormalized view.

**Trade-off:** Synchronous = consistency, asynchronous = scalability. Most systems tolerate eventual consistency (milliseconds to seconds delay).

### Step 5: Handle Commands with Validation and Events

Process commands through command handlers that validate, execute business logic, and publish events.

**Flow:**
1. Command arrives (`PlaceOrderCommand`)
2. Handler loads aggregate from write model
3. Aggregate validates business rules
4. Aggregate processes command and generates events (`OrderPlaced`)
5. Events persisted and published to event bus
6. Return success/failure to client

**Idempotency:** Commands should be idempotent or use deduplication (`command_id` tracking).

### Step 6: Implement Query Handlers Against Read Models

Route queries to appropriate read model without touching write model. Return DTOs, not domain entities.

**Flow:**
1. Query arrives (`GetOrderDetailsByIdQuery`)
2. Handler executes optimized query against read model
3. Return DTO (`OrderDetailsDTO`)

**Anti-pattern:** Query handlers that navigate domain objects - defeats purpose of read model optimization.

### Step 7: Manage Eventual Consistency

Design UI and API responses acknowledging eventual consistency. Provide feedback when data may be stale.

**Techniques:**
- Return command result immediately, poll for updated read model
- Versioning - include version stamp, detect stale reads
- Command acceptance confirmation: "Order placed, processing..."
- WebSockets/polling to notify when read model updated

**User Experience:** "Your order is being processed" instead of immediately showing order in history.

## Example Application

**Situation:** SaaS analytics platform where users run complex reports but also create/update campaigns. Single database model causing query timeouts and write contention.

**CQRS Implementation:**
- **Write Model:** Normalized PostgreSQL with `Campaign`, `AdGroup`, `Keyword` aggregates enforcing budget constraints and bidding rules
- **Read Models:**
  - Analytics read model (Elasticsearch) - denormalized documents with pre-computed metrics, optimized for dashboard queries
  - Reporting read model (Redshift) - columnar storage for OLAP queries
  - Search read model (Elasticsearch) - optimized for keyword search with facets
- **Synchronization:** Write model publishes events (`CampaignCreated`, `BidUpdated`) to Kafka, read model consumers update their stores
- **Commands:** `CreateCampaign`, `UpdateBid`, `PauseCampaign` - validate against write model, return immediately
- **Queries:** `GetCampaignAnalytics`, `RunPerformanceReport`, `SearchKeywords` - execute against appropriate read model

**Outcome:** Report queries 100x faster (pre-computed aggregations). Write throughput 10x increase (no query contention). Independent scaling - 5 read replicas, 1 write database. New read model for mobile app added without changing write side.

## Anti-Patterns

- Applying CQRS to simple CRUD apps where read and write patterns are identical (over-engineering)
- Synchronous read model updates defeating scalability benefits
- Sharing entities between command and query sides (coupling)
- Not handling eventual consistency in UI - users see stale data without indication
- Creating separate read models for every query instead of grouping by access pattern
- Ignoring idempotency in command handlers - duplicate commands cause inconsistent state
- Using CQRS without understanding the complexity cost - adds operational overhead

## Related

- event-sourcing (natural fit with CQRS)
- event-driven-architecture (asynchronous synchronization)
- domain-driven-design (bounded contexts, aggregates inform CQRS boundaries)
- eventual-consistency (read model synchronization)
- materialized-views (database-level CQRS pattern)
- read-replicas (simple alternative before full CQRS)
