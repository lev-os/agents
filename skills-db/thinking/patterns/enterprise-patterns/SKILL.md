---
name: enterprise-patterns
description: Apply proven architectural patterns from Martin Fowler's PoEAA for building scalable, maintainable enterprise applications - Repository, Unit of Work, Service Layer, Domain Model
---

# Enterprise Patterns

## Overview

Enterprise Patterns are a collection of over 40 proven architectural patterns documented by Martin Fowler in "Patterns of Enterprise Application Architecture" (PoEAA) for solving recurring challenges in large-scale business applications. Despite technology evolution from Smalltalk to CORBA to Java to .NET to modern cloud, the same fundamental design problems persist: managing domain logic complexity, bridging object-relational impedance mismatch, handling concurrency, organizing web presentation, and managing distributed systems.

The patterns organize into categories: Domain Logic (Transaction Script, Domain Model, Service Layer), Data Source (Repository, Active Record, Data Mapper, Unit of Work), Object-Relational Mapping (Identity Map, Lazy Load, inheritance mapping), Web Presentation (MVC, Front Controller, Template View), Distribution (Remote Facade, DTO), and Concurrency (Optimistic/Pessimistic Offline Lock). While originally published in 2002, these patterns remain relevant in 2025 because they address architectural fundamentals, not implementation details. Modern frameworks (Spring, .NET Core, Django) implement many patterns internally, but understanding the underlying patterns enables better architecture decisions and prevents common pitfalls.

## When to Use

- Building enterprise applications with complex business logic and data persistence
- Designing layered architecture with clear separation between presentation, domain, and data
- Managing object-relational impedance mismatch (objects vs. database tables)
- Coordinating transactions across multiple database operations
- Handling offline concurrency in multi-user business applications
- Refactoring legacy applications with tangled domain logic and data access
- Establishing architectural consistency across large development teams

## The Process

### Step 1: Choose Domain Logic Pattern

Select how to organize business logic based on complexity. This is the foundational decision affecting entire architecture.

**Transaction Script:** Procedural approach - each use case implemented as single procedure. Database-centric, simple to understand, minimal OOP. **Use when:** Simple CRUD operations, straightforward business logic, small team, rapid development. **Example:** E-commerce checkout as single `processCheckout(cart)` function with SQL queries.

**Domain Model:** Object-oriented approach - business logic distributed across rich domain objects with behavior and data. **Use when:** Complex business rules, sophisticated validation, domain-driven design, long-term maintainability. **Example:** E-commerce with `Order`, `LineItem`, `DiscountRule` objects collaborating to calculate totals.

**Table Module:** Hybrid - single class per database table containing all logic for those rows. **Use when:** Moderate complexity, working with record sets (Microsoft ADO.NET), team transitioning from procedural to OO.

**Service Layer:** Establishes application boundary, coordinates domain operations, orchestrates transactions. **Use when:** Exposing operations to multiple clients (web, mobile, API), need transaction boundaries, separating application logic from domain logic. **Always use with Domain Model.** **Example:** `OrderService` with `placeOrder()`, `cancelOrder()` methods coordinating domain objects.

**Decision guide:** Simple CRUD → Transaction Script. Complex domain → Domain Model + Service Layer. Moderate complexity → Table Module.

### Step 2: Select Data Source Architectural Pattern

Choose how domain objects interact with database. This manages object-relational impedance mismatch.

**Active Record:** Domain objects know how to persist themselves - `user.save()`, `order.find(id)`. Simple, rapid development, but couples domain logic to database. **Use when:** Simple domain, one class maps to one table, rapid prototyping. **Rails, Laravel use this.** **Anti-pattern for complex domains.**

**Data Mapper:** Separate layer (repository/mapper) transfers data between domain objects and database. Domain objects have zero knowledge of persistence. **Use when:** Complex domain model, domain-driven design, need to test business logic without database. **Hibernate, Entity Framework, SQLAlchemy use this.**

**Repository:** Collection-like interface for retrieving domain objects - `orderRepository.findByCustomer(customer)`. Abstracts query construction, provides domain-oriented retrieval methods. **Always use with Domain Model.** **Implements Data Mapper pattern.**

**Table Data Gateway:** Gateway object for table operations - one gateway per table. **Row Data Gateway:** Gateway per database row - wraps CRUD for single record.

**Decision guide:** Complex domain → Repository + Data Mapper. Simple domain, rapid development → Active Record. Legacy SQL-centric → Table/Row Data Gateway.

### Step 3: Implement Transaction Management with Unit of Work

Coordinate database writes and transaction boundaries. Unit of Work tracks changes and commits atomically.

**Unit of Work pattern:** Maintains list of objects affected by business transaction, coordinates writing changes, ensures atomic commits. **Prevents partial writes, missing updates, duplicate saves.**

**How it works:** (1) Track new objects (inserts), modified objects (updates), deleted objects (deletes) during transaction. (2) On commit: execute all tracked changes in single database transaction. (3) On rollback: discard all tracked changes.

**Identity Map integration:** Ensures each object loaded only once per transaction - maintains object identity. Prevents update anomalies from multiple in-memory copies of same database row.

**Example:** User updates order, adds line item, applies discount. Unit of Work tracks: 1 update (Order), 1 insert (LineItem), 1 update (Discount). Single `unitOfWork.commit()` writes all changes atomically or none if validation fails.

**Framework support:** Hibernate Session, Entity Framework DbContext, SQLAlchemy Session all implement Unit of Work. Understand the pattern even if framework provides it.

**Manual implementation:** Maintain three collections (new, dirty, deleted), register object changes, generate SQL on commit. Use when framework doesn't provide or need fine-grained control.

### Step 4: Apply Object-Relational Behavioral Patterns

Optimize database access and manage object lifecycle. These patterns improve performance and correctness.

**Lazy Load:** Object doesn't contain all data but knows how to retrieve it. **Four variations:** Lazy initialization (load on first access), virtual proxy (proxy object loads real object), value holder (wrapper with load logic), ghost (partial object that loads full state on access).

**Use when:** Object graphs are large, most use cases don't need all related data, reducing initial query complexity. **Example:** Loading `Order` doesn't automatically load all `LineItems` - loaded on `order.getLineItems()` call.

**Identity Map:** Cache of loaded objects keyed by ID - ensures single instance per database row per transaction. **Prevents:** Update anomalies, redundant queries, memory waste. **Example:** Two parts of code load `User(id=123)` - Identity Map returns same object instance, ensuring changes are seen by both.

**Query Object:** Represents database query as object rather than string. Enables query composition, type safety, encapsulation. **Example:** Criteria API, LINQ, QueryDSL. Build query incrementally: `repository.findOrders().where(status='PENDING').olderThan(30.days).orderBy('created')`.

**Practical advice:** Use Lazy Load for optional relationships. Always use Identity Map (most ORMs provide). Use Query Object for complex, dynamic queries.

### Step 5: Choose Web Presentation Pattern

Organize web layer to separate presentation from domain logic. Pattern choice affects maintainability and testing.

**Model View Controller (MVC):** Separates domain logic (Model), presentation (View), and input handling (Controller). **Most common web pattern.** **Use when:** Complex UI logic, multiple views of same data, need testability.

**Page Controller:** One controller per page/action - `CheckoutController`, `ProfileController`. Simple, maps to URLs naturally. **Use when:** Simple web apps, traditional request-response flow. **Examples:** Spring MVC, ASP.NET MVC, Rails controllers.

**Front Controller:** Single controller handles all requests, routes to appropriate handlers. Centralizes common logic (authentication, logging). **Use when:** Complex routing, shared preprocessing, API gateways. **Examples:** Express.js middleware, Servlet filters, Django middleware.

**Template View:** Embed markers in HTML templates - `{{user.name}}`, `<%= order.total %>`. **Use when:** Designers work with HTML, simple rendering. **Examples:** ERB, Handlebars, Jinja2, Razor.

**Transform View:** Process domain data element-by-element transforming to HTML (XSLT-style). **Use when:** Complex transformations, separating data structure from presentation. **Less common in modern web.**

**Two Step View:** First transform domain to logical page, then logical page to HTML. Enables consistent styling, easy skin changes. **Use when:** Multiple themes, complex common layouts.

**Decision guide:** Most web apps → MVC + Page Controller + Template View. Complex SPA → Front Controller + API. Need centralized request processing → Front Controller.

## Example Application

**Situation:** Building insurance claims processing system. Complex business rules (policy validation, claim eligibility, fraud detection), multi-user concurrent access, needs transaction integrity, expected 10-year lifespan.

**Step 1 - Domain Logic:** Selected **Domain Model + Service Layer**. Complex rules require rich objects (`Policy`, `Claim`, `ClaimRule`, `FraudDetector`). Service Layer (`ClaimProcessingService`) provides transaction boundaries and coordinates domain operations.

**Step 2 - Data Source:** Selected **Repository + Data Mapper**. Domain model has no persistence knowledge. `ClaimRepository` with methods `findPendingClaims()`, `findByPolicyNumber()`. Data Mapper (ORM) handles object-to-table mapping. Active Record rejected - couples domain to database.

**Step 3 - Transaction:** Implemented **Unit of Work**. Processing claim involves: update Claim status, create Payment, update Policy, log Audit. Unit of Work ensures atomic commit - all succeed or all rollback. Identity Map prevents loading same Claim twice in transaction.

**Step 4 - Optimization:** Used **Lazy Load** for Claim.attachments (large files, not always needed). **Query Object** for dynamic claim searches (by date range, status, policy type, fraud score). Identity Map provided by ORM.

**Step 5 - Web Layer:** Selected **MVC + Front Controller + Template View**. Front Controller handles authentication, logging, error handling. Page Controllers per feature (`ClaimSubmissionController`, `ClaimReviewController`). Template View for adjuster UI.

**Outcome:** Clean architecture - domain logic testable without database (77% test coverage). Transaction integrity - zero partial updates in production. Performance - Lazy Load reduced initial query time 60%. Maintainability - added new claim types without modifying existing code (Open-Closed Principle).

## Anti-Patterns

- ❌ Using Domain Model for simple CRUD - over-engineering, use Transaction Script
- ❌ Active Record with complex domain - tight coupling prevents testing and violates SRP
- ❌ Bypassing Unit of Work with direct SQL - creates partial write bugs
- ❌ Not using Identity Map - update anomalies from multiple in-memory copies of same row
- ❌ Eager loading everything - performance killer, use Lazy Load strategically
- ❌ Putting business logic in controllers - should be in domain layer, controllers orchestrate only
- ❌ Applying all patterns at once - start simple, add patterns as complexity demands
- ❌ Pattern dogma over pragmatism - patterns solve problems, not goals themselves

## Related

- domain-driven-design (strategic approach using many enterprise patterns)
- clean-architecture (architectural framework incorporating enterprise patterns)
- repository-pattern (specific data access pattern)
- unit-of-work-pattern (transaction coordination)
- service-layer-pattern (application boundary)
- mvc-pattern (web presentation)
- active-record-pattern (simple data access)
- orm-frameworks (implement many patterns)
