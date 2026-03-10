---
name: convex
description: Convex backend skill for CLI operations, MCP integration, Agent Component setup, deploy-key auth, and agent-safe development workflows.
aliases: [convex, convex-mcp, convex-agent, convex-cli]
triggers: [convex, convex key, convex deploy key, convex mcp, convex agent mode, convex cli]
skill_type: workflow
category: backend-platform
displayName: Convex
---

# Convex

Use this skill when building or operating Convex projects with coding agents.

This skill is optimized for:

- local development with `npx convex dev`
- cloud-agent development with `CONVEX_AGENT_MODE=anonymous`
- MCP server setup for Cursor/Claude Code/VS Code
- deploy-key based CI/CD (`CONVEX_DEPLOY_KEY`)
- Agent Component bootstrap (`@convex-dev/agent`)

## Routing

1. If user has no Convex account/key yet:
   - use anonymous agent mode:
   - `CONVEX_AGENT_MODE=anonymous npx convex dev`

2. If user is local and can log in interactively:
   - use normal dev flow:
   - `npx convex dev`

3. If workflow is CI/non-interactive:
   - require `CONVEX_DEPLOY_KEY`
   - use `npx convex deploy`

4. If user wants AI editor/tooling integration:
   - configure MCP server:
   - `npx -y convex@latest mcp start`

## Core Workflows

### A) Bootstrap Convex in a repo

```bash
npm install convex
npx convex dev
```

Expected outcomes:

- `convex/` directory created
- `.env.local` has `CONVEX_DEPLOYMENT`
- generated code updates in `convex/_generated`

### B) Agent-safe development (cloud coding agents)

```bash
CONVEX_AGENT_MODE=anonymous npx convex dev
```

Use this for Codex/Devin/Jules/Cursor Cloud style environments where interactive login is unavailable and you want isolated backend state.

### C) Configure Convex MCP server

Default command:

```bash
npx -y convex@latest mcp start
```

Common options:

```bash
# Single project only
npx -y convex@latest mcp start --project-dir /path/to/project

# Enable production access explicitly (dangerous)
npx -y convex@latest mcp start --dangerously-enable-production-deployments --prod

# Restrict high-risk tools
npx -y convex@latest mcp start --disable-tools data,run,envSet
```

Claude Code example:

```bash
claude mcp add-json convex '{"type":"stdio","command":"npx","args":["convex","mcp","start"]}'
claude mcp get convex
```

### D) Deploy key flow (CI/CD)

Set key and deploy:

```bash
export CONVEX_DEPLOY_KEY='...'
npx convex deploy
```

Supported key shapes (reference):

- production deploy key: `prod:...|...`
- preview deploy key: `preview:team:project|...`
- dev deploy key: `dev:...|...`

### E) Agent Component setup

Install and register:

```bash
npm install @convex-dev/agent
```

```ts
// convex/convex.config.ts
import { defineApp } from "convex/server";
import agent from "@convex-dev/agent/convex.config";

const app = defineApp();
app.use(agent);
export default app;
```

Then run:

```bash
npx convex dev
```

## CLI Cheat Sheet

```bash
npx convex
npx convex dev
npx convex dashboard
npx convex docs
npx convex run <functionName> '{"arg":"value"}'
npx convex logs
npx convex env list
npx convex env get <NAME>
npx convex env set <NAME> <VALUE>
npx convex env remove <NAME>
npx convex deploy
npx convex codegen
npx convex data
npx convex insights
```

## Security Rules

- Never print secret values from `CONVEX_DEPLOY_KEY` or env vars in logs.
- Do not enable production MCP access unless explicitly requested.
- Prefer disabling mutation-capable MCP tools when auditing or exploring data.

## Validation Checklist

- `npx convex dev` starts and syncs successfully
- `convex/_generated` exists and updates
- `npx convex env list` returns deployment env vars
- MCP server starts and responds in client tool
- CI deploy path works with `CONVEX_DEPLOY_KEY`

## References (Official)

- https://docs.convex.dev/cli
- https://docs.convex.dev/cli/agent-mode
- https://docs.convex.dev/cli/deploy-key-types
- https://docs.convex.dev/production/environment-variables
- https://docs.convex.dev/ai/convex-mcp-server
- https://docs.convex.dev/agents
- https://docs.convex.dev/agents/getting-started
