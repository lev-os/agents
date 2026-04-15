# Operator UX Standards

## Core Principle
Admin UI should enable fast, correct decisions under uncertainty.

## 1) Information Hierarchy
- Always show status, severity, owner, freshness.
- Keep primary actions visible near primary data.

## 2) Decision Support
- High-risk actions show impact text.
- Destructive/financial/moderation actions require reason input.
- Confirm dialogs must be specific.

## 3) State Coverage
- Empty: explain why and next action.
- Error: show failure context + retry.
- Loading: avoid layout jumps.
- Stale: show timestamp + refresh path.

## 4) Queue UX
- Default sort by urgency/SLA risk.
- Bulk actions only when safe.
- Show transition history in detail view.

## 5) Accessibility + Speed
- Keyboard-friendly for repetitive workflows.
- Predictable focus after mutations.
- Contrast-safe status badges.

## 6) Consistency
- Same filters/badges, action semantics, and search/sort/pagination conventions across sections.
