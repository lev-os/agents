#!/bin/bash
# Fast git sync with project code resolution
# Usage: gitsync [codes|paths...] [--dry-run]
#        gitsync all [--dry-run]

set -uo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; DIM='\033[2m'; NC='\033[0m'

# Resolve symlinks to get real script directory (macOS compatible)
_resolve_path() {
    local target="$1"
    while [ -L "$target" ]; do
        local link=$(readlink "$target")
        if [[ "$link" = /* ]]; then
            target="$link"
        else
            target="$(dirname "$target")/$link"
        fi
    done
    echo "$target"
}
REAL_SCRIPT="$(_resolve_path "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$REAL_SCRIPT")/.." && pwd)"

# XDG-compliant paths - lev is source of truth
LEV_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/lev"
LEV_DATA="${XDG_DATA_HOME:-$HOME/.local/share}/lev"

# Priority: lev config > lev data > local fallback
if [ -f "$LEV_CONFIG/projects.yaml" ]; then
    PROJECTS_FILE="$LEV_CONFIG/projects.yaml"
    PROJECTS_FORMAT="yaml"
elif [ -f "$LEV_DATA/projects.json" ]; then
    PROJECTS_FILE="$LEV_DATA/projects.json"
    PROJECTS_FORMAT="json"
else
    PROJECTS_FILE="$SCRIPT_DIR/projects.json"
    PROJECTS_FORMAT="json"
fi
DRY_RUN=0
CONFLICTS=()
SYNCED=()
SKIPPED=()
DIRTY=()

# Parse --dry-run from args
TARGETS=()
for arg in "$@"; do
    case "$arg" in
        --dry-run|-n) DRY_RUN=1 ;;
        *) TARGETS+=("$arg") ;;
    esac
done

# Resolve project code to path
resolve_code() {
    local code="$1"
    local path=""

    if [ -f "$PROJECTS_FILE" ]; then
        if [ "$PROJECTS_FORMAT" = "yaml" ]; then
            # Parse YAML (lev format: projects.<name>.path)
            path=$(python3 -c "
import yaml, os
with open('$PROJECTS_FILE') as f:
    data = yaml.safe_load(f) or {}
code = '$code'
projects = data.get('projects', {})
# Check aliases first
if code in data.get('aliases', {}):
    code = data['aliases'][code]
# Look up project by name
if code in projects:
    p = projects[code]
    if isinstance(p, dict):
        print(os.path.expanduser(p.get('path', '')))
    else:
        print(os.path.expanduser(p))
" 2>/dev/null)
        else
            # Parse JSON (gitsync format: projects.<code> = path)
            path=$(python3 -c "
import json, os
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
code = '$code'
# Check aliases first
if code in data.get('aliases', {}):
    code = data['aliases'][code]
# Look up project
if code in data.get('projects', {}):
    p = data['projects'][code]
    if isinstance(p, dict):
        print(os.path.expanduser(p.get('path', '')))
    else:
        print(os.path.expanduser(p))
" 2>/dev/null)
        fi
    fi

    if [ -n "$path" ] && [ -d "$path" ]; then
        echo "$path"
        return 0
    fi

    # Fallback: treat as path
    local expanded=$(eval echo "$code" 2>/dev/null)
    if [ -d "$expanded" ]; then
        echo "$(cd "$expanded" && pwd)"
        return 0
    fi

    return 1
}

# Find all dirty repos from registered projects
find_dirty() {
    if [ ! -f "$PROJECTS_FILE" ]; then
        echo -e "${RED}No projects file found${NC}" >&2
        return 1
    fi

    local paths
    if [ "$PROJECTS_FORMAT" = "yaml" ]; then
        paths=$(python3 -c "
import yaml, os
with open('$PROJECTS_FILE') as f:
    data = yaml.safe_load(f) or {}
for name, proj in data.get('projects', {}).items():
    if isinstance(proj, dict):
        print(os.path.expanduser(proj.get('path', '')))
    else:
        print(os.path.expanduser(proj))
" 2>/dev/null)
    else
        paths=$(python3 -c "
import json, os
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
for code, proj in data.get('projects', {}).items():
    if isinstance(proj, dict):
        print(os.path.expanduser(proj.get('path', '')))
    else:
        print(os.path.expanduser(proj))
" 2>/dev/null)
    fi

    local proj_path dirty ahead
    while IFS= read -r proj_path; do
        [ -d "$proj_path/.git" ] || continue
        dirty=$(git -C "$proj_path" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
        ahead=$(git -C "$proj_path" rev-list --count @{u}..HEAD 2>/dev/null || echo 0)
        if [ "$dirty" -gt 0 ] || [ "${ahead:-0}" -gt 0 ]; then
            echo "$proj_path"
        fi
    done <<< "$paths"
}

# Flush bd changes if .beads/ exists
flush_bd() {
    local dir="$1"
    [ -d "$dir/.beads" ] || return 0

    if [ "$DRY_RUN" -eq 1 ]; then
        printf "${CYAN}bd${NC} "
        return 0
    fi

    # Run bd from the repo directory (it auto-discovers .beads/)
    pushd "$dir" >/dev/null 2>&1 || return 0

    # Check if daemon is running (has socket)
    if [ -S ".beads/bd.sock" ]; then
        # Daemon handles sync, just signal flush
        bd sync --flush-only -q 2>/dev/null && printf "${GREEN}b${NC}" || printf "."
    else
        # No daemon, full sync (but skip git ops - gitsync handles that)
        bd sync --flush-only -q 2>/dev/null && printf "${GREEN}B${NC}" || printf "."
    fi

    popd >/dev/null 2>&1
}

# Import bd changes after pull
import_bd() {
    local dir="$1"
    [ -d "$dir/.beads" ] || return 0
    [ "$DRY_RUN" -eq 1 ] && return 0

    pushd "$dir" >/dev/null 2>&1 || return 0
    bd sync --import-only -q >/dev/null 2>&1
    popd >/dev/null 2>&1
}

# Sync a single repo
sync_one() {
    local dir="$1"
    cd "$dir" 2>/dev/null || { echo -e "${RED}✗ $dir (not found)${NC}"; return 1; }
    git rev-parse --git-dir &>/dev/null || return 0

    local branch=$(git branch --show-current 2>/dev/null || echo "detached")
    local name=$(basename "$dir")
    local dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    local ahead=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo 0)

    if [ "$DRY_RUN" -eq 1 ]; then
        if [ "$dirty" -gt 0 ] || [ "${ahead:-0}" -gt 0 ]; then
            printf "${CYAN}%-25s${NC} %-15s ${YELLOW}D${NC} " "$name" "($branch)"
            [ "$dirty" -gt 0 ] && printf "${DIM}%s dirty${NC} " "$dirty"
            [ "${ahead:-0}" -gt 0 ] && printf "${DIM}%s ahead${NC}" "$ahead"
            printf "\n"
            DIRTY+=("$dir")
        else
            printf "${DIM}%-25s %-15s .${NC}\n" "$name" "($branch)"
            SKIPPED+=("$dir")
        fi
        return 0
    fi

    printf "${BLUE}%-25s${NC} %-15s " "$name" "($branch)"

    # Flush bd first (if .beads/ exists)
    flush_bd "$dir"

    # Commit
    if [ "$dirty" -gt 0 ]; then
        git add . >/dev/null 2>&1
        git commit -m "sync $(date '+%m-%d %H:%M')" --no-verify -q >/dev/null 2>&1 && printf "${GREEN}C${NC}" || printf "."
    else
        printf "."
    fi

    # Pull
    local pull_out=$(git pull --no-rebase 2>&1)
    if echo "$pull_out" | grep -q "CONFLICT"; then
        printf " ${RED}CONFLICT${NC}\n"
        CONFLICTS+=("$dir")
        return 1
    else
        printf "${GREEN}P${NC}"
    fi

    # Import bd after pull (if .beads/ exists)
    import_bd "$dir"

    # Push
    git push -q 2>/dev/null && printf "${GREEN}U${NC}" || printf "."
    printf " ${GREEN}✓${NC}\n"
    SYNCED+=("$dir")
}

# Process a repo + worktrees + submodules
process_repo() {
    local main="$1"
    sync_one "$main"

    # Worktrees
    cd "$main" 2>/dev/null || return
    git worktree list --porcelain 2>/dev/null | grep "^worktree " | cut -d' ' -f2 | while read wt; do
        [ "$wt" = "$main" ] && continue
        [ -d "$wt" ] && sync_one "$wt"
    done

    # Submodules
    [ -f "$main/.gitmodules" ] || return 0
    cd "$main"
    while IFS= read -r sm; do
        [ -d "$sm" ] && sync_one "$sm"
    done < <(git submodule foreach --quiet 'echo $toplevel/$sm_path' 2>/dev/null || true)
}

# Header
if [ "$DRY_RUN" -eq 1 ]; then
    echo -e "${CYAN}gitsync --dry-run${NC} - D=dirty .=clean\n"
else
    echo -e "${BLUE}gitsync${NC} - C=commit P=pull U=push\n"
fi

# Get all registered project paths
all_projects() {
    if [ ! -f "$PROJECTS_FILE" ]; then
        echo -e "${RED}No projects file found${NC}" >&2
        return 1
    fi

    if [ "$PROJECTS_FORMAT" = "yaml" ]; then
        python3 -c "
import yaml, os
with open('$PROJECTS_FILE') as f:
    data = yaml.safe_load(f) or {}
for name, proj in data.get('projects', {}).items():
    if isinstance(proj, dict):
        path = proj.get('path', '')
    else:
        path = proj
    expanded = os.path.expanduser(path)
    if os.path.isdir(expanded):
        print(expanded)
" 2>/dev/null
    else
        python3 -c "
import json, os
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
for code, proj in data.get('projects', {}).items():
    if isinstance(proj, dict):
        path = proj.get('path', '')
    else:
        path = proj
    expanded = os.path.expanduser(path)
    if os.path.isdir(expanded):
        print(expanded)
" 2>/dev/null
    fi
}

# Handle "all" mode
if [ "${TARGETS[0]:-}" = "all" ]; then
    echo -e "${BLUE}Syncing all registered projects...${NC}\n"
    while IFS= read -r proj_path; do
        [ -n "$proj_path" ] && process_repo "$proj_path"
    done < <(all_projects)

    if [ "$DRY_RUN" -eq 1 ] && [ ${#DIRTY[@]} -eq 0 ]; then
        echo -e "${GREEN}All repos clean${NC}"
    fi
else
    # Resolve and process each target
    [ ${#TARGETS[@]} -eq 0 ] && TARGETS=(".")

    for target in "${TARGETS[@]}"; do
        resolved=$(resolve_code "$target")
        if [ $? -eq 0 ] && [ -n "$resolved" ]; then
            process_repo "$resolved"
        else
            echo -e "${RED}✗ Unknown project: $target${NC}"
        fi
    done
fi

# Report
echo ""
if [ "$DRY_RUN" -eq 1 ]; then
    [ ${#DIRTY[@]} -gt 0 ] && echo -e "${YELLOW}${#DIRTY[@]} repos need sync${NC}"
    [ ${#SKIPPED[@]} -gt 0 ] && echo -e "${DIM}${#SKIPPED[@]} repos clean${NC}"
elif [ ${#CONFLICTS[@]} -gt 0 ]; then
    echo -e "${RED}⚠ CONFLICTS:${NC}"
    printf '  %s\n' "${CONFLICTS[@]}"
    exit 1
else
    echo -e "${GREEN}Done${NC} - ${#SYNCED[@]} synced"
fi
