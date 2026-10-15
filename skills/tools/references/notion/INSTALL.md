# Notion CLI installation

## Runtime and checks

This package bundles Notion CLI guidance and its existing license. `ntn` is a
host-installed executable. The official script supports macOS/Linux; the npm
method supports macOS/Linux/Windows and requires Node 22+ and npm 10+.

```bash
command -v ntn
ntn --version
ntn --help
```

## Install

With compatible Node/npm, the official package is:

```bash
npm install --global ntn
```

For the direct macOS/Linux installer, download the shell script to a temporary
file, inspect it, then execute it only within the requested installation scope:

```bash
NTN_INSTALLER="$(mktemp -t ntn-install)"
curl -fsSL https://ntn.dev -o "$NTN_INSTALLER"
less "$NTN_INSTALLER"
bash "$NTN_INSTALLER"
```

The endpoint serves shell content to curl; a browser redirects to the docs.
Windows also has `winget install Notion.ntn` (x64). Select one method and record
it; documentation is not an instruction to install every variant.

## Credentials and verification

Use an already-present `NOTION_API_TOKEN` without printing it. `ntn login`
creates a separate CLI session and is used only when that setup is requested.
The `--version`/help checks are offline; a permitted read of the exact workspace
or page separately verifies access. Read the operation guidance before calls.

## Update and remove

For npm, use `npm update --global ntn` or `npm uninstall --global ntn`. For
direct installs inspect `ntn update --help` before updating; remove only the
recorded executable and installation-created symlink. Inspect `ntn logout
--help` before a requested session logout. Preserve the workspace, keychain and
unrelated tokens; software removal does not authorize deleting credentials.

Source: [official installation](https://developers.notion.com/cli/get-started/installation), checked 2026-10-12.
