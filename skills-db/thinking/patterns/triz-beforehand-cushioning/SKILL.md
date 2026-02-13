---
name: triz-beforehand-cushioning
description: Prepare emergency measures beforehand to compensate for low reliability or high-risk failures
---

# TRIZ Beforehand Cushioning (Principle #11)

## Overview

Beforehand Cushioning (also called Cushion in Advance or Preliminary Counteraction) is one of Genrich Altshuller's 40 Inventive Principles from TRIZ (Theory of Inventive Problem Solving), derived from analysis of over 200,000 patents. The principle states: prepare emergency means beforehand to compensate for the relatively low reliability of an object.

The core insight: if failures cannot be totally eliminated, prepare in advance for situations with high risk or high cost of failure. Reliability is never absolute, so build redundancy, safety margins, and fallback mechanisms before they are needed.

Beforehand Cushioning appears in three forms:
1. **Physical Safeguards** - Protective materials or structures installed proactively
2. **Process Redundancy** - Backup systems activated when primary systems fail
3. **Temporal Buffers** - Time-based safety margins built into schedules

## When to Use

- System reliability is less than 100% but failure cost is high
- Failures are rare but catastrophic when they occur
- Testing for failure is expensive or destructive
- Response time after failure is critical
- Regulatory compliance requires fail-safe mechanisms
- User safety depends on system integrity
- Recovery from failure is more expensive than prevention

## The Process

### Step 1: Identify High-Risk Failure Modes

What failures, though unlikely, would have severe consequences?

**Example:** Home fire is rare but deadly, especially for sleeping occupants.

### Step 2: Assess Reliability Limitations

Acknowledge that you cannot eliminate the risk entirely.

**Example:** Cannot guarantee zero electrical fires from faulty wiring or appliances.

### Step 3: Design Beforehand Countermeasures

Create safeguards that are already in place before failure occurs.

**Types of Countermeasures:**
- **Protective Materials:** Flame-resistant mattresses, fire-retardant building materials
- **Warning Systems:** Smoke detectors, carbon monoxide alarms
- **Escape Routes:** Multiple exits, fire escapes, emergency lighting
- **Backup Systems:** Redundant power supplies, failover servers
- **Insurance Mechanisms:** Financial protection against loss

**Example:** Mandate flame-resistant baby mattresses and furniture.

### Step 4: Test Countermeasure Activation

Verify that safeguards activate correctly when needed.

**Example:** Monthly smoke detector tests, annual fire drill exercises.

### Step 5: Communicate the Cushion to Users

Ensure stakeholders understand that protections exist and how to use them.

**Example:** Exit signs, evacuation maps, safety instruction placards.

## Example Application

**Situation (Smartphone Durability):** Smartphone screens crack when dropped, causing expensive repairs and user frustration.

**Application:**
1. **Failure Mode:** Drop from 1-2 meters onto hard surface
2. **Reliability Limit:** Cannot make glass unbreakable without excessive weight/cost
3. **Beforehand Countermeasures:**
   - Chemically strengthened Gorilla Glass (material-level cushioning)
   - Raised bezel edge to protect screen surface from direct impact
   - Internal shock-absorbing foam layers
   - Pre-applied screen protectors (user-facing cushioning)
4. **Testing:** Drop tests from multiple heights and angles
5. **Communication:** Marketing emphasizes "Corning Gorilla Glass protection"

**Outcome:** Screen survival rate increased from 60% to 85% in 1-meter drops, reduced warranty claims by 30%.

## Anti-Patterns

- Adding cushioning that is more expensive than the failure cost
- Over-engineering protections for low-consequence failures
- Creating safeguards that are difficult to maintain or test
- Cushioning that creates new risks (flame retardants that emit toxic fumes)
- Relying on cushioning instead of improving base reliability
- Assuming cushioning eliminates the need for user training
- Failing to update countermeasures as failure modes evolve

## Related

- fmea (identify failure modes to prioritize cushioning efforts)
- fault-tree-analysis (understand failure paths that need cushioning)
- fail-safe-design (design systems that fail into safe states)
- redundancy-principle (duplicate critical components for reliability)
- defense-in-depth (layer multiple safeguards for high-risk systems)
