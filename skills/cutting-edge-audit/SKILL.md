---
name: cutting-edge-audit
description: |
  Full-repo audit against cutting-edge best practices. Detects stack, researches live for current practices, scans every file, fixes everything, and generates a detailed report with checklist.
  Triggers: "audit", "best practices", "cutting-edge", "modernize", "code review", "audit my code", "check my code"
skill_type: workflow
user-invokable: true
argument-hint: "[optional: focus area like 'security' or 'performance']"
---

# Cutting-Edge Audit

You are executing a full-repo best practices audit. Follow these 5 steps IN ORDER. Do not skip steps. Do not take shortcuts.

---

## STEP 1: DETECT — Stack Discovery

Scan the entire repository to build a complete stack manifest.

### 1a. File Extension Survey
Use Glob to find all file types. Count occurrences. Identify primary and secondary languages.

### 1b. Package Manifests
Read ALL dependency/config files to identify frameworks and exact versions:
- `package.json`, `yarn.lock`, `pnpm-lock.yaml` (Node/JS/TS)
- `pyproject.toml`, `requirements.txt`, `setup.py`, `Pipfile` (Python)
- `Cargo.toml` (Rust) / `go.mod` (Go) / `Gemfile` (Ruby)
- `pom.xml`, `build.gradle` (Java/Kotlin) / `composer.json` (PHP)
- `*.csproj` (.NET) / `pubspec.yaml` (Dart) / `mix.exs` (Elixir)

### 1c. Framework Detection
From dependencies, identify specific frameworks:
- Frontend: React, Vue, Svelte, Angular, Next.js, Nuxt, Astro, etc.
- Backend: Express, FastAPI, Django, Rails, Gin, Phoenix, etc.
- Mobile: React Native, Flutter, SwiftUI, etc.
- Infra: Docker, Terraform, Kubernetes, etc.

### 1d. Architecture Scan
Identify from directory structure:
- Monorepo vs single package
- API patterns (REST, GraphQL, gRPC, tRPC)
- Test framework(s)
- CI/CD configuration
- Database/ORM setup

### 1e. Pin Versions
Pin exact versions for every major dependency. This is critical — "React best practices" is useless, "React 19.1 best practices 2026" is actionable.

### DETECT OUTPUT
Write this to your working memory (do not create a file):
```
PRIMARY LANGUAGES: [list with versions]
FRAMEWORKS: [list with exact versions]
BUILD TOOLS: [list]
TEST FRAMEWORKS: [list]
CI/CD: [what's configured]
ARCHITECTURE: [patterns detected]
DATABASE/ORM: [if applicable]
INFRA: [Docker, K8s, etc.]
```

### DETECT GATE
Do NOT proceed until you have at least one language and one framework identified. If you can't find any, keep scanning — check file extensions, shebangs, config files. Every repo has a stack.

---

## STEP 2: RESEARCH — Live Best Practices Discovery

Use WebSearch to find current best practices. DO NOT rely on training data. Every practice needs a source URL.

### 2a. Stack-Specific Searches
For EACH major framework/language detected, search for:
1. `"{framework} {version} best practices {current_year}"`
2. `"{framework} migration guide latest"`
3. `"{framework} performance optimization {current_year}"`
4. `"{framework} security best practices"`
5. `"{framework} anti-patterns to avoid"`

Use sub-agents to parallelize these searches.

### 2b. Cross-Cutting Searches
Search for these regardless of stack:
1. **Security**: `"OWASP top 10 {current_year}"`, `"{language} security checklist"`
2. **Performance**: `"web performance best practices {current_year}"`
3. **Architecture**: `"{detected_pattern} best practices"` (e.g., "monorepo best practices 2026")
4. **Dependencies**: `"supply chain security {package_manager} {current_year}"`
5. **Testing**: `"{test_framework} best practices {current_year}"`
6. **Accessibility**: `"WCAG 2.2 compliance"` (if frontend detected)
7. **API Design**: `"{api_pattern} best practices"` (if API detected)
8. **CI/CD**: `"{ci_tool} optimization best practices"`

### 2c. Source Quality
Prioritize official docs, RFCs, conference talks, engineering blogs from major companies. Deprioritize listicles, content older than 18 months, and AI-generated summaries without primary sources.

### 2d. Fetch Key Pages
Use WebFetch on the most promising URLs to get detailed practices. Don't just rely on search snippets.

### RESEARCH OUTPUT
Compile organized notes:
```
STACK-SPECIFIC FINDINGS:
  [framework]:
    - Practice: [description]
      Source: [URL]
      Applies to: [which files/patterns in this repo]

CROSS-CUTTING FINDINGS:
  [category]:
    - Practice: [description]
      Source: [URL]
      Applies to: [which areas of the codebase]
```

### RESEARCH GATE
Do NOT proceed until you have at least 3 stack-specific and 3 cross-cutting practice categories, each with source URLs. If search returns nothing, try different queries — different keywords, date-scoped, framework-specific.

---

## STEP 3: AUDIT — Deep Code Scan

Read every file. Compare against researched practices. Produce findings.

### 3a. Architecture-Level Audit
Before individual files, evaluate:
- Directory structure against current best practices
- Dependency versions — outdated? Known vulnerabilities?
- Configuration files — following current recommendations?
- CI/CD pipeline — optimized? Security scanning?
- Docker/infra — multi-stage builds? Minimal base images?

### 3b. File-by-File Audit
Read EVERY source file. For each, check against ALL researched practices:

**Security:**
- Input validation and sanitization
- Auth patterns, secrets management (no hardcoded secrets)
- SQL injection, XSS, CSRF protection
- CORS configuration, dependency vulnerabilities

**Performance:**
- Unnecessary re-renders, redundant queries, N+1 problems
- Missing caching, memoization opportunities
- Bundle size (unused imports, heavy deps)
- Async patterns, database query optimization

**Modern Language Features:**
- Deprecated or outdated APIs when modern alternatives exist
- Missing new language features that simplify code
- Type safety opportunities

**Architecture:**
- Separation of concerns, error handling patterns
- Dead code and unused exports, code duplication
- API design conventions

**Testing:**
- Missing test coverage for critical paths
- Test anti-patterns (testing implementation details)
- Missing integration/e2e tests

**Accessibility** (if frontend):
- Semantic HTML, ARIA attributes
- Keyboard navigation, color contrast

### 3c. Cross-File Patterns
Look for systemic issues:
- Inconsistent error handling across codebase
- Mixed patterns (some files use X, others use Y)
- Missing shared types/interfaces
- Circular dependencies

### AUDIT OUTPUT
Build a findings list. Every finding MUST have:
```
- file: [path]
  line: [number or range]
  category: [security|performance|modern-features|architecture|testing|accessibility]
  severity: [critical|high|medium|low]
  finding: [what's wrong]
  practice: [what the cutting-edge practice is]
  source: [URL from research step]
  suggested_fix: [concrete code change]
```

Sort by severity (critical first).

### AUDIT GATE
Do NOT proceed until every directory has been scanned. If you find yourself saying "I'll skip the tests" or "config files don't need auditing" — stop. Scan them. Full repo means full repo.

---

## STEP 4: FIX — Apply All Changes

Take every finding from the audit and fix it.

### 4a. Fix Order
1. Critical security issues first
2. High severity next
3. Then medium and low
4. Architecture changes last (may affect many files)

### 4b. Fix Rules
- **Fix everything.** Every finding gets a code change.
- **Preserve behavior.** Fixes must not change external behavior unless the current behavior is a bug or security vulnerability.
- **Work file by file.** Group findings by file. Apply all fixes for a file in one pass.
- **Track every change.** For each fix, record:
  ```
  - file: [path]
    finding: [what was wrong]
    change: [what you changed]
    before: [code snippet before]
    after: [code snippet after]
  ```

### 4c. Dependency Updates
If audit found outdated dependencies:
- Update version numbers in manifest files
- Note breaking changes from research step
- Update code that uses changed APIs

### 4d. New Files Are OK
If best practices require new files (security headers middleware, error boundary components, CI config), create them.

### 4e. What NOT to Do
- Do not rewrite working code for style preferences alone
- Do not add dependencies unless the finding specifically requires one
- Do not change test assertions without verifying correctness
- Do not remove functionality — modernize it

### FIX GATE
Every audit finding must map to either a code change (with before/after) OR a documented exception with a concrete reason. Zero findings may be silently skipped.

---

## STEP 5: VERIFY — Confirm Fixes and Generate Report

### 5a. Re-Scan
After all fixes:
- Do fixed files still parse/compile?
- Did any fix introduce a new issue?
- Any remaining findings that were missed?

### 5b. Run Tests
If the repo has tests:
- Run the full test suite
- If tests fail, determine if failure is from your changes or pre-existing
- Fix any test failures caused by your changes
- Update test expectations if the fix intentionally changed behavior (document why)

If no tests exist, note this in the report.

### 5c. Generate Report
Write `CUTTING-EDGE-AUDIT.md` in the repo root:

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
```language
[old code]
```

After:
```language
[new code]
```

**Why:** [explanation with source link]

[Repeat for significant changes]

## Test Results

[Test output summary, or "No test suite detected"]

## Recommendations

[Anything that couldn't be auto-fixed — needs human decision, major refactors, etc.]
```

### 5d. Present Summary
Tell the user:
1. Total findings by severity
2. Total fixes applied
3. Any items that need manual attention
4. Test results
5. The report is at `CUTTING-EDGE-AUDIT.md`

---

## ANTI-PATTERNS — Do NOT Do These

| What you might think | What you must do instead |
|---|---|
| "I'll use my training data instead of searching" | Training data is stale. Search live. Every practice needs a URL. |
| "I'll just check the main files" | Full repo. Every file. Config, tests, CI, docs — all of it. |
| "This finding is minor, I'll skip the fix" | Fix everything. Minor today is tech debt tomorrow. |
| "I'll report the issues and let the user fix them" | YOU fix them. Report what you changed. That's the whole point. |
| "Only checking code style and formatting" | Style is shallow. Check architecture, security, performance, patterns, dependencies. |
| "Research found nothing new" | Search with different queries. Try framework-specific, version-specific, date-scoped. |
| "The code looks fine as-is" | You haven't searched yet. Search first, then judge. |

---

## Reference Files

The `dna.yaml` in this skill's directory contains the intent graph with validation rules. The `nodes/` directory contains expanded instructions for each step. These are reference materials — all execution logic is above.
