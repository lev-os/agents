---
name: half-life
description: Model decay processes by the time required for half of a quantity to degrade, enabling exponential decay predictions
---

# Half-Life

**What**: The time required for half of a quantity to decay or lose half its value—applies to radioactive decay, drug metabolism, information relevance, and any exponential decay process.

**When to use**: Modeling decay of knowledge, skill retention, technical debt accumulation, or any process where value/quantity declines exponentially over time.

**Introduced by**: Ernest Rutherford (1907) for radioactive decay; widely applied concept

## Core Mechanism

**Exponential decay formula**: N(t) = N₀ × (1/2)^(t/t₁/₂)

Where:
- N(t) = remaining quantity at time t
- N₀ = initial quantity
- t₁/₂ = half-life period

**Key insight**: After one half-life, 50% remains. After two half-lives, 25% remains. Decay is exponential, not linear.

## Execution Steps

### 1. Identify Decaying Quantity
What degrades over time? Knowledge, skills, relationships, documentation accuracy?

### 2. Measure Half-Life
How long until half the value is lost? Historical data or estimation.

### 3. Model Future Decay
Use half-life formula to predict future state.

### 4. Determine Refresh Cycle
How often must you refresh to maintain minimum threshold?

### 5. Design Decay Mitigation
Build reinforcement loops to counteract natural decay.

## Real-World Applications

**Documentation**: Half-life ~6-12 months in fast-moving projects. After 2 years, <25% still accurate.
**Skills**: Programming language knowledge half-life depends on ecosystem velocity (JavaScript ~2 years, SQL ~10 years)
**Relationships**: Professional network half-life ~2-3 years without maintenance
**Cache**: Data freshness half-life determines cache TTL

## Scoring Criteria

**Practitioner Weight**: 9/10 — Rutherford's work empirically validated; widely used in physics, medicine, chemistry
**Clarity & Executability**: 9/10 — Clear quantitative model; directly actionable
**Proven ROI**: 8/10 — Enables nuclear medicine, carbon dating, cache strategies, learning models
**Novelty**: 7/10 — Intuitive for physical decay; insightful when applied to information/skills
**Cross-Domain Applicability**: 9/10 — Physics, medicine, software caching, knowledge management, skill development

**Total Score**: 42/50 (Tier 1: Canonical)
