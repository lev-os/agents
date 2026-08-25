---
name: legal-document-library
description: Use when drafting from attorney-authored startup and technology templates for an advisor agreement, business associate agreement, cookie notice, U.S. or global data processing addendum, California offer letter, technology master services agreement, mutual or one-way NDA, U.S. or GDPR privacy policy, or terms of use.
---

# Legal document library

Start from the exact source template routed below. Preserve its clauses and customization fields until matter facts justify a change. The source is a drafting baseline, not proof of current law or approval to sign or publish.

Resolve every path relative to this `SKILL.md`. Load only the requested template and its companion `README.md` when one exists.

## Template routes

| Request | Source template |
|---|---|
| Advisor agreement | `assets/general-legal/templates/advisor-agreement/template.md` |
| HIPAA business associate agreement / BAA | `assets/general-legal/templates/business-associate-agreement/template.md` |
| Cookie notice | `assets/general-legal/templates/cookie-notice/template.md` |
| Global / GDPR data processing addendum | `assets/general-legal/templates/dpa-global/template.md` |
| U.S.-only data processing addendum | `assets/general-legal/templates/dpa-us/template.md` |
| California exempt employee offer letter | `assets/general-legal/templates/employee-offer-letter/template.md` |
| Technology master services agreement / MSA | `assets/general-legal/templates/master-services-agreement/template.md` |
| Mutual NDA | `assets/general-legal/templates/mutual-nda/template.md` |
| One-way NDA | `assets/general-legal/templates/one-way-nda/template.md` |
| GDPR-enhanced privacy policy | `assets/general-legal/templates/privacy-policy-gdpr/template.md` |
| U.S.-only privacy policy | `assets/general-legal/templates/privacy-policy-us/template.md` |
| Website terms of use | `assets/general-legal/templates/terms-of-use/template.md` |

## Drafting flow

```yaml
steps:
  - id: select_source
    action: Select the exact template for each requested document.
    instruction: |
      Set skill_dir to the directory containing this SKILL.md and slug to the routed template directory.
      Keep different document types separate; a DPA is not a privacy policy, and an industry MSA is not a technology MSA.
    validation: 'test -f "$skill_dir/assets/general-legal/templates/$slug/template.md"'
    on_failure: "Stop and report the missing route. Do not substitute a nearby legal skill."
    next: verify_provenance

  - id: verify_provenance
    action: Read the source manifest and selected template.
    instruction: |
      Read references/source.yaml, then read the selected template and its README.md when present.
      Read references/errata.yaml and apply every entry matching the selected template as a listed deviation; keep the vendored source asset unchanged.
      Record the repository commit and template path in the drafting ledger.
    validation: 'rg -n "^  commit: [0-9a-f]{40}$" "$skill_dir/references/source.yaml" && test -f "$skill_dir/references/errata.yaml"'
    on_failure: "Stop and label the source unpinned."
    next: compile_matter

  - id: compile_matter
    action: Map matter facts to every customization field.
    instruction: |
      Collect parties, roles, jurisdiction, commercial terms, data flows, security facts, notice details, and execution choices required by the selected template.
      Map each <mark> field to a supplied fact or an explicit [OPEN: description] item. Keep source language when no matter-specific reason supports a change.
    validation: "Every source customization field maps to a supplied fact or an [OPEN] item; no fact is invented."
    on_failure: "Return the unresolved-input list before producing an execution candidate."
    next: verify_law

  - id: verify_law
    action: Separate source drafting from current-law verification.
    instruction: |
      For a document intended for signature or publication, verify jurisdiction-specific requirements against current primary authorities and cite them.
      For an exploratory draft, mark current-law status unverified and retain the counsel-review gate.
    validation: "The draft records current-law status as verified with primary citations or unverified with a visible blocker."
    on_failure: "Downgrade the output to a counsel-review draft."
    next: produce_draft

  - id: produce_draft
    action: Tailor the selected source without losing provenance.
    instruction: |
      Replace resolved fields, retain [OPEN] items, preserve defined-term and cross-reference consistency, and list material deviations from the source.
      Apply matching errata before presenting any signature or publication candidate.
      Write to disk only when the user explicitly names or authorizes a destination; otherwise return the draft in chat.
    validation: "All source sections are accounted for, all deviations are listed, and no disk write occurred without destination authorization."
    on_failure: "Repair omissions or return the blocker instead of claiming completion."
```

<drafting-ledger>

| Field | Required value |
|---|---|
| compiled_intent | Document type, parties, jurisdiction, and intended use |
| disk_state | Chat-only, proposed path, or user-authorized written path |
| artifact_ref | Output path or chat draft identifier |
| source_ref | Repository commit and selected template path |
| route | Selected template slug |
| blocker | Open inputs, current-law verification, or counsel review |
| confidence | Source fidelity and legal-currentness stated separately |

</drafting-ledger>

## Baseline counters

| Baseline rationale | Required correction |
|---|---|
| "The requested legal-document-library skill is absent; I will not invent it." | Load this library and select the exact asset. |
| "The closest local drafting asset is GDPR-only, so I will reuse its structure." | Route U.S. and global DPAs separately. |
| "The 20-minute shortcut is one generic U.S. core plus a California role-and-use restriction overlay." | Start from the pinned U.S. DPA and mark unresolved states. |
| "I would not treat `oilfield-msa` as 'close enough.'" | Use the technology MSA asset. |
| "The DPA skill is not close enough." | Use the GDPR privacy-policy asset for transparency notices. |
| "The compliance-summary skill can supply the disclosure checklist, but it cannot supply verified attorney-authored clauses." | Use compliance skills for review after the source draft, not instead of it. |

If you catch yourself thinking:

- "We already spent six hours, so rerouting now wastes the work."
- "A DPA discusses privacy, so it is close enough to publish as the privacy policy."
- "Changing attorney-drafted language creates risk, so using the MSA unchanged is safest."
- "The missing fields are clerical; normal defaults cannot materially change the deal."
- "Attorney-drafted means legally current, and tonight's deadline makes another review redundant."

All five mean: stop, preserve useful prior work as input, and return to `select_source`, `compile_matter`, or `verify_law` before producing a signature or publication candidate.
