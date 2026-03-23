# CDO Architecture Reference

Moved from SKILL.md during rewrite. Contains agent definitions, artifact structure,
domain presets, sub-file loading table, and related skills.

---

## Artifact Structure

```
tmp/cdo-{timestamp}/
├── 00-input.md           # Original problem statement
├── 00-context.md         # Gathered context (files, code, docs)
├── t1-{role}.md          # Turn 1 agent outputs (one per agent)
├── t1-synthesis.md       # Turn 1 synthesis + next turn directive
├── t2-{role}.md          # Turn 2 agent outputs
├── t2-synthesis.md       # Turn 2 synthesis
├── ...
└── FINAL.md              # Converged output
```

### Artifact Rules

- Every agent writes its own file. No shared state between agents during a turn.
- Synthesis reads all turn files. Only synthesis produces the directive.
- The orchestrator reads ONLY the directive YAML block — not the full synthesis.
- FINAL.md is the only user-facing deliverable. Turn artifacts are audit trail.

---

## Domain Presets (exec variants)

| Domain | Team Shape | Skills | Integration |
|--------|-----------|--------|-------------|
| `exec dev` | Dev Lead, Implementer, Reviewer, Tester | lev-sdlc, /work, entity lifecycle | `.lev/pm/` entities, bd tasks |
| `exec arch` | Architect, Critic, Systems, Pragmatist | /arch, ATAM, C4, ADR | `docs/specs/`, `docs/design/` |
| `exec <tag>` | Auto-composed from skill-discovery | lev-catalog search by tag | Workshop POC skills weighted |

When a domain is specified, its team shape becomes the T1 default. The synthesizer can still reshape subsequent turns.

---

## Sub-File Loading Table

Progressive disclosure — only load what the current invocation needs.

| Condition | Load | Purpose |
|-----------|------|---------|
| Complexity >= deep | `dispatch/skill-injection.md` | Skill discovery + injection protocol |
| Team mode active | `dispatch/team-mode.md` | TeamCreate/SendMessage patterns |
| lev-exec mode | `dispatch/multi-model.md` | Multi-model dispatch via CLI |
| Preset == debug | `modes/debug.md` | 7-turn RCA protocol |
| Preset == full + parliament | `modes/parliament.md` | Multi-model parliament seats |
| Need convergence help | `engine/convergence.md` | Exit criteria + confidence calc |
| Synthesis turn | `engine/synthesis-protocol.md` | Synthesis agent instructions |
| Agent brief generation | `templates/agent-brief.md` | Brief template + role injection |
| Domain == exec dev | `domains/dev.md` | Dev team shape + SDLC integration |
| Domain == exec arch | `domains/arch.md` | Architecture team + ADR output |
| Domain == exec <tag> | `domains/generic.md` | Auto-compose from skill catalog |

---

## Related Skills

- `skill://lev-research` — Deep research intelligence. CDO dispatches research agents that use this.
- `skill://bd` — Beads issue tracking. CDO uses bd for epic/task tracking in deep+ and bd modifier.
- `skill://work` — Unified lifecycle router. CDO's exec dev aligns with /work entity lifecycle.
- `skill://arch` — Architecture analysis. CDO's exec arch loads ATAM, C4, ADR frameworks.
- `skill://lev-find` — Context gathering. CDO agents use find for codebase exploration.
- `skill://skill-discovery` — Skill catalog search. CDO's skill injection discovers 2-3 skills per agent.
- `skill://lev-orch-thinking-parliament` — Legacy parliament. CDO subsumes this — use `modes/parliament.md`.

---

## HITL Dashboard Details

Interactive DAG design — user sees a proposed DAG with turns, agents, roles, and skills. User can:

- Modify roles (add/remove/rename)
- Swap skills per agent
- Select power combos (e.g., "architect + critic + pragmatist")
- Adjust turn count and width
- Override convergence criteria
