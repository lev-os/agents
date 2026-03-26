---
name: automating-your-automations
description: >-
  Mine atuin history and shell logs to find repetitive workflows, build
  Rust CLI or bash automations. Use when analyzing command patterns or
  finding automation opportunities.
---

<!-- TOC: Core Insight | The Loop | Mine | Score | Propose | Build | Anti-Patterns | References -->

# Automating Your Automations

> **Core Insight:** Your command history is a fossil record of automation opportunities. Every repeated multi-step workflow is a Rust CLI waiting to be born.

| Principle | Implication |
|-----------|-------------|
| **Frequency x Pain = Priority** | 3-command sequence 50x/week > 10-command sequence 1x/month |
| **Complex → Rust; simple → bash** | State, error handling, SQLite → Rust CLI. Glue → bash |

---

## The Loop (Mandatory)

```
1. MINE      → atuin DB, zsh_history, systemd timers, journalctl
2. CLUSTER   → semantic similarity + temporal adjacency
3. SCORE     → frequency × time_saved × error_rate
4. PROPOSE   → Rust CLI vs bash script vs alias vs systemd timer
5. BUILD     → /rust-cli-with-sqlite or bash in ~/.local/bin/
6. VALIDATE  → 5x run, --dry-run, --robot JSON, ≥3x faster
7. INSTALL   → systemd timer, shell alias, or PATH binary
```

**Never skip 1-3.** Intuition about what's repetitive is unreliable; data wins.

---

## Step 1: Mine

### Data Sources

| Source | Location | Unique Value |
|--------|----------|--------------|
| **Atuin DB** | `~/.atuin/history.db` | Duration, exit codes, cwd, session grouping |
| **zsh_history** | `~/.zsh_history` | Timestamps in extended format |
| **Systemd** | `~/.config/systemd/user/*.timer` | Existing automation to audit |
| **Journalctl** | `journalctl --user` | Failure patterns |
| **bash/git/cron** | `~/.bash_history`, `git log`, `crontab -l` | Fallback sources |

### Essential Atuin Queries

Open read-only: `sqlite3 -readonly ~/.atuin/history.db`

Atuin stores `timestamp` and `duration` in **nanoseconds**. Exit 0 = success.

```sql
-- Top repeated commands
SELECT command, COUNT(*) as cnt, AVG(duration)/1e9 as avg_sec,
       SUM(CASE WHEN exit != 0 THEN 1 ELSE 0 END) as fails
FROM history GROUP BY command HAVING cnt > 5 ORDER BY cnt DESC LIMIT 30;

-- Multi-step workflows (commands within 10s in same session/cwd)
SELECT h1.command as step1, h2.command as step2, COUNT(*) as pair_cnt
FROM history h1 JOIN history h2
  ON h2.timestamp BETWEEN h1.timestamp AND h1.timestamp + 10000000000
  AND h1.cwd = h2.cwd AND h1.session = h2.session AND h1.id != h2.id
GROUP BY step1, step2 HAVING pair_cnt > 3
ORDER BY pair_cnt DESC LIMIT 20;

-- High-failure commands (retry/guard candidates)
SELECT command, COUNT(*) as total,
       ROUND(100.0 * SUM(CASE WHEN exit != 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as fail_pct
FROM history GROUP BY command HAVING total > 5 AND fail_pct > 20
ORDER BY total DESC LIMIT 20;
```

**Full cookbook (10 queries + export + analysis):** [ATUIN-QUERIES.md](references/ATUIN-QUERIES.md)

### THE EXACT PROMPT

```
Analyze my command history to find automation opportunities.

1. Query atuin DB: repeated commands, multi-step workflows,
   high-failure commands, time-of-day patterns, retry patterns
2. Inspect systemd user timers for gaps and silent failures
3. Score each pattern: frequency × time_saved × error_rate
4. Output top 10 candidates with: pattern, frequency, time estimate,
   recommended implementation (Rust/bash/alias/timer), complexity (S/M/L)
```

---

## Step 2: Score

| Factor | Weight | Source |
|--------|--------|--------|
| **Frequency** | 40% | `COUNT(*)` from atuin |
| **Time saved** | 30% | `AVG(duration) × frequency` |
| **Error rate** | 20% | `fail_pct` from atuin |
| **Simplicity** | 10% | Inverse of implementation complexity |

```
Score = freq_norm×0.4 + time_norm×0.3 + fail_norm×0.2 + simplicity_norm×0.1
```

Only automate if Score >= 0.3. **Expanded 5-factor formula with normalization:** [PATTERN-DETECTION.md](references/PATTERN-DETECTION.md)

---

## Step 3: Propose

```
Stateful? (remembers across runs)
├─ YES → Rust CLI + SQLite (/rust-cli-with-sqlite)
│  ├─ Scheduled? → systemd timer
│  └─ Interactive? → clap subcommands + --robot JSON
└─ NO
   ├─ >3 steps? → bash script → ~/.local/bin/
   ├─ Retry/guard? → bash wrapper + set -euo pipefail
   └─ Single command? → shell alias → ~/.zshrc.local
```

---

## Step 4: Build

**Rust CLIs** — every automation CLI must have:
- `--robot` / `--json` for machine output
- `--dry-run` for safe testing
- Non-zero exit codes on failure

Scaffold template: [RUST-SCAFFOLD.md](references/RUST-SCAFFOLD.md)

**Bash scripts** — always `set -euo pipefail`, install to `~/.local/bin/`

**Systemd timers** — creation, activation, monitoring: [SYSTEMD.md](references/SYSTEMD.md)

---

## Step 5: Validate

- [ ] Run 5x, compare output to manual execution
- [ ] `--dry-run` produces no side effects
- [ ] `--robot` output parses as valid JSON
- [ ] Automated ≥ 3x faster than manual
- [ ] Force failure → verify graceful behavior

---

## Anti-Patterns

| Don't | Instead |
|-------|---------|
| Automate before measuring | Run atuin queries first |
| Rust CLI for 2-line glue | Bash script or alias |
| Skip `--dry-run` | Always add dry-run mode |
| Ignore exit codes | Non-zero exit + logging |
| Automate rare commands (Score < 0.3) | Skip — maintenance > benefit |
| One giant script | Unix philosophy: small composable tools |

---

## Integration

| Need | Skill |
|------|-------|
| Rust CLI + SQLite patterns | `/rust-cli-with-sqlite` |
| Search prior agent sessions | `/cass` |
| Turn automation into a skill | `/sc` + `/sw` |
| Track automation tasks | `/br` |
| Optimize slow commands | `/extreme-software-optimization` |

---

## Reference Index

| Need | Read |
|------|------|
| Full atuin query cookbook (10 queries) | [ATUIN-QUERIES.md](references/ATUIN-QUERIES.md) |
| Shell history parsing (zsh/bash/fish) | [SHELL-HISTORY.md](references/SHELL-HISTORY.md) |
| Systemd timers: create, audit, monitor | [SYSTEMD.md](references/SYSTEMD.md) |
| Rust CLI scaffold + Cargo.toml | [RUST-SCAFFOLD.md](references/RUST-SCAFFOLD.md) |
| Real-world examples with scores | [EXAMPLES.md](references/EXAMPLES.md) |
| Clustering + scoring algorithms | [PATTERN-DETECTION.md](references/PATTERN-DETECTION.md) |

---

## Done When

- [ ] Atuin DB queried for all pattern types
- [ ] Top candidates scored and ranked
- [ ] At least one automation built and validated
- [ ] Automation installed (PATH, alias, or systemd timer)
- [ ] Time savings measured
