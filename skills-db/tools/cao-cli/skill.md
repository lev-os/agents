# Amazon Q Developer CLI (CAO) Skill

## Overview

Amazon Q Developer CLI (formerly CAO - Claude Agent Orchestrator) is an AI assistant CLI from AWS Labs. Note: Repository is no longer actively maintained - moved to closed-source Kiro CLI.

## When to Use

- Running Q Developer CLI as an agent backend
- Understanding agent configuration patterns
- MCP (Model Context Protocol) integration
- Hook-based tool execution

## CLI Command Reference

### Root Commands

```bash
q                              # Start interactive chat
q chat                         # AI assistant in terminal
q agent                        # Manage agents
q login                        # Log in to Amazon Q
q logout                       # Log out
q whoami                       # Current session info
q profile                      # Show profile
q settings                     # Customize appearance
q diagnostic                   # Run diagnostic tests
q mcp                          # Model Context Protocol
q version                      # Version info
```

### Chat Options

```bash
q                              # Interactive mode (default)
q --resume                     # Resume previous session
q --agent <name>               # Select agent profile
q --model <model>              # Override model selection
q --trust-all-tools            # Auto-approve all tools
q --trust-tools <tools>        # Selectively approve tools
q --no-interactive             # Non-interactive mode
q --wrap <mode>                # Text wrapping (never/auto/always)
q "message"                    # Direct message input
```

### Agent Management

```bash
q agent --list                 # List all agents
q agent --create               # Create new agent
```

## Agent Configuration Schema

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "agent_name",
  "description": "Agent description",
  "prompt": "System prompt",
  "mcpServers": {
    "server_name": { "command": "cmd", "args": [] }
  },
  "tools": ["*", "@git", "@fetch"],
  "toolAliases": { "@gits/some_tool": "aliased_name" },
  "allowedTools": ["fs_read", "use_aws"],
  "toolsSettings": {
    "fs_write": { "allowedPaths": ["~/**"] }
  },
  "resources": ["file://~/path/to/file.md"],
  "hooks": {
    "agentSpawn": [{ "command": "setup.sh" }],
    "preToolUse": [{ "matcher": "fs_write", "command": "validate.sh" }],
    "postToolUse": [{ "command": "process.sh" }]
  },
  "model": "claude-sonnet-4"
}
```

## Hook System

### Hook Triggers

| Trigger | When |
|---------|------|
| `agentSpawn` | During agent spawn |
| `userPromptSubmit` | Before sending user prompt |
| `preToolUse` | Before tool execution |
| `postToolUse` | After tool execution |

### Hook Configuration

```json
{
  "trigger": "preToolUse",
  "command": "validate.sh",
  "matcher": "fs_write",
  "timeout_ms": 5000,
  "max_output_size": 10240,
  "cache_ttl_seconds": 60
}
```

## MCP Integration

### Tool Reference Patterns

- `"@builtin"` - All built-in tools
- `"@mcp_server_name/tool_name"` - Specific MCP tool
- `"@mcp_server_name"` - All tools from server (wildcard)
- `"*"` - All available tools

### MCP Server Config

```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "."]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-fetch"]
    }
  }
}
```

## Built-in Tools

| Tool | Purpose |
|------|---------|
| `fs_read` | File system read access |
| `fs_write` | File system write access |
| `execute` | Command execution |
| `gh_issue` | GitHub integration |
| `delegate` | Subagent spawning |
| `todo` | Task tracking |
| `use_aws` | AWS CLI integration |
| `knowledge` | Knowledge base queries |
| `thinking` | Thought process display |

## Session Management

### Persistence

- File-based `ConversationState`
- SQLite database for settings
- Checkpoint system for resume
- Auto-compaction for context window

### Resume Session

```bash
q --resume                     # Resume last session
```

## Permission System

| Result | Behavior |
|--------|----------|
| `Allow` | Tool runs without confirmation |
| `Ask` | Requires user approval |
| `Deny` | Blocked with reasons |

## Architecture Patterns

### Agent Lifecycle

1. `Agent::new()` creates agent instance
2. `spawn()` creates background tokio task
3. `TaskExecutor` runs tools in parallel
4. `ConversationState` tracks history
5. `CheckpointManager` persists state

### State Machine

- `Idle` - Waiting for input
- `ExecutingRequest` - Processing request
- `WaitingForApproval` - Tool approval needed
- `ExecutingTools` - Running tools
- `ExecutingHooks` - Running hooks
- `Errored` - Error state

## Key Differences from Other CLIs

- No tmux session isolation (single-process)
- In-memory state with file persistence
- Native MCP integration
- Hook-based extensibility
- Subagent spawning via delegate tool

## Source

Repository: https://github.com/aws/amazon-q-developer-cli
Note: Moved to closed-source Kiro CLI (https://kiro.dev/cli/)
