---
name: backend-for-frontend
description: Create client-specific backend services that aggregate and transform data from downstream microservices to match each frontend's unique needs
---

# Backend for Frontend (BFF) Pattern

## Overview

The Backend for Frontend (BFF) pattern is a microservices architecture where separate backend services are created for each user interface or client type (web app, mobile app, IoT devices). Rather than forcing all frontends to consume a generic API, each BFF acts as a translation layer that aggregates data from multiple downstream microservices and transforms it to match the specific needs, data formats, and performance constraints of its corresponding frontend.

Introduced by Sam Newman in "Building Microservices," the BFF pattern emphasizes that each frontend should have its own tailored backend owned by the frontend team, not a shared backend team. This enables frontend and backend teams to evolve independently, optimizes API responses for specific clients (reducing over-fetching and under-fetching), and prevents the "one-size-fits-all API" anti-pattern. Common implementations use GraphQL (natural aggregation, flexible queries) or REST with custom aggregation logic. The key trade-off: improved frontend autonomy and performance versus increased operational complexity and potential code duplication across BFFs.

## When to Use

- Application serves multiple client types (web, iOS, Android, IoT) with different data needs
- Frontends require different data formats, interaction patterns, or performance characteristics
- Microservices architecture with 5+ downstream services requiring complex aggregation
- Preventing over-fetching (mobile bandwidth constraints) or under-fetching (multiple round trips)
- Frontend teams blocked by slow backend API changes from centralized team
- Different security/authorization requirements per client type
- Mobile apps need optimized payloads while web can handle richer data

## The Process

### Step 1: Identify Client-Specific Requirements

Analyze each frontend's unique data needs, performance constraints, and interaction patterns. BFF pattern makes sense only when clients have meaningfully different requirements.

**Map data needs per client:** Web dashboard needs full user profiles with analytics. Mobile app needs minimal user data for performance. IoT device needs only status updates, no UI metadata.

**Performance constraints:** Mobile on cellular: minimize payload size, reduce round trips. Web on WiFi: richer data acceptable. Desktop app: maximum data for offline capability.

**Interaction patterns:** Web SPA: one large initial load, then incremental updates. Mobile: frequent small requests to conserve battery. Admin dashboard: complex filters, aggregations, exports.

**When requirements converge:** If all clients need the same data format and performance characteristics, a general-purpose API works better - don't add BFF complexity unnecessarily.

**Output:** Client requirements matrix showing data needs, payload size constraints, latency requirements, and aggregation complexity per frontend type.

### Step 2: Design BFF Boundaries and Ownership

Create one BFF per frontend type (not per team or feature). Establish clear ownership - frontends own their BFFs.

**BFF per frontend type:** Common pattern - `web-bff`, `mobile-bff`, `admin-bff`. Avoid creating one BFF per platform variant (iOS/Android share `mobile-bff` unless truly different needs).

**Team ownership:** Frontend team owns their BFF codebase, deployment, and evolution. This is critical - centralized backend teams owning BFFs recreates the bottleneck BFF pattern solves. Frontend developers write BFF aggregation logic.

**Technology choice:** GraphQL naturally fits BFF pattern (flexible queries, built-in aggregation, schema stitching). REST requires custom aggregation endpoints. Some teams use GraphQL BFF wrapping REST microservices.

**Avoid feature-based BFFs:** Don't create `payments-bff`, `search-bff` - this is just a microservice, not BFF pattern. BFF organizes by client type, not domain.

**Shared infrastructure:** While BFFs are independent services, they can share deployment infrastructure, monitoring, authentication libraries (to avoid complete duplication).

### Step 3: Implement API Aggregation and Transformation

Build BFF to aggregate downstream microservices and transform responses to match frontend needs. This is the core BFF responsibility.

**API aggregation:** BFF calls multiple downstream services (user service, order service, inventory service) in parallel or sequentially, then combines responses into single payload. Example: mobile product page aggregates product details + reviews + inventory + recommendations into one response.

**Data transformation:** Downstream APIs return server-optimized formats. BFF reshapes to client-optimized format. Example: backend returns ISO timestamps, BFF converts to "2 hours ago" for mobile. Backend returns full address objects, BFF flattens to single string for list view.

**Query optimization:** Prevent N+1 queries by batching downstream requests. Use DataLoader pattern (batch and cache requests within single request). GraphQL BFFs get this automatically with Apollo DataSources.

**Response filtering:** Mobile BFF omits heavy fields (full descriptions, high-res images). Web BFF includes everything. Admin BFF adds audit metadata. Same backend data, different projections.

**Error handling:** BFF decides degradation strategy when downstream fails. Mobile BFF returns cached data. Web BFF shows partial UI. Admin BFF surfaces full error diagnostics.

### Step 4: Manage Code Duplication Strategically

Address the primary BFF trade-off - multiple BFFs implementing similar logic. Use libraries for shared concerns, but accept some duplication.

**Shared libraries for horizontal concerns:** Authentication, logging, monitoring, rate limiting - extract to shared libraries consumed by all BFFs. Don't duplicate infrastructure code.

**Accept business logic duplication initially:** When two BFFs implement similar aggregation logic, don't immediately create abstraction. Follow "rule of three" - extract to shared service after third implementation, not second.

**Downstream consolidation over BFF abstraction:** If all BFFs duplicate same aggregation logic, the downstream microservices may be poorly designed. Push aggregation downstream to dedicated service rather than sharing code across BFFs.

**Avoid "shared BFF":** Creating a shared layer used by all BFFs defeats the pattern purpose. Better to have a proper API gateway or consolidate downstream.

**Measure duplication:** Track what percentage of BFF code is duplicated. <20% acceptable (authentication, utilities). >50% signals architecture problem (wrong boundaries or missing downstream service).

### Step 5: Deploy and Monitor BFF Layer

Treat BFFs as independent services with deployment, monitoring, and reliability practices. Don't let BFF become single point of failure.

**Independent deployment:** Each BFF deploys on its own cadence with its frontend. Web BFF deploys 20x/day with web app. Mobile BFF deploys less frequently (app store release cycle).

**Circuit breakers and timeouts:** BFF aggregates multiple services - one slow service can't block entire response. Use circuit breakers (Netflix Hystrix, resilience4j). Set aggressive timeouts (prefer partial data to slow response).

**Monitoring and alerting:** Track BFF-specific metrics - aggregation latency, downstream call fan-out, cache hit rates, client error rates. Separate dashboards per BFF (mobile vs. web have different baselines).

**Performance budgets:** Mobile BFF has strict payload size budget (<100KB). Web BFF has latency budget (<200ms p95). Monitor and alert on budget violations.

**Versioning strategy:** BFF versions with its frontend, not downstream services. Mobile BFF v2 supports app v2 requirements while v1 remains for older app versions. Downstream services must maintain compatibility.

## Example Application

**Situation:** E-commerce platform with microservices (products, users, orders, reviews, inventory). Generic REST API forcing mobile app to make 7 requests per product page, consuming 850KB data, 3.2s load time on 3G.

**Step 1 - Requirements:** Mobile needs minimal data (title, price, thumbnail, availability) in 1 request. Web needs rich data (full gallery, reviews, specs, recommendations) acceptable in 2-3 requests. Admin dashboard needs audit metadata (created dates, edit history) not relevant to customers.

**Step 2 - Boundaries:** Created 3 BFFs - `mobile-bff` (owned by mobile team), `web-bff` (owned by web team), `admin-bff` (owned by admin team). Selected GraphQL for mobile/web BFFs (flexible queries), REST for admin BFF (simpler needs).

**Step 3 - Aggregation:** Mobile BFF `productPage(id)` query aggregates 5 downstream services (products, inventory, reviews-summary, recommendations, user-favorites) in parallel, returns 45KB optimized payload. Web BFF allows client to query specific fields. Admin BFF adds audit trail data from separate audit service.

**Step 4 - Duplication:** All BFFs shared authentication library (JWT validation) and observability middleware. Mobile/Web BFFs initially duplicated product aggregation logic (acceptable). After Admin BFF needed similar logic (third implementation), extracted shared product-aggregation-service consumed by all BFFs.

**Step 5 - Deployment:** Mobile BFF deployed with 500ms timeout, 100KB response size limit. Circuit breakers on all downstream calls with fallback to cached data. Separate Datadog dashboards per BFF. Mobile BFF v1/v2 coexist supporting old/new app versions.

**Outcome:** Mobile product page: 7 requests → 1 request, 850KB → 45KB (95% reduction), 3.2s → 0.8s load time (75% improvement). Web and mobile evolved independently (web added AR preview without mobile changes). Mobile team velocity increased 3x (no backend team dependency).

## Anti-Patterns

- ❌ Creating BFFs per team/feature rather than per client type - misses pattern purpose
- ❌ Backend team owns all BFFs - recreates centralized bottleneck BFF solves
- ❌ Using BFF when all clients have identical needs - unnecessary complexity
- ❌ BFF contains business logic beyond aggregation/transformation - belongs in domain services
- ❌ Creating "shared BFF" layer used by all BFFs - defeats independence benefit
- ❌ Immediately abstracting any duplicated code - accept duplication until third occurrence
- ❌ BFF calling other BFFs - creates coupling, indicates wrong boundaries
- ❌ Single BFF for all mobile platforms when iOS/Android have vastly different needs

## Related

- api-gateway-pattern (different level of abstraction)
- graphql-schema-stitching (BFF implementation technique)
- microservices-architecture (foundational pattern)
- api-composition-pattern (related aggregation approach)
- circuit-breaker-pattern (resilience for downstream calls)
- caching-strategies (performance optimization)
- rate-limiting (protecting downstream services)
