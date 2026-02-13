---
name: friction
description: Identify and manipulate resistance forces to either remove drag from desired behaviors or add obstacles to prevent unwanted ones
---

# Friction

## Overview

Friction is the force that resists motion between surfaces in contact. In physics, friction removes energy from systems over time through heat dissipation. As a mental model, friction represents any process or obstacle that resists progress toward goals. High friction makes actions difficult (drag, resistance, complexity). Low friction makes actions easy (flow, efficiency, simplicity). The key insight: Human behavior follows the path of least resistance. Want more of something? Reduce friction. Want less? Add friction. This applies to product design (UX removes barriers to conversion), operations (processes either enable or obstruct), and personal productivity (environment shapes behavior). Strategic friction management beats willpower.

## When to Use

- **Product design**: Optimizing user flows by removing barriers to core actions
- **Operations improvement**: Eliminating bureaucratic drag from value-creating work
- **Behavior change**: Making desired habits easy and undesired habits hard
- **Sales optimization**: Reducing purchase friction (forms, steps, decisions)
- **Team productivity**: Removing blockers that slow down shipping
- **Security design**: Adding intentional friction to prevent mistakes
- **Change management**: Understanding resistance to organizational changes

## The Process

### Step 1: Map Current Friction Points
Identify where resistance exists in the system. Track energy loss between intention and execution.

**Friction audit questions**:
- Where do people drop off in funnels (purchase, signup, onboarding)?
- What complaints include "it's too hard to..." or "why do I have to..."?
- Which processes take 10x longer than they should?
- Where do errors, delays, or rework occur frequently?
- What requires excessive approvals, steps, or coordination?

**Example**: E-commerce checkout - users must create account, verify email, enter billing + shipping separately, select shipping method, apply coupon code, review order, confirm. Each step = friction = abandonment risk.

### Step 2: Classify Friction as Good or Bad
Not all friction is wasteful. Some resistance serves valuable purposes (safety, quality, intentionality).

**Bad friction** (remove):
- Unnecessary steps that add no value
- Complex interfaces requiring mental effort
- Bureaucratic approval chains
- Redundant data entry
- Waiting for responses/handoffs
- Unclear instructions causing confusion

**Good friction** (keep/add):
- Confirmation steps preventing costly mistakes ("Are you sure you want to delete?")
- Quality gates catching defects
- Cooling-off periods for big decisions
- Authentication protecting sensitive data
- Review processes ensuring compliance

**Example**: Bank wire transfer has high friction (confirmations, delays) - this is good friction preventing fraud. Social media posting has low friction - sometimes bad (enables thoughtless posts).

### Step 3: Eliminate Bad Friction Systematically
For resistance that serves no purpose, remove it completely or reduce to minimum viable friction.

**Tactics for friction removal**:
- **Reduce steps**: Combine, eliminate, or automate steps
- **Pre-fill data**: Use defaults, saved information, smart predictions
- **Remove decisions**: Provide recommended path, not complex choices
- **Simplify interfaces**: Clear labels, obvious next actions
- **Automate handoffs**: Systems trigger next steps without human routing
- **Eliminate waiting**: Async processes, instant feedback

**Framework - The One-Click Rule**: Can you reduce friction to a single action? (Amazon 1-Click, Apple Pay, OAuth login)

**Example**: Slack's invite flow
- Before: Admin sends invite → user receives email → clicks link → creates account → verifies email → joins workspace (6 steps, high friction)
- After: Admin shares invite link → user clicks → instantly in workspace (2 steps, low friction)

### Step 4: Add Strategic Friction to Prevent Bad Outcomes
For undesired behaviors, intentionally increase resistance to make them harder.

**When to add friction**:
- Preventing destructive actions (delete, cancel, irreversible changes)
- Slowing impulsive decisions (emotional purchases, hasty replies)
- Enforcing quality standards (code reviews, testing requirements)
- Protecting sensitive operations (admin access, financial transfers)
- Breaking addictive patterns (social media, notifications)

**Tactics for adding friction**:
- **Confirmation steps**: "Type DELETE to confirm"
- **Cooling-off periods**: 24-hour holds on account cancellations
- **Manual overrides**: Require human approval for edge cases
- **Reduced availability**: Limit access (no work email on phone)
- **Increased distance**: Put distractions physically further away

**Example**: Twitter's "Are you sure you want to send this reply?" prompt (added friction to reduce toxic posts sent in anger).

### Step 5: Optimize Friction Gradient - Path of Least Resistance
Design systems so desired path has lowest friction, alternatives have progressively higher resistance.

**Principle**: Humans naturally flow toward easiest option. Shape the terrain.

**Example - Subscription cancellation**:
- **Desired path (keep subscription)**: Zero friction, auto-renew
- **Alternative 1 (downgrade plan)**: Low friction, one-click downgrade option
- **Alternative 2 (pause account)**: Medium friction, requires form + reason
- **Alternative 3 (cancel)**: High friction, buried in settings, requires phone call or multiple confirmations

User flows downhill (least resistance) by default. Only highly motivated users climb friction gradient to cancel.

### Step 6: Measure Friction Impact - Conversion and Throughput
Track metrics to validate friction changes. Reduced friction should increase flow; added friction should decrease unwanted behavior.

**Metrics**:
- **Conversion rates**: % completing desired action (signup, purchase, task)
- **Time-to-complete**: Duration from start to finish
- **Drop-off points**: Where users abandon (friction too high)
- **Error rates**: Mistakes due to confusion (poor UX friction)
- **Support tickets**: Requests for help (indicates friction)

**Example**: Reducing checkout from 5 pages to 1 page → conversion rate increases from 2% to 5% (friction reduction = 2.5x improvement).

## Example Application

**Scenario**: SaaS company has great product but struggles with low trial-to-paid conversion (15%). Users sign up but don't experience value before trial ends.

**Step 1 - Map friction**:
- Signup requires credit card upfront (psychological friction)
- Onboarding has 8-step tutorial (cognitive friction)
- Users must integrate 3rd party tools to see value (technical friction)
- No guidance on what to do first (decision friction)
- Trial expires in 7 days with no reminders (time friction)

**Step 2 - Classify**:
- **Bad friction**: Credit card requirement, 8-step tutorial, unclear first steps
- **Good friction**: Integration requirement (necessary for product value)

**Step 3 - Eliminate bad friction**:
- Remove credit card requirement for trial (psychological barrier removed)
- Replace 8-step tutorial with interactive 2-minute walkthrough (cognitive load reduced)
- Add "Recommended first action" button on dashboard (decision friction eliminated)
- Send progress emails at day 1, 3, 5 with tips (guidance reduces confusion)
- Extend trial to 14 days (time pressure reduced)

**Step 4 - Add strategic friction** (none needed - want users to convert, not prevent action)

**Step 5 - Optimize gradient**:
- **Easiest path**: Click "Recommended first action" → guided flow → immediate value
- **Medium path**: Explore features randomly (higher friction but discoverable)
- **Hard path**: Read docs, configure manually (highest friction, expert users)

**Step 6 - Measure**:
- Before: 15% conversion, 3.5 avg actions per trial user
- After: 32% conversion, 8.2 avg actions per trial user
- Friction reduction → 2x conversion improvement

**Result**: By systematically removing bad friction from value discovery, trial users experience product benefits faster, leading to higher paid conversion.

## Anti-Patterns

**Optimizing wrong friction**: Reducing friction on low-value activities while high-value paths remain blocked.

**Removing all friction**: Zero friction can be dangerous (no safeguards against mistakes, no quality control, impulsive bad decisions).

**Ignoring perception friction**: Even if technically easy, if users perceive something as difficult, it creates friction. Psychology matters as much as mechanics.

**Adding accidental friction**: Poorly designed processes that create drag unintentionally (bad UX, unclear instructions, broken flows).

**Friction blindness**: Not seeing friction because you're familiar with the system. Users experience it fresh every time.

**Fighting friction with willpower**: Trying to overcome systemic friction through personal discipline. Redesign the system instead.

## Related Frameworks

- **Activation Energy**: Initial friction barrier to starting new behavior
- **Nudge Theory**: Small friction changes that guide behavior
- **Path of Least Resistance**: Humans flow toward lowest-friction options
- **Lean Thinking**: Eliminate waste (friction) from value streams
- **User Experience (UX)**: Design discipline focused on friction reduction
- **Habit Formation**: Reduce friction for desired habits, increase for bad habits
- **Choice Architecture**: Structuring options to shape decisions through friction gradients
- **Default Effect**: Zero-friction option becomes most common choice
