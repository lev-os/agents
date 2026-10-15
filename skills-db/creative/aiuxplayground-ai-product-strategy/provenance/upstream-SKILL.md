---
name: ai-product-strategy
description: Help users decide where to apply AI effectively, manage the transition from deterministic to probabilistic software, and build long-term defensibility through verticalization and proprietary data.
---

# AI Product Strategy

Prioritize high-impact workflows and navigate non-deterministic development to build defensible AI products.

Help the user with ai product strategy using insights from 26 guests and posts across Lenny's Podcast and Newsletter.

## How to Help

1. **Define the wedge** - Identify high-friction chores where AI can provide a disproportionate payoff for the user.
2. **Select the architecture** - Choose between retrieval-augmented generation (RAG) and fine-tuning based on the need for live data vs. specific behavior.
3. **Scale agency safely** - Design a graduated approach to autonomy that keeps humans in the loop before moving to full automation.
4. **Build for the curve** - Align product roadmaps with future model capabilities rather than building complex scaffolding for today's limitations.

## Core Principles

### Account for squishy outputs
Alex Komoroske: "LLMs allow writing shitty software to be significantly cheaper, not necessarily good software, but good enough in certain contexts. And also it means that there's certain software now that isn't plain old computing that can be run cheaply. It's relatively expensive marginal cost."

Design product experiences that assume AI is non-deterministic and imperfect rather than trying to force 100% accuracy into your UI.

### Treat products as living organisms
Asha Sharma: "Because these models are so effective at this point, you want to start to tune them to certain types of outcomes. All of a sudden, these are these living organisms that just get better with the more interactions that happen. I think this is the new IP of every single company products that think and live and learn."

Measure success by the team's metabolism in ingesting data and improving learning loops rather than static feature releases.

### Find defensibility in verticalization
Logan Kilpatrick: "We're not going to launch some of these varied verticalized products. We're not going to launch an AI sales agent. That's just not what we're building towards. And companies who are and have some domain specific knowledge and they're really excited about that problem space, they can go into that and leverage our models and end up continuing to be on the cutting edge without having to do all that R&D effort themselves."

Avoid competing with foundational models by targeting specific industry niches where domain expertise provides a structural advantage.

### Incubate specific superpowers
Noah Weiss: "I think in the AI space, we're trying to hear from customers, what do you wish Slack could do if it had these new superpowers? Let's incubate a couple teams or prototype, give them space to run and pilot and then get something to launch that's amazing. Blows people away. That's the formula that we've seen."

Avoid generic AI features by identifying specific customer needs and giving dedicated teams space to prototype them independently.

### Build for the model's future
Sherwin Wu V2: "The field and the models themselves are just changing so, so quickly. They tend to disrupt themselves. The models will eat your scaffolding for breakfast."

Design for the capabilities expected in 12 to 18 months to avoid building custom scaffolding that will eventually be absorbed natively by the models.

### Adopt a graduated approach to autonomy
Aishwarya Naresh Reganti + Kiriti Badam: "You need to be deliberately starting in places where there is minimal impact and more human control so that you have a good grip of what are the current capabilities and what can I do with them and then slowly lean into the more agency and lesser control."

Safely deploy agentic systems by starting with human-in-the-loop suggestions before scaling to full autonomous interactions.

## Templates & Frameworks

- **AI Glossary - 20+ Key Terms** (An AI glossary) - A comprehensive reference list of AI terms with 'explain it like I'm 5' definitions, designed to be kept handy for meetings
- **AI Product Builder's 12 Principles** (Counterintuitive advice for building AI products) - A set of 12 counterintuitive principles for building AI products, compiled from 20+ AI product leaders across companies like GitHub, Canva, Superhuman, Perplexi
- **CC/CD (Continuous Calibration/Continuous Development) Framework** (Why your AI product needs a different development lifecycle) - A six-step development lifecycle framework for AI products that accounts for non-determinism and the agency-control tradeoff. Replaces traditional CI/CD thinkin
- **AI Integration Decision Framework** (Summary: AI and product management | Marily Nika (Meta, Google)) - A decision-making approach for when and how to add AI to your product
- **The Bitter Lesson Applied to AI Product Building** (Sherwin Wu V2) - Extension of Rich Sutton's Bitter Lesson to building products with AI — scaffolding and workarounds get eaten by model improvements
- **AI Startup Defensibility Framework** (Peter Deng) - Three pillars for building defensible AI startups: proprietary data flywheels, crafted workflows, and product craft that overcomes incumbent distribution.
- **AI Product Mindset Shift: Prototype-First vs. Design-First** (Counterintuitive advice for building AI products) - A framework contrasting the traditional software development approach with the AI-native approach where feasibility is uncertain
- **AI Product Differentiation Stack: Data > Interface > Model** (Counterintuitive advice for building AI products) - A hierarchy for where lasting competitive advantage lies in AI products
- **Stickiness Over Moats in AI** (Scott Wu) - In AI products, defensibility comes from compounding stickiness (accumulated knowledge, team workflows, learning) rather than hard barriers to entry

See `references/artifacts.md` for the full list with details.

## Questions to Help Users

- "What is the high-friction chore in your product where automation offers the biggest payoff?"
- "Does your use case require access to live, internal data or a specific, consistent behavior style?"
- "How are you designing the interface to handle non-deterministic or incorrect AI outputs?"
- "Are you building a feature that a foundational model update will likely render obsolete in a year?"
- "What proprietary data do you have that competitors cannot easily access or replicate?"
- "How will you measure the metabolism of your product's learning loops over time?"

## Common Mistakes to Flag

- **Building for current model limitations** - Creating complex scaffolding to solve today's model weaknesses is a losing strategy as foundational models will soon absorb that functionality.
- **Adding AI for its own sake** - Generic AI features without a validated, data-backed user problem fail to provide meaningful value or defensibility.
- **Assuming 100% accuracy** - Failing to account for the probabilistic nature of AI leads to broken user experiences when the model inevitably hallucinates.
- **Prioritizing prompt engineering over data** - The effectiveness of AI features is often constrained more by the quality and timeliness of underlying data than the prompt itself.

## Deep Dive

For all 45 sourced insights from 26 guests, see `references/guest-insights.md`

## Related Skills

- Ai Evals
- Ai Native Ux
