---
name: lev-research/templates
description: |
  [WHAT] Pre-built research templates for common analysis patterns
  [HOW] Structured perspective queries for tech assessment, gap analysis, and architecture exploration
  [WHEN] Use when researching follows a known pattern (evaluate tech, find gaps, understand architecture)
  [WHY] Templates ensure comprehensive coverage and consistent research quality

  Triggers: "assess", "evaluate", "gap analysis", "architecture exploration", "technology assessment"

lifecycle_integration:
  stage: captured
  input_artifact: null
  output_artifact: assessment-report.md

related_skills:
  - lev-research/perspectives
  - lev-find
---

# lev-research/templates - Research Templates

## Lev Concept

**What are research templates?**

Pre-structured research patterns that apply the 5-perspective methodology to common analysis scenarios. Instead of manually crafting queries, templates provide proven query sets for specific research goals.

**Why use templates?**

- **Consistency** - Same quality across similar research tasks
- **Completeness** - Templates ensure no perspective is missed
- **Speed** - Skip query crafting, use proven patterns
- **Best practices** - Encodes lessons from past research

**When to use templates:**
- Technology assessment (evaluate a tool/framework)
- Gap analysis (find what's missing)
- Architecture exploration (understand system design)
- Migration planning (assess current → future state)

---

## CLI Commands

### Invoke Template

```bash
# Technology assessment
lev-research "Redis" --template=technology_assessment

# Gap analysis
lev-research "error handling" --template=gap_analysis

# Architecture exploration
lev-research "API gateway" --template=architecture_exploration

# List available templates
lev-research --list-templates
```

### Custom Template

```bash
# Use template with custom parameters
lev-research "GraphQL" --template=technology_assessment --indexes=codebase,docs,tasks

# Override template queries
lev-research "caching" --template=gap_analysis --custom-queries=queries.yaml
```

---

## Workflows

### Workflow 1: Technology Assessment Template

**Use case:** Evaluating a technology/tool/framework for adoption or understanding current usage.

**Input:** Technology name (e.g., "Redis", "GraphQL", "Docker")

**Template structure:**
```yaml
research_template: technology_assessment
query: "assess {technology} for {use_case}"

perspectives:
  1_technical:
    queries:
      - "{technology} implementation patterns"
      - "{technology} architecture"
      - "{technology} performance benchmarks"
    indexes: [codebase, documentation]

  2_integration:
    queries:
      - "how to integrate {technology}"
      - "{technology} API usage"
      - "{technology} configuration"
    indexes: [codebase, documentation]

  3_existing_usage:
    queries:
      - "current {technology} usage"
      - "where is {technology} used"
      - "{technology} examples"
    indexes: [codebase]

  4_decisions:
    queries:
      - "why {technology} chosen"
      - "{technology} alternatives considered"
      - "{technology} decision ADR"
    indexes: [documentation, sessions]

  5_future:
    queries:
      - "TODO {technology} improvements"
      - "{technology} migration plans"
      - "{technology} issues"
    indexes: [tasks]

synthesis:
  - Current usage and patterns
  - Integration approach
  - Rationale and alternatives
  - Future plans and gaps
```

**Output example:**
```markdown
# Technology Assessment: Redis

## Current Usage
- Cache layer for API responses (src/cache/redis.ts)
- Session storage (src/auth/session-store.ts)
- Rate limiting (src/middleware/rate-limit.ts)

## Integration Patterns
- Bull queues for background jobs
- ioredis client with cluster support
- Redis Sentinel for HA

## Decision Rationale
- ADR-012: Chose Redis over Memcached for pub/sub support
- Performance: 10x faster than DB queries for session data
- Alternatives considered: Memcached, in-memory JS Map

## Future Plans
- TODO: Implement Redis Streams for event sourcing (#234)
- TODO: Add Redis cache warming on deploy (#189)
- Known issue: Connection pool exhaustion under load (#156)

## Recommendations
1. Add monitoring for cache hit rates
2. Document cache invalidation strategy
3. Plan Redis Streams migration (Q2)
```

---

### Workflow 2: Gap Analysis Template

**Use case:** Finding what's missing in a specific area (features, docs, tests, coverage).

**Input:** Area to analyze (e.g., "error handling", "authentication", "testing")

**Template structure:**
```yaml
research_template: gap_analysis
query: "find gaps in {area}"

perspectives:
  1_what_exists:
    queries:
      - "{area} implementation"
      - "{area} features"
      - "{area} coverage"
    indexes: [codebase, documentation]

  2_what_should_exist:
    queries:
      - "{area} requirements"
      - "{area} specifications"
      - "{area} best practices"
    indexes: [documentation, sessions]

  3_what_is_planned:
    queries:
      - "TODO {area}"
      - "{area} roadmap"
      - "{area} issues"
    indexes: [tasks]

  4_what_is_missing:
    - Cross-reference 1, 2, and 3
    - Identify requirements without implementation
    - Find planned work not in tasks
    - Discover undocumented functionality

synthesis:
  - Coverage map (implemented, documented, planned)
  - Gap identification (missing pieces)
  - Priority recommendations (what to do first)
```

**Output example:**
```markdown
# Gap Analysis: Error Handling

## What Exists
- Global error middleware (src/middleware/error-handler.ts)
- Custom error classes (src/errors/)
- Logging with Winston

## What Should Exist (Requirements)
- REQ-SEC-001: PII redaction in error logs
- REQ-OPS-003: Error alerting to Sentry
- Best practice: Structured error responses

## What Is Planned
- TODO: Implement error boundary for React (#145)
- Roadmap: Add error analytics dashboard (Q3)

## Gaps Identified
1. ❌ Missing: PII redaction (required by REQ-SEC-001)
2. ❌ Missing: Sentry integration (required by REQ-OPS-003)
3. ❌ Missing: Error documentation for API consumers
4. ⚠️  Undocumented: Custom error classes usage patterns
5. ⚠️  Planned but not tracked: Error analytics (needs BD task)

## Priority Recommendations
1. P0: Implement PII redaction (compliance requirement)
2. P1: Set up Sentry integration (operational visibility)
3. P2: Document error handling patterns (developer experience)
4. P3: Create BD task for error analytics dashboard
```

---

### Workflow 3: Architecture Exploration Template

**Use case:** Understanding how a component/system/module is designed and how it works.

**Input:** Component name (e.g., "API gateway", "auth system", "payment processing")

**Template structure:**
```yaml
research_template: architecture_exploration
query: "understand {component} architecture"

perspectives:
  1_structure:
    queries:
      - "{component} structure"
      - "{component} organization"
      - "{component} modules"
    indexes: [codebase]

  2_behavior:
    queries:
      - "how {component} works"
      - "{component} flow"
      - "{component} lifecycle"
    indexes: [codebase, documentation]

  3_interactions:
    queries:
      - "{component} dependencies"
      - "what uses {component}"
      - "{component} integration"
    indexes: [codebase]

  4_design:
    queries:
      - "{component} design decisions"
      - "why {component} architecture"
      - "{component} patterns"
    indexes: [documentation, sessions]

  5_evolution:
    queries:
      - "{component} refactoring"
      - "{component} changes history"
      - "TODO {component} improvements"
    indexes: [sessions, tasks]

synthesis:
  - Architecture diagram (structure + interactions)
  - Design rationale (why it works this way)
  - Evolution narrative (how it got here)
  - Future trajectory (where it's going)
```

**Output example:**
```markdown
# Architecture Exploration: API Gateway

## Structure
```
src/gateway/
├── routes/           # Route definitions
├── middleware/       # Request/response pipeline
├── handlers/         # Business logic handlers
└── plugins/          # Extension points
```

## Behavior
1. Request arrives → rate limiting middleware
2. Authentication middleware validates JWT
3. Route matcher selects handler
4. Handler executes business logic
5. Response formatter applies transformations
6. Logging middleware records metrics

## Interactions
**Dependencies:**
- Redis (rate limiting, caching)
- PostgreSQL (user data)
- RabbitMQ (async tasks)

**Dependents:**
- Web frontend (primary consumer)
- Mobile app (via REST API)
- Partner integrations (webhook callbacks)

## Design Decisions
- ADR-008: Chose Express over Fastify for middleware ecosystem
- ADR-015: Hexagonal architecture for testability
- Pattern: Middleware pipeline for separation of concerns

## Evolution
- v1.0: Monolithic Express app
- v2.0: Extracted middleware pipeline (2024-03)
- v2.5: Added plugin system (2024-08)
- TODO: Migrate to Fastify for performance (#234)
- TODO: Add GraphQL support (#189)

## Recommendations
1. Document plugin development guide
2. Add architecture diagram to docs
3. Plan Fastify migration (Q2 2026)
```

---

## Relates

### Depends On
- `lev-research/perspectives` - All templates use 5-perspective pattern
- `lev-find` - Executes template queries

### Works With
- `bd` - Create tasks from gap analysis results
- `lev-codifier` - Package research into skills/docs
- `exa-plus` - External research for prior art

### Enables
- `lev-cdo` - Planning based on assessments
- `lev-align` - Validation using architecture exploration
- Migration planning workflows

---

## Tips

**Customize templates:**
- Override queries for specific domains
- Add/remove perspectives as needed
- Adjust indexes for project structure

**Combine templates:**
```bash
# Assess → Find gaps → Plan migration
lev-research "Redis" --template=technology_assessment
lev-research "caching" --template=gap_analysis
# Then use findings for migration planning
```

**Create new templates:**
- Follow YAML structure above
- Save to `~/.lev/research/templates/{name}.yaml`
- Test on 2-3 topics before publishing
