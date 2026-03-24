---
name: ubs
description: |
  [WHAT] Static-analysis quality-gate wrapper around the external `ubs` CLI (Ultimate Bug Scanner).
  [HOW] Runs `ubs` on staged, diffed, or explicitly changed files with structured output, then uses the findings as a pre-commit or pre-review bug gate.
  [WHEN] Use before commit, during code review, when the user asks for bug scanning, or when a change needs a fast multi-language sanity pass.
  [WHY] Catches AI-agent bug patterns early without making UBS itself the project workflow router.

  Triggers: "ubs", "ultimate bug scanner", "bug scan", "static analysis", "quality gate", "scan for bugs", "pre-commit scan"
---

# UBS

Use `ubs` as a scoped gate. Keep the scope tight unless the user explicitly wants a full baseline scan.

## Prerequisites

```bash
command -v ubs
```

If missing, stop and tell the user:

```bash
brew install dicklesworthstone/tap/ubs
```

## Golden Rules

1. Prefer `--staged`, `--diff`, or explicit files over `ubs .`.
2. Use `--format=json` when you need machine-readable output.
3. Re-run after fixes to confirm the exit code is clean.
4. Treat UBS as a tool boundary; do not import its repo-level hooks as implicit Lev policy.

## Fast Path

```bash
ubs --staged --format=json --ci
```

If you only changed a few files:

```bash
ubs path/to/file.ts path/to/other.py --format=json --ci
```

## Core Commands

### Narrow scans

```bash
ubs --staged --format=json --ci
ubs --diff --format=json --ci
ubs src/file.ts src/other.py --format=json --ci
```

### Full or filtered scans

```bash
ubs . --format=json --ci
ubs --only=js,python . --format=json --ci
ubs --category=resource-lifecycle . --format=json --ci
```

### Diagnostics

```bash
ubs doctor
ubs doctor --fix
```

## Recommended Workflow

### Before commit

```bash
ubs --staged --fail-on-warning --format=json --ci
```

### During review

1. Scan only the touched files.
2. Inspect critical findings first.
3. Fix root causes, not symptoms.
4. Re-run the same narrow scan.

## Output Handling

Focus on:
- `summary`
- `findings[].file`
- `findings[].line`
- `findings[].severity`
- `findings[].category`
- `findings[].message`

If the user wants GitHub or CI artifacts:

```bash
ubs . --format=sarif --ci
ubs . --report-json .ubs/latest.json --html-report .ubs/latest.html --ci
```

## When Not To Use UBS

Do not default to UBS when:
- the user wants architectural review rather than static findings
- there are no changed files and no request for a baseline scan
- another domain-specific checker is clearly more appropriate

## Anti-Patterns

- Running `ubs .` on every small edit
- Ignoring critical findings without checking the code
- Treating UBS findings as proof without context
- Installing repo hooks or settings from the upstream repo without explicit user approval

## Minimal Report Pattern

```markdown
## UBS Findings
- Scope scanned:
- Critical:
- Warnings:
- Follow-up fixes:
```

Keep the summary in the active Lev artifact or review comment, not in detached scratch notes.
