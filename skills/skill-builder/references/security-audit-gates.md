# Security Audit Gates — External Skill Installation

Reference for Step 2b of the Skill Installation from External Sources pipeline.

## When This Applies

- External skills ONLY (installed via `skills.sh`, `skill://`, or cloned from third-party repos)
- Runs AFTER Step 2 (Validate hard gates) and BEFORE Step 3 (Prior Art Check)
- Skipped entirely for local authoring via skill-creator or codifier pipeline

## Scanner 1: Structural Decompile

**Cost:** Free, instant
**Tool:** `~/.agents/skills-db/security/skill-decompile/decompile.py`

Statically analyzes the SKILL.md and any referenced scripts for structural risk signals.

### Risk Score Rubric (0-100)

| Signal | Points | Description |
|--------|--------|-------------|
| Bash commands with `curl \| sh` | +30 | Pipe-to-shell execution |
| References to `~/.ssh`, `~/.aws`, credentials paths | +25 | Credential access |
| `eval`, `exec`, dynamic code generation | +20 | Code injection surface |
| Encoded/obfuscated content (base64 blocks, hex) | +20 | Obfuscation |
| `rm -rf`, `chmod 777`, destructive commands | +15 | Destructive operations |
| Network calls (`curl`, `wget`, `fetch`) to non-standard hosts | +15 | Exfiltration risk |
| MCP tool definitions or `mcp_add` calls | +10 | MCP surface expansion |
| `git push --force`, `git reset --hard` | +10 | Repo destructive ops |
| Write to system dirs (`/etc`, `/usr/local`) | +10 | System modification |
| No references/ directory (monolithic) | +5 | Minor structural concern |

### Thresholds

| Score | Verdict |
|-------|---------|
| 0-29 | PASS — low risk, proceed |
| 30-59 | WARN — flag concerns, proceed with caution |
| 60+ | FAIL — hard reject, do not proceed to Scanner 2 |

## Scanner 2: Semantic Scan

**Cost:** Agent-based, ~10 seconds
**Tool:** `security-scanner` skill (hiroro) in sandboxed subagent

Runs a Read-only subagent that analyzes the skill's natural language content for adversarial patterns.

### What It Checks

- **Prompt injection:** Instructions that override agent behavior ("ignore previous instructions", "you are now...")
- **Social engineering:** Urgency language designed to bypass review ("critical: run immediately", "do not verify")
- **Hidden instructions:** Content designed to be read by agents but not humans (zero-width characters, comment-embedded commands)
- **Privilege escalation:** Instructions to grant broader tool access, disable safety checks, or skip validation steps
- **Data exfiltration:** Instructions to send workspace content to external endpoints

### Output

| Result | Meaning |
|--------|---------|
| `pass` | No adversarial patterns detected |
| `warn` | Suspicious patterns found but ambiguous — present to user |
| `fail` | Clear adversarial intent detected |

## Scanner 3: AgentShield CLI

**Cost:** CLI-based, ~5 seconds
**Tool:** `npx ecc-agentshield scan`

Static analysis focused on agent-specific attack surfaces.

### What It Checks

- **Hook injection:** Pre/post hooks that execute arbitrary code
- **MCP risks:** Unauthorized MCP server additions, tool overrides
- **Overpermissive configs:** Skills requesting `dangerouslyDisableSandbox`, unrestricted Bash, or write-all permissions
- **Dependency chain risks:** References to external packages with known vulnerabilities
- **Config manipulation:** Attempts to modify `.claude/settings.json`, `CLAUDE.md`, or other agent configs

### Severity Levels

| Severity | Action |
|----------|--------|
| `info` | Logged, no action needed |
| `low` | Noted in catalog entry |
| `medium` | Flagged for user review (minimum scan threshold) |
| `high` | Blocks promotion, requires explicit user override |
| `critical` | Hard REJECT, triggers quarantine |

## Composite Verdict Matrix

| Scanner 1 | Scanner 2 | Scanner 3 | Final Verdict |
|-----------|-----------|-----------|---------------|
| PASS | pass | pass | PROCEED to Step 3 |
| PASS | pass | warn (medium) | PROCEED with user confirmation |
| PASS | warn | pass | PROCEED with user confirmation |
| PASS | warn | warn | PROCEED with user confirmation + detailed report |
| PASS | fail | any | REJECT — semantic threat |
| PASS | any | critical | REJECT + QUARANTINE |
| WARN | pass | pass | PROCEED with advisory note |
| WARN | warn+ | any | REJECT unless user explicitly overrides |
| FAIL (>=60) | — | — | HARD REJECT — early termination, Scanners 2-3 skipped |

## Quarantine Protocol

When a skill is quarantined:

1. Move to `~/.agents/skills-db/.archive/{name}/` with `_QUARANTINED` suffix
2. Write `quarantine-report.yaml` alongside the skill with:
   - Scanner results (all that ran)
   - Specific flags triggered
   - Timestamp
   - Source URL
3. Log to `~/.agents/skills-db/security/audit-log.jsonl`
4. Notify user with summary of findings
5. Quarantined skills cannot be activated without explicit `--force-install` and re-audit

## Audit Log Format

Each scan appends to `~/.agents/skills-db/security/audit-log.jsonl`:

```json
{
  "timestamp": "2026-03-10T12:00:00Z",
  "skill_name": "example-skill",
  "source": "github.com/user/repo",
  "scanner_1": {"risk_score": 25, "verdict": "pass", "flags": []},
  "scanner_2": {"verdict": "pass", "patterns": []},
  "scanner_3": {"verdict": "pass", "findings": []},
  "final_verdict": "proceed",
  "promoted": true
}
```
