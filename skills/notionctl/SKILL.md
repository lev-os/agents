---
name: notionctl
description: Thin direct Notion API CLI for the Leviathan workspace. Use when working with `notionctl`, `crates/lev-notionctl`, or `docs/plugins/notion.md`; when you need to inspect auth/config, query data sources, fetch pages, create or update pages, or add comments through the direct API; or when you need to enforce the boundary that workflows such as triage belong in FlowMind/skills rather than in the CLI.
---

# Notionctl

## Overview

Use this skill to work on Leviathan's direct Notion API CLI in `/Users/jean-patricksmith/digital/leviathan/crates/lev-notionctl/`.

Keep the surface thin. `notionctl` owns direct API operations and the local `doctor` check. Workflow semantics, policy logic, and inbox triage belong above the CLI in FlowMind or other skills.

## Boundary

Keep these commands inside notionctl:

- `doctor`
- `search`
- `db query`
- `page get`
- `page create`
- `page update`
- `comment add`

Keep these out of notionctl:

- inbox triage
- reconciliation policies
- rule engines
- workflow orchestration

If the request is really about higher-level workflow behavior, stop changing notionctl and move that logic into a FlowMind flow or another skill.

## Repo Anchors

Read these files first when changing the CLI:

- `/Users/jean-patricksmith/digital/leviathan/crates/lev-notionctl/src/main.rs`
- `/Users/jean-patricksmith/digital/leviathan/crates/lev-notionctl/tests/robot_mode.rs`
- `/Users/jean-patricksmith/digital/leviathan/docs/plugins/notion.md`
- `/Users/jean-patricksmith/digital/leviathan/plugins/notion/README.md`
- `/Users/jean-patricksmith/digital/leviathan/.lev/pm/specs/spec-notion-plugin-cli-2026-03-06.md`
- `/Users/jean-patricksmith/digital/leviathan/.lev/pm/handoffs/20260309-notionctl-plugin-core-execution-session-2.md`

## Workflow

1. Confirm the requested change belongs in the thin CLI boundary.
2. Update code, tests, and docs together so the contract stays aligned.
3. Preserve the robot-mode contract: dense help, `--json`, structured errors, stable exit codes.
4. Use direct Notion terminology where possible; if compatibility aliases remain, document them explicitly.
5. Treat `lev notion ...` as a thin delegate to notionctl, not a workflow host.

## Validation

Run these commands after changes:

```bash
cargo fmt --check --manifest-path /Users/jean-patricksmith/digital/leviathan/crates/lev-notionctl/Cargo.toml
cargo check --manifest-path /Users/jean-patricksmith/digital/leviathan/crates/lev-notionctl/Cargo.toml
cargo clippy --manifest-path /Users/jean-patricksmith/digital/leviathan/crates/lev-notionctl/Cargo.toml -- -D warnings
cargo test --manifest-path /Users/jean-patricksmith/digital/leviathan/crates/lev-notionctl/Cargo.toml
cargo run --manifest-path /Users/jean-patricksmith/digital/leviathan/crates/lev-notionctl/Cargo.toml -- --json doctor
```

For live smoke, require `NOTION_ACCESS_TOKEN` and safe shared IDs before mutating anything. Treat timeouts, missing shared objects, and auth failures as blockers to record, not reasons to widen the CLI.

## Notes

- `doctor` is the accepted local-ops exception inside the CLI.
- `db query` is still the current user-facing name even though the API uses `data_sources`.
- If the user asks to execute through `lev`, verify the local runtime first. In this checkout, `core/poly/bin/lev` has recently been unstable because of poly/core-sdlc runtime resolution issues.
