# AgentPing CLI Specification

## Design Philosophy

The AgentPing CLI is designed for AI agents first, humans second. Every command:
1. Accepts JSON via stdin or `--json` flag
2. Outputs structured JSON on stdout
3. Uses predictable exit codes
4. Provides clear error messages

## Command Structure

```
agentping <command> [subcommand] [options]
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (approved, answered, selected) |
| 1 | Rejected (denied, dismissed) |
| 2 | Timeout (no response in time) |
| 3 | Error (network, validation, system) |

---

## Core Commands

### `agentping approve <action>`

Request yes/no approval for an action.

**Arguments:**
- `<action>` - Description of the action requiring approval

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--title <title>` | string | - | Custom title (defaults to action) |
| `--details <text>` | string | - | Additional context |
| `--risk <level>` | enum | - | Risk level: low, medium, high |
| `-t, --timeout <seconds>` | number | 300 | Timeout in seconds |
| `--json` | boolean | false | Output JSON |
| `--quiet` | boolean | false | Only output approved/denied |
| `--agent <id>` | string | cli-agent | Agent identifier |
| `--agent-name <name>` | string | CLI Agent | Human-readable agent name |
| `--session <id>` | string | cli-session | Session identifier |
| `--stdin` | boolean | false | Read payload from stdin |

**Input JSON (stdin):**
```json
{
  "title": "Deploy to production?",
  "action": "deploy-v2.3.1",
  "details": "Includes database migration",
  "risk": "high"
}
```

**Output JSON:**
```json
{
  "approved": true,
  "action": "approved",
  "data": {
    "type": "approval",
    "approved": true
  },
  "enrichment": {
    "directives": [],
    "notes": "optional human notes"
  },
  "respondedAt": "2024-01-15T10:30:00Z",
  "respondedVia": "web-ui"
}
```

**Exit Codes:**
- `0` - Approved
- `1` - Denied
- `2` - Timeout
- `3` - Error

---

### `agentping ask <question>`

Ask a freeform question.

**Arguments:**
- `<question>` - The question to ask

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-o, --options <list>` | string | - | Comma-separated suggested options |
| `--context <text>` | string | - | Additional context |
| `-t, --timeout <seconds>` | number | 300 | Timeout in seconds |
| `--json` | boolean | false | Output JSON |
| `--quiet` | boolean | false | Only output the answer |
| `--agent <id>` | string | cli-agent | Agent identifier |
| `--agent-name <name>` | string | CLI Agent | Human-readable agent name |
| `--session <id>` | string | cli-session | Session identifier |
| `--stdin` | boolean | false | Read payload from stdin |

**Input JSON (stdin):**
```json
{
  "question": "What should I focus on next?",
  "context": "Currently working on auth module",
  "options": ["security", "performance", "documentation"]
}
```

**Output JSON:**
```json
{
  "action": "answered",
  "data": {
    "type": "answer",
    "value": "focus on security first"
  },
  "enrichment": {
    "directives": [
      {"type": "prioritize", "items": ["security", "performance"]}
    ],
    "notes": "We have a security audit next week"
  },
  "respondedAt": "2024-01-15T10:30:00Z",
  "respondedVia": "web-ui"
}
```

---

### `agentping select`

Present options for selection.

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--title <title>` | string | required | Selection title |
| `--options <list>` | string | - | Comma-separated options (simple mode) |
| `-f, --file <path>` | string | - | JSON file with detailed options |
| `--multiple` | boolean | false | Allow multiple selections |
| `--custom` | boolean | false | Allow custom input |
| `--min <n>` | number | - | Minimum selections required |
| `--max <n>` | number | - | Maximum selections allowed |
| `-t, --timeout <seconds>` | number | 300 | Timeout in seconds |
| `--json` | boolean | false | Output JSON |
| `--agent <id>` | string | cli-agent | Agent identifier |
| `--session <id>` | string | cli-session | Session identifier |
| `--stdin` | boolean | false | Read payload from stdin |

**Input JSON (stdin):**
```json
{
  "title": "Choose deployment targets",
  "context": "Select environments to deploy to",
  "options": [
    {"id": "dev", "label": "Development", "description": "Dev environment"},
    {"id": "staging", "label": "Staging", "description": "Pre-prod"},
    {"id": "prod", "label": "Production", "description": "Live", "metadata": {"risk": "high"}}
  ],
  "allowMultiple": true,
  "allowCustom": false,
  "minSelections": 1,
  "maxSelections": 2
}
```

**Output JSON:**
```json
{
  "action": "selected",
  "data": {
    "type": "selection",
    "selectedIds": ["dev", "staging"],
    "customValue": null
  },
  "enrichment": {
    "directives": [],
    "notes": "start with non-prod first"
  },
  "respondedAt": "2024-01-15T10:30:00Z",
  "respondedVia": "web-ui"
}
```

---

### `agentping approve-steps`

Request approval for multiple steps.

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-f, --file <path>` | string | required | JSON file with steps |
| `--partial` | boolean | true | Allow partial approval |
| `-t, --timeout <seconds>` | number | 300 | Timeout in seconds |
| `--json` | boolean | false | Output JSON |
| `--agent <id>` | string | cli-agent | Agent identifier |
| `--session <id>` | string | cli-session | Session identifier |
| `--stdin` | boolean | false | Read payload from stdin |

**Input JSON (stdin/file):**
```json
{
  "title": "Database Migration Plan",
  "context": "Migrating user table schema",
  "steps": [
    {
      "id": "backup",
      "description": "Create database backup",
      "risk": "low",
      "reversible": true,
      "details": "Full pg_dump to S3",
      "estimatedImpact": "2 minutes downtime"
    },
    {
      "id": "migrate",
      "description": "Run ALTER TABLE migrations",
      "risk": "medium",
      "reversible": true,
      "details": "Add new columns, create indexes"
    },
    {
      "id": "backfill",
      "description": "Backfill computed columns",
      "risk": "low",
      "reversible": true
    }
  ],
  "allowPartial": true,
  "defaultApproved": ["backup"]
}
```

**Output JSON:**
```json
{
  "action": "selected",
  "data": {
    "type": "step_approval",
    "approvedSteps": ["backup", "migrate"],
    "deniedSteps": ["backfill"]
  },
  "enrichment": {
    "directives": [
      {"type": "constraint", "rule": "run during maintenance window"},
      {"type": "skip", "target": "backfill", "reason": "defer to next sprint"}
    ],
    "notes": "Approved with modifications"
  },
  "respondedAt": "2024-01-15T10:30:00Z",
  "respondedVia": "web-ui"
}
```

---

### `agentping notify <message>`

Send a notification (no response expected).

**Arguments:**
- `<message>` - Notification message

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-l, --level <level>` | enum | info | Level: info, success, warning, error |
| `--agent <id>` | string | cli-agent | Agent identifier |
| `--agent-name <name>` | string | CLI Agent | Human-readable agent name |
| `--session <id>` | string | cli-session | Session identifier |

**Output:**
No output on success (fire-and-forget).

**Exit Codes:**
- `0` - Notification sent
- `3` - Error

---

### `agentping research`

Request research direction from human.

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--title <title>` | string | required | Research topic title |
| `--findings <text>` | string | - | Current findings summary |
| `-f, --file <path>` | string | - | JSON file with directions |
| `--custom` | boolean | true | Allow custom direction |
| `-t, --timeout <seconds>` | number | 300 | Timeout in seconds |
| `--json` | boolean | false | Output JSON |
| `--stdin` | boolean | false | Read payload from stdin |

**Input JSON (stdin):**
```json
{
  "title": "API Design Research",
  "currentFindings": "Found 3 viable patterns: REST, GraphQL, gRPC",
  "proposedDirections": [
    {"id": "rest", "direction": "REST API", "rationale": "Simplest, well-understood", "estimatedEffort": "quick"},
    {"id": "graphql", "direction": "GraphQL", "rationale": "Flexible queries", "estimatedEffort": "medium"},
    {"id": "grpc", "direction": "gRPC", "rationale": "High performance", "estimatedEffort": "deep"}
  ],
  "allowCustomDirection": true
}
```

**Output JSON:**
```json
{
  "action": "selected",
  "data": {
    "type": "selection",
    "selectedIds": ["rest", "graphql"]
  },
  "enrichment": {
    "directives": [
      {"type": "focus_on", "target": "developer experience"},
      {"type": "deep_research", "topic": "pagination patterns"}
    ]
  }
}
```

---

### `agentping review`

Request review of content.

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--title <title>` | string | required | Review title |
| `--content <text>` | string | - | Content to review |
| `-f, --file <path>` | string | - | File containing content |
| `--type <type>` | enum | text | Content type: code, text, markdown, json |
| `-t, --timeout <seconds>` | number | 300 | Timeout in seconds |
| `--json` | boolean | false | Output JSON |
| `--stdin` | boolean | false | Read payload from stdin |

---

### `agentping validate`

Validate a ping payload without sending.

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-f, --file <path>` | string | - | JSON file to validate |
| `--type <pingType>` | enum | - | Expected ping type |
| `--stdin` | boolean | false | Read from stdin |

**Output JSON:**
```json
{
  "valid": true,
  "type": "step_approval",
  "warnings": [],
  "errors": []
}
```

Or on error:
```json
{
  "valid": false,
  "errors": [
    {"path": "steps[0].risk", "message": "must be one of: low, medium, high"}
  ]
}
```

---

### `agentping render`

Render a ping for a specific surface (for adapter development).

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--surface <name>` | string | required | Target surface: cli, telegram, slack, web |
| `-f, --file <path>` | string | - | Ping JSON file |
| `--json` | boolean | false | Output JSON |
| `--stdin` | boolean | false | Read from stdin |

**Output JSON:**
```json
{
  "surface": "telegram",
  "rendered": {
    "text": "Deploy to production?",
    "reply_markup": {
      "inline_keyboard": [
        [{"text": "Approve", "callback_data": "approve"}],
        [{"text": "Deny", "callback_data": "deny"}]
      ]
    }
  },
  "fallback": {
    "text": "Deploy to production?",
    "options": ["Approve", "Deny"]
  }
}
```

---

## Adapter Commands

### `agentping adapter create`

Generate a new adapter scaffold.

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--name <name>` | string | required | Adapter name |
| `--template <name>` | string | default | Template: default, telegram, slack |
| `--output <dir>` | string | ./adapters | Output directory |

**Generated Structure:**
```
adapters/<name>/
+-- parser.ts       # Message -> PingSpec
+-- renderer.ts     # Response -> Native format
+-- config.yaml     # Platform settings
+-- index.ts        # Barrel export
+-- types.ts        # Platform-specific types
+-- README.md       # Adapter documentation
```

**parser.ts template:**
```typescript
import type { Ping, ParsedInteraction, QuickAction } from '@agentping/core';
import type { IInteractionParser } from '@agentping/core';

export const myplatformParser: IInteractionParser = {
  name: 'myplatform',
  priority: 50,

  canParse(ping: Ping): boolean {
    // Return true if this parser handles this ping type
    return ping.payload.type === 'approval';
  },

  parse(ping: Ping): ParsedInteraction {
    // Transform ping into platform-specific UI hints
    return {
      interactionType: 'approval',
      quickActions: [
        { id: 'approve', label: 'Approve', style: 'primary', action: { type: 'approve_all' } },
        { id: 'deny', label: 'Deny', style: 'danger', action: { type: 'deny_all' } },
      ],
      uiHints: {},
      fallbackText: ping.payload.title || 'Approval required',
      fallbackOptions: ['Approve', 'Deny'],
    };
  },
};
```

**renderer.ts template:**
```typescript
import type { Ping, ParsedInteraction, HumanResponse } from '@agentping/core';

export interface PlatformMessage {
  // Platform-specific message format
}

export function renderPing(ping: Ping, interaction: ParsedInteraction): PlatformMessage {
  // Convert ping to platform-native format
  return {
    // Platform-specific fields
  };
}

export function parseResponse(platformResponse: unknown): Partial<HumanResponse> {
  // Convert platform response to AgentPing format
  return {
    action: 'approved',
    data: { type: 'approval', approved: true },
  };
}
```

**config.yaml template:**
```yaml
name: myplatform
version: 1.0.0

# Platform connection settings
connection:
  type: webhook  # webhook | websocket | polling
  endpoint: ${MYPLATFORM_WEBHOOK_URL}

# Feature flags
features:
  inlineResponse: true
  richText: true
  buttons: true
  attachments: false

# Ping type support
supportedTypes:
  - notification
  - question
  - approval
  - selection

# Rate limits
rateLimit:
  requests: 30
  window: 60  # seconds
```

### `agentping adapter list`

List available adapters.

**Output JSON:**
```json
{
  "adapters": [
    {"name": "cli", "builtin": true, "status": "active"},
    {"name": "web-ui", "builtin": true, "status": "active"},
    {"name": "slack", "builtin": true, "status": "inactive"},
    {"name": "myplatform", "builtin": false, "status": "active"}
  ]
}
```

### `agentping adapter test`

Test an adapter with sample pings.

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--name <name>` | string | required | Adapter to test |
| `--type <pingType>` | enum | - | Specific ping type to test |
| `--verbose` | boolean | false | Show detailed output |

---

## Daemon Commands

### `agentping daemon start`

Start the AgentPing daemon.

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-p, --port <port>` | number | 7890 | Port to listen on |
| `--foreground` | boolean | false | Run in foreground |

### `agentping daemon stop`

Stop the running daemon.

### `agentping daemon status`

Check daemon status.

**Output JSON:**
```json
{
  "running": true,
  "pid": 12345,
  "port": 7890,
  "uptime": 3600,
  "pendingPings": 3,
  "adapters": ["cli", "web-ui"]
}
```

### `agentping daemon restart`

Restart the daemon.

**Options:**
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-p, --port <port>` | number | 7890 | Port to listen on |

---

## Global Options

Available on all commands:

| Flag | Description |
|------|-------------|
| `-h, --help` | Show help |
| `-V, --version` | Show version |
| `--json` | Output JSON format |
| `--quiet` | Minimal output |
| `--verbose` | Verbose output |
| `--config <path>` | Config file path |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENTPING_URL` | http://localhost:7890 | API endpoint |
| `AGENTPING_TIMEOUT` | 300 | Default timeout (seconds) |
| `AGENTPING_AGENT_ID` | cli-agent | Default agent ID |
| `AGENTPING_AGENT_NAME` | CLI Agent | Default agent name |
| `AGENTPING_SESSION_ID` | - | Default session ID |
| `AGENTPING_JSON` | false | Always output JSON |

---

## Error Response Format

All errors return JSON (when `--json` is used):

```json
{
  "error": true,
  "code": "VALIDATION_ERROR",
  "message": "Invalid payload: steps[0].risk must be low, medium, or high",
  "details": {
    "path": "steps[0].risk",
    "received": "critical",
    "expected": ["low", "medium", "high"]
  }
}
```

Error codes:
- `VALIDATION_ERROR` - Invalid input
- `TIMEOUT` - Response timeout
- `CONNECTION_ERROR` - Cannot reach daemon
- `NOT_FOUND` - Ping not found
- `INTERNAL_ERROR` - Server error

---

## Usage Examples

### Shell Script Integration

```bash
#!/bin/bash

# Request approval before destructive operation
if agentping approve "Delete old backups?" --json | jq -e '.approved' > /dev/null; then
  rm -rf /backups/old/*
  agentping notify --level success "Old backups deleted"
else
  agentping notify --level info "Deletion cancelled"
  exit 1
fi
```

### Multi-Step Workflow

```bash
#!/bin/bash

# Create steps file
cat > /tmp/deploy-steps.json << 'EOF'
{
  "title": "Production Deployment",
  "steps": [
    {"id": "test", "description": "Run test suite", "risk": "low", "reversible": true},
    {"id": "build", "description": "Build artifacts", "risk": "low", "reversible": true},
    {"id": "deploy", "description": "Deploy to prod", "risk": "high", "reversible": true}
  ]
}
EOF

# Get approvals
response=$(agentping approve-steps -f /tmp/deploy-steps.json --json)

# Execute approved steps
for step in $(echo $response | jq -r '.data.approvedSteps[]'); do
  case $step in
    test) npm test ;;
    build) npm run build ;;
    deploy) kubectl apply -f deploy.yaml ;;
  esac
done
```

### Piping JSON Input

```bash
# Generate ping dynamically
jq -n '{
  title: "Deploy \(env.VERSION)?",
  action: "deploy",
  risk: "high"
}' | agentping approve --stdin --json
```
