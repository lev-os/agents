---
name: map-is-not-the-territory
description: Recognize that models, representations, and abstractions are simplifications of reality, not reality itself—confusing the two leads to errors
---

# Map Is Not the Territory

**What**: A principle stating that representations of reality (maps, models, abstractions, words) are not reality itself—they are simplified, selective, and potentially outdated interpretations that omit details.

**When to use**: When working with models, plans, documentation, or any abstraction; when decisions are based on representations rather than direct observation.

**Introduced by**: Alfred Korzybski (1931) in "Science and Sanity"; core principle of General Semantics

## Core Mechanism

**Maps differ from territory in three ways:**
1. **Maps are reductions**: They necessarily omit details (map of NYC isn't 1:1 scale)
2. **Maps are static**: Territory changes; maps become outdated
3. **Maps are interpretations**: Different mapmakers emphasize different features

**Key insight**: Mistaking the map for the territory leads to planning failures, model rigidity, and blind spots.

## Execution Steps

### 1. Identify Your Maps
What models, plans, or abstractions are you using? Code comments, architecture diagrams, roadmaps, metrics dashboards.

### 2. Check Map-Territory Alignment
When did you last verify the map matches current reality? Maps decay over time.

### 3. Recognize Map Limitations
What does this map omit? Every abstraction highlights some features, hides others.

### 4. Go to the Territory When Possible
Don't debate the map—check reality. Talk to users, read the code, measure directly.

### 5. Update Maps Regularly
Treat documentation as living artifact. Reality changed; update the map.

### 6. Hold Maps Lightly
Prefer "the map suggests X" over "X is true." Maps are provisional tools, not truth.

### 7. Use Multiple Maps
Different abstractions reveal different aspects. Combine perspectives.

## Real-World Applications

**Code Comments vs. Code**: Comments describe what code *should* do; actual code determines what *does* happen. When they diverge, code is territory, comments are outdated map.

**Architecture Diagrams**: Show intended design, not actual dependencies. Over time, shortcuts and hacks create reality diverging from diagram.

**Roadmaps**: Plans represent intended future, not actual trajectory. External factors change territory; sticking rigidly to map leads astray.

**Metrics Dashboards**: Show selected KPIs, not full system state. Goodhart's Law: optimizing the map (metrics) harms the territory (actual goals).

## Scoring Criteria

**Practitioner Weight**: 8/10 — Korzybski founded field; principle widely applied in engineering, strategy, epistemology
**Clarity & Executability**: 9/10 — Extremely clear metaphor; immediate actionability (go check territory, update maps)
**Proven ROI**: 8/10 — Prevents planning failures, model rigidity, documentation drift; core to agile "inspect and adapt"
**Novelty**: 7/10 — Somewhat intuitive once stated, but frequently violated in practice
**Cross-Domain Applicability**: 10/10 — Universal—software, strategy, communication, science, organizations

**Total Score**: 42/50 (Tier 1: Canonical)
