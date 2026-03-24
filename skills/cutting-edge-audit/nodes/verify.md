# Verify: Confirm Fixes and Generate Report

## Step 1: Re-Scan

After all fixes are applied, do a quick re-scan:
- Do the fixed files still parse/compile?
- Did any fix introduce a new issue?
- Are there any remaining findings that were missed?

## Step 2: Run Tests (if available)

If the repo has tests:
- Run the full test suite
- If tests fail, determine if the failure is from your changes or pre-existing
- Fix any test failures caused by your changes
- Update test expectations if the fix intentionally changed behavior (document why)

If no tests exist, note this in the report.

## Step 3: Generate Final Report

Write the report to `CUTTING-EDGE-AUDIT.md` in the repo root.

Use this format:

```markdown
# Cutting-Edge Audit Report

**Repository:** [name]
**Date:** [date]
**Stack:** [detected stack summary]

## Executive Summary

[2-3 sentences: what was found, what was fixed, overall health assessment]

## Stack Analysis

[Stack manifest from detect step]

## Research Sources

[List of URLs consulted, grouped by category]

## Checklist

### Security
- [x] or [ ] [Practice description] — [pass/fail reason]

### Performance
- [x] or [ ] [Practice description] — [pass/fail reason]

### Modern Features
- [x] or [ ] [Practice description] — [pass/fail reason]

### Architecture
- [x] or [ ] [Practice description] — [pass/fail reason]

### Testing
- [x] or [ ] [Practice description] — [pass/fail reason]

### Accessibility
- [x] or [ ] [Practice description] — [pass/fail reason]

## Changes Made

### Critical
| File | Finding | Change | Source |
|------|---------|--------|--------|
| path | what was wrong | what was fixed | URL |

### High
[same table format]

### Medium
[same table format]

### Low
[same table format]

## Code Samples

### [Finding Title]
**File:** `path/to/file`

Before:
\`\`\`language
[old code]
\`\`\`

After:
\`\`\`language
[new code]
\`\`\`

**Why:** [explanation with source link]

[Repeat for significant changes]

## Test Results

[Test output summary, or "No test suite detected"]

## Recommendations

[Anything that couldn't be auto-fixed — needs human decision, major refactors, etc.]
```

## Step 4: Summary

Present the user with:
1. Total findings by severity
2. Total fixes applied
3. Any items that need manual attention
4. Test results
5. Link to the full report
