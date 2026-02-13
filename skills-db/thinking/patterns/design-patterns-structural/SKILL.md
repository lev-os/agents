---
name: design-patterns-structural
description: Compose objects and classes into larger structures while keeping them flexible and efficient using seven structural patterns from the Gang of Four
---

# Design Patterns (Structural)

## Overview

Structural design patterns explain how to assemble objects and classes into larger structures while keeping structures flexible and efficient. Introduced in the seminal 1994 book "Design Patterns: Elements of Reusable Object-Oriented Software" by Gamma, Helm, Johnson, and Vlissides (the Gang of Four), these patterns address object composition and typically use inheritance or composition to establish relationships between entities.

The seven structural patterns are: Adapter (interface compatibility), Bridge (separate abstraction from implementation), Composite (tree structures), Decorator (add responsibilities dynamically), Facade (simplified interface), Flyweight (share common state), and Proxy (surrogate or placeholder). Each pattern solves a specific structural problem in software design.

## When to Use

- Integrating incompatible interfaces between legacy and new systems (Adapter)
- Separating abstraction from implementation so both can vary independently (Bridge)
- Building tree structures to represent part-whole hierarchies (Composite)
- Adding behavior to objects without modifying their class (Decorator)
- Providing a simple interface to a complex subsystem (Facade)
- Supporting large numbers of fine-grained objects efficiently (Flyweight)
- Controlling access to an object or adding functionality transparently (Proxy)
- Refactoring monolithic code into composable, maintainable structures

## The Process

### Step 1: Adapter - Make Incompatible Interfaces Work Together

Use Adapter when you need to use an existing class but its interface doesn't match what you need. Wraps one interface to make it compatible with another.

**Recognize when:** You have existing code that can't be modified but needs to work with new code expecting a different interface.

**Example:** Your application uses `XMLParser` but a new library provides `JSONParser`. Create `JSONToXMLAdapter` that implements `XMLParser` interface but delegates to `JSONParser` internally.

**Structure:** Target interface -> Adapter (implements Target, holds reference to Adaptee) -> Adaptee (existing class)

### Step 2: Bridge - Separate Abstraction from Implementation

Use Bridge when you want to decouple an abstraction from its implementation so both can vary independently. Prevents class explosion from combinatorial inheritance.

**Recognize when:** You're facing a class hierarchy that's growing in two independent dimensions (e.g., shapes x rendering methods).

**Example:** Instead of `VectorCircle`, `RasterCircle`, `VectorSquare`, `RasterSquare`, create `Shape` abstraction with `Renderer` implementation. `Circle` holds reference to `Renderer`, can use `VectorRenderer` or `RasterRenderer`.

**Structure:** Abstraction (holds Implementor reference) -> RefinedAbstraction | Implementor interface -> ConcreteImplementors

### Step 3: Composite - Treat Individual Objects and Compositions Uniformly

Use Composite to compose objects into tree structures representing part-whole hierarchies. Clients treat individual objects and compositions identically.

**Recognize when:** You need to implement a tree-like structure where both leaf nodes and branches should be treated uniformly.

**Example:** File system where `File` and `Directory` share `FileSystemComponent` interface with `getSize()`. Directory's `getSize()` recursively sums children. Client code doesn't distinguish between files and directories.

**Structure:** Component interface -> Leaf (no children) | Composite (contains children, implements Component methods by delegating to children)

### Step 4: Decorator - Add Responsibilities Dynamically

Use Decorator to attach additional responsibilities to objects dynamically. Provides flexible alternative to subclassing for extending functionality.

**Recognize when:** You need to add behavior to objects at runtime, or when subclassing would create too many combinations.

**Example:** `Coffee` class with `Milk`, `Sugar`, `Vanilla` decorators. `new Vanilla(new Milk(new Coffee()))` - each decorator wraps the previous, calling its method then adding its own behavior.

**Structure:** Component interface -> ConcreteComponent | Decorator (holds Component, implements Component) -> ConcreteDecorators

### Step 5: Facade - Provide Simplified Interface to Complex Subsystem

Use Facade to provide a unified, simple interface to a set of interfaces in a subsystem. Defines higher-level interface making subsystem easier to use.

**Recognize when:** You have a complex subsystem with many interdependent classes that clients find difficult to use correctly.

**Example:** `VideoConverter` facade hides complexity of `AudioCodec`, `VideoCodec`, `BitrateReader`, `AudioMixer`, `VideoFrameBuffer`. Client calls `converter.convert(filename, format)` instead of orchestrating 10 classes.

**Structure:** Facade (delegates to subsystem classes) -> Subsystem classes (unaware of facade)

### Step 6: Flyweight - Share Common State Efficiently

Use Flyweight to support large numbers of fine-grained objects efficiently by sharing common parts of state. Distinguishes intrinsic (shared) from extrinsic (context-specific) state.

**Recognize when:** Application creates huge numbers of similar objects consuming significant memory; most object state can be made extrinsic.

**Example:** Text editor where each character could be an object. Instead, share `CharacterGlyph` objects (intrinsic: font, style) and pass position (extrinsic) at render time. 1000-character document uses ~26 glyph objects.

**Structure:** FlyweightFactory (creates/manages shared flyweights) -> Flyweight (stores intrinsic state) | Client passes extrinsic state

### Step 7: Proxy - Control Access or Add Functionality Transparently

Use Proxy to provide surrogate or placeholder for another object. Controls access, adds lazy initialization, logging, caching, or access control.

**Recognize when:** You need lazy initialization (virtual proxy), access control (protection proxy), local execution of remote service (remote proxy), or logging/caching (smart proxy).

**Example:** `ImageProxy` implements `Image` interface but delays loading actual `RealImage` until `display()` is first called. Subsequent calls use cached image. Client code unchanged.

**Structure:** Subject interface -> RealSubject | Proxy (implements Subject, holds RealSubject reference, controls access)

## Example Application

**Situation:** Building a document editor that must handle complex formatting, embedded objects, and support for different rendering platforms.

**Application of Structural Patterns:**
- **Composite:** Document tree where `Paragraph`, `Table`, `Image` are components; `Section` and `Document` are composites containing other components
- **Decorator:** Text formatting - `BoldDecorator(ItalicDecorator(Text))` allows runtime combination without class explosion
- **Bridge:** Separate document abstraction from platform-specific rendering (Windows, Mac, Linux renderers)
- **Flyweight:** Share `Font` and `Style` objects across millions of characters
- **Facade:** `DocumentExporter` facade simplifies complex export subsystem (PDF generator, image optimizer, font embedder)

**Outcome:** Clean composition model, memory-efficient character handling, platform-independent design, simple export API.

## Anti-Patterns

- Using Adapter when you should redesign the interface (adapters accumulate technical debt)
- Over-applying Decorator creating deeply nested "wrapper hell" that's hard to debug
- Composite where leaf/composite distinction matters to clients (defeats the pattern's purpose)
- Facade that becomes a "god object" coupling to entire subsystem
- Premature Flyweight optimization when object count doesn't warrant complexity
- Proxy adding significant latency or complexity for minimal benefit
- Applying patterns mechanically without verifying the specific problem exists

## Related

- adapter-pattern (detailed Adapter coverage)
- composite-pattern (detailed Composite coverage)
- decorator-pattern (detailed Decorator coverage)
- design-patterns-behavioral (patterns for object communication)
- design-patterns-creational (patterns for object creation)
- dependency-injection (related to Bridge and Proxy concepts)
