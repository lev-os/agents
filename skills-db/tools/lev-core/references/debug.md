# Debugging & Troubleshooting

## Diagnostic Commands

```bash
bd doctor              # Check for sync issues, missing hooks
bd stats               # Project statistics
lev daemon status      # Health check all daemons
lev --version          # Verify lev CLI version
```

## Common Issues

### Installation Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `lev: command not found` | Not installed globally | `npm install -g @lev-os/lev` |
| Permission denied on ~/.config/lev | Wrong ownership | `sudo chown -R $USER ~/.config/lev` |
| .lev not created | Not in project root | `cd your-project && lev install` |
| Config syntax error | Invalid YAML | Validate `.lev/config.yaml` |

### Daemon Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Port already in use | Conflicting process | `lsof -i :<port>` then kill |
| Daemon crashes immediately | Missing dependency | Check logs: `lev daemon logs <name>` |
| Health check timeout | Slow startup | Increase timeout or check resources |
| High CPU/memory | Memory leak | Restart: `lev daemon restart <name>` |

### Search Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| No results from `lev get` | Index not built | `lev index build` |
| Stale results | Index outdated | `lev index rebuild` |
| LEANN server not responding | Daemon not running | `lev daemon start leann` |

### Beads (bd) Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `bd: command not found` | Not in PATH | Check installation |
| Sync failures | Git conflicts | `bd sync --status` to diagnose |
| Missing issues | Wrong branch | Ensure on correct branch |
| Stale workspace | Daemon issue | `bd daemons list` to verify |

## Debug Mode

Enable verbose logging:

```bash
# Environment variable
DEBUG=lev:* lev <command>

# Or in config
# .lev/config.yaml
logging:
  level: debug
  verbose: true
```

## Log Locations

| Log | Location |
|-----|----------|
| Daemon logs | `~/.config/lev/logs/<daemon>.log` |
| Session logs | `~/.config/lev/sessions/` |
| Build logs | `.lev/cache/build.log` |

## Health Check Endpoints

```bash
# Check daemon health
curl http://localhost:18080/health  # ck-lite
curl http://localhost:18081/health  # leann
curl http://localhost:18082/health  # orchestrator
```

## Reset & Recovery

### Soft Reset (preserve config)

```bash
lev upgrade  # Reinstall without losing config
```

### Hard Reset (start fresh)

```bash
rm -rf .lev/
rm -rf ~/.config/lev/
lev install
```

### Clear Indexes

```bash
rm -rf .lev/indexes/
lev index build
```

### Clear Cache

```bash
rm -rf .lev/cache/
```

## Diagnostic Checklist

When things aren't working:

1. **Check versions**
   ```bash
   lev --version
   node --version
   pnpm --version
   ```

2. **Check daemons**
   ```bash
   bd daemons list
   lev daemon status
   ```

3. **Check logs**
   ```bash
   lev daemon logs ck-lite --tail 50
   ```

4. **Check config**
   ```bash
   cat .lev/config.yaml
   cat ~/.config/lev/config.yaml.example
   ```

5. **Run doctor**
   ```bash
   bd doctor
   ```

## Getting Help

- **Skills:** `openskills read lev-core`
- **BD docs:** `openskills read bd`
- **Search:** `lev get "your issue"`
- **Issues:** Check `bd ready` for related work

---

**Navigation:**
- ← Back to main skill: Load `SKILL.md`
- ← Install & setup: Load `references/install.md`
- ← Daemon management: Load `references/daemon.md`
