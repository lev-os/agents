---
name: system-archetypes
description: Recognize recurring system behavior patterns like limits-to-growth and tragedy-of-commons to predict failure modes and design interventions
---

# System Archetypes

## Overview
System archetypes, identified by Donella Meadows, Peter Senge, and systems pioneers at MIT, are recurring patterns of system behavior that appear across different contexts. These archetypes (limits to growth, shifting the burden, tragedy of the commons, etc.) help diagnose why systems behave unexpectedly and predict failure modes before they occur.

## When to Use
- System exhibiting counterintuitive or unexpected behavior
- Solutions that worked initially are now failing
- Success followed by unexpected decline or collapse
- Multiple stakeholders depleting a shared resource
- Short-term fixes creating long-term problems
- Observing same failure pattern across different projects

## The Process

### Step 1: Recognize the Pattern
Match observed system behavior to known archetypes. Common symptoms: initial growth followed by plateau (limits to growth), escalation between competing parties, success in one area causing failure in another.

**Example:** Company grows rapidly then stalls—classic "limits to growth" archetype where a limiting factor (talent, infrastructure) constrains what was previously exponential.

### Step 2: Map the System Structure
Diagram the reinforcing and balancing feedback loops creating the archetype. Identify: What's driving growth? What's the limiting factor? Where are delays causing oscillation?

**Example:** Limits to growth structure: Marketing drives user growth (reinforcing loop) → growth hits server capacity limit (balancing loop) → performance degrades → churn increases.

### Step 3: Identify the Leverage Point
Each archetype has characteristic high-leverage interventions. For limits to growth: remove or anticipate the constraint. For shifting the burden: strengthen fundamental solution vs. symptomatic fix.

**Example:** Remove the constraint (server capacity) before hitting limit, or shift growth target to a metric not constrained by servers (engagement vs. raw users).

### Step 4: Design Archetype-Specific Intervention
Apply the standard intervention for that archetype. Don't try generic solutions—each archetype requires specific structural changes.

**Example:** For "tragedy of the commons" (shared resource depletion), standard interventions are: educate users, regulate access, privatize resource, or convert to managed commons.

## Common System Archetypes

**Limits to Growth**: Initial success hits a constraint, causing plateau or decline. *Intervention*: Anticipate and remove constraint early.

**Shifting the Burden**: Symptomatic fix (painkillers) used instead of fundamental solution (exercise), weakening ability to use fundamental approach. *Intervention*: Strengthen fundamental solution despite taking longer.

**Tragedy of the Commons**: Multiple parties overexploit shared resource until collapse. *Intervention*: Regulation, privatization, or community management.

**Fixes that Fail**: Quick fix produces unintended consequences that worsen original problem. *Intervention*: Trace side effects before implementing fix.

**Success to the Successful**: Winner gains advantage that ensures continued winning, creating monopoly. *Intervention*: Limit runaway positive feedback, support diversity.

**Escalation**: Competing parties match each other's actions, spiraling upward. *Intervention*: Unilateral de-escalation or negotiated limits.

## Example Application

**Situation**: Software team keeps adding tools to solve collaboration problems but productivity keeps declining.

**Archetype Recognized**: "Shifting the Burden"—symptomatic solution (new tool) instead of fundamental solution (communication culture).

**Application**:
- Initial problem: Poor coordination
- Symptomatic fix: Buy new project management tool
- Side effect: More tools = more context switching = worse communication
- Atrophy: Team stops talking directly, relies on tool notifications
- Fundamental solution: Daily standups, shared working sessions, co-located seating

**Outcome**: Team removes 4 tools, implements daily sync + paired programming. Productivity increases 40%, tool costs drop 80%.

## Anti-Patterns
- ❌ Treating symptoms without recognizing underlying archetype
- ❌ Applying wrong intervention to misdiagnosed archetype
- ❌ Believing "this situation is unique"—most aren't
- ❌ Ignoring delays between action and feedback
- ❌ Intervening at wrong point in the causal loop
- ❌ Fighting the archetype structure instead of redesigning it

## Related
- 12-leverage-points
- feedback-loops
- second-order-thinking
- systems-thinking
