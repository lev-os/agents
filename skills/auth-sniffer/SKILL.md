---
name: auth-sniffer
description: Deterministic browser auth extraction for agent workflows. Use when you need to stop a running Brave/Chrome/Edge session, relaunch with CDP, extract cookie/localStorage/sessionStorage auth values, and restore normal browser state.
argument-hint: "--service <name> --robot [--browser brave] [--cookie <csv>] [--localStorageKeys=<csv>] [--sessionStorageKeys=<csv>] [--json]"
allowed-tools: Bash(auth-sniff:*)
skill_type: workflow
category: browser-auth
---

# Auth Sniffer Skill

Source of truth:
- FlowMind: `plugins/auth-sniffer/skills/auth-sniffer.flow.yaml`
- Runtime: `plugins/auth-sniffer/src/cli.ts`

## Deterministic Flow

1. Preflight browser and agentping status.
2. Select active CDP-capable browser (`--browser` overrides auto-select).
3. Kill active browser process set and wait until terminated.
4. Relaunch browser with CDP on explicit/free port.
5. Extract required `cookies`, `localStorage`, and `sessionStorage` keys.
6. Stop CDP browser, wait for shutdown, reopen normal browser.
7. Return structured result or structured error.

## Quick Commands

```bash
# Browser inventory (machine-readable)
auth-sniff --list-browsers --json

# Robot mode for a known service
auth-sniff --service twitter --robot --browser brave --json

# Custom extraction (cookie + storage keys)
auth-sniff \
  --domains .x.com \
  --cookie auth_token,ct0 \
  --localStorageKeys=twid \
  --sessionStorageKeys=auth_state \
  --robot \
  --browser brave \
  --json
```

## Output Contract

- Success: `{ "ok": true, "data": { ... } }`
- Error: `{ "ok": false, "error": { "code", "message", "suggestions" } }`
- Exit codes:
  - `0` success
  - `1` not found
  - `2` invalid args
  - `3` runtime error
  - `4` dependency missing
  - `5` timeout

## Build + Emit

```bash
# Compile FlowMind -> SmartDown artifact
pnpm -C plugins/auth-sniffer run skills:compile

# Compile and emit skill to ~/.agents/skills/auth-sniffer/
pnpm -C plugins/auth-sniffer run skills:emit
```
