# Claude Agent SDK - Complete API Reference

## Core Functions

### query()

Main entry point for agent interactions.

```python
async for message in query(
    prompt: str,
    options: ClaudeAgentOptions = None
) -> AsyncGenerator[Message, None]:
    ...
```

**Parameters**:
- `prompt` - The task or question for the agent
- `options` - Configuration options (see ClaudeAgentOptions)

**Yields**: Message objects with various subtypes

### Message Types

```python
# Result message (final output)
if hasattr(message, "result"):
    print(message.result)

# Init message (session started)
if hasattr(message, "subtype") and message.subtype == "init":
    session_id = message.session_id

# Tool use message
if hasattr(message, "tool_use"):
    print(f"Using tool: {message.tool_use.name}")

# Text delta (streaming)
if hasattr(message, "delta"):
    print(message.delta, end="")
```

## ClaudeAgentOptions

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    # Tool access
    allowed_tools=["Read", "Edit", "Bash"],  # Which tools agent can use

    # Permission handling
    permission_mode="standard",  # "standard" | "acceptEdits" | "bypassPermissions"

    # Model selection
    model="sonnet",  # "opus" | "sonnet" | "haiku"

    # Execution limits
    max_turns=100,  # Maximum tool execution cycles

    # Session management
    resume=None,  # Session ID to resume from

    # Custom tools
    mcp_servers={},  # MCP server configurations

    # Subagents
    agents={},  # Agent definitions for delegation

    # Behavior hooks
    hooks={},  # Lifecycle event handlers
)
```

## Built-in Tools Reference

### File Operations

```python
# Read - Read file contents
allowed_tools=["Read"]
# Agent can: Read any file in working directory

# Write - Create new files
allowed_tools=["Write"]
# Agent can: Create new files

# Edit - Modify existing files
allowed_tools=["Edit"]
# Agent can: Make precise edits to files

# Glob - Find files by pattern
allowed_tools=["Glob"]
# Agent can: Search for files matching patterns like "**/*.py"

# Grep - Search file contents
allowed_tools=["Grep"]
# Agent can: Search for text/regex in files
```

### System Operations

```python
# Bash - Execute commands
allowed_tools=["Bash"]
# Agent can: Run shell commands, scripts, git operations
# Note: Sandboxed by default for safety

# WebSearch - Search the web
allowed_tools=["WebSearch"]
# Agent can: Search for current information

# WebFetch - Fetch web pages
allowed_tools=["WebFetch"]
# Agent can: Retrieve and parse web content

# AskUserQuestion - Get user input
allowed_tools=["AskUserQuestion"]
# Agent can: Ask clarifying questions with multiple choice
```

### Delegation

```python
# Task - Spawn subagents
allowed_tools=["Task"]
# Agent can: Delegate to defined subagents
```

## Custom Tools (MCP)

### @tool Decorator

```python
from claude_agent_sdk import tool

@tool(
    name="tool_name",           # Unique identifier
    description="What it does", # Used by Claude to decide when to use
    parameters={                # JSON Schema for inputs
        "param1": str,
        "param2": int,
        "optional_param": {"type": "string", "default": "value"}
    }
)
async def my_tool(args: dict) -> dict:
    """
    Tool implementation.

    Args:
        args: Dictionary of parameters matching schema

    Returns:
        dict with "content" key containing list of content blocks
    """
    result = process(args["param1"], args["param2"])
    return {
        "content": [
            {"type": "text", "text": str(result)}
        ]
    }
```

### create_sdk_mcp_server()

```python
from claude_agent_sdk import create_sdk_mcp_server

server = create_sdk_mcp_server(
    name="my-server",      # Server identifier
    version="1.0.0",       # Semantic version
    tools=[tool1, tool2]   # List of @tool decorated functions
)
```

### Using Custom Tools

```python
options = ClaudeAgentOptions(
    mcp_servers={"my-server": server},
    allowed_tools=["mcp__my-server__tool_name"]
)
```

**Naming Convention**: `mcp__{server_name}__{tool_name}`

## AgentDefinition (Subagents)

```python
from claude_agent_sdk import AgentDefinition

agent = AgentDefinition(
    description="When to use this agent",  # Determines delegation
    prompt="System prompt for agent",       # Instructions
    tools=["Read", "Grep"],                # Tool access
    model="sonnet"                         # Model to use
)
```

### Using Subagents

```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Task"],  # Task enables delegation
    agents={
        "agent-name": agent_definition,
        "other-agent": other_definition
    }
)
```

## Hooks Reference

### Hook Types

```python
# PreToolUse - Before tool execution
# Can modify input or block execution
async def pre_hook(input_data, tool_use_id, context):
    # Return empty dict to continue
    # Return {"block": True} to prevent execution
    return {}

# PostToolUse - After successful tool execution
# Can log, audit, or modify state
async def post_hook(input_data, tool_use_id, context):
    return {}

# SessionStart - When session begins
async def session_start_hook(context):
    return {}

# SessionEnd - When session completes
async def session_end_hook(context):
    return {}

# UserPromptSubmit - Before user prompt processed
async def prompt_hook(prompt, context):
    return {}
```

### HookMatcher

```python
from claude_agent_sdk import HookMatcher

matcher = HookMatcher(
    matcher="Edit|Write",  # Regex pattern for tool names
    hooks=[hook_function]  # List of hook functions
)

options = ClaudeAgentOptions(
    hooks={
        "PostToolUse": [matcher]
    }
)
```

## External MCP Servers

### Subprocess-based Servers

```python
options = ClaudeAgentOptions(
    mcp_servers={
        "playwright": {
            "command": "npx",
            "args": ["@playwright/mcp@latest"]
        },
        "filesystem": {
            "command": "python",
            "args": ["-m", "mcp_server_filesystem", "/path"]
        }
    }
)
```

### Environment Variables

```python
mcp_servers={
    "github": {
        "command": "npx",
        "args": ["@modelcontextprotocol/server-github"],
        "env": {
            "GITHUB_TOKEN": os.environ.get("GITHUB_TOKEN")
        }
    }
}
```

## Error Handling

```python
async def run_agent():
    try:
        async for message in query(prompt="Do something"):
            if hasattr(message, "error"):
                logging.error(f"Agent error: {message.error}")
                continue
            if hasattr(message, "result"):
                return message.result
    except KeyboardInterrupt:
        logging.info("Agent interrupted")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
```

## Best Practices

### Tool Restriction

```python
# Read-only agent (safe for analysis)
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep"],
    permission_mode="bypassPermissions"
)

# Full capability agent (careful with permissions)
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Write", "Edit", "Bash"],
    permission_mode="standard"  # Require approval
)
```

### Model Selection

```python
# Critical security review - use best model
model="opus"

# General development tasks
model="sonnet"  # Default, good balance

# Simple, repetitive tasks
model="haiku"  # Faster, cheaper
```

### Context Management

```python
# For long-running tasks, use sessions
session_id = None

async for msg in query(prompt="Start analysis"):
    if hasattr(msg, 'session_id'):
        session_id = msg.session_id

# Later, resume with context
async for msg in query(
    prompt="Continue from before",
    options=ClaudeAgentOptions(resume=session_id)
):
    ...
```

## TypeScript Reference

```typescript
import { query, ClaudeAgentOptions } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Find bugs in auth.py",
  options: {
    allowedTools: ["Read", "Edit", "Bash"],
    permissionMode: "acceptEdits",
    model: "sonnet"
  }
})) {
  if ("result" in message) {
    console.log(message.result);
  }
}
```
