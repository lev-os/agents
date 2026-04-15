# Vibing With NTM Prompt Bank

Use these prompts as building blocks. Adjust them to the repo's actual `AGENTS.md`
instead of sending them blindly.

## Generic Start-of-Session Prompt

```text
Before doing anything else, read all of AGENTS.md and README.md and understand both. Then inspect the codebase enough to understand the project purpose, architecture, and the workflows that matter for this repo.

Register with MCP Agent Mail if the repo expects it, introduce yourself to the other agents, and check for any existing coordination threads. If the repo uses Beads and BV, use them to find ready work and pick the next task you can usefully advance now.

Do not get stuck in communication purgatory. Announce what you are taking on, reserve the relevant files or worktree scope, start doing real work, keep your bead status current, and reply promptly to important agent mail.

If the repo AGENTS.md has special rules for builds, tests, lints, or remote execution helpers such as rch, follow those rules exactly.
```

## NTM-Repo-Specific Marching Orders

This is closer to the marching order style used on the NTM repo itself:

```text
First read all of AGENTS.md and README.md carefully and understand both. Then investigate the codebase enough to understand the project architecture and the concrete workflow surfaces that matter for the current task.

Register with MCP Agent Mail, introduce yourself to the other agents, check your inbox, and respond promptly to any coordination messages. Use Beads and BV to decide what to work on next, mark your work clearly, and keep progress visible in both bead state and mail.

Do not drift into communication purgatory. Take one useful task, announce it, reserve the relevant scope, and start executing. When you are unsure what to do next, use BV or the repo's preferred triage surface and immediately start on the best ready task.
```

## Code Review Agent Prompt

```text
Explore the codebase deeply enough to understand the relevant execution flows, then do a methodical fresh-eyes review to find obvious bugs, regressions, race conditions, reliability issues, security problems, or sloppy assumptions. Fix the real problems you find and verify them according to the repo instructions.
```

## Move-to-Next-Bead Prompt

```text
Reread AGENTS.md so the repo rules are fresh. Use the available work graph tools to find the highest-impact ready task you can usefully advance now, claim it clearly, coordinate with the other agents, and start coding immediately instead of waiting for more instructions.
```

## Post-Compaction Prompt

```text
Reread AGENTS.md and re-establish the repo-specific rules before you do anything else. Then re-check your current bead, inbox, and the current work graph so you resume from real state instead of memory.
```

## Self-Review Prompt

```text
Read over all of the code you just wrote and the existing code you modified with fresh eyes. Look for obvious bugs, regressions, unsafe assumptions, confusing logic, missing tests, and sloppy edge cases. Fix anything you find before you move on.
```

## Cross-Review Prompt

```text
Turn your attention to code written by the other agents and review it critically for bugs, regressions, reliability problems, security issues, and poor assumptions. Diagnose root causes, then fix what actually needs fixing.
```

## Random Exploration Prompt

```text
Randomly explore unfamiliar parts of the codebase, trace the real execution flow, understand how those pieces fit into the larger workflow, and then do a fresh-eyes pass for obvious bugs and bad assumptions. Fix what you can justify.
```

## Commit-Only Prompt

```text
Based on your current understanding of the repo, group the existing changes into logical commits with detailed messages. Do not edit code. Exclude obviously ephemeral files. Follow the repo's branch and commit rules exactly.
```

## Graceful Shutdown Prompt

```text
Finish the smallest coherent piece of work you are currently in the middle of, checkpoint your status, update the bead and coordination thread, and then stop cleanly.
```
