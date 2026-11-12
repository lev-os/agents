# Analysis Extension Capture Pattern

Use this when a user asks to "capture this", "extend the analysis", or turn an in-chat conceptual clarification into durable planning/scoping material.

## Pattern

1. Preserve the clarified thesis in a human-readable analysis artifact.
2. Cross-link the new artifact from the nearest existing roadmap/analysis documents so future readers find the update.
3. Write each conceptual unit to its own record (SKILL.md, Where Rows Go), never to a capture file, with:
   - compiled intent rather than raw chat prose,
   - artifact refs to the analysis sections,
   - route state and next route,
   - QA seed for runtime, agentic, promotion, fallback, or boundary-risk claims,
   - explicit blocker rows for requested but unavailable worker/model/tool steps.
4. If the user asks for a structure such as "current vs ideal" or "10 must/must-not", verify those sections and counts with a deterministic check before closing.
5. Summarize the next implementation route as a proposed entity plus the first executable slice, not as a vague recommendation.

## Verification checklist

- New analysis artifact exists and has the requested sections.
- Each record written parses cleanly and holds its compiled intent, route recommendation, and blockers if any.
- No capture, sweep or ledger file was written; the ledger is in the reply.
- Existing roadmap/analysis files point to the new companion artifact.
- Final response distinguishes durable records from ignored/raw or git-ignored workshop artifacts.
