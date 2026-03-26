# Git Integration Patterns

## Table of Contents
- [Philosophy](#philosophy)
- [Dual Persistence Architecture](#dual-persistence-architecture)
- [File Descriptor Management](#file-descriptor-management)
- [Identity Resolution](#identity-resolution)
- [Commit Info Extraction](#commit-info-extraction)
- [Archive Structure](#archive-structure)
- [Path Security](#path-security)
- [Composable Hooks](#composable-hooks)

---

## Philosophy

**Git as audit trail, SQLite as query engine.**

Git provides:
- Human-auditable history (`git log`, `git blame`)
- Disaster recovery (distributed backups)
- Diff infrastructure (what changed, when, who)
- Merge conflict resolution (human-in-the-loop)

SQLite provides:
- Fast queries (FTS5 full-text search)
- Indexed lookups (O(1) by ID)
- Aggregate functions (unread counts, stats)
- Filtering and pagination

**Best of both worlds:** Write to both, read from the one that fits the query.

---

## Dual Persistence Architecture

### Message Storage

```python
# 1. Write to SQLite for queries
message = Message(
    project_id=project.id,
    sender_id=agent.id,
    subject=subject,
    body_md=body_md,
    importance=importance,
    ack_required=ack_required,
)
session.add(message)
await session.commit()

# 2. Write to Git for audit trail
message_path = _compute_message_path(project, message)
_write_message_file(archive, message_path, message)
_commit_message(archive, f"Message {message.id}: {subject[:50]}")
```

### File Layout

```
{storage_root}/
├── projects/
│   └── {slug}/
│       ├── messages/
│       │   ├── YYYY/MM/
│       │   │   └── {iso-timestamp}__{subject-slug}__{id}.md
│       │   └── threads/
│       │       └── {thread_id}.md  # Append-only digest
│       ├── agents/
│       │   └── {agent_name}/
│       │       ├── profile.json
│       │       ├── inbox/YYYY/MM/
│       │       └── outbox/YYYY/MM/
│       └── file_reservations/
│           └── {sha1(pattern)}.json
└── .git/
```

### Message File Format

```markdown
---
{
  "id": 1234,
  "thread_id": "TASK-123",
  "project": "/data/projects/backend",
  "project_slug": "backend",
  "from": "BlueLake",
  "to": ["GreenCastle"],
  "cc": [],
  "bcc": [],
  "subject": "[TASK-123] Migration complete",
  "importance": "normal",
  "ack_required": false,
  "created": "2025-01-15T10:30:00+00:00",
  "attachments": []
}
---

Database migration finished successfully.

## Changes
- Added `users.last_login` column
- Migrated 1.2M rows
- Created index on `users(email)`

Ready for API updates.
```

**Why JSON frontmatter?** Simpler than YAML, no ambiguity, easy to parse.

---

## File Descriptor Management

### The Problem

GitPython's `Repo` objects hold file descriptors. Under heavy load:
- Too many open repos = EMFILE (too many open files)
- Leaked FDs = resource exhaustion
- Unclosed repos = memory leaks

### Solution 1: Context Manager

```python
from contextlib import contextmanager
from typing import Generator
from git import Repo

@contextmanager
def _git_repo(path: str) -> Generator[Repo, None, None]:
    """
    Context manager that ensures Repo.close() is always called.

    Usage:
        with _git_repo("/path/to/repo") as repo:
            repo.index.add(["file.md"])
            repo.index.commit("Add file")
    """
    repo = Repo(path)
    try:
        yield repo
    finally:
        repo.close()
```

### Solution 2: LRU Cache with Cleanup

```python
from collections import OrderedDict
from git import Repo

class _LRURepoCache:
    """
    Size-limited cache that closes evicted repos.

    Prevents FD exhaustion while maintaining performance
    for frequently accessed repos.
    """

    def __init__(self, maxsize: int = 16):
        self._cache: OrderedDict[str, Repo] = OrderedDict()
        self._maxsize = maxsize

    def get(self, key: str) -> Repo | None:
        """Get repo, moving to end (most recently used)."""
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None

    def put(self, key: str, repo: Repo) -> None:
        """Add repo, evicting oldest if at capacity."""
        if key in self._cache:
            self._cache.move_to_end(key)
            return

        # Evict oldest if at capacity
        if len(self._cache) >= self._maxsize:
            _, evicted = self._cache.popitem(last=False)
            evicted.close()  # CRITICAL: Close to free FD

        self._cache[key] = repo

    def clear(self) -> int:
        """Close all repos and clear cache. Returns count cleared."""
        count = len(self._cache)
        for repo in self._cache.values():
            try:
                repo.close()
            except Exception:
                pass
        self._cache.clear()
        return count

    def __len__(self) -> int:
        return len(self._cache)
```

### EMFILE Recovery Pattern

```python
import gc

# Whitelist of tools safe to retry after EMFILE
_EMFILE_SAFE_TOOLS = frozenset({
    "fetch_inbox",
    "search_messages",
    "list_agents",
    "whois",
    # Read-only, idempotent tools only
})

async def handle_emfile_error(tool_name: str, func: Callable, *args, **kwargs):
    """
    Handle EMFILE by clearing caches and retrying.

    Only retries for whitelisted safe-to-retry tools.
    """
    try:
        return await func(*args, **kwargs)
    except OSError as e:
        if e.errno != errno.EMFILE:
            raise

        if tool_name not in _EMFILE_SAFE_TOOLS:
            raise ToolExecutionError(
                "RESOURCE_EXHAUSTED",
                "Too many open files. Please retry.",
                recoverable=True,
                data={"tool": tool_name, "safe_to_retry": False}
            )

        # Clear caches and retry
        cleared = _repo_cache.clear()
        gc.collect()
        await asyncio.sleep(0.05)  # Brief pause

        try:
            return await func(*args, **kwargs)
        except OSError:
            raise ToolExecutionError(
                "RESOURCE_EXHAUSTED",
                f"Too many open files even after clearing {cleared} cached repos.",
                recoverable=True,
                data={"cleared_repos": cleared}
            )
```

---

## Identity Resolution

### The Problem

Same project, different machines:
- `$HOME/projects/backend` (Mac example)
- `$HOME/work/backend` (example Linux path)
- `%USERPROFILE%\Projects\backend` (CI Windows example)

All should share one mailbox if they're the same Git repo.

### Solution: Identity Precedence

```python
def resolve_project_identity(path: str, mode: str = "dir") -> tuple[str, str]:
    """
    Resolve canonical project identity.

    Returns:
        (project_uid, slug) where:
        - project_uid is stable across machines
        - slug is human-readable presentation key

    Modes:
        dir: Use directory path (default, backward compatible)
        git-remote: Use normalized remote URL
        git-toplevel: Use repo root directory
        git-common-dir: Use git-common-dir (supports worktrees)
    """

    # Precedence hierarchy (first hit wins):

    # 1. Committed marker file
    marker_path = Path(path) / ".agent-mail-project-id"
    if marker_path.exists():
        return _read_marker(marker_path)

    # 2. Discovery YAML override
    yaml_path = Path(path) / ".agent-mail.yaml"
    if yaml_path.exists():
        override = _parse_discovery_yaml(yaml_path)
        if override.get("project_uid"):
            return override["project_uid"], _compute_slug(override)

    # 3. Private marker (in .git, not committed)
    private_marker = Path(path) / ".git" / "agent-mail" / "project-id"
    if private_marker.exists():
        return _read_marker(private_marker)

    # 4. Git-based identity
    if mode == "git-remote":
        return _identity_from_remote(path)
    elif mode == "git-toplevel":
        return _identity_from_toplevel(path)
    elif mode == "git-common-dir":
        return _identity_from_common_dir(path)

    # 5. Fallback: directory path hash
    return _identity_from_path(path)


def _identity_from_remote(path: str) -> tuple[str, str]:
    """
    Normalize remote URL to portable identity.

    Examples:
        git@github.com:owner/repo.git → github.com/owner/repo
        https://github.com/owner/repo.git → github.com/owner/repo
    """
    try:
        with _git_repo(path) as repo:
            remote = repo.remotes.origin.url
            normalized = _normalize_remote_url(remote)
            uid = hashlib.sha1(normalized.encode()).hexdigest()[:10]
            slug = f"{Path(path).name}-{uid}"
            return uid, slug
    except Exception:
        return _identity_from_path(path)


def _normalize_remote_url(url: str) -> str:
    """
    Normalize Git remote URL to canonical form.

    Handles:
        - SSH: git@host:owner/repo.git
        - HTTPS: https://host/owner/repo.git
        - Trailing .git
        - Case sensitivity
    """
    # SSH format
    if url.startswith("git@"):
        match = re.match(r"git@([^:]+):(.+?)(?:\.git)?$", url)
        if match:
            return f"{match.group(1)}/{match.group(2)}".lower()

    # HTTPS format
    parsed = urlparse(url)
    if parsed.scheme in ("http", "https"):
        path = parsed.path.rstrip("/")
        if path.endswith(".git"):
            path = path[:-4]
        return f"{parsed.netloc}{path}".lower()

    return url.lower()
```

### Privacy-Safe Slugs

```python
def _compute_safe_slug(path: str, uid: str) -> str:
    """
    Generate slug that doesn't leak filesystem structure.

    Pattern: {basename}-{uid_prefix}
    Example: backend-a1b2c3d4e5
    """
    basename = Path(path).name
    # Sanitize basename
    safe_name = re.sub(r"[^a-z0-9]", "-", basename.lower()).strip("-")[:40]
    return f"{safe_name}-{uid[:10]}"
```

---

## Commit Info Extraction

### Rich Commit Metadata

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class CommitInfo:
    hexsha: str           # Short hash (12 chars)
    summary: str          # First line of message
    authored_ts: datetime # Author timestamp
    insertions: int       # Lines added
    deletions: int        # Lines removed
    files_changed: int    # Number of files
    diff_hunks: int       # Number of hunks
    diff_preview: str     # First 12 +/- lines


async def extract_commit_info(
    archive: ProjectArchive,
    file_path: str,
    limit: int = 5,
) -> list[CommitInfo]:
    """
    Extract commit info for a file.

    Runs in thread pool to avoid blocking async loop.
    """
    def _extract():
        infos = []
        with _git_repo(archive.repo_root) as repo:
            for commit in repo.iter_commits(paths=file_path, max_count=limit):
                # Get diff stats
                if commit.parents:
                    diff = commit.diff(commit.parents[0], create_patch=True)
                    insertions = sum(d.diff.count(b"\n+") for d in diff if d.diff)
                    deletions = sum(d.diff.count(b"\n-") for d in diff if d.diff)
                    diff_preview = _extract_diff_preview(diff, max_lines=12)
                else:
                    insertions = deletions = 0
                    diff_preview = ""

                infos.append(CommitInfo(
                    hexsha=commit.hexsha[:12],
                    summary=commit.summary,
                    authored_ts=datetime.fromtimestamp(commit.authored_date),
                    insertions=insertions,
                    deletions=deletions,
                    files_changed=len(commit.stats.files),
                    diff_hunks=len(diff) if commit.parents else 0,
                    diff_preview=diff_preview,
                ))
        return infos

    return await asyncio.to_thread(_extract)
```

---

## Archive Structure

### Time-Partitioned Paths

```python
def _compute_message_path(project: Project, message: Message) -> str:
    """
    Compute path for message file.

    Pattern: messages/YYYY/MM/{timestamp}__{subject-slug}__{id}.md

    Benefits:
        - Easy to browse by date
        - Prevents huge directories
        - Sorts chronologically
        - Human-readable filenames
    """
    created = message.created_at
    year_month = created.strftime("%Y/%m")

    # Timestamp (filesystem-safe)
    timestamp = created.strftime("%Y-%m-%dT%H-%M-%SZ")

    # Subject slug (safe characters, truncated)
    subject_slug = _slugify_subject(message.subject)[:80] or "message"

    return f"messages/{year_month}/{timestamp}__{subject_slug}__{message.id}.md"


def _slugify_subject(subject: str) -> str:
    """Convert subject to filesystem-safe slug."""
    # Remove/replace unsafe characters
    slug = re.sub(r"[^a-zA-Z0-9._-]", "-", subject)
    # Collapse multiple dashes
    slug = re.sub(r"-+", "-", slug)
    # Strip leading/trailing
    return slug.strip("-_").lower()
```

### Agent Mailboxes

```python
def _compute_inbox_path(agent: Agent, message: Message) -> str:
    """
    Compute path for inbox copy.

    Pattern: agents/{name}/inbox/YYYY/MM/{id}.md

    Benefits:
        - Per-agent browsing
        - Time partitioned
        - Quick inbox listing with ls
    """
    created = message.created_at
    year_month = created.strftime("%Y/%m")
    return f"agents/{agent.name}/inbox/{year_month}/{message.id}.md"
```

---

## Path Security

### Traversal Prevention

```python
def _resolve_safe_path(
    archive: ProjectArchive,
    relative_path: str,
) -> Path:
    """
    Resolve path safely, preventing directory traversal.

    Raises ValueError if path escapes archive root.
    """
    # Normalize separators
    normalized = relative_path.strip().replace("\\", "/")

    # Reject obvious traversal patterns
    dangerous_patterns = [
        "..",
        "/../",
        "/..",
        normalized.startswith("/"),
        normalized.startswith("~"),
    ]
    if any(dangerous_patterns):
        raise ValueError(f"Invalid path: {relative_path}")

    # Resolve and verify containment
    root = archive.root.resolve()
    candidate = (archive.root / normalized).resolve()

    try:
        candidate.relative_to(root)
    except ValueError:
        raise ValueError(f"Path escapes archive root: {relative_path}")

    return candidate
```

### Safe Filename Generation

```python
import hashlib

def _safe_filename(value: str, max_length: int = 128) -> str:
    """
    Generate safe filename from arbitrary string.

    If value contains unsafe characters, hashes it.
    """
    # Try to use value directly if safe
    if re.match(r"^[a-zA-Z0-9._-]+$", value) and len(value) <= max_length:
        return value

    # Hash for safety
    hash_suffix = hashlib.sha1(value.encode()).hexdigest()[:10]
    safe_prefix = re.sub(r"[^a-zA-Z0-9]", "", value)[:max_length - 11]
    return f"{safe_prefix}_{hash_suffix}"
```

---

## Composable Hooks

### Chain-Runner Pattern

Install hooks that compose with existing tooling (Husky, pre-commit, lefthook):

```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit (chain-runner)

set -e

HOOK_NAME="pre-commit"
HOOKS_DIR="${GIT_DIR:-$(git rev-parse --git-dir)}/hooks.d/${HOOK_NAME}"

# Run scripts in hooks.d/pre-commit/*
if [[ -d "$HOOKS_DIR" ]]; then
    for script in "$HOOKS_DIR"/*; do
        if [[ -x "$script" ]]; then
            "$script" "$@" || exit $?
        fi
    done
fi

# Run original hook if it was saved
ORIG_HOOK="${GIT_DIR:-$(git rev-parse --git-dir)}/hooks/${HOOK_NAME}.orig"
if [[ -x "$ORIG_HOOK" ]]; then
    "$ORIG_HOOK" "$@" || exit $?
fi

exit 0
```

### Installation Strategy

```python
def install_hook(repo_path: str, hook_name: str, script_content: str) -> bool:
    """
    Install hook script composably.

    1. If no existing hook: install chain-runner + our script
    2. If chain-runner exists: just add our script to hooks.d
    3. If other hook exists: save as .orig, install chain-runner
    """
    git_dir = Path(repo_path) / ".git"
    hooks_dir = git_dir / "hooks"
    chain_runner = hooks_dir / hook_name
    hooks_d = git_dir / "hooks.d" / hook_name

    # Ensure hooks.d exists
    hooks_d.mkdir(parents=True, exist_ok=True)

    # Write our script
    our_script = hooks_d / "50-mcp-agent-mail"
    our_script.write_text(script_content)
    our_script.chmod(0o755)

    # Check if chain-runner already installed
    if chain_runner.exists():
        content = chain_runner.read_text()
        if "hooks.d" in content:
            return True  # Already using chain-runner

        # Save existing hook
        orig = hooks_dir / f"{hook_name}.orig"
        shutil.move(chain_runner, orig)

    # Install chain-runner
    chain_runner.write_text(CHAIN_RUNNER_TEMPLATE.format(hook_name=hook_name))
    chain_runner.chmod(0o755)

    return True
```

### Pre-Push Correctness

```python
def parse_pre_push_stdin() -> list[tuple[str, str, str, str]]:
    """
    Parse pre-push hook STDIN correctly.

    Format: <local_ref> <local_sha> <remote_ref> <remote_sha>

    Handle:
        - New branches (remote_sha is zeros)
        - Force pushes
        - Multiple refs per push
        - Tags
    """
    refs = []
    for line in sys.stdin:
        parts = line.strip().split()
        if len(parts) == 4:
            local_ref, local_sha, remote_ref, remote_sha = parts
            refs.append((local_ref, local_sha, remote_ref, remote_sha))
    return refs


def get_commits_to_push(local_sha: str, remote_sha: str) -> list[str]:
    """
    Get commits that will be pushed.

    Handles new branches (zeros remote) correctly.
    """
    # New branch: remote SHA is all zeros
    if remote_sha == "0" * 40:
        # All commits reachable from local_sha
        result = subprocess.run(
            ["git", "rev-list", local_sha],
            capture_output=True, text=True
        )
    else:
        # Commits between remote and local
        result = subprocess.run(
            ["git", "rev-list", f"{remote_sha}..{local_sha}"],
            capture_output=True, text=True
        )

    return result.stdout.strip().split("\n") if result.stdout.strip() else []
```

---

## Testing Git Integration

```python
import pytest
from pathlib import Path

@pytest.fixture
def git_repo(tmp_path):
    """Create isolated Git repo for testing."""
    repo_path = tmp_path / "repo"
    repo_path.mkdir()

    # Initialize
    subprocess.run(["git", "init"], cwd=repo_path, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_path, check=True
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=repo_path, check=True
    )

    # Initial commit
    (repo_path / "README.md").write_text("# Test")
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial"], cwd=repo_path, check=True)

    yield repo_path

    # Cleanup
    shutil.rmtree(repo_path)


class TestIdentityResolution:
    def test_dir_mode_uses_path(self, git_repo):
        uid, slug = resolve_project_identity(str(git_repo), mode="dir")
        assert "repo" in slug

    def test_marker_takes_precedence(self, git_repo):
        marker = git_repo / ".agent-mail-project-id"
        marker.write_text("custom-uid\ncustom-slug")

        uid, slug = resolve_project_identity(str(git_repo), mode="git-remote")
        assert uid == "custom-uid"
        assert slug == "custom-slug"


class TestPathSecurity:
    def test_rejects_traversal(self, git_repo):
        archive = ProjectArchive(root=git_repo)

        with pytest.raises(ValueError, match="traversal"):
            _resolve_safe_path(archive, "../../../etc/passwd")

    def test_rejects_absolute(self, git_repo):
        archive = ProjectArchive(root=git_repo)

        with pytest.raises(ValueError):
            _resolve_safe_path(archive, "/etc/passwd")
```
