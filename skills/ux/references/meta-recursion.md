---
name: meta-recursion
description: Run axiom explorer dig-axioms on the /ux pipeline itself to surface its own hidden assumptions
---

# Meta-Recursion: Axiom Explorer on the /ux Pipeline

Use axiom explorer's `axiom-drill-down` command to interrogate the /ux pipeline's own assumptions. This isn't automated — it's a reflective exercise you run when something feels off, when results surprise you, or when validating the pipeline itself.

## The Core Belief to Drill

> "A structured 7-step UX pipeline (Problem Framing → JTBD → Task Decomposition → IA → Interaction Models → Components → Wireframes) produces better UX outcomes than ad-hoc design."

## How to Run

1. Load axiom explorer: `~/.agents/skills-db/thinking/axioms/commands/INDEX.md`
2. Use the `axiom-drill-down` command (skills 1-3 + synthesis)
3. Input: the belief statement above
4. Run 3 levels of Socratic "why?"

## What to Interrogate

### Pipeline assumptions

- Does the pipeline assume users are **rational actors** who make decisions based on information architecture?
- Does the **linear step order** assume that problem framing must precede JTBD? What if the job IS the problem?
- Does **JTBD assume people can articulate their jobs**? (They often can't — observed behavior differs from stated preference)
- Does the wireframe step assume **visual fidelity correlates with usefulness**?

### Step 1b assumptions (after adding synthetic user research)

- Does Step 1b assume that **model-generated personas produce useful signal**? What's the null hypothesis?
- Does testing personas AFTER problem framing **reinforce the framer's biases**? (You constructed the personas from the problem spec YOU wrote)
- Is there **circular reasoning**? Problem spec → personas → reactions → JTBD → validates problem spec?
- Would running Step 1b BEFORE Step 1 (personas first, then problem framing) produce different results?

### Builder bias

- Is there **implicit builder-persona bias** in the whole framework? (High openness, high conscientiousness, systems-thinking orientation)
- Would a non-technical, non-builder user design a completely different pipeline?
- Does the pipeline optimize for **comprehensiveness** when users might need **speed**?

### Axiom explorer meta-recursion

- What are axiom explorer's own assumptions? (Socratic method assumes root beliefs exist and are discoverable)
- What are tribunal's own assumptions? (Multi-model comparison assumes model diversity = perspective diversity)
- Can you use this pipeline to invalidate itself? If not, it's not a real validation tool.

## When to Run This

- After implementing Step 1b, before declaring it production-ready
- When the pipeline produces surprising or suspicious results
- When you notice all studies producing similar outcomes (pipeline might be injecting uniformity)
- During skill quality reviews
- When a real user reacts differently than all synthetic personas predicted
