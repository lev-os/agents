# Research: Live Best Practices Discovery

Use the stack manifest from the detect step. Search the web for current cutting-edge best practices.

## Research Strategy

Run these searches in parallel using sub-agents where possible.

### Stack-Specific Research

For EACH major framework/language detected, search for:
1. `"{framework} {version} best practices {current_year}"`
2. `"{framework} migration guide latest"` — are they on the latest version? What changed?
3. `"{framework} performance optimization {current_year}"`
4. `"{framework} security best practices"`
5. `"{framework} anti-patterns to avoid"`

Examples:
- "Next.js 15 best practices 2026"
- "Python 3.13 new features migration"
- "React 19 patterns server components 2026"
- "Rust 2024 edition idioms"

### Cross-Cutting Research

Search for these regardless of stack:
1. **Security**: "OWASP top 10 {current_year}", "{language} security checklist {current_year}"
2. **Performance**: "web performance best practices {current_year}", "{framework} performance pitfalls"
3. **Architecture**: "{detected_pattern} best practices {current_year}" (e.g., "monorepo best practices 2026")
4. **Dependencies**: "supply chain security npm/pip/cargo {current_year}"
5. **Testing**: "{test_framework} best practices {current_year}", "testing anti-patterns"
6. **Accessibility**: "WCAG 2.2 compliance" (if frontend detected)
7. **API Design**: "{api_pattern} best practices" (if API detected)
8. **CI/CD**: "{ci_tool} optimization best practices"

### Source Quality

Prioritize:
- Official documentation and migration guides
- RFCs and proposals that shipped
- Conference talks from the current year
- Reputable engineering blogs (major tech companies, framework authors)

Deprioritize:
- Listicles and generic "top 10" articles
- Content older than 18 months
- AI-generated summaries without primary sources

## Output

Compile research notes organized by category:

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

Every practice MUST have a source URL. No URL = not a finding.
