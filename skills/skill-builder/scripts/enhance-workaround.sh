#!/usr/bin/env bash
# enhance-workaround.sh — Pipes skill-seekers enhance prompts to claude correctly.
#
# KNOWN BUG: some `skill-seekers enhance` versions pass a file path as a
# positional arg to `claude`. Claude CLI treats it as a literal string, not
# file contents, so SKILL.md is left unchanged.
#
# This wrapper:
# 1. Discovers the Python interpreter behind the installed `skill-seekers` CLI
# 2. Generates the prompt using the installed LocalSkillEnhancer API
# 3. Pipes that prompt to `claude -p`
#
# Usage:
#   ./enhance-workaround.sh output/oracle
#   ./enhance-workaround.sh output/react --timeout 900
#   ./enhance-workaround.sh output/react 900
#
# Requirements: skill-seekers, claude CLI, timeout/gtimeout

set -euo pipefail

usage() {
    cat <<'EOF'
Usage: enhance-workaround.sh <skill-dir> [--timeout N]

Examples:
  enhance-workaround.sh output/react
  enhance-workaround.sh output/react --timeout 900
  enhance-workaround.sh output/react 900
EOF
}

if [ "${1:-}" = "" ] || [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
    usage
    exit 0
fi

SKILL_DIR="$1"
shift || true
TIMEOUT=600

while [ "$#" -gt 0 ]; do
    case "$1" in
        --timeout)
            TIMEOUT="${2:?Missing value for --timeout}"
            shift 2
            ;;
        ''|*[!0-9]*)
            echo "❌ Unknown argument: $1" >&2
            usage >&2
            exit 1
            ;;
        *)
            TIMEOUT="$1"
            shift
            ;;
    esac
done

if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ Skill directory not found: $SKILL_DIR" >&2
    exit 1
fi

if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ SKILL.md not found in: $SKILL_DIR" >&2
    exit 1
fi

if ! command -v skill-seekers >/dev/null 2>&1; then
    echo "❌ skill-seekers is not installed or not on PATH" >&2
    exit 1
fi

if ! command -v claude >/dev/null 2>&1; then
    echo "❌ claude CLI is not installed or not on PATH" >&2
    exit 1
fi

TIMEOUT_BIN=""
if command -v timeout >/dev/null 2>&1; then
    TIMEOUT_BIN="timeout"
elif command -v gtimeout >/dev/null 2>&1; then
    TIMEOUT_BIN="gtimeout"
else
    echo "❌ timeout/gtimeout is required" >&2
    exit 1
fi

resolve_skill_seekers_python() {
    local wrapper first_line interpreter
    wrapper="$(command -v skill-seekers)"
    first_line="$(head -n 1 "$wrapper" 2>/dev/null || true)"
    if [ "${first_line#\#!}" != "$first_line" ]; then
        interpreter="${first_line#\#!}"
        if [ -x "$interpreter" ]; then
            printf '%s\n' "$interpreter"
            return 0
        fi
    fi

    if command -v python3 >/dev/null 2>&1; then
        printf '%s\n' "$(command -v python3)"
        return 0
    fi

    return 1
}

PYTHON_BIN="$(resolve_skill_seekers_python)" || {
    echo "❌ Could not resolve a Python interpreter for skill-seekers" >&2
    exit 1
}

PROMPT_FILE="$(mktemp "/tmp/enhance_prompt_$(basename "$SKILL_DIR").XXXXXX.txt")"

cleanup_success() {
    rm -f "$PROMPT_FILE"
}

echo "=== Enhance Workaround: $(basename "$SKILL_DIR") ==="
echo ""
echo "🐍 Python: $PYTHON_BIN"
echo "⏱️  Timeout: ${TIMEOUT}s"
echo ""

# Step 1: Generate enhance prompt using the installed skill-seekers API.
echo "📝 Generating enhance prompt..."
SKILL_DIR="$SKILL_DIR" PROMPT_FILE="$PROMPT_FILE" "$PYTHON_BIN" - <<'PY'
from inspect import signature
from os import environ

from skill_seekers.cli.enhance_skill_local import LocalSkillEnhancer

skill_dir = environ["SKILL_DIR"]
prompt_file = environ["PROMPT_FILE"]
enhancer = LocalSkillEnhancer(skill_dir)

kwargs = {}
params = signature(LocalSkillEnhancer.create_enhancement_prompt).parameters
if "use_summarization" in params:
    kwargs["use_summarization"] = True

prompt = enhancer.create_enhancement_prompt(**kwargs)
if not prompt:
    raise SystemExit("No enhancement prompt generated")

with open(prompt_file, "w", encoding="utf-8") as handle:
    handle.write(prompt)

print(f"   Prompt: {len(prompt):,} chars -> {prompt_file}")
PY

# Step 2: Backup current SKILL.md
cp "$SKILL_DIR/SKILL.md" "$SKILL_DIR/SKILL.md.backup"
echo "💾 Backed up SKILL.md → SKILL.md.backup"

# Step 3: Pipe to claude
echo "✨ Piping to claude -p..."
echo ""
(
    cd "$SKILL_DIR"
    cat "$PROMPT_FILE" | \
        "$TIMEOUT_BIN" "$TIMEOUT" claude -p \
            --dangerously-skip-permissions \
            --allowedTools "Read,Write,Edit,Glob,Grep"
)

# Step 4: Verify
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo ""
    echo "❌ SKILL.md not found after enhance" >&2
    echo "Prompt kept at: $PROMPT_FILE" >&2
    exit 1
fi

NEW_SIZE="$(wc -c < "$SKILL_DIR/SKILL.md")"

if cmp -s "$SKILL_DIR/SKILL.md" "$SKILL_DIR/SKILL.md.backup"; then
    echo ""
    echo "❌ SKILL.md was unchanged after enhance" >&2
    echo "Prompt kept at: $PROMPT_FILE" >&2
    exit 1
fi

cleanup_success

echo ""
echo "✅ Done. SKILL.md: ${NEW_SIZE} bytes"
