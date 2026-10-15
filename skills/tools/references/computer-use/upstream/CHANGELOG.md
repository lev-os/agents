# Changelog

## 0.1.2 - 2026-08-18

- Restore `Escape` as a valid `press_key` example. Testing against the real
  service shows the overlay's Esc cancel only applies to the physical key;
  a synthetic Escape sent through `press_key` is delivered to the app
  normally and does not stop the session.

## 0.1.1 - 2026-08-18

- Recycle the Computer Use client when the service reports that the user
  stopped the app session, so the stop no longer latches across turns.
- Signal the launcher's whole process group on release so a wedged client
  cannot survive a recycle.
- Stop suggesting `Escape` in the Skill: Esc is the Computer Use overlay's
  global cancel hotkey. Clear UI through accessibility elements instead.
- Document the stopped-session and `errAETimeout` behaviors.

## 0.1.0 - 2026-08-18

- Add a Claude Code plugin with a Computer Use Skill and MCP server.
- Add a stdio MCP bridge that preserves OpenAI's trusted client ancestry.
- Add MCP elicitation capability injection and automatic app-access acceptance.
- Release the Computer Use client after an idle timeout and relaunch it on
  demand, so applications are not held while the session is inactive.
- Preserve accessibility text and screenshot image blocks.
- Add fake-server unit coverage and a real local Computer Use smoke test.
- Publish the bridge as the `claude-codex-computer-use` npm executable.
