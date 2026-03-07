# Lev Install & Setup

## Quick Start

```bash
lev install              # Create ~/.config/lev and .lev directories
lev upgrade              # Force reinstall (alias for install --force)
lev install --config ./path/to/config.yaml  # Use custom config
```

## What Gets Installed

| Path | Purpose |
|------|---------|
| `~/.config/lev/` | Global config, logs, state |
| `~/.config/lev/logs/` | Daemon log files |
| `~/.config/lev/daemons/` | pmdaemon process configs |
| `.lev/` | Project-local directory |
| `.lev/config.yaml` | Project configuration |

## Configuration via .lev/config.yaml

```yaml
project:
  name: my-project

poly:
  daemons:
    - name: ck-lite
      autostart: true
    - name: orchestrator
      autostart: false
```

## Location Rules

`.lev` location is fixed (fractal pattern):
- **Global:** `~/.config/lev` (user-level)
- **Local:** `./.lev` (project-level)

Artifact paths within `.lev` (indexes, bd, cache) can be configured in `config.yaml`.

## First-Time Setup Checklist

1. **Install lev globally**
   ```bash
   npm install -g @lev-os/lev
   # or
   pnpm add -g @lev-os/lev
   ```

2. **Run lev install in your project**
   ```bash
   cd your-project
   lev install
   ```

3. **Verify installation**
   ```bash
   lev --version
   ls -la .lev/
   ls -la ~/.config/lev/
   ```

4. **Configure project** (optional)
   Edit `.lev/config.yaml` to customize daemons, indexes, etc.

## Upgrading

```bash
# Upgrade lev CLI
npm update -g @lev-os/lev

# Reinstall project artifacts
lev upgrade
# or
lev install --force
```

## Troubleshooting Install

| Issue | Solution |
|-------|----------|
| Permission denied on ~/.config/lev | `sudo chown -R $USER ~/.config/lev` |
| .lev not created | Run `lev install` from project root |
| Config not found | Check `.lev/config.yaml` exists |
| Daemons not starting | See `references/daemon.md` |

## Next Steps

After installation:
- **Start daemons:** `lev daemon start ck-lite`
- **Check status:** `bd ready` to see available work
- **Search codebase:** `lev get "your query"`

---

**Navigation:**
- ← Back to main skill: Load `SKILL.md`
- → Daemon management: Load `references/daemon.md`
- → Debugging: Load `references/debug.md`
