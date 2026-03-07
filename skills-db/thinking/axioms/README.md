# Axiom Explorer Framework

**Map beliefs, ideas, and prompts down to their root axioms and presumptions.**

A systematic framework for deep exploration using Socratic questioning, Humean skepticism, and empathetic inquiry. Functions as a "truth engine" for fact-checking, debate preparation, prompt refinement, and collaborative exploration.

---

## Quick Start

1. **Choose your goal** → Pick a command from the table below
2. **Run the skill stack** → Follow the sequence in order
3. **Get your output** → Actionable map with axioms, correlations, applications

**First time?** Try `/axiom-drill-down` (5-10 min) for quick Socratic exploration.

---

## 🎉 Status: Framework Fully Operational

**✅ All 10 skills codified** (2025-01-29)
- Complete input/output contracts
- Step-by-step execution instructions
- Output templates with required sections
- Quality checks for verification
- Examples from live execution
- Anti-patterns documented

**✅ Live execution validated** (axiom-20250129-002120)
- Full 7-step workflow completed successfully
- Generated 15 markdown files in 25 minutes
- Analyzed project's own core belief
- Confidence calibrated: 70% → 60-65%
- Result: "Bounded Pragmatism" - frameworks work in specific contexts

**📋 Ready to use:**
- All skills documented in `skills/*.md`
- All commands defined in `commands/*.md`
- Operating process in `docs/operating-process.md`
- Philosophy and safeguards established

---

## File Structure

```
domains/axioms/
├── README.md                 # This file
│
├── skills/                   # 10 reusable atomic patterns
│   ├── INDEX.md             # Full skill catalog with usage
│   ├── paraphrase-engineer.md
│   ├── steelman-enhance.md
│   ├── dig-axioms.md
│   ├── map-elements.md
│   ├── multi-devils-debate.md
│   ├── synthesize-apply.md
│   ├── reflection-loop.md
│   ├── proactive-guessing.md
│   ├── ans-quadrant-mapping.md
│   └── correlation-grounding.md
│
├── commands/                 # 8 orchestrated workflows
│   ├── INDEX.md             # Full command catalog with timing
│   ├── full-chain.md
│   ├── axiom-drill-down.md
│   ├── steelman-correlations.md
│   ├── unconceived-explorer.md
│   ├── emotional-tribal-mapper.md
│   ├── multi-side-debate.md
│   ├── prompt-digger.md
│   └── self-reflection.md
│
└── docs/                     # Reference materials
    ├── philosophy.md         # Socratic method, Humean skepticism, tone
    ├── safeguards.md         # Anti-hallucination, anti-sycophancy protocols
    └── ux-patterns.md        # Numbered suggestions, templates, visualizations
```

---

## When to Use This Framework

**Core Use Cases:**
- 🧠 **Exploring complex beliefs** - Trace reasoning to foundational assumptions
- 🤝 **Preparing for debates** - Understand your position and opposition deeply
- 🤖 **Refining LLM prompts** - Make implicit concepts explicit
- 💭 **Understanding emotional/tribal reasoning** - Map feelings, belonging, status drivers
- 🔍 **Fact-checking claims** - Ground arguments in empirical correlations
- 🔬 **Building hypotheses** - Formulate testable experiments from refined axioms
- 🏗️ **Practical building** - Blueprints for products, features, strategies

---

## Commands Overview

| Command | Purpose | Time | Output |
|---------|---------|------|--------|
| **full-chain** | Deep comprehensive analysis | 30-45min | Complete map with all perspectives |
| **axiom-drill-down** | Quick why-chain | 5-10min | Root axioms via Socratic questioning |
| **steelman-correlations** | Strengthen argument with data | 10-15min | Best version + empirical backing |
| **unconceived-explorer** | Find hidden assumptions | 10-15min | Blind spots and alternatives |
| **emotional-tribal-mapper** | Map feelings/tribal drivers | 15-20min | Emotional, political, ANS analysis |
| **multi-side-debate** | Simulate multiple perspectives | 20-30min | Multi-angle debate with synthesis |
| **prompt-digger** | Refine LLM instructions | 10-15min | Improved prompts with explicit concepts |
| **self-reflection** | Meta-analysis of own work | 5-10min | Process improvement and iteration |

**See `commands/INDEX.md` for detailed descriptions and skill stacks.**

---

## Skills Reference

### Core Sequential Skills (1-7)

1. **paraphrase-engineer** - Rephrase with variations to expose axioms
2. **steelman-enhance** - Build strongest charitable version
3. **dig-axioms** - Socratic "why?" questioning
4. **map-elements** - Detail axioms, emotions, tribal alignments
5. **multi-devils-debate** - Simulate opposing perspectives
6. **synthesize-apply** - Integrate findings, suggest applications
7. **reflection-loop** - Gather feedback, iterate

### Supporting Techniques

- **proactive-guessing** - Generate 5-8 diverse presumptions
- **ans-quadrant-mapping** - Map to Autonomic Nervous System states
- **correlation-grounding** - Anchor in empirical data

**See `skills/INDEX.md` for when to use each skill.**

---

## Philosophy & Approach

### Core Principles

**Socratic Method**
- Iterative questioning ("why why why") to expose assumptions
- Intellectual humility over certainty
- Stimulate critical thinking through exploration

**Humean Skepticism**
- Prioritize emotions, tribal affiliations, status-seeking over pure rationality
- Focus on empirical correlations, not causal necessity
- Doubt certainty, embrace uncertainty

**Tone: Neutral, Empathetic, Gentle**
- Non-judgmental exploration
- Frame as "possible mappings" not absolute truth
- Steelman all perspectives (strongest charitable version)
- Active listening through paraphrasing

**See `docs/philosophy.md` for detailed methodology.**

---

## Safeguards & Quality

Built-in protocols to mitigate LLM weaknesses:

- **Hallucinations** - Grounding via web search (RAG), Chain-of-Thought checks, explicit uncertainty
- **Sycophancy** - Neutrality prompts, offer alternatives instead of agreement
- **Lying/BS** - Honesty ("This is a guess"), fact-checking loops, correlation focus
- **Simulations** - Explicitly forbidden outside defined debate roles

**See `docs/safeguards.md` for full protocols.**

---

## User Experience Features

- **Numbered suggestions** - 5-8 contextual options (2-4 sentences) for easy selection
- **Template filling** - Structured formats with guidance for custom input
- **Inline replies** - Respond directly after sections
- **Visualizations** - Tables (Markdown) and graphs (Mermaid) for data/processes
- **Opt-in features** - ANS mapping, detailed nuance, visuals are optional
- **Low effort** - Minimize user typing, maximize exploration

**See `docs/ux-patterns.md` for interaction design.**

---

## Hidden Gems Dependencies

This framework leverages 10 powerful thinking frameworks (most already catalogued in `domains/hidden-gems/`):

| Framework | Used In | Status |
|-----------|---------|--------|
| **ARIZ** | steelman-enhance | ✅ [Documented](../hidden-gems/ariz.md) |
| **ACH** (Analysis of Competing Hypotheses) | dig-axioms | ✅ [Documented](../hidden-gems/analysis-competing-hypotheses.md) |
| **Polyvagal Theory** | map-elements | ✅ [Documented](../hidden-gems/polyvagal-theory.md) |
| **Cynefin Framework** | synthesize-apply | ✅ [Documented](../hidden-gems/cynefin-framework.md) |
| **OODA Loop** | reflection-loop | ✅ [Documented](../hidden-gems/ooda-loop.md) |
| **VSM** (Viable System Model) | orchestration | ✅ [Documented](../hidden-gems/viable-system-model.md) |
| **ITN Framework** | prioritization | ✅ [Documented](../hidden-gems/itn-framework.md) |
| **JTBD** (Jobs-to-be-Done) | applications | ✅ [Documented](../hidden-gems/jobs-to-be-done.md) |
| **Second-Order Thinking** | multi-devils-debate | ⚠️ In catalog, needs research ([Domain 01](../01-core-mental-models/task.csv), row 4) |
| **THINK Paradigm** | paraphrase-engineer | ❌ **Missing** - Needs research and documentation |

**Gaps identified:**
- **THINK Paradigm** - Not yet in catalog, referenced in original Axiom Explorer spec
- **Second-Order Thinking** - Catalogued but STATUS=UNKNOWN, needs full documentation

---

## Command Selection Guide

**I need to...**

- Understand a complex belief completely → **full-chain**
- Find root assumptions quickly → **axiom-drill-down**
- Strengthen weak argument → **steelman-correlations**
- Find blind spots → **unconceived-explorer**
- Understand emotional/political drivers → **emotional-tribal-mapper**
- Prepare for debate → **multi-side-debate**
- Improve LLM prompts → **prompt-digger**
- Validate my work → **self-reflection**

---

## Bootstrap & Integration

### Standalone Use
Each skill and command can be run independently via Claude Code or as prompts.

### Slash Command Integration
Commands are designed to work as `.claude/commands/` slash commands:

```bash
# Example: Make axiom-drill-down.md available as /axiom-drill-down
cp commands/axiom-drill-down.md ~/.claude/commands/
```

### Workflow Orchestration
Chain commands together for custom exploration:

```
1. Start with axiom-drill-down for quick mapping
2. Follow with emotional-tribal-mapper if sensitive topic
3. Finish with self-reflection to validate
```

### Context Loading
Reference skills in your prompts:

```
"Use the dig-axioms skill from domains/axioms/skills/ to explore why I believe X"
```

---

## Suggested First Command

**New to Axiom Explorer?** Start here:

```
Command: axiom-drill-down
Topic: Pick any belief you hold (e.g., "AI will replace knowledge work")
Time: 5-10 minutes
Expected: Root axioms exposed, quick synthesis
```

This gives you a feel for the Socratic method and output format before diving into longer explorations.

---

## Credits & Origin

This framework synthesizes insights from:
- Socratic questioning tradition
- David Hume's skeptical empiricism
- Modern cognitive science (Big 5, Haidt's moral foundations, Polyvagal Theory)
- Decision science (ACH, Cynefin, OODA)
- Problem-solving methods (ARIZ, TRIZ principles)

**Original concept:** "Axiom Explorer" / "Axiom Forge" multi-agent system for belief mapping and truth exploration.

---

## Contributing

To extend this framework:

1. **Add new skills** - Document in `skills/` with clear purpose and usage
2. **Create custom commands** - Chain existing skills for specific workflows
3. **Research missing gems** - Complete THINK Paradigm and Second-Order Thinking documentation
4. **Improve UX patterns** - Enhance templates, visualizations, interaction design
5. **Test and refine** - Run commands on real beliefs, iterate based on learnings

---

## Related Domains

- [Hidden Gems](../hidden-gems/) - Deep dives on leveraged frameworks
- [Core Mental Models](../01-core-mental-models/) - Foundational thinking tools
- [Decision-Making](../04-decision-making/) - Probabilistic reasoning and strategy
- [Cognitive Biases](../02-cognitive-biases/) - Understanding reasoning errors

---

**Ready to explore?** See `commands/INDEX.md` to pick your first workflow.
