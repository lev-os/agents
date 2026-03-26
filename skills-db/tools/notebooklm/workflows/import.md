# Import Notebook Workflow

Import all sources from a NotebookLM notebook into a markdown projection as linked
`notebook-source` files plus a dashboard/materialized view.

## Inputs

- `notebook-slug`: short kebab-case name for the notebook
- `dashboard-title`: human-readable dashboard title
- `projection-root`: current working directory; expected to be the target vault/workspace

If the user does not specify slug/title, derive them from `notebooklm status`.

## Step 1: Verify Auth

```bash
notebooklm status
```

If auth fails, run:

```bash
notebooklm login
```

## Step 2: Get Notebook Info

```bash
notebooklm status
```

Capture notebook id and notebook title.

## Step 3: Create Projection Folders

```bash
mkdir -p "Notes/NotebookLM/{notebook-slug}/Sources"
mkdir -p "Notes/NotebookLM/{notebook-slug}/QA"
mkdir -p "Notes/Dashboards"
```

## Step 4: Export Source List

```bash
notebooklm source list --json > /tmp/notebooklm-sources.json
```

Inspect source fields: `id`, `title`, `type`, `url`, `created_at`.

## Step 5: Create Source Files

```bash
python3 $HOME/.agents/skills/notebooklm/scripts/import_sources.py \
  --sources /tmp/notebooklm-sources.json \
  --slug {notebook-slug} \
  --dashboard "{dashboard-title}"
```

This creates one markdown file per source with frontmatter and related links.

## Step 6: Fetch Source Guides

The import script also fetches AI-generated source guides using:

```bash
notebooklm source guide <source-id> --json
```

For 20+ sources, expect a few minutes.

## Step 7: Create Dashboard

Use `templates/dashboard.md` as the reference materialized view:

- copy/adapt fields for the current notebook slug
- keep dashboard output in `Notes/Dashboards/`

## Step 8: Verify

```bash
ls "Notes/NotebookLM/{notebook-slug}/Sources" | wc -l
```

Validate:

- source count matches NotebookLM list
- source files contain frontmatter + source guide
- dashboard query paths match the notebook slug

## Output

- `Notes/NotebookLM/{notebook-slug}/Sources/*.md`
- `Notes/NotebookLM/{notebook-slug}/QA/`
- `Notes/Dashboards/{dashboard-title}.md`
