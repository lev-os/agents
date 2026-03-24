---
name: cm
description: |
  [WHAT] Procedural-memory wrapper around the external `cm` CLI (CASS Memory System).
  [HOW] Pulls task context with `cm context --json`, inspects playbook health, and optionally reflects sessions, while keeping Lev as the router and source of workflow truth.
  [WHEN] Use before non-trivial implementation, debugging, handoffs, retrospection, or when the user asks for memory, playbook, or cross-agent lessons.
  [WHY] Reuses durable cross-agent memory without letting an external memory tool become the project control plane.

  Triggers: "cm", "cass memory", "memory", "playbook", "procedural memory", "reflect", "session memory", "cross-agent memory"
---

# CM

Use `cm` as a tool boundary, not as a replacement for Lev planning, tracking, or canonical project state.

## Prerequisites

```bash
command -v cm
```

If missing, stop and tell the user:

```bash
brew install dicklesworthstone/tap/cm
```

## Golden Rules

1. In agent contexts, prefer `--json`.
2. Start with read paths before any write or reflection path.
3. Keep Lev artifacts authoritative for work tracking; `cm` augments context.
4. Do not change `cm` config, playbooks, or privacy settings unless the user asked.

## Fast Path

Run this before a non-trivial task:

```bash
cm context "<task>" --json
```

Use the response to extract:
- `relevantBullets`
- `antiPatterns`
- `historySnippets`
- `suggestedCassQueries`

## Core Commands

### Get task context

```bash
cm context "fix auth timeout bug" --json
cm context "design repo sync workflow" --json
```

### Check system state

```bash
cm quickstart --json
cm doctor --json
cm stats --json
cm usage --json
```

### Inspect playbook state

```bash
cm playbook list --json
cm top 10 --json
cm stale --json
cm why <bulletId> --json
```

### Reflection and validation

Only do this when the user explicitly wants memory updates or post-session curation.

```bash
cm reflect --days 7 --json
cm validate "Always verify token expiry before auth debugging" --json
```

## Recommended Workflow

### Before work

```bash
cm context "<current task>" --json
```

Then:
1. Pull relevant rules and anti-patterns into your working notes.
2. If a result suggests deeper search, hand off to `cass` for raw-session inspection.
3. Continue execution in Lev normally.

### After work

Only if the user wants learning captured:

```bash
cm reflect --days 1 --json
```

Review proposed rules before treating them as trusted guidance.

## Decision Boundary

Use `cm` when:
- you need distilled lessons
- you want anti-pattern warnings
- you need help recalling prior agent outcomes

Use `cass` instead when:
- you need raw session evidence
- you need cross-agent search over exact history
- you need line-level inspection of prior sessions

## Anti-Patterns

- Running reflection automatically on every task
- Treating `cm` rules as canonical without checking source evidence
- Letting `cm` own project configuration or control-plane decisions
- Updating playbooks during unrelated user requests

## Minimal Report Pattern

When `cm` yields useful guidance, summarize it briefly:

```markdown
## CM Findings
- Relevant rules:
- Anti-patterns:
- Follow-up cass queries:
```

Keep the authoritative plan/handoff in Lev artifacts, not inside `cm`.
