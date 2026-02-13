---
name: triz-self-service
description: Make objects service, repair, or maintain themselves, eliminating external intervention
---

# TRIZ Self-Service (Principle #25)

## Overview

Self-Service is one of Genrich Altshuller's 40 Inventive Principles from TRIZ (Theory of Inventive Problem Solving), derived from analysis of over 200,000 patents. The principle states: make an object service itself by performing auxiliary helpful functions.

The core insight: the most reliable and efficient service is one that requires no external intervention. By designing objects to maintain, clean, repair, balance, or optimize themselves, you eliminate dependency on external resources and reduce lifecycle costs.

Self-Service appears in three forms:
1. **Self-Maintenance** - Objects clean, calibrate, or repair themselves
2. **Self-Optimization** - Systems adjust their own parameters for peak performance
3. **Self-Recovery** - Components restore themselves after damage or depletion

## When to Use

- Maintenance costs exceed the value of the service performed
- External service is inconvenient, expensive, or impossible to access
- Downtime for servicing disrupts critical operations
- User expertise cannot be assumed for manual maintenance
- Service frequency is high enough that automation pays off
- Environmental conditions make external intervention hazardous
- Scalability requires reducing per-unit maintenance burden

## The Process

### Step 1: Identify Auxiliary Operations Requiring External Service

What maintenance, adjustment, or repair tasks currently require outside intervention?

**Example:** Traditional ovens require manual scrubbing to remove baked-on food residue.

### Step 2: Analyze the Service Mechanism

How is the service currently performed, and what resources does it consume?

**Example:** User scrubs with abrasive cleaner and elbow grease, taking 20-30 minutes.

### Step 3: Design Self-Service Capability

Engineer the object to perform the service task autonomously.

**Self-Service Mechanisms:**
- **Chemical Self-Cleaning:** Use catalytic coatings that decompose residue at high heat
- **Mechanical Self-Adjustment:** Balance systems (gyroscopes, counterweights)
- **Software Self-Optimization:** Algorithms that tune parameters based on performance data
- **Material Self-Healing:** Polymers that flow into cracks, metals that oxidize protectively
- **User Self-Service:** Enable users to perform service without specialized skills (IKEA assembly)

**Example:** Self-cleaning oven uses pyrolytic cycle (500°C heat) to incinerate food residue to ash.

### Step 4: Trigger Self-Service Appropriately

Determine when and how self-service activates (automatic, scheduled, user-initiated).

**Example:** User initiates self-clean cycle before leaving the house; oven locks door for safety.

### Step 5: Validate Effectiveness and Safety

Ensure self-service achieves the goal without creating new risks or failures.

**Example:** Test that ash is easily wiped away, door lock prevents burns, heat doesn't damage oven components.

## Example Application

**Situation (Bicycle Wheel Stability):** Bicycle wheels go out of true over time, requiring professional truing service.

**Application:**
1. **Auxiliary Operation:** Wheel truing (adjusting spoke tension to maintain roundness)
2. **Current Mechanism:** Bike shop mechanic uses truing stand and spoke wrench
3. **Self-Service Design:** Self-balancing wheel design using gyroscopic effect and dynamic spoke tensioning
4. **Trigger:** Continuous automatic adjustment as wheel rotates under load
5. **Validation:** Test that wheel maintains true under varied load and speed conditions

**Outcome:** Eliminates need for truing service, extends wheel lifespan by 40%, improves ride quality.

## Anti-Patterns

- Designing self-service mechanisms more expensive than the service cost
- Creating complex self-service that is harder to maintain than manual service
- Self-service that consumes excessive energy or materials
- Ignoring safety risks of autonomous service operations
- Assuming users will accept or trust self-service features
- Over-engineering self-service for infrequent maintenance needs
- Failing to provide manual override when self-service fails

## Related

- triz-beforehand-cushioning (prepare safeguards before failure, complementary to self-repair)
- automation-principle (reduce human intervention in routine operations)
- self-healing-systems (software and material systems that recover from damage)
- feedback-loops (sense and respond mechanisms enabling self-optimization)
- user-empowerment (enable users to service themselves, IKEA model)
