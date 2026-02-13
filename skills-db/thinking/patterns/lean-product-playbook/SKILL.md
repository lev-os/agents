---
name: lean-product-playbook
description: Systematic six-step methodology for iterating to product-market fit using the Product-Market Fit Pyramid framework
---

# Lean Product Playbook

## Overview
Dan Olsen's Lean Product Playbook provides a repeatable six-step process for achieving product-market fit. Built on the Product-Market Fit Pyramid framework, it emphasizes validating assumptions before building and iterating based on customer feedback rather than feature lists.

## Core Insight
Product-market fit happens when your product (value proposition, feature set, UX) aligns with your market (target customer, underserved needs). Most product failures stem from building before validating market assumptions.

**Framework**: Product-Market Fit Pyramid has five layers:
1. **Target Customer** (market layer)
2. **Underserved Needs** (market layer)
3. **Value Proposition** (product layer)
4. **Feature Set** (product layer)
5. **User Experience** (product layer)

## The Six-Step Lean Product Process

### Step 1: Determine Your Target Customers
Define WHO you're building for with specific segmentation. Avoid "everyone."

**Action**: Create customer personas with demographics, behaviors, and contexts.

**Example**: Not "small businesses" but "solo consultants billing $100-300K/year who manually track hours in spreadsheets."

### Step 2: Identify Underserved Customer Needs
Discover WHAT jobs customers need done that aren't being met well by existing solutions.

**Action**: Customer interviews using Jobs to Be Done framework. Ask about frustrations, workarounds, and alternatives tried.

**Question**: "Walk me through the last time you tried to [accomplish goal]. What was frustrating?"

### Step 3: Define Your Value Proposition
Articulate HOW your product addresses underserved needs better than alternatives.

**Action**: Map your benefits to customer needs. Be specific about what you do better/different.

**Format**: "For [target customer], who [statement of need], our product is a [product category] that [key benefit]. Unlike [primary competitive alternative], we [primary differentiation]."

### Step 4: Specify Your MVP Feature Set
Decide WHICH features to include in minimum viable product. Only include what's necessary to test core value proposition.

**Action**: Use MoSCoW method (Must have, Should have, Could have, Won't have). Focus on "must have."

**Rule**: If removing feature doesn't invalidate core value prop test, it's not MVP.

### Step 5: Create Your MVP Prototype
Build the LIGHTEST artifact that tests assumptions. Start with lowest fidelity possible.

**Fidelity ladder**:
- Mockups/wireframes (hours)
- Clickable prototype (days)
- Landing page + manual fulfillment (week)
- Functional MVP (weeks/months)

**Action**: Pick lowest fidelity that enables meaningful feedback.

### Step 6: Test Your MVP with Customers
Get real feedback from target customers. Measure if value proposition resonates.

**Action**: 5-8 customer interviews per iteration. Ask open questions about their experience, not "Do you like it?"

**Questions**:
- "What were you trying to accomplish?"
- "How does this compare to what you use today?"
- "Would you be disappointed if you couldn't use this anymore?"

## Iteration and Pivoting

After Step 6, analyze results:
- **Validated**: Build out features, improve UX
- **Partially validated**: Iterate on value prop or features
- **Invalidated**: Pivot to different need or customer segment

**Pivot types**:
- Customer segment pivot (same solution, different customer)
- Customer need pivot (same customer, different problem)
- Value proposition pivot (same need, different approach)

## Example Application

**Scenario**: Building project management tool for remote teams

**Step 1 - Target Customer**: Engineering managers at 10-50 person startups with fully remote teams

**Step 2 - Underserved Needs**: "Current tools feel like surveillance. We need visibility without micromanaging."

**Step 3 - Value Prop**: "Team-driven status updates that show progress without tracking time/activity."

**Step 4 - MVP Features**:
- Must: Daily async standup prompts, outcome tracking (not hours)
- Should: Slack integration
- Won't: Time tracking, activity monitoring, reporting dashboards

**Step 5 - Prototype**: Slack bot that asks 3 questions daily, posts to channel

**Step 6 - Test**: 5 teams use for 2 weeks. Interviews reveal: "Love async standups, but need way to see blockers across teams."

**Iteration**: Add "blocker board" feature, test again.

## When to Use
- Starting new product from scratch
- Adding major feature/product line
- Product struggling to gain traction (indicates PMF issues)
- Entering new market segment

## Anti-Patterns
- ❌ Skipping customer research in Steps 1-2 (building on assumptions)
- ❌ Defining features before value proposition
- ❌ Starting with high-fidelity prototypes (waste time if wrong)
- ❌ Testing with "friendly" customers who won't give honest feedback
- ❌ Asking "Would you buy this?" (hypothetical, unreliable)

## Success Metrics
- **Time to First Test**: Days from idea to customer feedback
- **Iteration Velocity**: How fast you complete test-learn-iterate cycles
- **Pivot Rate**: % of assumptions invalidated (healthy to find wrong assumptions early)
- **PMF Score**: Sean Ellis 40% test (40%+ would be "very disappointed" without product)

## Integration with Other Frameworks
**Builds on**:
- Jobs to Be Done: Use for Step 2 (identify needs)
- Continuous Discovery Habits: Weekly cadence for Steps 5-6
- The Mom Test: Question technique for Step 6

**Feeds into**:
- Opportunity Solution Trees: Map features to needs discovered
- RICE Prioritization: Prioritize features post-MVP
- Dual-Track Agile: Discovery track follows this process

## Common Pitfalls

### Building Too Much Before Testing
Most teams skip to high-fidelity prototypes. Use lowest fidelity that tests hypothesis.

### Confusing Customer Requests with Needs
Customers ask for features (solutions). Your job: uncover underlying need, find better solution.

### Testing with Wrong Customers
Don't test with people outside target segment or who won't actually use product.

### Not Iterating Fast Enough
Goal: 1-2 week iterations for Steps 4-6. Longer = more waste if assumptions wrong.

## References
- "The Lean Product Playbook" - Dan Olsen
- leanproductplaybook.com
- ProductMarketFit.com (Olsen's articles)

## Related
- jobs-to-be-done
- product-market-fit-survey
- continuous-discovery-habits
- mom-test
- dual-track-agile
- rice-prioritization
