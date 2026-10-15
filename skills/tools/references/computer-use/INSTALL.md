# Local installation

## Contents

- [Check prerequisites](#check-prerequisites)
- [Connect the bundled bridge](#connect-the-bundled-bridge)
- [Verify](#verify)
- [Recover and remove](#recover-and-remove)

## Check prerequisites

The bridge source and its executable entrypoint are bundled under `upstream/`.
It has no runtime npm dependencies: neither npm package installation nor a
marketplace is needed to run it. These dependencies remain host-installed:

| Dependency | Requirement / setup |
|---|---|
| macOS | Upstream runtime declares 14.4 or later; upstream verified arm64. Other architectures remain unverified. |
| Node.js | 22.14.0 or later. Check `node --version`; install a compatible version using the host's existing Node manager or [official Node downloads](https://nodejs.org/en/download). |
| ChatGPT or Codex | Supply your own installed app and working Computer Use runtime. Enable Computer Use through that app; this leaf does not download or redistribute OpenAI binaries. |
| Signed Codex launcher | Executable bundled at `/Applications/ChatGPT.app/Contents/Resources/codex` or `/Applications/Codex.app/Contents/Resources/codex`; upstream also supports a custom launcher path. |
| Computer Use client | Existing executable under the Codex data directory; see check below. |
| macOS permissions | Accessibility and Screen Recording for the installed OpenAI runtime. Grant them through macOS System Settings for the task's host. |
| MCP host | Claude Code or another compatible stdio MCP host. The command below is verified against local Claude CLI help; real host integration remains untested. |

Bind `CU_LEAF_ROOT` to the absolute directory containing this leaf's `SKILL.md`.
For the normal Tools installation:

```bash
CU_LEAF_ROOT="$HOME/.agents/skills/tools/references/computer-use"
node --version
claude --version
test -f "$CU_LEAF_ROOT/upstream/bin/computer-use-mcp-bridge.mjs"
test -x "${COMPUTER_USE_CLIENT_PATH:-${CODEX_HOME:-$HOME/.codex}/computer-use/Codex Computer Use.app/Contents/SharedSupport/SkyComputerUseClient.app/Contents/MacOS/SkyComputerUseClient}"
```

Check the launcher selected by `COMPUTER_USE_CODEX_LAUNCHER_PATH`, when present,
or one of the two default paths above. These checks establish file/runtime
availability; they do not prove macOS permissions or server connectivity.

## Connect the bundled bridge

Only run registration when the user requests host connection. The unchanged
bridge automatically accepts every upstream elicitation and launches the client
with an unrestricted profile. App text and screenshots return to the MCP host
and can reach its configured model provider. The current leaf install copies
source and instructions only.

Inspect live help and existing configuration before registering; preserve any
existing server with the same name:

```bash
claude mcp add --help
claude mcp list
claude mcp add --scope user --transport stdio computer-use -- node "$CU_LEAF_ROOT/upstream/bin/computer-use-mcp-bridge.mjs"
```

`--scope user` connects all Claude projects for this account. Use `--scope local`
from the named project root for project-only local setup. Start a fresh Claude
session and inspect `/mcp`. MCP-only registration does not load instructions:
read this Tools leaf explicitly or load it through the Tools router.

For another stdio MCP host, use command `node` with one argument: the absolute
path to `upstream/bin/computer-use-mcp-bridge.mjs`. Inspect that host's actual
configuration contract before writing it. This leaf is distributed through
Tools and Lev's skills; see the [worker/FlowMind loading contract](../../../lev/references/tool-skills.md).

## Verify

Offline checks use only the bundled fake service and do not control real apps:

```bash
cd "$CU_LEAF_ROOT"
shasum -a 256 -c UPSTREAM.sha256
node --test upstream/test/bridge.test.mjs
```

When real runtime testing is requested, run:

```bash
node "$CU_LEAF_ROOT/upstream/scripts/real-smoke-test.mjs"
```

This connects to the installed service, calls `list_apps` and reads Calculator
state plus a screenshot. It is a real app-access test. Then ask Claude to
compute `12 × 12` in Calculator and verify `144` in fresh state. Test drag/canvas
work on a disposable target and headless `claude -p` separately; arithmetic
alone does not prove either.

## Recover and remove

Use `upstream/README.md` for missing-client, signed-launcher, version mismatch,
idle-release and stopped-session diagnostics. Preserve the existing 60-second
idle timeout unless the task calls for another value. Do not use the fake-test
direct-launch override to bypass the real signed-launcher path.

If an action stops or its result is uncertain, read fresh state before retrying;
respect an explicit user stop. Read `claude mcp remove --help`, then remove only
the registered scope/name (`claude mcp remove --scope user computer-use` for
the user-scoped example). Restart the affected Claude session. Preserve the
installed OpenAI app/runtime and unrelated servers.
