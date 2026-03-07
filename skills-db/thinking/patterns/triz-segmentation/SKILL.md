---
name: triz-segmentation
description: Divide complex objects, systems, or processes into smaller independent parts to make them more manageable, flexible, or functional
---

# TRIZ Segmentation (Principle #1)

## Overview

Segmentation is the first of Genrich Altshuller's 40 Inventive Principles from TRIZ (Theory of Inventive Problem Solving), derived from analysis of over 200,000 patents. The principle states: divide an object into independent parts to increase its utility, adaptability, or to enable new functionalities impossible with the monolithic whole.

Segmentation appears in three forms:
1. **Physical Segmentation** - Divide into physically independent pieces
2. **Modular Segmentation** - Make easily assembled/disassembled
3. **Increased Degree of Segmentation** - Take segmentation to the extreme (powder, liquid, gas)

The underlying insight: what cannot be achieved with a whole object often becomes possible when it is divided. Resistance, flexibility, customization, and maintenance all improve through strategic division.

## When to Use

- A system is too rigid to adapt to varying conditions
- Transportation, storage, or handling of the whole is impractical
- Different parts need different properties or treatments
- You need customization without complete redesign
- Failure of one part shouldn't catastrophically affect the whole
- Assembly in confined spaces requires smaller components
- Different use cases require different configurations

## The Process

### Step 1: Identify the Constraint of Wholeness

What limitation exists because the object/system is currently monolithic?

**Example:** A full-length measuring pole cannot fit through doorways or car trunks.

### Step 2: Determine the Segmentation Type

- **Functional Segmentation:** Divide by function (modular catheter with diagnostic + delivery sections)
- **Spatial Segmentation:** Divide by location (multi-layer packaging materials)
- **Temporal Segmentation:** Divide by time of use (sectional furniture deployed as needed)
- **Granular Segmentation:** Reduce to smallest useful unit (powder medication for precise dosing)

### Step 3: Define Interface Points

Determine how segments will connect, interact, or combine. Design joints that are:
- Easy to assemble/disassemble
- Reliable under operational stress
- Compatible with varied configurations

**Example:** Hinged, spring-loaded measuring pole segments that snap back to vertical.

### Step 4: Optimize Each Segment Independently

Each segment can now be optimized for its specific function without compromising others.

**Example:** Multi-layer packaging - inner layer for cushioning, middle for moisture barrier, outer for rigidity.

### Step 5: Test Recombination Scenarios

Verify that segmented system meets requirements in all intended configurations.

## Example Application

**Situation (Medical Device Innovation):** Traditional catheters are single rigid units causing patient discomfort during complex procedures.

**Application:**
1. **Constraint:** Rigid catheter cannot navigate tortuous anatomy while maintaining diagnostic capability
2. **Type:** Functional segmentation - separate diagnostic and delivery modules
3. **Interface:** Quick-connect modular joints with fluid and electrical continuity
4. **Optimization:** Diagnostic tip optimized for sensing; delivery section optimized for flexibility
5. **Result:** Reduced patient discomfort by 40%, maintained diagnostic accuracy

**Outcome:** Modular catheter system enables mix-and-match configurations for different procedures, reducing inventory costs and improving outcomes.

## Anti-Patterns

- Segmenting where wholeness is the primary value (a painting, a precision instrument requiring exact alignment)
- Creating too many segments that increase assembly complexity beyond the benefit
- Weak interface design that makes segments unreliable when combined
- Segmenting without considering how parts will be managed, stored, or replaced
- Ignoring emergent properties that only exist in the whole system
- Over-engineering segments when simple division would suffice

## Related

- triz-taking-out (extract only the necessary part - more selective than full segmentation)
- triz-nested-doll (place segmented parts inside each other for compactness)
- first-principles-thinking (decompose to fundamentals before redesigning)
- domain-driven-design (segment software by bounded contexts)
- modular-architecture (software application of segmentation principle)
