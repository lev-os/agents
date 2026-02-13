---
name: incentives
description: Predict and shape behavior by understanding the hidden rewards and punishments that drive human action
---

# Incentives

## Overview

Incentives are the invisible forces that drive human behaviorthe carrots and sticks, rewards and punishments, that shape our choices and actions. Charlie Munger considered incentives one of the most powerful mental models, famously saying: "Never, ever think about something else when you should be thinking about incentives." People respond predictably to incentive structures, often in ways that surprise system designers. Understanding incentives means understanding behavior; shaping incentives means shaping outcomes.

## When to Use

- **Organizational design**: Structuring compensation, promotions, and recognition systems
- **Investment analysis**: Evaluating management decisions by examining what they're incentivized to do
- **Negotiation**: Understanding what the other party truly wants beyond stated positions
- **Culture building**: Aligning team behavior with company values through reinforcement structures
- **Problem diagnosis**: When outcomes don't match intentions, audit the incentive system
- **Product design**: Creating user behavior loops through reward mechanisms

## The Process

### Step 1: Identify Stated vs. Actual Incentives
What are people officially supposed to do? What are they actually rewarded or punished for? The gap reveals the true incentive structure.

**Example**: Company says "we value quality" but promotes managers who ship fastest, regardless of bugs. Actual incentive: Speed over quality.

### Step 2: Map All Stakeholders and Their Incentives
List every party involved and what they optimize for. Don't assume everyone shares your goals.

**Example**: Real estate transaction
- Buyer: Lowest price, best value
- Seller: Highest price, quick close
- Buyer's agent: Commission = 3% of price, wants higher price + fast close
- Seller's agent: Same incentives as buyer's agent
- Lender: Closing loan, doesn't care about price
- Inspector: Finding problems (justifies fee, repeat business from agents)

Surprise: Your agent is incentivized to close quickly at slightly higher price, not negotiate hardest for you.

### Step 3: Predict Behavior Based on Incentives
Given these incentives, how will each party behave? Ignore what they say; predict based on what they're rewarded for.

**Example**: Sales team paid on bookings (signed contracts) not revenue (collected payments). Prediction: They'll discount heavily to close deals, promise features that don't exist, and hand off bad-fit customers to support. Result: High churn, low profitability.

### Step 4: Test for Perverse Incentives
Look for unintended consequences where incentives produce opposite of desired outcome.

**Classic examples**:
- Cobra bounty in colonial India: Paid per dead cobra, people started breeding cobras to kill for bounty
- Wells Fargo quotas: Pressure to open accounts led to millions of fraudulent accounts
- Lines of code metrics: Developers write verbose, inefficient code to hit targets

### Step 5: Redesign Incentives to Align with Goals
Change the structure to reward desired outcomes, not easy-to-game proxies.

**Framework**: Incentivize outcomes, not activities. Measure impact, not motion.

**Example**: Instead of "support team measured by tickets closed per hour" (incentivizes rushing, not helping), use "customer satisfaction scores + first-contact resolution rate" (incentivizes actually solving problems).

### Step 6: Install Countermeasures Against Gaming
People will find creative ways to exploit any incentive system. Build in checks.

**Strategies**:
- Multiple metrics (hard to game all simultaneously)
- Spot audits for quality
- Reputation systems (long-term consequences)
- Skin in the game (share downside risk, not just upside)
- Cultural norms that shame gaming

## Example Application

**Scenario**: SaaS company struggling with customer churn after rapid growth

**Step 1 - Stated vs. actual**:
- Stated: "Customer success is our priority"
- Actual incentives: Sales paid on new bookings, not net revenue. Customer success team measured on renewal rate, but bonuses based on upsells.

**Step 2 - Stakeholder incentives**:
- Sales: Close deals fast, hit quarterly quota, promise anything
- CS: Keep customers from canceling, push expensive upgrades
- Product: Ship features sales promised (reactive), not what customers need
- Executives: Show growth metrics to investors (vanity metrics)

**Step 3 - Predicted behavior**:
- Sales will close bad-fit customers who churn in month 2-3
- CS will discount renewals to prevent churn (hides problem)
- Product will build one-off features for big customers (no leverage)
- Execs will celebrate new logos, ignore unit economics

**Step 4 - Perverse incentives found**:
- Paying sales on bookings incentivizes selling to anyone, even poor fits
- Measuring CS on renewal rate incentivizes discounting, not value delivery
- Product roadmap driven by loudest customer, not strategic vision

**Step 5 - Redesign**:
- Sales: 50% commission on booking, 50% on customer hitting 12-month mark (aligns with customer success)
- CS: Bonuses tied to NPS and expansion revenue from happy customers, not preventing cancellations
- Product: Measured on feature adoption rates and customer-reported value, not shipped features
- Execs: Report on cohort retention curves and LTV:CAC ratio, not just new logos

**Step 6 - Countermeasures**:
- Quarterly "ideal customer profile" fit score for new deals (penalize sales for bad fits)
- CS shares customer feedback in all-hands (social pressure against gaming)
- Product requires business case showing cross-customer value before building features
- Finance tracks true revenue (not bookings) as primary growth metric

**Result**: Churn drops from 8%/month to 3%/month over 6 months. Slower new logo growth, but higher quality customers. LTV increases 3x. Team aligned on sustainable growth.

## Anti-Patterns

**Assuming goodwill trumps incentives**: "Our team is mission-driven, they won't game the system." False. Even well-intentioned people respond to incentives. Design as if people will optimize for personal benefit, because they will.

**Single-metric optimization**: Any single KPI becomes the target and stops being useful (Goodhart's Law). Use balanced scorecards with competing tensions.

**Ignoring status and identity incentives**: Not all incentives are monetary. Recognition, titles, belonging, and autonomy often drive behavior more than cash.

**Complex incentive schemes**: If people can't explain how they're compensated, they can't optimize for it. Complexity creates confusion, not alignment.

**Static incentives in dynamic environments**: What worked last quarter may be wrong this quarter. Markets change, strategies evolveincentives must adapt.

**Incentivizing the wrong people**: Rewarding executives for stock price while individual contributors get pizza parties. Misalignment breeds cynicism.

## Related Frameworks

- **Principal-Agent Problem**: Misaligned incentives between decision-makers (agents) and those affected (principals)
- **Moral Hazard**: When people take risks because they don't bear the full consequences (incentive mismatch)
- **Tragedy of the Commons**: Individual incentives to exploit shared resources destroy collective value
- **Hanlon's Razor**: Before assuming malice, check if bad behavior is simply responding to perverse incentives
- **Second-Order Thinking**: Incentive changes create ripple effectspredict downstream consequences
- **Goodhart's Law**: When a measure becomes a target, it ceases to be a good measure (incentive gaming)
- **Skin in the Game**: Aligning incentives by ensuring decision-makers share in both upside and downside
