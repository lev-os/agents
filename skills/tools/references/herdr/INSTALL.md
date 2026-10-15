# Herdr installation

## Runtime and checks

This package contains optional terminal-transport guidance. `herdr` is a host
binary; other agents can run without it. Official stable binaries cover
macOS/Linux Intel and ARM64, and Windows x64. The Windows archive includes an
app-local ConPTY runtime: preserve the complete extracted directory.

```bash
command -v herdr
herdr --version
herdr --help
herdr agent --help
```

These checks inspect CLI availability. Starting Herdr, creating panes,
installing hooks or prompting an agent are separate task effects.

## Install

On a host already using Homebrew, a requested install is:

```bash
brew install herdr
```

For other supported hosts use the official manual release assets or installer.
Record the release, platform, install method and exact executable path. The
package uses the upstream `herdrdev/herdr` distribution; installing a different
source variant requires selecting it explicitly rather than substituting a
similarly named package.

## Integration and verification

No provider token is required for the basic terminal multiplexer. A controlled
agent keeps its own credentials and session identity. Read the operation
guidance, inspect live `herdr integration --help` when integrations are selected,
and configure hooks only within the requested scope. A help/version check
does not prove an agent pane, session restore or remote-host connectivity.

## Update and remove

Use `brew upgrade herdr` / `brew uninstall herdr` for the Homebrew example. Direct
installs use the official updater within a requested maintenance scope.
Preserve live sessions; changing a binary is separate from stopping/restarting
its server or uninstalling agent hooks. Remove only the recorded installation,
including associated Windows runtime files when that entire install is being
removed.

Source: [official installation](https://herdr.dev/docs/install/), checked 2026-10-12.
