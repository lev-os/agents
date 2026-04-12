# Daemon Management

## Quick Commands

```bash
bd daemons list              # Show all workspace daemons
lev daemon list              # Show registered poly daemons
lev daemon start <name>      # Start a daemon
lev daemon stop <name>       # Stop a daemon
lev daemon logs <name>       # View daemon logs
lev status                   # Show current system status
```

## Daemon Types

### Workspace Daemons (bd)

Managed by beads, track Claude Code sessions:

```bash
bd daemons list
# WORKSPACE                    PID    VERSION  UPTIME  LAST ACTIVITY
# /path/to/project             67051  0.30.0   2.0h    just now
```

### Poly Daemons

Long-running services defined in `core/*/src/daemons/`:

| Daemon | Purpose | Port |
|--------|---------|------|
| `ck-lite` | Lightweight Claude kernel | 18080 |
| `leann` | Vector index server | 18081 |
| `orchestrator` | Multi-agent coordination | 18082 |

## Configuration

### Project-Level (.lev/config.yaml)

```yaml
poly:
  daemons:
    - name: ck-lite
      autostart: true
      port: 18080
      env:
        LOG_LEVEL: debug

    - name: leann
      autostart: false
      healthcheck: /health
```

### Daemon Definition Pattern

Daemons are discovered via fractal pattern in `core/*/src/daemons/`:

```yaml
# core/polyglot-runners/config.yaml
fractals:
  daemons:
    glob: "core/*/src/daemons/**/*.{py,ts}"
    handler: poly:daemon-runner
    defaults:
      restart_policy: on-failure
      max_restarts: 3
      healthcheck: /health
```

## Lifecycle

```
┌─────────────────────────────────────────────────┐
│                 Daemon States                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  stopped ──start──> starting ──ready──> running │
│     ↑                   │                  │    │
│     └────stop───────────┴────error────────┘    │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Signals

| Signal | Action |
|--------|--------|
| `SIGTERM` | Graceful shutdown |
| `SIGUSR1` | Restart/reload |
| `SIGUSR2` | Debug dump |

## Logs

```bash
# View logs for a specific daemon
lev daemon logs ck-lite

# Logs location
~/.config/lev/logs/<daemon-name>.log
```

## Health Checks

```bash
# Check system status
lev status

# Check specific daemon health endpoint
curl http://localhost:18080/health
```

## Common Operations

### Start Multiple Daemons

```bash
# Start daemons individually
lev daemon start ck-lite
lev daemon start leann
```

### Stop Daemons

```bash
# Stop daemons individually
lev daemon stop ck-lite
lev daemon stop leann
```

### Restart After Config Change

```bash
# Stop then start (restart not available)
lev daemon stop ck-lite && lev daemon start ck-lite
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | `lsof -i :<port>` then kill conflicting process |
| Daemon won't start | Check logs: `lev daemon logs <name>` |
| Health check failing | Verify endpoint: `curl localhost:<port>/health` |
| High memory usage | Stop and start: `lev daemon stop <name> && lev daemon start <name>` |

## Adding a New Daemon

1. Create daemon file in `core/<package>/src/daemons/<name>.ts`
2. Register in `core/<package>/config.yaml`:
   ```yaml
   poly:
     daemons:
       - name: my-daemon
         handler: src/daemons/my-daemon.ts
         port: 18090
   ```
3. Run `lev install` to regenerate registry
4. Start: `lev daemon start my-daemon`

---

**Navigation:**
- ← Back to main skill: Load `SKILL.md`
- ← Install & setup: Load `references/install.md`
- → Debugging: Load `references/debug.md`
