---
name: mvc-pattern
description: Separate user interface logic into Model (data), View (presentation), and Controller (input handling) for maintainable, testable GUI applications
---

# Model-View-Controller (MVC)

## Overview

Model-View-Controller is a foundational architectural pattern for user interfaces that divides program logic into three interconnected components: Model (business logic and data), View (presentation and display), and Controller (input handling and coordination). Originally developed by Trygve Reenskaug for Smalltalk in the late 1970s, MVC became widely adopted across web frameworks (Rails, Django, ASP.NET), desktop applications, and mobile development.

Martin Fowler codified MVC in "Patterns of Enterprise Application Architecture" (2003) as a pattern where an input controller receives requests, sends messages to model objects, takes responses, and passes them to views for display. The core principle is Separated Presentation - keeping presentation objects distinct from domain model objects. This separation enables independent evolution of UI and business logic, improves testability by isolating concerns, and allows multiple views of the same data.

## When to Use

- Building user interfaces with complex business logic that must be tested independently
- Applications requiring multiple views of the same data (desktop + mobile + API)
- Web applications needing clear separation between routing, business logic, and templates
- Teams with specialized roles (frontend, backend, domain experts) working in parallel
- Systems where UI frequently changes but business rules remain stable
- Retrofitting testability into legacy GUI applications
- Frameworks that enforce MVC conventions (Rails, Django, Spring MVC)

## The Process

### Step 1: Define the Model - Business Logic and Data

The Model represents domain concepts, business rules, and data. It has no knowledge of views or controllers.

**Ask:** "What are the core business entities and their rules? What data needs to persist?"

**Implementation:** Create classes for domain objects (User, Product, Order) with business logic methods. Models notify observers of state changes but don't render UI.

**Example:** `OrderModel` calculates totals, validates inventory, enforces business rules. Exposes `getTotal()`, `addItem()`, `validatePayment()` - no HTML/UI code.

### Step 2: Build the View - Presentation Layer

The View displays data from the Model. It observes Model changes and updates display. Contains no business logic.

**Ask:** "How should this data appear to users? What formatting and layout are needed?"

**Implementation:** Create templates, HTML, or UI components that render Model data. Views subscribe to Model change events for automatic updates.

**Example:** `OrderView` renders order items as HTML table, displays total. When Model updates, View refreshes automatically. No calculation logic - purely presentation.

### Step 3: Implement the Controller - Input Coordinator

The Controller handles user input, updates Models, and selects Views to render. It's the "glue" coordinating Models and Views.

**Ask:** "What user actions are possible? How do inputs translate to Model changes and View updates?"

**Implementation:** Map user actions (button clicks, HTTP requests) to Controller methods. Controller invokes Model methods, then tells View what to render.

**Example:** `OrderController.addItem(productId)` receives user action, calls `OrderModel.addItem()`, selects `OrderView` to display updated order. Routes `/orders/:id` to `OrderController.show()`.

### Step 4: Establish Communication Flow

Connect the three components following MVC communication rules.

**Flow:** User interacts with View → Controller handles input → Controller updates Model → Model notifies observers → View updates display.

**Implementation:** Use observer pattern for Model-View communication. Controller directly calls Model methods and explicitly selects Views.

**Example:** User clicks "Add to Cart" → `OrderController.addToCart()` → Updates `OrderModel` → Model fires `orderChanged` event → `OrderView` listens, re-renders cart display.

### Step 5: Maintain Separation of Concerns

Enforce boundaries: Models know nothing of Views/Controllers, Views know Models but not Controllers, Controllers know both.

**Validation:** Can you test Model business logic without any UI? Can you swap View implementations without changing Model? Can you change routing without touching business rules?

**Refactoring:** If Model has HTML generation, move to View. If View has calculations, move to Model. If business logic is in Controller, move to Model.

## Example Application

**Situation:** E-commerce product catalog with web interface, mobile app, and REST API - all displaying the same inventory data with different presentations.

**Application of MVC:**
- **Model:** `ProductCatalog` manages inventory, pricing rules, search logic. `Product` entities with SKU, price, stock validation. Notifies observers when inventory changes.
- **View:** `WebProductView` renders HTML grid, `MobileProductView` optimizes for touch, `JSONProductView` serializes for API. All observe same `ProductCatalog` Model.
- **Controller:** `ProductController` handles search requests, filters, sort orders. Routes `/products/search?q=laptop` to `searchAction()`, updates Model with query, selects appropriate View (HTML vs JSON based on Accept header).

**Outcome:** Business logic tested independently (Model unit tests). Design team iterated UI rapidly without touching business rules. API and web UI share 100% of domain code. Mobile team joined later - reused Models, built new Views/Controllers.

## Anti-Patterns

- "Fat Controllers" with business logic - violates separation, makes testing harder (move to Model)
- Models importing View libraries - breaks independence, creates circular dependencies
- Views performing calculations or data manipulation - pollutes presentation layer (move to Model)
- Direct View-to-View communication bypassing Controller - creates hidden dependencies
- Treating MVC as strict dogma when simpler patterns suffice (over-engineering small apps)
- Controllers directly manipulating View internals rather than passing data
- Models with no observers - defeats automatic View updates, requires manual refresh
- Confusing MVC with similar patterns (MVP, MVVM) - understand the differences

## Related

- mvvm-pattern (evolution adding data binding and ViewModel)
- hexagonal-architecture (ports and adapters, similar separation)
- clean-architecture (extends MVC principles to system architecture)
- observer-pattern (mechanism for Model-View communication)
- separation-of-concerns (underlying design principle)
- dependency-injection (for wiring Controllers and Models)
