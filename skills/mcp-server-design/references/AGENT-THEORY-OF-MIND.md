# Agent Theory of Mind

## Table of Contents
- [Core Concept](#core-concept)
- [How Agents Think](#how-agents-think)
- [Common Agent Misconceptions](#common-agent-misconceptions)
- [Design Implications](#design-implications)
- [The Anticipation Framework](#the-anticipation-framework)
- [Real-World Examples](#real-world-examples)

---

## Core Concept

**Agent Theory of Mind** = designing APIs by modeling how AI agents will interpret, misinterpret, and interact with your tools.

Key insight: Agents are NOT humans. They:
- Parse tool descriptions literally and may miss implied context
- Try reasonable-seeming but incorrect approaches
- Persist in failed strategies without human intuition to pivot
- Waste significant cycles on preventable errors

**Your job:** Anticipate these failure modes and build systems that guide agents toward success.

---

## How Agents Think

### Tool Selection
```
1. Read tool description (first 50 chars matter most)
2. Match against current task requirements
3. Infer required parameters from context
4. Call tool with best-guess arguments
5. If error: attempt recovery or try alternative
```

### Common Reasoning Patterns

| Pattern | What Agent Does | Design Implication |
|---------|-----------------|-------------------|
| **Literal interpretation** | Takes descriptions at face value | Be explicit, not implicit |
| **Pattern matching** | Reuses patterns from similar tools | Follow conventions |
| **Trial and error** | Tries variations until success | Make errors informative |
| **Context inference** | Fills gaps from conversation | Don't assume context |
| **Analogy-based** | "This is like X, so I'll try Y" | Document differences |

---

## Common Agent Misconceptions

### 1. CLI vs MCP Confusion

**What agents think:** "This tool has a name, so I can run it like a CLI command."

**Reality:** MCP tools are called via JSON-RPC, not shell commands.

**Solution:** Install a "fake CLI" that intercepts shell invocations and explains the correct usage.

```bash
# Agents try:
$ mcp-agent-mail send --to BlueLake --subject "Hello"

# They see:
MCP Agent Mail is NOT a CLI tool!
Use MCP tools: mcp__mcp-agent-mail__send_message
```

### 2. Identity Confusion

**What agents think:** "I should identify myself by my program name or model."

**Typical mistakes:**
- `agent_name="claude-code"` (program name)
- `agent_name="opus-4.5"` (model name)
- `agent_name="BackendRefactorer"` (descriptive role)
- `agent_name="john"` (Unix $USER)

**Solution:** Detect these patterns and provide specific guidance:

```python
if _looks_like_program_name(value):
    return ("PROGRAM_NAME_AS_AGENT",
            f"'{value}' is a program name. Agent names must be "
            f"adjective+noun combinations like 'BlueLake'. "
            f"Use 'program' parameter for program names.")
```

### 3. Broadcast Assumption

**What agents think:** "I want everyone to know this, so I'll send to 'all'."

**Reality:** Broadcast wastes context and creates noise.

**Solution:** Explicitly reject broadcast with explanation:

```python
"Broadcast not supported. Agent Mail is designed for targeted communication. "
"List specific recipients who need this information."
```

### 4. Parameter Ordering

**What agents think:** "This parameter looks optional, I'll skip it."

**Reality:** Many "optional" parameters have important defaults.

**Solution:** Document defaults clearly and validate combinations:

```python
"""
ttl_seconds : int = 3600
    Time to live for the reservation. MUST be >= 60.
    Default: 3600 (1 hour). Tip: Renew before expiry.
"""
```

### 5. State Assumptions

**What agents think:** "I already set this up, so it must still exist."

**Reality:** State may have changed (expired, modified by others).

**Solution:** Make operations idempotent and state-checking:

```python
"""
Idempotency
-----------
- Safe to call multiple times
- If project already exists, returns existing record
- No destructive changes on repeat calls
"""
```

---

## Design Implications

### Make Implicit Knowledge Explicit

```markdown
# BAD (assumes knowledge)
project_key : str
    The project identifier.

# GOOD (explicit guidance)
project_key : str
    The ABSOLUTE path to your working directory (e.g., "/data/projects/backend").
    Two agents in the SAME directory = SAME project.
    Use `pwd` to get your current absolute path.
```

### Front-Load Critical Information

```markdown
# BAD (important info buried)
This tool sends messages to agents. Messages are stored in Git
and indexed in SQLite. Recipients must be registered. Note that
broadcast is not supported...

# GOOD (critical constraints first)
CRITICAL: No broadcast—list specific recipients.
Sends markdown messages to one or more agents by name.
Recipients MUST be registered first (use resource://agents/{project}).
```

### Provide Discovery Mechanisms

```markdown
Discovery
---------
To find available agents: resource://agents/{project_key}
To find your agent name: Check response from register_agent
To list projects: resource://projects
```

### Document Error Recovery

```markdown
Common mistakes
---------------
- "from_agent not registered": Call register_agent first with your project_key
- "FILE_RESERVATION_CONFLICT": Another agent holds exclusive lock; wait or coordinate
- "NOT_FOUND": Check spelling; use resource://agents to list available names
```

---

## The Anticipation Framework

For every tool, ask:

### 1. What might agents confuse this with?
- Similar-sounding tools
- CLI commands
- Different parameters

### 2. What invalid inputs will they try?
- Program names as identities
- Absolute paths when relative expected
- Broadcast keywords
- Placeholder values

### 3. What implicit assumptions are they making?
- State persistence
- Default values
- Parameter requirements

### 4. When they fail, what do they need to know?
- What went wrong (specific, not generic)
- Why it went wrong (context)
- How to fix it (actionable)
- What alternatives exist (suggestions)

### 5. How can we intercept before failure?
- Environment-level stubs
- Input normalization
- Fuzzy matching
- Auto-correction

---

## Real-World Examples

### Example 1: Agent Registration

**Without theory of mind:**
```python
@mcp.tool
def register_agent(project: str, name: str, program: str) -> dict:
    """Register an agent in a project."""
    if not is_valid_name(name):
        raise ValueError("Invalid agent name")
    # ...
```

**With theory of mind:**
```python
@mcp.tool
def register_agent(
    project_key: str,
    program: str,
    model: str,
    name: str | None = None,  # Optional - auto-generate if not provided
) -> dict:
    """
    Register an agent identity in a project.

    CRITICAL: Agent Naming Rules
    ----------------------------
    - Names MUST be adjective+noun combinations (e.g., "BlueLake", "GreenCastle")
    - INVALID: "BackendWorker", "claude-code", "gpt-4" (role/program/model names)
    - Best practice: Omit `name` to auto-generate a valid name

    Parameters
    ----------
    project_key : str
        ABSOLUTE path to working directory. Use `pwd` to get this.
    name : Optional[str]
        If provided, MUST be valid adjective+noun. If omitted, auto-generated.
    """
    # Detect common mistakes
    if name:
        mistake = _detect_agent_name_mistake(name)
        if mistake:
            if mode == "coerce":
                # Auto-generate instead of failing
                name = _generate_valid_name(project_key)
            else:
                raise ToolExecutionError(
                    mistake[0],
                    mistake[1],
                    data={"provided": name, "example_valid": "BlueLake"}
                )
    # ...
```

### Example 2: Message Sending

**Without theory of mind:**
```python
@mcp.tool
def send_message(to: list[str], body: str) -> dict:
    """Send a message to recipients."""
    # Just sends, no validation
```

**With theory of mind:**
```python
@mcp.tool
def send_message(
    project_key: str,
    sender_name: str,
    to: list[str],
    subject: str,
    body_md: str,
) -> dict:
    """
    Send markdown message to specific recipients.

    Discovery
    ---------
    Find recipients: resource://agents/{project_key}

    Do / Don't
    ----------
    Do:
    - Address only agents who need this information
    - Keep subjects concise (≤80 chars)
    - Use thread_id for related messages

    Don't:
    - Try to broadcast (to=["all"] will fail)
    - Send to program names (to=["claude-code"] is wrong)
    - Change topics mid-thread

    Examples
    --------
    {"to": ["BlueLake", "GreenCastle"], "subject": "[TASK-123] Update"}
    """
    # Validate each recipient
    for recipient in to:
        mistake = _detect_agent_name_mistake(recipient)
        if mistake:
            raise ToolExecutionError(
                mistake[0],
                f"Invalid recipient '{recipient}': {mistake[1]}",
                data={
                    "recipient": recipient,
                    "available": await list_agents(project_key),
                    "hint": "Use resource://agents/{project_key} to discover valid names"
                }
            )
    # ...
```

---

## Summary: The Theory of Mind Checklist

For every tool you design:

- [ ] What will agents confuse this with?
- [ ] What invalid inputs will they try?
- [ ] What assumptions are they making?
- [ ] When they fail, what do they need?
- [ ] How can we intercept before failure?
- [ ] Is the documentation explicit enough for literal interpretation?
- [ ] Are discovery mechanisms documented?
- [ ] Are common mistakes and fixes listed?
- [ ] Is idempotency behavior documented?
- [ ] Would a Haiku model understand this?
