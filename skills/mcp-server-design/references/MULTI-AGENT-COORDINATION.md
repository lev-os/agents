# Multi-Agent Coordination Patterns

## Table of Contents
- [Overview](#overview)
- [Advisory File Reservations](#advisory-file-reservations)
- [Staleness Detection](#staleness-detection)
- [Contact Policies](#contact-policies)
- [Message Threading](#message-threading)
- [Async Message Passing](#async-message-passing)
- [Conflict Resolution](#conflict-resolution)
- [Session Lifecycle](#session-lifecycle)
- [Product Bus Pattern](#product-bus-pattern)
- [Build Slots System](#build-slots-system)

---

## Overview

Multi-agent coordination is fundamentally different from human collaboration:
- Agents can't "just ask" each other in real-time
- Agents don't have implicit social cues
- Agents need explicit state machines for coordination

**Key insight:** Design for asynchronous, explicit, idempotent coordination.

**mcp_agent_mail's coordination primitives:**
- File reservations (advisory locks)
- Asynchronous messaging
- Contact approval system
- Thread-based conversations
- Staleness detection for abandoned resources

---

## Advisory File Reservations

File reservations prevent multiple agents from editing the same files simultaneously.

### Core Concepts

```python
class FileReservation:
    """Advisory lock on file paths/patterns."""
    id: int
    project_key: str
    agent_name: str
    path_pattern: str      # e.g., "src/api/*.py", "README.md"
    exclusive: bool        # True = write lock, False = read/observe
    expires_ts: datetime   # Auto-release after TTL
    released_ts: datetime | None  # Explicit release
    reason: str           # Human-readable explanation
```

### Reservation Workflow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Agent wants  │────▶│ Check for    │────▶│ Conflict?    │
│ to edit file │     │ conflicts    │     │              │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                           ┌──────────────────────┼──────────────────────┐
                           │ No                   │                      │ Yes
                           ▼                      │                      ▼
                  ┌──────────────┐                │             ┌──────────────┐
                  │ Grant        │                │             │ Return       │
                  │ reservation  │                │             │ conflict     │
                  └──────────────┘                │             │ details      │
                           │                      │             └──────────────┘
                           ▼                      │
                  ┌──────────────┐                │
                  │ Agent edits  │                │
                  │ files        │                │
                  └──────────────┘                │
                           │                      │
                           ▼                      │
                  ┌──────────────┐                │
                  │ Release      │◀───────────────┘
                  │ reservation  │    (or TTL expires)
                  └──────────────┘
```

### Implementation

```python
def file_reservation_paths(
    project_key: str,
    agent_name: str,
    paths: list[str],
    ttl_seconds: int = 3600,
    exclusive: bool = True,
    reason: str = ""
) -> dict:
    """
    Request advisory file reservations.

    Parameters
    ----------
    paths : list[str]
        File paths or glob patterns relative to project.
        Examples: ["src/api/auth.py", "tests/*.py", "config/**"]

    ttl_seconds : int = 3600
        Time to live. Minimum: 60 seconds.
        Expired reservations auto-release.
        Tip: Use renew_file_reservations if you need more time.

    exclusive : bool = True
        True = exclusive write lock (blocks other exclusive)
        False = shared read lock (allows other shared, blocks exclusive)

    Returns
    -------
    dict
        {
            "granted": [{id, path_pattern, exclusive, expires_ts}],
            "conflicts": [{path, holders: [{agent, expires_ts, reason}]}]
        }
    """
    granted = []
    conflicts = []

    for path in paths:
        # Check for conflicting reservations
        existing = find_conflicting_reservations(project_key, path, exclusive)

        # Filter to other agents only
        others = [r for r in existing if r.agent_name != agent_name]

        if others:
            conflicts.append({
                "path": path,
                "holders": [
                    {
                        "agent": r.agent_name,
                        "expires_ts": r.expires_ts.isoformat(),
                        "reason": r.reason,
                        "is_stale": is_reservation_stale(r)  # Hint for force-release
                    }
                    for r in others
                ]
            })
        else:
            # Grant reservation
            reservation = create_reservation(
                project_key=project_key,
                agent_name=agent_name,
                path_pattern=path,
                exclusive=exclusive,
                ttl_seconds=ttl_seconds,
                reason=reason
            )
            granted.append(reservation.to_dict())

    return {"granted": granted, "conflicts": conflicts}
```

### Glob Matching for Conflicts

```python
from fnmatch import fnmatchcase

def paths_conflict(pattern1: str, pattern2: str) -> bool:
    """
    Check if two path patterns could match the same file.

    Symmetric matching: either pattern matching the other counts.
    """
    # Exact match
    if pattern1 == pattern2:
        return True

    # One matches the other
    if fnmatchcase(pattern1, pattern2):
        return True
    if fnmatchcase(pattern2, pattern1):
        return True

    # Common prefix with glob
    # e.g., "src/*.py" vs "src/auth.py"
    return _glob_overlap(pattern1, pattern2)

def _glob_overlap(pat1: str, pat2: str) -> bool:
    """Check if globs could match overlapping files."""
    # Expand ** to match any depth
    parts1 = pat1.replace("**", "*").split("/")
    parts2 = pat2.replace("**", "*").split("/")

    # Compare component by component
    for p1, p2 in zip(parts1, parts2):
        if p1 == "*" or p2 == "*":
            continue
        if fnmatchcase(p1, p2) or fnmatchcase(p2, p1):
            continue
        return False

    return True
```

---

## Staleness Detection

Reservations can become stale when agents crash or disconnect without releasing.

### Staleness Heuristics

```python
def is_reservation_stale(reservation: FileReservation) -> bool:
    """
    Detect if a reservation is likely abandoned.

    Heuristics:
    1. Agent hasn't been active recently
    2. No messages sent/received
    3. No git commits from agent
    4. Reservation held much longer than typical
    """
    now = datetime.now(UTC)
    agent = get_agent(reservation.agent_name)

    # Heuristic 1: Agent inactivity
    if agent.last_active_ts:
        inactive_duration = now - agent.last_active_ts
        if inactive_duration > timedelta(hours=2):
            return True

    # Heuristic 2: No recent messages
    recent_messages = count_messages(
        agent_name=reservation.agent_name,
        since=now - timedelta(hours=1)
    )
    if recent_messages == 0 and reservation_age(reservation) > timedelta(hours=1):
        return True

    # Heuristic 3: No git activity
    if not has_recent_git_commits(agent.name, since=now - timedelta(hours=2)):
        if reservation_age(reservation) > timedelta(hours=2):
            return True

    # Heuristic 4: Unusually long hold time
    typical_hold = timedelta(hours=1)
    if reservation_age(reservation) > typical_hold * 3:
        return True

    return False

def reservation_age(reservation: FileReservation) -> timedelta:
    """Time since reservation was created."""
    return datetime.now(UTC) - reservation.created_ts
```

### Force Release with Notification

```python
def force_release_file_reservation(
    project_key: str,
    agent_name: str,  # Requesting agent
    file_reservation_id: int,
    note: str = "",
    notify_previous: bool = True
) -> dict:
    """
    Force-release a stale reservation held by another agent.

    Validates staleness heuristics before allowing release.
    Optionally notifies the previous holder.
    """
    reservation = get_reservation(file_reservation_id)

    if not reservation:
        raise ToolExecutionError(
            "NOT_FOUND",
            f"File reservation {file_reservation_id} not found"
        )

    if reservation.agent_name == agent_name:
        raise ToolExecutionError(
            "INVALID_OPERATION",
            "Use release_file_reservations for your own reservations"
        )

    # Validate staleness
    if not is_reservation_stale(reservation):
        raise ToolExecutionError(
            "RESERVATION_ACTIVE",
            f"Reservation held by {reservation.agent_name} appears active. "
            f"Last activity: {reservation.agent.last_active_ts}. "
            f"Wait for expiry or coordinate via messaging.",
            recoverable=False,
            data={
                "holder": reservation.agent_name,
                "expires_ts": reservation.expires_ts.isoformat(),
                "suggestion": "Send a message to coordinate"
            }
        )

    # Release
    reservation.released_ts = datetime.now(UTC)
    db.commit()

    # Notify previous holder
    if notify_previous:
        send_system_message(
            to=reservation.agent_name,
            subject=f"[SYSTEM] File reservation force-released",
            body=f"""Your reservation on `{reservation.path_pattern}` was force-released by {agent_name}.

Reason: Reservation appeared stale (no activity detected).

Note from releaser: {note or '(none)'}

If you're still active, you may re-reserve the files."""
        )

    return {
        "released": True,
        "reservation_id": file_reservation_id,
        "previous_holder": reservation.agent_name,
        "notified": notify_previous
    }
```

---

## Contact Policies

Contact policies control who can send messages to an agent.

### Policy Levels

```python
class ContactPolicy(Enum):
    OPEN = "open"           # Anyone can message
    AUTO = "auto"           # Auto-approve same-project agents
    CONTACTS_ONLY = "contacts_only"  # Only approved contacts
    BLOCK_ALL = "block_all"  # No messages accepted
```

### Contact Approval Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Agent A      │────▶│ request_     │────▶│ Policy       │
│ wants to     │     │ contact      │     │ check        │
│ message B    │     └──────────────┘     └──────┬───────┘
└──────────────┘                                  │
                                    ┌─────────────┼─────────────┐
                                    │ OPEN        │ AUTO        │ CONTACTS_ONLY
                                    ▼             ▼             ▼
                           ┌────────────┐ ┌────────────┐ ┌────────────┐
                           │ Auto-      │ │ Auto-      │ │ Create     │
                           │ approve    │ │ approve if │ │ pending    │
                           │            │ │ same proj  │ │ request    │
                           └────────────┘ └────────────┘ └────────────┘
                                    │             │             │
                                    └─────────────┼─────────────┘
                                                  ▼
                                         ┌────────────┐
                                         │ AgentLink  │
                                         │ created    │
                                         └────────────┘
```

### Implementation

```python
def request_contact(
    project_key: str,
    from_agent: str,
    to_agent: str,
    reason: str = "",
    ttl_seconds: int = 604800  # 7 days
) -> dict:
    """
    Request contact approval to message another agent.
    """
    target = get_agent(project_key, to_agent)
    if not target:
        raise ToolExecutionError("NOT_FOUND", f"Agent {to_agent} not found")

    policy = target.contact_policy or ContactPolicy.AUTO

    # Check policy
    if policy == ContactPolicy.BLOCK_ALL:
        raise ToolExecutionError(
            "CONTACT_BLOCKED",
            f"Agent {to_agent} is not accepting contact requests",
            recoverable=False
        )

    if policy == ContactPolicy.OPEN:
        # Auto-approve
        return _create_contact_link(from_agent, to_agent, approved=True)

    if policy == ContactPolicy.AUTO:
        # Auto-approve if same project
        requester = get_agent(project_key, from_agent)
        if requester and requester.project_key == target.project_key:
            return _create_contact_link(from_agent, to_agent, approved=True)

    # CONTACTS_ONLY or cross-project AUTO: Create pending request
    link = _create_contact_link(
        from_agent, to_agent,
        approved=False,
        expires_ts=datetime.now(UTC) + timedelta(seconds=ttl_seconds)
    )

    # Send notification
    send_message(
        to=[to_agent],
        subject=f"[CONTACT REQUEST] {from_agent} wants to message you",
        body=f"""Agent **{from_agent}** is requesting contact approval.

Reason: {reason or '(not provided)'}

To approve: `respond_contact(to_agent="{to_agent}", from_agent="{from_agent}", accept=True)`
To deny: `respond_contact(to_agent="{to_agent}", from_agent="{from_agent}", accept=False)`

This request expires in {ttl_seconds // 86400} days.""",
        ack_required=True
    )

    return {
        "status": "pending",
        "link_id": link.id,
        "expires_ts": link.expires_ts.isoformat()
    }
```

---

## Message Threading

Threads group related messages for coherent conversations.

### Thread Structure

```python
class Thread:
    thread_id: str         # e.g., "TKT-123" or auto-generated UUID
    project_key: str
    subject: str           # Thread subject (from first message)
    participants: list[str]  # Agent names involved
    message_count: int
    last_activity: datetime
```

### Thread Creation and Continuation

```python
def send_message(
    project_key: str,
    sender_name: str,
    to: list[str],
    subject: str,
    body_md: str,
    thread_id: str | None = None,
    **kwargs
) -> dict:
    """
    Send a message, optionally in a thread.

    Thread behavior:
    - If thread_id is provided, message joins existing thread
    - If no thread_id, a new thread is created for this message
    """
    if thread_id:
        thread = get_thread(project_key, thread_id)
        if not thread:
            raise ToolExecutionError(
                "NOT_FOUND",
                f"Thread {thread_id} not found",
                data={"available_threads": list_recent_threads(project_key)}
            )
    else:
        # Create new thread
        thread = create_thread(
            project_key=project_key,
            subject=subject,
            creator=sender_name
        )
        thread_id = thread.thread_id

    message = Message(
        project_key=project_key,
        thread_id=thread_id,
        sender_name=sender_name,
        subject=subject,
        body_md=body_md,
        **kwargs
    )

    # Update thread metadata
    thread.message_count += 1
    thread.last_activity = datetime.now(UTC)
    thread.participants = list(set(thread.participants + to + [sender_name]))

    db.add(message)
    db.commit()

    return message.to_dict()


def reply_message(
    project_key: str,
    message_id: int,
    sender_name: str,
    body_md: str,
    to: list[str] | None = None,
    subject_prefix: str = "Re:"
) -> dict:
    """
    Reply to an existing message, preserving thread.

    Automatically:
    - Inherits thread_id from original
    - Prefixes subject if not already
    - Defaults to=original sender if not provided
    """
    original = get_message(message_id)
    if not original:
        raise ToolExecutionError("NOT_FOUND", f"Message {message_id} not found")

    # Inherit thread
    thread_id = original.thread_id or str(original.id)

    # Default recipient to original sender
    if not to:
        to = [original.sender_name]

    # Prefix subject
    subject = original.subject
    if not subject.lower().startswith(subject_prefix.lower()):
        subject = f"{subject_prefix} {subject}"

    return send_message(
        project_key=project_key,
        sender_name=sender_name,
        to=to,
        subject=subject,
        body_md=body_md,
        thread_id=thread_id,
        reply_to=message_id,
        importance=original.importance,
        ack_required=original.ack_required
    )
```

---

## Async Message Passing

Agents coordinate through asynchronous message polling, not real-time chat.

### Polling Pattern

```python
def fetch_inbox(
    project_key: str,
    agent_name: str,
    since_ts: str | None = None,
    urgent_only: bool = False,
    limit: int = 20,
    include_bodies: bool = False
) -> list[dict]:
    """
    Retrieve recent messages without mutating state.

    Usage patterns:
    - Poll after each editing step in agent loop
    - Use since_ts with timestamp from last poll for incremental
    - Combine with acknowledge_message for ack_required messages

    Parameters
    ----------
    since_ts : str | None
        ISO-8601 timestamp. Only messages newer than this returned.
        Store the latest message timestamp for efficient polling.

    urgent_only : bool = False
        If true, only importance in {high, urgent}

    Returns
    -------
    list[dict]
        Messages with: id, subject, from, created_ts, importance, ack_required
        If include_bodies: also body_md
    """
    query = db.query(Message).join(Recipient).filter(
        Recipient.agent_name == agent_name,
        Message.project_key == project_key
    )

    if since_ts:
        parsed = parse_iso_timestamp(since_ts)
        query = query.filter(Message.created_ts > parsed)

    if urgent_only:
        query = query.filter(Message.importance.in_(["high", "urgent"]))

    messages = query.order_by(Message.created_ts.desc()).limit(limit).all()

    return [
        {
            "id": m.id,
            "subject": m.subject,
            "from": m.sender_name,
            "created_ts": m.created_ts.isoformat(),
            "importance": m.importance,
            "ack_required": m.ack_required,
            "thread_id": m.thread_id,
            **({"body_md": m.body_md} if include_bodies else {})
        }
        for m in messages
    ]
```

### Agent Loop Integration

```python
# Recommended agent loop pattern
class AgentLoop:
    def __init__(self, agent_name: str, project_key: str):
        self.agent_name = agent_name
        self.project_key = project_key
        self.last_inbox_check = None

    async def run_step(self, task):
        """Execute one step of agent work."""
        # 1. Check for coordination messages
        await self.check_inbox()

        # 2. Do work
        result = await self.execute_task(task)

        # 3. Check again (might have received urgent during work)
        await self.check_inbox()

        return result

    async def check_inbox(self):
        """Poll inbox for coordination messages."""
        messages = await fetch_inbox(
            project_key=self.project_key,
            agent_name=self.agent_name,
            since_ts=self.last_inbox_check,
            urgent_only=False,
            include_bodies=True
        )

        if messages:
            self.last_inbox_check = messages[0]["created_ts"]

        for msg in messages:
            await self.handle_message(msg)

    async def handle_message(self, msg: dict):
        """Process coordination message."""
        if msg["importance"] in ("high", "urgent"):
            # Prioritize urgent messages
            await self.handle_urgent(msg)

        if msg["ack_required"]:
            # Acknowledge receipt
            await acknowledge_message(
                project_key=self.project_key,
                agent_name=self.agent_name,
                message_id=msg["id"]
            )
```

---

## Conflict Resolution

When conflicts arise, provide clear resolution paths.

### Reservation Conflicts

```python
def handle_reservation_conflict(conflict: dict) -> str:
    """
    Generate guidance for resolving reservation conflicts.
    """
    holder = conflict["holders"][0]

    if holder.get("is_stale"):
        return f"""Reservation appears stale. You can:
1. Force-release: force_release_file_reservation(file_reservation_id={conflict['id']})
2. Wait for expiry: {holder['expires_ts']}
3. Message holder: send_message(to=["{holder['agent']}"], subject="File reservation coordination")"""

    return f"""Active reservation by {holder['agent']}.
1. Coordinate: send_message(to=["{holder['agent']}"], subject="Need access to {conflict['path']}")
2. Wait for release: check fetch_inbox for response
3. Wait for expiry: {holder['expires_ts']}"""
```

### Message Delivery Failures

```python
def handle_delivery_failure(recipient: str, reason: str) -> dict:
    """
    Structured error for message delivery failure.
    """
    if reason == "not_found":
        return ToolExecutionError(
            "RECIPIENT_NOT_FOUND",
            f"Recipient '{recipient}' not found",
            data={
                "available_agents": list_agents(),
                "suggestions": find_similar(recipient, list_agents()),
                "fix_hint": "Check resource://agents/{project_key} for valid recipients"
            }
        )

    if reason == "blocked":
        return ToolExecutionError(
            "CONTACT_BLOCKED",
            f"Agent '{recipient}' is not accepting messages from you",
            data={
                "suggestion": "Request contact approval first",
                "tool": "request_contact"
            }
        )

    if reason == "pending_contact":
        return ToolExecutionError(
            "CONTACT_PENDING",
            f"Contact request to '{recipient}' is pending approval",
            data={
                "status": "waiting",
                "suggestion": "Wait for approval or check inbox for response"
            }
        )
```

---

## Session Lifecycle

Proper session management ensures clean coordination state.

### Session Start

```python
def macro_start_session(
    human_key: str,
    program: str,
    model: str,
    agent_name: str | None = None,
    task_description: str = "",
    file_reservation_paths: list[str] | None = None,
    inbox_limit: int = 10
) -> dict:
    """
    Macro: Initialize an agent session.

    Bundles: ensure_project + register_agent + optional reservations + fetch_inbox

    This is the recommended entry point for agents starting work.
    """
    # 1. Ensure project exists
    project = ensure_project(human_key)

    # 2. Register/update agent
    agent = register_agent(
        project_key=human_key,
        program=program,
        model=model,
        name=agent_name,
        task_description=task_description
    )

    # 3. Reserve files if specified
    reservations = None
    if file_reservation_paths:
        reservations = file_reservation_paths(
            project_key=human_key,
            agent_name=agent["name"],
            paths=file_reservation_paths,
            ttl_seconds=3600,
            reason="Session start"
        )

    # 4. Fetch inbox
    inbox = fetch_inbox(
        project_key=human_key,
        agent_name=agent["name"],
        limit=inbox_limit,
        include_bodies=True
    )

    return {
        "project": project,
        "agent": agent,
        "reservations": reservations,
        "inbox": inbox,
        "unread_count": len([m for m in inbox if not m.get("read_at")])
    }
```

### Session End

```python
def end_session(project_key: str, agent_name: str) -> dict:
    """
    Clean up agent session state.

    - Releases all file reservations
    - Updates last_active timestamp
    - Optionally sends completion notification
    """
    # Release all reservations
    released = release_file_reservations(
        project_key=project_key,
        agent_name=agent_name
    )

    # Update activity
    update_agent_activity(project_key, agent_name)

    return {
        "reservations_released": released["released"],
        "session_ended": datetime.now(UTC).isoformat()
    }
```

---

## Product Bus Pattern

When agents work across multiple related projects (e.g., frontend + backend + shared libraries), the **product bus** provides cross-project organization.

### Product Hierarchy

```python
class Product(Base):
    """Cross-project organization."""
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

class ProductProjectLink(Base):
    """Link projects to products for organization."""
    __tablename__ = "product_project_links"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    role: Mapped[str] = mapped_column(String(64))  # e.g., "backend", "frontend", "shared"
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    __table_args__ = (
        UniqueConstraint("product_id", "project_id", name="uq_product_project"),
    )
```

### Use Cases

**1. Cross-Project Message Search**
```python
def search_product_messages(product_name: str, query: str) -> list[dict]:
    """
    Search messages across all projects in a product.

    Useful for:
    - Finding related discussions across repos
    - Understanding cross-team coordination
    - Auditing product-wide decisions
    """
    product = get_product(product_name)
    if not product:
        raise ToolExecutionError("NOT_FOUND", f"Product '{product_name}' not found")

    # Get all linked projects
    project_ids = [link.project_id for link in product.project_links]

    # Search across all projects
    return search_messages_multi_project(project_ids, query)
```

**2. Product-Scoped Agent Discovery**
```python
def list_product_agents(product_name: str) -> list[dict]:
    """
    List all agents working across the product.

    Returns agents from all linked projects with their
    current task descriptions.
    """
    product = get_product(product_name)

    agents = []
    for link in product.project_links:
        project_agents = list_agents(link.project.human_key)
        for agent in project_agents:
            agent["project_role"] = link.role
            agents.append(agent)

    return agents
```

**3. Cross-Project Coordination Messages**
```python
def broadcast_to_product(
    product_name: str,
    sender_name: str,
    subject: str,
    body_md: str,
    importance: str = "normal"
) -> dict:
    """
    Send a message to all agents in a product.

    Use sparingly - prefer targeted messages.
    Good for: release announcements, breaking changes, urgent coordination.
    """
    agents = list_product_agents(product_name)

    # Group by project for efficient delivery
    by_project = defaultdict(list)
    for agent in agents:
        by_project[agent["project_key"]].append(agent["name"])

    deliveries = []
    for project_key, recipients in by_project.items():
        result = send_message(
            project_key=project_key,
            sender_name=sender_name,
            to=recipients,
            subject=f"[{product_name}] {subject}",
            body_md=body_md,
            importance=importance
        )
        deliveries.append(result)

    return {
        "product": product_name,
        "projects_notified": len(by_project),
        "agents_notified": sum(len(r) for r in by_project.values()),
        "deliveries": deliveries
    }
```

---

## Build Slots System

For operations that require coarse concurrency control (builds, deploys, migrations), the **build slots** system provides time-limited exclusive access.

### Core Concepts

```python
class BuildSlot(Base):
    """Coarse concurrency control for builds/deploys."""
    __tablename__ = "build_slots"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id"), index=True)
    slot_type: Mapped[str] = mapped_column(String(64))  # "build", "deploy", "migrate"
    acquired_ts: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    expires_ts: Mapped[datetime] = mapped_column()
    released_ts: Mapped[datetime | None] = mapped_column(default=None)
    reason: Mapped[str] = mapped_column(Text, default="")
```

### Slot Operations

```python
def acquire_build_slot(
    project_key: str,
    agent_name: str,
    slot_type: str,
    ttl_seconds: int = 600,  # 10 minutes
    reason: str = ""
) -> dict:
    """
    Acquire exclusive slot for build/deploy operations.

    Parameters
    ----------
    slot_type : str
        One of: "build", "deploy", "migrate", "test"
        Only one agent can hold a given slot_type per project.

    ttl_seconds : int = 600
        Maximum hold time. Use renew_build_slot for longer operations.

    Returns
    -------
    dict
        {"acquired": True, "slot_id": int, "expires_ts": str}
        OR {"acquired": False, "holder": str, "expires_ts": str}
    """
    # Check for existing active slot
    existing = db.query(BuildSlot).filter(
        BuildSlot.project_id == get_project(project_key).id,
        BuildSlot.slot_type == slot_type,
        BuildSlot.released_ts.is_(None),
        BuildSlot.expires_ts > datetime.now(UTC)
    ).first()

    if existing:
        # Already held
        holder = get_agent_by_id(existing.agent_id)
        return {
            "acquired": False,
            "holder": holder.name,
            "expires_ts": existing.expires_ts.isoformat(),
            "reason": existing.reason,
            "suggestion": f"Wait for release or expiry, or message {holder.name}"
        }

    # Grant slot
    slot = BuildSlot(
        project_id=get_project(project_key).id,
        agent_id=get_agent(project_key, agent_name).id,
        slot_type=slot_type,
        expires_ts=datetime.now(UTC) + timedelta(seconds=ttl_seconds),
        reason=reason
    )
    db.add(slot)
    db.commit()

    return {
        "acquired": True,
        "slot_id": slot.id,
        "slot_type": slot_type,
        "expires_ts": slot.expires_ts.isoformat()
    }


def renew_build_slot(
    project_key: str,
    agent_name: str,
    slot_id: int,
    extend_seconds: int = 300
) -> dict:
    """
    Extend an active build slot.

    Use when operation is taking longer than expected.
    """
    slot = db.query(BuildSlot).get(slot_id)

    if not slot or slot.released_ts:
        raise ToolExecutionError("NOT_FOUND", f"Active slot {slot_id} not found")

    agent = get_agent(project_key, agent_name)
    if slot.agent_id != agent.id:
        raise ToolExecutionError(
            "PERMISSION_DENIED",
            f"Slot held by different agent",
            recoverable=False
        )

    # Extend from later of now or current expiry
    base = max(slot.expires_ts, datetime.now(UTC))
    slot.expires_ts = base + timedelta(seconds=extend_seconds)
    db.commit()

    return {
        "renewed": True,
        "slot_id": slot_id,
        "new_expires_ts": slot.expires_ts.isoformat()
    }


def release_build_slot(
    project_key: str,
    agent_name: str,
    slot_id: int
) -> dict:
    """Release a build slot when operation completes."""
    slot = db.query(BuildSlot).get(slot_id)

    if not slot:
        # Idempotent - already released or never existed
        return {"released": True, "slot_id": slot_id}

    agent = get_agent(project_key, agent_name)
    if slot.agent_id != agent.id:
        raise ToolExecutionError(
            "PERMISSION_DENIED",
            f"Cannot release slot held by another agent"
        )

    slot.released_ts = datetime.now(UTC)
    db.commit()

    return {
        "released": True,
        "slot_id": slot_id,
        "held_duration_seconds": (slot.released_ts - slot.acquired_ts).total_seconds()
    }
```

### Build Slot Workflow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Agent wants  │────▶│ acquire_     │────▶│ Slot free?   │
│ to build     │     │ build_slot   │     │              │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                           ┌──────────────────────┼──────────────────────┐
                           │ Yes                  │                      │ No
                           ▼                      │                      ▼
                  ┌──────────────┐                │             ┌──────────────┐
                  │ Run build    │                │             │ Wait or      │
                  │ operation    │                │             │ coordinate   │
                  └──────────────┘                │             └──────────────┘
                           │                      │
                           ▼                      │
                  ┌──────────────┐                │
                  │ Taking too   │                │
                  │ long?        │                │
                  └──────┬───────┘                │
                         │ Yes                    │
                         ▼                        │
                  ┌──────────────┐                │
                  │ renew_       │                │
                  │ build_slot   │                │
                  └──────────────┘                │
                           │                      │
                           ▼                      │
                  ┌──────────────┐                │
                  │ release_     │◀───────────────┘
                  │ build_slot   │    (or TTL expires)
                  └──────────────┘
```

### Integration with File Reservations

```python
def acquire_build_with_reservations(
    project_key: str,
    agent_name: str,
    slot_type: str,
    file_patterns: list[str],
    ttl_seconds: int = 600
) -> dict:
    """
    Acquire build slot AND reserve related files atomically.

    Common pattern: reserve build outputs while building.
    """
    # First acquire slot
    slot_result = acquire_build_slot(
        project_key, agent_name, slot_type, ttl_seconds
    )

    if not slot_result.get("acquired"):
        return slot_result

    # Then reserve files
    reservation_result = file_reservation_paths(
        project_key=project_key,
        agent_name=agent_name,
        paths=file_patterns,
        ttl_seconds=ttl_seconds,
        exclusive=True,
        reason=f"Build slot: {slot_type}"
    )

    return {
        "build_slot": slot_result,
        "file_reservations": reservation_result
    }
```

---

## Summary: Coordination Principles

| # | Principle | Implementation |
|---|-----------|----------------|
| 1 | **Async by default** | Poll-based messaging, not real-time |
| 2 | **Explicit state** | Reservations, contacts, threads, build slots |
| 3 | **Staleness detection** | Heuristics for abandoned resources |
| 4 | **Conflict guidance** | Structured errors with resolution paths |
| 5 | **Policy-based access** | Contact policies for message control |
| 6 | **Idempotent operations** | Safe to retry all coordination ops |
| 7 | **TTL everywhere** | Auto-expiry prevents resource hoarding |
| 8 | **Thread continuity** | Keep conversations coherent |
| 9 | **Cross-project coordination** | Product bus for multi-repo organization |
| 10 | **Coarse concurrency control** | Build slots for exclusive operations |
