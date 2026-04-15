# Structured Error Design

## Table of Contents
- [Philosophy](#philosophy)
- [The ToolExecutionError Class](#the-toolexecutionerror-class)
- [Error Type Taxonomy](#error-type-taxonomy)
- [The Data Payload](#the-data-payload)
- [Fuzzy Matching for Suggestions](#fuzzy-matching-for-suggestions)
- [Error Messages That Teach](#error-messages-that-teach)
- [Complete Examples](#complete-examples)

---

## Philosophy

**Errors are educational opportunities, not failures.**

Traditional error design:
```
ValueError: Invalid agent name
```

Agent-oriented error design:
```json
{
  "error": {
    "type": "DESCRIPTIVE_NAME",
    "message": "'BackendHarmonizer' looks like a descriptive role name. Agent names must be adjective+noun combinations like 'BlueLake' or 'GreenCastle'. Omit the 'name' parameter to auto-generate a valid name.",
    "recoverable": true,
    "data": {
      "provided": "BackendHarmonizer",
      "detected_pattern": "ends with 'izer'",
      "example_valid": ["BlueLake", "GreenCastle", "RedStone"],
      "fix_hint": "Omit 'name' parameter to auto-generate"
    }
  }
}
```

---

## The ToolExecutionError Class

```python
from typing import Any, Optional

class ToolExecutionError(Exception):
    """
    Structured error for MCP tool failures.

    Designed for agents: machine-parseable, educational, actionable.
    """

    def __init__(
        self,
        error_type: str,
        message: str,
        *,
        recoverable: bool = True,
        data: Optional[dict[str, Any]] = None,
    ):
        """
        Parameters
        ----------
        error_type : str
            Machine-parseable category (e.g., "NOT_FOUND", "BROADCAST_ATTEMPT").
            Used by agents for programmatic error handling.

        message : str
            Human-readable explanation with context and guidance.
            Should explain WHAT went wrong, WHY, and HOW to fix.

        recoverable : bool
            True = agent should retry with different input
            False = agent should escalate or abort

        data : dict
            Structured metadata for programmatic recovery:
            - suggestions: similar valid options
            - fix_hint: specific action to take
            - available_options: list of valid choices
            - provided: the invalid input that was given
        """
        super().__init__(message)
        self.error_type = error_type
        self.recoverable = recoverable
        self.data = data or {}

    def to_payload(self) -> dict[str, Any]:
        """Convert to JSON-serializable payload for MCP response."""
        return {
            "error": {
                "type": self.error_type,
                "message": str(self),
                "recoverable": self.recoverable,
                "data": self.data,
            }
        }
```

---

## Error Type Taxonomy

### Input Validation Errors

| Type | When | Recoverable | Example |
|------|------|-------------|---------|
| `INVALID_ARGUMENT` | Parameter fails basic validation | Yes | Empty string, wrong type |
| `INVALID_TIMESTAMP` | Timestamp format wrong | Yes | "2025/01/15" instead of ISO-8601 |
| `INVALID_THREAD_ID` | Thread ID contains invalid chars | Yes | Spaces, special chars |
| `EMPTY_PROGRAM` | Program parameter missing/empty | Yes | `program=""` |
| `EMPTY_MODEL` | Model parameter missing/empty | Yes | `model=""` |

### Intent Detection Errors

| Type | When | Recoverable | Example |
|------|------|-------------|---------|
| `PROGRAM_NAME_AS_AGENT` | Agent name is a program | Yes | `name="claude-code"` |
| `MODEL_NAME_AS_AGENT` | Agent name is a model | Yes | `name="gpt-4"` |
| `EMAIL_AS_AGENT` | Agent name looks like email | Yes | `name="user@example.com"` |
| `BROADCAST_ATTEMPT` | Recipient is broadcast keyword | Yes | `to=["all"]` |
| `DESCRIPTIVE_NAME` | Agent name describes role | Yes | `name="BackendWorker"` |
| `UNIX_USERNAME_AS_AGENT` | Agent name is $USER | Yes | `name="john"` |

### Lookup Errors

| Type | When | Recoverable | Example |
|------|------|-------------|---------|
| `NOT_FOUND` | Entity doesn't exist | Yes | Unknown agent/project |
| `ALREADY_EXISTS` | Duplicate creation | Yes | Agent name taken |

### Configuration Errors

| Type | When | Recoverable | Example |
|------|------|-------------|---------|
| `CONFIGURATION_ERROR` | Placeholder detected | Yes | `project="YOUR_PROJECT"` |
| `AUTH_ERROR` | Authentication failed | No | Invalid token |

### Resource Errors

| Type | When | Recoverable | Example |
|------|------|-------------|---------|
| `FILE_RESERVATION_CONFLICT` | Exclusive lock held | Yes | Another agent has file |
| `RATE_LIMITED` | Too many requests | Yes | Retry after cooldown |
| `DATABASE_ERROR` | DB operation failed | No | Connection lost |

---

## The Data Payload

The `data` field provides structured information for programmatic recovery:

### For NOT_FOUND Errors

```python
data={
    "entity_type": "agent",
    "provided": "BluDog",
    "project": "backend",
    "suggestions": [
        {"name": "BlueDog", "score": 0.91},
        {"name": "BlueLake", "score": 0.72},
    ],
    "available": ["BlueDog", "BlueLake", "GreenCastle"],
    "discovery_hint": "Use resource://agents/{project_key} to list all agents"
}
```

### For Intent Detection Errors

```python
data={
    "provided": "claude-code",
    "detected_pattern": "known program name",
    "mistake_type": "PROGRAM_NAME_AS_AGENT",
    "example_valid": ["BlueLake", "GreenCastle"],
    "fix_hint": "Use 'program' parameter for program names",
    "correct_usage": {
        "program": "claude-code",
        "model": "opus-4.5",
        "name": None  # or omit to auto-generate
    }
}
```

### For Validation Errors

```python
data={
    "parameter": "since_ts",
    "provided": "2025/01/15",
    "expected_format": "YYYY-MM-DDTHH:MM:SS+HH:MM",
    "example_valid": "2025-01-15T10:30:00+00:00",
    "common_mistakes": [
        "Missing timezone (add +00:00 or Z)",
        "Using slashes instead of dashes",
        "12-hour format without AM/PM"
    ]
}
```

### For Conflict Errors

```python
data={
    "resource": "file_reservation",
    "path_pattern": "src/**/*.py",
    "conflict_holders": [
        {"agent": "BlueLake", "expires_ts": "2025-01-15T12:00:00Z"}
    ],
    "options": [
        "Wait for expiry",
        "Request shared (non-exclusive) reservation",
        "Coordinate with holder via send_message"
    ]
}
```

---

## Fuzzy Matching for Suggestions

When entities aren't found, provide intelligent suggestions:

```python
from difflib import SequenceMatcher
from typing import TypeVar

T = TypeVar("T")

def _similarity_score(a: str, b: str) -> float:
    """Compute similarity between two strings (0.0 to 1.0)."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


async def _find_similar(
    query: str,
    options: list[str],
    limit: int = 5,
    min_score: float = 0.4,
) -> list[tuple[str, float]]:
    """
    Find similar options using fuzzy matching.

    Returns list of (option, score) sorted by descending score.
    """
    suggestions = []
    for option in options:
        score = _similarity_score(query, option)
        if score >= min_score:
            suggestions.append((option, score))

    suggestions.sort(key=lambda x: x[1], reverse=True)
    return suggestions[:limit]


# Usage in error handler
async def get_agent_or_error(project: Project, name: str) -> Agent:
    agent = await lookup_agent(project, name)
    if agent:
        return agent

    # Not found - provide helpful suggestions
    available = await list_agent_names(project)
    suggestions = await _find_similar(name, available)

    # Check for common mistakes
    mistake = _detect_agent_name_mistake(name)
    mistake_hint = f" ({mistake[1]})" if mistake else ""

    suggestion_text = ", ".join(f"'{s[0]}'" for s in suggestions[:3])

    raise ToolExecutionError(
        "NOT_FOUND",
        f"Agent '{name}' not found in project '{project.slug}'. "
        f"Did you mean: {suggestion_text}?{mistake_hint}",
        recoverable=True,
        data={
            "entity_type": "agent",
            "provided": name,
            "suggestions": [
                {"name": s[0], "score": round(s[1], 2)}
                for s in suggestions
            ],
            "available": available,
            "mistake_type": mistake[0] if mistake else None,
        }
    )
```

---

## Error Messages That Teach

### Structure of a Good Error Message

```
{WHAT went wrong}: '{specific_value}' {specific_problem}.
{WHY it's a problem}: {context/constraint}.
{HOW to fix}: {actionable_instruction}.
```

### Examples

**Bad:**
```
Invalid agent name
```

**Good:**
```
'BackendHarmonizer' looks like a descriptive role name. Agent names must be
randomly generated adjective+noun combinations like 'BlueLake' or 'GreenCastle',
NOT descriptive of the agent's task. Omit the 'name' parameter to auto-generate
a valid name.
```

**Bad:**
```
Timestamp parse error
```

**Good:**
```
Invalid since_ts format: '2025/01/15'. Expected ISO-8601 format like
'2025-01-15T10:30:00+00:00' or '2025-01-15T10:30:00Z'. Common mistakes:
missing timezone (add +00:00 or Z), using slashes instead of dashes,
or using 12-hour format without AM/PM.
```

**Bad:**
```
Agent not found
```

**Good:**
```
Agent 'BluDog' not found in project 'backend'. Did you mean: 'BlueDog', 'BlueLake'?
Agent names are case-insensitive but must match exactly. Use resource://agents/backend
to list all registered agents.
```

---

## Complete Examples

### Example 1: Agent Registration Error

```python
async def validate_agent_name(
    project_key: str,
    name: str | None,
    mode: str = "coerce",
) -> str | None:
    """Validate and possibly auto-correct agent name."""

    if not name:
        return None  # Will auto-generate

    sanitized = re.sub(r"[^A-Za-z0-9]", "", name.strip())[:128]

    if not sanitized:
        raise ToolExecutionError(
            "INVALID_ARGUMENT",
            f"Agent name '{name}' contains no valid characters after sanitization.",
            recoverable=True,
            data={
                "provided": name,
                "sanitized": "",
                "fix_hint": "Omit 'name' to auto-generate, or provide alphanumeric name"
            }
        )

    # Check for common mistakes
    mistake = _detect_agent_name_mistake(sanitized)

    if validate_agent_name_format(sanitized):
        return sanitized  # Valid!

    if mode == "strict":
        raise ToolExecutionError(
            mistake[0] if mistake else "INVALID_NAME_FORMAT",
            mistake[1] if mistake else (
                f"'{sanitized}' is not a valid agent name. "
                f"Names must be adjective+noun combinations from the predefined list."
            ),
            recoverable=True,
            data={
                "provided": name,
                "sanitized": sanitized,
                "mistake_type": mistake[0] if mistake else None,
                "example_valid": ["BlueLake", "GreenCastle", "RedStone"],
                "fix_hint": "Omit 'name' to auto-generate a valid name"
            }
        )

    # Coerce mode: auto-generate instead of failing
    return None  # Signals caller to auto-generate
```

### Example 2: Message Sending Validation

```python
async def validate_recipients(
    project: Project,
    recipients: list[str],
) -> list[Agent]:
    """Validate all recipients exist and are valid."""

    agents = []
    errors = []

    for recipient in recipients:
        # Check for broadcast attempts
        if recipient.lower() in {"all", "*", "everyone", "@all", "@everyone"}:
            errors.append(ToolExecutionError(
                "BROADCAST_ATTEMPT",
                f"'{recipient}' is a broadcast keyword. Agent Mail does not support "
                f"broadcasting to all agents. List specific recipient names in 'to'. "
                f"This design is intentional: targeted communication prevents context waste.",
                recoverable=True,
                data={
                    "recipient": recipient,
                    "available_agents": await list_agent_names(project),
                    "philosophy": "Targeted > Broadcast for agent coordination"
                }
            ))
            continue

        # Check for other mistakes
        mistake = _detect_agent_name_mistake(recipient)
        if mistake:
            errors.append(ToolExecutionError(
                mistake[0],
                f"Invalid recipient '{recipient}': {mistake[1]}",
                recoverable=True,
                data={
                    "recipient": recipient,
                    "hint": "Use agent names like 'BlueLake', not program/model names"
                }
            ))
            continue

        # Lookup agent
        agent = await lookup_agent(project, recipient)
        if not agent:
            available = await list_agent_names(project)
            suggestions = await _find_similar(recipient, available)
            errors.append(ToolExecutionError(
                "NOT_FOUND",
                f"Recipient '{recipient}' not found. Did you mean: "
                f"{', '.join(s[0] for s in suggestions[:3])}?",
                recoverable=True,
                data={
                    "recipient": recipient,
                    "suggestions": [{"name": s[0], "score": s[1]} for s in suggestions],
                    "available": available
                }
            ))
            continue

        agents.append(agent)

    if errors:
        # Return first error with context about all issues
        first = errors[0]
        first.data["total_errors"] = len(errors)
        first.data["all_invalid_recipients"] = [e.data.get("recipient") for e in errors]
        raise first

    return agents
```

---

## Exception Mapping

Transform raw exceptions into structured ToolExecutionErrors.

### Mapping Database Exceptions

```python
from sqlalchemy.exc import IntegrityError, OperationalError, NoResultFound
from sqlalchemy.orm.exc import ObjectDeletedError

def map_sqlalchemy_exception(e: Exception, context: dict) -> ToolExecutionError:
    """
    Map SQLAlchemy exceptions to structured errors.

    Parameters
    ----------
    e : Exception
        The caught SQLAlchemy exception
    context : dict
        Operation context: {"entity": "agent", "operation": "create", ...}
    """
    entity = context.get("entity", "resource")
    operation = context.get("operation", "operation")

    if isinstance(e, IntegrityError):
        # Unique constraint violation
        if "UNIQUE constraint failed" in str(e):
            return ToolExecutionError(
                "ALREADY_EXISTS",
                f"A {entity} with this identifier already exists.",
                recoverable=True,
                data={
                    "entity_type": entity,
                    "constraint": "unique",
                    "fix_hint": f"Use a different identifier or update existing {entity}"
                }
            )
        # Foreign key violation
        if "FOREIGN KEY constraint failed" in str(e):
            return ToolExecutionError(
                "REFERENCE_ERROR",
                f"Cannot {operation} {entity}: referenced entity does not exist.",
                recoverable=True,
                data={
                    "entity_type": entity,
                    "constraint": "foreign_key",
                    "fix_hint": "Ensure referenced entities exist first"
                }
            )

    if isinstance(e, NoResultFound):
        return ToolExecutionError(
            "NOT_FOUND",
            f"{entity.title()} not found.",
            recoverable=True,
            data={"entity_type": entity}
        )

    if isinstance(e, OperationalError):
        if "database is locked" in str(e):
            return ToolExecutionError(
                "DATABASE_BUSY",
                "Database is temporarily busy. Please retry.",
                recoverable=True,
                data={"retry_after_ms": 100}
            )
        if "disk I/O error" in str(e):
            return ToolExecutionError(
                "DATABASE_ERROR",
                "Database I/O error. Check disk space and permissions.",
                recoverable=False,
                data={"suggestion": "Check server logs for details"}
            )

    # Fallback
    return ToolExecutionError(
        "DATABASE_ERROR",
        f"Database error during {operation}.",
        recoverable=False,
        data={"original_error": str(e)[:200]}
    )


# Usage wrapper
def db_operation(entity: str, operation: str):
    """Decorator for database operations with exception mapping."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ToolExecutionError:
                raise  # Already structured
            except Exception as e:
                raise map_sqlalchemy_exception(
                    e, {"entity": entity, "operation": operation}
                )
        return wrapper
    return decorator


# Example usage
@db_operation(entity="agent", operation="create")
async def create_agent(project_key: str, name: str, **kwargs) -> Agent:
    agent = Agent(project_key=project_key, name=name, **kwargs)
    db.add(agent)
    await db.commit()
    return agent
```

### Mapping TypeError with Pattern Matching

```python
def map_type_error(e: TypeError, func_name: str, params: dict) -> ToolExecutionError:
    """
    Extract helpful hints from TypeError messages.

    Common patterns:
    - "missing required positional argument"
    - "unexpected keyword argument"
    - "takes N positional arguments but M were given"
    """
    msg = str(e)

    # Missing argument
    match = re.search(r"missing (\d+) required (?:positional|keyword-only) argument[s]?: (.+)", msg)
    if match:
        count, names = match.groups()
        return ToolExecutionError(
            "MISSING_ARGUMENT",
            f"Missing required parameter(s): {names}",
            recoverable=True,
            data={
                "function": func_name,
                "missing": [n.strip().strip("'") for n in names.split(",")],
                "provided": list(params.keys())
            }
        )

    # Unexpected argument
    match = re.search(r"unexpected keyword argument '(\w+)'", msg)
    if match:
        arg_name = match.group(1)
        return ToolExecutionError(
            "INVALID_ARGUMENT",
            f"Unknown parameter: '{arg_name}'",
            recoverable=True,
            data={
                "invalid_param": arg_name,
                "fix_hint": "Check tool documentation for valid parameters"
            }
        )

    # Wrong number of positional args
    match = re.search(r"takes (\d+) positional argument[s]? but (\d+) (?:was|were) given", msg)
    if match:
        expected, given = match.groups()
        return ToolExecutionError(
            "ARGUMENT_COUNT_ERROR",
            f"Expected {expected} argument(s) but got {given}",
            recoverable=True,
            data={
                "expected": int(expected),
                "given": int(given)
            }
        )

    # Fallback
    return ToolExecutionError(
        "TYPE_ERROR",
        f"Type error in {func_name}: {msg}",
        recoverable=True,
        data={"original": msg}
    )
```

### Mapping Git Exceptions

```python
from git import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

def map_git_exception(e: Exception, operation: str) -> ToolExecutionError:
    """Map GitPython exceptions to structured errors."""

    if isinstance(e, InvalidGitRepositoryError):
        return ToolExecutionError(
            "NOT_A_REPOSITORY",
            "The specified path is not a Git repository.",
            recoverable=False,
            data={
                "path": str(e),
                "fix_hint": "Run 'git init' or specify a valid repository path"
            }
        )

    if isinstance(e, NoSuchPathError):
        return ToolExecutionError(
            "PATH_NOT_FOUND",
            f"Path does not exist: {e}",
            recoverable=True,
            data={
                "path": str(e),
                "fix_hint": "Check path spelling or create the directory first"
            }
        )

    if isinstance(e, GitCommandError):
        # Parse common git errors
        stderr = e.stderr if hasattr(e, 'stderr') else str(e)

        if "Permission denied" in stderr:
            return ToolExecutionError(
                "PERMISSION_ERROR",
                "Git operation denied: insufficient permissions.",
                recoverable=False,
                data={"operation": operation}
            )

        if "would be overwritten" in stderr:
            return ToolExecutionError(
                "CONFLICT_ERROR",
                "Git operation would overwrite uncommitted changes.",
                recoverable=True,
                data={
                    "operation": operation,
                    "fix_hint": "Commit or stash changes first"
                }
            )

    return ToolExecutionError(
        "GIT_ERROR",
        f"Git operation failed: {operation}",
        recoverable=False,
        data={"original": str(e)[:200]}
    )
```

---

## EMFILE Recovery

Handle file descriptor exhaustion (too many open files).

### The Problem

```
OSError: [Errno 24] Too many open files
```

This happens when:
- Git operations hold many file handles
- Database connections accumulate
- Log files aren't closed properly

### Detection and Recovery

```python
import gc
import errno
from functools import wraps

# Tools safe to retry after EMFILE cleanup
EMFILE_SAFE_TOOLS = frozenset({
    "fetch_inbox",
    "list_agents",
    "search_messages",
    "whois",
    "get_project_stats",
})

class EMFILERecoveryError(ToolExecutionError):
    """Special error indicating EMFILE was encountered and recovery attempted."""
    pass


def is_emfile_error(e: Exception) -> bool:
    """Check if exception is file descriptor exhaustion."""
    if isinstance(e, OSError) and e.errno == errno.EMFILE:
        return True
    if "Too many open files" in str(e):
        return True
    return False


def cleanup_file_descriptors():
    """
    Aggressive cleanup to free file descriptors.

    Called when EMFILE is detected.
    """
    # 1. Clear Git repo cache (major FD consumer)
    global _repo_cache
    if _repo_cache:
        for path, repo in list(_repo_cache._cache.items()):
            try:
                repo.close()
            except Exception:
                pass
        _repo_cache.clear()

    # 2. Force garbage collection
    gc.collect()

    # 3. Close any dangling database connections
    # (depends on your connection pool implementation)
    try:
        db.engine.dispose()
    except Exception:
        pass

    # 4. Log for monitoring
    logger.warning("EMFILE recovery: cleared caches and forced GC")


def with_emfile_recovery(tool_name: str):
    """
    Decorator that recovers from EMFILE errors.

    Only retries for safe (read-only) tools.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if not is_emfile_error(e):
                    raise

                # Attempt recovery
                cleanup_file_descriptors()

                # Only retry safe tools
                if tool_name not in EMFILE_SAFE_TOOLS:
                    raise ToolExecutionError(
                        "RESOURCE_EXHAUSTED",
                        "Too many open files. Resources have been cleaned up. "
                        "Please retry your operation.",
                        recoverable=True,
                        data={
                            "error": "EMFILE",
                            "tool": tool_name,
                            "fix_hint": "Retry the same operation"
                        }
                    )

                # Retry once for safe tools
                try:
                    return await func(*args, **kwargs)
                except Exception as retry_e:
                    if is_emfile_error(retry_e):
                        raise ToolExecutionError(
                            "RESOURCE_EXHAUSTED",
                            "File descriptor exhaustion persists after cleanup. "
                            "Server may need restart.",
                            recoverable=False,
                            data={"error": "EMFILE_PERSISTENT"}
                        )
                    raise
        return wrapper
    return decorator


# Usage
@with_emfile_recovery("fetch_inbox")
async def fetch_inbox(project_key: str, agent_name: str, **kwargs) -> list[dict]:
    # ... implementation
    pass
```

### Proactive FD Management

```python
from contextlib import contextmanager

# Global repo cache with size limit
class LRURepoCache:
    """LRU cache for Git repos with FD-aware eviction."""

    def __init__(self, maxsize: int = 10):
        self._cache: OrderedDict[str, Repo] = OrderedDict()
        self._maxsize = maxsize

    def get(self, path: str) -> Repo | None:
        if path in self._cache:
            self._cache.move_to_end(path)
            return self._cache[path]
        return None

    def put(self, path: str, repo: Repo):
        # Evict oldest if at capacity
        while len(self._cache) >= self._maxsize:
            _, evicted = self._cache.popitem(last=False)
            evicted.close()  # CRITICAL: Close to free FD

        self._cache[path] = repo

    def clear(self):
        for repo in self._cache.values():
            try:
                repo.close()
            except Exception:
                pass
        self._cache.clear()


_repo_cache = LRURepoCache(maxsize=10)


@contextmanager
def git_repo(path: str) -> Generator[Repo, None, None]:
    """
    Context manager for Git repos that ensures cleanup.

    Uses cache for frequently accessed repos.
    """
    # Try cache first
    repo = _repo_cache.get(path)
    if repo:
        yield repo
        return

    # Open new repo
    repo = Repo(path)
    try:
        yield repo
        # Cache if successful
        _repo_cache.put(path, repo)
    except Exception:
        repo.close()  # Always close on error
        raise


# Usage
async def get_recent_commits(project_key: str) -> list[dict]:
    archive_path = get_archive_path(project_key)

    with git_repo(archive_path) as repo:
        commits = list(repo.iter_commits(max_count=10))
        return [
            {"sha": c.hexsha[:8], "message": c.summary}
            for c in commits
        ]
```

---

## Suggested Tool Calls Pattern

Include actionable tool calls in error payloads that agents can execute to recover:

```python
class ToolExecutionError(Exception):
    """Extended with suggested_tool_calls for guided recovery."""

    def __init__(
        self,
        error_type: str,
        message: str,
        *,
        recoverable: bool = True,
        data: dict = None,
        suggested_tool_calls: list[dict] = None,  # NEW!
    ):
        super().__init__(message)
        self.error_type = error_type
        self.recoverable = recoverable
        self.data = data or {}
        self.suggested_tool_calls = suggested_tool_calls or []

    def to_payload(self) -> dict:
        payload = {
            "error": {
                "type": self.error_type,
                "message": str(self),
                "recoverable": self.recoverable,
                "data": self.data,
            }
        }
        if self.suggested_tool_calls:
            payload["error"]["suggested_tool_calls"] = self.suggested_tool_calls
        return payload
```

### Example: Agent Not Found with Discovery Suggestion

```python
async def get_agent_or_error(project: Project, name: str) -> Agent:
    agent = await lookup_agent(project, name)
    if agent:
        return agent

    available = await list_agent_names(project)
    suggestions = await _find_similar(name, available)

    raise ToolExecutionError(
        "NOT_FOUND",
        f"Agent '{name}' not found. Did you mean: {suggestions[0][0]}?",
        recoverable=True,
        data={
            "provided": name,
            "suggestions": suggestions,
            "available": available,
        },
        suggested_tool_calls=[
            # Suggest discovering available agents
            {
                "tool": "mcp__mcp-agent-mail__fetch_inbox",
                "description": "List agents by fetching with valid name",
                "arguments": {
                    "project_key": project.human_key,
                    "agent_name": suggestions[0][0] if suggestions else available[0],
                }
            },
            # Or suggest using resource for discovery
            {
                "tool": "ReadMcpResourceTool",
                "description": "Discover all agents in project",
                "arguments": {
                    "server": "mcp-agent-mail",
                    "uri": f"resource://agents/{project.slug}",
                }
            },
        ]
    )
```

### Example: File Reservation Conflict with Coordination Options

```python
def handle_reservation_conflict(
    path: str,
    holder: Agent,
    expires: datetime,
    requester: Agent,
) -> ToolExecutionError:
    """Guide agent through conflict resolution."""

    time_remaining = (expires - datetime.now(UTC)).total_seconds()

    return ToolExecutionError(
        "FILE_RESERVATION_CONFLICT",
        f"Path '{path}' is reserved by {holder.name} until {expires.isoformat()}",
        recoverable=True,
        data={
            "path": path,
            "holder": holder.name,
            "expires_ts": expires.isoformat(),
            "time_remaining_seconds": time_remaining,
        },
        suggested_tool_calls=[
            # Option 1: Message the holder
            {
                "tool": "mcp__mcp-agent-mail__send_message",
                "description": "Ask holder to release reservation",
                "arguments": {
                    "project_key": holder.project.human_key,
                    "sender_name": requester.name,
                    "to": [holder.name],
                    "subject": f"Request to release {path}",
                    "body_md": f"Hi {holder.name}, I need to work on `{path}`. "
                              f"Could you release your reservation when ready?",
                    "importance": "high",
                }
            },
            # Option 2: Wait and retry
            {
                "tool": "mcp__mcp-agent-mail__file_reservation_paths",
                "description": f"Retry after reservation expires ({int(time_remaining)}s)",
                "arguments": {
                    "project_key": holder.project.human_key,
                    "agent_name": requester.name,
                    "paths": [path],
                    "exclusive": True,
                },
                "delay_seconds": int(time_remaining) + 5,  # Wait for expiry
            },
            # Option 3: Request shared access
            {
                "tool": "mcp__mcp-agent-mail__file_reservation_paths",
                "description": "Request non-exclusive (shared) reservation",
                "arguments": {
                    "project_key": holder.project.human_key,
                    "agent_name": requester.name,
                    "paths": [path],
                    "exclusive": False,  # Shared access
                }
            },
        ]
    )
```

### Example: Stale Reservation with Force Release Option

```python
def handle_stale_reservation(
    reservation: FileReservation,
    requester: Agent,
    staleness_signals: dict,
) -> ToolExecutionError:
    """Offer force-release for abandoned reservations."""

    return ToolExecutionError(
        "FILE_RESERVATION_CONFLICT",
        f"Path '{reservation.path_pattern}' reserved by {reservation.agent.name}, "
        f"but holder appears inactive (last active: {reservation.agent.last_active_ts})",
        recoverable=True,
        data={
            "path": reservation.path_pattern,
            "holder": reservation.agent.name,
            "staleness_signals": staleness_signals,
            "holder_last_active": reservation.agent.last_active_ts.isoformat(),
        },
        suggested_tool_calls=[
            # Force release (holder is inactive)
            {
                "tool": "mcp__mcp-agent-mail__force_release_file_reservation",
                "description": "Force release stale reservation (holder inactive)",
                "arguments": {
                    "project_key": reservation.project.human_key,
                    "agent_name": requester.name,
                    "file_reservation_id": reservation.id,
                    "notify_previous": True,  # Inform holder
                    "note": "Auto-released due to inactivity",
                }
            },
        ]
    )
```

---

## IntegrityError Idempotency

Handle concurrent creation gracefully by returning existing records:

```python
from sqlalchemy.exc import IntegrityError

async def register_agent(
    project_key: str,
    name: str,
    program: str,
    model: str,
    **kwargs,
) -> dict:
    """
    Register agent with idempotent handling.

    If concurrent creation causes IntegrityError, returns existing agent.
    """
    try:
        agent = Agent(
            project_key=project_key,
            name=name,
            program=program,
            model=model,
            **kwargs,
        )
        session.add(agent)
        await session.commit()
        return agent.to_dict()

    except IntegrityError as e:
        await session.rollback()

        # Check if it's a unique constraint on name
        if "UNIQUE constraint failed" in str(e) and "name" in str(e):
            # Return existing agent (idempotent behavior)
            existing = await session.execute(
                select(Agent).where(
                    Agent.project_key == project_key,
                    Agent.name == name,
                )
            )
            agent = existing.scalar_one_or_none()

            if agent:
                # Update last_active and return
                agent.last_active_ts = datetime.now(UTC)
                await session.commit()
                return agent.to_dict()

        # Re-raise if not the expected case
        raise map_sqlalchemy_exception(e, {"entity": "agent", "operation": "register"})
```

### Similar Pattern for AgentLinks

```python
async def request_contact(
    project_key: str,
    from_agent: str,
    to_agent: str,
    **kwargs,
) -> dict:
    """
    Request contact with idempotent handling.

    Concurrent requests for same link return existing pending/approved link.
    """
    try:
        link = AgentLink(
            from_agent_name=from_agent,
            to_agent_name=to_agent,
            project_key=project_key,
            status="pending",
            **kwargs,
        )
        session.add(link)
        await session.commit()
        return {"link": link.to_dict(), "status": "created"}

    except IntegrityError:
        await session.rollback()

        # Check for existing link
        existing = await session.execute(
            select(AgentLink).where(
                AgentLink.from_agent_name == from_agent,
                AgentLink.to_agent_name == to_agent,
                AgentLink.project_key == project_key,
            )
        )
        link = existing.scalar_one_or_none()

        if link:
            return {
                "link": link.to_dict(),
                "status": "existing",
                "note": f"Contact request already exists (status: {link.status})",
            }

        raise
```

---

## Global Exception Handler

Catch-all for unexpected exceptions.

```python
import traceback
import logging

logger = logging.getLogger(__name__)


async def global_tool_handler(
    tool_name: str,
    func: Callable,
    params: dict
) -> dict:
    """
    Global wrapper for all tool executions.

    - Maps known exceptions to structured errors
    - Logs unexpected errors
    - Never exposes stack traces to agents
    """
    try:
        return await func(**params)

    except ToolExecutionError:
        raise  # Already structured

    except TypeError as e:
        raise map_type_error(e, tool_name, params)

    except ValueError as e:
        # Usually validation errors
        raise ToolExecutionError(
            "INVALID_ARGUMENT",
            str(e),
            recoverable=True,
            data={"tool": tool_name}
        )

    except Exception as e:
        if is_emfile_error(e):
            cleanup_file_descriptors()
            raise ToolExecutionError(
                "RESOURCE_EXHAUSTED",
                "Server resource limit reached. Please retry.",
                recoverable=True
            )

        # Log for debugging, but don't expose to agent
        logger.exception(f"Unexpected error in {tool_name}")

        raise ToolExecutionError(
            "INTERNAL_ERROR",
            f"An unexpected error occurred in {tool_name}. "
            f"The error has been logged. Please retry or contact support.",
            recoverable=False,
            data={
                "tool": tool_name,
                "error_id": generate_error_id()  # For log correlation
            }
        )
```
