#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from autoresearch_core import AutoresearchError
from autoresearch_paths import lexical_abspath, parse_scope_patterns


@dataclass(frozen=True)
class RepoTarget:
    path: Path
    scope: str
    role: str = "companion"

    @property
    def scope_patterns(self) -> list[str]:
        return parse_scope_patterns(self.scope)


def normalize_scope_text(scope_text: str | None) -> str:
    patterns = parse_scope_patterns(scope_text)
    if not patterns:
        raise AutoresearchError("Scope may not be empty.")
    return ",".join(patterns)


def resolve_repo_target_path(primary_repo: Path, raw_path: str) -> Path:
    candidate = Path(raw_path.strip())
    if not str(candidate):
        raise AutoresearchError("Repo target path may not be empty.")
    if not candidate.is_absolute():
        candidate = primary_repo / candidate
    return candidate.resolve()


def parse_companion_repo_scope_specs(
    *,
    primary_repo: Path,
    companion_repo_scopes: list[str],
) -> list[RepoTarget]:
    seen_paths = {str(lexical_abspath(primary_repo))}
    targets: list[RepoTarget] = []
    for spec in companion_repo_scopes:
        if "=" not in spec:
            raise AutoresearchError(
                f"Expected PATH=SCOPE for companion repo scope, got: {spec!r}"
            )
        raw_path, raw_scope = spec.split("=", 1)
        repo_path = resolve_repo_target_path(primary_repo, raw_path)
        if str(repo_path) in seen_paths:
            raise AutoresearchError(
                f"Duplicate repo target configured for multi-repo run: {repo_path}"
            )
        seen_paths.add(str(repo_path))
        targets.append(
            RepoTarget(
                path=repo_path,
                scope=normalize_scope_text(raw_scope),
                role="companion",
            )
        )
    return targets


def build_repo_targets(
    *,
    primary_repo: Path,
    primary_scope: str,
    companion_repo_scopes: list[str] | None = None,
) -> list[RepoTarget]:
    primary_repo = primary_repo.resolve()
    targets = [
        RepoTarget(
            path=primary_repo,
            scope=normalize_scope_text(primary_scope),
            role="primary",
        )
    ]
    targets.extend(
        parse_companion_repo_scope_specs(
            primary_repo=primary_repo,
            companion_repo_scopes=list(companion_repo_scopes or []),
        )
    )
    return targets


def parse_repo_commit_specs(
    *,
    primary_repo: Path,
    primary_commit: str,
    repo_commit_specs: list[str] | None = None,
) -> dict[str, str]:
    primary_repo = primary_repo.resolve()
    commits: dict[str, str] = {}
    if primary_commit and primary_commit != "-":
        commits[str(primary_repo)] = primary_commit

    for spec in list(repo_commit_specs or []):
        if "=" not in spec:
            raise AutoresearchError(
                f"Expected PATH=COMMIT for repo commit, got: {spec!r}"
            )
        raw_path, raw_commit = spec.split("=", 1)
        repo_path = resolve_repo_target_path(primary_repo, raw_path)
        commit = raw_commit.strip()
        if not commit:
            raise AutoresearchError("Repo commit value may not be empty.")
        existing = commits.get(str(repo_path))
        if existing is not None and existing != commit:
            raise AutoresearchError(
                f"Conflicting repo commit provenance for {repo_path}: {existing!r} vs {commit!r}"
            )
        commits[str(repo_path)] = commit

    return commits


def normalize_repo_commit_map(raw: Any) -> dict[str, str]:
    if not isinstance(raw, dict):
        return {}
    normalized: dict[str, str] = {}
    for key, value in raw.items():
        if not isinstance(key, str) or not key.strip():
            continue
        if not isinstance(value, str) or not value.strip():
            continue
        normalized[str(Path(key).resolve())] = value.strip()
    return normalized


def repo_commit_map_for_targets(
    *,
    repo_targets: list[RepoTarget],
    primary_commit: str,
    repo_commit_specs: list[str] | None = None,
    existing: dict[str, str] | None = None,
) -> dict[str, str]:
    if not repo_targets:
        raise AutoresearchError("repo_targets may not be empty")
    primary_targets = [target for target in repo_targets if target.role == "primary"]
    if len(primary_targets) != 1:
        raise AutoresearchError("repo_targets must contain exactly one primary repo")
    primary_repo = primary_targets[0].path.resolve()
    allowed_paths = {str(target.path.resolve()) for target in repo_targets}
    commits = {
        path: commit
        for path, commit in normalize_repo_commit_map(existing or {}).items()
        if path in allowed_paths
    }
    commits.update(
        parse_repo_commit_specs(
            primary_repo=primary_repo,
            primary_commit=primary_commit,
            repo_commit_specs=repo_commit_specs,
        )
    )
    return commits


def serialize_repo_targets(targets: list[RepoTarget]) -> list[dict[str, str]]:
    return [
        {
            "path": str(target.path),
            "scope": target.scope,
            "role": target.role,
        }
        for target in targets
    ]


def repo_targets_from_config(primary_repo: Path, config: dict[str, Any]) -> list[RepoTarget]:
    configured = config.get("repos")
    if not configured:
        return build_repo_targets(
            primary_repo=primary_repo,
            primary_scope=str(config.get("scope") or ""),
        )
    if not isinstance(configured, list):
        raise AutoresearchError("Launch config.repos must be a list.")

    primary_repo = primary_repo.resolve()
    targets: list[RepoTarget] = []
    seen_paths: set[str] = set()
    primary_count = 0
    for index, entry in enumerate(configured):
        if not isinstance(entry, dict):
            raise AutoresearchError("Each launch config.repos entry must be an object.")
        raw_path = entry.get("path")
        raw_scope = entry.get("scope")
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise AutoresearchError("Each launch config.repos entry must include a non-empty path.")
        repo_path = resolve_repo_target_path(primary_repo, raw_path)
        if str(repo_path) in seen_paths:
            raise AutoresearchError(f"Duplicate repo target configured for launch: {repo_path}")
        seen_paths.add(str(repo_path))

        role = str(entry.get("role") or "").strip() or (
            "primary" if index == 0 and repo_path == primary_repo else "companion"
        )
        if role not in {"primary", "companion"}:
            raise AutoresearchError(
                f"Unsupported repo target role {role!r}; expected 'primary' or 'companion'."
            )
        if role == "primary":
            primary_count += 1
        targets.append(
            RepoTarget(
                path=repo_path,
                scope=normalize_scope_text(raw_scope if isinstance(raw_scope, str) else None),
                role=role,
            )
        )

    if primary_count != 1:
        raise AutoresearchError("Launch config.repos must contain exactly one primary repo.")
    return targets


def primary_scope_from_config(primary_repo: Path, config: dict[str, Any]) -> str:
    for target in repo_targets_from_config(primary_repo, config):
        if target.role == "primary":
            return target.scope
    raise AutoresearchError("Launch config.repos is missing a primary repo entry.")


def format_repo_target_label(target: RepoTarget, primary_repo: Path) -> str:
    if target.path.resolve() == primary_repo.resolve():
        return "."
    return str(target.path)
