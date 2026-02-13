---
name: team-topologies
description: Organizational design framework using four team types and three interaction modes to optimize flow and reduce cognitive load
---

# Team Topologies

## Overview

Team Topologies (2019) by Matthew Skelton and Manuel Pais provides a practical framework for organizing technical teams based on how software actually gets built. The core insight: team structure should follow the software architecture (Conway's Law), and organizations should deliberately design team interactions to optimize for fast flow of change. The framework defines exactly four fundamental team types (Stream-aligned, Enabling, Complicated Subsystem, Platform) and three interaction modes (Collaboration, X-as-a-Service, Facilitating). This constraint forces clarity and reduces cognitive load, enabling teams to own bounded contexts end-to-end.

## When to Use

- Reorganizing engineering teams for faster delivery and reduced handoffs
- Diagnosing why software architecture doesn't match business needs
- Reducing cognitive load on teams overwhelmed by too many responsibilities
- Planning platform team investments and internal developer experience
- Breaking monoliths into microservices with team boundaries that match
- Scaling organizations while maintaining autonomy and flow
- Applying Conway's Law deliberately rather than accidentally
- Transitioning from project-based to product-based team structures

## The Process

### Step 1: Map Current Team Interactions and Dependencies

Document existing teams and how they interact. Identify handoffs, wait states, and cognitive load problems. Look for teams with too many dependencies or too broad a scope. Note where Conway's Law is creating accidental architecture. **Example:** Team A needs approval from 3 other teams to deploy, creating 2-week cycle times despite 2-day technical work.

### Step 2: Define Stream-Aligned Teams Around Business Value

Create teams aligned to a single stream of business value (product, service, user journey, or persona). These are your primary teams - they should be able to deliver value independently. Each stream-aligned team owns their domain end-to-end, from requirements to production. Target team size: 5-9 people (cognitive limit). **Example:** Payments team owns checkout flow, payment processing, refunds, and reporting for payment domain.

### Step 3: Identify Complicated Subsystem Teams

Separate components requiring deep specialist knowledge that would overwhelm stream-aligned teams. These teams reduce cognitive load by encapsulating complexity (ML models, video processing, cryptography). Only create when subsystem genuinely requires specialized expertise AND is shared across streams. **Example:** ML Recommendations team owns model training pipeline, serving infrastructure, and experiment framework used by multiple product teams.

### Step 4: Design Platform Teams for Self-Service

Platform teams provide internal services that stream-aligned teams consume as self-service. Goal: reduce cognitive load by abstracting infrastructure/common capabilities. Platform should be "paved road" not "toll gate" - stream teams can opt out but usually won't. Treat internal teams as customers with SLAs. **Example:** Developer Platform team provides CI/CD, observability, and deployment tooling that product teams consume via APIs.

### Step 5: Deploy Enabling Teams for Capability Building

Enabling teams help stream-aligned teams acquire new capabilities (testing practices, cloud migration, new frameworks). Temporary engagement, not permanent dependency. Success = stream team can do it themselves. Facilitating interaction mode, then move on. **Example:** SRE Enablement team helps product teams adopt on-call practices, then reduces engagement as team matures.

### Step 6: Define Team Interaction Modes Explicitly

Choose interaction mode for each team pair: (1) Collaboration - close work together, temporary, high bandwidth; (2) X-as-a-Service - clear API, minimal coordination, versioned contract; (3) Facilitating - one team helps another grow capability, time-boxed. Document expected modes and evolution over time. **Example:** New domain: Platform + Stream collaborate closely. Mature domain: Platform provides X-as-a-Service, Stream consumes independently.

### Step 7: Evolve Topology as Software Evolves

Team topologies aren't static - plan for evolution. As domains mature, interaction modes should shift (collaboration to X-as-a-Service). As complexity emerges, consider complicated subsystem extraction. Review topology quarterly against delivery metrics and cognitive load. **Example:** After 6 months of collaboration, Platform team graduates infrastructure to self-service, allowing Stream team independence.

## Example Application

**Situation:** 200-person engineering org structured by function (frontend, backend, QA, ops). Cross-team coordination consuming 40% of capacity. Deployments require 8 team signoffs. Mean time to production: 3 weeks.

**Application:**
- Step 1: Mapped dependencies - every feature required 5+ teams, 12 handoff points per deployment
- Step 2: Created 8 stream-aligned teams around customer journeys (Onboarding, Core Product, Billing, Integrations)
- Step 3: Extracted ML team (recommendation models used by 6 streams) and Data Infrastructure (specialized knowledge)
- Step 4: Formed Platform team providing: CI/CD, Kubernetes, observability, feature flags as self-service
- Step 5: Created Enablement team for testing practices - 6-week engagement per stream team, then moved on
- Step 6: Documented interaction modes: Platform provides X-as-a-Service to all streams, ML team collaborates with Personalization stream while serving others via API
- Step 7: Quarterly review process established, with metrics: deployment frequency, cognitive load surveys, team autonomy scores

**Outcome:** Deployment frequency increased from bi-weekly to daily. Mean time to production dropped to 2 days. Team satisfaction increased 45%. Architecture began naturally aligning with team boundaries.

## Anti-Patterns

- Creating matrix organizations where teams report to multiple structures
- Platform teams that become gatekeepers instead of enablers
- Too many team types (beyond the 4 fundamental types adds confusion)
- Stream teams that depend on 5+ other teams to deliver (scope too broad or wrong boundaries)
- Permanent collaboration mode (should be temporary, move to X-as-a-Service)
- Enabling teams that create permanent dependencies instead of building capability
- Ignoring cognitive load when defining team scope (too broad = overwhelm)
- Forcing microservices without matching team structure (Conway's Law violation)
- Project teams that form and disband (prevents ownership and learning)

## Related

- Conway's Law - "organizations design systems that mirror their communication structure"
- Inverse Conway Maneuver - deliberately designing team structure to get desired architecture
- Domain-Driven Design - bounded contexts align naturally with stream-aligned teams
- DevOps - full ownership from stream-aligned teams enables DevOps practices
- Accelerate (Forsgren et al.) - research on organizational performance metrics
- The Phoenix Project - narrative illustrating flow and DevOps transformation
- High Output Management - complementary framework for team management within topologies
