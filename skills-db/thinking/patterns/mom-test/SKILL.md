---
name: mom-test
description: Customer interview methodology that extracts truthful insights by focusing on past behavior over future intentions
---

# The Mom Test

## Overview

Rob Fitzpatrick's "The Mom Test" provides a framework for customer interviews that reveals truth rather than polite lies. The core insight: people lie to you when they think it'll make you happy, and "mom" represents the most biased interviewer possible (wants to encourage you, hates to see you hurt). The methodology's genius is that questions passing "The Mom Test" extract useful information even from someone trying to spare your feelings. The framework has three rules: talk about their life (not your idea), ask about specifics in the past (not opinions about the future), and talk less while listening more.

## When to Use

- Validating product ideas before building (avoiding false-positive feedback)
- Understanding customer problems deeply (not just surface complaints)
- Deciding which features to build next (based on real behavior, not requests)
- Assessing product-market fit truthfully (distinguishing politeness from genuine interest)
- Training teams on effective customer development interviews
- Preventing "building something nobody wants" syndrome
- Converting customer conversations into actionable insights vs. vanity validation

## The Process

### Step 1: Talk About Their Life, Not Your Idea

Don't pitch your product or describe your solution. Ask about their workflow, problems, current alternatives, and constraints. Keep your idea in your pocket. The goal is understanding their world, not selling them on yours. **Example:** BAD: "Would you use an app that helps you track expenses?" GOOD: "How do you currently track your business expenses? What's frustrating about that process?"

### Step 2: Ask About Specifics in the Past, Not Generics or Opinions About the Future

Avoid hypotheticals ("Would you...?"), generics ("I usually..."), and future promises ("I would definitely..."). Ask about specific instances that already happened. Past behavior predicts future behavior; intentions don't. **Example:** BAD: "Would you pay $50/month for this?" GOOD: "Tell me about the last time you tried to solve this problem. What did you try? How much did it cost?"

### Step 3: Talk Less, Listen More

Your job is extracting signal, not broadcasting. Ask open-ended questions, let silence work, dig deeper with "why" and "tell me more." If you're doing more than 30% of the talking, you're pitching, not learning. **Example:** After they describe a problem, resist immediately explaining your solution. Instead: "That sounds frustrating. What have you tried to fix that?"

### Step 4: Identify and Avoid the Three Types of Bad Data

Filter out (a) Compliments ("Great idea!"), (b) Fluff (generic claims, hypotheticals, future promises), (c) Ideas (their feature suggestions). These are noise, not signal. When encountered, redirect to concrete past behavior. **Example:** They say "I would definitely use this!" → Redirect: "That's encouraging. When's the last time you looked for something like this?"

### Step 5: Focus on Finding Problems, Not Validating Solutions

Don't seek permission to build. Seek understanding of whether the problem exists, how painful it is, what they currently do about it, and what constraints matter. If the problem isn't painful enough to drive current action (even bad workarounds), your solution won't matter. **Example:** Discover they spend 5 hours/week on manual process but have never tried alternatives = weak problem signal. They've already tried 3 paid tools but all failed = strong problem signal.

### Step 6: Ask for Commitments, Not Opinions

End conversations by asking for something that costs them time, money, or reputation. Real commitments (clear next meeting, intro to decision-maker, pre-order, LOI) separate real interest from politeness. Give them concrete chances to reject you. **Example:** "Can we schedule 30 minutes next week to show you a prototype?" or "Would you introduce me to your CFO who owns this budget?" vs. vague "Let's stay in touch."

### Step 7: Prepare Your "Big 3" Questions Before Each Interview

With your team, identify the 3 most important questions (not topics, but specific questions) you need answered. Write them down. Use them to guide the conversation, but don't rigidly script the interview - follow interesting threads. **Example:** Big 3: (1) How much time do they spend on X per week? (2) What tools have they tried before? (3) Who else in the company cares about solving this?

## Example Application

**Situation:** Startup building "AI-powered meeting note-taker" planning customer interviews to validate demand.

**Application:**
- Step 1: Don't demo the product. Ask: "Walk me through what happens after you finish a 1-hour client meeting. How do you capture action items?"
- Step 2: Avoid "Would you use AI note-taking?" Instead: "Tell me about the last time meeting notes caused a problem. What went wrong?"
- Step 3: After they describe their process, stay silent for 3 seconds. They'll often fill the gap with the real pain point.
- Step 4: They say "I love this idea!" → Redirect: "Thanks! How much do you currently spend on meeting tools per month?"
- Step 5: Discovered they manually type notes into Slack (painful), have tried Otter.ai but stopped after 2 weeks (weak retention signal), spend $0 on meeting tools (price sensitivity signal)
- Step 6: End with: "Can I send you early access next week and we'll do a 30-min screen share of you using it in a real meeting?"
- Step 7: Big 3 prepared: (1) Current solution and its cost, (2) Past attempts to solve this, (3) Decision-making process for buying tools

**Outcome:** Out of 20 interviews, 15 gave compliments but only 3 committed to screen share. Those 3 became design partners. Avoided building for 15 people who were just being polite.

## Anti-Patterns

- Pitching your solution instead of exploring their problem ("Let me tell you about our amazing app...")
- Asking hypothetical questions ("Would you pay for this?" "Would you switch from your current tool?")
- Accepting compliments as validation ("They said it's a great idea, we should build it!")
- Ignoring weak commitments (they won't give you their email = they won't buy)
- Talking more than listening (you learn nothing when your mouth is moving)
- Taking feature requests literally ("They asked for X so we should build X")
- Leading questions that telegraph the "right" answer ("Don't you hate how slow current tools are?")
- Not digging into past behavior ("I usually do X" → Should ask: "When's the last time you did X?")

## Related

- Jobs to Be Done - adjacent framework for understanding customer motivations
- Continuous Discovery Habits (Teresa Torres) - systematic ongoing customer interviews
- Lean Customer Development (Cindy Alvarez) - broader customer development methodology
- Deploy Empathy (Michele Hansen) - customer research interview techniques
- Product-Market Fit Measurement - Mom Test helps assess genuine PMF vs. politeness
- Validation Board - canvas for tracking assumptions tested via Mom Test interviews
- Problem Interviews vs. Solution Interviews - Mom Test applies primarily to problem discovery
