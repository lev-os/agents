---
name: solid-principles
description: Write maintainable object-oriented code by following five design principles - Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
---

# SOLID Principles

## Overview

SOLID is a mnemonic for five foundational object-oriented design principles introduced by Robert C. Martin (Uncle Bob) in 2000, with the acronym coined by Michael Feathers. These principles make source code more understandable, flexible, and maintainable by reducing dependencies and coupling. Uncle Bob, author of Clean Code and Clean Architecture, emphasized that SOLID enables engineers to change one area of software without impacting others - the essence of modularity.

The five principles form a comprehensive framework: Single Responsibility (one reason to change), Open-Closed (extend without modifying), Liskov Substitution (subtype replaceability), Interface Segregation (no forced dependencies), and Dependency Inversion (depend on abstractions). Together, they guide developers toward designs that accommodate change gracefully rather than becoming brittle over time.

## When to Use

- Designing class structures and module boundaries in object-oriented systems
- Refactoring legacy code with tight coupling and unclear responsibilities
- Code reviews to evaluate design quality and maintainability
- Preventing "shotgun surgery" where one change requires modifying many classes
- Building systems expected to evolve over years with changing requirements
- Teaching object-oriented design principles to teams
- Diagnosing why code is difficult to test, extend, or understand

## The Process

### Step 1: Single Responsibility Principle (SRP) - One Reason to Change

Each class should have only one responsibility - one reason to change. If a class has multiple responsibilities, changes to one responsibility affect the others.

**Ask:** "What is this class's single job? Does it have more than one reason to change?"

**Example violation:** `UserManager` class that handles authentication, database persistence, email notifications, and logging - four reasons to change.

**Fix:** Split into `Authenticator`, `UserRepository`, `EmailNotifier`, `Logger` - each with one responsibility.

### Step 2: Open-Closed Principle (OCP) - Open for Extension, Closed for Modification

Software entities should be open for extension but closed for modification. Add new functionality by adding code, not changing existing code.

**Ask:** "Can I add new behavior without modifying existing classes?"

**Example violation:** Switch statement checking payment types (credit, debit, crypto) - adding new type requires modifying switch.

**Fix:** Use polymorphism - `PaymentProcessor` interface with `CreditCardProcessor`, `DebitCardProcessor`, `CryptoProcessor` implementations. New payment types extend without modifying existing code.

### Step 3: Liskov Substitution Principle (LSP) - Subtype Replaceability

Objects should be replaceable with instances of their subtypes without altering program correctness. Subtypes must honor the parent type's contract.

**Ask:** "Can I substitute a subclass anywhere the parent class is used without breaking behavior?"

**Example violation:** `Rectangle` class with `setWidth()` and `setHeight()`. `Square` subclass overrides both to maintain square constraint - violates substitution because `Rectangle` users expect independent width/height.

**Fix:** Don't make `Square` inherit from `Rectangle` - they have different invariants. Use composition or separate hierarchies.

### Step 4: Interface Segregation Principle (ISP) - No Forced Dependencies

Clients should not be forced to depend on interfaces they don't use. Large interfaces create unnecessary coupling.

**Ask:** "Does this interface force implementers to provide methods they don't need?"

**Example violation:** `Worker` interface with `work()`, `eat()`, `sleep()` - forces `RobotWorker` to implement `eat()` and `sleep()` with no-ops.

**Fix:** Split into `Workable`, `Eatable`, `Sleepable` interfaces. `HumanWorker` implements all three, `RobotWorker` implements only `Workable`.

### Step 5: Dependency Inversion Principle (DIP) - Depend on Abstractions

High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details.

**Ask:** "Do my high-level components depend on concrete low-level implementations?"

**Example violation:** `OrderProcessor` directly instantiates `MySQLDatabase` - tightly coupled to specific database.

**Fix:** `OrderProcessor` depends on `IDatabase` interface. `MySQLDatabase`, `PostgreSQLDatabase`, `MongoDatabase` all implement `IDatabase`. Inject the dependency.

## Example Application

**Situation:** E-commerce payment processing system becoming unmaintainable - every new payment method requires changing multiple files.

**Application of SOLID:**
- **SRP:** Separated `PaymentProcessor` (orchestration), `PaymentValidator` (validation logic), `PaymentLogger` (audit trail), `PaymentNotifier` (customer emails)
- **OCP:** Created `IPaymentMethod` interface - new payment types extend without modifying existing code
- **LSP:** All payment implementations (`CreditCard`, `PayPal`, `Crypto`) honor `IPaymentMethod` contract - can be substituted without breaking checkout flow
- **ISP:** Split fat `IPaymentMethod` interface into `IPayable`, `IRefundable`, `IRecurringBillable` - one-time payment methods don't implement recurring billing
- **DIP:** `PaymentProcessor` depends on `IPaymentMethod` abstraction, not concrete payment classes - injected via constructor

**Outcome:** Adding ApplePay required creating one new class implementing `IPaymentMethod` - zero changes to existing code. Testing improved (mock interfaces easily). Team velocity increased 3x for payment features.

## Anti-Patterns

- ❌ Applying SOLID dogmatically to simple code that doesn't need it (over-engineering)
- ❌ Creating unnecessary abstraction layers "just in case" (YAGNI violation)
- ❌ Splitting classes so granularly that understanding requires navigating 50 files
- ❌ Using SOLID as checklist without understanding the "why" behind each principle
- ❌ Ignoring SRP but over-applying OCP (common imbalance)
- ❌ Creating "do-nothing" interface implementations to satisfy ISP (indicates poor interface design)
- ❌ Treating SOLID as rules rather than guidelines for reducing coupling

## Related

- clean-architecture (architectural application of SOLID)
- dependency-injection (DIP implementation pattern)
- composition-over-inheritance (alternative to LSP violations)
- interface-design (foundation for ISP and DIP)
- refactoring-patterns (how to move toward SOLID from legacy code)
