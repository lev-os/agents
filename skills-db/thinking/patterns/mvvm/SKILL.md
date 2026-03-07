---
name: mvvm
description: Build reactive user interfaces by binding Views to ViewModels that expose observable state and commands, separating UI from presentation logic
---

# MVVM (Model-View-ViewModel)

## Overview

MVVM (Model-View-ViewModel) is a software architectural pattern that extends MVC specifically for modern UI frameworks with data binding capabilities. Introduced by Microsoft architects John Gossman and Ken Cooper in 2005 for Windows Presentation Foundation (WPF), MVVM addresses a critical limitation of MVC: the need to manually synchronize UI state with underlying data. The pattern separates UI (View) from presentation logic (ViewModel) from domain logic (Model), enabling declarative, reactive user interfaces where UI automatically updates when data changes.

The key innovation is the ViewModel layer - a presentation model that exposes observable properties and commands for Views to bind to. When ViewModel state changes, bound Views automatically update without manual DOM manipulation or UI code. This bidirectional binding dramatically reduces boilerplate while maintaining testability - ViewModels contain zero UI dependencies and can be tested as pure logic. Originally designed for desktop apps, MVVM has become dominant in mobile development (Android Jetpack, SwiftUI) and modern web frameworks (Vue, Angular, Knockout).

## When to Use

- Building applications with complex, stateful UIs requiring frequent updates
- Mobile app development on Android (ViewModel + LiveData/Flow) or iOS (SwiftUI)
- Web applications using reactive frameworks (Vue, Angular, Blazor)
- Projects requiring comprehensive UI testing without running actual UI
- Forms-heavy applications with extensive validation and real-time feedback
- Dashboards or data visualization apps with frequently changing data
- When your UI framework provides native data binding capabilities

## The Process

### Step 1: Define Models - Domain Logic and Data

Create Model classes representing business entities and domain logic, completely independent of UI concerns.

**Ask:** "What are my core domain objects and business rules?"

**Implementation:**
- Build domain entities (User, Product, Order, etc.) with business logic
- Define data access interfaces (repositories, API clients)
- Encapsulate business rules and validations
- Ensure Models have no knowledge of ViewModels or Views

**Example:** `UserRepository` class with `getUser(id)`, `updateUser(user)`, `validateEmail(email)` methods - pure domain logic

### Step 2: Create ViewModels - Presentation Logic and Observable State

Build ViewModel classes that expose observable properties and commands for Views to bind to. ViewModels translate Model data into UI-friendly formats.

**Ask:** "What state does the UI need? What user actions must I handle?"

**Implementation:**
- Create ViewModel class for each View (screen or major component)
- Expose observable properties for all UI-bound data (text, visibility, enabled state)
- Implement commands/methods for user actions (button clicks, form submissions)
- Call Model methods to execute business logic
- Transform Model data into UI-appropriate formats (dates, currency, etc.)
- NO direct UI manipulation or framework-specific code

**Example:** `UserProfileViewModel` with observable properties `userName`, `email`, `isLoading`, `errorMessage` and commands `updateProfile()`, `changePassword()`

### Step 3: Build Views - Declarative UI with Data Binding

Create Views that declaratively bind to ViewModel properties and commands - no manual DOM manipulation or state synchronization.

**Ask:** "How do I bind UI elements to ViewModel state?"

**Implementation:**
- Define UI structure (XAML, XML layouts, JSX, template syntax)
- Bind input elements to ViewModel properties (two-way binding)
- Bind display elements to ViewModel state (one-way binding)
- Bind user actions (clicks, submissions) to ViewModel commands
- Let the framework handle synchronization automatically
- Views contain NO business logic or state management

**Example (Android):**
```xml
<TextView text="@{viewModel.userName}" />
<Button onClick="@{() -> viewModel.updateProfile()}" enabled="@{!viewModel.isLoading}" />
```

### Step 4: Establish Reactive Data Flow

Wire ViewModels to Models and Views to ViewModels using observable patterns - changes propagate automatically.

**Ask:** "How do state changes flow from Model to UI and back?"

**Data Flow:**
1. **User Input → ViewModel:** View binds input to ViewModel property, framework updates property on change
2. **ViewModel → Model:** ViewModel calls Model methods with updated data
3. **Model → ViewModel:** Model returns results, ViewModel updates observable properties
4. **ViewModel → View:** Framework detects property changes, automatically updates bound UI elements

**Example:** User edits email field → `email` property updates → ViewModel validates and calls `UserRepository.updateEmail()` → updates `isLoading` and `errorMessage` observables → UI automatically shows loading spinner and error messages

### Step 5: Implement Lifecycle Awareness (Mobile)

On mobile platforms, make ViewModels lifecycle-aware to survive configuration changes (screen rotation) and clean up resources.

**Ask:** "How do I preserve state across lifecycle events?"

**Mobile-Specific Concerns:**
- **Android:** Use `ViewModel` base class (Jetpack) - survives rotation automatically
- **iOS:** Use `@StateObject` or `@ObservedObject` (SwiftUI) for lifecycle management
- Clear subscriptions/listeners in ViewModel cleanup methods
- Store persistent state in Models, transient UI state in ViewModels

**Example (Android):** Extend `androidx.lifecycle.ViewModel`, override `onCleared()` to cancel coroutines and release resources

### Step 6: Test ViewModels Independently

Write comprehensive tests for ViewModels without touching UI framework - pure logic testing.

**Testing Strategy:**
- Mock Model dependencies (repositories, services)
- Set ViewModel properties and call commands
- Assert observable state changes correctly
- Verify Model methods called with correct parameters
- Test edge cases, error handling, validation logic

**Example:** Test `UserProfileViewModel.updateProfile()` with invalid email → assert `errorMessage` observable contains validation error, `isLoading` is false, `UserRepository.updateUser()` never called

## Example Application

**Situation:** Building an Android e-commerce app with complex product filtering, real-time price updates, and shopping cart management - traditional manual UI updates becoming unmaintainable.

**Application of MVVM:**

**Models:**
- `ProductRepository`: Fetches products from API, manages caching
- `CartManager`: Maintains shopping cart state, calculates totals
- `PriceService`: Provides real-time price updates via WebSocket

**ViewModels:**
- `ProductListViewModel`: Exposes `products` (LiveData<List<Product>>), `isLoading`, `filters`, `applyFilter()` command
  - Calls `ProductRepository.getProducts(filters)` when filters change
  - Updates `products` observable when data arrives
  - UI automatically re-renders product list

- `CartViewModel`: Exposes `cartItems`, `total`, `itemCount`, `addToCart(productId)`, `removeItem(itemId)` commands
  - Calls `CartManager.addItem()`, updates `cartItems` and `total` observables
  - UI (cart icon badge, total display) updates automatically

- `ProductDetailViewModel`: Exposes `product`, `currentPrice` (updates from PriceService), `addToCart()` command
  - Subscribes to `PriceService.observePrice(productId)`, updates `currentPrice` observable
  - Price changes propagate to UI in real-time without manual updates

**Views (XML Layouts):**
- Bind RecyclerView to `viewModel.products`, loading spinner to `viewModel.isLoading`
- Bind cart badge count to `viewModel.itemCount`, total to `viewModel.total`
- Bind "Add to Cart" button click to `viewModel.addToCart()` command

**Outcome:** Zero manual UI updates - change ViewModel observables, UI automatically synchronizes. Comprehensive ViewModel testing without running Android emulator. Survives screen rotation preserving filter state and cart contents.

## Common Pitfalls

**Fat ViewModels:** ViewModels containing business logic that belongs in Models - leads to duplication and difficult testing. **Fix:** Keep ViewModels focused on presentation concerns, delegate domain logic to Models.

**UI Logic in ViewModels:** ViewModels directly manipulating UI elements or importing UI framework types - breaks testability. **Fix:** Use observable properties and let Views bind declaratively.

**Anemic Models:** All logic in ViewModels, Models reduced to data containers - wastes architectural benefits. **Fix:** Rich domain Models with business logic, ViewModels translate for UI.

**Over-Observability:** Making every field observable when it never changes - performance overhead. **Fix:** Only observable properties that actually change and affect UI.

**Not Handling Lifecycle:** ViewModels leaking memory by not cleaning up subscriptions/listeners. **Fix:** Use lifecycle-aware components, clean up in `onCleared()` or equivalent.

**Bidirectional Binding Loops:** Two-way bindings creating infinite update loops. **Fix:** Careful binding design, use events/commands for user actions instead of property setters where appropriate.

## Key Insights

**Testing Superiority:** ViewModels are pure Kotlin/Swift/C# classes with zero Android/iOS/WPF dependencies - test at full speed with JUnit/XCTest, no UI framework required. This is MVVM's killer feature.

**Boilerplate Reduction:** Eliminate thousands of lines of manual `findViewById()`, `setText()`, `setOnClickListener()` code - framework handles synchronization automatically through bindings.

**State Preservation:** Mobile ViewModels survive configuration changes (rotation) automatically - no manual state save/restore in `onSaveInstanceState()`.

**Not Universal:** MVVM requires framework support for data binding. Without it (vanilla JavaScript, React without additional libraries), the pattern adds complexity without benefit - use simpler patterns.

**Evolution of MVC:** MVVM solves MVC's manual synchronization problem but introduces new concerns (binding complexity, debugging difficulty). Right tool for reactive UIs, overkill for simple screens.

**Performance Considerations:** Observable patterns and binding frameworks have overhead - for performance-critical UIs (games, animations), manual optimization may be needed despite MVVM benefits.

## Related Patterns

- **MVC (Model-View-Controller):** MVVM's ancestor - manual synchronization instead of automatic binding
- **MVP (Model-View-Presenter):** Alternative to MVVM with Presenter mediating all View interactions
- **Clean Architecture:** Often combined with MVVM - ViewModels call Use Cases instead of Models directly
- **Repository Pattern:** Used within Models to abstract data sources from ViewModels
- **Observer Pattern:** Foundation of MVVM's reactive data flow
- **Command Pattern:** ViewModels expose commands for user actions instead of direct method calls
