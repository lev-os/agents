# Audit: Deep Code Scan

With research findings in hand, scan every file in the repository.

## Scan Strategy

### Phase 1: Architecture-Level Audit
Before touching individual files, evaluate:
- Directory structure against current best practices
- Dependency versions — are they outdated? Are there known vulnerabilities?
- Configuration files — are they following current recommendations?
- CI/CD pipeline — is it optimized? Does it have security scanning?
- Docker/infra setup — multi-stage builds? Minimal base images?

### Phase 2: File-by-File Audit
Read every source file. For each file, check against ALL researched practices:

**Security**
- Input validation and sanitization
- Authentication/authorization patterns
- Secrets management (no hardcoded secrets, env vars)
- SQL injection, XSS, CSRF protection
- Dependency vulnerabilities
- CORS configuration

**Performance**
- Unnecessary re-renders (React), redundant queries, N+1 problems
- Missing caching, memoization opportunities
- Bundle size concerns (unused imports, heavy dependencies)
- Async patterns — proper use of concurrency
- Database query optimization

**Modern Language Features**
- Using deprecated or outdated APIs when modern alternatives exist
- Missing new language features that simplify code (pattern matching, using declarations, etc.)
- Type safety opportunities (stricter types, branded types, etc.)

**Architecture**
- Separation of concerns
- Error handling patterns (proper error boundaries, result types, etc.)
- Dead code and unused exports
- Code duplication that could use shared utilities
- API design (REST conventions, GraphQL schema design, etc.)

**Testing**
- Missing test coverage for critical paths
- Test anti-patterns (testing implementation details, brittle selectors)
- Missing integration/e2e tests for key flows

**Accessibility** (if frontend)
- Semantic HTML
- ARIA attributes
- Keyboard navigation
- Color contrast

### Phase 3: Cross-File Patterns
Look for systemic issues:
- Inconsistent error handling across the codebase
- Mixed patterns (some files use X, others use Y)
- Missing shared types/interfaces
- Circular dependencies

## Output

Build a findings list. Every finding must have:

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

Sort by severity (critical first). Do not skip files. Do not skip categories.
