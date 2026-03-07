---
type: report
created: YYYY-MM-DDTHH:MM:SS
updated: YYYY-MM-DDTHH:MM:SS
status: draft | complete
scope: codebase | research | audit | analysis
agent: agent-name
confidence: 0.0-1.0
related_tasks: [task-id-1]
related_docs: [path/to/doc.md]
---

# Report: {{TITLE}}

## Executive Summary

- **Objective**: {{what was investigated}}
- **Finding**: {{primary result}}
- **Action**: {{recommended next action}}

## Findings

| ID | Finding | Severity | Evidence |
|---|---|---|---|
| F1 | {{finding}} | {{H/M/L}} | {{path:line or source}} |
| F2 | {{finding}} | {{H/M/L}} | {{path:line or source}} |

## Analysis Notes

- {{key insight}}
- {{constraint}}
- {{unknown/risk}}

## Recommended Actions

### Immediate
- [ ] {{action 1}}
- [ ] {{action 2}}

### Next
- [ ] {{action 3}}

## Validation

- [ ] Evidence paths verified.
- [ ] Recommendations are actionable.
- [ ] Blockers/dependencies are listed.

## References

- {{path/to/code-or-doc}}
- {{url-or-report}}
- {{issue-id}}

## Next Workflow Step

- Design path: `work "design {{topic}}"`
- Spec path: `work "specify {{topic}}"`
