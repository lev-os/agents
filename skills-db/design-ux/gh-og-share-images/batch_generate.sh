#!/usr/bin/env bash
# Batch generate GitHub social preview images for all repos in ~/projects/
#
# Usage:
#   bash batch_generate.sh              # all repos in ~/projects/
#   bash batch_generate.sh --dry-run    # list repos without generating

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR="${SCRIPT_DIR}/generate_og_image.py"
PROJECTS_DIR="${HOME}/projects"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

generated=0
skipped=0
errors=0
total=0

echo "=== GitHub Social Preview Image Batch Generator ==="
echo "Projects dir: ${PROJECTS_DIR}"
echo "Generator: ${GENERATOR}"
echo ""

for repo_dir in "${PROJECTS_DIR}"/*/; do
    # Skip if not a git repo
    if [[ ! -d "${repo_dir}/.git" ]]; then
        continue
    fi

    total=$((total + 1))
    repo_name=$(basename "$repo_dir")

    # Check if it has a GitHub remote
    remote_url=$(git -C "$repo_dir" remote get-url origin 2>/dev/null || echo "")
    if [[ -z "$remote_url" ]] || [[ "$remote_url" != *github.com* ]]; then
        echo "SKIP  ${repo_name} (no GitHub remote)"
        skipped=$((skipped + 1))
        continue
    fi

    # Only process repos owned by Dicklesworthstone
    if [[ "$remote_url" != *Dicklesworthstone* ]] && [[ "$remote_url" != *dicklesworthstone* ]]; then
        echo "SKIP  ${repo_name} (not owned by you)"
        skipped=$((skipped + 1))
        continue
    fi

    if $DRY_RUN; then
        echo "WOULD ${repo_name}"
        continue
    fi

    echo "--- ${repo_name} ---"
    if python3 "$GENERATOR" "$repo_dir" 2>&1; then
        generated=$((generated + 1))
    else
        echo "ERROR ${repo_name}"
        errors=$((errors + 1))
    fi
    echo ""
done

echo "=== Summary ==="
echo "Total repos scanned: ${total}"
echo "Generated: ${generated}"
echo "Skipped: ${skipped}"
echo "Errors: ${errors}"
