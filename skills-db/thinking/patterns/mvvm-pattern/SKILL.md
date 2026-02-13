---
name: mvvm-pattern
description: Separate UI from business logic using Model (data), View (UI markup), and ViewModel (presentation logic with data binding) for testable, reactive applications
---

# Model-View-ViewModel (MVVM)

## Overview

Model-View-ViewModel is an architectural pattern designed for modern UI frameworks with data binding capabilities, enabling automatic synchronization between UI and application state. Introduced by John Gossman (Microsoft WPF/Silverlight architect) in 2005, MVVM evolved from MVC to leverage declarative data binding in frameworks like WPF, Angular, Vue, SwiftUI, and Jetpack Compose. The pattern eliminates most "glue code" that manually updates UI when data changes.

The three components are: Model (business logic and data sources), View (UI markup with binding expressions), and ViewModel (presentation logic that exposes bindable properties and commands). The key differentiator from MVC is the ViewModel - a "value converter" that shapes Model data for View consumption and handles View logic without knowing View implementation details. Two-way data binding keeps View and ViewModel synchronized automatically, enabling reactive UIs where changes propagate instantly.

## When to Use

- Frameworks with robust data binding (WPF, Xamarin, Angular, Vue, SwiftUI, Jetpack Compose)
- Applications with complex UI state requiring synchronization across multiple components
- Teams needing high testability - ViewModel can be unit tested without UI
- "Massive View Controller" problems where presentation logic bloats UI code
- Desktop/mobile apps with frequent UI changes but stable business logic
- Real-time dashboards where data updates must reflect instantly in UI
- Cross-platform development sharing ViewModels across iOS/Android
- Separating UI designers (working in markup) from developers (writing ViewModels)

## The Process

### Step 1: Define the Model - Business Logic Layer

The Model represents domain entities, data access, and business rules. Identical to MVC - no UI dependencies.

**Ask:** "What are the core business entities? Where does data come from (API, database, cache)?"

**Implementation:** Create domain classes with business logic. Models expose data but don't know about ViewModels or Views. Use repositories/services for data access.

**Example:** `UserModel` with `getUserProfile(id)`, `validateEmail(email)`, `updatePassword(old, new)`. Returns domain objects. No UI-specific formatting.

### Step 2: Create the ViewModel - Presentation Logic

ViewModel exposes data and operations the View needs, converting Model data to View-friendly formats. Contains presentation logic, validation, and commands.

**Ask:** "What data does the View need to display? What actions can users perform? How should Model data be formatted?"

**Implementation:** Expose observable properties (React state, Vue reactive, SwiftUI @Published). Implement commands/methods for user actions. Transform Model data for display.

**Example:** `UserProfileViewModel` exposes `fullName` (computed from firstName + lastName), `isEmailValid` (bool for validation state), `saveProfileCommand` (triggered by Save button). Updates when Model changes.

### Step 3: Build the View - UI Markup with Data Binding

View is declarative markup (XAML, HTML, SwiftUI) that binds to ViewModel properties. Contains no logic - only bindings and layout.

**Ask:** "How should ViewModel data be rendered? What UI controls map to ViewModel properties and commands?"

**Implementation:** Use binding syntax to connect UI elements to ViewModel. Text inputs bind to properties, buttons bind to commands. Framework handles synchronization.

**Example:** `<input v-model="fullName" />` binds to ViewModel `fullName` property. `<button @click="saveProfileCommand">Save</button>` triggers ViewModel method. No JavaScript/Swift code in View - pure markup.

### Step 4: Establish Two-Way Data Binding

Configure automatic synchronization between View and ViewModel using framework binding mechanisms.

**Flow:** User types in input → Framework updates ViewModel property → ViewModel validates/transforms → ViewModel notifies observers → View updates automatically.

**Implementation:** Mark ViewModel properties as observable (INotifyPropertyChanged in C#, @Published in Swift, Vue reactive, React useState). Framework propagates changes bidirectionally.

**Example:** User edits email field → ViewModel `email` property updates → ViewModel runs validation → `isEmailValid` changes → Save button enable/disable state updates automatically.

### Step 5: Implement Commands for User Actions

ViewModel exposes commands (methods) that View invokes for user interactions. Commands encapsulate "what happens when user clicks this."

**Ask:** "What actions can users perform? What business logic should execute?"

**Implementation:** Create command objects or methods that update Model, perform async operations, handle errors. View binds buttons/gestures to commands.

**Example:** `saveProfileCommand` validates inputs, calls `UserModel.updateProfile()`, handles success/error, updates UI state (loading spinner, success message). View just binds button - no code.

### Step 6: Maintain Separation and Testability

ViewModel should have zero View dependencies - no imports of UI frameworks (UIKit, SwiftUI, Android views).

**Validation:** Can you unit test ViewModel without rendering UI? Can you swap View implementations (web → mobile) without changing ViewModel?

**Testing:** Mock Models, instantiate ViewModel, call commands, assert observable properties changed correctly. No UI automation needed.

## Example Application

**Situation:** Social media iOS app with "Massive View Controller" problem - 2000-line view controllers mixing networking, business logic, and UI updates. Difficult to test, frequent bugs in UI state management.

**Application of MVVM:**
- **Model:** `PostRepository` fetches posts from API, caches locally. `Post` entities with like/comment logic. `UserRepository` manages authentication.
- **ViewModel:** `FeedViewModel` exposes `@Published var posts: [PostViewModel]`, `isLoading: Bool`, `refreshCommand`. Each `PostViewModel` has `likePostCommand`, `shareCommand`. Transforms API data to display format (relative timestamps, formatted counts).
- **View:** SwiftUI `FeedView` with `ForEach(viewModel.posts)` binding. `PostView` binds to `PostViewModel` properties. Buttons use `.onTapGesture { viewModel.likePostCommand() }`. Pure declarative UI.

**Outcome:** ViewModel unit tests cover 100% of presentation logic (mock repositories). View reduced to 150 lines of SwiftUI markup. Reused ViewModels for iPad version with different layouts. Bug rate decreased 60% - state synchronization automatic.

## Anti-Patterns

- ViewModel importing View frameworks (UIKit, SwiftUI) - breaks testability and separation
- Business logic in ViewModel instead of Model - ViewModel should orchestrate, not implement
- View directly accessing Model - bypassing ViewModel breaks separation of concerns
- Over-relying on two-way binding for complex state - can create debugging nightmares
- Treating MVVM as silver bullet when MVC suffices - data binding overhead for simple UIs
- "Massive ViewModel" replacing "Massive View Controller" - need to decompose ViewModels too
- Using MVVM in frameworks without data binding - defeats the purpose, use MVC instead
- Tight coupling between specific View and ViewModel - should be reusable across Views

## Related

- mvc-pattern (predecessor pattern without data binding)
- observer-pattern (mechanism for property change notifications)
- data-binding (core enabling technology)
- reactive-programming (RxSwift, Combine, RxJS for advanced MVVM)
- clean-architecture (system-level architecture complementing MVVM)
- presentation-model (Martin Fowler pattern similar to ViewModel)
- unidirectional-data-flow (alternative to two-way binding)
