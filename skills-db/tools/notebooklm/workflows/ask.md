# Ask Notebook Workflow

Ask a NotebookLM notebook a question and save the answer as a markdown reference note
with `[N]` citations resolved to local passage-level links.

## Inputs

- `question`: question to ask
- `title`: short title for the Q&A note
- `notebook-slug`: notebook folder name
- `dashboard-title`: dashboard/materialized view title

## Step 1: Verify Auth

```bash
notebooklm status
```

If auth fails:

```bash
notebooklm login
```

## Step 2: Ask the Question

```bash
notebooklm ask --new --json "{question}" > /tmp/qa-output.json
```

Flags:

- `--new` to avoid conversational contamination
- `--json` to preserve structured references

## Step 3: Extract Passages

```bash
python3 $HOME/.agents/skills/notebooklm/scripts/extract_passages.py \
  --qa /tmp/qa-output.json \
  --sources /tmp/notebooklm-sources.json \
  --slug {notebook-slug} > /tmp/passage-map.json
```

This appends `## Cited Passages / ### Passage N` blocks to source files.

## Step 4: Resolve Citations

```bash
python3 $HOME/.agents/skills/notebooklm/scripts/resolve_citations.py \
  --qa /tmp/qa-output.json \
  --sources /tmp/notebooklm-sources.json \
  --slug {notebook-slug} \
  --passages /tmp/passage-map.json \
  --title "{title}" \
  --dashboard "{dashboard-title}" \
  --output "Notes/NotebookLM/{notebook-slug}/QA/{date} {title}.md"
```

This:

1. deduplicates evidence chunks
2. maps answer markers to source ids
3. resolves markers to local links
4. writes a durable reference note

## Step 5: Verify

Check that:

- source links render
- passage anchors scroll to evidence
- uncited sources are explicitly listed
- the Q&A note is reusable outside NotebookLM

## Batch Mode

For multiple questions:

1. run `notebooklm ask --new --json` per question
2. call `extract_passages.py` with all QA JSONs
3. resolve each note separately

## Output

- `Notes/NotebookLM/{notebook-slug}/QA/*.md`
- enriched source files with passage blocks
- reusable markdown citations suitable for downstream publishers
