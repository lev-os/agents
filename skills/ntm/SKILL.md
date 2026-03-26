---
name: ntm
description: Named Tmux Manager for orchestrating Claude, Codex, and Gemini agents in tmux sessions. Use when you need to spawn, attach, message, inspect, or doctor a multi-agent tmux workspace.
---

# NTM

Use `ntm` when the job is bigger than one agent and tmux becomes the coordination surface.

## Install

```bash
brew install tmux
brew install dicklesworthstone/tap/ntm
```

## Shell Integration

```bash
eval "$(ntm shell zsh)"
```

## When to Use

- starting a multi-agent session in tmux
- broadcasting or targeting prompts across panes
- checking health, dependencies, or quota
- resuming from a handoff or attaching to an existing session

## Quick Start

```bash
ntm spawn myproject --cc=2 --cod=1 --gmi=1
ntm attach myproject
ntm send myproject --all "Read AGENTS.md and start on the next bead"
ntm status myproject
ntm doctor
```

## Useful Commands

```bash
ntm deps
ntm health myproject
ntm activity myproject
ntm handoff myproject
ntm mail myproject
ntm locks myproject
ntm checkpoint myproject
ntm watch myproject
ntm tutorial
```

## Agent Notes

- Use `ntm doctor` first in a fresh environment.
- Use `ntm deps` when agents or tmux integration look broken.
- `ntm send` is for prompt fan-out; use targeted flags when you only want one model family.
- If shell integration is missing, load it before assuming the binary is broken.

