# Skill Seekers: Extract from External Source

Preflight:
```bash
command -v skill-seekers || echo "NOT INSTALLED — see references/setup.md"
```

If not installed, guide the user through references/setup.md.

Run extraction based on source type:
```bash
# Website
skill-seekers scrape --name {name} --url {url}

# GitHub repo
skill-seekers github --repo {owner/repo}

# PDF
skill-seekers pdf --pdf {file} --name {name}

# Multi-source
skill-seekers unified --config {config.json}
```

After extraction, check output:
```bash
ls output/{name}/SKILL.md
```

For large docs (>5K pages), see references/advanced-commands.md for splitting strategies.

After successful extraction, proceed to authoring to apply the format spec.
