## Refresh current state

`--refresh` is an optional modifier and combines with the existing scopes and
explanation modes. With no topic or explicit conversation-selection scope,
use the current conversation. Preserve numeric/recent/project selections from
the entrypoint; refresh each selected conversation rather than replacing the set.
It requests
fresh evidence, not a Git pull, implementation, tracker update, or task resume.
Separately authorized actions retain their own scope.

When `--refresh` is requested after a long gap or suspected refactor, refresh
before explaining because old paths, names, decisions, and test results may
describe a retired system:

1. Bind the current project and snapshot the date, checkout revision, branch,
   dirty state, and known upstream lag. Follow its config, current vocabulary,
   owner guidance, and active workstream pointers. State which checkout was
   inspected; do not call it latest without checking.
2. Extract the old conversation's load-bearing claims: purpose, chosen owners,
   implementation status, unresolved decisions, and next action. Recheck each
   against current code, declared contracts, tests, and linked runtime evidence.
   Use structural discovery tools when available. Follow moves through current
   imports, owner declarations, and Git history; a missing path or similar name
   alone does not prove deletion or equivalence.
3. Mark each consequential claim current, superseded, or unverified with a
   concrete source and date/revision. Show a compact then/now comparison when it
   helps. Preserve the original intent while using current established terms;
   conflicting owners remain an explicit gap rather than a synthesized decision.
4. Run the smallest safe check that could disprove the central current claim
   when practical. Distinguish an existing implementation, a fresh test pass,
   and live end-to-end proof. If checks or hosts are unavailable, name the gap
   and continue the evidence that is accessible.
5. Explain the purpose, material changes, surviving decisions, current blocker,
   and next eligible action. State the coverage window and what was actually
   checked. Never resume a retired plan merely because it was this chat's last
   recommendation.

Bad: repeat "create core/eval" from an old chat without checking today's tree.
Good: find its current owner and tests, explain which extraction landed, and
identify the remaining integration evidence. If no project source is accessible,
give a dated historical explanation and mark current state unverified.
