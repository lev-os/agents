# ATAM Evaluation Reference

Architecture Tradeoff Analysis Method - systematic approach for evaluating software architectures against quality attribute requirements.

## ATAM Phases

### Phase 0: Partnership and Preparation
- Identify stakeholders and their concerns
- Gather existing documentation
- Schedule evaluation sessions
- Duration: 1-2 weeks before evaluation

### Phase 1: Evaluation (Day 1)
1. **Present ATAM** - Explain method to stakeholders (30 min)
2. **Present Business Drivers** - Stakeholder presents context, goals, constraints (60 min)
3. **Present Architecture** - Architect presents current/proposed architecture (90 min)
4. **Identify Architectural Approaches** - Catalog styles, patterns, tactics (30 min)
5. **Generate Quality Attribute Utility Tree** - Build prioritized scenario tree (120 min)

### Phase 2: Evaluation (Day 2)
6. **Analyze Architectural Approaches** - Map scenarios to architecture decisions (180 min)
7. **Brainstorm and Prioritize Scenarios** - Stakeholder-generated scenarios (90 min)
8. **Analyze Architectural Approaches** (continued) - Analyze new scenarios (60 min)
9. **Present Results** - Findings, risks, tradeoffs (60 min)

### Phase 3: Follow-Up
- Produce written report
- Track risk mitigation
- Duration: 1 week after evaluation

## Building the Utility Tree

### Structure

```
Quality Attribute (root)
  |
  +-- Attribute Refinement (child)
       |
       +-- (Importance, Difficulty) Scenario (leaf)
```

### Example Utility Tree

```
Performance
  |
  +-- Latency
  |    +-- (H,M) User query returns results in <200ms at p95 under normal load
  |    +-- (H,H) User query returns results in <500ms at p99 during peak (10x normal)
  |
  +-- Throughput
       +-- (M,M) System processes 1000 transactions/second sustained
       +-- (H,H) System handles 10,000 concurrent WebSocket connections

Availability
  |
  +-- Uptime
  |    +-- (H,M) System maintains 99.9% uptime (8.76 hours downtime/year)
  |    +-- (M,H) System recovers from single node failure in <30 seconds
  |
  +-- Degradation
       +-- (H,M) System degrades gracefully under 2x expected load

Modifiability
  |
  +-- Feature Addition
  |    +-- (M,L) New payment provider added in <2 developer-days
  |    +-- (H,M) New API endpoint added without redeploying core services
  |
  +-- Technology Update
       +-- (L,M) Database can be migrated with <4 hours downtime

Security
  |
  +-- Authentication
  |    +-- (H,L) All API endpoints require valid JWT token
  |    +-- (H,M) Brute force attacks blocked after 5 failed attempts
  |
  +-- Data Protection
       +-- (H,H) PII encrypted at rest and in transit, keys rotated quarterly
```

### Ranking Guide

**Importance (to stakeholders)**
- H: Business-critical, contractual, regulatory
- M: Significant impact on user experience or operations
- L: Nice to have, can defer

**Difficulty (to achieve)**
- H: Requires significant architectural change, unknown solution
- M: Known solution but non-trivial implementation
- L: Straightforward, established pattern

### Architectural Drivers

Scenarios ranked (H,H) or (H,M) are **architectural drivers** - they shape major design decisions.

## Identifying Sensitivity Points

A **sensitivity point** is an architectural decision where a small change significantly affects a quality attribute.

### How to Find Them

1. For each architectural decision, ask: "What happens if we change X by 10%?"
2. If quality attribute impact is disproportionate, mark as sensitivity point

### Examples

| Decision | Parameter | Sensitivity |
|----------|-----------|-------------|
| Connection pool size | Pool size | 10 -> 20 connections: 50% latency improvement |
| Cache TTL | TTL duration | 60s -> 30s: 2x cache misses, 40% more DB load |
| Retry count | Max retries | 3 -> 5 retries: 30% longer timeout, 2x downstream load during failure |
| Thread pool | Thread count | 50 -> 100 threads: Memory doubles, context switching degrades CPU |

## Identifying Tradeoff Points

A **tradeoff point** is an architectural decision that affects two or more quality attributes in opposite directions.

### How to Find Them

1. List decisions that affect multiple quality attributes
2. Identify where improving one degrades another

### Examples

| Decision | QA Improved | QA Degraded |
|----------|-------------|-------------|
| Add caching layer | Performance (+latency) | Consistency (-freshness) |
| Microservices decomposition | Modifiability (+independence) | Performance (-network overhead) |
| Encrypt all data at rest | Security (+confidentiality) | Performance (-CPU overhead) |
| Synchronous API calls | Consistency (+immediacy) | Availability (-cascading failures) |
| Detailed logging | Debuggability (+observability) | Performance (-I/O overhead) |

## Risk Cataloging

### Risk Categories

1. **Architectural Risk**: Decision that may cause problems if wrong
2. **Sensitivity Risk**: Sensitivity point with uncertain optimal value
3. **Tradeoff Risk**: Tradeoff where balance may be wrong for evolving requirements

### Risk Documentation Format

```
RISK: [Short identifier]
CATEGORY: [Architectural | Sensitivity | Tradeoff]
DESCRIPTION: [What could go wrong]
AFFECTED QAs: [List]
LIKELIHOOD: [H/M/L]
IMPACT: [H/M/L]
MITIGATION: [Proposed action]
OWNER: [Role/team responsible]
```

### Example Risk Catalog

```
RISK: R-001 Single Database Bottleneck
CATEGORY: Architectural
DESCRIPTION: All services share single PostgreSQL instance; may not scale beyond 5K TPS
AFFECTED QAs: Performance, Availability
LIKELIHOOD: M
IMPACT: H
MITIGATION: Implement read replicas; design for future sharding
OWNER: Platform team

RISK: R-002 Cache Invalidation Timing
CATEGORY: Sensitivity
DESCRIPTION: Cache TTL of 60s may cause stale data issues for pricing updates
AFFECTED QAs: Consistency, Performance
LIKELIHOOD: H
IMPACT: M
MITIGATION: Implement event-driven cache invalidation for price changes
OWNER: Commerce team

RISK: R-003 Sync vs Async Communication
CATEGORY: Tradeoff
DESCRIPTION: Synchronous order processing ensures consistency but creates availability risk
AFFECTED QAs: Consistency, Availability
LIKELIHOOD: M
IMPACT: H
MITIGATION: Implement circuit breaker; design async fallback path
OWNER: Order team
```

## ATAM Output Artifacts

1. **Utility Tree** - Prioritized quality attribute scenarios
2. **Sensitivity Points** - List with affected QAs
3. **Tradeoff Points** - List with competing QAs
4. **Risk Catalog** - Prioritized risks with mitigations
5. **Non-Risks** - Decisions that were examined and found acceptable
6. **Architectural Approaches** - Catalog of styles/patterns used
