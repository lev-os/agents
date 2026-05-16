#!/usr/bin/env python3
"""Skills runtime helper for the active surface and hidden catalog."""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import sqlite3
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency fallback
    yaml = None


ROOT = Path(__file__).resolve().parent
SKILLS_DIR = ROOT / "skills"
SKILLS_DB_DIR = ROOT / "skills-db"
WORKFLOW_FLOWS_DIR = SKILLS_DIR / "workflow" / "flows"
CDO_DIR = SKILLS_DIR / "cdo"
CACHE_DIR = Path(os.environ.get("LEV_CACHE_DIR", Path.home() / ".cache" / "lev-skills"))
CACHE_TTL_SECONDS = int(os.environ.get("LEV_SKILLS_CACHE_TTL", "300"))
CACHE_BG_REFRESH_AFTER = int(os.environ.get("LEV_SKILLS_BG_REFRESH_AFTER", "60"))
INVENTORY_CACHE_FILE = CACHE_DIR / "inventory-cache.json"
SKILLS_STATE_FILE = ROOT / "skills-state.json"
SKILLS_INVENTORY_FILE = ROOT / "skills-inventory.jsonl"
SKILL_GRAPH_FILE = ROOT / "skill-graph.json"
CASS_DB_PATH = Path.home() / "Library" / "Application Support" / "com.coding-agent-search.coding-agent-search" / "agent_search.db"

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
                '  lev-skills discover|find "query" [--json] [--category=...] [--limit=N] [--no-cache]',
                '  lev-skills pick "query" [--json] [--category=...] [--rotation=eligible,experimental] [--no-cache]',
                "  lev-skills inventory [--json] [--include-hidden] [--rebuild]",
                "  lev-skills list",
                "  lev-skills validate",
                "  lev-skills refresh [--repo-local]",
                "  lev-skills help",
                "",
                "NOTES",
                "  discover uses the local filesystem inventory as the canonical source of truth",
                f"  graph metadata is read from {SKILL_GRAPH_FILE} when present",
                f"  inventory writes a grep-able manifest to {SKILLS_INVENTORY_FILE}",
                "  hidden catalog buckets (.archive, _todo, _workshop) are excluded from normal ranking",
                "  qmd is only touched by explicit refresh; discover does not query qmd",
                "",
                "OPTIONS",
                "  --category=NAME   Scope discovery to a specific domain/category",
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


def cache_key(query: str, category: str | None, all_collections: bool, mode: str = "discover") -> str:
    parts = [mode, query.lower().strip(), category or "", str(all_collections)]
    digest = hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]
    return f"{mode}-{digest}.json"


def get_cached_result(key: str) -> dict | None:
    cache_file = CACHE_DIR / key
    if not cache_file.exists():
        return None
    try:
        stat = cache_file.stat()
        age = time.time() - stat.st_mtime
        if age > CACHE_TTL_SECONDS:
            return None
        with cache_file.open() as handle:
            data = json.load(handle)
        data["_cache"] = {"hit": True, "age_seconds": int(age)}
        return data
    except (OSError, json.JSONDecodeError):
        return None


def set_cached_result(key: str, data: dict) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = CACHE_DIR / key
        with cache_file.open("w") as handle:
            json.dump(data, handle)
    except OSError:
        return


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


def extract_frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    raw = text[3:end]
    if yaml is not None:
        try:
            loaded = yaml.safe_load(raw)
            if isinstance(loaded, dict):
                return loaded
        except Exception:
            pass

    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"\'')
    return meta


def parse_meta(path: Path) -> dict:
    meta = extract_frontmatter(path)
    name = str(meta.get("name") or path.parent.name).strip()
    description = str(meta.get("description") or "").strip()
    nested_meta = meta.get("metadata") if isinstance(meta.get("metadata"), dict) else {}
    tags = coerce_list(meta.get("tags")) + coerce_list(nested_meta.get("tags") if isinstance(nested_meta, dict) else [])
    triggers = coerce_list(meta.get("triggers")) + coerce_list(meta.get("legacy_aliases"))
    aliases = coerce_list(meta.get("aliases")) + coerce_list(meta.get("related_skills"))
    return {
        "name": name,
        "description": description,
        "tags": sorted({item for item in tags if item}),
        "triggers": sorted({item for item in triggers if item}),
        "aliases": sorted({item for item in aliases if item}),
        "raw": meta,
    }


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


def catalog_rows(include_hidden: bool = True) -> list[dict]:
    rows = []
    for skill_md in sorted(SKILLS_DB_DIR.rglob("SKILL.md")):
        rel = skill_md.relative_to(SKILLS_DB_DIR)
        if len(rel.parts) < 2:
            continue
        category = rel.parts[0]
        if not include_hidden and category in HARD_HIDDEN_CATEGORIES:
            continue
        meta = parse_meta(skill_md)
        rows.append(
            {
                "category": category,
                "name": meta["name"],
                "description": meta["description"],
                "path": str(skill_md),
            }
        )
    return rows


def load_skill_graph() -> dict[str, dict]:
    if not SKILL_GRAPH_FILE.exists():
        return {}
    try:
        data = json.loads(SKILL_GRAPH_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return {}

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
    category = dir_parts[0] if base_label == "skills-db" else "skills"
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


def default_lifecycle_for(row: dict) -> tuple[str, str]:
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
        data = default_state_document()
        SKILLS_STATE_FILE.write_text(json.dumps(data, indent=2) + "\n")
        return data
    try:
        return json.loads(SKILLS_STATE_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        data = default_state_document()
        SKILLS_STATE_FILE.write_text(json.dumps(data, indent=2) + "\n")
        return data


def candidate_handoff_dirs() -> list[Path]:
    explicit = os.environ.get("LEV_SKILLS_HANDOFF_DIR")
    dirs: list[Path] = []
    if explicit:
        path = Path(explicit).expanduser()
        if path.exists():
            dirs.append(path)
    cwd = Path.cwd().resolve()
    for parent in [cwd, *cwd.parents]:
        handoffs = parent / ".lev" / "pm" / "handoffs"
        if handoffs.exists() and handoffs not in dirs:
            dirs.append(handoffs)
            break
    return dirs


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


def extract_usage_counts(rows: list[dict]) -> Counter[str]:
    alias_map = build_alias_map(rows)
    resolved: Counter[str] = Counter()

    for handoff_dir in candidate_handoff_dirs():
        for path in handoff_dir.rglob("*.md"):
            try:
                text = path.read_text(errors="ignore")
            except OSError:
                continue
            for alias in parse_usage_markers(text):
                key = resolve_alias(alias_map, alias)
                if key:
                    resolved[key] += 1

    if CASS_DB_PATH.exists():
        try:
            conn = sqlite3.connect(CASS_DB_PATH)
            cursor = conn.cursor()
            query = (
                "SELECT content FROM messages "
                "WHERE content LIKE '%Loaded `%' "
                "OR content LIKE '%Using skills:%' "
                "OR content LIKE '%skill://%'"
            )
            for (content,) in cursor.execute(query):
                for alias in parse_usage_markers(content):
                    key = resolve_alias(alias_map, alias)
                    if key:
                        resolved[key] += 1
            conn.close()
        except sqlite3.Error:
            pass

    return resolved


def usage_tier(count: int) -> str:
    if count >= 10:
        return "hot"
    if count >= 3:
        return "warm"
    if count >= 1:
        return "cold"
    return "none"


def build_inventory(force_rebuild: bool = False) -> list[dict]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if not force_rebuild and INVENTORY_CACHE_FILE.exists():
        age = time.time() - INVENTORY_CACHE_FILE.stat().st_mtime
        if age < CACHE_TTL_SECONDS:
            try:
                return json.loads(INVENTORY_CACHE_FILE.read_text())
            except (OSError, json.JSONDecodeError):
                pass

    state_db = load_state_db()
    rows: list[dict] = []

    for skill_md in sorted(SKILLS_DIR.rglob("SKILL.md")):
        rel = skill_md.relative_to(SKILLS_DIR)
        if rel.parts[0] == ".system":
            continue
        rows.append(build_skill_row("skills", skill_md, rel.parts))

    for skill_md in sorted(SKILLS_DB_DIR.rglob("SKILL.md")):
        rel = skill_md.relative_to(SKILLS_DB_DIR)
        if len(rel.parts) < 2:
            continue
        rows.append(build_skill_row("skills-db", skill_md, rel.parts))

    usage_counts = extract_usage_counts(rows)
    overrides = state_db.get("skills", {}) if isinstance(state_db, dict) else {}
    graph_nodes = load_skill_graph()

    enriched: list[dict] = []
    for row in rows:
        graph_entry = graph_entry_for(row, graph_nodes)
        graph_id = str(graph_entry.get("id") or "") if graph_entry else ""
        graph_lane = str(graph_entry.get("lane") or "") if graph_entry else ""
        graph_lifecycle = str(graph_entry.get("lifecycle") or "") if graph_entry else ""
        graph_source = str(graph_entry.get("source_project") or "") if graph_entry else ""
        graph_tags = coerce_list(graph_entry.get("tags")) if graph_entry else []
        graph_neighbors = coerce_list(graph_entry.get("_neighbors")) if graph_entry else []
        graph_degree = int(graph_entry.get("_degree") or 0) if graph_entry else 0
        lifecycle, rotation_role = default_lifecycle_for(row)
        override = overrides.get(row["path_key"], {}) if isinstance(overrides, dict) else {}
        lifecycle = override.get("lifecycle", lifecycle)
        rotation_role = override.get("rotation_role", rotation_role)
        merged_tags = set(row.get("tags", [])) | set(row.get("triggers", [])) | set(row.get("aliases", []))
        merged_tags |= set(token for token in row["path_tokens"] if token)
        merged_tags |= set(token for token in row["category_tokens"] if token)
        merged_tags |= set(graph_tags)
        merged_tags |= set(tokenize(graph_lane))
        merged_tags |= set(tokenize(graph_source))
        merged_tags |= set(override.get("intent_tags", [])) if isinstance(override, dict) else set()
        usage_count = int(override.get("usage_count", usage_counts.get(row["path_key"], 0))) if isinstance(override, dict) else int(usage_counts.get(row["path_key"], 0))
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
        graph_tokens = sorted(set(tokenize(" ".join([graph_id, graph_lane, graph_source, *graph_tags, *graph_neighbors]))))
        enriched.append(
            {
                **row,
                "lifecycle": lifecycle,
                "rotation_role": rotation_role,
                "usage_count": usage_count,
                "usage_tier": usage_tier(usage_count),
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
                "rotation_weight": float(override.get("rotation_weight", 1.0)) if isinstance(override, dict) else 1.0,
                "notes": override.get("notes", "") if isinstance(override, dict) else "",
                "anomaly": "nested-under-skill" if row["surface"] == "catalog-nested" and row["parent_skill"] else "",
            }
        )

    enriched.sort(key=lambda item: (item["base"], item["path_key"]))
    SKILLS_INVENTORY_FILE.write_text(
        "".join(json.dumps(item, sort_keys=True) + "\n" for item in enriched)
    )
    INVENTORY_CACHE_FILE.write_text(json.dumps(enriched))
    return enriched


def filtered_inventory(
    rows: list[dict],
    *,
    category: str | None = None,
    include_hidden: bool = False,
    rotation_roles: set[str] | None = None,
) -> list[dict]:
    output = []
    category_norm = normalize_name(category or "")
    for row in rows:
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
    desc_tokens = set(row["description_tokens"])
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
    category: str | None = None,
    include_hidden: bool = False,
    rotation_roles: set[str] | None = None,
    force_rebuild: bool = False,
    limit: int = 30,
) -> list[dict]:
    rows = build_inventory(force_rebuild=force_rebuild)
    candidates = filtered_inventory(rows, category=category, include_hidden=include_hidden, rotation_roles=rotation_roles)
    query_terms = tokenize(query)
    matches = []
    for row in candidates:
        score, matched_terms = score_row(row, query, query_terms)
        if score <= 0:
            continue
        matches.append(
            {
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
                "doc_type": "skill",
                "source": "inventory",
                "anomaly": row.get("anomaly", ""),
            }
        )
    if matches:
        best_term_count = max(len(item["matched_terms"]) for item in matches)
        if best_term_count >= 2:
            matches = [item for item in matches if len(item["matched_terms"]) == best_term_count]
    matches.sort(key=lambda item: (-item["adjusted_score"], item["skill_name"].lower(), item["path_key"]))
    return matches[:limit]


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


def cmd_discover(args: list[str]) -> int:
    if not args:
        print("error: discover requires a query", file=sys.stderr)
        return 1

    query = ""
    json_mode = False
    no_cache = False
    category = None
    all_collections = True
    limit = 30

    for arg in args:
        if arg == "--json":
            json_mode = True
        elif arg == "--no-cache":
            no_cache = True
        elif arg == "--all":
            all_collections = True
        elif arg == "--primary-only":
            all_collections = False
        elif arg.startswith("--category="):
            category = arg.split("=", 1)[1]
        elif arg.startswith("--limit="):
            limit = max(1, int(arg.split("=", 1)[1]))
        elif arg == "--limit":
            continue
        elif arg.isdigit() and query:
            limit = max(1, int(arg))
        else:
            query = arg

    if not query:
        print("error: discover requires a query", file=sys.stderr)
        return 1

    if json_mode and not no_cache:
        key = cache_key(query, category, all_collections, mode="discover")
        cached = get_cached_result(key)
        if cached:
            print(json.dumps(cached, indent=2))
            return 0

    matches = discover_matches(query, category=category, force_rebuild=no_cache, limit=limit)
    payload = discover_payload(query, matches, category)

    if json_mode:
        key = cache_key(query, category, all_collections, mode="discover")
        set_cached_result(key, payload)
        payload["_cache"] = {"hit": False, "age_seconds": 0}
        print(json.dumps(payload, indent=2))
        return 0

    return print_discover_text(payload)


def cmd_pick(args: list[str]) -> int:
    if not args:
        print("error: pick requires a query", file=sys.stderr)
        return 1

    query = ""
    json_mode = False
    no_cache = False
    category = None
    rotation = "eligible,experimental"

    for arg in args:
        if arg == "--json":
            json_mode = True
        elif arg == "--no-cache":
            no_cache = True
        elif arg.startswith("--category="):
            category = arg.split("=", 1)[1]
        elif arg.startswith("--rotation="):
            rotation = arg.split("=", 1)[1]
        else:
            query = arg

    if not query:
        print("error: pick requires a query", file=sys.stderr)
        return 1

    rotation_roles = parse_rotation_roles(rotation) or {"eligible", "experimental"}
    matches = discover_matches(
        query,
        category=category,
        rotation_roles=rotation_roles,
        force_rebuild=no_cache,
    )
    if not matches:
        payload = {"query": query, "rotation_roles": sorted(rotation_roles), "picked": None, "candidates": []}
        if json_mode:
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
        "query": query,
        "rotation_roles": sorted(rotation_roles),
        "picked": picked,
        "candidates": top_candidates,
    }
    if json_mode:
        print(json.dumps(payload, indent=2))
        return 0
    print(
        f"{picked['skill_name']} [{picked['category']}/{picked['rotation_role']}] "
        f"usage={picked['usage_count']} :: {picked['local_path']}"
    )
    return 0


def cmd_inventory(args: list[str]) -> int:
    json_mode = "--json" in args
    include_hidden = "--include-hidden" in args
    rebuild = "--rebuild" in args or "--no-cache" in args
    rows = build_inventory(force_rebuild=rebuild)
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
    """Refresh qmd indexes and rebuild inventory."""

    repo_local = "--repo-local" in args
    try:
        if repo_local:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                print("warning: not in a git repo, skipping repo-local qmd refresh", file=sys.stderr)
            else:
                print("Refreshing qmd index for repo-local workflow")
                subprocess.run(["qmd", "update"], timeout=180, check=False)
        else:
            print("Refreshing full qmd index...")
            subprocess.run(["qmd", "update"], timeout=180, check=False)
            print("Done. Running embed pass...")
            subprocess.run(["qmd", "embed", "-f"], timeout=600, check=False)
        build_inventory(force_rebuild=True)
        print(f"Inventory rebuilt at {SKILLS_INVENTORY_FILE}")
        return 0
    except subprocess.TimeoutExpired:
        print("error: refresh timed out", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print("error: qmd not found in PATH", file=sys.stderr)
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

    print("\nTier 2: visible skills-db catalog")
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
    try:
        with skill_md_path.open(errors="ignore") as f:
            first = f.readline()
            if first.strip() != "---":
                return errors

            for line_num, line in enumerate(f, start=2):
                if line.strip() == "---":
                    break

                if line and not line[0].isspace() and ":" in line:
                    key = line.split(":", 1)[0].strip()
                    if key and key not in supported_attrs:
                        rel_path = skill_md_path.relative_to(ROOT)
                        errors.append(
                            f"{rel_path}:{line_num} unsupported attribute '{key}' "
                            f"(supported: {', '.join(sorted(supported_attrs))})"
                        )
    except Exception as e:  # pragma: no cover - validation fallback
        rel_path = skill_md_path.relative_to(ROOT)
        errors.append(f"{rel_path} error reading file: {e}")

    return errors


def cmd_validate() -> int:
    active = active_skill_rows()
    cdo_rows = cdo_subskill_rows()
    workflow_rows = workflow_flow_rows()
    catalog = catalog_rows(include_hidden=False)

    errors = []
    warnings = []

    for skill_md in sorted(SKILLS_DIR.rglob("SKILL.md")):
        if skill_md.parent.name == ".system":
            continue
        errors.extend(validate_skill_yaml(skill_md))

    for skill_md in sorted(SKILLS_DB_DIR.rglob("SKILL.md")):
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
    if command == "inventory":
        return cmd_inventory(args)
    if command == "list":
        return cmd_list()
    if command == "validate":
        return cmd_validate()
    if command == "refresh":
        return cmd_refresh(args)

    if command.startswith("-"):
        print(f"unknown option: {command}", file=sys.stderr)
        return 1

    return cmd_discover(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
