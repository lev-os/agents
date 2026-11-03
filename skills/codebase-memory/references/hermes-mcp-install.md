# Hermes install recipe for codebase-memory-mcp

Use this when the user asks to install `DeusData/codebase-memory-mcp` into Hermes as an MCP server.

## Why this path

The upstream installer can auto-configure several coding agents, but Hermes should own its own MCP config. Install the binary with `--skip-config`, then add it through `hermes mcp add`.

## Commands

```bash
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh -o /tmp/codebase-memory-install.sh
bash /tmp/codebase-memory-install.sh --skip-config --dir=/opt/data/home/.local/bin
printf 'Y\n' | /opt/data/.local/bin/hermes mcp add codebase-memory --command /opt/data/home/.local/bin/codebase-memory-mcp
/opt/data/.local/bin/hermes mcp test codebase-memory
```

## Expected result

- Installed binary: `/opt/data/home/.local/bin/codebase-memory-mcp`
- `codebase-memory-mcp --version` returns a version, e.g. `0.8.1`
- Hermes config gains:

```yaml
mcp_servers:
  codebase-memory:
    command: /opt/data/home/.local/bin/codebase-memory-mcp
    enabled: true
```

- `hermes mcp test codebase-memory` connects and discovers 14 tools.

## Fresh-session requirement

MCP tool schemas are loaded at session start. After installing or changing MCP config, restart the gateway or start a new Hermes session before expecting the tools in chat.

## Notes

If `hermes` is not on the tool PATH, use the absolute Hermes binary discovered in this environment: `/opt/data/.local/bin/hermes`. Do not encode temporary PATH failures as a durable tool limitation.
