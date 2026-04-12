---
name: rust-crates-publishing
description: >-
  Publish Rust crates to crates.io. Use when cargo publish, crates.io tokens, GitHub Actions release workflows, or version/tag alignment are needed.
---

# Rust Crates Publishing

## Quick Start
Add a publish job to your release workflow that runs on tags and requires `CARGO_REGISTRY_TOKEN`:

```yaml
publish-crates:
  name: Publish to crates.io
  needs: release
  runs-on: ubuntu-latest
  timeout-minutes: 15
  if: ${{ !contains(github.ref, '-') }} # skip pre-releases
  steps:
    - uses: actions/checkout@v4
    - uses: dtolnay/rust-toolchain@nightly
    - name: Publish to crates.io
      if: ${{ env.CARGO_REGISTRY_TOKEN != '' }}
      env:
        CARGO_REGISTRY_TOKEN: ${{ secrets.CARGO_REGISTRY_TOKEN }}
      run: cargo publish --all-features
```

## Workflow
- [ ] Ensure crate metadata is ready: `Cargo.toml` version, license, README, repository.
- [ ] Confirm tag matches version (ex: tag `v1.2.3` -> `package.version = "1.2.3"`).
- [ ] Add a release workflow that builds artifacts first, then publishes.
- [ ] Gate publish on tags and non-pre-release tags.
- [ ] Require `CARGO_REGISTRY_TOKEN` secret; skip publish if missing.
- [ ] Dry-run locally: `cargo publish --dry-run`.

## Release Trigger Pattern
Use tag triggers and allow manual dispatch:

```yaml
on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      tag:
        description: 'Tag to release (e.g., v0.1.0)'
        required: true
        type: string
```

## Workspace Publishing
- Publish dependency crates first, then the top-level crate.
- Use `cargo publish -p crate_name` for each crate.

```bash
cargo publish -p core-crate --all-features
cargo publish -p cli-crate --all-features
```

## Guardrails
- Never publish from PRs or forks; only from tags on the main repo.
- Use `--locked` in CI if lockfiles are committed.
- Avoid `publish = false` in `[package]` for crates meant to ship.

## Validation
- `cargo package`
- `cargo publish --dry-run`
- `cargo package --list` (verify included files)
- Ensure CI can reach crates.io (no network restrictions).

## Notes
- `CARGO_REGISTRY_TOKEN` should be a crates.io API token with publish scope.
- Skip publish for pre-releases by checking tag contains `-`.
- Keep publish job last (`needs: release`) to avoid partial releases.

## Troubleshooting
- `HTTP 401` / `token rejected`: confirm token scope and repo secret name.
- `version already uploaded`: bump `package.version` and retag.
- `readme not found`: set `readme = "README.md"` in `Cargo.toml`.

## Deep Dive
- Advanced publishing edge cases: `references/ADVANCED.md`
