---
name: multi-agent-swarm-workflow
description: >-
  Run multi-agent coding swarms using NTM, Agent Mail, Beads, and BV. Use when
  spawning agent swarms, coordinating parallel implementation, sending marching
  orders, or running quality review loops.
---

<!-- TOC: Quick Start | THE EXACT PROMPT | Swarm Loop | Quality Loops | BV Commands | Agent Lifecycle | Model Mix | FAQ | References -->

# Multi-Agent Swarm Workflow

> **Core Insight:** Every agent is fungible and a generalist. They all read the same AGENTS.md. Telling one it's a "frontend agent" doesn't make it better at frontend. The swarm self-organizes through Agent Mail and Beads.

## Quick Start

```bash
# 1. Ensure prerequisites
am                          # Start Agent Mail server
br ready                    # Verify beads exist

# 2. Spawn swarm
ntm spawn myproject --cc=3 --cod=2 --gmi=1

# 3. Send marching orders to all
ntm send myproject --all "$(cat marching_orders.txt)"

# 4. Monitor
ntm dashboard myproject
```

---

## THE EXACT PROMPT — Initial Marching Orders

Send this to every agent at session start:

```
First read ALL of the AGENTS dot md file and README dot md file super carefully and understand ALL of both! Then use your code investigation agent mode to fully understand the code, and technical architecture and purpose of the project. Then register with MCP Agent Mail and introduce yourself to the other agents.

Be sure to check your agent mail and to promptly respond if needed to any messages; then proceed meticulously with your next assigned beads, working on the tasks systematically and meticulously and tracking your progress via beads and agent mail messages.

Don't get stuck in "communication purgatory" where nothing is getting done; be proactive about starting tasks that need to be done, but inform your fellow agents via messages when you do so and mark beads appropriately.

When you're not sure what to do next, use the bv tool mentioned in AGENTS dot md to prioritize the best beads to work on next; pick the next one that you can usefully work on and get started. Make sure to acknowledge all communication requests from other agents and that you are aware of all active agents and their names.  Use ultrathink.
```

### Why This Works

| Element | Purpose |
|---------|---------|
| Read AGENTS.md + README | Establishes full project context |
| Agent Mail registration | Enables coordination |
| Check mail, respond | Prevents isolation |
| Avoid communication purgatory | Keep work moving |
| Use bv for prioritization | Decentralized task selection |
| Use ultrathink | Maximum reasoning depth |

---

## The Swarm Loop

```
1. Agent reads AGENTS.md, README
2. Registers with Agent Mail
3. Runs: bv --robot-next
4. Claims bead, reserves files
5. Works on bead
6. Self-reviews
7. Releases files, closes bead
8. Checks mail, responds
9. Goto 3
```

### THE EXACT PROMPT — Move to Next Bead

```
Reread AGENTS dot md so it's still fresh in your mind.   Use ultrathink.   Use bv with the robot flags (see AGENTS dot md for info on this) to find the most impactful bead(s) to work on next and then start on it. Remember to mark the beads appropriately and communicate with your fellow agents. Pick the next bead you can actually do usefully now and start coding on it immediately; communicate what you're working on to your fellow agents and mark beads appropriately as you work. And respond to any agent mail messages you've received.
```

### THE EXACT PROMPT — Post-Compaction

When an agent compacts, immediately restore context:

```
Reread AGENTS dot md so it's still fresh in your mind.   Use ultrathink.
```

---

## Quality Loops

Run these iteratively until they return clean (no changes made):

### THE EXACT PROMPT — Self-Review

```
Great, now I want you to carefully read over all of the new code you just wrote and other existing code you just modified with "fresh eyes" looking super carefully for any obvious bugs, errors, problems, issues, confusion, etc. Carefully fix anything you uncover. Use ultrathink.
```

### THE EXACT PROMPT — Cross-Review

```
Ok can you now turn your attention to reviewing the code written by your fellow agents and checking for any issues, bugs, errors, problems, inefficiencies, security problems, reliability issues, etc. and carefully diagnose their underlying root causes using first-principle analysis and then fix or revise them if necessary? Don't restrict yourself to the latest commits, cast a wider net and go super deep! Use ultrathink.
```

### THE EXACT PROMPT — Random Exploration

```
I want you to sort of randomly explore the code files in this project, choosing code files to deeply investigate and understand and trace their functionality and execution flows through the related code files which they import or which they are imported by.

Once you understand the purpose of the code in the larger context of the workflows, I want you to do a super careful, methodical, and critical check with "fresh eyes" to find any obvious bugs, problems, errors, issues, silly mistakes, etc. and then systematically and meticulously and intelligently correct them.

Be sure to comply with ALL rules in AGENTS dot md and ensure that any code you write or revise conforms to the best practice guides referenced in the AGENTS dot md file. Use ultrathink.
```

### The Steady-State Signal

When all three review types return clean (no bugs found, no changes made), the code is solid.

---

## BV Commands

**CRITICAL:** Never run bare `bv` — it launches interactive TUI that blocks the session.

```bash
# THE MEGA-COMMAND: Start here
bv --robot-triage

# Get single top pick
bv --robot-next

# Get parallel execution tracks
bv --robot-plan

# Check for cycles (MUST FIX if found)
bv --robot-insights | jq '.Cycles'

# Find bottlenecks
bv --robot-insights | jq '.bottlenecks'
```

---

## File Reservations

Before editing, reserve files:

```python
file_reservation_paths(
    project_key="/path/to/project",
    agent_name="GreenCastle",
    paths=["src/auth/**/*.ts"],
    ttl_seconds=3600,
    exclusive=True,
    reason="bd-123"
)
```

After completing, release:

```python
release_file_reservations(project_key, agent_name)
```

---

## Committing Work

### THE EXACT PROMPT — Commit Changes

```
Now, based on your knowledge of the project, commit all changed files now in a series of logically connected groupings with super detailed commit messages for each and then push. Take your time to do it right. Don't edit the code at all. Don't commit obviously ephemeral files. Use ultrathink.
```

---

## Agent Lifecycle

### Starting a Swarm

```bash
# 1. Prerequisites
am                          # Start Agent Mail
br ready                    # Verify beads exist

# 2. Spawn
ntm spawn myproject --cc=3 --cod=2 --gmi=1

# 3. Initialize (send to ALL agents)
ntm send myproject --all "$(cat marching_orders.txt)"
```

### Adding Agents Mid-Session

```bash
ntm add myproject --cc=2    # Add 2 more Claude agents
ntm send myproject:5 "$(cat marching_orders.txt)"  # Initialize just pane 5
```

### Replacing Dead Agents

```bash
# Check what was in progress
br list --status in_progress

# Add replacement
ntm add myproject --cc=1

# Initialize (it will pick up stuck beads)
ntm send myproject --cc "$(cat marching_orders.txt)"
```

### Graceful Shutdown

```bash
# Let agents finish current beads
ntm send myproject --all "Complete current bead, commit, then stop"

# Wait for commits
ntm activity myproject --watch

# Kill session
ntm kill myproject
```

---

## Model Mix Guide

| Mix | Best For |
|-----|----------|
| `--cc=3 --cod=2 --gmi=1` | General development (recommended start) |
| `--cc=5` | Complex architecture, deep reasoning |
| `--cc=2 --cod=3` | High-volume straightforward coding |
| `--cc=2 --cod=2 --gmi=2` | Cross-validation, diverse perspectives |

**Tips:**
- Start small (3-6 agents), scale up as coordination stabilizes
- Different models catch different bugs in cross-review
- Codex excels at boilerplate; Claude at architecture; Gemini at documentation

---

## FAQ

**Q: How do agents know what to work on?**
A: `bv --robot-triage` or `bv --robot-next` finds the highest-impact ready bead.

**Q: How do they avoid conflicts?**
A: File reservations in Agent Mail. Pre-commit guard enforces exclusivity.

**Q: What if an agent crashes?**
A: Start a new session, read AGENTS.md, check bead status, continue. Every agent is fungible.

**Q: How many agents?**
A: Start with 3-6. More agents = faster but more coordination overhead.

**Q: What model mix?**
A: Try 3 Claude (Opus), 2 Codex (GPT 5.2), 1 Gemini. They have different strengths.

---

## References

| Topic | Reference |
|-------|-----------|
| All prompts | [PROMPTS.md](references/PROMPTS.md) |
| Architecture diagram | [ARCHITECTURE.md](references/ARCHITECTURE.md) |
| UI/UX quality prompts | [UI-UX-PROMPTS.md](references/UI-UX-PROMPTS.md) |
| NTM commands | See `ntm` skill |
| Agent Mail | See `using-agent-mail` skill |
| BV prioritization | See `bv-graph-triage` skill |

---

## Validation

```bash
# Swarm is working when:
ntm dashboard myproject   # Shows active agents
br list --status in_progress   # Shows beads being worked
ntm mail inbox myproject  # Shows coordination messages
```
