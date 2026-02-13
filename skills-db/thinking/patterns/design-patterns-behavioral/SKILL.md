---
name: design-patterns-behavioral
description: Manage algorithms, relationships, and responsibilities between objects using eleven behavioral patterns from the Gang of Four
---

# Design Patterns (Behavioral)

## Overview

Behavioral design patterns concern algorithms and the assignment of responsibilities between objects. They describe not just patterns of objects or classes but also the patterns of communication between them. Introduced in the 1994 Gang of Four book "Design Patterns," behavioral patterns characterize complex control flow that's difficult to follow at runtime, shifting focus from flow of control to how objects interconnect.

The eleven behavioral patterns are: Chain of Responsibility (pass requests along chain), Command (encapsulate requests as objects), Interpreter (grammar implementation), Iterator (sequential access), Mediator (centralized communication), Memento (capture and restore state), Observer (notify dependents of changes), State (alter behavior when state changes), Strategy (interchangeable algorithms), Template Method (define algorithm skeleton), and Visitor (add operations without changing classes).

## When to Use

- Decoupling request senders from receivers with multiple potential handlers (Chain of Responsibility)
- Queuing operations, supporting undo/redo, or logging requests (Command)
- Implementing domain-specific languages or expression evaluation (Interpreter)
- Providing uniform traversal without exposing internal structure (Iterator)
- Reducing chaotic dependencies between tightly coupled objects (Mediator)
- Implementing undo mechanisms or checkpointing (Memento)
- Building event-driven systems with one-to-many dependencies (Observer)
- Replacing complex conditional logic based on object state (State)
- Selecting algorithms at runtime (Strategy)
- Defining algorithm structure while allowing step customization (Template Method)
- Adding operations to object structures without modifying them (Visitor)

## The Process

### Step 1: Chain of Responsibility - Pass Request Until Handled

Use when you want to give more than one object a chance to handle a request. Chain receiving objects and pass request along until one handles it.

**Recognize when:** Multiple objects may handle a request, handler isn't known a priori, or you want to issue request without specifying receiver.

**Example:** Logging system with `DebugLogger -> InfoLogger -> ErrorLogger`. Each logger checks if it should handle the log level; if not, passes to next. Request flows until handled or chain ends.

**Structure:** Handler (defines interface, optional successor link) -> ConcreteHandlers (handle or forward)

### Step 2: Command - Encapsulate Request as Object

Use to encapsulate a request as an object, letting you parameterize clients, queue requests, log operations, and support undo.

**Recognize when:** You need to parameterize objects with operations, queue operations, support undo/redo, or log all operations.

**Example:** Text editor with `BoldCommand`, `PasteCommand`, `DeleteCommand`. Each command stores receiver and parameters. Invoker calls `execute()`. Commands stored in history enable undo via `unexecute()`.

**Structure:** Command interface (execute, undo) -> ConcreteCommands | Invoker (triggers commands) | Receiver (performs action)

### Step 3: Iterator - Sequential Access Without Exposing Structure

Use to provide a way to access elements of an aggregate object sequentially without exposing its underlying representation.

**Recognize when:** You need to traverse a collection without exposing its internal structure, or support multiple traversal methods.

**Example:** Tree structure needs depth-first and breadth-first traversal. `DepthFirstIterator` and `BreadthFirstIterator` both implement `Iterator` interface. Client code uses same loop regardless of traversal strategy.

**Structure:** Iterator interface (next, hasNext) -> ConcreteIterators | Aggregate (creates Iterator) -> ConcreteAggregate

### Step 4: Mediator - Centralize Complex Communications

Use to define an object that encapsulates how a set of objects interact. Promotes loose coupling by preventing objects from referring to each other explicitly.

**Recognize when:** Objects communicate in complex ways, reusing objects is difficult due to dependencies, or a behavior distributed across classes should be customizable.

**Example:** Chat room where `User` objects don't reference each other directly. `ChatRoom` mediator handles message routing. Adding broadcast, private messages, or message filtering happens in mediator only.

**Structure:** Mediator interface -> ConcreteMediator (coordinates colleagues) | Colleague (communicates via mediator)

### Step 5: Memento - Capture and Restore State

Use to capture an object's internal state without violating encapsulation, allowing the object to be restored to this state later.

**Recognize when:** You need to save and restore object state (undo), create snapshots, or preserve encapsulation while persisting state.

**Example:** Text editor's `EditorState` memento stores cursor position and content. `Editor` creates mementos before changes. `History` caretaker stores mementos. Undo restores from history stack.

**Structure:** Originator (creates/restores from Memento) | Memento (stores state) | Caretaker (manages Memento storage)

### Step 6: Observer - Notify Dependents of Changes

Use to define one-to-many dependency between objects so when one changes state, all dependents are notified and updated automatically.

**Recognize when:** An abstraction has two aspects with one depending on the other, change to one object requires changing unknown others, or an object should notify others without knowing who they are.

**Example:** Stock price `Subject` notifies `PriceDisplay`, `AlertSystem`, `PortfolioManager` observers. Adding new observer requires no changes to Subject. Used extensively in event-driven UIs.

**Structure:** Subject (attach, detach, notify) | Observer interface (update) -> ConcreteObservers

### Step 7: State - Alter Behavior When Internal State Changes

Use to allow an object to alter its behavior when its internal state changes. Object appears to change its class.

**Recognize when:** Object behavior depends on its state and must change at runtime, or operations have large conditionals depending on state.

**Example:** `TCPConnection` with `ListeningState`, `EstablishedState`, `ClosedState`. Method calls delegate to current state object. State transitions are explicit, eliminates complex switch statements.

**Structure:** Context (maintains State reference) | State interface -> ConcreteStates (implement state-specific behavior)

### Step 8: Strategy - Interchangeable Algorithms

Use to define a family of algorithms, encapsulate each one, and make them interchangeable. Lets algorithm vary independently from clients.

**Recognize when:** You need different variants of an algorithm, or algorithm selection should happen at runtime.

**Example:** `PaymentProcessor` accepts `PaymentStrategy`. `CreditCardStrategy`, `PayPalStrategy`, `CryptoStrategy` encapsulate payment algorithms. Client code unchanged when adding new payment methods.

**Structure:** Context (uses Strategy) | Strategy interface -> ConcreteStrategies (implement algorithm)

### Step 9: Template Method - Define Algorithm Skeleton

Use to define the skeleton of an algorithm in a method, deferring some steps to subclasses. Lets subclasses redefine certain steps without changing algorithm structure.

**Recognize when:** You want to implement invariant parts of an algorithm once and let subclasses implement varying behavior.

**Example:** `DataParser` template with `openFile()`, `parseData()` (abstract), `closeFile()`, `logResult()`. `XMLParser` and `JSONParser` subclasses override only `parseData()`. Algorithm structure enforced.

**Structure:** AbstractClass (template method calls abstract/hook methods) -> ConcreteClasses (implement abstract methods)

### Step 10: Visitor - Add Operations Without Modifying Classes

Use to represent an operation to be performed on elements of an object structure. Lets you define new operations without changing classes of elements.

**Recognize when:** Object structure contains many classes with differing interfaces and you want to perform operations depending on concrete classes, or many distinct operations need to be performed.

**Example:** Compiler AST with `NumberNode`, `AddNode`, `MultiplyNode`. `PrintVisitor`, `EvaluateVisitor`, `OptimizeVisitor` add operations without modifying node classes. Double dispatch enables correct method selection.

**Structure:** Visitor interface (visitConcreteA, visitConcreteB) | Element interface (accept) -> ConcreteElements (call visitor method)

## Example Application

**Situation:** Building a workflow automation system that must handle complex state transitions, support undo, and allow pluggable processing steps.

**Application of Behavioral Patterns:**
- **State:** Workflow items transition through `Draft -> Review -> Approved -> Published` states; each state encapsulates valid operations
- **Command:** All user actions (`ApproveCommand`, `RejectCommand`, `EditCommand`) are commands supporting undo/redo
- **Observer:** Stakeholders notified when workflow items change state
- **Strategy:** Pluggable approval strategies (`SingleApprover`, `MultiApprover`, `HierarchicalApproval`)
- **Chain of Responsibility:** Validation chain where each validator handles specific rules

**Outcome:** Clean state management, full undo support, decoupled notifications, pluggable approval logic, extensible validation.

## Anti-Patterns

- Observer with too many notifications causing performance issues (consider event batching)
- Chain of Responsibility with no handler catching the request (silent failures)
- State pattern with states knowing too much about each other (defeats decoupling)
- Command without proper undo semantics (partial undo breaks system)
- Strategy when algorithm selection is static (unnecessary indirection)
- Overusing Mediator creating a "god object" that knows everything
- Visitor when object structure changes frequently (every new element breaks all visitors)

## Related

- observer-pattern (detailed Observer coverage)
- state-machines (formal state modeling)
- command-pattern (detailed Command coverage)
- design-patterns-structural (patterns for object composition)
- design-patterns-creational (patterns for object creation)
- event-driven-architecture (Observer at architectural scale)
