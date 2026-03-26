# Complete Swarm Prompt Reference

## Table of Contents
- [Initial Marching Orders](#initial-marching-orders)
- [Work Loop Prompts](#work-loop-prompts)
- [Quality Review Prompts](#quality-review-prompts)
- [Commit & Test Prompts](#commit--test-prompts)

---

## Initial Marching Orders

### THE EXACT PROMPT — Session Start

```
First read ALL of the AGENTS dot md file and README dot md file super carefully and understand ALL of both! Then use your code investigation agent mode to fully understand the code, and technical architecture and purpose of the project. Then register with MCP Agent Mail and introduce yourself to the other agents.

Be sure to check your agent mail and to promptly respond if needed to any messages; then proceed meticulously with your next assigned beads, working on the tasks systematically and meticulously and tracking your progress via beads and agent mail messages.

Don't get stuck in "communication purgatory" where nothing is getting done; be proactive about starting tasks that need to be done, but inform your fellow agents via messages when you do so and mark beads appropriately.

When you're not sure what to do next, use the bv tool mentioned in AGENTS dot md to prioritize the best beads to work on next; pick the next one that you can usefully work on and get started. Make sure to acknowledge all communication requests from other agents and that you are aware of all active agents and their names.  Use ultrathink.
```

**Delivery:**
```bash
ntm send myproject --all "$(cat marching_orders.txt)"
```

---

## Work Loop Prompts

### THE EXACT PROMPT — Move to Next Bead

```
Reread AGENTS dot md so it's still fresh in your mind.   Use ultrathink.   Use bv with the robot flags (see AGENTS dot md for info on this) to find the most impactful bead(s) to work on next and then start on it. Remember to mark the beads appropriately and communicate with your fellow agents. Pick the next bead you can actually do usefully now and start coding on it immediately; communicate what you're working on to your fellow agents and mark beads appropriately as you work. And respond to any agent mail messages you've received.
```

### THE EXACT PROMPT — Post-Compaction Recovery

```
Reread AGENTS dot md so it's still fresh in your mind.   Use ultrathink.
```

**When to use:** Immediately after an agent performs context compaction.

---

## Quality Review Prompts

### THE EXACT PROMPT — Self-Review

```
Great, now I want you to carefully read over all of the new code you just wrote and other existing code you just modified with "fresh eyes" looking super carefully for any obvious bugs, errors, problems, issues, confusion, etc. Carefully fix anything you uncover. Use ultrathink.
```

**When to use:** After completing each bead, before moving on.

**Keep running until:** No more bugs are found.

### THE EXACT PROMPT — Cross-Review

```
Ok can you now turn your attention to reviewing the code written by your fellow agents and checking for any issues, bugs, errors, problems, inefficiencies, security problems, reliability issues, etc. and carefully diagnose their underlying root causes using first-principle analysis and then fix or revise them if necessary? Don't restrict yourself to the latest commits, cast a wider net and go super deep! Use ultrathink.
```

**When to use:** Periodically during implementation, especially after major milestones.

### THE EXACT PROMPT — Random Exploration

```
I want you to sort of randomly explore the code files in this project, choosing code files to deeply investigate and understand and trace their functionality and execution flows through the related code files which they import or which they are imported by.

Once you understand the purpose of the code in the larger context of the workflows, I want you to do a super careful, methodical, and critical check with "fresh eyes" to find any obvious bugs, problems, errors, issues, silly mistakes, etc. and then systematically and meticulously and intelligently correct them.

Be sure to comply with ALL rules in AGENTS dot md and ensure that any code you write or revise conforms to the best practice guides referenced in the AGENTS dot md file. Use ultrathink.
```

**When to use:** For deep quality checks, especially near project completion.

---

## Commit & Test Prompts

### THE EXACT PROMPT — Commit Changes

```
Now, based on your knowledge of the project, commit all changed files now in a series of logically connected groupings with super detailed commit messages for each and then push. Take your time to do it right. Don't edit the code at all. Don't commit obviously ephemeral files. Use ultrathink.
```

### THE EXACT PROMPT — Add Test Coverage

```
Do we have full unit test coverage without using mocks/fake stuff? What about complete e2e integration test scripts with great, detailed logging? If not, then create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid with detailed comments.
```

---

## Quality Loop Pattern

Run these three prompts in order, repeating until all return clean:

```
┌─────────────────┐
│  Self-Review    │◄──────┐
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│  Cross-Review   │       │
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│ Random Explore  │───────┘
└─────────────────┘   (if changes made)
         │
         ▼ (no changes)
┌─────────────────┐
│   Code Solid    │
└─────────────────┘
```

---

## Prompt Delivery Methods

### To Single Agent Type

```bash
ntm send myproject --cc "Prompt here"    # Claude Code only
ntm send myproject --cod "Prompt here"   # Codex only
ntm send myproject --gmi "Prompt here"   # Gemini only
```

### To All Agents

```bash
ntm send myproject --all "Prompt here"
```

### To Specific Agent

```bash
ntm send myproject --pane cc-1 "Prompt here"
```

### From File

```bash
ntm send myproject --all "$(cat prompt.txt)"
```
