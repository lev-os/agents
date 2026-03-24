# Scaffold: Generate Skill Directory

Produce the full directory structure:

```
{skill-name}/
├── dna.yaml           # The graph declaration (entry, nodes, edges, contracts)
├── nodes/             # Content for each node
│   ├── intake.md
│   ├── {route-a}.md
│   └── deliver.md
├── bin/
│   └── flow           # Symlink to shared flow CLI or copy
├── schemas/           # Output validation schemas (if needed)
└── anti_patterns.yaml # Optional: extracted for reuse
```

Generate dna.yaml from the authored steps. Each step becomes a node.
Routes become edges. Validation becomes contracts.

After generating, validate:
```bash
python3 ~/.agents/skills/skill-builder/bin/flow validate --skill {output_path}
```

Must exit 0. Fix any errors before proceeding.
