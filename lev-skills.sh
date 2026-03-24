#!/usr/bin/env python3
"""Skills runtime helper for the active surface and hidden catalog."""

import hashlib
import json
import os
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SKILLS_DIR = ROOT / "skills"
SKILLS_DB_DIR = ROOT / "skills-db"
DISCOVERY = SKILLS_DIR / "skill-discovery" / "skill-discovery"
WORKFLOW_FLOWS_DIR = SKILLS_DIR / "workflow" / "flows"
CDO_DIR = SKILLS_DIR / "cdo"
CACHE_DIR = Path(os.environ.get("LEV_CACHE_DIR", Path.home() / ".cache" / "lev-skills"))
CACHE_TTL_SECONDS = int(os.environ.get("LEV_SKILLS_CACHE_TTL", "300"))
CACHE_BG_REFRESH_AFTER = int(os.environ.get("LEV_SKILLS_BG_REFRESH_AFTER", "60"))

COMMAND_HOOKED = {
    "gitsync": "sync",
    "lev-intake": "intake",
    "cdo": "cdo",
    "ux": "ux",
    "interview": "interview",
    "work": "handoff",
}

ACTIVE_KEEP_FOLDERS = {
    "find-skills",
    "gitsync",
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


def usage() -> int:
    print(
        "\n".join(
            [
                "lev-skills.sh - skills runtime helper",
                "",
                "USAGE",
                '  lev-skills.sh discover "query" [--json] [--category=...] [--all] [--primary-only] [--no-cache]',
                "  lev-skills.sh list",
                "  lev-skills.sh validate",
                "  lev-skills.sh refresh [--repo-local]",
                "  lev-skills.sh help",
                "",
                "NOTES",
                "  discover searches all skills-* qmd collections by default",
                "  hidden catalog buckets (.archive, _todo, _workshop) are excluded from normal ranking",
                "",
                "OPTIONS",
                "  --category=NAME   Scope discovery to a specific domain/category",
                "  --all             Accepted for compatibility; all collections are already searched by default",
                "  --primary-only    Restrict discovery to skills-canonical + skills-db",
                "  --no-cache        Bypass discover cache",
                "  --repo-local      Refresh index for current repo only (pre-commit friendly)",
            ]
        )
    )
    return 0


def cache_key(query: str, category: str | None, all_collections: bool) -> str:
    parts = [query.lower().strip(), category or "", str(all_collections)]
    digest = hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]
    return f"discover-{digest}.json"


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


def parse_meta(path: Path) -> dict:
    """Read shallow frontmatter metadata for SKILL docs."""

    lines = []
    with path.open(errors="ignore") as handle:
        first = handle.readline()
        if first.strip() != "---":
            return {"name": path.parent.name, "description": ""}
        for line in handle:
            if line.strip() == "---":
                break
            lines.append(line.rstrip("\n"))
            if len(lines) >= 80:
                break

    name = ""
    description = ""
    for index, line in enumerate(lines):
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip("\"'")
        elif line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip("\"'")
            if description in {"|", ">", "|-", ">-"}:
                for cont in lines[index + 1 :]:
                    if cont.startswith("  "):
                        piece = cont.strip()
                        if piece:
                            description = piece
                            break
                    elif cont.strip():
                        break

    return {"name": name or path.parent.name, "description": description}


def normalize_name(name: str) -> str:
    return name.strip().lower().replace("_", "-")


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


def cmd_discover(args: list[str]) -> int:
    if not args:
        print("error: discover requires a query", file=sys.stderr)
        return 1

    query = ""
    json_mode = False
    no_cache = False
    category = None
    all_collections = True
    passthrough = []

    for arg in args:
        if arg == "--json":
            json_mode = True
            passthrough.append(arg)
        elif arg == "--no-cache":
            no_cache = True
        elif arg == "--all":
            all_collections = True
        elif arg == "--primary-only":
            all_collections = False
        elif arg.startswith("--category="):
            category = arg.split("=", 1)[1]
        else:
            query = arg

    if not query:
        print("error: discover requires a query", file=sys.stderr)
        return 1

    if json_mode and not no_cache:
        key = cache_key(query, category, all_collections)
        cached = get_cached_result(key)
        if cached:
            age = cached.get("_cache", {}).get("age_seconds", 0)
            if age >= CACHE_BG_REFRESH_AFTER:
                refresh_cmd = [
                    str(Path(__file__).resolve()),
                    "discover",
                    query,
                    "--json",
                    "--no-cache",
                ]
                if category:
                    refresh_cmd.append(f"--category={category}")
                if not all_collections:
                    refresh_cmd.append("--primary-only")
                subprocess.Popen(
                    refresh_cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,
                )
            print(json.dumps(cached, indent=2))
            return 0

    env = os.environ.copy()
    env["SKILL_DISCOVERY_ALL"] = "1" if all_collections else "0"
    if category:
        env["SKILL_DISCOVERY_CATEGORY"] = category

    result = subprocess.run(
        [str(DISCOVERY), query, *passthrough],
        capture_output=json_mode,
        text=True,
        env=env,
    )

    if json_mode and result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            key = cache_key(query, category, all_collections)
            set_cached_result(key, data)
            data["_cache"] = {"hit": False, "age_seconds": 0}
            print(json.dumps(data, indent=2))
            return 0
        except json.JSONDecodeError:
            print(result.stdout)
            return result.returncode

    if json_mode:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        return result.returncode
    return result.returncode


def cmd_refresh(args: list[str]) -> int:
    """Refresh qmd indexes for skills collections."""

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
                print("warning: not in a git repo, skipping repo-local refresh", file=sys.stderr)
                return 0
            print("Refreshing qmd index for repo-local workflow")
            subprocess.run(["qmd", "update"], timeout=180, check=False)
            return 0

        print("Refreshing full qmd index...")
        subprocess.run(["qmd", "update"], timeout=180, check=False)
        print("Done. Running embed pass...")
        subprocess.run(["qmd", "embed", "-f"], timeout=600, check=False)
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
                
                # Only check top-level keys (no leading spaces)
                if line and not line[0].isspace():
                    if ":" in line:
                        key = line.split(":", 1)[0].strip()
                        if key and key not in supported_attrs:
                            rel_path = skill_md_path.relative_to(ROOT)
                            errors.append(
                                f"{rel_path}:{line_num} unsupported attribute '{key}' "
                                f"(supported: {', '.join(sorted(supported_attrs))})"
                            )
    except Exception as e:
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
    
    # Validate all SKILL.md files for YAML frontmatter
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

    if command == "discover":
        return cmd_discover(args)
    if command == "list":
        return cmd_list()
    if command == "validate":
        return cmd_validate()
    if command == "refresh":
        return cmd_refresh(args)

    print(f"unknown command: {command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
