---
name: raci-matrix
description: Clarify roles when cross-functional projects cause "who's doing this?" confusion
---

# RACI Matrix (Responsibility Assignment Matrix)
**Domain:** Executive Management & Strategy
**Practitioners:** Project management, organizational design
**Source:** Project management methodologies, widely adopted standard
**Classification:** Responsibility assignment, decision rights, role clarity

## Overview

The RACI Matrix (Responsibility Assignment Matrix) is a project management tool that clarifies roles and decision rights by assigning one of four responsibility types to each stakeholder for every task or deliverable. It prevents ambiguity about who does the work, who has final say, who provides input, and who needs updates—eliminating "I thought you were handling that" failures.

RACI is an acronym for four distinct responsibility types:
- **Responsible (R):** The person who does the work to complete the task
- **Accountable (A):** The person who ultimately answers for correct completion (only one per task)
- **Consulted (C):** Subject-matter experts whose opinions are sought (two-way communication)
- **Informed (I):** Those kept up-to-date on progress (one-way communication)

**Core Insight:** Role clarity dramatically reduces coordination overhead, decision bottlenecks, and blame diffusion. One person must be Accountable for each deliverable.

## Mental Model

```
No RACI:
Task → Confusion → "Who's doing this?" → Delays → Blame diffusion → Rework

With RACI:
Task → Clear R/A/C/I → Parallel execution → Accountability → On-time delivery

Critical Rule:
EXACTLY ONE "A" per task (too many = diffused accountability)
AT LEAST ONE "R" per task (someone must do the work)
```

## When to Use

**Trigger Conditions:**
- Cross-functional projects with 3+ teams involved
- Decision bottlenecks ("waiting for approval" delays)
- Repeated blame diffusion ("I thought Marketing was doing that")
- New organizational structure or team formation
- Complex initiatives with many stakeholders
- Roles and responsibilities are unclear or disputed

**Best Contexts:**
- Matrix organizations (dual reporting lines)
- Large transformation programs
- Product launches involving engineering, design, marketing, sales, legal
- Process redesign or operational improvement initiatives
- Mergers and integrations

## Implementation

### Step 1: List Tasks/Deliverables (Rows)
- Break project into discrete tasks or deliverables (not too granular)
- Use work breakdown structure (WBS) as input
- Include decision points (e.g., "Approve final design", "Select vendor")
- Example rows: "Define requirements", "Design UI mockups", "Write code", "QA testing", "Launch announcement"

### Step 2: List Stakeholders/Roles (Columns)
- Identify all individuals or roles involved in project
- Use roles (e.g., "Product Manager") not names for reusability
- Include cross-functional partners (legal, finance, marketing)
- Example columns: PM, Eng Lead, Designer, QA, Marketing, Legal, Exec Sponsor

### Step 3: Assign RACI for Each Cell
- For each task-stakeholder intersection, assign R, A, C, or I (or leave blank)
- Apply rules:
  - **Exactly one A** per row (ultimate decision-maker)
  - **At least one R** per row (who does the work; can be same as A for small tasks)
  - **C for two-way input** (experts consulted before decision)
  - **I for one-way updates** (FYI only, no input required)

### Step 4: Validate with Stakeholders
- Review matrix with all parties to confirm agreement
- Challenge any row with multiple A's (symptom of unclear accountability)
- Challenge any row with no A (who's ultimately responsible?)
- Identify overloaded individuals (too many R's or A's)

### Step 5: Socialize and Use
- Publish RACI as project artifact (Confluence, shared doc)
- Reference during kickoff, status meetings, and retrospectives
- Update as roles or scope change
- Use to resolve disputes: "According to RACI, Alice is Accountable for this decision"

### Step 6: Monitor and Adapt
- Track delays caused by unclear RACI
- Refine granularity (too detailed = overhead; too coarse = ambiguity)
- Reassign if someone is bottleneck (too many A's)

## Practical Examples

**Product Launch RACI:**

| Task | PM | Eng Lead | Designer | QA | Marketing | Legal | Exec |
|------|----|----|----|----|----|----|-----|
| Define product requirements | A/R | C | C | I | C | I | I |
| Design UI mockups | C | I | A/R | I | C | - | I |
| Write backend code | C | A/R | I | I | - | - | I |
| QA testing plan | C | C | I | A/R | I | - | I |
| Launch messaging | C | I | C | - | A/R | C | I |
| Legal compliance review | I | I | - | - | I | A/R | I |
| Go/No-Go decision | C | C | C | C | C | C | A |

**Interpretation:**
- PM is Accountable for requirements (sole decision-maker)
- Designer is both Accountable and Responsible for UI (does work + owns outcome)
- Legal is Accountable for compliance (can block launch if non-compliant)
- Exec is Accountable for final Go/No-Go (all others Consulted)

**Outcome:** Launch delivered on time; zero "who's responsible?" delays; legal caught compliance issue early (they were designated A for that task)

## Common Pitfalls

1. **Multiple A's per task** - Diffused accountability; no single decision-maker
2. **No A assigned** - Orphan task; falls through cracks
3. **Too many C's** - Consultation overhead; slow decisions (limit to 3-5 per task)
4. **Confusing R and A** - R does the work; A owns the outcome (can delegate R, not A)
5. **Over-granularity** - RACI for every subtask creates matrix explosion
6. **Static RACI** - Roles change; matrix becomes stale and ignored
7. **RACI theater** - Created but never referenced; not used for decision-making

## Decision Support

**When RACI is high-value:**
- 5+ stakeholders with overlapping responsibilities
- History of missed handoffs or duplicated work
- Cross-functional dependencies
- New team or reorganization

**When RACI may be overkill:**
- Small team (<5 people) with clear roles
- Simple projects with few dependencies
- Highly autonomous teams with strong trust
- Fast-moving startups (RACI adds bureaucracy)

## Integration Points

**Complements:**
- DACI Framework (Driver-Approver-Contributor-Informed, Intuit variant)
- RAPID Framework (Recommend-Agree-Perform-Input-Decide, Bain variant)
- Work Breakdown Structure (WBS provides task rows)
- Organizational Design (role clarity at structural level)
- OKRs (Accountable owner for each Key Result)

**Contrasts with:**
- Consensus decision-making (RACI creates single A, not group)
- Flat org structures (RACI formalizes hierarchy)

## Success Metrics

**Measured Impact (Case Study: Building Materials Distributor):**
- **Operational efficiency:** +25%
- **Employee satisfaction:** +30% (role clarity reduces frustration)
- **Decision-making time:** -15%
- **Project delays:** -20%

**Leading Indicators:**
- Reduction in "who's doing this?" questions
- Faster decision velocity (tracked via project milestones)
- Decrease in duplicate work
- Improved on-time delivery rates
- Reduced escalations to leadership

## Variants and Extensions

**DACI (Intuit):**
- Driver (owns execution), Approver (final say), Contributor (provides input), Informed
- Emphasizes driver role (not just R, but orchestrator)

**RAPID (Bain):**
- Recommend, Agree, Perform, Input, Decide
- Adds "Agree" (must agree before decision) vs. "Consulted" (input sought but not binding)

**RASCI:**
- Adds "S" for Supportive (provides resources to R)

**RACI-VS:**
- Adds "V" for Verify (checks work) and "S" for Sign-off (formal approval)

## Historical Context

**Origins:** Project management methodologies (1950s-1960s); formalized in PMBOK (Project Management Body of Knowledge)

**Adoption:** Widely adopted in 1980s-1990s for complex enterprise projects; standard tool in Six Sigma, Agile, and PRINCE2

**Modern Use:** Essential for remote/distributed teams where implicit coordination is harder; used in 70%+ of Fortune 500 companies

**Empirical Support:** Research shows clear role definition reduces project failure rates by 30-40%; case studies document 15-25% efficiency gains

## Best Practices

1. **One A per row** - Non-negotiable rule; diffused accountability kills projects
2. **Limit C's to 3-5** - Too many cooks slow decisions
3. **Use roles, not names** - Makes RACI reusable across projects
4. **Start coarse, refine** - High-level tasks first; add detail only where needed
5. **Publish visibly** - RACI in shared location everyone can access
6. **Reference actively** - Use in meetings: "Let's check the RACI"
7. **Update when roles change** - Stale RACI is worse than no RACI

## Technical Implementation

**Google Sheets / Excel Template:**
```
| Task/Deliverable | PM | Eng | Design | QA | ... |
|------------------|----|----|--------|----|----|
| Row 1            | A  | R  | C      | I  |    |
| Row 2            | C  | A/R| C      | I  |    |
```

**Color Coding:**
- Red = A (Accountable)
- Blue = R (Responsible)
- Green = C (Consulted)
- Yellow = I (Informed)

**Validation Rules:**
- Conditional formatting to highlight rows with 0 or 2+ A's (errors)

## Key Principles

1. **Exactly one throat to choke** - One person Accountable per task
2. **Do-ers vs. Deciders** - R does work; A owns outcome
3. **Two-way vs. One-way** - C provides input (consulted); I receives updates (informed)
4. **Clarity > Consensus** - RACI creates role clarity, not agreement
5. **Living document** - Update as project evolves

---

**Generated:** 2025-12-10
**Score:** 45/50 (Practitioner: 9/10, Clarity: 10/10, ROI: 9/10, Novelty: 7/10, Cross-domain: 10/10)
**Status:** Industry-standard project management tool, universally applicable for role clarity
