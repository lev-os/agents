# Complementary Tools — strace, perf, /proc, ss

> GDB is rarely used alone. These tools provide the surrounding evidence that makes GDB findings actionable.

---

## Decision Matrix: Which Tool When

| Question | Tool | Why |
|----------|------|-----|
| What syscalls is a thread making? | `strace -p TID` | Real-time syscall trace |
| What function is consuming CPU? | `perf record -p PID` | Statistical sampling |
| Is the process listening/connected? | `ss -ltnp` / `ss -tnp` | Socket state |
| What state are all threads in? | `ps -Lp PID` | Quick overview |
| What's the full call stack? | `gdb --batch -p PID` | Complete backtrace |
| Is data queued in a socket? | `ss -tnp` (check Recv-Q/Send-Q) | Network bottleneck |
| What files does the process have open? | `ls -la /proc/PID/fd` | File descriptor state |
| Is the process consuming memory? | `/proc/PID/status` | Memory stats |
| Why did the process crash? | `gdb binary core` | Core dump analysis |
| Where is time spent (flamegraph)? | `perf record` + `perf script` | CPU profiling |

---

## strace Integration

### Basic Thread-Level Tracing

```bash
# Trace a specific thread's syscalls (non-destructive, 5s window)
timeout 5s strace -tt -T -s 120 -p $TID \
  -e trace=network,poll,epoll_wait,futex 2>&1 | head -200

# Trace ALL threads (creates per-thread output files)
timeout 8s strace -ff -tt -s 128 -p $PID \
  -e trace=network,poll,epoll_wait,futex \
  -o /tmp/strace_out 2>&1

# Read per-thread results
for f in /tmp/strace_out.*; do
  echo "=== $(basename $f) ==="
  head -30 "$f"
  echo
done
```

### strace Filters for Common Scenarios

```bash
# Network debugging (what's happening on sockets)
strace -tt -T -e trace=network -p $PID

# File I/O debugging
strace -tt -T -e trace=file,desc -p $PID

# Futex debugging (locks, condvars, channels)
strace -tt -T -e trace=futex -p $PID

# Per-call timing + summary (slowness diagnosis)
strace -tt -T -C -p $PID
# -C gives both per-call timing AND summary: % time, calls, errors per syscall

# Selective syscall counting (fast)
timeout 10s strace -c -p $PID 2>&1
```

### strace + GDB Workflow

```bash
# Step 1: strace tells you WHAT the thread is doing
timeout 5s strace -tt -T -p $HOT_TID \
  -e trace=network,futex 2>&1 | head -50
# Example output: accept4() returning EAGAIN in tight loop

# Step 2: GDB tells you WHERE in the code this is happening
gdb --batch -ex "thread apply all bt" -p $PID 2>&1 | \
  grep -A20 "Thread.*$HOT_TID"
# Example output: backtrace showing the accept loop code path

# Step 3: Combined picture → diagnosis
# "Thread asupersync-work (TID 3480909) is calling accept4() in a tight
#  loop at listener.rs:142 without polling first → EAGAIN spin loop"
```

### strace Overhead Warning

| Flag | Overhead | Use When |
|------|----------|----------|
| `-c` (summary only) | ~5% | Always safe, production OK |
| `-e trace=network` | ~10-20% | Short bursts (5-10s) |
| `-e trace=all` | ~50-100x | NEVER in production |
| `-f` (follow forks) | +20% per fork | Process spawns children |
| `-ff` (per-thread files) | +20% per thread | Need per-thread separation |

---

## perf Integration

### CPU Profiling

```bash
# Record at 199Hz for 8 seconds (low overhead, high signal)
perf record -F 199 -g -p $PID -- sleep 8

# Quick report
perf report --stdio --no-children --sort comm,dso,symbol | head -200

# Flamegraph (requires flamegraph tools)
perf script | stackcollapse-perf.pl | flamegraph.pl > /tmp/flame.svg
```

### perf + GDB Correlation

```bash
# perf shows WHERE time is spent (statistical, low overhead)
# GDB shows WHY time is spent there (exact state, high overhead)

# Step 1: perf identifies the hot function
perf record -F 199 -g -p $PID -- sleep 5
perf report --stdio | head -50
# Example: 45% in accept_loop::poll_accept

# Step 2: GDB shows the exact state at that function
gdb --batch -ex "thread apply all bt" -p $PID 2>&1 | \
  grep -B5 -A10 'accept_loop\|poll_accept'
```

### perf stat (Quick Overview)

```bash
# System-wide performance counters for a process
perf stat -p $PID -- sleep 5
# Shows: task-clock, context-switches, CPU-migrations, page-faults,
#        cycles, instructions, branches, branch-misses

# Key metrics:
# - instructions/cycle < 0.5 → memory-bound
# - context-switches high → contention
# - page-faults high → memory allocation
```

---

## /proc Filesystem

### Process State

```bash
PID=12345

# Overall status (threads, memory, state, context switches)
cat /proc/$PID/status | grep -E 'State|Threads|VmRSS|VmPeak|voluntary_ctxt_switches|nonvoluntary_ctxt_switches'

# Command line (useful to confirm you have the right process)
tr '\0' ' ' < /proc/$PID/cmdline; echo

# Environment (check for configuration issues)
tr '\0' '\n' < /proc/$PID/environ | grep -E 'PORT|HOST|MODE|LOG|RUST'

# Process executable path (even if binary was replaced)
readlink -f /proc/$PID/exe
# Shows "(deleted)" if binary was updated while process was running
```

### Thread-Level /proc

```bash
# List all threads with names
for tid in $(ls /proc/$PID/task/); do
  printf "TID %6s: %-20s wchan: %-20s stat: %s\n" \
    "$tid" \
    "$(cat /proc/$PID/task/$tid/comm 2>/dev/null)" \
    "$(cat /proc/$PID/task/$tid/wchan 2>/dev/null)" \
    "$(cat /proc/$PID/task/$tid/stat 2>/dev/null | cut -d')' -f2 | awk '{print $1}')"
done

# Per-thread CPU accounting
cat /proc/$PID/task/*/stat | awk -F')' '{split($2,a," "); printf "TID: %s utime: %s stime: %s\n", $1, a[12], a[13]}'
```

### File Descriptors

```bash
# List all open FDs
ls -la /proc/$PID/fd/ 2>/dev/null | head -50

# Socket FDs specifically
ls -la /proc/$PID/fd/ 2>/dev/null | grep socket

# FD count (high count = possible leak)
ls /proc/$PID/fd/ 2>/dev/null | wc -l

# FD limits
cat /proc/$PID/limits | grep 'open files'
```

### Memory Maps

```bash
# Simplified memory map
cat /proc/$PID/maps | head -40

# Memory summary
cat /proc/$PID/smaps_rollup 2>/dev/null || cat /proc/$PID/status | grep Vm
```

---

## ss (Socket Statistics)

### Essential ss Commands

```bash
# Is anything listening on a port?
ss -ltnp "sport = :$PORT"

# All established connections for a port
ss -tnp state established "sport = :$PORT"

# Check for connection backlog (pending accepts)
ss -ltnp "sport = :$PORT"
# Recv-Q = current backlog
# Send-Q = max backlog (listen() argument)
# Recv-Q approaching Send-Q = server can't accept fast enough

# All connections for a PID
ss -tnp | grep "pid=$PID"
```

### Interpreting Recv-Q and Send-Q

**For LISTEN sockets:**
| Recv-Q | Meaning |
|--------|---------|
| 0 | Healthy — no pending connections |
| 1-10 | Normal under load |
| > 50 | Warning — accept() is slow |
| = Send-Q | Critical — backlog full, new connections dropped |

**For ESTABLISHED sockets:**
| Queue | High Value Means |
|-------|-----------------|
| Recv-Q > 0 (server) | Server not reading data — thread stuck elsewhere |
| Send-Q > 0 (server) | Client slow or network congested |
| Recv-Q > 0 (client) | Client not reading responses |

### ss + GDB Correlation

```bash
# Step 1: Find stuck connections
ss -tnp state established "sport = :$PORT" | awk '$2 > 0 {print}'
# Recv-Q=325 means 325 bytes sitting unread

# Step 2: Which thread should be reading?
gdb --batch -ex "thread apply all bt" -p $PID 2>&1 | \
  grep -B3 -A5 'recv\|read\|epoll'

# Step 3: Is the reader thread stuck on something else?
# If the reader shows up in a mutex wait or futex, THAT's your bug
```

---

## Combined Diagnosis Workflow (The Full Sequence)

For a process that "seems stuck" or "isn't responding":

```bash
PID=12345
PORT=8765
OUT_DIR=/tmp/debug_${PID}_$(date +%s)
mkdir -p "$OUT_DIR"

echo "=== Step 1: Process state ===" | tee "$OUT_DIR/00_summary.txt"
ps -p $PID -o pid,ppid,etime,pcpu,pmem,stat,comm,args | tee -a "$OUT_DIR/00_summary.txt"

echo "=== Step 2: Thread state ===" | tee -a "$OUT_DIR/00_summary.txt"
ps -Lp $PID -o pid,tid,psr,pcpu,stat,wchan:32,comm --sort=-pcpu | tee "$OUT_DIR/01_threads.txt"

echo "=== Step 3: Socket state ===" | tee -a "$OUT_DIR/00_summary.txt"
ss -ltnp "sport = :$PORT" | tee "$OUT_DIR/02_listen.txt"
ss -tnp state established "sport = :$PORT" | tee "$OUT_DIR/03_established.txt"

echo "=== Step 4: Endpoint probe ===" | tee -a "$OUT_DIR/00_summary.txt"
curl -sS -i --max-time 5 "http://127.0.0.1:$PORT/" \
  -w '\ncode=%{http_code} ttfb=%{time_starttransfer}s total=%{time_total}s\n' \
  2>&1 | tee "$OUT_DIR/04_probe.txt"

echo "=== Step 5: ptrace + GDB ===" | tee -a "$OUT_DIR/00_summary.txt"
sudo sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'
timeout 30s gdb --batch \
  -ex "set pagination off" \
  -ex "thread apply all bt full" \
  -p $PID 2>&1 | tee "$OUT_DIR/05_gdb_bt.txt"

echo "=== Step 6: Hot thread strace ===" | tee -a "$OUT_DIR/00_summary.txt"
HOT_TID=$(ps -Lp $PID -o tid,pcpu --sort=-pcpu --no-headers | head -1 | awk '{print $1}')
timeout 5s strace -tt -T -s 120 -p $HOT_TID \
  -e trace=network,poll,epoll_wait,futex 2>&1 | tee "$OUT_DIR/06_strace_hot.txt"

echo "=== Step 7: /proc info ===" | tee -a "$OUT_DIR/00_summary.txt"
cat /proc/$PID/status | tee "$OUT_DIR/07_proc_status.txt"
ls -la /proc/$PID/fd/ 2>/dev/null | tee "$OUT_DIR/08_fd_list.txt"

echo ""
echo "Debug artifacts saved to: $OUT_DIR/"
echo "Thread count: $(grep -c '^Thread ' "$OUT_DIR/05_gdb_bt.txt" 2>/dev/null || echo ?)"
echo "Hot thread TID: $HOT_TID"
echo "Hot thread top syscall: $(head -5 "$OUT_DIR/06_strace_hot.txt" | tail -1)"
```

---

## rr (Record and Replay Debugger)

The most powerful debugging tool for non-deterministic bugs. Records full program execution and replays it deterministically.

### Installation
```bash
# Ubuntu/Debian
sudo apt-get install -y rr
# Or latest from source
git clone https://github.com/rr-debugger/rr && cd rr
mkdir build && cd build && cmake .. && make -j$(nproc) && sudo make install
```

### Requirements and Limitations
- Needs hardware perf counters: check by running `rr record` (it will error if unsupported)
- Doesn't work in most VMs (nested virtualization needed) or Docker without `--privileged`
- Performance overhead: 1.5-5x recording, near-native replay
- x86/x86_64 only (ARM support experimental)
- Single-machine: can't record distributed systems

### Basic Workflow
```bash
# Record (captures everything: syscalls, signals, scheduling decisions)
rr record ./binary arg1 arg2
# or with chaos mode to vary scheduling (expose race conditions)
rr record --chaos ./binary

# Replay (deterministic — same thread interleaving every time)
rr replay
# In the replay GDB session, all normal GDB commands work PLUS:
# reverse-continue, reverse-step, reverse-next, reverse-finish
```

### Batch Mode for Agents
```bash
# Record
rr record ./binary 2>&1 | tee /tmp/rr_record.log
RC=${PIPESTATUS[0]}

# Replay with automated backtrace capture
rr replay -- \
  -ex "set pagination off" \
  -ex "bt full" \
  -ex "thread apply all bt" \
  2>&1 | tee /tmp/rr_replay.log

# Replay with reverse debugging to find corruption source
rr replay -- \
  -ex "set pagination off" \
  -ex "break *crash_address" \
  -ex "continue" \
  -ex "watch *(int*)corrupted_address" \
  -ex "reverse-continue" \
  -ex "bt full" \
  2>&1 | tee /tmp/rr_reverse.log
```

### The "Reverse Watchpoint" Technique (rr's Killer Feature)
```
Problem: Memory at 0xABCD is corrupted when you read it at line 200.
         Who wrote the bad value?

1. rr replay → crash happens at the corrupted read
2. watch *(int*)0xABCD → set watchpoint
3. reverse-continue → rr runs BACKWARD to the last write to 0xABCD
4. bt → shows the exact code that wrote the corruption
5. info locals → shows the bogus value being written
```
This is impossible with any other tool. GDB forward-only watchpoints only catch the corruption IF you set them before it happens. rr lets you start from the crash and work backwards.

### When to Use rr vs GDB
| Scenario | Tool | Why |
|----------|------|-----|
| Crash that reproduces reliably | GDB | Simpler, less overhead |
| Race condition / intermittent | rr | Deterministic replay catches it |
| Data corruption (who wrote?) | rr | Reverse watchpoints |
| Production process (can't restart) | GDB attach | rr requires starting under rr |
| Need to vary scheduling | rr --chaos | Exposes hidden races |

---

## bpftrace (eBPF-Based Dynamic Tracing)

Low-overhead production tracing. Unlike GDB/strace, bpftrace doesn't stop the process.

### Installation
```bash
sudo apt-get install -y bpftrace
# Verify
bpftrace --version
```

### Key Difference from GDB
GDB stops the process to inspect it. bpftrace instruments it WITHOUT stopping — perfect for production or timing-sensitive bugs.

### Essential One-Liners
```bash
# Trace a specific function's calls (userspace)
sudo bpftrace -e 'uprobe:/path/to/binary:function_name { printf("called from tid=%d\n", tid); }'

# Count syscalls by thread
sudo bpftrace -p $PID -e "tracepoint:raw_syscalls:sys_enter { @[tid, comm] = count(); }"

# Trace futex calls (lock debugging without stopping)
sudo bpftrace -p $PID -e "tracepoint:syscalls:sys_enter_futex { @[tid, args->uaddr, args->op & 0xf] = count(); }"

# Histogram of syscall latency
sudo bpftrace -p $PID -e "tracepoint:raw_syscalls:sys_enter { @start[tid] = nsecs; } tracepoint:raw_syscalls:sys_exit /@start[tid]/ { @latency = hist(nsecs - @start[tid]); delete(@start[tid]); }"

# Trace socket accept with timing
sudo bpftrace -e 'kprobe:inet_csk_accept { @start[tid] = nsecs; } kretprobe:inet_csk_accept /@start[tid]/ { printf("accept took %d us\n", (nsecs - @start[tid]) / 1000); delete(@start[tid]); }'

# Find which threads are context-switching most (contention)
sudo bpftrace -p $PID -e "tracepoint:sched:sched_switch { @[args->prev_comm, args->prev_pid] = count(); }"
```

### bpftrace + GDB Workflow
```bash
# Step 1: bpftrace identifies the pattern (no process stopping)
timeout 5s sudo bpftrace -p $PID -e "uprobe:/proc/$PID/exe:accept_loop { @calls = count(); }"
# "accept_loop called 50000 times in 5 seconds → tight loop"

# Step 2: GDB captures the exact state
gdb --batch -ex "thread apply all bt" -p $PID
# Shows the call stack at the accept loop

# Step 3: Combined diagnosis without any production impact from Step 1
```

### bpftrace Overhead
| Trace Type | Overhead | Production Safe? |
|-----------|----------|-----------------|
| Tracepoint (kernel) | ~100ns/event | Yes |
| Kprobe (kernel function) | ~200ns/event | Yes, with care |
| Uprobe (user function) | ~1μs/event | Yes, low-frequency functions |
| USDT (pre-defined probes) | ~100ns/event | Yes |

---

## ltrace (Library Call Tracing)

Traces calls to shared library functions. Sits between strace (syscalls only) and GDB (full debugging).

```bash
# Trace specific library calls
ltrace -e malloc+free+realloc -p $PID 2>&1 | head -100

# Trace with call timing
ltrace -tt -T -e 'pthread_mutex_lock+pthread_mutex_unlock' -p $PID 2>&1 | head -100

# Count library calls (like strace -c)
ltrace -c -p $PID -e '*' 2>&1

# Trace specific library
ltrace -l /usr/lib/x86_64-linux-gnu/libssl.so -p $PID
```

### When ltrace Fills the Gap
| Need | strace | ltrace | GDB |
|------|--------|--------|-----|
| Syscall tracing | ✓ | ✗ | ✓ (slow) |
| Library function calls | ✗ | ✓ | ✓ (breakpoints) |
| Malloc/free tracking | ✗ | ✓ | ✓ (slow) |
| No process stop | ✗ | ✗ | ✗ |
| Lock call timing | ✗ | ✓ | ✓ (slow) |

---

## SystemTap

Kernel and userspace probing with a scripting language. More powerful than bpftrace for complex analysis but requires kernel headers and build step.

```bash
# Install
sudo apt-get install -y systemtap systemtap-runtime

# Trace accept() calls with backtraces
sudo stap -e 'probe syscall.accept4 { if (pid() == target()) printf("%s[%d] accept4\n", execname(), tid()) }' -x $PID

# Thread state monitoring
sudo stap -e 'probe scheduler.cpu_on { if (task_pid(task_current()) == target()) printf("TID %d scheduled on CPU %d\n", tid(), cpu()) }' -x $PID
```

---

## addr2line & objdump (Offline Symbol Resolution)

When you have addresses from GDB but no symbols loaded:

```bash
# addr2line: address → source location
addr2line -e /path/to/binary -fip 0x55df60a7307b
# Output: function_name at source.rs:42 (discriminator 3)

# Batch: resolve multiple addresses
echo -e "0xADDR1\n0xADDR2\n0xADDR3" | addr2line -e binary -fip

# objdump: full disassembly for offline analysis
objdump -d -M intel /path/to/binary > /tmp/disasm.txt
grep -A20 'function_name' /tmp/disasm.txt

# objdump with source interleaving (if debug info available)
objdump -d -S -M intel /path/to/binary > /tmp/disasm_with_source.txt

# nm: list symbols
nm -C /path/to/binary | grep -i 'accept\|poll\|http'
# -C demangles C++/Rust symbols

# readelf: ELF structure examination
readelf -sW /path/to/binary | grep -i FUNC | sort -k2
# Shows function addresses for manual correlation with GDB output

# Rust demangling
echo '_ZN4core3fmt5write17h...' | rustfilt
# or for batch:
cat /tmp/gdb_bt.txt | rustfilt
```

---

## Extended /proc Filesystem Reference

Beyond the basics, `/proc` offers deep process introspection:

```bash
PID=12345

# === Memory Details ===
# Detailed memory map with sizes
cat /proc/$PID/smaps | grep -E '^[0-9a-f]|Rss:|Pss:|Shared|Private|Referenced'

# Memory summary (single line per category)
cat /proc/$PID/smaps_rollup

# OOM score (higher = more likely to be killed)
cat /proc/$PID/oom_score
cat /proc/$PID/oom_score_adj

# === CPU & Scheduling ===
# CPU affinity mask
taskset -p $PID
# Per-thread
for tid in $(ls /proc/$PID/task/); do
  printf "TID %s: %s\n" "$tid" "$(taskset -p $tid 2>/dev/null | awk '{print $NF}')"
done

# Scheduling policy
chrt -p $PID

# NUMA memory placement
numastat -p $PID 2>/dev/null

# === Namespaces ===
ls -la /proc/$PID/ns/
# Shows namespace IDs — compare between processes to check if they share namespaces

# NSpid: PID in each PID namespace (host, container, nested)
grep NSpid /proc/$PID/status

# === Security ===
# Capabilities
cat /proc/$PID/status | grep -i cap
# Decode: capsh --decode=00000000a80425fb

# Seccomp status
grep Seccomp /proc/$PID/status
# 0 = disabled, 1 = strict, 2 = filter

# === I/O ===
# Per-process I/O stats
cat /proc/$PID/io
# read_bytes, write_bytes, cancelled_write_bytes

# === Cgroup ===
cat /proc/$PID/cgroup
# Shows cgroup membership (memory limits, CPU quotas)
```

---

## Tool Availability Quick Check

Before starting a debugging session, verify what's available:

```bash
echo "=== Tool Availability ==="
for tool in gdb strace perf ltrace rr bpftrace addr2line objdump nm readelf stap; do
  printf "%-15s: %s\n" "$tool" "$(which $tool 2>/dev/null || echo 'NOT FOUND')"
done

echo ""
echo "=== Kernel Features ==="
printf "ptrace_scope:  %s\n" "$(cat /proc/sys/kernel/yama/ptrace_scope)"
printf "perf_events:   %s\n" "$(cat /proc/sys/kernel/perf_event_paranoid)"
printf "kprobes:       %s\n" "$(cat /proc/sys/debug/kprobes-optimization 2>/dev/null || echo 'N/A')"
printf "core_pattern:  %s\n" "$(cat /proc/sys/kernel/core_pattern)"
echo ""
echo "=== Hardware ==="
printf "perf counters: %s\n" "$(rr record --print-capabilities 2>/dev/null || echo 'rr not installed')"
printf "CPU model:     %s\n" "$(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2)"
```

---

## Installation — Complete Toolkit

```bash
# Ubuntu/Debian — full debugging toolkit
sudo apt-get update
sudo apt-get install -y \
  gdb \
  strace \
  ltrace \
  linux-tools-$(uname -r) linux-tools-generic \
  binutils \
  elfutils \
  valgrind \
  rr

# Optional but powerful
sudo apt-get install -y \
  bpftrace \
  systemtap \
  systemtap-runtime \
  perf-tools-unstable

# If linux-tools fails (non-stock kernels)
sudo apt-get install -y gdb strace ltrace binutils
perf stat ls 2>/dev/null && echo "perf works" || echo "perf needs kernel headers"

# Rust-specific debugging tools
cargo install cargo-flamegraph
# For demangling
cargo install rustfilt

# Verify everything
for tool in gdb strace ltrace perf rr bpftrace addr2line objdump nm; do
  printf "%-12s %s\n" "$tool:" "$($tool --version 2>&1 | head -1 || echo 'not available')"
done
```
