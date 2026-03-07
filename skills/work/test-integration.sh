#!/bin/bash
# Work Skill Integration Test
# Tests basic functionality and integration points

set -e

echo "🧪 Work Skill Integration Tests"
echo "================================"
echo ""

# Test 1: SKILL.md exists
echo "Test 1: SKILL.md exists"
if [ -f ~/.claude/skills/work/SKILL.md ]; then
    echo "✅ PASS: SKILL.md found"
else
    echo "❌ FAIL: SKILL.md not found"
    exit 1
fi
echo ""

# Test 2: README.md exists
echo "Test 2: README.md exists"
if [ -f ~/.claude/skills/work/README.md ]; then
    echo "✅ PASS: README.md found"
else
    echo "❌ FAIL: README.md not found"
    exit 1
fi
echo ""

# Test 3: Templates directory exists
echo "Test 3: Templates directory exists"
if [ -d ~/.claude/skills/work/templates ]; then
    echo "✅ PASS: templates/ directory found"
else
    echo "❌ FAIL: templates/ directory not found"
    exit 1
fi
echo ""

# Test 4: report.md template exists
echo "Test 4: report.md template exists"
if [ -f ~/.claude/skills/work/templates/report.md ]; then
    echo "✅ PASS: report.md template found"
else
    echo "❌ FAIL: report.md template not found"
    exit 1
fi
echo ""

# Test 5: Lev router updated
echo "Test 5: Lev master router integration"
if grep -q "work.*lifecycle router" ~/.claude/skills/lev/SKILL.md; then
    echo "✅ PASS: Lev router includes work skill"
else
    echo "❌ FAIL: Lev router not updated"
    exit 1
fi
echo ""

# Test 6: Output directories exist
echo "Test 6: Output directories"
for dir in reports proposals plans handoffs; do
    mkdir -p ~/.lev/pm/$dir 2>/dev/null || true
    if [ -d ~/.lev/pm/$dir ]; then
        echo "✅ PASS: .lev/pm/$dir exists"
    else
        echo "⚠️  WARN: .lev/pm/$dir not found (will create on first use)"
    fi
done
echo ""

# Test 7: Skill discovery
echo "Test 7: Skill discovery via lev get"
if command -v lev &> /dev/null; then
    if lev get "work skill" --scope=knowledge 2>/dev/null | grep -q "work"; then
        echo "✅ PASS: Work skill discoverable via lev get"
    else
        echo "⚠️  WARN: Work skill not indexed (run lev index build)"
    fi
else
    echo "⚠️  WARN: lev CLI not available (optional)"
fi
echo ""

# Test 8: BD availability
echo "Test 8: BD integration"
if command -v bd &> /dev/null; then
    echo "✅ PASS: BD CLI available"
else
    echo "⚠️  WARN: BD CLI not available (optional, will degrade gracefully)"
fi
echo ""

# Test 9: YAML frontmatter validation
echo "Test 9: Template YAML frontmatter"
if head -20 ~/.claude/skills/work/templates/report.md | grep -q "^---$"; then
    echo "✅ PASS: report.md has YAML frontmatter"
else
    echo "❌ FAIL: report.md missing YAML frontmatter"
    exit 1
fi
echo ""

# Test 10: File permissions
echo "Test 10: File permissions"
if [ -r ~/.claude/skills/work/SKILL.md ]; then
    echo "✅ PASS: SKILL.md readable"
else
    echo "❌ FAIL: SKILL.md not readable"
    exit 1
fi
echo ""

# Summary
echo "================================"
echo "Integration Test Summary"
echo "================================"
echo ""
echo "✅ Core files present"
echo "✅ Lev router integration complete"
echo "✅ Template system ready"
echo "✅ Output directories prepared"
echo ""
echo "⚠️  Optional dependencies:"
echo "   - lev CLI (for skill discovery)"
echo "   - BD CLI (for task tracking)"
echo ""
echo "Status: READY FOR USE"
echo ""
echo "Quick start:"
echo '  work "Analyze something interesting"'
echo ""
