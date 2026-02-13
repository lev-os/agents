---
name: triz-nested-doll
description: Place one object inside another, which is inside a third, maximizing space utilization and increasing system compactness
---

# TRIZ Nested Doll / Matryoshka (Principle #7)

## Overview

The Nested Doll (Matryoshka) principle is the seventh of Altshuller's 40 Inventive Principles from TRIZ. The principle states: place one object inside another; make one object pass through a cavity in another object; use the empty internal spaces of objects for additional functions.

Named after Russian nesting dolls, this principle addresses a fundamental design challenge: eliminating wasted space while maintaining full functionality. The insight: empty space inside objects is an untapped resource.

Two application modes:
1. **Static Nesting** - Objects permanently nested for storage or transport (measuring cups)
2. **Dynamic Nesting** - Objects extend from nested state for operation (telescoping antenna)

## When to Use

- Storage or transport space is severely limited
- System must be compact in one state, extended in another
- Empty internal cavities exist in structural components
- Multiple sizes of similar objects need efficient storage
- Portable systems need to collapse for mobility
- Cost reduction requires minimizing material and shipping volume
- Protection of inner components from environment

## The Process

### Step 1: Identify Empty Space or Size Constraints

Map the unused internal volumes or the space constraints driving the need for compactness.

**Example:** Camping trailer must fit on car hitch for transport but provide living space at site.

### Step 2: Determine Nesting Geometry

Design shapes that fit inside each other:
- **Conical Nesting:** Stacking cups, funnels
- **Cylindrical Nesting:** Telescoping tubes, measuring spoons
- **Rectangular Nesting:** Storage containers, folding furniture
- **Organic Nesting:** Custom shapes that interlock

**Example:** Beauer 3X trailer uses rectangular sections that telescope outward.

### Step 3: Design Extension/Extraction Mechanism

How do nested objects deploy or separate for use?
- Slide/telescope
- Hinge/unfold
- Lift/stack
- Rotate/unscrew

**Example:** Trailer sections slide out on rails, lock in extended position.

### Step 4: Ensure Functional Integrity in Both States

Nested state must be robust for transport; extended state must perform fully.

**Example:** Each trailer section, when extended, provides structural walls and weatherproofing.

### Step 5: Address Scaling Implications

If nesting creates size variations, ensure each size is still functional.

**Example:** Nested screwdrivers - each size must have sufficient torque-bearing capability.

## Example Application

**Situation (Industrial Chimney Construction):** Tall industrial chimneys require construction or repair at height, with difficult logistics for transporting long sections.

**Application:**
1. **Constraint:** Long chimney sections cannot be transported to site
2. **Geometry:** Cylindrical nesting - telescoping tube sections fit inside each other
3. **Mechanism:** Hydraulic lift extends sections vertically from inside
4. **Integrity:** When extended, sections lock and seal at joints
5. **Scaling:** Each outer section supports weight of all inner sections

**Outcome:** Complete chimney delivered in single compact unit, extended on-site without crane.

## Example Application (Consumer Product)

**Situation (Multi-Tool Screwdriver):** Users need multiple screwdriver sizes but carrying many tools is inconvenient.

**Application:**
1. **Constraint:** Need 6+ driver sizes in pocket-portable form
2. **Geometry:** Cylindrical - smaller drivers nest inside larger ones
3. **Mechanism:** Pull/twist to extract; largest handle serves as hammer
4. **Integrity:** Each extracted driver locks into handle for torque
5. **Scaling:** Smaller drivers have proportionally smaller tips

**Outcome:** Full toolkit in single pocket-sized tool.

## Example Application (Software Architecture)

**Situation:** Software components need to scale from minimal to full-featured without separate codebases.

**Application:**
1. **Constraint:** Can't maintain separate products for different feature tiers
2. **Geometry:** Feature nesting - basic tier contained within standard, standard within premium
3. **Mechanism:** License keys or configuration enable outer "shells" of functionality
4. **Integrity:** Each tier is complete and functional
5. **Scaling:** Incremental capability unlocked without reinstallation

**Outcome:** Single codebase serves entire product line with nested feature sets.

## Anti-Patterns

- Nesting fragile components that can be damaged by contact
- Creating nested designs that can't be disassembled for maintenance
- Over-nesting to the point where inner items are inaccessible
- Ignoring structural requirements when inner items must bear load
- Assuming nesting always saves space (poor geometry can waste more)
- Forgetting that nested items may have different thermal/environmental needs

## Related

- triz-segmentation (divide first, then potentially nest the segments)
- triz-taking-out (extract vs. nest - opposite approaches to space)
- fractal-design (self-similar structures at multiple scales)
- information-architecture (nested hierarchies in content)
- composite-pattern (software nested structures)
