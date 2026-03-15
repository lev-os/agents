---
name: cdo-multi-model
description: Multi-model dispatch via lev exec for genuine perspective diversity
---

**When to use**: `/cdo lev-exec` flag, or stacked with any preset.

**Model Roster**:
| Model | Dispatch Method | Role Affinity | Why |
|-------|----------------|--------------|-----|
| codex gpt-5.2 | `codex --model gpt-5.2-pro -q "<brief>"` | Deep thinker | Frontier reasoning, extended thinking |
| codex gpt-5.4 | `codex --model gpt-5.4 -q "<brief>"` | Code analyst | Codex-optimized for implementation |
| claude-opus-4-6 | Agent tool, default | Architect | Deep edge-case reasoning |
| claude-sonnet-4-6 | Agent tool, subagent_type=general-purpose | Generalist | Fast, balanced |
| claude-haiku-4-5 | Agent tool, subagent_type=general-purpose, mode=auto | Scout/naming | Tests clarity — if haiku can't parse it, the concept isn't well-formed |

**Dispatch Pattern**:
- Claude models: Agent tool with appropriate subagent_type
- GPT/codex models: Bash tool → `codex --model {model} -q "$(cat tmp/cdo-{session}/brief-{role}.md)" > tmp/cdo-{session}/t{N}-{role}.md`
- All write to same artifact directory
- Synthesizer always runs as Claude (it needs to read all files)

**When to use which model**:
- Naming decisions → haiku (scout test: is the name clear to a weaker model?)
- Architecture → opus (deep reasoning)
- Implementation feasibility → codex gpt-5.4
- Strategic thinking → gpt-5.2
- General perspective → sonnet
