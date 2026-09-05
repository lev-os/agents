---
name: subagent-driven-development
description: Compatibility route for implementation with coder and reviewer agents. Load $coder --sdd=checkpoint, or pass --sdd=pair when explicitly requested.
---

# Subagent-Driven Development Compatibility Route

Load `$coder --sdd=checkpoint`. If the caller explicitly requested paired
coder/reviewer sessions, load `$coder --sdd=pair` instead. The canonical batch,
review, evidence, retry, escalation, and final-integration contracts live inline
in `$coder`.
