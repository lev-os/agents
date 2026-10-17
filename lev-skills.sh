#!/usr/bin/env python3
"""Skills runtime helper for the active surface and hidden catalog."""

from __future__ import annotations

import hashlib
import base64
import json
import math
import os
import posixpath
import random
import re
import selectors
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency fallback
    yaml = None


ROOT = Path(__file__).resolve().parent
SKILLS_DIR = ROOT / "skills"
SKILLS_DB_DIR = ROOT / "skills-db"
SKILL_REPOS_DIR = ROOT / "_repos"
WORKFLOW_FLOWS_DIR = SKILLS_DIR / "workflow" / "flows"
CDO_DIR = SKILLS_DIR / "cdo"
CACHE_DIR = Path(os.environ.get("LEV_CACHE_DIR", Path.home() / ".cache" / "lev-skills"))
CACHE_TTL_SECONDS = int(os.environ.get("LEV_SKILLS_CACHE_TTL", "300"))
CACHE_BG_REFRESH_AFTER = int(os.environ.get("LEV_SKILLS_BG_REFRESH_AFTER", "60"))
DISCOVERY_CACHE_VERSION = 5
RESULT_CACHE_ENVELOPE_VERSION = 2
QMD_QUERY_COLLECTIONS = ("skills-db", "skills-db-bundle-docs")
QMD_REFRESH_COLLECTIONS = (
    "skills-db",
    "skills-db-bundle-docs",
    "skills-db-archive",
    "skills-db-backlog",
    "skills-db-workshop",
)
QMD_CANDIDATE_LIMIT = 50
QMD_MAX_QUERY_BYTES = 8192
QMD_QUERY_TIMEOUT_SECONDS = 45.0
QMD_TOTAL_QUERY_TIMEOUT_SECONDS = 180.0
QMD_REFRESH_TIMEOUT_SECONDS = 1200.0
QMD_MAX_OUTPUT_BYTES = 16 * 1024 * 1024
QMD_MAX_MANIFEST_BYTES = 2 * 1024 * 1024
QMD_INTEGRITY_TIMEOUT_SECONDS = 90.0
# Match Python's default conversion ceiling and stay bounded if that guard is disabled.
MAX_CLI_INTEGER_DIGITS = 4300
SOURCE_SNAPSHOT_VERSION = 2
SKILLS_STATE_FILE = ROOT / "skills-state.json"
SKILLS_INVENTORY_FILE = ROOT / "skills-inventory.jsonl"
SKILLS_INVENTORY_SNAPSHOT_FILE = ROOT / "skills-inventory.snapshot.json"
TAXONOMY_CONFIG_FILE = ROOT / "skills-taxonomy.json"
SKILL_GRAPH_FILE = ROOT / "skill-graph.json"
LEV_ROOT = Path(os.environ.get("LEV_ROOT", Path.home() / "lev")).expanduser().resolve()
SKILL_GRAPH_DIR = Path(
    os.environ.get("LEV_SKILL_GRAPH_DIR", LEV_ROOT / "workshop" / "pocs" / "skill-graph")
).expanduser().resolve()
CURRENT_INVENTORY_REVISION = ""

COMMAND_HOOKED = {
    "lev-intake": "intake",
    "cdo": "cdo",
    "ux": "ux",
    "interview": "interview",
    "work": "handoff",
}

ACTIVE_KEEP_FOLDERS = {
    "find-skills",
    "interview",
    "lev",
    "lev-align",
    "lev-builder",
    "cdo",
    "lev-design",
    "lev-design-os",
    "lev-find",
    "lev-find-llm-tldr",
    "lev-find-qmd",
    "lev-index",
    "lev-intake",
    "lev-learn",
    "lev-orch-sidequest",
    "lev-plan",
    "lev-research",
    "lev-sdlc",
    "lev-social",
    "lev-workshop",
    "skill-discovery",
    "ux",
    "visual-explainer",
    "work",
    "workflow",
}

ALLOWED_FOLDER_NAME_DRIFT = {
    "lev-design-os",
    "lev-find-llm-tldr",
    "lev-find-qmd",
    "lev-orch-sidequest",
    "lev-research",
}

REQUIRED_CDO_SUBSKILLS = {"engine", "dispatch", "domains", "modes"}

REQUIRED_WORKFLOW_FLOWS = {
    "cited-research",
    "quality-audit",
    "reverse-engineer-specs",
    "rust-plan",
    "tt-adapter-add",
    "tt-health",
    "tt-release",
    "tt-research",
    "tt-strategy-create",
}

HARD_HIDDEN_CATEGORIES = {".archive", "_todo", "_workshop"}
STOPWORDS = {
    "a",
    "an",
    "and",
    "app",
    "for",
    "from",
    "help",
    "i",
    "in",
    "into",
    "my",
    "need",
    "of",
    "on",
    "or",
    "the",
    "this",
    "to",
    "use",
    "with",
}
LIFECYCLE_ORDER = {
    "core": 0,
    "active": 1,
    "workflow": 2,
    "nested": 3,
    "rotation": 4,
    "experimental": 5,
    "catalog": 6,
    "incubating": 7,
    "backlog": 8,
    "archived": 9,
}
HOME_PREFIX = re.escape(str(Path.home()))
ACTIVE_SKILL_PATH_RE = re.compile(rf"(?:{HOME_PREFIX}|~)/\.agents/skills/((?:[^\s/]+/)*[^\s/]+)/SKILL\.md")
CATALOG_SKILL_PATH_RE = re.compile(rf"(?:{HOME_PREFIX}|~)/\.agents/skills-db/((?:[^\s/]+/)*[^\s/]+)/SKILL\.md")
REPO_SKILL_PATH_RE = re.compile(rf"(?:{HOME_PREFIX}|~)/\.agents/_repos/((?:[^\s/]+/)*[^\s/]+)/SKILL\.md")
LOADED_SKILL_RE = re.compile(r"Loaded `([^`]+)`")
SKILL_URI_RE = re.compile(r"skill://([A-Za-z0-9_.:/-]+)")


def usage() -> int:
    print(
        "\n".join(
            [
                "lev-skills - skills runtime helper",
                "",
                "USAGE",
                '  lev-skills "query" [--json] [--category=...] [--limit=N] [--no-cache]',
                '  lev-skills discover --query TEXT [--query TEXT ...] [--tags CSV] [--namespace skills-db|skills|_repos] [--backend lexical|qmd]',
                '  lev-skills discover|find "query" [--backend lexical|qmd] [--json] [--category=...] [--limit=N] [--no-cache]',
                '  lev-skills pick "query" [--json] [--category=...] [--namespace skills-db|skills|_repos] [--rotation=eligible,experimental] [--no-cache]',
                "  lev-skills tree [--view subjects|collections] [--depth N] [--json]",
                "  lev-skills browse --node NODE_ID [--limit N] [--json]",
                "  lev-skills browse --cursor TOKEN [--json]",
                "  lev-skills get SOURCE_ID_OR_NAME [--json]",
                "  lev-skills inventory [--json] [--include-hidden] [--rebuild]",
                "  lev-skills list",
                "  lev-skills validate",
                "  lev-skills refresh [--repo-local]",
                "  lev-skills graph stats|rebuild|verify|resolve <skill://uri> [--json] [--expand]",
                "  lev-skills help",
                "",
                "NOTES",
                "  discover uses the local filesystem inventory as the canonical source of truth",
                f"  graph metadata is read from {SKILL_GRAPH_FILE} when present",
                f"  graph rebuild uses {SKILL_GRAPH_DIR}",
                f"  inventory --rebuild writes a source-bound manifest to {SKILLS_INVENTORY_FILE}",
                "  catalog skills are read from skills-db/<category>/ and _repos/<category>/<repo>/",
                "  hidden catalog buckets (.archive, _todo, _workshop) are excluded from normal ranking",
                "  lexical discovery is the default; QMD discovery searches only approved skills-db collections",
                "",
                "OPTIONS",
                "  --category=NAME   Scope discovery to a specific domain/category",
                "  --namespace=NAME  Scope lexical discovery to skills-db, skills, or _repos; QMD supports skills-db only",
                "  --backend=NAME    Select lexical (default) or QMD retrieval for discover/find",
                "  --all             Accepted for compatibility; all visible inventory is already searched by default",
                "  --primary-only    Accepted for compatibility; currently equivalent to default inventory search",
                "  --rotation=MODE   pick filter: eligible, experimental, pinned, or all",
                "  --include-hidden  Include hidden catalog buckets in inventory output",
                "  --no-cache        Bypass discover/inventory cache",
                "  --rebuild         Force an inventory rebuild",
                "  --repo-local      Refresh qmd for current repo only (pre-commit friendly)",
            ]
        )
    )
    return 0


def cache_key(
    query: str,
    category: str | None,
    all_collections: bool,
    mode: str = "discover",
    limit: int | None = None,
    revision: str = "",
    namespace: str | None = None,
) -> str:
    parts = [
        f"v{DISCOVERY_CACHE_VERSION}",
        mode,
        query.lower().strip(),
        category or "",
        str(all_collections),
        str(limit) if limit is not None else "",
        namespace or "",
        revision,
    ]
    digest = hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]
    return f"{mode}-v{DISCOVERY_CACHE_VERSION}-{digest}.json"


def discover_cache_request(
    query: str,
    category: str | None,
    all_collections: bool,
    limit: int,
    revision: str,
    namespace: str | None = None,
) -> dict:
    return {
        "mode": "discover",
        "matcher_version": 1,
        "request_schema_version": 1,
        "query": query,
        "category": category,
        "all_collections": all_collections,
        "namespace": namespace,
        "limit": limit,
        "revision": revision,
        "schema_version": 2,
    }


def cached_match_is_valid(match: object) -> bool:
    if not isinstance(match, dict):
        return False
    string_fields = (
        "path",
        "path_key",
        "skill_name",
        "category",
        "surface",
        "lifecycle",
        "rotation_role",
        "usage_tier",
        "skill_uri",
        "lane",
        "graph_id",
        "local_path",
        "doc_type",
        "source",
        "anomaly",
        "source_id",
        "realpath",
        "digest",
        "content_revision",
        "index_revision",
        "source_namespace",
        "source_collection",
        "bundle_id",
        "bundle_revision",
        "bundle_scope",
        "bundle_boundary_status",
    )
    if any(not isinstance(match.get(field), str) for field in string_fields):
        return False
    if not match["path"] or match["path"] != match["local_path"]:
        return False
    if match["realpath"] != match["path"] or not re.fullmatch(r"[a-f0-9]{64}", match["digest"]):
        return False
    if match["content_revision"] != match["digest"]:
        return False
    if not isinstance(match.get("diagnostics"), list) or any(
        not isinstance(item, str) for item in match["diagnostics"]
    ):
        return False
    if not isinstance(match.get("relationships"), list) or not isinstance(
        match.get("relationship_uncertainty"), list
    ):
        return False
    if not isinstance(match.get("source_record"), dict) or not isinstance(match.get("source_scope"), dict):
        return False
    if (
        match["source_record"].get("real_path") != match["realpath"]
        or match["source_scope"].get("namespace") != match["source_namespace"]
        or match["source_scope"].get("collection") != match["source_collection"]
    ):
        return False
    bundle = match.get("bundle")
    if (
        not isinstance(bundle, dict)
        or bundle.get("bundle_id") != match["bundle_id"]
        or bundle.get("revision") != match["bundle_revision"]
        or not isinstance(bundle.get("members"), list)
    ):
        return False
    for member in bundle["members"]:
        if (
            not isinstance(member, dict)
            or not isinstance(member.get("source_id"), str)
            or not isinstance(member.get("path"), str)
            or member.get("path") != member.get("local_path")
            or not isinstance(member.get("realpath"), str)
            or not isinstance(member.get("digest"), str)
            or not re.fullmatch(r"[a-f0-9]{64}", member["digest"])
            or member.get("content_revision") != member.get("digest")
            or member.get("index_revision") != match["index_revision"]
        ):
            return False
    if (
        not isinstance(match.get("matched_groups"), list)
        or any(not isinstance(item, str) for item in match["matched_groups"])
        or not isinstance(match.get("group_scores"), dict)
        or set(match["group_scores"]) != set(match["matched_groups"])
        or not isinstance(match.get("group_matches"), dict)
        or set(match["group_matches"]) != set(match["matched_groups"])
    ):
        return False
    for group_id, group_match in match["group_matches"].items():
        score = group_match.get("score") if isinstance(group_match, dict) else None
        try:
            finite_score = math.isfinite(float(score))
        except (OverflowError, TypeError, ValueError):
            finite_score = False
        if (
            not isinstance(group_match, dict)
            or not isinstance(score, (int, float))
            or isinstance(score, bool)
            or not finite_score
            or not isinstance(group_match.get("matched_terms"), list)
            or any(not isinstance(term, str) for term in group_match["matched_terms"])
            or match["group_scores"].get(group_id) != score
        ):
            return False
    if match["doc_type"] not in {"skill", "markdown"} or match["source"] != "inventory":
        return False
    for field in ("score", "adjusted_score"):
        value = match.get(field)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return False
        try:
            if not math.isfinite(float(value)):
                return False
        except (OverflowError, ValueError):
            return False
    usage_count = match.get("usage_count")
    graph_degree = match.get("graph_degree")
    if (
        not isinstance(usage_count, int)
        or isinstance(usage_count, bool)
        or usage_count < 0
        or not isinstance(graph_degree, int)
        or isinstance(graph_degree, bool)
        or graph_degree < 0
    ):
        return False
    for field in ("intent_tags", "matched_terms"):
        value = match.get(field)
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            return False
    return True


def cached_payload_is_valid(payload: object, request: dict) -> bool:
    if not isinstance(payload, dict) or "_cache" in payload:
        return False
    expected_category = [request["category"]] if request["category"] else []
    expected_query = {
        "raw": request["query"],
        "normalized_phrase": normalize_name(request["query"]),
        "ordered_tokens": tokenize(request["query"]),
    }
    expected_normalized_request = {
        "mode": "discover",
        "matcher_version": 1,
        "request_schema_version": 1,
        "queries": [expected_query],
        "tags_raw": None,
        "normalized_tags": [],
        "category": normalize_name(request["category"]) if request["category"] else None,
        "namespace": request.get("namespace"),
        "visibility": "legacy_discovery_visible",
        "roles": None,
        "revision": request["revision"],
        "limit": request["limit"],
        "order": "score_desc_name_asc_path_key_asc",
        "all_collections": request["all_collections"],
    }
    if (
        payload.get("schema_version") != "lev.skills.discover.v1"
        or payload.get("status") not in {"ok", "empty"}
        or payload.get("evaluation_origin") != "cli_evaluation"
        or payload.get("query") != request["query"]
        or payload.get("category_filter") != expected_category
        or payload.get("source_of_truth") != str(SKILLS_INVENTORY_FILE)
        or payload.get("index_revision") != request["revision"]
        or payload.get("normalized_request") != expected_normalized_request
    ):
        return False
    matches = payload.get("matches")
    if (
        not isinstance(matches, list)
        or len(matches) > request["limit"]
        or any(not cached_match_is_valid(match) for match in matches)
        or any(match.get("index_revision") != request["revision"] for match in matches)
    ):
        return False
    if payload.get("returned_count") != len(matches) or payload.get("limit") != request["limit"]:
        return False
    total = payload.get("total")
    if not isinstance(total, int) or isinstance(total, bool) or total < len(matches):
        return False
    if payload.get("status") != ("ok" if total else "empty") or payload.get("next_cursor") is not None:
        return False
    groups = payload.get("query_groups")
    if not isinstance(groups, list) or len(groups) != 1:
        return False
    group = groups[0]
    group_total = group.get("total") if isinstance(group, dict) else None
    if (
        not isinstance(group_total, int)
        or isinstance(group_total, bool)
        or group_total < 0
    ):
        return False
    if (
        not isinstance(group, dict)
        or group.get("id") != "group-1"
        or group.get("kind") != "query"
        or group.get("raw") != request["query"]
        or group.get("normalized") != expected_query["normalized_phrase"]
        or group.get("tokens") != expected_query["ordered_tokens"]
        or group.get("status") != ("ok" if group_total else "empty")
        or group.get("duplicate_of") is not None
        or group.get("evaluated") is not True
        or group.get("evaluation_origin") != "cli_evaluation"
        or not isinstance(group.get("predicate_fingerprint"), str)
        or not re.fullmatch(r"[a-f0-9]{64}", group["predicate_fingerprint"])
        or not isinstance(group.get("request_fingerprint"), str)
        or not re.fullmatch(r"[a-f0-9]{64}", group["request_fingerprint"])
    ):
        return False
    if total != group_total:
        return False
    if any(not set(match["matched_groups"]).issubset({group["id"]}) for match in matches):
        return False
    return True


def get_cached_result(key: str, request: dict) -> dict | None:
    cache_file = CACHE_DIR / key
    if not cache_file.exists():
        return None
    try:
        stat = cache_file.stat()
        age = time.time() - stat.st_mtime
        if age > CACHE_TTL_SECONDS:
            return None
        with cache_file.open() as handle:
            document = json.load(handle)
        if not isinstance(document, dict):
            return None
        integrity = document.get("integrity_sha256")
        body = {field: value for field, value in document.items() if field != "integrity_sha256"}
        try:
            if integrity != digest_json(body):
                return None
        except (RecursionError, TypeError, ValueError):
            return None
        if body.get("cache_version") != RESULT_CACHE_ENVELOPE_VERSION:
            return None
        if body.get("request") != request:
            return None
        result = body.get("result")
        if not cached_payload_is_valid(result, request):
            return None
        payload = dict(result)
        payload["_cache"] = {"hit": True, "age_seconds": int(age)}
        return payload
    except (OSError, RecursionError, UnicodeDecodeError, json.JSONDecodeError):
        return None


def cached_discovery_result_is_current(
    cached: dict,
    request: dict,
    *,
    rows: list[dict],
    revision: str,
    rows_by_id: dict[str, dict],
    bundles: dict[str, dict],
) -> bool:
    """Validate cached contributions and hydrate their source facts without rescoring the corpus."""
    result = {field: value for field, value in cached.items() if field != "_cache"}
    expected_result_fields = {
        "schema_version",
        "status",
        "evaluation_origin",
        "query",
        "category_filter",
        "source_of_truth",
        "index_revision",
        "normalized_request",
        "breadcrumbs",
        "total",
        "returned_count",
        "limit",
        "next_cursor",
        "diagnostics",
        "next_actions",
        "query_groups",
        "matches",
    }
    if set(result) != expected_result_fields or result.get("index_revision") != revision:
        return False

    groups = request.get("groups")
    outcomes = result.get("query_groups")
    if not isinstance(groups, list) or len(groups) != 1 or not isinstance(outcomes, list) or len(outcomes) != 1:
        return False
    group = groups[0]
    outcome = outcomes[0]
    if not isinstance(group, dict) or not isinstance(outcome, dict):
        return False
    expected_predicate = _predicate_fingerprint(
        group,
        category=request["category"],
        namespace=request["namespace"],
        visibility="legacy_discovery_visible",
        roles=None,
        revision=revision,
    )
    expected_ranking_request = _ranking_request_fingerprint(
        group,
        category=request["category"],
        namespace=request["namespace"],
        visibility="legacy_discovery_visible",
        roles=None,
        revision=revision,
        limit=request["limit"],
    )
    if (
        outcome.get("predicate_fingerprint") != expected_predicate
        or outcome.get("request_fingerprint") != expected_ranking_request
        or outcome.get("evaluated") is not True
        or outcome.get("evaluation_origin") != "cli_evaluation"
    ):
        return False

    eligible_rows = filtered_inventory(
        rows,
        category=request["category"],
        namespace=request["namespace"],
        include_hidden=False,
        rotation_roles=None,
    )
    eligible_by_id = {
        row["source_id"]: row
        for row in eligible_rows
        if isinstance(row.get("source_id"), str)
        and row.get("doc_type", "skill") in {"skill", "markdown"}
    }
    query_terms = set(group.get("tokens", []))
    seen_ids: set[str] = set()
    matches = result.get("matches")
    if not isinstance(matches, list):
        return False

    for match in matches:
        if not isinstance(match, dict):
            return False
        source_id = match.get("source_id")
        if not isinstance(source_id, str) or source_id in seen_ids:
            return False
        row = eligible_by_id.get(source_id)
        if row is None:
            return False
        seen_ids.add(source_id)

        expected_base = {
            "source_id": row["source_id"],
            "path": row["path"],
            "path_key": row["path_key"],
            "skill_name": row["name"],
            "category": row["category"],
            "surface": row["surface"],
            "lifecycle": row["lifecycle"],
            "rotation_role": row["rotation_role"],
            "usage_count": row["usage_count"],
            "usage_tier": row["usage_tier"],
            "skill_uri": row["skill_uri"],
            "lane": row["lane"],
            "graph_id": row["graph_id"],
            "graph_degree": row["graph_degree"],
            "intent_tags": row["intent_tags"],
            "local_path": row["path"],
            "doc_type": row.get("doc_type", "skill"),
            "source": "inventory",
            "anomaly": row.get("anomaly", ""),
        }
        try:
            expected_descriptor = _source_descriptor(
                row, revision=revision, rows_by_id=rows_by_id, bundles=bundles
            )
        except (RuntimeError, KeyError, TypeError, ValueError):
            return False
        expected_source_fields = {**expected_base, **expected_descriptor}
        ranking_fields = {
            "score",
            "adjusted_score",
            "matched_terms",
            "matched_groups",
            "group_scores",
            "group_matches",
        }
        if set(match) != set(expected_source_fields) | ranking_fields:
            return False
        if any(match.get(key) != value for key, value in expected_source_fields.items()):
            return False

        matched_terms = match.get("matched_terms")
        score = match.get("score")
        if (
            not isinstance(matched_terms, list)
            or not matched_terms
            or matched_terms != sorted(set(matched_terms))
            or not set(matched_terms).issubset(query_terms)
            or score != match.get("adjusted_score")
            or not isinstance(score, (int, float))
            or isinstance(score, bool)
            or score <= 0
            or match.get("matched_groups") != [group["id"]]
            or match.get("group_scores") != {group["id"]: score}
            or match.get("group_matches")
            != {group["id"]: {"score": score, "matched_terms": matched_terms}}
        ):
            return False

    ordered = sorted(
        matches,
        key=lambda item: (-item["adjusted_score"], item["skill_name"].lower(), item["path_key"]),
    )
    return matches == ordered


def set_cached_result(key: str, data: dict, request: dict) -> None:
    if not cached_payload_is_valid(data, request):
        return
    document = {
        "cache_version": RESULT_CACHE_ENVELOPE_VERSION,
        "request": request,
        "result": data,
    }
    document["integrity_sha256"] = digest_json(document)
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = CACHE_DIR / key
        with cache_file.open("w") as handle:
            json.dump(document, handle, ensure_ascii=False, sort_keys=True, allow_nan=False)
    except (OSError, TypeError, ValueError):
        return


class QmdBackendError(RuntimeError):
    pass


def run_bounded_process(
    cmd: list[str],
    *,
    timeout: float,
    max_output_bytes: int = QMD_MAX_OUTPUT_BYTES,
    max_input_bytes: int = QMD_MAX_MANIFEST_BYTES,
    cwd: Path | None = None,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run one child with a wall-clock limit, process-group cleanup, and bounded output."""
    input_bytes = input_text.encode("utf-8") if input_text is not None else b""
    if len(input_bytes) > max_input_bytes:
        raise QmdBackendError(f"QMD process input exceeded {max_input_bytes} bytes")
    process = subprocess.Popen(
        cmd,
        cwd=str(cwd or ROOT),
        stdin=subprocess.PIPE if input_text is not None else subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,
        start_new_session=(os.name == "posix"),
    )
    selector = selectors.DefaultSelector()
    output = {"stdout": bytearray(), "stderr": bytearray()}
    pipes = {
        process.stdout: "stdout",
        process.stderr: "stderr",
    }
    if process.stdin is not None:
        pipes[process.stdin] = "stdin"
        os.set_blocking(process.stdin.fileno(), False)
    for pipe, name in pipes.items():
        if pipe is None:
            continue
        if name != "stdin":
            os.set_blocking(pipe.fileno(), False)
            selector.register(pipe, selectors.EVENT_READ, name)
    input_offset = 0
    if process.stdin is not None:
        selector.register(process.stdin, selectors.EVENT_WRITE, "stdin")
    deadline = time.monotonic() + timeout
    total_output = 0
    failure = None

    try:
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                failure = "timed out"
                break
            events = selector.select(min(remaining, 0.25))
            if not events and process.poll() is not None:
                for key in list(selector.get_map().values()):
                    if key.data == "stdin":
                        selector.unregister(key.fileobj)
                        key.fileobj.close()
                continue
            for key, _ in events:
                name = key.data
                pipe = key.fileobj
                if name == "stdin":
                    if input_offset >= len(input_bytes):
                        selector.unregister(pipe)
                        pipe.close()
                        continue
                    try:
                        input_offset += os.write(pipe.fileno(), input_bytes[input_offset : input_offset + 65536])
                    except BrokenPipeError:
                        selector.unregister(pipe)
                        pipe.close()
                    continue
                chunk = os.read(pipe.fileno(), 65536)
                if not chunk:
                    selector.unregister(pipe)
                    pipe.close()
                    continue
                total_output += len(chunk)
                if total_output > max_output_bytes:
                    failure = f"output exceeded {max_output_bytes} bytes"
                    break
                output[name].extend(chunk)
            if failure:
                break
    except BaseException:
        _cleanup_bounded_process(process)
        raise
    finally:
        selector.close()

    if failure:
        _cleanup_bounded_process(process)
        raise QmdBackendError(f"QMD process {failure}")

    try:
        process.wait(timeout=max(0.0, deadline - time.monotonic()))
    except subprocess.TimeoutExpired as error:
        _cleanup_bounded_process(process)
        raise QmdBackendError("QMD process timed out") from error
    if os.name == "posix":
        try:
            os.killpg(process.pid, 0)
        except ProcessLookupError:
            pass
        else:
            _terminate_process_group(process)
    return subprocess.CompletedProcess(
        cmd,
        process.returncode,
        output["stdout"].decode("utf-8", errors="replace"),
        output["stderr"].decode("utf-8", errors="replace"),
    )


def _cleanup_bounded_process(process: subprocess.Popen) -> None:
    """Stop the owned process group even when its leader already exited."""
    _terminate_process_group(process)
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        try:
            process.kill()
        except OSError:
            pass
        process.wait()
    if process.stdin is not None and not process.stdin.closed:
        process.stdin.close()
    for pipe in (process.stdout, process.stderr):
        if pipe is not None and not pipe.closed:
            pipe.close()


def _terminate_process_group(process: subprocess.Popen) -> None:
    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
    except (ProcessLookupError, PermissionError, OSError):
        try:
            process.kill()
        except OSError:
            pass


def run_command(cmd: list[str], *, timeout: float = 15.0) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)


def normalize_name(name: str) -> str:
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", (name or "").strip())
    text = text.replace("_", "-")
    text = re.sub(r"[^A-Za-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-").lower()


def tokenize(text: str) -> list[str]:
    normalized = normalize_name(text).replace("-", " ")
    tokens = [token for token in normalized.split() if token and token not in STOPWORDS]
    return tokens


def coerce_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, dict):
        return [str(key).strip() for key in value.keys() if str(key).strip()]
    text = str(value).strip()
    if not text:
        return []
    if "," in text:
        return [piece.strip() for piece in text.split(",") if piece.strip()]
    return [text]


def json_compatible(value) -> bool:
    pending: list[tuple[str, object]] = [("visit", value)]
    active: set[int] = set()
    completed: set[int] = set()
    while pending:
        action, item = pending.pop()
        if action == "leave":
            active.discard(id(item))
            completed.add(id(item))
            continue
        if item is None or isinstance(item, (str, bool, int)):
            continue
        if isinstance(item, float):
            if not math.isfinite(item):
                return False
            continue
        if not isinstance(item, (list, dict)):
            return False
        identity = id(item)
        if identity in active:
            return False
        if identity in completed:
            continue
        active.add(identity)
        pending.append(("leave", item))
        if isinstance(item, list):
            pending.extend(("visit", child) for child in item)
        else:
            if any(not isinstance(key, str) for key in item):
                return False
            pending.extend(("visit", child) for child in item.values())
    return True


def split_frontmatter(data: bytes) -> tuple[str, bytes | None, bytes]:
    lines = data.splitlines(keepends=True)
    if not lines or lines[0].rstrip(b"\r\n").strip() != b"---":
        return "absent", None, data
    for index, line in enumerate(lines[1:], start=1):
        if line.rstrip(b"\r\n").strip() == b"---":
            return "present", b"".join(lines[1:index]), b"".join(lines[index + 1 :])
    return "unterminated", b"".join(lines[1:]), b""


def parse_source_metadata(data: bytes, *, markdown: bool = True) -> tuple[dict, bytes, str, list[str]]:
    if not markdown:
        return (
            {
                "status": "not_applicable",
                "value": None,
                "raw_yaml": None,
                "raw_header_base64": None,
                "error": None,
            },
            b"",
            "not_checked_non_markdown",
            [],
        )

    header_status, raw_header, body = split_frontmatter(data)
    diagnostics: list[str] = []
    encoding_status = "utf8"
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as error:
        encoding_status = "invalid_utf8_body" if header_status == "present" else "invalid_utf8"
        diagnostics.append(f"source is not valid UTF-8 at byte {error.start}")

    raw_header_base64 = base64.b64encode(raw_header).decode("ascii") if raw_header is not None else None
    if header_status == "absent":
        return (
            {
                "status": "absent",
                "value": None,
                "raw_yaml": None,
                "raw_header_base64": None,
                "error": None,
            },
            body,
            encoding_status,
            diagnostics,
        )

    if header_status == "unterminated":
        try:
            raw_yaml = raw_header.decode("utf-8") if raw_header is not None else None
        except UnicodeDecodeError:
            raw_yaml = None
            encoding_status = "invalid_utf8_header"
        error = "frontmatter opening delimiter has no closing delimiter"
        diagnostics.append(error)
        return (
            {
                "status": "unterminated_frontmatter",
                "value": None,
                "raw_yaml": raw_yaml,
                "raw_header_base64": raw_header_base64,
                "error": error,
            },
            body,
            encoding_status,
            diagnostics,
        )

    try:
        raw_yaml = raw_header.decode("utf-8") if raw_header is not None else ""
    except UnicodeDecodeError as error:
        message = f"frontmatter is not valid UTF-8 at byte {error.start}"
        diagnostics.append(message)
        return (
            {
                "status": "invalid_utf8",
                "value": None,
                "raw_yaml": None,
                "raw_header_base64": raw_header_base64,
                "error": message,
            },
            body,
            "invalid_utf8_header",
            diagnostics,
        )

    if yaml is None:
        message = "complete YAML parser unavailable; metadata was not parsed"
        diagnostics.append(message)
        return (
            {
                "status": "parser_unavailable",
                "value": None,
                "raw_yaml": raw_yaml,
                "raw_header_base64": raw_header_base64,
                "error": message,
            },
            body,
            encoding_status,
            diagnostics,
        )

    try:
        loaded = yaml.safe_load(raw_yaml)
    except Exception as error:
        message = f"YAML parse failed: {error}"
        diagnostics.append(message)
        return (
            {
                "status": "malformed_yaml",
                "value": None,
                "raw_yaml": raw_yaml,
                "raw_header_base64": raw_header_base64,
                "error": message,
            },
            body,
            encoding_status,
            diagnostics,
        )

    if loaded is None:
        if raw_yaml.strip():
            message = "frontmatter must be a mapping, not YAML null"
            diagnostics.append(message)
            return (
                {
                    "status": "unsupported_type",
                    "value": None,
                    "raw_yaml": raw_yaml,
                    "raw_header_base64": raw_header_base64,
                    "error": message,
                },
                body,
                encoding_status,
                diagnostics,
            )
        loaded = {}
    if not isinstance(loaded, dict) or not json_compatible(loaded):
        message = "parsed YAML contains a non-JSON-compatible value or top-level type"
        diagnostics.append(message)
        return (
            {
                "status": "unsupported_type",
                "value": None,
                "raw_yaml": raw_yaml,
                "raw_header_base64": raw_header_base64,
                "error": message,
            },
            body,
            encoding_status,
            diagnostics,
        )

    return (
        {
            "status": "parsed",
            "value": loaded,
            "raw_yaml": raw_yaml,
            "raw_header_base64": raw_header_base64,
            "error": None,
        },
        body,
        encoding_status,
        diagnostics,
    )


def extract_frontmatter(path: Path) -> dict:
    try:
        data = path.read_bytes()
    except OSError:
        return {}
    metadata, _, _, _ = parse_source_metadata(data, markdown=path.suffix.lower() == ".md")
    value = metadata.get("value")
    return value if isinstance(value, dict) else {}


def metadata_list(value, field_name: str, diagnostics: list[str]) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [piece.strip() for piece in value.split(",") if piece.strip()]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return [item.strip() for item in value if item.strip()]
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        return [key.strip() for key in value if key.strip()]
    diagnostics.append(f"metadata field {field_name} must be a string or string collection")
    return []


def markdown_summary(body: bytes) -> tuple[str, list[str], str | None]:
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        return "", [], "Markdown body is not valid UTF-8; content tokens were not produced"
    tokens = sorted(set(tokenize(text)))
    lines = []
    for line in text.splitlines():
        candidate = line.strip()
        if not candidate or candidate.startswith(("#", chr(96) * 3, "~~~")):
            continue
        lines.append(candidate)
        if len(" ".join(lines)) >= 400:
            break
    return " ".join(lines)[:400], tokens, None


def parse_meta_data(path: Path, data: bytes) -> dict:
    original_metadata, body, encoding_status, diagnostics = parse_source_metadata(
        data, markdown=path.suffix.lower() == ".md"
    )
    metadata = original_metadata.get("value")
    metadata = metadata if isinstance(metadata, dict) else {}
    name_value = metadata.get("name")
    fallback_name = path.parent.name if path.name.casefold() == "skill.md" else path.stem
    if name_value is None:
        name = fallback_name
    elif isinstance(name_value, str) and name_value.strip():
        name = name_value.strip()
    else:
        diagnostics.append("metadata field name must be a non-empty string")
        name = fallback_name

    description_value = metadata.get("description")
    description = description_value.strip() if isinstance(description_value, str) else ""
    if description_value is not None and not isinstance(description_value, str):
        diagnostics.append("metadata field description must be a string")
    body_summary, content_tokens, body_error = markdown_summary(body)
    if body_error:
        diagnostics.append(body_error)
    if not description and (
        path.name.casefold() != "skill.md" or original_metadata.get("status") == "absent"
    ):
        description = body_summary

    nested_metadata = metadata.get("metadata", {})
    if nested_metadata is None:
        nested_metadata = {}
    if not isinstance(nested_metadata, dict):
        diagnostics.append("metadata field metadata must be a mapping")
        nested_metadata = {}
    tags = metadata_list(metadata.get("tags"), "tags", diagnostics)
    tags += metadata_list(nested_metadata.get("tags"), "metadata.tags", diagnostics)
    triggers = metadata_list(metadata.get("triggers"), "triggers", diagnostics)
    triggers += metadata_list(metadata.get("legacy_aliases"), "legacy_aliases", diagnostics)
    aliases = metadata_list(metadata.get("aliases"), "aliases", diagnostics)
    aliases += metadata_list(metadata.get("related_skills"), "related_skills", diagnostics)
    return {
        "name": name,
        "description": description,
        "tags": sorted(set(tags)),
        "triggers": sorted(set(triggers)),
        "aliases": sorted(set(aliases)),
        "raw": metadata,
        "original_metadata": original_metadata,
        "content_tokens": content_tokens,
        "encoding_status": encoding_status,
        "diagnostics": diagnostics,
    }


def parse_meta(path: Path) -> dict:
    try:
        data = path.read_bytes()
    except OSError as error:
        message = f"source read failed: {error}"
        return {
            "name": path.parent.name if path.name.casefold() == "skill.md" else path.stem,
            "description": "",
            "tags": [],
            "triggers": [],
            "aliases": [],
            "raw": {},
            "original_metadata": {
                "status": "unreadable",
                "value": None,
                "raw_yaml": None,
                "raw_header_base64": None,
                "error": message,
            },
            "diagnostics": [message],
        }
    return parse_meta_data(path, data)


def active_skill_rows() -> list[dict]:
    rows = []
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        folder = skill_md.parent.name
        if folder == ".system":
            continue
        meta = parse_meta(skill_md)
        rows.append(
            {
                "folder": folder,
                "name": meta["name"],
                "description": meta["description"],
                "path": str(skill_md),
                "core": folder in ACTIVE_KEEP_FOLDERS,
            }
        )
    return rows


def cdo_subskill_rows() -> list[dict]:
    rows = []
    if not CDO_DIR.exists():
        return rows
    for skill_md in sorted(CDO_DIR.glob("*/SKILL.md")):
        meta = parse_meta(skill_md)
        rows.append(
            {
                "folder": skill_md.parent.name,
                "name": meta["name"],
                "description": meta["description"],
                "path": str(skill_md),
            }
        )
    return rows


def workflow_flow_rows() -> list[dict]:
    rows = []
    if not WORKFLOW_FLOWS_DIR.exists():
        return rows
    for skill_md in sorted(WORKFLOW_FLOWS_DIR.glob("*/SKILL.md")):
        meta = parse_meta(skill_md)
        rows.append(
            {
                "folder": skill_md.parent.name,
                "name": meta["name"],
                "description": meta["description"],
                "path": str(skill_md),
            }
        )
    return rows


def walk_source_files(root: Path):
    if not root.exists():
        return
    if not root.is_dir():
        raise RuntimeError(f"source root is not a directory: {root}")
    approved_corpus = root.resolve() == SKILLS_DB_DIR.resolve()

    def onerror(error):
        raise RuntimeError(f"cannot enumerate source root {root}: {error}") from error

    for directory, child_dirs, filenames in os.walk(root, onerror=onerror, followlinks=False):
        directory_path = Path(directory)
        kept_dirs = []
        for child in sorted(child_dirs):
            if child in {".git", ".DS_Store"}:
                continue
            child_path = directory_path / child
            if child_path.is_symlink():
                if approved_corpus:
                    raise RuntimeError(f"source directory symlink is not admitted: {child_path}")
                continue
            kept_dirs.append(child)
        child_dirs[:] = kept_dirs
        for filename in sorted(filenames):
            if filename in {".git", ".DS_Store"}:
                continue
            path = directory_path / filename
            if path.is_symlink() and not approved_corpus:
                continue
            if path.is_symlink():
                try:
                    real_path = path.resolve(strict=True)
                except OSError as error:
                    raise RuntimeError(f"source symlink is unreadable: {path}: {error}") from error
                if not real_path.is_relative_to(root.resolve()):
                    raise RuntimeError(f"source symlink escapes its corpus root: {path} -> {real_path}")
            if path.is_file():
                yield path


def source_file_specs() -> list[tuple[str, Path, Path, tuple[str, ...]]]:
    specs: list[tuple[str, Path, Path, tuple[str, ...]]] = []
    for path in walk_source_files(SKILLS_DB_DIR) or ():
        specs.append(("skills-db", SKILLS_DB_DIR, path, path.relative_to(SKILLS_DB_DIR).parts))
    for path in walk_source_files(SKILLS_DIR) or ():
        relative = path.relative_to(SKILLS_DIR)
        if relative.parts[0] != ".system" and path.name.casefold() == "skill.md":
            specs.append(("skills", SKILLS_DIR, path, relative.parts))
    for path in walk_source_files(SKILL_REPOS_DIR) or ():
        relative = path.relative_to(SKILL_REPOS_DIR)
        if path.name.casefold() == "skill.md" and len(relative.parts) >= 3:
            specs.append(("_repos", SKILL_REPOS_DIR, path, relative.parts))
    specs.sort(key=lambda item: (item[0], "/".join(item[3])))
    return specs


def catalog_skill_files():
    for base_label, root, minimum_parts in (
        ("skills-db", SKILLS_DB_DIR, 2),
        ("_repos", SKILL_REPOS_DIR, 3),
    ):
        for skill_md in walk_source_files(root) or ():
            if skill_md.name.casefold() != "skill.md":
                continue
            rel = skill_md.relative_to(root)
            if len(rel.parts) >= minimum_parts:
                yield base_label, root, skill_md, rel.parts


def catalog_rows(include_hidden: bool = True) -> list[dict]:
    rows = []
    for base_label, _, skill_md, rel_parts in catalog_skill_files():
        category = rel_parts[0]
        if not include_hidden and category in HARD_HIDDEN_CATEGORIES:
            continue
        meta = parse_meta(skill_md)
        rows.append(
            {
                "base": base_label,
                "category": category,
                "source_repo": rel_parts[1] if base_label == "_repos" else None,
                "name": meta["name"],
                "description": meta["description"],
                "path": str(skill_md),
            }
        )
    return rows


def load_skill_graph() -> dict[str, dict]:
    data, _ = read_graph_input()
    return graph_nodes_from_data(data)


def graph_nodes_from_data(data: dict) -> dict[str, dict]:
    raw_nodes = data.get("nodes", {})
    raw_edges = data.get("edges", [])
    if not isinstance(raw_nodes, dict):
        return {}

    degree: Counter[str] = Counter()
    neighbors: defaultdict[str, list[str]] = defaultdict(list)
    if isinstance(raw_edges, list):
        for edge in raw_edges:
            if not isinstance(edge, dict):
                continue
            source = str(edge.get("source") or "").strip()
            target = str(edge.get("target") or "").strip()
            if not source or not target:
                continue
            degree[source] += 1
            degree[target] += 1
            neighbors[source].append(target)
            neighbors[target].append(source)

    graph: dict[str, dict] = {}
    for node_id, node in raw_nodes.items():
        if not isinstance(node, dict) or node.get("kind") != "skill":
            continue
        node_name = str(node.get("name") or node_id)
        enriched = {
            **node,
            "_degree": degree.get(str(node_id), 0),
            "_neighbors": sorted(set(neighbors.get(str(node_id), []))),
        }
        aliases = {
            normalize_name(str(node_id)),
            normalize_name(node_name),
            normalize_name(str(node.get("id") or "")),
        }
        for alias in aliases:
            if alias:
                graph[alias] = enriched
    return graph


def load_skill_graph_payload() -> dict:
    if not SKILL_GRAPH_FILE.exists():
        raise RuntimeError(f"skill graph not found: {SKILL_GRAPH_FILE}")
    data, _ = read_graph_input()
    return data


def graph_entry_for(row: dict, graph_nodes: dict[str, dict]) -> dict | None:
    keys = [
        row.get("slug", ""),
        row.get("name", ""),
        row.get("folder", ""),
        row.get("rel_dir", "").split("/")[-1],
    ]
    for key in keys:
        normalized = normalize_name(str(key))
        if normalized in graph_nodes:
            return graph_nodes[normalized]
    return None


def build_skill_row(base_label: str, skill_md: Path, rel_parts: tuple[str, ...]) -> dict:
    meta = parse_meta(skill_md)
    dir_parts = rel_parts[:-1]
    folder = dir_parts[-1]
    path_key = f"{base_label}/{'/'.join(dir_parts)}"
    category = dir_parts[0] if base_label in {"skills-db", "_repos"} else "skills"
    source_repo = dir_parts[1] if base_label == "_repos" else None
    surface = "active"
    group = None
    if base_label == "skills":
        if dir_parts[0] == "workflow" and len(dir_parts) >= 3 and dir_parts[1] == "flows":
            surface = "workflow"
            group = "workflow/flows"
        elif len(dir_parts) > 1:
            surface = "nested"
            group = "/".join(dir_parts[:-1])
    else:
        if category in HARD_HIDDEN_CATEGORIES:
            surface = "hidden"
        elif base_label == "_repos":
            surface = "catalog-repo"
        elif len(dir_parts) > 2:
            surface = "catalog-nested"
        else:
            surface = "catalog"
        group = category

    own_dir = skill_md.parent
    descendant_skills = [
        child for child in own_dir.rglob("SKILL.md") if child.parent != own_dir
    ]
    parent_skill = None
    if base_label == "skills-db" and len(dir_parts) > 2:
        parent_candidate = SKILLS_DB_DIR.joinpath(*dir_parts[:-1]) / "SKILL.md"
        if parent_candidate.exists():
            parent_skill = str(parent_candidate)

    row = {
        "path": str(skill_md.resolve()),
        "path_key": path_key,
        "base": base_label,
        "surface": surface,
        "group": group,
        "category": category,
        "source_repo": source_repo,
        "folder": folder,
        "name": meta["name"],
        "slug": normalize_name(meta["name"] or folder),
        "description": meta["description"],
        "tags": meta["tags"],
        "triggers": meta["triggers"],
        "aliases": meta["aliases"],
        "rel_dir": "/".join(dir_parts),
        "depth": len(dir_parts),
        "core": base_label == "skills" and len(dir_parts) == 1 and folder in ACTIVE_KEEP_FOLDERS,
        "has_children": bool(descendant_skills),
        "child_skill_count": len(descendant_skills),
        "parent_skill": parent_skill,
    }
    row["path_tokens"] = sorted(set(tokenize(row["rel_dir"])))
    row["name_tokens"] = sorted(set(tokenize(row["name"]) + tokenize(folder)))
    row["description_tokens"] = sorted(set(tokenize(row["description"])))
    row["tag_tokens"] = sorted(set(tokenize(" ".join(row["tags"] + row["triggers"] + row["aliases"]))))
    row["category_tokens"] = sorted(set(tokenize(category)))
    return row


def build_source_row(
    base_label: str,
    root: Path,
    path: Path,
    rel_parts: tuple[str, ...],
    data: bytes,
    descendants: dict[tuple[str, tuple[str, ...]], int],
    entrypoint_paths: dict[tuple[str, tuple[str, ...]], Path],
) -> dict:
    meta = parse_meta_data(path, data)
    entrypoint = path.name.casefold() == "skill.md"
    directory_parts = rel_parts[:-1]
    collection = rel_parts[0] if len(rel_parts) > 1 else base_label
    relative_path = Path(*rel_parts).as_posix()
    occurrence_key = f"{base_label}/{relative_path}"
    legacy_path_key = f"{base_label}/{'/'.join(directory_parts)}" if directory_parts else None
    path_key = legacy_path_key if entrypoint and legacy_path_key else occurrence_key
    if base_label == "skills":
        category = "skills"
    else:
        category = collection
    source_repo = rel_parts[1] if base_label == "_repos" and len(rel_parts) > 1 else None
    folder = path.parent.name
    surface = "document"
    group = category
    if entrypoint:
        if base_label == "skills":
            surface = "active"
            if rel_parts[0] == "workflow" and len(rel_parts) >= 3 and rel_parts[1] == "flows":
                surface = "workflow"
                group = "workflow/flows"
            elif len(directory_parts) > 1:
                surface = "nested"
                group = "/".join(directory_parts[:-1])
        elif category in HARD_HIDDEN_CATEGORIES:
            surface = "hidden"
        elif base_label == "_repos":
            surface = "catalog-repo"
        elif len(directory_parts) > 2:
            surface = "catalog-nested"
        else:
            surface = "catalog"
    elif category in HARD_HIDDEN_CATEGORIES:
        surface = "hidden"
    elif path.suffix.lower() != ".md":
        surface = "asset"

    folder_name = folder if entrypoint else path.stem
    name = meta["name"] or folder_name
    slug = normalize_name(name or folder_name)
    parent_skill = None
    if entrypoint and base_label == "skills-db" and len(directory_parts) > 2:
        for length in range(len(directory_parts) - 1, 0, -1):
            parent_key = (base_label, tuple(directory_parts[:length]))
            if parent_key in entrypoint_paths:
                parent_skill = str(entrypoint_paths[parent_key].resolve())
                break

    original_metadata = meta["original_metadata"]
    encoding_status = meta["encoding_status"]
    content_tokens = (
        meta["content_tokens"]
        if not entrypoint or original_metadata.get("status") == "absent"
        else []
    )
    diagnostics = list(dict.fromkeys(meta["diagnostics"]))
    row = {
        "path": str(path.resolve()),
        "path_key": path_key,
        "occurrence_key": occurrence_key,
        "legacy_path_key": legacy_path_key if entrypoint else None,
        "base": base_label,
        "surface": surface,
        "group": group,
        "category": category,
        "source_repo": source_repo,
        "folder": folder,
        "name": name,
        "slug": slug,
        "description": meta["description"],
        "tags": meta["tags"],
        "triggers": meta["triggers"],
        "aliases": meta["aliases"],
        "rel_dir": "/".join(directory_parts) if entrypoint else relative_path,
        "depth": len(directory_parts) if entrypoint else len(rel_parts),
        "core": base_label == "skills" and len(directory_parts) == 1 and folder_name in ACTIVE_KEEP_FOLDERS,
        "has_children": bool(descendants.get((base_label, tuple(directory_parts)), 0)) if entrypoint else False,
        "child_skill_count": descendants.get((base_label, tuple(directory_parts)), 0) if entrypoint else 0,
        "parent_skill": parent_skill,
        "doc_type": "skill" if entrypoint else ("markdown" if path.suffix.lower() == ".md" else "asset"),
        "source": {
            "collection": collection,
            "relative_path": relative_path,
            "real_path": str(path.resolve()),
            "sha256": hashlib.sha256(data).hexdigest(),
            "digest_scope": "file_bytes",
            "bytes": len(data),
            "status": "readable",
            "read_error": None,
            "target_inside_corpus": True,
            "encoding_status": encoding_status,
        },
        "structure": {
            "entrypoint_candidate": entrypoint,
            "declared_skill_type": (
                original_metadata["value"].get("skill_type")
                if isinstance(original_metadata.get("value"), dict)
                and isinstance(original_metadata["value"].get("skill_type"), str)
                else None
            ),
            "role_status": "needs_semantic_review",
            "candidate_basis": (
                "case-insensitive entrypoint filename"
                if entrypoint
                else "source file occurrence retained by membership"
            ),
        },
        "original_metadata": original_metadata,
        "quality": {
            "metadata_status": original_metadata.get("status", "unknown"),
            "source_available": True,
            "runtime_status": "untested",
            "authored_claims_are_verdicts": False,
        },
        "diagnostics": diagnostics,
        "content_tokens": content_tokens,
    }
    row["source_id"] = source_id_for(base_label, relative_path)
    row["digest"] = row["source"]["sha256"]
    row["content_revision"] = row["source"]["sha256"]
    row["path_tokens"] = sorted(set(tokenize(row["rel_dir"])))
    row["name_tokens"] = sorted(set(tokenize(name) + tokenize(folder_name)))
    row["description_tokens"] = sorted(set(tokenize(row["description"])))
    row["tag_tokens"] = sorted(set(tokenize(" ".join(row["tags"] + row["triggers"] + row["aliases"]))))
    row["category_tokens"] = sorted(set(tokenize(category)))
    return row


RELATIONSHIP_FIELDS = (
    "related_skills", "dependencies", "subsumes", "source_flow", "references", "requires"
)


def project_relationships(rows: list[dict]) -> dict[str, list[dict]]:
    rows_by_id = {row["source_id"]: row for row in rows if isinstance(row.get("source_id"), str)}
    rows_by_path: defaultdict[tuple[str, str], list[str]] = defaultdict(list)
    names: defaultdict[str, set[str]] = defaultdict(set)
    for row in rows:
        source_id = row.get("source_id")
        if not isinstance(source_id, str):
            continue
        source = row.get("source") if isinstance(row.get("source"), dict) else {}
        relative_path = source.get("relative_path")
        base = row.get("base")
        if isinstance(base, str) and isinstance(relative_path, str):
            rows_by_path[(base, relative_path)].append(source_id)
        for value in (row.get("name"), row.get("slug"), row.get("folder")):
            if isinstance(value, str) and value.strip():
                names[normalize_name(value)].add(source_id)

    def string_values(value: object) -> list[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return [item for child in value for item in string_values(child)]
        if isinstance(value, dict):
            target_keys = {"id", "source_id", "path", "target", "name", "skill"}
            return [item for key, child in value.items() if key in target_keys for item in string_values(child)]
        return []

    def external_runtime_reference(key: str, value: str) -> bool:
        if key not in {"dependencies", "requires"}:
            return False
        return bool(re.search(r"(?:^|[,\s])[^,\s]+(?:>=|<=|==|~=|!=|>|<|\^|~)[^,\s]+", value))

    def resolve_target(row: dict, declaration_key: str, value: str, declared_base: object) -> dict:
        if value in rows_by_id:
            return {"original_value": value, "resolution_status": "resolved", "target_source_id": value}
        if value.startswith("source:") and value[len("source:") :] in rows_by_id:
            target = value[len("source:") :]
            return {"original_value": value, "resolution_status": "resolved", "target_source_id": target}
        if external_runtime_reference(declaration_key, value):
            return {"original_value": value, "resolution_status": "external_runtime"}
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", value) or value.startswith("/"):
            return {"original_value": value, "resolution_status": "external"}

        source = row.get("source") if isinstance(row.get("source"), dict) else {}
        relative_path = source.get("relative_path")
        namespace = row.get("base")
        if not isinstance(relative_path, str) or not isinstance(namespace, str):
            return {"original_value": value, "resolution_status": "not_resolved"}
        source_directory = PurePosixPath(relative_path).parent.as_posix()
        if source_directory == ".":
            source_directory = ""
        path_like = "/" in value or value.startswith((".", "..")) or bool(PurePosixPath(value).suffix)
        if path_like:
            if isinstance(declared_base, str) and declared_base:
                if declared_base.startswith("/") or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", declared_base):
                    return {"original_value": value, "resolution_status": "external"}
                base_directory = posixpath.normpath(posixpath.join(source_directory, declared_base))
            else:
                base_directory = source_directory
            target_path = posixpath.normpath(posixpath.join(base_directory, value))
            if target_path in {"..", "."} or target_path.startswith("../") or target_path.startswith("/"):
                return {"original_value": value, "resolution_status": "external"}
            target_ids = rows_by_path.get((namespace, target_path), [])
            if len(target_ids) == 1:
                return {
                    "original_value": value,
                    "resolution_status": "resolved",
                    "target_source_id": target_ids[0],
                }
            if len(target_ids) > 1:
                return {
                    "original_value": value,
                    "resolution_status": "ambiguous",
                    "candidate_source_ids": sorted(set(target_ids)),
                }
            return {"original_value": value, "resolution_status": "missing"}

        possible_names = sorted(names.get(normalize_name(value), set()))
        if len(possible_names) > 1:
            return {
                "original_value": value,
                "resolution_status": "ambiguous",
                "candidate_source_ids": possible_names,
            }
        return {
            "original_value": value,
            "resolution_status": "not_resolved",
            **({"candidate_source_ids": possible_names} if possible_names else {}),
        }

    output: dict[str, list[dict]] = {}
    for row in rows:
        source_id = row.get("source_id")
        if not isinstance(source_id, str):
            continue
        original_metadata = row.get("original_metadata")
        metadata = original_metadata.get("value") if isinstance(original_metadata, dict) else None
        metadata = metadata if isinstance(metadata, dict) else {}
        source = row.get("source") if isinstance(row.get("source"), dict) else {}
        source_ref = source.get("relative_path")
        source_directory = PurePosixPath(source_ref).parent.as_posix() if isinstance(source_ref, str) else ""
        if source_directory == ".":
            source_directory = ""
        declared_base = metadata.get("base")
        declarations = []
        for declaration_key in RELATIONSHIP_FIELDS:
            if declaration_key not in metadata:
                continue
            original_value = metadata[declaration_key]
            targets = [
                resolve_target(row, declaration_key, value, declared_base)
                for value in string_values(original_value)
            ]
            statuses = [target["resolution_status"] for target in targets]
            if not statuses:
                resolution_status = "not_resolved"
            elif all(status == "resolved" for status in statuses):
                resolution_status = "resolved"
            elif "external_runtime" in statuses:
                resolution_status = "external_runtime"
            elif "ambiguous" in statuses:
                resolution_status = "ambiguous"
            elif "external" in statuses:
                resolution_status = "external"
            elif "resolved" in statuses:
                resolution_status = "partially_resolved"
            elif "missing" in statuses:
                resolution_status = "missing"
            else:
                resolution_status = "not_resolved"
            declarations.append(
                {
                    "declaration_key": declaration_key,
                    "original_value": original_value,
                    "source_ref": source_ref,
                    "resolution_context": {
                        "source_directory": source_directory,
                        "declared_base": declared_base,
                    },
                    "resolution_status": resolution_status,
                    "semantic_status": "authored_not_verified",
                    "targets": targets,
                }
            )
        output[source_id] = declarations
    return output


def default_lifecycle_for(row: dict) -> tuple[str, str]:
    if row.get("doc_type") in {"markdown", "asset"}:
        if row["surface"] == "hidden":
            if row["category"] == ".archive":
                return "archived", "none"
            if row["category"] == "_todo":
                return "backlog", "none"
            return "incubating", "none"
        return "catalog", "none"
    if row["surface"] == "active":
        if row["core"]:
            return "core", "pinned"
        return "active", "eligible"
    if row["surface"] == "workflow":
        return "workflow", "none"
    if row["surface"] == "nested":
        return "nested", "none"
    if row["surface"] == "hidden":
        category = row["category"]
        if category == ".archive":
            return "archived", "none"
        if category == "_todo":
            return "backlog", "none"
        return "incubating", "none"
    if row["category"] == "experimental":
        return "experimental", "experimental"
    if row["surface"] == "catalog-nested":
        return "catalog", "none"
    return "catalog", "none"


def default_state_document() -> dict:
    return {
        "_schema": 1,
        "taxonomy": {
            "lifecycle": {
                "core": "Pinned runtime skill; always available.",
                "active": "Active runtime skill; eligible for normal use.",
                "workflow": "Workflow-only entrypoint; not part of random rotation.",
                "nested": "Nested helper skill; address directly, do not rotate globally.",
                "experimental": "Visible experimental skill; may be sampled intentionally.",
                "catalog": "Catalog skill; available but not active by default.",
                "incubating": "Workshop or staging skill under evaluation.",
                "backlog": "Queued for later cleanup or promotion.",
                "archived": "Retired; never surface in normal discovery.",
            },
            "rotation_role": {
                "pinned": "Always-on, never random.",
                "eligible": "Allowed in normal rotation.",
                "experimental": "Only for experimental rotation.",
                "none": "Do not randomize.",
            },
        },
        "skills": {},
    }


def load_state_db() -> dict:
    if not SKILLS_STATE_FILE.exists():
        return default_state_document()
    try:
        data = json.loads(SKILLS_STATE_FILE.read_bytes())
    except FileNotFoundError:
        return default_state_document()
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"skills state is unreadable or invalid: {error}") from error
    if not isinstance(data, dict) or not isinstance(data.get("skills", {}), dict):
        raise RuntimeError("skills state must be a JSON object with a skills mapping")
    for key, value in data.get("skills", {}).items():
        if not isinstance(key, str) or not isinstance(value, dict):
            raise RuntimeError("skills state entries must map string keys to JSON objects")
    return data


def read_input_document(path: Path, label: str, default: dict) -> tuple[dict, dict]:
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return default, {"status": "missing", "sha256": None}
    except OSError as error:
        raise RuntimeError(f"{label} is unreadable: {error}") from error
    try:
        data = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label} JSON is invalid: {error}") from error
    if not isinstance(data, dict):
        raise RuntimeError(f"{label} must be a JSON object")
    return data, {"status": "present", "sha256": hashlib.sha256(raw).hexdigest()}


def read_state_input() -> tuple[dict, dict]:
    state, signature = read_input_document(SKILLS_STATE_FILE, "skills state", default_state_document())
    if not isinstance(state.get("skills", {}), dict):
        raise RuntimeError("skills state must contain a skills mapping")
    for key, value in state.get("skills", {}).items():
        if not isinstance(key, str) or not isinstance(value, dict):
            raise RuntimeError("skills state entries must map string keys to JSON objects")
    return state, signature


def read_graph_input() -> tuple[dict, dict]:
    graph, signature = read_input_document(
        SKILL_GRAPH_FILE, "skill graph", {"nodes": {}, "edges": []}
    )
    nodes = graph.get("nodes", {})
    edges = graph.get("edges", [])
    if not isinstance(nodes, dict) or not isinstance(edges, list):
        raise RuntimeError("skill graph must contain a nodes object and edges array")
    return graph, signature


def digest_json(value) -> str:
    serialized = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def source_id_for(base_label: str, relative_path: str) -> str:
    """Return the stable source namespace plus exact relative filename identity."""
    if base_label not in {"skills-db", "skills", "_repos"}:
        raise ValueError(f"unapproved source namespace: {base_label!r}")
    if not isinstance(relative_path, str) or not relative_path:
        raise ValueError("source relative filename must be a non-empty string")
    if relative_path.startswith("/"):
        raise ValueError("source relative filename must not be absolute")
    parts = relative_path.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("source relative filename must be canonical")
    return f"{base_label}/{relative_path}"


def _unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _reject_json_constant(value: str):
    raise ValueError(f"invalid JSON constant: {value}")


def _taxonomy_error(message: str) -> RuntimeError:
    return RuntimeError(f"taxonomy configuration is invalid: {message}")


def observed_skills_db_collections() -> set[str]:
    """Return the current top-level source collections, excluding disposed trash."""
    if not SKILLS_DB_DIR.exists():
        return set()
    if not SKILLS_DB_DIR.is_dir():
        raise _taxonomy_error(f"skills-db source root is not a directory: {SKILLS_DB_DIR}")
    names = set()
    try:
        for entry in SKILLS_DB_DIR.iterdir():
            if entry.name == ".trash":
                continue
            if entry.is_symlink():
                raise _taxonomy_error(f"skills-db collection root is a symlink: {entry.name}")
            if entry.is_dir():
                names.add(entry.name)
    except OSError as error:
        raise _taxonomy_error(f"cannot inspect skills-db source collections: {error}") from error
    return names


def validate_taxonomy_config(config: object) -> dict:
    if not isinstance(config, dict):
        raise _taxonomy_error("document must be an object")
    required_top = {
        "schema_version", "provenance", "source_namespaces", "nodes", "source_collections", "rules"
    }
    if set(config) != required_top:
        missing = sorted(required_top - set(config))
        extra = sorted(set(config) - required_top)
        raise _taxonomy_error(f"top-level fields mismatch (missing={missing}, extra={extra})")
    if config.get("schema_version") != "skills-taxonomy/v2":
        raise _taxonomy_error("unsupported schema_version")

    provenance = config.get("provenance")
    if (
        not isinstance(provenance, dict)
        or set(provenance) != {
            "source_ref", "source_sha256", "leaves_are_examples_not_exhaustive",
            "category_guidance_ref", "category_guidance_sha256", "category_guidance_status",
        }
        or not isinstance(provenance.get("source_ref"), str)
        or not provenance["source_ref"]
        or not isinstance(provenance.get("source_sha256"), str)
        or not re.fullmatch(r"[a-f0-9]{64}", provenance["source_sha256"])
        or provenance.get("leaves_are_examples_not_exhaustive") is not True
        or not isinstance(provenance.get("category_guidance_ref"), str)
        or not provenance["category_guidance_ref"]
        or not isinstance(provenance.get("category_guidance_sha256"), str)
        or not re.fullmatch(r"[a-f0-9]{64}", provenance["category_guidance_sha256"])
        or provenance.get("category_guidance_status") != "proposed"
    ):
        raise _taxonomy_error("provenance must bind the accepted tree and proposed category guidance")

    namespace_values = config.get("source_namespaces")
    if not isinstance(namespace_values, list) or not namespace_values:
        raise _taxonomy_error("source_namespaces must be a non-empty array")
    namespaces = {}
    for item in namespace_values:
        if (
            not isinstance(item, dict)
            or set(item) != {"id", "root", "role", "node_id"}
            or any(not isinstance(item.get(key), str) or not item[key] for key in ("id", "root", "role", "node_id"))
        ):
            raise _taxonomy_error("each source namespace needs id, root, role, and node_id strings")
        if item["id"] in namespaces:
            raise _taxonomy_error(f"duplicate source namespace: {item['id']}")
        namespaces[item["id"]] = item
    if set(namespaces) != {"skills-db", "skills", "_repos"}:
        raise _taxonomy_error("source_namespaces must declare skills-db, skills, and _repos exactly")
    expected_namespace_roles = {
        "skills-db": "approved_corpus",
        "skills": "installed_entrypoints",
        "_repos": "curated_repositories",
    }
    if any(
        namespaces[key]["root"] != key or namespaces[key]["role"] != expected_namespace_roles[key]
        for key in namespaces
    ):
        raise _taxonomy_error("source namespace roots and roles must match their admitted declarations")

    node_values = config.get("nodes")
    if not isinstance(node_values, list) or not node_values:
        raise _taxonomy_error("nodes must be a non-empty array")
    nodes = {}
    valid_kinds = {
        "subject", "view_group", "task_group", "task", "form_group", "form", "distribution",
        "source_group", "administration_group", "administration", "platform_group", "platform",
        "platform_variant", "source_namespace", "source_collection",
    }
    for item in node_values:
        if not isinstance(item, dict):
            raise _taxonomy_error("each node must be an object")
        allowed = {"id", "label", "parent_id", "view_kind", "examples", "examples_exhaustive"}
        if not {"id", "label", "parent_id", "view_kind"} <= set(item) or set(item) - allowed:
            raise _taxonomy_error("node fields are missing or unsupported")
        if any(not isinstance(item.get(key), str) or not item[key] for key in ("id", "label", "view_kind")):
            raise _taxonomy_error("node id, label, and view_kind must be non-empty strings")
        if item["view_kind"] not in valid_kinds:
            raise _taxonomy_error(f"unsupported node view_kind: {item['view_kind']}")
        if item["parent_id"] is not None and not isinstance(item["parent_id"], str):
            raise _taxonomy_error(f"node {item['id']} parent_id must be a string or null")
        if "examples" in item:
            if (
                not isinstance(item["examples"], list)
                or any(not isinstance(example, str) for example in item["examples"])
                or item.get("examples_exhaustive") is not False
            ):
                raise _taxonomy_error(f"node {item['id']} examples must be explicitly non-exhaustive")
        elif "examples_exhaustive" in item:
            raise _taxonomy_error(f"node {item['id']} cannot declare example exhaustiveness without examples")
        if item["id"] in nodes:
            raise _taxonomy_error(f"duplicate taxonomy node id: {item['id']}")
        nodes[item["id"]] = item
    for item in node_values:
        if item["parent_id"] is not None and item["parent_id"] not in nodes:
            raise _taxonomy_error(f"node {item['id']} references a missing parent")
        seen_ancestors = set()
        current = item
        while current["parent_id"] is not None:
            if current["id"] in seen_ancestors:
                raise _taxonomy_error(f"taxonomy node hierarchy contains a cycle at {current['id']}")
            seen_ancestors.add(current["id"])
            current = nodes[current["parent_id"]]
    namespace_node_ids = {item["node_id"] for item in namespace_values}
    if {node["id"] for node in node_values if node["view_kind"] == "source_namespace"} != namespace_node_ids:
        raise _taxonomy_error("source namespace nodes must match source_namespaces exactly")
    for item in namespace_values:
        node = nodes.get(item["node_id"])
        if not node or node.get("view_kind") != "source_namespace":
            raise _taxonomy_error(f"source namespace {item['id']} must reference a source_namespace node")

    collection_values = config.get("source_collections")
    if not isinstance(collection_values, list):
        raise _taxonomy_error("source_collections must be an array")
    collections = {}
    for item in collection_values:
        if (
            not isinstance(item, dict)
            or set(item) != {"namespace", "name", "policy", "node_id"}
            or any(not isinstance(item.get(key), str) or not item[key] for key in ("namespace", "name", "policy", "node_id"))
            or item.get("name") in {".", ".."}
            or "/" in item.get("name", "")
            or "\\" in item.get("name", "")
        ):
            raise _taxonomy_error("each source collection needs namespace, name, policy, and node_id strings")
        if item["namespace"] not in namespaces or item["policy"] not in {"regular", "administrative"}:
            raise _taxonomy_error(f"invalid source collection declaration: {item}")
        if item["node_id"] not in nodes or nodes[item["node_id"]].get("view_kind") != "source_collection":
            raise _taxonomy_error(f"source collection {item['name']} must reference a source_collection node")
        if (
            nodes[item["node_id"]].get("label") != item["name"]
            or nodes[item["node_id"]].get("parent_id") != namespaces[item["namespace"]]["node_id"]
        ):
            raise _taxonomy_error(f"source collection {item['name']} must remain under its namespace node")
        key = (item["namespace"], item["name"])
        if key in collections:
            raise _taxonomy_error(f"duplicate source collection: {key}")
        collections[key] = item
    corpus_collections = [item for item in collection_values if item["namespace"] == "skills-db"]
    administrative_collections = {".archive", "_todo", "_workshop"}
    declared_corpus_names = {item["name"] for item in corpus_collections}
    actual_corpus_names = observed_skills_db_collections()
    if (
        not administrative_collections <= declared_corpus_names
        or {item["name"] for item in corpus_collections if item["policy"] == "administrative"}
        != administrative_collections
        or next((item["policy"] for item in corpus_collections if item["name"] == "other"), None) != "regular"
    ):
        raise _taxonomy_error("skills-db must retain the three administrative collections and regular other collection")
    missing_corpus_declarations = actual_corpus_names - declared_corpus_names
    if missing_corpus_declarations:
        missing_names = ", ".join(sorted(missing_corpus_declarations))
        raise _taxonomy_error(f"observed skills-db collections are undeclared: {missing_names}")
    collection_node_ids = {item["node_id"] for item in collection_values}
    if {node["id"] for node in node_values if node["view_kind"] == "source_collection"} != collection_node_ids:
        raise _taxonomy_error("source collection nodes must match source_collections exactly")

    rules = config.get("rules")
    expected_rule_sets = {
        "namespace_views", "collection_views", "path_views", "metadata_views", "structural_views", "task_cues"
    }
    if not isinstance(rules, dict) or set(rules) != expected_rule_sets:
        raise _taxonomy_error("rules must declare namespace, collection, path, metadata, structure, and task views")
    namespace_views = rules["namespace_views"]
    if (
        not isinstance(namespace_views, dict)
        or set(namespace_views) != set(namespaces)
        or any(namespace_views.get(key) != namespaces[key]["node_id"] for key in namespaces)
    ):
        raise _taxonomy_error("namespace_views must map every source namespace to its declared node")

    collection_views = rules["collection_views"]
    if not isinstance(collection_views, list):
        raise _taxonomy_error("collection_views must be an array")
    rule_ids = set()
    for item in collection_views:
        if (
            not isinstance(item, dict)
            or set(item) != {
                "id", "namespace", "collection", "target_node_ids", "basis_kind", "basis_status",
                "basis_source", "basis_description",
            }
            or any(not isinstance(item.get(key), str) or not item[key] for key in (
                "id", "namespace", "collection", "basis_kind", "basis_status", "basis_source", "basis_description"
            ))
            or item["namespace"] not in namespaces
            or not isinstance(item["target_node_ids"], list)
            or not item["target_node_ids"]
            or any(not isinstance(target, str) or target not in nodes for target in item["target_node_ids"])
            or len(item["target_node_ids"]) != len(set(item["target_node_ids"]))
            or (item["namespace"], item["collection"]) not in collections
        ):
            raise _taxonomy_error("invalid collection view rule")
        valid_basis = {
            ("accepted_source_grouping", "accepted_example", "accepted-tree"),
            ("source_policy", "source_policy", "accepted-tree"),
            ("proposed_collection_guidance", "provisional", "category-review"),
        }
        if (item["basis_kind"], item["basis_status"], item["basis_source"]) not in valid_basis:
            raise _taxonomy_error(f"collection view rule {item['id']} has an unsupported evidence status")
        if item["id"] in rule_ids:
            raise _taxonomy_error(f"duplicate taxonomy rule id: {item['id']}")
        rule_ids.add(item["id"])

    path_views = rules["path_views"]
    if not isinstance(path_views, list):
        raise _taxonomy_error("path_views must be an array")
    for item in path_views:
        if (
            not isinstance(item, dict)
            or set(item) != {
                "id", "namespace", "match", "path", "target_node_ids", "example", "basis_kind",
                "basis_status", "basis_source", "basis_description",
            }
            or any(not isinstance(item.get(key), str) or not item[key] for key in (
                "id", "namespace", "match", "path", "example", "basis_kind", "basis_status",
                "basis_source", "basis_description",
            ))
            or item["namespace"] not in namespaces
            or item["match"] not in {"exact", "prefix"}
            or item["path"].startswith("/")
            or any(part in {"", ".", ".."} for part in item["path"].rstrip("/").split("/"))
            or (item["match"] == "prefix" and item["path"].endswith("/"))
            or item["basis_kind"] not in {"accepted_example", "accepted_structure"}
            or item["basis_status"] not in {"accepted_example", "accepted_structure"}
            or item["basis_source"] != "accepted-tree"
            or not isinstance(item["target_node_ids"], list)
            or not item["target_node_ids"]
            or any(not isinstance(target, str) or target not in nodes for target in item["target_node_ids"])
            or len(item["target_node_ids"]) != len(set(item["target_node_ids"]))
        ):
            raise _taxonomy_error("invalid path view rule")
        if item["basis_kind"] == "accepted_example" and item["basis_status"] != "accepted_example":
            raise _taxonomy_error(f"path view rule {item['id']} must label accepted examples")
        if item["id"] in rule_ids:
            raise _taxonomy_error(f"duplicate taxonomy rule id: {item['id']}")
        rule_ids.add(item["id"])

    metadata_views = rules["metadata_views"]
    if not isinstance(metadata_views, dict) or set(metadata_views) != {"subjects", "tasks", "platforms", "forms"}:
        raise _taxonomy_error("metadata_views must map subjects, tasks, platforms, and forms")
    expected_kinds = {"subjects": "subject", "tasks": "task", "platforms": "platform", "forms": "form"}
    for field, mapping in metadata_views.items():
        if not isinstance(mapping, dict) or not mapping:
            raise _taxonomy_error(f"metadata_views.{field} must be a non-empty object")
        normalized_values = set()
        for value, target in mapping.items():
            if not isinstance(value, str) or not value or not isinstance(target, str) or target not in nodes:
                raise _taxonomy_error(f"metadata_views.{field} has an invalid value mapping")
            normalized_value = normalize_name(value)
            if not normalized_value or normalized_value in normalized_values:
                raise _taxonomy_error(f"metadata_views.{field} contains an empty or duplicate normalized value")
            normalized_values.add(normalized_value)
            node_kind = nodes[target]["view_kind"]
            if field == "platforms":
                valid_kind = node_kind == "platform"
            else:
                valid_kind = node_kind == expected_kinds[field]
            if not valid_kind:
                raise _taxonomy_error(f"metadata_views.{field} maps to the wrong view kind")

    structural_views = rules["structural_views"]
    if not isinstance(structural_views, list):
        raise _taxonomy_error("structural_views must be an array")
    for item in structural_views:
        if (
            not isinstance(item, dict)
            or set(item) != {
                "id", "selector", "value", "target_node_id", "basis_kind", "basis_status",
                "basis_source", "basis_description",
            }
            or any(not isinstance(item.get(key), str) or not item[key] for key in (
                "id", "selector", "target_node_id", "basis_kind", "basis_status", "basis_source", "basis_description"
            ))
            or item["selector"] not in {"entrypoint_candidate", "declared_skill_type", "path_segment"}
            or not isinstance(item.get("target_node_id"), str)
            or item["target_node_id"] not in nodes
            or nodes[item["target_node_id"]]["view_kind"] != "form"
            or item["basis_kind"] != "structural_form_hint"
            or item["basis_status"] != "provisional"
            or item["basis_source"] != "source-structure"
        ):
            raise _taxonomy_error("invalid structural form view rule")
        if item["selector"] == "entrypoint_candidate" and item["value"] is not True:
            raise _taxonomy_error(f"structural rule {item['id']} needs entrypoint_candidate=true")
        if item["selector"] != "entrypoint_candidate" and (
            not isinstance(item["value"], str) or not item["value"]
        ):
            raise _taxonomy_error(f"structural rule {item['id']} needs a non-empty string value")
        if item["selector"] == "path_segment" and "/" in item["value"]:
            raise _taxonomy_error(f"structural path segment rule {item['id']} must name one segment")
        if item["id"] in rule_ids:
            raise _taxonomy_error(f"duplicate taxonomy rule id: {item['id']}")
        rule_ids.add(item["id"])

    task_cues = rules["task_cues"]
    if not isinstance(task_cues, list):
        raise _taxonomy_error("task_cues must be an array")
    for item in task_cues:
        if not isinstance(item, dict) or not isinstance(item.get("selector"), str):
            raise _taxonomy_error("invalid task cue rule")
        selector = item["selector"]
        if selector == "source_collection":
            expected_fields = {
                "id", "selector", "namespace", "collection", "target_node_id", "basis_kind",
                "basis_status", "basis_source", "basis_description",
            }
            valid = (
                set(item) == expected_fields
                and all(isinstance(item.get(key), str) and item[key] for key in expected_fields - {"selector"})
                and item["namespace"] in namespaces
                and (item["namespace"], item["collection"]) in collections
                and item["target_node_id"] in nodes
                and nodes[item["target_node_id"]]["view_kind"] == "task"
                and item["basis_kind"] == "proposed_collection_guidance"
                and item["basis_status"] == "provisional"
                and item["basis_source"] == "category-review"
            )
        elif selector == "name_description_tokens":
            expected_fields = {
                "id", "selector", "tokens", "target_node_id", "basis_kind", "basis_status",
                "basis_source", "basis_description",
            }
            tokens = item.get("tokens")
            valid = (
                set(item) == expected_fields
                and all(isinstance(item.get(key), str) and item[key] for key in expected_fields - {"selector", "tokens"})
                and isinstance(tokens, list)
                and bool(tokens)
                and all(isinstance(token, str) and token for token in tokens)
                and len({normalize_name(token) for token in tokens}) == len(tokens)
                and item["target_node_id"] in nodes
                and nodes[item["target_node_id"]]["view_kind"] == "task"
                and item["basis_kind"] == "explicit_name_description_cue"
                and item["basis_status"] == "provisional"
                and item["basis_source"] == "source-fields"
            )
        else:
            valid = False
        if not valid:
            raise _taxonomy_error(f"invalid task cue rule for selector {selector}")
        if item["id"] in rule_ids:
            raise _taxonomy_error(f"duplicate taxonomy rule id: {item['id']}")
        rule_ids.add(item["id"])

    return config


def load_taxonomy_config(path: Path | None = None) -> dict:
    config_path = Path(path) if path is not None else TAXONOMY_CONFIG_FILE
    try:
        raw = config_path.read_bytes()
    except FileNotFoundError:
        return {
            "status": "unconfigured",
            "config": None,
            "sha256": None,
            "path": str(config_path),
            "diagnostics": ["skills-taxonomy.json is absent; accepted category views are unconfigured"],
        }
    except OSError as error:
        raise RuntimeError(f"taxonomy configuration is unreadable: {config_path}: {error}") from error
    try:
        parsed = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_json_object,
            parse_constant=_reject_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"taxonomy configuration is malformed: {config_path}: {error}") from error
    config = validate_taxonomy_config(parsed)
    return {
        "status": "configured",
        "config": config,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "path": str(config_path),
        "diagnostics": [],
    }


def taxonomy_signature(taxonomy_state: dict) -> dict:
    return {"status": taxonomy_state["status"], "sha256": taxonomy_state.get("sha256")}


def build_bundle_catalog(source_records: list[dict]) -> tuple[list[dict], dict[str, str]]:
    """Build one snapshot per evidenced package or unresolved standalone file."""
    entrypoints: defaultdict[tuple[str, tuple[str, ...]], list[dict]] = defaultdict(list)
    normalized_records = []
    seen_source_ids = set()
    for record in source_records:
        base = record.get("base")
        relative_path = record.get("relative_path")
        source_id = source_id_for(base, relative_path)
        if source_id in seen_source_ids:
            raise RuntimeError(f"duplicate source occurrence: {source_id}")
        seen_source_ids.add(source_id)
        parts = tuple(relative_path.split("/"))
        normalized = {**record, "source_id": source_id, "relative_parts": parts}
        normalized_records.append(normalized)
        if base == "skills-db" and parts[-1].casefold() == "skill.md":
            entrypoints[(base, parts[:-1])].append(normalized)

    groups: defaultdict[tuple[str, str], list[tuple[dict, tuple[str, ...], str, str, str, str, str | None]]] = defaultdict(list)
    assignments: dict[str, str] = {}
    for record in normalized_records:
        base = record["base"]
        parts = record["relative_parts"]
        package = None
        ambiguous = False
        if base == "skills-db":
            for length in range(len(parts) - 1, -1, -1):
                candidates = entrypoints.get((base, parts[:length]), [])
                if candidates:
                    if len(candidates) == 1:
                        package = candidates[0]
                    else:
                        ambiguous = True
                    break

        if package is not None:
            root_parts = package["relative_parts"][:-1]
            member_parts = parts[len(root_parts) :]
            grouping_key = ("package", package["source_id"])
            bundle_id = f"bundle:{package['source_id']}"
            scope = "package_snapshot"
            boundary_status = "entrypoint_directory"
            entrypoint_source_id = package["source_id"]
        else:
            root_parts = parts[:-1]
            member_parts = parts[-1:]
            grouping_key = ("standalone", record["source_id"])
            bundle_id = f"bundle:{record['source_id']}"
            scope = "standalone_file"
            entrypoint_source_id = None
            if ambiguous:
                boundary_status = "unknown_multiple_entrypoints"
            elif base in {"skills", "_repos"}:
                boundary_status = "unknown_unenumerated_assets"
            else:
                boundary_status = "unknown_no_package_marker"

        member_path = PurePosixPath(*member_parts).as_posix()
        groups[grouping_key].append(
            (record, tuple(root_parts), member_path, bundle_id, scope, boundary_status, entrypoint_source_id)
        )
        assignments[record["source_id"]] = bundle_id

    catalog = []
    for grouping_key, members_with_context in groups.items():
        first_record, _, _, bundle_id, scope, boundary_status, entrypoint_source_id = members_with_context[0]

        members = [
            {
                "source_id": record["source_id"],
                "relative_path": member_path,
                "digest": record["sha256"],
            }
            for record, _, member_path, _, _, _, _ in members_with_context
        ]
        members.sort(key=lambda item: (item["relative_path"], item["digest"], item["source_id"]))
        bundle_digest_payload = [
            {"relative_path": item["relative_path"], "digest": item["digest"]} for item in members
        ]
        catalog.append(
            {
                "bundle_id": bundle_id,
                "source_namespace": first_record["base"],
                "entrypoint_source_id": entrypoint_source_id,
                "scope": scope,
                "boundary_status": boundary_status,
                "digest_scope": "sorted_member_relative_paths_and_file_digests",
                "member_count": len(members),
                "members": members,
                "sha256": digest_json(bundle_digest_payload),
            }
        )
    catalog.sort(key=lambda item: item["bundle_id"])
    if set(assignments) != seen_source_ids:
        raise RuntimeError("bundle catalog did not assign every source occurrence exactly once")
    return catalog, assignments


def project_taxonomy_row(row: dict, taxonomy_state: dict) -> dict:
    if taxonomy_state.get("status") != "configured":
        unresolved_views = ["subject", "task", "platform", "form", "distribution"]
        return {
            "status": "unconfigured",
            "semantic_status": "unresolved",
            "memberships": [],
            "semantic_memberships": [],
            "unresolved_views": unresolved_views,
            "unresolved": [
                {
                    "view": view,
                    "status": "unconfigured",
                    "basis": {"kind": "taxonomy_configuration_absent", "path": taxonomy_state.get("path")},
                }
                for view in unresolved_views
            ],
            "diagnostics": list(taxonomy_state.get("diagnostics", [])),
        }

    config = taxonomy_state["config"]
    nodes = {node["id"]: node for node in config["nodes"]}
    rules = config["rules"]
    source = row.get("source") if isinstance(row.get("source"), dict) else {}
    namespace = row.get("base")
    collection = source.get("collection")
    relative_path = source.get("relative_path")
    disposed = has_disposed_ancestor(row)
    membership_map: dict[str, dict] = {}

    def store_membership(node_id: str, rule_id: str, basis: dict) -> None:
        membership = membership_map.setdefault(
            node_id,
            {"node_id": node_id, "status": "projected", "rule_ids": [], "basis": [], "basis_statuses": []},
        )
        if rule_id not in membership["rule_ids"]:
            membership["rule_ids"].append(rule_id)
        if basis not in membership["basis"]:
            membership["basis"].append(basis)
        basis_status = basis.get("basis_status")
        if isinstance(basis_status, str) and basis_status not in membership["basis_statuses"]:
            membership["basis_statuses"].append(basis_status)

    def add_membership(node_id: str, rule_id: str, basis: dict) -> None:
        source_basis = {
            **basis,
            "source_id": row.get("source_id"),
            "source_ref": relative_path,
        }
        store_membership(node_id, rule_id, source_basis)
        source_node_id = node_id
        parent_id = nodes[node_id].get("parent_id")
        while parent_id is not None:
            store_membership(
                parent_id,
                rule_id,
                {
                    "kind": "taxonomy_ancestor_rollup",
                    "basis_status": source_basis.get("basis_status", "source_provenance"),
                    "from_node_id": source_node_id,
                    "source_basis": source_basis,
                },
            )
            parent_id = nodes[parent_id].get("parent_id")

    namespace_node = rules["namespace_views"].get(namespace)
    if namespace_node:
        add_membership(
            namespace_node,
            "source-namespace",
            {
                "kind": "source_provenance",
                "basis_status": "source_provenance",
                "basis_source": "source-record",
                "field": "base",
                "value": namespace,
            },
        )

    for collection_item in config["source_collections"]:
        if collection_item["namespace"] == namespace and collection_item["name"] == collection:
            add_membership(
                collection_item["node_id"],
                "source-collection",
                {
                    "kind": "source_provenance",
                    "basis_status": "source_provenance",
                    "basis_source": "source-record",
                    "field": "source.collection",
                    "value": collection,
                    "policy": collection_item["policy"],
                },
            )
            break

    diagnostics = []
    if disposed:
        diagnostics.append(".trash source is retained by identity and suppressed from semantic views by the existing disposal policy")
    else:
        for rule in rules["collection_views"]:
            if rule["namespace"] == namespace and rule["collection"] == collection:
                for node_id in rule["target_node_ids"]:
                    add_membership(
                        node_id,
                        rule["id"],
                        {
                            "kind": rule["basis_kind"],
                            "basis_status": rule["basis_status"],
                            "basis_source": rule["basis_source"],
                            "field": "source.collection",
                            "value": collection,
                            "description": rule["basis_description"],
                        },
                    )

        for rule in rules["path_views"]:
            if rule["namespace"] != namespace or not isinstance(relative_path, str):
                continue
            path = rule["path"]
            if rule["match"] == "exact":
                matches = relative_path == path
            else:
                matches = relative_path == path or relative_path.startswith(path + "/")
            if matches:
                for node_id in rule["target_node_ids"]:
                    add_membership(
                        node_id,
                        rule["id"],
                        {
                            "kind": rule["basis_kind"],
                            "basis_status": rule["basis_status"],
                            "basis_source": rule["basis_source"],
                            "field": "source.relative_path",
                            "value": relative_path,
                            "example": rule["example"],
                            "description": rule["basis_description"],
                        },
                    )

        original_metadata = row.get("original_metadata")
        metadata = original_metadata.get("value") if isinstance(original_metadata, dict) else None
        metadata = metadata if isinstance(metadata, dict) else {}
        for field, mapping in rules["metadata_views"].items():
            if field not in metadata:
                continue
            value = metadata[field]
            if isinstance(value, str):
                values = [value]
            elif isinstance(value, list) and all(isinstance(item, str) for item in value):
                values = value
            elif isinstance(value, dict) and all(isinstance(key, str) for key in value):
                values = list(value)
            else:
                diagnostics.append(f"metadata field {field} has no supported taxonomy value shape")
                continue
            normalized_mapping = {normalize_name(key): target for key, target in mapping.items()}
            for item in values:
                normalized = normalize_name(item.strip())
                target_node = normalized_mapping.get(normalized)
                if target_node:
                    add_membership(
                        target_node,
                        f"authored-metadata-{field}",
                        {
                            "kind": "authored_metadata",
                            "basis_status": "authored_metadata",
                            "basis_source": "original_metadata",
                            "field": field,
                            "value": item,
                        },
                    )
                else:
                    diagnostics.append(f"unresolved taxonomy value in {field}: {item}")

        structure = row.get("structure") if isinstance(row.get("structure"), dict) else {}
        path_parts = set(PurePosixPath(relative_path).parts) if isinstance(relative_path, str) else set()
        for rule in rules["structural_views"]:
            if rule["selector"] == "entrypoint_candidate":
                matches = structure.get("entrypoint_candidate") is True
            elif rule["selector"] == "declared_skill_type":
                matches = normalize_name(str(structure.get("declared_skill_type") or "")) == normalize_name(rule["value"])
            else:
                matches = rule["value"].casefold() in {part.casefold() for part in path_parts}
            if matches:
                add_membership(
                    rule["target_node_id"],
                    rule["id"],
                    {
                        "kind": rule["basis_kind"],
                        "basis_status": rule["basis_status"],
                        "basis_source": rule["basis_source"],
                        "field": rule["selector"],
                        "value": rule["value"],
                        "description": rule["basis_description"],
                    },
                )

        for rule in rules["task_cues"]:
            if rule["selector"] == "source_collection":
                matches = namespace == rule["namespace"] and collection == rule["collection"]
                evidence = {"field": "source.collection", "value": collection}
            else:
                matches = False
                evidence = None
                for field in ("name", "description"):
                    observed_tokens = set(tokenize(str(row.get(field) or "")))
                    matched_tokens = sorted(observed_tokens & {normalize_name(token) for token in rule["tokens"]})
                    field_origin = (
                        "authored_metadata"
                        if field in metadata and isinstance(metadata.get(field), str)
                        else ("source_path_fallback" if field == "name" else "source_body_summary")
                    )
                    for token in matched_tokens:
                        matches = True
                        add_membership(
                            rule["target_node_id"],
                            rule["id"],
                            {
                                "kind": rule["basis_kind"],
                                "basis_status": rule["basis_status"],
                                "basis_source": rule["basis_source"],
                                "field": field,
                                "field_origin": field_origin,
                                "token": token,
                                "description": rule["basis_description"],
                            },
                        )
            if rule["selector"] == "source_collection" and matches:
                add_membership(
                    rule["target_node_id"],
                    rule["id"],
                    {
                        "kind": rule["basis_kind"],
                        "basis_status": rule["basis_status"],
                        "basis_source": rule["basis_source"],
                        **evidence,
                        "description": rule["basis_description"],
                    },
                )

    memberships = []
    for node_id in sorted(membership_map):
        membership = membership_map[node_id]
        membership["rule_ids"].sort()
        membership["basis_statuses"].sort()
        membership["basis"].sort(key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False))
        memberships.append(membership)

    semantic_kinds = {"subject", "task", "platform", "platform_variant", "form", "distribution"}
    semantic_memberships = [
        item["node_id"] for item in memberships if nodes[item["node_id"]]["view_kind"] in semantic_kinds
    ]
    view_kinds = {
        "subject": {"subject"},
        "task": {"task"},
        "platform": {"platform", "platform_variant"},
        "form": {"form"},
        "distribution": {"distribution"},
    }
    unresolved_views = [
        view
        for view, kinds in view_kinds.items()
        if not any(nodes[item["node_id"]]["view_kind"] in kinds for item in memberships)
    ]
    unresolved = [
        {
            "view": view,
            "status": "unresolved",
            "basis": {
                "kind": "disposed_source_suppressed" if disposed else "no_matching_accepted_rule_or_metadata_value",
                "source_id": row.get("source_id"),
                "source_ref": relative_path,
            },
        }
        for view in unresolved_views
    ]
    return {
        "status": "projected",
        "semantic_status": "projected" if semantic_memberships else "unresolved",
        "memberships": memberships,
        "semantic_memberships": semantic_memberships,
        "unresolved_views": unresolved_views,
        "unresolved": unresolved,
        "diagnostics": diagnostics,
    }


def build_taxonomy_catalog(rows: list[dict], taxonomy_state: dict) -> dict:
    source_ids = {row.get("source_id") for row in rows if isinstance(row.get("source_id"), str)}
    if taxonomy_state.get("status") != "configured":
        return {
            "status": "unconfigured",
            "config_sha256": None,
            "distinct_resource_count": len(source_ids),
            "nodes": [],
            "source_collections": [],
            "view_counts": {},
            "example_diagnostics": [],
            "diagnostics": list(taxonomy_state.get("diagnostics", [])),
        }

    config = taxonomy_state["config"]
    counts: defaultdict[str, set[str]] = defaultdict(set)
    collection_counts: defaultdict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        source_id = row.get("source_id")
        if not isinstance(source_id, str):
            continue
        taxonomy = row.get("taxonomy") if isinstance(row.get("taxonomy"), dict) else {}
        for membership in taxonomy.get("memberships", []):
            node_id = membership.get("node_id") if isinstance(membership, dict) else None
            if isinstance(node_id, str):
                counts[node_id].add(source_id)
        source = row.get("source") if isinstance(row.get("source"), dict) else {}
        collection = source.get("collection")
        if isinstance(row.get("base"), str) and isinstance(collection, str):
            collection_counts[(row["base"], collection)].add(source_id)

    observed_paths = [
        (
            row.get("base"),
            (row.get("source") or {}).get("relative_path") if isinstance(row.get("source"), dict) else None,
        )
        for row in rows
    ]
    mapped_examples = set()
    declared_examples = set()
    for rule in config["rules"]["path_views"]:
        matched_source = any(
            namespace == rule["namespace"]
            and isinstance(relative_path, str)
            and (
                relative_path == rule["path"]
                if rule["match"] == "exact"
                else relative_path == rule["path"] or relative_path.startswith(rule["path"] + "/")
            )
            for namespace, relative_path in observed_paths
        )
        example_key = normalize_name(rule["example"])
        for target in rule["target_node_ids"]:
            declared_examples.add((target, example_key))
            if matched_source:
                mapped_examples.add((target, example_key))
    source_collection_names = {
        (item["namespace"], normalize_name(item["name"])) for item in config["source_collections"]
    }
    example_diagnostics = []
    for node in config["nodes"]:
        for example in node.get("examples", []):
            if node["view_kind"] == "source_group" and ("skills-db", normalize_name(example)) in source_collection_names:
                continue
            example_key = (node["id"], normalize_name(example))
            if example_key not in mapped_examples:
                example_diagnostics.append(
                    {
                        "node_id": node["id"],
                        "example": example,
                        "status": (
                            "accepted_example_rule_has_no_source_match"
                            if example_key in declared_examples
                            else "unmapped_illustrative_example"
                        ),
                        "basis": "No current source occurrence is bound to this non-exhaustive accepted-tree example.",
                    }
                )

    return {
        "status": "projected",
        "config_sha256": taxonomy_state.get("sha256"),
        "distinct_resource_count": len(source_ids),
        "nodes": config["nodes"],
        "source_collections": [
            {
                **item,
                "resource_count": len(collection_counts[(item["namespace"], item["name"])]),
            }
            for item in config["source_collections"]
        ],
        "view_counts": {node["id"]: len(counts[node["id"]]) for node in config["nodes"]},
        "example_diagnostics": example_diagnostics,
        "diagnostics": [],
    }


def scan_source_inputs(*, include_bytes: bool = False) -> tuple[dict[str, bool], list[dict]]:
    if not SKILLS_DB_DIR.is_dir():
        if not SKILLS_DB_DIR.exists():
            raise RuntimeError(f"required skills-db source root is missing: {SKILLS_DB_DIR}")
        raise RuntimeError(f"required skills-db source root is not a directory: {SKILLS_DB_DIR}")
    roots = {
        "skills-db": SKILLS_DB_DIR,
        "skills": SKILLS_DIR,
        "_repos": SKILL_REPOS_DIR,
    }
    root_presence = {}
    for label, path in roots.items():
        if path.exists() and not path.is_dir():
            raise RuntimeError(f"source root is not a directory: {path}")
        root_presence[label] = path.is_dir()

    records = []
    for base_label, root, path, rel_parts in source_file_specs():
        try:
            data = path.read_bytes()
        except OSError as error:
            raise RuntimeError(f"source file is unreadable: {path}: {error}") from error
        relative_path = Path(*rel_parts).as_posix()
        record = {
            "base": base_label,
            "relative_path": relative_path,
            "occurrence_key": f"{base_label}/{relative_path}",
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "path": path,
            "root": root,
            "rel_parts": rel_parts,
        }
        if include_bytes:
            record["data"] = data
        records.append(record)
    records.sort(key=lambda item: item["occurrence_key"])
    return root_presence, records


def input_fingerprints(
    root_presence: dict[str, bool],
    source_records: list[dict],
    state_signature: dict,
    graph_signature: dict,
    taxonomy_input: dict | None = None,
    bundle_catalog_sha256: str | None = None,
) -> dict:
    taxonomy_input = taxonomy_input or {"status": "unconfigured", "sha256": None}
    bundle_catalog_sha256 = bundle_catalog_sha256 or digest_json([])
    source_inventory = [
        {
            "occurrence_key": item["occurrence_key"],
            "sha256": item["sha256"],
            "bytes": item["bytes"],
        }
        for item in source_records
    ]
    source_membership_sha256 = digest_json(
        {"roots": root_presence, "occurrences": [item["occurrence_key"] for item in source_inventory]}
    )
    source_content_sha256 = digest_json(source_inventory)
    alias_inputs_sha256 = digest_json(
        {
            "source_content_sha256": source_content_sha256,
            "state": state_signature,
            "graph": graph_signature,
        }
    )
    source_fingerprint = digest_json(
        {
            "snapshot_version": SOURCE_SNAPSHOT_VERSION,
            "source_membership_sha256": source_membership_sha256,
            "source_content_sha256": source_content_sha256,
            "state": state_signature,
            "graph": graph_signature,
            "alias_inputs_sha256": alias_inputs_sha256,
            "taxonomy_input": taxonomy_input,
            "bundle_catalog_sha256": bundle_catalog_sha256,
        }
    )
    return {
        "source_membership_sha256": source_membership_sha256,
        "source_content_sha256": source_content_sha256,
        "alias_inputs_sha256": alias_inputs_sha256,
        "taxonomy_input": taxonomy_input,
        "bundle_catalog_sha256": bundle_catalog_sha256,
        "source_fingerprint": source_fingerprint,
        "source_count": len(source_records),
        "skills_db_source_count": sum(item["base"] == "skills-db" for item in source_records),
        "state": state_signature,
        "graph": graph_signature,
        "root_presence": root_presence,
    }


def alias_priority(row: dict) -> tuple[int, int, int, str]:
    lifecycle_rank = LIFECYCLE_ORDER.get(row.get("lifecycle") or "catalog", 99)
    base_rank = 0 if row["base"] == "skills" else 1
    return (lifecycle_rank, base_rank, row.get("depth", 99), row["path_key"])


def build_alias_map(rows: list[dict]) -> dict[str, list[dict]]:
    mapping: defaultdict[str, list[dict]] = defaultdict(list)
    for row in rows:
        aliases = {
            row["slug"],
            normalize_name(row["name"]),
            normalize_name(row["folder"]),
            normalize_name(row["rel_dir"]),
            normalize_name(row["path_key"]),
            normalize_name(row.get("occurrence_key", "")),
            normalize_name(row.get("legacy_path_key", "")),
        }
        aliases.update(normalize_name(item) for item in row.get("aliases", []))
        aliases.update(normalize_name(item) for item in row.get("triggers", []))
        for alias in sorted(alias for alias in aliases if alias):
            mapping[alias].append(row)
    return mapping


def resolve_alias(alias_map: dict[str, list[dict]], key: str) -> str | None:
    normalized = normalize_name(key)
    candidates = alias_map.get(normalized)
    if not candidates:
        return None
    return sorted(candidates, key=alias_priority)[0]["path_key"]


def parse_usage_markers(text: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for match in LOADED_SKILL_RE.findall(text):
        counts[normalize_name(match)] += 1
    for match in SKILL_URI_RE.findall(text):
        counts[normalize_name(match.split("/")[-1])] += 1
    for rel in ACTIVE_SKILL_PATH_RE.findall(text):
        counts[normalize_name(f"skills/{rel}" if not rel.startswith("skills/") else rel)] += 1
    for rel in CATALOG_SKILL_PATH_RE.findall(text):
        counts[normalize_name(f"skills-db/{rel}" if not rel.startswith("skills-db/") else rel)] += 1
    for rel in REPO_SKILL_PATH_RE.findall(text):
        counts[normalize_name(f"_repos/{rel}" if not rel.startswith("_repos/") else rel)] += 1
    for line in text.splitlines():
        if "Using skills:" not in line:
            continue
        tail = line.split("Using skills:", 1)[1]
        for raw in re.split(r"[\s,]+", tail):
            token = raw.strip("`*.,;:()[]{}")
            if not token:
                continue
            if token.lower() in {"and", "or", "using", "skills"}:
                continue
            counts[normalize_name(token.split("/")[-1])] += 1
    return counts


def usage_tier(count: int) -> str:
    if count >= 10:
        return "hot"
    if count >= 3:
        return "warm"
    if count >= 1:
        return "cold"
    return "none"


def ensure_complete_yaml_parser() -> None:
    if yaml is not None:
        return
    candidate = Path("/usr/bin/python3")
    try:
        candidate_exists = candidate.is_file()
        same_interpreter = Path(sys.executable).resolve() == candidate.resolve()
    except OSError:
        candidate_exists = False
        same_interpreter = False
    if candidate_exists and not same_interpreter:
        argv = [str(candidate), str(Path(__file__).resolve()), *sys.argv[1:]]
        try:
            os.execve(str(candidate), argv, os.environ.copy())
        except OSError as error:
            raise RuntimeError(
                f"complete YAML parser unavailable; explicit rebuild failed before writes: {error}"
            ) from error
    raise RuntimeError(
        "complete YAML parser unavailable; explicit rebuild failed before writes"
    )


def preflight_inventory_inputs(
    *, require_graph: bool = True, include_bytes: bool = False
) -> tuple[dict, dict, dict | None, dict, dict[str, bool], list[dict], dict, list[dict], dict[str, str]]:
    taxonomy_state = load_taxonomy_config()
    ensure_complete_yaml_parser()
    state_db, state_signature = read_state_input()
    graph_data: dict | None = None
    graph_signature = {"status": "deferred"}
    if require_graph:
        graph_data, graph_signature = read_graph_input()
    root_presence, source_records = scan_source_inputs(include_bytes=include_bytes)
    bundle_catalog, bundle_assignments = build_bundle_catalog(source_records)
    return (
        state_db,
        state_signature,
        graph_data,
        graph_signature,
        root_presence,
        source_records,
        taxonomy_state,
        bundle_catalog,
        bundle_assignments,
    )


def previous_usage_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    try:
        raw = SKILLS_INVENTORY_FILE.read_bytes()
    except OSError:
        return counts
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return counts
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            return {}
        if not isinstance(row, dict):
            return {}
        path_key = row.get("path_key")
        count = row.get("usage_count")
        if (
            isinstance(path_key, str)
            and isinstance(count, int)
            and not isinstance(count, bool)
            and count >= 0
        ):
            counts[path_key] = count
        occurrence_key = row.get("occurrence_key")
        if isinstance(occurrence_key, str) and isinstance(count, int) and not isinstance(count, bool) and count >= 0:
            counts[occurrence_key] = count
    return counts


def alias_projection_digest(rows: list[dict]) -> str:
    aliases = []
    for row in sorted(rows, key=lambda item: item.get("occurrence_key", "")):
        aliases.append(
            {
                "occurrence_key": row.get("occurrence_key"),
                "path_key": row.get("path_key"),
                "name": row.get("name"),
                "slug": row.get("slug"),
                "aliases": row.get("aliases", []),
                "triggers": row.get("triggers", []),
            }
        )
    return digest_json(aliases)


def atomic_write(path: Path, payload: bytes) -> None:
    temporary_path = None
    try:
        fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temporary_path = Path(temporary_name)
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except OSError:
                pass


def read_inventory_rows() -> tuple[list[dict], bytes]:
    try:
        inventory_bytes = SKILLS_INVENTORY_FILE.read_bytes()
    except FileNotFoundError as error:
        raise RuntimeError("skills inventory is missing; requires rebuild with inventory --rebuild") from error
    except OSError as error:
        raise RuntimeError(f"skills inventory is unreadable: {error}") from error
    try:
        text = inventory_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise RuntimeError(f"skills inventory is not valid UTF-8: {error}") from error

    rows = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise RuntimeError(f"skills inventory row {line_number} is invalid JSON: {error}") from error
        if not isinstance(row, dict):
            raise RuntimeError(f"skills inventory row {line_number} must be a JSON object")
        rows.append(row)
    return rows, inventory_bytes


def read_validated_inventory() -> tuple[list[dict], dict]:
    taxonomy_state = load_taxonomy_config()
    try:
        snapshot_bytes = SKILLS_INVENTORY_SNAPSHOT_FILE.read_bytes()
    except FileNotFoundError as error:
        raise RuntimeError(
            "skills inventory snapshot is missing or legacy-unverifiable; requires rebuild with inventory --rebuild"
        ) from error
    except OSError as error:
        raise RuntimeError(f"skills inventory snapshot is unreadable; run inventory --rebuild: {error}") from error
    try:
        snapshot = json.loads(snapshot_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(
            f"skills inventory snapshot is corrupt; run inventory --rebuild: {error}"
        ) from error
    if not isinstance(snapshot, dict) or snapshot.get("snapshot_version") != SOURCE_SNAPSHOT_VERSION:
        raise RuntimeError(
            "skills inventory snapshot is legacy-unverifiable; run inventory --rebuild"
        )
    snapshot_digest = snapshot.get("snapshot_digest")
    snapshot_payload = {key: value for key, value in snapshot.items() if key != "snapshot_digest"}
    try:
        calculated_snapshot_digest = digest_json(snapshot_payload)
    except (TypeError, ValueError) as error:
        raise RuntimeError(
            f"skills inventory snapshot fields are corrupt; run inventory --rebuild: {error}"
        ) from error
    if snapshot_digest != calculated_snapshot_digest:
        raise RuntimeError("skills inventory snapshot checksum is corrupt; run inventory --rebuild")

    state_db, state_signature = read_state_input()
    graph_data, graph_signature = read_graph_input()
    root_presence, source_records = scan_source_inputs()
    bundle_catalog, bundle_assignments = build_bundle_catalog(source_records)
    bundle_catalog_sha256 = digest_json(bundle_catalog)
    taxonomy_input = taxonomy_signature(taxonomy_state)
    current_inputs = input_fingerprints(
        root_presence,
        source_records,
        state_signature,
        graph_signature,
        taxonomy_input,
        bundle_catalog_sha256,
    )
    recorded_source_fingerprint = digest_json(
        {
            "snapshot_version": SOURCE_SNAPSHOT_VERSION,
            "source_membership_sha256": snapshot.get("source_membership_sha256"),
            "source_content_sha256": snapshot.get("source_content_sha256"),
            "state": snapshot.get("state_input"),
            "graph": snapshot.get("graph_input"),
            "alias_inputs_sha256": snapshot.get("alias_inputs_sha256"),
            "taxonomy_input": snapshot.get("taxonomy_input"),
            "bundle_catalog_sha256": snapshot.get("bundle_catalog_sha256"),
        }
    )
    if snapshot.get("source_fingerprint") != recorded_source_fingerprint:
        raise RuntimeError("skills inventory snapshot inputs are corrupt; run inventory --rebuild")
    if snapshot.get("source_fingerprint") != current_inputs["source_fingerprint"]:
        raise RuntimeError(
            "skills inventory is stale: source membership/content, state, graph, taxonomy, bundle, or alias inputs changed; "
            "run inventory --rebuild"
        )
    if (
        snapshot.get("bundle_catalog_sha256") != bundle_catalog_sha256
        or snapshot.get("bundle_catalog") != bundle_catalog
    ):
        raise RuntimeError("skills inventory bundle catalog is stale; run inventory --rebuild")

    rows, inventory_bytes = read_inventory_rows()
    if hashlib.sha256(inventory_bytes).hexdigest() != snapshot.get("inventory_sha256"):
        raise RuntimeError("skills inventory snapshot does not match inventory bytes; run inventory --rebuild")
    source_by_key = {item["occurrence_key"]: item for item in source_records}
    row_keys = [row.get("occurrence_key") for row in rows]
    if any(not isinstance(key, str) for key in row_keys) or len(row_keys) != len(set(row_keys)):
        raise RuntimeError("skills inventory snapshot has missing or duplicate source occurrence keys; run inventory --rebuild")
    if set(row_keys) != set(source_by_key):
        raise RuntimeError("skills inventory source accounting is stale; run inventory --rebuild")
    bundle_by_id = {item["bundle_id"]: item for item in bundle_catalog}
    seen_source_ids = set()
    for row in rows:
        source_record = source_by_key[row["occurrence_key"]]
        source = row.get("source")
        expected_source_id = source_id_for(source_record["base"], source_record["relative_path"])
        bundle_id = bundle_assignments.get(expected_source_id)
        bundle = bundle_by_id.get(bundle_id)
        if (
            not isinstance(source, dict)
            or row.get("base") != source_record["base"]
            or source.get("relative_path") != source_record["relative_path"]
            or source.get("sha256") != source_record["sha256"]
            or source.get("bytes") != source_record["bytes"]
            or source.get("real_path") != str(source_record["path"].resolve())
            or row.get("source_id") != expected_source_id
            or expected_source_id in seen_source_ids
            or row.get("digest") != source_record["sha256"]
            or row.get("content_revision") != source_record["sha256"]
            or not bundle
            or row.get("bundle_id") != bundle_id
            or row.get("bundle_revision") != bundle["sha256"]
            or row.get("bundle_scope") != bundle["scope"]
            or row.get("bundle_boundary_status") != bundle["boundary_status"]
        ):
            raise RuntimeError("skills inventory identity, digest, or bundle projection is stale; run inventory --rebuild")
        seen_source_ids.add(expected_source_id)

    expected_relationships = project_relationships(rows)
    for row in rows:
        if row.get("relationship_declarations") != expected_relationships.get(row["source_id"], []):
            raise RuntimeError("skills inventory relationship projection is corrupt; run inventory --rebuild")
        if row.get("taxonomy") != project_taxonomy_row(row, taxonomy_state):
            raise RuntimeError("skills inventory taxonomy projection is corrupt; run inventory --rebuild")
    if snapshot.get("taxonomy") != build_taxonomy_catalog(rows, taxonomy_state):
        raise RuntimeError("skills inventory taxonomy catalog is corrupt; run inventory --rebuild")

    alias_digest = alias_projection_digest(rows)
    if alias_digest != snapshot.get("alias_projection_sha256"):
        raise RuntimeError("skills inventory alias projection is corrupt; run inventory --rebuild")
    expected_revision = digest_json(
        {
            "source_fingerprint": current_inputs["source_fingerprint"],
            "inventory_sha256": snapshot["inventory_sha256"],
            "alias_projection_sha256": alias_digest,
            "yaml_parser": snapshot.get("yaml_parser"),
            "bundle_catalog_sha256": bundle_catalog_sha256,
            "taxonomy_input": taxonomy_input,
        }
    )
    if snapshot.get("revision") != expected_revision:
        raise RuntimeError("skills inventory snapshot revision is invalid; run inventory --rebuild")
    if snapshot.get("source_count") != len(rows):
        raise RuntimeError("skills inventory snapshot source count is invalid; run inventory --rebuild")
    if snapshot.get("skills_db_source_count") != current_inputs["skills_db_source_count"]:
        raise RuntimeError("skills inventory snapshot corpus count is invalid; run inventory --rebuild")

    global CURRENT_INVENTORY_REVISION
    CURRENT_INVENTORY_REVISION = expected_revision
    return rows, snapshot


def rebuild_inventory() -> tuple[list[dict], dict]:
    (
        state_db,
        state_signature,
        graph_data,
        graph_signature,
        root_presence,
        source_records,
        taxonomy_state,
        bundle_catalog,
        bundle_assignments,
    ) = preflight_inventory_inputs(include_bytes=True)
    if graph_data is None:
        raise RuntimeError("skill graph preflight did not produce input data")
    bundle_catalog_sha256 = digest_json(bundle_catalog)
    taxonomy_input = taxonomy_signature(taxonomy_state)
    current_inputs = input_fingerprints(
        root_presence,
        source_records,
        state_signature,
        graph_signature,
        taxonomy_input,
        bundle_catalog_sha256,
    )
    bundle_by_id = {item["bundle_id"]: item for item in bundle_catalog}
    previous_counts = previous_usage_counts()
    entrypoint_paths = {
        (record["base"], tuple(record["rel_parts"][:-1])): record["path"]
        for record in source_records
        if record["path"].name.casefold() == "skill.md"
    }
    descendants: Counter[tuple[str, tuple[str, ...]]] = Counter()
    for base_label, parts in entrypoint_paths:
        for length in range(1, len(parts)):
            ancestor = (base_label, tuple(parts[:length]))
            if ancestor in entrypoint_paths:
                descendants[ancestor] += 1

    graph_nodes = graph_nodes_from_data(graph_data)
    overrides = state_db.get("skills", {})
    enriched: list[dict] = []
    for record in source_records:
        row = build_source_row(
            record["base"],
            record["root"],
            record["path"],
            tuple(record["rel_parts"]),
            record["data"],
            descendants,
            entrypoint_paths,
        )
        bundle_id = bundle_assignments[row["source_id"]]
        bundle = bundle_by_id[bundle_id]
        row.update(
            {
                "bundle_id": bundle_id,
                "bundle_revision": bundle["sha256"],
                "bundle_scope": bundle["scope"],
                "bundle_boundary_status": bundle["boundary_status"],
            }
        )
        graph_entry = graph_entry_for(row, graph_nodes) if row["doc_type"] == "skill" else None
        graph_id = str(graph_entry.get("id") or "") if graph_entry else ""
        graph_lane = str(graph_entry.get("lane") or "") if graph_entry else ""
        graph_lifecycle = str(graph_entry.get("lifecycle") or "") if graph_entry else ""
        graph_source = str(graph_entry.get("source_project") or "") if graph_entry else ""
        graph_tags = coerce_list(graph_entry.get("tags")) if graph_entry else []
        graph_neighbors = coerce_list(graph_entry.get("_neighbors")) if graph_entry else []
        graph_degree = int(graph_entry.get("_degree") or 0) if graph_entry else 0
        lifecycle, rotation_role = default_lifecycle_for(row)
        override = overrides.get(row["occurrence_key"])
        if not isinstance(override, dict):
            override = overrides.get(row["path_key"])
        if not isinstance(override, dict) and row.get("legacy_path_key"):
            override = overrides.get(row["legacy_path_key"])
        if not isinstance(override, dict):
            override = {}
        lifecycle = override.get("lifecycle", lifecycle)
        rotation_role = override.get("rotation_role", rotation_role)
        if not isinstance(lifecycle, str) or not lifecycle:
            raise RuntimeError(f"invalid lifecycle override for {row['path_key']}")
        if not isinstance(rotation_role, str) or not rotation_role:
            raise RuntimeError(f"invalid rotation_role override for {row['path_key']}")
        rotation_weight_value = override.get("rotation_weight", 1.0)
        if (
            not isinstance(rotation_weight_value, (int, float))
            or isinstance(rotation_weight_value, bool)
        ):
            raise RuntimeError(f"invalid rotation_weight override for {row['path_key']}")
        try:
            rotation_weight = float(rotation_weight_value)
        except (OverflowError, ValueError) as error:
            raise RuntimeError(f"invalid rotation_weight override for {row['path_key']}") from error
        if not math.isfinite(rotation_weight):
            raise RuntimeError(f"invalid rotation_weight override for {row['path_key']}")
        merged_tags = set(row.get("tags", [])) | set(row.get("triggers", [])) | set(row.get("aliases", []))
        merged_tags |= set(token for token in row["path_tokens"] if token)
        merged_tags |= set(token for token in row["category_tokens"] if token)
        merged_tags |= set(graph_tags)
        merged_tags |= set(tokenize(graph_lane))
        merged_tags |= set(tokenize(graph_source))
        merged_tags |= set(metadata_list(override.get("intent_tags"), "intent_tags", row["diagnostics"]))
        prior_count = previous_counts.get(row["path_key"], previous_counts.get(row["occurrence_key"], 0))
        count_value = override.get("usage_count", prior_count)
        if not isinstance(count_value, int) or isinstance(count_value, bool) or count_value < 0:
            raise RuntimeError(f"invalid usage_count override for {row['path_key']}")
        search_blob = " ".join(
            [
                row["name"],
                row["folder"],
                row["description"],
                row["category"],
                graph_lane,
                graph_source,
                " ".join(graph_tags),
                " ".join(graph_neighbors),
                " ".join(sorted(merged_tags)),
                row["rel_dir"],
            ]
        )
        graph_tokens = sorted(
            set(tokenize(" ".join([graph_id, graph_lane, graph_source, *graph_tags, *graph_neighbors])))
        )
        enriched.append(
            {
                **row,
                "lifecycle": lifecycle,
                "rotation_role": rotation_role,
                "usage_count": count_value,
                "usage_tier": usage_tier(count_value),
                "intent_tags": sorted(tag for tag in merged_tags if tag),
                "search_blob": normalize_name(search_blob).replace("-", " "),
                "skill_uri": f"skill://{graph_id or row['slug']}",
                "graph_id": graph_id,
                "lane": graph_lane,
                "graph_lifecycle": graph_lifecycle,
                "graph_source_project": graph_source,
                "graph_tags": graph_tags,
                "graph_degree": graph_degree,
                "graph_neighbors": graph_neighbors[:12],
                "graph_tokens": graph_tokens,
                "rotation_weight": rotation_weight,
                "notes": override.get("notes", ""),
                "anomaly": "nested-under-skill" if row["surface"] == "catalog-nested" and row["parent_skill"] else "",
            }
        )

    relationship_projections = project_relationships(enriched)
    for row in enriched:
        row["relationship_declarations"] = relationship_projections.get(row["source_id"], [])
        row["taxonomy"] = project_taxonomy_row(row, taxonomy_state)

    enriched.sort(key=lambda item: (item["base"], item["path_key"], item["occurrence_key"]))
    inventory_bytes = "".join(
        json.dumps(item, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
        for item in enriched
    ).encode("utf-8")
    inventory_sha256 = hashlib.sha256(inventory_bytes).hexdigest()
    alias_digest = alias_projection_digest(enriched)
    yaml_parser = {
        "name": "PyYAML",
        "version": str(getattr(yaml, "__version__", "unknown")),
    }
    revision = digest_json(
        {
            "source_fingerprint": current_inputs["source_fingerprint"],
            "inventory_sha256": inventory_sha256,
            "alias_projection_sha256": alias_digest,
            "yaml_parser": yaml_parser,
            "bundle_catalog_sha256": bundle_catalog_sha256,
            "taxonomy_input": taxonomy_input,
        }
    )
    snapshot = {
        "snapshot_version": SOURCE_SNAPSHOT_VERSION,
        "source_fingerprint": current_inputs["source_fingerprint"],
        "source_membership_sha256": current_inputs["source_membership_sha256"],
        "source_content_sha256": current_inputs["source_content_sha256"],
        "alias_inputs_sha256": current_inputs["alias_inputs_sha256"],
        "taxonomy_input": taxonomy_input,
        "bundle_catalog_sha256": bundle_catalog_sha256,
        "bundle_catalog": bundle_catalog,
        "taxonomy": build_taxonomy_catalog(enriched, taxonomy_state),
        "state_input": current_inputs["state"],
        "graph_input": current_inputs["graph"],
        "root_presence": current_inputs["root_presence"],
        "source_count": len(enriched),
        "skills_db_source_count": current_inputs["skills_db_source_count"],
        "inventory_sha256": inventory_sha256,
        "alias_projection_sha256": alias_digest,
        "yaml_parser": yaml_parser,
        "revision": revision,
    }
    snapshot["snapshot_digest"] = digest_json(snapshot)
    snapshot_bytes = (
        json.dumps(snapshot, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")

    atomic_write(SKILLS_INVENTORY_FILE, inventory_bytes)
    atomic_write(SKILLS_INVENTORY_SNAPSHOT_FILE, snapshot_bytes)
    global CURRENT_INVENTORY_REVISION
    CURRENT_INVENTORY_REVISION = revision
    return enriched, snapshot


def build_inventory(force_rebuild: bool = False) -> list[dict]:
    if force_rebuild:
        rows, _ = rebuild_inventory()
        return rows
    rows, _ = read_validated_inventory()
    return rows

def has_disposed_ancestor(row: dict) -> bool:
    for key in ("path", "path_key"):
        source_path = str(row.get(key) or "").replace("\\", "/")
        if ".trash" in source_path.split("/"):
            return True
    return False


def filtered_inventory(
    rows: list[dict],
    *,
    category: str | None = None,
    namespace: str | None = None,
    include_hidden: bool = False,
    rotation_roles: set[str] | None = None,
) -> list[dict]:
    output = []
    category_norm = normalize_name(category or "")
    for row in rows:
        if has_disposed_ancestor(row):
            continue
        if namespace is not None and row.get("base") != namespace:
            continue
        if not include_hidden and row["lifecycle"] in {"archived", "backlog", "incubating"}:
            continue
        if category_norm and normalize_name(row["category"]) != category_norm:
            continue
        if rotation_roles is not None and row["rotation_role"] not in rotation_roles:
            continue
        output.append(row)
    return output


def score_row(row: dict, query: str, query_terms: list[str]) -> tuple[float, list[str]]:
    if not query_terms:
        return 0.0, []
    name_tokens = set(row["name_tokens"])
    tag_tokens = set(row["intent_tags"]) | set(row["tag_tokens"])
    desc_tokens = set(row["description_tokens"]) | set(row.get("content_tokens", []))
    category_tokens = set(row["category_tokens"])
    path_tokens = set(row["path_tokens"])
    graph_tokens = set(row.get("graph_tokens", []))
    matched_terms: list[str] = []
    score = 0.0

    for term in query_terms:
        if term in name_tokens:
            score += 14
            matched_terms.append(term)
            continue
        if term in tag_tokens:
            score += 9
            matched_terms.append(term)
            continue
        if term in desc_tokens:
            score += 5
            matched_terms.append(term)
            continue
        if term in category_tokens:
            score += 3
            matched_terms.append(term)
            continue
        if term in path_tokens:
            score += 2
            matched_terms.append(term)
            continue
        if term in graph_tokens:
            score += 2.5
            matched_terms.append(term)
            continue

    if not matched_terms:
        return 0.0, []

    coverage = len(set(matched_terms)) / max(len(set(query_terms)), 1)
    score *= 0.55 + coverage
    if len(set(matched_terms)) == 1 and len(set(query_terms)) >= 3:
        score *= 0.30
    if query and normalize_name(query) == row["slug"]:
        score += 20
    elif normalize_name(query).replace("-", " ") in row["search_blob"]:
        score += 6

    score += min(2.0, math.log10(row["usage_count"] + 1))
    if row["rotation_role"] == "pinned":
        score += 1.5
    if row["lifecycle"] == "core":
        score += 1.0
    if row.get("graph_id"):
        score += min(1.5, math.log2(row.get("graph_degree", 0) + 1) * 0.35)
    if row["surface"] == "catalog-nested":
        score -= 1.5

    return round(score, 4), sorted(set(matched_terms))


def discover_matches(
    query: str,
    *,
    rows: list[dict] | None = None,
    category: str | None = None,
    namespace: str | None = None,
    include_hidden: bool = False,
    rotation_roles: set[str] | None = None,
    limit: int | None = 30,
) -> list[dict]:
    if rows is None:
        rows = build_inventory()
    candidates = filtered_inventory(
        rows,
        category=category,
        namespace=namespace,
        include_hidden=include_hidden,
        rotation_roles=rotation_roles,
    )
    query_terms = tokenize(query)
    matches = []
    for row in candidates:
        if row.get("doc_type") == "asset":
            continue
        score, matched_terms = score_row(row, query, query_terms)
        if score <= 0:
            continue
        matches.append(
            {
                "source_id": row["source_id"],
                "path": row["path"],
                "path_key": row["path_key"],
                "skill_name": row["name"],
                "score": score,
                "adjusted_score": score,
                "category": row["category"],
                "surface": row["surface"],
                "lifecycle": row["lifecycle"],
                "rotation_role": row["rotation_role"],
                "usage_count": row["usage_count"],
                "usage_tier": row["usage_tier"],
                "skill_uri": row["skill_uri"],
                "lane": row["lane"],
                "graph_id": row["graph_id"],
                "graph_degree": row["graph_degree"],
                "intent_tags": row["intent_tags"],
                "matched_terms": matched_terms,
                "local_path": row["path"],
                "doc_type": row.get("doc_type", "skill"),
                "source": "inventory",
                "anomaly": row.get("anomaly", ""),
            }
        )
    matches.sort(key=lambda item: (-item["adjusted_score"], item["skill_name"].lower(), item["path_key"]))
    return matches[:limit] if limit is not None else matches


def discover_payload(query: str, matches: list[dict], category: str | None) -> dict:
    return {
        "query": query,
        "category_filter": [category] if category else [],
        "source_of_truth": str(SKILLS_INVENTORY_FILE),
        "matches": matches,
    }


def print_discover_text(payload: dict) -> int:
    matches = payload.get("matches", [])
    if not matches:
        print("No strong local skill matches found.")
        return 0
    for item in matches[:8]:
        print(
            f"- {item['skill_name']} [{item['category']}/{item['lifecycle']}] "
            f"score={item['adjusted_score']} usage={item['usage_count']} :: {item['local_path']}"
        )
    return 0


def parse_rotation_roles(value: str | None) -> set[str] | None:
    if value is None:
        return None
    value = value.strip().lower()
    if value in {"all", "any", "*"}:
        return {"pinned", "eligible", "experimental", "none"}
    roles = {normalize_name(part) for part in value.split(",") if part.strip()}
    return roles or None


class CliRequestError(ValueError):
    def __init__(self, code: str, message: str, *, extra: dict | None = None):
        super().__init__(message)
        self.code = code
        self.extra = extra or {}


def _parse_cli_integer(value: str, option: str, *, signed: bool = False) -> int:
    pattern = r"-?\d+" if signed else r"\d+"
    if not re.fullmatch(pattern, value):
        raise CliRequestError("invalid_request", f"{option} requires an integer")
    digit_count = len(value[1:] if value.startswith("-") else value)
    if digit_count > MAX_CLI_INTEGER_DIGITS:
        raise CliRequestError("invalid_request", f"{option} exceeds the supported numeric size")
    try:
        return int(value)
    except (ValueError, OverflowError) as error:
        raise CliRequestError("invalid_request", f"{option} requires a supported integer") from error


def emit_cli_error(code: str, message: str, *, json_mode: bool, extra: dict | None = None) -> int:
    if json_mode:
        payload = {
            "schema_version": "lev.skills.error.v1",
            "status": "error",
            "error": {"code": code, "message": message},
            "diagnostics": [message],
            "next_actions": [],
        }
        if extra:
            payload.update(extra)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"error: {message}", file=sys.stderr)
        for alternative in (extra or {}).get("alternatives", []):
            if not isinstance(alternative, dict):
                continue
            print(
                f"- {alternative.get('source_id')} :: {alternative.get('path')} sha256={alternative.get('digest')}",
                file=sys.stderr,
            )
    return 1


def _option_value(args: list[str], index: int, flag: str) -> tuple[str, int]:
    arg = args[index]
    if "=" in arg:
        _, value = arg.split("=", 1)
        next_index = index
    else:
        if index + 1 >= len(args) or args[index + 1].startswith("--"):
            raise CliRequestError("invalid_request", f"{flag} requires a value")
        value = args[index + 1]
        next_index = index + 1
    if value == "":
        raise CliRequestError("invalid_request", f"{flag} requires a non-empty value")
    return value, next_index


def _normalized_query_group(group: dict, index: int, *, max_tokens: int = 32) -> dict:
    query = group["query"]
    tokens = tokenize(query)
    if not tokens:
        raise CliRequestError("invalid_request", "query groups must contain at least one searchable term")
    if len(tokens) > max_tokens:
        raise CliRequestError("invalid_request", f"query groups may contain at most {max_tokens} searchable terms")
    return {
        "id": f"group-{index + 1}",
        "kind": group["kind"],
        "raw": group["raw"],
        "query": query,
        "normalized": normalize_name(query),
        "tokens": tokens,
    }


def parse_discovery_request(args: list[str]) -> dict:
    json_mode = "--json" in args
    query_values: list[str] = []
    positional: list[str] = []
    tags_raw: str | None = None
    category: str | None = None
    namespace: str | None = None
    backend = "lexical"
    limit = 30
    no_cache = False
    seen: set[str] = set()
    i = 0
    while i < len(args):
        arg = args[i]
        flag = arg.split("=", 1)[0] if arg.startswith("--") else ""
        if not flag:
            positional.append(arg)
            i += 1
            continue
        if flag in {"--query", "--tags", "--category", "--namespace", "--limit", "--backend"}:
            if flag != "--query" and flag in seen:
                raise CliRequestError("invalid_request", f"{flag} may be supplied only once")
            value, i = _option_value(args, i, flag)
            if flag == "--query":
                query_values.append(value)
            elif flag == "--tags":
                tags_raw = value
            elif flag == "--category":
                category = value
            elif flag == "--namespace":
                namespace = value
            elif flag == "--backend":
                backend = value.lower()
            else:
                limit = max(1, _parse_cli_integer(value, "--limit", signed=True))
            seen.add(flag)
            i += 1
            continue
        if flag in {"--json", "--no-cache", "--all", "--primary-only"}:
            if "=" in arg:
                raise CliRequestError("invalid_request", f"{flag} does not take a value")
            if flag in seen:
                raise CliRequestError("invalid_request", f"{flag} may be supplied only once")
            seen.add(flag)
            if flag == "--no-cache":
                no_cache = True
            i += 1
            continue
        raise CliRequestError("invalid_request", f"unknown flag: {arg}")

    if namespace is not None and namespace not in {"skills-db", "skills", "_repos"}:
        raise CliRequestError("invalid_request", f"unsupported namespace: {namespace}")
    if backend not in {"lexical", "qmd"}:
        raise CliRequestError("invalid_request", f"unsupported discovery backend: {backend}")
    if backend == "qmd" and namespace not in {None, "skills-db"}:
        raise CliRequestError("unsupported_namespace", "the QMD backend supports only the skills-db namespace")
    if query_values and positional:
        raise CliRequestError("invalid_request", "positional query text cannot be combined with --query")
    if not query_values and positional:
        if len(positional) == 2 and re.fullmatch(r"\d+", positional[1]) and "--limit" not in seen:
            limit = max(1, _parse_cli_integer(positional[1], "positional limit"))
            positional = positional[:1]
        if len(positional) != 1:
            raise CliRequestError("invalid_request", "discovery accepts one quoted positional query")
        query_values = [positional[0]]
    if backend == "qmd" and limit > QMD_CANDIDATE_LIMIT:
        raise CliRequestError(
            "invalid_request",
            f"the QMD backend supports --limit up to {QMD_CANDIDATE_LIMIT}",
        )
    if any(not value.strip() for value in query_values):
        raise CliRequestError("invalid_request", "query values must be non-empty")
    if backend == "qmd" and any(
        len(value.encode("utf-8")) > QMD_MAX_QUERY_BYTES
        for value in [*query_values, *([tags_raw] if tags_raw is not None else [])]
    ):
        raise CliRequestError(
            "invalid_request",
            f"QMD query text may not exceed {QMD_MAX_QUERY_BYTES} UTF-8 bytes per group",
        )

    groups: list[dict] = []
    for value in query_values:
        groups.append({"kind": "query", "raw": value, "query": value})
    normalized_tags: list[str] = []
    if tags_raw is not None:
        parts = tags_raw.split(",")
        if not parts or any(not part.strip() for part in parts):
            raise CliRequestError("invalid_request", "--tags must be a comma-separated list without empty values")
        tag_tokens: list[str] = []
        for part in parts:
            normalized_tag = normalize_name(part)
            tokens = tokenize(part)
            if not normalized_tag or not tokens:
                raise CliRequestError("invalid_request", "each --tags value must contain a searchable term")
            normalized_tags.append(normalized_tag)
            tag_tokens.extend(tokens)
        groups.append(
            {
                "kind": "tags",
                "raw": tags_raw,
                "query": " ".join(tag_tokens),
                "normalized_tags": normalized_tags,
            }
        )
    if not groups:
        raise CliRequestError("invalid_request", "discover requires a query or --tags")
    if len(groups) > 8:
        raise CliRequestError("invalid_request", "discovery accepts at most 8 supplied query or tags groups")
    max_tokens = 256 if backend == "qmd" else 32
    normalized_groups = [
        _normalized_query_group(group, index, max_tokens=max_tokens)
        for index, group in enumerate(groups)
    ]
    return {
        "json": json_mode,
        "groups": normalized_groups,
        "tags_raw": tags_raw,
        "normalized_tags": normalized_tags,
        "category": category,
        "namespace": namespace,
        "backend": backend,
        "limit": limit,
        "no_cache": no_cache,
        "all_collections": True,
    }


def parse_pick_request(args: list[str]) -> dict:
    json_mode = "--json" in args
    positional: list[str] = []
    category: str | None = None
    namespace: str | None = None
    rotation = "eligible,experimental"
    no_cache = False
    seen: set[str] = set()
    i = 0
    while i < len(args):
        arg = args[i]
        flag = arg.split("=", 1)[0] if arg.startswith("--") else ""
        if not flag:
            positional.append(arg)
            i += 1
            continue
        if flag in {"--category", "--namespace", "--rotation"}:
            if flag in seen:
                raise CliRequestError("invalid_request", f"{flag} may be supplied only once")
            value, i = _option_value(args, i, flag)
            if flag == "--category":
                category = value
            elif flag == "--namespace":
                namespace = value
            else:
                rotation = value
            seen.add(flag)
            i += 1
            continue
        if flag in {"--json", "--no-cache"}:
            if "=" in arg or flag in seen:
                raise CliRequestError("invalid_request", f"{flag} is malformed or repeated")
            seen.add(flag)
            no_cache = no_cache or flag == "--no-cache"
            i += 1
            continue
        raise CliRequestError("invalid_request", f"unknown flag: {arg}")
    if len(positional) != 1 or not positional[0].strip():
        raise CliRequestError("invalid_request", "pick requires one quoted query")
    query_tokens = tokenize(positional[0])
    if not query_tokens:
        raise CliRequestError("invalid_request", "pick query must contain a searchable term")
    if len(query_tokens) > 32:
        raise CliRequestError("invalid_request", "pick query may contain at most 32 searchable terms")
    if namespace is not None and namespace not in {"skills-db", "skills", "_repos"}:
        raise CliRequestError("invalid_request", f"unsupported namespace: {namespace}")
    roles = parse_rotation_roles(rotation)
    if roles is None or not roles.issubset({"pinned", "eligible", "experimental", "none"}):
        raise CliRequestError("invalid_request", f"unsupported rotation selector: {rotation}")
    return {
        "json": json_mode,
        "query": positional[0],
        "category": category,
        "namespace": namespace,
        "rotation": rotation,
        "rotation_roles": roles,
        "no_cache": no_cache,
    }


def parse_tree_request(args: list[str]) -> dict:
    json_mode = "--json" in args
    view = "subjects"
    depth = 2
    seen: set[str] = set()
    i = 0
    while i < len(args):
        arg = args[i]
        flag = arg.split("=", 1)[0] if arg.startswith("--") else ""
        if flag in {"--view", "--depth"}:
            if flag in seen:
                raise CliRequestError("invalid_request", f"{flag} may be supplied only once")
            value, i = _option_value(args, i, flag)
            if flag == "--view":
                view = value
            else:
                depth = _parse_cli_integer(value, "--depth", signed=True)
            seen.add(flag)
            i += 1
            continue
        if flag == "--json" and arg == flag and flag not in seen:
            seen.add(flag)
            i += 1
            continue
        if not flag:
            raise CliRequestError("invalid_request", f"unexpected positional argument: {arg}")
        raise CliRequestError("invalid_request", f"unknown flag: {arg}")
    if view not in {"subjects", "collections"}:
        raise CliRequestError("invalid_request", f"unsupported tree view: {view}")
    if depth < 0:
        raise CliRequestError("invalid_request", "tree depth must be greater than or equal to zero")
    return {"json": json_mode, "view": view, "depth": depth}


def parse_browse_request(args: list[str]) -> dict:
    json_mode = "--json" in args
    node_id: str | None = None
    cursor: str | None = None
    limit = 10
    seen: set[str] = set()
    i = 0
    while i < len(args):
        arg = args[i]
        flag = arg.split("=", 1)[0] if arg.startswith("--") else ""
        if flag in {"--node", "--cursor", "--limit"}:
            if flag in seen:
                raise CliRequestError("invalid_request", f"{flag} may be supplied only once")
            value, i = _option_value(args, i, flag)
            if flag == "--node":
                node_id = value
            elif flag == "--cursor":
                cursor = value
            else:
                limit = _parse_cli_integer(value, "browse --limit")
            seen.add(flag)
            i += 1
            continue
        if flag == "--json" and arg == flag and flag not in seen:
            seen.add(flag)
            i += 1
            continue
        if not flag:
            raise CliRequestError("invalid_request", f"unexpected positional argument: {arg}")
        raise CliRequestError("invalid_request", f"unknown flag: {arg}")
    if cursor is not None:
        if node_id is not None or "--limit" in seen:
            raise CliRequestError("invalid_cursor", "a cursor already binds node and limit")
        return {"json": json_mode, "cursor": cursor}
    if node_id is None:
        raise CliRequestError("invalid_request", "browse requires --node or --cursor")
    if limit < 1 or limit > 100:
        raise CliRequestError("invalid_request", "browse limit must be between 1 and 100")
    return {"json": json_mode, "node_id": node_id, "limit": limit}


def parse_get_request(args: list[str]) -> dict:
    json_mode = "--json" in args
    names: list[str] = []
    seen_json = False
    for arg in args:
        if arg == "--json":
            if seen_json:
                raise CliRequestError("invalid_request", "--json may be supplied only once")
            seen_json = True
        elif arg.startswith("--"):
            raise CliRequestError("invalid_request", f"unknown flag: {arg}")
        else:
            names.append(arg)
    if len(names) != 1 or not names[0].strip():
        raise CliRequestError("invalid_request", "get requires one exact source ID or name")
    return {"json": json_mode, "source_key": names[0]}


def _cursor_request_fingerprint(node_id: str, revision: str, limit: int) -> str:
    return digest_json(
        {
            "command": "browse",
            "node_id": node_id,
            "revision": revision,
            "limit": limit,
            "visibility": "all_non_disposed",
            "order": "normalized_name_source_id",
        }
    )


def _make_browse_cursor(node_id: str, revision: str, limit: int, offset: int) -> str:
    payload = {
        "version": 1,
        "command": "browse",
        "revision": revision,
        "node_id": node_id,
        "visibility": "all_non_disposed",
        "order": "normalized_name_source_id",
        "limit": limit,
        "offset": offset,
        "request_fingerprint": _cursor_request_fingerprint(node_id, revision, limit),
    }
    payload["checksum"] = digest_json(payload)
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _decode_browse_cursor(token: str) -> dict:
    if len(token) > 4096 or not re.fullmatch(r"[A-Za-z0-9_-]+", token):
        raise CliRequestError("invalid_cursor", "browse cursor is malformed")
    try:
        raw = base64.urlsafe_b64decode(token + "=" * ((-len(token)) % 4))
        payload = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_json_object,
            parse_constant=_reject_json_constant,
        )
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CliRequestError("invalid_cursor", "browse cursor is malformed") from error
    fields = {
        "version", "command", "revision", "node_id", "visibility", "order", "limit", "offset",
        "request_fingerprint", "checksum",
    }
    if not isinstance(payload, dict) or set(payload) != fields:
        raise CliRequestError("invalid_cursor", "browse cursor fields are invalid")
    checksum = payload.get("checksum")
    unsigned = {key: value for key, value in payload.items() if key != "checksum"}
    try:
        valid_checksum = checksum == digest_json(unsigned)
    except (TypeError, ValueError, RecursionError):
        valid_checksum = False
    if not valid_checksum:
        raise CliRequestError("invalid_cursor", "browse cursor checksum is invalid")
    if (
        payload.get("version") != 1
        or isinstance(payload.get("version"), bool)
        or payload.get("command") != "browse"
        or not isinstance(payload.get("revision"), str)
        or not re.fullmatch(r"[a-f0-9]{64}", payload["revision"])
        or not isinstance(payload.get("node_id"), str)
        or not payload["node_id"]
        or payload.get("visibility") != "all_non_disposed"
        or payload.get("order") != "normalized_name_source_id"
        or not isinstance(payload.get("limit"), int)
        or isinstance(payload.get("limit"), bool)
        or not 1 <= payload["limit"] <= 100
        or not isinstance(payload.get("offset"), int)
        or isinstance(payload.get("offset"), bool)
        or payload["offset"] < 0
        or not isinstance(payload.get("request_fingerprint"), str)
        or payload["request_fingerprint"] != _cursor_request_fingerprint(
            payload["node_id"], payload["revision"], payload["limit"]
        )
    ):
        raise CliRequestError("invalid_cursor", "browse cursor request binding is invalid")
    return payload


def _index_error_code(error: RuntimeError, *, taxonomy_required: bool = False) -> str:
    message = str(error).lower()
    if taxonomy_required and "taxonomy" in message:
        return "taxonomy_unavailable"
    if "stale" in message:
        return "stale_index"
    return "invalid_index"


def _descriptor_indexes(rows: list[dict], snapshot: dict) -> tuple[dict[str, dict], dict[str, dict], dict[str, set[str]]]:
    rows_by_id = {row["source_id"]: row for row in rows if isinstance(row.get("source_id"), str)}
    bundles = {
        bundle["bundle_id"]: bundle
        for bundle in snapshot.get("bundle_catalog", [])
        if isinstance(bundle, dict) and isinstance(bundle.get("bundle_id"), str)
    }
    aliases: defaultdict[str, set[str]] = defaultdict(set)
    for row in rows:
        source_id = row.get("source_id")
        if not isinstance(source_id, str):
            continue
        values = [
            row.get("name"), row.get("slug"), row.get("folder"), row.get("rel_dir"),
            row.get("path_key"), row.get("legacy_path_key"),
        ]
        values.extend(row.get("aliases", []) if isinstance(row.get("aliases"), list) else [])
        values.extend(row.get("triggers", []) if isinstance(row.get("triggers"), list) else [])
        for value in values:
            if isinstance(value, str):
                key = normalize_name(value)
                if key:
                    aliases[key].add(source_id)
    return rows_by_id, bundles, aliases


def _bundle_member_descriptor(row: dict, revision: str) -> dict:
    source = row.get("source") if isinstance(row.get("source"), dict) else {}
    path = row.get("path")
    return {
        "source_id": row["source_id"],
        "source_namespace": row.get("base"),
        "source_collection": source.get("collection"),
        "relative_path": source.get("relative_path"),
        "skill_name": row.get("name"),
        "local_path": path,
        "path": path,
        "realpath": source.get("real_path"),
        "digest": row.get("digest"),
        "content_revision": row.get("content_revision"),
        "index_revision": revision,
        "diagnostics": list(row.get("diagnostics", [])),
    }


def _source_descriptor(
    row: dict,
    *,
    revision: str,
    rows_by_id: dict[str, dict],
    bundles: dict[str, dict],
) -> dict:
    source = row.get("source") if isinstance(row.get("source"), dict) else {}
    source_id = row["source_id"]
    bundle_id = row.get("bundle_id")
    bundle_record = bundles.get(bundle_id)
    if not isinstance(bundle_record, dict) or bundle_record.get("sha256") != row.get("bundle_revision"):
        raise RuntimeError(f"validated bundle descriptor is missing or stale for {source_id}")
    members = []
    for member in bundle_record.get("members", []):
        member_id = member.get("source_id") if isinstance(member, dict) else None
        member_row = rows_by_id.get(member_id) if isinstance(member_id, str) else None
        if member_row is None or member_row.get("digest") != member.get("digest"):
            raise RuntimeError(f"validated bundle member is missing or stale for {source_id}")
        members.append(_bundle_member_descriptor(member_row, revision))
    relationships = row.get("relationship_declarations", [])
    uncertainty = []
    for declaration in relationships if isinstance(relationships, list) else []:
        if not isinstance(declaration, dict):
            continue
        if declaration.get("resolution_status") != "resolved":
            uncertainty.append(
                {
                    "declaration_key": declaration.get("declaration_key"),
                    "resolution_status": declaration.get("resolution_status", "unknown"),
                    "targets": declaration.get("targets", []),
                }
            )
    path = row.get("path")
    descriptor = {
        "source_id": source_id,
        "skill_name": row.get("name"),
        "local_path": path,
        "path": path,
        "realpath": source.get("real_path"),
        "digest": row.get("digest"),
        "content_revision": row.get("content_revision"),
        "index_revision": revision,
        "source_namespace": row.get("base"),
        "source_collection": source.get("collection"),
        "source_scope": {
            "namespace": row.get("base"),
            "collection": source.get("collection"),
            "relative_path": source.get("relative_path"),
            "digest_scope": source.get("digest_scope"),
        },
        "source_record": dict(source),
        "taxonomy": row.get("taxonomy"),
        "metadata": row.get("original_metadata"),
        "structure": row.get("structure"),
        "quality": row.get("quality"),
        "source": "inventory",
        "doc_type": row.get("doc_type", "skill"),
        "lifecycle": row.get("lifecycle"),
        "availability": row.get("quality", {}).get("source_available", source.get("status") == "readable"),
        "metadata_status": row.get("quality", {}).get("metadata_status"),
        "diagnostics": list(row.get("diagnostics", [])),
        "bundle_id": bundle_id,
        "bundle_revision": row.get("bundle_revision"),
        "bundle_scope": row.get("bundle_scope"),
        "bundle_boundary_status": row.get("bundle_boundary_status"),
        "bundle_member_source_ids": [member["source_id"] for member in members],
        "bundle": {
            "bundle_id": bundle_record["bundle_id"],
            "revision": bundle_record["sha256"],
            "scope": bundle_record["scope"],
            "boundary_status": bundle_record["boundary_status"],
            "digest_scope": bundle_record["digest_scope"],
            "entrypoint_source_id": bundle_record.get("entrypoint_source_id"),
            "member_count": bundle_record["member_count"],
            "members": members,
        },
        "relationships": list(relationships) if isinstance(relationships, list) else [],
        "relationship_uncertainty": uncertainty,
        "content_delivery": {"mode": "descriptor_only", "content_loaded": False},
        "anomaly": row.get("anomaly", ""),
    }
    return descriptor


def _with_source_descriptor(
    match: dict,
    *,
    revision: str,
    rows_by_id: dict[str, dict],
    bundles: dict[str, dict],
) -> dict:
    row = rows_by_id.get(match.get("source_id"))
    if row is None:
        raise RuntimeError(f"validated discovery match has no source row: {match.get('source_id')}")
    result = dict(match)
    result.update(_source_descriptor(row, revision=revision, rows_by_id=rows_by_id, bundles=bundles))
    return result


def _predicate_fingerprint(
    group: dict,
    *,
    category: str | None,
    namespace: str | None,
    visibility: str,
    roles: set[str] | None,
    revision: str,
) -> str:
    return digest_json(
        {
            "matcher_version": 1,
            "tokens": sorted(set(group["tokens"])),
            "category": normalize_name(category) if category else None,
            "namespace": namespace,
            "visibility": visibility,
            "roles": sorted(roles) if roles is not None else None,
            "revision": revision,
        }
    )


def _ranking_request_fingerprint(
    group: dict,
    *,
    category: str | None,
    namespace: str | None,
    visibility: str,
    roles: set[str] | None,
    revision: str,
    limit: int,
) -> str:
    return digest_json(
        {
            "normalized_phrase": group["normalized"],
            "ordered_tokens": group["tokens"],
            "matcher_version": 1,
            "category": normalize_name(category) if category else None,
            "namespace": namespace,
            "visibility": visibility,
            "roles": sorted(roles) if roles is not None else None,
            "revision": revision,
            "limit": limit,
            "order": "score_desc_name_asc_path_key_asc",
        }
    )


def _navigation_rows(rows: list[dict], taxonomy: dict) -> tuple[dict[str, dict], dict[str, list[dict]]]:
    nodes = [node for node in taxonomy.get("nodes", []) if isinstance(node, dict) and isinstance(node.get("id"), str)]
    node_by_id = {node["id"]: node for node in nodes}
    node_rows: defaultdict[str, list[dict]] = defaultdict(list)
    memberships: defaultdict[str, set[str]] = defaultdict(set)
    for row in rows:
        if has_disposed_ancestor(row):
            continue
        source = row.get("source") if isinstance(row.get("source"), dict) else {}
        for membership in row.get("taxonomy", {}).get("memberships", []):
            node_id = membership.get("node_id") if isinstance(membership, dict) else None
            if isinstance(node_id, str):
                memberships[node_id].add(row["source_id"])
        for node in nodes:
            kind = node.get("view_kind")
            include = False
            if kind == "source_namespace":
                include = row.get("base") == node.get("label")
            elif kind == "source_collection":
                parent = node_by_id.get(node.get("parent_id"), {})
                include = row.get("base") == parent.get("label") and source.get("collection") == node.get("label")
            elif node["id"] in memberships and row["source_id"] in memberships[node["id"]]:
                include = True
            if include:
                node_rows[node["id"]].append(row)
    for node_id, values in node_rows.items():
        values.sort(key=lambda row: (normalize_name(str(row.get("name", ""))), row["source_id"]))
    return node_by_id, dict(node_rows)


def _breadcrumbs(node_id: str, node_by_id: dict[str, dict]) -> list[dict]:
    chain = []
    seen = set()
    current = node_by_id.get(node_id)
    while current is not None:
        key = current.get("id")
        if not isinstance(key, str) or key in seen:
            raise RuntimeError(f"taxonomy breadcrumb parent chain is invalid at {node_id}")
        seen.add(key)
        chain.append({"id": key, "label": current.get("label", key)})
        parent_id = current.get("parent_id")
        current = node_by_id.get(parent_id) if isinstance(parent_id, str) else None
        if parent_id is not None and current is None:
            raise RuntimeError(f"taxonomy breadcrumb parent is missing for {key}")
    return list(reversed(chain))


def _tree_node(
    node: dict,
    *,
    node_by_id: dict[str, dict],
    node_rows: dict[str, list[dict]],
    projected_counts: dict,
    children_by_parent: dict[str | None, list[dict]],
    depth: int,
    level: int,
) -> dict:
    node_id = node["id"]
    value = {
        key: item for key, item in node.items()
        if key not in {"path", "local_path", "realpath"}
    }
    value["breadcrumbs"] = _breadcrumbs(node_id, node_by_id)
    value["projected_resource_count"] = projected_counts.get(node_id)
    value["eligible_count"] = len(node_rows.get(node_id, []))
    value["eligible_resource_count"] = value["eligible_count"]
    value["children"] = []
    if level < depth:
        value["children"] = [
            _tree_node(
                child,
                node_by_id=node_by_id,
                node_rows=node_rows,
                projected_counts=projected_counts,
                children_by_parent=children_by_parent,
                depth=depth,
                level=level + 1,
            )
            for child in children_by_parent.get(node_id, [])
        ]
    return value


def qmd_config_path() -> Path:
    if os.environ.get("QMD_CONFIG_DIR"):
        directory = Path(os.environ["QMD_CONFIG_DIR"]).expanduser()
    elif os.environ.get("XDG_CONFIG_HOME"):
        directory = Path(os.environ["XDG_CONFIG_HOME"]).expanduser() / "qmd"
    else:
        directory = Path.home() / ".config" / "qmd"
    return directory / "index.yml"


def qmd_database_path() -> Path:
    if os.environ.get("INDEX_PATH"):
        return Path(os.environ["INDEX_PATH"]).expanduser().resolve()
    cache_root = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")).expanduser()
    return (cache_root / "qmd" / "index.sqlite").resolve()


def approved_qmd_collection_paths() -> dict[str, Path]:
    return {
        "skills-db": SKILLS_DB_DIR,
        "skills-db-bundle-docs": SKILLS_DB_DIR / "creative/roundtable-marvkr--better-design/source/.agents/skills",
        "skills-db-archive": SKILLS_DB_DIR / ".archive",
        "skills-db-backlog": SKILLS_DB_DIR / "_todo",
        "skills-db-workshop": SKILLS_DB_DIR / "_workshop",
    }


def preflight_qmd(*, refresh: bool = False) -> tuple[Path, dict, dict[str, Path], str]:
    config_path = qmd_config_path()
    package_root = qmd_package_root()
    node = qmd_node_executable()
    bridge = ROOT / "lev-skills-qmd.mjs"
    if not bridge.is_file():
        raise QmdBackendError(f"QMD SDK bridge is missing: {bridge}")
    inspect_request = {"operation": "inspect", "configPath": str(config_path)}
    try:
        inspect_result = run_bounded_process(
            [node, str(bridge), json.dumps(inspect_request, separators=(",", ":"))],
            cwd=ROOT,
            timeout=10,
            max_output_bytes=1024 * 1024,
        )
    except (OSError, QmdBackendError) as error:
        raise QmdBackendError(f"cannot inspect QMD configuration: {error}") from error
    inspected = parse_qmd_json(inspect_result.stdout)
    if inspect_result.returncode != 0:
        detail = inspected.get("error") if isinstance(inspected, dict) else None
        raise QmdBackendError(detail if isinstance(detail, str) else "QMD configuration inspection failed")
    if not isinstance(inspected, dict) or inspected.get("status") != "inspected":
        raise QmdBackendError("QMD configuration inspection returned an invalid response")
    config = {
        "collections": inspected.get("collections"),
    }
    if not isinstance(config, dict) or not isinstance(config.get("collections"), dict):
        raise QmdBackendError("QMD configuration must declare its existing collections")

    expected_paths = approved_qmd_collection_paths()
    roots = {}
    for name in QMD_REFRESH_COLLECTIONS:
        collection = config["collections"].get(name)
        if not isinstance(collection, dict):
            raise QmdBackendError(f"approved QMD collection is missing: {name}")
        configured_path = collection.get("path")
        if not isinstance(configured_path, str) or not configured_path:
            raise QmdBackendError(f"QMD collection {name} has no source path")
        try:
            actual_path = Path(configured_path).expanduser().resolve(strict=True)
            expected_path = expected_paths[name].resolve(strict=True)
        except OSError as error:
            raise QmdBackendError(f"QMD collection {name} has an unavailable source path: {error}") from error
        if actual_path != expected_path or not actual_path.is_dir():
            raise QmdBackendError(f"QMD collection {name} is outside its approved skills-db source root")
        if collection.get("pattern") != "**/*.md":
            raise QmdBackendError(f"QMD collection {name} must use the approved Markdown pattern")
        roots[name] = actual_path

    embed_model = inspected.get("embedModel")
    if not isinstance(embed_model, str) or not embed_model:
        raise QmdBackendError("QMD embedding model is not configured")
    resolved_model_path = inspected.get("embedModelPath")
    if not isinstance(resolved_model_path, str) or not resolved_model_path:
        raise QmdBackendError(f"configured QMD embedding model is not cached: {embed_model}; no download was attempted")
    model_path = Path(resolved_model_path).expanduser()
    try:
        with model_path.open("rb") as handle:
            if model_path.stat().st_size <= 4 or handle.read(4) != b"GGUF":
                raise QmdBackendError(f"configured QMD embedding model is not a valid GGUF file: {model_path}")
    except OSError as error:
        raise QmdBackendError(f"configured QMD embedding model is unavailable: {model_path}: {error}") from error
    return config_path, config, roots, embed_model


def _qmd_expected_manifest(records: list[dict], roots: dict[str, Path]) -> list[dict]:
    """Map current canonical Markdown occurrences to their exact QMD collection paths."""
    output = []
    seen_ids = set()
    seen_paths = set()
    corpus_root = roots.get("skills-db")
    if corpus_root is None:
        raise QmdBackendError("approved QMD integrity scope is missing the skills-db root")
    special_roots = (
        "skills-db-bundle-docs",
        "skills-db-archive",
        "skills-db-backlog",
        "skills-db-workshop",
    )
    for record in records:
        if not isinstance(record, dict) or record.get("base") != "skills-db":
            continue
        source = record.get("source") if isinstance(record.get("source"), dict) else None
        relative_path = source.get("relative_path") if source is not None else record.get("relative_path")
        path_value = record.get("path")
        source_digest = (source.get("sha256") if source is not None else record.get("sha256")) or record.get("digest")
        if not isinstance(relative_path, str) or not relative_path.lower().endswith(".md"):
            continue
        relative_parts = relative_path.split("/")
        if any(part in {"", ".", ".."} for part in relative_parts):
            raise QmdBackendError(f"canonical Markdown path is not normalized: {relative_path}")
        if ".trash" in relative_parts:
            continue
        if not isinstance(path_value, (str, Path)):
            raise QmdBackendError(f"canonical Markdown source has no file path: {relative_path}")
        try:
            file_path = Path(path_value).resolve(strict=True)
        except OSError as error:
            raise QmdBackendError(f"canonical Markdown source is unavailable: {relative_path}: {error}") from error
        if not file_path.is_file() or file_path.suffix.lower() != ".md":
            raise QmdBackendError(f"canonical Markdown source is not a Markdown file: {relative_path}")
        if not isinstance(source_digest, str) or not re.fullmatch(r"[a-f0-9]{64}", source_digest):
            raise QmdBackendError(f"canonical Markdown source has no valid raw-byte digest: {relative_path}")
        try:
            source_relative = file_path.relative_to(corpus_root).as_posix()
        except ValueError as error:
            raise QmdBackendError(f"canonical Markdown source is outside skills-db: {relative_path}") from error
        if source_relative != relative_path:
            raise QmdBackendError(f"canonical Markdown source path changed: {relative_path}")

        collection_name = "skills-db"
        collection_path = None
        for special_name in special_roots:
            special_root = roots.get(special_name)
            if special_root is None:
                continue
            try:
                collection_path = file_path.relative_to(special_root).as_posix()
            except ValueError:
                continue
            collection_name = special_name
            break
        if collection_path is None:
            try:
                collection_path = file_path.relative_to(corpus_root).as_posix()
            except ValueError as error:
                raise QmdBackendError(f"canonical Markdown source has no approved QMD collection: {relative_path}") from error
        if collection_path in {"", "."} or any(part in {"", ".", ".."} for part in collection_path.split("/")):
            raise QmdBackendError(f"canonical QMD collection path is not normalized: {collection_path}")

        source_id = record.get("source_id") or record.get("occurrence_key") or f"skills-db/{relative_path}"
        if source_id != f"skills-db/{relative_path}" or source_id in seen_ids:
            raise QmdBackendError(f"canonical source identity is missing or duplicated: {source_id}")
        key = (collection_name, collection_path)
        if key in seen_paths:
            raise QmdBackendError(f"canonical QMD occurrence is duplicated: {collection_name}/{collection_path}")
        seen_ids.add(source_id)
        seen_paths.add(key)
        output.append({
            "source_id": source_id,
            "source_relative_path": relative_path,
            "file_path": str(file_path),
            "source_sha256": source_digest,
            "collection": collection_name,
            "path": collection_path,
        })
    output.sort(key=lambda item: (item["collection"], item["path"], item["source_id"]))
    return output


def qmd_index_integrity_guard(
    *,
    config_path: Path,
    roots: dict[str, Path],
    model: str,
    records: list[dict],
) -> dict:
    db_path = qmd_database_path()
    if not db_path.is_file():
        raise QmdBackendError(f"QMD index is unavailable: {db_path}")
    manifest = _qmd_expected_manifest(records, roots)
    request = {
        "operation": "integrity",
        "dbPath": str(db_path),
        "configPath": str(config_path),
        "collections": list(QMD_REFRESH_COLLECTIONS),
        "roots": {name: str(roots[name]) for name in QMD_REFRESH_COLLECTIONS},
        "model": model,
        "expectedDocuments": len(manifest),
    }
    node = qmd_node_executable()
    bridge = ROOT / "lev-skills-qmd.mjs"
    try:
        result = run_bounded_process(
            [node, str(bridge), json.dumps(request, separators=(",", ":"))],
            cwd=ROOT,
            timeout=QMD_INTEGRITY_TIMEOUT_SECONDS,
            max_output_bytes=1024 * 1024,
            max_input_bytes=QMD_MAX_MANIFEST_BYTES,
            input_text=json.dumps({"documents": manifest}, separators=(",", ":")),
        )
    except (OSError, QmdBackendError) as error:
        raise QmdBackendError(f"QMD index integrity check failed: {error}") from error
    response = parse_qmd_json(result.stdout)
    if not isinstance(response, dict):
        raise QmdBackendError("QMD index integrity check returned malformed JSON")
    if result.returncode != 0 or response.get("status") != "integrity_checked":
        detail = response.get("error") if isinstance(response.get("error"), str) else "invalid integrity response"
        code = response.get("code") if isinstance(response.get("code"), str) else "qmd_index_integrity"
        raise QmdBackendError(f"{code}: {detail}")
    if (
        response.get("expectedDocuments") != len(manifest)
        or response.get("actualDocuments") != len(manifest)
        or response.get("missingPaths") != 0
        or response.get("extraPaths") != 0
        or response.get("staleBodies") != 0
        or response.get("pendingEmbeddingHashes") != 0
        or response.get("missingVectorIds") != 0
        or response.get("model") != model
        or not isinstance(response.get("fingerprint"), str)
        or not re.fullmatch(r"[a-f0-9]{6,64}", response["fingerprint"])
    ):
        raise QmdBackendError("qmd_index_integrity: QMD index does not cover the current canonical manifest")
    return response


def qmd_node_executable() -> str:
    candidates = []
    diagnostics = []
    if os.environ.get("QMD_NODE"):
        candidates.append(os.environ["QMD_NODE"])
    candidates.extend(("/opt/homebrew/opt/node@24/bin/node", "/usr/local/opt/node@24/bin/node"))
    node_on_path = shutil.which("node")
    if node_on_path:
        candidates.append(node_on_path)
    for candidate in candidates:
        if not Path(candidate).is_file() or not os.access(candidate, os.X_OK):
            continue
        try:
            result = run_bounded_process([candidate, "--version"], timeout=5, max_output_bytes=1024)
        except (OSError, QmdBackendError) as error:
            diagnostics.append(str(error))
            continue
        version_match = re.match(r"v?(\d+)\.", result.stdout.strip())
        if result.returncode == 0 and version_match and int(version_match.group(1)) == 24:
            return candidate
        diagnostics.append(f"{candidate} reported {result.stdout.strip() or result.returncode}")
    detail = "; ".join(diagnostics[-3:])
    suffix = f": {detail}" if detail else ""
    raise QmdBackendError(f"QMD refresh requires the installed Node 24 runtime{suffix}")


def qmd_package_root() -> Path:
    prefix = Path(os.environ.get("QMD_PREFIX", Path.home() / ".local" / "share" / "qmd" / "npm")).expanduser()
    package = prefix / "lib" / "node_modules" / "@tobilu" / "qmd"
    if not (package / "dist" / "index.js").is_file():
        raise QmdBackendError(f"installed QMD SDK is unavailable: {package}")
    return package


def parse_qmd_json(raw: str) -> object:
    try:
        return json.loads(raw, object_pairs_hook=_unique_json_object, parse_constant=_reject_json_constant)
    except (ValueError, TypeError, json.JSONDecodeError) as error:
        raise QmdBackendError(f"QMD returned malformed JSON: {error}") from error


def _qmd_result_path(raw_path: object, roots: dict[str, Path]) -> Path:
    if not isinstance(raw_path, str) or not raw_path or len(raw_path) > 4096:
        raise QmdBackendError("QMD returned a missing or invalid source path")
    if raw_path.startswith("qmd://") or "\x00" in raw_path:
        raise QmdBackendError("QMD did not resolve a result to an on-disk source path")
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        if ".." in candidate.parts:
            raise QmdBackendError("QMD returned a traversal path")
        candidate = ROOT / candidate
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as error:
        raise QmdBackendError(f"QMD returned a missing source path: {raw_path}") from error
    if not any(resolved.is_relative_to(root) for root in roots.values()):
        raise QmdBackendError(f"QMD returned a path outside the approved skills-db collections: {raw_path}")
    if not resolved.is_file():
        raise QmdBackendError(f"QMD returned a non-file source path: {raw_path}")
    return resolved


def _qmd_source_row(path: Path, rows_by_file_identity: dict) -> dict:
    try:
        stat = path.stat()
    except OSError as error:
        raise QmdBackendError(f"QMD result source is unreadable: {path}: {error}") from error
    candidates = rows_by_file_identity.get((stat.st_dev, stat.st_ino), [])
    if len(candidates) != 1:
        raise QmdBackendError(f"QMD returned an unknown or ambiguous canonical source: {path}")
    return candidates[0]


def _qmd_fingerprints(
    group: dict,
    *,
    category: str | None,
    revision: str,
    limit: int,
) -> tuple[str, str]:
    predicate = digest_json(
        {
            "backend": "qmd", "tokens": sorted(set(group["tokens"])),
            "category": normalize_name(category) if category else None,
            "namespace": "skills-db", "visibility": "legacy_discovery_visible", "revision": revision,
        }
    )
    request = digest_json(
        {
            "backend": "qmd", "normalized_phrase": group["normalized"],
            "ordered_tokens": group["tokens"], "category": normalize_name(category) if category else None,
            "namespace": "skills-db", "visibility": "legacy_discovery_visible", "revision": revision,
            "limit": limit, "candidate_limit": QMD_CANDIDATE_LIMIT,
            "order": "qmd_score_desc_name_asc_path_key_asc",
        }
    )
    return predicate, request


def _qmd_query_results(
    group: dict,
    *,
    request: dict,
    rows: list[dict],
    roots: dict[str, Path],
    deadline: float,
    output_remaining: int,
) -> tuple[list[dict], int]:
    qmd = shutil.which("qmd")
    if not qmd:
        raise QmdBackendError("QMD launcher is not available in PATH")
    query_text = " ".join(group["tokens"])
    query_document = f"lex: {query_text}\nvec: {query_text}"
    command = [
        qmd, "--index", "index", "query", query_document,
        "--format", "json", "--full-path", "--full", "--no-rerank",
        "--candidate-limit", str(QMD_CANDIDATE_LIMIT), "--n", str(QMD_CANDIDATE_LIMIT),
    ]
    for collection in roots:
        command.extend(("--collection", collection))
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise QmdBackendError("QMD query exceeded its total time limit")
    try:
        result = run_bounded_process(
            command,
            cwd=ROOT,
            timeout=min(QMD_QUERY_TIMEOUT_SECONDS, remaining),
            max_output_bytes=max(0, output_remaining),
        )
    except (OSError, QmdBackendError) as error:
        raise QmdBackendError(str(error)) from error
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()[-1][:400] if result.stderr.strip() else "no diagnostic output"
        raise QmdBackendError(f"QMD query failed with exit status {result.returncode}: {detail}")
    raw_results = parse_qmd_json(result.stdout)
    if not isinstance(raw_results, list):
        raise QmdBackendError("QMD returned a non-array result")

    rows_by_identity = defaultdict(list)
    for row in rows:
        if row.get("base") != "skills-db" or row.get("doc_type", "skill") not in {"skill", "markdown"}:
            continue
        try:
            stat = Path(row["path"]).stat()
        except OSError as error:
            raise QmdBackendError(f"canonical source disappeared during QMD retrieval: {row.get('path')}") from error
        rows_by_identity[(stat.st_dev, stat.st_ino)].append(row)

    eligible_rows = filtered_inventory(
        rows,
        category=request["category"],
        namespace="skills-db",
        include_hidden=False,
    )
    eligible_by_id = {
        row["source_id"]: row
        for row in eligible_rows
        if row.get("doc_type", "skill") in {"skill", "markdown"}
    }
    found = {}
    for raw in raw_results:
        if not isinstance(raw, dict):
            raise QmdBackendError("QMD returned a malformed result row")
        score = raw.get("score")
        try:
            score_value = float(score) if not isinstance(score, bool) and isinstance(score, (int, float)) else math.nan
        except (OverflowError, ValueError, TypeError):
            score_value = math.nan
        if not math.isfinite(score_value) or not 0 < score_value <= 1:
            raise QmdBackendError("QMD returned an invalid, negative, or non-finite score")
        path = _qmd_result_path(raw.get("file"), roots)
        row = _qmd_source_row(path, rows_by_identity)
        try:
            source_bytes = path.read_bytes()
        except OSError as error:
            raise QmdBackendError(f"QMD result source is unreadable: {path}: {error}") from error
        if hashlib.sha256(source_bytes).hexdigest() != row.get("digest"):
            raise QmdBackendError(f"canonical source changed during QMD retrieval: {path}")
        indexed_body = raw.get("body")
        if not isinstance(indexed_body, str):
            raise QmdBackendError(f"QMD returned no full indexed body for freshness validation: {path}")
        if indexed_body != source_bytes.decode("utf-8", errors="replace"):
            raise QmdBackendError(f"QMD indexed content is stale for canonical source: {path}")
        source_id = row.get("source_id")
        if source_id not in eligible_by_id:
            continue
        row = eligible_by_id[source_id]
        lexical_score, matched_terms = score_row(row, group["query"], group["tokens"])
        match = {
            "source_id": source_id,
            "path": row["path"],
            "path_key": row["path_key"],
            "skill_name": row["name"],
            "score": score_value,
            "adjusted_score": score_value,
            "backend_score": score_value,
            "retrieval_backend": "qmd",
            "category": row["category"],
            "surface": row["surface"],
            "lifecycle": row["lifecycle"],
            "rotation_role": row["rotation_role"],
            "usage_count": row["usage_count"],
            "usage_tier": row["usage_tier"],
            "skill_uri": row["skill_uri"],
            "lane": row["lane"],
            "graph_id": row["graph_id"],
            "graph_degree": row["graph_degree"],
            "intent_tags": row["intent_tags"],
            "matched_terms": matched_terms,
            "local_path": row["path"],
            "doc_type": row.get("doc_type", "skill"),
            "source": "inventory",
            "anomaly": row.get("anomaly", ""),
            "lexical_score": lexical_score,
        }
        prior = found.get(source_id)
        if prior is None or match["adjusted_score"] > prior["adjusted_score"]:
            found[source_id] = match
    matches = sorted(
        found.values(),
        key=lambda item: (-item["adjusted_score"], item["skill_name"].lower(), item["path_key"]),
    )
    return matches, len(result.stdout.encode("utf-8")) + len(result.stderr.encode("utf-8"))


def cmd_discover_qmd(request: dict, rows: list[dict], snapshot: dict) -> int:
    try:
        config_path, _, roots, embed_model = preflight_qmd(refresh=False)
        qmd_index_integrity_guard(
            config_path=config_path,
            roots=roots,
            model=embed_model,
            records=rows,
        )
        active_roots = {name: roots[name] for name in QMD_QUERY_COLLECTIONS}
        revision = snapshot["revision"]
        deadline = time.monotonic() + QMD_TOTAL_QUERY_TIMEOUT_SECONDS
        output_remaining = QMD_MAX_OUTPUT_BYTES
        outcomes = []
        evaluated = {}
        union = {}
        for group in request["groups"]:
            predicate, ranking_request = _qmd_fingerprints(
                group,
                category=request["category"],
                revision=revision,
                limit=request["limit"],
            )
            duplicate = evaluated.get(ranking_request)
            if duplicate:
                prior, raw_matches = duplicate
                outcome = {
                    "id": group["id"], "kind": group["kind"], "raw": group["raw"],
                    "normalized": group["normalized"], "tokens": group["tokens"],
                    "status": prior["status"], "total": prior["total"],
                    "predicate_fingerprint": predicate, "request_fingerprint": ranking_request,
                    "duplicate_of": prior["id"], "evaluated": False,
                    "evaluation_origin": "mapped_duplicate", "backend": "qmd",
                }
            else:
                raw_matches, consumed_bytes = _qmd_query_results(
                    group,
                    request=request,
                    rows=rows,
                    roots=active_roots,
                    deadline=deadline,
                    output_remaining=output_remaining,
                )
                output_remaining -= consumed_bytes
                if output_remaining < 0:
                    raise QmdBackendError("QMD queries exceeded the total output limit")
                outcome = {
                    "id": group["id"], "kind": group["kind"], "raw": group["raw"],
                    "normalized": group["normalized"], "tokens": group["tokens"],
                    "status": "ok" if raw_matches else "empty", "total": len(raw_matches),
                    "predicate_fingerprint": predicate, "request_fingerprint": ranking_request,
                    "duplicate_of": None, "evaluated": True,
                    "evaluation_origin": "qmd_query", "backend": "qmd", "total_exact": False,
                }
                evaluated[ranking_request] = (outcome, raw_matches)
            outcomes.append(outcome)
            for match in raw_matches:
                source_id = match["source_id"]
                entry = union.setdefault(
                    source_id,
                    {"best": dict(match), "matched_groups": [], "group_scores": {}, "group_matches": {}, "matched_terms": set()},
                )
                if match["adjusted_score"] > entry["best"]["adjusted_score"]:
                    entry["best"] = dict(match)
                if group["id"] not in entry["matched_groups"]:
                    entry["matched_groups"].append(group["id"])
                entry["group_scores"][group["id"]] = match["adjusted_score"]
                entry["group_matches"][group["id"]] = {
                    "score": match["adjusted_score"], "matched_terms": match["matched_terms"]
                }
                entry["matched_terms"].update(match["matched_terms"])

        union_matches = []
        for value in union.values():
            match = dict(value["best"])
            match["matched_groups"] = value["matched_groups"]
            match["group_scores"] = value["group_scores"]
            match["group_matches"] = value["group_matches"]
            match["matched_terms"] = sorted(value["matched_terms"])
            union_matches.append(match)
        union_matches.sort(key=lambda item: (-item["adjusted_score"], item["skill_name"].lower(), item["path_key"]))
        total = len(union_matches)
        rows_by_id, bundles, _ = _descriptor_indexes(rows, snapshot)
        selected = [
            _with_source_descriptor(match, revision=revision, rows_by_id=rows_by_id, bundles=bundles)
            for match in union_matches[: request["limit"]]
        ]
        normalized_request = {
            "mode": "discover", "backend": "qmd",
            "queries": [
                {"raw": group["raw"], "normalized_phrase": group["normalized"], "ordered_tokens": group["tokens"]}
                for group in request["groups"] if group["kind"] == "query"
            ],
            "tags_raw": request["tags_raw"], "normalized_tags": request["normalized_tags"],
            "category": normalize_name(request["category"]) if request["category"] else None,
            "namespace": "skills-db", "visibility": "legacy_discovery_visible", "revision": revision,
            "limit": request["limit"], "candidate_limit": QMD_CANDIDATE_LIMIT,
            "order": "qmd_score_desc_name_asc_path_key_asc",
        }
        legacy_query = request["groups"][0]["raw"] if len(request["groups"]) == 1 and request["groups"][0]["kind"] == "query" else None
        payload = {
            "schema_version": "lev.skills.discover.v1", "status": "ok" if total else "empty",
            "evaluation_origin": "qmd_query", "backend": "qmd", "total_exact": False,
            "candidate_limit": QMD_CANDIDATE_LIMIT,
            "query": legacy_query, "category_filter": [request["category"]] if request["category"] else [],
            "source_of_truth": str(SKILLS_INVENTORY_FILE), "index_revision": revision,
            "normalized_request": normalized_request, "breadcrumbs": [], "total": total,
            "returned_count": len(selected), "limit": request["limit"], "next_cursor": None,
            "diagnostics": [], "next_actions": ["Open returned source paths directly; get is optional."],
            "query_groups": outcomes, "matches": selected,
            "_cache": {"hit": False, "bypassed": True},
        }
        if request["json"]:
            print(json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False))
            return 0
        return print_discover_text(payload)
    except QmdBackendError as error:
        message = str(error)
        code = "qmd_backend_error"
        if "timed out" in message or "time limit" in message:
            code = "qmd_timeout"
        elif "model" in message.lower():
            code = "qmd_model_unavailable"
        elif "index is unavailable" in message.lower():
            code = "qmd_index_unavailable"
        elif "stale qmd index" in message.lower() or "stale_qmd_index" in message.lower():
            code = "stale_qmd_index"
        elif "index integrity" in message.lower() or "qmd_index_integrity" in message.lower():
            code = "qmd_index_integrity"
        elif "stale" in message.lower() or "changed during" in message.lower():
            code = "stale_qmd_index"
        elif "outside" in message.lower() or "traversal" in message.lower() or "unknown or ambiguous" in message.lower():
            code = "qmd_untrusted_source"
        elif "failed with exit status" in message:
            code = "qmd_engine_failed"
        return emit_cli_error(code, message, json_mode=request["json"])


def cmd_discover(args: list[str]) -> int:
    json_mode = "--json" in args
    try:
        request = parse_discovery_request(args)
    except CliRequestError as error:
        return emit_cli_error(error.code, str(error), json_mode=json_mode, extra=error.extra)

    groups = request["groups"]
    try:
        rows, snapshot = read_validated_inventory()
    except RuntimeError as error:
        group_outcomes = [
            {
                "id": group["id"],
                "kind": group["kind"],
                "raw": group["raw"],
                "normalized": group["normalized"],
                "tokens": group["tokens"],
                "status": "unevaluated",
                "evaluation_origin": "unevaluated",
                "total": None,
                "predicate_fingerprint": None,
                "request_fingerprint": None,
                "duplicate_of": None,
                "diagnostics": [str(error)],
            }
            for group in groups
        ]
        code = _index_error_code(error)
        return emit_cli_error(
            code,
            str(error),
            json_mode=request["json"],
            extra={"query_groups": group_outcomes, "matches": []},
        )

    if request["backend"] == "qmd":
        return cmd_discover_qmd(request, rows, snapshot)

    revision = snapshot["revision"]
    rows_by_id, bundles, _ = _descriptor_indexes(rows, snapshot)
    cacheable = len(groups) == 1 and groups[0]["kind"] == "query" and request["namespace"] is None
    cache_request = None
    result_cache_key = None
    if request["json"] and cacheable and not request["no_cache"]:
        cache_request = discover_cache_request(
            groups[0]["raw"],
            request["category"],
            request["all_collections"],
            request["limit"],
            revision,
            namespace=request["namespace"],
        )
        result_cache_key = cache_key(
            groups[0]["raw"],
            request["category"],
            request["all_collections"],
            mode="discover",
            limit=request["limit"],
            revision=revision,
            namespace=request["namespace"],
        )
        cached = get_cached_result(result_cache_key, cache_request)
        if cached and cached_discovery_result_is_current(
            cached,
            request,
            rows=rows,
            revision=revision,
            rows_by_id=rows_by_id,
            bundles=bundles,
        ):
            cached["evaluation_origin"] = "cache"
            for group_outcome in cached.get("query_groups", []):
                if isinstance(group_outcome, dict):
                    group_outcome["evaluated"] = False
                    group_outcome["evaluation_origin"] = "cache"
            print(json.dumps(cached, indent=2, ensure_ascii=False))
            return 0

    roles = None
    outcomes = []
    evaluated: dict[str, tuple[dict, list[dict]]] = {}
    union: dict[str, dict] = {}

    for group in groups:
        predicate = _predicate_fingerprint(
            group,
            category=request["category"],
            namespace=request["namespace"],
            visibility="legacy_discovery_visible",
            roles=roles,
            revision=revision,
        )
        ranking_request = _ranking_request_fingerprint(
            group,
            category=request["category"],
            namespace=request["namespace"],
            visibility="legacy_discovery_visible",
            roles=roles,
            revision=revision,
            limit=request["limit"],
        )
        duplicate = evaluated.get(ranking_request)
        if duplicate:
            prior, raw_matches = duplicate
            outcome = {
                "id": group["id"],
                "kind": group["kind"],
                "raw": group["raw"],
                "normalized": group["normalized"],
                "tokens": group["tokens"],
                "status": prior["status"],
                "total": prior["total"],
                "predicate_fingerprint": predicate,
                "request_fingerprint": ranking_request,
                "duplicate_of": prior["id"],
                "evaluated": False,
                "evaluation_origin": "mapped_duplicate",
            }
        else:
            raw_matches = discover_matches(
                group["query"],
                rows=rows,
                category=request["category"],
                namespace=request["namespace"],
                limit=None,
            )
            outcome = {
                "id": group["id"],
                "kind": group["kind"],
                "raw": group["raw"],
                "normalized": group["normalized"],
                "tokens": group["tokens"],
                "status": "ok" if raw_matches else "empty",
                "total": len(raw_matches),
                "predicate_fingerprint": predicate,
                "request_fingerprint": ranking_request,
                "duplicate_of": None,
                "evaluated": True,
                "evaluation_origin": "cli_evaluation",
            }
            evaluated[ranking_request] = (outcome, raw_matches)
        outcomes.append(outcome)
        mapped_matches = raw_matches if not duplicate else duplicate[1]
        for match in mapped_matches:
            source_id = match["source_id"]
            entry = union.setdefault(
                source_id,
                {
                    "best": dict(match),
                    "matched_groups": [],
                    "group_scores": {},
                    "group_matches": {},
                    "matched_terms": set(),
                },
            )
            if match["adjusted_score"] > entry["best"]["adjusted_score"]:
                entry["best"] = dict(match)
            if group["id"] not in entry["matched_groups"]:
                entry["matched_groups"].append(group["id"])
            entry["group_scores"][group["id"]] = match["adjusted_score"]
            entry["group_matches"][group["id"]] = {
                "score": match["adjusted_score"],
                "matched_terms": match["matched_terms"],
            }
            entry["matched_terms"].update(match["matched_terms"])

    union_matches = []
    for source_id, value in union.items():
        match = dict(value["best"])
        match["matched_groups"] = value["matched_groups"]
        match["group_scores"] = value["group_scores"]
        match["group_matches"] = value["group_matches"]
        match["matched_terms"] = sorted(value["matched_terms"])
        union_matches.append(match)
    union_matches.sort(
        key=lambda item: (-item["adjusted_score"], item["skill_name"].lower(), item["path_key"])
    )
    total = len(union_matches)
    selected = [
        _with_source_descriptor(match, revision=revision, rows_by_id=rows_by_id, bundles=bundles)
        for match in union_matches[: request["limit"]]
    ]
    legacy_query = groups[0]["raw"] if len(groups) == 1 and groups[0]["kind"] == "query" else None
    normalized_request = {
        "mode": "discover",
        "matcher_version": 1,
        "request_schema_version": 1,
        "queries": [
            {"raw": group["raw"], "normalized_phrase": group["normalized"], "ordered_tokens": group["tokens"]}
            for group in groups
            if group["kind"] == "query"
        ],
        "tags_raw": request["tags_raw"],
        "normalized_tags": request["normalized_tags"],
        "category": normalize_name(request["category"]) if request["category"] else None,
        "namespace": request["namespace"],
        "visibility": "legacy_discovery_visible",
        "roles": None,
        "revision": revision,
        "limit": request["limit"],
        "order": "score_desc_name_asc_path_key_asc",
        "all_collections": request["all_collections"],
    }
    payload = {
        "schema_version": "lev.skills.discover.v1",
        "status": "ok" if total else "empty",
        "evaluation_origin": "cli_evaluation",
        "query": legacy_query,
        "category_filter": [request["category"]] if request["category"] else [],
        "source_of_truth": str(SKILLS_INVENTORY_FILE),
        "index_revision": revision,
        "normalized_request": normalized_request,
        "breadcrumbs": [],
        "total": total,
        "returned_count": len(selected),
        "limit": request["limit"],
        "next_cursor": None,
        "diagnostics": [],
        "next_actions": ["Open returned source paths directly; get is optional."],
        "query_groups": outcomes,
        "matches": selected,
    }

    if request["json"] and cacheable and not request["no_cache"]:
        assert cache_request is not None and result_cache_key is not None
        set_cached_result(result_cache_key, payload, cache_request)
        payload["_cache"] = {"hit": False, "age_seconds": 0}
    elif request["json"]:
        payload["_cache"] = {"hit": False, "bypassed": True}

    if request["json"]:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    return print_discover_text(payload)


def cmd_pick(args: list[str]) -> int:
    json_mode = "--json" in args
    try:
        request = parse_pick_request(args)
    except CliRequestError as error:
        return emit_cli_error(error.code, str(error), json_mode=json_mode, extra=error.extra)

    query = request["query"]
    category = request["category"]
    namespace = request["namespace"]
    rotation_roles = request["rotation_roles"]
    try:
        rows, snapshot = read_validated_inventory()
    except RuntimeError as error:
        return emit_cli_error(
            _index_error_code(error), str(error), json_mode=request["json"], extra={"candidates": []}
        )
    rows = [row for row in rows if row.get("doc_type") == "skill"]
    matches = discover_matches(
        query,
        rows=rows,
        category=category,
        namespace=namespace,
        rotation_roles=rotation_roles,
    )
    revision = snapshot["revision"]
    rows_by_id, bundles, _ = _descriptor_indexes(rows, snapshot)
    matches = [
        _with_source_descriptor(match, revision=revision, rows_by_id=rows_by_id, bundles=bundles)
        for match in matches
    ]
    normalized_request = {
        "mode": "pick",
        "normalized_phrase": normalize_name(query),
        "ordered_tokens": tokenize(query),
        "category": normalize_name(category) if category else None,
        "namespace": namespace,
        "visibility": "rotation_roles",
        "roles": sorted(rotation_roles),
        "revision": revision,
        "limit": 30,
        "order": "score_desc_name_asc_path_key_asc",
    }
    if not matches:
        payload = {
            "schema_version": "lev.skills.pick.v1",
            "status": "empty",
            "query": query,
            "rotation_roles": sorted(rotation_roles),
            "normalized_request": normalized_request,
            "index_revision": revision,
            "picked": None,
            "candidates": [],
        }
        if request["json"]:
            print(json.dumps(payload, indent=2))
            return 0
        print("No rotatable skills matched that query.")
        return 0

    top_candidates = matches[: min(12, len(matches))]
    weights = []
    for item in top_candidates:
        weight = 1.0
        if item["rotation_role"] == "experimental":
            weight *= 1.25
        if item["usage_count"] > 0:
            weight *= 1 / max(1.0, math.log2(item["usage_count"] + 1))
        weights.append(max(weight, 0.05))
    picked = random.choices(top_candidates, weights=weights, k=1)[0]
    payload = {
        "schema_version": "lev.skills.pick.v1",
        "status": "ok",
        "query": query,
        "rotation_roles": sorted(rotation_roles),
        "normalized_request": normalized_request,
        "index_revision": revision,
        "picked": picked,
        "candidates": top_candidates,
    }
    if request["json"]:
        print(json.dumps(payload, indent=2))
        return 0
    print(
        f"{picked['skill_name']} [{picked['category']}/{picked['rotation_role']}] "
        f"usage={picked['usage_count']} :: {picked['local_path']}"
    )
    return 0


def cmd_tree(args: list[str]) -> int:
    json_mode = "--json" in args
    try:
        request = parse_tree_request(args)
    except CliRequestError as error:
        return emit_cli_error(error.code, str(error), json_mode=json_mode, extra=error.extra)
    try:
        rows, snapshot = read_validated_inventory()
    except RuntimeError as error:
        return emit_cli_error(
            _index_error_code(error, taxonomy_required=True), str(error), json_mode=request["json"]
        )
    taxonomy = snapshot.get("taxonomy")
    if not isinstance(taxonomy, dict) or taxonomy.get("status") != "projected":
        return emit_cli_error(
            "taxonomy_unavailable",
            "accepted taxonomy tree is unavailable; rebuild the source inventory after taxonomy repair",
            json_mode=request["json"],
        )
    try:
        node_by_id, node_rows = _navigation_rows(rows, taxonomy)
        all_nodes = [node for node in taxonomy.get("nodes", []) if isinstance(node, dict)]
        if request["view"] == "subjects":
            selected = [node for node in all_nodes if str(node.get("id", "")).startswith("view.")]
        else:
            selected = [
                node for node in all_nodes if node.get("view_kind") in {"source_namespace", "source_collection"}
            ]
        selected_ids = {node["id"] for node in selected}
        children_by_parent: defaultdict[str | None, list[dict]] = defaultdict(list)
        roots = []
        for node in selected:
            parent_id = node.get("parent_id")
            if isinstance(parent_id, str) and parent_id in selected_ids:
                children_by_parent[parent_id].append(node)
            else:
                roots.append(node)
        projected_counts = taxonomy.get("view_counts", {})
        items = [
            _tree_node(
                node,
                node_by_id=node_by_id,
                node_rows=node_rows,
                projected_counts=projected_counts,
                children_by_parent=children_by_parent,
                depth=request["depth"],
                level=0,
            )
            for node in roots
        ]
        rendered_count = len(
            [node for root in items for node in _flatten_tree_nodes(root)]
        )
    except RuntimeError as error:
        return emit_cli_error("taxonomy_unavailable", str(error), json_mode=request["json"])

    revision = snapshot["revision"]
    payload = {
        "schema_version": "lev.skills.tree.v1",
        "status": "ok",
        "index_revision": revision,
        "normalized_request": {
            "view": request["view"],
            "depth": request["depth"],
            "visibility": "all_non_disposed",
            "revision": revision,
            "order": "configured_sibling_order",
        },
        "breadcrumbs": [],
        "total": rendered_count,
        "returned_count": len(items),
        "depth": request["depth"],
        "items": items,
        "diagnostics": list(taxonomy.get("diagnostics", [])),
        "next_actions": ["Browse a node by its exact ID."],
    }
    if request["json"]:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    for node in _flatten_tree_nodes_from_items(items):
        print(f"{'  ' * node['_level']}- {node['label']} [{node['id']}] eligible={node['eligible_count']}")
    return 0


def _flatten_tree_nodes(node: dict) -> list[dict]:
    output = [node]
    for child in node.get("children", []):
        output.extend(_flatten_tree_nodes(child))
    return output


def _flatten_tree_nodes_from_items(items: list[dict]) -> list[dict]:
    output = []
    stack = [(item, 0) for item in reversed(items)]
    while stack:
        node, level = stack.pop()
        output.append({**node, "_level": level})
        stack.extend((child, level + 1) for child in reversed(node.get("children", [])))
    return output


def cmd_browse(args: list[str]) -> int:
    json_mode = "--json" in args
    try:
        request = parse_browse_request(args)
    except CliRequestError as error:
        return emit_cli_error(error.code, str(error), json_mode=json_mode, extra=error.extra)
    cursor = None
    if request.get("cursor") is not None:
        try:
            cursor = _decode_browse_cursor(request["cursor"])
        except CliRequestError as error:
            return emit_cli_error(error.code, str(error), json_mode=request["json"])
    try:
        rows, snapshot = read_validated_inventory()
    except RuntimeError as error:
        code = "stale_cursor" if cursor is not None and "stale" in str(error).lower() else _index_error_code(
            error, taxonomy_required=True
        )
        return emit_cli_error(code, str(error), json_mode=request["json"])
    taxonomy = snapshot.get("taxonomy")
    if not isinstance(taxonomy, dict) or taxonomy.get("status") != "projected":
        return emit_cli_error(
            "taxonomy_unavailable",
            "accepted taxonomy tree is unavailable; rebuild the source inventory after taxonomy repair",
            json_mode=request["json"],
        )
    revision = snapshot["revision"]
    if cursor is not None:
        if cursor["revision"] != revision:
            return emit_cli_error("stale_cursor", "browse cursor belongs to a different index revision", json_mode=request["json"])
        node_id = cursor["node_id"]
        limit = cursor["limit"]
        offset = cursor["offset"]
    else:
        node_id = request["node_id"]
        limit = request["limit"]
        offset = 0
    try:
        node_by_id, node_rows = _navigation_rows(rows, taxonomy)
    except RuntimeError as error:
        return emit_cli_error("taxonomy_unavailable", str(error), json_mode=request["json"])
    node = node_by_id.get(node_id)
    if node is None:
        return emit_cli_error(
            "unknown_node", f"taxonomy node is unknown: {node_id}", json_mode=request["json"], extra={"node_id": node_id}
        )
    eligible = node_rows.get(node_id, [])
    total = len(eligible)
    if offset > total:
        return emit_cli_error("invalid_cursor", "browse cursor offset exceeds the current node total", json_mode=request["json"])
    page = eligible[offset : offset + limit]
    try:
        rows_by_id, bundles, _ = _descriptor_indexes(rows, snapshot)
        items = [
            _source_descriptor(row, revision=revision, rows_by_id=rows_by_id, bundles=bundles)
            for row in page
        ]
        breadcrumbs = _breadcrumbs(node_id, node_by_id)
    except RuntimeError as error:
        return emit_cli_error("invalid_index", str(error), json_mode=request["json"])
    next_cursor = None
    if offset + len(page) < total:
        next_cursor = _make_browse_cursor(node_id, revision, limit, offset + len(page))
    status = "ok" if page else "empty"
    payload = {
        "schema_version": "lev.skills.browse.v1",
        "status": status,
        "index_revision": revision,
        "normalized_request": {
            "node_id": node_id,
            "visibility": "all_non_disposed",
            "revision": revision,
            "limit": limit,
            "order": "normalized_name_source_id",
            "offset": offset,
        },
        "node_id": node_id,
        "breadcrumbs": breadcrumbs,
        "projected_resource_count": taxonomy.get("view_counts", {}).get(node_id),
        "eligible_count": total,
        "total": total,
        "returned_count": len(items),
        "limit": limit,
        "next_cursor": next_cursor,
        "items": items,
        "diagnostics": [],
        "next_actions": ["Open returned source paths directly; get is optional."],
    }
    if request["json"]:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    if not items:
        print(f"No retained sources in {node_id}.")
        return 0
    for item in items:
        print(f"- {item['skill_name']} [{item['source_namespace']}/{item['source_collection']}] :: {item['path']}")
    if next_cursor:
        print(f"next_cursor: {next_cursor}")
    return 0


def cmd_get(args: list[str]) -> int:
    json_mode = "--json" in args
    try:
        request = parse_get_request(args)
    except CliRequestError as error:
        return emit_cli_error(error.code, str(error), json_mode=json_mode, extra=error.extra)
    try:
        rows, snapshot = read_validated_inventory()
    except RuntimeError as error:
        return emit_cli_error(_index_error_code(error), str(error), json_mode=request["json"])
    revision = snapshot["revision"]
    rows_by_id, bundles, aliases = _descriptor_indexes(rows, snapshot)
    source_key = request["source_key"]
    exact = rows_by_id.get(source_key)
    if exact is not None:
        candidate_ids = [source_key] if not has_disposed_ancestor(exact) else []
    else:
        candidate_ids = sorted(
            source_id for source_id in aliases.get(normalize_name(source_key), set())
            if source_id in rows_by_id and not has_disposed_ancestor(rows_by_id[source_id])
        )
    if not candidate_ids:
        return emit_cli_error(
            "source_not_found", f"no retained source matches: {source_key}", json_mode=request["json"]
        )
    if len(candidate_ids) > 1:
        try:
            alternatives = [
                _source_descriptor(rows_by_id[source_id], revision=revision, rows_by_id=rows_by_id, bundles=bundles)
                for source_id in candidate_ids
            ]
        except RuntimeError as error:
            return emit_cli_error("invalid_index", str(error), json_mode=request["json"])
        return emit_cli_error(
            "ambiguous_source",
            f"source name is ambiguous: {source_key}",
            json_mode=request["json"],
            extra={"alternatives": alternatives},
        )
    try:
        item = _source_descriptor(
            rows_by_id[candidate_ids[0]], revision=revision, rows_by_id=rows_by_id, bundles=bundles
        )
    except RuntimeError as error:
        return emit_cli_error("invalid_index", str(error), json_mode=request["json"])
    payload = {
        "schema_version": "lev.skills.get.v1",
        "status": "ok",
        "index_revision": revision,
        "normalized_request": {
            "source_key": source_key,
            "exact_source_id": source_key == item["source_id"],
            "revision": revision,
        },
        "breadcrumbs": [],
        "total": 1,
        "returned_count": 1,
        "limit": 1,
        "next_cursor": None,
        "items": [item],
        "diagnostics": [],
        "next_actions": ["Open the recorded path directly; this response contains descriptors, not file bytes."],
    }
    if request["json"]:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    print(f"{item['skill_name']} :: {item['path']} sha256={item['digest']}")
    return 0


def cmd_inventory(args: list[str]) -> int:
    json_mode = "--json" in args
    include_hidden = "--include-hidden" in args
    rebuild = "--rebuild" in args
    try:
        rows = build_inventory(force_rebuild=rebuild)
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    visible = filtered_inventory(rows, include_hidden=include_hidden)
    if json_mode:
        print(json.dumps(visible, indent=2))
        return 0

    print(f"inventory_file: {SKILLS_INVENTORY_FILE}")
    print(f"total_rows: {len(rows)}")
    print(f"visible_rows: {len(visible)}")
    print("lifecycle_counts:")
    lifecycle_counts = Counter(item["lifecycle"] for item in rows)
    for lifecycle, count in sorted(lifecycle_counts.items(), key=lambda item: item[0]):
        print(f"- {lifecycle}: {count}")
    print("top_used:")
    for item in sorted(rows, key=lambda entry: (-entry["usage_count"], entry["path_key"]))[:15]:
        print(f"- {item['usage_count']:>3} {item['name']} [{item['path_key']}]")
    return 0


def cmd_refresh(args: list[str]) -> int:
    """Refresh only the approved skills-db QMD collections and rebuild after success."""
    if any(arg != "--repo-local" for arg in args) or args.count("--repo-local") > 1:
        print("error: refresh accepts only one optional --repo-local flag", file=sys.stderr)
        return 1
    try:
        inventory_preflight = preflight_inventory_inputs()
        source_records = inventory_preflight[5]
        config_path, _, roots, embed_model = preflight_qmd(refresh=True)
        qmd_package_root()
        node = qmd_node_executable()
        db_path = qmd_database_path()
        if not db_path.is_file():
            raise QmdBackendError(f"QMD index is unavailable: {db_path}")
        bridge = ROOT / "lev-skills-qmd.mjs"
        if not bridge.is_file():
            raise QmdBackendError(f"QMD SDK bridge is missing: {bridge}")
        request = {
            "operation": "refresh",
            "dbPath": str(db_path),
            "configPath": str(config_path),
            "collections": list(QMD_REFRESH_COLLECTIONS),
            "embedCollections": list(QMD_REFRESH_COLLECTIONS),
            "force": False,
            "maxDocsPerBatch": 50,
            "maxBatchBytes": 16 * 1024 * 1024,
        }
        result = run_bounded_process(
            [node, str(bridge), json.dumps(request, separators=(",", ":"))],
            cwd=ROOT,
            timeout=QMD_REFRESH_TIMEOUT_SECONDS,
            max_output_bytes=2 * 1024 * 1024,
        )
        response = parse_qmd_json(result.stdout)
        if not isinstance(response, dict):
            raise QmdBackendError("QMD SDK bridge returned a malformed response")
        if result.returncode != 0:
            detail = response.get("error") if isinstance(response.get("error"), str) else f"exit status {result.returncode}"
            raise QmdBackendError(f"QMD SDK refresh failed: {detail}")
        update = response.get("update")
        embeds = response.get("embeds")
        if (
            response.get("status") != "complete"
            or response.get("updatedCollections") != list(QMD_REFRESH_COLLECTIONS)
            or response.get("embedCollections") != list(QMD_REFRESH_COLLECTIONS)
            or response.get("force") is not False
            or not isinstance(update, dict)
            or update.get("collections") != len(QMD_REFRESH_COLLECTIONS)
            or update.get("skipped") != 0
            or not isinstance(embeds, list)
            or len(embeds) != len(QMD_REFRESH_COLLECTIONS)
        ):
            raise QmdBackendError("QMD SDK refresh returned partial or unscoped work")
        numeric_update_fields = ("indexed", "updated", "unchanged", "removed")
        if any(
            not isinstance(update.get(field), int)
            or isinstance(update.get(field), bool)
            or update[field] < 0
            for field in numeric_update_fields
        ):
            raise QmdBackendError("QMD SDK refresh returned invalid update counts")
        for expected, embed in zip(QMD_REFRESH_COLLECTIONS, embeds):
            if (
                not isinstance(embed, dict)
                or embed.get("collection") != expected
                or embed.get("force") is not False
                or embed.get("errors") != 0
                or any(
                    not isinstance(embed.get(field), int)
                    or isinstance(embed.get(field), bool)
                    or embed[field] < 0
                    for field in ("docsProcessed", "chunksEmbedded")
                )
            ):
                raise QmdBackendError(f"QMD embedding did not complete for approved collection {expected}")
        qmd_index_integrity_guard(
            config_path=config_path,
            roots=roots,
            model=embed_model,
            records=source_records,
        )
        build_inventory(force_rebuild=True)
        print(f"QMD refreshed for {len(QMD_REFRESH_COLLECTIONS)} approved skills-db collections.")
        print(f"Inventory rebuilt at {SKILLS_INVENTORY_FILE}")
        return 0
    except QmdBackendError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except FileNotFoundError as error:
        print(f"error: required QMD runtime file is missing: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"error: QMD refresh could not complete: {error}", file=sys.stderr)
        return 1
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


def run_skill_graph_script(script_name: str, args: list[str] | None = None) -> int:
    script = SKILL_GRAPH_DIR / script_name
    if not script.exists():
        print(f"error: skill graph script missing: {script}", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, str(script), *(args or [])],
        cwd=str(SKILL_GRAPH_DIR),
        check=False,
    )
    return result.returncode


def graph_stats_payload() -> dict:
    data = load_skill_graph_payload()
    nodes = data.get("nodes", {})
    edges = data.get("edges", [])
    if not isinstance(nodes, dict):
        nodes = {}
    if not isinstance(edges, list):
        edges = []

    by_kind = Counter()
    by_lane = Counter()
    by_edge_kind = Counter()
    for node in nodes.values():
        if not isinstance(node, dict):
            continue
        by_kind[str(node.get("kind") or "")] += 1
        lane = str(node.get("lane") or "")
        if lane:
            by_lane[lane] += 1
    for edge in edges:
        if isinstance(edge, dict):
            by_edge_kind[str(edge.get("kind") or "")] += 1

    return {
        "graph_path": str(SKILL_GRAPH_FILE),
        "builder_dir": str(SKILL_GRAPH_DIR),
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "by_kind": dict(sorted(by_kind.items())),
        "by_lane": dict(sorted(by_lane.items())),
        "by_edge_kind": dict(sorted(by_edge_kind.items())),
    }


def cmd_graph(args: list[str]) -> int:
    if not args:
        args = ["stats"]

    command = args[0]
    rest = args[1:]
    json_mode = "--json" in rest
    rest = [arg for arg in rest if arg != "--json"]

    if command in {"stats", "status"}:
        try:
            payload = graph_stats_payload()
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        if json_mode:
            print(json.dumps(payload, indent=2))
            return 0
        print(f"graph_path: {payload['graph_path']}")
        print(f"builder_dir: {payload['builder_dir']}")
        print(f"total_nodes: {payload['total_nodes']}")
        print(f"total_edges: {payload['total_edges']}")
        print("by_kind:")
        for kind, count in payload["by_kind"].items():
            print(f"- {kind}: {count}")
        print("by_lane:")
        for lane, count in payload["by_lane"].items():
            print(f"- {lane}: {count}")
        print("by_edge_kind:")
        for edge_kind, count in payload["by_edge_kind"].items():
            print(f"- {edge_kind}: {count}")
        return 0

    if command == "rebuild":
        verify = "--verify" in rest
        try:
            seed_script = SKILL_GRAPH_DIR / "seed.py"
            if not seed_script.is_file():
                raise RuntimeError(f"skill graph seed script missing: {seed_script}")
            if verify and not (SKILL_GRAPH_DIR / "runtime.py").is_file():
                raise RuntimeError(
                    f"skill graph runtime verifier missing: {SKILL_GRAPH_DIR / 'runtime.py'}"
                )
            preflight_inventory_inputs(require_graph=False)
        except RuntimeError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        rc = run_skill_graph_script("seed.py")
        if rc != 0:
            return rc
        try:
            rows = build_inventory(force_rebuild=True)
        except RuntimeError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        print(f"Inventory rebuilt at {SKILLS_INVENTORY_FILE} ({len(rows)} rows)")
        if verify:
            return run_skill_graph_script("runtime.py")
        return 0

    if command == "verify":
        return run_skill_graph_script("runtime.py", rest)

    if command == "resolve":
        if not rest:
            print("error: graph resolve requires a skill:// or lane:// URI", file=sys.stderr)
            return 1
        return run_skill_graph_script("cli.py", ["resolve", *rest])

    print(f"unknown graph command: {command}", file=sys.stderr)
    return 1


def cmd_list() -> int:
    active = active_skill_rows()
    cdo_rows = cdo_subskill_rows()
    workflow_rows = workflow_flow_rows()
    catalog = {}
    for item in catalog_rows(include_hidden=False):
        catalog[item["name"]] = {
            "name": item["name"],
            "description": item["description"],
            "category": item["category"],
        }

    print("Tier 1: protected runtime skills")
    for item in sorted(active, key=lambda row: (0 if row["folder"] == "lev" else 1, row["folder"])):
        print(f"- {item['name']} [{item['folder']}] :: {item['description']}")

    print("\nTier 1: nested cdo skills")
    for item in cdo_rows:
        print(f"- {item['name']} [cdo/{item['folder']}] :: {item['description']}")

    print("\nTier 1: workflow flows")
    for item in sorted(workflow_rows, key=lambda row: row["folder"]):
        print(f"- {item['name']} [workflow/flows/{item['folder']}] :: {item['description']}")

    print("\nTier 2: visible catalog")
    for item in sorted(catalog.values(), key=lambda row: (row["category"], row["name"])):
        print(f"- {item['name']} [{item['category']}] :: {item['description']}")
    return 0


def validate_skill_yaml(skill_md_path: Path) -> list[str]:
    """Validate SKILL.md YAML frontmatter for unsupported attributes."""

    supported_attrs = {
        "name",
        "description",
        "metadata",
        "argument-hint",
        "compatibility",
        "license",
        "disable-model-invocation",
        "user-invokable",
    }

    errors = []
    rel_path = skill_md_path.relative_to(ROOT)
    try:
        data = skill_md_path.read_bytes()
    except OSError as error:
        return [f"{rel_path} error reading file: {error}"]
    meta = parse_meta_data(skill_md_path, data)
    metadata_status = meta["original_metadata"].get("status")
    if metadata_status not in {"parsed", "absent"}:
        errors.append(
            f"{rel_path} metadata {metadata_status}: "
            f"{meta['original_metadata'].get('error') or 'metadata was not parsed'}"
        )
    for diagnostic in meta["diagnostics"]:
        if diagnostic not in {
            meta["original_metadata"].get("error"),
            None,
        }:
            errors.append(f"{rel_path} {diagnostic}")
    metadata = meta["original_metadata"].get("value")
    if isinstance(metadata, dict):
        for key in metadata:
            if key not in supported_attrs:
                errors.append(
                    f"{rel_path} unsupported attribute {key!r} "
                    f"(supported: {', '.join(sorted(supported_attrs))})"
                )

    return errors


def cmd_validate() -> int:
    active = active_skill_rows()
    cdo_rows = cdo_subskill_rows()
    workflow_rows = workflow_flow_rows()
    catalog = catalog_rows(include_hidden=False)

    errors = []
    warnings = []

    for skill_md in walk_source_files(SKILLS_DIR) or ():
        if skill_md.name.casefold() != "skill.md":
            continue
        rel = skill_md.relative_to(SKILLS_DIR)
        if rel.parts[0] == ".system":
            continue
        errors.extend(validate_skill_yaml(skill_md))

    for skill_md in walk_source_files(SKILLS_DB_DIR) or ():
        if skill_md.name.casefold() == "skill.md":
            errors.extend(validate_skill_yaml(skill_md))

    active_names = defaultdict(list)
    active_folders = {item["folder"] for item in active}

    for item in active:
        active_names[item["name"]].append(item)
        if item["folder"] not in ACTIVE_KEEP_FOLDERS:
            errors.append(f"unexpected active skill: {item['folder']} path={item['path']}")
        elif (
            normalize_name(item["folder"]) != normalize_name(item["name"])
            and item["folder"] not in ALLOWED_FOLDER_NAME_DRIFT
        ):
            errors.append(
                f"name drift: folder={item['folder']} name={item['name']} path={item['path']}"
            )

    for name, items in sorted(active_names.items()):
        if len(items) > 1:
            errors.append(f"duplicate active skill name: {name} -> {[x['folder'] for x in items]}")

    for required in sorted(ACTIVE_KEEP_FOLDERS):
        if required not in active_folders:
            errors.append(f"keep-set skill missing from active surface: {required}")

    cdo_folders = {item["folder"] for item in cdo_rows}
    for required in sorted(REQUIRED_CDO_SUBSKILLS):
        if required not in cdo_folders:
            errors.append(f"missing cdo subskill: cdo/{required}")

    flow_folders = {item["folder"] for item in workflow_rows}
    for required in sorted(REQUIRED_WORKFLOW_FLOWS):
        if required not in flow_folders:
            errors.append(f"missing workflow flow: workflow/flows/{required}")

    for item in active:
        folder = item["folder"]
        if folder.startswith("workflow-"):
            errors.append(
                f"workflow sidecar leakage: {folder} should be under skills/workflow/flows/"
            )

    active_name_set = set(active_names)
    for skill_folder, command_name in COMMAND_HOOKED.items():
        if skill_folder not in active_folders and skill_folder not in active_name_set:
            errors.append(
                f"command-hooked skill missing from active: {skill_folder} (command: /{command_name})"
            )

    catalog_names = defaultdict(list)
    for item in catalog:
        catalog_names[item["name"]].append(item)

    for name, items in sorted(catalog_names.items()):
        visible_categories = sorted({row["category"] for row in items})
        if len(items) > 1:
            warnings.append(f"duplicate catalog skill name: {name} -> {visible_categories}")

    catalog_name_set = set(catalog_names)
    active_name_set = {item["name"] for item in active}
    for name in sorted(active_name_set & catalog_name_set):
        errors.append(f"active/catalog overlap: {name}")

    flow_name_set = {item["name"] for item in workflow_rows}
    for name in sorted(flow_name_set & catalog_name_set):
        errors.append(f"workflow/catalog overlap: {name}")

    if errors:
        print("VALIDATE: FAIL")
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")
    else:
        print("VALIDATE: PASS")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    print(
        "\nSummary: "
        f"active={len(active)} "
        f"cdo_nested={len(cdo_rows)} "
        f"workflow_flows={len(workflow_rows)} "
        f"catalog={len({item['name'] for item in catalog_rows(include_hidden=False)})}"
    )
    return 1 if errors else 0


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in {"help", "-h", "--help"}:
        return usage()

    command = sys.argv[1]
    args = sys.argv[2:]

    if command in {"discover", "find"}:
        return cmd_discover(args)
    if command == "pick":
        return cmd_pick(args)
    if command == "tree":
        return cmd_tree(args)
    if command == "browse":
        return cmd_browse(args)
    if command == "get":
        return cmd_get(args)
    if command == "inventory":
        return cmd_inventory(args)
    if command == "list":
        return cmd_list()
    if command == "validate":
        return cmd_validate()
    if command == "refresh":
        return cmd_refresh(args)
    if command == "graph":
        return cmd_graph(args)

    if command.startswith("-"):
        return emit_cli_error(
            "invalid_request",
            f"unknown flag: {command}",
            json_mode="--json" in sys.argv[1:],
        )

    return cmd_discover(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
