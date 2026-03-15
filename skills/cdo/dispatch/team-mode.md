---
name: cdo-team-mode
description: TeamCreate lifecycle for persistent CDO roles across multiple turns
---

**When to use**: deep+ preset auto-enables, or explicit `team` flag.

**Why team for long graphs**: Teammates accumulate context across turns. An Advocate who saw T1 findings brings richer perspective to T3 than a fresh subagent.

**Lifecycle**:

1. **INIT**: TeamCreate with problem slug
```
TeamCreate: team_name="cdo-{problem-slug}", description="{problem}"
```

2. **SPAWN**: Create teammates for each role
```
Agent(subagent_type=general-purpose, team_name="cdo-{slug}", name="{role}",
     prompt="You are the {role}. {brief with skills injected}")
```

3. **PER-TURN**: SendMessage to existing teammates with turn focus
```
SendMessage(team_name="cdo-{slug}", recipient="{role}",
           message="Turn {N} focus: {from synthesis directive}. Read: {input files}. Write to: {output file}")
```

4. **ADAPTIVE RESIZE**:
- New role needed: spawn additional teammate
- Role no longer relevant: SendMessage shutdown_request
- Width changes: adjust team composition between turns

5. **SHUTDOWN**: After FINAL synthesis
```
SendMessage(team_name="cdo-{slug}", recipient="all", message="CDO complete. Shutting down.")
TeamDelete(team_name="cdo-{slug}")
```

**Subagent mode** (quick/think): Skip TeamCreate. Use parallel Agent calls in single message. Each is ephemeral.
