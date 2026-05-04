# DSL Specification

Complete DSL for building Leviathan entities: skills, commands, and packages.

## Skills DSL

### Frontmatter Schema

```yaml
---
name: skill-name              # kebab-case, matches directory name
description: >                # When to use (triggers, scenarios)
  Triggers on "X", "Y", "Z". Use when...
version: 1.0.0                # Semantic version
dependencies:                 # Optional external requirements
  - python>=3.10
  - git>=2.30
replaces:                     # Optional: commands this skill supersedes
  - old-command
---
```

### Structure Rules

```
skill-name/
├── SKILL.md            # REQUIRED: 100-150 lines max
│   ├── Frontmatter     # name, description, version
│   ├── Decision tree   # Quick routing logic
│   ├── Quick reference # Cheat sheet
│   └── Reference links # Pointers to references/
├── references/         # Heavy documentation
│   ├── api.md
│   ├── patterns.md
│   └── troubleshooting.md
├── scripts/            # Optional automation
│   └── install.sh
└── assets/             # Optional resources
    └── templates/
```

### Validation Rules

| Rule | Threshold | Action |
|------|-----------|--------|
| SKILL.md > 150 lines | Move content to references/ |
| Single file > 500 lines | Consider splitting |
| Total skill > 2000 lines | Consider sub-skills |
| No references/ with heavy SKILL.md | Create references/, split |

### Progressive Disclosure Pattern

Keep in SKILL.md:
- Frontmatter
- Decision tree / quick router
- Cheat sheet / quick reference
- Pointers to references/

Move to references/:
- API details
- Extended examples
- Edge cases
- Troubleshooting

## Commands DSL

### Registration Pattern

Commands register in `core/{package}/config.yaml` under `poly.sdk`:

```yaml
# core/memory/config.yaml
poly:
  sdk:
    remember:
      handler: src/commands/remember.ts
      description: 'Store information in memory'
      aliases: [mem, r]                    # Optional shortcuts
      args:
        - name: key
          type: string
          required: true
          description: 'Memory key'
        - name: value
          type: string
          required: true
          description: 'Value to store'
        - name: ttl
          type: number
          required: false
          default: 0
          description: 'Time to live (0 = permanent)'
      lifecycle:                           # Optional hooks
        before: [validate-auth]
        after: [emit-event]
      whisper: |                           # Optional agent guidance
        Use this command to persist information across sessions.
```

### Argument Types

| Type | Description | Example |
|------|-------------|---------|
| string | Text value | `--name "my-skill"` |
| number | Numeric value | `--ttl 3600` |
| boolean | Flag | `--force` |
| array | Multiple values | `--tags tag1,tag2` |
| object | JSON structure | `--config '{"key": "val"}'` |

### Argument Options

```yaml
args:
  - name: platform
    type: string
    required: false
    enum: [claude-code, cursor, aider]    # Allowed values
    default: claude-code
    description: 'Target platform'
```

### Handler Structure

```typescript
// core/memory/src/commands/remember.ts
import type { CommandContext } from '@lev-os/poly-sdk';

export interface RememberArgs {
  key: string;
  value: string;
  ttl?: number;
}

export async function remember(
  args: RememberArgs,
  ctx: CommandContext
): Promise<void> {
  // Implementation
  const { key, value, ttl = 0 } = args;
  await ctx.memory.set(key, value, { ttl });
  ctx.log.info(`Stored ${key}`);
}

// MCP tool export (optional)
export const rememberTool = {
  name: 'memory_remember',
  description: 'Store information in memory',
  inputSchema: {
    type: 'object',
    properties: {
      key: { type: 'string' },
      value: { type: 'string' },
      ttl: { type: 'number', default: 0 }
    },
    required: ['key', 'value']
  }
};
```

### Command Location Guidelines

| Domain | Package | Example Commands |
|--------|---------|------------------|
| Search/RAG | core/index | lev get, lev rag |
| Memory | core/memory | lev remember, lev forget |
| Disclosure | core/disclosure | lev promote, lev whisper |
| Build/Poly | core/polyglot-runners | lev build, lev daemon |
| Triggers | core/triggers | lev trigger |
| Lifecycle | core/lifecycle | lev intake, lev crystallize |

## Packages DSL

### config.yaml Schema

```yaml
# core/my-pkg/config.yaml
package:
  name: my-pkg                    # kebab-case
  version: 0.1.0                  # Semantic version
  type: core_package              # Always core_package
  namespace: mypkg                # For MCP tools, isolation
  description: 'What this package does (min 10 chars)'

integration:
  agent_coupling: loose           # loose | tight
  core_initializer: optional      # optional | required
  tool_exposure: selective        # selective | full | none
  universal_context: false        # Boolean
  adapters: [cli]                 # mcp | cli | http | grpc

architecture:
  layers:
    - layer_one
    - layer_two
  backends:
    - backend_one
  capabilities:
    - capability_one

core_hooks:                       # Which lifecycle hooks to use
  - initialization
  - mcp_registration

namespace:
  prefix: 'mypkg:'               # Must end with :
  isolation: shared              # agent | session | shared
  permissions:
    - 'read:shared:data'
    - 'write:shared:data'

# Command registration (see Commands DSL above)
poly:
  sdk:
    my-command:
      handler: src/commands/my-command.ts
      description: 'Description'
```

### Directory Structure

```
core/my-pkg/
├── config.yaml           # REQUIRED: Package manifest
├── package.json          # Node package definition
├── tsconfig.json         # TypeScript config
├── src/
│   ├── index.ts          # Main exports
│   ├── commands/         # CLI handlers
│   │   └── my-command.ts
│   └── lib/              # Shared utilities
│       └── helpers.ts
├── tests/
│   ├── my-command.test.ts
│   └── fixtures/
└── README.md             # Package documentation
```

### package.json Template

```json
{
  "name": "@lev-os/my-pkg",
  "version": "0.1.0",
  "type": "module",
  "main": "./src/index.ts",
  "exports": {
    ".": "./src/index.ts",
    "./commands/*": "./src/commands/*.ts"
  },
  "scripts": {
    "build": "tsc",
    "test": "vitest run",
    "lint": "eslint src/"
  },
  "dependencies": {},
  "devDependencies": {
    "typescript": "^5.0.0",
    "vitest": "^1.0.0"
  }
}
```

## Fractal Pattern

Each core package "owns" its domain and declares commands:

```
core/
├── index/config.yaml        # Declares: lev rag, lev get
├── memory/config.yaml       # Declares: lev remember
├── polyglot-runners/config.yaml  # Declares: lev install, lev daemon
└── triggers/config.yaml     # Declares: lev trigger
```

The poly registry builder scans all `config.yaml` files and auto-generates CLI entries.

## Module Composition (Expose Pattern)

Some modules expose surfaces that others contribute to:

```yaml
# core/config/config.yaml (exposes 'config' surface)
package:
  name: config
  expose:
    surface: config
    schema:
      persist_keys:
        type: array
        default: []

# core/memory/config.yaml (contributes)
config:
  persist_keys: [episodic, semantic]
```

Build-time aggregation auto-namespaces by module path.

## Examples

### Minimal Skill

```yaml
---
name: hello-world
description: Example skill that demonstrates basic structure.
version: 1.0.0
---

# Hello World

## Usage

Say "hello world" to trigger this skill.

## Response

Respond with "Hello, World!"
```

### Minimal Command

```yaml
# core/example/config.yaml
poly:
  sdk:
    hello:
      handler: src/commands/hello.ts
      description: 'Print hello world'
```

```typescript
// core/example/src/commands/hello.ts
export async function hello(): Promise<void> {
  console.log('Hello, World!');
}
```

### Minimal Package

```yaml
# core/example/config.yaml
package:
  name: example
  version: 0.1.0
  type: core_package
  namespace: example
  description: 'Example package demonstrating minimal structure'

integration:
  agent_coupling: loose
  core_initializer: optional
  tool_exposure: none
  universal_context: false
  adapters: [cli]
```
