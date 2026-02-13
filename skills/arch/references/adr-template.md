# ADR Template (MADR 4.0.0)

Markdown Any Decision Record template based on MADR 4.0.0 specification.

## File Naming Convention

```
docs/decisions/NNNN-short-title-with-dashes.md
```

Where NNNN is a zero-padded sequence number (0001, 0002, etc.).

## Status Lifecycle

```
proposed -> accepted -> [deprecated | superseded]
                    \-> rejected
```

- **proposed**: Under discussion
- **accepted**: Approved and implemented
- **rejected**: Considered but not adopted
- **deprecated**: No longer applies (e.g., system decommissioned)
- **superseded**: Replaced by newer decision (link to replacement)

---

## Template

```markdown
# [NNNN] [Short Title]

## Status

[proposed | accepted | rejected | deprecated | superseded by [ADR-NNNN](NNNN-new-decision.md)]

## Context

[Describe the issue motivating this decision. Include technical context, business drivers, and constraints. Be factual and avoid editorializing.]

## Decision Drivers

* [Driver 1: e.g., "Need to support 10x current load within 6 months"]
* [Driver 2: e.g., "Team has limited experience with distributed systems"]
* [Driver 3: e.g., "Must maintain backward compatibility with existing API"]

## Considered Options

1. [Option 1: Brief title]
2. [Option 2: Brief title]
3. [Option 3: Brief title]

## Decision Outcome

**Chosen option: "[Option N]"** because [brief justification linking to drivers].

### Consequences

**Good:**
* [Positive consequence 1]
* [Positive consequence 2]

**Bad:**
* [Negative consequence 1, with mitigation if applicable]
* [Negative consequence 2]

**Neutral:**
* [Side effect that is neither good nor bad]

### Confirmation

[How will we know this decision is working? What metrics, reviews, or checkpoints validate success?]

## Options Detail

### Option 1: [Title]

[Description of the option]

**Pros:**
* [Advantage 1]
* [Advantage 2]

**Cons:**
* [Disadvantage 1]
* [Disadvantage 2]

### Option 2: [Title]

[Description of the option]

**Pros:**
* [Advantage 1]

**Cons:**
* [Disadvantage 1]

### Option 3: [Title]

[Description]

**Pros:**
* [Advantage 1]

**Cons:**
* [Disadvantage 1]

## Links

* [Related ADR](NNNN-related-decision.md)
* [Architecture documentation](../architecture.md)
* [External reference](https://example.com)

## Notes

[Optional: Additional context, meeting notes, stakeholder feedback, or revision history]
```

---

## Quick Template (Minimal)

For simpler decisions that don't require full analysis:

```markdown
# [NNNN] [Short Title]

## Status

accepted

## Context

[1-2 sentences describing the problem]

## Decision

[1-2 sentences stating what we decided]

## Consequences

[2-4 bullet points on impact]
```

---

## ADR Writing Guidelines

### Context Section

- State facts, not opinions
- Include numbers where available (users, transactions, latency)
- Mention constraints (time, budget, skills, existing systems)
- Reference related ADRs if this builds on previous decisions

### Decision Drivers

- Prioritize by importance
- Make drivers specific and measurable where possible
- Include both technical and business drivers
- 3-5 drivers is typical

### Considered Options

- Always include 2+ options (even if one is "do nothing")
- Include options that were seriously considered, not strawmen
- Name options descriptively (not "Option A")

### Decision Outcome

- State the chosen option clearly
- Link decision to specific drivers
- Acknowledge trade-offs explicitly

### Consequences

- Be honest about negatives
- Include mitigation strategies for bad consequences
- Consider short-term vs long-term consequences
- Think about consequences for different stakeholders

### Confirmation

- Define measurable success criteria
- Set timeline for review
- Identify who will evaluate success

---

## Example ADR

```markdown
# 0012 Use PostgreSQL for Order Storage

## Status

accepted

## Context

The order service currently stores orders in MongoDB. With growing order volume (now 50K orders/day, projected 200K/day in 12 months), we're experiencing:
- Increasing query latency for order history (p95 >500ms)
- Difficulty maintaining data consistency across order updates
- Limited support for complex reporting queries

The finance team needs transactional reporting that's difficult to achieve with our current document model.

## Decision Drivers

* Must support ACID transactions for order state changes
* Need efficient complex queries for financial reporting
* Team has strong PostgreSQL experience
* Must migrate with <2 hours downtime

## Considered Options

1. Optimize existing MongoDB setup
2. Migrate to PostgreSQL
3. Migrate to CockroachDB

## Decision Outcome

**Chosen option: "Migrate to PostgreSQL"** because it provides ACID transactions, excellent query performance for our access patterns, and the team has deep expertise, reducing risk and time-to-delivery.

### Consequences

**Good:**
* ACID transactions simplify order state management
* Rich query capabilities support finance reporting needs
* Team expertise reduces implementation risk

**Bad:**
* Migration requires careful planning and testing (~6 weeks)
* Horizontal scaling more complex than MongoDB (mitigated: current projections fit single instance with read replicas)

**Neutral:**
* Need to maintain MongoDB skills for other services

### Confirmation

Success criteria:
- Order history queries <100ms at p95
- Zero data loss during migration
- Finance reports generated in <30 seconds

Review checkpoint: 30 days post-migration

## Options Detail

### Option 1: Optimize existing MongoDB

Add indexes, implement caching, tune queries.

**Pros:**
* No migration risk
* Faster to implement

**Cons:**
* Doesn't solve transaction requirements
* Complex reporting still difficult
* May only delay the problem

### Option 2: Migrate to PostgreSQL

Full migration of order data to PostgreSQL.

**Pros:**
* ACID transactions
* Excellent query optimizer
* Team expertise
* Mature ecosystem

**Cons:**
* Migration effort and risk
* Horizontal scaling requires more planning

### Option 3: Migrate to CockroachDB

Distributed SQL database with horizontal scaling.

**Pros:**
* ACID transactions
* Built-in horizontal scaling
* PostgreSQL wire protocol

**Cons:**
* Team unfamiliar with operations
* Higher infrastructure complexity
* Overkill for current scale

## Links

* [ADR-0008: Order Service Architecture](0008-order-service-architecture.md)
* [PostgreSQL Migration Runbook](../runbooks/postgres-migration.md)
```
