---
name: security-hub
description: |
  [WHAT] Unified security skill router — routes to the right security sub-skill based on intent
  [HOW] Decision tree routes to: security-review (code audit), security-best-practices (language-specific), security-threat-model (threat modeling), security-ownership-map (ownership topology)
  [WHEN] Use when user mentions security, audit, vulnerability, threat model, OWASP, pentest, code review security, ownership analysis
  [WHY] Prevents loading 4 separate security skills; routes to the right one based on context

  Triggers: "security", "audit", "vulnerability", "threat model", "OWASP", "pentest", "code review security", "ownership", "bus factor", "security review"
skill_type: router
category: security
subsumes:
  - security-review
  - security-best-practices
  - security-threat-model
  - security-ownership-map
---

# Security Hub — Unified Security Router

Routes security requests to the appropriate specialized sub-skill. Use this router instead of loading individual security skills directly.

## Decision Tree

**Step 1: Identify Intent**

| User Intent | Sub-Skill | Load When |
|-------------|-----------|-----------|
| Code audit, checklist review, pre-deployment checks | `security-review` | User asks to "review security", "check for vulnerabilities", "audit this code" |
| Language-specific best practices (Python/JS/Go) | `security-best-practices` | User asks for "secure coding in [language]", "framework security", "language-specific security" |
| Threat modeling, trust boundaries, abuse paths | `security-threat-model` | User asks to "threat model", "enumerate threats", "attacker paths", "AppSec analysis" |
| Ownership risk, bus factor, maintainer topology | `security-ownership-map` | User asks for "ownership analysis", "bus factor", "who owns sensitive code", "orphaned code" |

**Step 2: Clarify Ambiguity**

- If intent is unclear, ask: "What type of security work? (1) Code review (2) Language best practices (3) Threat model (4) Ownership analysis"
- If scope is unclear (e.g., "security audit"), default to `security-review` (broadest checklist)

## Sub-Skill Quick Reference

### security-review (Code Audit Checklist)
Pre-deployment security checklist covering: secrets management, input validation, SQL injection, auth/authz, XSS/CSRF, rate limiting, dependency security. Best for: code review, pre-deploy gates, general vulnerability scanning.

### security-best-practices (Language/Framework Security)
Language and framework-specific security guidance (Python, JS/TS, Go). Loads reference docs for secure-by-default coding, passive vulnerability detection, and security report generation. Best for: new projects, framework-specific security, secure coding patterns.

### security-threat-model (AppSec Threat Modeling)
Repository-grounded threat modeling: trust boundaries, assets, attacker capabilities, abuse paths, and mitigations. Produces Markdown threat model documents. Best for: architecture review, AppSec planning, risk prioritization.

### security-ownership-map (Ownership Topology)
Git-based ownership analysis: compute bus factor, identify orphaned sensitive code, map maintainer topology, export graph data (CSV/JSON/GraphML). Best for: security maintainer analysis, CODEOWNERS drift, ownership risk.

## Cross-Cutting Workflows

Use **multiple sub-skills together** for comprehensive security analysis:

1. **New Project Security**
   - Start: `security-best-practices` (secure-by-default patterns)
   - Then: `security-review` (pre-deploy checklist)

2. **AppSec Deep Dive**
   - Start: `security-threat-model` (enumerate threats)
   - Then: `security-review` (validate controls)
   - Then: `security-ownership-map` (identify maintainers for high-risk code)

3. **Incident Response / Post-Mortem**
   - Start: `security-ownership-map` (who owns the vulnerable code?)
   - Then: `security-threat-model` (how was this exploitable?)
   - Then: `security-best-practices` (what secure pattern prevents this?)

4. **CODEOWNERS Validation**
   - Start: `security-ownership-map` (compute actual ownership)
   - Then: `security-threat-model` (identify sensitive boundaries)
   - Compare: ownership map vs CODEOWNERS file

## Notes

- **Progressive disclosure:** Load only the sub-skill you need. The router stays small; sub-skills contain the full content.
- **No overlap:** Each sub-skill has a distinct scope. No redundant checklists across skills.
- **Composable:** Chain sub-skills together for end-to-end security workflows.
