---
name: daci-framework
description: Decision-making framework clarifying who drives, approves, contributes to, and gets informed about decisions
---

# DACI Decision-Making Framework

## Overview

DACI, developed at Intuit in the 1980s as a variant of RACI, is a responsibility assignment framework specifically designed for decision-making clarity. The critical insight: most group decisions fail not from bad ideas but from unclear accountability. DACI assigns four distinct roles - Driver (shepherds process), Approver (single decision-maker), Contributors (provide input), Informed (receive updates) - with the game-changing constraint that there's exactly ONE Approver. This eliminates "decision by committee" paralysis, reduces meeting overhead, and ensures someone is accountable for making the call by the deadline.

## When to Use

- Making important decisions with multiple stakeholders but unclear ownership
- Preventing "too many cooks" syndrome where everyone has veto power
- Accelerating decision velocity in fast-paced environments
- Clarifying who has voice (Contributors) vs. vote (Approver) vs. execution responsibility (Driver)
- Onboarding stakeholders to a decision process transparently
- Resolving pre-existing confusion about who makes the final call
- Documenting decision authority for future reference

## The Process

### Step 1: Identify the Decision to Be Made

Define the specific decision requiring clarity. Frame it as a question with clear alternatives or approval threshold. Determine deadline for decision. Assess decision importance and reversibility. **Example:** "Should we migrate to microservices architecture?" (major, hard-to-reverse) vs. "Should we add dark mode?" (minor, reversible).

### Step 2: Assign the Driver (One Person)

Select someone to shepherd the decision process - not necessarily the subject-matter expert or most senior person, but whoever will corral stakeholders, gather information, and drive to resolution by deadline. Driver doesn't make the decision but owns the process. **Example:** Product Manager drives product decisions, Engineering Manager drives technical architecture decisions, even if they don't approve.

### Step 3: Assign the Approver (Exactly One Person)

Identify the single person with authority and context to make the final call. Only one Approver per decision - multiple approvers creates decision paralysis. Approver should have accountability for outcomes. If multiple approvers seem necessary, the decision should be broken into smaller decisions. **Example:** CTO approves build-vs-buy for infrastructure, VP Product approves roadmap prioritization.

### Step 4: Identify Contributors (Subject-Matter Experts)

List people with relevant expertise, data, or perspectives who should provide input. Contributors have "voice but not vote" - they're consulted and can make recommendations, but don't make final decision. Keep list focused on essential input sources. **Example:** For architecture decision - lead engineers, security team, SRE team, data team contribute technical perspectives.

### Step 5: Identify Informed (Affected Stakeholders)

List people whose work will be affected by the decision and need to know outcome, but don't need to contribute to making it. "No voice, no vote" - they're notified after decision is made. Over-including people as Informed creates noise; limit to those genuinely impacted. **Example:** For architecture change - customer success team (may affect support), sales team (may affect positioning), marketing (may affect messaging).

### Step 6: Run the Decision Process

Driver collects input from Contributors, synthesizes information, presents options to Approver with recommendation. Approver makes decision by deadline. Driver communicates decision to Informed group with rationale. Document decision and DACI roles for future reference. **Example:** Driver creates decision doc, runs 2 input sessions with Contributors, presents 3 options to Approver, Approver chooses, Driver emails Informed group.

### Step 7: Execute and Iterate

After decision is made, Driver ensures execution begins. Monitor outcomes. If decision proves wrong and is reversible, iterate quickly. If irreversible, document learnings for future decisions. Review whether DACI roles were correct for this type of decision. **Example:** Track metrics post-decision, run retrospective at 30 days, adjust DACI template for similar future decisions.

## Example Application

**Situation:** SaaS company debating whether to build in-house analytics or buy third-party tool. Decision dragging for 3 months across 15 stakeholders with weekly meetings and no resolution.

**Application:**
- Step 1: Decision = "Build custom analytics vs. buy Segment/Amplitude by end of month"
- Step 2: Driver = VP Engineering (owns process, gathering info, driving to decision)
- Step 3: Approver = CTO (single decision-maker, accountable for technical strategy)
- Step 4: Contributors = Lead Data Engineer (technical feasibility), Product Manager (feature requirements), Finance (cost analysis), Customer Success (customer requests)
- Step 5: Informed = Engineering team (implementation work), Product team (roadmap planning), Sales (positioning)
- Step 6: Driver ran 2 working sessions with Contributors over 1 week, created decision memo with build cost ($500K, 6 months) vs. buy cost ($100K/year), presented to CTO, CTO approved "buy Amplitude" decision, Driver notified Informed group
- Step 7: Implemented Amplitude in 2 weeks, tracked adoption, retrospective confirmed faster time-to-value

**Outcome:** Decision made in 1 week vs. 3+ months of previous drift, stakeholder satisfaction increased (clarity on roles), 15-person weekly meeting eliminated, engineering team freed for product work.

## Anti-Patterns

- Multiple Approvers creating "veto power gridlock" (defeats single-decision-maker purpose)
- Driver is also Approver (same person shepherding and deciding can create bias)
- Too many Contributors (every stakeholder becomes contributor, drowning signal in noise)
- Confusing "Informed" with "Contributor" (over-including people who then expect input rights)
- No documented DACI roles (verbal agreement leads to future confusion about "I thought I approved this")
- Approver delegates decision back to group (defeats accountability)
- Driver doesn't actively drive (waits for consensus instead of forcing decision by deadline)
- Using DACI for trivial decisions (overhead not worth it for reversible, low-stakes calls)

## Related

- RACI Matrix (Responsible, Accountable, Consulted, Informed) - predecessor focused on task execution
- RAPID Framework (Recommend, Agree, Perform, Input, Decide) - Bain's alternative decision framework
- Decision Records (ADRs) - documentation format for decisions and rationale
- High Output Management - managerial leverage through clear decision authority
- Delegation Levels - spectrum from "tell me what to do" to "no need to tell me"
- OKRs - goal-setting framework that needs decision clarity for execution
- Eisenhower Matrix - prioritizes decisions, DACI clarifies who makes them
