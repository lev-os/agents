# Template: Code Review

Source-code-focused evaluation against coding standards.
Use for PR reviews, migration audits, or codebase health checks.

## Categories

### CORRECTNESS (weight: 0.3)
- [ ] Logic is correct for stated requirements
- [ ] Edge cases handled (nil, empty, overflow, concurrent access)
- [ ] No data races or thread-safety issues
- [ ] Error paths return meaningful feedback
- [ ] State mutations are intentional and documented

### STYLE (weight: 0.2)
- [ ] Follows project naming conventions
- [ ] File length within limits (500 LOC Swift, 700 LOC TS)
- [ ] Functions are focused (single responsibility)
- [ ] No dead code or commented-out blocks
- [ ] Imports are minimal and organized

### PERFORMANCE (weight: 0.2)
- [ ] No unnecessary allocations in hot paths
- [ ] Async operations don't block main thread
- [ ] Collection operations are efficient (no O(n^2) where O(n) suffices)
- [ ] Caching used where appropriate
- [ ] No unbounded growth (memory leaks, accumulating listeners)

### SECURITY (weight: 0.15)
- [ ] No hardcoded secrets or credentials
- [ ] User input is validated/sanitized
- [ ] No injection vulnerabilities (SQL, command, XSS)
- [ ] Sensitive data handled appropriately (keychain, not UserDefaults)
- [ ] Network calls use HTTPS

### TESTS (weight: 0.15)
- [ ] Unit tests exist for core logic
- [ ] Test coverage meets threshold (70%+)
- [ ] Tests are deterministic (no flaky timing deps)
- [ ] Edge cases have dedicated test cases
- [ ] Mocks/stubs are minimal and focused

## Verdict Rules

- **PASS**: All categories >= 75% AND no P0 security issues
- **NEEDS_WORK**: Any category < 75% OR any P0/P1 issue
- **BLOCKED**: Cannot read source or dependencies unresolvable
