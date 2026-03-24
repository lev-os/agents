---
name: cutting-edge-audit
description: |
  Full-repo audit against cutting-edge best practices. Detects stack, researches live for current practices, scans every file, fixes everything, and generates a detailed report with checklist.
  Triggers: "audit", "best practices", "cutting-edge", "modernize", "code review", "audit my code", "check my code"
user-invokable: true
argument-hint: "[optional: focus area like 'security' or 'performance']"
---

# Cutting-Edge Audit

Deep, research-backed audit of an entire repository against current best practices — then fix everything found.

## Flow

This skill follows the `dna.yaml` intent graph:

1. **Detect** — scan the repo, identify languages, frameworks, versions, architecture
2. **Research** — live web search for cutting-edge practices per detected stack + cross-cutting (security, performance, architecture)
3. **Audit** — read every file, compare against researched practices, produce findings with severity
4. **Fix** — apply code changes for every finding, track before/after
5. **Verify** — re-scan, run tests, generate `CUTTING-EDGE-AUDIT.md` report

## Invoking

```
/cutting-edge-audit
```

Or naturally:
- "audit this repo for best practices"
- "check my code against cutting-edge practices"
- "modernize this codebase"

## What Gets Checked

- **Security**: OWASP top 10, input validation, secrets management, dependency vulnerabilities, CORS, auth patterns
- **Performance**: N+1 queries, unnecessary re-renders, missing caching, bundle size, async patterns
- **Modern Features**: deprecated APIs, new language features, type safety improvements
- **Architecture**: separation of concerns, error handling, dead code, circular dependencies, API design
- **Testing**: coverage gaps, test anti-patterns, missing integration tests
- **Accessibility**: semantic HTML, ARIA, keyboard navigation (if frontend)

## Output

1. **Inline code fixes** — every finding gets fixed in place
2. **CUTTING-EDGE-AUDIT.md** — full report with:
   - Pass/fail checklist by category
   - Changes table with file, finding, fix, and source URL
   - Before/after code samples
   - Test results
   - Recommendations for items needing human decision

## Rules

- Every practice must come from a live web search with a source URL
- Every file gets scanned — no skipping tests, configs, or "minor" files
- Every finding gets fixed — no "recommendations" without code changes
- Fixes must not break existing behavior unless fixing a bug/vulnerability

## DNA

The full intent graph is in `dna.yaml`. Load it for node routing, validation rules, and anti-pattern detection.
