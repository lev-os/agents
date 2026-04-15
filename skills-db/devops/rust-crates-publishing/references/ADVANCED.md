# Advanced: crates.io Publishing

## Token + Auth
- Use a crates.io API token with publish scope; store as `CARGO_REGISTRY_TOKEN` secret.
- If 2FA is enabled on the account, publish must use an API token (not password).

## Version/Tag Hygiene
- Enforce tag/version alignment (ex: tag `v1.2.3` -> `package.version = "1.2.3"`).
- For workspaces, ensure each crate’s version is set correctly before publishing.

## Workspace Order
- Publish dependency crates first, then downstream crates.
- Use explicit publish order with `cargo publish -p` to avoid race/conflicts.

## Package Contents
- Verify included files with `cargo package --list`.
- Use `[package] include`/`exclude` to control shipped files.
- Ensure `readme`, `license`, and `repository` fields are set when required.

## CI Guardrails
- Only publish from tag builds on the canonical repo (not forks).
- Skip pre-release tags (ex: `v1.2.3-beta.1`).
- Keep publish job last (`needs: release`) to avoid partial releases.

## Common Failures
- `version already uploaded`: bump version, retag.
- `readme not found`: set `readme = "README.md"` or point to correct path.
- `missing license`: set `license` or `license-file`.
- `HTTP 401`: wrong secret name or token lacks publish scope.

## Dry Run Discipline
- Always run `cargo publish --dry-run` before release.
- Use `cargo package` to validate package layout locally.
