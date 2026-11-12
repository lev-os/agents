# RouterGrowth installation

## Choose a transport

- REST needs only `curl` and the key. No CLI is required.
- MCP: `claude mcp add --transport http routergrowth https://api.routergrowth.com/mcp`
  (from the docs; this skill update did not run it).
- CLI: npm `routergrowth` (MIT; latest 0.7.2 on 2026-11-12, `npm view`). The
  binary is `routergrowth`. The docs name version 0.4.0 as the minimum, 0.6.0 for
  `events`, and 0.7.0 for `batch`, `watch` and `--prefer`.

```bash
npm install -g routergrowth    # only when the user asks
```

This skill update installed nothing.

## Credentials and verification

The key variable is `ROUTERGROWTH_API_KEY` (keys start `rg_live_`; the user mints
them in the dashboard under Settings, API keys). It lives in the user's local env
file. Never print it. Free checks:

```bash
command -v routergrowth
routergrowth --version
routergrowth balance
```

A new workspace gets 1 USD of credit that expires after 7 days (from the docs).

## Remove

`npm uninstall -g routergrowth`, and remove the MCP entry with the client's own
command. This does not revoke the key.

Source: <https://routergrowth.com/SKILL.md> and the npm registry, checked 2026-11-12.
