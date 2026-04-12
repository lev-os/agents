# Mistake Detection Patterns

## Table of Contents
- [Philosophy](#philosophy)
- [The Detection System](#the-detection-system)
- [Detector Implementations](#detector-implementations)
- [Placeholder Detection](#placeholder-detection)
- [Suspicious Pattern Detection](#suspicious-pattern-detection)
- [Integration Points](#integration-points)
- [Testing Mistake Detectors](#testing-mistake-detectors)

---

## Philosophy

**Detect what agents MEANT, not just what they said.**

When an agent passes `name="claude-code"`, they didn't randomly type that. They:
1. Understood they needed to identify themselves
2. Chose their program name as an identifier
3. Expected it to work

The system should recognize this intent and guide them to the correct approach.

---

## The Detection System

```python
def _detect_mistake(value: str) -> tuple[str, str] | None:
    """
    Detect common mistakes when agents provide invalid values.

    Returns:
        (error_type, helpful_message) if mistake detected
        None if no obvious mistake
    """
    if _looks_like_program_name(value):
        return ("PROGRAM_NAME_AS_AGENT", _program_name_message(value))

    if _looks_like_model_name(value):
        return ("MODEL_NAME_AS_AGENT", _model_name_message(value))

    if _looks_like_email(value):
        return ("EMAIL_AS_AGENT", _email_message(value))

    if _looks_like_broadcast(value):
        return ("BROADCAST_ATTEMPT", _broadcast_message(value))

    if _looks_like_descriptive_name(value):
        return ("DESCRIPTIVE_NAME", _descriptive_name_message(value))

    if _looks_like_unix_username(value):
        return ("UNIX_USERNAME_AS_AGENT", _unix_username_message(value))

    return None
```

---

## Detector Implementations

### 1. Program Name Detection

```python
_KNOWN_PROGRAM_NAMES: frozenset[str] = frozenset({
    # Anthropic
    "claude-code", "claude",
    # OpenAI
    "codex-cli", "codex",
    # Editors/IDEs
    "cursor", "windsurf", "cline", "aider",
    "copilot", "github-copilot",
    # Google
    "gemini-cli", "gemini",
    # Others
    "opencode", "vscode", "neovim", "vim", "emacs", "zed", "continue",
    "bolt", "replit", "v0", "devin",
})


def _looks_like_program_name(value: str) -> bool:
    """Check if value looks like a program name (not a valid agent name)."""
    return value.lower().strip() in _KNOWN_PROGRAM_NAMES


def _program_name_message(value: str) -> str:
    return (
        f"'{value}' looks like a program name, not an agent name. "
        f"Agent names must be adjective+noun combinations like 'BlueLake' or 'GreenCastle'. "
        f"Use the 'program' parameter for program names, and omit 'name' to auto-generate "
        f"a valid agent name."
    )
```

### 2. Model Name Detection

```python
_MODEL_NAME_PATTERNS: tuple[str, ...] = (
    # OpenAI
    "gpt-", "gpt4", "gpt3", "o1-", "o3-",
    # Anthropic
    "claude-", "opus", "sonnet", "haiku",
    # Google
    "gemini-", "palm",
    # Meta
    "llama",
    # Mistral
    "mistral", "codestral", "mixtral",
    # Others
    "qwen", "deepseek", "phi-",
)


def _looks_like_model_name(value: str) -> bool:
    """Check if value looks like a model name (not a valid agent name)."""
    v = value.lower().strip()
    return any(pattern in v for pattern in _MODEL_NAME_PATTERNS)


def _model_name_message(value: str) -> str:
    return (
        f"'{value}' looks like a model name, not an agent name. "
        f"Agent names must be adjective+noun combinations like 'RedStone' or 'PurpleBear'. "
        f"Use the 'model' parameter for model names, and omit 'name' to auto-generate "
        f"a valid agent name."
    )
```

### 3. Email Detection

```python
def _looks_like_email(value: str) -> bool:
    """Check if value looks like an email address."""
    return "@" in value and "." in value.split("@")[-1]


def _email_message(value: str) -> str:
    return (
        f"'{value}' looks like an email address. Agent names are simple identifiers "
        f"like 'BlueDog', not email addresses. Check the 'to' parameter format."
    )
```

### 4. Broadcast Detection

```python
_BROADCAST_KEYWORDS: frozenset[str] = frozenset({
    "all", "*", "everyone", "broadcast", "@all", "@everyone",
    "team", "channel", "group", "everybody",
})


def _looks_like_broadcast(value: str) -> bool:
    """Check if value looks like a broadcast attempt."""
    return value.lower().strip() in _BROADCAST_KEYWORDS


def _broadcast_message(value: str) -> str:
    return (
        f"'{value}' looks like a broadcast attempt. Agent Mail doesn't support "
        f"broadcasting to all agents. List specific recipient agent names in the 'to' "
        f"parameter. This design is intentional: targeted communication prevents "
        f"context waste and noise."
    )
```

### 5. Descriptive Name Detection

```python
_DESCRIPTIVE_SUFFIXES: tuple[str, ...] = (
    # Role-based
    "agent", "bot", "assistant", "helper",
    # Management
    "manager", "coordinator", "orchestrator",
    # Technical roles
    "developer", "engineer", "architect",
    # Actions
    "migrator", "refactorer", "fixer", "builder",
    "harmonizer", "integrator", "optimizer", "analyzer",
    # Workers
    "worker", "runner", "handler", "processor",
)


def _looks_like_descriptive_name(value: str) -> bool:
    """Check if value looks like a descriptive role name instead of adjective+noun."""
    v = value.lower()
    return any(v.endswith(suffix) for suffix in _DESCRIPTIVE_SUFFIXES)


def _descriptive_name_message(value: str) -> str:
    return (
        f"'{value}' looks like a descriptive role name. Agent names must be randomly "
        f"generated adjective+noun combinations like 'WhiteMountain' or 'BrownCreek', "
        f"NOT descriptive of the agent's task. The purpose is memorable, unique identifiers—"
        f"not role descriptions. Omit the 'name' parameter to auto-generate a valid name."
    )
```

### 6. Unix Username Detection

```python
def _looks_like_unix_username(value: str) -> bool:
    """
    Check if value looks like a Unix username rather than adjective+noun.

    Unix usernames typically:
    - All lowercase
    - 3-16 characters
    - Alphanumeric only
    - Not matching our adjective/noun wordlists
    """
    v = value.strip()

    if not v:
        return False

    # Agent names are PascalCase; usernames are lowercase
    if v.islower() and v.isalnum() and 2 <= len(v) <= 16:
        # Check it's not in our valid wordlists
        if v not in ADJECTIVES_LOWER and v not in NOUNS_LOWER:
            return True

    return False


def _unix_username_message(value: str) -> str:
    return (
        f"'{value}' looks like a Unix username (possibly from $USER environment variable). "
        f"Agent names must be adjective+noun combinations like 'BlueLake' or 'GreenCastle'. "
        f"When you called register_agent, the system generated a valid name for you. "
        f"To find your actual agent name, check the response from register_agent or use "
        f"resource://agents/{{project_key}} to list all registered agents in this project."
    )
```

---

## Placeholder Detection

Catch unconfigured integrations:

```python
_PROJECT_PLACEHOLDERS: tuple[str, ...] = (
    "YOUR_PROJECT",
    "YOUR_PROJECT_PATH",
    "YOUR_PROJECT_KEY",
    "PROJECT_KEY",
    "PLACEHOLDER",
    "<PROJECT>",
    "{PROJECT}",
    "$PROJECT",
    "${PROJECT}",
    "PATH_TO_PROJECT",
    "/path/to/project",
)

_AGENT_PLACEHOLDERS: tuple[str, ...] = (
    "YOUR_AGENT",
    "YOUR_AGENT_NAME",
    "AGENT_NAME",
    "YOUR_NAME",
    "<AGENT>",
    "{AGENT}",
    "$AGENT",
    "${AGENT_NAME}",
)


def _detect_placeholder(value: str, param_type: str = "project") -> str | None:
    """
    Detect placeholder values that indicate unconfigured integration.

    Returns error message if placeholder detected, None otherwise.
    """
    upper = value.upper().strip()
    placeholders = _PROJECT_PLACEHOLDERS if param_type == "project" else _AGENT_PLACEHOLDERS

    for pattern in placeholders:
        if pattern.upper() in upper or upper == pattern.upper():
            return (
                f"Detected placeholder value '{value}' instead of a real {param_type}. "
                f"This typically means a hook or integration script hasn't been configured yet. "
                f"Replace placeholder values with your actual {param_type}."
            )

    return None
```

**Usage:**

```python
async def validate_project_key(identifier: str) -> Project:
    placeholder_error = _detect_placeholder(identifier, "project")
    if placeholder_error:
        raise ToolExecutionError(
            "CONFIGURATION_ERROR",
            placeholder_error,
            recoverable=True,
            data={
                "parameter": "project_key",
                "provided": identifier,
                "fix_hint": "Update AGENT_MAIL_PROJECT or project_key in your configuration",
                "example_valid": "/data/projects/backend"
            }
        )
    # ... continue validation
```

---

## Suspicious Pattern Detection

Catch overly broad or dangerous inputs:

### File Reservation Patterns

```python
_OVERLY_BROAD_PATTERNS: frozenset[str] = frozenset({
    "*", "**", "**/*", "**/**", ".", "..", "./", "../",
})


def _detect_suspicious_file_reservation(pattern: str) -> str | None:
    """
    Detect suspicious file reservation patterns that might be too broad.

    Returns warning message or None if pattern looks reasonable.
    """
    p = pattern.strip()

    # Catch overly broad patterns
    if p in _OVERLY_BROAD_PATTERNS:
        return (
            f"Pattern '{p}' is too broad and would reserve the entire project. "
            f"Use more specific patterns like 'src/api/*.py' or 'lib/auth/**'. "
            f"Broad reservations block other agents unnecessarily."
        )

    # Catch absolute paths (should be project-relative)
    if p.startswith("/") and not p.startswith("//"):
        return (
            f"Pattern '{p}' looks like an absolute path. File reservation patterns "
            f"should be project-relative (e.g., 'src/module.py' not '{p}'). "
            f"The system automatically resolves patterns relative to the project root."
        )

    # Warn about very short wildcards
    if len(p) <= 2 and "*" in p:
        return (
            f"Pattern '{p}' is very short and may match more files than intended. "
            f"Consider using a more specific pattern like 'src/*.py'."
        )

    # Catch home directory patterns
    if p.startswith("~") or p.startswith("$HOME"):
        return (
            f"Pattern '{p}' references home directory. File reservations must be "
            f"project-relative. Use paths like 'config/settings.yaml' instead."
        )

    return None
```

### Thread ID Patterns

```python
import re

_THREAD_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def _detect_suspicious_thread_id(thread_id: str) -> str | None:
    """Detect invalid or suspicious thread IDs."""

    if not thread_id or not thread_id.strip():
        return "Thread ID cannot be empty."

    t = thread_id.strip()

    if not _THREAD_ID_RE.fullmatch(t):
        return (
            f"Thread ID '{t}' contains invalid characters. "
            f"Thread IDs must start with alphanumeric, contain only [A-Za-z0-9._-], "
            f"and be at most 128 characters. Example: 'TASK-123', 'br-456'."
        )

    # Warn about overly generic IDs
    generic_ids = {"thread", "main", "default", "general", "misc", "other"}
    if t.lower() in generic_ids:
        return (
            f"Thread ID '{t}' is very generic. Consider using specific identifiers "
            f"like task numbers (TASK-123) or feature names (auth-refactor) "
            f"for better organization."
        )

    return None
```

---

## Integration Points

### In Parameter Validation

```python
async def validate_agent_registration(
    project_key: str,
    name: str | None,
    program: str,
    model: str,
    mode: str = "coerce",
) -> dict:
    """Validate registration parameters with mistake detection."""

    # Check project_key
    placeholder = _detect_placeholder(project_key, "project")
    if placeholder:
        raise ToolExecutionError("CONFIGURATION_ERROR", placeholder, ...)

    # Check program
    if not program or not program.strip():
        raise ToolExecutionError("EMPTY_PROGRAM", "Program parameter is required.", ...)

    # Check model
    if not model or not model.strip():
        raise ToolExecutionError("EMPTY_MODEL", "Model parameter is required.", ...)

    # Check name (if provided)
    if name:
        mistake = _detect_mistake(name)
        if mistake:
            if mode == "strict":
                raise ToolExecutionError(mistake[0], mistake[1], ...)
            # coerce mode: will auto-generate instead
            name = None

    return {"project_key": project_key, "name": name, "program": program, "model": model}
```

### In Message Sending

```python
async def validate_recipients(to: list[str], project: Project) -> list[Agent]:
    """Validate recipients with mistake detection."""

    agents = []

    for recipient in to:
        # Check for mistakes
        mistake = _detect_mistake(recipient)
        if mistake:
            raise ToolExecutionError(
                mistake[0],
                f"Invalid recipient '{recipient}': {mistake[1]}",
                data={
                    "recipient": recipient,
                    "available_agents": await list_agent_names(project)
                }
            )

        # Lookup agent
        agent = await get_agent(project, recipient)
        if not agent:
            # Provide suggestions
            suggestions = await find_similar_agents(project, recipient)
            raise ToolExecutionError(
                "NOT_FOUND",
                f"Recipient '{recipient}' not found. Did you mean: {suggestions}?",
                data={"suggestions": suggestions}
            )

        agents.append(agent)

    return agents
```

---

## Testing Mistake Detectors

```python
import pytest
from your_module import (
    _looks_like_program_name,
    _looks_like_model_name,
    _looks_like_email,
    _looks_like_broadcast,
    _looks_like_descriptive_name,
    _looks_like_unix_username,
    _detect_mistake,
    _detect_suspicious_file_reservation,
)


class TestProgramNameDetection:
    """Tests for program name detection."""

    def test_known_programs_detected(self):
        programs = ["claude-code", "codex-cli", "cursor", "copilot"]
        for prog in programs:
            assert _looks_like_program_name(prog), f"Should detect '{prog}'"

    def test_case_insensitive(self):
        assert _looks_like_program_name("CLAUDE-CODE")
        assert _looks_like_program_name("Claude")

    def test_valid_names_not_detected(self):
        valid = ["BlueLake", "GreenCastle", "RedStone"]
        for name in valid:
            assert not _looks_like_program_name(name), f"'{name}' should not match"


class TestBroadcastDetection:
    """Tests for broadcast attempt detection."""

    def test_broadcast_keywords(self):
        broadcasts = ["all", "*", "everyone", "@all", "@everyone"]
        for b in broadcasts:
            assert _looks_like_broadcast(b), f"Should detect '{b}'"

    def test_valid_recipients_not_detected(self):
        assert not _looks_like_broadcast("BlueLake")
        assert not _looks_like_broadcast("all-hands")  # Not exact match


class TestSuspiciousFileReservation:
    """Tests for suspicious file pattern detection."""

    def test_overly_broad(self):
        for pattern in ["*", "**", "**/*", "."]:
            result = _detect_suspicious_file_reservation(pattern)
            assert result is not None, f"Should flag '{pattern}'"
            assert "too broad" in result.lower()

    def test_absolute_paths(self):
        result = _detect_suspicious_file_reservation("$HOME/project/src")
        assert result is not None
        assert "absolute path" in result.lower()

    def test_valid_patterns_pass(self):
        valid = ["src/api/*.py", "lib/auth/**", "config/settings.yaml"]
        for pattern in valid:
            result = _detect_suspicious_file_reservation(pattern)
            assert result is None, f"'{pattern}' should be valid"
```
