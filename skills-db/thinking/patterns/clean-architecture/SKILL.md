---
name: clean-architecture
description: Build maintainable systems by organizing code into concentric layers where dependencies point inward, isolating business logic from frameworks and infrastructure
---

# Clean Architecture

## Overview

Clean Architecture is a software architecture philosophy introduced by Robert C. Martin (Uncle Bob) in 2012, synthesizing decades of architectural thinking including Hexagonal Architecture, Onion Architecture, and Ports & Adapters. The core principle: organize code into concentric layers where dependencies flow inward, with business rules at the center completely isolated from frameworks, databases, and UI. The outermost layers (web frameworks, databases) depend on inner layers (business logic), never the reverse - enabling you to defer infrastructure decisions, swap implementations, and test business logic without external dependencies.

The architecture addresses a fundamental problem: most codebases become tightly coupled to frameworks and databases, making them difficult to test, migrate, or evolve. By inverting dependencies through interfaces and dependency injection, Clean Architecture makes your business logic the most stable, tested, and portable part of your system - frameworks and databases become swappable plugins rather than foundational dependencies.

## When to Use

- Building long-lived enterprise applications expected to evolve over decades
- Projects requiring framework/database independence for future migrations
- Systems with complex business rules needing comprehensive automated testing
- Applications with multiple delivery mechanisms (web, mobile, API, CLI)
- When business logic longevity exceeds infrastructure component lifespans
- Teams needing clear architectural boundaries for parallel development
- Projects where business rules must be tested without external dependencies

## The Process

### Step 1: Identify Core Business Entities (Innermost Layer)

Define domain Entities - enterprise-wide business objects with critical business rules. These are the most abstract, stable components.

**Ask:** "What are my fundamental business concepts that would exist even without this application?"

**Implementation:**
- Create entity classes representing core domain concepts (User, Order, Account)
- Encapsulate enterprise business rules as entity methods
- Entities have NO dependencies on frameworks, databases, or outer layers
- Entities change only when fundamental business rules change

**Example:** `Account` entity with `balance` property and `withdraw(amount)` method enforcing overdraft rules - rule exists regardless of database or framework choice

### Step 2: Define Use Cases (Application Business Rules)

Create Use Case classes encapsulating application-specific business logic - orchestrating entity interactions to fulfill user intent.

**Ask:** "What are the specific operations users perform in this application?"

**Implementation:**
- One Use Case class per application operation (RegisterUser, PlaceOrder, TransferFunds)
- Use Cases orchestrate entities and coordinate application flow
- Define interfaces for external dependencies (IDatabase, IEmailService)
- Use Cases depend on Entities but not on outer layers (frameworks, UI, database implementations)

**Example:** `PlaceOrderUseCase` that validates inventory, creates Order entity, calculates total, calls `IPaymentGateway.charge()` interface, updates entities - no direct database or HTTP code

### Step 3: Create Interface Adapters (Controllers, Presenters, Gateways)

Build adapter layer converting between Use Case interfaces and external frameworks/formats.

**Ask:** "How do I translate between my business logic format and external systems?"

**Implementation:**
- **Controllers:** Convert web requests/CLI input to Use Case format, invoke Use Cases
- **Presenters:** Format Use Case output for Views (ViewModel, JSON, HTML)
- **Gateways:** Implement Use Case interfaces (IDatabase, IEmailService) with actual infrastructure
- Adapters depend inward on Use Cases, Use Cases depend only on interfaces

**Example:** `OrderController` receives HTTP POST, validates JSON, calls `PlaceOrderUseCase.execute(orderRequest)`, passes result to `OrderPresenter.formatResponse()`, returns HTTP response

### Step 4: Implement Frameworks & Drivers (Outermost Layer)

Add concrete implementations of frameworks, databases, external services - the most volatile, replaceable components.

**Ask:** "What specific technologies implement my interfaces?"

**Implementation:**
- Database implementations (PostgreSQLOrderRepository implements IOrderRepository)
- Web framework setup (Express routes, FastAPI endpoints)
- External service clients (StripePaymentGateway implements IPaymentGateway)
- UI frameworks (React, Vue, Android Views)
- This layer is swappable - change PostgreSQL to MongoDB without touching Use Cases

**Example:** `PostgreSQLUserRepository` implementing `IUserRepository` interface with SQL queries - swap to `MongoDBUserRepository` or `InMemoryUserRepository` for testing without changing Use Cases

### Step 5: Enforce Dependency Rule - Dependencies Point Inward Only

Wire components with dependency injection, ensuring outer layers depend on inner layers through interfaces.

**Ask:** "Do any inner layer components import or know about outer layer implementations?"

**The Dependency Rule:**
- Source code dependencies point inward: Frameworks → Adapters → Use Cases → Entities
- Inner layers define interfaces, outer layers implement them
- Use Cases depend on `IDatabase` interface (inner), never on `PostgreSQLDatabase` class (outer)
- Inject implementations at runtime through dependency injection containers

**Violation Example:** Use Case importing `import express from 'express'` - breaks independence. **Fix:** Use Case should define `IHttpRequest` interface, Controller (adapter layer) handles Express specifics

### Step 6: Test Business Logic Without External Dependencies

Leverage Clean Architecture's dependency inversion to test Entities and Use Cases with zero infrastructure.

**Testing Strategy:**
- **Entity Tests:** Pure unit tests with no mocks - Entities have no dependencies
- **Use Case Tests:** Mock interface dependencies (IDatabase, IEmailService) with test doubles
- **Adapter Tests:** Test Controllers/Presenters with mocked Use Cases
- **Integration Tests:** Test full stack including real databases in outer layer

**Example:** Test `TransferFundsUseCase` by providing `InMemoryAccountRepository` implementing `IAccountRepository` - no database, no network, millisecond execution

## Example Application

**Situation:** Building a healthcare patient management system requiring HIPAA compliance, expected to run for 20+ years, needing web app, mobile app, and CLI for hospital staff - current framework (Rails) approaching end-of-life but business logic must persist.

**Application of Clean Architecture:**

**Entities (Core):**
- `Patient`: Encapsulates patient demographics, consent rules, data access controls (HIPAA)
- `Appointment`: Scheduling business rules (conflicts, buffer times, cancellation policies)
- `MedicalRecord`: Data ownership, access audit trail requirements

**Use Cases (Application Logic):**
- `ScheduleAppointmentUseCase`: Checks conflicts, validates insurance, creates Appointment, sends notifications
  - Depends on `IPatientRepository`, `IAppointmentRepository`, `INotificationService` interfaces
  - Zero knowledge of PostgreSQL, SendGrid, or web frameworks
- `AccessMedicalRecordUseCase`: Enforces HIPAA authorization, logs access audit trail
- `TransferPatientUseCase`: Coordinates patient transfer between facilities with consent verification

**Interface Adapters:**
- `WebAppointmentController`: Handles HTTP requests, calls `ScheduleAppointmentUseCase`, formats JSON responses
- `CLIAppointmentController`: Parses command-line args, calls same Use Case, outputs table format
- `PostgreSQLPatientRepository`: Implements `IPatientRepository` with SQL queries
- `SendGridNotificationService`: Implements `INotificationService` with email API calls

**Frameworks & Drivers:**
- Web: Next.js framework → routes to WebControllers
- Mobile: React Native → calls WebControllers via API or local Use Cases
- CLI: Node.js script → routes to CLIControllers
- Database: PostgreSQL with pg library
- Email: SendGrid SDK

**Outcome:** Framework migration Rails → Next.js required changing only outermost layer. Use Cases with HIPAA business logic unchanged. Mobile app added without duplicating business logic. Comprehensive Use Case tests run in milliseconds without database. System ready for 20-year lifespan with swappable infrastructure.

## Common Pitfalls

**Leaky Abstractions:** Interfaces exposing implementation details (IDatabase.getPostgreSQLConnection()) instead of domain concepts. **Fix:** Design interfaces around business operations, not technology specifics.

**Anemic Use Cases:** Use Cases as thin pass-throughs to repositories with no orchestration logic - wastes architectural overhead. **Fix:** Use Cases should coordinate multiple entities, enforce policies, handle complex flows.

**Framework Contamination:** Business logic importing framework types (Express Request, Django Model) - defeats independence. **Fix:** Use Cases define framework-agnostic interfaces, adapters translate.

**Over-Abstraction:** Creating interfaces for every single class including unlikely-to-change components. **Fix:** Abstraction at architectural boundaries only - between layers, not within layers.

**Ignoring Practicality:** Applying Clean Architecture to simple CRUD apps - massive overhead for minimal benefit. **Fix:** Reserve for complex, long-lived business logic; simpler patterns for simple apps.

**Testing Neglect:** Building architecture but not leveraging testability - missing the primary benefit. **Fix:** High coverage Use Case tests with mocked interfaces - validate architecture pays off.

## Key Insights

**Framework Independence:** Your business logic outlives any framework. Clean Architecture lets you migrate Express → Fastify → Hono without rewriting Use Cases - 5-10 year ROI.

**Testability Revolution:** Testing business logic without booting a database or web server is 100-1000x faster - enables true TDD with millisecond feedback loops.

**Database as Detail:** Most apps couple to databases early, making migrations painful. Clean Architecture treats database as swappable plugin - defer choice, change PostgreSQL → MongoDB → DynamoDB as needed.

**Architectural Boundaries:** Clear layers enable team parallelization - database team builds repositories, frontend team builds controllers, backend team builds Use Cases simultaneously.

**Not for Everything:** Simple CRUD apps, prototypes, and MVPs suffer under Clean Architecture overhead. Apply to complex business logic expected to survive multiple technology generations.

**Dependency Inversion Principle:** The Dependency Rule is SOLID's Dependency Inversion Principle applied architecturally - depend on abstractions (interfaces), not concretions (implementations).

## Related Patterns

- **Hexagonal Architecture (Ports & Adapters):** Similar concept - business logic at center, adapters at edges
- **Onion Architecture:** Another architectural style with dependency inversion - inspired Clean Architecture
- **SOLID Principles:** Clean Architecture is SOLID applied at system level (especially Dependency Inversion)
- **Domain-Driven Design (DDD):** Often combined - DDD defines Entities and domain model, Clean Architecture structures layers
- **Repository Pattern:** Used in adapter layer to implement data access interfaces defined by Use Cases
- **Dependency Injection:** Mechanism for wiring outer layer implementations to inner layer interfaces
