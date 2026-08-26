---
name: legal-hub
description: |
  [WHAT] Unified legal skill router — routes to the right legal sub-skill based on intent
  [HOW] Decision tree routes to source-backed document drafting, case research, investigation, maritime law, contract review, risk assessment, and verification
  [WHEN] Use when the user needs legal drafting, research, review, litigation support, compliance, investigation, or risk analysis
  [WHY] Keeps the large local legal catalog behind one intent router

  Triggers: "legal", "lawsuit", "case", "maritime", "notice", "discovery", "deposition", "complaint", "motion", "evidence", "OSINT", "investigation", "witness", "settlement", "damages", "precedent"
skill_type: router
category: legal
subsumes:
  - lawyer-analyst
  - maritime-expert
  - case-analyzer
  - legal-verified-research-memo
  - red-team-verifier-patrick-munro
  - legal-risk-assessment-zacharie-laik
  - legal-simulation-patrick-munro
  - investigation
  - osint
  - brief
  - compliance-check
  - legal-response
  - legal-risk-assessment
  - review-contract
  - triage-nda
  - legal-document-library
---

# Legal Hub — Unified Legal Router

Route to one legal capability without loading the full catalog.

## Quick Reference

| Intent | Route To | Path |
|--------|----------|------|
| Startup or technology document drafting | `legal-document-library` | Pinned attorney-authored source templates |
| Case law research | `lawyer-analyst` | General legal analysis |
| Maritime PI / admiralty | `maritime-expert` | Maritime domain expertise |
| Case analysis | `case-analyzer` | Structured case breakdown |
| Cited legal memo | `legal-verified-research-memo` | Produces verified, cited memos |
| Stress-test arguments | `red-team-verifier-patrick-munro` | Devil's advocate for legal arguments |
| Risk assessment | `legal-risk-assessment-zacharie-laik` | Severity × likelihood framework |
| Legal simulation | `legal-simulation-patrick-munro` | Scenario modeling |
| OSINT investigation | `osint` | danielmiessler's OSINT methods |
| Investigation | `investigation` | danielmiessler's investigation methodology |
| Legal briefing | `brief` | Anthropics — contextual legal briefings |
| Compliance check | `compliance-check` | Anthropics — regulatory compliance |
| Contract review | `review-contract` | Anthropics — clause-by-clause analysis |
| NDA triage | `triage-nda` | Anthropics — GREEN/YELLOW/RED classification |

## Document drafting

Use `legal-document-library` for advisor agreements, BAAs, cookie notices, U.S. or global DPAs, California exempt offer letters, technology MSAs, mutual or one-way NDAs, U.S. or GDPR-enhanced privacy policies, and website terms. Its source assets are pinned and separate from current-law verification.

For other document types, search the catalog by document name. Common routes include:

### Litigation
- `complaint-for-negligence` — negligence complaint drafting
- `motion-to-dismiss` — MTD analysis and opposition
- `summary-judgment` / `summary-judgment-motion` — SJ preparation
- `discovery-plan` / `discovery-response-summary` — discovery management
- `deposition-preparation` / `deposition-summary` — depo prep
- `settlement-agreement` / `settlement-summary` — settlement analysis
- `damages-calculator` — damages estimation
- `demand-letter` / `demand-package` — demand preparation

### Maritime / PI Specific
- `maritime-case-summary` — maritime case analysis
- `maritime-expert` — maritime domain expertise
- `pi-demand-summary` — personal injury demand package
- `pi-intake-form` — PI case intake
- `medical-record-chronology` — medical records timeline
- `medical-treatment-summary` — treatment summary
- `expert-witness-report-analysis` — expert report analysis
- `ime-report-analysis` — independent medical exam analysis

### Evidence / Investigation
- `case-chronology` — timeline construction
- `evidence-liability-summary` — evidence assessment
- `investigation-report-summary` — investigation findings
- `witness-prep` / `witness-summary` — witness preparation
- `expert-witness-designation` — expert witness management
- `spoliation-letter` — evidence preservation
- `preservation-letter` — litigation hold

### OSINT / Research
- `osint` — open source intelligence methods
- `investigation` — investigation methodology
- `legal-research` / `legal-research-summary` — legal research
- `case-viability-report` — case strength assessment

## Routing Logic

```
USER INTENT → ROUTE
─────────────────────────────────
"research case law" → lawyer-analyst
"maritime law" → maritime-expert
"analyze this case" → case-analyzer
"write legal memo" → legal-verified-research-memo
"stress test argument" → red-team-verifier-patrick-munro
"assess risk" → legal-risk-assessment-zacharie-laik
"simulate scenario" → legal-simulation-patrick-munro
"find people/OSINT" → osint + investigation
"draft startup/technology document" → legal-document-library
"draft other document" → search the legal catalog by name
"review contract" → review-contract
"compliance check" → compliance-check
```

## Loading a Spoke

To load any sub-skill: `cat ~/.agents/skills-db/legal/<skill-name>/SKILL.md`

For generic document prompts, search the legal catalog rather than loading it wholesale.
