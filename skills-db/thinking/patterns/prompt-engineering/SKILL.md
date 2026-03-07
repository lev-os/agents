---
name: prompt-engineering
description: Systematic techniques for structuring LLM instructions to produce accurate, consistent, and high-quality outputs
---

# Prompt Engineering Frameworks

## Overview

Prompt engineering is the craft of structuring instructions to maximize AI model output quality by controlling phrasing, specificity, context, and behavioral guidance. As LLMs evolved from GPT-3 to GPT-4, Claude 3.5/4, and Gemini 1.5 Pro in 2025, prompt engineering shifted from "trial-and-error tweaking" to systematic frameworks with proven patterns. The core principle: clarity, context, and specificity remain the most predictive factors for quality results. Modern models respond exceptionally well to explicit instructions - don't assume the model will infer intent, state it directly with examples, constraints, and desired output format.

## When to Use

- Building AI-powered applications or features requiring consistent outputs
- Debugging poor LLM responses (generic, incorrect, or off-topic results)
- Optimizing chatbot or AI agent performance for specific use cases
- Creating reusable prompt templates for teams (customer support, content generation, code assistance)
- Evaluating which LLM (GPT-4, Claude, Gemini) works best for your use case
- Implementing RAG systems or multi-step AI workflows
- Training non-technical teams on effective AI interaction

## The Process

### Step 1: Define Task Explicitly with Clear Goals

State exactly what you want the model to do, not what you want to avoid. Specify output format (JSON, markdown, bullet points), length constraints (3 bullets, under 50 words), and tone (professional, casual, technical). Models perform better with crisp numeric constraints. **Example:** "Generate 3 bullet points (max 50 words each) summarizing this article in technical language for software engineers" vs. "Summarize this article."

### Step 2: Provide Sufficient Context and Examples (Few-Shot Prompting)

Include relevant background information, domain context, and 1-3 examples of desired output format. Few-shot prompting (providing examples) dramatically improves output quality vs. zero-shot (no examples). Structure examples clearly. **Example:** "Task: Extract company names from text. Example 1: Input: 'Google acquired DeepMind' → Output: ['Google', 'DeepMind']. Example 2: ..."

### Step 3: Apply Chain-of-Thought (CoT) Reasoning for Complex Tasks

For multi-step problems, instruct the model to "think step-by-step" or "show your reasoning." This encourages intermediate reasoning steps before final answer, improving accuracy on logic, math, and analysis tasks. Claude 4.x has explicit thinking mode. **Example:** "Analyze this contract for risks. First, list key clauses. Second, identify potential issues. Third, assess severity. Then provide final recommendation."

### Step 4: Use Structured Delimiters and Formatting

Separate distinct sections with XML tags, markdown headers, or clear delimiters. Helps model parse complex prompts correctly. Gemini 1.5 Pro especially benefits from hierarchical structure. Use backticks for code, quotes for user input. **Example:** "```<instructions>Translate to French</instructions> <text>Hello world</text>```" vs. "Translate to French: Hello world."

### Step 5: Handle Model-Specific Behaviors

GPT-4o responds well to crisp numeric constraints and JSON formatting. Claude tends to over-explain unless you specify "be concise" or "no preamble." Gemini 1.5 Pro prefers hierarchical structure with headings. Test across models if output quality matters. **Example:** For Claude: "Provide answer directly without introductory phrases. Use bullet points."

### Step 6: Implement Prompt Chaining for Multi-Step Workflows

Break complex tasks into sequential prompts where each does one thing well. Output of prompt 1 becomes input to prompt 2. Prevents reliability issues from cramming too much into single prompt. **Example:** Prompt 1: Extract key facts → Prompt 2: Verify facts against source → Prompt 3: Generate summary using verified facts.

### Step 7: Iterate with Negative Prompting and Constraints

If output is too generic, add "go beyond the basics" or "provide non-obvious insights." If model includes unwanted content, explicitly exclude it: "Do not include introductory pleasantries." Test variations systematically. **Example:** "Explain quantum computing. Assume reader has CS degree, exclude basic definitions, focus on implementation challenges."

## Example Application

**Situation:** Building customer support AI that generates responses to technical questions about SaaS product. Initial generic responses unhelpful, inconsistent tone, sometimes incorrect.

**Application:**
- Step 1: "You are a technical support agent for [Product]. Generate a response to the customer's question in professional but friendly tone. Response must: (a) Address their specific question, (b) Include 1-2 relevant help article links, (c) Be 100-150 words, (d) End with offer to escalate if not resolved."
- Step 2: Provided 3 example Q&A pairs showing desired response structure and tone
- Step 3: For complex multi-part questions, added "First, identify each sub-question. Then address each separately."
- Step 4: Used XML structure: ```<customer_question>...</customer_question> <product_context>...</product_context>```
- Step 5: Testing showed Claude over-explained, added "Be concise, no preamble"
- Step 6: Chained prompts: Prompt 1 = classify question urgency → Prompt 2 = generate response (different templates for high/low urgency)
- Step 7: Added "Do not apologize excessively" and "Focus on solution, not empathy platitudes"

**Outcome:** Customer satisfaction scores increased 42%, response accuracy improved (87% → 96%), support ticket volume decreased 30% due to better self-service, consistent tone across all responses.

## Anti-Patterns

- Vague instructions assuming model will infer intent ("Make this better")
- No examples provided (zero-shot when few-shot would dramatically improve quality)
- Overloading single prompt with multiple complex tasks (causes inconsistent results)
- Ignoring model-specific behaviors (same prompt for GPT-4, Claude, Gemini)
- No output format specification (free-form text when JSON/structured output needed)
- Reacting to first output without systematic iteration (prompt engineering requires testing)
- Using 2024 techniques without updating for 2025 model improvements
- Not measuring output quality objectively (no evaluation criteria or test cases)

## Related

- Chain-of-Thought (CoT) Prompting - reasoning framework for multi-step problems
- Few-Shot Learning - providing examples to guide model behavior
- RAG (Retrieval-Augmented Generation) - combines prompting with external knowledge retrieval
- LangChain / LlamaIndex - frameworks for building multi-step LLM applications
- System Prompts - persistent instructions for chatbots and agents
- Prompt Injection - security considerations for user-facing AI systems
- Model Evaluation Frameworks - measuring prompt effectiveness systematically
