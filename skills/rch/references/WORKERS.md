# Worker Management

## Update Rust on All Workers

```bash
# Get worker IPs and keys from config
cat ~/.config/rch/workers.toml

# Update each (parallel-safe)
ssh -i ~/.ssh/KEY.pem ubuntu@IP "rustup update nightly && rustup default nightly && rustc --version"
```

### Batch Update Script

```bash
#!/bin/bash
workers=(
  "css:~/.ssh/contabo_new_baremetal_superserver_box.pem:209.145.54.164"
  "csd:~/.ssh/contabo_new_baremetal_sense_demo_box.pem:144.126.137.164"
  "fmd:~/.ssh/je_ovh_ssh_key.pem:51.222.245.56"
  "yto:~/.ssh/je_ovh_ssh_key.pem:37.187.75.150"
)

for w in "${workers[@]}"; do
  IFS=':' read -r name key ip <<< "$w"
  echo "=== Updating $name ($ip) ==="
  ssh -i "$key" "ubuntu@$ip" "rustup update nightly && rustc --version" &
done
wait
echo "All workers updated"
```

---

## Add a New Worker

1. **Ensure SSH access:**
   ```bash
   ssh -i ~/.ssh/NEW_KEY.pem ubuntu@NEW_IP "echo 'Connected'"
   ```

2. **Install Rust:**
   ```bash
   ssh -i ~/.ssh/NEW_KEY.pem ubuntu@NEW_IP \
     "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain nightly"
   ```

3. **Add to config** (`~/.config/rch/workers.toml`):
   ```toml
   [[workers]]
   id = "new-worker"
   host = "NEW_IP"
   user = "ubuntu"
   identity_file = "~/.ssh/NEW_KEY.pem"
   total_slots = 16        # Based on CPU cores
   priority = 90           # Higher = preferred
   tags = ["provider-name"]
   ```

4. **Verify:**
   ```bash
   rch workers list
   rch workers probe new-worker
   ```

---

## Remove/Disable a Worker

### Temporary (Drain)

```bash
rch workers drain WORKER_ID
# Note: Drain state is in-memory, resets on daemon restart
```

### Permanent

Comment out in `~/.config/rch/workers.toml`:
```toml
# [[workers]]
# id = "broken-worker"
# ...
```

Then restart daemon:
```bash
pkill -9 rchd; rch daemon start
```

---

## Worker Selection Logic

RCH selects workers based on:
1. **Available slots** (total - in-use)
2. **Priority** (higher preferred)
3. **Speed benchmark** (if run)
4. **Circuit breaker state** (closed = healthy)

Run benchmarks:
```bash
rch workers benchmark
```

---

## Verify Worker Rust Installation

```bash
# Quick check all workers
for w in $(rch workers list --json 2>/dev/null | jq -r '.data[].id'); do
  echo -n "$w: "
  # Extract connection info and test
  host=$(grep -A5 "id = \"$w\"" ~/.config/rch/workers.toml | grep host | head -1 | cut -d'"' -f2)
  key=$(grep -A5 "id = \"$w\"" ~/.config/rch/workers.toml | grep identity | head -1 | cut -d'"' -f2)
  key="${key/#\~/$HOME}"
  ssh -i "$key" -o ConnectTimeout=5 "ubuntu@$host" "rustc --version 2>/dev/null || echo 'NO RUST'" 2>/dev/null
done
```
