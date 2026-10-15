---
name: computer-use
description: Control local macOS applications through the installed Computer Use MCP tools. Use for GUI work that is not better served by a dedicated API, connector, or CLI.
---

# Computer Use

This plugin exposes OpenAI's locally installed Computer Use service directly as
Claude Code MCP tools. Use the tools whose names begin with
`mcp__plugin_claude-codex-computer-use_computer-use__`.

The bridge automatically handles the service's app-access elicitation. Do not
ask the user to approve Computer Use access and do not attempt to manage the
OpenAI app's allowlist.

## Required observation and action loop

1. Start with `get_app_state` for the named application. Pass the app's display
   name or bundle identifier directly.
2. Read the returned accessibility text first. Use the accompanying screenshot
   when the accessibility tree is incomplete or visual context matters.
3. Prefer actions using the latest `element_index`. Use coordinates only when
   the target is unavailable or unreliable through accessibility.
4. Perform one or more tightly related actions.
5. Call `get_app_state` again before deciding the next action. Re-derive element
   indices from the latest state and never assume an old index is still valid.

The `get_app_state` result may be a diff from the preceding state. Request a
full state only when the earlier tree is unavailable or a diff is insufficient.

## Tools

- `list_apps`: discover apps only when the requested app cannot be identified
  from its name or bundle identifier.
- `get_app_state`: read accessibility state and capture a screenshot.
- `click`: click by `element_index`, or by coordinates as a fallback.
- `set_value`: replace the value of an editable accessibility element.
- `type_text`: type into the target app.
- `press_key`: send a key or key combination such as `Return`, `Tab`,
  `super+c`, or `Escape`.
- `scroll`: scroll an element or view.
- `drag`: drag between coordinates.
- `select_text`: select matching text or place the cursor around it.
- `perform_secondary_action`: invoke an accessibility action explicitly
  exposed by an element. Never guess the action name.

## App targeting

- No separate launch step is needed. `get_app_state` launches the app when
  necessary.
- Try the app name or known bundle identifier directly before calling
  `list_apps`.
- If targeting by display name fails, call `list_apps`, find the bundle
  identifier, and retry once with that identifier.
- `press_key` and `type_text` target the selected app; they are not global
  keyboard shortcuts.

## Recovery

If an action behaves unexpectedly, immediately fetch a fresh app state. If the
accessibility tree is sparse, inspect the screenshot and use coordinates. Keep
the loop observable: state, action, state.

If a tool result says the application session was explicitly stopped by the
user, the user pressed Esc on the Computer Use overlay. Stop the Computer Use
loop, tell the user, and continue only when they ask. The bridge recycles the
client automatically, so the next attempt starts a fresh session.
