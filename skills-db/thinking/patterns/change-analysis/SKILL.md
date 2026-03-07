---
name: Change Analysis
description: Root cause investigation method that identifies the cause of problems by comparing the current failed state to a previous problem-free state to isolate what changed
---

## Overview

Change Analysis is a comparative root cause technique based on a simple insight: if a system was working correctly and then started failing, something must have changed. By systematically identifying differences between the "before" (working) and "after" (failing) states, investigators can pinpoint causal factors even in complex systems.

The methodology is particularly effective for diagnosing shifts in system behavior over time, such as increased incident rates, degraded performance, or emerging quality issues. Change Analysis recognizes that change propagates through systems with directional and exponential characteristics - multiple simultaneous changes can interact in non-additive ways, making comprehensive change mapping critical.

**Key distinction**: Change Analysis focuses on temporal comparison (before vs. after) while other RCA methods analyze structural relationships. It's the method of choice when "things were working fine until recently."

## When to Use

Apply Change Analysis when you need to:

- **Diagnose performance degradation** that appeared after a specific point in time
- **Investigate increased incident rates** or safety metrics showing negative trends
- **Troubleshoot after deployments** when new code/config caused unexpected problems
- **Analyze quality shifts** in manufacturing or service delivery
- **Debug "what changed?" mysteries** where system behavior suddenly differs from baseline
- **Validate suspected causes** by confirming they align with failure timeline
- **Prevent recurrence** by understanding which types of changes introduce risk

**Don't use when**: System never worked correctly (no baseline for comparison), failure occurs randomly without correlation to changes, or you need to analyze a specific complex failure mechanism (use Fault Tree Analysis instead).

## Process

### 1. Establish the Problem and Baseline
Precisely define the current problem: what's failing, where, when did it start, how severe. Then identify a clear comparison baseline - a time period or system state when things worked correctly.

**Example**: "API error rate increased from 0.1% to 2.5% starting Nov 10, 14:00 UTC. Baseline: Nov 1-9, error rate stable at 0.1%"

### 2. Map the Timeline
Create a chronological list of ALL changes that occurred between the baseline period and problem emergence. Include three types:
- **Mandated changes**: Deliberate actions (deployments, config changes, policy updates)
- **Natural changes**: Environmental shifts noticed or unnoticed (traffic growth, seasonal patterns, dependency updates)
- **Caused changes**: Unintended consequences of other changes (cache invalidation after deployment, cascading failures)

**Critical**: Cast a wide net. Include changes outside your direct control (upstream services, infrastructure, external dependencies).

### 3. Categorize Change Characteristics
For each identified change, document:
- **What**: Specific nature of the change
- **Where**: Which system components affected
- **When**: Exact timing relative to problem onset
- **Extent**: Scope and magnitude of change

**Timing alignment**: Changes occurring immediately before or concurrent with problem onset are prime suspects.

### 4. Classify Causal Relationships
Evaluate each change for its relationship to the problem:

**Unrelated**: Change and problem have no plausible connection (different systems, misaligned timing)

**Correlated**: Change timing aligns with problem, but causal mechanism unclear (coincidence possible)

**Contributing**: Change plausibly contributed to problem but isn't sufficient alone (enabler or amplifier)

**Root Cause**: Change is necessary and sufficient to explain the problem

### 5. Test Hypotheses
For changes classified as Contributing or Root Cause, validate through:
- **Rollback testing**: If possible, reverse the change and observe if problem resolves
- **Controlled reproduction**: Apply the change in a test environment and verify problem appears
- **Data correlation**: Analyze metrics/logs to confirm cause-effect relationship beyond timing

**Evidence-based validation**: Move changes from "correlated" to "contributing/root cause" only with evidence.

### 6. Account for Change Interactions
Recognize directional and exponential characteristics of change:

**Directional**: Systems continue in the direction of change until another change intervenes. If performance degraded after Change A, it won't spontaneously improve without Change B.

**Exponential**: Multiple simultaneous changes compound non-linearly. Two small changes might interact to produce large effects neither would cause alone.

**Interaction analysis**: If single changes don't fully explain the problem, look for combinations.

### 7. Implement Corrective Actions
Based on validated root causes:
- **Immediate**: Rollback or mitigate problematic changes
- **Short-term**: Implement monitoring/controls to detect similar changes
- **Long-term**: Update change management processes to prevent recurrence

## Example

**Scenario**: E-commerce site experiencing 3x increase in checkout failures

**Problem Definition**: Checkout success rate dropped from 95% to 68% starting Dec 5, 10:00 AM

**Baseline**: Dec 1-4, checkout success rate stable at 95%

**Change Mapping**:
- Dec 4, 11:00 PM: Deployed new payment gateway SDK v3.2 (mandated)
- Dec 5, 9:00 AM: Marketing launched email campaign, traffic +40% (mandated)
- Dec 5, 9:30 AM: Auto-scaling triggered, added 3 new server instances (caused by traffic)
- Dec 3, unknown: Payment provider updated API rate limits (natural, discovered during investigation)

**Initial Classification**:
- SDK deployment: **Correlated** (timing close, plausible connection)
- Email campaign: **Correlated** (traffic increase could stress system)
- Auto-scaling: **Contributing** (new instances might have config issues)
- Rate limit change: **Unrelated** (timing doesn't match, still under limits)

**Hypothesis Testing**:
- Rollback SDK to v3.1 in staging → checkout success returns to 95% ✓
- Apply v3.2 in isolated environment → reproduces 68% success rate ✓
- Log analysis reveals SDK v3.2 has timeout bug under load (30% failure rate at >100 req/sec) ✓

**Validated Root Cause**: Payment gateway SDK v3.2 timeout bug

**Contributing Factor**: Traffic increase from email campaign pushed system over SDK's performance threshold

**Corrective Actions**:
- Immediate: Rollback SDK to v3.1
- Short-term: Add payment gateway performance monitoring and alerts
- Long-term: Require load testing for all payment-related dependencies before production deployment

## Anti-Patterns

**Recency Bias**: Focusing only on the most recent change before failure, missing earlier changes with delayed effects. Review full timeline, not just last 24 hours.

**Narrow Scope**: Limiting change search to your own deployments, missing upstream dependency changes, infrastructure modifications, or external factors.

**Single Change Fixation**: Finding one change that correlates and stopping investigation. Multiple changes often interact; validate you've found the complete picture.

**No Baseline Validation**: Assuming baseline was "perfect" without verifying. The baseline may have had latent issues that later changes exposed.

**Change Blindness**: Missing "natural" changes like traffic growth, data volume increases, or environmental shifts because they weren't deliberate actions.

**Hypothesis Confirmation**: Searching for evidence that supports your suspected change while ignoring contradictory data. Follow evidence, not assumptions.

**Skipping Rollback Validation**: Declaring a change the root cause without actually testing if reverting it fixes the problem. Correlation isn't causation.

## Related Frameworks

- **5 Whys**: Complementary technique; use Change Analysis to identify "what changed," then 5 Whys to understand "why that change caused problems"
- **Fault Tree Analysis**: Use Change Analysis to identify suspect changes, then FTA to decompose complex failure mechanisms
- **A/B Testing**: Similar comparison logic applied proactively; Change Analysis is retrospective A/B analysis
- **Incident Timeline Analysis**: Change Analysis is specialized form of timeline analysis focused on identifying change events
- **Configuration Management**: Preventive complement; robust config management makes Change Analysis easier by tracking all changes
- **Rollback Procedures**: Operational complement; Change Analysis identifies what to roll back, procedures enable safe execution
