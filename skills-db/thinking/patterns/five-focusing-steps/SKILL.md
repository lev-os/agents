---
name: Five Focusing Steps
description: A systematic methodology for identifying and eliminating system constraints to maximize throughput, based on Eliyahu Goldratt's Theory of Constraints
---

## Overview

The Five Focusing Steps are the core methodology of the Theory of Constraints (TOC), introduced by Eliyahu Goldratt in his 1984 book "The Goal". This framework provides a cyclical process for continuously improving system performance by identifying bottlenecks (constraints) and systematically removing them.

The fundamental insight: every system has exactly one constraint at any given time that limits its performance. Total process throughput can only be improved when that constraint is improved. Rather than trying to optimize everything simultaneously, focus your efforts on the single limiting factor.

This framework is applicable to manufacturing, software development, operations, strategic planning, and any domain where throughput matters. It's particularly powerful because it prevents wasted effort on non-constraints while ensuring maximum leverage from improvement activities.

## When to Use

Apply the Five Focusing Steps when:

- System throughput is below desired levels and you need to identify what's holding you back
- Multiple improvement opportunities exist but resources are limited (focus question: "what will have the biggest impact?")
- Teams are busy optimizing non-bottleneck activities while the real constraint goes unaddressed
- You've implemented one improvement and need to systematically identify the next constraint
- Performance gains from previous improvements have plateaued (signal: the constraint has shifted)
- Cross-functional conflicts arise about where to invest resources (this provides objective prioritization)

Don't use this framework for:

- Problems that aren't throughput-related (e.g., quality issues that don't affect flow)
- Situations where constraints are policy-based or cultural rather than capacity-based (use other TOC thinking processes)
- One-time projects without ongoing flow (though the identify-exploit-subordinate logic still applies)

## Process

### Step 1: Identify the Constraint

**Find the bottleneck.** The constraint is the resource or step with the longest queue, highest utilization, or smallest capacity relative to demand.

In manufacturing: look for inventory piling up before a workstation. In software: find the team/service with the longest backlog. In sales: identify the stage where deals stall most frequently.

Use data: measure cycle time, queue depth, utilization rates, and throughput at each stage. The constraint will be obvious from the metrics—it's where work accumulates.

### Step 2: Exploit the Constraint

**Maximize output from the bottleneck using only existing resources.** Don't spend money yet. Get everything possible from what you already have.

Tactics: eliminate downtime (breaks, changeovers), reduce waste (defects, rework), optimize scheduling (batch similar work), remove distractions (meetings, interruptions).

For a constrained production line: keep it running during breaks by staggering worker schedules. For a constrained engineering team: protect their time ruthlessly, eliminate meetings, provide perfect handoffs.

Key principle: every minute lost at the constraint is a minute lost for the entire system forever. An hour saved at a non-constraint is worthless.

### Step 3: Subordinate Everything Else

**Align all non-constraint resources to support the constraint's maximum throughput.** Synchronize the entire system to the rhythm of the bottleneck.

This often feels counterintuitive: upstream teams may sit idle waiting for the constraint. This is correct. Non-constraints running at 100% create inventory, not throughput.

Example: If your constraint can process 100 units/day, upstream processes should produce exactly 100 units/day, no more. Overproduction creates work-in-progress inventory that hides problems and slows feedback.

Set policies: "Don't start new work unless the constraint has capacity to process it." This prevents queue overload and maintains system flow.

### Step 4: Elevate the Constraint

**Add resources to increase constraint capacity.** Now you can spend money: hire people, buy equipment, add servers, expand space.

Only take this step after fully exploiting and subordinating. Why? Because Steps 2-3 might eliminate the constraint entirely without capital investment. Many "constraints" are actually mismanagement of existing capacity.

Calculate ROI carefully: how much additional throughput will this investment create? Compare against the value of that throughput. If the constraint processes $10M/year and you can increase capacity 20% for $500K, the math is obvious.

### Step 5: Prevent Inertia—Return to Step 1

**When the constraint breaks, a new constraint appears immediately.** Don't rest. Systems always have constraints—that's the nature of systems.

Critical: elevating a constraint often shifts it to an unexpected location. Your manufacturing line might now be constrained by raw material delivery, or sales capacity, or product design throughput.

Beware inertia: policies designed to support the old constraint can become the new constraint. If you built processes around protecting Machine A's uptime, but Machine B is now the bottleneck, those policies are now harmful.

Repeat the cycle continuously. The Five Focusing Steps are not a one-time fix but a continuous improvement methodology.

## Example

**Software deployment bottleneck:**

1. **Identify**: Dev team ships 50 features/month, but QA can only test 30/month. QA is the constraint.

2. **Exploit**: Improve test efficiency with better test data, eliminate duplicate test runs, prioritize high-value features first, batch similar tests. QA now tests 38/month without adding people.

3. **Subordinate**: Dev team reduces output to 38 features/month. "Excess" dev time goes to writing better tests, improving documentation, reducing defects that waste QA time. This feels wrong but prevents untested feature pile-up.

4. **Elevate**: Hire 2 more QA engineers. QA capacity increases to 60/month. QA is no longer the constraint.

5. **Return to Step 1**: New constraint emerges—deployment pipeline can only handle 45 deploys/month. Infrastructure is now the bottleneck. Begin cycle again.

## Anti-Patterns

**Optimizing non-constraints**: Increasing dev team from 10 to 15 people when QA is already overloaded just creates a bigger backlog. Feels productive ("we're shipping more code!") but reduces system throughput (more untested features, longer feedback cycles).

**Skipping exploitation/subordination and jumping to elevation**: Buying expensive equipment before maximizing existing capacity. This is the most common mistake—capital spending feels like progress, but optimization is free.

**Running non-constraints at 100% utilization**: "Keep everyone busy" creates inventory buildup, hides variability, and obscures the actual constraint. Idle time at non-constraints is healthy and necessary.

**Maintaining old policies after the constraint shifts**: "We must always prioritize Machine A" made sense when it was the bottleneck. Now it's harmful. Inertia kills continuous improvement.

**Treating symptoms instead of constraints**: Adding buffers, expediting orders, working overtime—these address consequences, not causes. Find and fix the actual constraint.

**Declaring victory after one cycle**: Elevating one constraint doesn't eliminate constraints from your system. They just move. The work is never done.

## Related Frameworks

- **Throughput Accounting** (TOC): Financial metrics aligned with constraint management
- **Drum-Buffer-Rope** (TOC): Scheduling system based on constraint rhythm
- **Critical Chain Project Management** (TOC): Applies constraint thinking to project management
- **Lean Manufacturing**: Shares focus on flow and waste elimination, different methodology
- **Value Stream Mapping** (Lean): Visual tool for identifying constraints in process flows
- **Bottleneck Analysis** (Operations Research): Mathematical approach to constraint identification
- **Current Reality Tree** (TOC): Diagnostic tool for identifying root cause constraints
- **System Dynamics**: Mathematical modeling of constraints and feedback loops
