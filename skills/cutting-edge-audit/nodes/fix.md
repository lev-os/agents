# Fix: Apply All Changes

Take every finding from the audit and fix it. No exceptions.

## Rules

1. **Fix everything.** Every finding gets a code change. If a fix would break something, find a non-breaking way to achieve the same goal.

2. **Preserve behavior.** Fixes must not change the external behavior of the code unless the current behavior is a bug or security vulnerability.

3. **Work file by file.** Group findings by file. Apply all fixes for a file in one pass to avoid conflicts.

4. **Order matters.** Fix in this order:
   - Critical security issues first
   - High severity next
   - Then medium and low
   - Architecture changes last (they may affect many files)

5. **Track every change.** For each fix, record:
   ```
   - file: [path]
     finding: [what was wrong]
     change: [what you changed]
     before: [code snippet before]
     after: [code snippet after]
   ```

6. **Dependency updates.** If the audit found outdated dependencies:
   - Update version numbers in manifest files
   - Note any breaking changes from the research step
   - Update code that uses changed APIs

7. **New files are OK.** If best practices require new files (e.g., security headers middleware, error boundary components, CI config), create them.

8. **Configuration changes.** Update configs (tsconfig, eslint, CI workflows, Docker) to match current recommendations.

## What NOT to do

- Do not rewrite working code for style preferences alone
- Do not add dependencies unless the finding specifically requires one
- Do not change test assertions without verifying the new assertion is correct
- Do not remove functionality — modernize it

## After Fixing

Count your changes. Every audit finding must map to either:
- A code change (with before/after), OR
- A documented exception with a concrete reason

Zero findings should be silently skipped.
