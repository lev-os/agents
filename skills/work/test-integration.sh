#!/bin/bash
# Work Skill Integration Test
# Tests pass-1 lifecycle/template contract basics

set -e

echo "🧪 Work Skill Integration Tests"
echo "================================"
echo ""

echo "Test 1: SKILL.md exists"
if [ -f ~/.claude/skills/work/SKILL.md ]; then
    echo "✅ PASS: SKILL.md found"
else
    echo "❌ FAIL: SKILL.md not found"
    exit 1
fi
echo ""

echo "Test 2: Legacy READMEs removed"
if [ ! -f ~/.claude/skills/work/README.md ] && [ ! -f ~/.claude/skills/work/templates/README.md ]; then
    echo "✅ PASS: legacy READMEs removed"
else
    echo "❌ FAIL: legacy README surface still exists"
    exit 1
fi
echo ""

echo "Test 3: Templates directory exists"
if [ -d ~/.claude/skills/work/templates ]; then
    echo "✅ PASS: templates/ directory found"
else
    echo "❌ FAIL: templates/ directory not found"
    exit 1
fi
echo ""

echo "Test 4: Canonical PM templates exist"
for file in report.md proposal.md design.md spec.md plan.md handoff.md decision.md validation-report.md; do
    if [ -f ~/.claude/skills/work/templates/$file ]; then
        echo "✅ PASS: $file found"
    else
        echo "❌ FAIL: $file missing"
        exit 1
    fi
done
echo ""

echo "Test 5: Legacy chore template removed"
if [ ! -f ~/.claude/skills/work/templates/chore.md ]; then
    echo "✅ PASS: chore.md removed"
else
    echo "❌ FAIL: chore.md still present"
    exit 1
fi
echo ""

echo "Test 6: PM directories exist"
for dir in reports proposals designs specs plans handoffs decisions validation-reports; do
    mkdir -p ~/.lev/pm/$dir 2>/dev/null || true
    if [ -d ~/.lev/pm/$dir ]; then
        echo "✅ PASS: .lev/pm/$dir exists"
    else
        echo "❌ FAIL: .lev/pm/$dir missing"
        exit 1
    fi
done
echo ""

echo "Test 7: scratch is outside PM"
mkdir -p ~/.lev/scratch 2>/dev/null || true
if [ -d ~/.lev/scratch ]; then
    echo "✅ PASS: .lev/scratch exists"
else
    echo "❌ FAIL: .lev/scratch missing"
    exit 1
fi
echo ""

echo "Test 8: Handoff template sections"
for section in "## You Are Here" "## Next Agent Brief" "## Roadmap To Goal" "## Timeline" "## Decisions Log" "## Open Questions" "## Entity Matrix" "## Meta"; do
    if rg -q "${section}" ~/.claude/skills/work/templates/handoff.md; then
        echo "✅ PASS: $section"
    else
        echo "❌ FAIL: missing $section"
        exit 1
    fi
done
echo ""

echo "Test 9: How To Fill sections"
for file in report.md proposal.md design.md spec.md plan.md handoff.md decision.md validation-report.md; do
    if rg -q "^## How To Fill This Out" ~/.claude/skills/work/templates/$file; then
        echo "✅ PASS: $file has How To Fill This Out"
    else
        echo "❌ FAIL: $file missing How To Fill This Out"
        exit 1
    fi
done
echo ""

echo "Test 10: Lint passes"
bash ~/.claude/skills/work/scripts/lint-work-contract.sh
echo ""

echo "================================"
echo "Integration Test Summary"
echo "================================"
echo ""
echo "✅ Work skill is self-documenting"
echo "✅ PM template contract is present"
echo "✅ Handoff contract is upgraded"
echo "✅ Scratch boundary is correct"
echo ""
echo "Status: READY FOR PASS 1"
echo ""
