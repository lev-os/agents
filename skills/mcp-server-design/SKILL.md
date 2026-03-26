---
name: mcp-server-design
description: >-
  Design agent-friendly MCP servers with optimal UX. Use when building MCP tools,
  designing agent APIs, writing tool documentation, implementing error handling,
  or creating multi-agent coordination systems.
---

# MCP Server Design

> **Core Insight:** Agents are NOT humans. Design for "agent theory of mind"—anticipate how agents will misuse, misunderstand, or misapply your tools, then build systems that guide them toward success rather than simply rejecting errors.

> **Why MCP?** "Once you have something expressed as an MCP server it makes it easy to use with an LLM in a plug-and-play, self-documented way." — MCP provides standardized tool discovery and invocation.

## The One Rule

**Make the wrong thing impossible and the right thing obvious.**

Every design decision should pass: "If an agent makes an obvious mistake, does this educate them or just fail?"

---

## The 12 Core Principles

| # | Principle | Implementation |
|---|-----------|----------------|
| 1 | **Anticipate Intent** | Detect what agents MEANT, not just what they said |
| 2 | **Fail Helpfully** | Structured errors with suggestions, not stack traces |
| 3 | **Intercept Early** | Catch mistakes at environment level before tool calls |
| 4 | **Forgive by Default** | Auto-correct invalid inputs; educate in strict mode |
| 5 | **Document for Agents** | Do/Don't sections, examples, discovery hints |
| 6 | **Scope Narrowly** | No broadcast; force explicit, targeted actions |
| 7 | **Provide Macros** | Bundle common multi-step workflows for reliability |
| 8 | **Precision Over Breadth** | ≤7 tools per cluster; capability gating reduces context 70% |
| 9 | **Workflow-First Design** | Guide agents through multi-step tasks with next_actions |
| 10 | **Defense in Depth** | XSS sanitization, path traversal prevention, EMFILE recovery |
| 11 | **Full Observability** | Query tracking, slow query detection, cost logging |
| 12 | **Graceful Degradation** | Suggested tool calls in errors, concurrent creation idempotency |

---

## THE PROMPT

```
Design an MCP server for [DOMAIN/PURPOSE].

Requirements:
- Tool cluster: [main operations]
- Target agents: [Claude Code, Codex, Gemini CLI, etc.]
- Coordination needs: [single-agent/multi-agent]

Follow mcp-server-design patterns:
1. Define mistake detection for common errors
2. Create structured error types with recovery hints
3. Write agent-friendly tool documentation
4. Implement input normalization and auto-correction
5. Design resources for discovery
6. Add validation scripts

Run checklist before finalizing.
```

---

## Quick Reference: 65+ Design Patterns

### Architecture Patterns

| Pattern | Description | Reference |
|---------|-------------|-----------|
| **Taxonomy-Driven Tools** | ≤7 tools per cluster; larger menus degrade success 85% | [TOOL-DOCUMENTATION.md](references/TOOL-DOCUMENTATION.md) |
| **Dual Persistence** | Git (human-auditable) + SQLite FTS5 (queryable) | [GIT-INTEGRATION.md](references/GIT-INTEGRATION.md) |
| **Async Message Passing** | Non-blocking poll-based coordination | [MULTI-AGENT-COORDINATION.md](references/MULTI-AGENT-COORDINATION.md) |
| **Advisory File Reservations** | TTL-based leases with conflict detection | [MULTI-AGENT-COORDINATION.md](references/MULTI-AGENT-COORDINATION.md) |
| **Identity Precedence** | project_uid vs slug separation | [GIT-INTEGRATION.md](references/GIT-INTEGRATION.md) |
| **Capability Gating** | ~70% context reduction for minimal profiles | [TOOL-FILTERING.md](references/TOOL-FILTERING.md) |
| **Product Bus Pattern** | Cross-project organization via ProductProjectLink | [MULTI-AGENT-COORDINATION.md](references/MULTI-AGENT-COORDINATION.md) |
| **Build Slots System** | Coarse concurrency control for builds/deploys | [MULTI-AGENT-COORDINATION.md](references/MULTI-AGENT-COORDINATION.md) |
| **Settings Hierarchy** | 100+ config options, frozen dataclasses, env cascade | [VALIDATION-PATTERNS.md](references/VALIDATION-PATTERNS.md) |

### Error Handling Patterns

| Pattern | Description | Reference |
|---------|-------------|-----------|
| **ToolExecutionError** | Structured errors with type/message/recoverable/data | [ERROR-DESIGN.md](references/ERROR-DESIGN.md) |
| **Exception Mapping** | SQLAlchemy → NOT_FOUND, TypeError → hints | [ERROR-DESIGN.md](references/ERROR-DESIGN.md) |
| **Fuzzy Suggestions** | SequenceMatcher for typo recovery | [ERROR-DESIGN.md](references/ERROR-DESIGN.md) |
| **EMFILE Recovery** | Whitelist safe-to-retry tools, clear caches | [ERROR-DESIGN.md](references/ERROR-DESIGN.md) |
| **Suggested Tool Calls** | `recoverable=True` + `suggested_tool_calls` payload | [ERROR-DESIGN.md](references/ERROR-DESIGN.md) |
| **IntegrityError Idempotency** | Concurrent creation returns existing record | [ERROR-DESIGN.md](references/ERROR-DESIGN.md) |
| **Stale Resource Release** | Multi-dimensional heuristics for abandoned reservations | [ERROR-DESIGN.md](references/ERROR-DESIGN.md) |

### Validation Patterns

| Pattern | Description | Reference |
|---------|-------------|-----------|
| **Three Enforcement Modes** | strict/coerce/always_auto | [VALIDATION-PATTERNS.md](references/VALIDATION-PATTERNS.md) |
| **Mistake Detection** | 6 detectors: program/model/email/broadcast/descriptive/unix | [MISTAKE-DETECTION.md](references/MISTAKE-DETECTION.md) |
| **Placeholder Detection** | YOUR_PROJECT, $PROJECT, etc. | [MISTAKE-DETECTION.md](references/MISTAKE-DETECTION.md) |
| **FTS5 Sanitization** | Strip leading wildcards, convert bare * to None | [VALIDATION-PATTERNS.md](references/VALIDATION-PATTERNS.md) |
| **Timestamp Coercion** | Auto-convert Z → +00:00, slashes → dashes | [VALIDATION-PATTERNS.md](references/VALIDATION-PATTERNS.md) |
| **Pre-computed Sets** | O(1) validation via frozenset | [VALIDATION-PATTERNS.md](references/VALIDATION-PATTERNS.md) |

### Agent UX Patterns

| Pattern | Description | Reference |
|---------|-------------|-----------|
| **Fake CLI Stub** | Intercept shell invocations, explain MCP usage | [INSTALLATION-PATTERNS.md](references/INSTALLATION-PATTERNS.md) |
| **No Broadcast** | Explicit rejection with philosophy explanation | [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md) |
| **Macro Tools** | Bundle multi-step workflows | [TOOL-DOCUMENTATION.md](references/TOOL-DOCUMENTATION.md) |
| **next_actions Hints** | Guide agents to follow-up actions | [TOOL-DOCUMENTATION.md](references/TOOL-DOCUMENTATION.md) |
| **14+ Resources** | Discovery mechanisms for every entity type | [RESOURCE-DESIGN.md](references/RESOURCE-DESIGN.md) |

### Git Integration Patterns

| Pattern | Description | Reference |
|---------|-------------|-----------|
| **Context Manager Cleanup** | Prevent FD leaks with `with _git_repo()` | [GIT-INTEGRATION.md](references/GIT-INTEGRATION.md) |
| **LRU Repo Cache** | Size-limited cache with eviction cleanup | [GIT-INTEGRATION.md](references/GIT-INTEGRATION.md) |
| **Commit Info Extraction** | hexsha, summary, insertions/deletions, diff hunks | [GIT-INTEGRATION.md](references/GIT-INTEGRATION.md) |
| **Identity Resolution** | 4 modes: dir, git-remote, git-toplevel, git-common-dir | [GIT-INTEGRATION.md](references/GIT-INTEGRATION.md) |
| **Composable Hooks** | Chain-runner preserves existing Husky/pre-commit | [INSTALLATION-PATTERNS.md](references/INSTALLATION-PATTERNS.md) |

### Query Optimization Patterns

| Pattern | Description | Reference |
|---------|-------------|-----------|
| **N+1 Elimination** | Batch fetch with GROUP BY | [QUERY-OPTIMIZATION.md](references/QUERY-OPTIMIZATION.md) |
| **JOIN Aliasing** | `aliased(Agent)` for self-joins | [QUERY-OPTIMIZATION.md](references/QUERY-OPTIMIZATION.md) |
| **Query Tracking** | Context-var based per-request stats | [QUERY-OPTIMIZATION.md](references/QUERY-OPTIMIZATION.md) |
| **Slow Query Detection** | Configurable thresholds with logging | [QUERY-OPTIMIZATION.md](references/QUERY-OPTIMIZATION.md) |

### Installation Patterns

| Pattern | Description | Reference |
|---------|-------------|-----------|
| **Multi-Agent Discovery** | Auto-detect Claude/Codex/Cursor/Gemini/Copilot/Aider/etc | [INSTALLATION-PATTERNS.md](references/INSTALLATION-PATTERNS.md) |
| **Token Cascade** | env → .env → generate → fallback | [INSTALLATION-PATTERNS.md](references/INSTALLATION-PATTERNS.md) |
| **Atomic File Writes** | mktemp + mv for safe config updates | [INSTALLATION-PATTERNS.md](references/INSTALLATION-PATTERNS.md) |
| **Hook Injection** | SessionStart/PreToolUse/PostToolUse lifecycle hooks | [INSTALLATION-PATTERNS.md](references/INSTALLATION-PATTERNS.md) |
| **Rate-Limited Polling** | Inbox checks with timestamp files | [INSTALLATION-PATTERNS.md](references/INSTALLATION-PATTERNS.md) |
| **Shared Bash Library** | lib.sh (18KB) with reusable functions | [OPERATIONAL-PATTERNS.md](references/OPERATIONAL-PATTERNS.md) |
| **Per-IDE Integration** | Separate scripts for each coding agent | [OPERATIONAL-PATTERNS.md](references/OPERATIONAL-PATTERNS.md) |
| **Pre-commit Guard** | Git hooks for coordination validation | [OPERATIONAL-PATTERNS.md](references/OPERATIONAL-PATTERNS.md) |

### Database Patterns

| Pattern | Description | Reference |
|---------|-------------|-----------|
| **Query Tracking** | Context-var based per-request stats | [DATABASE-PATTERNS.md](references/DATABASE-PATTERNS.md) |
| **Slow Query Detection** | Configurable thresholds with logging | [DATABASE-PATTERNS.md](references/DATABASE-PATTERNS.md) |
| **Lock Retry with Backoff** | Exponential backoff + ±25% jitter | [DATABASE-PATTERNS.md](references/DATABASE-PATTERNS.md) |
| **SQLite Optimization** | WAL mode, busy_timeout, synchronous=NORMAL | [DATABASE-PATTERNS.md](references/DATABASE-PATTERNS.md) |
| **FTS5 Auto-Sync Triggers** | Automatic full-text index maintenance | [DATABASE-PATTERNS.md](references/DATABASE-PATTERNS.md) |
| **8 Core Tables** | Project, Agent, Message, Recipient, Thread, FileReservation, AgentLink, Product | [DATABASE-PATTERNS.md](references/DATABASE-PATTERNS.md) |

### LLM Integration Patterns

| Pattern | Description | Reference |
|---------|-------------|-----------|
| **Dual-Mode Summarization** | Single thread detail vs multi-thread aggregate | [LLM-INTEGRATION.md](references/LLM-INTEGRATION.md) |
| **Model Alias Resolution** | Map nicknames to canonical model IDs | [LLM-INTEGRATION.md](references/LLM-INTEGRATION.md) |
| **Provider Environment Bridge** | GEMINI_API_KEY → GOOGLE_API_KEY mapping | [LLM-INTEGRATION.md](references/LLM-INTEGRATION.md) |
| **Cost Logging Callbacks** | Token usage and cost tracking | [LLM-INTEGRATION.md](references/LLM-INTEGRATION.md) |
| **LLM Refinement Mode** | JSON parsing with fallback heuristics | [LLM-INTEGRATION.md](references/LLM-INTEGRATION.md) |

### Testing Patterns

| Pattern | Description | Reference |
|---------|-------------|-----------|
| **Haiku Canary Tests** | Validate APIs with smaller models | [TESTING-PATTERNS.md](references/TESTING-PATTERNS.md) |
| **XSS Corpus Testing** | 13 attack categories (script, event, protocol, etc) | [TESTING-PATTERNS.md](references/TESTING-PATTERNS.md) |
| **Path Traversal Prevention** | Security tests for directory escape | [TESTING-PATTERNS.md](references/TESTING-PATTERNS.md) |
| **Time Travel Testing** | Timestamp edge cases (DST, timezone, epoch) | [TESTING-PATTERNS.md](references/TESTING-PATTERNS.md) |
| **Image Processing Edge Cases** | Palette modes, data URIs, format detection | [TESTING-PATTERNS.md](references/TESTING-PATTERNS.md) |
| **Advisory Semantics Tests** | File reservation conflict scenarios | [TESTING-PATTERNS.md](references/TESTING-PATTERNS.md) |

---

## Workflow

### Phase 1: Design
- [ ] **Cluster tools** — Group by workflow (≤7 per cluster)
- [ ] **Define primitives** — Atomic operations that compose
- [ ] **Design macros** — Bundle common multi-step workflows
- [ ] **Plan resources** — Discovery mechanisms for every entity

### Phase 2: Anticipate Failures
- [ ] **List 10 mistakes** — Per tool, how will agents misuse it?
- [ ] **Design detectors** — Program names, broadcast, placeholders
- [ ] **Map exceptions** — SQLAlchemy → structured, TypeError → hints
- [ ] **Plan recovery** — EMFILE retry, concurrent creation retry

### Phase 3: Implement
- [ ] **Structured errors** — ToolExecutionError with data payloads
- [ ] **Input normalization** — Coerce mode auto-corrects
- [ ] **Pre-computed sets** — O(1) validation via frozenset
- [ ] **Query optimization** — Batch fetches, N+1 elimination

### Phase 4: Document
- [ ] **Do/Don't sections** — Behavioral guidance in every docstring
- [ ] **Discovery sections** — How to find parameter values
- [ ] **Examples** — JSON-RPC format with realistic values
- [ ] **Common mistakes** — Pitfall avoidance with fixes

### Phase 5: Install & Integrate
- [ ] **Fake CLI stub** — Catch confused agents
- [ ] **Hook injection** — SessionStart, PreToolUse, PostToolUse
- [ ] **Multi-agent detection** — Auto-discover installed agents
- [ ] **Atomic config writes** — Safe updates with backups

### Phase 6: Validate
- [ ] **Test with Haiku** — Canary for unclear APIs
- [ ] **Test mistake detection** — All detector types
- [ ] **Test error payloads** — Machine-parseable
- [ ] **Test concurrent access** — Race conditions handled

---

## Tool Documentation Template

Every tool MUST have these sections:

```python
"""
Brief one-liner description.

Discovery
---------
How to find required parameter values:
- project_key: Use `pwd` for absolute working directory
- agent_name: Use resource://agents/{project_key}
- thread_id: Use resource://threads/{project_key}

When to use
-----------
- Scenario 1 that triggers this tool
- Scenario 2
- NOT for: scenario that should use different tool

Parameters
----------
param_name : type
    Description. MUST be [constraint]. (RECOMMENDED: [suggestion])

Returns
-------
dict
    {
        field1: type,  # Description
        field2: type,  # Description
        next_actions: list[str]  # Suggested follow-up actions
    }

Do / Don't
----------
Do:
- Specific positive guidance with reason
- Another best practice

Don't:
- Specific anti-pattern with consequence
- Another mistake to avoid

Examples
--------
Basic usage:
```json
{"jsonrpc":"2.0","id":"1","method":"tools/call","params":{"name":"tool_name","arguments":{...}}}
```

Common mistakes
---------------
- Mistake 1: explanation and fix
- Mistake 2: explanation and fix

Idempotency
-----------
- Safe to call multiple times. Returns existing record if already exists.

Edge cases
----------
- If X is empty: [behavior]
- If Y not found: [behavior with suggestions]
"""
```

**Full template:** [TOOL-DOCUMENTATION.md](references/TOOL-DOCUMENTATION.md)

---

## Structured Error Design

```python
class ToolExecutionError(Exception):
    def __init__(
        self,
        error_type: str,           # Machine-parseable category
        message: str,              # Human-readable explanation
        *,
        recoverable: bool = True,  # Should agent retry?
        data: dict = None          # Structured hints
    ):
        self.error_type = error_type
        self.recoverable = recoverable
        self.data = data or {}

    def to_payload(self) -> dict:
        return {
            "error": {
                "type": self.error_type,
                "message": str(self),
                "recoverable": self.recoverable,
                "data": self.data,  # suggestions, fix_hint, available_options
            }
        }
```

**Error types:** BROADCAST_ATTEMPT, PROGRAM_NAME_AS_AGENT, CONFIGURATION_ERROR, NOT_FOUND, INVALID_ARGUMENT, FILE_RESERVATION_CONFLICT, EMFILE, TIMEOUT, etc.

**Deep dive:** [ERROR-DESIGN.md](references/ERROR-DESIGN.md)

---

## Mistake Detection System

Detect what agents MEANT when they make errors:

```python
# Known program names agents confuse with identities
_KNOWN_PROGRAMS = frozenset({
    "claude-code", "codex-cli", "cursor", "copilot", "gemini-cli",
    "aider", "cline", "windsurf", "continue", "bolt", "devin", ...
})

# Model name patterns
_MODEL_PATTERNS = ("gpt-", "claude-", "opus", "sonnet", "haiku", "llama", "mistral", ...)

# Broadcast attempts to intercept
_BROADCAST_KEYWORDS = {"all", "*", "everyone", "@all", "@everyone", "team", "channel"}

# Descriptive suffixes (role-based names)
_DESCRIPTIVE_SUFFIXES = ("agent", "bot", "worker", "handler", "migrator", "harmonizer", ...)

def _detect_mistake(value: str) -> tuple[str, str] | None:
    """Returns (error_type, helpful_message) or None."""
    if value.lower() in _KNOWN_PROGRAMS:
        return ("PROGRAM_NAME_AS_AGENT",
                f"'{value}' is a program name. Use 'program' parameter instead.")
    if any(p in value.lower() for p in _MODEL_PATTERNS):
        return ("MODEL_NAME_AS_AGENT",
                f"'{value}' is a model name. Use 'model' parameter instead.")
    if value.lower() in _BROADCAST_KEYWORDS:
        return ("BROADCAST_ATTEMPT",
                "Broadcast not supported. List specific recipients.")
    if any(value.lower().endswith(s) for s in _DESCRIPTIVE_SUFFIXES):
        return ("DESCRIPTIVE_NAME",
                f"'{value}' looks like a role. Use adjective+noun like 'BlueLake'.")
    # ... more detectors
    return None
```

**Full patterns:** [MISTAKE-DETECTION.md](references/MISTAKE-DETECTION.md)

---

## Input Normalization

Auto-correct instead of rejecting:

```python
# Three enforcement modes
MODES = {
    "strict":      "Reject invalid, return detailed error",
    "coerce":      "Auto-fix invalid, use valid result (DEFAULT)",
    "always_auto": "Ignore user input, always auto-generate",
}

# Normalization examples
def normalize_timestamp(value: str) -> datetime:
    """Smart coercion for timestamps."""
    normalized = value.strip()
    normalized = normalized.replace("/", "-")  # Slashes → dashes
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"  # Z → +00:00
    if not re.search(r"[Z+-]", normalized):
        normalized += "+00:00"  # Add missing timezone
    return datetime.fromisoformat(normalized)

def sanitize_fts_query(query: str) -> str | None:
    """Clean FTS5 queries."""
    # Strip leading wildcards (FTS5 doesn't support *foo)
    query = re.sub(r"^\*+", "", query)
    # Bare wildcards return None (empty results)
    if query in ("*", "**", "."):
        return None
    return query
```

**Deep dive:** [VALIDATION-PATTERNS.md](references/VALIDATION-PATTERNS.md)

---

## The "Fake CLI" Pattern

Agents often confuse MCP servers with CLI tools. Solution:

```bash
#!/usr/bin/env bash
# Install as ~/.local/bin/mcp-agent-mail (and symlinks)

cat <<'MSG'
+=====================================================================+
|   This is NOT a CLI tool!                                           |
|                                                                     |
|   It's an MCP server. Use the MCP tools directly:                   |
|     - mcp__mcp-agent-mail__register_agent                           |
|     - mcp__mcp-agent-mail__send_message                             |
|     - mcp__mcp-agent-mail__fetch_inbox                              |
|                                                                     |
|   WRONG: mcp-agent-mail send --to BlueLake                          |
|   RIGHT: Use MCP tools in your agent                                |
+=====================================================================+
MSG
exit 1
```

Create symlinks for all naming variations:
- `mcp-agent-mail`
- `mcp_agent_mail`
- `mcpagentmail`
- `agentmail`

**Full patterns:** [INSTALLATION-PATTERNS.md](references/INSTALLATION-PATTERNS.md)

---

## Resource Design for Discovery

Agents need to know WHERE to find parameter values:

```python
# 14+ resources for comprehensive discovery
RESOURCES = [
    "resource://projects",                    # List all projects
    "resource://project/{slug}",              # Project + agents
    "resource://agents/{project_key}",        # Discover agents with unread counts
    "resource://file_reservations/{slug}",    # View locks + stale analysis
    "resource://message/{id}",                # Fetch single message
    "resource://thread/{thread_id}",          # List thread messages
    "resource://inbox/{agent}",               # Agent's inbox
    "resource://outbox/{agent}",              # Sent messages
    "resource://views/urgent-unread/{agent}", # Filtered view
    "resource://views/ack-required/{agent}",  # Pending acknowledgements
    "resource://views/acks-stale/{agent}",    # Old unacked messages
    "resource://tooling/metrics",             # Tool call stats
    "resource://tooling/recent",              # Recent activity
    "resource://tooling/capabilities",        # Available capabilities
]
```

**Full patterns:** [RESOURCE-DESIGN.md](references/RESOURCE-DESIGN.md)

---

## Macro Tools for Workflows

Bundle multi-step operations for smaller models:

```python
@mcp.tool
def macro_start_session(project_key: str, program: str, model: str) -> dict:
    """
    Boot a complete session in one call:
    1. ensure_project(project_key)
    2. register_agent(project_key, program, model)
    3. fetch_inbox(project_key, agent_name)

    Returns combined result with next_actions hints.
    """
    project = await ensure_project(project_key)
    agent = await register_agent(project_key, program, model)
    inbox = await fetch_inbox(project_key, agent["name"])

    return {
        "project": project,
        "agent": agent,
        "inbox": inbox,
        "next_actions": [
            "Consider file_reservation_paths before editing",
            "Check inbox for urgent messages",
            "Renew file reservations in 30 minutes if still working"
        ]
    }
```

**Other macros:**
- `macro_prepare_thread` — Join thread with context
- `macro_file_reservation_cycle` — Reserve → work → release
- `macro_contact_handshake` — Request + approve + welcome

---

## No Broadcast Philosophy

> "Not every agent NEEDS to know everything. That would be distracting and waste context space."

**Implementation:**
```python
if recipient.lower() in {"all", "*", "everyone", "@all"}:
    raise ToolExecutionError(
        "BROADCAST_ATTEMPT",
        "Broadcast not supported. List specific recipient names. "
        "This design is intentional: targeted communication is more efficient "
        "and prevents context waste.",
        recoverable=True,
        data={
            "available_recipients": await list_agents(project),
            "philosophy": "Targeted > Broadcast for agent coordination"
        }
    )
```

---

## Git Integration Best Practices

```python
# Context manager prevents FD leaks
@contextmanager
def _git_repo(path: str) -> Generator[Repo, None, None]:
    repo = Repo(path)
    try:
        yield repo
    finally:
        repo.close()

# LRU cache with eviction cleanup
class _LRURepoCache:
    def __init__(self, maxsize: int = 16):
        self._cache = OrderedDict()
        self._maxsize = maxsize

    def get(self, key: str) -> Repo | None:
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None

    def put(self, key: str, repo: Repo) -> None:
        if len(self._cache) >= self._maxsize:
            _, evicted = self._cache.popitem(last=False)
            evicted.close()  # Cleanup!
        self._cache[key] = repo
```

**Full patterns:** [GIT-INTEGRATION.md](references/GIT-INTEGRATION.md)

---

## Checklist: Before Shipping

### Error Handling
- [ ] Every error has `error_type`, `message`, `recoverable`, `data`
- [ ] `data` includes suggestions, fix_hint, available_options
- [ ] Fuzzy matching suggests alternatives on NOT_FOUND
- [ ] Mistake detectors catch program/model/broadcast/descriptive names
- [ ] Exception mapping for SQLAlchemy, TypeError, KeyError
- [ ] EMFILE recovery with safe-to-retry whitelist

### Documentation
- [ ] Every tool has Do/Don't section
- [ ] Every tool has Examples with JSON-RPC format
- [ ] Every tool has Discovery section
- [ ] Common mistakes documented with fixes
- [ ] next_actions hints in macro returns

### Input Handling
- [ ] coerce mode auto-corrects invalid inputs
- [ ] strict mode provides detailed guidance
- [ ] Placeholders detected (YOUR_PROJECT, $PROJECT)
- [ ] Timestamps auto-coerced (Z → +00:00, slashes → dashes)
- [ ] FTS5 queries sanitized (leading wildcards stripped)
- [ ] Pre-computed validation sets for O(1) lookup

### Agent UX
- [ ] Fake CLI stub installed for confused agents
- [ ] Macros bundle common multi-step workflows
- [ ] Broadcast explicitly prevented with explanation
- [ ] 14+ resources for entity discovery
- [ ] Query string parsing handles embedded params

### Git Integration
- [ ] Context manager cleanup for Repo objects
- [ ] LRU cache with eviction cleanup
- [ ] Identity resolution modes documented
- [ ] Composable hooks preserve existing tooling

### Query Optimization
- [ ] N+1 queries eliminated with batch fetches
- [ ] Query tracking via context vars
- [ ] Slow query detection with thresholds

### Testing
- [ ] Test with Haiku (canary for unclear APIs)
- [ ] Test mistake detection for all detector types
- [ ] Test fuzzy matching suggestions
- [ ] Test concurrent agent creation (race conditions)
- [ ] Test EMFILE recovery

---

## Reference Index

| Need | File |
|------|------|
| Agent theory of mind patterns | [AGENT-THEORY-OF-MIND.md](references/AGENT-THEORY-OF-MIND.md) |
| Structured error design | [ERROR-DESIGN.md](references/ERROR-DESIGN.md) |
| Tool documentation templates | [TOOL-DOCUMENTATION.md](references/TOOL-DOCUMENTATION.md) |
| Mistake detection patterns | [MISTAKE-DETECTION.md](references/MISTAKE-DETECTION.md) |
| Input validation/normalization | [VALIDATION-PATTERNS.md](references/VALIDATION-PATTERNS.md) |
| Resource design for discovery | [RESOURCE-DESIGN.md](references/RESOURCE-DESIGN.md) |
| Git integration patterns | [GIT-INTEGRATION.md](references/GIT-INTEGRATION.md) |
| Query optimization | [QUERY-OPTIMIZATION.md](references/QUERY-OPTIMIZATION.md) |
| Installation & integration | [INSTALLATION-PATTERNS.md](references/INSTALLATION-PATTERNS.md) |
| Multi-agent coordination | [MULTI-AGENT-COORDINATION.md](references/MULTI-AGENT-COORDINATION.md) |
| Anti-patterns to avoid | [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md) |
| Complete checklists | [CHECKLISTS.md](references/CHECKLISTS.md) |
| Tool filtering & capability gating | [TOOL-FILTERING.md](references/TOOL-FILTERING.md) |
| Database patterns & optimization | [DATABASE-PATTERNS.md](references/DATABASE-PATTERNS.md) |
| LLM integration patterns | [LLM-INTEGRATION.md](references/LLM-INTEGRATION.md) |
| Operational patterns & scripts | [OPERATIONAL-PATTERNS.md](references/OPERATIONAL-PATTERNS.md) |
| Testing strategies & security | [TESTING-PATTERNS.md](references/TESTING-PATTERNS.md) |

---

## Quick Search

```bash
# Find specific pattern
grep -ri "broadcast" .claude/skills/mcp-server-design/references/

# Find all error types
grep -i "error_type" .claude/skills/mcp-server-design/references/

# Find all Do/Don't examples
grep -A 10 "Do / Don't" .claude/skills/mcp-server-design/references/

# Find all code examples
grep -B 2 -A 20 "```python" .claude/skills/mcp-server-design/references/
```
