---
name: domain-driven-design
description: Model complex software to match the problem domain by building ubiquitous language with domain experts and organizing code into bounded contexts
---

# Domain-Driven Design (DDD)

## Overview

Domain-Driven Design (DDD) is a strategic software design approach introduced by Eric Evans in his 2003 book, focusing on modeling software to match the problem domain according to input from domain experts. The core insight: for complex domains, technical patterns matter less than deeply understanding the business problem and embedding domain terminology directly into software systems.

At its heart, DDD advocates that domain experts and developers must share a common language - the ubiquitous language - which becomes embedded in code structure, variable names, and conversations. This shared language lives within bounded contexts (logical boundaries where a particular domain model is consistent). DDD introduces tactical patterns (entities, value objects, aggregates) and strategic patterns (bounded contexts, context mapping) to manage complexity in the heart of software.

## When to Use

- Complex business domains with intricate rules and logic (finance, healthcare, logistics)
- Multiple domain experts with deep knowledge separate from development team
- Systems where technical debt accumulates from domain/code mismatch
- Microservices architecture requiring clear domain boundaries
- Legacy systems where business logic is scattered and unclear
- Projects where business rules change frequently and developers struggle to keep up
- Cross-functional teams need shared understanding between business and engineering

## The Process

### Step 1: Collaborate with Domain Experts to Build Ubiquitous Language

Work with domain experts to create shared terminology that both business and developers use consistently. This language must be precise and embedded everywhere.

**Example (e-commerce):** Don't say "user" and "customer" interchangeably. Define: "Customer" = someone who has purchased, "Visitor" = browsing, "Account" = registered profile. Use these terms in code: `class Customer`, `customer.purchaseHistory()`.

**Process:** Workshops, event storming sessions, glossary documentation, code reviews checking language consistency.

### Step 2: Identify Bounded Contexts - Logical Domain Boundaries

Define areas where a particular domain model is consistent and valid. Different contexts may have different models for the same concept.

**Example:** In "Sales" context, "Customer" includes payment methods and purchase history. In "Support" context, "Customer" includes ticket history and SLA tier. These are different models with different responsibilities - separate bounded contexts.

**Boundaries prevent:** Global models that try to serve all contexts and become bloated and inconsistent.

### Step 3: Model Domain Objects - Entities, Value Objects, Aggregates

Classify domain concepts based on their characteristics:

**Entities:** Objects with distinct identity and lifecycle (Customer, Order, Product)
- Identity matters: Customer #12345 is not the same as Customer #67890 even if names match
- Mutable: Customer address can change but remains the same Customer

**Value Objects:** Defined only by attributes, no identity (Address, Money, DateRange)
- Immutable: If amount changes, create new Money object
- Replaceable: Two Money(100, USD) objects are interchangeable

**Aggregates:** Clusters of entities/value objects treated as single unit with root entity
- Example: Order (root) contains LineItems (entities) and ShippingAddress (value object)
- All access to LineItems goes through Order - maintains consistency

### Step 4: Define Aggregate Roots and Consistency Boundaries

Each aggregate has a root entity that enforces invariants. External objects can only reference the root.

**Example:** Order aggregate with LineItems. Rule: "Total line items cannot exceed $10,000."
- External code calls `order.addLineItem(item)` not `lineItem.setQuantity()`
- Order (root) validates total before adding item - consistency guaranteed

### Step 5: Map Context Relationships - How Bounded Contexts Interact

Define how contexts integrate: Shared Kernel (shared code), Customer-Supplier (upstream/downstream), Anti-Corruption Layer (translation between contexts).

**Example:** Sales context (upstream) publishes `OrderPlaced` events. Support context (downstream) translates via Anti-Corruption Layer: `OrderPlaced.customerId` → `SupportTicket.accountReference`. Support doesn't adopt Sales' customer model.

### Step 6: Align Code Structure with Domain Model

Package code by domain concepts, not technical layers. Ubiquitous language should be visible in file structure.

**Not:** `/controllers`, `/services`, `/models` (technical layers)
**Instead:** `/sales/customer`, `/sales/order`, `/support/ticket` (domain concepts)

## Example Application

**Situation:** Insurance company's policy management system - developers couldn't keep up with business rule changes, bugs in premium calculations.

**Application of DDD:**
- **Ubiquitous Language:** Worked with underwriters to define precise terms - "Policy," "Endorsement," "Rider," "Premium," "Underwriting," "Risk Assessment" - embedded in code
- **Bounded Contexts:** Identified "Underwriting" (risk assessment), "Policy Administration" (lifecycle management), "Claims" (payout processing) - separated contexts
- **Domain Objects:** Policy (entity with identity), Premium (value object - immutable calculation), PolicyAggregate (root enforcing "no coverage gaps" invariant)
- **Context Mapping:** Underwriting context (upstream) publishes `PolicyApproved` event → Policy Administration creates policy record
- **Code Structure:** Reorganized from technical layers to `/underwriting`, `/policy-administration`, `/claims`

**Outcome:** Business rule changes went from 3-week development cycles to same-day updates (change isolated to specific domain module). Defect rate dropped 60% (invariants enforced at aggregate roots). New developers understood domain in days instead of months.

## Anti-Patterns

- ❌ Using DDD for simple CRUD applications (over-engineering - use basic MVC)
- ❌ Creating single ubiquitous language across entire system (ignores bounded contexts)
- ❌ Letting technical concerns leak into domain model (persistence, UI logic in domain classes)
- ❌ Treating DDD patterns as cargo cult - applying entities/aggregates without domain expert collaboration
- ❌ Neglecting ubiquitous language consistency - developers and business using different terms
- ❌ Making every object an entity (identity isn't always meaningful - use value objects)
- ❌ Organizing code by technical layers instead of domain concepts

## Related

- bounded-context (strategic DDD pattern for domain boundaries)
- ubiquitous-language (shared vocabulary between business and engineering)
- event-storming (collaborative domain modeling workshop technique)
- hexagonal-architecture (isolating domain logic from technical concerns)
- microservices (often aligned with bounded contexts)
