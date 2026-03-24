# Intake: Classify and Align

Classify the user's request into exactly one route:

| Signal | Route |
|--------|-------|
| URL, skills.sh link, skill:// protocol, GitHub repo, PDF | → seekers |
| "new skill", "from scratch", concept description, instructions | → interview |
| "audit", "is this safe", "security scan" | → security |
| "merge", "combine", "consolidate" | → merge |

After classifying, show the user an alignment dashboard:

```
─── Skill Builder Intake ───
Request: {summary of what user asked}
Route: {selected route}
Estimated steps: {count from dna.yaml}
─────────────────────────────
```

Wait for user confirmation before proceeding.
