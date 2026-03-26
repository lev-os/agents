# GDB Batch Mode Recipes

> **Rule:** Agents must NEVER use interactive GDB. These recipes are all batch-mode, non-blocking, and safe to pipe to files.

---

## Recipe 1: Quick Backtrace (Most Common)

```bash
PID=12345
gdb --batch \
  -ex "set pagination off" \
  -ex "thread apply all bt" \
  -p $PID 2>&1 | tee /tmp/gdb_bt_$PID.txt
```

## Recipe 2: Full Backtrace with Local Variables

```bash
PID=12345
gdb --batch \
  -ex "set pagination off" \
  -ex "set print pretty on" \
  -ex "set print elements 200" \
  -ex "thread apply all bt full" \
  -p $PID 2>&1 | tee /tmp/gdb_full_bt_$PID.txt
```

## Recipe 3: Safe Attach-Capture-Detach with ptrace Management

The "kitchen sink" recipe — handles ptrace, captures everything, restores state:

```bash
#!/usr/bin/env bash
set -euo pipefail
PID=${1:?Usage: $0 PID}
OUT=/tmp/gdb_capture_${PID}_$(date +%s).txt

# Verify process exists
ps -p $PID -o pid,comm,args >/dev/null 2>&1 || { echo "PID $PID not found"; exit 1; }

# Save and relax ptrace
ORIG=$(cat /proc/sys/kernel/yama/ptrace_scope)
if [[ "$ORIG" != "0" ]]; then
  sudo sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'
  echo "ptrace_scope: $ORIG -> 0"
fi

# Capture
timeout 30s gdb --batch \
  -ex "set confirm off" \
  -ex "set pagination off" \
  -ex "set print thread-events off" \
  -ex "set print pretty on" \
  -ex "info threads" \
  -ex "thread apply all bt full" \
  -ex "info registers" \
  -ex "info proc mappings" \
  -ex "detach" \
  -ex "quit" \
  -p "$PID" >"$OUT" 2>&1
RC=$?

# Restore ptrace
sudo sh -c "echo $ORIG > /proc/sys/kernel/yama/ptrace_scope"
echo "ptrace_scope restored to $ORIG"

echo "gdb rc=$RC | output: $OUT"
echo "Threads: $(grep -c '^Thread ' "$OUT" 2>/dev/null || echo 0)"
```

## Recipe 4: Repeated Sampling (Statistical Profiling)

Take 20 backtrace snapshots at 0.5s intervals:

```bash
PID=12345
OUT=/tmp/gdb_samples_$PID.txt
> "$OUT"

for i in $(seq 1 20); do
  echo "=== SAMPLE $i at $(date -Is) ===" >> "$OUT"
  timeout 3s gdb --batch \
    -ex "set pagination off" \
    -ex "thread apply all bt 5" \
    -p $PID >> "$OUT" 2>&1
  sleep 0.5
done

echo "Samples saved to $OUT"
echo "Top functions:"
grep -oP '#\d+ .+? in \K\S+' "$OUT" | sort | uniq -c | sort -nr | head -15
```

## Recipe 5: Crash Capture (Run Binary Under GDB)

```bash
BINARY=/path/to/binary
ARGS="--flag1 --flag2"
OUT=/tmp/gdb_crash_$(basename $BINARY)_$(date +%s).txt

timeout 60s gdb --batch \
  -ex "set pagination off" \
  -ex "set print pretty on" \
  -ex "run" \
  -ex "bt full" \
  -ex "thread apply all bt" \
  -ex "info registers" \
  -ex "info sharedlibrary" \
  -ex "quit" \
  --args "$BINARY" $ARGS \
  >"$OUT" 2>&1

echo "Crash capture: $OUT"
grep -E '^(Program|Thread|#0)' "$OUT" | head -20
```

## Recipe 6: Crash with Timeout (For Processes That Hang Instead of Crash)

```bash
BINARY=/path/to/binary
TIMEOUT=30

# GDB with alarm signal for timeout
timeout ${TIMEOUT}s gdb --batch \
  -ex "set pagination off" \
  -ex "run" \
  -ex "bt full" \
  -ex "thread apply all bt" \
  --args "$BINARY" \
  2>&1 | tee /tmp/gdb_timeout_bt.txt

RC=${PIPESTATUS[0]}
if [[ $RC -eq 124 ]]; then
  echo "Process hung (timeout after ${TIMEOUT}s)"
  # Re-attach to capture hang state
  PID=$(pgrep -f "$(basename $BINARY)" | head -1)
  if [[ -n "$PID" ]]; then
    timeout 10s gdb --batch \
      -ex "thread apply all bt" \
      -p $PID 2>&1 | tee -a /tmp/gdb_timeout_bt.txt
    kill $PID
  fi
fi
```

## Recipe 7: Breakpoint + Continue (Trace Specific Function)

```bash
BINARY=/path/to/binary
FUNC=handle_request
MAX_HITS=5

gdb --batch \
  -ex "set pagination off" \
  -ex "set print pretty on" \
  -ex "break $FUNC" \
  -ex "commands 1" \
  -ex "  bt 5" \
  -ex "  info args" \
  -ex "  continue" \
  -ex "end" \
  -ex "run" \
  --args "$BINARY" \
  2>&1 | head -500 | tee /tmp/gdb_trace_${FUNC}.txt
```

## Recipe 8: Core Dump Analysis

```bash
BINARY=/path/to/binary
CORE=/tmp/core.12345.binary

gdb --batch \
  -ex "set pagination off" \
  -ex "set print pretty on" \
  -ex "bt full" \
  -ex "thread apply all bt full" \
  -ex "info registers" \
  -ex "x/20i \$pc" \
  -ex "info locals" \
  -ex "info args" \
  "$BINARY" "$CORE" \
  2>&1 | tee /tmp/gdb_core_analysis.txt
```

## Recipe 9: LD_PRELOAD / Shared Library Debugging

When a segfault happens inside a shared library:

```bash
PID=12345

gdb --batch \
  -ex "set pagination off" \
  -ex "info sharedlibrary" \
  -ex "thread apply all bt full" \
  -p $PID 2>&1 | tee /tmp/gdb_shlib_bt.txt

# Find the crashing shared library
grep -E '\.so' /tmp/gdb_shlib_bt.txt | head -20
```

## Recipe 10: GDB Script File (Complex Debugging)

For complex scenarios, write commands to a file:

```bash
cat > /tmp/gdb_commands.txt << 'EOF'
set pagination off
set confirm off
set print pretty on
set print elements 500
set logging file /tmp/gdb_detailed.log
set logging on

echo \n=== THREAD LIST ===\n
info threads

echo \n=== ALL BACKTRACES ===\n
thread apply all bt full

echo \n=== MEMORY MAP ===\n
info proc mappings

echo \n=== SHARED LIBRARIES ===\n
info sharedlibrary

set logging off
detach
quit
EOF

gdb --batch -x /tmp/gdb_commands.txt -p $PID 2>&1
echo "Detailed log: /tmp/gdb_detailed.log"
```

## Recipe 11: ASAN + GDB Combo (Memory Corruption)

```bash
# Rust: Build with AddressSanitizer
RUSTFLAGS="-Zsanitizer=address" cargo +nightly build \
  --target x86_64-unknown-linux-gnu 2>&1 | tail -5

# Run under GDB — ASAN will abort on error, GDB catches the abort
ASAN_OPTIONS="abort_on_error=1:detect_leaks=0:print_scariness=1" \
gdb --batch \
  -ex "set pagination off" \
  -ex "set print pretty on" \
  -ex "handle SIGABRT stop print" \
  -ex "run" \
  -ex "bt full" \
  -ex "thread apply all bt" \
  -ex "info registers" \
  --args ./target/x86_64-unknown-linux-gnu/debug/binary \
  2>&1 | tee /tmp/asan_gdb.txt

# C/C++:
# gcc -fsanitize=address -g -O1 -fno-omit-frame-pointer source.c -o binary
```

Key ASAN_OPTIONS:
- `abort_on_error=1` — makes ASAN abort instead of exit, so GDB catches it
- `detect_leaks=0` — skip leak detection (slow, usually not what you want in GDB)
- `halt_on_error=1` — stop at first error
- `print_scariness=1` — rate how dangerous the bug is
- `fast_unwind_on_fatal=0` — slow but more accurate stack traces

## Recipe 12: TSAN + GDB (Data Race Detection)

```bash
# Rust
RUSTFLAGS="-Zsanitizer=thread" cargo +nightly build \
  --target x86_64-unknown-linux-gnu 2>&1 | tail -5

TSAN_OPTIONS="abort_on_error=1:second_deadlock_stack=1:history_size=7" \
gdb --batch \
  -ex "set pagination off" \
  -ex "handle SIGABRT stop print" \
  -ex "run" \
  -ex "bt full" \
  -ex "thread apply all bt full" \
  --args ./target/x86_64-unknown-linux-gnu/debug/binary \
  2>&1 | tee /tmp/tsan_gdb.txt

# TSAN output shows TWO stack traces: the conflicting accesses
# GDB backtrace shows the CURRENT state at the race
```

## Recipe 13: Reverse Debugging with rr

```bash
BINARY=/path/to/binary
ARGS="--flag1 --flag2"

# Step 1: Record (run this once)
rr record --chaos $BINARY $ARGS 2>&1 | tee /tmp/rr_record.log
echo "Recording complete. Replay traces in ~/.local/share/rr/"

# Step 2: Replay with crash backtrace
# Note: rr replay spawns GDB internally; pass GDB args after --
rr replay -- \
  -ex "set pagination off" \
  -ex "set print pretty on" \
  -ex "continue" \
  -ex "bt full" \
  -ex "thread apply all bt" \
  -ex "info registers" \
  2>&1 | tee /tmp/rr_crash_bt.txt

# Step 3: Replay with reverse debugging (find corruption source)
# First, get the crash address from Step 2, then:
CRASH_ADDR=0xDEADBEEF  # Replace with actual address
rr replay -- \
  -ex "set pagination off" \
  -ex "continue" \
  -ex "watch *(int*)$CRASH_ADDR" \
  -ex "reverse-continue" \
  -ex "bt full" \
  -ex "info locals" \
  -ex "list" \
  2>&1 | tee /tmp/rr_reverse.txt
```

## Recipe 14: Multi-Snapshot Differential (What Changed Between Snapshots)

Take two snapshots and diff them to see what changed:

```bash
PID=12345
INTERVAL=10  # seconds between snapshots

echo "=== SNAPSHOT 1 ===" > /tmp/snap1.txt
gdb --batch -ex "set pagination off" -ex "thread apply all bt 10" -p $PID >> /tmp/snap1.txt 2>&1

sleep $INTERVAL

echo "=== SNAPSHOT 2 ===" > /tmp/snap2.txt
gdb --batch -ex "set pagination off" -ex "thread apply all bt 10" -p $PID >> /tmp/snap2.txt 2>&1

# Diff: which threads changed state?
echo "=== THREADS THAT CHANGED ==="
diff <(grep -A3 '^Thread ' /tmp/snap1.txt) <(grep -A3 '^Thread ' /tmp/snap2.txt) || true

echo ""
echo "=== THREADS UNCHANGED (likely stuck) ==="
comm -12 <(grep -A3 '^Thread ' /tmp/snap1.txt | sort) <(grep -A3 '^Thread ' /tmp/snap2.txt | sort)
```

## Recipe 15: Python-Scripted Thread Categorization

```bash
cat > /tmp/categorize_threads.py << 'PYEOF'
import gdb
import sys

categories = {
    'epoll_wait': 'IO_WAIT',
    'poll_schedule': 'IO_WAIT',
    'futex_wait': 'MUTEX_WAIT',
    '__lll_lock_wait': 'MUTEX_WAIT',
    'pthread_cond_wait': 'CONDVAR_WAIT',
    'accept4': 'ACCEPTING',
    'recv': 'RECEIVING',
    'send': 'SENDING',
    'nanosleep': 'SLEEPING',
    'clock_nanosleep': 'SLEEPING',
}

results = {'RUNNING': [], 'IO_WAIT': [], 'MUTEX_WAIT': [],
           'CONDVAR_WAIT': [], 'ACCEPTING': [], 'RECEIVING': [],
           'SENDING': [], 'SLEEPING': [], 'UNKNOWN': []}

for thread in gdb.selected_inferior().threads():
    thread.switch()
    frame = gdb.newest_frame()

    # Walk frames to categorize
    cat = 'UNKNOWN'
    depth = 0
    f = frame
    while f and depth < 20:
        name = f.name() or ''
        for pattern, category in categories.items():
            if pattern in name:
                cat = category
                break
        if cat != 'UNKNOWN':
            break
        f = f.older()
        depth += 1

    if cat == 'UNKNOWN' and frame.name():
        cat = 'RUNNING'

    # Get thread name
    try:
        tid = thread.ptid[1]
        with open(f'/proc/{gdb.selected_inferior().pid}/task/{tid}/comm') as cf:
            tname = cf.read().strip()
    except:
        tname = '?'

    top_func = frame.name() or '??'
    results[cat].append(f"  Thread {thread.num} (TID {thread.ptid[1]}, {tname}): {top_func}")

print("\n=== THREAD CATEGORIES ===")
for cat, threads in sorted(results.items()):
    if threads:
        print(f"\n{cat} ({len(threads)} threads):")
        for t in threads:
            print(t)

total = sum(len(v) for v in results.values())
print(f"\nTotal: {total} threads")
print(f"Active: {len(results['RUNNING'])}")
print(f"Waiting: {total - len(results['RUNNING'])}")
PYEOF

gdb --batch \
  -ex "set pagination off" \
  -ex "source /tmp/categorize_threads.py" \
  -p $PID 2>&1 | tee /tmp/thread_categories.txt
```

## Recipe 16: Mutex Deadlock Detector Script

```bash
cat > /tmp/deadlock_detect.py << 'PYEOF'
import gdb
import re

# Build a map of which threads are waiting on which addresses
waiters = {}  # addr -> [thread_nums]
holders = {}  # thread_num -> [held_lock_addrs]

for thread in gdb.selected_inferior().threads():
    thread.switch()
    frame = gdb.newest_frame()

    # Walk frames looking for mutex waits
    f = frame
    depth = 0
    while f and depth < 30:
        name = f.name() or ''

        # Check for futex_wait / lll_lock_wait
        if 'lll_lock_wait' in name or 'futex_wait' in name:
            # Try to get the mutex address from the argument
            try:
                # The mutex address is typically the first argument
                older = f.older()
                if older and 'pthread_mutex_lock' in (older.name() or ''):
                    try:
                        mutex_addr = str(older.read_var('mutex'))
                        waiters.setdefault(mutex_addr, []).append(thread.num)
                    except:
                        pass
            except:
                pass
            break

        f = f.older()
        depth += 1

print("=== DEADLOCK ANALYSIS ===")
print(f"\nThreads waiting on locks: {sum(len(v) for v in waiters.values())}")
for addr, threads in waiters.items():
    print(f"  Lock {addr}: waited on by threads {threads}")

if len(waiters) >= 2:
    print("\nPOTENTIAL DEADLOCK: Multiple locks contested")
    print("Examine 'thread apply all bt full' output to determine")
    print("which thread holds each lock and build the wait-for graph.")
else:
    print("\nNo multi-lock contention detected (may not be a lock deadlock)")
PYEOF

gdb --batch \
  -ex "set pagination off" \
  -ex "source /tmp/deadlock_detect.py" \
  -p $PID 2>&1 | tee /tmp/deadlock_analysis.txt
```

## Recipe 17: Memory Region Inspector

```bash
PID=12345

gdb --batch \
  -ex "set pagination off" \
  -ex "set print pretty on" \
  -ex "info proc mappings" \
  -ex "info sharedlibrary" \
  -ex "print (long)sbrk(0)" \
  -p $PID 2>&1 | tee /tmp/memory_map_$PID.txt

# Analyze the output
echo ""
echo "=== MEMORY SUMMARY ==="
echo "Heap size: $(gawk '/heap/{split($1,a,"-"); printf "%d MB", (strtonum("0x"a[2]) - strtonum("0x"a[1])) / 1048576}' /proc/$PID/maps)"
echo "Stack regions: $(grep -c stack /proc/$PID/maps)"
echo "Shared libs: $(grep -c '\.so' /proc/$PID/maps)"
echo "Anonymous maps: $(grep -c 'anon' /proc/$PID/maps)"
echo "Total VMAs: $(wc -l < /proc/$PID/maps)"
echo "RSS: $(awk '/VmRSS/{print $2, $3}' /proc/$PID/status)"
echo "Peak: $(awk '/VmPeak/{print $2, $3}' /proc/$PID/status)"
```

## Recipe 18: Signal-Aware Crash Catcher

For binaries that handle signals themselves (overriding SIGSEGV handler):

```bash
gdb --batch \
  -ex "set pagination off" \
  -ex "set print pretty on" \
  -ex "handle SIGSEGV stop nopass" \
  -ex "handle SIGBUS stop nopass" \
  -ex "handle SIGABRT stop nopass" \
  -ex "handle SIGFPE stop nopass" \
  -ex "handle SIGILL stop nopass" \
  -ex "run" \
  -ex "echo === SIGNAL RECEIVED ===\n" \
  -ex "print \$_siginfo" \
  -ex "echo === FAULTING ADDRESS ===\n" \
  -ex "print/x \$_siginfo._sifields._sigfault.si_addr" \
  -ex "echo === BACKTRACE ===\n" \
  -ex "bt full" \
  -ex "echo === ALL THREADS ===\n" \
  -ex "thread apply all bt" \
  -ex "echo === REGISTERS ===\n" \
  -ex "info registers" \
  -ex "echo === DISASSEMBLY AT CRASH ===\n" \
  -ex "x/10i \$pc" \
  -ex "echo === MEMORY AROUND FAULT ===\n" \
  -ex "x/16gx \$_siginfo._sifields._sigfault.si_addr" \
  --args /path/to/binary \
  2>&1 | tee /tmp/signal_crash.txt

echo ""
echo "=== CRASH SUMMARY ==="
grep -E 'Signal|Program received|SIGSEGV|SIGABRT|SIGBUS' /tmp/signal_crash.txt | head -5
```

## Recipe 19: Valgrind + GDB Integration

```bash
# Start binary under Valgrind with GDB server
valgrind --vgdb=yes --vgdb-error=0 \
  --tool=memcheck --leak-check=full --track-origins=yes \
  ./binary arg1 arg2 &
VPID=$!
sleep 2

# Connect GDB to Valgrind's gdb server
gdb --batch \
  -ex "target remote | vgdb --pid=$VPID" \
  -ex "continue" \
  -ex "bt full" \
  -ex "monitor leak_check full reachable any" \
  -ex "detach" \
  ./binary 2>&1 | tee /tmp/valgrind_gdb.txt

kill $VPID 2>/dev/null || true
```

## Recipe 20: Automated Regression Bisect (GDB + git bisect)

```bash
# Create the test script
cat > /tmp/bisect_test.sh << 'TESTEOF'
#!/bin/bash
# Build
cargo build --release 2>/dev/null || exit 125  # skip if build fails

# Run under GDB — check for the specific crash
timeout 30s gdb --batch \
  -ex "set pagination off" \
  -ex "run" \
  -ex "bt" \
  --args ./target/release/binary test_input \
  2>&1 > /tmp/bisect_gdb.txt

# Check if the specific bug is present
if grep -q "SIGSEGV\|SIGABRT\|specific_function_name" /tmp/bisect_gdb.txt; then
  exit 1  # bad commit
else
  exit 0  # good commit
fi
TESTEOF
chmod +x /tmp/bisect_test.sh

# Run bisect
git bisect start
git bisect bad HEAD
git bisect good KNOWN_GOOD_COMMIT
git bisect run /tmp/bisect_test.sh
```

---

## Output Parsing Cheatsheet

```bash
FILE=/tmp/gdb_bt.txt

# Count threads
grep -c '^Thread ' "$FILE"

# List thread names and top frame
grep -A1 '^Thread ' "$FILE" | grep -v '^--$'

# Find threads in specific functions
grep -B2 'accept4\|epoll_wait\|futex_wait\|poll\|recv\|send' "$FILE"

# Find threads NOT in expected wait states (potential bugs)
grep -B2 'in ??\|running at' "$FILE"

# Extract unique function names from backtraces
grep -oP 'in \K\S+' "$FILE" | sort -u

# Find the thread with the deepest stack (potential recursion)
awk '/^Thread /{t=$0; d=0} /^#/{d++} d>max{max=d; mt=t}END{print max, mt}' "$FILE"
```

## Advanced Output Parsing

More sophisticated parsing for production diagnostics:

```bash
FILE=/tmp/gdb_bt.txt

# === Thread State Summary ===
echo "Thread State Summary:"
echo "  Unknown/Active: $(grep -c 'syscall\|in ??' "$FILE" 2>/dev/null || echo 0)"
echo "  IO Wait:    $(grep -c 'epoll_wait\|poll_schedule\|pipe_read' "$FILE" 2>/dev/null || echo 0)"
echo "  Lock Wait:  $(grep -c 'lll_lock_wait\|futex_wait\|pthread_mutex' "$FILE" 2>/dev/null || echo 0)"
echo "  Accept:     $(grep -c 'accept4\|accept$' "$FILE" 2>/dev/null || echo 0)"
echo "  Sleep:      $(grep -c 'nanosleep\|clock_nanosleep' "$FILE" 2>/dev/null || echo 0)"

# === Deepest Stack (potential infinite recursion) ===
echo ""
echo "Deepest stack:"
awk '/^Thread /{t=$0; d=0} /^#/{d++} d>max{max=d; mt=t} END{printf "  %d frames in %s\n", max, mt}' "$FILE"

# === Function Frequency (poor man's profiler from single snapshot) ===
echo ""
echo "Most common functions across all threads:"
grep -oP 'in \K\S+' "$FILE" | sort | uniq -c | sort -nr | head -15

# === Unique call paths ===
echo ""
echo "Unique top-3-frame signatures:"
awk '/^Thread /{if(sig)sigs[sig]++; sig=""; n=0} /^#[0-2]/{sig=sig" "$NF; n++} END{if(sig)sigs[sig]++; for(s in sigs)printf "%3d %s\n",sigs[s],s}' "$FILE" | sort -nr | head -10

# === Extract mutex addresses (for deadlock analysis) ===
echo ""
echo "Futex/mutex addresses being waited on:"
grep -oP 'futex\(0x[0-9a-f]+' "$FILE" | sort | uniq -c | sort -nr

# === Thread name → state mapping ===
echo ""
echo "Thread name → state:"
awk '/^Thread .*LWP/{name=$0} /^#0/{printf "  %-50s → %s\n", name, $0}' "$FILE" | head -30
```
