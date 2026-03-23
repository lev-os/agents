---
name: study-construction
description: Methodology for constructing synthetic user research studies — how to reason about personas, dimensions, matrices, and signal interpretation
---

# Synthetic User Research: Study Construction Methodology

This is a methodology reference, not a template. It teaches you HOW to construct a study for a specific problem. Every study is different. If two studies look the same, one of them is wrong.

## 1. Analyze the Problem Space

Before constructing personas, understand what you're testing:

- **Read problem_spec.yaml** — who is `for_whom`? What are the constraints? What does success look like?
- **Identify the decision being made** — are you validating a problem framing? Testing a feature concept? Comparing interaction models?
- **Ask: what kind of disagreement would be useful?** If all personas agree, you learn nothing. What axes of human variation would produce meaningful divergence for THIS problem?

## 2. Choose Relevant Dimensions

Not every study needs the same psychological dimensions. Pick the axes that matter:

**Common dimension sets by problem type:**

- **Developer tools**: domain expertise (beginner/expert), workflow style (CLI-first/GUI-first), team size context (solo/enterprise), risk tolerance
- **Consumer products**: tech literacy, attention span, brand loyalty, price sensitivity, privacy concern level
- **Enterprise/B2B**: org size, decision authority, compliance burden, change tolerance, vendor fatigue
- **Healthcare/regulated**: domain expertise, liability awareness, patient interaction frequency, regulatory knowledge
- **Creative tools**: skill level, workflow rigidity, collaboration needs, output volume

**Axiom explorer dimensions (load from `~/.agents/skills-db/thinking/axioms/skills/map-elements.md` when relevant):**

- Emotional drivers + polyvagal state — useful when the product touches anxiety, trust, or safety
- Tribal affiliations — useful when the product intersects identity or community
- Big 5 personality — useful as a general-purpose differentiator, but often too abstract. Prefer domain-specific dimensions.
- ANS state distribution — useful for products that involve stress, performance, or high-stakes decisions
- Cognitive biases — useful when you want to test whether the design accommodates or exploits common thinking errors

**Rule: If you can't articulate WHY a dimension matters for THIS study, don't include it.**

## 3. Construct Personas

Each persona is a **coherent worldview**, not a list of traits. The prompt injection should read like a person describing themselves, not a psych profile.

**Construction process:**

1. Start with the user segments from `for_whom` in problem_spec
2. For each segment, ask: what beliefs, constraints, and experiences shape how this person would react?
3. Write the persona as a first-person worldview (200-400 words)
4. Include: what they care about, what they're afraid of, what they've been burned by, what they're optimizing for
5. Do NOT include: instructions to the model about how to respond. The persona IS the instruction.

**Diversity check:**

- Are any two personas too similar? If you can't predict different reactions, merge them.
- Are you missing a segment that matters? Check problem_spec constraints — who would be most affected?
- Is there a persona that would HATE this? Include them. Resistance is signal.

**Persona count:**

- 2 personas: binary decision, clear A/B
- 3 personas: triangulation, good default
- 4-6 personas: broad user space, multiple segments
- More than 6: diminishing returns. You're testing a matrix, not running a census.

## 4. Design the Test Matrix

Personas and models are independent axes. Every persona should run against every model you care about.

**Why test across models:**

- Different reasoning strengths surface different aspects of the persona
- A weak model might miss nuance but capture gut reactions
- A strong model might overthink but catch edge cases
- Cross-model agreement on a persona reaction = strong signal
- Cross-model divergence = the persona prompt isn't specific enough, or the reaction genuinely depends on reasoning depth

**Why test across CLI runners (when available):**

- Different training data means different model "personalities"
- Claude, GPT, Gemini have different cultural priors
- Testing across model families eliminates single-provider bias
- If Claude and GPT disagree about a persona's reaction, the disagreement is the insight

**Matrix sizing:**

- 3 personas × 3 models = 9 runs (good default)
- 3 personas × 5 CLIs = 15 runs (cross-provider validation)
- 5 personas × 3 models = 15 runs (broad user space)
- Keep total under 20 runs unless you have a specific reason for more

## 5. Interpret Results

**Convergence patterns:**

- **All personas, all models agree**: Strong signal. This is probably true. Lock it.
- **All personas agree, models split**: The signal is real but reasoning-depth-dependent. The strong model's reasoning is usually more reliable.
- **Personas split, all models agree within persona**: Real user segment difference. Design for both.
- **Everything diverges**: Your stimulus is ambiguous or your personas aren't specific enough. Refine and re-run.

**Edge detection:**

- Look for reactions that only appear at one reasoning level — these are the non-obvious insights
- Look for reactions that only one persona has — these are the underserved segments
- Look for contradictions within a single persona across models — your persona prompt has ambiguity

**Integration into JTBD:**

- Each distinct persona reaction pattern becomes a `user_type` in `jobs.graph.json`
- Shared concerns become `constraints` on job statements
- Shared excitement becomes motivation language
- Edge cases go into the risk register or inform scope boundaries
