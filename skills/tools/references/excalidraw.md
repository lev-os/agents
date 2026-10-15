# Excalidraw diagrams through mcporter

Use the hosted Excalidraw+ Streamable HTTP MCP through the installed `mcporter`
CLI. Install no Excalidraw MCP server. The API is public beta, so live discovery
is the source of truth for tool names, schemas, and permissions.

## Connect

1. Check the CLI and credential without printing the credential:

   ```zsh
   command -v mcporter
   test -n "${EXCLAIDRAW_API_KEY:-}"
   ```

   The exact variable name is `EXCLAIDRAW_API_KEY`. Stop if either check fails.

2. Inspect the existing entry:

   ```zsh
   mcporter config get excalidraw --json
   ```

   If it is absent and connection setup is in scope, add the hosted endpoint.
   Single quotes keep the secret out of the config:

   ```zsh
   mcporter config add excalidraw https://api.excalidraw.com/api/v1/mcp \
     --scope home \
     --header 'Authorization=Bearer ${EXCLAIDRAW_API_KEY}' \
     --description 'Hosted Excalidraw+ MCP for editable diagrams'
   ```

   Stop instead of replacing a different endpoint or auth setup. The saved
   value must remain the environment placeholder, never the resolved key.

3. Discover the tools allowed by the current key:

   ```zsh
   mcporter list excalidraw --schema
   ```

   Missing tools usually mean missing API-key permissions. Treat that as an
   authorization blocker, not a reason to install another server.

## Create or edit a diagram

1. Load the live diagram contract before the first diagram write in each
   session:

   ```zsh
   mcporter call excalidraw.read_diagram_format --output json
   ```

2. Select an existing scene or create one only when the requested work permits
   a remote write. Use the schemas returned by `mcporter list`; do not guess
   arguments.

3. Use `create_diagram` for semantic node-and-edge diagrams. Use `DOWN` for
   workflows and flowcharts, and `RIGHT` for architecture maps and pipelines.
   Pass structured arguments with `--args`:

   ```zsh
   mcporter call excalidraw.create_diagram --args '<JSON matching the live schema>'
   ```

4. For an existing scene, use `search_scene_content` for targeted reads. Use
   `edit_scene_content` for follow-up changes or custom layouts. Keep writes to
   the named scene and requested elements.

5. After a substantial write, call `take_screenshot` and inspect the image for
   clipped text, overlap, broken bindings, unclear flow, and unreadable arrows.
   Confirm the returned scene or element IDs. A successful call without visual
   inspection is not diagram verification.

Stop with the last successful call and missing proof when the key is absent,
authentication fails, permissions hide a required tool, the format guide fails,
a write returns no provider ID, or the screenshot cannot confirm the result.
