---
name: legal-hub
description: |
  [WHAT] Unified legal skill router — routes to the right legal sub-skill based on intent
  [HOW] Decision tree routes to: case research, OSINT/investigation, maritime law, contract review, legal risk assessment, red-team verification, document drafting (700+ templates)
  [WHEN] Use when user mentions legal, lawsuit, case law, maritime, notice, discovery, deposition, complaint, motion, evidence, OSINT, investigation, crew, witness
  [WHY] Prevents loading 700 separate legal skills; routes to the right one based on context

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
---

# Legal Hub — Unified Legal Router

> **700+ legal skills** from lawvable/awesome-legal-skills + anthropics/knowledge-work-plugins + marketplace picks.
> This router gets you to the right one without loading everything.

## Quick Reference

| Intent | Route To | Path |
|--------|----------|------|
| Case law research | `lawyer-analyst` | General legal analysis, 273 installs |
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

## Document Drafting (700+ templates)

The lawvable collection includes templates for virtually every legal document type. Key categories for the Sun v. Virgin case:

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
"draft [document]" → search 700+ templates by name
"review contract" → review-contract
"compliance check" → compliance-check
```

## Loading a Spoke

To load any sub-skill: `cat ~/.agents/skills-db/legal/<skill-name>/SKILL.md`

For the 700+ document templates, each has its own dir with a SKILL.md containing the template prompt.
