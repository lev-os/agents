---
name: triz-taking-out
description: Separate an interfering or essential part from an object to place it in more favorable conditions or remove harmful interactions
---

# TRIZ Taking Out / Extraction (Principle #2)

## Overview

Taking Out (also called Extraction or Separation) is the second of Altshuller's 40 Inventive Principles from TRIZ. Unlike full segmentation, Taking Out is selective: extract only the interfering part (to remove harm) or the essential part (to optimize it independently).

The principle operates in two directions:
1. **Extract Harm** - Remove the problematic component to a location where it causes no damage
2. **Extract Value** - Separate the useful component to place it where it functions best

The key insight: when a system creates both value and harm in the same location, physically separating the source of harm (or moving the valuable function) often resolves contradictions that seem impossible.

## When to Use

- A useful function creates harmful byproducts in its current location
- Environmental constraints prevent optimal operation of a key component
- One part interferes with another's performance
- A component needs operating conditions different from the main system
- Cost can be reduced by extracting and remotely providing a function
- Safety requires separating hazardous elements from people

## The Process

### Step 1: Identify the Interference or Essential Property

What is causing harm, or what essential function is constrained by its current location?

**Example:** Aircraft cabin air conditioning burns expensive jet fuel when engines run to power it.

### Step 2: Determine Extraction Direction

- **Extract Harmful Part:** Move the problem source away from the affected area
- **Extract Essential Part:** Move the valuable component to where it operates better

**Example:** Extract the cooling function from the aircraft to a ground unit.

### Step 3: Design the Separation Mechanism

How will the extracted part maintain necessary connections while operating remotely?

**Example:** Ground-based AC unit connects via flexible hose to aircraft cabin during boarding.

### Step 4: Optimize the Extracted Component

Now free from constraints, the extracted part can be optimized for its specific function.

**Example:** Ground AC unit can use efficient electric power, unlimited water cooling, larger capacity.

### Step 5: Verify Remaining System Functions Correctly

Ensure the main system still operates properly with the extraction in place.

## Example Application

**Situation (Dow Corning - Xiameter):** Dow Corning needed to serve price-sensitive commodity silicone customers without cannibalizing their premium service-inclusive business model.

**Application:**
1. **Interference:** Full-service model's cost structure priced out commodity buyers
2. **Direction:** Extract the "service" component from the product offering
3. **Mechanism:** Create entirely separate business entity (Xiameter) with no-service, low-price model
4. **Optimization:** Xiameter optimized for pure shipping logistics - no technical support, no customization
5. **Verification:** Main Dow Corning brand maintained premium positioning for service-requiring customers

**Outcome:** Captured commodity market segment without eroding premium brand margins. Each entity optimized for its customer segment.

## Example Application (Industrial)

**Situation:** Cogeneration plants pollute residential areas with smoke, particulates, and CO emissions.

**Application:**
1. **Interference:** Heat/power generation produces harmful emissions where people live
2. **Direction:** Extract the pollution-producing facility from residential proximity
3. **Mechanism:** Locate plant at safe distance; transmit power/heat via lines and pipes
4. **Optimization:** Plant can use larger pollution control equipment without space constraints
5. **Verification:** Residents receive energy without exposure; plant operates efficiently

**Outcome:** Same utility delivered, harmful byproducts isolated at manageable distance.

## Anti-Patterns

- Extracting when integration is the source of value (separating tightly coupled systems that need proximity)
- Creating expensive transmission/connection costs that exceed extraction benefits
- Extracting without ensuring the remaining system is still complete
- Over-extracting until you have many disconnected components that lose synergy
- Assuming extraction always means physical separation (can be temporal or functional)
- Ignoring maintenance complexity of separated systems

## Related

- triz-segmentation (divides entire object vs. taking out specific part)
- triz-intermediary (use intermediate carrier instead of extraction)
- separation-of-concerns (software principle of isolating functions)
- microservices (architectural extraction of service functions)
- outsourcing (business extraction of non-core functions)
