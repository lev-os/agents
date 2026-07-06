# Pattern Detection Algorithms

## Clustering Methods

### Exact Match

`GROUP BY command` — catches identical commands.

### Prefix Clustering

`GROUP BY substr(command, 1, instr(command, ' '))` — catches variations:

```
git commit -m "fix: login bug"  → git commit -m "<msg>"
git commit -m "feat: add navbar" → git commit -m "<msg>"
```

### Parameterized Template Clustering

1. Tokenize command by spaces
2. Per token position across prefix group: >50% unique values → `<param>`, else keep literal
3. Group by resulting template

### Temporal Adjacency

Commands within N seconds in the same session = workflow steps:

```sql
SELECT h1.command, h2.command, COUNT(*) as co_occurrence
FROM history h1
JOIN history h2 ON h2.timestamp BETWEEN h1.timestamp AND h1.timestamp + 10e9
  AND h1.session = h2.session AND h1.id < h2.id
GROUP BY h1.command, h2.command
HAVING co_occurrence > 3
ORDER BY co_occurrence DESC;
```

### Directory-Scoped

Same command in different `cwd` = different automation. Group by `(cwd, command_template)`.

---

## Scoring Algorithm (Expanded)

### Input Metrics

| Metric | Source | Range |
|--------|--------|-------|
| `frequency` | `COUNT(*)` | 1-N |
| `avg_duration` | `AVG(duration)/1e9` | 0-N seconds |
| `fail_rate` | failed/total | 0.0-1.0 |
| `chain_length` | Steps in workflow | 1-N |
| `recency` | Days since last occurrence | 0-N |

### Normalization

```
freq_norm    = min(ln(frequency) / ln(max_freq), 1.0)
time_norm    = min((avg_duration * frequency) / 3600, 1.0)
fail_norm    = fail_rate
chain_norm   = min((chain_length - 1) / 5, 1.0)
recency_norm = max(1.0 - days_since_last / 30, 0.0)
```

### 5-Factor Composite (full precision)

```
score = freq_norm×0.30 + time_norm×0.25 + fail_norm×0.15
      + chain_norm×0.15 + recency_norm×0.15
```

The SKILL.md uses a simplified 4-factor version (without chain_length and recency) for quick scoring. Use this 5-factor version when building a Rust CLI analyzer.

### Thresholds

| Score | Action |
|-------|--------|
| >= 0.7 | **Automate immediately** |
| 0.4-0.7 | **Consider automating** |
| 0.3-0.4 | **Monitor** |
| < 0.3 | **Skip** |

---

## Advanced: Ritual Detection

Session-start rituals (first 3 commands of each session):

```sql
WITH session_starts AS (
    SELECT session, command,
           ROW_NUMBER() OVER (PARTITION BY session ORDER BY timestamp) as cmd_order
    FROM history
)
SELECT command, COUNT(*) as cnt
FROM session_starts
WHERE cmd_order <= 3
GROUP BY command
HAVING cnt > 5
ORDER BY cnt DESC LIMIT 10;
```

If same 2-3 commands appear in >50% of session starts → candidate for startup script or shell hook.

---

## Advanced: Periodic Pattern Detection

Commands with regular intervals → systemd timer candidates:

```sql
WITH intervals AS (
    SELECT command,
           timestamp - LAG(timestamp) OVER (PARTITION BY command ORDER BY timestamp) as gap_ns
    FROM history
)
SELECT command,
       COUNT(*) as occurrences,
       ROUND(AVG(gap_ns) / 1e9 / 3600, 1) as avg_gap_hours,
       ROUND(
           CASE WHEN AVG(gap_ns) > 0
                THEN SQRT(AVG(gap_ns * gap_ns) - AVG(gap_ns) * AVG(gap_ns)) / AVG(gap_ns)
                ELSE 999 END, 2
       ) as regularity  -- lower = more regular
FROM intervals
WHERE gap_ns IS NOT NULL AND gap_ns > 60000000000
GROUP BY command
HAVING occurrences > 5
ORDER BY regularity ASC LIMIT 20;
```

`regularity < 0.5` = strong timer candidate.

---

## Extraction: Systemd & Journalctl

```bash
# Extract all user timer/service pairs
for timer in ~/.config/systemd/user/*.timer; do
    name=$(basename "$timer" .timer)
    echo "$name"
    grep -E 'OnCalendar|OnUnitActiveSec|OnBootSec' "$timer" 2>/dev/null
    grep -E 'ExecStart' ~/.config/systemd/user/"$name".service 2>/dev/null
    echo "---"
done

# Services that failed in the past week
journalctl --user --since "7 days ago" --priority=err --no-pager -o json \
  | jq -r '.UNIT // .SYSLOG_IDENTIFIER' | sort | uniq -c | sort -rn
```
