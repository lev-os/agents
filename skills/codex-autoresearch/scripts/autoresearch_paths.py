#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from autoresearch_core import (
    AUTORESEARCH_OWNED_BASENAMES,
    EXEC_SCRATCH_ROOT,
    AutoresearchError,
    LESSONS_FILE_NAME,
    LAUNCH_MANIFEST_NAME,
    ParsedLog,
    RUNTIME_LOG_NAME,
    RUNTIME_STATE_NAME,
)

RUNS_DIR_NAME = ".autoresearch/runs"
CHECKPOINT_LOCK_NAME = "checkpoint.lock"


@dataclass(frozen=True)
class GitStatusEntry:
    status: str
    paths: tuple[str, ...]

    @property
    def staged_code(self) -> str:
        return self.status[0] if self.status else " "

    @property
    def unstaged_code(self) -> str:
        return self.status[1] if len(self.status) > 1 else " "

    @property
    def has_staged_change(self) -> bool:
        return self.staged_code not in {" ", "?"}

    @property
    def touched_paths(self) -> tuple[str, ...]:
        return self.paths


def lexical_abspath(path: Path | None = None) -> Path:
    return Path(os.path.abspath(str(path or Path.cwd())))


def find_repo_root(start: Path | None = None) -> Path:
    current = lexical_abspath(start)
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return current


def canonical_repo_root(start: Path | None = None) -> Path:
    return find_repo_root(start).resolve()


def has_git_repo(start: Path | None = None) -> bool:
    return (find_repo_root(start) / ".git").exists()


def sanitize_run_tag(run_tag: str | None) -> str:
    text = " ".join(str(run_tag or "").split()).strip()
    if not text:
        return ""
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip("._-")
    return slug or ""


def run_artifact_root(cwd: Path | None = None, run_tag: str | None = None) -> Path:
    repo = find_repo_root(cwd)
    slug = sanitize_run_tag(run_tag)
    if not slug:
        return repo
    return repo / RUNS_DIR_NAME / slug


def default_results_path(cwd: Path | None = None, run_tag: str | None = None) -> Path:
    return run_artifact_root(cwd, run_tag) / "research-results.tsv"


def default_launch_manifest_path(cwd: Path | None = None, run_tag: str | None = None) -> Path:
    return run_artifact_root(cwd, run_tag) / LAUNCH_MANIFEST_NAME


def default_runtime_state_path(cwd: Path | None = None, run_tag: str | None = None) -> Path:
    return run_artifact_root(cwd, run_tag) / RUNTIME_STATE_NAME


def default_runtime_log_path(cwd: Path | None = None, run_tag: str | None = None) -> Path:
    return run_artifact_root(cwd, run_tag) / RUNTIME_LOG_NAME


def default_lessons_path(cwd: Path | None = None, run_tag: str | None = None) -> Path:
    return run_artifact_root(cwd, run_tag) / LESSONS_FILE_NAME


def default_state_path(cwd: Path | None = None, run_tag: str | None = None) -> Path:
    if cwd is None and not sanitize_run_tag(run_tag):
        return Path("autoresearch-state.json")
    return run_artifact_root(cwd, run_tag) / "autoresearch-state.json"


def default_checkpoint_lock_path(cwd: Path | None = None) -> Path:
    return find_repo_root(cwd) / ".autoresearch" / CHECKPOINT_LOCK_NAME


def results_repo_root(results_path: Path) -> Path:
    context = results_path.parent if results_path.is_absolute() else lexical_abspath(results_path.parent)
    return find_repo_root(context)


def resolve_repo_path(repo_arg: str | None) -> Path:
    return find_repo_root(Path(repo_arg or Path.cwd())).resolve()


def resolve_repo_relative(repo: Path, raw: str | None, default_path: Path) -> Path:
    if raw is None:
        return default_path
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = repo / candidate
    return candidate.resolve()


def resolve_repo_managed_path(
    requested_path: str | None,
    *,
    results_path: Path,
    default_name: str,
) -> Path:
    repo = results_repo_root(results_path)
    if requested_path is None:
        return repo / default_name

    candidate = Path(requested_path)
    if not candidate.is_absolute():
        candidate = repo / candidate
    return lexical_abspath(candidate)


def parse_scope_patterns(scope_text: str | None) -> list[str]:
    if not scope_text:
        return []
    return [token for token in re.split(r"[\s,]+", scope_text.strip()) if token]


def path_is_in_scope(path: str, patterns: list[str]) -> bool:
    if not patterns:
        return False

    normalized = path.replace("\\", "/")
    stripped_path = normalized.lstrip("./")
    candidate = PurePosixPath(stripped_path)
    for pattern in patterns:
        pattern = pattern.strip()
        if not pattern:
            continue

        normalized_pattern = pattern.replace("\\", "/").lstrip("./")
        is_glob = any(marker in normalized_pattern for marker in "*?[")
        base = normalized_pattern.rstrip("/")

        if normalized_pattern.endswith("/") or not is_glob:
            if base and (stripped_path == base or stripped_path.startswith(f"{base}/")):
                return True

        variants = {normalized_pattern}
        while True:
            expanded = {variant.replace("**/", "") for variant in variants if "**/" in variant}
            expanded -= variants
            if not expanded:
                break
            variants |= expanded

        if any(candidate.match(variant) for variant in variants):
            return True

    return False


def is_autoresearch_owned_artifact(path: str | Path) -> bool:
    candidate = Path(path)
    names = [candidate.name]
    parent_name = candidate.parent.name
    if parent_name and parent_name != ".":
        names.append(parent_name)

    for name in names:
        pending = [name]
        seen = set()
        while pending:
            current = pending.pop()
            if current in seen:
                continue
            seen.add(current)
            if current in AUTORESEARCH_OWNED_BASENAMES:
                return True
            for base in AUTORESEARCH_OWNED_BASENAMES:
                if current.startswith(f"{base}.") or current.endswith(f".{base}"):
                    return True

            path_name = Path(current)
            suffix = path_name.suffix
            if suffix:
                stem = path_name.stem
                for marker in (".prev", ".bak", ".tmp"):
                    if stem.endswith(marker):
                        pending.append(f"{stem[: -len(marker)]}{suffix}")
            for marker in (".prev", ".bak", ".tmp"):
                if current.endswith(marker):
                    pending.append(current[: -len(marker)])
    return False


def default_exec_state_path(cwd: Path | None = None) -> Path:
    repo_root = canonical_repo_root(cwd)
    digest = hashlib.sha256(str(repo_root).encode("utf-8")).hexdigest()[:12]
    return EXEC_SCRATCH_ROOT / digest / "autoresearch-state.exec.json"


def prev_archive_path(path: Path) -> Path:
    if path.suffix:
        return path.with_name(f"{path.stem}.prev{path.suffix}")
    return path.with_name(f"{path.name}.prev")


def archive_path_to_prev(path: Path) -> Path | None:
    if not path.exists():
        return None
    archive_path = prev_archive_path(path)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    path.replace(archive_path)
    return archive_path


def resolve_state_path(
    requested_path: str | None,
    *,
    mode: str | None = None,
    cwd: Path | None = None,
    allow_exec_scratch_fallback: bool = False,
    run_tag: str | None = None,
) -> Path:
    if requested_path:
        candidate = Path(requested_path)
        if candidate.is_absolute() or cwd is None:
            return candidate
        return lexical_abspath(find_repo_root(cwd) / candidate)

    repo_state_path = default_state_path(cwd, run_tag)
    if mode == "exec":
        return default_exec_state_path(cwd)
    if repo_state_path.exists():
        return repo_state_path

    if allow_exec_scratch_fallback:
        scratch_state_path = default_exec_state_path(cwd)
        if scratch_state_path.exists():
            return scratch_state_path
    return repo_state_path


def resolve_state_path_for_log(
    requested_path: str | None,
    parsed: ParsedLog | dict[str, str] | None,
    *,
    cwd: Path | None = None,
) -> Path:
    if isinstance(parsed, ParsedLog):
        metadata = parsed.metadata
    elif isinstance(parsed, dict):
        metadata = parsed
    else:
        metadata = {}
    mode = metadata.get("mode")
    exec_mode = mode == "exec"
    run_tag = metadata.get("run_tag")
    return resolve_state_path(
        requested_path,
        mode="exec" if exec_mode else None,
        cwd=cwd,
        allow_exec_scratch_fallback=exec_mode,
        run_tag=run_tag,
    )


def cleanup_exec_state(cwd: Path | None = None) -> tuple[Path, bool]:
    state_path = default_exec_state_path(cwd)
    removed = False
    if state_path.exists():
        state_path.unlink()
        removed = True

    scratch_root = EXEC_SCRATCH_ROOT.resolve()
    parent = state_path.parent
    while parent.exists() and parent != scratch_root:
        try:
            parent.rmdir()
        except OSError:
            break
        parent = parent.parent

    return state_path, removed


def git_status_entries(repo: Path) -> list[GitStatusEntry]:
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "-z",
        ],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        raise AutoresearchError(stderr or "git status failed")

    entries = [entry for entry in completed.stdout.decode("utf-8", errors="replace").split("\0") if entry]
    parsed_entries: list[GitStatusEntry] = []
    index = 0
    while index < len(entries):
        entry = entries[index]
        status = entry[:2]
        paths = [entry[3:] if len(entry) > 3 else entry]
        if "R" in status or "C" in status:
            if index + 1 < len(entries):
                paths.append(entries[index + 1])
            index += 1
        parsed_entries.append(GitStatusEntry(status=status, paths=tuple(paths)))
        index += 1
    return parsed_entries


def git_status_paths(repo: Path) -> list[str]:
    paths: list[str] = []
    for entry in git_status_entries(repo):
        paths.extend(entry.touched_paths)
    return paths
