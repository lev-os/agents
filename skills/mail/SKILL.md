---
name: mail
description: "Agent mail for multi-session coordination. Wraps levmail CLI. Register, send, inbox, claim, broadcast, roster."
---

# /mail — Agent Mail

Multi-session agent coordination over `.lev/mail/`. Wraps the `levmail` CLI at `~/.local/bin/levmail`.

## Commands

```
/mail                      # inbox (all messages, newest first)
/mail inbox                # same
/mail inbox <agent-id>     # messages addressed to <agent-id>
/mail send <to> <subject>  # write + send a message (body from context or stdin)
/mail read <file>          # read a specific message
/mail claim <path>         # claim ownership of a file/workstream/folder
/mail broadcast <subject>  # send to all-agents
/mail register <id>        # set this session's agent ID
/mail whoami               # show current agent ID
/mail roster               # show all known agent IDs from message headers
/mail archive <file>       # move message to archive/
```

## How It Works

### First Use in a Session

If no agent ID is registered, prompt to register:
```
You haven't registered an agent ID yet.
Run: /mail register <id>

Active roster:
  A0 — oversight
  A1 — arch IR
  A2 — dashboard
  A3 — constraint code
  A4 — constraint content
```

### /mail (inbox)

```bash
levmail inbox
```

Output format:
```
INBOX (5 messages)
──────────────────
20260411-from-A3-to-A0-parity-update.md    from:A3  subject:parity-update
20260411-broadcast-A0-convergence.md        from:A0  subject:convergence
...
```

### /mail send <to> <subject>

Inline body from conversation context. Uses `levmail send`:

```bash
echo "body text" | levmail send <to> <subject>
```

For longer messages, write the body from the current conversation's key points.

### /mail claim <path>

```bash
levmail claim <path>
```

Broadcasts to all agents: "Agent {id} claims ownership of {path}. Other agents should not modify without coordinating."

### /mail broadcast <subject>

```bash
echo "body" | levmail broadcast <subject>
```

Sends to `all-agents` — every session sees it in their inbox.

## Message Format

Messages are markdown files in `.lev/mail/` with YAML frontmatter:

```yaml
---
from: A0
to: A3
date: 2026-04-11
subject: parity-update
---

Message body here.
```

## Known Issue

The `.lev/mail/.agent-id` file gets clobbered by parallel sessions. Each session overwrites it. Workaround: re-register at session start. Future fix: use env var `LEVMAIL_AGENT_ID` so each shell holds its own identity.

## Data Sources

- `.lev/mail/*.md` — message files
- `.lev/mail/.agent-id` — current session's registered ID
- `.lev/mail/archive/` — archived messages
- `~/.local/bin/levmail` — the CLI

## Protocols

### Detangle Protocol (established 2026-04-10)

Multi-agent coordination for workstream convergence:
1. Each agent dumps nuggets: `/mail broadcast nugget-dump`
2. Each reads all dumps: `/mail inbox`
3. Claim lanes: `/mail claim <path>`
4. Send handoffs: `/mail send <agent> <topic>`
5. Update handoffs with `detangle_sync` block

Full protocol: `.lev/mail/20260410-detangle-protocol-all-agents.md`

### Nugget Ledger Format

```
[VERIFIED|ASSUMED|STALE] <nugget> — owner: <path> — confidence: <0-1>
```

## Graph Footer

After every /mail command, append the shared graph footer from `~/.claude/skills/_shared/graph-footer.md`.
