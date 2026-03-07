---
name: bottlenecks
description: When identifying and addressing the constraining factor yields disproportionate system improvement
tags: [systems, constraints, optimization, theory-of-constraints, engineering, operations]
---

# Bottlenecks

## Overview
The single point in a system with the lowest capacity, which limits the throughput of the entire system. Like a physical bottle where liquid flow is constrained by the narrow neck, system performance is constrained by its weakest link. Improving non-bottleneck components yields no system-level improvement; only addressing the bottleneck increases overall throughput. This principle is foundational to Theory of Constraints (Goldratt) and systems optimization.

## Core Principle
**System throughput is determined by the bottleneck capacity. Optimizing anything else is waste.**

Mathematical reality: If step A processes 100 units/hour and step B processes 50 units/hour, the system can only produce 50 units/hour regardless of improvements to step A.

## Types of Bottlenecks

### Capacity Bottlenecks
**Physical or resource constraints**
- Manufacturing: Slowest machine on assembly line
- Software: Database query performance limits request throughput
- Organizations: Single expert who must approve all decisions

### Policy Bottlenecks
**Artificial constraints from rules or processes**
- Approval workflows requiring serial sign-offs
- Batch processing when streaming would work
- Quality gates that catch non-issues

### Temporary vs. Structural Bottlenecks
**Temporary**: Load spikes (Black Friday traffic)
**Structural**: Inherent system design (single-threaded code)

## Execution Steps (Theory of Constraints)

### 1. Identify the Bottleneck
- **Measure throughput** at each stage
- **Find the slowest step** (where work queues build up)
- **Confirm with data**: Inventory/backlog accumulates before bottleneck
- **Distinguish from variability**: Random fluctuations vs. systematic constraint

**Methods**:
- Observe where WIP (work in progress) accumulates
- Measure utilization rates (bottleneck = 100% utilized)
- Process mining / value stream mapping
- Little's Law: Throughput = WIP / Lead Time

**Example**: E-commerce checkout—where do users drop off? Payment processing might be slow.

### 2. Exploit the Bottleneck
**Maximize utilization of the constraining resource**
- Eliminate downtime (no breaks, batch switching costs)
- Ensure quality inputs (don't waste bottleneck capacity on defects)
- Offload non-essential work from bottleneck
- Add buffers before bottleneck to prevent starvation

**Example**: If expert review is bottleneck, ensure only high-quality work reaches them.

### 3. Subordinate Everything Else
**Align all non-bottleneck processes to support the bottleneck**
- Don't produce faster than bottleneck can consume (creates WIP buildup)
- Batch sizes should match bottleneck capacity
- Upstream processes optimize for bottleneck success, not local efficiency

**Example**: If deployment is bottleneck, code review speed is irrelevant (don't rush poor quality).

### 4. Elevate the Bottleneck
**Increase capacity of the constraint**
- Add resources (hire, buy equipment, scale servers)
- Improve efficiency (better algorithms, training)
- Parallelize (horizontal scaling)
- Eliminate the step (do you really need it?)

**Example**: Vertical or horizontal database scaling, caching, read replicas.

### 5. Repeat (Find the New Bottleneck)
**Improving one bottleneck shifts the constraint elsewhere**
- Continuously measure system performance
- Identify the new bottleneck (it's always somewhere)
- Avoid inertia (old constraint may no longer be the constraint)

**Example**: After speeding up database, frontend rendering becomes new bottleneck.

## Anti-Patterns

**Optimizing Non-Bottlenecks**: Improving fast components while ignoring the constraint (illusion of progress)

**Local Optimization**: Maximizing departmental efficiency at expense of system throughput

**Premature Elevation**: Adding capacity before exploiting (throwing money at problem)

**Balanced Capacity**: Making all steps equal speed (expensive and fragile—any disruption creates new bottleneck)

**Ignoring Shifting Bottlenecks**: Optimizing for yesterday's constraint

## Quality Indicators

**High Signal**:
- Clear identification of single constraining factor
- Measurable throughput improvement from bottleneck changes
- WIP reduction after addressing bottleneck
- System-level metrics improve (not just local)
- Understand second-order bottlenecks

**Low Signal**:
- "Everything is a bottleneck" (haven't identified the constraint)
- Improvements with no throughput change
- Optimizing fastest components
- Ignoring utilization data
- No measurement of system-level flow

## Cross-Domain Applications

### Software Engineering
- **Database queries**: Slow query dominates response time
- **API rate limits**: Third-party service constrains throughput
- **Build times**: Compilation step limits deployment frequency
- **Single-threaded execution**: CPU-bound operations

### Product Development
- **User research**: Insights generation slower than design/engineering
- **Code review**: Senior engineers bottleneck merge rate
- **QA testing**: Manual testing limits deployment cadence

### Organizations
- **Decision-making**: Executive approval required for all projects
- **Hiring**: Interview capacity limits growth
- **Knowledge silos**: Single expert becomes dependency

### Personal Productivity
- **Energy, not time**: Willpower/focus is often the bottleneck, not hours
- **Context switching**: Interruptions limit deep work throughput
- **Learning rate**: Information processing, not availability, constrains skill growth

## Related Frameworks
- **Theory of Constraints (TOC)**: Goldratt's comprehensive methodology
- **Little's Law**: Throughput = WIP / Lead Time (quantifying flow)
- **Queueing Theory**: Mathematical analysis of bottlenecks
- **Value Stream Mapping**: Visualizing flow and identifying constraints
- **80/20 Rule (Pareto)**: Focus on the constraint yields disproportionate returns

## Scoring (42/50)
- **Practitioner Weight** (9/10): Widely used in manufacturing, DevOps, operations
- **Clarity** (9/10): Intuitive concept with clear analytical methods
- **Proven ROI** (9/10): Measurable throughput improvements
- **Novelty** (5/10): Well-established in operations management
- **Applicability** (10/10): Universal across systems (manufacturing, software, organizations, personal)

## Sources
- Eliyahu Goldratt: The Goal (Theory of Constraints novel)
- Eliyahu Goldratt: Theory of Constraints
- Gene Kim, et al.: The Phoenix Project (TOC applied to DevOps)
- John Little: Little's Law (queueing theory)
- Value Stream Mapping literature (Lean manufacturing)
- Donald Reinertsen: The Principles of Product Development Flow
