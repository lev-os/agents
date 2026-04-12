# MCP Resource Design Patterns

## Table of Contents
- [Overview](#overview)
- [Resource vs Tool Decision](#resource-vs-tool-decision)
- [Resource URI Patterns](#resource-uri-patterns)
- [Query String Parsing](#query-string-parsing)
- [Discovery Resources](#discovery-resources)
- [Metadata Resources](#metadata-resources)
- [Content Resources](#content-resources)
- [Resource Implementation](#resource-implementation)

---

## Overview

Resources are the discovery backbone of MCP servers. They answer the question: "What valid values can I use for this parameter?"

**Key insight:** Every tool parameter with non-obvious values should have a corresponding resource for discovery.

**mcp_agent_mail exposes 14+ resources:**
```
resource://agents/{project_key}
resource://threads/{project_key}
resource://file_reservations/{project_key}
resource://messages/{project_key}
resource://inbox/{project_key}/{agent_name}
resource://outbox/{project_key}/{agent_name}
resource://contacts/{project_key}/{agent_name}
resource://project/{project_key}
resource://archive/{project_key}
resource://config
resource://metrics
resource://health
resource://schema
resource://capabilities
```

---

## Resource vs Tool Decision

### Use Resources For

| Purpose | Example |
|---------|---------|
| **Listing entities** | List all agents in project |
| **Discovery** | Find valid parameter values |
| **Read-only data** | Configuration, metrics |
| **Metadata** | Schema, capabilities |
| **Cached/static info** | Wordlists, constants |

### Use Tools For

| Purpose | Example |
|---------|---------|
| **Mutations** | Create, update, delete |
| **Side effects** | Send message, reserve file |
| **Complex queries** | FTS5 search with filters |
| **Stateful operations** | Acknowledge, mark read |
| **Multi-step workflows** | Macro operations |

### Decision Flowchart

```
Is it read-only?
├─ No → Use Tool
└─ Yes → Does it require complex parameters?
         ├─ Yes → Use Tool (with read-only behavior)
         └─ No → Does agent need it for discovery?
                  ├─ Yes → Use Resource
                  └─ No → Use Tool (for consistency)
```

---

## Resource URI Patterns

### Hierarchical Structure

```
resource://{entity_type}/{scope}/{optional_sub_entity}
```

**Examples:**
```
resource://agents/{project_key}           # All agents in project
resource://inbox/{project_key}/{agent}    # Specific agent's inbox
resource://file_reservations/{project_key}/{path}  # Specific reservation
```

### Naming Conventions

| Pattern | Use Case |
|---------|----------|
| `{entity}s/{scope}` | Collection listing |
| `{entity}/{scope}/{id}` | Single entity |
| `{entity}/{scope}/{parent}/{child}` | Nested relationship |

### Good URI Examples

```python
# Collection resources
"resource://agents/{project_key}"           # List agents
"resource://threads/{project_key}"          # List threads
"resource://file_reservations/{project_key}"  # List reservations

# Scoped collections
"resource://inbox/{project_key}/{agent_name}"    # Agent's inbox
"resource://contacts/{project_key}/{agent_name}" # Agent's contacts

# Singleton resources
"resource://config"        # Server configuration
"resource://health"        # Health check
"resource://capabilities"  # Server capabilities
```

### Bad URI Examples

```python
# Too generic
"resource://data"              # What data?
"resource://list"              # List of what?

# Inconsistent plurality
"resource://agent/{project}"   # Should be "agents"
"resource://messages/{id}"     # Missing project scope

# Unclear hierarchy
"resource://{project}/agents"  # Project should be typed
```

---

## Query String Parsing

Resources can accept query parameters for filtering without becoming tools.

### Implementation Pattern

```python
from urllib.parse import urlparse, parse_qs

@mcp.resource("resource://agents/{project_key}")
async def list_agents(project_key: str, uri: str) -> list[dict]:
    """
    List agents in project with optional filtering.

    Query Parameters
    ----------------
    active : bool
        If true, only return agents active in last 24h
    program : str
        Filter by program name (e.g., "claude-code")
    limit : int
        Maximum results (default: 100)

    Examples
    --------
    resource://agents/backend?active=true
    resource://agents/backend?program=claude-code&limit=10
    """
    # Parse query string
    parsed = urlparse(uri)
    params = parse_qs(parsed.query)

    # Extract with defaults
    active_only = params.get("active", ["false"])[0].lower() == "true"
    program_filter = params.get("program", [None])[0]
    limit = int(params.get("limit", ["100"])[0])

    # Build query
    query = db.query(Agent).filter(Agent.project_key == project_key)

    if active_only:
        cutoff = datetime.now(UTC) - timedelta(hours=24)
        query = query.filter(Agent.last_active_ts > cutoff)

    if program_filter:
        query = query.filter(Agent.program == program_filter)

    return [agent.to_dict() for agent in query.limit(limit).all()]
```

### Query Parameter Best Practices

1. **Use standard names:**
   - `limit`, `offset` for pagination
   - `since`, `until` for time ranges
   - `active`, `archived` for status filters

2. **Provide defaults:**
   ```python
   limit = int(params.get("limit", ["100"])[0])  # Default 100
   ```

3. **Document in docstring:**
   ```python
   """
   Query Parameters
   ----------------
   limit : int = 100
       Maximum results to return
   """
   ```

4. **Validate ranges:**
   ```python
   limit = min(int(params.get("limit", ["100"])[0]), 1000)  # Cap at 1000
   ```

---

## Discovery Resources

Discovery resources help agents find valid parameter values.

### Agent Discovery

```python
@mcp.resource("resource://agents/{project_key}")
async def list_agents(project_key: str) -> list[dict]:
    """
    List all registered agents in project.

    Use this resource to discover valid values for:
    - send_message(to=[...])
    - whois(agent_name=...)
    - request_contact(to_agent=...)

    Returns
    -------
    list[dict]
        Each agent: { name, program, model, task_description,
                      last_active_ts, inception_ts }

    Example Response
    ----------------
    [
        {
            "name": "BlueLake",
            "program": "claude-code",
            "model": "opus-4.5",
            "task_description": "API refactoring",
            "last_active_ts": "2025-01-15T10:30:00+00:00"
        },
        {
            "name": "GreenCastle",
            "program": "codex-cli",
            "model": "gpt5-codex",
            "task_description": "Database migrations"
        }
    ]
    """
    agents = db.query(Agent).filter(Agent.project_key == project_key).all()
    return [
        {
            "name": a.name,
            "program": a.program,
            "model": a.model,
            "task_description": a.task_description,
            "last_active_ts": a.last_active_ts.isoformat() if a.last_active_ts else None,
            "inception_ts": a.inception_ts.isoformat() if a.inception_ts else None,
        }
        for a in agents
    ]
```

### Thread Discovery

```python
@mcp.resource("resource://threads/{project_key}")
async def list_threads(project_key: str) -> list[dict]:
    """
    List active threads in project.

    Use this resource to discover valid values for:
    - send_message(thread_id=...)
    - reply_message(...)
    - summarize_thread(thread_id=...)

    Returns
    -------
    list[dict]
        Each thread: { thread_id, subject, participant_count,
                       message_count, last_activity }
    """
    threads = db.query(Thread).filter(
        Thread.project_key == project_key
    ).order_by(Thread.last_activity.desc()).limit(50).all()

    return [
        {
            "thread_id": t.thread_id,
            "subject": t.subject,
            "participant_count": len(t.participants),
            "message_count": t.message_count,
            "last_activity": t.last_activity.isoformat()
        }
        for t in threads
    ]
```

### File Reservation Discovery

```python
@mcp.resource("resource://file_reservations/{project_key}")
async def list_file_reservations(project_key: str) -> list[dict]:
    """
    List active file reservations in project.

    Use this resource to:
    - Check for conflicts before reserving
    - Discover who holds locks on files
    - Find expired/stale reservations

    Returns
    -------
    list[dict]
        Each reservation: { id, path_pattern, agent_name, exclusive,
                           expires_ts, reason }
    """
    now = datetime.now(UTC)
    reservations = db.query(FileReservation).filter(
        FileReservation.project_key == project_key,
        FileReservation.released_ts.is_(None),
        FileReservation.expires_ts > now
    ).all()

    return [
        {
            "id": r.id,
            "path_pattern": r.path_pattern,
            "agent_name": r.agent_name,
            "exclusive": r.exclusive,
            "expires_ts": r.expires_ts.isoformat(),
            "reason": r.reason,
            "is_stale": _is_reservation_stale(r)  # Useful hint
        }
        for r in reservations
    ]
```

---

## Metadata Resources

Metadata resources expose server configuration and capabilities.

### Configuration Resource

```python
@mcp.resource("resource://config")
async def get_config() -> dict:
    """
    Return server configuration (non-sensitive).

    Useful for agents to understand:
    - What enforcement modes are available
    - Default TTL values
    - Rate limits
    - Feature flags
    """
    return {
        "enforcement_mode": settings.enforcement_mode,
        "default_file_reservation_ttl": settings.default_file_reservation_ttl,
        "max_message_size": settings.max_message_size,
        "max_attachment_size": settings.max_attachment_size,
        "features": {
            "llm_summaries": settings.llm_enabled,
            "image_conversion": settings.convert_images,
            "git_integration": settings.git_enabled
        },
        "rate_limits": {
            "messages_per_minute": 60,
            "file_reservations_per_agent": 100
        }
    }
```

### Capabilities Resource

```python
@mcp.resource("resource://capabilities")
async def get_capabilities() -> dict:
    """
    Return server capabilities for capability gating.

    Agents can use this to:
    - Check if features are available
    - Adapt behavior based on server version
    - Skip unavailable operations
    """
    return {
        "version": "1.2.0",
        "protocol_version": "2024-11-05",
        "tools": [
            "register_agent",
            "send_message",
            "file_reservation_paths",
            # ... full list
        ],
        "resources": [
            "agents",
            "threads",
            "inbox",
            # ... full list
        ],
        "features": {
            "fts5_search": True,
            "fuzzy_matching": True,
            "llm_summaries": settings.llm_enabled,
            "git_archive": True
        }
    }
```

### Health Resource

```python
@mcp.resource("resource://health")
async def health_check() -> dict:
    """
    Return server health status.

    Useful for:
    - Verifying server is responsive
    - Checking database connectivity
    - Monitoring resource usage
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "database": "connected",
        "uptime_seconds": (datetime.now(UTC) - _start_time).total_seconds(),
        "active_agents": db.query(Agent).filter(
            Agent.last_active_ts > datetime.now(UTC) - timedelta(hours=1)
        ).count()
    }
```

---

## Content Resources

Content resources provide access to actual data, not just metadata.

### Inbox Resource

```python
@mcp.resource("resource://inbox/{project_key}/{agent_name}")
async def get_inbox(project_key: str, agent_name: str, uri: str) -> list[dict]:
    """
    Get recent messages for an agent.

    Query Parameters
    ----------------
    limit : int = 20
        Maximum messages to return
    since : str
        ISO timestamp; only messages after this
    unread_only : bool = false
        If true, only unread messages
    urgent_only : bool = false
        If true, only urgent/high importance

    Returns
    -------
    list[dict]
        Messages with: { id, subject, from, created_ts, importance,
                        ack_required, read_at, body_md (if include_body) }

    Examples
    --------
    resource://inbox/backend/BlueLake
    resource://inbox/backend/BlueLake?unread_only=true
    resource://inbox/backend/BlueLake?since=2025-01-15T00:00:00Z
    """
    parsed = urlparse(uri)
    params = parse_qs(parsed.query)

    limit = int(params.get("limit", ["20"])[0])
    since = params.get("since", [None])[0]
    unread_only = params.get("unread_only", ["false"])[0].lower() == "true"
    urgent_only = params.get("urgent_only", ["false"])[0].lower() == "true"

    query = db.query(Message).join(Recipient).filter(
        Recipient.agent_name == agent_name,
        Message.project_key == project_key
    )

    if since:
        query = query.filter(Message.created_ts > parse_iso(since))
    if unread_only:
        query = query.filter(Recipient.read_ts.is_(None))
    if urgent_only:
        query = query.filter(Message.importance.in_(["high", "urgent"]))

    messages = query.order_by(Message.created_ts.desc()).limit(limit).all()

    return [msg.to_summary_dict() for msg in messages]
```

### Archive Resource

```python
@mcp.resource("resource://archive/{project_key}")
async def get_archive_info(project_key: str) -> dict:
    """
    Get Git archive information for project.

    Returns
    -------
    dict
        Archive metadata: { path, branch, last_commit, structure }
    """
    archive_path = get_archive_path(project_key)

    with _git_repo(archive_path) as repo:
        head = repo.head.commit
        return {
            "path": str(archive_path),
            "branch": repo.active_branch.name,
            "last_commit": {
                "hexsha": head.hexsha[:8],
                "summary": head.summary,
                "author": str(head.author),
                "authored_datetime": head.authored_datetime.isoformat()
            },
            "structure": {
                "agents": len(list((archive_path / "agents").iterdir())),
                "messages": _count_messages(archive_path),
                "file_reservations": len(list((archive_path / "file_reservations").iterdir()))
            }
        }
```

---

## Resource Implementation

### Registration Pattern

```python
from mcp.server import Server
from mcp.types import Resource

mcp = Server("my-server")

# Method 1: Decorator
@mcp.resource("resource://agents/{project_key}")
async def list_agents(project_key: str) -> list[dict]:
    ...

# Method 2: Explicit registration
async def list_threads(project_key: str) -> list[dict]:
    ...

mcp.register_resource(
    Resource(
        uri="resource://threads/{project_key}",
        name="Thread List",
        description="List active threads in project",
        mimeType="application/json"
    ),
    list_threads
)
```

### Error Handling in Resources

Resources should handle errors gracefully:

```python
@mcp.resource("resource://agents/{project_key}")
async def list_agents(project_key: str) -> list[dict]:
    """List agents with graceful error handling."""
    try:
        project = get_project(project_key)
        if not project:
            return {
                "error": "PROJECT_NOT_FOUND",
                "message": f"Project '{project_key}' not found",
                "hint": "Use ensure_project tool first"
            }

        agents = db.query(Agent).filter(
            Agent.project_id == project.id
        ).all()

        return [a.to_dict() for a in agents]

    except Exception as e:
        logger.exception("Error listing agents")
        return {
            "error": "INTERNAL_ERROR",
            "message": "Failed to list agents",
            "recoverable": True
        }
```

### Caching Pattern

For expensive resources, implement caching:

```python
from functools import lru_cache
from datetime import datetime, timedelta

_cache = {}
_cache_ttl = timedelta(seconds=30)

@mcp.resource("resource://metrics")
async def get_metrics() -> dict:
    """Get server metrics with caching."""
    cache_key = "metrics"
    now = datetime.now(UTC)

    if cache_key in _cache:
        cached_at, data = _cache[cache_key]
        if now - cached_at < _cache_ttl:
            return data

    # Compute expensive metrics
    data = {
        "total_messages": db.query(Message).count(),
        "active_agents": db.query(Agent).filter(
            Agent.last_active_ts > now - timedelta(hours=1)
        ).count(),
        "computed_at": now.isoformat()
    }

    _cache[cache_key] = (now, data)
    return data
```

---

## Resource Documentation Template

Every resource should document:

```python
@mcp.resource("resource://{entity}/{scope}")
async def get_entity(scope: str, uri: str) -> ReturnType:
    """
    One-line description of what this resource provides.

    Discovery
    ---------
    - What tool parameters this helps populate
    - Related resources for more context

    Query Parameters
    ----------------
    param1 : type = default
        Description of parameter
    param2 : type = default
        Description of parameter

    Returns
    -------
    type
        Description of return structure with field explanations

    Example Response
    ----------------
    ```json
    {
        "field1": "value1",
        "field2": 123
    }
    ```

    Examples
    --------
    resource://entity/scope
    resource://entity/scope?param1=value
    resource://entity/scope?param1=value&param2=other

    Related
    -------
    - tool_name: Uses this resource's values
    - other_resource: Provides complementary data
    """
    pass
```

---

## Summary: The 5 Resource Principles

| # | Principle | Implementation |
|---|-----------|----------------|
| 1 | **Discovery First** | Every non-obvious parameter has a resource |
| 2 | **Hierarchical URIs** | `resource://{type}/{scope}/{sub}` |
| 3 | **Query Filtering** | Use query strings for optional filters |
| 4 | **Rich Metadata** | Return useful hints, not just raw data |
| 5 | **Graceful Degradation** | Return structured errors, not exceptions |
