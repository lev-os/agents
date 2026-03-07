---
name: availability-heuristic
description: Correct probability and frequency judgments distorted by mentally available examples by seeking base rate data before relying on vivid anecdotes
---

# Availability Heuristic

## Overview
The availability heuristic, discovered by Amos Tversky and Daniel Kahneman in 1973, is a cognitive shortcut where people judge the probability or frequency of events based on how easily examples come to mind rather than actual statistical data. Vivid, recent, or emotionally charged events are more mentally "available," leading to systematic bias: we overestimate shark attacks (dramatic, memorable) and underestimate heart disease (common but mundane). This heuristic is efficient but predictably wrong when mental availability diverges from reality.

## When to Use
- Assessing risks or making safety decisions (travel, health, security)
- Evaluating frequency of business events (customer complaints, bugs, churn)
- Making investment decisions influenced by recent news
- Noticing you're disproportionately worried about rare but vivid threats
- Media coverage is shaping your perception of what's common vs. rare
- You need to justify probability estimates with actual data

## The Process

### Step 1: Recognize When You're Using Availability
Notice when your probability judgment is based on "I can easily think of examples" rather than data. Red flags: recency ("just saw a news story"), vividness ("that was dramatic"), or personal experience ("happened to my friend").

**Example:** After seeing news about a plane crash, thinking "Air travel is dangerous" despite aviation being statistically the safest transport mode.

### Step 2: Question the Source of Mental Availability
Ask: "Why is this example so easy to recall? Is it because it's frequent, or because it's vivid/recent/emotional?" Media coverage, personal experience, and drama all increase mental availability independent of actual frequency.

**Example:** Tversky & Kahneman's "K" experiment: People think more English words start with "K" than have "K" as the third letter, because "kangaroo" comes to mind faster than "acknowledge"—but the reverse is true.

### Step 3: Seek Base Rate Data
Before making a judgment, actively look up actual frequency or probability statistics. Replace "easily recalled examples" with hard numbers, incidence rates, or historical frequency.

**Example:** Instead of judging risk based on news stories, look up CDC data: Heart disease kills 650,000 Americans annually; sharks kill <1. You're 650,000x more likely to die from heart disease.

### Step 4: Adjust for Known Availability Biases
Systematically discount mentally available examples:
- Discount recent events (recency bias)
- Discount personal experiences (small sample size)
- Discount dramatic/emotional events (media selection effect)
- Discount vivid imagery (salience effect)

**Example:** A VC sees two startups fail in AI space this month (vivid, recent). Before concluding "AI startups are risky," check base rate: What percentage of AI startups in portfolio failed over 5 years?

### Step 5: Create Counter-Examples
Deliberately generate examples that contradict your initial availability-based judgment. Force your brain to surface the non-salient but statistically dominant cases.

**Example:** If you think "customers are always complaining about feature X," actively count: How many customers used feature X without complaining? 10,000 used it, 47 complained = 0.47% complaint rate, not "always."

## Example Application

**Situation:** A product manager thinks "login bugs are our biggest technical problem" after seeing 3 support tickets about login issues in one week.

**Application:**
- **Step 1 (Recognize)**: PM realizes judgment is based on "I just saw these tickets" (recency + vividness)
- **Step 2 (Question source)**: Why are login bugs so memorable? Because they block all access (high impact), not because they're frequent
- **Step 3 (Seek data)**: Pull analytics: Login bugs = 3 tickets out of 2,847 total tickets this week (0.1%). Search bugs = 421 tickets (14.8%). Payment bugs = 217 tickets (7.6%)
- **Step 4 (Adjust)**: Discount the 3 login tickets because they were recent and visible, not representative
- **Step 5 (Counter-examples)**: Generate non-salient cases: 150,000 successful logins happened without tickets

**Outcome:** PM correctly prioritizes fixing search functionality (15% of tickets) over login (0.1% of tickets), improving experience for 42x more users.

## Anti-Patterns
- ❌ Completely ignoring vivid examples (they might be early warning signals of emerging issues)
- ❌ Over-correcting by only trusting statistics and dismissing all qualitative data
- ❌ Assuming "everyone knows" base rates (most people don't look them up)
- ❌ Using availability heuristic for unique/unprecedented events where no base rate exists
- ❌ Treating all anecdotes equally (a single extreme outlier can be valuable signal)
- ❌ Forgetting that availability is adaptive in some contexts (e.g., remembering which foods made you sick)

## Related
- confirmation-bias
- base-rate-fallacy
- anchoring
- gamblers-fallacy
- framing-effects
