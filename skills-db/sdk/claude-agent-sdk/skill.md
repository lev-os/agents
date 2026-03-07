---
name: claude-agent-sdk
description: Guide for building production AI agents with Anthropic's Claude Agent SDK. Use when the user wants to create custom agents, implement automation pipelines, add custom tools, configure subagents, or integrate Claude into existing workflows. Triggers on "build an agent", "claude agent sdk", "create automation", "custom tool", "subagent", or "agent pipeline".
version: 1.0.0
dependencies: python>=3.10, claude-agent-sdk>=1.0.0
---

# Claude Agent SDK

Build production-ready AI agents using Anthropic's official SDK - the same tools powering Claude Code.

## Quick Decision Tree

```
User wants to build agents?
│
├─→ Simple single-task agent?
│   └─→ See "Basic Agent" below
│
├─→ Agent with custom tools?
│   └─→ See "Custom Tools (MCP)" below
│
├─→ Multi-agent orchestration?
│   └─→ See "Subagents" below
│
├─→ Integrate into existing workflow?
│   └─→ See "Integration Patterns" below
│
└─→ Need detailed reference?
    └─→ Load references/api-reference.md
```

## Installation

```bash
# Python
pip install claude-agent-sdk

# TypeScript
npm install @anthropic-ai/claude-agent-sdk
```

**Requirement**: Claude Code must be installed (serves as SDK runtime).

## Basic Agent

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Bash"],
            permission_mode="acceptEdits"  # Auto-approve edits
        )
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

### Built-in Tools

No implementation needed - just allow them:

| Tool | Purpose |
|------|---------|
| `Read` | Read files |
| `Write` | Create files |
| `Edit` | Modify files |
| `Bash` | Run commands |
| `Glob` | Find files by pattern |
| `Grep` | Search file contents |
| `WebSearch` | Search the web |
| `WebFetch` | Fetch web pages |

### Permission Modes

- `standard` - Ask for approval (default)
- `acceptEdits` - Auto-approve file changes
- `bypassPermissions` - Full autonomy (CI/CD use)

## Custom Tools (MCP)

Create in-process MCP servers for custom functionality:

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, query, ClaudeAgentOptions

@tool("get_weather", "Get temperature for location", {"lat": float, "lon": float})
async def get_weather(args: dict) -> dict:
    # Your implementation
    return {"content": [{"type": "text", "text": f"Temperature: 72°F"}]}

custom_server = create_sdk_mcp_server(
    name="my-tools",
    version="1.0.0",
    tools=[get_weather]
)

async for message in query(
    prompt="What's the weather in SF?",
    options=ClaudeAgentOptions(
        mcp_servers={"my-tools": custom_server},
        allowed_tools=["mcp__my-tools__get_weather"]
    )
):
    print(message)
```

**Tool naming**: `mcp__{server_name}__{tool_name}`

## Subagents

Delegate tasks to specialized agents:

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async for message in query(
    prompt="Review auth module for security issues",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Grep", "Task"],  # Task enables subagents
        agents={
            "security-reviewer": AgentDefinition(
                description="Security code review specialist",
                prompt="You are a security expert. Find vulnerabilities.",
                tools=["Read", "Grep", "Glob"],  # Read-only
                model="sonnet"
            ),
            "test-runner": AgentDefinition(
                description="Runs and analyzes tests",
                prompt="Execute tests and analyze results.",
                tools=["Bash", "Read"],
                model="haiku"  # Faster for routine tasks
            )
        }
    )
):
    if hasattr(message, "result"):
        print(message.result)
```

**Best Practice**: One job per subagent. Orchestrator plans and delegates.

## Sessions (Context Persistence)

Maintain state across interactions:

```python
session_id = None

# First query - capture session
async for msg in query(prompt="Read the auth module"):
    if hasattr(msg, 'subtype') and msg.subtype == 'init':
        session_id = msg.session_id

# Resume with full context
async for msg in query(
    prompt="Now find all callers",  # "it" understood from context
    options=ClaudeAgentOptions(resume=session_id)
):
    print(msg)
```

## Hooks (Behavior Control)

Inject custom logic at key points:

```python
from claude_agent_sdk import HookMatcher

async def audit_log(input_data, tool_use_id, context):
    file_path = input_data.get('tool_input', {}).get('file_path')
    with open('audit.log', 'a') as f:
        f.write(f"{datetime.now()}: modified {file_path}\n")
    return {}

async for message in query(
    prompt="Refactor utils.py",
    options=ClaudeAgentOptions(
        hooks={
            "PostToolUse": [HookMatcher(matcher="Edit|Write", hooks=[audit_log])]
        }
    )
):
    print(message)
```

**Available hooks**: `PreToolUse`, `PostToolUse`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`

## Integration Patterns

### CI/CD Pipeline

```python
async def run_code_review(pr_branch: str):
    async for msg in query(
        prompt=f"Review changes in {pr_branch}",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Bash"],
            permission_mode="bypassPermissions"
        )
    ):
        if hasattr(msg, "result"):
            return msg.result
```

### REST API Wrapper

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/analyze")
async def analyze(code_path: str):
    results = []
    async for msg in query(
        prompt=f"Analyze {code_path}",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Grep"])
    ):
        if hasattr(msg, "result"):
            results.append(msg.result)
    return {"analysis": results}
```

### External MCP Server

```python
async for message in query(
    prompt="Open example.com and describe it",
    options=ClaudeAgentOptions(
        mcp_servers={
            "playwright": {
                "command": "npx",
                "args": ["@playwright/mcp@latest"]
            }
        }
    )
):
    print(message)
```

## Model Selection

| Model | Use Case |
|-------|----------|
| `opus` | Critical tasks, complex reasoning |
| `sonnet` | Balanced performance (default) |
| `haiku` | Fast, routine tasks |

## References

- **references/api-reference.md** - Complete API documentation
- **references/patterns.md** - Production patterns and examples

Load references as needed for detailed implementation guidance.
