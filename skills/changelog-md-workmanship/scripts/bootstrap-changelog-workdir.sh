#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
assets_dir="$skill_dir/assets"

target_dir="."
force="false"
huge="false"

for arg in "$@"; do
  case "$arg" in
    --force)
      force="true"
      ;;
    --huge)
      huge="true"
      ;;
    *)
      target_dir="$arg"
      ;;
  esac
done

mkdir -p "$target_dir"

copy_if_needed() {
  local src="$1"
  local dst="$2"

  if [[ -e "$dst" && "$force" != "true" ]]; then
    echo "skip: $dst already exists"
    return 0
  fi

  cp "$src" "$dst"
  echo "write: $dst"
}

if [[ "$huge" == "true" ]]; then
  copy_if_needed "$assets_dir/CHANGELOG-TEMPLATE-HUGE.md" "$target_dir/CHANGELOG.md"
  mkdir -p "$target_dir/CHANGELOG_RESEARCH"
  copy_if_needed "$assets_dir/CHANGELOG-COVERAGE-LEDGER-TEMPLATE.md" "$target_dir/CHANGELOG_RESEARCH/COVERAGE-LEDGER.md"
  copy_if_needed "$assets_dir/CHANGELOG-RESEARCH-OVERVIEW-TEMPLATE.md" "$target_dir/CHANGELOG_RESEARCH/00-overview.md"
  copy_if_needed "$assets_dir/CHANGELOG-RESEARCH-CHUNK-TEMPLATE.md" "$target_dir/CHANGELOG_RESEARCH/01-version-spine.md"
  copy_if_needed "$assets_dir/CHANGELOG-RESEARCH-CHUNK-TEMPLATE.md" "$target_dir/CHANGELOG_RESEARCH/02-history-chunk-a.md"
  copy_if_needed "$assets_dir/CHANGELOG-RESEARCH-CHUNK-TEMPLATE.md" "$target_dir/CHANGELOG_RESEARCH/03-history-chunk-b.md"
  copy_if_needed "$assets_dir/CHANGELOG-RESEARCH-CHUNK-TEMPLATE.md" "$target_dir/CHANGELOG_RESEARCH/99-open-questions.md"
else
  copy_if_needed "$assets_dir/CHANGELOG-TEMPLATE.md" "$target_dir/CHANGELOG.md"
  copy_if_needed "$assets_dir/CHANGELOG-RESEARCH-TEMPLATE.md" "$target_dir/CHANGELOG_RESEARCH.md"
fi

cat <<EOF

Bootstrapped changelog workspace in: $target_dir

Suggested next steps:
  1. Read AGENTS.md and README.md
  2. Run: scripts/build-version-spine.py --repo "$target_dir"
  3. Run: scripts/extract-tracker-workstreams.py --repo "$target_dir" --format markdown
  4. Start chunked research and update CHANGELOG.md after each chunk
  5. Optionally cluster commits with: scripts/cluster-history.py --repo "$target_dir"
  6. Audit with: scripts/validate-changelog-md.py "$target_dir/CHANGELOG.md"
EOF
