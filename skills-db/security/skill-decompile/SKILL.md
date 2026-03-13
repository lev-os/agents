---
name: skill-decompile
description: "Decompile any SKILL.md into deterministic YAML for structural security analysis. Extracts permissions, surfaces, risk signals, and produces a scored verdict."
skill_type: tool
category: security
allowed-tools: Bash(python3:*), Read
argument-hint: "<skill.md> [--output yaml|json] [--verbose] | --dir <path> [--report]"
---

# Skill Decompile — SKILL.md Security Scanner

Converts freeform SKILL.md files into normalized, machine-auditable YAML structures. Bridges the gap between human-authored skill definitions and deterministic security scanning.

## Usage

```bash
# Single file
python3 ~/.agents/skills-db/security/skill-decompile/decompile.py ~/.agents/skills/auth-sniffer/SKILL.md

# Single file, JSON output
python3 ~/.agents/skills-db/security/skill-decompile/decompile.py ~/.agents/skills/auth-sniffer/SKILL.md --output json --verbose

# Scan entire skills directory with summary report
python3 ~/.agents/skills-db/security/skill-decompile/decompile.py --dir ~/.agents/skills/ --report

# Full directory scan as YAML
python3 ~/.agents/skills-db/security/skill-decompile/decompile.py --dir ~/.agents/skills/ --output yaml
```

## What It Extracts

| Category | Details |
|----------|---------|
| **meta** | name, description, skill_type, source (local/external) |
| **permissions** | allowed_tools, requests for bash/write/network/env |
| **surfaces** | URLs, shell commands, env vars, file paths |
| **risk_signals** | eval, base64, obfuscation, exfil patterns, prompt injection |
| **complexity** | line count, code blocks, reference files, decision tree depth |
| **verdict** | risk_score (0-100), risk_level, specific flags |

## Risk Scoring

- 0-20: **safe** — no concerning patterns
- 21-40: **low** — minor signals, likely benign
- 41-60: **medium** — review recommended
- 61-80: **high** — manual audit required
- 81-100: **critical** — block until reviewed

## When to Use

- Before installing a third-party skill
- Periodic security audit of skill inventory
- CI/CD gate for skill contributions
- Comparing skill versions for permission drift
