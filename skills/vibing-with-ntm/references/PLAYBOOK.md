# Vibing With NTM Playbook

Use this file when the main skill body is not enough and you want the denser
operational playbook.

## Spawn and Monitor

```bash
ntm config get projects_base
ntm quick myproject --template=go

ntm spawn myproject --cc=3 --cod=2 --gmi=1
ntm spawn myproject --cc=5 --cod=5 --no-user
ntm spawn myproject --label frontend --cc=3
ntm spawn myproject --label backend --cc=2 --worktrees
ntm spawn myproject --stagger-mode=smart --cc=6 --cod=4
ntm add myproject --cc=2

ntm list
ntm status myproject
ntm attach myproject
ntm dashboard myproject
ntm view myproject
```

### Recommended Starting Sizes

- `--cc=3 --cod=2 --gmi=1`: strong default
- `--cc=5`: deep reasoning, lower coordination overhead
- `--cc=5 --cod=5`: only when the operator loop is already working well

## Operator Tending

```bash
ntm --robot-snapshot
ntm --robot-attention --since-cursor=42
ntm --robot-markdown --md-compact
ntm --robot-terse
ntm --robot-mail-check --mail-project=myproject --urgent-only

ntm mail inbox myproject
ntm locks list myproject --all-agents
ntm coordinator digest myproject
ntm coordinator conflicts myproject
ntm work triage --format=markdown
ntm assign myproject --auto --strategy=dependency
```

### Attention Profiles and Waits

Useful attention profiles:

- `operator`
- `debug`
- `minimal`
- `alerts`

Useful wait conditions:

- `idle`
- `action_required`
- `mail_pending`
- `reservation_conflict`
- `file_conflict`

If the cursor expires, re-run `ntm --robot-snapshot`.

## Reservations and Isolation

Default coordination model:

- Beads decide what should happen.
- Agent Mail says who is doing it.
- File reservations or worktrees prevent collisions.
- NTM surfaces shared state and lets the operator intervene.

Agent Mail reservation example:

```python
file_reservation_paths(
    project_key="/path/to/project",
    agent_name="GreenCastle",
    paths=["internal/auth/**/*.go"],
    ttl_seconds=3600,
    exclusive=True,
    reason="br-123"
)
```

If repo policy allows worktrees, they are also valid:

```bash
ntm spawn myproject --cc=3 --worktrees
ntm worktrees list
ntm worktrees merge claude_1
```

## High-Value Monitoring and Output

```bash
ntm activity myproject --watch
ntm health myproject
ntm watch myproject --cc
ntm copy myproject --all
ntm copy myproject --code
ntm grep "panic" myproject -C 3
ntm logs myproject --panes=1,2
```

## Swarm Anti-Patterns

### Communication Purgatory

Agents keep talking about coordination without taking work.

Fix: require one explicit task owner, one scope claim, and immediate execution.

### File Thrashing

Multiple agents edit the same file or same logical area.

Fix: reserve scope first. When appropriate, move heavy-isolation work to worktrees. Pick a canonical owner when conflicts appear.

### DONE-But-Not-Closed Work

Work is functionally done but the bead state is stale, so downstream work stays blocked.

Fix: periodically check the actual graph state with `bv --robot-triage`, `ntm work triage`, and the relevant `br` status commands.

### Broken Build Drift

One agent breaks the baseline and the swarm keeps coding as if nothing happened.

Fix: announce that the build is broken, route one or two agents to repair it, and obey the repo's heavy-verification rules such as offloading via `rch` when required.

### Idle Agent Drift

An agent stops making progress but still exists in the swarm.

Fix: inspect `--robot-snapshot`, `--robot-tail`, current bead ownership, and whether the agent actually needs a new targeted prompt instead of a vague nudge.

## Agent Lifecycle

### Adding Agents Mid-Session

```bash
ntm add myproject --cc=2
ntm send myproject --panes=5,6 "Read AGENTS.md, check mail, and pick ready work."
```

### Replacing a Dead Agent

```bash
br list --status in_progress
ntm add myproject --cc=1
ntm send myproject --cc "$(cat marching_orders.txt)"
```

### Graceful Shutdown

```bash
ntm send myproject --all "Checkpoint current work and report blockers before stopping."
ntm activity myproject --watch
ntm checkpoint save myproject -m "swarm shutdown"
```

## Troubleshooting

| Problem | What to do |
| --- | --- |
| `spawn` asks to create a directory | Resolve the repo through `projects_base`, use `ntm quick`, or make the repo discoverable from the configured base |
| No ready work | Run `bv --robot-triage`, `bv --robot-next`, or `ntm work triage` |
| Coordination chaos | Check Agent Mail inboxes, lock state, and coordinator digest/conflicts |
| Agent compacted | Re-read repo instructions, then re-check bead, inbox, and `--robot-snapshot` |
| Cursor expired | Re-run `ntm --robot-snapshot` |
| Build broken by swarm | Broadcast the failure, stop speculative work, and route a repair slice immediately |
| Agent looks dead | Inspect `ntm --robot-tail`, bead ownership, and whether it actually needs retasking or replacement |

## FAQ

**How do agents know what to work on?**  
Use `bv --robot-triage`, `bv --robot-next`, or `ntm work triage`.

**How do they avoid conflicts?**  
With file reservations by default, and optionally worktrees when repo policy allows them.

**How many agents should I start with?**  
Usually 3-6. Scale up only when the operator loop is already healthy.

**What is the operator's main monitoring loop?**  
`--robot-snapshot` -> `--robot-attention` / `--robot-wait` -> act -> repeat.

## Validation

The swarm is healthy when:

```bash
ntm dashboard myproject
br list --status in_progress
ntm --robot-terse
ntm --robot-snapshot
```

Repo-specific verification commands still matter. If the repo `AGENTS.md` says to
offload heavy builds or tests through a helper such as `rch`, follow that rule.
