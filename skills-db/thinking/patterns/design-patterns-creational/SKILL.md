---
name: design-patterns-creational
description: Control object creation mechanisms using five creational patterns from the Gang of Four to increase flexibility and reuse
---

# Design Patterns (Creational)

## Overview

Creational design patterns abstract the instantiation process, making systems independent of how objects are created, composed, and represented. Introduced in the 1994 Gang of Four book "Design Patterns," creational patterns give flexibility in what gets created, who creates it, how it gets created, and when. They encapsulate knowledge about which concrete classes the system uses and hide how instances of these classes are created and combined.

The five creational patterns are: Abstract Factory (families of related objects), Builder (step-by-step construction), Factory Method (defer instantiation to subclasses), Prototype (clone existing objects), and Singleton (ensure single instance). Each addresses different aspects of object creation complexity in software systems.

## When to Use

- Creating families of related objects without specifying concrete classes (Abstract Factory)
- Constructing complex objects step-by-step with many optional parameters (Builder)
- Delegating object creation to subclasses (Factory Method)
- Creating new objects by copying existing ones when instantiation is expensive (Prototype)
- Ensuring a class has exactly one instance with global access point (Singleton)
- Decoupling client code from concrete class implementations
- Avoiding constructor parameter explosion or telescoping constructors
- Supporting multiple product representations from same construction process

## The Process

### Step 1: Factory Method - Defer Instantiation to Subclasses

Use Factory Method to define an interface for creating objects but let subclasses decide which class to instantiate. Provides hook for subclasses.

**Recognize when:** A class can't anticipate which objects it must create, or a class wants subclasses to specify created objects.

**Example:** `LogisticsApp` with abstract `createTransport()` method. `RoadLogistics` returns `Truck`, `SeaLogistics` returns `Ship`. Both implement `Transport` interface. Main app code works with any transport without knowing concrete types.

**Structure:** Creator (declares factory method) -> ConcreteCreators (implement factory method) | Product interface -> ConcreteProducts

**Code Pattern:**
```
abstract class Creator {
  abstract createProduct(): Product
  operation() { product = this.createProduct(); product.doStuff() }
}
```

### Step 2: Abstract Factory - Create Families of Related Objects

Use Abstract Factory to provide an interface for creating families of related or dependent objects without specifying concrete classes.

**Recognize when:** System should be independent of how products are created, system should be configured with one of multiple product families, or products in a family are designed to work together.

**Example:** UI toolkit supporting Windows and Mac. `GUIFactory` with `createButton()`, `createCheckbox()`. `WindowsFactory` creates `WindowsButton`, `WindowsCheckbox`. `MacFactory` creates `MacButton`, `MacCheckbox`. Client code uses factory interface, unaware of platform.

**Structure:** AbstractFactory -> ConcreteFactories | AbstractProduct -> ConcreteProducts (families)

**Key distinction from Factory Method:** Abstract Factory creates multiple related products; Factory Method creates one product type.

### Step 3: Builder - Construct Complex Objects Step-by-Step

Use Builder to separate the construction of a complex object from its representation, allowing the same construction process to create different representations.

**Recognize when:** Algorithm for creating complex object should be independent of parts and assembly, or construction process must allow different representations.

**Example:** `HouseBuilder` with `buildWalls()`, `buildDoors()`, `buildWindows()`, `buildRoof()`. `WoodHouseBuilder` and `StoneHouseBuilder` implement steps differently. `Director` calls steps in order. Client gets complete house without knowing construction details.

**Structure:** Builder interface (build steps) -> ConcreteBuilders (implement steps, provide result) | Director (defines build order) | Product (complex object)

**Code Pattern:**
```
house = new HouseBuilder()
  .setWalls(4)
  .setDoors(2)
  .setWindows(6)
  .setGarage(true)
  .build()
```

### Step 4: Prototype - Clone Existing Objects

Use Prototype to specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.

**Recognize when:** System should be independent of how products are created, classes to instantiate are specified at runtime, or avoiding factory hierarchy parallel to product hierarchy.

**Example:** Shape editor with complex shapes. Instead of recreating `Circle` with all its properties, clone existing instance. `shape.clone()` creates deep copy. Prototype registry holds preconfigured shapes for cloning.

**Structure:** Prototype interface (clone) -> ConcretePrototypes (implement clone) | Client (asks prototype to clone itself)

**Key consideration:** Implement deep copy correctly - cloned objects must not share mutable state with original.

### Step 5: Singleton - Ensure Single Instance

Use Singleton to ensure a class has only one instance and provide a global point of access to it.

**Recognize when:** There must be exactly one instance of a class accessible from well-known access point, or sole instance should be extensible by subclassing.

**Example:** Database connection pool, configuration manager, logger. `Database.getInstance()` returns single instance, creating it on first call (lazy initialization).

**Structure:** Singleton class with private constructor, static instance variable, static getInstance() method

**Modern considerations:**
- Thread safety: Use double-checked locking or static initialization
- Testability: Singleton makes testing difficult - prefer dependency injection
- Hidden dependencies: Singleton creates implicit coupling
- Many consider Singleton an anti-pattern - use sparingly, prefer DI containers

## Example Application

**Situation:** Building a document processing system that must support multiple document formats (PDF, Word, HTML) with complex document structures.

**Application of Creational Patterns:**
- **Abstract Factory:** `DocumentFactory` interface with `PDFFactory`, `WordFactory`, `HTMLFactory`. Each creates compatible `Document`, `Page`, `Paragraph` objects for its format
- **Builder:** `DocumentBuilder` constructs complex documents step-by-step: `addTitle()`, `addSection()`, `addTable()`, `addImage()`. Same building process creates different document types
- **Factory Method:** `Document` class with abstract `createPage()` - subclasses like `PDFDocument` create appropriate `PDFPage` objects
- **Prototype:** Template documents stored as prototypes. Creating "Invoice" document clones existing invoice template rather than recreating from scratch
- **Singleton:** `DocumentRegistry` singleton maintains catalog of available document types and templates

**Outcome:** Client code creates documents without knowing concrete classes, same construction process produces multiple formats, templates are efficiently cloned, central registry provides document type discovery.

## Decision Guide

| Pattern | Use When |
|---------|----------|
| Factory Method | Subclasses should determine instantiated type |
| Abstract Factory | Need families of related objects |
| Builder | Object requires many construction steps |
| Prototype | Creating object is more expensive than cloning |
| Singleton | Exactly one instance needed globally |

## Anti-Patterns

- Singleton overuse creating hidden dependencies and testing nightmares
- Abstract Factory when only one product family exists (over-engineering)
- Builder for simple objects that could use constructor or static factory
- Prototype with improper deep copy causing subtle shared-state bugs
- Factory returning concrete types instead of interfaces (defeats purpose)
- Creating factories for every class (factory explosion)
- Using Singleton for convenience rather than genuine single-instance requirement

## Related

- dependency-injection (modern alternative to some creational patterns)
- factory-pattern (detailed Factory Method coverage)
- builder-pattern (detailed Builder coverage)
- design-patterns-structural (patterns for object composition)
- design-patterns-behavioral (patterns for object communication)
- object-pool (related creational pattern not in GoF)
