# Anti-Patterns: What NOT to Do

## Table of Contents
- [Overview](#overview)
- [Error Handling Anti-Patterns](#error-handling-anti-patterns)
- [Documentation Anti-Patterns](#documentation-anti-patterns)
- [Input Validation Anti-Patterns](#input-validation-anti-patterns)
- [Tool Design Anti-Patterns](#tool-design-anti-patterns)
- [State Management Anti-Patterns](#state-management-anti-patterns)
- [Communication Anti-Patterns](#communication-anti-patterns)

---

## Overview

Every anti-pattern represents a failure mode that wastes agent cycles. Learn these to avoid them.

**Key insight:** Most anti-patterns assume human users who can:
- Read between the lines
- Search for additional documentation
- Learn from trial and error
- Adjust behavior based on subtle cues

Agents can't do these things well. Design accordingly.

---

## Error Handling Anti-Patterns

### 1. Generic Error Messages

**Anti-pattern:**
```python
raise ValueError("Invalid input")
raise Exception("Operation failed")
raise RuntimeError("Error occurred")
```

**Why it fails:** Agent has no information to recover.

**Correct approach:**
```python
raise ToolExecutionError(
    "INVALID_AGENT_NAME",
    f"Agent name '{name}' is invalid because it uses a model name pattern. "
    f"Agent names must be adjective+noun combinations like 'BlueLake'.",
    recoverable=True,
    data={
        "provided": name,
        "detected_pattern": "model name (contains 'gpt-')",
        "example_valid": ["BlueLake", "GreenCastle"],
        "fix_hint": "Omit 'name' parameter to auto-generate"
    }
)
```

---

### 2. Stack Traces as Errors

**Anti-pattern:**
```python
# Just let exceptions propagate
def register_agent(name):
    return db.insert({"name": name})  # Raises sqlite3.IntegrityError on duplicate
```

**Why it fails:** Stack traces are for developers, not agents.

**Correct approach:**
```python
def register_agent(name):
    try:
        return db.insert({"name": name})
    except sqlite3.IntegrityError:
        raise ToolExecutionError(
            "ALREADY_EXISTS",
            f"Agent name '{name}' already exists in this project.",
            recoverable=True,
            data={
                "name": name,
                "suggestion": _generate_alternative_name(),
                "fix_hint": "Use a different name or omit to auto-generate"
            }
        )
```

---

### 3. Boolean Success/Failure

**Anti-pattern:**
```python
def validate_name(name: str) -> bool:
    return name in VALID_NAMES

# Caller has no idea why it failed
if not validate_name(input_name):
    raise ValueError("Invalid name")
```

**Why it fails:** Loses diagnostic information.

**Correct approach:**
```python
def validate_name(name: str) -> tuple[bool, str | None]:
    """Returns (is_valid, error_message_if_invalid)."""
    if not name:
        return False, "Name cannot be empty"
    if name.lower() in KNOWN_PROGRAMS:
        return False, f"'{name}' is a program name, not an agent name"
    if name.lower() not in VALID_NAMES:
        return False, f"'{name}' is not in the valid name list"
    return True, None
```

---

### 4. Swallowing Errors

**Anti-pattern:**
```python
def send_message(to, body):
    try:
        result = _do_send(to, body)
    except Exception:
        pass  # Silently fail
    return {"status": "ok"}
```

**Why it fails:** Agent thinks operation succeeded when it didn't.

**Correct approach:**
```python
def send_message(to, body):
    try:
        result = _do_send(to, body)
    except RecipientNotFoundError as e:
        raise ToolExecutionError(
            "NOT_FOUND",
            f"Recipient '{e.recipient}' not found.",
            data={"suggestions": find_similar(e.recipient)}
        )
    except DatabaseError as e:
        raise ToolExecutionError(
            "DATABASE_ERROR",
            "Failed to store message. Please retry.",
            recoverable=True
        )
    return result
```

---

## Documentation Anti-Patterns

### 5. Implicit Requirements

**Anti-pattern:**
```python
def send_message(project_key: str, sender_name: str, to: list[str]):
    """Send a message to recipients."""
    pass
```

**Why it fails:** Agent doesn't know:
- What format `project_key` should be
- Where to get `sender_name`
- How to discover valid `to` values

**Correct approach:**
```python
def send_message(project_key: str, sender_name: str, to: list[str]):
    """
    Send a message to recipients.

    Discovery
    ---------
    - project_key: Use `pwd` to get your absolute working directory
    - sender_name: Use your agent name from register_agent response
    - to: Use resource://agents/{project_key} to list available recipients

    Parameters
    ----------
    project_key : str
        ABSOLUTE path to your working directory (e.g., "/data/projects/backend").

    sender_name : str
        Your registered agent name (adjective+noun like "BlueLake").
        NOT your program name ("claude-code") or model ("opus-4.5").

    to : list[str]
        Recipient agent names. At least one required.
        NO broadcast ("all", "*") - list specific names.
    """
    pass
```

---

### 6. Missing Do/Don't Guidance

**Anti-pattern:**
```python
def file_reservation_paths(project_key: str, paths: list[str], ttl: int):
    """Reserve file paths for exclusive editing."""
    pass
```

**Why it fails:** Agent doesn't know best practices or common mistakes.

**Correct approach:**
```python
def file_reservation_paths(project_key: str, paths: list[str], ttl: int):
    """
    Reserve file paths for exclusive editing.

    Do / Don't
    ----------
    Do:
    - Reserve files BEFORE starting edits
    - Use specific patterns (e.g., "src/api/*.py")
    - Set realistic TTL and renew if needed

    Don't:
    - Reserve entire repository ("**/*")
    - Hold long-lived locks when not actively editing
    - Ignore conflicts - coordinate with holders or wait
    """
    pass
```

---

### 7. Examples Without Context

**Anti-pattern:**
```python
"""
Example: send_message(to=["X"], body="Y")
"""
```

**Why it fails:** Unrealistic values don't show proper usage.

**Correct approach:**
```python
"""
Examples
--------
Simple notification:
```json
{
  "project_key": "/data/projects/backend",
  "sender_name": "BlueLake",
  "to": ["GreenCastle"],
  "subject": "[TASK-123] Migration complete",
  "body_md": "Database migration finished. Ready for API updates."
}
```

Urgent request with acknowledgment:
```json
{
  "project_key": "/data/projects/backend",
  "sender_name": "BlueLake",
  "to": ["GreenCastle", "RedStone"],
  "subject": "[URGENT] Build blocked",
  "body_md": "Need auth review before release.",
  "importance": "urgent",
  "ack_required": true
}
```
"""
```

---

## Input Validation Anti-Patterns

### 8. Rejecting Instead of Correcting

**Anti-pattern:**
```python
def register_agent(name: str):
    if not is_valid(name):
        raise ValueError("Invalid name")
```

**Why it fails:** Agent must guess what valid input looks like.

**Correct approach:**
```python
def register_agent(name: str | None = None):
    if name:
        if is_valid(name):
            return name
        # Try to understand intent
        mistake = _detect_mistake(name)
        if mistake and mode == "strict":
            raise ToolExecutionError(mistake[0], mistake[1], ...)
        # Coerce mode: auto-generate
    return _generate_valid_name()
```

---

### 9. Case-Sensitive Matching

**Anti-pattern:**
```python
def lookup_agent(name: str):
    return db.query("SELECT * FROM agents WHERE name = ?", name)
```

**Why it fails:** "BlueLake" vs "bluelake" vs "BLUELAKE" confusion.

**Correct approach:**
```python
def lookup_agent(name: str):
    normalized = name.strip().lower()
    return db.query("SELECT * FROM agents WHERE LOWER(name) = ?", normalized)
```

---

### 10. No Fuzzy Matching

**Anti-pattern:**
```python
def lookup_agent(name: str):
    agent = db.get(name)
    if not agent:
        raise ValueError(f"Agent '{name}' not found")
```

**Why it fails:** Agent can't recover from typos.

**Correct approach:**
```python
def lookup_agent(name: str):
    agent = db.get(name)
    if not agent:
        available = db.list_agent_names()
        suggestions = find_similar(name, available)
        raise ToolExecutionError(
            "NOT_FOUND",
            f"Agent '{name}' not found. Did you mean: {', '.join(s[0] for s in suggestions[:3])}?",
            data={
                "provided": name,
                "suggestions": [{"name": s[0], "score": s[1]} for s in suggestions],
                "available": available
            }
        )
    return agent
```

---

### 11. Placeholder Values Accepted

**Anti-pattern:**
```python
def ensure_project(project_key: str):
    return db.create_or_get(project_key)  # Accepts "YOUR_PROJECT"
```

**Why it fails:** Creates garbage projects from unconfigured integrations.

**Correct approach:**
```python
_PLACEHOLDERS = ("YOUR_PROJECT", "PATH_TO_PROJECT", "$PROJECT", "${PROJECT}")

def ensure_project(project_key: str):
    upper = project_key.upper()
    for placeholder in _PLACEHOLDERS:
        if placeholder in upper:
            raise ToolExecutionError(
                "CONFIGURATION_ERROR",
                f"Detected placeholder value '{project_key}'. "
                f"Replace with your actual project path.",
                data={"example": "/data/projects/backend"}
            )
    return db.create_or_get(project_key)
```

---

## Tool Design Anti-Patterns

### 12. Too Many Required Parameters

**Anti-pattern:**
```python
def register_agent(
    project_key: str,
    name: str,          # Required
    program: str,
    model: str,
    task_description: str,
    contact_policy: str,
):
    pass
```

**Why it fails:** More required parameters = more chances for error.

**Correct approach:**
```python
def register_agent(
    project_key: str,
    program: str,
    model: str,
    name: str | None = None,           # Optional - auto-generate
    task_description: str = "",         # Optional - empty default
    contact_policy: str = "auto",       # Optional - sensible default
):
    pass
```

---

### 13. No Idempotency

**Anti-pattern:**
```python
def ensure_project(project_key: str):
    # Always creates new, fails on duplicate
    return db.insert({"key": project_key})
```

**Why it fails:** Agent can't safely retry after transient failures.

**Correct approach:**
```python
def ensure_project(project_key: str):
    """
    Idempotency
    -----------
    Safe to call multiple times. If project exists, returns existing record.
    No destructive changes on repeat calls.
    """
    existing = db.get(project_key)
    if existing:
        return existing
    return db.insert({"key": project_key})
```

---

### 14. Monolithic Tools

**Anti-pattern:**
```python
def do_everything(action: str, **kwargs):
    if action == "register":
        # 50 lines
    elif action == "send_message":
        # 100 lines
    elif action == "file_reservation":
        # 80 lines
    # ...
```

**Why it fails:** Hard to discover, hard to document, error-prone.

**Correct approach:**
```python
# Separate, focused tools
def register_agent(...): ...
def send_message(...): ...
def file_reservation_paths(...): ...

# Optional macro for common workflows
def macro_start_session(...):
    """Bundles: ensure_project + register_agent + fetch_inbox"""
    pass
```

---

### 15. No Discovery Mechanism

**Anti-pattern:**
```python
def send_message(to: list[str], body: str):
    """Send message to recipients."""
    pass  # No way to discover valid recipients
```

**Why it fails:** Agent must guess valid parameter values.

**Correct approach:**
```python
# Provide resources for discovery
@mcp.resource("agents/{project_key}")
def list_agents(project_key: str):
    """List all registered agents in project."""
    return [a.name for a in db.list_agents(project_key)]

# Document in tool
def send_message(to: list[str], body: str):
    """
    Discovery
    ---------
    Find recipients: resource://agents/{project_key}
    """
    pass
```

---

## State Management Anti-Patterns

### 16. No Expiration Handling

**Anti-pattern:**
```python
def file_reservation_paths(paths: list[str]):
    db.insert({"paths": paths, "agent": current_agent})
    # Never expires, never cleaned up
```

**Why it fails:** Dead agents hold locks forever.

**Correct approach:**
```python
def file_reservation_paths(paths: list[str], ttl_seconds: int = 3600):
    """
    Parameters
    ----------
    ttl_seconds : int = 3600
        Time to live. Expired reservations auto-release.
        Minimum: 60 seconds. Default: 1 hour.
        Tip: Renew with renew_file_reservations if needed.
    """
    expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
    db.insert({"paths": paths, "agent": current_agent, "expires_at": expires_at})

# Background cleanup
async def cleanup_expired_file_reservations():
    while True:
        db.delete("file_reservations WHERE expires_at < ?", datetime.now())
        await asyncio.sleep(60)
```

---

### 17. Assuming Persistent State

**Anti-pattern:**
```python
def get_current_agent():
    return GLOBAL_STATE["current_agent"]  # Assumes always set
```

**Why it fails:** Agent sessions restart; state is lost.

**Correct approach:**
```python
def get_agent_or_register(project_key: str, program: str, model: str):
    """
    Get current agent identity, registering if needed.

    Idempotent: safe to call at start of every tool invocation.
    """
    # Check if we have a valid session
    if _session_agent and _session_agent.is_active():
        return _session_agent

    # Re-register (idempotent)
    return register_agent(project_key, program, model)
```

---

## Communication Anti-Patterns

### 18. Allowing Broadcast

**Anti-pattern:**
```python
def send_message(to: list[str], body: str):
    if to == ["all"]:
        recipients = db.list_all_agents()
    # ...
```

**Why it fails:** Wastes context, creates noise, no accountability.

**Correct approach:**
```python
def send_message(to: list[str], body: str):
    for recipient in to:
        if recipient.lower() in {"all", "*", "everyone", "@all"}:
            raise ToolExecutionError(
                "BROADCAST_ATTEMPT",
                "Broadcast is not supported. List specific recipient names. "
                "This design is intentional: targeted communication is more efficient "
                "and prevents context waste.",
                data={"available_agents": list_agents()}
            )
```

---

### 19. No Acknowledgment Mechanism

**Anti-pattern:**
```python
def send_message(to: list[str], body: str):
    db.insert({"to": to, "body": body})
    return {"status": "sent"}  # No way to know if received/read
```

**Why it fails:** Agent can't confirm delivery or get feedback.

**Correct approach:**
```python
def send_message(to: list[str], body: str, ack_required: bool = False):
    """
    Parameters
    ----------
    ack_required : bool = False
        If true, recipients should call acknowledge_message after reading.
        Use for important messages that require confirmation.
    """
    msg = db.insert({"to": to, "body": body, "ack_required": ack_required})
    return {"id": msg.id, "ack_required": ack_required}

def acknowledge_message(message_id: int, agent_name: str):
    """Confirm receipt of a message. Safe to call multiple times."""
    pass
```

---

## Summary: The Anti-Pattern Checklist

Before shipping, verify you don't have:

- [ ] Generic error messages without context
- [ ] Stack traces exposed to agents
- [ ] Boolean success/failure without diagnostics
- [ ] Swallowed exceptions
- [ ] Implicit parameter requirements
- [ ] Missing Do/Don't guidance
- [ ] Unrealistic examples
- [ ] Rejection without correction
- [ ] Case-sensitive matching
- [ ] No fuzzy suggestions
- [ ] Placeholder values accepted
- [ ] Too many required parameters
- [ ] Non-idempotent operations
- [ ] Monolithic god-tools
- [ ] No discovery mechanism
- [ ] No expiration handling
- [ ] Assumed persistent state
- [ ] Broadcast allowed
- [ ] No acknowledgment mechanism
