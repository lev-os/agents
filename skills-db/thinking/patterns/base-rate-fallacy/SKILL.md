---
name: Base Rate Fallacy
description: Ignoring statistical base rates in favor of vivid case-specific information when assessing probability
---

# Base Rate Fallacy

## Overview

The Base Rate Fallacy occurs when we ignore the underlying statistical frequency (base rate) of an event in the general population, focusing instead on specific case details that seem more relevant or vivid. This leads to systematic errors in probability judgment and risk assessment.

Discovered by Amos Tversky and Daniel Kahneman in the 1970s, the base rate fallacy stems from the representativeness heuristic—our tendency to judge likelihood based on how well something matches a mental prototype rather than actual statistical probability.

Classic example: A person fits the stereotype of a librarian (quiet, loves books, organized). Is this person more likely to be a librarian or a salesperson? Most people say librarian, ignoring that salespeople vastly outnumber librarians (~4 million vs ~150,000 in the US). Even if 90% of librarians fit this profile but only 10% of salespeople do, the sheer base rate difference means this person is still more likely to be a salesperson.

The bias is particularly dangerous in medical diagnosis, legal reasoning, hiring decisions, and risk assessment—anywhere specific case details feel compelling but base rate probabilities tell a different story.

**Key insight**: Vivid, specific information feels more relevant than abstract statistics, even when statistics are more predictive. Our minds prioritize narrative over numbers.

## When to Use

Apply Base Rate awareness in these situations:

- **Medical diagnosis**: Interpreting test results, especially for rare diseases (positive test doesn't mean you have the disease)
- **Hiring decisions**: Evaluating candidates with impressive but statistically rare profiles
- **Risk assessment**: Judging probability of terrorist attacks, plane crashes, rare crimes
- **Legal reasoning**: Assessing guilt based on circumstantial evidence (prosecutor's fallacy)
- **Investment decisions**: Evaluating startup success based on founder profiles vs. actual startup survival rates
- **Product analytics**: Interpreting user behavior patterns without considering overall usage statistics
- **Security threats**: Responding to specific threat intelligence vs. baseline threat frequency

**Trigger question**: "What's the base rate for this event in the general population, and am I properly weighting it?"

## Process

### 1. Identify the Base Rate

Before evaluating case-specific information, establish the underlying frequency:
- What percentage of the population exhibits this outcome?
- How common is this condition/event in the relevant reference class?
- What are the prior probabilities before considering new evidence?

**Action**: Look up actual statistics for the population or category you're evaluating. Don't estimate—find the number.

### 2. Gather Case-Specific Information (Likelihood)

Collect the vivid, specific details about this particular case:
- Test results, symptoms, or diagnostic indicators
- Individual characteristics, credentials, or behaviors
- Situational factors or contextual clues

**Action**: Document the specific evidence that makes this case seem distinctive or noteworthy.

### 3. Apply Bayes' Theorem (Mental or Formal)

Combine base rate with case-specific evidence using Bayesian updating:
- **Base rate**: P(hypothesis is true in general)
- **Likelihood**: P(observing this evidence | hypothesis is true)
- **False positive rate**: P(observing this evidence | hypothesis is false)
- **Posterior probability**: Updated probability after considering evidence

**Mental shortcut**: "Even if this evidence makes the hypothesis X times more likely, if the base rate is very low, the final probability may still be low."

**Action**: Calculate or estimate: (Base Rate × Likelihood) / [(Base Rate × Likelihood) + (1 - Base Rate) × False Positive Rate]

### 4. Compare Magnitude: Base Rate vs. Likelihood Ratio

Assess which dominates: the base rate or the diagnostic power of your evidence.
- **Low base rate + moderate evidence** = Still probably false (e.g., rare disease + positive test)
- **High base rate + weak counter-evidence** = Still probably true (e.g., common condition + negative test)

**Action**: Ask: "Is my evidence strong enough to overcome the prior probability?"

### 5. Seek Disconfirming Base Rates

Actively search for base rates that contradict your intuitive judgment:
- "What percentage of people with this profile actually succeed?"
- "How many times has this specific pattern led to a false alarm?"
- "What's the failure rate for things that look exactly like this?"

**Action**: Devil's advocate question: "What base rate would make me change my mind, and is that the actual base rate?"

### 6. Test with Concrete Numbers (Natural Frequencies)

Reframe probabilities as natural frequencies to make base rates more intuitive:
- Instead of: "90% test accuracy, 1% disease prevalence"
- Use: "Out of 1,000 people: 10 have the disease, 9 test positive (true positive). 990 don't have it, 99 test positive (false positive). So 108 total positives, only 9 actually have disease = 8% chance."

**Action**: Convert percentages to "out of 1,000 people" format and count concrete cases.

### 7. Create Decision Protocols That Force Base Rate Consideration

Build checklists or decision trees that require explicit base rate lookup before judgment:
- Medical diagnosis: Look up disease prevalence before interpreting symptoms
- Hiring: Review overall success rate for this candidate profile before making offer
- Security: Check historical false alarm rate before escalating threat

**Action**: Institutionalize base rate consultation as a mandatory step in high-stakes decisions.

## Example

**Scenario**: A software engineer takes a coding assessment and scores 95/100. You're deciding whether to hire them.

**Base Rate Fallacy in action**:
- **Case-specific focus**: "95/100 is excellent! This person is clearly a top performer."
- **Intuitive judgment**: High confidence they'll be a great hire
- **Ignored base rate**: What percentage of people who score 95/100 actually succeed in the role?

**Better approach using this framework**:

1. **Identify base rate**: Historical data shows 60% of hires succeed long-term at your company
2. **Gather case evidence**: This candidate scored 95/100 on the assessment
3. **Apply Bayes' Theorem**: What's the success rate for people who score 90+?
   - Your data: 90+ scorers have 80% success rate (vs. 60% overall)
   - Base rate of 90+ scorers: 20% of all candidates
4. **Compare magnitude**: Evidence is moderately strong (80% vs. 60% = 1.33x improvement), but not overwhelming
5. **Seek disconfirming base rate**: Check: What's the failure rate for 90+ scorers? Still 20% fail.
6. **Natural frequencies**: "Out of 100 people who score 90+, 80 succeed and 20 fail. This person is likely in the 80, but 1-in-5 chance they're in the 20."
7. **Decision protocol**: Require additional signal (reference checks, work sample) before making final decision, since 20% failure rate is non-trivial

**Result**: You hire with realistic expectations (80% confidence, not 95%+), and you collect additional evidence to further update your probability. This prevents overconfidence based on a single impressive data point.

## Anti-Patterns

**Ignoring base rates entirely**: Treating every case as unique and dismissing statistical patterns as "not applicable to this specific situation." Statistics exist precisely because individual cases follow aggregate patterns.

**Privileging anecdotes over data**: "I know someone who scored poorly but became a top performer" outweighs data on 1,000 cases. Singular vivid examples shouldn't override base rates.

**Assuming irrelevant base rates**: Using the wrong reference class (e.g., "startup success rate is 10%" when evaluating a well-funded Series A company with product-market fit—different base rate).

**Overcorrecting to pure base rate reasoning**: Ignoring all case-specific evidence and defaulting only to base rates. Bayes' Theorem requires combining both.

**Falling for the "prosecutor's fallacy"**: Confusing P(evidence | innocent) with P(innocent | evidence). Just because innocent people rarely exhibit this evidence doesn't mean people with this evidence are rarely innocent (depends on base rate).

**Mistaking representativeness for probability**: "This person looks exactly like a successful founder" doesn't mean they're likely to succeed if the base rate for founder success is 5%.

**Failing to update base rates with new information**: Using outdated statistics or failing to recalculate base rates as conditions change.

## Related Frameworks

- **Availability Heuristic**: Vivid case details are mentally available; abstract base rates are not, causing the bias
- **Representativeness Heuristic**: Judging probability by similarity to prototypes rather than actual frequency
- **Confirmation Bias**: Once we form a judgment based on case details, we ignore base rate evidence that contradicts it
- **Anchoring**: Initial case-specific information anchors judgment, preventing adjustment toward base rates
- **Conjunction Fallacy**: Related error where specific scenarios seem more probable than general ones (Linda the feminist bank teller)
- **Survivorship Bias**: Focusing on visible success cases while ignoring the base rate of failures
- **Bayes' Theorem**: The formal mathematical tool for correctly combining base rates with new evidence
