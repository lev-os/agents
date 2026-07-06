# The Seven Taxonomy Axes

> These axes are the cognitive backbone of mode selection. Most reasoning disagreements trace to mixing up which axis matters.

## Axis 1: Ampliative vs Non-Ampliative

**Non-ampliative (truth-preserving):** Conclusions contained in premises. If premises are true, conclusion MUST be true.
- Modes: Deductive (A1), Mathematical Proof (A2), Formal Verification (A3), Equational (A4), Type-Theoretic (A7)
- Strength: certainty, assurance, verification
- Weakness: can't discover anything new -- only makes explicit what's implicit

**Ampliative (knowledge-extending):** Conclusions go beyond premises. Even if premises are true, conclusion MIGHT be false.
- Modes: Inductive (B1), Statistical (B2), Bayesian (B3), Abductive (B5), Analogical (B6), Case-Based (B7), Fermi (B11)
- Strength: discovery, learning, pattern recognition, hypothesis generation
- Weakness: always fallible, requires calibration

**Selection rule:** Discovery/exploration projects need ampliative modes. Verification/compliance projects need non-ampliative. Most real projects need BOTH -- at least 2 from each side.

## Axis 2: Monotonic vs Non-Monotonic

**Monotonic:** Adding information NEVER retracts conclusions. What's proved stays proved.
- Modes: Deductive (A1), Mathematical Proof (A2), Formal Verification (A3)
- Where it applies: pure logic, mathematics, formal specifications

**Non-monotonic:** Adding information CAN retract conclusions. "Birds fly" is true until "this bird is a penguin."
- Modes: Default Reasoning (E2), Defeasible (E6), Belief Revision (E1), Non-Monotonic (E2), Paraconsistent (E7)
- Where it applies: virtually ALL real-world reasoning

**Selection rule:** If the project deals with exceptions, overrides, feature flags, or "normally X but sometimes Y," include non-monotonic modes. This is almost always the case.

## Axis 3: Uncertainty vs Vagueness

**Uncertainty:** The fact is crisp but we don't know which value it has. "The coin landed heads or tails -- we don't know which." Tools: probability, statistics, Bayesian reasoning.
- Modes: Probabilistic (C1), Bayesian (B3), Statistical (B2), Dempster-Shafer (C3), Sensitivity (C5)

**Vagueness:** The predicate itself has blurred boundaries. "Is this system fast?" has no crisp answer. Tools: fuzzy logic, rough sets, prototype reasoning.
- Modes: Fuzzy (D1 - mapped as fuzzy reasoning), Rough-Set (D1), Ambiguity-Detection (D2), Prototype (D3), Sorites-Aware (D4)

**Selection rule:** Performance, reliability, capacity → uncertainty modes. UX quality, "good enough," naming, categorization → vagueness modes. **Never treat a vague predicate as a probability problem.**

## Axis 4: Descriptive vs Normative

**Descriptive:** What IS the case. Facts, causes, mechanisms, patterns.
- Modes: Causal-Inference (F1), Systems-Thinking (F7), Inductive (B1), Root-Cause (F5), Diagnostic (G11)

**Normative:** What OUGHT to be the case. Values, duties, preferences, goals.
- Modes: Ethical (K3), Deontic (J1), Decision-Analysis (G1), Compliance (K6), Prioritization (G4)

**Selection rule:** Most dangerous axis to confuse. When someone says "the architecture has a problem," that's normative (it violates their values about good architecture). Include at least one explicitly normative mode to surface hidden value judgments. Pair it with a descriptive mode analyzing the same area.

## Axis 5: Belief vs Action

**Belief-oriented:** What should we believe/accept as true?
- Modes: Bayesian (B3), Inductive (B1), Belief-Revision (E1), Calibration (L2), Scientific (K2)
- Focus: updating knowledge, reducing ignorance, tracking confidence

**Action-oriented:** What should we DO?
- Modes: Decision-Analysis (G1), Planning (G8), Resource-Allocation (G3), Satisficing (G5), Strategic-Planning (G2)
- Focus: choosing actions under constraints, optimizing outcomes

**Selection rule:** Analysis-focused runs need belief modes. Implementation-focused runs need action modes. Strategy projects need explicit separation -- "what is true" and "what to do about it" are different questions.

## Axis 6: Single-Agent vs Multi-Agent

**Single-agent:** Other entities are part of the environment (predictable, statistical).
- Modes: Most formal (A), causal (F), and practical (G) modes
- Assumption: the world doesn't strategically respond to your analysis

**Multi-agent:** Other entities are strategic agents with their own goals.
- Modes: Game-Theoretic (H1), Adversarial-Review (H2), Negotiation (H3), Mechanism-Design (H4), Perspective-Taking (I4), Theory-of-Mind (H*)
- Assumption: users, attackers, competitors, and team members will respond to changes

**Selection rule:** If the project has users, competitors, attackers, or interacting teams, include multi-agent modes. Security projects MUST include adversarial. Platform/marketplace projects MUST include mechanism design.

## Axis 7: Truth vs Adoption

**Truth-oriented:** Is the conclusion correct? Accuracy, validity, soundness.
- Modes: Deductive (A1), Statistical (B2), Causal-Inference (F1), Scientific (K2)
- Focus: getting the right answer

**Adoption-oriented:** Will stakeholders accept the conclusion? Persuasion, framing, audience fit.
- Modes: Rhetorical (I3), Perspective-Taking (I4), Narrative (I5), Sensemaking (I5)
- Focus: getting the answer used

**Selection rule:** Many technically correct findings die because nobody acts on them. If the report needs to influence stakeholders (it usually does), include at least one adoption-oriented mode. Otherwise the analysis is correct but inert.

## Axis Coverage Matrix

Use this to verify your 10 modes span sufficient axes:

```
         Non-amp  Amp  Mono  Non-mono  Uncert  Vague  Desc  Norm  Belief  Action  Single  Multi  Truth  Adopt
A1 Ded     X            X                              X                   X       X              X
B1 Ind            X            X                       X            X              X              X
B3 Bay            X            X        X              X            X              X              X
F5 Root                        X                       X                                  X       X
F7 Sys                         X                       X                          X       X       X
H2 Adv            X                                           X           X              X        X
A8 Edge    X            X                              X                   X       X              X
I4 Persp          X                             X                    X                   X               X
F3 Count          X            X                       X            X              X              X
L2 Debias                                                    X     X              X              X
```

**Target:** At least one X in every column. If a column is empty, your analysis has a structural blind spot on that axis.
