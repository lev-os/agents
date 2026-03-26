# Query Optimization Patterns

## Table of Contents
- [Overview](#overview)
- [N+1 Query Elimination](#n1-query-elimination)
- [FTS5 Full-Text Search](#fts5-full-text-search)
- [Query Tracking](#query-tracking)
- [Index Strategy](#index-strategy)
- [Connection Management](#connection-management)
- [Caching Patterns](#caching-patterns)
- [Batch Operations](#batch-operations)

---

## Overview

MCP servers are query-heavy. Every tool call typically involves database operations. Poor query patterns lead to:
- Slow tool responses (agents retry, waste tokens)
- Resource exhaustion under load
- Unpredictable latency

**Key insight:** Optimize for the agent use pattern—many small, concurrent queries.

**mcp_agent_mail optimizations:**
- Eager loading to eliminate N+1
- FTS5 for full-text search
- Query tracking with slow query detection
- Strategic indexes for common access patterns
- Pre-computed validation sets

---

## N+1 Query Elimination

N+1 is the most common performance anti-pattern in MCP servers.

### The Problem

```python
# BAD: N+1 query pattern
def list_agents(project_key: str) -> list[dict]:
    agents = db.query(Agent).filter(Agent.project_key == project_key).all()

    results = []
    for agent in agents:
        # N additional queries!
        last_message = db.query(Message).filter(
            Message.sender_name == agent.name
        ).order_by(Message.created_ts.desc()).first()

        results.append({
            "name": agent.name,
            "last_message": last_message.subject if last_message else None
        })

    return results  # 1 + N queries total
```

### The Solution: Eager Loading

```python
from sqlalchemy.orm import joinedload, selectinload

# GOOD: Single query with eager loading
def list_agents(project_key: str) -> list[dict]:
    agents = db.query(Agent).options(
        selectinload(Agent.messages)  # Eager load messages
    ).filter(
        Agent.project_key == project_key
    ).all()

    results = []
    for agent in agents:
        # No additional queries - messages already loaded
        last_message = sorted(
            agent.messages,
            key=lambda m: m.created_ts,
            reverse=True
        )[0] if agent.messages else None

        results.append({
            "name": agent.name,
            "last_message": last_message.subject if last_message else None
        })

    return results  # 2 queries total (1 for agents, 1 for all messages)
```

### Subquery Alternative

```python
from sqlalchemy import func

# BETTER: Subquery for aggregates
def list_agents_with_stats(project_key: str) -> list[dict]:
    # Subquery for message counts
    message_counts = db.query(
        Message.sender_name,
        func.count(Message.id).label('count'),
        func.max(Message.created_ts).label('last_active')
    ).group_by(Message.sender_name).subquery()

    # Join with agents
    agents = db.query(
        Agent,
        message_counts.c.count,
        message_counts.c.last_active
    ).outerjoin(
        message_counts,
        Agent.name == message_counts.c.sender_name
    ).filter(
        Agent.project_key == project_key
    ).all()

    return [
        {
            "name": a.Agent.name,
            "message_count": a.count or 0,
            "last_message_at": a.last_active.isoformat() if a.last_active else None
        }
        for a in agents
    ]  # 1 query total!
```

---

## FTS5 Full-Text Search

SQLite FTS5 provides fast full-text search for messages.

### FTS5 Table Setup

```python
# Create FTS5 virtual table
def setup_fts5():
    db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
            subject,
            body_md,
            content='messages',
            content_rowid='id',
            tokenize='porter unicode61'
        )
    """)

    # Triggers to keep FTS in sync
    db.execute("""
        CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages BEGIN
            INSERT INTO messages_fts(rowid, subject, body_md)
            VALUES (new.id, new.subject, new.body_md);
        END
    """)

    db.execute("""
        CREATE TRIGGER IF NOT EXISTS messages_ad AFTER DELETE ON messages BEGIN
            INSERT INTO messages_fts(messages_fts, rowid, subject, body_md)
            VALUES ('delete', old.id, old.subject, old.body_md);
        END
    """)

    db.execute("""
        CREATE TRIGGER IF NOT EXISTS messages_au AFTER UPDATE ON messages BEGIN
            INSERT INTO messages_fts(messages_fts, rowid, subject, body_md)
            VALUES ('delete', old.id, old.subject, old.body_md);
            INSERT INTO messages_fts(rowid, subject, body_md)
            VALUES (new.id, new.subject, new.body_md);
        END
    """)
```

### FTS5 Query Sanitization

```python
def sanitize_fts5_query(query: str) -> str | None:
    """
    Sanitize user input for FTS5 queries.

    FTS5 pitfalls:
    - Leading wildcards cause full scan: '*foo' is slow
    - Bare '*' matches nothing
    - Unbalanced quotes cause errors
    - Special characters need escaping
    """
    if not query or not query.strip():
        return None

    query = query.strip()

    # Bare wildcard matches nothing
    if query == "*":
        return None

    # Strip leading wildcards (cause full table scan)
    while query.startswith("*"):
        query = query[1:].strip()

    if not query:
        return None

    # Balance quotes
    if query.count('"') % 2 != 0:
        query = query.replace('"', '')

    # Escape special FTS5 characters if not intentional
    # Let through: AND, OR, NOT, *, "phrases"
    special_chars = ['(', ')', ':', '^']
    for char in special_chars:
        query = query.replace(char, f'"{char}"')

    return query or None


def search_messages(project_key: str, query: str, limit: int = 20) -> list[dict]:
    """
    Full-text search over messages.

    Query syntax (FTS5):
    - Phrase: "build plan"
    - Prefix: migrat*
    - Boolean: plan AND users
    - NOT: error NOT warning
    """
    sanitized = sanitize_fts5_query(query)

    if not sanitized:
        return []

    results = db.execute("""
        SELECT m.id, m.subject, m.sender_name, m.created_ts,
               m.importance, m.thread_id,
               snippet(messages_fts, 1, '<b>', '</b>', '...', 32) as snippet
        FROM messages m
        JOIN messages_fts ON m.id = messages_fts.rowid
        WHERE messages_fts MATCH :query
        AND m.project_key = :project_key
        ORDER BY bm25(messages_fts)
        LIMIT :limit
    """, {"query": sanitized, "project_key": project_key, "limit": limit})

    return [
        {
            "id": r.id,
            "subject": r.subject,
            "from": r.sender_name,
            "created_ts": r.created_ts.isoformat(),
            "importance": r.importance,
            "thread_id": r.thread_id,
            "snippet": r.snippet
        }
        for r in results
    ]
```

---

## Query Tracking

Track queries to detect performance issues.

### Query Counter

```python
import threading
from contextlib import contextmanager
from collections import defaultdict
from time import perf_counter

class QueryTracker:
    """Track query patterns and performance."""

    _local = threading.local()

    @classmethod
    def get_stats(cls) -> dict:
        """Get current request's query stats."""
        if not hasattr(cls._local, 'stats'):
            cls._local.stats = {
                'count': 0,
                'total_time': 0.0,
                'queries': [],
                'slow_queries': []
            }
        return cls._local.stats

    @classmethod
    def reset(cls):
        """Reset stats for new request."""
        cls._local.stats = {
            'count': 0,
            'total_time': 0.0,
            'queries': [],
            'slow_queries': []
        }

    @classmethod
    @contextmanager
    def track(cls, query: str):
        """Track a single query."""
        stats = cls.get_stats()
        start = perf_counter()

        try:
            yield
        finally:
            elapsed = perf_counter() - start
            stats['count'] += 1
            stats['total_time'] += elapsed
            stats['queries'].append({
                'query': query[:200],  # Truncate
                'time': elapsed
            })

            # Flag slow queries (>100ms)
            if elapsed > 0.1:
                stats['slow_queries'].append({
                    'query': query,
                    'time': elapsed
                })

    @classmethod
    def report(cls) -> str:
        """Generate performance report."""
        stats = cls.get_stats()
        report = f"Queries: {stats['count']}, Total: {stats['total_time']*1000:.1f}ms"

        if stats['slow_queries']:
            report += f"\nSlow queries ({len(stats['slow_queries'])}):"
            for sq in stats['slow_queries'][:3]:
                report += f"\n  - {sq['time']*1000:.1f}ms: {sq['query'][:100]}"

        return report
```

### Integration with SQLAlchemy

```python
from sqlalchemy import event

def setup_query_tracking(engine):
    """Attach query tracking to SQLAlchemy engine."""

    @event.listens_for(engine, "before_cursor_execute")
    def before_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info['query_start'] = perf_counter()

    @event.listens_for(engine, "after_cursor_execute")
    def after_execute(conn, cursor, statement, parameters, context, executemany):
        elapsed = perf_counter() - conn.info.get('query_start', perf_counter())
        stats = QueryTracker.get_stats()
        stats['count'] += 1
        stats['total_time'] += elapsed

        if elapsed > 0.1:  # 100ms threshold
            stats['slow_queries'].append({
                'query': statement,
                'params': str(parameters)[:100],
                'time': elapsed
            })
```

### N+1 Detection

```python
def detect_n_plus_one(stats: dict) -> list[str]:
    """Detect potential N+1 patterns from query log."""
    warnings = []

    # Group similar queries
    query_patterns = defaultdict(int)
    for q in stats['queries']:
        # Normalize query (remove specific values)
        normalized = re.sub(r"'[^']*'", "'?'", q['query'])
        normalized = re.sub(r"\d+", "?", normalized)
        query_patterns[normalized] += 1

    # Flag patterns that repeat many times
    for pattern, count in query_patterns.items():
        if count > 5:
            warnings.append(
                f"Possible N+1: Query pattern executed {count} times:\n  {pattern[:100]}"
            )

    return warnings
```

---

## Index Strategy

Strategic indexes for MCP access patterns.

### Common Access Patterns

```python
# Index for common queries

# 1. Agent lookup by project
# Query: WHERE project_key = ? AND name = ?
db.execute("CREATE INDEX IF NOT EXISTS idx_agents_project_name ON agents(project_key, name)")

# 2. Messages by recipient (inbox)
# Query: WHERE recipient_name = ? ORDER BY created_ts DESC
db.execute("CREATE INDEX IF NOT EXISTS idx_recipients_agent_created ON recipients(agent_name, created_ts DESC)")

# 3. Messages by thread
# Query: WHERE thread_id = ? ORDER BY created_ts
db.execute("CREATE INDEX IF NOT EXISTS idx_messages_thread_created ON messages(thread_id, created_ts)")

# 4. File reservations by project (conflict check)
# Query: WHERE project_key = ? AND released_ts IS NULL AND expires_ts > ?
db.execute("""
    CREATE INDEX IF NOT EXISTS idx_reservations_active
    ON file_reservations(project_key, released_ts, expires_ts)
    WHERE released_ts IS NULL
""")

# 5. Agent activity (staleness check)
# Query: WHERE last_active_ts < ?
db.execute("CREATE INDEX IF NOT EXISTS idx_agents_last_active ON agents(last_active_ts)")
```

### Partial Indexes

```python
# Partial index for active reservations only
db.execute("""
    CREATE INDEX IF NOT EXISTS idx_active_reservations
    ON file_reservations(project_key, path_pattern)
    WHERE released_ts IS NULL AND expires_ts > datetime('now')
""")

# Partial index for unread messages
db.execute("""
    CREATE INDEX IF NOT EXISTS idx_unread_messages
    ON recipients(agent_name, message_id)
    WHERE read_ts IS NULL
""")

# Partial index for urgent messages
db.execute("""
    CREATE INDEX IF NOT EXISTS idx_urgent_messages
    ON messages(project_key, created_ts DESC)
    WHERE importance IN ('high', 'urgent')
""")
```

### Covering Indexes

```python
# Covering index: Include all columns needed for query
# Avoids table lookup entirely
db.execute("""
    CREATE INDEX IF NOT EXISTS idx_inbox_covering
    ON recipients(agent_name, message_id, read_ts, ack_ts)
    INCLUDE (created_ts)
""")
```

---

## Connection Management

Proper connection handling prevents resource exhaustion.

### Connection Pool

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

def create_optimized_engine(db_path: str):
    """Create engine with optimized connection pool."""
    return create_engine(
        f"sqlite:///{db_path}",
        poolclass=QueuePool,
        pool_size=5,           # Base connections
        max_overflow=10,       # Additional under load
        pool_timeout=30,       # Wait for connection
        pool_recycle=3600,     # Recycle after 1 hour
        pool_pre_ping=True,    # Verify connection health
        connect_args={
            "check_same_thread": False,  # Allow multi-threaded
            "timeout": 30                 # SQLite busy timeout
        }
    )
```

### SQLite Pragmas

```python
from sqlalchemy import event

def configure_sqlite(engine):
    """Configure SQLite for performance."""

    @event.listens_for(engine, "connect")
    def set_pragmas(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()

        # WAL mode for concurrent reads
        cursor.execute("PRAGMA journal_mode=WAL")

        # Increase cache size (negative = KB)
        cursor.execute("PRAGMA cache_size=-64000")  # 64MB

        # Synchronous mode (NORMAL for balance)
        cursor.execute("PRAGMA synchronous=NORMAL")

        # Memory-mapped I/O
        cursor.execute("PRAGMA mmap_size=268435456")  # 256MB

        # Temp storage in memory
        cursor.execute("PRAGMA temp_store=MEMORY")

        cursor.close()
```

---

## Caching Patterns

Cache expensive computations and frequent queries.

### Pre-computed Validation Sets

```python
from functools import lru_cache

# Pre-compute at module load for O(1) lookup
_ADJECTIVES: frozenset[str] = frozenset()
_NOUNS: frozenset[str] = frozenset()
_VALID_NAMES: frozenset[str] = frozenset()

def _load_wordlists():
    """Load wordlists once at startup."""
    global _ADJECTIVES, _NOUNS, _VALID_NAMES

    _ADJECTIVES = frozenset(load_file("adjectives.txt"))
    _NOUNS = frozenset(load_file("nouns.txt"))

    # Pre-compute all valid combinations
    _VALID_NAMES = frozenset(
        f"{adj.title()}{noun.title()}"
        for adj in _ADJECTIVES
        for noun in _NOUNS
    )

# Call at module load
_load_wordlists()

def is_valid_agent_name(name: str) -> bool:
    """O(1) validation using pre-computed set."""
    return name in _VALID_NAMES
```

### LRU Cache for Expensive Queries

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def get_project_stats_cached(project_key: str, cache_time: str) -> dict:
    """
    Cached project statistics.

    cache_time parameter forces cache invalidation (pass current minute).
    """
    return {
        "agent_count": db.query(Agent).filter(Agent.project_key == project_key).count(),
        "message_count": db.query(Message).filter(Message.project_key == project_key).count(),
        "active_reservations": db.query(FileReservation).filter(
            FileReservation.project_key == project_key,
            FileReservation.released_ts.is_(None)
        ).count()
    }

def get_project_stats(project_key: str) -> dict:
    """Get project stats with 1-minute cache."""
    # Cache key includes current minute
    cache_key = datetime.now().strftime("%Y-%m-%d-%H-%M")
    return get_project_stats_cached(project_key, cache_key)
```

### Time-Based Cache Invalidation

```python
from time import time

class TTLCache:
    """Simple TTL cache for MCP responses."""

    def __init__(self, ttl_seconds: int = 60):
        self._cache: dict = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> tuple[bool, any]:
        """Get value if not expired. Returns (hit, value)."""
        if key in self._cache:
            value, expires = self._cache[key]
            if time() < expires:
                return True, value
            del self._cache[key]
        return False, None

    def set(self, key: str, value: any):
        """Set value with TTL."""
        self._cache[key] = (value, time() + self._ttl)

    def invalidate(self, key: str):
        """Explicitly invalidate a key."""
        self._cache.pop(key, None)

    def clear(self):
        """Clear all cached values."""
        self._cache.clear()

# Usage
_agent_cache = TTLCache(ttl_seconds=30)

def list_agents(project_key: str) -> list[dict]:
    cache_key = f"agents:{project_key}"
    hit, cached = _agent_cache.get(cache_key)
    if hit:
        return cached

    agents = db.query(Agent).filter(Agent.project_key == project_key).all()
    result = [a.to_dict() for a in agents]

    _agent_cache.set(cache_key, result)
    return result
```

---

## Batch Operations

Batch writes for efficiency.

### Bulk Insert

```python
def send_to_multiple_recipients(
    message: Message,
    recipients: list[str]
) -> list[Recipient]:
    """Batch insert recipients."""
    # BAD: Individual inserts
    # for name in recipients:
    #     db.add(Recipient(message_id=message.id, agent_name=name))

    # GOOD: Bulk insert
    recipient_objects = [
        Recipient(message_id=message.id, agent_name=name)
        for name in recipients
    ]
    db.bulk_save_objects(recipient_objects)
    db.commit()

    return recipient_objects
```

### Batch Update

```python
def mark_messages_read(
    agent_name: str,
    message_ids: list[int]
) -> int:
    """Batch update read status."""
    now = datetime.now(UTC)

    # Single UPDATE statement
    updated = db.query(Recipient).filter(
        Recipient.agent_name == agent_name,
        Recipient.message_id.in_(message_ids),
        Recipient.read_ts.is_(None)
    ).update(
        {"read_ts": now},
        synchronize_session=False
    )

    db.commit()
    return updated
```

### Batch Delete

```python
def cleanup_expired_reservations() -> int:
    """Batch delete expired reservations."""
    now = datetime.now(UTC)

    # Single DELETE statement
    deleted = db.query(FileReservation).filter(
        FileReservation.expires_ts < now,
        FileReservation.released_ts.is_(None)
    ).update(
        {"released_ts": now},  # Soft delete
        synchronize_session=False
    )

    db.commit()
    return deleted
```

---

## Summary: Optimization Checklist

| # | Pattern | Benefit |
|---|---------|---------|
| 1 | **Eager loading** | Eliminate N+1 queries |
| 2 | **FTS5 sanitization** | Safe, fast full-text search |
| 3 | **Query tracking** | Detect performance issues |
| 4 | **Strategic indexes** | Fast lookups for common patterns |
| 5 | **Partial indexes** | Smaller, faster indexes |
| 6 | **Connection pooling** | Prevent resource exhaustion |
| 7 | **SQLite pragmas** | Optimize for concurrent access |
| 8 | **Pre-computed sets** | O(1) validation |
| 9 | **TTL caching** | Reduce repeated queries |
| 10 | **Batch operations** | Efficient bulk writes |
