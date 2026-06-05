---
name: notionctl
description: "Thin Notion API CLI for doctor, search, queries, pages, and comments. Use when changing notionctl/lev-notionctl or keeping triage and policy out of the CLI surface."
---

# Notionctl

## Overview

Use this skill to work on Leviathan's direct Notion API CLI in `$HOME/digital/leviathan/crates/lev-notionctl/`.

Keep the surface thin. `notionctl` owns direct API operations and the local `doctor` check. Workflow semantics, policy logic, and inbox triage belong above the CLI in FlowMind or other skills.

## Boundary

Keep these commands inside notionctl:

- `doctor`
- `auth set`
- `auth list`
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

- `$HOME/digital/leviathan/crates/lev-notionctl/src/main.rs`
- `$HOME/digital/leviathan/crates/lev-notionctl/tests/robot_mode.rs`
- `$HOME/digital/leviathan/docs/plugins/notion.md`
- `$HOME/digital/leviathan/plugins/notion/README.md`
- `$HOME/digital/leviathan/.lev/pm/specs/spec-notion-plugin-cli-2026-03-06.md`
- `$HOME/digital/leviathan/.lev/pm/handoffs/20260309-notionctl-plugin-core-execution-session-2.md`

## Workflow

1. Confirm the requested change belongs in the thin CLI boundary.
2. Update code, tests, and docs together so the contract stays aligned.
3. Preserve the robot-mode contract: dense help, `--json`, structured errors, stable exit codes.
4. Use direct Notion terminology where possible; if compatibility aliases remain, document them explicitly.
5. Treat `lev notion ...` as a thin delegate to notionctl, not a workflow host.

## Profile Auth and Keychain Setup

Use profiles whenever more than one Notion workspace/account can be present. Kingly and Leviathan should not share a generic token during migration work.

Token resolution:

1. No profile: read `NOTION_ACCESS_TOKEN`.
2. Profile selected by `--profile <name>` or `NOTION_PROFILE=<name>`: read `NOTION_ACCESS_TOKEN_<PROFILE>`.
3. If the profile env token is missing on macOS: read Keychain service `notionctl`, account `<profile>`.
4. When a profile is selected, do not fall back to `NOTION_ACCESS_TOKEN`.

Reproducible setup on each Mac:

```bash
export NOTION_ACCESS_TOKEN_KINGLY='...'
export NOTION_ACCESS_TOKEN_LEV='...'

cargo run --manifest-path $HOME/digital/leviathan/crates/lev-notionctl/Cargo.toml -- \
  --profile kingly auth set --token-env NOTION_ACCESS_TOKEN_KINGLY
cargo run --manifest-path $HOME/digital/leviathan/crates/lev-notionctl/Cargo.toml -- \
  --profile lev auth set --token-env NOTION_ACCESS_TOKEN_LEV

cargo run --manifest-path $HOME/digital/leviathan/crates/lev-notionctl/Cargo.toml -- \
  --profile kingly --json doctor
cargo run --manifest-path $HOME/digital/leviathan/crates/lev-notionctl/Cargo.toml -- \
  --profile lev --json doctor
```

`auth list` can report environment-visible profiles and selected-profile status. It does not enumerate all Keychain items; verify Keychain profiles one at a time with `doctor --profile <name>`.

For tests and CI, set `NOTIONCTL_DISABLE_KEYCHAIN=1` to force env-only auth resolution.

Security note: Keychain avoids long-lived shell exports, but the Notion token remains a bearer secret. Treat page/database sharing, separate Notion integrations, and future data leases as the real authorization boundary above notionctl.

## Validation

Run these commands after changes:

```bash
cargo fmt --check --manifest-path $HOME/digital/leviathan/crates/lev-notionctl/Cargo.toml
cargo check --manifest-path $HOME/digital/leviathan/crates/lev-notionctl/Cargo.toml
cargo clippy --manifest-path $HOME/digital/leviathan/crates/lev-notionctl/Cargo.toml -- -D warnings
cargo test --manifest-path $HOME/digital/leviathan/crates/lev-notionctl/Cargo.toml
cargo run --manifest-path $HOME/digital/leviathan/crates/lev-notionctl/Cargo.toml -- --json doctor
cargo run --manifest-path $HOME/digital/leviathan/crates/lev-notionctl/Cargo.toml -- --profile lev --json doctor
```

For live smoke, require `NOTION_ACCESS_TOKEN` and safe shared IDs before mutating anything. Treat timeouts, missing shared objects, and auth failures as blockers to record, not reasons to widen the CLI.

## Notes

- `doctor` is the accepted local-ops exception inside the CLI.
- `db query` is still the current user-facing name even though the API uses `data_sources`.
- If the user asks to execute through `lev`, verify the local runtime first. In this checkout, `core/poly/bin/lev` has recently been unstable because of poly/core-sdlc runtime resolution issues.
