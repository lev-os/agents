---
name: defendr
description: |
  [WHAT] 4-layer security scanner for untrusted code: static analysis, malware/CVE scanning, Docker sandbox, agentic review.
  [HOW] Orchestrates rg patterns, ClamAV, pip-audit, osv-scanner, semgrep, Docker strace, and LLM code review.
  [WHEN] Before running cloned repos, installing pip/npm packages, intake of external code, pre-commit on untrusted PRs, workshop evaluation.
  [WHY] Agents clone and execute code from the internet. One malicious setup.py and your machine is owned.

  Triggers: "security scan", "malware scan", "defendr", "scan for malware", "virus scan", "supply chain",
    "is this safe", "scan this repo", "audit dependencies", "sandbox", "before running", "untrusted code"
skill_type: leaf
version: 1.0.0
---

# Defendr — 4-Layer Security Scanner

Run all 4 layers in order. Stop and flag on any critical finding.

## Layer 1: Static Pattern Analysis

No tools needed. Uses `rg` (ripgrep). Run this FIRST on raw source before any install.

### Supply Chain (setup.py / pyproject.toml / package.json)

```bash
# Code execution in install scripts
rg --glob '**/setup.py' -n 'os\.system\(|subprocess\.(call|run|Popen)\(|eval\(|exec\(' TARGET_DIR

# Custom build backends (not setuptools/flit/poetry/hatch)
rg --glob '**/pyproject.toml' -n 'build-backend.*=.*(?!setuptools|flit|poetry|hatch|maturin)' TARGET_DIR

# npm install hooks
rg --glob '**/package.json' -n '"(pre|post)install"\s*:\s*"' TARGET_DIR

# curl|sh pattern
rg --glob '**/{Makefile,*.sh,install*}' -n 'curl\s.*\|\s*(sh|bash)|wget\s.*\|\s*(sh|bash)' TARGET_DIR

# Dynamic imports in setup
rg --glob '**/setup.py' -n '__import__\(' TARGET_DIR
```

### Obfuscation

```bash
# Base64 decode + exec (classic payload delivery)
rg -n 'base64\.(b64)?decode.*exec|exec.*base64\.(b64)?decode' TARGET_DIR

# Hex-encoded or rot13 strings
rg -n '\\x[0-9a-f]{2}\\x[0-9a-f]{2}\\x[0-9a-f]{2}|codecs\.decode\(.*rot13' TARGET_DIR

# Eval with constructed string
rg -n 'eval\(\s*['"'"'"].*['"'"'"]\s*\+|eval\(\s*chr\(|eval\(\s*"\\x' TARGET_DIR

# JavaScript packer
rg --glob '**/*.js' -n 'eval\(function\(p,a,c,k,e,[rd]\)' TARGET_DIR
```

### Network / Reverse Shells

```bash
# Reverse shell patterns
rg -n '/bin/sh\s+-i|socket\.connect.*\d+\.\d+\.\d+\.\d+|nc\s+-e\s+/bin|bash\s+-c\s.*dev/tcp' TARGET_DIR

# HTTP POST to hardcoded IP
rg --glob '**/*.py' -n 'requests\.(post|put)\(['"'"'"]https?://\d+\.\d+\.\d+\.\d+' TARGET_DIR

# DNS exfiltration
rg --glob '**/*.py' -n 'socket\.getaddrinfo\(.*\+.*\+|\.encode\(\)\.hex\(\).*resolve' TARGET_DIR
```

### Hardcoded Secrets

```bash
# API keys / tokens
rg -n '['"'"'"](?:sk-|ak-|AKIA|ghp_|gho_|github_pat_)[a-zA-Z0-9]{20,}['"'"'"]' TARGET_DIR

# Private keys
rg -n '-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----' TARGET_DIR

# AWS access keys
rg -n 'AKIA[0-9A-Z]{16}' TARGET_DIR
```

### Prompt Injection

```bash
# LLM prompt injection in source/docs
rg -i -n 'ignore\s+(all\s+)?previous\s+instructions|you\s+are\s+now\s+a|system\s*:\s*you\s+are' TARGET_DIR

# Hidden instructions in HTML/Markdown comments
rg -i --glob '**/*.{md,html}' -n '<!--.*(?:ignore|override|bypass|admin|sudo|root|secret).*-->' TARGET_DIR
```

**Verdict:** Any match in setup.py/pyproject.toml = STOP. Review manually. Matches in application code = flag and continue to Layer 2.

## Layer 2: Tool-Based Scanning

Install these tools, then scan.

### ClamAV (malware signatures)

```bash
# Install (one-time)
brew install clamav
cd /opt/homebrew/etc/clamav/
cp freshclam.conf.sample freshclam.conf
sed -i '' 's/^Example/#Example/' freshclam.conf
freshclam    # Downloads ~300MB virus definitions

# Scan
clamscan -r --infected --no-summary TARGET_DIR
# Exit code 1 = virus found. Any "FOUND" line = STOP.
```

### pip-audit (Python CVEs)

```bash
# Install
pip install pip-audit

# Scan requirements.txt
pip-audit --requirement TARGET_DIR/requirements.txt --format json

# Scan installed venv
pip-audit --format json
```

### osv-scanner (multi-ecosystem CVEs)

```bash
# Install
brew install osv-scanner

# Scan (recursive, all ecosystems)
osv-scanner --format json -r TARGET_DIR
```

### semgrep (SAST rules)

```bash
# Install
pip install semgrep

# Scan with auto rules
semgrep --config auto --json TARGET_DIR
```

### Check tool availability

```bash
command -v clamscan && echo "ClamAV: ready" || echo "ClamAV: MISSING — brew install clamav && freshclam"
command -v pip-audit && echo "pip-audit: ready" || echo "pip-audit: MISSING — pip install pip-audit"
command -v osv-scanner && echo "osv-scanner: ready" || echo "osv-scanner: MISSING — brew install osv-scanner"
command -v semgrep && echo "semgrep: ready" || echo "semgrep: MISSING — pip install semgrep"
```

**Verdict:** ClamAV FOUND = STOP. Critical CVEs with no fix = flag. High CVEs = warn and continue.

## Layer 3: Docker Sandbox

Install deps inside an isolated container. Monitor syscalls. No network access.

### Build the sandbox

```bash
# Create scan container (one-time, reusable)
docker run -d \
  --name defendr-sandbox \
  --network none \
  --memory 512m \
  --cpus 1.0 \
  --read-only \
  --tmpfs /tmp:rw,size=256m \
  --tmpfs /root:rw,size=64m \
  -v "$(pwd)/TARGET_DIR:/scan:ro" \
  python:3.12-slim \
  sleep infinity

# Or reuse existing
docker start defendr-sandbox 2>/dev/null || echo "create it first"
```

### Run sandboxed install with strace

```bash
docker exec defendr-sandbox bash -c '
  apt-get update -qq && apt-get install -y -qq strace >/dev/null 2>&1
  cd /scan
  if [ -f requirements.txt ]; then
    strace -f -e trace=network,open,connect -o /tmp/trace.log \
      pip install --no-cache-dir -r requirements.txt 2>&1
  elif [ -f setup.py ] || [ -f pyproject.toml ]; then
    strace -f -e trace=network,open,connect -o /tmp/trace.log \
      pip install --no-cache-dir . 2>&1
  fi

  echo "=== SUSPICIOUS FILE ACCESS ==="
  grep -E "open.*(etc/passwd|etc/shadow|\.ssh/|\.aws/|\.config/)" /tmp/trace.log 2>/dev/null || echo "none"

  echo "=== NETWORK CALLS ==="
  grep -c "connect(" /tmp/trace.log 2>/dev/null || echo "0"

  echo "=== NON-TEMP FILE WRITES ==="
  grep "O_WRONLY\|O_CREAT" /tmp/trace.log | grep -v "/tmp\|/proc\|__pycache__\|\.pyc" | head -20
'
```

### Cleanup

```bash
docker stop defendr-sandbox && docker rm defendr-sandbox
```

**Verdict:** Any access to `/etc/passwd`, `/.ssh/`, `/.aws/` = CRITICAL. Network calls during install with `--network=none` = suspicious (should fail silently). Non-temp file writes outside package dirs = flag.

## Layer 4: Agentic Review

After Layers 1-3, if findings exist, review the flagged files with an LLM.

### What to review

Feed each flagged file to the LLM with this prompt:

```
You are a security auditor. This file was flagged by automated scanning.

File: {path}
Flag: {rule_id} — {description}
Matched line: {match}

Analyze this file for:
1. Is this a genuine security risk or a false positive?
2. If genuine: what is the attack vector?
3. If false positive: explain why the pattern matched but is safe.
4. Severity: critical / high / medium / low / false-positive

Respond with a structured verdict.
```

### Decision matrix

| Layer 1 | Layer 2 | Layer 3 | Layer 4 | Verdict |
|---------|---------|---------|---------|---------|
| clean | clean | clean | — | SAFE — proceed |
| flags | clean | clean | false-positive | SAFE — proceed |
| flags | clean | clean | genuine | BLOCK — do not execute |
| clean | CVEs | clean | — | WARN — update deps |
| any | FOUND | any | — | BLOCK — malware detected |
| any | any | suspicious | genuine | BLOCK — behavioral threat |

## Quick Run (All 4 Layers)

```bash
TARGET=poc/osint/username-search/sherlock

echo "=== LAYER 1: Static ==="
rg --glob '**/setup.py' -n 'os\.system\|subprocess\|eval\(|exec\(' "$TARGET"
rg -n 'base64.*decode.*exec|-----BEGIN.*PRIVATE KEY|AKIA[0-9A-Z]{16}' "$TARGET"
rg -n '/bin/sh\s+-i|socket\.connect|reverse.shell' "$TARGET"

echo "=== LAYER 2: Tools ==="
clamscan -r --infected --no-summary "$TARGET"
pip-audit --requirement "$TARGET/requirements.txt" --format json 2>/dev/null
osv-scanner -r "$TARGET" --format json 2>/dev/null

echo "=== LAYER 3: Sandbox ==="
docker exec defendr-sandbox bash -c 'cd /scan && pip install --no-cache-dir -r requirements.txt 2>&1 | tail -5'

echo "=== LAYER 4: Review flagged files ==="
# Feed any findings to LLM for verdict
```

## Error Handling

| Error | Fix |
|-------|-----|
| `rg: command not found` | `brew install ripgrep` |
| `clamscan: command not found` | `brew install clamav && freshclam` |
| `pip-audit: command not found` | `pip install pip-audit` |
| `osv-scanner: command not found` | `brew install osv-scanner` |
| `docker: command not found` | Install Docker Desktop or `brew install colima && colima start` |
| `freshclam` fails | Check `/opt/homebrew/etc/clamav/freshclam.conf` has `Example` commented out |
| Container can't write | Add `--tmpfs /tmp:rw,size=256m` to docker run |
