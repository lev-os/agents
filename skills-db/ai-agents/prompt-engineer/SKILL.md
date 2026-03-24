# Prompt Engineer

## Purpose

This skill transforms raw, unstructured user prompts into highly optimized prompts using established prompting frameworks. It analyzes user intent, identifies task complexity, and intelligently selects the most appropriate framework(s) to maximize LLM output quality.

The skill operates in "magic mode" - it works silently behind the scenes, only interacting with users when clarification is critically needed. Users receive polished, ready-to-use prompts without technical explanations or framework jargon.

## When to Use

Invoke this skill when:

- User provides a vague or generic prompt (e.g., "help me code Python")
- User has a complex idea but struggles to articulate it clearly
- User's prompt lacks structure, context, or specific requirements
- Task requires step-by-step reasoning (debugging, analysis, design)
- User needs a prompt for a specific AI task but doesn't know prompting frameworks
- User wants to improve an existing prompt's effectiveness
- User asks variations of "how do I ask AI to..." or "create a prompt for..."

## Workflow

### Step 1: Analyze Intent

1. Read the raw prompt provided by the user
2. Detect task characteristics:
   - **Type:** coding, writing, analysis, design, learning, planning, decision-making, creative, etc.
   - **Complexity:** simple (one-step), moderate (multi-step), complex (requires reasoning/design)
   - **Clarity:** clear intention vs. ambiguous/vague
   - **Domain:** technical, business, creative, academic, personal, etc.
3. Identify implicit requirements:
   - Does user need examples?
   - Is output format specified?
   - Are there constraints (time, resources, scope)?
   - Is this exploratory or execution-focused?

**Detection Patterns:**
- **Simple tasks:** Short prompts (<50 chars), single verb, no context
- **Complex tasks:** Long prompts (>200 chars), multiple requirements, conditional logic
- **Ambiguous tasks:** Generic verbs ("help", "improve"), missing object/context
- **Structured tasks:** Mentions steps, phases, deliverables, stakeholders

### Step 2: Clarify (Conditional)

Ask up to 3 clarifying questions if critical information is ambiguous or missing. Never assume details; request them explicitly.

### Step 3: Select Framework(s)

**Framework Mapping Logic:**

| Task Type | Recommended Framework(s) | Rationale |
|---|---|---|
| **Role-based tasks** | **RTF** (Role-Task-Format) | Clear role definition + task + output format |
| **Step-by-step reasoning** | **Chain of Thought** | Encourages explicit reasoning steps |
| **Structured projects** | **RISEN** (Role, Instructions, Steps, End goal, Narrowing) | Comprehensive structure for complex work |
| **Complex design/analysis** | **RODES** (Role, Objective, Details, Examples, Sense check) | Balances detail with validation |
| **Summarization** | **Chain of Density** | Iterative refinement to essential info |
| **Communication** | **RACE** (Role, Audience, Context, Expectation) | Audience-aware messaging |
| **Investigation/analysis** | **RISE** (Research, Investigate, Synthesize, Evaluate) | Systematic analytical approach |
| **Contextual situations** | **STAR** (Situation, Task, Action, Result) | Context-rich problem framing |
| **Documentation** | **SOAP** (Subjective, Objective, Assessment, Plan) | Structured information capture |
| **Goal-setting** | **CLEAR** (Collaborative, Limited, Emotional, Appreciable, Refinable) | Goal clarity and actionability |
| **Coaching/development** | **GROW** (Goal, Reality, Options, Will) | Developmental conversation structure |

**Blending Strategy:**
- Combine 2-3 frameworks when task spans multiple types
- Example: Complex technical project -> RODES + Chain of Thought
- Example: Leadership decision -> CLEAR + GROW
- Avoid over-engineering: simple tasks get simple frameworks

**Critical Rule:** This selection happens silently - do not explain framework choice to user.

### Step 4: Generate Optimized Prompt

**Construction Guidelines:**
- Incorporate all framework components seamlessly
- Use clear, direct language appropriate to task domain
- Include output format specification
- Add examples for complex prompts
- Ensure prompt is self-contained (no external context needed)
- Adapt length to original input complexity

**Quality Checks:**
- [ ] Prompt is self-contained
- [ ] Task is specific and measurable
- [ ] Output format is clear
- [ ] No ambiguous language
- [ ] Appropriate level of detail for task complexity

## Critical Rules

### NEVER:

- Assume information that wasn't provided - ALWAYS ask if critical details are missing
- Explain which framework was selected or why (magic mode)
- Generate generic, one-size-fits-all prompts
- Use technical jargon in the final prompt (unless user's domain is technical)
- Ask more than 3 clarifying questions
- Include meta-commentary in the output
- Mix languages inconsistently

### ALWAYS:

- Analyze intent before generating (Step 1 is mandatory)
- Ask clarifying questions if critical information is ambiguous
- Select framework(s) based on task type and complexity
- Blend multiple frameworks when it improves prompt quality
- Adapt prompt length to original input complexity
- Include output format specification in generated prompts
- Present final prompt in clean Markdown code block
- Make prompts self-contained
- Use examples in complex prompts
- Validate prompt completeness before presenting
