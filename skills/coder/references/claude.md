# Claude Code worker

Prefer the Lev Claude provider binding. For a direct fallback, use print mode
with `--output-format stream-json`, partial messages, and verbose events. Keep
project instructions, skills, plugins, hooks, MCP servers, and custom agents
enabled; a customization failure is a blocker to diagnose, not a reason to run
the mutation with less project context.

Preserve the full event stream and extract the terminal result only after exit.
Resume the explicit Claude session when supported. CAAM is authoritative for
the selected profile alias and bridges the macOS Claude Code keychain; validate
the profile before launch without printing credential contents.

For concurrent Claude identities, use an existing isolated or shallow CAAM
profile. Do not use global activation when another Claude process may share the
login keychain or auth files. If the access timestamp looks expired but CAAM
marks it refreshable, use the live CLI auth result as evidence and escalate only
on an actual validation or provider failure.

