# Database Patterns

> **Principle**: Robust database access with query tracking, lock handling, and optimization for SQLite's constraints.

## Query Tracking

Track queries per-request using context variables:

```python
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

_query_tracker: ContextVar["QueryTracker | None"] = ContextVar("query_tracker", default=None)

@dataclass(slots=True)
class QueryTracker:
    """Track query statistics for a single request."""
    total: int = 0
    total_time_ms: float = 0.0
    per_table: dict[str, int] = field(default_factory=dict)
    slow_query_ms: float | None = None
    slow_queries: list[dict[str, Any]] = field(default_factory=list)

    def record(self, table: str, duration_ms: float, sql: str = ""):
        """Record a query execution."""
        self.total += 1
        self.total_time_ms += duration_ms
        self.per_table[table] = self.per_table.get(table, 0) + 1

        # Track slow queries
        if self.slow_query_ms and duration_ms > self.slow_query_ms:
            self.slow_queries.append({
                "table": table,
                "duration_ms": duration_ms,
                "sql": sql[:500],  # Truncate for safety
            })

@contextmanager
def track_queries(slow_threshold_ms: float | None = 100.0):
    """Context manager to track queries in the current request."""
    tracker = QueryTracker(slow_query_ms=slow_threshold_ms)
    token = _query_tracker.set(tracker)
    try:
        yield tracker
    finally:
        _query_tracker.reset(token)
        if tracker.slow_queries:
            logger.warning(f"Slow queries detected: {len(tracker.slow_queries)}")
            for sq in tracker.slow_queries:
                logger.warning(f"  {sq['table']}: {sq['duration_ms']:.1f}ms")
```

## SQLAlchemy Event Listener

Hook into SQLAlchemy events for tracking:

```python
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time

@event.listens_for(Engine, "before_cursor_execute")
def _before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.perf_counter())

@event.listens_for(Engine, "after_cursor_execute")
def _after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    start_times = conn.info.get("query_start_time", [])
    if start_times:
        duration = (time.perf_counter() - start_times.pop()) * 1000

        tracker = _query_tracker.get()
        if tracker:
            # Extract table name from SQL (simplified)
            table = _extract_table_name(statement)
            tracker.record(table, duration, statement)
```

## Database Lock Retry with Backoff

Handle SQLite's single-writer limitation:

```python
import random
from functools import wraps

def retry_on_db_lock(
    max_retries: int = 5,
    base_delay: float = 0.1,
    max_delay: float = 5.0,
):
    """
    Retry decorator for database lock errors.

    Uses exponential backoff with ±25% jitter:
    - Attempt 1: 100ms ± 25ms
    - Attempt 2: 200ms ± 50ms
    - Attempt 3: 400ms ± 100ms
    - Attempt 4: 800ms ± 200ms
    - Attempt 5: 1600ms ± 400ms (capped at max_delay)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except OperationalError as e:
                    if "database is locked" not in str(e):
                        raise

                    last_error = e
                    if attempt < max_retries - 1:
                        # Exponential backoff with jitter
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        jitter = delay * 0.25 * (2 * random.random() - 1)
                        actual_delay = delay + jitter

                        logger.warning(
                            f"Database locked, retry {attempt + 1}/{max_retries} "
                            f"after {actual_delay:.3f}s"
                        )
                        time.sleep(actual_delay)

            raise last_error

        return wrapper
    return decorator

# Usage
@retry_on_db_lock(max_retries=5, base_delay=0.1)
def save_message(session: Session, message: Message) -> Message:
    session.add(message)
    session.commit()
    return message
```

## SQLite Optimization Pragmas

Configure SQLite for better concurrent access:

```python
def configure_sqlite_engine(db_path: str) -> Engine:
    """
    Create SQLite engine with optimized settings.

    Settings:
    - WAL mode: Allows concurrent reads during writes
    - busy_timeout: Wait 30s for locks instead of failing immediately
    - synchronous=NORMAL: Balance durability and speed
    - cache_size: 64MB for faster repeated queries
    - temp_store=MEMORY: Use RAM for temp tables
    """
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA busy_timeout=30000")  # 30 seconds
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=-65536")  # 64MB
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.execute("PRAGMA mmap_size=268435456")  # 256MB
        cursor.close()

    return engine
```

## FTS5 Full-Text Search Setup

Configure FTS5 with auto-sync triggers:

```python
def setup_fts5(engine: Engine):
    """
    Set up FTS5 virtual table for message search.

    Features:
    - Porter stemmer tokenizer for better matching
    - Auto-sync triggers keep FTS in sync with messages table
    - Column weighting: subject (2.0), body (1.0)
    """
    with engine.connect() as conn:
        # Create FTS5 virtual table
        conn.execute(text("""
            CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
                subject,
                body_md,
                content='messages',
                content_rowid='id',
                tokenize='porter unicode61'
            )
        """))

        # Auto-sync trigger: INSERT
        conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages BEGIN
                INSERT INTO messages_fts(rowid, subject, body_md)
                VALUES (new.id, new.subject, new.body_md);
            END
        """))

        # Auto-sync trigger: DELETE
        conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS messages_ad AFTER DELETE ON messages BEGIN
                INSERT INTO messages_fts(messages_fts, rowid, subject, body_md)
                VALUES ('delete', old.id, old.subject, old.body_md);
            END
        """))

        # Auto-sync trigger: UPDATE
        conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS messages_au AFTER UPDATE ON messages BEGIN
                INSERT INTO messages_fts(messages_fts, rowid, subject, body_md)
                VALUES ('delete', old.id, old.subject, old.body_md);
                INSERT INTO messages_fts(rowid, subject, body_md)
                VALUES (new.id, new.subject, new.body_md);
            END
        """))

        conn.commit()

def search_messages(session: Session, query: str, limit: int = 20) -> list[Message]:
    """
    Search messages using FTS5.

    Query syntax (FTS5):
    - Phrase: "exact phrase"
    - Prefix: word*
    - Boolean: word1 AND word2, word1 OR word2
    - Negation: word1 NOT word2
    """
    # Sanitize query for FTS5
    safe_query = sanitize_fts_query(query)
    if not safe_query:
        return []

    result = session.execute(text("""
        SELECT m.* FROM messages m
        JOIN messages_fts fts ON m.id = fts.rowid
        WHERE messages_fts MATCH :query
        ORDER BY bm25(messages_fts, 2.0, 1.0)  -- Weight subject higher
        LIMIT :limit
    """), {"query": safe_query, "limit": limit})

    return [Message(**row._mapping) for row in result]
```

## 8 Core Database Tables

Standard schema for MCP coordination:

```python
class Project(Base):
    """Project identity and metadata."""
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    human_key: Mapped[str] = mapped_column(String(1024))  # Original path
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

class Agent(Base):
    """Agent identity within a project."""
    __tablename__ = "agents"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    name: Mapped[str] = mapped_column(String(64), index=True)  # Adjective+Noun
    program: Mapped[str] = mapped_column(String(64))  # claude-code, codex-cli
    model: Mapped[str] = mapped_column(String(128))  # claude-3-5-sonnet
    task_description: Mapped[str] = mapped_column(Text, default="")
    inception_ts: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    last_active_ts: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    __table_args__ = (
        UniqueConstraint("project_id", "name", name="uq_agent_project_name"),
    )

class Message(Base):
    """Message content and metadata."""
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("agents.id"), index=True)
    thread_id: Mapped[str | None] = mapped_column(String(64), index=True)
    reply_to_id: Mapped[int | None] = mapped_column(ForeignKey("messages.id"))
    subject: Mapped[str] = mapped_column(String(512))
    body_md: Mapped[str] = mapped_column(Text)
    importance: Mapped[str] = mapped_column(String(16), default="normal")
    ack_required: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

class Recipient(Base):
    """Message delivery tracking per recipient."""
    __tablename__ = "recipients"
    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"), index=True)
    agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id"), index=True)
    kind: Mapped[str] = mapped_column(String(8))  # to, cc, bcc
    read_ts: Mapped[datetime | None] = mapped_column(default=None)
    ack_ts: Mapped[datetime | None] = mapped_column(default=None)

class Thread(Base):
    """Thread metadata and summary cache."""
    __tablename__ = "threads"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    subject: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    last_message_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

class FileReservation(Base):
    """Advisory file locks."""
    __tablename__ = "file_reservations"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id"), index=True)
    path_pattern: Mapped[str] = mapped_column(String(512))
    exclusive: Mapped[bool] = mapped_column(default=True)
    reason: Mapped[str] = mapped_column(Text, default="")
    created_ts: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    expires_ts: Mapped[datetime] = mapped_column()
    released_ts: Mapped[datetime | None] = mapped_column(default=None)

class AgentLink(Base):
    """Contact permissions between agents."""
    __tablename__ = "agent_links"
    id: Mapped[int] = mapped_column(primary_key=True)
    from_agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id"), index=True)
    to_agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id"), index=True)
    from_project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    to_project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    status: Mapped[str] = mapped_column(String(16))  # pending, approved, denied
    created_ts: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    expires_ts: Mapped[datetime] = mapped_column()

class Product(Base):
    """Cross-project organization (product bus)."""
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
```

## Connection Pool Management

Manage connections for multi-threaded access:

```python
from sqlalchemy.pool import QueuePool

def create_engine_with_pool(db_path: str, pool_size: int = 5) -> Engine:
    """
    Create engine with connection pool.

    For SQLite with WAL mode:
    - pool_size: Number of connections to maintain
    - max_overflow: Additional connections allowed under load
    - pool_recycle: Reconnect after N seconds (handles stale connections)
    """
    return create_engine(
        f"sqlite:///{db_path}",
        poolclass=QueuePool,
        pool_size=pool_size,
        max_overflow=10,
        pool_recycle=3600,  # 1 hour
        pool_pre_ping=True,  # Verify connections before use
        connect_args={"check_same_thread": False},
    )
```

## Do / Don't

**Do:**
- Use WAL mode for concurrent access
- Set busy_timeout to handle lock contention
- Track queries per request
- Use FTS5 triggers for auto-sync
- Add jitter to backoff delays

**Don't:**
- Use default SQLite settings in production
- Ignore database lock errors
- Create FTS tables without triggers
- Exceed 5-10 connections for SQLite
- Log full SQL statements (truncate for safety)
