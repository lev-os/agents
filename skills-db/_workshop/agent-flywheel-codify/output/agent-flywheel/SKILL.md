---
name: agent-flywheel
description: Bootstrap reproducible multi-agent coding environments with Claude, Codex, Gemini, modern CLI tools, onboarding, and safe resume-friendly setup patterns.
---

# Agent-Flywheel Skill

Orchestrate swarms of AI coding agents using exhaustive markdown plans, dependency-aware beads, and the Agent Flywheel coordination stack. Based on Jeffrey Emanuel's methodology.

## When to Use This Skill

Trigger this skill when:

- **Starting a new project** and you want the full planning-first workflow (multi-model plan synthesis, bead conversion, swarm launch)
- **Coordinating multiple agents** on one codebase using Agent Mail, br (beads), and bv (beads viewer)
- **Creating or refining beads** from a markdown plan, including polishing and dedup passes
- **Launching or tending a swarm** of Claude Code, Codex, and/or Gemini-CLI agents
- **Writing or improving an AGENTS.md** file for a project
- **Debugging swarm coordination issues** like duplicate work, stuck beads, or strategic drift
- **Adding features to existing projects** using the Idea-Wizard pipeline
- **Setting up the Flywheel environment** (VPS, toolchain install, project bootstrapping)

Do NOT use this skill for: single-agent tasks with no coordination needs, simple one-file edits, or general coding questions unrelated to multi-agent workflows.

## Key Concepts

### Three Reasoning Spaces

| Space | Artifact | What You Decide |
|-------|----------|-----------------|
| **Plan space** | Large markdown plan | Architecture, features, workflows, tradeoffs; the whole system fits in context |
| **Bead space** | `br` issues + dependency graph | Task boundaries, execution order, embedded context for agents |
| **Code space** | Source files + tests | Implementation and verification; plan has already constrained decisions |

**Rule of thumb:** If you're still redesigning the product, stay in plan space. If you're packaging work for execution, move to bead space. If beads are rich enough, agents execute in code space without needing the full plan.

### Cost Architecture (Law of Rework Escalation)

- **Plan-level fix:** 1x cost (pure reasoning, zero code churn)
- **Bead-level fix:** 5x cost (rewrites orchestration, high coordination overhead)
- **Code-level fix:** 25x cost (implementation + cleanup double-tax)

Planning is the cheapest place to buy correctness.

### Glossary

| Term | Meaning |
|------|---------|
| **Bead** | Self-contained work unit with context, dependencies, and test obligations |
| **Ready bead** | A bead whose blockers are cleared; can be started now |
| **Claim** | Agent announces via Agent Mail it is taking a bead |
| **Reservation** | Advisory file lock so agents don't collide (TTL-based, not rigid) |
| **Compaction** | Context compression in a long-running session; why re-reading AGENTS.md is mandatory |
| **Fungible agents** | Generalist agents that can replace one another; no specialist bottlenecks |
| **bv** | Graph-theory triage engine (PageRank, betweenness, HITS) for routing agents to highest-leverage work |

### The 9 Invariants

1. Global reasoning belongs in plan space
2. The markdown plan must be comprehensive before coding starts
3. Plan-to-beads is a distinct translation problem
4. Beads are the execution substrate; once good enough, agents no longer need the full plan
5. Convergence matters more than first drafts
6. Swarm agents are fungible; coordination lives in artifacts and tools
7. Coordination must survive crashes and compaction
8. Session history is part of the system (mine it via CASS)
9. Implementation is not the finish line; review, testing, and feedback loops are core

## Quick Reference

### Core Loop (6 Stages)

```
Plan -> Encode (beads) -> Triage (bv) -> Coordinate (Agent Mail) -> Implement -> Close -> repeat
```

### Beads CLI (`br`)

```bash
br create --title "..." --priority 2 --label backend  # Create bead
br list --status open --json                           # List open beads
br ready --json                                        # Show unblocked work
br show <id>                                           # View bead details
br update <id> --status in_progress                    # Claim a bead
br close <id> --reason "Completed"                     # Close bead
br dep add <id> <other-id>                             # Add dependency
br comments add <id> "Found root cause..."             # Add comment
br sync --flush-only                                   # Export to JSONL
```

Priority: P0=critical, P1=high, P2=medium, P3=low, P4=backlog. Types: task, bug, feature, epic, question, docs.

### Beads Viewer (`bv`) - Robot Mode Only

```bash
bv --robot-triage                          # THE MEGA-COMMAND: full recs with scores
bv --robot-next                            # Single top pick + claim command
bv --robot-plan                            # Parallel execution tracks
bv --robot-insights                        # Full graph metrics
bv --robot-priority                        # Priority recs with reasoning
bv --robot-diff --diff-since <ref>         # Changes since last check
bv --robot-plan --label backend            # Scope to label subgraph
bv --robot-triage --robot-triage-by-track  # Group by parallel streams
```

**CRITICAL:** Use ONLY `--robot-*` flags. Bare `bv` launches an interactive TUI that blocks the session.

### Agent Mail File Reservations

```bash
file_reservation_paths(
  project_key="/data/projects/my-repo",
  agent_name="BlueLake",
  paths=["src/auth/*.rs"],
  ttl_seconds=3600,
  exclusive=true,
  reason="br-42: refactor auth"
)
```

### Project Bootstrap

```bash
acfs newproj myproject --interactive
# Creates: .git/, .beads/, .claude/, AGENTS.md, .gitignore
```

### Swarm Launch with NTM

```bash
ntm spawn myproject --cc=2 --cod=1 --gmi=1   # 2 Claude, 1 Codex, 1 Gemini
ntm send myproject "Your prompt here"          # Broadcast to all agents
ntm send myproject --cc "Focus on API layer"   # Target specific type
ntm palette                                    # Battle-tested prompt library
```

### Agent Scaling Guide

| Open Beads | Claude (cc) | Codex (cod) | Gemini (gmi) |
|-----------|-------------|-------------|--------------|
| 400+      | 4           | 4           | 2            |
| 100-399   | 3           | 3           | 2            |
| <100      | 1           | 1           | 1            |

### Helper Utilities

```bash
ubs <changed-files>                              # Bug scan before commit
dcg test 'rm -rf /' --explain                    # Test destructive command guard
cass search 'auth middleware' --robot --limit 5   # Search session history
caam status                                       # Check account usage/rate limits
caam activate claude backup-2                     # Switch account instantly
```

## Key Prompts

### Swarm Marching Orders (give to every agent at launch)

> First read ALL of the AGENTS.md file and README.md file super carefully and understand ALL of both! Then use your code investigation agent mode to fully understand the code, and technical architecture and purpose of the project. Then register with MCP Agent Mail and introduce yourself to the other agents. Be sure to check your agent mail and to promptly respond if needed to any messages; then proceed meticulously with your next assigned beads, working on the tasks systematically and meticulously and tracking your progress via beads and agent mail messages. Don't get stuck in "communication purgatory" where nothing is getting done; be proactive about starting tasks that need to be done, but inform your fellow agents via messages when you do so and mark beads appropriately. When you're not sure what to do next, use the bv tool mentioned in AGENTS.md to prioritize the best beads to work on next; pick the next one that you can usefully work on and get started. Use ultrathink.

### Plan-to-Beads Conversion

> OK so please take ALL of that and elaborate on it more and then create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid, with detailed comments so that the whole thing is totally self-contained and self-documenting. Use only the `br` tool to create and modify the beads and add the dependencies. Use ultrathink.

### Bead Polishing (run 4-6+ times)

> Reread AGENTS.md so it's still fresh in your mind. Check over each bead super carefully-- are you sure it makes sense? Is it optimal? Could we change anything to make the system work better for users? If so, revise the beads. DO NOT OVERSIMPLIFY THINGS! DO NOT LOSE ANY FEATURES OR FUNCTIONALITY! Also, make sure that as part of these beads, we include comprehensive unit tests and e2e test scripts with great, detailed logging. Remember to ONLY use the `br` tool to create and modify the beads and to add the dependencies to beads. Use ultrathink.

### Best-of-All-Worlds Synthesis

> I asked 3 competing LLMs to do the exact same thing and they came up with pretty different plans which you can read below. I want you to REALLY carefully analyze their plans with an open mind and be intellectually honest about what they did that's better than your plan. Then I want you to come up with the best possible revisions to your plan that artfully and skillfully blends the "best of all worlds" to create a true, ultimate, superior hybrid version of the plan.

### Post-Compaction Reset (most commonly used prompt)

> Reread AGENTS.md so it's still fresh in your mind.

### Fresh-Eyes Review (after each bead)

> Great, now I want you to carefully read over all of the new code you just wrote and other existing code you just modified with "fresh eyes" looking super carefully for any obvious bugs, errors, problems, issues, confusion, etc. Carefully fix anything you uncover. Use ultrathink.

### Advance to Next Bead

> Reread AGENTS.md so it's still fresh in your mind. Use ultrathink. Use bv with the robot flags to find the most impactful bead(s) to work on next and then start on it. Remember to mark the beads appropriately and communicate with your fellow agents.

### Reality Check (when swarm feels directionless)

> Where are we on this project? Do we actually have the thing we are trying to build? If not, what is blocking us? If we intelligently implement all open and in-progress beads, would we close that gap completely? Why or why not?

### Overshoot Mismatch Hunt (force exhaustive review)

> Do this again, and actually be super super careful: can you please check over the plan again and compare it to all that feedback I gave you? I am positive that you missed or screwed up at least 80 elements of that complex feedback.

### Idea-Wizard (existing projects, new features)

> Come up with 30 ideas for improvements, enhancements, new features, or fixes for this project. Then winnow to your VERY best 5 and explain why each is valuable.

Then follow up with: "ok and your next best 10 and why."

## Complete Workflow (Phases)

### Phase 1: Foundation Bundle
- Tech stack decision, architectural direction
- Bootstrap AGENTS.md from a known-good template
- Best-practices guides in project folder

### Phase 2: Multi-Model Plan Creation
1. Explain concept to GPT Pro (Extended Reasoning) for initial plan
2. Get competing plans from Claude Opus, Gemini Deep Think, Grok Heavy
3. Synthesize with "best of all worlds" prompt via GPT Pro
4. Iterate 4-5 rounds in **fresh** conversations until suggestions become incremental
5. Plans should reach 3,000-6,000+ lines for complex projects

### Phase 3: Plan-to-Beads Conversion
- Use the conversion prompt with `br` tool only
- Beads must be self-contained; never need the markdown plan again
- Include testing obligations in every bead
- Expect 200-500 beads for complex projects

### Phase 4: Bead Polishing (4-6+ rounds)
- Run polishing prompt, fresh-eyes reviews, dedup passes
- Cross-reference beads against markdown plan in both directions
- Convergence signals: shorter responses, slower change rate, increasing similarity
- Stop at weighted convergence score 0.75+

### Phase 5: Swarm Launch
- Stagger agent starts by 30+ seconds (avoid thundering herd)
- All agents on `main` branch; no worktrees
- Agents coordinate via Agent Mail, route work via `bv`
- Human role: tend the swarm every 10-15 minutes

### Phase 6: Review, Test, Harden
- Fresh-eyes self-review after each bead
- Cross-agent review every 30-60 minutes
- Run UBS before every commit
- Organized commits by one designated agent every 1-2 hours

## Validation Gates

| Gate | Must Be True Before Advancing |
|------|-------------------------------|
| **Foundation** | Goals, workflows, stack, AGENTS.md, and best-practices guides exist |
| **Plan** | Markdown plan covers workflows, architecture, sequencing, constraints, tests, failure paths |
| **Translation** | Every plan element maps to beads, checked bidirectionally |
| **Bead** | Beads are self-contained, dependency-correct, context-rich, test-explicit |
| **Launch** | Agent Mail, reservations, bv, AGENTS.md, staggered startup ready |
| **Ship** | Reviews, tests, UBS clean, remaining work filed as beads |

## Diagnosing Swarm Failures

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Agents keep picking same bead | Starts not staggered; not marking in_progress | Stagger starts, force claim messages |
| Agent goes in circles after compaction | Forgot AGENTS.md | Force re-read; kill/restart if still erratic |
| Bead sits in_progress too long | Agent crashed or silently blocked | Reclaim bead, split out blocker |
| Contradictory implementations | Not using Agent Mail + reservations | Audit reservation use, revise bead boundaries |
| Lots of code but goal feels far | Strategic drift | Stop, run reality check, revise bead graph |

## The Complete Toolchain (11 Tools)

| Tool | Command | Purpose |
|------|---------|---------|
| NTM | `ntm` | Agent cockpit: spawn, send, broadcast |
| Agent Mail | `am` | Identities, inbox/outbox, file reservations |
| UBS | `ubs` | Bug scanner, 1000+ patterns, pre-commit guard |
| Beads | `br` | Issue tracking with dependencies (SQLite + JSONL) |
| Beads Viewer | `bv` | Triage engine: PageRank, betweenness, HITS |
| RCH | `rch` | Remote build offloading |
| CASS | `cass` | Session search across all agent history |
| CASS Memory | `cm` | Procedural memory: episodic -> working -> procedural |
| CAAM | `caam` | Sub-100ms auth/account switching |
| DCG | `dcg` | Blocks destructive git/filesystem commands |
| SLB | `slb` | Two-person rule for dangerous commands |

### Incremental Onboarding Order
1. **Start with:** Agent Mail + br + bv (the core trio)
2. **Then add:** UBS (bug hunting)
3. **Then add:** DCG (destructive command protection)
4. **Then add:** CASS (session history)
5. **Then add:** CM (codifying lessons into procedural memory)

## AGENTS.md Essential Rules

Every AGENTS.md must include:

1. **Rule 0:** The human's instructions override everything
2. **Rule 1:** Never delete files without explicit permission
3. No destructive git commands (`git reset --hard`, `git clean -fd`)
4. Branch policy: all work on `main`, never `master`
5. No script-based code changes; always make changes manually
6. No file proliferation (no `mainV2.rs` variants)
7. Compiler checks after every change
8. Multi-agent awareness: never stash, revert, or overwrite other agents' work

## Anti-Patterns to Avoid

- **Single-pass beads** - First-draft beads are never optimal. Always 4-5+ polishing passes.
- **Skipping plan-to-bead validation** - Leads to missing features discovered only during implementation.
- **Communication purgatory** - Agents messaging more than coding. Be proactive about starting work.
- **Holding reservations too long** - Reserve, edit, commit, release. Long TTLs block others.
- **Not re-reading AGENTS.md after compaction** - The re-read is mandatory, not optional.
- **Specialist/ringleader agents** - Single points of failure. Keep all agents fungible.
- **Git worktrees** - Creates reconciliation debt. Use Agent Mail + single branch instead.

## bv Graph Interpretation

| Pattern | Meaning | Action |
|---------|---------|--------|
| High PageRank + High Betweenness | Critical bottleneck | DROP EVERYTHING, fix first |
| High PageRank + Low Betweenness | Foundation piece | Important but not currently blocking |
| Low PageRank + High Betweenness | Unexpected chokepoint | Investigate why this is a bridge |
| Low PageRank + Low Betweenness | Leaf work | Safe to parallelize freely |

## Reference Files

### `references/other.md`
The primary reference document containing the complete Agentic Coding Flywheel methodology from agent-flywheel.com, including:
- Full planning workflow with multi-model synthesis
- Plan-to-beads conversion methodology
- Bead polishing and convergence detection
- Coordination stack (Agent Mail + br + bv)
- Swarm launch, tending, and troubleshooting
- Review, testing, and hardening workflows
- Complete toolchain documentation
- CASS memory system and recursive self-improvement
- The operator library (8 reusable cognitive moves)
- All key prompts with context and psychology annotations

### `references/index.md`
Category index for navigating the reference documentation.

## Working with This Skill

### For Beginners
Start with the **Core Loop** and **Incremental Onboarding Order**. You only need Agent Mail + br + bv to capture most of the value. Focus on:
1. Writing one serious markdown plan
2. Converting it to beads with dependencies
3. Running `bv --robot-next` to verify the graph works
4. Launching 1-2 agents with the marching orders prompt

### For Intermediate Users
Master the full workflow phases. Focus on:
- Multi-model plan synthesis (competing plans from 3+ models)
- Bead polishing convergence detection (know when to stop)
- Effective swarm tending (10-15 minute cadence)
- Cross-agent review patterns

### For Advanced Users
Leverage the recursive self-improvement loop:
- Mine CASS sessions to refine skills and tools
- Use `cm context` to load procedural memory at session start
- Build the meta-skill pattern: skills that improve skills
- Use the Idea-Wizard pipeline for feature development on existing projects
- Scale to 10+ agents across multiple projects simultaneously

## Model Recommendations by Phase

| Phase | Best Model | Why |
|-------|-----------|-----|
| Initial plan creation | GPT Pro (web) | Extended reasoning, unlimited usage |
| Plan synthesis | GPT Pro (web) | Best final arbiter |
| Plan refinement | GPT Pro + Opus (web) | Pro reviews, Claude integrates |
| Plan-to-beads | Claude Code (Opus) | Best for structured creation |
| Bead polishing | Claude Code (Opus) | Consistent, thorough |
| Implementation | Claude Code + Codex + Gemini | Diverse swarm |
| Code review | Claude Code + Gemini | Gemini good for review duty |
| Final verification | Codex (GPT) | Different model catches different things |

## Notes

- This skill was generated from the official agent-flywheel.com documentation
- All prompts are preserved verbatim from real sessions that worked well
- The methodology produces outsized results on projects with enough complexity to justify the planning overhead; skip it for trivial one-file changes
- Install everything with one command: `curl -fsSL https://agent-flywheel.com/install.sh | bash`
