---
name: Current Reality Tree
description: A logical diagram that maps cause-effect relationships between undesirable effects to identify root causes that drive most organizational problems
---

## Overview

The Current Reality Tree (CRT) is one of the five thinking processes in Eliyahu Goldratt's Theory of Constraints. It's a diagnostic tool that analyzes complex organizational problems by visually mapping the network of cause-and-effect relationships between symptoms (Undesirable Effects) to identify the core problem or root cause driving them.

Unlike traditional root cause analysis that examines problems in isolation, the CRT recognizes that most organizational issues share common root causes. By revealing these connections, it prevents the "whack-a-mole" problem where solving one issue makes another worse, or where teams address symptoms while the underlying driver persists.

The power of the CRT lies in its logic-based structure. Each causal connection must pass sufficiency tests (does A truly cause B?), making it a rigorous analytical tool rather than speculation. The result is a tree diagram where multiple problems (UDEs) trace back to one or a few core causes—focusing improvement efforts with surgical precision.

## When to Use

Apply the Current Reality Tree when:

- Multiple problems seem unrelated but you suspect a common root cause exists
- Previous solutions haven't stuck, and problems keep recurring in different forms
- Teams disagree about what to fix first (CRT provides objective prioritization based on causal analysis)
- Symptoms are obvious but underlying causes remain unclear
- You need to build consensus around the true problem before proposing solutions
- System behavior is counterintuitive or results contradict stated policies

Don't use this framework for:

- Simple, isolated problems with obvious causes (CRT is overkill for straightforward issues)
- Time-critical situations requiring immediate action (CRT takes hours to days)
- Situations where symptoms are the actual problem, not manifestations of deeper issues
- Problems where data is unavailable to validate causal relationships

## Process

### Step 1: List Undesirable Effects (UDEs)

**Identify 5-10 symptoms or problems currently plaguing the system.** These are observable, measurable negative outcomes.

Be specific and factual: "Customer complaints increased 40% in Q3" not "customers are unhappy." "Deploy cycle time is 3 weeks" not "we're slow."

Include diverse UDEs from different parts of the organization. The goal is breadth—cast a wide net to capture the full problem landscape.

Test each UDE: Is this a symptom or a root cause? If it's something you can directly control, it's probably too deep (closer to a root cause). UDEs should be things you observe, not things you do.

### Step 2: Identify Direct Causes

**For each UDE, ask "What directly causes this to happen?"** Draw causal arrows from causes to effects.

Use rigorous logic: Does A alone cause B (sufficiency)? Or does A plus X cause B (combined sufficiency)? Be precise.

Look for entities that appear multiple times as causes. These are likely intermediate effects with their own underlying causes—candidates for further investigation.

Apply the "Categories of Legitimate Reservation" tests:
- **Clarity**: Is the entity clearly stated?
- **Entity Existence**: Does this entity actually exist in our system?
- **Causality Existence**: Does the cause truly lead to the effect?
- **Cause Sufficiency**: Is this cause enough to produce the effect, or are other causes needed?

### Step 3: Connect the Web

**Link intermediate effects to trace chains of causality backward.** Start from UDEs and work down, asking "What causes this?" until patterns emerge.

You'll see convergence: multiple branches tracing back to common entities. These connection points are critical—they indicate leverage points where one intervention affects multiple problems.

Watch for circular logic (A causes B causes A). This indicates a reinforcing feedback loop rather than simple causality. Note these separately.

Stop when you reach entities that are clearly controllable (policies, decisions, resource allocations). These are potential root causes.

### Step 4: Identify Core Problems

**Find the entities at the base of the tree that cause the most UDEs.** Typically, 80%+ of UDEs trace back to 1-3 core problems.

A core problem should:
- Be under your control or influence (not external factors like "the economy")
- Directly cause multiple intermediate effects that cascade to UDEs
- Be specific enough to act on (not "poor communication"—what policy creates poor communication?)

Validate with stakeholders: Does this logic hold? Are we missing causal connections? This builds shared understanding and ownership.

### Step 5: Verify the Logic

**Test the complete tree from bottom to top.** Starting from core problems, follow the arrows: if we had this core problem, would it logically produce these intermediate effects and UDEs?

Look for missing links: are there gaps in causality? Do we need additional entities to make the logic sound?

Challenge assumptions: what must be true for this causal relationship to hold? Document these assumptions—they're often the real root causes hiding beneath visible problems.

### Step 6: Validate Against Reality

**Check the CRT against observable data.** Does the tree predict current system behavior? Are there UDEs we observe that the tree doesn't explain? (If so, we're missing causes.)

Test with "what-if" scenarios: If we removed this core problem, would the UDEs disappear? If the tree says yes but stakeholders disagree, refine the analysis.

Socialize the CRT with people close to the problems. They'll spot flawed logic or missing connections quickly.

## Example

**Software team struggling with quality and delivery:**

**UDEs identified:**
- Bug backlog growing 15%/month
- Customer escalations up 50% in 6 months
- Releases delayed 60% of the time
- Developer burnout (2 quit this quarter)
- Technical debt increasing (test coverage falling)

**Causal analysis reveals:**
- Releases delayed because of last-minute bug discoveries
- Last-minute bugs happen because testing occurs late in cycle
- Late testing happens because developers rush to "code complete" before writing tests
- Developers rush because they're overcommitted to too many features
- Overcommitment happens because product roadmap doesn't account for tech debt time
- Product doesn't account for tech debt because leadership measures feature velocity only

**Core problem identified:** "Success metrics focus exclusively on feature output, ignoring quality and sustainability."

This single policy decision (how we measure success) cascades through developer behavior, testing practices, bug rates, release delays, and ultimately customer satisfaction. Fixing individual symptoms (hire more testers, mandate better tests) won't work until the core problem—the measurement system—changes.

## Anti-Patterns

**Stopping at symptoms**: Identifying "we need better testing" as the core problem when the real issue is resource allocation or incentive structures that prevent good testing.

**Creating trees too large**: 50+ entities makes the CRT unwieldy and obscures the core problem. If your tree is massive, you're likely including too much detail or not consolidating similar entities.

**Assuming correlation is causation**: "Sales are down and marketing budget is down, therefore budget cuts caused sales drops." Test rigorously: is there true causality or coincidental timing?

**Confusing UDEs with causes**: "Poor communication" is usually a symptom (UDE) of deeper issues like lack of shared goals, role clarity, or trust. Keep asking "why."

**Accepting vague entities**: "Culture problems" or "leadership issues" aren't actionable core problems. What specific policies, decisions, or structures create those manifestations?

**Skipping validation**: Building the CRT in isolation then presenting it as truth. The CRT is a hypothesis—validate it with people who live the problems daily.

**Analysis paralysis**: The CRT is a diagnostic tool, not an end in itself. Once you've identified the core problem with sufficient confidence, move to solution design (Evaporating Cloud, Future Reality Tree).

## Related Frameworks

- **Five Focusing Steps** (TOC): Broader methodology for constraint management; CRT helps identify the constraint
- **Evaporating Cloud** (TOC): Next step after CRT—resolves the core conflict perpetuating the root cause
- **Future Reality Tree** (TOC): Tests whether proposed solutions actually resolve the core problem without creating new UDEs
- **5 Whys** (Lean): Simpler linear root cause analysis; CRT handles multiple interconnected problems
- **Fishbone Diagram/Ishikawa**: Visual root cause tool; less rigorous about logic testing than CRT
- **Causal Loop Diagrams** (System Dynamics): Shows feedback loops and system behavior over time; complements CRT's snapshot view
- **Systems Thinking**: Broader discipline; CRT is a specific tool within systems thinking methodology
