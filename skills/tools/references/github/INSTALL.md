# GitHub installation

## Runtime and checks

This package bundles GitHub operation guidance and its compatibility reference.
The `gh` executable is host-installed. Git is also required for clone/checkout
operations. GitHub supports macOS, Linux and Windows; select the release asset
for the host architecture or its package manager.

```bash
command -v gh
gh --version
gh --help
```

## Install

On macOS with an existing Homebrew installation:

```bash
brew install gh
```

For other hosts or a manually pinned binary, use the official
[installation index](https://github.com/cli/cli#installation) and release assets.
Read the selected install method before executing it. This documentation update
does not run a global installer or create a GitHub session.

## Credentials and verification

Inspect `gh auth status --help`, then `gh auth status`. Use the existing
authorized account or process environment token; keep its value out of output.
Establish a login with `gh auth login` only when requested. Resolve the target
repository in the operation guidance before a provider call. CLI/version
checks prove local availability; target access needs a scoped provider read.

## Update and remove

For a Homebrew install, use `brew upgrade gh` or `brew uninstall gh` within a
requested software-maintenance scope. For a manual binary, remove only the
recorded installed executable. Removing the executable is separate from
revoking credentials; inspect `gh auth logout --help` before a requested logout.
Preserve repositories, worktrees and unrelated accounts.

Source: [official macOS installation](https://github.com/cli/cli/blob/trunk/docs/install_macos.md), checked 2026-10-12.
