# Quality Attributes Reference

Complete taxonomy of quality attributes for software architecture analysis.

## Quality Attribute Taxonomy

### Runtime Qualities

| Attribute | Definition | Measures |
|-----------|------------|----------|
| **Performance** | Time/resource behavior under load | Latency (p50/p95/p99), throughput (TPS), resource utilization |
| **Availability** | Proportion of time system is operational | Uptime %, MTBF, MTTR |
| **Reliability** | Probability of failure-free operation | Error rate, failure frequency, data loss incidents |
| **Scalability** | Ability to handle increased load | Max concurrent users, linear scaling coefficient |
| **Interoperability** | Ability to exchange information with other systems | API compatibility, protocol support, data format support |

### Development Qualities

| Attribute | Definition | Measures |
|-----------|------------|----------|
| **Modifiability** | Ease of making changes | Time to implement feature, lines changed per feature, coupling metrics |
| **Testability** | Ease of demonstrating faults | Code coverage achievable, test setup time, mock complexity |
| **Maintainability** | Ease of correcting defects | Time to fix bug, MTTR for production issues |
| **Reusability** | Ability to use components elsewhere | Component dependencies, interface generality |
| **Portability** | Ease of moving to new environment | Platform-specific code %, migration effort |

### Security Qualities

| Attribute | Definition | Measures |
|-----------|------------|----------|
| **Confidentiality** | Data accessible only to authorized | Encryption coverage, access control granularity |
| **Integrity** | Data/system protected from unauthorized modification | Audit coverage, tamper detection rate |
| **Authenticity** | Verification of identity claims | Auth methods supported, MFA coverage |
| **Non-repudiation** | Ability to prove actions occurred | Audit log completeness, chain of custody |
| **Accountability** | Actions traceable to actor | Audit log coverage, identity resolution |

### Operations Qualities

| Attribute | Definition | Measures |
|-----------|------------|----------|
| **Deployability** | Ease of deploying new versions | Deployment frequency, rollback time, blue-green capability |
| **Observability** | Ability to understand internal state | Metric coverage, log searchability, trace completeness |
| **Configurability** | Ease of changing behavior without code | Config options count, restart requirements |
| **Recoverability** | Ability to restore after failure | RTO, RPO, backup frequency |
| **Operability** | Ease of operating in production | Runbook coverage, automation level |

### Evolution Qualities

| Attribute | Definition | Measures |
|-----------|------------|----------|
| **Extensibility** | Ease of adding new capabilities | Plugin architecture, extension points |
| **Evolvability** | Ability to change over time | Breaking change frequency, deprecation process |
| **Flexibility** | Ability to adapt to varying requirements | Configuration options, runtime adaptability |

### Business Qualities

| Attribute | Definition | Measures |
|-----------|------------|----------|
| **Time-to-Market** | Speed of delivering features | Lead time, cycle time |
| **Cost** | Development and operational expenses | TCO, cost per transaction |
| **Supportability** | Ease of providing customer support | Issue resolution time, self-service rate |
| **Compliance** | Adherence to regulations | Audit findings, certification status |

## Quality Attribute Scenario Format

A well-formed QA scenario has six parts:

```
SOURCE      ->  STIMULUS       ->  ARTIFACT    ->  ENVIRONMENT  ->  RESPONSE       ->  MEASURE
[Who/what]      [Event/request]    [What]          [Conditions]     [System action]    [Criteria]
```

### Template

```
When [SOURCE] performs [STIMULUS] on [ARTIFACT] under [ENVIRONMENT] conditions,
the system shall [RESPONSE] within [MEASURE].
```

### Examples by Quality Attribute

**Performance**
```
SOURCE:      End user
STIMULUS:    Submits search query
ARTIFACT:    Search service
ENVIRONMENT: Normal load (1000 concurrent users)
RESPONSE:    Returns results
MEASURE:     <200ms at p95
```

**Availability**
```
SOURCE:      Infrastructure
STIMULUS:    Single availability zone failure
ARTIFACT:    Core API
ENVIRONMENT: Production
RESPONSE:    Continues serving requests
MEASURE:     <30 second failover, no data loss
```

**Security**
```
SOURCE:      External attacker
STIMULUS:    Attempts SQL injection
ARTIFACT:    User input fields
ENVIRONMENT: Any
RESPONSE:    Blocks request, logs attempt
MEASURE:     100% detection rate, alert within 1 minute
```

**Modifiability**
```
SOURCE:      Developer
STIMULUS:    Adds new payment provider
ARTIFACT:    Payment module
ENVIRONMENT: Development
RESPONSE:    Implements integration
MEASURE:     <2 developer-days, no changes to order service
```

**Deployability**
```
SOURCE:      CI/CD pipeline
STIMULUS:    Deploys new version
ARTIFACT:    Production environment
ENVIRONMENT: Business hours
RESPONSE:    Completes deployment
MEASURE:     <15 minutes, zero downtime, automatic rollback on failure
```

## Common Quality Attribute Tensions

Architectural decisions often require trading off competing quality attributes:

| Tension | Description | Resolution Strategies |
|---------|-------------|----------------------|
| **Performance vs Security** | Encryption/validation adds latency | Hardware acceleration, efficient algorithms, caching auth decisions |
| **Performance vs Consistency** | Strong consistency requires coordination | Choose consistency level per use case, CQRS |
| **Availability vs Consistency** | CAP theorem | Define consistency requirements per data type |
| **Modifiability vs Performance** | Abstraction layers add overhead | Profile-guided optimization, lazy evaluation |
| **Security vs Usability** | Strong auth friction | Risk-based authentication, SSO |
| **Scalability vs Cost** | Horizontal scaling increases infra cost | Autoscaling, spot instances, reserved capacity |
| **Deployability vs Reliability** | Frequent deploys increase failure risk | Feature flags, canary deployments, automated rollback |
| **Testability vs Performance** | Test hooks add overhead | Compile-time removal, separate test builds |

## NFR Priority Ranking Process

### Step 1: Stakeholder Identification

List stakeholders and their primary concerns:
- Business: Revenue, time-to-market, cost
- Operations: Uptime, observability, deployability
- Security: Compliance, data protection
- Development: Modifiability, testability
- Users: Performance, availability, usability

### Step 2: Pairwise Comparison

For each stakeholder group, rank quality attributes pairwise:
"If you could only have one, would you choose A or B?"

### Step 3: Weighted Scoring

| Quality Attribute | Business | Ops | Security | Dev | Users | Total |
|-------------------|----------|-----|----------|-----|-------|-------|
| Performance       | 3        | 2   | 1        | 2   | 5     | 13    |
| Availability      | 4        | 5   | 2        | 1   | 4     | 16    |
| Security          | 3        | 2   | 5        | 1   | 2     | 13    |
| Modifiability     | 4        | 1   | 1        | 5   | 1     | 12    |

Weights: Business=1.5, Ops=1.2, Security=1.3, Dev=1.0, Users=1.0

### Step 4: Architectural Drivers

Top 3-5 quality attributes become architectural drivers that shape major decisions.

## Quality Attribute Checklist

Before finalizing architecture, verify each critical QA has:

- [ ] Measurable acceptance criteria
- [ ] Specific scenarios with stimulus/response/measure
- [ ] Identified architectural tactics to achieve
- [ ] Trade-offs documented against competing QAs
- [ ] Monitoring/fitness functions defined
- [ ] Stakeholder sign-off on priority
