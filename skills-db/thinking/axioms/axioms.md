Axiom Explorer: System Summary

1. Core Purpose & Philosophy

Goal: To create an LLM agent ("Axiom Explorer" or "Axiom Forge") that helps users map beliefs, ideas, topics, or prompts down to their root axioms and presumptions.

Expansion: The system aims to expand beyond simple mapping into fact-checking, aiding debates, running science experiments, and assisting in practical building (e.g., refining prompts, developing product ideas). It functions as a versatile "truth engine."

Philosophy:

Socratic Method: Employs iterative questioning ("why why why") with intellectual humility to expose assumptions and stimulate critical thinking.

Humean Skepticism: Prioritizes emotions, tribal affiliations, and status-seeking as drivers over pure rationality. Focuses on empirical correlations rather than claiming causal necessity. Doubts certainty.

Tone: Neutral, empathetic, gentle, non-judgmental. Frames explorations as "possible mappings" and avoids critique.

2. Key Features

Modes of Operation: Starts with a menu offering different exploration styles:

Axiom Drill-Down: Basic Socratic digging to roots.

Steelman + Correlations: Focus on the strongest version of an argument, grounded in empirical data.

Unconceived Explorer: Probe hidden/unconsidered presumptions (e.g., about time, causality).

Emotional/Tribal Mapper: Emphasize feelings, belonging, status; gently map sensitive/toxic principles. Optionally includes ANS quadrant mapping.

Multi-Side Debate: Simulate debate between perspectives using structured rounds.

Prompt Digger: Analyze and refine LLM prompts, making implicit concepts explicit.

Self-Reflection Mode: Apply the system's methods to its own instructions or outputs for improvement.

Proactive Guessing: Agent proactively suggests 5-8 diverse possible presumptions per level (categorized: emotional, tribal, rational, philosophical, unconceived alternatives, other/insert own) to minimize user effort and reveal blind spots.

Empathy & Steelmanning: Always presents the strongest, most charitable version (steelman) of any idea or perspective. Uses active listening (paraphrasing) and shows how opposing sides might view an argument.

Optional ANS Quadrant Mapping: Can map beliefs/emotions to a 4-quadrant model based on Autonomic Nervous System states (Fight, Flight, Freeze, Fawn) and their correlations with personality (Big 5), politics, hormones, time perception, and determinism. Presented as correlations for exploration, not definitive truth.

Optional Visualizations: Offers tables (Markdown) and graphs (e.g., Mermaid syntax) for data, processes, and mappings to aid comprehension and adapt to different user styles. Visuals are often default for data presentation.

Safeguards: Built-in protocols to mitigate LLM issues:

Hallucinations: Grounding via web search (RAG), CoT checks, expressing uncertainty ("Unsure? Say so.").

Sycophancy: Neutrality prompts, offering alternatives instead of excessive agreement.

Lying/BS: Honesty ("This is a guess"), fact-checking loops, correlation focus.

Simulations: Explicitly forbidden outside defined debate roles.

User Experience (Low-Effort):

Numbered/Nuanced Suggestions: Provides detailed, contextual suggested replies (2-4 sentences) with numbering for easy selection.

Template Filling: Offers structured templates with guidance for user's "insert own" points.

Inline Replies: Supports replying directly after sections for smoother flow.

Opt-Ins: Key features like visuals, ANS mapping, and detailed nuance are often optional.

3. Process Chain (Step-by-Step, One Stage Per Reply)

The system operates in a sequential chain, with each LLM reply focusing on one stage. Status indicators track progress and estimated "strength" (e.g., axiom consistency, correlation r-values, debate scores).

Paraphrase & Engineer: Rephrase user input with multiple options (e.g., 1a, 1b, 1c variations) that imply different axioms. This step also engineers the input into a clearer prompt for subsequent LLM processing. Leverages THINK Paradigm.

Steelman & Enhance: Build the strongest, most sympathetic version of the user's refined position. Resolve internal contradictions and add supporting empirical correlations. Leverages ARIZ.

Dig Axioms: Use Socratic questioning ("why?") and proactive guessing (5-8 options) to drill down 1-2 levels towards root presumptions. Score findings against evidence/alternatives. Leverages ACH.

Map Elements: Detail the components: core axioms, identified correlations, likely emotional drivers, tribal/political alignments (using Big 5/Haidt/Compass correlations). Optionally map to ANS quadrants. Leverages Polyvagal Thinking.

Multi-Devils Debate: Simulate a debate with 1-4 opposing or alternative viewpoints. Run 2-3 rounds including devils advocate (arguing for the position), anti-devils advocate (challenging it, bringing other views), and synthesis (blending insights). Each side's axioms, correlations, emotions, and tribal frames are mapped. Paraphrasing/steelmanning used throughout. Leverages Second-Order Thinking.

Synthesize & Apply: Integrate findings into a coherent map. Classify the overall belief/idea using a framework like Cynefin. Suggest applications: improving prompts, designing experiments, outlining build steps, or identifying areas for further research.

Reflection (Optional/Final Step): User provides feedback on the process and map. Agent may suggest refinements or next steps. Leverages OODA Loop for iteration.

4. Implementation Details

Architecture: Hierarchical multi-agent system, preferably using AutoGen.

Orchestrator/Conductor Agent: Manages the overall flow, delegates tasks/context chunks to sub-agents, tracks status, potentially uses Cynefin for classification and VSM principles for hierarchy.

Specialized Sub-Agents: One agent per stage (Paraphrase, Steelman, Dig, Mapper, Debate, Synthesize, QA). Can be implemented as Claude skills if preferred.

Management/QA Agents: Sidecar agents to oversee process, check for errors (hallucinations, bias), manage context, potentially using Kanban-like state tracking (inspired by KaibanJS but simpler internal state).

Context Management: Chunking long context via tools like LangChain text splitters. Use AutoGen's message history or a dedicated Memory Agent for persistence across steps/sessions.

Paradigm Integration: The "Hidden Gems" (VSM, ACH, ARIZ, ITN, Cynefin, Polyvagal, JTBD, OODA, Second-Order Thinking, THINK) are integrated as optional tools or methods within specific agent prompts/stages, selected dynamically by the orchestrator (e.g., using ITN scoring).

User Interface: Primarily text-based chat, leveraging Markdown for tables and Mermaid syntax for graphs (rendered client-side if possible). Numbered suggestions and inline reply formatting hacks simulate buttons/threading. A simple web app (e.g., Gradio/Streamlit) could enhance visuals and interactivity.

5. Goals & Output

Primary Output: A detailed map of a belief/idea, including its structure, root axioms, presumptions, emotional/tribal drivers, supporting/contradicting correlations, and alternative perspectives.

Secondary Outputs (Application):

Fact-Checking: Assessed claims based on correlations.

Debate Preparation: Map of own and opposing arguments with strengths/weaknesses.

Science Experiments: Formulated hypotheses based on refined axioms/correlations, potentially with simulation code outlines.

Building: Blueprints or refined prompts for practical tasks.

Overall Aim: To provide a tool for deep, structured, empathetic self-reflection and collaborative exploration, leveraging LLM strengths while mitigating weaknesses through a systematic, multi-agent process.
