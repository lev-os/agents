# Mode Composition: Stacks, Pairs, and Hybrid Reasoning

> Real-world reasoning is inherently hybrid. Single modes are rarely sufficient. This reference defines proven mode combinations for specific problem types.

## The Principle of Hybrid Reasoning

A single mode has signature strengths and signature blind spots. Composition compensates blind spots while preserving strengths. The key insight: **modes compose like functions** -- the output of one becomes the input or constraint of another.

## Antagonistic Pairs

These mode pairs are designed to CHALLENGE each other. Include at least one antagonistic pair in every run:

| Mode A | Mode B | Tension | Value |
|--------|--------|---------|-------|
| Deductive (A1) | Inductive (B1) | Top-down vs bottom-up | Catches both false premises and overgeneralization |
| Worst-Case (L3) | Option-Generation (B5) | Pessimism vs possibility | Prevents both recklessness and paralysis |
| Simplicity (B9) | Systems-Thinking (F7) | Reduce vs expand | Finds the right level of complexity |
| Adversarial (H2) | Perspective-Taking (I4) | Attack vs empathize | Stress-tests from hostile AND friendly viewpoints |
| Root-Cause (F5) | Second-Order (F6) | Look backward vs look forward | Diagnoses past AND predicts future problems |
| Formal-Verification (A3) | Satisficing (G5) | Perfect vs good-enough | Calibrates quality/effort tradeoff |
| Debiasing (L2) | Any dominant mode | Meta vs object-level | Catches the lead agent's own biases |

## Complementary Pairs

These modes strengthen each other rather than opposing:

| Mode A | Mode B | Synergy |
|--------|--------|---------|
| Causal-Inference (F1) | Counterfactual (F3) | Identify causes, then test them by imagining alternatives |
| Failure-Mode (F4) | Edge-Case (A8) | What can fail + boundary conditions where it fails |
| Bayesian (B3) | Reference-Class (B10) | Prior calibration from base rates |
| Analogical (B6) | Case-Based (B7) | Transfer patterns from similar domains and past cases |
| Decision-Analysis (G1) | Multi-Criteria (G6) | Structure choices, then handle multiple objectives |
| Argument-Mapping (I1) | Steelmanning (I5) | Map argument structure, then strengthen before attacking |

## Proven Mode Stacks by Problem Type

### Stack 1: Software Architecture Review (10 modes)
```
F7 Systems-Thinking        → See feedback loops and emergent behavior
F2 Dependency-Mapping       → Trace dependency chains and blast radius
A1 Deductive               → Verify logical consistency of design contracts
H2 Adversarial-Review      → Stress-test security assumptions
F4 Failure-Mode            → Enumerate what can go wrong (FMEA)
I4 Perspective-Taking      → Users, maintainers, oncall, new contributors
B5 Option-Generation       → Alternative architectures that weren't chosen
F3 Counterfactual          → What if key decisions were made differently?
G4 Prioritization          → Which improvements matter most?
L2 Debiasing               → Catch confirmation bias in the review
```

### Stack 2: Bug Hunt / Code Quality (10 modes)
```
G11 Clinical-Operational   → Diagnosis from symptoms, gather evidence
B1 Inductive               → Pattern-match from observed code to general flaws
H2 Adversarial-Review      → Attack the code's trust assumptions
A1 Deductive               → Trace logical implications of code paths
F1 Causal-Inference        → Distinguish correlation from causation in bugs
A7 Type-Theoretic          → Check type system contracts and invariants
A8 Edge-Case               → Boundary conditions, empty inputs, overflows
F5 Root-Cause              → 5-Whys from symptoms to fundamental causes
B3 Bayesian                → Update bug probability as evidence accumulates
L2 Debiasing               → Don't skip uncomfortable code paths
```

### Stack 3: Incident / Postmortem Analysis (10 modes)
```
F5 Root-Cause              → 5-Whys to fundamental cause
F1 Causal-Inference        → Separate correlation from causation
G11 Clinical-Operational   → Diagnostic reasoning from symptoms
F3 Counterfactual          → "What if we had done X instead?"
B3 Bayesian                → Update probability of hypotheses as new info arrives
F6 Second-Order-Effects    → What downstream effects did the incident cause?
E1 Belief-Revision         → How should this change our mental models?
G5 Satisficing             → Good-enough fix now vs perfect fix later
H2 Adversarial-Review      → Could this be an attack, not an accident?
L2 Debiasing               → Avoid hindsight bias, availability bias
```

### Stack 4: Creative Innovation / Feature Ideation (10 modes)
```
B8 Conceptual-Blending     → Merge ideas from different domains
B6 Analogical              → Transfer from well-understood domains
B5 Option-Generation       → Divergent exploration of solution space
I4 Perspective-Taking      → Users, non-users, competitors, future-selves
F6 Second-Order-Effects    → Ripple effects of each idea
K4 Design-Thinking         → Empathize → Define → Ideate → Prototype → Test
H4 Mechanism-Design        → Design incentives so adoption works
D3 Prototype-Reasoning     → Category by similarity to ideal examples
G1 Decision-Analysis       → Evaluate ideas with structured payoff analysis
L1 Meta-Evaluation         → Are we asking the right questions?
```

### Stack 5: Strategy / Business Analysis (10 modes)
```
G2 Strategic-Planning      → Set objectives, assess environment, formulate strategy
H1 Game-Theoretic          → Model competitor and stakeholder strategic responses
G1 Decision-Analysis       → Structure choices with payoff matrices
B10 Reference-Class        → Ground predictions in base rates of similar projects
B11 Fermi                  → Order-of-magnitude sizing for feasibility
G6 Multi-Criteria          → Balance conflicting objectives with explicit tradeoffs
C4 Info-Gap                → Decisions robust over wide uncertainty horizon
F6 Second-Order-Effects    → What happens after the first move?
I4 Perspective-Taking      → Customers, investors, employees, regulators
L2 Debiasing               → Planning fallacy, overconfidence, sunk cost
```

### Stack 6: Security / Threat Modeling (10 modes)
```
H2 Adversarial-Review      → Red-team the system
H1 Game-Theoretic          → Model attacker incentives and capabilities
L3 Worst-Case              → Assume the worst plausible scenario
F4 Failure-Mode            → Enumerate failure modes with severity
A1 Deductive               → Trace logical implications of trust boundaries
F2 Dependency-Mapping      → Map supply chain and blast radius
K6 Compliance              → Check regulatory and standard conformance
K1 Legal                   → License, liability, and regulatory exposure
J1 Deontic                 → Obligations, permissions, prohibitions
L2 Debiasing               → Don't assume "we would never do that"
```

### Stack 7: Research / Academic Analysis (10 modes)
```
K2 Scientific              → Hypothesize, predict, test, revise
A1 Deductive               → Verify logical validity of arguments
B3 Bayesian                → Evidence quality and belief updating
I1 Argument-Mapping        → Decompose argument structure
I5 Steelmanning            → Construct strongest version before critiquing
D2 Ambiguity-Detection     → Find statements with multiple interpretations
L1 Meta-Evaluation         → Is the methodology sound?
L2 Debiasing               → Confirmation bias, selection bias, reporting bias
F1 Causal-Inference        → Distinguish correlation from causation
B1 Inductive               → How well do the data support the generalizations?
```

### Stack 8: Policy / Governance Review (10 modes)
```
J1 Deontic                 → Obligations, permissions, prohibitions
K3 Ethical                 → Moral frameworks applied to technology decisions
K1 Legal                   → Legal compliance and liability
K6 Compliance              → Standard and regulatory conformance
I4 Perspective-Taking      → Affected stakeholders
F1 Causal-Inference        → Does this policy actually cause the desired outcome?
H4 Mechanism-Design        → Will self-interested actors follow the rules?
I3 Rhetorical              → Is the policy communicated effectively?
F6 Second-Order-Effects    → Unintended consequences
E7 Paraconsistent          → Handle conflicting requirements without explosion
```

### Stack 9: UX / Product Quality (10 modes)
```
K4 Design-Thinking         → Empathy-driven, user-centered analysis
I4 Perspective-Taking      → New user, power user, admin, support agent
D2 Ambiguity-Detection     → Confusing UI text, unclear affordances
I3 Rhetorical              → Error messages, onboarding copy, help text quality
A8 Edge-Case               → Empty states, error states, extreme inputs
B6 Analogical              → Compare to best-in-class products
G5 Satisficing             → Is "good enough" actually good enough?
F7 Systems-Thinking        → User journey as a system with feedback loops
H1 Game-Theoretic          → User incentives, dark patterns, engagement hooks
L2 Debiasing               → Designer bias, curse of knowledge
```

### Stack 10: Migration / Major Refactor Planning (10 modes)
```
F2 Dependency-Mapping      → What depends on what?
E1 Belief-Revision         → Which assumptions need updating for the new world?
E5 Revision-Planning       → Sequence of changes to reach target state
G8 Planning                → Action sequences under constraints
F4 Failure-Mode            → What can go wrong during migration?
F3 Counterfactual          → What if we migrated differently?
G3 Resource-Allocation     → Time, people, risk budget
L3 Worst-Case              → What if the migration fails halfway?
A8 Edge-Case               → Data edge cases that break during migration
G4 Prioritization          → What to migrate first for maximum value
```

## Mode Composition Chains

Modes can chain sequentially where one's output feeds the next:

```
Diagnostic chain:     Clinical-Operational → Root-Cause → Counterfactual → Recommendation
Theory-to-test:       Abductive → Deductive → Experimental-Design → Statistical
Discovery chain:      Inductive → Analogical → Conceptual-Blending → Option-Generation
Risk chain:           Failure-Mode → Worst-Case → Sensitivity → Decision-Analysis
Governance chain:     Deontic → Compliance → Mechanism-Design → Rhetorical
Calibration chain:    Reference-Class → Bayesian → Debiasing → Calibration
```

## Dynamic Mode Selection During Synthesis

After Phase 5 (collection), if you identify blind spots, you CAN:
1. Spawn 1-2 additional agents with gap-filling modes
2. Send a targeted prompt addressing the specific blind spot
3. Integrate their findings into the existing synthesis

This is optional and should only be done when a critical axis is completely uncovered and the gap matters for the project.
