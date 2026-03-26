1. Update handoff (matrix, decisions, timeline)
2. If code changed: run tests/build
3. git add {files} && git commit
4. git pull --rebase
5. Ask the user: "Ready to push? Run: git push" — do NOT push without explicit user approval
6. git status shows "up to date with origin"
Unpushed work is at risk — remind the user, but let them decide when to push.
