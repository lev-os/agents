# Work Templates

Location: `~/.agents/skills/work/templates/`

This directory contains the active templates used by `/work`.

## Available Templates

1. `report.md`
- Use for research findings, audits, and evidence capture.

2. `proposal.md`
- Use for non-trivial solution proposals before execution.

3. `spec.md`
- Use for behavioral spec + acceptance criteria before implementation.

4. `handoff.md`
- Use for session continuity and tick-by-tick state tracking.

There is no `plan.md` template in this skill.

## Required Load Rule

At session start, always load:
- `handoff.md`

Load as needed:
- `report.md`
- `proposal.md`
- `spec.md`

## Handoff Naming

Use:
- `{YYYYMMDD}-{workstream}-{component}-{slug}-session-{N}.md`

Examples:
- `20260301-work-skill-core-reconstruction-session-1.md`
- `20260301-sdlc-docs-gates-audit-session-2.md`

## Minimal Usage Pattern

1. Start or resume handoff from `handoff.md`.
2. Append ticks for each substantive change.
3. Use `report.md` for research-heavy iterations.
4. Use `proposal.md` and `spec.md` before non-trivial execution.
5. Close session with updated `Next Agent Brief`, `Decisions Log`, and `Entity Matrix`.
