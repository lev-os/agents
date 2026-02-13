---
name: Fault Tree Analysis
description: Top-down deductive methodology for analyzing system failures by mapping logical relationships between faults, subsystems, and redundant safety elements using Boolean logic diagrams
---

## Overview

Fault Tree Analysis (FTA) is a systematic, top-down approach to root cause analysis that starts with an undesired event (the "top event") and works backwards to identify all possible causes. Originally developed in 1962 at Bell Laboratories for the Minuteman I missile system, FTA creates a tree-like logic diagram showing how lower-level component failures and conditions combine to produce system-level failures.

Unlike bottom-up approaches like FMEA, FTA excels at analyzing specific known failures in complex systems by decomposing them into their contributing factors using Boolean logic gates (AND, OR). The visual tree structure makes it particularly valuable for communicating failure scenarios to stakeholders and identifying critical paths that require redundancy or safeguards.

**Key distinction**: FTA is deductive (known failure → find causes) while FMEA is inductive (examine components → predict failures).

## When to Use

Apply Fault Tree Analysis when you need to:

- **Investigate critical system failures** in high-stakes environments (aerospace, nuclear, medical devices)
- **Analyze a specific undesired event** where the failure has already occurred or is well-defined
- **Identify single points of failure** and validate redundancy requirements
- **Calculate failure probabilities** for system-level events based on component reliability data
- **Communicate complex failure scenarios** to non-technical stakeholders through visual diagrams
- **Prioritize risk mitigation** by identifying minimal cut sets (smallest combinations of events causing failure)
- **Compare design alternatives** by analyzing how architectural changes affect failure paths

**Don't use when**: You need to explore all possible failure modes proactively (use FMEA instead), the system is too simple for tree analysis, or you lack sufficient data on component failure rates for quantitative analysis.

## Process

### 1. Define the Top Event
Precisely specify the undesired system-level failure you're analyzing. Should be specific, measurable, and represent a single failure condition.

**Example**: "Aircraft landing gear fails to deploy" not "landing gear problems"

### 2. Identify Immediate Causes
Determine all events or conditions that directly cause the top event. Use Boolean logic gates:
- **OR gate**: Any single input causes the output (parallel redundancy failure)
- **AND gate**: All inputs must occur simultaneously for output (sequential dependencies)

### 3. Decompose Each Cause
For each immediate cause, recursively identify its contributing factors. Continue until reaching "basic events" - component failures or human errors that cannot be decomposed further.

**Stop criteria**: Events with known failure rates, events outside system boundaries, or events too rare to analyze further.

### 4. Calculate Minimal Cut Sets
Identify the smallest combinations of basic events that, if they all occur, guarantee the top event. These represent critical vulnerabilities.

**Example**: If "Power Loss" OR "Sensor Failure" both lead to top event, you have two single-point failures requiring attention.

### 5. Perform Quantitative Analysis (Optional)
If component failure rates are available, calculate the probability of the top event using Boolean algebra on the tree structure.

**Formula**: For OR gates: P(A or B) = P(A) + P(B) - P(A)×P(B). For AND gates: P(A and B) = P(A)×P(B)

### 6. Identify and Prioritize Mitigations
Focus on minimal cut sets with highest probability or severity. Add redundancy for OR gates, break dependencies for AND gates.

### 7. Document and Validate
Review tree with domain experts to ensure completeness. Update as system design evolves or new failure data emerges.

## Example

**Scenario**: Server cluster outage analysis

**Top Event**: Customer-facing API becomes unavailable

**Level 1 Causes** (OR gate):
- Load balancer failure
- All backend servers fail (AND gate required)
- Database becomes unreachable

**Level 2 Decomposition**:
- "All backend servers fail" requires:
  - Server A fails AND Server B fails AND Server C fails
- "Database unreachable" can occur via:
  - Database crashes OR Network partition OR Credential rotation breaks connection

**Minimal Cut Sets Identified**:
1. Load balancer failure (single point!)
2. Database crash (single point!)
3. Network partition (single point!)
4. A+B+C server failures (extremely unlikely, but possible)

**Mitigation Actions**:
- Add redundant load balancer (eliminates cut set #1)
- Implement database clustering (reduces cut set #2 probability)
- Add multi-region failover (addresses cut set #3)

## Anti-Patterns

**Analysis Paralysis**: Creating overly complex trees with excessive decomposition. Stop at basic events with known failure rates or outside your control.

**Ignoring Time Dependencies**: FTA struggles with sequential failures where timing matters. If "Event A must occur before Event B", use Event Tree Analysis or FMEA instead.

**Confirmation Bias**: Building the tree to prove a predetermined cause. Let the evidence guide the structure, not your hypothesis.

**Stale Documentation**: Creating a beautiful tree diagram but never updating it as the system evolves. FTA is living documentation, not a one-time exercise.

**Quantitative Theater**: Calculating precise probabilities with unreliable input data. Garbage in, garbage out. Qualitative analysis is often more valuable than false precision.

**Skipping Validation**: Not reviewing the completed tree with operators, maintenance teams, or other domain experts who know how the system actually fails.

## Related Frameworks

- **FMEA (Failure Mode Effects Analysis)**: Bottom-up complement to FTA; use FMEA to discover failure modes, FTA to analyze specific critical failures
- **Event Tree Analysis**: Forward-looking version of FTA; starts with initiating event and maps possible outcomes
- **5 Whys**: Simpler root cause tool for less complex systems; escalate to FTA when 5 Whys reveals complex interactions
- **Fishbone Diagram**: Brainstorming-focused alternative; less rigorous than FTA but faster for initial investigation
- **Bow-Tie Analysis**: Combines FTA (left side: causes) with Event Tree (right side: consequences) for comprehensive risk analysis
