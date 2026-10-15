# AI Product Strategy - Frameworks, Templates & Checklists

*95 artifacts extracted from Lenny's Podcast and Newsletter*

## Frameworks

### 3 Pillars of AI Integration (Cam Adams)
A decision-making framework for how to source and implement AI features in a product.

How it works: Pillar 1: Build proprietary tech where you have a data advantage (e.g., design/images). Pillar 2: Partner with best-in-class for commodities (e.g., OpenAI for text, RunwayML for video). Pillar 3: Leverage an app developer ecosystem for niche use cases (e.g., music generators, avatars).

### 4 Layers of Enterprise AI Evolution (Marc Benioff)
A mental model for how enterprise AI capabilities stack and evolve over time.

How it works: Layer 1: Automate customer touchpoints (sales, service, marketing). Layer 2: Aggregate data into a unified cloud (Data Cloud). Layer 3: Agentic platform (Agentforce resolving issues autonomously). Layer 4: Robotic drone layer feeding off the platform.

### 8 Prompt Engineering Techniques Framework (Five proven prompt engineering techniques (and a few more-advanced tactics))
A structured collection of 8 prompt engineering techniques organized into 5 core tactics and 3 advanced tactics, each with templates, examples, and academic sources

How it works: CORE TACTICS:
1. Role-playing - Instruct AI to assume expert persona
2. Style unbundling - Break down expert style into components, then apply
3. Emotion prompting - Add emotional stakes to get more careful responses
4. Few-shot learning - Provide examples before asking for similar output
5. Synthetic bootstrap - Use AI to generate examples, then use those as inputs

ADVANCED TACTICS:
6. Chain-of-thought - Break complex problems into step-by-step reasoning
7. Retrieval-augmented generation (RAG) - Provide relevant documents as context
8. LLM-as-a-judge - Use AI to evaluate and rate quality of outputs

### AI Agent Cost Optimization Levers (Make product management fun again with AI agents)
Two-lever framework for reducing AI agent operational costs, with guidance on when to bother optimizing.

How it works: Two levers to reduce AI agent costs:
1. Pick a cheaper model
2. Feed it less data

Process:
- First, get the thing working with a good model and lots of data
- If it's not a frequent use case, don't bother with cost optimization
- If it runs 100+ times a day and costs $10 each time, then pull the two levers

Context from Flo Crivello (Lindy): 'Companies have millions and millions of dollars in payroll and then they spend a thousand dollars on an AI. Every dollar you spend on the AI agent platform is saving you $10 that a human would have done otherwise.'

### AI App Improvement Matrix (Chip Huyen)
A comparative framework highlighting the difference between perceived high-value AI tasks and actual high-value AI tasks.

How it works: What people think improves apps: Staying up to date with news, adopting newest agentic frameworks, agonizing over vector databases, constantly evaluating smarter models, fine-tuning. What actually improves apps: Talking to users, building reliable platforms, preparing better data, optimizing end-to-end workflows, writing better prompts.

### AI Integration Decision Framework (Summary: AI and product management | Marily Nika (Meta, Google))
A decision-making approach for when and how to add AI to your product

How it works: Step 1: Start from the problem. Ask 'Is there a problem that can be solved with a smart solution?' — don't start from the technology.
Step 2: Avoid the shiny object trap. Make sure there is a real pain point before considering AI.
Step 3: Check your data. Only use AI when you already have some data, or data from an adjacent product.
Step 4: For MVP/buy-in, don't build AI yet. Create a Figma prototype and a demo of what the experience will be like.
Step 5: For every product you ship, ask: 'Can this be made smarter?' Examples: fraud detection, healthcare accuracy, personalization.
Step 6: Determine build vs. buy. Most startups should use off-the-shelf models. Build your own only if existing solutions don't meet needs or you have a competitive advantage (more relevant for larger companies).

### AI Model Customization Spectrum (An AI glossary)
A summary framework distinguishing the five key techniques for teaching and customizing AI models, from broad training to runtime augmentation

How it works: 1. Pre-training: Teaches the model general knowledge (and language)
2. Fine-tuning: Specializes the model for specific tasks
3. RLHF: Aligns the model with human preferences
4. Prompt engineering: The skills of crafting better inputs to guide the model toward the most useful outputs
5. RAG: A technique that retrieves additional relevant information from external sources at run-time to give the model up-to-date or task-specific context it wasn't trained on

### AI Model Training Stages (Garrett Lord)
Mental model for understanding how AI models are developed and improved.

How it works: 1. Pre-training: Sucking up the entire corpus of written human knowledge. 2. Post-training: Augmenting and improving data across specific disciplines using RLHF (preference ranking), SFT (prompt-response pairs), Trajectories (step-by-step tool use), and Rubrics (models acting as judges).

### AI Product Builder's 12 Principles (Counterintuitive advice for building AI products)
A set of 12 counterintuitive principles for building AI products, compiled from 20+ AI product leaders across companies like GitHub, Canva, Superhuman, Perplexity, and others

How it works: 1. Think AI-native, not bolt-on: The first-pass product is often a bolt-on or chat experience. The high-value experience requires a deeper rethink. Start by asking 'What is technologically possible?' and prototype.
2. Solve real problems: Demo value isn't user value. Building a cool AI demo doesn't mean customers love it.
3. Design great UX to teach usage: Give people starting points and confidence. Reduce fear of empty prompt boxes. AI tools require intuitive design AND ongoing education.
4. Leverage proprietary data: Data and interfaces may matter more than models. Companies with deep vertical data (properly licensed) will have an advantage.
5. Be intentional about your wedge: Start with a core workflow that feels like a chore where promise-to-payoff is high if you get it right. Select for big reward and repeat use.
6. Brand it as AI: Labeling features as 'AI-powered' increases engagement and helps users understand capabilities.
7. Start small: Tiny, almost invisible features (pre-filling names, data transformations) often have bigger impact than Big AI Features. Focus on what users do 100 times a day.
8. Expect imperfection: AI is probabilistic, not deterministic. Give users options, invest in prompt engineering, measure acceptance rates. GitHub Copilot's 35% acceptance rate benchmark.
9. Build for improving models: Design products to leverage foundation model strengths that automatically improve as models improve. RAG works well with right context.
10. Plan for scale: Avoid excessive scaffolding logic. Prefer fine-tuning and few-shot training. Plan infrastructure scalability from the outset.
11. Rethink your metrics: Best AI features may reduce time-in-app. Don't be surprised—gen AI finds best PMF with productivity tools.
12. Prioritize speed: Pre-compute AI outputs so they're instantaneous. Speed alone is a massive lever on UX.

### AI Product Desirability-Viability-Feasibility Triangle (Summary: AI and product management | Marily Nika (Meta, Google))
A three-circle Venn diagram for evaluating AI product opportunities: find the intersection of user desirability, business viability, and research/technical feasibility

How it works: Three overlapping circles:
1. Desirable by users — Is there real user demand for this?
2. Viable business — Can this be monetized or create business value?
3. Feasible from a research-scientist and technical perspective — Can the AI/ML actually deliver this with current technology and data?

The sweet spot is the intersection of all three. This extends the traditional desirability-viability-feasibility framework by explicitly calling out research feasibility as distinct from engineering feasibility.

### AI Product Differentiation Stack: Data > Interface > Model (Counterintuitive advice for building AI products)
A hierarchy for where lasting competitive advantage lies in AI products

How it works: Three layers of AI product differentiation (from most to least defensible):

1. Proprietary/uniquely structured data (with proper licensing, not scraped)
2. Superior interface that transforms antiquated workflows
3. Models (increasingly commoditized, available via open source, moving to edge/local)

Implications:
- Companies with deep vertical data understanding will have an advantage
- Designers will be more important than ever
- Models will run locally on devices within a few years
- License to use data matters more than ability to scrape it

### AI Product Management Venn Diagram (Marily Nika)
A mental model for finding the sweet spot for an AI product feature.

How it works: The intersection of three bubbles: 1) Desirable by users, 2) Viable for the business, and 3) Feasible from a research scientist and technical perspective.

### AI Product Mindset Shift: Prototype-First vs. Design-First (Counterintuitive advice for building AI products)
A framework contrasting the traditional software development approach with the AI-native approach where feasibility is uncertain

How it works: Traditional software (past 10 years):
1. Assume what you want to build can be fairly easily built
2. Deeply understand the customer problem and opportunity
3. Design what you believe to be a great solution
4. Build it

AI-native approach:
1. Start by asking 'What is technologically possible?'
2. Prototype to test feasibility
3. Validate that it's actually good (even if it appears good, it may not be)
4. Iterate on prompts, model selection, and UX

Key difference: With AI, it is wholly unclear if something is possible to build, and when built, wholly unclear if it is any good.

### AI Safety Levels (ASL) (Benjamin Mann)
A risk assessment framework to categorize the potential societal harm of AI models at different intelligence thresholds.

How it works: ASL-3: Minor risk of harm but not significant (current state). ASL-4: Significant loss of human life if a bad actor misuses the technology (e.g., biological uplift/pandemics). ASL-5: Extinction-level risk if misused or if the model becomes misaligned and pursues its own goals.

### AI Startup Defensibility Framework (Peter Deng)
Three pillars for building defensible AI startups: proprietary data flywheels, crafted workflows, and product craft that overcomes incumbent distribution.

How it works: Pillar 1: Proprietary Data Flywheel — start with unique data, build a mechanism where product usage generates more valuable data, train models on that data to improve the product (example: Windsurf's code acceptance/rejection data). Pillar 2: Crafted Workflow — deeply understand a vertical, integrate into how people actually work, make the product ergonomically fit into people's lives. Pillar 3: Product Craft — build something so delightful that users switch from incumbents with massive distribution advantages (example: Granola overcoming Google Meet/Zoom, Cursor/Windsurf beating Microsoft Copilot).

### AI Wedge Selection Criteria (Promise-to-Payoff Matrix) (Counterintuitive advice for building AI products)
A framework for selecting which workflow to apply AI to first, based on the ratio of user effort to reward

How it works: Selection criteria for your initial AI wedge workflow:
- Core workflow that feels like a chore (high frequency, low satisfaction)
- Promise-to-payoff ratio is high if you get it right
- Upfront user effort (trying it out, customizing) yields big reward (substantial time savings)
- Invites repeat use (not a one-time interaction)

The diagram shows a 2x2 with axes of 'User effort to set up/try' vs 'Reward/time savings delivered' — target the quadrant where effort is reasonable but reward is high.

### AI as New Teammate Analogy (Why your AI product needs a different development lifecycle)
A mental model for deciding how much autonomy to give an AI system, comparing it to onboarding a new team member.

How it works: Core analogy: Treat your AI system like onboarding a brilliant new teammate who doesn't yet know how your team works.

- Don't hand them your highest-stakes projects on day one
- Start small and observe their work
- Build trust through demonstrated competence
- As they show what they can handle, gradually expand their scope
- AI systems need the same graduated path from low to high autonomy

This maps directly to the CC/CD framework: each version is like expanding the scope of what you trust the 'teammate' to do independently.

### AI product differentiation test (Tamar Yehoshua)
When building AI products, ensure your differentiator is something that persists and improves as LLMs get better, rather than compensating for current LLM weaknesses.

How it works: Key questions: 1) Does your product get better as LLMs get better? 2) Are you building compensations for current LLM weaknesses that will become obsolete? 3) Is your differentiator independent of specific LLM limitations? It's okay to build temporary compensations if you understand they'll go away, but they can't be your differentiator.

### AI-First Product Leadership Mindset (Tomer Cohen)
A framework for PMs to take ownership of AI as the core engine of their product, not delegate it to engineering

How it works: Key questions every PM should answer: 1) What is the objective of our algorithm? (write it on a board as a mathematical formula) 2) What features/parameters have we added for the algorithm to learn on? 3) What is our data collection and fine-tuning strategy? 4) What infrastructure changes could unlock product outcomes? Analogy: River rafting boat — everyone adds speed and accuracy (features), but the guide (PM) holds the two pedals that navigate the boat (AI). If you're not the guide, what are you doing?

### Agent Behavior Spectrum (An AI glossary)
A framework for evaluating how 'agentic' an AI system is, based on five behavioral criteria

How it works: An AI system becomes more 'agentic' the more of these behaviors it exhibits:
1. Acts proactively — as opposed to waiting to be prompted
2. Makes its own plan — as opposed to being given instructions
3. Takes real-world action (e.g., updating a CRM, running code, commenting on a ticket) — as opposed to only sharing recommendations
4. Draws on live data (e.g., web search, customer support queue) — as opposed to relying on static training or manually uploaded files
5. Creates its own feedback loop — watches its own output and iterates without human assistance

### Agentic Behavior Spectrum (Make product management fun again with AI agents)
A framework for evaluating how 'agentic' an AI system is, based on six behaviors. Used to map and compare different AI product categories.

How it works: Six agentic behaviors (each adds to the 'agent' spectrum):
1. Acts proactively — as opposed to waiting to be prompted
2. Makes a plan — as opposed to being given instructions
3. Leverages context — accessing internal knowledge base, pulling up-to-date info regularly
4. Draws on live data — web search, support queue (vs. static training or manual uploads)
5. Takes real-world action — updates CRM, runs code, comments on ticket (vs. only recommendations)
6. Creates its own feedback loop — watches own output and iterates without human assistance

Product categories mapped against these behaviors:
- AI Chat (e.g., ChatGPT, Claude)
- AI Copilots (e.g., Cursor, GitHub Copilot)
- AI Prototyping (e.g., Lovable, Bolt)
- AI Automations (e.g., Zapier, Lindy, Relay, Gumloop, Cassidy)
- AI Agents (fully autonomous)

Each category checks some but not all boxes. The 'AI automations' category is currently the most practical for PM busywork.

### Artificial Social Intelligence (Sander Schulhoff)
A concept analogous to social intelligence but for human-AI communication - understanding how to talk to AIs, interpret their responses, and adapt prompts accordingly

How it works: Three components: 1. Understanding the best way to talk to AIs (prompt construction). 2. Understanding what their responses mean (output interpretation). 3. Adapting your next prompts based on responses (iterative refinement). Parallels interpersonal social intelligence but applied to AI communication.

### Bloom's 2 Sigma Effect (Marc Andreessen)
An educational framework demonstrating that 1-on-1 tutoring improves student outcomes by two standard deviations.

How it works: Used to justify the use of AI as a personalized tutor. It takes a student from the 50th percentile to the 99th percentile by providing a tight feedback loop and real-time correction.

### Build for Where Models Are Going (Sherwin Wu V2)
Product strategy principle for AI startups — build for 80% capability that clicks when models improve rather than optimizing for current model limitations

How it works: 1. Don't build scaffolding to compensate for current model weaknesses — models eat scaffolding for breakfast. 2. Build products that assume 80% of needed capability exists today. 3. Ship something that 'almost works' — as models improve (o3 → 5.1 → 5.2), the product suddenly clicks. 4. Don't blindly follow customer requests for better versions of current tooling (vector stores, agent frameworks) — these are local maxima. 5. Balance customer feedback with your thesis on where models are heading in 1-2 years. Key quote from Kevin Weil: 'This is the worst the models will ever be.'

### CC/CD (Continuous Calibration/Continuous Development) Framework (Why your AI product needs a different development lifecycle)
A six-step development lifecycle framework for AI products that accounts for non-determinism and the agency-control tradeoff. Replaces traditional CI/CD thinking for AI systems.

How it works: The CC/CD framework is a continuous loop with two phases:

**Continuous Development (CD):**
1. CD 1: Scope capability and curate data — Define the version by agency level (not features). Start with high-control, low-agency. Build a reference dataset of 20-100 examples.
2. CD 2: Set up application — Build the simplest version. Set up logging (user inputs, system outputs, interactions). Design control handoffs for humans to take back control. Add guardrails and compliance basics. Don't overengineer.
3. CD 3: Design evals — Define application-specific evaluation metrics tied to the scoped task. Run evals against the reference dataset. Aim for broad coverage, not perfection.

**Transition: Deploy** — Deploy to a small cohort. Not a finish line, but a transition to calibration.

**Continuous Calibration (CC):**
4. CC 4: Run evals — Run eval metrics on live interaction data. Sample intelligently using system-specific signals (reroutes, thumbs up/down, conversation turns). Use control handoff logs as eval signals.
5. CC 5: Analyze behavior and spot error patterns — Manually review 20-50 low-accuracy examples. Focus on weakest-performing segments. Document error patterns in a table.
6. CC 6: Apply fixes — Apply targeted fixes (prompt tweaks, model changes, retrieval improvements). Re-run evals. Revisit eval design if needed. Iterate steps 2-5.

**Repeat:** Each cycle earns more agency. Gradually move from high-control/low-agency to low-control/high-agency.

### Chef-to-Ingredients Mindset Shift for AI Products (Tomer Cohen)
Analogy for how AI changes the PM's role from controlling every aspect of the experience to controlling the ingredients and guidelines

How it works: Traditional PM: Like a chef deciding every part of the dish — ambiance, temperature of the broccoli, exact user flows, defaults, onboarding progression. AI-first PM: Provide the ingredients and cooking guidelines, then let AI create personalized experiences. Key shift: AI is not deterministic, so you must give it rope to learn. Build safety guards and responsible AI around it, but let go of controlling the exact experience.

### Continuous Calibration, Continuous Development (CCCD) (Aishwarya Naresh Reganti + Kiriti Badam)
An iterative lifecycle framework for building AI products that adapts to non-deterministic user behavior and model outputs.

How it works: Continuous Development (Right Loop): Scope capability, curate data, setup application, design evaluation metrics, deploy. Continuous Calibration (Left Loop): Analyze behavior in production, spot error patterns, apply fixes, design new evaluation metrics for emerging patterns.

### Data Requirements Guide for AI Products (Summary: AI and product management | Marily Nika (Meta, Google))
Rules of thumb for how much data you need depending on the type of AI product

How it works: Low data (e.g., 20 labeled examples): Simple classification tasks like determining if a photo is of a cat or a dog.
High data (thousands of data points): Complicated NLP products, voice recognizers, and other complex AI systems.
Key insight: Data requirements scale with the complexity of the task.

### Defensible AI Startup Criteria (Mike Krieger)
A mental model for evaluating if an AI startup idea will survive against foundational model incumbents.

How it works: Four pillars of defensibility: 1. Differentiated industry knowledge (e.g., specific legal or biotech workflows). 2. Differentiated go-to-market (knowing exactly which persona buys the tool). 3. Novel distribution or UI form factors (building weird, advanced power-user interfaces). 4. Existential startup speed and drive.

### Diverge Then Converge for AI Integration (Tomer Cohen)
A two-phase approach to integrating AI into product roadmaps: first let teams explore freely, then converge top-down on the best bets

How it works: Phase 1 (Diverge): Ask teams to let go of existing roadmaps. Go back to core objectives they were trying to solve. Explore how new AI capabilities could solve those objectives better. Allow duplicates and creativity. Focus on learning. Phase 2 (Converge): Top-down selection of the 4-5 best bets. Consolidate resourcing. Run focused weekly reviews on just those bets. Account for capacity and cost constraints.

### Economic Turing Test (Benjamin Mann)
A threshold for defining Transformative AI based on economic replacement rather than general intelligence.

How it works: Contract an AI agent for a job for 1-3 months. If the employer decides to hire the agent thinking it's human, it passes the test for that role. If AI passes this test for 50% of money-weighted jobs in the economy, society has reached Transformative AI.

### Embeddings Explained (Latitude/Longitude Analogy) (I built a Lenny chatbot using GPT-3. Here’s how to build your own.)
Simple mental model for understanding what embeddings are and why they're useful

How it works: Embeddings are a condensed mathematical representation of text chunks. Analogy: Just like latitude and longitude can help you tell how close two cities are on a map, embeddings do the same for text. If you want to know if two pieces of text are similar, calculate their embeddings and compare — chunks with embeddings that are 'closer' together are semantically similar. This makes it easy to search a content archive and find articles most likely to answer a given question. Cost: $0.0004 per 1,000 tokens.

### Ensemble of Models Architecture (Kevin Weil)
Breaking down a complex problem and routing specific tasks to different models based on cost, speed, and reasoning requirements.

How it works: Treat models like a company of specialized humans. Use o-series for deep reasoning, 4o-mini for fast/cheap checks, and fine-tuned models for specific tasks. Combine their outputs for a superior final result.

### GPT-3 Chatbot Architecture Pattern (I built a Lenny chatbot using GPT-3. Here’s how to build your own.)
A 4-step architecture for building a chatbot that can answer questions based on a custom content archive

How it works: Step 1: Download and store the content archive in a searchable format (create embeddings). Step 2: Build code to find relevant chunks of text from the archive given a user question. Step 3: When a user asks a question, retrieve the most relevant chunks and insert them into the GPT-3 prompt as context. Step 4: Display the resulting answer to the user. This is essentially a Retrieval-Augmented Generation (RAG) pattern.

### Human-Centered AI Framework (Dr. Fei Fei Li)
A guiding philosophy for developing AI that ensures the technology serves humanity.

How it works: Requires integration of interdisciplinary research (medicine, law, humanities), education, ecosystem outreach, and active participation in public policy and regulation.

### Imitation Learning vs High-Compute Reinforcement Learning (Scott Wu)
The paradigm shift from training models to mimic internet text (imitation learning) to training models through task completion and automated feedback (reinforcement learning), which is what makes coding agents possible

How it works: Imitation Learning (2022 era): Read all internet text, train model to talk like someone on the internet. Result: passed Turing test, encyclopedic knowledge. High-Compute RL (2024+): Model does work on tasks, gets evaluated on correctness, learns from feedback. Code is ideal because: running code provides automated feedback → feeds RL loop → models get great at coding. This is the paradigm shift that made autonomous coding agents possible.

### Iterative Deployment (Kevin Weil)
Shipping AI capabilities early and often to co-evolve with society and learn together in public.

How it works: Don't wait for perfect understanding of a model's capabilities or keep breakthroughs secret. Ship early, see how people use it, and iterate based on real-world feedback and societal adaptation.

### Leadership Buy-in Strategy for AI Projects (Summary: AI and product management | Marily Nika (Meta, Google))
Three-part approach to getting leadership to invest in AI initiatives

How it works: 1. Use examples of successful adjacent products: Remind leadership about how a previous project in the same space sounded crazy at the time but worked out well. Leverage internal proof points.
2. Provide contingency and rollback plans: In case the project doesn't work out, present the rollback plan and mention the maximum downside of doing the project.
3. Bridge the research-to-monetization gap: PMs need to figure out ways to monetize research scientists' ideas. Example: there was a willingness-to-pay survey for ChatGPT to try to monetize it — PMs must bridge that gap.

### Mixture of Reasoning Experts (Sander Schulhoff)
An ensembling technique that uses multiple differently-configured 'experts' (different models, roles, or tool access) to solve the same problem, then takes the consensus answer

How it works: Steps: 1. Define a question/problem. 2. Create multiple 'experts' - different LLMs, same LLM with different roles, or LLMs with different tool access (e.g., internet). 3. Send the same question to all experts. 4. Collect responses. 5. Take the most common answer as final response. Example: Real Madrid trophies question - soccer historian expert says 13, internet-connected expert says 13, English professor says 4 → answer is 13. Different roles activate different neural regions, producing varied but often complementary results.

### Model Maximalism (Kevin Weil)
A product philosophy of building for the capabilities of models that are 2 months away, rather than over-indexing on current limitations.

How it works: If your product barely works on the edge of current capabilities, keep going. In two months, the underlying model will improve and the product will sing. Avoid building heavy scaffolding for temporary model flaws.

### North Star Goal-Setting for Technology Exploration (Sam Schillace)
Instead of aimlessly playing with new tech, pick ambitious concrete goals ('north stars') that force real learning and produce useful insights even if the specific goal isn't commercially valuable.

How it works: Step 1: Pick a 'north star' — an ambitious, concrete goal (e.g., 'Can AI agents independently write a Go implementation in Python?'). Step 2: The goal should be something a competent person could do mostly independently — this tests whether the system can too. Step 3: Grind toward the goal for a focused period (e.g., a week). Step 4: Pay attention to insights that emerge along the way (e.g., discovering that a debugger agent is useful, or that shared whiteboard memory makes agents smarter). Step 5: The goal itself may not be valuable, but the system/insights you build are. Contrast with bad approach: 'Let me poke at JavaScript/ChatGPT for a while.'

### Open-Book Test / Notecard Analogy for Prompt Engineering (I built a Lenny chatbot using GPT-3. Here’s how to build your own.)
A mental model for understanding how to improve GPT-3 accuracy by stuffing relevant context into the prompt

How it works: Analogy: GPT-3 is like a student taking an open-book test. The prompt has limited space (~4000 tokens, where each token ≈ ¾ of a word). You write the most relevant information on a 'notecard' (the context portion of the prompt) and include it alongside the user's question. GPT-3's reasoning capabilities then use the provided context to generate accurate answers rather than relying on potentially outdated or missing training data. This addresses two problems: (1) hallucination — GPT-3 confidently generating false information, and (2) missing data — GPT-3's knowledge cutoff and inability to access paywalled content.

### Open-Ended Knowledge Work vs. Repeatable Business Processes (Sherwin Wu V2)
Taxonomy for identifying where AI has the most impact — distinguishing between creative knowledge work (software engineering) and repeatable SOPs (support, operations, utilities)

How it works: Open-ended knowledge work: Software engineering, data science, strategic finance — non-repeatable, creative, exploratory. Tools: Codex, Cursor, coding agents. Repeatable business processes: Support, operations, utilities, compliance — follows SOPs, high determinism needed, don't want deviation. Tools: Business process automation, integrated with business data and systems. Key insight: Silicon Valley overindexes on the first category, but the second category may represent equal or greater opportunity and is massively underrated because tech workers don't experience it.

### OpenAI Prompt Engineering Guide (Logan Kilpatrick)
A resource containing best practices for getting better outputs from LLMs.

How it works: Includes tactics like providing extensive context, telling the model to 'take a break', or adding a smiley face to encourage a 'positive interaction' and better performance.

### Product as Organism (Asha Sharma)
A mental model for modern AI product development where products are living systems that continuously ingest data, digest reward models, and improve outcomes.

How it works: Marks a shift from static artifacts to living organisms. The key metric is the 'metabolism' of the team to process data and tune outcomes. Requires continuous loops of synthetic data generation, reward design, A/B testing, and fine-tuning.

### Query Fan-Out (How AI Search Works) (Robby Stein)
Under-the-hood explanation of how Google AI Mode constructs responses by running dozens of sub-queries against the search index and data backends

How it works: Process: 1) User asks a question. 2) AI model generates dozens of related sub-queries (query fan-out). 3) Each sub-query searches Google's index like a traditional search. 4) Model also requests real-time data from backends (shopping graph: 50B products updated 2B times/hour; Maps: 250M places; finance data). 5) For each search, content is evaluated using Google's human rater guidelines: Does it satisfy user intent? Has sources? Cites information? Is original? 6) Model synthesizes results into a coherent response with links to authoritative sources. Implication for creators: Traditional SEO signals still apply because AI is literally searching.

### Stickiness Over Moats in AI (Scott Wu)
In AI products, defensibility comes from compounding stickiness (accumulated knowledge, team workflows, learning) rather than hard barriers to entry

How it works: Moats = competitors can't enter the market. Stickiness = once using a product, switching cost is high. Sources of stickiness for AI coding agents: 1) Agent learns your codebase over time (like a 5-year engineer vs day-1 hire), 2) Accumulates knowledge from every team member's interactions, 3) Multiplayer workflows: Slack conversations, GitHub PR reviews, Linear tickets all feed agent context, 4) Team knowledge transfer through agent (onboarding, cross-functional context). Compare to hiring a tenured engineer — the value compounds over time.

### Text Completion to Agents Paradigm Shift (Scott Wu)
The product experience is shifting from text-to-text completion (chatbots, autocomplete) to autonomous agents that make decisions, interact with real-world tools, take feedback, and iterate across multiple steps

How it works: Wave 1 (Text Completion): GitHub Copilot, marketing copy, customer support, education. Text in → text out. Wave 2 (Agents): Autonomous systems that make decisions, interact with real-world tools (Slack, GitHub, Linear, browsers), take in feedback, iterate over multiple steps. Key shift: from synchronous single-turn to asynchronous multi-step with human oversight at key decision points.

### The Bitter Lesson (Dr. Fei Fei Li)
A historical observation in AI research regarding model complexity versus data scale.

How it works: The principle that simpler algorithms paired with massive amounts of compute and data will consistently outperform complex, hand-crafted models over time.

### The Bitter Lesson Applied to AI Product Building (Sherwin Wu V2)
Extension of Rich Sutton's Bitter Lesson to building products with AI — scaffolding and workarounds get eaten by model improvements

How it works: Original Bitter Lesson: Less human-engineered logic + more compute = better AI. Applied to building with AI: Less scaffolding + better models = better products. Historical examples: Vector stores (2022-2023) → models learned to search on their own. Agent frameworks → becoming less necessary as models handle orchestration. Current scaffolding at risk: Skills files, AGENTS.md, file-based context management may be eaten by future models. Key quote from Nicolas (Fintool founder): 'The models will eat your scaffolding for breakfast.' OpenAI API team admits they've been guilty of this too — taking left and right turns on scaffolding that models later made unnecessary.

### The Golden Recipe for Modern AI (Dr. Fei Fei Li)
The three foundational pillars required to build modern AI models.

How it works: 1. Big Data (internet-scale datasets). 2. Neural Network Architectures (algorithms to learn patterns). 3. GPUs (massive compute power).

### Three Buckets of Engineering Work (Varun Mohan)
Framework for understanding how AI changes engineering: What should I solve? How should I solve it? Solving it. AI is consuming from the bottom up.

How it works: Bucket 1: 'What should I solve?' (business problems, prioritization, product decisions) — Remains human. Bucket 2: 'How should I solve it?' (architecture, best practices, technical approach) — AI increasingly handles this with deep codebase understanding. Bucket 3: 'Solving it' (writing the actual code) — AI handles vast majority. Engineering evolves toward Bucket 1: identifying business problems and making technical decisions.

### Three Dimensions of Agents (Aparna Chennapragada)
A mental model for defining and evaluating what makes an AI agent effective.

How it works: 1) Autonomy: The ability to delegate higher-order goals, not just fine-motor tasks. 2) Complexity: Handling multi-step tasks (e.g., 'build a prototype') rather than one-shot queries. 3) Natural Interaction/Asynchronous: The ability to work when the user is not working, or jump into a meeting to converse naturally.

### Three Implications of AI Chatbots (I built a Lenny chatbot using GPT-3. Here’s how to build your own.)
Three categories of impact from GPT-3 chatbot technology

How it works: 1. Content creators get a new format: Every newsletter, book, blog, and podcast used as evergreen reference can be repackaged as a chatbot. Benefits for audiences (instant answers vs. searching archives) and creators (new monetization, fewer repetitive questions, more time for creation). A new class of creators will emerge who build compelling chatbot experiences. 2. Organizing your notes is over: No need for fancy filing systems. A chatbot on top of all your notes can act as a personal research assistant, detect patterns in your thinking, and synthesize information. 3. Enterprise knowledge management changes forever: Chatbots as automated librarians for company knowledge, sourcing info from the right person or document, proactively recording tacit knowledge by interviewing key people, eliminating repetitive internal questions.

### Three Types of Technology Plays (Hamilton Helmer)
A mental model for categorizing how companies interact with a new foundational technology like AI.

How it works: 1. The technology play itself (e.g., Intel for chips). 2. Companies that wouldn't exist without the tech (e.g., Microsoft for chips). 3. Tertiary companies that utilize the tech but existed before and will exist after (e.g., auto manufacturers using chips).

### Two Modes of Prompt Engineering (Sander Schulhoff)
Framework distinguishing conversational prompt engineering (iterating in chat) from product-focused prompt engineering (optimizing a single prompt for millions of API calls)

How it works: Mode 1: Conversational - iterating with chatbot in real-time, seeing outputs directly, informal. Mode 2: Product-focused - one or few critical prompts running thousands/millions of inputs per day, requires perfection, uses automated optimization techniques, never changed unless necessary. Most research and highest ROI is on Mode 2.

### Two Problems with Vanilla GPT-3 for Domain-Specific Q&A (I built a Lenny chatbot using GPT-3. Here’s how to build your own.)
Identifies the two core problems that make raw GPT-3 unreliable for answering domain-specific questions

How it works: Problem 1: Hallucination — GPT-3 tends to return nonsensical or false completions confidently, described as being 'like a very smart and overeager 6-year-old' that tries to give good answers even when it doesn't know what it's talking about. Problem 2: Missing/Outdated Data — GPT-3 has a knowledge cutoff (2021 at the time of writing) and cannot access paywalled content. Combined, these mean GPT-3 can give confident but wrong answers. Solution: Feed relevant source content into the prompt as context (RAG pattern).

### Utility of AI Products Equation (Mike Krieger)
A three-part mental model for what makes an AI product actually useful to end users.

How it works: Utility = Model Intelligence (the raw reasoning power) + Context and Memory (getting the right documents/data via tools like MCP) + Applications and UI (discoverable integrations and repeatable workflows).

### Working Backwards for AI Adoption (Inbal S)
A product development approach starting with the customer problem rather than the technology.

How it works: Instead of asking 'What should we do with AI?', identify the specific workflow or manual task causing friction first. Then evaluate if AI can shorten time, make it seamless, or reduce friction.

## Templates

### AI Product Version Scoping Template (Agency Ladder) (Why your AI product needs a different development lifecycle)
A template for breaking down a large AI product vision into versioned capabilities, each defined by its agency level, control mechanisms, and data flywheel.

How it works: For each version, define:
- Version number (v1, v2, v3...)
- Capability description
- Agency level (low / medium / high)
- Control level (high / medium / low)
- What data you'll collect (flywheel)
- Eval metrics for this version
- Control handoff mechanism
- Graduation criteria to next version

Customer Support Example:
| Version | Capability | Agency | Control | Eval Metric | Flywheel Data |
| v1 | Route tickets to correct department | Low | High | Routing accuracy | User phrasing patterns, department confusion data, metadata relevance |
| v2 | Suggest resolutions based on SOPs (human reviews) | Medium | Medium | Retrieval quality | Retrieval breakdowns, document gaps, agent edits |
| v3 | Auto-resolve scoped tickets with human fallback | High | Low | Resolution accuracy, user satisfaction | Safe-to-automate queries, fallback triggers |

Marketing Assistant Example:
| v1 | Draft email/ad/social copy from prompts | Low | High |
| v2 | Build multi-step campaigns and run them | Medium | Medium |
| v3 | Launch, A/B test, and auto-optimize campaigns across channels | High | Low |

Coding Assistant Example:
| v1 | Suggest inline completions and boilerplate snippets | Low | High |
| v2 | Generate larger blocks (tests, refactors) for human review | Medium | Medium |
| v3 | Apply scoped changes and open PRs autonomously | High | Low |

## Checklists

### 4 Main Challenges for AI PMs (Summary: AI and product management | Marily Nika (Meta, Google))
Four key challenges that AI product managers face, with strategies for addressing each

How it works: 1. Dealing with uncertainty: Model training results may not answer your original hypothesis. Be prepared for unexpected outcomes.
2. Leadership support: You might have to pivot, so leading that change can be difficult. Be prepared and communicate proactively.
3. Getting good data is hard: Be willing to do everything — even go to the street and ask people to contribute data. Get creative with data sourcing.
4. Career trajectory is not defined by launches: Unlike traditional PMs who advance by launching products, AI PMs do research work. Clarify with hiring managers early on what progress means and how you will be assessed.

### AI Agent Design Checklist (Make product management fun again with AI agents)
A five-point checklist for planning any AI agent before choosing a platform or building it. Ensures the agent is well-scoped, safe, and effective.

How it works: ☑️ 1. Do I understand this task?
- Can I clearly explain how I'd do this manually with mouse, keyboard, and coffee?
- Do I know where the key information lives?
- Can I provide examples of what success looks like?
- Best practice: Do the task once or twice manually first.

☑️ 2. Could I start even smaller?
- What's the worst/most dreaded part? Start by delegating only that.
- If dream is to monitor 5 competitor websites, launch with 1.
- Cut scope ruthlessly (treat agent like a product launch).

☑️ 3. Can I keep the downside low?
- Instead of pinging a Slack channel → Send me a DM that I can copy-paste
- Instead of sending an email → Create a draft and star the thread for my review
- Instead of making a decision → Make a recommendation
- Instead of modifying a document → Append suggestions at the bottom
- Physically restrict access with permissions.

☑️ 4. Am I giving enough context?
- Where to access the right data
- Guidance for making decisions (e.g., share your prioritization framework)
- How to identify people on your team (e.g., who's on the CS team)
- NOT needed: competitive landscape presentations, 3-year vision, full org chart

☑️ 5. (Danger zone) Am I staying close to raw customer signals?
- Don't let AI summarize everything — you'll degrade your customer intuition
- Insist on exact quotes and direct links to original support tickets, sales call snippets, screen recordings
- Use AI to traverse, roam, navigate, cluster, and clean up data — not to blur your vision
- Alternative: Use AI to reason about root cause to better classify (not summarize)

### AI Agent Launch Recap (5-Step Summary) (Make product management fun again with AI agents)
A high-level summary checklist for the entire AI agent building process, from ideation to scaling.

How it works: 1. Start small: Pick a task you know well, and scope it down.
2. Design for limited downside: Create safety nets for inevitable mistakes.
3. Build with words: Leverage AI to leapfrog the learning curve.
4. Iterate with compassion: Even the smartest colleague needs feedback.
5. Slowly build trust: Gradually increase scope and responsibility.

### AI Glossary - 20+ Key Terms (An AI glossary)
A comprehensive reference list of AI terms with 'explain it like I'm 5' definitions, designed to be kept handy for meetings

How it works: Terms covered:
1. Model - A computer program built to work like a human brain
2. LLM (large language model) - Text-based models for understanding and generating human-readable text
3. Transformer - The 2017 algorithmic architecture that made modern AI possible via 'attention' mechanism
4. Training/Pre-training - Process of learning by analyzing massive data using next-token prediction
5. Supervised learning - Training on labeled data where correct answers are provided
6. Unsupervised learning - Training on data without labels to discover patterns
7. Post-training - Additional steps after training (fine-tuning, RLHF)
8. Fine-tuning - Additional training on specific data for specialized use cases
9. RLHF - Teaching models to behave as humans want using human feedback and reward models
10. Prompt engineering - Crafting questions/instructions for better AI responses (conversational and system/product prompts)
11. RAG (retrieval-augmented generation) - Giving models access to external information at run-time
12. Evals - Structured ways to measure AI system performance (unit tests for AI)
13. Inference - When the model runs and generates a response
14. MCP (model context protocol) - Open standard for AI models to interact with external tools
15. Gen AI (generative AI) - AI systems that create new content
16. GPT (generative pre-trained transformer) - The three key elements: generative + pre-trained + transformer
17. Token - Basic unit of text AI models understand (sometimes a word, often part of a word)
18. Agent - AI system that takes actions on your behalf to accomplish goals
19. Vibe coding - Building apps using AI by describing what you want in plain English
20. AGI (artificial general intelligence) - AI that is generally smart across a wide range of tasks
21. Hallucination - When AI generates confident but factually incorrect responses
22. Synthetic data - Artificially generated data for training (text, images, audio)

### AI Product Building Checklist (Counterintuitive advice for building AI products)
A synthesized checklist of key considerations when building AI features, drawn from the closing thoughts and expert insights

How it works: Mindset:
- [ ] Have you prototyped to understand what's technologically possible before designing the solution?
- [ ] Are you thinking AI-native rather than bolt-on?
- [ ] Are you solving a real user problem, not just building a cool demo?

Wedge Selection:
- [ ] Does your chosen workflow feel like a chore for users?
- [ ] Is the promise-to-payoff ratio high?
- [ ] Will it invite repeat use?
- [ ] Is it something users do frequently (100x/day)?

Design & UX:
- [ ] Have you reduced the intimidation of empty prompt boxes?
- [ ] Do you provide starting points and visual guidance?
- [ ] Is there a post-generation editing flow?
- [ ] Have you considered branding the feature as 'AI-powered'?
- [ ] Is the AI output instantaneous (pre-computed if possible)?

Testing & Validation:
- [ ] Are you testing longitudinally (past the novelty phase)?
- [ ] Are you segmenting AI embracers vs. AI skeptics?
- [ ] Are you using high-touch methods (Slack groups, not just surveys)?
- [ ] Have you defined your 'good enough' acceptance rate?

Technical Architecture:
- [ ] Is your product designed to improve automatically as base models improve?
- [ ] Have you avoided excessive scaffolding logic?
- [ ] Have you planned for scalability from the outset?
- [ ] Are you investing in prompt engineering as a primary quality lever?
- [ ] Do you have proprietary/licensed data that differentiates you?

Metrics:
- [ ] Have you accounted for time-in-app potentially going down?
- [ ] Are you measuring 'Is this making your job easier?' not just engagement?
- [ ] Are you tracking acceptance/adoption rates for AI outputs?

### AI Product Building Principles (Boris Cherny)
Rules of thumb for developing applications powered by LLMs.

How it works: 1) Don't box the model in with strict workflows; give it tools and a goal. 2) The Bitter Lesson: always bet on the more general model over specific fine-tuning or scaffolding. 3) Build for the model that will exist 6 months from now, even if current product-market fit feels weak.

### AI Product Rigor Checklist — 4 Questions (25 proven tactics to accelerate AI adoption at your company)
Four questions every PM should clearly answer when presenting an AI product to avoid the trap of flashy demos without substance

How it works: When you share your AI product, you should clearly answer four questions:
1. What customer problem are you solving?
2. Can AI solve it better than non-AI solutions?
3. What ground-truth dataset and evaluations do you have?
4. How have you prepared for the model to fail?

### Further Study Resources for AI/GPT-3 (I built a Lenny chatbot using GPT-3. Here’s how to build your own.)
Curated list of 7 resources for going deeper on neural networks, transformers, and GPT

How it works: 1. 'But what is a neural network?' (YouTube video by 3Blue1Brown). 2. 'Neural networks and deep learning' (online book at neuralnetworksanddeeplearning.com). 3. 'Transformers, explained' (YouTube video). 4. 'Let's build GPT: from scratch, in code, spelled out' (YouTube video by Andrej Karpathy). 5. 'The end of organizing' (Every.to article by Dan Shipper). 6. 'GPT-3 is the best journal I've ever used' (Every.to article by Dan Shipper). 7. '6 new theories about AI' (Every.to Napkin Math article). Additionally recommended: Andrej Karpathy's YouTube channel for technical understanding of how GPT works.

### Prompt Engineering Technique Selection Guide (Five proven prompt engineering techniques (and a few more-advanced tactics))
A guide for choosing which prompt engineering technique to use based on your situation

How it works: Choose your technique based on the problem:

1. Role-playing — Use when: You need domain-specific expertise or a particular perspective. Problem it solves: Generic, unfocused responses.

2. Style unbundling — Use when: You admire a specific style but want to understand and selectively apply its elements. Problem it solves: Can't pinpoint what makes communication effective.

3. Emotion prompting — Use when: You need AI to produce especially careful, high-quality output. Problem it solves: AI produces adequate but not exceptional work. Caveat: Use judiciously.

4. Few-shot learning — Use when: You need output that matches a specific format or style from examples. Problem it solves: AI doesn't know your team's conventions.

5. Synthetic bootstrap — Use when: You lack real-world examples or need diverse test cases quickly. Problem it solves: Insufficient data for user research or testing.

6. Chain-of-thought — Use when: The task requires reasoning, problem-solving, or multi-step processes. Problem it solves: AI jumps to conclusions without considering all factors.

7. RAG — Use when: You need responses grounded in specific, current, or specialized information. Problem it solves: AI's training data is outdated or doesn't cover your niche.

8. LLM-as-a-judge — Use when: You have multiple outputs and need to evaluate quality objectively. Problem it solves: Human feedback is too expensive or slow for iteration.

### Prompt Structure Components (Sander Schulhoff)
The key structural elements that should be present in a well-formed prompt, distinct from prompting techniques

How it works: Components: 1. Role (optional, only useful for expressive/style tasks, NOT accuracy tasks). 2. Additional information/context (place at beginning for caching; dump as much as possible in conversational mode; be selective in product mode for cost/latency). 3. Examples (few-shot; use common formats like Q:/A: or XML). 4. Directive (core intent - what you actually want done). 5. Output formatting (table, bullet list, structured output specification).

### RAG Data Preparation Techniques (Chip Huyen)
A list of tactical data processing steps to improve Retrieval-Augmented Generation performance.

How it works: 1) Optimize chunk size (balance between containing enough context vs. being too broad). 2) Add contextual metadata and summaries to chunks. 3) Generate hypothetical questions that each chunk can answer. 4) Rewrite raw data (like podcast transcripts) into explicit Question/Answer formats. 5) Annotate documentation specifically for AI reading (explaining human 'common sense' context).

## Examples

### AI Mode Origin Story: Startup-Style Development at Google (Robby Stein)
How Google built AI Mode in roughly one year using a small team, trusted testers, and progressive validation

How it works: Timeline: Started ~summer of previous year. Stage 1: 5-10 person team built a rough prototype — 'moments of brilliance' (e.g., planning a family outing and getting Maps, park info, walkability all in one response). Stage 2: 500 external trusted testers including friends and family who gave brutally honest feedback via screenshots and DMs. Stage 3: Launched in Labs for broader testing with real query data. Stage 4: Full public launch in US, then expanding to all countries/languages. Key insight: The trigger was seeing users append 'AI' to their Google queries, trying to force AI responses — a clear signal of unmet need.

### AI Model Landscape by Type (An AI glossary)
Categorized examples of real AI models organized by their type and specialization

How it works: Language models (LLMs): ChatGPT o3, Claude Sonnet 4, Gemini 2.5 Pro, Meta Llama 4, Grok 3, DeepSeek, Mistral
Video models: Google Veo 3, OpenAI Sora, Runway Gen-4
Voice/audio models: ElevenLabs, Cartesia, Suno
Traditional AI models: Classification (fraud detection), Ranking (search, social feeds, ads), Regression (numerical predictions)
Vibe coding tools: Cursor, Windsurf, Bolt, Lovable, v0, Replit

### AlphaGo Move 37 — AI Seeing What Humans Cannot (How AI will impact product management)
The story of AlphaGo's move 37 against Lee Sedol, used as an analogy for how AI will find strategic insights no human PM has ever seen.

How it works: In the match between AlphaGo and Lee Sedol (one of the world's top Go players), the 37th move in Game Two was a move that flummoxed even the world's best Go players. 'That's a very strange move,' said one commentator. 'I thought it was a mistake,' said the other. The move turned the course of the game. AlphaGo won, and Lee Sedol was speechless. This illustrates that AI can see patterns in data that no human has ever seen in 4,000+ years — the same will apply to product strategy.

### AutoML Renewable Energy Use Case (Summary: AI and product management | Marily Nika (Meta, Google))
Real-world example of a company using Google's AutoML no-code tool for significant operational improvement

How it works: A renewable-energy company used Google Cloud's AutoML to reduce their turbine maintenance procedure from three weeks to a few hours. AutoML allows training of custom machine learning models with minimal effort and no coding required.

### Chime's Internal GPTs (Logan Kilpatrick)
Custom GPTs built internally at Chime to automate marketing and data analysis.

How it works: One GPT generates Facebook/Google ad ideas; another acts as a data scientist to deliver experiment results and answer follow-up questions about product implications.

### Customer Support AI — Full CC/CD Walkthrough (Why your AI product needs a different development lifecycle)
A complete worked example showing how a customer support AI product would progress through v1 (routing), v2 (suggestion), and v3 (auto-resolution) using the CC/CD framework.

How it works: v1 — Ticket Routing (High Control, Low Agency):
- Capability: Route tickets to correct department
- Eval: Routing accuracy
- Control handoff: Receiving agent can reroute; correction is logged
- Flywheel: Learn user phrasing patterns, department confusion points, metadata relevance
- What can go wrong if skipped: Misrouted tickets compound downstream — wrong SOPs retrieved, wrong resolutions generated

v2 — Response Suggestions (Medium Control, Medium Agency):
- Capability: Retrieve SOPs and past resolutions, suggest draft responses for human review
- Eval: Retrieval quality (are suggestions relevant?)
- Control handoff: Human agent reviews and edits before sending
- Flywheel: Discover where retrieval breaks down, which documents need updates, how agents edit suggestions

v3 — Auto-Resolution (Low Control, High Agency):
- Capability: Resolve scoped tickets autonomously with human fallback
- Eval: Resolution accuracy, user satisfaction
- Control handoff: Escalation to human for out-of-scope or low-confidence cases
- Flywheel: Identify safe-to-automate queries, refine fallback triggers

Key lesson: If you shipped v3 directly, a misrouted refund request could be tagged as billing, pull the wrong SOP, generate a plausible but incorrect resolution, and erode user trust — and you'd be stuck untangling a chain of failures with no visibility into the root cause.

### Customer Support Agent Progression (Aishwarya Naresh Reganti + Kiriti Badam)
A three-step progression for safely deploying a customer support AI agent.

How it works: V1: Routing tickets to the right department (high control, human can undo). V2: Copilot drafting responses based on SOPs for human agents to edit. V3: End-to-end resolution assistant interacting directly with customers.

### Dragon for Physicians Fine-Tuning (Asha Sharma)
A real-world example of how high-quality data annotation dramatically improves AI product performance.

How it works: Microsoft's Dragon AI product for physicians improved its character acceptance rate from 30-60% (using synthetic fine-tuning) to 83% by feeding the model 600,000 expert-annotated patient-physician interactions.

### Duolingo AI-Powered Course Creation (25 proven tactics to accelerate AI adoption at your company)
How Duolingo rebuilt their course content creation process with AI, massively accelerating output

How it works: Duolingo went from 100 courses in 12 years to 150 courses in just 12 months with AI's help. CPO Cem Kansu: 'We vibe coded the first Duolingo Chess lesson in hours instead of weeks.' AI adoption was defined as both 'making our products better' and 'empowering employees to do their best work.' They also run FriAIdays (2-hour blocks every Friday for AI experimentation) and 'AI Show and Tell' at all-hands meetings. Every employee received $300 to try AI tools, courses, and subscriptions.

### Ensemble Model Architecture for AI Products (Michael Truell)
A hybrid approach to using AI models to balance cost, speed, and reasoning quality.

How it works: 1. Custom fast models for high-frequency, low-latency tasks (e.g., autocomplete predicting diffs in <300ms). 2. Custom routing models to search the codebase and select context. 3. Large foundation models (GPT/Sonnet) for high-level reasoning and sketching changes. 4. Smaller specialty models to fill in the exact code diffs based on the foundation model's sketch.

### GitHub Copilot / Cursor Agency Ladder (Why your AI product needs a different development lifecycle)
Real-world example of how coding assistants followed the agency-ladder approach, progressing from inline completions to autonomous PRs.

How it works: Progression observed in tools like GitHub Copilot and Cursor:
- v1: Suggest inline completions and boilerplate snippets (low agency)
- v2: Generate larger blocks like tests or refactors for human review (medium agency)
- v3: Apply scoped changes and open pull requests autonomously (high agency)

Most users only see the current version, but the underlying system climbed the agency ladder gradually — first completions, then blocks, then PRs — with each step earned through usage, feedback, and iteration.

### Healthcare AI Diagnostic Assistant (Jason Droege)
A real-world example of enterprise AI implementation requiring expert-in-the-loop labeling.

How it works: An AI agent reads 200-300 pages of patient documentation to surface the top 5-10 critical factors (e.g., hidden allergies) for doctors handling rare cases. It requires internal doctors to label data and create evals to teach the model what 'good' looks like for their specific hospital's standards.

### ImageNet (Dr. Fei Fei Li)
A massive dataset curated to train computer vision models, proving that big data was the missing ingredient for AI.

How it works: Curated 15 million images from the internet, mapped to a taxonomy of 22,000 concepts using WordNet, and open-sourced to the research community via an annual challenge.

### Incident.io AI-Generated Summaries (75% adoption) (Counterintuitive advice for building AI products)
Example of identifying a high-frequency mundane task and achieving 75% AI adoption by automating incident summaries

How it works: Approach: Instead of asking 'what cool new things could AI do,' they asked 'what's the thing our users do 100 times a day that AI could make better.'
Feature: AI-generated incident summaries
Result: 75% of incident summaries are now AI-generated. Users vastly prefer automatically generated summaries to writing these themselves.
Key lesson: Look for high-frequency tasks users already do repeatedly, not novel AI capabilities.

### Jensen Huang's 'Everyone Is a Programmer' Quote (How AI will impact product management)
Jensen Huang's statement that AI will make programming unnecessary and that the programming language will be human language.

How it works: Jensen Huang, CEO of Nvidia: 'Everybody who sits on a stage like this would tell you it is vital that your children learn computer science. That everybody should learn how to program. In fact, it's almost exactly the opposite. It is our job to create computing technology such that nobody has to program. That the programming language is human. Everybody in the world is now a programmer. This is the miracle of artificial intelligence.'

### Lyft's Pricing Algorithm Rebuild (Adriel Frederick)
A case study on why operational control must be a first-order requirement in ML products.

How it works: Lyft built a complex pricing algorithm with PhDs that lacked operational flexibility. When they needed to make manual price changes for specific city events (like a snowstorm), the system couldn't handle it. They had to completely rebuild it to put 'humans in the loop' to set constraints and strategy.

### Marketing Assistant Progression (Aishwarya Naresh Reganti + Kiriti Badam)
A three-step progression for safely deploying an AI marketing assistant.

How it works: V1: Draft emails or social copy. V2: Build and run a multi-step campaign. V3: Launch, A/B test, and auto-optimize campaigns across channels.

### Medical Coding Prompt Engineering (Sander Schulhoff)
Real-world case study of using few-shot prompting with reasoning chains to boost GPT-4 accuracy on medical coding by 70%

How it works: Task: Get GPT-4 to perform medical coding on doctor transcripts. Starting point: Little to no accuracy, improper formatting, poor reasoning. Solution: Collected coded documents, attached reasoning for why each was coded that way, included all examples in the prompt, then gave model a new unseen transcript. Result: 70% accuracy improvement. Technique used: Few-shot prompting with chain-of-thought reasoning in the examples.

### Site Outage RL Environment (Edwin Chen)
A conceptual example of a reinforcement learning environment used to train AI agents on complex, multi-step tasks.

How it works: Setup: A simulated startup with Gmail, Slack, Jira, GitHub, and a codebase. Event: AWS and Slack go down. Task: Figure out why the site went down and fix it. Reward mechanism: Passing unit tests or writing an accurate post-mortem retro.

### Wind Turbine Maintenance with Auto ML (Marily Nika)
A real-world case study of applying no-code AI to a physical operational problem.

How it works: Instead of humans climbing ladders to inspect wind turbines (taking 3 weeks), a company flew drones to take photos, uploaded the images to Auto ML, and identified which turbines needed maintenance in just a few hours.

### Zapier Sales AI Automation — Lead Research (25 proven tactics to accelerate AI adoption at your company)
Zapier's AI workflow that auto-packages marketing engagement data for account reps when targeted leads engage with content

How it works: When targeted leads engage with marketing content, AI auto-packages that information for the account rep. Result: 10 hours saved per week per rep on lead research. Zapier also built a workflow that checks Zendesk tickets and identifies customers ready for sales conversations, turning customer support into a revenue driver. Template available at: https://zapier.com/templates/details/target-account-engagement-alert-rep-outreach-kit

### monday.com AI Agent — Second Brain Case Study (How to build your PM second brain with ChatGPT)
Real example of how Amir Klein used the second brain approach to build monday.com's first AI agent product

How it works: Context: Amir's first month at monday.com, tasked with building their first AI agent (an AI co-pilot for users to get insights, explanations, and build complex workflows).

Problem: Overwhelming amount of context spread across Slack channels, Notion pages, Monday boards, decks, Google Docs. Hundreds of tiny fragments impossible to piece together mentally.

What he fed into the Project:
- Decks from colleagues
- PDFs of monday.com documentation pages explaining product functionality
- CSV files containing Reddit threads (thousands of conversations about monday.com, AI, and competitors)
- Over time: hundreds of threads' worth of artifacts

Key insight surfaced by the second brain: Users weren't blocked by capability but by confidence. They needed scaffolding, not features.

Outcome: This insight unlocked the product direction they eventually shipped—described as a huge success. The Project grew to contain dozens of files after hundreds of threads.

Additional uses: Created waitlist sign-up forms, generated Lovable prototypes (one closely resembling what they eventually shipped), and produced tailored communications for multiple stakeholders.

## Tools

### Anthropic Prompt Improver (Mike Krieger)
A tool in the Anthropic console that takes a problem description and examples, and agentically creates and iterates on an optimized prompt.

How it works: It automatically inserts XML tags to separate what the AI should be thinking versus what it should be saying, which humans rarely do optimally from scratch.

### Curated AI Learning Resources (An AI glossary)
Collection of recommended videos, articles, and tools for understanding AI concepts in depth

How it works: How LLMs work: every.to primer (https://every.to/p/how-ai-works), Andrej Karpathy deep dive (YouTube)
Transformers: FT interactive explanation (https://ig.ft.com/generative-ai/), 3Blue1Brown visual deep dive (YouTube)
Tokenizer tool: https://tiktokenizer.vercel.app/
Training visual explanation: YouTube video
Ilya Sutskever on next-token prediction: YouTube video
RLHF guide: labellerr.com blog post
Fine-tuning vs RAG vs Prompt Engineering: YouTube overview
MCP explanation: YouTube video
Anthropic guide to building effective agents: https://www.anthropic.com/engineering/building-effective-agents
Anthropic guide to reducing hallucinations: https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
Aman Khan's eval guide: Lenny's Newsletter guest post (https://www.lennysnewsletter.com/p/beyond-vibe-checks-a-pms-complete)
Synthetic data deep dive: YouTube video
Prompt engineering podcast episode: YouTube video

