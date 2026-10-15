# Claude Codex Computer Use

An experimental, unofficial bridge that lets
[Claude Code](https://code.claude.com) control local macOS applications
through an existing OpenAI Computer Use installation.

The package contains no OpenAI binaries. It starts the Computer Use client
already installed on the user's Mac and translates the small MCP compatibility
gap between Claude Code and that client.

## Requirements

- macOS. The installed OpenAI runtime currently declares macOS 14.4 or later.
- Claude Code with plugin support. Version 2.1.223 is verified.
- ChatGPT or Codex with OpenAI Computer Use installed and working.
- Accessibility and Screen Recording permissions granted to the OpenAI
  Computer Use runtime.

The bridge looks for the Computer Use client at:

```text
$CODEX_HOME/computer-use/Codex Computer Use.app/Contents/SharedSupport/
SkyComputerUseClient.app/Contents/MacOS/SkyComputerUseClient
```

When `CODEX_HOME` is unset, it defaults to `~/.codex`.

## Install as a Claude Code plugin

In a Claude Code session:

```text
/plugin marketplace add songkeys/claude-codex-computer-use
/plugin install claude-codex-computer-use@songkeys
```

Or from the shell:

```sh
claude plugin marketplace add songkeys/claude-codex-computer-use
claude plugin install claude-codex-computer-use@songkeys
```

New sessions load the Computer Use Skill and MCP server automatically.

Inspect the installation with:

```text
/plugin
/mcp
```

## Install the MCP bridge from npm

The plugin installation is recommended because it includes both the MCP bridge
and the Computer Use Skill. The npm package can also be used as a standalone
stdio MCP server:

```sh
claude mcp add computer-use -- npx -y claude-codex-computer-use@latest
```

Or as a direct `.mcp.json` entry:

```json
{
  "mcpServers": {
    "computer-use": {
      "command": "npx",
      "args": ["-y", "claude-codex-computer-use@latest"]
    }
  }
}
```

This MCP-only installation does not load the bundled Skill. Prefer the plugin
unless the MCP client supplies its own Computer Use instructions.

## Usage

Ask Claude to use Computer Use explicitly, or describe a desktop task:

```text
Use Computer Use to inspect Calculator and enter 42.
```

```text
Open System Settings with Computer Use and tell me what page is visible.
```

The bundled Skill instructs Claude to use an observable state/action/state
loop:

1. Read the target app with `get_app_state`.
2. Use accessibility elements when available and screenshot coordinates only
   as a fallback.
3. Perform the action.
4. Fetch a fresh app state before deciding the next action.

## How it works

The OpenAI Computer Use service authenticates the client process ancestry.
Launching its MCP client directly from Claude Code is rejected as an
unauthenticated sender. The bridge therefore uses the signed Codex executable
bundled with ChatGPT or Codex as a process launcher:

```text
Claude Code
  -> claude-codex-computer-use bridge
  -> signed Codex launcher
  -> OpenAI Computer Use MCP client
  -> OpenAI Computer Use service
```

Codex is not used as an agent and no OpenAI model request is made by the
bridge. It runs `codex sandbox` with Codex's disabled/unrestricted permission
profile so the signed client can access its normal caches, macOS services, and
Unix sockets.

The Computer Use client requires its MCP client to advertise the elicitation
capability and answers app-access approvals through it. The bridge guarantees
that capability is present on `initialize` and automatically accepts the
app-access elicitation, so sessions work unattended. All other JSON-RPC
messages, including screenshot image blocks, pass through unchanged.

The Computer Use service treats a connected client as an active hold on the
controlled applications and releases them when the client exits. Codex ends
its client at the end of a conversation, but Claude Code keeps plugin MCP
servers alive for the whole session. The bridge therefore terminates the
client after 60 seconds without traffic and relaunches it on demand,
transparently replaying the recorded `initialize` handshake, so apps are not
held between tasks.

The service also scopes a user-initiated stop (the overlay's Esc cancel) to
the client's current "turn", which never ends for a long-lived client. When a
tool result reports that the app session was stopped by the user, the bridge
recycles the client so the next request starts a fresh session instead of
hitting the same stop again.

## Configuration

Environment variables:

| Variable | Purpose |
| --- | --- |
| `CODEX_HOME` | Override the Codex data directory. Defaults to `~/.codex`. |
| `COMPUTER_USE_CLIENT_PATH` | Override the full path to `SkyComputerUseClient`. |
| `COMPUTER_USE_CODEX_LAUNCHER_PATH` | Override the signed Codex executable path. |
| `COMPUTER_USE_BRIDGE_IDLE_TIMEOUT_MS` | Idle time before the client is released. Defaults to `60000`; `0` keeps the client running for the whole session. |
| `COMPUTER_USE_BRIDGE_DEBUG=1` | Write bridge diagnostics to stderr. |

The signed launcher is discovered in this order:

1. `COMPUTER_USE_CODEX_LAUNCHER_PATH`
2. `/Applications/ChatGPT.app/Contents/Resources/codex`
3. `/Applications/Codex.app/Contents/Resources/codex`

## Security and data flow

Installing this package gives Claude access to the local Computer Use tools,
which can read screenshots, click, type, scroll, drag, and interact with
applications.

The bridge intentionally:

- automatically accepts the Computer Use MCP app-access elicitation;
- launches the signed client with an unrestricted Codex permission profile;
- passes accessibility text and screenshots back to Claude as MCP tool
  results;
- releases the client after an idle timeout so applications are not held
  between tasks, and relaunches it on demand.

Claude Code may send those tool results to the configured model provider as
part of the conversation. Do not install the plugin unless that behavior is
acceptable for the applications and data on the Mac.

## Compatibility

The initial release was verified with:

| Component | Verified version |
| --- | --- |
| Claude Code | 2.1.223 |
| ChatGPT bundled Codex | 0.148.0-alpha.15 |
| OpenAI Computer Use runtime | 26.817.1000761 |
| macOS / architecture | macOS 27.0 / arm64 |
| MCP protocol | 2025-11-25 |

OpenAI Computer Use is an internal desktop integration rather than a stable
third-party SDK. ChatGPT, Codex, or Computer Use updates may change binary
paths, process-authentication rules, or protocol behavior.

## Development

The bridge has no runtime npm dependencies.

```sh
pnpm install
pnpm test
pnpm smoke
```

`pnpm test` uses a fake Computer Use server and is safe to run anywhere.
`pnpm smoke` connects to the real local service, calls `list_apps`, and
verifies that `get_app_state` returns both text and a JPEG screenshot.

## Troubleshooting

### `Sender process is not authenticated`

The Computer Use client was started directly instead of through the signed
Codex launcher. Ensure ChatGPT or Codex is installed in `/Applications`, or set
`COMPUTER_USE_CODEX_LAUNCHER_PATH`.

### Computer Use client is missing

Enable or reinstall OpenAI Computer Use first, then verify that its client
exists below `$CODEX_HOME/computer-use`.

### Client and server version mismatch

Quit and relaunch ChatGPT so its Computer Use client and runtime update
together, then retry the smoke test.

### `This application session has been explicitly stopped by the user`

Someone pressed Esc on the Computer Use overlay, which cancels the app
session for the current turn. The bridge recycles the client automatically,
so simply ask Claude to continue when you are ready.

### ChatGPT still lists the app under Computer Use

ChatGPT's Computer Use menu can keep showing an app (with a "Stop Using …"
action) after the bridge has released the client. The service keeps its app
session record so that a follow-up turn can resume without a new approval,
and only Codex's own turn-tracking closes it. External clients have no
supported way to send that signal. The record is bookkeeping: the controlling
client process is gone and new bridge sessions are unaffected. Clear it with
the "Stop Using …" action in ChatGPT, or by quitting ChatGPT.

### `SkyComputerUseClient computer-history` processes linger

These are ChatGPT's own history/recording helpers, spawned by its
`codex app-server` daemon whenever Computer Use is used and kept around
afterwards. They are idle, they do not hold control of any application, and
they are not managed by this bridge. The client the bridge manages runs with
a plain `mcp` argument and exits on idle release. The helpers exit when
ChatGPT quits.

### `errAETimeout: the AppleEvent timed out`

The Computer Use service could not reach the target application in time. The
call can block for a few minutes. Retry once; if it persists, quit and
relaunch the target application, and as a last resort quit and relaunch
ChatGPT so its Computer Use service restarts.

### Plugin changes do not appear

Restart Claude Code or run `/plugin marketplace update songkeys` and
reinstall. Claude Code runs a cached copy of the installed plugin, so editing
a checkout does not affect an existing installation until the plugin is
updated.

## License and trademarks

The bridge code is available under the [MIT License](./LICENSE).

This project is independent and is not affiliated with, endorsed by, or
sponsored by OpenAI or Anthropic. OpenAI, ChatGPT, Codex, Anthropic, Claude,
and related names may be trademarks of their respective owners. Users must
supply and be licensed to use their own OpenAI and Anthropic software and
accounts.

## Prior art

This project mirrors
[kimi-computer-use](https://github.com/songkeys/kimi-computer-use), the same
bridge for Kimi Code CLI.
