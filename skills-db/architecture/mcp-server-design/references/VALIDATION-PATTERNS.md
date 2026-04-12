# Validation and Input Normalization Patterns

## Table of Contents
- [Philosophy](#philosophy)
- [The Three Enforcement Modes](#the-three-enforcement-modes)
- [Input Normalization Pipeline](#input-normalization-pipeline)
- [Pre-computed Validation Sets](#pre-computed-validation-sets)
- [Timestamp Validation](#timestamp-validation)
- [Path Validation](#path-validation)
- [Recipient Validation](#recipient-validation)
- [Configuration Validation](#configuration-validation)

---

## Philosophy

**Validate to educate, normalize to succeed.**

Traditional validation:
```python
if not is_valid(input):
    raise ValueError("Invalid input")
```

Agent-friendly validation:
```python
if not is_valid(input):
    if mode == "coerce" and can_infer_intent(input):
        return normalize(input)  # Auto-fix
    else:
        raise ToolExecutionError(
            "INVALID_INPUT",
            f"'{input}' is invalid because {reason}. "
            f"Valid format: {format}. Example: {example}",
            data={"suggestions": find_similar(input, valid_options)}
        )
```

---

## The Three Enforcement Modes

```python
from enum import Enum

class EnforcementMode(str, Enum):
    """Control how validation failures are handled."""

    STRICT = "strict"
    # Reject invalid input, return detailed error with suggestions
    # Use for: debugging, development, explicit validation requests

    COERCE = "coerce"  # DEFAULT
    # Auto-fix invalid input when intent is clear, use valid result
    # Use for: production, smaller models, forgiving UX

    ALWAYS_AUTO = "always_auto"
    # Ignore user input entirely, always auto-generate
    # Use for: guaranteed valid values, maximum reliability
```

### Implementation

```python
def validate_agent_name(
    name: str | None,
    project: Project,
    mode: EnforcementMode = EnforcementMode.COERCE,
) -> str:
    """
    Validate or normalize an agent name.

    Returns a valid agent name according to the enforcement mode.
    """

    # ALWAYS_AUTO: Skip all validation
    if mode == EnforcementMode.ALWAYS_AUTO:
        return _generate_random_name(project)

    # No name provided: auto-generate
    if not name or not name.strip():
        return _generate_random_name(project)

    # Sanitize input
    sanitized = _sanitize_name(name)

    # Check if already valid
    if _is_valid_agent_name(sanitized):
        # Check uniqueness
        if await _name_exists(project, sanitized):
            if mode == EnforcementMode.STRICT:
                raise ToolExecutionError(
                    "ALREADY_EXISTS",
                    f"Agent name '{sanitized}' already exists in project.",
                    data={"suggestion": _generate_random_name(project)}
                )
            # COERCE: generate new name
            return _generate_random_name(project)
        return sanitized

    # Invalid name: check for mistakes
    mistake = _detect_mistake(name)

    if mode == EnforcementMode.STRICT:
        raise ToolExecutionError(
            mistake[0] if mistake else "INVALID_NAME",
            mistake[1] if mistake else f"'{name}' is not a valid agent name.",
            recoverable=True,
            data={
                "provided": name,
                "sanitized": sanitized,
                "example_valid": ["BlueLake", "GreenCastle", "RedStone"],
                "fix_hint": "Omit 'name' parameter to auto-generate"
            }
        )

    # COERCE: auto-generate valid name
    return _generate_random_name(project)
```

### Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Server configuration with validation mode."""

    # Validation modes
    agent_name_enforcement_mode: EnforcementMode = EnforcementMode.COERCE
    project_key_enforcement_mode: EnforcementMode = EnforcementMode.STRICT
    thread_id_enforcement_mode: EnforcementMode = EnforcementMode.COERCE

    # Environment override
    class Config:
        env_prefix = "MCP_"
        # MCP_AGENT_NAME_ENFORCEMENT_MODE=strict
```

---

## Input Normalization Pipeline

```python
import re
from typing import Callable

def normalize_input(
    value: str,
    validators: list[Callable[[str], str | None]],
    normalizers: list[Callable[[str], str]],
    mode: EnforcementMode = EnforcementMode.COERCE,
) -> str:
    """
    Generic input normalization pipeline.

    1. Run validators (return error message or None)
    2. If validation fails and mode is strict, raise error
    3. Apply normalizers in sequence
    4. Return normalized value
    """

    # Step 1: Validate
    for validator in validators:
        error = validator(value)
        if error:
            if mode == EnforcementMode.STRICT:
                raise ToolExecutionError("VALIDATION_ERROR", error)
            # COERCE mode continues to normalization
            break

    # Step 2: Normalize
    result = value
    for normalizer in normalizers:
        result = normalizer(result)

    return result


# Example normalizers
def strip_whitespace(value: str) -> str:
    return value.strip()

def remove_special_chars(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "", value)

def truncate(max_length: int) -> Callable[[str], str]:
    def _truncate(value: str) -> str:
        return value[:max_length]
    return _truncate

def lowercase(value: str) -> str:
    return value.lower()

def to_pascal_case(value: str) -> str:
    """Convert to PascalCase."""
    words = re.split(r"[-_\s]+", value)
    return "".join(word.capitalize() for word in words if word)


# Example validators
def not_empty(value: str) -> str | None:
    if not value or not value.strip():
        return "Value cannot be empty"
    return None

def max_length(limit: int) -> Callable[[str], str | None]:
    def _validator(value: str) -> str | None:
        if len(value) > limit:
            return f"Value exceeds maximum length of {limit} characters"
        return None
    return _validator

def matches_pattern(pattern: str, description: str) -> Callable[[str], str | None]:
    compiled = re.compile(pattern)
    def _validator(value: str) -> str | None:
        if not compiled.fullmatch(value):
            return f"Value must match {description}"
        return None
    return _validator
```

### Agent Name Sanitization

```python
def _sanitize_name(name: str) -> str:
    """
    Sanitize agent name input.

    Pipeline:
    1. Strip whitespace
    2. Remove non-alphanumeric characters
    3. Truncate to 128 characters
    4. Convert to PascalCase
    """
    sanitized = name.strip()
    sanitized = re.sub(r"[^A-Za-z0-9]", "", sanitized)
    sanitized = sanitized[:128]

    # Ensure PascalCase
    if sanitized and not sanitized[0].isupper():
        sanitized = sanitized.capitalize()

    return sanitized
```

---

## Pre-computed Validation Sets

O(1) validation via frozenset:

```python
from typing import FrozenSet

# Word lists for valid agent names
ADJECTIVES: tuple[str, ...] = (
    "Blue", "Green", "Red", "Purple", "Golden", "Silver",
    "White", "Black", "Brown", "Orange", "Yellow", "Pink",
    "Bright", "Dark", "Light", "Swift", "Calm", "Bold",
    # ... 70+ adjectives
)

NOUNS: tuple[str, ...] = (
    "Lake", "Castle", "Stone", "Bear", "Wolf", "Eagle",
    "Mountain", "River", "Forest", "Valley", "Creek", "Peak",
    "Storm", "Cloud", "Star", "Moon", "Sun", "Fire",
    # ... 60+ nouns
)

# Pre-compute all valid combinations at module load
_VALID_NAMES: FrozenSet[str] = frozenset(
    f"{adj}{noun}".lower()
    for adj in ADJECTIVES
    for noun in NOUNS
)  # ~4,278 combinations

# Also store lowercased wordlists for partial matching
ADJECTIVES_LOWER: FrozenSet[str] = frozenset(a.lower() for a in ADJECTIVES)
NOUNS_LOWER: FrozenSet[str] = frozenset(n.lower() for n in NOUNS)


def is_valid_agent_name(name: str) -> bool:
    """O(1) validation of agent name format."""
    return name.lower() in _VALID_NAMES


def validate_agent_name_format(name: str) -> bool:
    """
    Check if name matches adjective+noun pattern.

    More permissive than is_valid_agent_name:
    - Checks structure (starts with adjective, ends with noun)
    - Doesn't require exact wordlist match
    """
    n = name.lower()

    # Check if starts with known adjective
    for adj in ADJECTIVES_LOWER:
        if n.startswith(adj):
            remainder = n[len(adj):]
            if remainder in NOUNS_LOWER:
                return True

    return False
```

### Benefits of Pre-computation

```python
import timeit

# Runtime validation (slow)
def validate_runtime(name: str) -> bool:
    for adj in ADJECTIVES:
        for noun in NOUNS:
            if name.lower() == f"{adj}{noun}".lower():
                return True
    return False

# Pre-computed validation (fast)
def validate_precomputed(name: str) -> bool:
    return name.lower() in _VALID_NAMES

# Benchmark
# validate_runtime: ~0.5ms per call
# validate_precomputed: ~0.0001ms per call (5000x faster)
```

---

## Timestamp Validation

```python
from datetime import datetime, timezone
import re

# ISO-8601 patterns
_ISO_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}"  # Date
    r"[T ]"                 # Separator
    r"\d{2}:\d{2}:\d{2}"   # Time
    r"(\.\d+)?"            # Optional microseconds
    r"(Z|[+-]\d{2}:?\d{2})?$"  # Optional timezone
)


def validate_timestamp(
    value: str,
    mode: EnforcementMode = EnforcementMode.COERCE,
) -> datetime:
    """
    Validate and parse ISO-8601 timestamp.

    Accepts:
    - 2025-01-15T10:30:00Z
    - 2025-01-15T10:30:00+00:00
    - 2025-01-15 10:30:00

    COERCE mode: Attempts common format fixes
    STRICT mode: Requires exact ISO-8601
    """

    if not value or not value.strip():
        raise ToolExecutionError(
            "INVALID_TIMESTAMP",
            "Timestamp cannot be empty.",
            data={"example": "2025-01-15T10:30:00Z"}
        )

    normalized = value.strip()

    # COERCE: Try common format fixes
    if mode == EnforcementMode.COERCE:
        # Replace slashes with dashes
        normalized = normalized.replace("/", "-")

        # Add missing timezone
        if not re.search(r"[Z+-]", normalized):
            normalized += "+00:00"

        # Normalize 'Z' to '+00:00'
        if normalized.endswith("Z"):
            normalized = normalized[:-1] + "+00:00"

    try:
        # Try parsing
        dt = datetime.fromisoformat(normalized)

        # Ensure timezone-aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt

    except ValueError as e:
        raise ToolExecutionError(
            "INVALID_TIMESTAMP",
            f"Invalid timestamp format: '{value}'. "
            f"Expected ISO-8601 format like '2025-01-15T10:30:00+00:00' or '2025-01-15T10:30:00Z'. "
            f"Common mistakes: missing timezone (add +00:00 or Z), "
            f"using slashes instead of dashes, 12-hour format without AM/PM.",
            recoverable=True,
            data={
                "provided": value,
                "normalized_attempt": normalized,
                "expected_format": "YYYY-MM-DDTHH:MM:SS+HH:MM",
                "example_valid": "2025-01-15T10:30:00+00:00",
            }
        )
```

---

## Path Validation

```python
from pathlib import Path

def validate_project_key(
    value: str,
    mode: EnforcementMode = EnforcementMode.STRICT,
) -> str:
    """
    Validate project key (must be absolute path).

    Project keys are absolute paths to working directories.
    Two agents in the same directory = same project.
    """

    # Check for placeholder values
    placeholder_error = _detect_placeholder(value, "project")
    if placeholder_error:
        raise ToolExecutionError(
            "CONFIGURATION_ERROR",
            placeholder_error,
            recoverable=True,
            data={
                "parameter": "project_key",
                "provided": value,
                "fix_hint": "Use `pwd` to get your working directory",
                "example_valid": "/data/projects/backend"
            }
        )

    normalized = value.strip()

    # Must be absolute path
    if not normalized.startswith("/"):
        if mode == EnforcementMode.COERCE:
            # Try to resolve relative path
            try:
                normalized = str(Path(normalized).resolve())
            except Exception:
                pass

        if not normalized.startswith("/"):
            raise ToolExecutionError(
                "INVALID_PATH",
                f"Project key must be an absolute path. "
                f"Got: '{value}'. Use `pwd` to get your absolute working directory.",
                recoverable=True,
                data={
                    "provided": value,
                    "fix_hint": "Use absolute path like /data/projects/backend",
                }
            )

    # Remove trailing slash for consistency
    normalized = normalized.rstrip("/")

    return normalized


def validate_file_pattern(
    pattern: str,
    mode: EnforcementMode = EnforcementMode.COERCE,
) -> str:
    """
    Validate file reservation pattern.

    Patterns should be project-relative (not absolute).
    """

    p = pattern.strip()

    # Check for suspicious patterns
    warning = _detect_suspicious_file_reservation(p)
    if warning:
        if mode == EnforcementMode.STRICT:
            raise ToolExecutionError(
                "SUSPICIOUS_PATTERN",
                warning,
                recoverable=True,
                data={
                    "pattern": p,
                    "suggestion": "Use specific patterns like 'src/api/*.py'"
                }
            )
        # COERCE: log warning but continue
        # (actual logging omitted for brevity)

    # Normalize: remove leading ./
    if p.startswith("./"):
        p = p[2:]

    # Normalize: remove leading /
    if p.startswith("/") and not p.startswith("//"):
        p = p.lstrip("/")

    return p
```

---

## Recipient Validation

```python
async def validate_recipients(
    recipients: list[str],
    project: Project,
    mode: EnforcementMode = EnforcementMode.STRICT,
) -> list[Agent]:
    """
    Validate message recipients.

    Returns list of validated Agent objects.
    Raises ToolExecutionError if any recipient is invalid.
    """

    if not recipients:
        raise ToolExecutionError(
            "EMPTY_RECIPIENTS",
            "At least one recipient is required in 'to', 'cc', or 'bcc'.",
            recoverable=True,
            data={"fix_hint": "Add recipient names to the 'to' parameter"}
        )

    agents = []
    errors = []

    for recipient in recipients:
        # Check for broadcast attempt
        if recipient.lower() in {"all", "*", "everyone", "@all", "@everyone"}:
            errors.append({
                "recipient": recipient,
                "error_type": "BROADCAST_ATTEMPT",
                "message": f"'{recipient}' looks like a broadcast attempt. "
                           f"Agent Mail doesn't support broadcasting. "
                           f"List specific recipient agent names."
            })
            continue

        # Check for common mistakes
        mistake = _detect_mistake(recipient)
        if mistake:
            errors.append({
                "recipient": recipient,
                "error_type": mistake[0],
                "message": mistake[1]
            })
            continue

        # Lookup agent
        agent = await _lookup_agent(project, recipient)
        if agent:
            agents.append(agent)
        else:
            # Not found: suggest similar
            available = await _list_agent_names(project)
            suggestions = _find_similar(recipient, available)
            errors.append({
                "recipient": recipient,
                "error_type": "NOT_FOUND",
                "message": f"Recipient '{recipient}' not found.",
                "suggestions": [s[0] for s in suggestions[:3]]
            })

    if errors:
        first_error = errors[0]
        raise ToolExecutionError(
            first_error["error_type"],
            first_error["message"],
            recoverable=True,
            data={
                "invalid_recipients": errors,
                "valid_recipients": [a.name for a in agents],
                "available_agents": await _list_agent_names(project),
                "total_errors": len(errors)
            }
        )

    return agents
```

---

## Configuration Validation

```python
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Server settings with validation.

    All settings can be overridden via environment variables
    with MCP_ prefix (e.g., MCP_DATA_DIR).
    """

    # Paths
    data_dir: str = "/data/mcp_agent_mail"
    archive_base_dir: str = "/data/mcp_agent_mail/archive"

    # Enforcement modes
    agent_name_enforcement_mode: EnforcementMode = EnforcementMode.COERCE

    # Limits
    max_message_body_size: int = 1_000_000  # 1MB
    max_attachment_size: int = 10_000_000   # 10MB
    max_recipients: int = 50
    default_file_reservation_ttl: int = 3600  # 1 hour
    min_file_reservation_ttl: int = 60       # 1 minute

    @field_validator("data_dir", "archive_base_dir")
    @classmethod
    def validate_absolute_path(cls, v: str) -> str:
        if not v.startswith("/"):
            raise ValueError(f"Path must be absolute: {v}")
        return v

    @field_validator("agent_name_enforcement_mode", mode="before")
    @classmethod
    def validate_enforcement_mode(cls, v: str) -> EnforcementMode:
        if isinstance(v, EnforcementMode):
            return v
        try:
            return EnforcementMode(v.lower())
        except ValueError:
            valid = [m.value for m in EnforcementMode]
            raise ValueError(
                f"Invalid enforcement mode: '{v}'. "
                f"Valid modes: {valid}"
            )

    @field_validator("min_file_reservation_ttl")
    @classmethod
    def validate_min_ttl(cls, v: int) -> int:
        if v < 60:
            raise ValueError(
                "Minimum file reservation TTL must be at least 60 seconds. "
                "This prevents very short locks that cause race conditions."
            )
        return v

    class Config:
        env_prefix = "MCP_"
        env_file = ".env"
        case_sensitive = False
```

---

## Settings Hierarchy Pattern

For MCP servers with 100+ configuration options, use a hierarchical settings structure with frozen dataclasses.

### Hierarchical Structure

```python
from dataclasses import dataclass, field
from typing import Optional
import os

# Type conversion helpers for environment variables
def _bool(val: str | bool | None) -> bool:
    """Convert string to bool, handling common variations."""
    if isinstance(val, bool):
        return val
    if val is None:
        return False
    return val.lower() in ("true", "1", "yes", "on")

def _int(val: str | int | None, default: int = 0) -> int:
    """Convert string to int with default."""
    if val is None:
        return default
    if isinstance(val, int):
        return val
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def _float(val: str | float | None, default: float = 0.0) -> float:
    """Convert string to float with default."""
    if val is None:
        return default
    if isinstance(val, float):
        return val
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


@dataclass(slots=True, frozen=True)
class ToolFilterSettings:
    """Settings for tool capability filtering."""
    enabled: bool = False
    profile: str = "full"  # full, core, minimal, messaging, custom
    mode: str = "include"  # include, exclude
    clusters: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class LLMSettings:
    """Settings for LLM integration."""
    enabled: bool = True
    default_model: str = "gpt-4o-mini"
    fallback_model: str = "gpt-3.5-turbo"
    timeout_seconds: int = 30
    max_retries: int = 2
    cost_tracking: bool = True
    max_cost_per_request_usd: float = 0.10
    max_daily_cost_usd: float = 10.0


@dataclass(slots=True, frozen=True)
class DatabaseSettings:
    """Settings for database access."""
    path: str = ""
    wal_mode: bool = True
    busy_timeout_ms: int = 30000
    synchronous: str = "NORMAL"  # OFF, NORMAL, FULL
    cache_size_kb: int = 65536
    pool_size: int = 5
    slow_query_threshold_ms: float = 100.0


@dataclass(slots=True, frozen=True)
class GitSettings:
    """Settings for Git integration."""
    author_name: str = "MCP Agent Mail"
    author_email: str = "mcp@localhost"
    repo_cache_size: int = 16
    auto_commit: bool = True
    sign_commits: bool = False


@dataclass(slots=True, frozen=True)
class FileReservationSettings:
    """Settings for file reservations."""
    default_ttl_seconds: int = 3600
    min_ttl_seconds: int = 60
    max_ttl_seconds: int = 86400
    stale_threshold_seconds: int = 1800
    force_release_enabled: bool = True


@dataclass(slots=True, frozen=True)
class MessageSettings:
    """Settings for messaging."""
    max_body_size: int = 1_000_000
    max_attachment_size: int = 10_000_000
    max_recipients: int = 50
    convert_images_to_webp: bool = True
    inline_small_images: bool = True
    inline_threshold_bytes: int = 32768


@dataclass(slots=True, frozen=True)
class Settings:
    """
    Root settings container with 100+ options across categories.

    All values are frozen (immutable) after construction.
    Uses slots for memory efficiency.
    """
    # Sub-settings
    tool_filter: ToolFilterSettings = field(default_factory=ToolFilterSettings)
    llm: LLMSettings = field(default_factory=LLMSettings)
    database: DatabaseSettings = field(default_factory=DatabaseSettings)
    git: GitSettings = field(default_factory=GitSettings)
    file_reservation: FileReservationSettings = field(default_factory=FileReservationSettings)
    message: MessageSettings = field(default_factory=MessageSettings)

    # Enforcement modes
    agent_name_mode: str = "coerce"
    project_key_mode: str = "strict"
    thread_id_mode: str = "coerce"

    # Paths
    data_dir: str = "/data/mcp_agent_mail"
    archive_base_dir: str = "/data/mcp_agent_mail/archive"

    # Debugging
    debug: bool = False
    log_level: str = "INFO"
    query_logging: bool = False
```

### Loading from Environment

```python
def load_settings() -> Settings:
    """
    Load settings from environment variables.

    Environment variable naming convention:
    - MCP_<CATEGORY>_<SETTING> for nested settings
    - MCP_<SETTING> for root-level settings

    Examples:
    - MCP_TOOL_FILTER_ENABLED=true
    - MCP_LLM_DEFAULT_MODEL=claude-3-5-sonnet
    - MCP_DATABASE_BUSY_TIMEOUT_MS=60000
    - MCP_DEBUG=true
    """
    # Load tool filter settings
    tool_filter_clusters = os.getenv("MCP_TOOL_FILTER_CLUSTERS", "")
    tool_filter_tools = os.getenv("MCP_TOOL_FILTER_TOOLS", "")

    tool_filter = ToolFilterSettings(
        enabled=_bool(os.getenv("MCP_TOOL_FILTER_ENABLED", "false")),
        profile=os.getenv("MCP_TOOL_FILTER_PROFILE", "full"),
        mode=os.getenv("MCP_TOOL_FILTER_MODE", "include"),
        clusters=tuple(c.strip() for c in tool_filter_clusters.split(",") if c.strip()),
        tools=tuple(t.strip() for t in tool_filter_tools.split(",") if t.strip()),
    )

    # Load LLM settings
    llm = LLMSettings(
        enabled=_bool(os.getenv("MCP_LLM_ENABLED", "true")),
        default_model=os.getenv("MCP_LLM_DEFAULT_MODEL", "gpt-4o-mini"),
        fallback_model=os.getenv("MCP_LLM_FALLBACK_MODEL", "gpt-3.5-turbo"),
        timeout_seconds=_int(os.getenv("MCP_LLM_TIMEOUT"), 30),
        max_retries=_int(os.getenv("MCP_LLM_MAX_RETRIES"), 2),
        cost_tracking=_bool(os.getenv("MCP_LLM_COST_TRACKING", "true")),
        max_cost_per_request_usd=_float(os.getenv("MCP_LLM_MAX_COST_REQUEST"), 0.10),
        max_daily_cost_usd=_float(os.getenv("MCP_LLM_MAX_COST_DAILY"), 10.0),
    )

    # Load database settings
    database = DatabaseSettings(
        path=os.getenv("MCP_DATABASE_PATH", "/data/mcp_agent_mail/db.sqlite"),
        wal_mode=_bool(os.getenv("MCP_DATABASE_WAL_MODE", "true")),
        busy_timeout_ms=_int(os.getenv("MCP_DATABASE_BUSY_TIMEOUT_MS"), 30000),
        synchronous=os.getenv("MCP_DATABASE_SYNCHRONOUS", "NORMAL"),
        cache_size_kb=_int(os.getenv("MCP_DATABASE_CACHE_SIZE_KB"), 65536),
        pool_size=_int(os.getenv("MCP_DATABASE_POOL_SIZE"), 5),
        slow_query_threshold_ms=_float(os.getenv("MCP_DATABASE_SLOW_QUERY_MS"), 100.0),
    )

    # Load git settings
    git = GitSettings(
        author_name=os.getenv("MCP_GIT_AUTHOR_NAME", "MCP Agent Mail"),
        author_email=os.getenv("MCP_GIT_AUTHOR_EMAIL", "mcp@localhost"),
        repo_cache_size=_int(os.getenv("MCP_GIT_REPO_CACHE_SIZE"), 16),
        auto_commit=_bool(os.getenv("MCP_GIT_AUTO_COMMIT", "true")),
        sign_commits=_bool(os.getenv("MCP_GIT_SIGN_COMMITS", "false")),
    )

    # Load file reservation settings
    file_reservation = FileReservationSettings(
        default_ttl_seconds=_int(os.getenv("MCP_FILE_RESERVATION_DEFAULT_TTL"), 3600),
        min_ttl_seconds=_int(os.getenv("MCP_FILE_RESERVATION_MIN_TTL"), 60),
        max_ttl_seconds=_int(os.getenv("MCP_FILE_RESERVATION_MAX_TTL"), 86400),
        stale_threshold_seconds=_int(os.getenv("MCP_FILE_RESERVATION_STALE_THRESHOLD"), 1800),
        force_release_enabled=_bool(os.getenv("MCP_FILE_RESERVATION_FORCE_RELEASE", "true")),
    )

    # Load message settings
    message = MessageSettings(
        max_body_size=_int(os.getenv("MCP_MESSAGE_MAX_BODY_SIZE"), 1_000_000),
        max_attachment_size=_int(os.getenv("MCP_MESSAGE_MAX_ATTACHMENT_SIZE"), 10_000_000),
        max_recipients=_int(os.getenv("MCP_MESSAGE_MAX_RECIPIENTS"), 50),
        convert_images_to_webp=_bool(os.getenv("MCP_MESSAGE_CONVERT_IMAGES", "true")),
        inline_small_images=_bool(os.getenv("MCP_MESSAGE_INLINE_IMAGES", "true")),
        inline_threshold_bytes=_int(os.getenv("MCP_MESSAGE_INLINE_THRESHOLD"), 32768),
    )

    # Build root settings
    return Settings(
        tool_filter=tool_filter,
        llm=llm,
        database=database,
        git=git,
        file_reservation=file_reservation,
        message=message,
        agent_name_mode=os.getenv("MCP_AGENT_NAME_MODE", "coerce"),
        project_key_mode=os.getenv("MCP_PROJECT_KEY_MODE", "strict"),
        thread_id_mode=os.getenv("MCP_THREAD_ID_MODE", "coerce"),
        data_dir=os.getenv("MCP_DATA_DIR", "/data/mcp_agent_mail"),
        archive_base_dir=os.getenv("MCP_ARCHIVE_BASE_DIR", "/data/mcp_agent_mail/archive"),
        debug=_bool(os.getenv("MCP_DEBUG", "false")),
        log_level=os.getenv("MCP_LOG_LEVEL", "INFO"),
        query_logging=_bool(os.getenv("MCP_QUERY_LOGGING", "false")),
    )


# Global singleton (loaded once at startup)
_settings: Settings | None = None

def get_settings() -> Settings:
    """Get cached settings instance."""
    global _settings
    if _settings is None:
        _settings = load_settings()
    return _settings
```

### Benefits of Frozen Dataclasses

1. **Immutability**: Settings can't be accidentally modified at runtime
2. **Memory Efficiency**: `slots=True` reduces memory overhead
3. **Type Safety**: Clear typing for all configuration
4. **Hierarchical Organization**: Related settings grouped together
5. **Default Values**: Every setting has a sensible default
6. **Easy Testing**: Create test settings with different values

---

## Advanced Timestamp Coercion

Handle the many ways agents format timestamps wrong.

### Common Agent Timestamp Mistakes

| Agent Input | Problem | Coerced Output |
|-------------|---------|----------------|
| `2025/01/15T10:30:00` | Slashes instead of dashes | `2025-01-15T10:30:00` |
| `2025-01-15 10:30:00` | Space instead of T | `2025-01-15T10:30:00` |
| `2025-01-15T10:30:00Z` | Z instead of +00:00 | `2025-01-15T10:30:00+00:00` |
| `2025-01-15T10:30:00` | Missing timezone | `2025-01-15T10:30:00+00:00` |
| `2025-01-15` | Date only, no time | `2025-01-15T00:00:00+00:00` |
| `10:30:00` | Time only, no date | Today's date + time |
| `Jan 15, 2025` | Human format | `2025-01-15T00:00:00+00:00` |

### Comprehensive Timestamp Coercion

```python
from datetime import datetime, timezone, date
from dateutil import parser as dateutil_parser
import re

def coerce_timestamp(
    value: str,
    default_tz: timezone = timezone.utc,
    allow_date_only: bool = True,
) -> datetime:
    """
    Aggressively coerce various timestamp formats to datetime.

    Pipeline:
    1. Strip whitespace and normalize
    2. Try ISO-8601 parsing (fast path)
    3. Apply common fixes
    4. Fall back to dateutil (slow but flexible)
    5. Ensure timezone-aware result
    """
    if not value or not value.strip():
        raise ToolExecutionError(
            "INVALID_TIMESTAMP",
            "Timestamp cannot be empty",
            data={"example": datetime.now(timezone.utc).isoformat()}
        )

    original = value
    normalized = value.strip()

    # Step 1: Common normalizations
    # Slashes → dashes
    normalized = re.sub(r"(\d{4})/(\d{2})/(\d{2})", r"\1-\2-\3", normalized)

    # Space separator → T
    normalized = re.sub(r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})", r"\1T\2", normalized)

    # Z → +00:00 (Python's fromisoformat doesn't like Z before 3.11)
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    # Step 2: Try fast ISO-8601 parse
    try:
        dt = datetime.fromisoformat(normalized)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=default_tz)
        return dt
    except ValueError:
        pass

    # Step 3: Handle date-only
    if allow_date_only and re.match(r"^\d{4}-\d{2}-\d{2}$", normalized):
        try:
            d = date.fromisoformat(normalized)
            return datetime.combine(d, datetime.min.time(), tzinfo=default_tz)
        except ValueError:
            pass

    # Step 4: Handle time-only (assume today)
    if re.match(r"^\d{2}:\d{2}(:\d{2})?$", normalized):
        try:
            time_part = datetime.strptime(normalized, "%H:%M:%S" if ":" in normalized[3:] else "%H:%M")
            today = date.today()
            return datetime.combine(today, time_part.time(), tzinfo=default_tz)
        except ValueError:
            pass

    # Step 5: Fall back to dateutil (handles "Jan 15, 2025", etc.)
    try:
        dt = dateutil_parser.parse(normalized, fuzzy=True)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=default_tz)
        return dt
    except Exception:
        pass

    # All parsing failed
    raise ToolExecutionError(
        "INVALID_TIMESTAMP",
        f"Could not parse timestamp: '{original}'. "
        f"Expected ISO-8601 format like '2025-01-15T10:30:00+00:00'.",
        recoverable=True,
        data={
            "provided": original,
            "normalized_attempt": normalized,
            "examples": [
                "2025-01-15T10:30:00+00:00",
                "2025-01-15T10:30:00Z",
                "2025-01-15",
            ],
            "common_mistakes": [
                "Missing timezone: Add +00:00 or Z",
                "Wrong separator: Use T between date and time",
                "Slashes: Use dashes (2025-01-15, not 2025/01/15)"
            ]
        }
    )


def format_timestamp_for_response(dt: datetime) -> str:
    """
    Format datetime for JSON response.

    Always uses ISO-8601 with explicit timezone.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()
```

### Timestamp Range Validation

```python
def validate_timestamp_range(
    since: str | None,
    until: str | None,
    max_range_days: int = 365,
) -> tuple[datetime | None, datetime | None]:
    """
    Validate and coerce a timestamp range.

    Returns (since_dt, until_dt) or raises ToolExecutionError.
    """
    since_dt = coerce_timestamp(since) if since else None
    until_dt = coerce_timestamp(until) if until else None

    # Validate range is sensible
    if since_dt and until_dt:
        if since_dt > until_dt:
            raise ToolExecutionError(
                "INVALID_RANGE",
                f"'since' ({since}) is after 'until' ({until}). "
                f"Did you swap them?",
                recoverable=True,
                data={
                    "since": since,
                    "until": until,
                    "fix_hint": "Swap the values or correct the timestamps"
                }
            )

        range_days = (until_dt - since_dt).days
        if range_days > max_range_days:
            raise ToolExecutionError(
                "RANGE_TOO_LARGE",
                f"Time range of {range_days} days exceeds maximum of {max_range_days}. "
                f"Use a narrower range or paginate.",
                recoverable=True,
                data={
                    "range_days": range_days,
                    "max_days": max_range_days
                }
            )

    return since_dt, until_dt
```

---

## FTS5 Query Sanitization

SQLite FTS5 has specific syntax requirements. Agents often get these wrong.

### FTS5 Pitfalls

| Agent Input | Problem | Result |
|-------------|---------|--------|
| `*` | Bare wildcard | Matches nothing |
| `*error` | Leading wildcard | Full table scan (slow) |
| `"unclosed quote` | Unbalanced quotes | Syntax error |
| `AND OR` | Bare operators | Syntax error |
| `fix(bug)` | Unescaped parens | Interpreted as grouping |
| `:label` | Unescaped colon | Column prefix syntax |

### Comprehensive FTS5 Sanitizer

```python
import re

def sanitize_fts5_query(query: str) -> str | None:
    """
    Sanitize user input for FTS5 MATCH queries.

    Returns sanitized query or None if query is effectively empty.

    Pipeline:
    1. Handle empty/whitespace-only
    2. Strip leading wildcards (cause full scan)
    3. Handle bare wildcards
    4. Balance quotes
    5. Escape special characters (unless intentional)
    6. Validate result
    """
    if not query:
        return None

    sanitized = query.strip()

    if not sanitized:
        return None

    # Step 1: Bare wildcard → no results
    if sanitized == "*":
        return None

    # Step 2: Strip leading wildcards (cause full table scan)
    # "*error" → "error"
    original_len = len(sanitized)
    while sanitized.startswith("*"):
        sanitized = sanitized[1:].lstrip()

    if not sanitized:
        return None

    # Step 3: Balance quotes
    # 'unclosed "quote' → 'unclosed quote'
    quote_count = sanitized.count('"')
    if quote_count % 2 != 0:
        # Remove all quotes (conservative approach)
        sanitized = sanitized.replace('"', '')

    # Step 4: Escape special FTS5 characters
    # Unless they're clearly intentional boolean operators
    special_chars = {
        '(': ' ',  # Grouping → space
        ')': ' ',
        ':': ' ',  # Column prefix → space
        '^': ' ',  # Boost → space
    }

    # Keep AND, OR, NOT as operators if uppercase
    # Otherwise escape
    words = sanitized.split()
    processed = []
    for word in words:
        upper = word.upper()
        if upper in ('AND', 'OR', 'NOT') and word == upper:
            # Intentional boolean operator
            processed.append(word)
        else:
            # Escape special chars
            for char, replacement in special_chars.items():
                word = word.replace(char, replacement)
            if word.strip():
                processed.append(word.strip())

    sanitized = ' '.join(processed)

    # Step 5: Final validation
    if not sanitized or sanitized.isspace():
        return None

    # Check for dangerous patterns
    if re.match(r'^(AND|OR|NOT)\s*$', sanitized, re.IGNORECASE):
        # Bare boolean operator
        return None

    return sanitized


def build_fts5_query(
    terms: list[str],
    mode: str = "all",  # "all", "any", "phrase"
) -> str | None:
    """
    Build FTS5 query from search terms.

    Parameters
    ----------
    terms : list[str]
        Search terms
    mode : str
        - "all": All terms must match (AND)
        - "any": Any term matches (OR)
        - "phrase": Exact phrase match

    Returns
    -------
    str | None
        FTS5 query string or None if no valid terms
    """
    # Sanitize each term
    clean_terms = []
    for term in terms:
        sanitized = sanitize_fts5_query(term)
        if sanitized:
            clean_terms.append(sanitized)

    if not clean_terms:
        return None

    if mode == "phrase":
        # Quote for exact phrase
        return f'"{" ".join(clean_terms)}"'
    elif mode == "any":
        return " OR ".join(clean_terms)
    else:  # "all" is default
        return " AND ".join(clean_terms)
```

### FTS5 Search Implementation

```python
def search_messages(
    project_key: str,
    query: str,
    limit: int = 20,
    offset: int = 0,
) -> list[dict]:
    """
    Full-text search over message subjects and bodies.

    Query syntax (after sanitization):
    - Simple terms: error log
    - Phrases: "build plan"
    - Prefix: migrat* (matches migration, migrating, etc.)
    - Boolean: plan AND users
    - Negation: error NOT warning

    Returns messages sorted by relevance (bm25 score).
    """
    sanitized = sanitize_fts5_query(query)

    if not sanitized:
        # Return empty results, not error
        return []

    try:
        results = db.execute("""
            SELECT
                m.id,
                m.subject,
                m.sender_name,
                m.created_ts,
                m.importance,
                m.thread_id,
                snippet(messages_fts, 0, '<mark>', '</mark>', '...', 32) as subject_snippet,
                snippet(messages_fts, 1, '<mark>', '</mark>', '...', 64) as body_snippet,
                bm25(messages_fts) as relevance
            FROM messages m
            JOIN messages_fts ON m.id = messages_fts.rowid
            WHERE messages_fts MATCH :query
            AND m.project_key = :project_key
            ORDER BY bm25(messages_fts)
            LIMIT :limit OFFSET :offset
        """, {
            "query": sanitized,
            "project_key": project_key,
            "limit": limit,
            "offset": offset
        })

        return [
            {
                "id": r.id,
                "subject": r.subject,
                "subject_snippet": r.subject_snippet,
                "body_snippet": r.body_snippet,
                "from": r.sender_name,
                "created_ts": r.created_ts.isoformat(),
                "importance": r.importance,
                "thread_id": r.thread_id,
                "relevance_score": abs(r.relevance)  # bm25 returns negative
            }
            for r in results
        ]

    except Exception as e:
        # FTS5 syntax error - return helpful message
        if "fts5: syntax error" in str(e).lower():
            raise ToolExecutionError(
                "SEARCH_SYNTAX_ERROR",
                f"Invalid search query syntax. Your query '{query}' "
                f"(sanitized to '{sanitized}') contains invalid FTS5 syntax.",
                recoverable=True,
                data={
                    "original_query": query,
                    "sanitized_query": sanitized,
                    "examples": [
                        "error log (simple terms)",
                        '"build plan" (exact phrase)',
                        "migrat* (prefix match)",
                        "error AND NOT warning (boolean)"
                    ]
                }
            )
        raise
```

### FTS5 Query Examples

```python
# Good queries (after sanitization)
"build plan"          # → Phrase search
"error NOT warning"   # → Boolean negation
"migrat*"             # → Prefix match
"api AND endpoint"    # → Boolean AND
"user OR admin"       # → Boolean OR

# Bad queries → sanitization results
"*"                   # → None (empty)
"*error"              # → "error" (leading wildcard stripped)
'"unclosed'           # → "unclosed" (quotes removed)
"(test)"              # → "test" (parens removed)
"AND"                 # → None (bare operator)
":column"             # → "column" (colon removed)
```

---

## Thread ID Validation

Thread IDs have specific format requirements.

```python
import re

# Valid thread ID patterns
THREAD_ID_PATTERN = re.compile(r'^[A-Za-z0-9_-]{1,64}$')

def validate_thread_id(
    value: str,
    mode: EnforcementMode = EnforcementMode.COERCE,
) -> str:
    """
    Validate and normalize thread ID.

    Valid format: alphanumeric with underscores and hyphens, 1-64 chars.
    Examples: TKT-123, auth_refactor, uuid-v4-here
    """
    if not value or not value.strip():
        raise ToolExecutionError(
            "INVALID_THREAD_ID",
            "Thread ID cannot be empty",
            data={"example": "TKT-123"}
        )

    normalized = value.strip()

    # Remove common prefixes agents might add
    for prefix in ['thread:', 'id:', '#']:
        if normalized.lower().startswith(prefix):
            normalized = normalized[len(prefix):].strip()

    # Replace spaces with hyphens
    if mode == EnforcementMode.COERCE:
        normalized = re.sub(r'\s+', '-', normalized)

    # Remove invalid characters
    if mode == EnforcementMode.COERCE:
        normalized = re.sub(r'[^A-Za-z0-9_-]', '', normalized)

    # Truncate if too long
    if len(normalized) > 64:
        if mode == EnforcementMode.COERCE:
            normalized = normalized[:64]
        else:
            raise ToolExecutionError(
                "INVALID_THREAD_ID",
                f"Thread ID exceeds 64 character limit (got {len(value)})",
                data={"provided": value, "length": len(value)}
            )

    # Final validation
    if not normalized:
        raise ToolExecutionError(
            "INVALID_THREAD_ID",
            f"Thread ID '{value}' contains no valid characters after sanitization",
            data={"provided": value, "sanitized": ""}
        )

    if not THREAD_ID_PATTERN.match(normalized):
        raise ToolExecutionError(
            "INVALID_THREAD_ID",
            f"Thread ID '{normalized}' contains invalid characters. "
            f"Use only letters, numbers, underscores, and hyphens.",
            data={
                "provided": value,
                "sanitized": normalized,
                "pattern": "alphanumeric, underscore, hyphen only"
            }
        )

    return normalized
```
