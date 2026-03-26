# GDB Debugging Techniques — Complete Catalog

## Table of Contents

1. [Attach Patterns](#attach-patterns)
2. [ptrace Policy Management](#ptrace-policy-management)
3. [Thread Investigation](#thread-investigation)
4. [Network Service Debugging](#network-service-debugging)
5. [Deadlock Detection](#deadlock-detection)
6. [Memory Corruption](#memory-corruption)
7. [Stripped Binary Handling](#stripped-binary-handling)
8. [Async Runtime Debugging](#async-runtime-debugging)
9. [Signal Handling](#signal-handling)
10. [Watchpoints](#watchpoints)
11. [Conditional Breakpoints](#conditional-breakpoints)
12. [Python GDB Extensions](#python-gdb-extensions)
13. [Disassembly Reading & Register Analysis](#disassembly-reading--register-analysis)
14. [Lock Contention Analysis](#lock-contention-analysis)
15. [Stripped Binary Forensics](#stripped-binary-forensics)
16. [Async Runtime Internals (Tokio/async-std)](#async-runtime-internals-tokioasync-std)
17. [Core Dump Forensics](#core-dump-forensics)

---

## Attach Patterns

### Safe Batch Attach (Agent Default)

The safest pattern: attach, capture, detach, all non-interactively with timeout protection:

```bash
ORIG=$(cat /proc/sys/kernel/yama/ptrace_scope)
sudo sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'
timeout 30s gdb --batch \
  -ex "set confirm off" \
  -ex "set pagination off" \
  -ex "set print thread-events off" \
  -ex "set print pretty on" \
  -ex "thread apply all bt full" \
  -ex "detach" \
  -ex "quit" \
  -p $PID 2>&1 | tee /tmp/gdb_bt_$(date +%s).txt
RC=$?
sudo sh -c "echo $ORIG > /proc/sys/kernel/yama/ptrace_scope"
echo "gdb exited with rc=$RC"
```

### Repeated Sampling (Poor Man's Profiler)

Take multiple snapshots to build a statistical picture:

```bash
for i in $(seq 1 10); do
  echo "=== Sample $i at $(date -Is) ==="
  timeout 5s gdb --batch -ex "thread apply all bt 5" -p $PID 2>&1
  sleep 1
done | tee /tmp/gdb_samples.txt

# Aggregate: which functions appear most?
grep -oP '#\d+ .+? in \K\S+' /tmp/gdb_samples.txt | sort | uniq -c | sort -nr | head -20
```

### Attach to Specific Thread

When you know which thread is problematic:

```bash
# TID from: ps -Lp $PID -o tid,pcpu --sort=-pcpu
gdb --batch \
  -ex "set pagination off" \
  -ex "thread apply all bt" \
  -p $TID 2>&1
```

Note: Attaching to a TID still stops the whole process briefly. GDB shows all threads but you can focus on the one you attached to.

---

## ptrace Policy Management

### Understanding ptrace_scope Values

| Value | Name | Who Can Attach | Default On |
|-------|------|---------------|------------|
| 0 | classic | Any process with same UID | — |
| 1 | restricted | Only direct parent | Ubuntu, most distros |
| 2 | admin-only | Processes with CAP_SYS_PTRACE | Hardened servers |
| 3 | none | Nobody (not even root) | Extreme lockdown |

### Relaxation Patterns

```bash
# Pattern 1: Relax permanently (development machines)
sudo sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'
# Persist across reboot:
echo 'kernel.yama.ptrace_scope = 0' | sudo tee /etc/sysctl.d/99-ptrace.conf
sudo sysctl -p /etc/sysctl.d/99-ptrace.conf

# Pattern 2: Relax temporarily (save and restore)
ORIG=$(cat /proc/sys/kernel/yama/ptrace_scope)
sudo sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'
# ... do debugging ...
sudo sh -c "echo $ORIG > /proc/sys/kernel/yama/ptrace_scope"
printf 'ptrace_scope restored to %s\n' "$(cat /proc/sys/kernel/yama/ptrace_scope)"

# Pattern 3: Per-process capability (no global change)
# Run gdb with CAP_SYS_PTRACE
sudo setcap cap_sys_ptrace+ep $(which gdb)
# WARNING: This allows ANY user running gdb to attach to ANY process
```

### Containers and Namespaces

```bash
# Docker: add --cap-add=SYS_PTRACE to docker run
docker run --cap-add=SYS_PTRACE ...

# Kubernetes: add to securityContext
# securityContext:
#   capabilities:
#     add: ["SYS_PTRACE"]

# Podman: --cap-add=SYS_PTRACE
podman run --cap-add=SYS_PTRACE ...
```

---

## Thread Investigation

### Thread State Mapping

```bash
# GDB thread info shows thread IDs and current frame
gdb --batch -ex "info threads" -p $PID 2>&1

# Map GDB thread numbers to kernel TIDs
gdb --batch -ex "info threads" -p $PID 2>&1 | \
  awk '/Thread/{print $1, $2, $NF}'

# Cross-reference with /proc thread names
for tid in $(ls /proc/$PID/task/); do
  printf "TID %6s: %-20s wchan: %s\n" \
    "$tid" \
    "$(cat /proc/$PID/task/$tid/comm 2>/dev/null)" \
    "$(cat /proc/$PID/task/$tid/wchan 2>/dev/null)"
done
```

### Finding the Problem Thread

```bash
# Step 1: Which threads are consuming CPU?
ps -Lp $PID -o tid,pcpu,stat,wchan:32,comm --sort=-pcpu --no-headers | head -10

# Step 2: For each hot thread, what syscall is it making?
for tid in $(ps -Lp $PID -o tid,pcpu --sort=-pcpu --no-headers | head -3 | awk '{print $1}'); do
  echo "=== TID $tid ==="
  timeout 3s strace -tt -T -p $tid -e trace=network,futex,poll 2>&1 | head -30
  echo
done

# Step 3: Full backtrace of the hot thread
HOT_TID=$(ps -Lp $PID -o tid,pcpu --sort=-pcpu --no-headers | head -1 | awk '{print $1}')
gdb --batch -ex "thread apply all bt" -p $HOT_TID 2>&1
```

### Tokio/async-std Runtime Threads

Async Rust runtimes create worker threads that all look similar. To distinguish:

```bash
# Thread names in Tokio follow patterns:
# tokio-runtime-worker  — executor threads
# blocking-*            — blocking task pool
# Your custom names     — tokio::task::Builder::new().name("my-task")

# Get all thread names
ls /proc/$PID/task/ | while read tid; do
  printf "%s\t%s\t%s%%\n" "$tid" \
    "$(cat /proc/$PID/task/$tid/comm 2>/dev/null)" \
    "$(ps -o pcpu= -p $tid 2>/dev/null | tr -d ' ')"
done | sort -t$'\t' -k3 -nr | head -20
```

### CPU Affinity Analysis

CPU affinity determines which cores a thread is allowed to run on. Pinning threads to specific cores is common in high-performance systems, and misconfigurations can cause severe performance problems (e.g., all worker threads pinned to a single core).

```bash
# Process-level affinity (inherited by new threads unless overridden)
taskset -p $PID
# Output: pid 12345's current affinity mask: ff
# ff = 0b11111111 = cores 0-7 allowed

# Per-thread affinity — essential when threads are pinned to different cores
for tid in $(ls /proc/$PID/task/); do
  allowed=$(grep 'Cpus_allowed:' /proc/$PID/task/$tid/status | awk '{print $2}')
  allowed_list=$(grep 'Cpus_allowed_list:' /proc/$PID/task/$tid/status | awk '{print $2}')
  comm=$(cat /proc/$PID/task/$tid/comm 2>/dev/null)
  printf "TID %-8s %-25s mask=%-8s cores=%s\n" "$tid" "$comm" "$allowed" "$allowed_list"
done

# Danger sign: multiple compute-heavy threads all pinned to the same core
# This creates contention where threads constantly preempt each other,
# getting high involuntary context switches but poor throughput.
```

### NUMA Analysis

Non-Uniform Memory Access architectures have multiple memory nodes. Cross-node memory access incurs a significant latency penalty (typically 1.5-2x local access time). For latency-sensitive services, NUMA misplacement can dominate performance.

```bash
# Which NUMA nodes exist and what CPUs belong to each?
lscpu | grep -i numa
# NUMA node0 CPU(s): 0-15
# NUMA node1 CPU(s): 16-31

# Where is this process's memory allocated?
numastat -p $PID
# Shows per-node memory allocation: local_node, other_node, numa_hit, numa_miss

# Per-thread NUMA binding
for tid in $(ls /proc/$PID/task/); do
  node=$(grep 'Mems_allowed_list:' /proc/$PID/task/$tid/status | awk '{print $2}')
  printf "TID %-8s allowed_nodes=%s\n" "$tid" "$node"
done

# Key diagnostic: if a thread runs on node 0's CPUs but its memory is on node 1,
# every memory access crosses the interconnect. This shows as:
# - numa_miss count increasing in `numastat -p $PID`
# - Higher than expected latency despite low CPU usage
# - `perf stat -e node-loads,node-load-misses -p $PID` shows remote access ratio
```

### Scheduling Policy and Context Switches

Scheduling policy reveals whether threads use real-time priorities (which can starve other threads or the entire system) and context switch counters reveal contention patterns.

```bash
# Scheduling policy per thread
for tid in $(ls /proc/$PID/task/); do
  policy=$(chrt -p $tid 2>/dev/null | head -1)
  printf "TID %-8s %s\n" "$tid" "$policy"
done
# SCHED_OTHER = normal time-sharing (default, uses nice values)
# SCHED_FIFO  = real-time, runs until it yields or is preempted by higher priority FIFO
# SCHED_RR    = real-time, like FIFO but with time quantum rotation among same-priority
# SCHED_BATCH = optimized for throughput, longer time slices
# SCHED_IDLE  = only runs when nothing else wants the CPU

# Context switch analysis — the single most revealing metric for contention
for tid in $(ls /proc/$PID/task/); do
  vol=$(grep 'voluntary_ctxt_switches' /proc/$PID/task/$tid/status | awk '{print $2}')
  invol=$(grep 'nonvoluntary_ctxt_switches' /proc/$PID/task/$tid/status | awk '{print $2}')
  comm=$(cat /proc/$PID/task/$tid/comm 2>/dev/null)
  printf "TID %-8s %-25s voluntary=%-10s involuntary=%s\n" "$tid" "$comm" "$vol" "$invol"
done | sort -t= -k3 -nr

# Interpretation:
# High voluntary, low involuntary = thread frequently waits (I/O, locks, sleep)
#   → Normal for I/O-bound threads. Concerning only if you expect CPU-bound work.
# Low voluntary, high involuntary = thread wants CPU but keeps getting preempted
#   → CPU contention. Too many threads competing for too few cores.
#   → Check: are more threads active than available cores? Is affinity too restrictive?
# High both = thread alternates between I/O waits and CPU bursts, and is contended
# Low both = thread is mostly idle or blocked long-term (e.g., accept() waiting)

# Snapshot the counters, wait, then snapshot again to get rates:
declare -A INVOL_BEFORE
for tid in $(ls /proc/$PID/task/); do
  INVOL_BEFORE[$tid]=$(grep 'nonvoluntary_ctxt_switches' /proc/$PID/task/$tid/status 2>/dev/null | awk '{print $2}')
done
sleep 5
for tid in $(ls /proc/$PID/task/); do
  before=${INVOL_BEFORE[$tid]:-0}
  after=$(grep 'nonvoluntary_ctxt_switches' /proc/$PID/task/$tid/status 2>/dev/null | awk '{print $2}')
  delta=$((after - before))
  if [ "$delta" -gt 0 ]; then
    comm=$(cat /proc/$PID/task/$tid/comm 2>/dev/null)
    printf "TID %-8s %-25s involuntary_switches_in_5s=%s\n" "$tid" "$comm" "$delta"
  fi
done | sort -t= -k2 -nr
```

---

## Network Service Debugging

### Complete Network Diagnosis

```bash
PORT=8765
PID=$(ss -ltnp "sport = :$PORT" | awk 'NR>1{match($NF,/pid=([0-9]+)/,a); print a[1]}')

# 1. Is it listening?
ss -ltnp "sport = :$PORT"
# Recv-Q = pending connections in accept queue. High value = accept() too slow

# 2. Established connections — check Recv-Q and Send-Q
ss -tnp state established "sport = :$PORT"
# Recv-Q > 0 on server side = data waiting to be read = server stuck
# Send-Q > 0 on server side = data waiting to be sent = client slow or network issue

# 3. Probe endpoint
curl -sS -i --max-time 5 -X POST "http://127.0.0.1:$PORT/endpoint" \
  -H 'content-type: application/json' \
  --data '{"test": true}' \
  -w '\ncode=%{http_code} connect=%{time_connect}s ttfb=%{time_starttransfer}s total=%{time_total}s\n'

# 4. GDB backtrace to see what threads are doing
gdb --batch -ex "thread apply all bt" -p $PID 2>&1 | tee /tmp/net_bt.txt

# 5. Find threads handling network I/O
grep -B5 'accept\|recv\|send\|epoll\|poll\|read\|write' /tmp/net_bt.txt
```

### Socket FD Investigation

```bash
# List all sockets owned by process
ls -la /proc/$PID/fd/ | grep socket
sudo lsof -Pan -p $PID -iTCP

# Find which FD is the listener
sudo lsof -Pan -p $PID -iTCP -sTCP:LISTEN

# Check FD info
for fd in $(ls /proc/$PID/fd/ 2>/dev/null); do
  link=$(readlink /proc/$PID/fd/$fd 2>/dev/null)
  if [[ "$link" == *socket* ]]; then
    echo "FD $fd: $link"
    cat /proc/$PID/fdinfo/$fd 2>/dev/null | head -5
  fi
done
```

### TIME_WAIT Socket Accumulation

TIME_WAIT is a normal TCP state after active close, but excessive accumulation indicates a connection churn problem — the service is creating and destroying connections too rapidly, exhausting ephemeral ports.

```bash
# Count TIME_WAIT sockets (system-wide)
ss -tn state time-wait | wc -l

# TIME_WAIT sockets specific to your service's port
ss -tn state time-wait "sport = :$PORT or dport = :$PORT" | wc -l

# Are we running out of ephemeral ports?
cat /proc/sys/net/ipv4/ip_local_port_range
# Default: 32768 60999 = 28231 ports
# If TIME_WAIT count approaches this number, new connections will fail with EADDRNOTAVAIL

# Mitigation check — is tcp_tw_reuse enabled?
cat /proc/sys/net/ipv4/tcp_tw_reuse
# 0 = disabled (default), 1 = enabled (allows reuse of TIME_WAIT sockets for new outgoing connections)
# 2 = enabled for loopback only (safer)

# TIME_WAIT duration (not directly tunable on Linux, always 2*MSL = 60s)
# But you can reduce it effectively with tcp_tw_reuse or SO_LINGER(0) on close

# Connection creation rate — if this is high and connections are short-lived, TIME_WAIT will accumulate
ss -s
# Look at: TCP: X (estab Y, closed Z, orphaned W, timewait T)
```

### TCP Window and Congestion Analysis

When connections exist but throughput is poor, TCP internals reveal the bottleneck. The `ss -ti` command exposes the kernel's TCP state machine for each connection.

```bash
# Detailed TCP info for connections to your service
ss -ti state established "sport = :$PORT"

# Key fields in ss -ti output:
# cwnd:N        — congestion window (in segments). How many segments can be in-flight.
#                  Small cwnd = congestion or slow start. Healthy long-lived connection: cwnd >> 10
# ssthresh:N    — slow start threshold. cwnd grows exponentially until ssthresh, then linearly.
#                  If ssthresh is very low, a congestion event recently occurred.
# rtt:X/Y       — smoothed RTT / RTT variance (in ms). High variance = unstable path.
# retrans:X/Y   — retransmit counter / total retransmits. Non-zero = packet loss.
# bytes_sent:N  — total bytes sent on this connection
# bytes_acked:N — total bytes acknowledged
# send Xbps     — current send rate
# rcv_space:N   — receive window advertised by peer

# Example interpretation:
# cwnd:3 ssthresh:2 retrans:0/5 rtt:150/75
# → cwnd=3 is tiny, ssthresh=2 means congestion events occurred (5 retransmits),
#   RTT 150ms with high variance (75ms). This connection is severely congestion-limited.

# Find connections with high retransmit counts (indicates packet loss)
ss -ti state established "sport = :$PORT" | grep -E 'retrans:[1-9]'

# System-wide TCP statistics for aggregate view
cat /proc/net/snmp | grep Tcp
# TCPRetransSegs = total retransmissions (compare over time for rate)
```

### Connection Reset and Error Analysis

```bash
# Summary statistics including resets, errors, overflows
ss -s
# Key lines:
# TCP: X (estab Y, closed Z, orphaned W, timewait T)
#   InSegs OutSegs RetransSegs InErrs OutRsts
# High OutRsts = your service is actively rejecting connections (RST sent)
# High InErrs = malformed packets arriving

# Detailed protocol stats
cat /proc/net/netstat | grep -E 'TCPAbortOn|ListenOverflows|ListenDrops'
# TCPAbortOnTimeout — connections abandoned after retransmit timeout
# TCPAbortOnData    — RST sent while data in receive queue (application not reading)
# TCPAbortOnClose   — RST sent on close with unread data (common: client sends, server closes)
# TCPAbortOnMemory  — connection aborted due to memory pressure
# ListenOverflows   — SYN received but accept queue full (application not calling accept() fast enough)
# ListenDrops       — total drops from listen queue (includes overflows)

# Watch these counters change over time
watch -n 1 'grep -E "ListenOverflows|ListenDrops" /proc/net/netstat'
```

### Half-Open Connection Detection

Half-open connections indicate network path problems, firewall interference, or remote host issues.

```bash
# SYN_SENT: our side sent SYN, waiting for SYN-ACK
# → Remote host is not responding (down, firewalled, or slow)
ss -tn state syn-sent "dport = :$PORT or sport = :$PORT"

# SYN_RECV: we received SYN, sent SYN-ACK, waiting for ACK
# → Client sent SYN but never completed handshake (SYN flood attack or network issue)
ss -tn state syn-recv "sport = :$PORT"

# High SYN_RECV count on a server = possible SYN flood
# Check SYN cookies status:
cat /proc/sys/net/ipv4/tcp_syncookies
# 1 = enabled (mitigates SYN floods by not allocating state until handshake completes)

# CLOSE_WAIT: remote side closed, we haven't closed yet
# → Application bug: we received FIN but never called close() on the socket
# This is almost always a bug in the application (leaked socket/connection)
ss -tn state close-wait "sport = :$PORT"
# If this count grows over time, you have a connection leak
```

### Unix Domain Socket Debugging

Unix domain sockets are used for local IPC and are invisible to TCP tools. They're common in database connections, container runtimes, and systemd services.

```bash
# List all listening Unix sockets with owning process
ss -xlp
# x = Unix sockets, l = listening, p = show process

# List connected (established) Unix sockets
ss -xp state established

# Find Unix sockets owned by your process
ss -xp | grep "pid=$PID"
# Or:
sudo lsof -U -p $PID

# Examine Unix socket queue depths
ss -xl | grep my_socket_name
# Recv-Q on a listening Unix socket = pending connections waiting for accept()
# If this is consistently > 0, the server is falling behind

# Abstract namespace sockets (start with @) vs filesystem sockets
ss -xlp | grep '@'   # Abstract — no filesystem entry, removed when process exits
ss -xlp | grep '/'   # Filesystem — /var/run/docker.sock, /tmp/mysql.sock, etc.

# Check socket file permissions (filesystem sockets only)
ls -la /var/run/docker.sock
# srw-rw---- 1 root docker 0 ... /var/run/docker.sock
# s = socket. Permissions matter: connecting process needs write permission.
```

---

## Deadlock Detection

### Mutex/Lock Deadlock

```bash
# Full backtraces — look for threads all waiting on locks
gdb --batch \
  -ex "set pagination off" \
  -ex "thread apply all bt full" \
  -p $PID 2>&1 | tee /tmp/deadlock_bt.txt

# Look for classic deadlock signature:
# Thread 1: __lll_lock_wait() → pthread_mutex_lock() → function_A()
# Thread 2: __lll_lock_wait() → pthread_mutex_lock() → function_B()
# Where function_A holds lock that B wants, and vice versa

grep -B10 'lll_lock_wait\|pthread_mutex_lock\|futex.*WAIT' /tmp/deadlock_bt.txt
```

### Async Deadlock (Tokio/async-std)

Async deadlocks don't show mutex waits — they show idle worker threads while tasks are starved:

```bash
# All workers in epoll_wait = no tasks to run (but you have pending requests)
# This means a task is blocking the runtime

# Look for:
# 1. All tokio-runtime-worker threads in epoll_wait
# 2. No thread actively processing your request
# 3. blocking-* threads stuck on I/O or sync operations

grep -A3 'Thread.*tokio-runtime-worker' /tmp/deadlock_bt.txt | grep -c epoll_wait
# If this equals your worker count, the runtime is starved
```

### Complete Lock-Graph Construction Algorithm

A lock graph is a directed graph where an edge from thread T to lock L means "T is waiting for L", and an edge from lock L to thread T means "T holds L". A cycle in this graph proves deadlock. Here is the systematic procedure to build it from GDB output.

```bash
# Step 1: Capture full backtraces with local variables for all threads
gdb --batch \
  -ex "set pagination off" \
  -ex "set print pretty on" \
  -ex "thread apply all bt full" \
  -p $PID 2>&1 | tee /tmp/lock_graph_bt.txt

# Step 2: Identify all threads blocked in lock acquisition
# These appear as threads whose innermost frames are in futex_wait or __lll_lock_wait
grep -B20 '__lll_lock_wait\|futex_wait\|__GI___lll_lock_wait' /tmp/lock_graph_bt.txt

# Step 3: For each blocked thread, extract the mutex address being waited on
# The mutex address appears as the argument to pthread_mutex_lock (frame above futex_wait)
# In the backtrace, look for:
#   #1  0x00007f... in __GI___pthread_mutex_lock (mutex=0x5555deadbeef) at ...
# The mutex= value is the lock address this thread is WAITING for.

# Step 4: For threads NOT blocked in futex, they may be HOLDING locks
# Check local variables and function arguments for mutex pointers
# Also check: which mutexes were locked but not yet unlocked in the call chain?

# Step 5: Build the graph (pseudocode):
#   For each blocked thread T_blocked:
#     mutex_addr = extract mutex address from pthread_mutex_lock argument
#     Find thread T_holder that holds mutex_addr
#       (T_holder is the thread NOT in futex_wait whose code path locked this mutex)
#     Add edge: T_blocked --waits_for--> mutex_addr --held_by--> T_holder
#   A cycle in this graph = deadlock
```

#### Python GDB Script for Automated Lock Graph Construction

```bash
cat > /tmp/lock_graph.py << 'PYEOF'
import gdb
import re

class LockGraph(gdb.Command):
    """Build lock-wait graph from all threads to detect deadlocks."""
    def __init__(self):
        super().__init__("lock-graph", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        waiters = {}   # tid -> mutex_addr (thread is waiting for this mutex)
        holders = {}   # mutex_addr -> tid (this thread holds this mutex)
        thread_info = {}

        for t in gdb.selected_inferior().threads():
            t.switch()
            tid = t.ptid[1]
            frame = gdb.newest_frame()
            frames = []
            f = frame
            while f:
                frames.append(f)
                f = f.older()

            thread_info[tid] = [fr.name() or '??' for fr in frames[:5]]

            # Check if this thread is blocked in lock wait
            top_names = [fr.name() or '' for fr in frames[:4]]
            is_waiting = any('lll_lock_wait' in n or 'futex_wait' in n for n in top_names)

            if is_waiting:
                # Find the pthread_mutex_lock frame and extract mutex address
                for fr in frames:
                    name = fr.name() or ''
                    if 'pthread_mutex_lock' in name:
                        try:
                            fr.select()
                            mutex_val = gdb.parse_and_eval('mutex')
                            mutex_addr = str(mutex_val)
                            waiters[tid] = mutex_addr
                            print(f"Thread {tid} WAITING for mutex at {mutex_addr}")
                        except Exception as e:
                            print(f"Thread {tid} waiting but can't extract mutex: {e}")
                        break

        # Report
        print("\n=== LOCK WAIT GRAPH ===")
        if not waiters:
            print("No threads blocked on mutexes.")
            return

        for tid, mutex in waiters.items():
            frames_str = ' -> '.join(thread_info.get(tid, ['??'])[:3])
            print(f"  Thread {tid} --waits--> {mutex}")
            print(f"    backtrace: {frames_str}")

        # Check for cycles (simplified: if two threads wait for each other's resources)
        print("\n=== CYCLE DETECTION ===")
        print("Manual step: cross-reference mutex addresses with holder threads")
        print("If Thread A waits for mutex M1 held by Thread B,")
        print("and Thread B waits for mutex M2 held by Thread A → DEADLOCK")

LockGraph()
PYEOF

gdb --batch \
  -ex "source /tmp/lock_graph.py" \
  -ex "lock-graph" \
  -p $PID 2>&1
```

### Extracting Mutex Addresses from Futex Arguments

When the `pthread_mutex_lock` frame doesn't have debug info, you can still extract the mutex address from the futex syscall arguments and the register state.

```bash
# The futex syscall signature:
#   futex(uint32_t *uaddr, int futex_op, uint32_t val, ...)
# uaddr (first arg, in rdi register) is the address of the futex word
# For a pthread_mutex_t, the futex word is at offset 0 of the mutex structure
# So rdi in the futex frame = the mutex address

gdb --batch \
  -ex "set pagination off" \
  -ex "thread apply all bt" \
  -p $PID 2>&1 | tee /tmp/bt.txt

# For each thread in futex_wait, switch to it and examine rdi
# In batch mode, extract all at once:
gdb --batch \
  -ex "set pagination off" \
  -ex "set \$i = 1" \
  -ex "thread apply all bt 3" \
  -p $PID 2>&1

# Alternative: use strace to see live futex calls
# Each futex(addr, FUTEX_WAIT, ...) call shows the waited-on address
sudo strace -f -e futex -p $PID 2>&1 | head -50
# Output: [pid 12345] futex(0x5555deadbeef, FUTEX_WAIT_PRIVATE, 2, NULL) = -1 EAGAIN
# The first argument (0x5555deadbeef) is the mutex/futex address
```

### Self-Deadlock Detection

A self-deadlock occurs when a single thread tries to acquire a mutex it already holds. This is the simplest form of deadlock and is common when using non-recursive mutexes in code with complex call graphs.

```bash
# Signature: a single thread blocked in pthread_mutex_lock, and the backtrace
# shows the SAME mutex being locked earlier in the call chain.
#
# Example backtrace:
#   #0  __lll_lock_wait ()
#   #1  pthread_mutex_lock (mutex=0x5555AABBCCDD)    ← trying to lock
#   #2  inner_function ()
#   #3  middle_function ()
#   #4  outer_function ()
#   #5  pthread_mutex_lock (mutex=0x5555AABBCCDD)    ← already locked here!
#   #6  entry_function ()
#
# Detection: look for the same mutex address appearing twice in a single thread's backtrace

# Quick grep to find self-deadlocks
gdb --batch -ex "thread apply all bt full" -p $PID 2>&1 | \
  awk '/^Thread/{thread=$0} /pthread_mutex_lock.*mutex=/{
    mutex=$0; gsub(/.*mutex=/, "", mutex); gsub(/[^0-9a-fx].*/, "", mutex);
    if (seen[thread,mutex]++) print "SELF-DEADLOCK: " thread " locks " mutex " twice";
    else seen[thread,mutex]=1
  }'

# Fix: use PTHREAD_MUTEX_RECURSIVE if re-entrancy is intentional,
# or refactor to avoid nested locking of the same mutex.
```

### Reader-Writer Lock Deadlocks

RwLock deadlocks are subtler than mutex deadlocks because multiple readers can coexist, but specific patterns create irrecoverable situations.

```bash
# Pattern 1: Reader Upgrade Deadlock
# Thread holds read lock, then tries to acquire write lock on same RwLock
# The write lock waits for all readers to release — but this thread IS a reader
# Result: thread deadlocks against itself
#
# Backtrace signature:
#   #0  futex_wait ()
#   #1  __pthread_rwlock_wrlock_full ()  ← wants write
#   ...
#   #N  __pthread_rwlock_rdlock ()       ← already holds read (same rwlock address!)

# Pattern 2: Write Starvation / Reader Convoy
# Not a deadlock per se, but effectively the same symptom (no progress):
# - Writer waiting for readers to drain
# - New readers keep arriving and acquiring the read lock
# - Writer waits forever (or effectively forever)
# This depends on the rwlock implementation: PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP
# prevents new readers from acquiring while a writer is waiting.

# Pattern 3: Bidirectional RwLock Deadlock
# Thread A: holds read on Lock1, wants write on Lock2
# Thread B: holds read on Lock2, wants write on Lock1
# Classic order inversion, but with RwLocks

# Diagnosis from GDB:
gdb --batch -ex "thread apply all bt full" -p $PID 2>&1 | \
  grep -E 'rwlock|RwLock|pthread_rwlock' -A5 -B5
# Look for rwlock addresses in the arguments, same approach as mutex lock graph
```

### Priority Inversion Pattern Recognition

Priority inversion occurs when a high-priority thread is blocked waiting for a lock held by a low-priority thread, and a medium-priority thread preempts the low-priority thread, effectively blocking the high-priority thread behind the medium-priority one.

```bash
# Evidence collection:
# 1. Identify thread priorities
for tid in $(ls /proc/$PID/task/); do
  prio=$(cat /proc/$PID/task/$tid/stat | awk '{print $18}')  # priority field
  nice=$(cat /proc/$PID/task/$tid/stat | awk '{print $19}')  # nice value
  policy=$(chrt -p $tid 2>/dev/null | head -1 | awk -F: '{print $2}')
  comm=$(cat /proc/$PID/task/$tid/comm 2>/dev/null)
  printf "TID %-8s %-25s priority=%-4s nice=%-4s policy=%s\n" "$tid" "$comm" "$prio" "$nice" "$policy"
done

# 2. Build lock graph (as above) and overlay priorities
# If high-priority thread waits on lock held by low-priority thread: potential inversion

# 3. Check if priority inheritance is enabled on the mutex
# PTHREAD_PRIO_INHERIT mutexes automatically boost the holder's priority
# Check mutex attributes: __kind field in pthread_mutex_t
# Bit 5 (0x20) set = PTHREAD_MUTEX_PRIO_INHERIT_NP

gdb --batch \
  -ex "set pagination off" \
  -ex "print *(pthread_mutex_t*)0xMUTEX_ADDR" \
  -p $PID 2>&1
# Look at __data.__kind: values include
#   0 = PTHREAD_MUTEX_TIMED_NP (normal, no PI)
#  32 = PTHREAD_MUTEX_TIMED_NP | PTHREAD_MUTEX_PRIO_INHERIT_NP
```

---

## Memory Corruption

### Use ASAN with GDB

```bash
# Compile with AddressSanitizer
RUSTFLAGS="-Zsanitizer=address" cargo +nightly build --target x86_64-unknown-linux-gnu

# Run under GDB to catch the exact moment ASAN triggers
gdb --batch \
  -ex "set environment ASAN_OPTIONS=abort_on_error=1:detect_leaks=0" \
  -ex "run" \
  -ex "bt full" \
  --args ./target/x86_64-unknown-linux-gnu/debug/binary \
  2>&1 | tee /tmp/asan_bt.txt
```

### Valgrind Integration

```bash
# Valgrind + GDB server (for interactive debugging of memory errors)
valgrind --vgdb=yes --vgdb-error=0 ./binary &
gdb ./binary -ex "target remote | vgdb" -ex "continue"
```

---

## Stripped Binary Handling

When the binary has no debug symbols (common with release builds):

```bash
# Check if stripped
file /proc/$PID/exe
readelf -sW /proc/$PID/exe | head -5

# If binary was deleted (common after rebuild while process runs)
# /proc/PID/exe → /path/to/binary (deleted)
cp /proc/$PID/exe /tmp/recovered_binary
file /tmp/recovered_binary

# For Rust binaries: check for dynamic symbols
readelf -sW /tmp/recovered_binary | grep -i 'accept\|poll\|http\|mcp\|render' | head -20

# GDB will still show frame addresses even without symbols
gdb --batch -ex "thread apply all bt" -p $PID 2>&1
# Output: #0 0x000055df60a7307b in ?? ()
# The ?? means no symbol info — but addresses can be mapped with addr2line if you have the debug binary
```

---

## Signal Handling

```bash
# Send signal while attached (useful for triggering dump)
gdb --batch \
  -ex "handle SIGUSR1 nostop noprint pass" \
  -ex "continue" \
  -p $PID

# Catch specific signal in batch mode
gdb --batch \
  -ex "handle SIGSEGV stop" \
  -ex "continue" \
  -ex "bt full" \
  -ex "info registers" \
  -p $PID 2>&1 | tee /tmp/signal_bt.txt
```

---

## Watchpoints

Hardware watchpoints trigger when a memory location changes — invaluable for data corruption:

```bash
# Watch a global variable
gdb --batch \
  -ex "watch my_global_var" \
  -ex "continue" \
  -ex "bt full" \
  --args ./binary 2>&1

# Watch a memory address
gdb --batch \
  -ex "watch *(int*)0x7ffff7dd1234" \
  -ex "continue" \
  -ex "bt full" \
  -p $PID 2>&1
```

---

## Conditional Breakpoints

```bash
# Break only when a condition is true
gdb --batch \
  -ex "break accept if errno == 11" \
  -ex "commands" \
  -ex "bt" \
  -ex "continue" \
  -ex "end" \
  -ex "run" \
  --args ./binary 2>&1

# Break on Nth hit
gdb --batch \
  -ex "break suspicious_function" \
  -ex "ignore 1 99" \
  -ex "run" \
  -ex "bt full" \
  --args ./binary 2>&1
```

---

## Python GDB Extensions

For complex inspection, GDB Python scripting is powerful:

```bash
# Create a script file
cat > /tmp/gdb_inspect.py << 'EOF'
import gdb

class ThreadDump(gdb.Command):
    """Dump all threads with their top 3 frames"""
    def __init__(self):
        super().__init__("thread-dump", gdb.COMMAND_USER)
    def invoke(self, arg, from_tty):
        for t in gdb.selected_inferior().threads():
            t.switch()
            frame = gdb.newest_frame()
            print(f"\nThread {t.num} (TID {t.ptid[1]}):")
            for i in range(3):
                if frame is None:
                    break
                print(f"  #{i} {frame.name() or '??'} at {frame.pc():#x}")
                frame = frame.older()

ThreadDump()
EOF

# Use the script
gdb --batch \
  -ex "source /tmp/gdb_inspect.py" \
  -ex "thread-dump" \
  -p $PID 2>&1
```

---

## Debugging Patterns by Language

### Rust

```bash
# Rust panics: catch the unwind
gdb --batch \
  -ex "break rust_panic" \
  -ex "run" \
  -ex "bt full" \
  --args ./target/debug/binary 2>&1

# Rust tokio: find blocked futures
gdb --batch \
  -ex "thread apply all bt" \
  -p $PID 2>&1 | grep -A10 'tokio.*poll\|Future.*poll'
```

### Go

```bash
# Go goroutine dump (SIGQUIT gives goroutine traces)
kill -QUIT $PID  # Prints to stderr, doesn't kill

# GDB with Go runtime
gdb --batch \
  -ex "source $(go env GOROOT)/src/runtime/runtime-gdb.py" \
  -ex "info goroutines" \
  -ex "thread apply all bt" \
  -p $PID 2>&1
```

### C/C++

```bash
# Standard debug workflow
gdb --batch \
  -ex "set pagination off" \
  -ex "thread apply all bt full" \
  -ex "info sharedlibrary" \
  -p $PID 2>&1
```

---

## Severity Reference

| Symptom | Severity | First Tool | Second Tool |
|---------|----------|-----------|-------------|
| Segfault/crash | Critical | `gdb --batch -ex bt` (core or attach) | ASAN build |
| 100% CPU spin | High | `ps -Lp` + `strace -p TID` | `gdb --batch -ex "thread apply all bt"` |
| Deadlock (0% CPU) | High | `gdb --batch -ex "thread apply all bt full"` | Lock graph analysis |
| Slow responses | Medium | `ss` + endpoint probes | `perf record` + `gdb` |
| Memory leak | Medium | `heaptrack` or valgrind | `gdb` with watchpoints |
| Intermittent crash | Medium | Core dump analysis | Conditional breakpoints |

---

## Disassembly Reading & Register Analysis

Understanding disassembly is essential when you have no source code, when the optimizer has rearranged code beyond recognition, or when you need to understand exactly what instruction faulted. This section covers x86_64 specifically, as it is the dominant architecture for server-side debugging.

### x86_64 Register Reference

The x86_64 architecture has 16 general-purpose 64-bit registers, plus special-purpose registers. Understanding their conventional roles is critical for reading disassembly and interpreting crash state.

**Instruction and Stack Management:**

| Register | Purpose | Notes |
|----------|---------|-------|
| `rip` | Instruction pointer | Address of the NEXT instruction to execute. In a crash, this is where execution stopped. |
| `rsp` | Stack pointer | Points to the top of the stack (lowest address, stack grows down). Modified by push/pop/call/ret. |
| `rbp` | Base pointer / Frame pointer | In frame-pointer-enabled code, points to the base of the current stack frame. Omitted with `-fomit-frame-pointer` (default in release builds). |
| `rflags` | Flags register | Contains condition flags (ZF=zero, CF=carry, OF=overflow, SF=sign). Controls conditional jumps. |

**System V AMD64 ABI — Function Arguments (Linux, macOS):**

The calling convention dictates how arguments are passed. The first six integer/pointer arguments go in registers, in this exact order:

| Argument # | Register | Example: `fn(a, b, c, d, e, f, g)` |
|-----------|----------|-------------------------------------|
| 1st | `rdi` | a |
| 2nd | `rsi` | b |
| 3rd | `rdx` | c |
| 4th | `rcx` | d |
| 5th | `r8` | e |
| 6th | `r9` | f |
| 7th+ | stack | g (pushed right-to-left onto stack) |

Floating-point arguments use `xmm0`-`xmm7` instead.

**Return value:** `rax` (integer/pointer), `xmm0` (float/double). For 128-bit returns, `rax:rdx`.

**Caller-saved (volatile) registers:** `rax`, `rcx`, `rdx`, `rsi`, `rdi`, `r8`-`r11`
These may be destroyed by any function call. If a caller needs these values after a call, it must save them first.

**Callee-saved (non-volatile) registers:** `rbx`, `rbp`, `r12`-`r15`
Functions must preserve these. If a function uses them, it pushes them on entry and pops them on exit.

```bash
# View all registers in GDB
gdb --batch \
  -ex "info registers" \
  -p $PID 2>&1

# Output interpretation:
# rax            0x0                 0          ← return value or scratch
# rbx            0x7f1234567890      ...        ← callee-saved (preserved across calls)
# rcx            0x5555555551a0      ...        ← 4th argument or scratch
# rdx            0x0                 0          ← 3rd argument or scratch
# rsi            0x7fffffffde10      ...        ← 2nd argument (often pointer to buffer)
# rdi            0x5555555592a0      ...        ← 1st argument (often 'self' or 'this')
# rbp            0x7fffffffdd80      ...        ← frame pointer (if not omitted)
# rsp            0x7fffffffdd60      ...        ← stack pointer
# r8             0x0                 0          ← 5th argument
# r9             0x1                 1          ← 6th argument
# r10            0x7f1234566000      ...        ← scratch (used by syscall)
# r11            0x246               ...        ← scratch (used by syscall for rflags)
# r12-r15        ...                            ← callee-saved
# rip            0x555555555169      ...        ← instruction that caused the fault
# eflags         0x10246             [ PF ZF IF RF ]

# View specific register with formatting
# As hex:
gdb --batch -ex "print/x \$rdi" -p $PID 2>&1
# As decimal:
gdb --batch -ex "print/d \$rax" -p $PID 2>&1
# As string (if it's a char*):
gdb --batch -ex "x/s \$rdi" -p $PID 2>&1
```

### Reading Disassembly Output

GDB provides several commands for disassembly. Each has different strengths.

```bash
# disas (disassemble): shows the current function's disassembly
# The => arrow marks the current instruction pointer
gdb --batch \
  -ex "disas" \
  -p $PID 2>&1

# Output example:
# Dump of assembler code for function process_request:
#    0x555555555140 <+0>:     endbr64                    ← function entry (CET)
#    0x555555555144 <+4>:     push   rbp                 ← save frame pointer
#    0x555555555145 <+5>:     mov    rbp,rsp             ← establish new frame
#    0x555555555148 <+8>:     sub    rsp,0x40            ← allocate 64 bytes of stack
#    0x55555555514c <+12>:    mov    QWORD PTR [rbp-0x38],rdi  ← save 1st arg
#    ...
# => 0x555555555169 <+41>:    mov    rdx,QWORD PTR [rax] ← CURRENT INSTRUCTION
#    0x55555555516c <+44>:    test   rdx,rdx
#    ...

# x/Ni $pc: examine N instructions starting at program counter
# More flexible than disas — works even without function boundaries
gdb --batch \
  -ex "x/20i \$pc" \
  -p $PID 2>&1

# Examine instructions at an arbitrary address
gdb --batch \
  -ex "x/10i 0x555555555140" \
  -p $PID 2>&1

# Use Intel syntax (many find it more readable than AT&T)
gdb --batch \
  -ex "set disassembly-flavor intel" \
  -ex "disas" \
  -p $PID 2>&1
# Intel: mov rax, [rbp-0x8]    (destination first)
# AT&T:  mov -0x8(%rbp), %rax  (source first, % prefix, () for dereference)
```

### The `x/` (Examine Memory) Command — Complete Reference

The `x` command is GDB's most versatile memory inspection tool. Its syntax is `x/NFS ADDRESS` where:

- **N** = count (how many units to display)
- **F** = format (how to display each unit)
- **S** = size (how big is each unit)

**Format specifiers (F):**

| Format | Meaning | Example output |
|--------|---------|---------------|
| `x` | Hexadecimal | `0x7f1234567890` |
| `d` | Signed decimal | `-42` |
| `u` | Unsigned decimal | `4294967254` |
| `o` | Octal | `037777777726` |
| `t` | Binary | `1111...1011010110` |
| `c` | Character | `65 'A'` |
| `s` | Null-terminated string | `"hello world"` |
| `i` | Machine instruction (disassemble) | `mov %rax,%rdx` |
| `a` | Address (symbol+offset) | `0x555555555169 <main+41>` |
| `f` | Float | `3.14159` |

**Size specifiers (S):**

| Size | Meaning | Bytes |
|------|---------|-------|
| `b` | Byte | 1 |
| `h` | Halfword | 2 |
| `w` | Word | 4 |
| `g` | Giant (quadword) | 8 |

```bash
# Common patterns:

# Dump 16 64-bit values from stack (most useful for x86_64)
# x/16gx $rsp
gdb --batch -ex "x/16gx \$rsp" -p $PID 2>&1
# Shows stack contents — return addresses, saved registers, local variables

# Read a C string from a pointer
gdb --batch -ex "x/s \$rdi" -p $PID 2>&1
# x/s 0x555555556004: "Connection refused"

# Examine 32 bytes as hex bytes (good for binary data / packet inspection)
gdb --batch -ex "x/32xb \$rsi" -p $PID 2>&1

# Disassemble 20 instructions from current PC
gdb --batch -ex "x/20i \$pc" -p $PID 2>&1

# Examine a struct — dump 8 quadwords from a pointer
gdb --batch -ex "x/8gx \$rdi" -p $PID 2>&1
# Shows the raw memory layout of whatever rdi points to

# Examine memory at a known address (e.g., global variable)
gdb --batch -ex "x/4gx 0x555555558040" -p $PID 2>&1

# Read 4 32-bit integers
gdb --batch -ex "x/4dw 0x7fffffffde00" -p $PID 2>&1
```

### Common Crash Patterns in Disassembly

#### NULL Pointer Dereference

The most common crash. The faulting instruction tries to read from or write through a register that contains 0 (or a small value close to 0, indicating a struct field offset from a NULL base).

```
# SIGSEGV at this instruction:
=> 0x555555555169:    mov    rdx, QWORD PTR [rax]
# info registers shows: rax = 0x0

# Diagnosis: rax is NULL, and we're trying to read the 64-bit value at address 0.
# Look at preceding instructions to find where rax was set:
#    0x555555555160:    mov    rax, QWORD PTR [rbp-0x18]   ← rax loaded from local variable
# So the local variable at rbp-0x18 is a NULL pointer.

# Variant: NULL + offset (struct field access on NULL pointer)
=> 0x555555555169:    mov    rdx, QWORD PTR [rax+0x28]
# rax = 0x0, trying to read at address 0x28
# This means: ptr->field_at_offset_0x28 where ptr is NULL
# The offset (0x28 = 40 bytes) can identify the struct and field.
```

#### Use-After-Free

Harder to spot than NULL deref because the address looks valid (it's a heap address that was valid before the free). The memory contents are garbage or free-list metadata.

```
# SIGSEGV or corrupted data at:
=> 0x555555555200:    mov    rax, QWORD PTR [rbx+0x10]
# rbx = 0x5555555a2340 — looks like a valid heap address

# But examining the memory reveals freed state:
# x/4gx 0x5555555a2340
# 0x5555555a2340: 0x0000000000000000  0x0000555555590001
# 0x5555555a2350: 0x00007f12345670a0  0x00007f12345670a0
#                  ↑ forward pointer    ↑ backward pointer (free list!)

# glibc free chunks have this pattern:
# [prev_size] [size|flags] [fd] [bk]
# The fd/bk pointers are free-list metadata — this memory has been freed.

# If you see addresses that look like other heap chunks in what should be data fields,
# that's strong evidence of use-after-free.
```

#### Stack Overflow

The stack has a fixed size (default 8MB on Linux). When recursion or large stack allocations exhaust it, rsp moves below the stack guard page and triggers SIGSEGV.

```
# SIGSEGV with rsp at an unusual address:
# info registers shows: rsp = 0x7fffff7fefc0
# But stack should be near:      0x7fffffffe000
# The difference: about 8MB — stack has grown to its limit

# Confirm by checking stack boundaries:
# info proc mappings  (look for [stack])
# 0x7fffff800000     0x800000000000    0x800000  rw-p  [stack]
# rsp (0x7fffff7fefc0) is BELOW the stack mapping — guard page hit

# Common cause: unbounded recursion
# The backtrace will show hundreds or thousands of frames of the same function:
# #0 recursive_function (n=0) at lib.rs:42
# #1 recursive_function (n=1) at lib.rs:42
# #2 recursive_function (n=2) at lib.rs:42
# ... (thousands of frames)

# Or: large stack allocation (e.g., `let buffer: [u8; 4_000_000] = [0; 4_000_000];`)
# The backtrace is short, but rsp drops dramatically in a single frame.
```

#### Buffer Overflow in Disassembly

```
# Signs of buffer overflow — writes past the end of an allocation:
# The crash often occurs in a DIFFERENT function than the one with the bug,
# because the overflow corrupts adjacent data that is used later.

# Stack buffer overflow typically crashes at function return:
=> 0x5555555551ff:    ret
# Because the saved return address on the stack was overwritten with garbage.
# rsp points to the corrupted return address:
# x/gx $rsp → 0x4141414141414141  (clearly overwritten, 'AAAA...')

# Canary detection — stack smashing detected:
# If compiled with -fstack-protector, look for:
#   __stack_chk_fail()
# in the backtrace. The canary (a random value placed between locals and saved rbp/rip)
# was overwritten, and the function's epilog detected it.
```

#### Vtable Corruption (C++ / Trait Object Corruption)

```
# C++ virtual function call:
=> 0x555555555300:    call   QWORD PTR [rax]
# rax = 0x4141414141414141  ← vtable pointer is corrupted

# Normal pattern: rax points to a vtable in .rodata
# Corrupted: rax is garbage, or points to freed/overwritten memory

# For Rust trait objects (fat pointers: [data_ptr, vtable_ptr]):
# The vtable pointer is the second element. If corrupted:
=> 0x555555555300:    call   QWORD PTR [rax+0x18]  ← calling method from corrupted vtable

# Diagnosis:
# 1. What is rax? x/gx $rax — is it a valid address in .rodata?
# 2. If rax looks valid but the vtable entries are garbage, the vtable was overwritten
# 3. If rax itself is garbage, the object pointer was corrupted
```

### Reading Rust Name Mangling

Rust uses a specific name mangling scheme that encodes the full module path, type parameters, and function name. Understanding the pattern helps when symbols are partially available.

```bash
# Rust v0 mangling format (since Rust 1.38):
# _RNvCs1234_10my_crate7my_func
# _R = Rust v0 prefix
# N = namespace (v = value, t = type)
# Cs = crate disambiguator
# 10my_crate = length-prefixed crate name
# 7my_func = length-prefixed function name

# Legacy mangling (still common):
# _ZN4core3fmt9Formatter9write_str17h1234567890abcdefE
# _ZN = C++ ABI prefix (Rust uses it for compatibility)
# 4core = module "core" (4 = length)
# 3fmt = module "fmt"
# 9Formatter = type "Formatter"
# 9write_str = function "write_str"
# 17h1234567890abcdef = hash suffix (unique per monomorphization)

# Demangling tools:
rustfilt '_ZN4core3fmt9Formatter9write_str17h1234567890abcdefE'
# Output: core::fmt::Formatter::write_str

# Or use c++filt (works for legacy Rust mangling):
echo '_ZN4core3fmt9Formatter9write_str17h1234567890abcdefE' | c++filt
# Output: core::fmt::Formatter::write_str::h1234567890abcdef

# In GDB, enable automatic demangling for disassembly output:
gdb --batch \
  -ex "set print asm-demangle on" \
  -ex "disas" \
  -p $PID 2>&1
# Before: call 0x555555555a00 <_ZN4core3fmt9Formatter9write_str17hE>
# After:  call 0x555555555a00 <core::fmt::Formatter::write_str>

# Demangle all symbols in a backtrace:
gdb --batch -ex "thread apply all bt" -p $PID 2>&1 | rustfilt

# For batch processing symbol tables:
readelf -sW binary | rustfilt | grep 'my_module'
```

---

## Lock Contention Analysis

Lock contention occurs when threads spend significant time waiting to acquire locks rather than doing useful work. Unlike deadlock (which is a permanent condition), contention is a performance problem — the program makes progress, but slowly.

### Identifying Lock Contention from GDB Backtraces

```bash
# Capture and analyze
gdb --batch \
  -ex "set pagination off" \
  -ex "thread apply all bt 10" \
  -p $PID 2>&1 | tee /tmp/contention_bt.txt

# Count threads in lock wait — if many threads are here, you have contention
grep -c '__lll_lock_wait\|futex_wait\|pthread_mutex_lock' /tmp/contention_bt.txt

# The classic three-frame contention pattern:
#   #0  __lll_lock_wait ()              ← kernel futex wait
#   #1  __GI___pthread_mutex_lock ()    ← glibc mutex implementation
#   #2  your_application_function ()    ← YOUR code that acquires the lock
#
# The function at frame #2 tells you WHICH lock acquisition site is contended.
# If many threads show the same frame #2, that single lock is the bottleneck.

# Aggregate contention sites:
grep -A2 '__lll_lock_wait' /tmp/contention_bt.txt | grep '#2' | sort | uniq -c | sort -nr
# Output:
#   47 #2  0x555555555abc in connection_pool::get ()
#   12 #2  0x555555555def in logger::write ()
#    3 #2  0x555555555fed in cache::lookup ()
# → 47 threads waiting for the connection pool lock = severe contention
```

### Futex Internals

The futex (Fast Userspace muTEX) is the kernel mechanism underlying all userspace synchronization primitives on Linux. Understanding futex operations helps interpret strace and GDB output.

```bash
# Futex syscall: futex(uint32_t *uaddr, int futex_op, uint32_t val, ...)
#
# uaddr: pointer to the 32-bit futex word in userspace memory
#   - For pthread_mutex_t, this is the __lock field (offset 0)
#   - For pthread_rwlock_t, there are multiple futex words
#   - For std::sync::Mutex in Rust, this is the atomic state variable
#
# futex_op: operation to perform
#   FUTEX_WAIT (0)         — sleep if *uaddr == val (avoids lost wakeup)
#   FUTEX_WAKE (1)         — wake up N waiters
#   FUTEX_WAIT_PRIVATE (128) — same as WAIT but for process-private futexes (optimization)
#   FUTEX_WAKE_PRIVATE (129) — same as WAKE but for process-private futexes
#
# val: expected value (for WAIT) or number of waiters to wake (for WAKE)
#   - FUTEX_WAIT: only sleep if *uaddr still equals val
#     This prevents race: if value changed between userspace check and syscall, don't sleep
#   - FUTEX_WAKE: wake at most val waiters (usually 1 for mutex unlock, INT_MAX for broadcast)

# Observing futex operations in real time:
sudo strace -f -e futex -T -p $PID 2>&1 | head -100
# Output:
# [pid 12345] futex(0x55aabb0, FUTEX_WAIT_PRIVATE, 2, NULL) = 0  <0.003142>
#              ↑ address      ↑ wait (private)     ↑ expected  ↑ duration=3.14ms
# [pid 12346] futex(0x55aabb0, FUTEX_WAKE_PRIVATE, 1) = 1
#              ↑ same addr    ↑ wake               ↑ wake 1    ↑ woke 1 waiter

# Interpreting the expected value (val) for glibc pthread_mutex_t:
# 0 = unlocked
# 1 = locked, no waiters
# 2 = locked, with waiters (futex_wait will be called)
# So FUTEX_WAIT with val=2 means: "I see the mutex is locked with waiters; sleep until woken"
```

### Building a Lock Ownership Map

This is the systematic procedure for determining which thread holds which lock when multiple threads are contended.

```bash
# Step 1: For each thread blocked in futex_wait, record the address being waited on
gdb --batch \
  -ex "set pagination off" \
  -ex "thread apply all bt full 5" \
  -p $PID 2>&1 | tee /tmp/ownership_bt.txt

# Parse out: thread number, mutex address from pthread_mutex_lock arguments
# Example output line:
# Thread 5 (Thread 0x7f... (LWP 12345)):
# #0  __lll_lock_wait ()
# #1  __GI___pthread_mutex_lock (mutex=0x5555aabbccdd)
# → Thread 5 waits on 0x5555aabbccdd

# Step 2: Examine the mutex to find its owner
# glibc pthread_mutex_t.__data.__owner contains the TID of the holding thread
gdb --batch \
  -ex "set pagination off" \
  -ex "print ((pthread_mutex_t*)0x5555aabbccdd)->__data.__owner" \
  -p $PID 2>&1
# Output: $1 = 12340  ← TID of the thread holding this mutex

# Step 3: Map TID back to GDB thread number
gdb --batch -ex "info threads" -p $PID 2>&1 | grep 12340
# Thread 3 (Thread 0x7f... (LWP 12340)):

# Step 4: Build the directed graph
# Thread 5 --waits_for--> mutex@0x5555aabbccdd --held_by--> Thread 3
# Thread 7 --waits_for--> mutex@0x5555aabbccdd --held_by--> Thread 3
# Thread 3 --waits_for--> mutex@0x5555eeff0011 --held_by--> Thread 5
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# CYCLE DETECTED: Thread 3 ↔ Thread 5 = DEADLOCK

# Step 5: For non-deadlock contention (no cycle), identify the bottleneck holder
# If 47 threads wait for a mutex held by Thread 3, what is Thread 3 doing?
gdb --batch -ex "thread 3" -ex "bt full" -p $PID 2>&1
# This reveals whether Thread 3 is:
# - Doing legitimate long-running work under the lock (lock scope too broad)
# - Blocked on I/O while holding the lock (design issue)
# - Blocked on another lock (potential transitive contention chain)
```

### Spinlock Detection

Spinlocks and adaptive mutexes do not enter the kernel (no futex_wait) when they expect short waits. This makes them invisible to futex-based detection but visible through CPU consumption.

```bash
# Pattern: thread consuming 100% CPU but stuck in __pthread_mutex_lock
# WITHOUT a corresponding futex_wait
# This means the mutex is an adaptive mutex (PTHREAD_MUTEX_ADAPTIVE_NP)
# that spins in userspace before falling back to futex

# Detection via strace: no futex syscalls despite lock contention
sudo strace -f -e futex -c -p $PID 2>&1
# If threads are at 100% CPU and you see very few futex calls: spinning

# Detection via perf: cycles burned in __pthread_mutex_lock
perf top -p $PID -t $TID
# If __pthread_mutex_lock or __lll_lock_wait_private dominates: contention

# glibc adaptive mutex: PTHREAD_MUTEX_ADAPTIVE_NP
# Behavior: spin for a configurable number of iterations, then futex_wait
# The spin count is tuned by glibc based on the number of CPUs
# On a many-core machine, spinning is cheaper than context switching
# But if the critical section is long, spinning wastes CPU

# To distinguish spin contention from productive CPU usage:
# Compare instructions retired (perf stat) with useful work metrics
perf stat -e instructions,cycles,cache-misses -p $PID -- sleep 5
# High cycles but low instructions = spinning (or cache thrashing)
# High cycles AND high instructions = doing actual work
```

### Condvar vs Mutex Deadlocks

Condition variables add another dimension to lock analysis. A thread calling `pthread_cond_wait` atomically releases the associated mutex and sleeps. The distinction matters for diagnosis.

```bash
# In a backtrace:
# pthread_cond_wait (cond=0xADDR1, mutex=0xADDR2)
# → Thread is WAITING for a signal/broadcast on the condvar
# → Thread has RELEASED the mutex (another thread can acquire it)
# → This is NORMAL — the thread is waiting for a condition to become true

# vs:
# pthread_mutex_lock (mutex=0xADDR2)
# → Thread is trying to ACQUIRE the mutex
# → If blocked, another thread HOLDS the mutex

# Condvar deadlock patterns:

# Pattern 1: Lost wakeup
# Thread A: pthread_cond_wait(cond, mutex) — sleeping, waiting for signal
# Thread B: already sent the signal BEFORE Thread A started waiting
# Result: Thread A waits forever because the signal was lost
# Fix: always check the predicate in a loop, and signal AFTER changing the predicate

# Pattern 2: Wrong mutex
# Thread A: pthread_cond_wait(cond, mutex1)
# Thread B: lock(mutex2); change_condition(); pthread_cond_signal(cond); unlock(mutex2);
# The condvar is associated with mutex1 but Thread B uses mutex2
# Result: race condition, potentially lost wakeups

# Diagnosis from GDB:
gdb --batch -ex "thread apply all bt full" -p $PID 2>&1 | \
  grep -E 'pthread_cond_wait|pthread_cond_timedwait' -A3 -B3
# Note the mutex= argument: is it the same mutex other threads are using?
# Note the cond= argument: is anyone ever signaling this condvar?
```

### Lock Elision and Adaptive Mutexes

Modern glibc provides adaptive mutexes that combine spinning with futex. Understanding the behavior is important because they create unique diagnostic patterns.

```bash
# glibc PTHREAD_MUTEX_ADAPTIVE_NP behavior:
# 1. First, attempt a trylock (atomic compare-and-swap)
# 2. If that fails, spin for a short period (proportional to CPU count)
#    During spinning: no syscall, pure userspace busy-wait
#    This phase shows as cycles in __pthread_mutex_lock WITHOUT futex_wait
# 3. If still contended after spinning, fall back to futex(FUTEX_WAIT)
#    Now the thread sleeps and doesn't consume CPU

# To determine the mutex type:
gdb --batch \
  -ex "print ((pthread_mutex_t*)0xMUTEX_ADDR)->__data.__kind" \
  -p $PID 2>&1
# Values:
# 0 = PTHREAD_MUTEX_TIMED_NP (normal, goes to futex immediately)
# 1 = PTHREAD_MUTEX_RECURSIVE_NP (allows same thread to lock multiple times)
# 2 = PTHREAD_MUTEX_ERRORCHECK_NP (returns error on double-lock instead of deadlocking)
# 3 = PTHREAD_MUTEX_ADAPTIVE_NP (spins before futex)
# Add 32 (0x20) for PRIO_INHERIT, 64 (0x40) for PRIO_PROTECT

# Hardware Lock Elision (HLE) / Transactional Synchronization Extensions (TSX):
# Intel TSX allows mutexes to be elided entirely using hardware transactions
# The lock acquisition becomes a transaction — if no conflict, no actual locking occurs
# glibc support was removed in 2.35 due to TSX errata, but older systems may have it
# Evidence: perf stat shows RTM_RETIRED.ABORTED events
```

---

## Stripped Binary Forensics

When a binary is stripped (debug symbols removed), GDB shows `??` for function names, no source file references, and no local variable information. This section covers systematic techniques for extracting maximum information from stripped binaries.

### Determining Binary Strip Level

Not all stripping is equal. Understanding what was removed tells you what tools will work.

```bash
# file command — quick triage
file /proc/$PID/exe
# Possible outputs:
# "ELF 64-bit LSB pie executable, x86-64, ... dynamically linked, ... stripped"
#   → No debug info, no symbol table. But dynamic symbols exist (shared lib calls).
# "ELF 64-bit LSB pie executable, x86-64, ... dynamically linked, ... not stripped"
#   → Symbol table present. Function names available. No debug info (no line numbers/locals).
# "ELF 64-bit LSB pie executable, x86-64, ... dynamically linked, ... with debug_info, not stripped"
#   → Full debug info. Best case.

# Detailed check for debug sections
readelf -S /proc/$PID/exe | grep -E '\.debug_|\.symtab|\.strtab'
# .symtab        — symbol table (function names, globals). Removed by `strip`.
# .strtab        — string table for .symtab. Removed with it.
# .debug_info    — DWARF type info, variable names. Removed by `strip -g` or `strip`.
# .debug_line    — source file/line number mapping. Removed by strip.
# .debug_abbrev  — DWARF abbreviation tables. Removed by strip.
# .debug_str     — DWARF string table. Removed by strip.
# .debug_ranges  — address ranges for compilation units. Removed by strip.

# What's left even after full stripping:
readelf -S /proc/$PID/exe | grep -E '\.dynsym|\.dynstr|\.plt|\.got'
# .dynsym  — dynamic symbol table (ALWAYS present in dynamically linked binaries)
# .dynstr  — string table for .dynsym
# .plt     — procedure linkage table (stubs for shared library calls)
# .got     — global offset table (resolved addresses for shared library functions)
# These sections are REQUIRED for the dynamic linker and cannot be stripped.
```

### Exploiting Dynamic Symbols

Even fully stripped binaries retain dynamic symbols for every function imported from shared libraries (libc, libpthread, libssl, etc.) and every function exported (if the binary is also a shared library).

```bash
# Static symbol table (often stripped):
readelf -sW /proc/$PID/exe | head -5
# May show: "Symbol table '.symtab' is not found" if stripped

# Dynamic symbol table (always present for dynamically linked):
readelf --dyn-syms /proc/$PID/exe | head -20
# Shows all imported/exported symbols:
#   1: 0000000000000000 0 FUNC GLOBAL DEFAULT UND pthread_mutex_lock@GLIBC_2.2.5
#   2: 0000000000000000 0 FUNC GLOBAL DEFAULT UND malloc@GLIBC_2.2.5
#   3: 000055555555a100 42 FUNC GLOBAL DEFAULT 14 my_exported_function

# nm equivalents:
nm -D /proc/$PID/exe          # Dynamic symbols only
nm -D /proc/$PID/exe | grep ' T '  # Exported (defined) functions
nm -D /proc/$PID/exe | grep ' U '  # Undefined (imported) functions

# For Rust binaries compiled with cdylib:
nm -D /proc/$PID/exe | rustfilt | grep -v '^$' | head -20

# The PLT entries tell you what library functions the binary calls:
objdump -d -j .plt /proc/$PID/exe 2>/dev/null | head -40
# Each PLT entry is a stub that jumps through the GOT to the actual function
```

### Using addr2line with Separate Debug Info

```bash
# addr2line maps addresses to function names + source locations
# But it needs debug info — either in the binary or in a separate file

# Basic usage (if debug info is available):
addr2line -e /path/to/binary -fip 0xADDRESS
# -f = show function name
# -i = show inlined functions
# -p = pretty print (one line per frame)
# Output: my_function at src/main.rs:42 (inlined by) handle_request at src/server.rs:100

# For addresses from GDB backtraces:
# GDB shows: #0 0x55df60a7307b in ?? ()
# Need to subtract the base address for PIE binaries:
# Base address from: info proc mappings → first mapping of the executable
# Offset = 0x55df60a7307b - 0x55df60000000 = 0xa7307b
addr2line -e /path/to/debug/binary -fip 0xa7307b

# Finding the base address of a running PIE binary:
head -1 /proc/$PID/maps
# 55df60000000-55df60001000 r--p 00000000 ...
# Base = 0x55df60000000

# For non-PIE binaries, use the address directly (no subtraction needed).
```

### Split Debug Info Patterns

Production binaries are often stripped but the debug info is preserved separately. Knowing where to find it is crucial.

```bash
# Pattern 1: Build-ID based (most common on modern Linux)
# Every ELF binary has a unique build ID — a hash of its content
file /proc/$PID/exe | grep -o 'BuildID\[sha1\]=[a-f0-9]*'
# Or:
readelf -n /proc/$PID/exe | grep 'Build ID'
# Output: Build ID: 2d4c84567890abcdef1234567890abcdef123456

# Debug info location: /usr/lib/debug/.build-id/XX/YYYY...YYYY.debug
# Where XX = first 2 hex chars, YYYY = remaining
# Example: /usr/lib/debug/.build-id/2d/4c84567890abcdef1234567890abcdef123456.debug

# Tell GDB where to find split debug info:
gdb --batch \
  -ex "set debug-file-directory /usr/lib/debug" \
  -ex "thread apply all bt" \
  -p $PID 2>&1
# GDB automatically matches by build ID

# Pattern 2: Debug link (less common)
readelf -S /proc/$PID/exe | grep .gnu_debuglink
objdump -s -j .gnu_debuglink /proc/$PID/exe 2>/dev/null
# Contains the filename of the separate debug file + CRC32 checksum
# GDB searches: /usr/lib/debug + the binary's directory

# Pattern 3: debuginfod (modern distros — Fedora, Ubuntu 22.04+)
# Automatic download of debug info from a server
export DEBUGINFOD_URLS="https://debuginfod.ubuntu.com"
# GDB and other tools will automatically fetch debug info by build ID

# Pattern 4: Manual — install debug packages
# Ubuntu/Debian:
apt list --installed 2>/dev/null | grep dbgsym
# To install debug symbols for a library:
# sudo apt install libc6-dbg   (or the -dbgsym variant)
```

### Recovering a Binary from a Running Process

```bash
# Even if the binary file has been deleted from disk (common after rebuild while process runs),
# the kernel keeps it in memory as long as the process runs
ls -la /proc/$PID/exe
# lrwxrwxrwx 1 user user 0 ... /proc/12345/exe -> /path/to/binary (deleted)

# Recover it:
cp /proc/$PID/exe /tmp/recovered_binary
file /tmp/recovered_binary
# This gives you the exact binary the process is running

# Also recover shared libraries:
cat /proc/$PID/maps | grep '\.so' | awk '{print $6}' | sort -u | while read lib; do
  if [ -f "$lib" ]; then
    echo "OK: $lib"
  else
    echo "MISSING: $lib"
    # Library was deleted/updated. Recover from /proc/$PID/map_files/ if needed.
  fi
done

# The map_files directory has symlinks to the exact file (by inode, even if deleted):
ls -la /proc/$PID/map_files/ | head -20
# 55df60000000-55df60001000 -> /path/to/binary (deleted)
# You can copy from here too:
cp "/proc/$PID/map_files/55df60000000-55df60001000" /tmp/recovered_binary
```

### Offline Disassembly and Address Correlation

When GDB shows `??` for function names, you can use offline tools to map addresses to code regions.

```bash
# Full disassembly with Intel syntax
objdump -d -M intel /tmp/recovered_binary > /tmp/full_disasm.txt

# Find the code at a specific address from GDB backtrace:
# GDB shows: #0 0x55df60a7307b in ?? ()
# Subtract base (for PIE): offset = 0xa7307b
grep -A 20 'a7307b:' /tmp/full_disasm.txt
# Or for non-PIE, search for the full address

# Find function boundaries
# Functions typically start with a prologue:
grep -n 'endbr64\|push.*rbp' /tmp/full_disasm.txt | head -50
# endbr64 = Intel CET (Control-flow Enforcement Technology) landing pad
# push rbp; mov rbp,rsp = classic frame pointer setup

# Find which function contains address 0xa7307b:
# Look in the disassembly for the nearest preceding function label
# objdump puts function names (if available) as labels:
#   0000000000a72f00 <some_function>:
#     a72f00: endbr64
#     a72f04: push rbp
#     ...
#     a7307b: mov rax,QWORD PTR [rdx]  ← your address
#     ...
#     a730ff: ret

# For stripped binaries without function labels, identify boundaries by prologue/epilogue:
# Start: endbr64 or push rbp; mov rbp,rsp
# End: ret (or leave; ret)

# Cross-reference with shared library calls (these have names even in stripped binaries):
objdump -d -j .plt /tmp/recovered_binary | head -60
# Shows what library functions are called and their PLT stub addresses
# In the main disassembly, `call` to a PLT address = library function call
```

### DWARF Information Extraction

When debug info exists (either in the binary or separately), DWARF sections contain rich type and source mapping information.

```bash
# Type information (structures, enums, function signatures):
readelf -wi /path/to/debug_binary 2>/dev/null | head -200
# Shows DW_TAG_structure_type, DW_TAG_member, DW_TAG_subprogram, etc.
# Useful for understanding data layouts even when source is unavailable

# Line number information (maps addresses to source file:line):
readelf -wl /path/to/debug_binary 2>/dev/null | head -100
# Shows the line number program — a state machine that maps instruction addresses
# to source locations. This is what addr2line uses internally.

# Function address ranges:
readelf -wR /path/to/debug_binary 2>/dev/null | head -100
# Shows DW_AT_ranges — which address ranges belong to which compilation unit

# Dump all DWARF info for a specific compilation unit:
# Use dwarfdump or llvm-dwarfdump for better formatting:
llvm-dwarfdump --debug-info /path/to/debug_binary 2>/dev/null | head -200

# Extract just function names and their address ranges:
readelf -wi /path/to/debug_binary 2>/dev/null | \
  grep -E 'DW_AT_name|DW_AT_low_pc|DW_AT_high_pc' | head -100
```

---

## Async Runtime Internals (Tokio/async-std)

Debugging async Rust in GDB requires understanding how the compiler and runtime transform `async fn` code into state machines. Without this understanding, GDB backtraces of async code are nearly incomprehensible — showing generated poll functions, opaque state enums, and runtime internals instead of your logical call stack.

### How Async Rust Compiles

Every `async fn` is transformed by the compiler into a state machine that implements the `Future` trait. Each `.await` point becomes a state variant.

```rust
// Source code:
async fn fetch_and_process(url: String) -> Result<Data> {
    let response = client.get(&url).await?;     // await point 1
    let body = response.text().await?;           // await point 2
    let data = parse(body)?;
    save_to_db(&data).await?;                    // await point 3
    Ok(data)
}

// What the compiler generates (conceptually):
enum FetchAndProcessFuture {
    State0 { url: String },                      // initial: before first await
    State1 { url: String, response: Response },   // after await 1, before await 2
    State2 { body: String },                      // after await 2, before await 3
    State3 { data: Data },                        // after await 3
    Complete,
}

impl Future for FetchAndProcessFuture {
    type Output = Result<Data>;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Result<Data>> {
        // Match on current state, try to make progress, transition to next state
        // Return Poll::Pending if the inner future isn't ready
        // Return Poll::Ready when done
    }
}
```

What this means for GDB: when you see a backtrace, you don't see `fetch_and_process` as a function call. Instead you see:
```
#0  <project::fetch_and_process::{{closure}} as core::future::future::Future>::poll
```
And the "local variables" are actually fields of the generated state enum.

### The Future Trait and What GDB Sees

```bash
# When GDB shows a thread executing an async function, the frames look like:
#
# #0  <tokio::time::sleep::Sleep as core::future::future::Future>::poll (...)
# #1  <my_app::handle_request::{{closure}} as core::future::future::Future>::poll (...)
# #2  <tokio::task::harness::Harness<T>>::poll (...)
# #3  tokio::runtime::scheduler::multi_thread::worker::Context::run_task (...)
# #4  tokio::runtime::scheduler::multi_thread::worker::run (...)
#
# Reading bottom-up:
# #4-#3: Tokio runtime machinery — worker thread running a task
# #2: Tokio task harness — manages task lifecycle (cancellation, join handle)
# #1: YOUR async function — this is where your logic is
# #0: An inner future YOUR function is .await-ing (in this case, sleep)
#
# The {{closure}} suffix appears because async blocks/functions are
# desugared into closures that return Futures.

# To find YOUR code in the noise:
gdb --batch -ex "thread apply all bt" -p $PID 2>&1 | \
  grep -v 'tokio::' | grep -v 'core::future' | grep -v 'std::' | \
  grep '::poll\|::{{closure}}'
# This filters out runtime internals and shows your application's futures
```

### Tokio Thread Model — Deep Dive

```bash
# Tokio creates several types of threads, each with distinct roles:

# 1. Runtime Worker Threads: tokio-runtime-worker
#    Count: usually = number of CPU cores (configurable)
#    Role: run the async event loop — poll futures, handle I/O readiness, run timers
#    Normal state: epoll_wait (idle, waiting for I/O events or timer expiry)
#    Busy state: polling a future (your code)
#    CRITICAL: these threads must NEVER block on sync operations
#    If one blocks, you lose 1/N of your runtime capacity

# Identify runtime workers:
ls /proc/$PID/task/ | while read tid; do
  comm=$(cat /proc/$PID/task/$tid/comm 2>/dev/null)
  if [[ "$comm" == *runtime-worker* ]]; then
    wchan=$(cat /proc/$PID/task/$tid/wchan 2>/dev/null)
    cpu=$(ps -o pcpu= -p $tid 2>/dev/null | tr -d ' ')
    echo "Worker TID=$tid wchan=$wchan cpu=${cpu}%"
  fi
done

# 2. Blocking Pool Threads: tokio-runtime-w (truncated name) or blocking-N
#    Created on-demand by spawn_blocking()
#    Role: run synchronous/blocking code off the async runtime
#    These CAN block — that's their entire purpose
#    Default max: 512 threads (configurable)
#    Idle threads are reaped after 10 seconds

# 3. Signal/Driver Thread
#    Handles Unix signal delivery to the runtime
#    Usually blocked in signal_wait

# Count each type:
for tid in $(ls /proc/$PID/task/); do
  cat /proc/$PID/task/$tid/comm 2>/dev/null
done | sort | uniq -c | sort -nr
```

### Diagnosing Task Starvation

Task starvation is the most common Tokio failure mode. The runtime has tasks to run but can't make progress because worker threads are occupied.

```bash
# Diagnostic procedure:

# Step 1: Verify the symptom — requests are timing out but the process is alive
curl -sS --max-time 5 http://127.0.0.1:$PORT/health
# Timeout or slow response confirms starvation

# Step 2: Check worker thread states
gdb --batch \
  -ex "set pagination off" \
  -ex "thread apply all bt 8" \
  -p $PID 2>&1 | tee /tmp/starvation_bt.txt

# Step 3: Classify each worker thread
# Category A: Worker in epoll_wait → idle, no tasks to poll
#   epoll_wait → tokio::runtime::io::driver::Driver::turn → ...
# Category B: Worker executing your code → actively processing a task
#   your_function → ... → tokio::runtime::scheduler::...
# Category C: Worker blocked in sync operation → STARVATION CAUSE
#   std::thread::sleep → ... → tokio::runtime::scheduler::...
#   std::io::Read::read → ... → tokio::runtime::scheduler::...
#   reqwest::blocking::Client::get → ... → tokio::runtime::scheduler::...
#   __lll_lock_wait → pthread_mutex_lock → your_sync_code

# If ALL workers are in Category A but requests time out:
# → Tasks exist but aren't being scheduled
# → Common cause: all tasks are waiting for a channel/oneshot that will never be fulfilled
# → Or: a spawn_blocking call that exhausted the blocking pool

# If ALL workers are in Category C:
# → Every worker is blocked on sync I/O or sleep
# → This is the classic "blocking in async" bug
# → Find the sync call in the backtrace and wrap it in spawn_blocking

# If SOME workers are in Category B with your code, doing CPU work for a long time:
# → Task is CPU-bound and monopolizing the worker
# → Solution: add yield_now() points or move to spawn_blocking

grep -c 'epoll_wait' /tmp/starvation_bt.txt
# Compare to total worker count:
for tid in $(ls /proc/$PID/task/); do
  grep -q 'runtime.worker' /proc/$PID/task/$tid/comm 2>/dev/null && echo $tid
done | wc -l
```

### Channel Debugging (mpsc/broadcast/watch/oneshot)

```bash
# Tokio channels are a major source of hangs — a receiver waiting for data
# that a sender will never send (sender dropped or deadlocked)

# In GDB backtraces, channel waits appear as:
# tokio::sync::mpsc::chan::Rx<T>::recv → poll → park
# tokio::sync::oneshot::Receiver<T>::poll

# Diagnosing: is the sender alive?
# 1. Find the receiver thread — it's waiting in a recv/poll
# 2. The channel's internal state shows if senders exist:
#    - Sender count = 0 → all senders dropped → receiver will get None/error
#    - Sender count > 0 → at least one sender exists
#    - Queue size > 0 → data in queue but receiver not reading it
#    - Queue size = 0, senders exist → senders haven't sent yet

# For Rust: examining the internal state requires knowing the struct layout
# Use `print` with type casting or the `rust-gdb` pretty printers

# Common deadlock pattern: async function holds a mpsc::Sender,
# tries to send on a full bounded channel, which blocks the runtime worker,
# which prevents the receiver (on the same runtime) from draining the channel.
# Fix: use try_send() and handle backpressure, or ensure receiver is on a different task.
```

### Waker Mechanics

The Waker is the mechanism by which futures tell the runtime "I'm ready to make progress — poll me again." Understanding it helps diagnose tasks that are stuck because their waker was never triggered.

```bash
# The poll cycle:
# 1. Runtime calls future.poll(cx) — cx contains a Waker
# 2. If the future can't complete, it saves the Waker and returns Poll::Pending
#    The Waker is typically stored in the I/O driver or timer data structure
# 3. When the event occurs (I/O ready, timer fires), the stored Waker is invoked
# 4. Waker.wake() tells the runtime to re-schedule this task for polling
# 5. Runtime calls future.poll(cx) again — goto step 2 if still not ready

# A "stuck" task = one whose Waker is never invoked:
# - The I/O event never happens (remote host never responds, no data arrives)
# - The timer was never set (code path skipped the timeout)
# - The Waker was dropped without being invoked (bug in a custom Future impl)
# - The task that should trigger the waker is itself stuck (transitive stall)

# In GDB, a task waiting for its Waker looks like an idle runtime worker
# (in epoll_wait or parked). The task simply isn't in any thread's backtrace
# because it's not being polled — it's in the runtime's task queue,
# registered with an I/O resource, waiting for an event that never comes.

# Diagnostic: if you suspect a waker issue, enable tokio-console
# (https://github.com/tokio-rs/console) which tracks task states,
# poll counts, and waker invocations at runtime.
```

---

## Core Dump Forensics

Core dumps capture the complete memory state of a process at the moment of a crash (or at the moment of manual generation via `gcore`). They are the most information-rich artifact for post-mortem debugging, but extracting useful information requires systematic analysis beyond basic `bt`.

### Deep Address Space Analysis

```bash
# Load the core dump with the binary
gdb /path/to/binary /path/to/core

# In batch mode:
gdb --batch \
  -ex "set pagination off" \
  -ex "bt full" \
  -ex "info proc mappings" \
  -ex "info sharedlibrary" \
  -ex "maintenance info sections" \
  -ex "info files" \
  --core /path/to/core /path/to/binary 2>&1 | tee /tmp/core_analysis.txt

# info proc mappings — full address space layout
# Shows every memory mapping: start/end address, size, permissions, backing file
# Key regions to identify:
#   [heap]     — dynamic allocations (malloc/new/Box::new)
#   [stack]    — thread stacks (one per thread, typically 8MB each)
#   [vdso]     — virtual dynamic shared object (kernel-injected, provides fast syscalls)
#   [vsyscall] — legacy fast syscall page
#   /path/binary — the executable's own mappings (.text, .rodata, .data, .bss)
#   /lib/...   — shared library mappings

# info sharedlibrary — loaded shared libraries with address ranges
# Shows each .so with its text segment range
# CRITICAL for address resolution: an address in 0x7f... is likely in a shared library
# This mapping tells you which one

# maintenance info sections — all ELF sections from all loaded objects
# More detailed than info sharedlibrary: shows .text, .data, .bss, .plt, .got per object

# info files — entry point and section ranges
# Shows the binary's entry point (_start) and section boundaries
```

### Examining the Signal Frame

When a process crashes, the kernel delivers a signal (SIGSEGV, SIGABRT, SIGFPE, etc.) and creates a signal frame on the stack containing detailed information about the fault.

```bash
# The signal info structure — contains the reason for the crash
gdb --batch \
  -ex "print \$_siginfo" \
  --core /path/to/core /path/to/binary 2>&1

# Detailed signal information breakdown:
gdb --batch \
  -ex "set pagination off" \
  -ex "print \$_siginfo.si_signo" \
  -ex "print \$_siginfo.si_code" \
  -ex "print \$_siginfo._sifields._sigfault.si_addr" \
  --core /path/to/core /path/to/binary 2>&1

# Signal number interpretation (si_signo):
#  11 (SIGSEGV) — segmentation fault: invalid memory access
#   6 (SIGABRT) — abort: process called abort() (panic, assertion failure)
#   8 (SIGFPE)  — floating point exception (also integer divide by zero)
#   5 (SIGTRAP) — trace/breakpoint trap (debugger breakpoint, int3)
#   7 (SIGBUS)  — bus error (unaligned access, accessing beyond mmap'd file)

# si_code interpretation for SIGSEGV:
#  SEGV_MAPERR (1) — address is not mapped (no virtual memory at this address)
#    Common causes: NULL pointer dereference, stack overflow, wild pointer
#  SEGV_ACCERR (2) — address is mapped but permissions deny the access
#    Common causes: writing to read-only memory (.rodata, .text), NX violation,
#    writing to a guard page, accessing memory after mprotect(PROT_NONE)

# si_addr — the exact address that caused the fault
# This is the gold — it tells you exactly what the faulting instruction tried to access
# Cross-reference with info proc mappings to determine:
# - 0x0 to 0xfff: NULL dereference (+ struct offset)
# - In [heap] range but invalid: use-after-free or heap overflow
# - Just below [stack]: stack overflow (hit guard page)
# - In .text/.rodata: attempted write to read-only section
# - Not in any mapping: wild pointer or integer-to-pointer cast

# Example: segfault at address 0x28
# si_addr = 0x28, si_code = SEGV_MAPERR
# Diagnosis: NULL + 0x28 offset = accessing a field at offset 40 of a NULL pointer
# The struct field at offset 0x28 can identify the type.
```

### Heap Examination

Understanding glibc malloc internals helps diagnose heap corruption, use-after-free, and double-free bugs from core dumps.

```bash
# glibc malloc chunk structure (in-use):
# ┌──────────────┬──────────────────────────┐
# │ prev_size    │ size | flags (A|M|P)     │ ← chunk header (16 bytes on x86_64)
# ├──────────────┴──────────────────────────┤
# │ user data                               │ ← pointer returned by malloc()
# │ ...                                     │
# └─────────────────────────────────────────┘
#
# Flags in the size field (bottom 3 bits):
#   P (bit 0) = PREV_INUSE: previous chunk is in use (1) or free (0)
#   M (bit 1) = IS_MMAPPED: chunk was allocated via mmap (not arena)
#   A (bit 2) = NON_MAIN_ARENA: chunk belongs to a non-main arena (threaded malloc)
#
# The actual size = size_field & ~0x7 (mask off flag bits)

# Examine a chunk header (go 16 bytes before the user pointer):
gdb --batch \
  -ex "x/4gx 0xUSER_PTR - 16" \
  --core /path/to/core /path/to/binary 2>&1
# Output:
# 0x5555555a2330: 0x0000000000000000  0x0000000000000051
# 0x5555555a2340: 0x48656c6c6f20576f  0x726c642100000000
#                  ↑ prev_size=0       ↑ size=0x50|P=1     ↑ user data begins here
# Actual chunk size: 0x50 = 80 bytes (including header). User gets 80-16 = 64 bytes.

# Free chunk structure (small/normal bins):
# ┌──────────────┬──────────────────────────┐
# │ prev_size    │ size | flags             │
# ├──────────────┴──────────────────────────┤
# │ fd (forward pointer to next free chunk) │
# │ bk (backward pointer to prev free)     │
# │ (possibly more for large chunks)        │
# └─────────────────────────────────────────┘
#
# Detecting a freed chunk:
# x/4gx 0xPTR - 16
# If the first quadword of user data looks like a heap address → probably fd pointer → freed
# If both first two quadwords look like heap addresses → fd and bk → definitely freed

# Main arena location (glibc):
# The main_arena is a global variable in libc
gdb --batch \
  -ex "print main_arena" \
  --core /path/to/core /path/to/binary 2>&1
# If debug symbols for libc are available, this shows the entire arena state:
# mutex, flags, fastbinsY[], top, last_remainder, bins[], etc.

# Without libc debug symbols, find it by address:
# main_arena is typically at a known offset from the libc base
# readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep main_arena
```

### Stack Examination

Manual stack examination is essential when frame pointers are omitted (common in optimized builds) and GDB can't reconstruct the backtrace.

```bash
# Raw stack dump — show 100 quadwords from the stack pointer
gdb --batch \
  -ex "x/100gx \$rsp" \
  --core /path/to/core /path/to/binary 2>&1

# Interpreting raw stack contents:
# Return addresses: values in the executable's .text range (0x5555555xxxxx for PIE)
# Saved frame pointers: values near $rsp (within a few KB)
# Local variables: arbitrary values
# Function arguments: may be on stack if more than 6 args

# Manual backtrace via frame pointer chain:
# If frame pointers are preserved (compiled without -fomit-frame-pointer):
# rbp → saved_rbp | return_addr
#        ↓
#        saved_rbp | return_addr
#        ↓
#        ...

gdb --batch \
  -ex "set \$fp = \$rbp" \
  -ex "while \$fp != 0" \
  -ex "  printf \"frame at %p, return addr = %p\\n\", \$fp, *(void**)(\$fp + 8)" \
  -ex "  set \$fp = *(void**)\$fp" \
  -ex "end" \
  --core /path/to/core /path/to/binary 2>&1

# Stack canary detection:
# With -fstack-protector, the compiler places a random canary value between
# local variables and the saved rbp/return address.
# If a buffer overflow overwrites past the locals, it corrupts the canary,
# and the function epilog detects this and calls __stack_chk_fail().

# In the core dump, look for:
# - __stack_chk_fail in the backtrace → canary was corrupted → buffer overflow
# - The canary value is stored in the thread-local storage (FS:0x28 on x86_64):
gdb --batch \
  -ex "print *(long*)\$fs_base + 0x28" \
  --core /path/to/core /path/to/binary 2>&1
# Compare this with the value at the expected canary location on the stack

# Common sentinel values that indicate corruption:
# 0x4141414141414141 — 'AAAA...' — classic buffer overflow with 'A' fill
# 0xdeadbeefdeadbeef — intentional poisoning (debug allocators)
# 0xfefefefefefefefe — ASAN freed memory fill
# 0xbebebebebebebebe — ASAN stack after return fill
# 0xcccccccccccccccc — MSVC uninitialized stack fill (if cross-debugging)
```

### Core Dump Collection Setup

Proper core dump collection configuration must be in place BEFORE the crash. These settings determine whether a core dump is generated, where it goes, and how large it can be.

```bash
# 1. Enable core dumps (process-level limit)
# This is the #1 reason people don't get core dumps — it's disabled by default
ulimit -c unlimited    # Allow unlimited core file size
# WARNING: ulimit -c 0 DISABLES core dumps entirely (the default on most systems)

# Check current limit:
ulimit -c
# If 0: no core dumps will be generated

# Make it persistent — add to /etc/security/limits.conf:
# *  soft  core  unlimited
# *  hard  core  unlimited

# 2. Configure core dump destination (system-level)
# The core_pattern controls WHERE core dumps are written and their filename

# Classic file-based pattern:
sudo sysctl kernel.core_pattern='/tmp/core.%p.%e.%t'
# %p = PID
# %e = executable name (first 15 chars)
# %t = UNIX timestamp
# %u = UID
# %g = GID
# %s = signal number that caused the dump
# %h = hostname
# Example filename: /tmp/core.12345.my_server.1706000000

# Persist across reboot:
echo 'kernel.core_pattern = /tmp/core.%p.%e.%t' | sudo tee /etc/sysctl.d/99-coredump.conf
sudo sysctl -p /etc/sysctl.d/99-coredump.conf

# 3. For setuid/setcap binaries:
cat /proc/sys/fs/suid_dumpable
# 0 = no core dump for setuid programs (default, secure)
# 1 = core dump but owned by root
# 2 = core dump with normal permissions (needed for debugging setcap/setuid binaries)
sudo sysctl fs.suid_dumpable=2

# 4. systemd-coredump (modern distros — the default on Fedora, Arch, Ubuntu 22.04+)
# systemd intercepts core dumps and stores them compressed in /var/lib/systemd/coredump/
# Managed via coredumpctl:

# List recent core dumps:
coredumpctl list
# Output:
# TIME       PID UID GID SIG COREFILE EXE
# Wed 12:34  123 1000 1000 11 present /usr/bin/my_server

# Open the most recent core dump directly in GDB:
coredumpctl debug
# Or for a specific PID:
coredumpctl debug 12345

# Extract the core file:
coredumpctl dump 12345 > /tmp/core.12345

# Show info about a core dump:
coredumpctl info 12345

# systemd-coredump configuration: /etc/systemd/coredump.conf
# [Coredump]
# Storage=external      # Save core dumps (vs 'none' to disable)
# Compress=yes          # Compress with zstd
# ProcessSizeMax=2G     # Max core dump size to process
# ExternalSizeMax=2G    # Max size to store
# MaxUse=1G             # Total disk space for all core dumps
# KeepFree=1G           # Minimum free space to maintain

# 5. Generate a core dump on demand (without killing the process)
gcore $PID
# Creates core.$PID in the current directory
# The process is stopped briefly during dump, then resumed
# Useful for capturing state of a hung process without killing it

# 6. Verify core dump generation works:
# Test with: sleep 1000 & kill -SIGSEGV $!
# Then check if core file appears in the expected location
```
