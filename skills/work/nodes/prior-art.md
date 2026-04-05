Load /prior-art skill. Return a provenance report in chat; do not write a markdown artifact unless the user explicitly asks for one.

Search before creating:
```bash
cass search "{topic}" --robot --limit 5 --fields minimal
rg -rl "{topic}" .lev/ docs/ reports/ prompt-exports/ 2>/dev/null
rg -rl "{topic}" ~/.agents/diagrams 2>/dev/null
lev get "{topic}" --json
qmd query "{topic}"
```

Report: | Found | Path | Relation | Action |
