# Add a tool to Tools

`tools --add-tool <repo|package|path>` and `tools --absorb <source>` are skill
selectors, not implemented shell commands. Both select this branch. Use
`--add-tool` for an independent integration leaf; use `--absorb` to learn into
an existing leaf through `skill://skill-builder --absorb`.

## Package the leaf

1. Read the existing Tools contents table and resolve the target leaf. Reuse
   an existing owner when the tool overlaps; create a new leaf when its runtime
   and operation require their own instructions. Done: one owner and one
   package path are identified.
2. Route external intake to `skill://skill-builder`. Clone the GitHub repo
   directly when the user requests a repo copy. Pin the revision, preserve
   source bytes, license, notice and required references, and complete that
   owner's security intake. Done: source inventory and audit results exist;
   unavailable or failed checks remain explicit.
3. Put the leaf under `references/<tool>/` with a `SKILL.md`. Bundle helper
   scripts, bridge/CLI entrypoints and redistributable binaries with their
   required files. Preserve an unchanged repo under `upstream/` when a
   one-to-one copy is requested. Keep downloaded runtime installs, caches,
   credentials and build output outside the skill. Done: entrypoints resolve
   within the leaf, and every host dependency is listed.
4. Write `INSTALL.md` or an inline installation section for every leaf. State
   the supported OS/architecture and versions, dependency checks, bundled
   versus host-installed tools, exact scoped install/configuration commands,
   credentials/permissions, verification and removal. For API-only leaves,
   explicitly state that no CLI is required and document the transport and
   credential setup. An unknown installer stays unknown; inspect the source
   or official help rather than inventing a package name. Done: a fresh host
   has a concrete setup path or a named blocking prerequisite.
5. Add one relative contents-table route and at least two or three useful
   search terms per tool to the Tools description. Keep operation details in
   the leaf. Preserve old caller paths during any separately authorized
   migration. Done: links resolve and existing routes remain reachable.
6. Verify source hashes, relative paths, bundled entrypoints and appropriate
   offline tests; record structural, behavioral and host integration results
   separately. Configure or launch a real MCP/connector only within the
   user's authorized setup/test scope. Done: the report identifies what was
   copied, what can run locally and what has actually run on the host.

## Ship with Lev

Tools is linked from `skill://lev`; its leaves travel with the skill package.
Keep them available to worker agents through the current skills inventory and
the package's relative references. Use `skill://<top-level-or-db-id>` for
guidance loading; see the [Lev loading contract](../../lev/references/tool-skills.md)
for exact selection, worker context and the included FlowMind declaration.

This route does not require a separate Lev plugin or marketplace. A tool's
bundled entrypoint or documented host runtime remains its own dependency.
Skill loading does not install binaries, connect MCP servers or grant provider
access. Only add runtime registration in its actual owner when the task calls
for that distinct behavior.
