---
name: apple-tester
description: CLI-first Apple UI tester for iOS Simulator and macOS app automation. Use for deterministic observe/act/verify testing and promotion to XCTest artifacts.
---

# Apple Tester Skill

## Purpose

`apple-tester` is a tester harness, not an autonomous runtime. Default usage is direct command execution + dev watch loop. Use server mode only when you need persistent session state or streamed logs.

Use `apple-tester` as the only public entrypoint. Do not invoke `apple-driver` (or `agent-apple`) directly for daemon/session workflows.

## Strict loop

Always run this loop:

1. `snapshot`
2. Plan one action
3. Execute one action
4. Verify with `is` / `get` / `assert`
5. Repeat

Never run free-form multi-action plans without verification.

## Quick start

If `apple-tester` is not on your PATH yet, install it once from the repo root:

```bash
pnpm apple-tester:cli:install
```

```bash
apple-tester doctor --build-driver
apple-tester server start
apple-tester session start --macos
apple-tester snapshot --json
apple-tester tap @m1
apple-tester is visible @m1
apple-tester session stop
apple-tester server stop
```

## Host input safety

macOS host-input gestures are blocked by default to avoid stealing local mouse/keyboard focus.

Use `--allow-host-input` only for explicit gesture actions:

```bash
apple-tester session start --macos --allow-host-input
apple-tester hold @m1 --duration-ms 900 --allow-host-input
apple-tester right-click @m3 --allow-host-input
```

## iOS flow

```bash
apple-tester server start
apple-tester session start --ios --udid <SIM_UDID>
apple-tester snapshot --json
apple-tester tap @i1
apple-tester swipe --from 200,700 --to 200,250
apple-tester session stop
apple-tester server stop
```

## macOS gestures

```bash
apple-tester hold @m1 --duration-ms 900 --allow-host-input
apple-tester longpress --coords 640,380 --allow-host-input
apple-tester right-click @m3 --allow-host-input
apple-tester swipe --from 400,500 --to 900,500 --duration-ms 500 --allow-host-input
```

## Promotion

Promotion compiles a successful exploratory run into deterministic XCTest files and a promotion manifest:

```bash
apple-tester promote --run-id <RUN_ID> --platform ios --name "Login Smoke"
apple-tester promote --run-id <RUN_ID> --platform ios --name "Login Smoke" --dry-run --diff-lines 120
apple-tester promote --run-id <RUN_ID> --platform ios --name "Login Smoke" --dry-run --write-report ./artifacts/promotion-report.json
```

Output targets:
- iOS: `apps/ios/UITests/Generated/*.swift`
- macOS: `apps/macos/UITests/Generated/*.swift`

## Log streaming for agents

For parser-friendly polling, prefer NDJSON log output:

```bash
apple-tester logs --json --follow | jq -c '.entries[] | {seq, level, message}'
```

## Canonical local development loop

```bash
pnpm dev:watch
```

This performs deterministic change detection and targeted rebuilds without relaunching apps by default (`--no-relaunch`).

## Notes

- `right-click` is macOS-only.
- `hold`/`longpress` use press-and-hold semantics on macOS and best-effort equivalent on iOS.
- Prefer accessibility identifiers in app code for stable promoted tests.
- Use `apple-tester logs --follow` for live daemon diagnostics when actions fail.

## Technique Map

- **Identify scope** — Determine what the skill applies to before executing.
- **Follow workflow** — Use documented steps; avoid ad-hoc shortcuts.
- **Verify outputs** — Check results match expected contract.
- **Handle errors** — Graceful degradation when dependencies missing.
- **Reference docs** — Load references/ when detail needed.
- **Preserve state** — Don't overwrite user config or artifacts.

## Technique Notes

Skill-specific technique rationale. Apply patterns from the skill body. Progressive disclosure: metadata first, body on trigger, references on demand.

## Prompt Architect Overlay

**Role Definition:** Specialist for apple-tester domain. Executes workflows, produces artifacts, routes to related skills when needed.

**Input Contract:** Context, optional config, artifacts from prior steps. Depends on skill.

**Output Contract:** Artifacts, status, next-step recommendations. Format per skill.

**Edge Cases & Fallbacks:** Missing context—ask or infer from workspace. Dependency missing—degrade gracefully; note in output. Ambiguous request—clarify before proceeding.
