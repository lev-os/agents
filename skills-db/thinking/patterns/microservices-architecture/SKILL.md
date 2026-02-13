---
name: microservices-architecture
description: Design distributed systems as a collection of loosely coupled, independently deployable services organized around business capabilities
---

# Microservices Architecture

## Overview

Microservices architecture structures an application as a collection of loosely coupled, independently deployable services, each running in its own process and communicating via lightweight mechanisms. Popularized by practitioners at Netflix, Amazon, and Spotify in the 2010s, and codified by Sam Newman in "Building Microservices" (2015), this architectural style enables organizations to scale development teams, deploy independently, and adopt diverse technology stacks per service.

Each microservice is organized around a business capability (not technical function), owns its data, and can be developed, deployed, and scaled independently. This contrasts with monolithic architectures where all functionality lives in a single deployable unit. Martin Fowler and James Lewis formally defined the pattern in 2014, emphasizing smart endpoints and dumb pipes.

## When to Use

- Organization has grown beyond what a single team can effectively develop and deploy
- Different parts of the system have different scaling requirements
- System requires high availability and fault isolation
- Teams need to deploy independently without coordinating releases
- Different services benefit from different technology choices
- Business requires rapid iteration on specific capabilities
- System must evolve incrementally from a monolith (strangler pattern)

## When NOT to Use

- Small team (fewer than 5-8 developers) - operational overhead exceeds benefits
- Simple domain that doesn't justify distribution complexity
- Strong data consistency requirements across the entire system
- Greenfield project without clear domain understanding (start monolith, extract later)
- Organization lacks DevOps maturity for distributed operations

## The Process

### Step 1: Decompose by Business Capability

Identify services by business capabilities, not technical layers. Each service represents a bounded context from Domain-Driven Design.

**Ask:** "What are the distinct business capabilities? What would each team own end-to-end?"

**Example decomposition for e-commerce:**
- `orders-service` - Order lifecycle, not "order database"
- `inventory-service` - Stock management, availability
- `payments-service` - Payment processing, refunds
- `notifications-service` - Email, SMS, push notifications
- `catalog-service` - Product information, search

**Anti-pattern:** Decomposing by technical layer (`api-service`, `database-service`, `frontend-service`) - creates distributed monolith.

### Step 2: Define Service Boundaries and APIs

Each service exposes well-defined APIs and owns its data. Services communicate through APIs, never by accessing each other's databases directly.

**Design principles:**
- API-first design - define contracts before implementation
- Backward compatibility - never break existing consumers
- Versioning strategy - URI versioning (`/v1/orders`) or header-based
- Contract testing - verify API compatibility between services

**Database per service:** Each service owns its datastore. `orders-service` has orders database, `inventory-service` has inventory database. No shared databases.

### Step 3: Choose Communication Patterns

Select synchronous or asynchronous communication based on requirements.

**Synchronous (REST/gRPC):**
- Use for: Queries requiring immediate response, simple request-response
- Pattern: API Gateway routes requests, services call each other directly
- Risk: Cascading failures, latency accumulation

**Asynchronous (Event-driven):**
- Use for: Commands that don't need immediate response, eventual consistency acceptable
- Pattern: Services publish events to message broker (Kafka, RabbitMQ), consumers react
- Benefit: Decoupling, resilience, natural audit trail

**Example:** Order placed -> `OrderPlacedEvent` published -> `inventory-service` reserves stock, `payments-service` initiates charge, `notifications-service` sends confirmation. Services don't know about each other.

### Step 4: Implement Resilience Patterns

Distributed systems fail partially. Design for failure with these patterns.

**Circuit Breaker:** Stop calling failing service, fail fast, allow recovery. When `payments-service` is down, circuit opens after threshold failures, returns fallback response.

**Timeout:** Never wait forever. Set timeouts on all inter-service calls.

**Retry with backoff:** Retry transient failures with exponential backoff. Jitter prevents thundering herd.

**Bulkhead:** Isolate failures. Separate thread pools for different dependencies so one slow service doesn't exhaust all threads.

**Fallback:** Degrade gracefully. If recommendations service fails, show popular items instead of error.

### Step 5: Handle Data Consistency

Microservices sacrifice strong consistency for availability and partition tolerance (CAP theorem). Use eventual consistency patterns.

**Saga pattern:** Coordinate multi-service transactions as sequence of local transactions with compensating actions.
- Order saga: Create order -> Reserve inventory -> Charge payment -> Ship
- If payment fails: Compensate by releasing inventory reservation

**Event sourcing:** Store state as sequence of events. Enables temporal queries, audit, replay.

**CQRS:** Separate read and write models. Optimize queries without affecting command processing.

### Step 6: Establish Observability

Distributed systems require comprehensive observability to debug and operate.

**Three pillars:**
1. **Logging:** Structured logs with correlation IDs. Aggregate centrally (ELK, Splunk)
2. **Metrics:** Service health, latency percentiles, error rates (Prometheus, Datadog)
3. **Distributed tracing:** Follow requests across services (Jaeger, Zipkin)

**Correlation ID:** Generate unique ID at edge, propagate through all services. Essential for debugging distributed transactions.

### Step 7: Deployment and Operations

Each service deploys independently with its own CI/CD pipeline.

**Containerization:** Package services as containers (Docker) for consistent deployment.

**Orchestration:** Kubernetes for container orchestration - service discovery, scaling, self-healing.

**Service mesh:** Sidecar proxy (Istio, Linkerd) handles cross-cutting concerns - mTLS, observability, traffic management.

**Feature flags:** Deploy code without enabling features. Decouple deployment from release.

## Example Application

**Situation:** Monolithic e-commerce platform struggling with deployment coordination, scaling bottlenecks, and team friction.

**Microservices Migration:**
1. **Strangler pattern:** New features built as services, gradually extracting from monolith
2. **Service decomposition:** Identified 7 bounded contexts -> 7 services
3. **API Gateway:** Kong routes requests, handles auth, rate limiting
4. **Event-driven:** Kafka for order events, enabling loose coupling
5. **Resilience:** Hystrix circuit breakers, timeouts, bulkheads
6. **Observability:** Distributed tracing with Jaeger, metrics with Prometheus
7. **Deployment:** Each service has own pipeline, deploys to Kubernetes

**Outcome:** Teams deploy independently (10x/day vs 1x/week), `catalog-service` scales separately during traffic spikes, `payments-service` uses different tech stack optimized for its needs, failures isolated.

## Anti-Patterns

- Distributed monolith - services tightly coupled, must deploy together
- Shared database - defeats independent deployment and data ownership
- Synchronous chains - long call chains create latency and fragility
- No API versioning - breaking changes cascade across services
- Insufficient observability - impossible to debug production issues
- Too many services too soon - operational overhead kills small teams
- Not investing in automation - manual deploys don't scale
- Ignoring organizational change - microservices require DevOps culture

## Related

- domain-driven-design (bounded contexts inform service boundaries)
- event-driven-architecture (asynchronous communication pattern)
- api-design (service interface design)
- circuit-breaker-pattern (resilience pattern detail)
- saga-pattern (distributed transaction handling)
- twelve-factor-app (service design principles)
