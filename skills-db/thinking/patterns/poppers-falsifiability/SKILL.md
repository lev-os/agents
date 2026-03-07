---
name: poppers-falsifiability
description: Scientific theories must be testable and capable of being proven false
---

# Popper's Falsifiability

## Core Concept

Popper's Falsifiability Criterion states that for a theory to be genuinely scientific, it must be possible in principle to establish that it is false. A scientific theory makes specific predictions that future observations might reveal to be false. Rather than attempting to verify theories, scientists should attempt to falsify them - theories that survive rigorous attempts at falsification are provisionally accepted (corroborated), but never proven true.

This criterion solves the problem of induction: we can never prove a universal theory true through observations, but we can prove it false with a single counterexample. Scientific progress occurs when theories are shown wrong and replaced with better explanations.

## When to Use

- Evaluating whether a hypothesis is scientifically testable
- Designing experiments with meaningful falsification conditions
- Distinguishing science from pseudoscience
- Building product hypotheses that can be invalidated
- Setting up A/B tests with clear success/failure criteria
- Evaluating theoretical frameworks for practical utility
- Identifying unfalsifiable claims masquerading as scientific

## Implementation

### 1. State the Theory Explicitly
What exactly is being claimed?
- "All swans are white"
- "This feature increases engagement"
- "Our algorithm reduces bias"

### 2. Identify Falsifiable Predictions
What observable outcomes does this theory predict?
- If theory true → expect observations X
- If theory false → expect observations Y
- X and Y must be distinguishable

### 3. Design a Test That Could Disprove It
What observation would prove this theory false?
- **Swan theory**: Observe a non-white swan
- **Engagement theory**: Run A/B test, engagement doesn't increase
- **Bias theory**: Measure demographic outcomes, disparate impact persists

### 4. Ensure the Test is Risky
The test must have genuine potential to falsify:
- Not designed to always confirm
- Clear falsification criteria stated in advance
- No post-hoc rationalization allowed

### 5. Run the Test
Actually attempt to falsify the theory
- Don't just look for confirmation
- Actively seek disconfirming evidence
- Be willing to abandon theory if falsified

### 6. Interpret Results
- **Falsified**: Theory disproven, reject or modify
- **Survives**: Theory corroborated (not proven), provisionally accept
- **Unfalsifiable**: Not a scientific theory, reclassify

### 7. Iterate
Surviving theories should face increasingly rigorous tests
- Science progresses through surviving falsification attempts

## Real-World Examples

**Product Development**
- **Falsifiable**: "Users who see onboarding video complete setup 20% more"
- **Test**: A/B test with completion rate as metric, <15% increase = falsified
- **Unfalsifiable**: "The video creates a better user experience" (no measurable criteria)
- **Application**: Define success metrics before shipping, kill features that fail tests

**Machine Learning**
- **Falsifiable**: "This model achieves >90% accuracy on test set"
- **Test**: Holdout test set, <90% = falsified
- **Unfalsifiable**: "This model captures the essence of the data"
- **Application**: Rigorous benchmarking with predefined thresholds

**Business Strategy**
- **Falsifiable**: "Entering market X increases revenue by $1M in 12 months"
- **Test**: Track revenue for 12 months, <$500K = pivot signal
- **Unfalsifiable**: "This market feels like a good strategic fit"
- **Application**: Set quantitative OKRs that trigger strategy changes

**Medical Science**
- **Einstein's Relativity**: Predicted light bending near sun, measurable during eclipse
- **Test**: 1919 Eddington expedition measured deflection
- **Result**: Prediction confirmed, theory survived falsification attempt (GPS systems depend on it)
- **Application**: Theories with precise, testable predictions enable technological progress

**Pseudoscience Detection**
- **Astrology**: Makes vague predictions reinterpreted post-hoc ("You will face challenges")
- **Unfalsifiable**: Any outcome can be explained after the fact
- **Application**: Dismiss claims that can't specify what would prove them wrong

## Benefits

**Intellectual Rigor**
- Clear demarcation between science and non-science
- Prevent unfalsifiable speculation from wasting resources
- Focus on testable hypotheses

**Practical Progress**
- Theories that make precise predictions enable engineering
- Failed theories get discarded quickly
- Resources allocated to promising directions

**Epistemic Humility**
- No theory is ever "proven" - all are provisional
- Science advances through being wrong better
- Reduces dogmatism

**Decision Quality**
- Forces clear success criteria before action
- Enables data-driven pivots
- Protects against confirmation bias

## Common Pitfalls

- **Single Falsification Isn't Enough**: In practice, anomalies require replication and investigation
- **Auxiliary Hypotheses**: Can protect core theory (e.g., "instrument was broken")
- **Probabilistic Theories**: Harder to falsify - requires statistical significance
- **Practical Unfalsifiability**: Some scientific theories (string theory) may be true but currently untestable
- **Naive Falsificationism**: Popper himself acknowledged more nuance than strict falsificationism

## When NOT to Apply

**Observational and Descriptive Sciences**
Anthropology, paleontology, some aspects of evolutionary biology
- Historical sciences can't always run controlled experiments
- Still valuable knowledge even without strict falsifiability

**Early Exploration**
In pre-paradigmatic phases, overly strict falsifiability stifles creativity
- Allow speculation before demanding rigorous testability

**Mathematics and Logic**
These are deductive systems, not empirical theories
- Truth through proof, not falsification

**Ethical and Value Questions**
"Should we build this?" is not falsifiable
- Normative claims aren't scientific claims

## Relationship to Other Frameworks

**Alder's Razor**
"What cannot be settled by experiment is not worth debating"
- More extreme: Popper allows unfalsifiable metaphysics, just not as science
- Alder: Don't even discuss it

**Bayesian Epistemology**
Updating beliefs based on evidence
- Compatible: Falsification = extreme negative evidence → very low posterior probability
- Difference: Bayesianism is gradual, falsificationism is binary

**Null Hypothesis Testing**
Statistical framework assuming no effect until proven otherwise
- Operationalizes Popperian falsificationism in statistics
- p-value: Probability of observing data if null (falsifying hypothesis) true

**Ockham's Razor**
Prefer simpler explanations
- Both are demarcation criteria
- Occam: Among competing hypotheses
- Popper: Between science and non-science

**Kuhn's Paradigms**
Thomas Kuhn: Science doesn't strictly follow falsificationism
- Normal science: Puzzle-solving within paradigm, anomalies accommodated
- Revolutionary science: Paradigm shifts when anomalies accumulate
- Popper: Normative ideal; Kuhn: Descriptive reality

## Historical Context

**Karl Popper** (1902-1994)
- Austrian-British philosopher
- "The Logic of Scientific Discovery" (Logik der Forschung, 1934)
- Escaped Nazi Austria, taught at LSE
- Influenced by Einstein's overthrow of Newton

**Problem of Induction**
David Hume: Can't prove universal theories from finite observations
- Popper's solution: Don't try to prove - try to disprove

**Context: Vienna Circle**
Logical positivists required verification
- Popper: Verification impossible, falsification possible

**Einstein's Influence**
General Relativity made risky predictions (light deflection)
- Contrasted with Freud/Marx theories that explained everything post-hoc

**Impact**
- Gold standard for scientific respectability
- Influenced hypothesis testing in statistics
- Shaped experimental design methodology
- Foundation of critical rationalism

## Success Metrics

- Theories generate precise, testable predictions
- Failed predictions lead to theory revision or abandonment
- Resources not wasted on unfalsifiable speculation
- Clear experimental design with falsification criteria
- Faster iteration through rigorous testing

## Practical Application Framework

**For Researchers:**
**Step 1**: State hypothesis explicitly
**Step 2**: Derive falsifiable predictions
**Step 3**: Design experiment where hypothesis could fail
**Step 4**: Run experiment seeking disconfirmation
**Step 5**: If falsified → reject/modify; if corroborated → continue testing
**Step 6**: Publish methods and results (enable replication)

**For Product Teams:**
**Step 1**: Define hypothesis: "Feature X increases metric Y by Z%"
**Step 2**: Set falsification threshold: "If <0.5Z%, kill feature"
**Step 3**: Design A/B test
**Step 4**: Run test with statistical rigor
**Step 5**: Ship if corroborated, kill if falsified
**Step 6**: Document learnings

**For Evaluating Claims:**
**Step 1**: Ask "What observation would prove this wrong?"
**Step 2**: If no answer → unfalsifiable → not scientific
**Step 3**: If answer exists → evaluate test feasibility
**Step 4**: Demand test before accepting claim

## Key Insight

Popper's Falsifiability transforms how we think about knowledge: scientific theories aren't proven true, they're just theories that haven't been proven false yet. This humility is powerful - it means we're always one observation away from needing a better explanation. For practitioners, this translates to: define what failure looks like before you start, be willing to kill your darlings when data demands it, and trust the theories that survive the most rigorous attempts to disprove them. Falsifiability isn't just philosophy - it's the foundation of testable hypotheses, A/B testing culture, and data-driven decision making.

---

**Primary Sources**: Karl Popper "The Logic of Scientific Discovery" (1934), "Conjectures and Refutations" (1963)
**Related Concepts**: Problem of Induction, Demarcation Problem, Null Hypothesis, Bayesian Epistemology, Paradigm Shifts
**Complexity**: Medium - concept clear, nuances in application (auxiliary hypotheses, statistical falsification)
**Estimated Learning**: 30 minutes to understand, practice to consistently apply in hypothesis formation
