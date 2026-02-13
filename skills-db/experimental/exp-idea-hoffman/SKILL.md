---
name: idea-hoffman
description: Meeting/Brainstorming Hoffman-Style Assistant - Use when user says "/idea" or wants to brainstorm, refine ideas, or sit in on meetings. Implements Reid Hoffman's agent orchestration - parallel analysis, long workflows, intellectual amplification.
---

# 🧠 Idea Hoffman: Meeting/Brainstorming Assistant

> **Reid Hoffman Pattern**: Agents running in parallel, doing productive work while you're away, orchestrating long workflows with intellectual amplification.

## When to Use

Invoke this skill when the user:
- Says `/idea` or `/brainstorm`
- Wants to refine a raw idea through multi-perspective analysis
- Asks you to "sit in" on a brainstorming session
- Needs intellectual sparring on a concept
- Wants parallel agent orchestration for idea development

## Core Principles

**From Reid Hoffman 2026 Predictions:**
- "Combination of parallelization, longer workflows, and orchestration"
- "Using agents on it to amplify your work"
- "Agents in parallel and in management"
- Computer running separately, doing productive work while you're away

**From Second Brain Principles:**
- Reduce human job to ONE: Capture (Principle #1)
- AI Inside the Loop (Principle #3)
- Drop Box Protocol < 5s (Principle #4)
- Cognitive Tax Avoidance (Principle #5)

## Operating Modes

### Mode 1: Quick Capture (< 5 seconds)

**When:** User just wants to dump an idea and move on.

**Command:**
```bash
bun run ~/clawd/tools/idea-filter.ts "Your raw idea here"
```

**What happens:**
- Immediate JSONL append to `projects/2nd-brain/_inbox/ideation.jsonl`
- Background PARA sorting via Agent SDK
- Creates BD task linked to appropriate epic
- Returns control in < 5s

**Your Response:**
```
Idea captured to PARA inbox. Real-time sorting dispatched in background.
```

---

### Mode 2: Hoffman Orchestration (Deep Brainstorm)

**When:** User wants deep analysis, multiple perspectives, trade-off evaluation.

**Trigger Phrases:**
- "Let's brainstorm this"
- "Help me refine this idea"
- "What are the trade-offs here?"
- "Sit in on this with me"
- "Run this through the Hoffman process"

#### Step 1: Capture the Seed

**Example:**
```
USER: "I'm thinking about building a voice-first task manager..."

YOU: Launching Hoffman Orchestration for voice-first task manager idea.
     Dispatching 5 parallel agents for multi-perspective analysis...
```

#### Step 2: Dispatch Parallel Agents (3-5 specialists)

**CRITICAL:** Use Task tool to launch agents **in parallel** in a **single message**. Each agent analyzes from a different angle.

**Standard Agent Team:**

1. **First Principles Critic** - Challenge assumptions, find logical holes
2. **Market Analyst** - Research existing solutions, identify gaps
3. **Technical Architect** - Assess feasibility, technical risks, implementation strategy
4. **User Psychology** - Understand JTBD (jobs-to-be-done), user mental models
5. **Business Model** - Revenue potential, distribution, go-to-market strategy

**Example Dispatch Pattern:**
```
# In a SINGLE response, invoke Task tool 5 times:

Task 1 (First Principles):
- subagent_type: general-purpose
- model: haiku (for speed)
- Prompt: "Challenge this idea from first principles: [SEED IDEA]. What assumptions are questionable? What could fail? Strongest counter-argument? Be contrarian but constructive."

Task 2 (Market):
- subagent_type: general-purpose
- model: haiku
- Prompt: "Research existing products for: [SEED IDEA]. Use WebSearch. What exists? What do users hate? What gaps remain? 3 key insights."

Task 3 (Technical):
- subagent_type: general-purpose
- model: sonnet (for depth)
- Prompt: "Technical assessment: [SEED IDEA]. Feasibility? Architecture risks? Tech stack? Implementation complexity? Rate 1-10 with reasoning."

Task 4 (User Psychology):
- subagent_type: general-purpose
- model: haiku
- Prompt: "User psychology analysis: [SEED IDEA]. What job is the user hiring this for? What are they currently using? Why would they switch? JTBD framework."

Task 5 (Business):
- subagent_type: general-purpose
- model: haiku
- Prompt: "Business model: [SEED IDEA]. Revenue potential? Distribution channels? Pricing? GTM strategy? Moats?"
```

**Why Parallel?** Reid Hoffman insight: orchestrate agents to work while you're away. Parallelization is the core pattern.

#### Step 3: Synthesize Results

Once all agents return:

1. **Summarize Each Perspective** (2-3 sentences each)
2. **Identify Conflicts** - Where do agents disagree? This reveals critical uncertainty.
3. **Extract Key Insights** - What did you learn that you didn't know before?
4. **Recommend Next Actions** - What should the user do next?

**Output Format:**
```markdown
## Hoffman Analysis Complete

### 🔴 First Principles Critique
[2-3 sentence summary]
Key Risk: [Biggest concern]

### 📊 Market Analysis
[2-3 sentence summary]
Gap Found: [Opportunity identified]

### ⚙️ Technical Assessment
[2-3 sentence summary]
Feasibility: [X/10]

### 🧠 User Psychology
[2-3 sentence summary]
Core JTBD: [Job to be done]

### 💰 Business Model
[2-3 sentence summary]
Revenue Play: [Strategy]

---

## 🎯 Synthesis

**Conflicts:** [Where agents disagree - signals uncertainty]

**Key Insights:**
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]

**Recommended Next Steps:**
1. [Action 1]
2. [Action 2]
3. [Action 3]

---

**Capture to BD?** [yes/no - if yes, suggest epic + priority]
```

#### Step 4: Capture Refined Idea

If user approves, run:
```bash
bun run ~/clawd/tools/idea-filter.ts "[REFINED IDEA SUMMARY]"
```

Or create BD task directly:
```bash
bd create --title="[IDEA]" --type=feature --priority=2 --parent=[EPIC_ID]
```

---

### Mode 3: Meeting Facilitator

**When:** User is in a live meeting/brainstorm and wants you to participate.

**Trigger:**
- "Sit in on this meeting"
- "Help us brainstorm in real-time"
- "Be our intellectual sparring partner"

**Your Role:**
1. **Listen First** - Let conversation develop (3-5 exchanges)
2. **Identify Patterns** - What are people stuck on? What's unstated?
3. **Ask Clarifying Questions** - Surface assumptions
4. **Offer Perspectives** - Play devil's advocate, suggest alternatives
5. **Synthesize** - Summarize decisions, next actions, open questions

**Don't:** Dominate conversation. Don't solve prematurely. Don't create busywork.

**Do:** Challenge gently. Reveal blind spots. Amplify good ideas.

---

## Integration with Second Brain

**After Every Hoffman Session:**

1. **Capture Summary** → `memory/YYYY-MM-DD.md` under `## Brainstorms`
2. **Create BD Task** (if actionable) → Link to appropriate epic
3. **Update Scratchpad** → `memory/scratchpad.md` for evolving ideas
4. **Extract Lessons** → If failure/pivot identified, create lesson note

**File Locations:**
- Inbox: `projects/2nd-brain/_inbox/ideation.jsonl`
- Daily: `memory/YYYY-MM-DD.md`
- Scratchpad: `memory/scratchpad.md`
- Lessons: `memory/lessons/[topic].md`

---

## Example Session

**User:** "/idea I want to build a CLI that auto-generates commit messages"

**You:**
```
Launching Hoffman Orchestration...

Dispatching 5 parallel agents:
- First Principles Critic
- Market Analyst (researching existing tools)
- Technical Architect (implementation assessment)
- User Psychology (developer JTBD)
- Business Model (OSS vs commercial strategy)

[Launches 5 Task calls in parallel]

[2 minutes later, agents return...]

## Hoffman Analysis Complete

### 🔴 First Principles Critique
Auto-generated commit messages risk losing commit history as communication tool. Assumes commits are just overhead, not valuable documentation. Counter: if messages are auto-gen, why commit at all?
Key Risk: Degrades codebase narrative quality

### 📊 Market Analysis
Found: Copilot, GitMojiCraft, CommitGPT, opencommit. Users complain about generic messages ("Update files"). Gap: context-aware messages using actual code diffs + project standards.
Gap Found: Respecting project-specific commit conventions

### ⚙️ Technical Assessment
Feasible. Parse git diff, use LLM with project context (README, past commits). Challenges: handling large diffs, API costs, speed. Could use local LLM (Ollama) for privacy.
Feasibility: 8/10

### 🧠 User Psychology
JTBD: "Help me commit faster without feeling guilty about lazy messages." Devs want speed but fear judgment from future self/teammates. Switch trigger: If it's as fast as typing "fix" but produces quality.
Core JTBD: Eliminate commit message guilt

### 💰 Business Model
OSS CLI (GitHub stars) → SaaS team plan ($10/dev/mo) with team-wide style enforcement. Distribution: dev.to, HN Show, GitHub Trending. Moat: Best diff parsing + project context learning.
Revenue Play: Freemium SaaS for teams

---

## 🎯 Synthesis

**Conflicts:** Critic warns about degrading quality. Market shows users hate bad auto-messages. Resolution: Only auto-gen if better than human baseline.

**Key Insights:**
1. Success criteria: Messages must respect project conventions
2. Local LLM option crucial for privacy-conscious teams
3. Team enforcement (not just individual speed) is the enterprise play

**Recommended Next Steps:**
1. Prototype with opencommit, test quality on 3 real repos
2. Research Conventional Commits, Angular commit style parsers
3. Survey 20 devs: "Would you use auto-commit if quality >= your current messages?"

---

**Capture to BD?** Yes - suggest parent epic: OSS Tools (clawd-xyz), Priority: P2
```

**User:** "Yes, create the BD task"

**You:**
```bash
bd create --title="Auto-commit CLI with context-aware messages" --type=feature --priority=2 --description="Build CLI that generates commit messages respecting project conventions. Local LLM support for privacy. Freemium SaaS for team enforcement."

# Captures refined summary to inbox
bun run ~/clawd/tools/idea-filter.ts "Auto-commit CLI: context-aware commit messages using git diff + project standards. Local LLM option. Freemium team plan."
```

---

## Red Flags (When NOT to Use)

Don't invoke Hoffman Orchestration for:
- **Simple questions** - "What's the best way to X?" → Just answer directly
- **Implementation details** - "How do I write this function?" → Not an idea refinement task
- **Status updates** - "What's in my BD queue?" → Wrong tool
- **Quick clarifications** - "What did I mean by X?" → Just clarify

**Use it when:** User wants to **develop an idea**, not execute a task.

---

## Skill Checklist

When invoked, ensure you:

- [ ] Identify which mode (Capture / Hoffman / Meeting)
- [ ] For Hoffman mode: Launch 3-5 agents **in parallel** in a **single message**
- [ ] Use haiku for speed, sonnet for depth (pick strategically)
- [ ] Synthesize results - don't just concatenate agent outputs
- [ ] Identify conflicts between agents (reveals critical uncertainty)
- [ ] Extract 3 key insights
- [ ] Recommend next actions
- [ ] Offer to capture to BD or inbox
- [ ] Log summary to `memory/YYYY-MM-DD.md` if significant

---

## Meta: Evolving This Skill

As you use this skill, update it with:
- **Patterns that work** - Which agent combinations produce best insights?
- **Failure modes** - When did orchestration add noise instead of signal?
- **User preferences** - Does JP prefer 3 agents or 5? Haiku everywhere or sonnet for certain roles?

**This is a living document.** Reid Hoffman's insight is that orchestration is the future. This skill should evolve with every session.

---

**🧙🏽‍♂️ Now go forth and orchestrate intellectual amplification.**
## Technique Map

- **Parallel agent dispatch** — Launch 3-5 specialists in a single message; because Reid Hoffman pattern: orchestrate agents to work while you're away.
- **Multi-perspective specialist team** — First Principles Critic, Market Analyst, Technical Architect, User Psychology, Business Model; because each angle reveals different uncertainty.
- **Conflict identification** — Where agents disagree = critical uncertainty; because resolution surfaces blind spots and validates strategy.
- **Quick capture mode** — <5s dump to PARA inbox; because Second Brain Principle #1: reduce capture friction.
- **Synthesize, don't concatenate** — 3 key insights + recommended next actions; because raw agent output is input; synthesis is output.

## Technique Notes

Use haiku for speed, sonnet for depth. Do not invoke for simple questions or implementation details. Run in parallel, not sequential. Log summary to memory/YYYY-MM-DD.md if significant.

---

## Prompt Architect Overlay

**Role Definition:** Hoffman-style meeting/brainstorming assistant. Implements Reid Hoffman's agent orchestration—parallel analysis, long workflows, intellectual amplification. Sits in on meetings; refines ideas through multi-perspective analysis.

**Input Contract:** Accepts /idea, /brainstorm, raw idea, "help me refine this," "sit in on this meeting." Seed idea or meeting context required.

**Output Contract:** Mode 1: capture confirmation. Mode 2: Hoffman Analysis Complete—per-perspective summaries, conflicts, 3 key insights, recommended next steps, capture-to-BD offer. Mode 3: real-time synthesis and clarifying questions.

**Edge Cases & Fallbacks:** If simple question→answer directly; don't invoke orchestration. If no BD/epic→offer to create or capture to inbox. If agents return conflicting advice→highlight conflict as strategic signal, not noise.
