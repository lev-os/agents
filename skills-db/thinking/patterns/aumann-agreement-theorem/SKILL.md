---
name: Aumann's Agreement Theorem
description: Two rational Bayesian agents with the same prior beliefs cannot agree to disagree if their posterior beliefs are common knowledge
---

# Aumann's Agreement Theorem

## Overview

**Counterintuitive theorem about rational disagreement**: Two rational Bayesian agents with the same prior beliefs cannot "agree to disagree" about any probability if their posterior beliefs are common knowledge.

**Core insight**: Honest, persistent disagreement between equally informed rational agents is mathematically impossible—if disagreement persists, it reveals differing priors, hidden information, or irrationality.

**Source**: Robert Aumann (1976), popularized by rationality community and economics

## The Framework

### The Formal Statement

If two Bayesian agents:
1. Have **common priors** (started with same initial beliefs)
2. Have **common knowledge** of each other's posterior beliefs
3. Are **rational** (update beliefs via Bayes' theorem)

Then their posterior probabilities for any event must be **identical**.

In simpler terms: "Rational agents with common priors cannot agree to disagree."

### What "Common Knowledge" Means

**Not just**: Both know each other's beliefs.

**But**: Both know that both know, and both know that both know that both know, and so on infinitely.

This is a very strong requirement—most real disagreements don't achieve this.

### The Paradox

In practice, rational, intelligent people disagree constantly about everything from politics to product strategy.

**Aumann's theorem says**: These disagreements must stem from:
- Different priors (different starting assumptions about the world)
- Information asymmetry (one person knows something the other doesn't)
- Lack of common knowledge (beliefs aren't fully transparent)
- Irrationality (not updating properly on evidence)
- Dishonesty (strategic misrepresentation of beliefs)

## When to Use

**Diagnostic tool for disagreements**:
- When two smart people reach different conclusions from "the same" information
- Debugging why consensus isn't emerging despite discussion
- Identifying hidden assumptions causing conflict
- Detecting information asymmetries in teams

**Signal of deeper issues**:
- Persistent disagreement after extensive discussion suggests different priors or hidden info
- Quick convergence after sharing beliefs suggests good Bayesian updating
- Unwillingness to share beliefs or update suggests motivated reasoning

**Not applicable when**:
- Disagreement is about values/preferences (not factual beliefs)
- Participants aren't trying to be rational (political posturing)
- Common knowledge is impossible (too complex to fully share models)

## Implementation Steps

### 1. Make Beliefs Explicit

Transform vague disagreement into quantified probabilities:

**Bad**: "I think this feature will succeed" vs. "I think it will fail"

**Good**: "I'm 70% confident this feature increases engagement" vs. "I'm 30% confident"

Now you have quantified disagreement to investigate.

### 2. Check for Common Priors

Ask: "What did we believe before looking at this specific evidence?"

**If priors differ**: Disagreement is explained—trace back to source of divergent priors
- "I've seen 10 similar features fail; you've seen 5 succeed"
- "I weight user interviews heavily; you weight quantitative data heavily"

**If priors match**: Information asymmetry or updating errors must explain disagreement.

### 3. Exchange Information

Share all evidence and reasoning that informed your posterior belief:
- "I updated from 50% to 70% because user testing showed 40% engagement lift"
- "I updated from 50% to 30% because last 3 similar features saw 20% initial lift but returned to baseline in 2 weeks"

**Ideal outcome**: As you share, beliefs should converge toward a common value.

### 4. Update on Each Other's Beliefs

**Key insight**: Your disagreement partner's posterior is itself evidence.

If someone equally rational sees the same data and reaches a different conclusion, that difference is information:
- "Why would they believe 30% if they have the same data I do?"
- "Perhaps they weighted evidence differently—that weighting is itself a signal"
- "Their 30% should move my 70% somewhat toward middle"

### 5. Identify Asymmetries

If beliefs don't converge, systematically check:

**Information asymmetry**:
- "What do you know that I don't?"
- "What analysis did you run that I haven't seen?"

**Model asymmetry**:
- "What framework are you using to interpret this data?"
- "What assumptions are built into your reasoning?"

**Prior asymmetry**:
- "What historical patterns are you pattern-matching to?"
- "What base rates are you anchoring on?"

### 6. Converge or Diagnose

**If beliefs converge**: Aumann was right—you were rational Bayesians who just needed to share information.

**If beliefs don't converge**: You've identified a non-Aumann condition:
- **Different priors**: Trace to source, decide if one prior is better justified
- **Hidden information**: One party has relevant data not shared
- **Irrationality**: One/both updating incorrectly (cognitive bias, motivated reasoning)
- **Different values**: Not actually a factual disagreement but a preference mismatch

## Common Pitfalls

**Assuming common priors when they don't exist**: People from different backgrounds, disciplines, or experiences genuinely start with different base assumptions. This doesn't make disagreement irrational.

**Treating values as probabilities**: "Should we ship feature X?" involves values (user welfare vs. revenue), not just factual predictions. Aumann doesn't apply to value disagreements.

**Insufficient information sharing**: Stating your conclusion ("I believe 70%") without sharing the evidence and reasoning. Common knowledge requires transparency.

**Overconfidence blocking updates**: Clinging to your number even after hearing counterarguments. If you're truly rational, learning of disagreement should itself move your belief.

**Social signaling vs. honest belief**: In many contexts, stated beliefs are tribal markers, not actual probability estimates. Aumann assumes honest reporting.

**Complexity barrier**: Real-world beliefs involve complex causal models that can't be fully communicated. Common knowledge is often unattainable for practical reasons.

## Real-World Applications

**Team decision-making**: Product manager believes 80% chance feature will hit KPI, engineer believes 20%. Red flag—dig into assumptions and information gaps before proceeding.

**Investment committees**: When smart investors disagree on company valuation, it reveals different models of business dynamics or access to different information channels.

**Scientific peer review**: Persistent disagreement between qualified scientists with access to the same studies suggests different priors about theory or different weightings of evidence types.

**Forecasting tournaments**: Superforecasters converge on probabilities when sharing reasoning, consistent with Aumann. Persistent divergence reveals hidden variables or biases.

**Debugging assumptions**: Two engineers debug same issue, form different hypotheses. Trace the disagreement to different diagnostic frameworks or different evidence weightings.

## Power Moves

**Use disagreement as information**: If someone you respect disagrees with you, don't dismiss it—treat their divergent belief as evidence you're missing something. Update toward their position even without knowing their reasoning yet.

**Demand quantification**: Force vague disagreements into probability space. "I think it's risky" vs. "It's not that risky" becomes "I'd give it 30% chance of major problems" vs. "I'd say 10%." Now you can investigate the 20-point gap.

**Assume good faith**: If someone seems irrational for disagreeing, first check if you've achieved common knowledge of beliefs and evidence. Often the "irrationality" disappears when information asymmetries are resolved.

**Pre-commit to updating**: Before discussing, commit to updating your belief proportionally to strength of counterarguments. This prevents motivated cognition from blocking Aumann convergence.

**Track where you don't converge**: When beliefs don't converge after honest exchange, you've discovered a deep crux—either a prior difference worth examining or evidence one of you is reasoning incorrectly.

**Short-circuit with prediction markets**: If Aumann convergence isn't happening through discussion, betting mechanisms can reveal true beliefs and force reconciliation.

## Limitations

**Rare in practice**: True common knowledge is almost never achieved in real discussions. People have different background knowledge, different memories of conversations, different interpretations of evidence.

**Computationally intractable**: Full Bayesian updating on all evidence is impossible for humans. We use heuristics and simplifications that introduce divergence.

**Different utility functions**: Even with identical beliefs about probabilities, people can disagree on action because they value outcomes differently.

**Malicious actors**: Theorem assumes honesty. Strategic agents can profitably misrepresent beliefs.

**Value of disagreement**: In practice, intellectual diversity and disagreement often produces better outcomes than premature consensus, even if theoretically "irrational."

## Related Frameworks

- **Bayesian Updating**: The updating mechanism Aumann assumes all rational agents use
- **Common Knowledge Logic**: The formal structure of "everyone knows that everyone knows..."
- **Prediction Markets**: Practical mechanism for aggregating beliefs toward Aumann consensus
- **Devil's Advocate**: Institutionalizing disagreement when natural convergence would be premature
- **Red Team Exercises**: Forcing exploration of beliefs that would be dismissed under pure Aumann convergence

## Why It Matters

**Diagnostic lens**: When smart people disagree, don't just argue harder—investigate the asymmetries Aumann predicts must exist.

**Epistemic humility**: Your confidence should be shaken by learning that equally rational people with similar information disagree. Their disagreement is evidence.

**Culture signal**: Teams that quickly converge on beliefs after transparent discussion are exhibiting Aumann-like rationality. Persistent vague disagreements signal communication problems.

**Meta-lesson**: The theorem's practical irrelevance (people disagree constantly) reveals how far human cognition is from ideal Bayesian reasoning—and where improvement opportunities lie.

## Sources

- [Wikipedia - Aumann's Agreement Theorem](https://en.wikipedia.org/wiki/Aumann's_agreement_theorem)
- [Scott Aaronson - Common Knowledge and Aumann's Agreement Theorem](https://scottaaronson.blog/?p=2410)
- [LessWrong - Aumann's Agreement Theorem](https://www.lesswrong.com/w/aumann-s-agreement-theorem)
- [Tyler Cowen & Robin Hanson - Are Disagreements Honest?](https://mason.gmu.edu/~rhanson/deceive.pdf)
