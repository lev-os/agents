# Security: 3-Scanner Audit

Run the security pipeline. This is NOT optional.

```bash
bash ~/.agents/skills/skill-builder/scripts/run-security-audit.sh {skill_path}/SKILL.md
```

Or manually:

Scanner 1 — Structural Decompile:
```bash
python3 ~/.agents/skills-db/security/skill-decompile/decompile.py {file} --output yaml
```
risk_score >= 60 → HARD REJECT.

Scanner 2 — Semantic Scan:
Load security-scanner skill in sandboxed read-only subagent.

Scanner 3 — AgentShield:
```bash
npx ecc-agentshield scan --path {dir} --min-severity medium
```

All pass → proceed. Any hard fail → REJECT + quarantine.
See references/security-audit-gates.md for the full rubric.
