---
name: triz-intermediary
description: Use an intermediary object, person, or process to connect two elements that cannot or should not interact directly
---

# TRIZ Intermediary (Principle #24)

## Overview

Intermediary is one of Genrich Altshuller's 40 Inventive Principles from TRIZ (Theory of Inventive Problem Solving), derived from analysis of over 200,000 patents. The principle states: use an intermediary carrier article or intermediary process to enable, improve, or protect the interaction between two elements.

The core insight: when direct interaction is impossible, inefficient, or harmful, introduce a third element to mediate the relationship. The intermediary can transform, translate, buffer, or optimize the connection without requiring changes to the original elements.

Intermediary appears in three forms:
1. **Physical Intermediary** - An object that enables physical connection (adapters, couplers, buffers)
2. **Process Intermediary** - An agent or service that facilitates interaction (brokers, translators, routers)
3. **Temporal Intermediary** - A mechanism that manages timing mismatches (queues, caches, schedulers)

## When to Use

- Two elements cannot connect directly due to incompatibility
- Direct interaction would damage one or both elements
- The interaction needs translation, transformation, or buffering
- Modifying the original elements is impractical or expensive
- You need flexibility to change one element without affecting the other
- Distribution, aggregation, or routing is required
- Safety concerns prevent direct contact

## The Process

### Step 1: Identify the Direct Interaction Challenge

What prevents or degrades direct connection between the two elements?

**Example:** Vacuum cleaner motor generates high suction but cannot navigate tight spaces.

### Step 2: Define Intermediary Requirements

What must the intermediary do to solve the interaction problem?

**Requirements Categories:**
- **Physical Translation:** Size, shape, material compatibility
- **Property Transformation:** Voltage conversion, speed reduction, pressure regulation
- **Routing/Distribution:** One-to-many, many-to-one, selective routing
- **Protection:** Shield from heat, chemicals, electrical discharge
- **Temporal Buffering:** Absorb timing mismatches, smooth bursts

**Example:** Intermediary must be flexible to navigate corners while maintaining suction.

### Step 3: Design or Select the Intermediary

Choose the simplest intermediary that meets requirements.

**Example:** Flexible hose with internal ribbing for structural integrity.

### Step 4: Optimize Interface Points

Ensure clean, efficient connection at both ends of the intermediary.

**Example:** Standardized coupling at motor end, swivel joint at attachment end.

### Step 5: Test End-to-End Performance

Verify that the intermediary enables the desired interaction without introducing new problems.

**Example:** Measure suction loss through hose, test durability under repeated flexing.

## Example Application

**Situation (Software Onboarding Complexity):** New users struggle with complex software setup, leading to high abandonment rates.

**Application:**
1. **Direct Challenge:** New user lacks knowledge to configure 30+ settings correctly
2. **Intermediary Requirements:** Guide user through decisions without overwhelming them
3. **Intermediary Design:** Step-by-step onboarding wizard with contextual help
4. **Interface Optimization:**
   - Start screen with single "Get Started" button
   - Completion screen with "Launch Application" transition
5. **Testing:** A/B test shows wizard reduces abandonment from 40% to 12%

**Outcome:** 70% reduction in support tickets during first week, 28% increase in successful onboarding completions.

## Anti-Patterns

- Adding intermediary when direct connection is actually possible
- Choosing an intermediary that is more complex than the problem
- Creating bottlenecks through slow or limited-capacity intermediaries
- Failing to maintain or upgrade the intermediary as needs evolve
- Over-relying on intermediaries instead of fixing underlying incompatibilities
- Introducing intermediaries that add latency or reduce quality unacceptably
- Not providing fallback when intermediary fails

## Related

- adapter-pattern (software design pattern for interface compatibility)
- proxy-pattern (intermediary object controlling access to another)
- mediator-pattern (centralized coordination between multiple elements)
- translation-layer (transform data/protocols between systems)
- buffer-abstraction (temporal intermediary for rate mismatches)
