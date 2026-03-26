# Tool Documentation for Agents

## Table of Contents
- [The Problem](#the-problem)
- [Documentation Structure](#documentation-structure)
- [Required Sections](#required-sections)
- [The Do/Don't Pattern](#the-dodont-pattern)
- [Writing Discovery Sections](#writing-discovery-sections)
- [Examples That Work](#examples-that-work)
- [Complete Template](#complete-template)

---

## The Problem

Traditional API documentation assumes a human reader who:
- Has context about the system
- Can infer implicit requirements
- Knows to search for additional resources
- Learns from trial and error

Agents:
- Parse descriptions literally
- Miss implied context
- Don't search for help unprompted
- Waste cycles on preventable errors

**Solution:** Documentation that anticipates agent reasoning patterns.

---

## Documentation Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  Brief one-liner (WHAT)                                         │
├─────────────────────────────────────────────────────────────────┤
│  Discovery (HOW TO FIND required values)                        │
├─────────────────────────────────────────────────────────────────┤
│  When to use (WHEN to choose this tool)                         │
├─────────────────────────────────────────────────────────────────┤
│  Parameters (INPUT specification)                               │
├─────────────────────────────────────────────────────────────────┤
│  Returns (OUTPUT specification)                                 │
├─────────────────────────────────────────────────────────────────┤
│  Do / Don't (BEHAVIORAL guidance)                               │
├─────────────────────────────────────────────────────────────────┤
│  Examples (CONCRETE usage patterns)                             │
├─────────────────────────────────────────────────────────────────┤
│  Common mistakes (PITFALL avoidance)                            │
├─────────────────────────────────────────────────────────────────┤
│  Idempotency (RETRY safety)                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Required Sections

### 1. Brief One-Liner

First line of docstring. Front-load the action verb.

```python
# GOOD
"""Send a Markdown message to one or more recipients."""

# BAD
"""This tool is used for communication between agents."""
```

### 2. Discovery Section

Tell agents HOW to find required parameter values:

```markdown
Discovery
---------
To discover available agent names for recipients, use: resource://agents/{project_key}
Agent names are NOT the same as program names or user names.
To find your own agent name: Check the response from register_agent.
```

### 3. When to Use

Explicit triggers for tool selection:

```markdown
When to use
-----------
- Before starting any work: register your identity
- When you need to coordinate with another agent
- When you've completed a task and need to notify stakeholders
```

### 4. Parameters (NumPy Style)

```markdown
Parameters
----------
project_key : str
    The ABSOLUTE path to your working directory (e.g., "/data/projects/backend").
    MUST be an absolute path, not relative. Use `pwd` to get this.

sender_name : str
    Your agent name from register_agent. MUST match exactly (case-insensitive).

to : list[str]
    Primary recipients. At least one required. Use resource://agents to discover names.

importance : str = "normal"
    One of: "low", "normal", "high", "urgent". Default: "normal".
    Tip: Use "urgent" sparingly—it's for blocking issues only.
```

### 5. Returns

```markdown
Returns
-------
dict
    {
        "id": str,              # Message ID for reference
        "created_ts": str,      # ISO-8601 timestamp
        "subject": str,         # Echoed back for confirmation
        "recipients": {
            "to": list[str],
            "cc": list[str],
            "bcc": list[str]
        },
        "thread_id": str | null  # If part of a thread
    }
```

### 6. Do / Don't Section

**Critical for agent guidance:**

```markdown
Do / Don't
----------
Do:
- Keep subjects concise and specific (aim for ≤ 80 characters)
- Use `thread_id` to keep related discussion in a single thread
- Address only relevant recipients; use CC/BCC sparingly
- Prefer Markdown links; attach images only when essential

Don't:
- Send large, repeated binaries—reuse prior attachments when possible
- Change topics mid-thread—start a new thread for a new subject
- Broadcast to "all" agents—target just the agents who need to act
- Use your program name as sender_name—use your registered agent name
```

### 7. Examples

JSON-RPC format with realistic values:

```markdown
Examples
--------
Simple message:
```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "tools/call",
  "params": {
    "name": "send_message",
    "arguments": {
      "project_key": "/data/projects/backend",
      "sender_name": "GreenCastle",
      "to": ["BlueLake"],
      "subject": "Plan for /api/users",
      "body_md": "See below for implementation plan."
    }
  }
}
```

With thread (reply pattern):
```json
{
  "project_key": "/data/projects/backend",
  "sender_name": "GreenCastle",
  "to": ["BlueLake"],
  "subject": "Re: [TASK-123] API implementation",
  "body_md": "Completed the endpoint. Ready for review.",
  "thread_id": "TASK-123"
}
```
```

### 8. Common Mistakes

```markdown
Common mistakes
---------------
- Passing relative path: Use absolute path from `pwd`, not "./project"
- Using program as sender: Use your agent name ("BlueLake"), not "claude-code"
- Broadcast attempt: to=["all"] fails; list specific recipients
- Missing registration: Call register_agent before send_message
```

### 9. Idempotency

```markdown
Idempotency
-----------
- NOT idempotent: Each call creates a new message
- If you need to ensure delivery, use ack_required=true
- Duplicate sends will create duplicate messages—check before resending
```

---

## The Do/Don't Pattern

The most impactful documentation section for agents.

### Why It Works

Agents tend to:
1. Try reasonable-seeming approaches that don't work
2. Not know system-specific constraints
3. Miss implicit best practices

Do/Don't explicitly addresses these.

### Structure

```markdown
Do / Don't
----------
Do:
- [Positive action] [because/benefit]
- [Another positive action]

Don't:
- [Anti-pattern] [because/consequence]
- [Another anti-pattern]
```

### Examples by Tool Type

**Messaging Tool:**
```markdown
Do:
- Keep subjects concise (≤80 chars) for inbox readability
- Use thread_id for related messages
- Include context—recipients may lack your conversation history

Don't:
- Broadcast to all agents (wastes context, creates noise)
- Change topics mid-thread (start a new thread instead)
- Attach large files repeatedly (reference prior attachments)
```

**File Reservation Tool:**
```markdown
Do:
- Reserve files BEFORE starting edits
- Use specific patterns (e.g., `src/api/*.py`) not broad globs
- Set realistic TTL and renew if needed

Don't:
- Reserve entire repository (`**/*`)
- Hold long-lived exclusive locks when not actively editing
- Ignore conflicts—coordinate with holders or wait
```

**Registration Tool:**
```markdown
Do:
- Register once at session start
- Omit `name` to auto-generate a valid name
- Use consistent project_key across tools

Don't:
- Use descriptive names ("BackendWorker")—use adjective+noun
- Use your program name as agent name
- Create multiple identities for one session
```

---

## Writing Discovery Sections

Agents need to know WHERE to find parameter values.

### Pattern

```markdown
Discovery
---------
[Parameter]: [How to get it]
[Another parameter]: [How to get it]
```

### Examples

**For Agent Name:**
```markdown
Discovery
---------
To find agent names: resource://agents/{project_key}
Your own name: Check response from register_agent
Agent names look like: "BlueLake", "GreenCastle" (adjective+noun)
```

**For Project Key:**
```markdown
Discovery
---------
To find project key: Use `pwd` in your working directory
Project keys are absolute paths like "/data/projects/backend"
Two agents in same directory = same project
```

**For Thread ID:**
```markdown
Discovery
---------
To find existing threads: resource://threads/{project_key}
Thread IDs are often task IDs: "TASK-123", "br-456"
Create your own: Use consistent naming like ticket numbers
```

---

## Examples That Work

### Bad Examples (Avoid)

```markdown
# Too minimal
Example: send_message(to=["Agent"], body="Hello")

# Unrealistic values
Example: {"to": ["X"], "body": "Y"}

# Missing context
Example: Use the tool to send messages.
```

### Good Examples (Use)

```markdown
Examples
--------

1. Simple notification:
```json
{
  "project_key": "/data/projects/smartedgar",
  "sender_name": "BlueLake",
  "to": ["GreenCastle"],
  "subject": "[br-123] Schema migration complete",
  "body_md": "The user table migration is done. Ready for API updates."
}
```

2. Urgent request with acknowledgment:
```json
{
  "project_key": "/data/projects/smartedgar",
  "sender_name": "BlueLake",
  "to": ["GreenCastle", "RedStone"],
  "subject": "[URGENT] Build blocked on auth module",
  "body_md": "Need review of auth changes before 3pm. Blocking release.",
  "importance": "urgent",
  "ack_required": true
}
```

3. Thread reply:
```json
{
  "project_key": "/data/projects/smartedgar",
  "sender_name": "GreenCastle",
  "to": ["BlueLake"],
  "subject": "Re: [br-123] Schema migration complete",
  "body_md": "API updated to use new schema. Tests passing.",
  "thread_id": "br-123"
}
```
```

---

## Complete Template

```python
@mcp.tool
def tool_name(
    param1: str,
    param2: list[str],
    param3: int = 100,
) -> dict:
    """
    Brief one-liner describing what this tool does.

    Discovery
    ---------
    param1: Use `resource://X` or command `Y` to find valid values.
    param2: Check response from tool_Z or resource://W.

    When to use
    -----------
    - Scenario 1 that triggers this tool
    - Scenario 2 that triggers this tool
    - NOT for: scenario that should use different tool

    Parameters
    ----------
    param1 : str
        Description. MUST be [constraint]. Example: "value".

    param2 : list[str]
        Description. At least one required. Use Discovery above.

    param3 : int = 100
        Optional. Default: 100. Range: 1-1000.
        Tip: Higher values = slower but more complete.

    Returns
    -------
    dict
        {
            "field1": str,  # Description
            "field2": int,  # Description
            "nested": {
                "subfield": list[str]
            }
        }

    Do / Don't
    ----------
    Do:
    - Positive guidance with reason
    - Another positive pattern

    Don't:
    - Anti-pattern with consequence
    - Another anti-pattern

    Examples
    --------
    Basic usage:
    ```json
    {"param1": "realistic_value", "param2": ["item1", "item2"]}
    ```

    Advanced usage:
    ```json
    {"param1": "value", "param2": ["item"], "param3": 500}
    ```

    Common mistakes
    ---------------
    - Mistake 1: explanation and how to fix
    - Mistake 2: explanation and how to fix

    Idempotency
    -----------
    - [Safe to call multiple times / Creates new resource each time]
    - [Behavior on duplicate input]

    Edge cases
    ----------
    - If param2 is empty: [behavior]
    - If param1 not found: [behavior with suggestions]
    """
    pass
```
