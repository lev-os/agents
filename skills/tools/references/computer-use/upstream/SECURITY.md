# Security

## Reporting a vulnerability

Please report vulnerabilities through GitHub's private vulnerability reporting
for `songkeys/claude-codex-computer-use`. Do not include private screenshots,
credentials, or application data in a public issue.

## Security model

This package has no runtime npm dependencies and contains no OpenAI binaries or
credentials. It launches a Computer Use installation already present on the
user's Mac.

The bridge automatically accepts the Computer Use MCP app-access elicitation
and launches the signed client with an unrestricted Codex permission profile.
Once enabled, the tools can inspect screenshots and accessibility content and
can click, type, scroll, drag, or otherwise interact with local applications.

Accessibility text and screenshots are returned to the MCP client and may be
sent to the model provider configured in Claude Code. Users are responsible
for deciding which applications and data are appropriate for that provider.
