# AgentMail installation

## Runtime and checks

This package includes mailbox operations, monitoring and the SuntiQ identity
reference. The CLI is host-installed; API-only integrations can use an existing
HTTP/SDK client instead. The current official native CLI supports macOS 11+
(Intel/Apple Silicon), Linux and Windows x64. Use the documented musl Linux
archive when a static build is needed; manual GNU archives have extra runtime
requirements. Windows npm installation is currently unsupported; use official
release assets/installer there.

```bash
command -v agentmail
agentmail --version
agentmail --help
```

## Install

For a requested macOS/Linux install with existing npm:

```bash
npm install --global agentmail-cli
```

The current package is `agentmail-cli`; do not substitute the older
`@agentmail/cli` package. The official CLI page also documents direct native
release installers, so npm is not a required runtime for the resulting binary.
Record the installed version/method. Existing operation examples include the
older 0.7 CLI's colon-separated resource names; discover actual installed help
and follow the official migration notes before selecting commands.

## Credentials and verification

Use authorized `AGENTMAIL_API_KEY` process environment credentials without
printing them. Version/help checks are offline. A permitted read of the exact
inbox verifies access; an organization list does not establish inbox access.
Inbox creation, sends, drafts and keys are provider writes, not setup checks.
API-only setup still requires the exact endpoint, token scope and transport
from the selected official API contract.

## Update and remove

For npm, use `npm install --global agentmail-cli@latest` or `npm uninstall
--global agentmail-cli` in the requested maintenance scope. For a native
installer, remove only its recorded binary/links. Preserve provider inboxes,
API keys and machine-local credential files; software removal does not revoke
or delete those resources.

Source: [official CLI installation and migration](https://www.agentmail.to/docs/integrations/cli), checked 2026-10-12.
