---
type: dashboard
status: active
---

# {name}

## Sources

```dataview
TABLE source_type AS "Type", url AS "URL", date AS "Added"
FROM "Notes/NotebookLM/{notebook-slug}/Sources"
WHERE type = "notebook-source"
SORT date DESC
```

## Q&A Log

```dataview
TABLE date AS "Date", source AS "Source"
FROM "Notes/NotebookLM/{notebook-slug}/QA"
WHERE type = "reference"
SORT date DESC
```
