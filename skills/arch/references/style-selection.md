# Architecture Style Selection Reference

Decision frameworks for selecting architecture styles, API contracts, and fitness functions.

## Architecture Style Matrix

| Style | Best For | Team Size | Scalability | Complexity | Deployment |
|-------|----------|-----------|-------------|------------|------------|
| **Monolith** | Small teams, early stage, well-understood domain | 1-10 | Vertical | Low | Simple |
| **Modular Monolith** | Growing teams, domain boundaries emerging | 5-25 | Vertical + some horizontal | Medium | Simple |
| **Microservices** | Large orgs, independent team scaling, polyglot | 25+ | Horizontal per service | High | Complex |
| **Event-Driven** | Async workflows, decoupled integrations, CQRS | 10+ | Horizontal | High | Medium |
| **Serverless** | Variable load, event processing, cost optimization | Any | Auto | Medium | Managed |
| **Layered** | CRUD apps, clear separation of concerns | 1-15 | Vertical | Low | Simple |

## 5-Question Decision Heuristic

Answer sequentially; first "yes" suggests the style:

### Q1: Do you need independent deployment of components by different teams?
- YES -> Consider **Microservices** or **Modular Monolith**
- NO -> Continue

### Q2: Is your load highly variable or event-driven?
- YES -> Consider **Serverless** or **Event-Driven**
- NO -> Continue

### Q3: Do you have clear domain boundaries that rarely change?
- YES -> Consider **Modular Monolith**
- NO -> Continue

### Q4: Is your team small (<10) with shared codebase ownership?
- YES -> Consider **Monolith** or **Layered**
- NO -> Continue

### Q5: Do you need to integrate many external systems asynchronously?
- YES -> Consider **Event-Driven**
- NO -> Start with **Monolith**, extract as needed

## Style Deep Dives

### Monolith

**When to use:**
- Startup/MVP phase
- Small team with shared ownership
- Well-understood, stable domain
- Simple deployment requirements

**When to avoid:**
- Need for independent scaling of components
- Multiple teams need autonomous deployment
- Polyglot requirements

**Evolution path:** Monolith -> Modular Monolith -> Extract hot services

### Modular Monolith

**When to use:**
- Domain boundaries are clear but team is not ready for distributed systems
- Want microservices benefits without operational complexity
- Preparing for potential future extraction

**Structure:**
```
/src
  /modules
    /orders      (own DB schema, internal API)
    /inventory   (own DB schema, internal API)
    /users       (own DB schema, internal API)
  /shared        (cross-cutting concerns only)
```

**Rules:**
- Modules communicate via defined interfaces only
- No direct database access across modules
- Shared kernel kept minimal

### Microservices

**When to use:**
- Multiple teams need independent deployment
- Different components have vastly different scaling needs
- Polyglot persistence/technology requirements
- Organization is mature in DevOps practices

**Prerequisites (don't start without):**
- [ ] Automated CI/CD pipelines
- [ ] Container orchestration (K8s or equivalent)
- [ ] Centralized logging and tracing
- [ ] Service discovery mechanism
- [ ] API gateway
- [ ] Team per service (or small set of services)

**Decomposition strategies:**
1. By business capability (Orders, Payments, Shipping)
2. By subdomain (DDD bounded contexts)
3. By data ownership (who owns this entity?)

### Event-Driven

**When to use:**
- Loose coupling between components
- Async processing acceptable
- Need to react to state changes across systems
- CQRS/event sourcing beneficial

**Patterns:**
- **Event notification**: Fire and forget
- **Event-carried state transfer**: Event contains all needed data
- **Event sourcing**: Events are source of truth
- **CQRS**: Separate read/write models

**Pitfalls:**
- Eventual consistency complexity
- Event schema evolution
- Debugging distributed flows
- Exactly-once processing challenges

### Serverless

**When to use:**
- Highly variable load (including zero)
- Event-driven processing
- Cost optimization (pay per invocation)
- Rapid development, managed infrastructure

**Constraints:**
- Cold start latency (100ms-1s)
- Execution time limits (15 min typical max)
- Stateless by design
- Vendor lock-in risk

**Good fit:** API backends, event processing, scheduled jobs, webhooks
**Poor fit:** Long-running processes, stateful workloads, low-latency requirements

## API Contract Selection

| Protocol | Best For | Latency | Coupling | Tooling |
|----------|----------|---------|----------|---------|
| **REST** | Public APIs, CRUD, web/mobile clients | Medium | Low | Excellent |
| **GraphQL** | Complex client data needs, mobile optimization | Medium | Medium | Good |
| **gRPC** | Service-to-service, high throughput, streaming | Low | High | Good |
| **Event/Async** | Decoupled integration, workflows | Variable | Very Low | Medium |
| **WebSocket** | Real-time bidirectional, live updates | Very Low | Medium | Medium |

### Selection Questions

1. **Who is the consumer?**
   - External/public: REST or GraphQL
   - Internal services: gRPC or Events
   - Real-time UI: WebSocket

2. **What are latency requirements?**
   - <10ms: gRPC or WebSocket
   - <100ms: Any synchronous
   - Seconds acceptable: Events/async

3. **How complex is the data shape?**
   - Simple CRUD: REST
   - Complex, nested, variable: GraphQL
   - Structured, schema-enforced: gRPC

4. **Is eventual consistency acceptable?**
   - Yes: Events
   - No: Synchronous (REST, gRPC)

## Fitness Functions

Automated checks that verify architecture characteristics are maintained.

### Fitness Function Taxonomy

#### 1. Dependency Fitness Functions

Verify architectural boundaries and dependencies.

```
Function: no-circular-dependencies
Type: Static analysis
Trigger: CI pipeline
Tool: dependency-cruiser, ArchUnit, jdepend
Threshold: 0 cycles
```

```
Function: layer-violation-check
Type: Static analysis
Trigger: CI pipeline
Rule: Controllers cannot import Repositories directly
Threshold: 0 violations
```

```
Function: module-coupling
Type: Static analysis
Trigger: Weekly
Metric: Afferent/efferent coupling per module
Threshold: Ce < 10 per module
```

#### 2. Performance Fitness Functions

```
Function: api-latency-p95
Type: Runtime metric
Trigger: Continuous (alerting)
Threshold: <200ms for GET endpoints
Action: Alert if exceeded for >5 minutes
```

```
Function: database-query-time
Type: Runtime metric
Trigger: Continuous
Threshold: No query >100ms
Action: Log slow queries, alert if >10/minute
```

```
Function: load-test-baseline
Type: Synthetic test
Trigger: Pre-deployment
Tool: k6, Gatling
Threshold: Throughput within 10% of baseline
```

#### 3. Reliability Fitness Functions

```
Function: error-rate
Type: Runtime metric
Trigger: Continuous
Threshold: <0.1% 5xx errors
Action: Alert, auto-rollback if >1%
```

```
Function: chaos-test
Type: Synthetic test
Trigger: Weekly (staging)
Tool: Chaos Monkey, Gremlin
Scenario: Kill 1 instance, verify recovery <30s
```

```
Function: circuit-breaker-coverage
Type: Static analysis
Trigger: CI pipeline
Rule: All external calls wrapped in circuit breaker
Threshold: 100% coverage
```

#### 4. Security Fitness Functions

```
Function: dependency-vulnerabilities
Type: Static analysis
Trigger: CI pipeline, daily scan
Tool: Snyk, Dependabot, Trivy
Threshold: 0 critical/high vulnerabilities
```

```
Function: secret-detection
Type: Static analysis
Trigger: Pre-commit, CI
Tool: git-secrets, trufflehog
Threshold: 0 detected secrets
```

```
Function: authentication-coverage
Type: API test
Trigger: CI pipeline
Rule: All non-public endpoints return 401 without auth
Threshold: 100% coverage
```

#### 5. Deployability Fitness Functions

```
Function: deployment-time
Type: CI metric
Trigger: Every deployment
Threshold: <15 minutes from commit to production
```

```
Function: rollback-capability
Type: Synthetic test
Trigger: Monthly
Scenario: Execute rollback, verify <5 minutes
```

```
Function: database-migration-reversibility
Type: Static analysis
Trigger: CI pipeline
Rule: Every migration has corresponding rollback
Threshold: 100%
```

#### 6. Code Quality Fitness Functions

```
Function: test-coverage
Type: Static analysis
Trigger: CI pipeline
Threshold: >80% line coverage, >70% branch coverage
```

```
Function: code-complexity
Type: Static analysis
Trigger: CI pipeline
Tool: SonarQube, CodeClimate
Threshold: Cyclomatic complexity <10 per function
```

```
Function: documentation-coverage
Type: Static analysis
Trigger: CI pipeline
Rule: Public APIs have OpenAPI spec
Threshold: 100% endpoint coverage
```

#### 7. Operational Fitness Functions

```
Function: log-format-compliance
Type: Static analysis + runtime
Trigger: CI + continuous
Rule: All logs in structured JSON format
Threshold: 100% compliance
```

```
Function: trace-propagation
Type: Synthetic test
Trigger: CI pipeline
Scenario: Request through all services has consistent trace ID
Threshold: 100% propagation
```

```
Function: resource-utilization
Type: Runtime metric
Trigger: Continuous
Threshold: CPU <70%, Memory <80% sustained
Action: Alert, trigger autoscaling
```

### Implementing Fitness Functions

1. **Start with architectural drivers** - What quality attributes matter most?
2. **Automate in CI/CD** - Run on every change where possible
3. **Set actionable thresholds** - Clear pass/fail, not just metrics
4. **Evolve thresholds** - Tighten as system matures
5. **Balance coverage vs noise** - Don't create alert fatigue
