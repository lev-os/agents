# Reasoning Mode Taxonomy

> 80 modes across 12 categories. Use this to select the 10 best modes for the target project.

## Category A: Formal and Mathematical Reasoning

| Code | ID | Name | Description | Best For |
|------|-----|------|-------------|----------|
| A1 | deductive | Deductive Inference | If premises are true and inference rules valid, conclusion must be true. Truth-preserving, monotonic. | Spec checking, compliance logic, formal arguments |
| A2 | mathematical-proof | Mathematical Proof | Proof-theoretic reasoning emphasizing derivability and proof structure. | Formal methods, theorem proving, certified pipelines |
| A3 | formal-verification | Formal Verification | Constructive proofs corresponding to verified programs (proofs as programs). | Verified software, protocol verification |
| A4 | equational | Equational Reasoning | Transform expressions using equalities and rewrite rules preserving meaning. | Refactoring, optimization proofs, invariant manipulation |
| A5 | model-theoretic | Model-Theoretic | Reason by constructing/analyzing models that satisfy a theory. | Consistency checks, finding hidden assumptions, counterexamples |
| A6 | constraint-sat | Constraint Satisfaction | Model problems as variables with domains and constraints; search for satisfying assignments. | Scheduling, resource allocation, configuration validation |
| A7 | type-theoretic | Type-Theoretic | Use type systems as proof frameworks. Types encode invariants, type-checking proves properties. | API contract verification, state machine correctness |
| A8 | edge-case | Edge-Case Analysis | Systematically explore boundary conditions, limits, and degenerate inputs. | Test planning, robustness review, API contract validation |

## Category B: Ampliative Reasoning

| Code | ID | Name | Description | Best For |
|------|-----|------|-------------|----------|
| B1 | inductive | Inductive Inference | Generalize from observed instances to broader patterns. Ampliative (conclusions go beyond premises). | Pattern recognition, trend analysis, empirical generalization |
| B2 | statistical | Statistical Reasoning | Use data distributions, sampling, and frequentist/Bayesian estimation. | A/B testing, performance analysis, capacity planning |
| B3 | bayesian | Bayesian Reasoning | Update belief probabilities as new evidence arrives. Prior + likelihood = posterior. | Diagnosis, risk assessment, sequential decision-making |
| B4 | likelihood | Likelihood Reasoning | Evaluate which hypothesis makes observed data most probable. | Model selection, debugging competing theories |
| B5 | option-generation | Option Generation | Divergent exploration of the solution space before converging. | Feature ideation, architecture alternatives, brainstorming |
| B6 | analogical | Analogical Reasoning | Transfer knowledge from a well-understood source to a less-understood target. | Cross-domain insights, learning from prior projects |
| B7 | case-based | Case-Based Reasoning | Solve new problems by adapting solutions from similar past cases. | Incident response, pattern matching from history |
| B8 | conceptual-blending | Conceptual Blending | Merge two or more conceptual frames to create novel structures. | Innovation, naming, metaphor design, cross-domain discovery |
| B9 | simplicity | Simplicity / MDL | Prefer the simplest explanation that accounts for the data (Occam's razor formalized). | Architecture simplification, eliminating unnecessary complexity |
| B10 | reference-class | Reference-Class Forecasting | Ground predictions in the base rate of similar past projects. | Estimation, planning, risk calibration |
| B11 | fermi | Fermi Estimation | Decompose unknowns into estimable sub-problems and multiply. | Order-of-magnitude sizing, feasibility checks, capacity planning |

## Category C: Uncertainty Representation

| Code | ID | Name | Description | Best For |
|------|-----|------|-------------|----------|
| C1 | probabilistic | Probabilistic Reasoning | Assign and propagate probabilities over outcomes using probability theory. | Risk quantification, decision under uncertainty |
| C2 | fuzzy | Fuzzy Logic | Reason with graded truth values (0-1) instead of binary true/false. | Threshold tuning, user preference modeling |
| C3 | dempster-shafer | Dempster-Shafer | Represent uncertainty and ignorance separately using belief functions. | Sensor fusion, evidence combination with unknown reliability |
| C4 | info-gap | Info-Gap Analysis | Find decisions that are robust over a wide horizon of uncertainty. | Architecture decisions under deep uncertainty |
| C5 | sensitivity | Sensitivity Analysis | Determine which input variations most affect outcomes. | Configuration tuning, parameter importance ranking |

## Category D: Vagueness and Approximation

| Code | ID | Name | Description | Best For |
|------|-----|------|-------------|----------|
| D1 | rough-set | Rough-Set Reasoning | Classify with indiscernibility relations when boundaries are unclear. | Feature selection, incomplete data analysis |
| D2 | ambiguity-detection | Ambiguity Detection | Identify statements that admit multiple valid interpretations. | Requirements review, API documentation, spec critique |
| D3 | prototype-reasoning | Prototype Reasoning | Categorize by similarity to prototypical examples rather than necessary/sufficient conditions. | User persona modeling, feature categorization |
| D4 | sorites | Sorites-Aware | Handle heap paradoxes: when does "a few" become "many"? | Threshold definition, SLA boundaries, degradation policies |
| D5 | supervaluation | Supervaluational | Evaluate under all admissible precisifications of vague terms. | Requirements validation, policy interpretation |

## Category E: Change and Belief Revision

| Code | ID | Name | Description | Best For |
|------|-----|------|-------------|----------|
| E1 | belief-revision | Belief Revision (AGM) | Rationally update beliefs when new information contradicts existing ones. Minimize information loss. | Assumption management, migration planning |
| E2 | non-monotonic | Non-Monotonic Reasoning | Conclusions can be retracted when new information arrives. Default reasoning with exceptions. | Policy systems, exception handling, feature flags |
| E3 | temporal | Temporal Reasoning | Reason about time: sequences, durations, deadlines, temporal constraints. | Scheduling, workflow ordering, race condition detection |
| E4 | frame-problem | Frame-Aware | Track what changes and what stays the same after an action. | State management review, side-effect analysis |
| E5 | revision-planning | Revision Planning | Plan a sequence of belief changes to reach a target epistemic state. | Migration strategies, phased rollouts |
| E6 | defeasible | Defeasible Reasoning | Draw tentative conclusions that hold unless overridden by stronger evidence. | Default configurations, fallback chains |
| E7 | paraconsistent | Paraconsistent | Reason productively with contradictory information without explosion. | Legacy system analysis, conflicting requirements |

## Category F: Causal and Counterfactual Reasoning

| Code | ID | Name | Description | Best For |
|------|-----|------|-------------|----------|
| F1 | causal-inference | Causal Inference | Distinguish correlation from causation using interventions and DAGs. | Performance diagnosis, A/B test interpretation |
| F2 | dependency-mapping | Dependency Mapping | Trace and visualize dependency chains (code, data, infrastructure). | Architecture review, blast radius analysis, refactoring |
| F3 | counterfactual | Counterfactual Reasoning | "What if X had been different?" Evaluate alternative histories. | Post-mortem analysis, design alternative evaluation |
| F4 | failure-mode | Failure Mode Analysis (FMEA) | Systematically enumerate what can fail, how likely, and how severe. | Reliability review, SLA planning, chaos engineering |
| F5 | root-cause | Root-Cause Analysis | Trace observed symptoms back to their fundamental causes (5 Whys, fault trees). | Debugging, incident analysis, systemic improvement |
| F6 | second-order-effects | Second-Order Effects | Trace consequences of consequences: ripple effects and feedback loops. | Change impact analysis, policy review |
| F7 | systems-thinking | Systems Thinking | Model the whole as interacting subsystems with feedback loops, delays, and emergent behavior. | Architecture review, organizational analysis, holistic diagnosis |

## Category G: Practical Reasoning

| Code | ID | Name | Description | Best For |
|------|-----|------|-------------|----------|
| G1 | decision-analysis | Decision Analysis | Structure choices with payoff matrices, expected value, and utility theory. | Build-vs-buy, technology selection, priority ranking |
| G2 | strategic-planning | Strategic Planning | Set objectives, assess environment, formulate strategy, plan execution. | Roadmap creation, competitive positioning |
| G3 | resource-allocation | Resource Allocation | Optimize distribution of limited resources across competing demands. | Sprint planning, capacity allocation, budget optimization |
| G4 | prioritization | Prioritization | Rank items by weighted criteria (impact, urgency, effort, risk). | Backlog grooming, feature selection, triage |
| G5 | satisficing | Satisficing | Find "good enough" solutions when optimal is infeasible or not worth the cost. | MVP scoping, deadline-driven decisions |
| G6 | multi-criteria | Multi-Criteria Decision | Balance multiple conflicting objectives with explicit tradeoffs. | Vendor selection, architecture tradeoffs |
| G7 | means-end | Means-End Analysis | Identify the gap between current and goal state, then find operators to close it. | Debugging, migration planning, task decomposition |
| G8 | planning | Automated Planning | Construct action sequences achieving goals from initial state under constraints. | CI/CD pipeline design, deployment orchestration |
| G9 | test-plan | Test Planning | Design test strategies covering requirements, risk areas, and edge cases. | QA strategy, test suite design |
| G10 | cost-benefit | Cost-Benefit Analysis | Quantify and compare costs vs benefits of alternatives. | Investment decisions, feature ROI, tech debt tradeoffs |
| G11 | clinical-operational | Clinical/Operational | Diagnose problems by gathering symptoms, forming differentials, testing hypotheses. | Bug triage, performance investigation, incident response |

## Category H: Strategic and Social Reasoning

| Code | ID | Name | Description | Best For |
|------|-----|------|-------------|----------|
| H1 | game-theoretic | Game-Theoretic | Model strategic interactions between rational agents with competing interests. | API pricing, rate limiting, abuse prevention |
| H2 | adversarial-review | Adversarial Review | Deliberately attack assumptions, designs, and claims to find weaknesses. | Security review, proposal critique, stress testing |
| H3 | negotiation | Negotiation | Find mutually beneficial agreements between parties with different preferences. | API contract negotiation, cross-team prioritization |
| H4 | mechanism-design | Mechanism Design | Design rules/incentives so self-interested participants produce desired outcomes. | Incentive structures, governance models |

## Category I: Dialectical and Rhetorical Reasoning

| Code | ID | Name | Description | Best For |
|------|-----|------|-------------|----------|
| I1 | argument-mapping | Argument Mapping | Decompose arguments into premises, inferences, and conclusions; map support/attack. | ADR review, proposal evaluation, requirements disputes |
| I2 | dialectical | Dialectical Reasoning | Thesis + antithesis -> synthesis through structured debate. | Design review, resolving conflicting requirements |
| I3 | rhetorical | Rhetorical Analysis | Evaluate persuasiveness, audience fit, and communication effectiveness. | Documentation review, API naming, error message quality |
| I4 | perspective-taking | Perspective-Taking | Inhabit different stakeholder viewpoints to find blind spots. | UX review, API design, onboarding experience |
| I5 | steelmanning | Steelmanning | Construct the strongest version of an argument before critiquing it. | Fair evaluation, avoiding strawman dismissals |

## Category J: Modal, Temporal, and Spatial Reasoning

| Code | ID | Name | Description | Best For |
|------|-----|------|-------------|----------|
| J1 | deontic | Deontic Reasoning | Reason about obligations, permissions, and prohibitions. | Compliance, RBAC design, policy enforcement |
| J2 | epistemic | Epistemic Reasoning | Reason about knowledge: what is known, unknown, knowable. | Documentation gaps, observability, logging strategy |
| J3 | alethic-modal | Alethic Modal | Reason about necessity and possibility: must, can, cannot. | Invariant identification, impossibility proofs |
| J4 | spatial | Spatial Reasoning | Reason about layout, containment, adjacency, distance. | UI layout, network topology, data locality |

## Category K: Domain-Specific Reasoning

| Code | ID | Name | Description | Best For |
|------|-----|------|-------------|----------|
| K1 | legal | Legal Reasoning | Apply rules to facts using precedent, analogy, and statutory interpretation. | License compliance, ToS review, regulatory conformance |
| K2 | scientific | Scientific Reasoning | Hypothesize, predict, experiment, revise. Emphasis on falsifiability. | Performance experiments, feature experiments |
| K3 | ethical | Ethical Reasoning | Apply moral frameworks (utilitarian, deontological, virtue) to technology decisions. | Privacy review, bias auditing, harm reduction |
| K4 | design-thinking | Design Thinking | Empathize, define, ideate, prototype, test. User-centered problem solving. | UX improvement, feature design, onboarding flows |
| K5 | medical-diagnostic | Medical Diagnostic | Differential diagnosis: generate, test, eliminate hypotheses from symptoms. | Complex debugging, system health diagnosis |
| K6 | compliance | Compliance Reasoning | Verify conformance to standards, regulations, and policies. | GDPR, SOC2, accessibility, coding standards |
| K7 | financial | Financial Reasoning | Apply accounting, valuation, and financial modeling frameworks. | Cost modeling, pricing strategy, ROI analysis |

## Category L: Meta-Reasoning

| Code | ID | Name | Description | Best For |
|------|-----|------|-------------|----------|
| L1 | meta-evaluation | Meta-Evaluation | Evaluate the reasoning process itself: are we asking the right questions? | Methodology review, process improvement |
| L2 | debiasing | Debiasing | Identify and correct cognitive biases in reasoning and decision-making. | Assumption auditing, avoiding groupthink |
| L3 | worst-case | Worst-Case Reasoning | Plan for the worst plausible outcome and ensure survivability. | Disaster recovery, security hardening, SLA design |
| L4 | uncertainty-meta | Uncertainty About Uncertainty | Recognize when the uncertainty model itself may be wrong. | Black swan preparedness, model risk |
| L5 | scope-control | Scope Control | Monitor and manage scope creep, feature bloat, and complexity growth. | Project management, architecture simplification |
| L6 | reflective-equilibrium | Reflective Equilibrium | Iteratively adjust principles and judgments until they cohere. | Standard-setting, policy design, framework selection |

## Mode Selection Heuristics

### By Project Type

| Project Type | Recommended Core Modes |
|-------------|----------------------|
| **Web application** | F7, F5, A8, H2, I4, B5, G4, F4, K3, L2 |
| **CLI tool** | A1, A8, I4, F4, G7, B9, F2, H2, G9, L1 |
| **Library/SDK** | A7, A1, A8, I4, F2, B6, H2, G9, K6, D2 |
| **Data pipeline** | F7, F4, F2, A8, C1, E3, G3, B2, F5, L3 |
| **ML/AI system** | B3, B2, K2, K3, L2, C1, H2, F1, B1, I4 |
| **Infrastructure** | F4, F7, L3, A6, E3, G3, F2, H2, C4, K6 |
| **Research paper** | A1, B3, K2, I1, I5, D2, L1, L2, B1, F3 |
| **Business plan** | G1, G2, G10, B11, F6, H1, I4, L2, B5, C1 |
| **Security system** | H2, H1, L3, F4, A1, K6, K3, G9, A8, F5 |
| **Organizational process** | F7, I4, H4, G3, L1, K3, H1, I3, E1, L2 |
| **API design** | A7, A1, A8, I4, D2, F2, K6, B6, H2, G9 |
| **Migration/refactor** | F2, E1, E5, G8, F4, F3, G3, L3, A8, G4 |
| **Incident response** | F5, F1, G11, F3, B3, F6, E1, G5, H2, L2 |

## Signature Failure Modes (Critical for Agent Prompts)

Every reasoning mode has a characteristic way it breaks. Including these in agent prompts helps agents avoid their mode's signature trap:

| Mode | Signature Failure | How to Avoid |
|------|-------------------|--------------|
| Deductive (A1) | Garbage-in: false premises → valid but wrong conclusion | Check premises against reality, not just logic |
| Inductive (B1) | Overgeneralization from small or biased samples | State sample size, look for counterexamples |
| Bayesian (B3) | Overconfident priors; no sensitivity analysis | Always test: "what if my prior is wrong?" |
| Abductive (B5) | Story bias: most appealing explanation, not best supported | Generate 3+ explanations before picking |
| Analogical (B6) | False analogy: shared surface, different causation | Verify the structural mapping, not just surface similarity |
| Causal-Inference (F1) | Hidden confounders; causal diagrams missing key variables | Ask "what else could explain this?" |
| Root-Cause (F5) | Stopping at first plausible cause instead of digging deeper | Always ask at least 5 "why?"s |
| Systems-Thinking (F7) | Vague loop stories without measurable hypotheses | Require specific, testable claims about feedback loops |
| Adversarial (H2) | Severity inflation: rating findings as CRITICAL using worst-case threat models that don't match deployment reality; counting defensive fallbacks as vulnerabilities | Calibrate severity against actual deployment context. For every vulnerability, demonstrate a concrete exploit scenario realistic for this project's actual exposure. Classify each finding as reachable-in-production vs defensive-fallback vs test-only |
| Game-Theoretic (H1) | Assuming rationality/common knowledge that doesn't exist | Check whether players actually behave as modeled |
| Perspective-Taking (I4) | Projecting your own values onto other stakeholders | Validate with actual user data when possible |
| Debiasing (L2) | Ritualized checklists not actually changing conclusions | Every bias check must produce a specific action |
| Simplicity (B9) | Structural bias toward removal: mandate to "find unnecessary complexity" creates confirmation bias where every module is evaluated through a lens that favors deletion. "Zero callers" claims based on grep-only methodology miss indirect paths | Higher evidence bar for "unnecessary" claims. Search for type names, constructors, method calls, re-exports, conditional compilation — not just module imports. Before recommending removal, verify through multiple search methodologies |
| Conceptual-Blending (B8) | Forced connections between unrelated domains | Skip domains with no genuine structural parallel |
| Failure-Mode (F4) | Enumerating obvious failures, missing subtle cascade effects | Focus on failures that trigger other failures |
| Fermi (B11) | Hidden unit mistakes or untested implicit assumptions | Double-check units and orders of magnitude |

## Complementary Mode Map

Which modes strengthen each other when paired:

```
Formal (A) ←→ Ampliative (B): verification ←→ discovery
Formal (A) ←→ Meta (L): rigor ←→ calibration
Ampliative (B) ←→ Uncertainty (C): pattern ←→ confidence bounds
Uncertainty (C) ←→ Causal (F): probability ←→ mechanism
Causal (F) ←→ Practical (G): why ←→ what to do
Practical (G) ←→ Strategic (H): plan ←→ anticipate opponents
Strategic (H) ←→ Dialectical (I): compete ←→ communicate
Dialectical (I) ←→ Domain (K): argue ←→ contextualize
Domain (K) ←→ Meta (L): expertise ←→ reflect on expertise
```
