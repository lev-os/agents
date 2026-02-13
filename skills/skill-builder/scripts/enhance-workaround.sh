#!/usr/bin/env bash
# enhance-workaround.sh — Pipes skill-seekers enhance prompt to claude correctly.
#
# KNOWN BUG: `skill-seekers enhance` passes a file path as a positional arg
# to `claude`. Claude CLI treats it as a literal string, not file contents.
# The SKILL.md never gets updated.
#
# This script generates the prompt via Python and pipes it to claude -p.
#
# Usage:
#   ./enhance-workaround.sh output/oracle
#   ./enhance-workaround.sh output/react --timeout 900
#
# Requirements: skill-seekers, claude CLI, python3

set -euo pipefail

SKILL_DIR="${1:?Usage: enhance-workaround.sh <skill-dir> [--timeout N]}"
TIMEOUT="${2:-600}"
PROMPT_FILE="/tmp/enhance_prompt_$(basename "$SKILL_DIR").txt"

# Resolve skill-seekers package path
SS_PATH=$(python3 -c "import skill_seekers; import os; print(os.path.dirname(skill_seekers.__path__[0]))")

echo "=== Enhance Workaround: $(basename "$SKILL_DIR") ==="
echo ""

# Step 1: Generate enhance prompt
echo "📝 Generating enhance prompt..."
python3 -c "
import sys
sys.path.insert(0, '$SS_PATH')
from skill_seekers.cli.enhance_skill_local import LocalSkillEnhancer
e = LocalSkillEnhancer('$SKILL_DIR')
prompt = e.create_enhancement_prompt(use_summarization=True)
with open('$PROMPT_FILE', 'w') as f:
    f.write(prompt)
print(f'   Prompt: {len(prompt):,} chars → $PROMPT_FILE')
"

# Step 2: Backup current SKILL.md
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    cp "$SKILL_DIR/SKILL.md" "$SKILL_DIR/SKILL.md.backup"
    echo "💾 Backed up SKILL.md → SKILL.md.backup"
fi

# Step 3: Pipe to claude
echo "✨ Piping to claude -p (timeout: ${TIMEOUT}s)..."
echo ""
cd "$SKILL_DIR" && \
    cat "$PROMPT_FILE" | \
    timeout "$TIMEOUT" claude -p \
    --dangerously-skip-permissions \
    --allowedTools "Read,Write,Edit,Glob,Grep"

# Step 4: Verify
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    NEW_SIZE=$(wc -c < "$SKILL_DIR/SKILL.md")
    echo ""
    echo "✅ Done. SKILL.md: ${NEW_SIZE} bytes"
else
    echo ""
    echo "❌ SKILL.md not found after enhance"
    exit 1
fi

# Cleanup
rm -f "$PROMPT_FILE"
