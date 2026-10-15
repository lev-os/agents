# Slack installation

## Choose a transport

This package includes both CLI and Web API guidance. The CLI is optional for
API-only work: use host `curl` or the task's existing HTTP/SDK client with the
method's required token type. Check `curl --version` for raw HTTP. No Slack CLI
or desktop Slack application is required for that route.

## CLI installation and checks

The official CLI supports macOS and Linux; Windows has a separate official
guide. Git is a CLI dependency. App development additionally needs the runtime
selected by that app (JavaScript/Python Bolt or Deno); installing the CLI alone
does not install or qualify those runtimes.

Read `slack-cli.md` to identify the official executable, including the per-user
`~/.slack/bin/slack` path and collision check. Verify it with:

```bash
"$SLACK_CMD" version
"$SLACK_CMD" help
```

For a requested macOS/Linux install, download and inspect the official script
before executing it:

```bash
SLACK_INSTALLER="$(mktemp -t slack-install)"
curl -fsSL https://downloads.slack-edge.com/slack-cli/install.sh -o "$SLACK_INSTALLER"
less "$SLACK_INSTALLER"
bash "$SLACK_INSTALLER"
```

Preserve an existing different `slack` binary; the installer supports a chosen
alias. Use its documented version option when pinning. The source guide covers
manual archives for macOS Intel/Apple Silicon and Linux x86_64/ARM64.

## Credentials and verification

Follow the existing-login bridge in `slack-cli.md` before requesting another
login or token. API-only calls use the token type and scopes from the actual
method contract. Keep tokens process-local and out of logs. Version checks are
offline; permitted `auth.test` plus scope/header inspection separately verifies
identity and capability. A login is not permission to send or install an app.

## Remove

For a requested removal, use the official uninstall guide and remove only the
CLI executable/symlink belonging to the selected installation. Keep credential
stores, app projects and other `slack` commands. Revoking credentials or removing
a hosted app is a separate provider effect.

Sources: [macOS/Linux installation](https://docs.slack.dev/tools/slack-cli/guides/installing-the-slack-cli-for-mac-and-linux/), [Windows](https://docs.slack.dev/tools/slack-cli/guides/installing-the-slack-cli-for-windows/), [uninstall](https://docs.slack.dev/tools/slack-cli/guides/uninstalling-the-slack-cli/), checked 2026-10-12.
