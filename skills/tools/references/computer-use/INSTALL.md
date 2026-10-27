# Local installation

Agents use `scripts/cu.mjs` (SKILL.md). Its default engine, Codex's `cua_repl`,
needs only the ChatGPT app with Computer Use turned on; nothing else to
install. The sections below set up open-computer-use (the fallback engine,
`CU_ENGINE=ocu`) and the songkeys package.

## Contents

- [open-computer-use (fallback engine)](#open-computer-use-fallback-engine)
- [songkeys MCP package (optional)](#songkeys-mcp-package-optional)
- [Remove](#remove)

## open-computer-use (fallback engine)

| Need | Check |
|---|---|
| macOS 14.0 or later | `sw_vers -productVersion` |
| Node.js 18 or later on `PATH` | `node --version`. With nvm, the CLI lives in that Node version's global folder; switching the default Node version hides it until you install it again |
| The CLI | `open-computer-use --version` (1.1.2 tested 2026-10-20) |

Install, then grant permissions:

```sh
npm i -g open-computer-use        # no dependencies; postinstall only prints help
open-computer-use doctor          # opens onboarding when a permission is missing
open-computer-use doctor --json   # must show "allGranted":true
```

The user grants **Accessibility** and **Screen Recording** to "Open Computer
Use" in System Settings, Privacy & Security. The permission app is notarized
with a fixed Developer ID (`com.ifuryst.opencomputeruse`, team J9P29FA5BX), so
the grants stay across updates. It has no Dock icon and adds no login item.
Do not run `ocu locked-use enable`.

Verify (Calculator 12 × 12; tested from a T3 Code agent shell, 2026-10-20):

```sh
open -g -a Calculator
open-computer-use call get_app_state --args '{"app":"Calculator"}'
# click All Clear, 1, 2, Multiply, 1, 2, Equals by element_index in one --calls run,
# then read state: the input view text must be 144
```

The CLI needs no registration. MCP registration is optional; it gives the model
tools and inline screenshots: `claude mcp add --scope user --transport stdio
open-computer-use -- open-computer-use mcp`. Ask the user first: a user-scope
server starts with every Claude session.

## songkeys MCP package (optional)

The `upstream/` folder holds songkeys/claude-codex-computer-use unchanged
(`UPSTREAM.md`). It runs OpenAI's own client from the user's ChatGPT or Codex
app. It needs:

| Need | Check |
|---|---|
| Node.js 22.14.0 or later | `node --version` |
| ChatGPT or Codex app with Computer Use turned on | The signed launcher at `/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex` or `/Applications/Codex.app/Contents/Resources/codex`, or `COMPUTER_USE_CODEX_LAUNCHER_PATH` |
| The Computer Use client | `test -x "${CODEX_HOME:-$HOME/.codex}/computer-use/Codex Computer Use.app/Contents/SharedSupport/SkyComputerUseClient.app/Contents/MacOS/SkyComputerUseClient"` |
| A host app that may send Apple Events | See below |

### The host app must declare `NSAppleEventsUsageDescription`

macOS charges the client's Apple Events to the app that started the agent (the
responsible app). An app without `NSAppleEventsUsageDescription` in its
`Info.plist` is refused with no prompt. Every call then returns
`bootstrapTimedOut`, and the system log shows `errAEEventNotPermitted`. A TCC
reset does not help.

Check a host:

```sh
/usr/libexec/PlistBuddy -c "Print :NSAppleEventsUsageDescription" "/Applications/<App>.app/Contents/Info.plist"
```

Checked 2026-10-20: iTerm, Ghostty, Warp, ChatGPT and Claude declare it. T3 Code
(Beta) and Terminal do not (Terminal is Apple's own app; untested). T3 Lev adds
it in its build (`leviathan/apps/lev/t3-lev/build.yaml`, step "make it its own
app").

Register it only from a host that declares the string, and only when the user
asks:

```sh
CU_LEAF_ROOT="$HOME/.agents/skills/tools/references/computer-use"
claude mcp add --scope user --transport stdio computer-use -- node "$CU_LEAF_ROOT/upstream/bin/computer-use-mcp-bridge.mjs"
```

Its startup code accepts every app-access request on its own and runs the client
with an unrestricted profile. That acceptance does not authorize a new task,
private-data access or a change other people can see.

Offline check, with no real app access:

```sh
cd "$CU_LEAF_ROOT" && shasum -a 256 -c UPSTREAM.sha256 && node --test upstream/test/bridge.test.mjs
```

Real check: `node "$CU_LEAF_ROOT/upstream/scripts/real-smoke-test.mjs"` (lists
apps, reads Calculator). For other failures, read `upstream/README.md`.

## Remove

- open-computer-use: `npm rm -g open-computer-use`. Remove its MCP entry if you
  added one (`claude mcp remove --scope user open-computer-use`). The macOS
  grants stay in System Settings until the user removes them.
- Codex engine: `claude mcp remove --scope user computer-use`. Keep the user's
  ChatGPT or Codex app as it is.
