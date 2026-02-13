# Layers — Shearing Layers Classifier Reference

Full reference for Stewart Brand's "How Buildings Learn" framework applied to software architecture, crossed with Lev's L0-L3 depth model.

---

## Core Theory

Stewart Brand observed that buildings are composed of layers that change at different rates. These layers **shear against each other** because of their different velocities. The layers that change slowly constrain those that change quickly.

> "Because of the different rates of change of its components, a building is always tearing itself apart."
> — Stewart Brand, *How Buildings Learn* (1994)

This applies directly to software systems: the database schema (Site) changes on a different timescale than UI copy (Stuff), and coupling them creates shearing stress.

---

## The 6 Brand Layers

### Layer 1: Site (Decades)

**Building:** Geographic location, legal lot, orientation
**Software:** Core domain model, database schema, fundamental data structures

```
Velocity:    Slowest — changes measured in years to decades
Persistence: Maximum — survives complete rewrites
Risk:        Highest — wrong choice constrains everything above
Examples:
  - PostgreSQL → MongoDB migration
  - Monolith → microservices split
  - Core entity model redesign
  - Primary language choice (Rust, TypeScript, Python)
```

**Architectural implication:** Design reviews mandatory. Migration plans required. Never change casually.

---

### Layer 2: Structure (30-50 years)

**Building:** Foundation, load-bearing walls, structural frame
**Software:** Module boundaries, API contracts, authentication/authorization architecture

```
Velocity:    Slow — changes every few years
Persistence: High — survives feature cycles
Risk:        High — breaking changes propagate widely
Examples:
  - Auth system migration (JWT → OAuth2)
  - API versioning strategy change
  - Module extraction / monorepo restructure
  - Event bus architecture change
  - Core SDK interface redesign
```

**Architectural implication:** Need backward compatibility plan. Phased rollout. Feature flags for transition.

---

### Layer 3: Skin (20 years)

**Building:** Exterior cladding, facade, paint, windows
**Software:** UI framework, design system, public-facing API surface

```
Velocity:    Medium — changes every 1-3 years
Persistence: Medium — survives several release cycles
Risk:        Medium — user-visible, but usually reversible
Examples:
  - React → Svelte migration
  - Material UI → custom design system
  - REST → GraphQL surface layer
  - Mobile app native → cross-platform
  - Website redesign (full visual refresh)
```

**Architectural implication:** Visual review needed. User testing recommended. Can experiment with feature flags.

---

### Layer 4: Services (7-15 years)

**Building:** HVAC, electrical, plumbing, elevators
**Software:** CI/CD, monitoring, deployment, infrastructure-as-code

```
Velocity:    Fast — changes multiple times per year
Persistence: Medium — survives project phases
Risk:        Medium — failure affects all developers/operations
Examples:
  - Jenkins → GitHub Actions migration
  - Add Datadog/New Relic monitoring
  - Docker → Kubernetes migration
  - Terraform module restructure
  - Add/change CDN configuration
```

**Architectural implication:** Ops review needed. Rollback plan required. Test in staging first.

---

### Layer 5: Space Plan (3-7 years)

**Building:** Interior walls, room layouts, furniture arrangement
**Software:** Feature routing, page layouts, navigation structure, configuration

```
Velocity:    Faster — changes monthly to quarterly
Persistence: Low-Medium — tied to feature lifecycle
Risk:        Lower — user flow impact, usually recoverable
Examples:
  - Add new route/page to application
  - Reorganize navigation menu
  - Feature flag implementation
  - A/B test configuration
  - Permission/role restructure
  - Add new API endpoint (non-breaking)
```

**Architectural implication:** User flow review helpful. Feature flags recommended. Quick iteration expected.

---

### Layer 6: Stuff (Daily)

**Building:** Furniture, decorations, personal items
**Software:** Copy text, log messages, env variables, config values, error messages

```
Velocity:    Fastest — changes daily or per-commit
Persistence: Minimal — ephemeral, easily replaced
Risk:        Lowest — easily reversible, rarely breaks things
Examples:
  - Error message wording
  - Log format changes
  - Environment variable values
  - README updates
  - Comment improvements
  - Debug flag toggles
```

**Architectural implication:** Ship fast. No review needed for most changes. Iterate freely.

---

## L0-L3 Depth Model Cross-Reference

Lev's depth model is orthogonal to Brand's velocity model. Together they form a 2D classification space.

### Depth Definitions

```
L0: OVERVIEW  — High-level summary, orientation, "what is this?"
L1: STRUCTURE — Components, boundaries, relationships
L2: DETAILS   — Implementation specifics, how things work
L3: RUNTIME   — Behavior, state transitions, live data
```

### Cross-Reference Matrix

| | Site | Structure | Skin | Services | Space Plan | Stuff |
|---|---|---|---|---|---|---|
| **L0** | Domain vision | System architecture | Brand identity | Infra strategy | UX strategy | Content strategy |
| **L1** | Entity model | Module boundaries | Component library | Pipeline config | Route structure | Config schema |
| **L2** | Table schemas | API contracts | Component props | Deploy scripts | Feature logic | Env values |
| **L3** | Query perf | Auth flows | Render behavior | Health checks | User sessions | Log output |

### Persistence Layer

The third dimension: **persistence** determines whether something lives in the System Graph (permanent) or CDO Graph (ephemeral).

```
System Graph (permanent):
  - Database schemas, API contracts, module boundaries
  - Infrastructure config, deployment manifests
  - Source code, test suites

CDO Graph (ephemeral):
  - Design proposals, architecture decisions in progress
  - Debug sessions, investigation notes
  - Feature experiments, A/B test analysis
  - Brainstorm outputs, research findings
```

**Rule of thumb:**
```
If it goes into version control → System Graph
If it informs a decision but isn't the decision → CDO Graph
If it's a thinking artifact → CDO Graph
If it's an implementation artifact → System Graph
```

---

## Classification Algorithm

```
INPUT: description of change

STEP 1 — Velocity Classification
  Parse for keywords:
    Site:       "schema", "migration", "core model", "database", "fundamental"
    Structure:  "architecture", "module", "boundary", "API contract", "auth"
    Skin:       "UI", "design", "component", "visual", "frontend framework"
    Services:   "CI", "CD", "monitoring", "deployment", "infrastructure"
    Space Plan: "route", "feature", "navigation", "config", "permission"
    Stuff:      "message", "log", "env", "copy", "comment", "readme"

STEP 2 — Depth Classification
  Parse for scope signals:
    L0: "overview", "strategy", "vision", "high-level"
    L1: "boundary", "interface", "structure", "component"
    L2: "implement", "function", "props", "config", "script"
    L3: "runtime", "trace", "behavior", "state", "performance"

STEP 3 — Persistence Classification
  Parse for artifact type:
    System:  "code", "schema", "config", "test", "deploy"
    CDO:     "design", "proposal", "analysis", "research", "brainstorm"

OUTPUT: { layer, depth, persistence, review_requirements }
```

---

## Review Requirements by Classification

| Classification | Review Type | Approvers | Time Budget |
|---------------|------------|-----------|-------------|
| Site + L1 + System | Architecture review | Senior eng + architect | 1-2 weeks |
| Structure + L1-L2 + System | Design review | Team lead | 3-5 days |
| Skin + L2 + System | Visual + code review | Designer + dev | 1-3 days |
| Services + L2 + System | Ops review | DevOps + team lead | 1-2 days |
| Space Plan + L2 + CDO→System | Feature review | PM + dev | 1-2 days |
| Stuff + L3 + CDO | Self-review sufficient | Author | Same day |

---

## Coupling Inversions (Anti-Patterns)

When a fast layer depends on a slow layer's implementation details (not interface):

```
❌ Stuff depending on Site internals
   Example: Error messages hardcoded to database column names

❌ Space Plan coupled to Structure internals
   Example: Feature flags that depend on auth implementation details

❌ Skin coupled to Services
   Example: UI components that import deployment config

✓ Slow layers exposing stable interfaces to fast layers
✓ Fast layers consuming only published contracts
✓ Each layer owning its own rate of change
```

**Fix coupling inversions by:**
1. Introduce an interface at the layer boundary
2. Fast layer depends on interface, not implementation
3. Slow layer implements the interface

---

## Quick Reference Card

```
🏗️ LAYERS — 3 questions, 15 seconds

Q1: How fast does it change?
    Site → Structure → Skin → Services → Space Plan → Stuff
    (slow)                                          (fast)

Q2: How deep is the detail?
    L0 Overview → L1 Structure → L2 Details → L3 Runtime
    (high)                                       (ground)

Q3: Permanent or ephemeral?
    System Graph (code, config, schema)
    CDO Graph (proposals, analysis, research)
```
