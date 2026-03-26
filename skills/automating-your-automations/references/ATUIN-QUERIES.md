# Atuin Query Cookbook

## Schema

```sql
CREATE TABLE history (
    id TEXT PRIMARY KEY,         -- UUID
    timestamp INTEGER NOT NULL,  -- nanoseconds since epoch
    duration INTEGER NOT NULL,   -- nanoseconds (divide by 1e9 for seconds)
    exit INTEGER NOT NULL,       -- exit code (0 = success)
    command TEXT NOT NULL,        -- full command string
    cwd TEXT NOT NULL,           -- working directory
    session TEXT NOT NULL,        -- session UUID (groups commands in same shell)
    hostname TEXT NOT NULL        -- machine hostname
);
```

Always open read-only: `sqlite3 -readonly ~/.atuin/history.db`

---

## Pattern Detection Queries

### 1. Most Repeated Exact Commands

```sql
SELECT command, COUNT(*) as cnt,
       ROUND(AVG(duration) / 1e9, 2) as avg_sec,
       SUM(CASE WHEN exit != 0 THEN 1 ELSE 0 END) as fails,
       MIN(datetime(timestamp / 1e9, 'unixepoch', 'localtime')) as first_seen,
       MAX(datetime(timestamp / 1e9, 'unixepoch', 'localtime')) as last_seen
FROM history
GROUP BY command HAVING cnt > 5
ORDER BY cnt DESC LIMIT 50;
```

### 2. Command Prefixes (Semantic Groups)

```sql
SELECT substr(command, 1, instr(command || ' ', ' ') - 1) as base_cmd,
       COUNT(*) as cnt, COUNT(DISTINCT cwd) as unique_dirs,
       ROUND(AVG(duration) / 1e9, 2) as avg_sec
FROM history
GROUP BY base_cmd HAVING cnt > 10
ORDER BY cnt DESC LIMIT 30;
```

### 3. Multi-Step Workflows (Temporal Adjacency)

```sql
SELECT h1.command as step1, h2.command as step2,
       COUNT(*) as pair_cnt, h1.cwd as directory
FROM history h1
JOIN history h2
  ON h2.timestamp > h1.timestamp
  AND h2.timestamp < h1.timestamp + 10000000000
  AND h1.cwd = h2.cwd AND h1.session = h2.session AND h1.id != h2.id
GROUP BY step1, step2, directory HAVING pair_cnt > 3
ORDER BY pair_cnt DESC LIMIT 30;
```

### 4. Three-Step Chains

```sql
SELECT h1.command as step1, h2.command as step2, h3.command as step3,
       COUNT(*) as chain_cnt
FROM history h1
JOIN history h2
  ON h2.timestamp BETWEEN h1.timestamp AND h1.timestamp + 15000000000
  AND h1.session = h2.session
JOIN history h3
  ON h3.timestamp BETWEEN h2.timestamp AND h2.timestamp + 15000000000
  AND h2.session = h3.session
GROUP BY step1, step2, step3 HAVING chain_cnt > 2
ORDER BY chain_cnt DESC LIMIT 20;
```

### 5. High-Failure Commands

```sql
SELECT command, COUNT(*) as total,
       SUM(CASE WHEN exit != 0 THEN 1 ELSE 0 END) as fails,
       ROUND(100.0 * SUM(CASE WHEN exit != 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as fail_pct,
       ROUND(AVG(duration) / 1e9, 2) as avg_sec
FROM history
GROUP BY command HAVING total > 5 AND fail_pct > 20
ORDER BY total * fail_pct DESC LIMIT 20;
```

### 6. Time-of-Day Patterns

```sql
SELECT substr(command, 1, instr(command || ' ', ' ') - 1) as cmd,
       CAST(strftime('%H', timestamp / 1e9, 'unixepoch', 'localtime') AS INTEGER) as hour,
       COUNT(*) as cnt
FROM history
GROUP BY cmd, hour HAVING cnt > 5
ORDER BY cmd, hour;
```

### 7. Day-of-Week Patterns

```sql
SELECT substr(command, 1, instr(command || ' ', ' ') - 1) as cmd,
       CASE CAST(strftime('%w', timestamp / 1e9, 'unixepoch', 'localtime') AS INTEGER)
         WHEN 0 THEN 'Sun' WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue'
         WHEN 3 THEN 'Wed' WHEN 4 THEN 'Thu' WHEN 5 THEN 'Fri'
         WHEN 6 THEN 'Sat' END as dow,
       COUNT(*) as cnt
FROM history
GROUP BY cmd, dow HAVING cnt > 10
ORDER BY cmd, CAST(strftime('%w', timestamp / 1e9, 'unixepoch', 'localtime') AS INTEGER);
```

### 8. Commands by Working Directory

```sql
SELECT cwd, substr(command, 1, instr(command || ' ', ' ') - 1) as base_cmd,
       COUNT(*) as cnt, ROUND(AVG(duration) / 1e9, 2) as avg_sec
FROM history
GROUP BY cwd, base_cmd HAVING cnt > 10
ORDER BY cnt DESC LIMIT 40;
```

### 9. Longest-Running Commands

```sql
SELECT command, COUNT(*) as cnt,
       ROUND(AVG(duration) / 1e9, 1) as avg_sec,
       ROUND(MAX(duration) / 1e9, 1) as max_sec,
       ROUND(SUM(duration) / 1e9 / 3600, 2) as total_hours
FROM history WHERE duration > 0
GROUP BY command HAVING cnt > 3 AND avg_sec > 5
ORDER BY total_hours DESC LIMIT 20;
```

### 10. Retry Patterns

```sql
SELECT h1.command, COUNT(*) as retry_cnt
FROM history h1
JOIN history h2
  ON h1.command = h2.command
  AND h2.timestamp BETWEEN h1.timestamp AND h1.timestamp + 30000000000
  AND h1.session = h2.session
  AND h1.exit != 0 AND h2.exit = 0
GROUP BY h1.command HAVING retry_cnt > 2
ORDER BY retry_cnt DESC LIMIT 20;
```

---

## Analysis Queries

```sql
-- Overview
SELECT COUNT(*) as total, COUNT(DISTINCT command) as unique_cmds,
       COUNT(DISTINCT session) as sessions, COUNT(DISTINCT cwd) as dirs,
       MIN(datetime(timestamp/1e9, 'unixepoch', 'localtime')) as earliest,
       MAX(datetime(timestamp/1e9, 'unixepoch', 'localtime')) as latest
FROM history;

-- Diversity (lower = more repetitive = more automation opportunity)
SELECT ROUND(100.0 * COUNT(DISTINCT substr(command, 1, instr(command||' ',' ')-1)) / COUNT(*), 2) as diversity_pct
FROM history;

-- Total time waiting on commands >1s
SELECT ROUND(SUM(duration)/1e9/3600, 1) as wait_hours FROM history WHERE duration > 1e9;
```

## Export

```bash
sqlite3 -readonly -header -csv ~/.atuin/history.db \
  "SELECT command, COUNT(*) as cnt, AVG(duration)/1e9 as avg_sec,
   SUM(CASE WHEN exit!=0 THEN 1 ELSE 0 END) as fails
   FROM history GROUP BY command HAVING cnt > 3
   ORDER BY cnt DESC" > /tmp/atuin_patterns.csv
```

## Safety

- Always `-readonly` when opening atuin DB
- Don't touch `.db-wal` or `.db-shm` files
- `records.db` is sync state — ignore it
- Add `LIMIT` on large databases (>100MB)
