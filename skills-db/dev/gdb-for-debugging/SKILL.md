---
name: gdb-for-debugging
description: >-
  Debug running processes with GDB, strace, and /proc inspection. Use when:
  process hang, spin loop, segfault, crash, backtrace, attach debugger, ptrace,
  core dump, thread starvation, accept loop, deadlock, busy wait, or diagnose
  why a process is stuck.
---

<!-- TOC: Core Principle | Prerequisites | The Loop | Quick Reference | Attach to Running Process | Reading GDB Output | Diagnosing Hangs | Crash & Segfault | Thread Analysis | When GDB Is Blocked | Advanced Techniques | Reverse Debugging (rr) | Memory Corruption & Sanitizers | Hardware Watchpoints | Lock Graph & Deadlock Proof | Async Runtime Debugging | Container & Namespace Debugging | Multi-Process Debugging | Race Condition Methodology | GDB Python Scripting | Core Dump Forensics | Iterative Workflow | Anti-Patterns | Checklist | References -->

# GDB for Debugging

> **Core Principle:** Observe first, intervene minimally, detach cleanly. GDB is a scalpel — use it to gather evidence, not to poke randomly.

> **The ptrace Reality:** On modern Linux, `ptrace_scope=1` blocks GDB attach by default. You MUST relax this before attaching, or you'll waste time on "Operation not permitted" errors. This is the #1 thing agents get wrong.

---

## Prerequisites — Do This First

```bash
# 1. Check ptrace policy (MUST be 0 for gdb attach to work)
cat /proc/sys/kernel/yama/ptrace_scope
# 0 = classic (any process can attach)  ← REQUIRED
# 1 = restricted (only parent can attach) ← DEFAULT, blocks gdb -p

# 2. Relax ptrace if needed (requires sudo)
sudo sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'

# 3. Verify gdb is installed
which gdb || sudo apt-get install -y gdb

# 4. Verify the target process exists
ps -p $PID -o pid,pcpu,pmem,stat,etime,comm,args
```

**CRITICAL:** After relaxing ptrace, you can leave it at 0 on development machines. On production, restore with `echo 1 > /proc/sys/kernel/yama/ptrace_scope` after debugging.

---

## The Loop (Mandatory)

```
1. TRIAGE        → ps, ss, /proc — what is the process doing?
2. RELAX PTRACE  → echo 0 > /proc/sys/kernel/yama/ptrace_scope
3. ATTACH GDB    → gdb --batch -ex "thread apply all bt" -p PID
4. ANALYZE       → Read backtraces, identify hot threads, stuck syscalls
5. TARGETED DIVE → strace specific threads, inspect /proc/PID/fd
6. DIAGNOSE      → Map symptoms to root cause
7. FIX           → Patch code or configuration
8. VERIFY        → Confirm fix resolves the issue
```

---

## Quick Reference — Copy-Paste Commands

```bash
# === INSTANT TRIAGE (run these BEFORE touching gdb) ===
ps -p $PID -o pid,ppid,etime,pcpu,pmem,stat,comm,args
ps -Lp $PID -o pid,tid,psr,pcpu,stat,wchan:32,comm --sort=-pcpu | head -40

# === RELAX PTRACE + FULL BACKTRACE (the most common operation) ===
ORIG=$(cat /proc/sys/kernel/yama/ptrace_scope)
sudo sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'
gdb --batch -ex "set pagination off" -ex "thread apply all bt full" -p $PID 2>&1 | tee /tmp/gdb_bt_$PID.txt
# Optionally restore: sudo sh -c "echo $ORIG > /proc/sys/kernel/yama/ptrace_scope"

# === BACKTRACE VIA HOT THREAD TID (attaches to whole process via TID) ===
gdb --batch -ex "thread apply all bt" -p $TID 2>&1 | head -100

# === ATTACH, BACKTRACE, DETACH IN ONE SHOT (safe for production-ish) ===
gdb -batch-silent \
  -ex "set confirm off" \
  -ex "set pagination off" \
  -ex "thread apply all bt" \
  -ex "detach" \
  -ex "quit" \
  -p $PID 2>&1 | tee /tmp/gdb_bt.txt

# === NETWORK: SOCKET STATE + BACKTRACES ===
ss -ltnp "sport = :$PORT"                        # Listening?
ss -tnp state established "sport = :$PORT"       # Connections? Check Recv-Q
gdb --batch -ex "thread apply all bt" -p $PID    # What's each thread doing?

# === STRACE A SPECIFIC THREAD (when gdb shows a thread is hot) ===
timeout 5s strace -tt -T -s 120 -p $TID -e trace=network,poll,epoll_wait,futex 2>&1 | head -200

# === PERF RECORD (when you need flamegraph-level detail) ===
perf record -F 199 -g -p $PID -- sleep 8
perf report --stdio --no-children --sort comm,dso,symbol | head -200
```

---

## Attach to a Running Process

### Step 1: Identify the Target

```bash
# Find the process
ps -eo pid,etimes,pcpu,pmem,args | grep "$PROCESS_NAME" | grep -v grep

# Get thread-level detail (ESSENTIAL for multi-threaded processes)
ps -Lp $PID -o pid,tid,psr,pcpu,stat,wchan:32,comm --sort=-pcpu | head -40
# Look for: Rl+ (running on CPU) vs Sl+ (sleeping) — running threads are your suspects
```

### Step 2: Relax ptrace

```bash
# Save original value, relax, and verify
ORIG=$(cat /proc/sys/kernel/yama/ptrace_scope)
sudo sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'
printf 'ptrace_scope: before=%s after=%s\n' "$ORIG" "$(cat /proc/sys/kernel/yama/ptrace_scope)"
```

### Step 3: GDB Batch Attach

**Always use batch mode** for agent-driven debugging. Interactive GDB blocks your session.

```bash
# Full thread backtraces (THE go-to command)
gdb --batch \
  -ex "set pagination off" \
  -ex "set print thread-events off" \
  -ex "thread apply all bt full" \
  -p $PID 2>&1 | tee /tmp/${PROCESS_NAME}_gdb_bt.txt

# Quick summary (fewer details, faster)
gdb --batch \
  -ex "thread apply all bt 10" \
  -p $PID 2>&1 | tee /tmp/${PROCESS_NAME}_gdb_bt.txt
```

### Step 4: Parse the Output

```bash
# Count threads
grep -c '^Thread ' /tmp/${PROCESS_NAME}_gdb_bt.txt

# Find threads in specific functions
grep -A5 'accept4\|epoll_wait\|futex\|poll\|recv\|send' /tmp/${PROCESS_NAME}_gdb_bt.txt

# Find threads NOT sleeping (potential busy loops)
grep -B2 'syscall\|in ??\|running' /tmp/${PROCESS_NAME}_gdb_bt.txt
```

---

## Reading GDB Output Like an Expert

Understanding GDB output is the difference between staring at a wall of text and instantly identifying the bug. This section teaches you to read backtraces the way a systems engineer does.

### Anatomy of a Backtrace Frame

```
#3  0x00007f8a4c3e5b7f in __GI___pthread_mutex_lock (mutex=0x5555deadbeef) at pthread_mutex_lock.c:80
│   │                        │                         │                       │
│   │                        │                         │                       └─ Source location (if debug info)
│   │                        │                         └─ Function arguments (invaluable for lock debugging)
│   │                        └─ Function name (demangled). ?? means no symbols
│   └─ Instruction pointer — exact address being executed
└─ Frame number. #0 is the innermost (current), higher numbers are callers
```

**Key insight:** Frame #0 is WHERE the thread is right now. Frame #1 is who called it. Frame #2 is who called THAT. Reading bottom-up gives you the causal chain: "main() called server_loop() called accept_connection() called accept4()".

### Decoding `??` and Missing Symbols

When you see `#0 0x000055df60a7307b in ?? ()`, the binary is stripped. You have options:

```bash
# Option 1: addr2line (if you have a debug build or separate .debug file)
addr2line -e /path/to/binary -fip 0x55df60a7307b
# → function_name at source.rs:42

# Option 2: readelf to find the closest named symbol
readelf -sW /proc/$PID/exe | gawk '$2 ~ /^[0-9a-f]/ && strtonum("0x"$2) <= strtonum("0x55df60a7307b")' | tail -3
# Shows the symbol just below the address — likely the function containing it

# Option 3: objdump for disassembly at that address
objdump -d /proc/$PID/exe | grep -A20 'a7307b'
# Shows the instructions around the crash point

# Option 4: For Rust binaries, dynamic symbols are often still present
readelf --dyn-syms /proc/$PID/exe | grep -i 'accept\|poll\|http\|tokio' | head -20
```

### GDB Thread ID vs Kernel TID Mapping

GDB assigns its own thread numbers (Thread 1, Thread 2, ...) which DON'T match kernel TIDs. To correlate:

```bash
# GDB header line format:
# Thread 3 (Thread 0x7f8a4c3e5700 (LWP 3480909)):
#                                       ^^^^^^^^
#                                       This is the kernel TID (LWP = Light Weight Process)

# Map GDB threads to kernel TIDs
gdb --batch -ex "info threads" -p $PID 2>&1 | awk '/Thread/{print "GDB",$1,"→ TID",$NF}'

# Then correlate with ps thread output
ps -Lp $PID -o tid,pcpu,comm --sort=-pcpu | head -10
# Match TIDs to identify which GDB thread is the hot one
```

### Reading Rust Backtraces in GDB

Rust symbol names are mangled. GDB usually demangles them, but not always:

```bash
# Mangled: _ZN3std2io5stdio6_print17hXXXXXXXXXXXXXXXXE
# Demangled: std::io::stdio::_print

# Enable demangling in GDB
gdb --batch \
  -ex "set print asm-demangle on" \
  -ex "set print demangle on" \
  -ex "thread apply all bt" \
  -p $PID 2>&1 | tee /tmp/bt.txt

# If still mangled, pipe through rustfilt
cat /tmp/bt.txt | rustfilt

# Rust async futures show up as generated state machine types:
# <my_module::my_function::{{closure}} as core::future::future::Future>::poll
# This means: "the future created by my_module::my_function is being polled"
# The actual code is inside my_function, at whatever .await was last reached
```

### Interpreting Crash Registers

When a process segfaults, the register state tells you exactly what happened:

```bash
# Get registers at crash
gdb --batch \
  -ex "set pagination off" \
  -ex "run" \
  -ex "info registers" \
  -ex "x/5i \$pc" \
  --args /path/to/binary 2>&1

# Key registers (x86_64 System V ABI):
# rip — instruction pointer (where the crash happened)
# rsp — stack pointer (if near guard page, stack overflow)
# rax — return value / scratch (if 0 and dereferenced, NULL pointer)
# rdi — first argument to current function
# rsi — second argument
# rdx — third argument
# rcx — fourth argument
# r8  — fifth argument
# r9  — sixth argument
# rbp — frame pointer (if -fno-omit-frame-pointer was used)

# Example crash analysis:
# Instruction: mov (%rax),%rdx    ← dereferencing rax
# rax = 0x0000000000000000        ← rax is NULL
# Diagnosis: NULL pointer dereference — whatever was supposed to be in rax was never initialized

# Example: use-after-free
# Instruction: mov 0x10(%rax),%rdx
# rax = 0x00005555deadbeef        ← looks like valid heap address
# But the memory at that address contains garbage/freed patterns
# Check: x/4gx $rax — freed glibc chunks often show 0x0 or free-list pointers
```

### Identifying the "Interesting" Thread

In a 50+ thread process, most threads are idle. Here's how to find the one that matters:

```bash
# Method 1: Find threads NOT in expected wait states
gdb --batch -ex "thread apply all bt 3" -p $PID 2>&1 | \
  grep -v 'epoll_wait\|poll_schedule\|futex_wait\|nanosleep\|pipe_read' | \
  grep -B1 '^#0'

# Method 2: Parse for threads doing actual work
gdb --batch -ex "thread apply all bt 3" -p $PID 2>&1 | \
  awk '/^Thread/{t=$0} /^#0.*accept4|^#0.*recv|^#0.*write|^#0.*your_function/{print t; print}'

# Method 3: Cross-reference with CPU usage (most reliable)
HOT_TID=$(ps -Lp $PID -o tid,pcpu --sort=-pcpu --no-headers | head -1 | awk '{print $1}')
gdb --batch -ex "info threads" -p $PID 2>&1 | grep "$HOT_TID"
# Shows which GDB thread number corresponds to the hot TID
```

### The Three-Second Rule for Backtrace Triage

When faced with a wall of backtraces, apply this 3-second triage:

1. **Count threads:** `grep -c '^Thread ' bt.txt` — 54 threads? That's a lot for a simple server.
2. **Find non-sleeping:** `grep -c 'epoll_wait\|futex_wait\|nanosleep' bt.txt` — if 53 are sleeping, 1 is your suspect.
3. **Check that one:** What's it doing? `accept4` loop? `malloc` recursion? `pthread_mutex_lock`? That's your bug.

---

## Diagnosing Hangs & Spin Loops

> **Real-world incident:** A Rust async HTTP server (am) was at 183% CPU while MCP POST requests timed out with 0 bytes returned. GDB revealed 54 threads, with `asupersync-work` thread spinning in `accept4()` returning EAGAIN in a tight loop — the accept loop lacked backoff/polling.

### The Pattern

```
1. ps -Lp shows one thread at ~100% CPU (Rl+ state)
2. strace on that TID shows a tight syscall loop (accept4/EAGAIN, futex/WAKE)
3. gdb bt shows the call stack leading to the tight loop
4. ss shows socket state (Recv-Q > 0 = unread data = stuck reader)
```

### Complete Hang Diagnosis Workflow

```bash
PID=12345  # Your target process

# 1. Which threads are hot?
ps -Lp $PID -o pid,tid,psr,pcpu,stat,wchan:32,comm --sort=-pcpu | head -20

# 2. Socket health (for network services)
ss -ltnp "sport = :$PORT"                         # Listen backlog filling up?
ss -tnp state established "sport = :$PORT"         # Recv-Q > 0 = stuck reader

# 3. What syscall is the hot thread making?
HOT_TID=$(ps -Lp $PID -o tid,pcpu --sort=-pcpu --no-headers | head -1 | awk '{print $1}')
timeout 5s strace -tt -T -s 120 -p $HOT_TID \
  -e trace=network,poll,epoll_wait,futex 2>&1 | head -200

# 4. Full backtrace
gdb --batch -ex "set pagination off" -ex "thread apply all bt full" -p $PID \
  2>&1 | tee /tmp/hang_bt.txt

# 5. If binary is stripped (no symbols), recover it
cp /proc/$PID/exe /tmp/recovered_binary
file /tmp/recovered_binary
readelf -sW /tmp/recovered_binary | grep -i 'accept\|poll\|http\|mcp' | head -20
```

### Common Hang Patterns

| Symptom | strace Shows | GDB Shows | Root Cause |
|---------|-------------|-----------|------------|
| 100% CPU, no progress | `accept4()=EAGAIN` tight loop | Userspace accept loop | Missing epoll/poll before accept |
| 100% CPU, futex spam | `futex(WAKE)` rapid-fire | Spinlock or busy-wait | Contention or broken condvar |
| 0% CPU, won't respond | `futex(WAIT)` forever | Deadlock in mutex | Lock ordering bug |
| Slow responses | `epoll_wait()` returns, slow handling | Deep call stack | Thread starvation or slow I/O |
| Network timeout | Connection established but no data | Thread blocked on lock | Reader thread blocked elsewhere |

---

## Crash & Segfault Debugging

### Core Dumps

```bash
# Enable core dumps
ulimit -c unlimited
echo '/tmp/core.%p.%e' | sudo tee /proc/sys/kernel/core_pattern

# After crash, analyze
gdb /path/to/binary /tmp/core.PID.binary_name
# In gdb:
#   bt full                    — backtrace with local variables
#   thread apply all bt        — all threads at crash time
#   info registers             — register state
#   x/20i $pc                  — disassembly around crash point
```

### GDB Run with Crash Capture

```bash
# Run binary under gdb, auto-capture crash info
gdb --batch \
  -ex "set pagination off" \
  -ex "run" \
  -ex "bt full" \
  -ex "thread apply all bt" \
  -ex "info registers" \
  -ex "quit" \
  --args /path/to/binary --arg1 --arg2 \
  2>&1 | tee /tmp/crash_bt.txt
```

### Breakpoint Debugging (for reproducible crashes)

```bash
# Run with breakpoint at a specific function
gdb --batch \
  -ex "set pagination off" \
  -ex "break suspicious_function" \
  -ex "run" \
  -ex "bt full" \
  -ex "info locals" \
  -ex "continue" \
  -ex "quit" \
  --args /path/to/binary \
  2>&1 | tee /tmp/break_bt.txt
```

### Timeout Protection (for hangs during debug)

```bash
# GDB with timeout — prevents hanging indefinitely
timeout 30s gdb --batch \
  -ex "set pagination off" \
  -ex "thread apply all bt" \
  -p $PID 2>&1 | tee /tmp/gdb_bt.txt
echo "gdb_rc=$?"
```

---

## Thread Analysis Deep Dive

### Map Thread Names to Backtraces

```bash
# Get thread names from /proc
ls /proc/$PID/task/ | while read tid; do
  name=$(cat /proc/$PID/task/$tid/comm 2>/dev/null || echo "?")
  wchan=$(cat /proc/$PID/task/$tid/wchan 2>/dev/null || echo "?")
  printf "TID %s: %s (wchan: %s)\n" "$tid" "$name" "$wchan"
done

# Cross-reference with gdb thread list
gdb --batch -ex "info threads" -p $PID 2>&1
```

### Thread Wait Channel Analysis (No GDB Needed)

```bash
# Quick thread state without attaching
ps -Lp $PID -o pid,tid,pcpu,stat,wchan:30,comm | head -40

# Common wchan values:
# futex_do_wait    — waiting on a futex (mutex, condvar, channel)
# poll_schedule_timeout — epoll/poll wait (normal for I/O threads)
# -                — running on CPU (hot thread!)
# pipe_read        — waiting for pipe input
# unix_stream_read — waiting for Unix socket data
```

---

## When GDB Is Blocked (Fallback Techniques)

If ptrace cannot be relaxed (e.g., container, hardened host):

```bash
# 1. /proc thread states (always available)
ps -Lp $PID -o pid,tid,psr,pcpu,stat,wchan:32,comm --sort=-pcpu

# 2. /proc/PID/syscall (may need root)
for i in $(seq 1 200); do cat /proc/$PID/syscall 2>/dev/null; done | \
  awk '{print $1}' | sort | uniq -c | sort -nr | head -20

# 3. /proc/PID/status (always readable by owner)
cat /proc/$PID/status | grep -E 'State|Threads|VmRSS|voluntary_ctxt_switches|nonvoluntary_ctxt_switches'

# 4. strace with sudo (if available)
sudo timeout 5s strace -ff -tt -s 128 -p $PID \
  -e trace=network,poll,epoll_wait,futex \
  -o /tmp/strace_out 2>&1

# 5. perf record (if available)
perf record -F 199 -g -p $PID -- sleep 8
perf report --stdio --no-children | head -200
```

---

## Advanced Techniques (From Real Sessions)

### LD_PRELOAD Deadlock Avoidance

When debugging a process that uses `LD_PRELOAD`, setting the variable in the shell environment causes GDB itself to load the interposed library, which can deadlock GDB during initialization (especially if the library interposes `malloc`, `free`, or `pthread_mutex_lock`).

```bash
# BAD: GDB itself loads the preload library and may deadlock
LD_PRELOAD=/path/to/lib.so gdb --batch -ex run --args ./binary

# GOOD: Only the target process gets the preload
gdb --batch \
  -ex "set env LD_PRELOAD /path/to/lib.so" \
  -ex "run" \
  -ex "bt" \
  --args ./binary
```

### Stack Overflow Provocation (Recursion Detection)

When a process hangs due to suspected infinite recursion but the default 8MB stack is too large to overflow naturally, artificially limit it to force a crash with a revealing backtrace:

```bash
ulimit -s 256    # 256KB stack (default is 8MB) — recursion overflows much faster
gdb --batch \
  -ex "set pagination off" \
  -ex "run" \
  -ex "thread apply all bt 25" \
  --args ./binary 2>&1 | tee /tmp/recursion_bt.txt

# Iterative fix loop: crash → fix recursion A → crash → fix recursion B → ...
```

### strace -k for Symbolized Stacks (GDB Alternative)

When GDB causes issues (LD_PRELOAD deadlock, etc.), `strace -k` provides call stacks at every syscall:

```bash
timeout 20s strace -f -k -o /tmp/crash.strace ./binary || true
grep -A10 'SIGSEGV\|SIGABRT' /tmp/crash.strace | head -40
```

### Shared Library Breakpoints

Breakpoints on functions in shared libraries (including `LD_PRELOAD` libraries) require `pending` mode:

```bash
gdb --batch \
  -ex "set breakpoint pending on" \
  -ex "break sched_yield" \
  -ex "break __sched_yield" \
  -ex "break pthread_yield" \
  -ex "run" \
  -ex "thread apply all bt" \
  --args ./binary
```

Set multiple symbol variants because the actual name varies (`sched_yield`, `__sched_yield`, `pthread_yield`). If all miss, the code may use raw `syscall()` — use conditional breakpoints: `break syscall if $rdi==24`.

### The `start` Command (Break at main)

When you need to catch early initialization issues, `start` runs to the beginning of `main()` and stops:

```bash
timeout 15s gdb -q -batch \
  -ex 'set pagination off' \
  -ex 'set env LD_PRELOAD /path/to/lib.so' \
  -ex 'start' \
  -ex 'thread apply all bt' \
  --args /path/to/binary
```

This is especially useful when the process crashes during initialization before you can attach.

### Background + Sleep + Attach (For Processes That Hang, Not Crash)

When a process hangs rather than crashes, you can't use `gdb -ex run -ex bt` because the program never stops. Instead, start it in the background and attach after it reaches its hung state:

```bash
/path/to/binary --arg1 --arg2 &
pid=$!
sleep 5   # Let it reach the hung state
gdb -q -batch \
  -ex 'set pagination off' \
  -ex 'thread apply all bt' \
  -p "$pid" || true
kill -TERM "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
```

**Key insight:** The sleep duration should be long enough for the process to enter the hang, but short enough not to waste time. Adjust based on how quickly the bug manifests.

**Gotcha:** Don't try `gdb -ex "run &" -ex "shell sleep 5" -ex "interrupt"` — this is unreliable in batch mode. The background-then-attach pattern above is the proven approach from real sessions.

### Conditional Breakpoints on Raw Syscalls

When breakpoints on named libc functions (`sched_yield`, `accept`) don't fire because the code uses raw `syscall()` or inline assembly, break on the `syscall` instruction itself with a register condition:

```bash
timeout 30 gdb -q -batch \
  -ex 'set pagination off' \
  -ex 'set breakpoint pending on' \
  -ex 'break syscall if $rdi==24' \
  -ex 'run' \
  -ex 'bt' \
  -ex 'thread apply all bt' \
  --args /path/to/binary
```

Common x86_64 syscall numbers: `24` = `sched_yield`, `232` = `epoll_wait`, `288` = `accept4`, `202` = `futex`.

### Exit Code Conventions

```
Exit code 139 = SIGSEGV (128 + signal 11)
Exit code 134 = SIGABRT (128 + signal 6)
Exit code 137 = SIGKILL (128 + signal 9)
Exit code 136 = SIGFPE  (128 + signal 8)
```

Unix convention: exit code = 128 + signal number. When you see exit code 139, the process was killed by a segfault.

### Per-Thread Kernel Stacks (No GDB Needed)

When GDB can't attach, `/proc` provides kernel-level stack traces for every thread:

```bash
# Per-thread kernel stacks
for tid in $(ls /proc/$PID/task/); do
  echo "=== Thread $tid ($(cat /proc/$PID/task/$tid/comm 2>/dev/null)) ==="
  cat /proc/$PID/task/$tid/stack 2>/dev/null
  echo
done

# Per-thread current syscall
for tid in $(ls /proc/$PID/task/); do
  printf "TID %s (%s): syscall %s\n" \
    "$tid" \
    "$(cat /proc/$PID/task/$tid/comm 2>/dev/null)" \
    "$(cat /proc/$PID/task/$tid/syscall 2>/dev/null | awk '{print $1}')"
done
```

### Orphan Process Cleanup

Both GDB and target processes can become orphaned after timeout kills. Always include cleanup:

```bash
# After timeout-wrapped GDB sessions
pkill -f "gdb -q --batch" 2>/dev/null || true
pkill -f "gdb -q -batch" 2>/dev/null || true

# The safe pattern: always clean up the target too
kill -TERM "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
```

### Signal Handling in Batch Mode

Configure GDB to stop on specific signals for crash analysis:

```bash
# Catch SIGABRT (Rust panics, C++ abort)
gdb --batch \
  -ex "set pagination off" \
  -ex "handle SIGABRT stop print pass" \
  -ex "run" \
  -ex "bt full" \
  --args /path/to/binary

# For Rust: catch the panic unwind
gdb --batch \
  -ex "break rust_panic" \
  -ex "run" \
  -ex "bt full" \
  --args ./target/debug/binary
```

### Debug vs Release Build Warning

From real sessions: "debug preload does not hang, so this is likely optimization-sensitive." Always reproduce bugs with the **same build profile** (debug/release) that exhibited the issue. Compiler optimizations can eliminate function calls, inline code, and reorder operations.

---

## Iterative GDB-Driven Debugging Workflow

Real sessions reveal this consistent 6-phase loop, often repeated 6-8+ times in a single debugging session:

```
Phase 1: TRIAGE
  → ps aux, top, /proc/PID/stat — identify failure mode
  → ls /proc/PID/task/ | wc -l — thread count
  → ls -la /proc/PID/fd | wc -l — FD count

Phase 2: QUICK SYSCALL PROFILE
  → strace -p $PID -c (3s timeout) — syscall frequency
  → If ptrace blocked: sample /proc/PID/syscall 200x
  → Find the dominant syscall

Phase 3: PER-THREAD ANALYSIS
  → /proc/PID/task/*/stat — per-thread CPU time
  → Identify hottest thread by utime/stime
  → /proc/PID/task/*/stack — kernel stacks

Phase 4: FULL BACKTRACE
  → gdb --batch -ex "thread apply all bt" -p PID
  → If ptrace blocked: run binary directly under GDB
  → Fallback: strace -f -k for symbolized stacks

Phase 5: TARGETED INVESTIGATION
  → Breakpoints on specific functions
  → Conditional breakpoints for raw syscalls
  → ulimit -s 8192 for recursion detection
  → strace -ff for per-thread output

Phase 6: FIX AND VERIFY
  → Make code fix → REBUILD (critical!) → re-run under GDB
  → If new issue found → loop back to Phase 4
  → Continue until clean run
```

**Critical lesson from sessions:** After making code changes, you MUST rebuild before re-running GDB. Debugging a stale binary wastes time and produces confusing results.

---

## Reverse Debugging with rr

`rr` is the single most powerful debugging tool for non-deterministic bugs. It records full program execution (every syscall, signal, scheduling decision) and replays it deterministically, enabling you to go **backwards** from a crash to find the root cause. This is impossible with GDB alone.

### When to Use rr vs GDB

| Scenario | Use | Why |
|----------|-----|-----|
| Crash that reproduces reliably | GDB | Simpler, less overhead |
| Race condition / intermittent bug | rr | Deterministic replay catches it every time |
| Data corruption (who wrote the bad value?) | rr | Reverse watchpoints — the killer feature |
| Production process (can't restart) | GDB attach | rr requires starting under rr |
| Need to vary scheduling to expose races | rr --chaos | Randomizes thread interleaving |
| Heisenbug (disappears under debugger) | rr | Records at near-native speed, replays under debugger |

### The Record-Replay Workflow

```bash
# Step 1: Record (captures EVERYTHING — deterministic replay guaranteed)
rr record ./binary arg1 arg2
# With chaos mode (varies scheduling to expose race conditions):
rr record --chaos ./binary arg1 arg2

# Step 2: Replay (deterministic — same execution every time)
rr replay
# You're now in a GDB session where ALL normal GDB commands work, PLUS:
#   reverse-continue  (rc)  — run backward until breakpoint/watchpoint
#   reverse-step       (rs)  — step one instruction backward
#   reverse-next       (rn)  — step one source line backward
#   reverse-finish     (rf)  — run backward until current function's caller
```

### The Reverse Watchpoint Technique (rr's Killer Feature)

This solves the classic "who corrupted this memory?" problem that is nearly impossible with forward-only debugging:

```bash
# Problem: Memory at address 0xABCD is corrupted when you read it at line 200.
#          Who wrote the bad value? Could be any of 50 threads at any of 1000 code points.

# Step 1: Record the crashing run
rr record ./binary

# Step 2: Replay to the crash point
rr replay \
  -ex "set pagination off" \
  -ex "continue"
# → crash happens, you see the corrupted value

# Step 3: Set a watchpoint on the corrupted address
# watch *(int*)0xABCD

# Step 4: Run BACKWARDS to find who wrote the corruption
# reverse-continue
# → rr runs the entire execution in reverse and stops at the LAST write to 0xABCD

# Step 5: Examine the writer
# bt full → shows the exact code that wrote the bad value
# info locals → shows what value was written and why
# list → shows the source code

# In batch mode:
CRASH_ADDR=0xDEADBEEF  # Replace with actual address from crash
rr replay \
  -ex "set pagination off" \
  -ex "continue" \
  -ex "watch *(int*)$CRASH_ADDR" \
  -ex "reverse-continue" \
  -ex "bt full" \
  -ex "info locals" \
  2>&1 | tee /tmp/rr_reverse.txt
```

### rr Requirements and Limitations

```bash
# Check if rr will work on this machine
rr cpufeatures
# Needs: hardware perf counters (HPC)

# Install
sudo apt-get install -y rr

# Limitations:
# - Doesn't work in most VMs (needs nested virtualization or HPC passthrough)
# - Docker: needs --privileged or --cap-add=SYS_PTRACE --cap-add=SYS_ADMIN
# - Performance: 1.2-5x recording overhead (much less than valgrind)
# - x86/x86_64 only (ARM support experimental)
# - Can't record distributed systems (single machine only)
# - Can't attach to running process (must start under rr)

# Kernel setting that may need adjustment
sudo sysctl kernel.perf_event_paranoid=1  # rr needs ≤ 1
```

### rr + Chaos Mode for Race Condition Hunting

```bash
# Run 10 chaos recordings — each will schedule threads differently
for i in $(seq 1 10); do
  echo "=== Chaos run $i ==="
  timeout 30s rr record --chaos ./binary test_args 2>&1
  if [ $? -ne 0 ]; then
    echo "Bug triggered on chaos run $i!"
    rr replay -ex "bt full" -ex "thread apply all bt" 2>&1 | tee /tmp/chaos_crash_$i.txt
    break
  fi
done
```

---

## Memory Corruption & Sanitizer Integration

Memory corruption bugs (use-after-free, buffer overflow, stack corruption, double-free) are the hardest class of bugs because the crash often happens far from the corruption. Sanitizers catch corruption at the moment it happens, and GDB lets you inspect the full state.

### AddressSanitizer (ASAN) + GDB

ASAN detects: heap-buffer-overflow, stack-buffer-overflow, use-after-free, double-free, memory leaks. The key is making ASAN **abort** so GDB catches it:

```bash
# Rust: Build with ASAN
RUSTFLAGS="-Zsanitizer=address" cargo +nightly build \
  --target x86_64-unknown-linux-gnu 2>&1 | tail -5

# C/C++:
# gcc -fsanitize=address -g -O1 -fno-omit-frame-pointer source.c -o binary

# Run under GDB — ASAN aborts on error, GDB catches the abort
ASAN_OPTIONS="abort_on_error=1:detect_leaks=0:halt_on_error=1:print_scariness=1:fast_unwind_on_fatal=0" \
gdb --batch \
  -ex "set pagination off" \
  -ex "handle SIGABRT stop print" \
  -ex "run" \
  -ex "bt full" \
  -ex "thread apply all bt" \
  -ex "info registers" \
  --args ./target/x86_64-unknown-linux-gnu/debug/binary \
  2>&1 | tee /tmp/asan_gdb.txt
```

**Critical ASAN_OPTIONS explained:**
- `abort_on_error=1` — ASAN calls abort() instead of _exit(), so GDB catches it
- `detect_leaks=0` — Skip leak detection (slow, not what you need for corruption)
- `halt_on_error=1` — Stop at first error instead of continuing
- `print_scariness=1` — Rate how dangerous the bug is (informational)
- `fast_unwind_on_fatal=0` — Slow but more accurate stack traces

### ThreadSanitizer (TSAN) + GDB

TSAN detects data races — two threads accessing the same memory without synchronization where at least one is a write. TSAN output shows TWO stack traces: the two conflicting accesses.

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

# TSAN key options:
# second_deadlock_stack=1 — show both stacks in deadlock reports
# history_size=7 — larger history (0-7, each level doubles memory)
# suppressions=file.txt — suppress known false positives
```

### MemorySanitizer (MSAN) — Uninitialized Memory

MSAN detects reads of uninitialized memory. Requires that ALL code (including libc) is instrumented, which typically means building everything from source. Most practical for C/C++ projects.

```bash
# C/C++ only (Rust doesn't support MSAN directly)
# clang -fsanitize=memory -fno-omit-frame-pointer -g source.c -o binary
MSAN_OPTIONS="abort_on_error=1" \
gdb --batch \
  -ex "handle SIGABRT stop print" \
  -ex "run" \
  -ex "bt full" \
  --args ./binary 2>&1 | tee /tmp/msan_gdb.txt
```

### Manual Memory Corruption Analysis in GDB

When sanitizers aren't available (release build, production binary):

```bash
# Examine the crash point
gdb --batch \
  -ex "set pagination off" \
  -ex "run" \
  -ex "bt full" \
  -ex "info registers" \
  -ex "x/20i \$pc" \
  -ex "x/8gx \$rsp" \
  --args /path/to/binary 2>&1 | tee /tmp/crash.txt

# After examining the crash, look for corruption patterns:

# 1. NULL dereference: rax=0 and instruction reads from (%rax)
#    → Something returned NULL that shouldn't have (failed allocation, missing init)

# 2. Use-after-free: Address looks valid but content is garbage
#    x/4gx $rax  → shows freed heap patterns (glibc uses fd/bk pointers)
#    Freed chunk: 0x0000000000000000 0x0000000000000041  (size=0x41, freed)
#                 0x00007f8a4c3e0010 0x00007f8a4c3e0010  (fd/bk point to freelist)

# 3. Stack overflow: rsp is below the stack mapping
#    cat /proc/$PID/maps | grep stack
#    Compare rsp value — if below the stack region, stack overflow

# 4. Heap buffer overflow: writing past the end of a malloc'd buffer
#    Often corrupts the next chunk's metadata, causing crash in free() later
#    Signature: crash in __GI___libc_free or malloc_consolidate

# 5. Double free: crash in free() with corrupted freelist
#    glibc reports: "double free or corruption (fasttop)" or similar

# 6. Stack buffer overflow (canary detected):
#    Crash in __stack_chk_fail
#    → A buffer on the stack was overwritten past its boundary, clobbering the canary
```

---

## Hardware Watchpoints & Data Corruption

Hardware watchpoints use CPU debug registers to trigger when a memory location is read or written. They have zero overhead (no instruction-level stepping) and catch the exact moment data changes. x86_64 has 4 hardware watchpoint registers, so you can watch up to 4 addresses simultaneously.

### Setting Watchpoints in Batch Mode

```bash
# Watch a specific address for writes
gdb --batch \
  -ex "set pagination off" \
  -ex "watch *(int*)0x7ffff7dd1234" \
  -ex "continue" \
  -ex "bt full" \
  -ex "info locals" \
  -p $PID 2>&1 | tee /tmp/watchpoint.txt

# Watch a global variable by name
gdb --batch \
  -ex "watch my_global_counter" \
  -ex "continue" \
  -ex "bt full" \
  --args ./binary 2>&1

# Read watchpoint (trigger on reads, not just writes)
gdb --batch \
  -ex "rwatch *(int*)0xADDRESS" \
  -ex "continue" \
  -ex "bt full" \
  -p $PID 2>&1

# Access watchpoint (trigger on both reads and writes)
gdb --batch \
  -ex "awatch *(char[16]*)0xADDRESS" \
  -ex "continue" \
  -ex "bt full" \
  -p $PID 2>&1
```

### Watchpoint Strategies for Corruption Bugs

```bash
# Strategy 1: Watch the corrupted field directly
# If a struct field is being corrupted, watch that specific offset:
# struct Foo { int a; int b; char *c; }  ← c is being corrupted
# If foo is at 0x5555000, c is at offset 8 (a=4 + b=4, 8-byte aligned already)
gdb --batch \
  -ex "watch *(char**)0x555500000008" \
  -ex "continue" \
  -ex "bt full" \
  --args ./binary 2>&1

# Strategy 2: Watch a sentinel value
# Place a known value (0xDEADBEEF) at a location and watch for changes:
gdb --batch \
  -ex "set *(int*)0xADDRESS = 0xDEADBEEF" \
  -ex "watch *(int*)0xADDRESS" \
  -ex "continue" \
  -ex "bt full" \
  -p $PID 2>&1

# Strategy 3: Watch malloc chunk metadata
# If crashes happen in free()/malloc(), the heap metadata is corrupted.
# Watch the chunk header (16 bytes before the user pointer):
gdb --batch \
  -ex "watch *(long*)(0xUSER_PTR - 16)" \
  -ex "continue" \
  -ex "bt full" \
  --args ./binary 2>&1

# Hardware watchpoint limits:
# x86_64: 4 watchpoints, each up to 8 bytes wide
# "Too many hardware watchpoints" → GDB falls back to software (VERY slow)
# Check: info watchpoints — shows hw vs sw type
```

---

## Lock Graph Construction & Deadlock Proof

A deadlock exists when there's a cycle in the lock-wait graph. This section shows how to formally prove a deadlock from GDB output, not just guess.

### The Lock Graph Algorithm

```
Step 1: Identify all threads blocked in lock acquisition
        → Threads in __lll_lock_wait, futex_wait, pthread_mutex_lock
        → Record: {thread_id, mutex_address_being_waited_on}

Step 2: For each blocked thread, extract the mutex address
        → Look at pthread_mutex_lock(mutex=0xADDRESS) argument
        → Or examine rdi register in futex frame (first arg = futex address)

Step 3: Identify which thread holds each contested mutex
        → For non-blocked threads: check their call chain for lock acquisitions
        → Use: print *(pthread_mutex_t*)0xADDRESS → __data.__owner = TID
        → The __owner field directly tells you which thread holds the mutex

Step 4: Build directed graph
        → Edge: T_blocked --waits_for--> Mutex_A --held_by--> T_holder

Step 5: Cycle detection
        → If T1 waits for M1 held by T2, AND T2 waits for M2 held by T1
        → That's a cycle → DEADLOCK PROVEN
```

### Practical Lock Graph Construction

```bash
# Step 1: Capture full state
gdb --batch \
  -ex "set pagination off" \
  -ex "set print pretty on" \
  -ex "thread apply all bt full" \
  -p $PID 2>&1 | tee /tmp/deadlock_bt.txt

# Step 2: Find blocked threads and their mutex addresses
grep -B15 '__lll_lock_wait\|futex_wait_queue' /tmp/deadlock_bt.txt | \
  grep -E 'Thread|pthread_mutex_lock.*mutex='

# Example output:
# Thread 3 (Thread 0x7f... (LWP 1234)):
#   #1  pthread_mutex_lock (mutex=0x5555AABB0010)
# Thread 5 (Thread 0x7f... (LWP 1236)):
#   #1  pthread_mutex_lock (mutex=0x5555AABB0060)

# Step 3: Who holds each mutex? (the __owner field is the TID of the holder)
gdb --batch \
  -ex "set pagination off" \
  -ex "print ((pthread_mutex_t*)0x5555AABB0010)->__data.__owner" \
  -ex "print ((pthread_mutex_t*)0x5555AABB0060)->__data.__owner" \
  -p $PID 2>&1

# Example output:
# $1 = 1236    ← mutex 0x0010 is held by TID 1236 (Thread 5)
# $2 = 1234    ← mutex 0x0060 is held by TID 1234 (Thread 3)

# Step 4: Build the graph
# Thread 3 (TID 1234) waits for mutex 0x0010, held by Thread 5 (TID 1236)
# Thread 5 (TID 1236) waits for mutex 0x0060, held by Thread 3 (TID 1234)
# → CYCLE: T3 → M_0010 → T5 → M_0060 → T3
# → DEADLOCK PROVEN

# Step 5: Where in the code did each thread acquire its lock?
# Look at the full backtrace for each thread — the frames ABOVE the futex_wait
# show the call chain that led to the lock acquisition
```

### Common Deadlock Patterns

| Pattern | Signature | Root Cause |
|---------|-----------|------------|
| Classic AB-BA | Two threads, each waiting for the other's lock | Lock ordering violation |
| Self-deadlock | One thread, same mutex address in two frames | Non-recursive mutex re-locked |
| Reader-upgrade | rwlock: rdlock held, wrlock requested, same thread | Can't upgrade read to write |
| Condvar deadlock | Thread in pthread_cond_wait but waker thread is blocked | Waker needs lock held by waiter |
| Channel deadlock (Rust) | All senders waiting for receivers, all receivers waiting for senders | Circular channel dependency |

---

## Async Runtime Debugging (Tokio/async-std)

Async Rust is notoriously hard to debug because the generated state machines are opaque, tasks can be scattered across threads, and traditional thread-level debugging doesn't map well to the logical task model.

### Understanding What GDB Sees in Async Rust

```
Source code:           async fn handle_request(req: Request) -> Response {
                         let data = fetch_data(&req).await;   // await point 1
                         let result = process(data).await;     // await point 2
                         respond(result)
                       }

What the compiler generates:  enum HandleRequest {
                                State0 { req: Request },
                                State1 { data_future: FetchDataFuture, req: Request },
                                State2 { process_future: ProcessFuture },
                              }

What GDB shows:        <my_module::handle_request::{{closure}} as core::future::future::Future>::poll
                       This is the generated Future::poll() for handle_request
                       The actual state (State0/1/2) determines which .await the task is at
```

### Tokio Thread Model

```bash
# Tokio creates several thread types:
ps -Lp $PID -o tid,comm --no-headers
# tokio-runtime-w  — executor threads (run the event loop, poll futures)
# blocking-0       — blocking thread pool (spawn_blocking tasks)
# signal-hook      — signal handler thread
# main             — the main thread

# Healthy state: all tokio-runtime-worker threads in epoll_wait (waiting for events)
# Unhealthy states:
#   - All workers in epoll_wait BUT requests are timing out
#     → Tasks exist but aren't being polled (task starvation)
#   - One worker NOT in epoll_wait, burning CPU
#     → A task is blocking the runtime thread (accidental std::thread::sleep,
#       synchronous I/O, CPU-heavy computation on runtime thread)
#   - All workers in futex_wait
#     → Runtime itself is stuck (mutex contention in scheduler)
```

### Diagnosing Task Starvation

Task starvation happens when a single task monopolizes a runtime thread, preventing other tasks from being polled. This is the most common Tokio bug.

```bash
# Step 1: Confirm all workers are busy (not in epoll_wait)
gdb --batch -ex "thread apply all bt 5" -p $PID 2>&1 | \
  grep -A5 'tokio-runtime' | grep -v epoll_wait
# If workers are NOT in epoll_wait, they're executing tasks

# Step 2: What is the blocking task doing?
gdb --batch -ex "thread apply all bt full" -p $PID 2>&1 | \
  grep -B3 -A20 'tokio-runtime-w' | grep -v epoll_wait
# Look for:
#   - std::thread::sleep (should use tokio::time::sleep instead)
#   - std::io::Read/Write (should use tokio::io instead)
#   - reqwest::blocking (should use reqwest::Client async)
#   - sqlite::Connection (synchronous SQLite — wrap in spawn_blocking)
#   - Deep computation without yield_now()

# Step 3: Confirm with strace
HOT_TID=$(ps -Lp $PID -o tid,pcpu --sort=-pcpu --no-headers | head -1 | awk '{print $1}')
timeout 3s strace -tt -T -p $HOT_TID 2>&1 | head -30
# If you see nanosleep, read/write on regular files, etc. → blocking the runtime
```

### Diagnosing Async Deadlocks

Async deadlocks look different from thread deadlocks. Instead of threads blocked on futex, you see threads idle (epoll_wait) while tasks are pending but never scheduled:

```bash
# Symptom: all workers in epoll_wait, but requests are pending
# Root causes:
# 1. Mutex held across .await (task yields while holding lock, never gets re-polled
#    because the next task also needs the lock)
# 2. Channel full: sender .awaits on full channel, receiver .awaits on empty channel
#    (circular dependency between tasks)
# 3. JoinHandle deadlock: task A .awaits task B's JoinHandle, task B .awaits task A's

# Diagnosis approach:
# Since the runtime IS idle (epoll_wait), the problem is that tasks can't make progress
# You need to examine what tasks exist and what they're waiting for

# Check Tokio's internal task count (if console subscriber is enabled)
# Otherwise, look at the state of shared resources:
gdb --batch \
  -ex "set pagination off" \
  -ex "thread apply all bt full" \
  -p $PID 2>&1 | grep -i 'mutex\|rwlock\|channel\|mpsc\|oneshot\|watch'
# If you see Mutex or RwLock guard values in the local variables → held across await
```

---

## Container & Namespace Debugging

Debugging processes inside containers introduces PID namespace translation, capability restrictions, and filesystem isolation challenges.

### Docker Debugging

```bash
# Method 1: Add capabilities at container start
docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined ...

# Method 2: nsenter into existing container (from host)
CONTAINER_PID=$(docker inspect --format '{{.State.Pid}}' $CONTAINER_NAME)
# Enter the container's namespaces with host tools
sudo nsenter -t $CONTAINER_PID -m -u -i -n -p -- gdb --batch \
  -ex "thread apply all bt" -p 1 2>&1
# Note: PID 1 inside the container is the main process

# Method 3: docker exec with GDB installed in container
docker exec -it $CONTAINER_NAME bash -c \
  "apt-get update && apt-get install -y gdb && gdb --batch -ex 'thread apply all bt' -p 1"

# Method 4: Copy binary out, analyze separately
docker cp $CONTAINER_NAME:/path/to/binary /tmp/
docker cp $CONTAINER_NAME:/proc/1/maps /tmp/container_maps
# Offline analysis with addr2line, objdump, etc.
```

### PID Namespace Translation

```bash
# Inside a container, PID 1 is your process. On the host, it's a different PID.
# Translation:

# From host → container PID
docker inspect --format '{{.State.Pid}}' $CONTAINER_NAME
# This gives the host-side PID

# From container PID → host PID
grep NSpid /proc/$HOST_PID/status
# NSpid: 12345    1
#        ^host    ^container
# The process is PID 12345 on host, PID 1 in container

# GDB on host using host PID (no nsenter needed if ptrace_scope=0)
sudo gdb --batch -ex "thread apply all bt" -p $HOST_PID 2>&1
```

### Kubernetes Debugging

```bash
# Exec into the pod
kubectl exec -it $POD_NAME -- bash

# If GDB isn't installed, use an ephemeral debug container (k8s 1.23+)
kubectl debug -it $POD_NAME --image=ubuntu --target=$CONTAINER_NAME -- bash
apt-get update && apt-get install -y gdb strace procps
# The debug container shares the process namespace

# If securityContext doesn't allow ptrace
# Add to pod spec:
# spec:
#   containers:
#   - name: myapp
#     securityContext:
#       capabilities:
#         add: ["SYS_PTRACE"]
#   shareProcessNamespace: true  # needed for debug container to see app PIDs
```

---

## Multi-Process Debugging (Forks & Daemons)

### Following Forks

When a process forks, GDB by default follows the parent. For debugging the child (e.g., a daemon's worker process):

```bash
# Follow child after fork
gdb --batch \
  -ex "set follow-fork-mode child" \
  -ex "set detach-on-fork off" \
  -ex "run" \
  -ex "bt full" \
  --args ./daemon_binary 2>&1

# Follow parent (default, but explicit)
gdb --batch \
  -ex "set follow-fork-mode parent" \
  -ex "run" \
  -ex "bt full" \
  --args ./binary 2>&1

# Debug BOTH parent and child (each in separate inferior)
gdb --batch \
  -ex "set detach-on-fork off" \
  -ex "run" \
  -ex "info inferiors" \
  -ex "inferior 1" -ex "thread apply all bt" \
  -ex "inferior 2" -ex "thread apply all bt" \
  --args ./forking_binary 2>&1
```

### Debugging Daemonized Processes

Daemons typically double-fork and detach from the terminal. To debug:

```bash
# Method 1: Prevent daemonization (if the binary supports it)
./daemon --foreground --no-daemon

# Method 2: Attach to the final daemon process
./daemon  # let it daemonize
PID=$(pgrep -x daemon_name)
gdb --batch -ex "thread apply all bt" -p $PID 2>&1

# Method 3: Follow the fork chain
gdb --batch \
  -ex "set follow-fork-mode child" \
  -ex "set detach-on-fork off" \
  -ex "catch fork" \
  -ex "run" \
  -ex "continue" \
  -ex "continue" \
  -ex "bt full" \
  --args ./daemon 2>&1
# Each "continue" follows through one fork in the chain
```

---

## Race Condition Methodology

Race conditions are the hardest bugs because they depend on timing. A systematic approach is essential.

### The Systematic Approach

```
1. REPRODUCE: Can you trigger the race reliably?
   → If intermittent: use rr --chaos (varies scheduling)
   → If load-dependent: increase concurrency (more threads, more requests)
   → If timing-dependent: add artificial delays (sleep in strategic locations)

2. DETECT: What tool catches it?
   → Data race: TSAN (ThreadSanitizer)
   → Memory corruption from race: ASAN + high concurrency
   → Deadlock from race: GDB attach when stuck + lock graph
   → Logic error from race: rr record + reverse debugging

3. LOCALIZE: Where exactly is the unsynchronized access?
   → TSAN output shows both conflicting accesses with stack traces
   → rr reverse-continue from the corruption to the write
   → bpftrace to count function calls without stopping the process

4. FIX: What synchronization is needed?
   → Mutex for exclusive access
   → RwLock for read-heavy patterns
   → Atomic for simple counters/flags
   → Channel for producer-consumer
   → Arc<T> for shared ownership in Rust

5. VERIFY: Is the fix correct?
   → Run TSAN again (should be clean)
   → Run rr --chaos multiple times
   → Stress test with high concurrency
```

### TSAN Data Race Detection

```bash
# Rust
RUSTFLAGS="-Zsanitizer=thread" cargo +nightly build \
  --target x86_64-unknown-linux-gnu

# Run with high thread count to increase race likelihood
TSAN_OPTIONS="abort_on_error=1:second_deadlock_stack=1:history_size=7" \
  ./target/x86_64-unknown-linux-gnu/debug/binary \
  --threads 16 --requests 10000 2>&1 | tee /tmp/tsan.txt

# TSAN output format:
# WARNING: ThreadSanitizer: data race
#   Write of size 8 at 0xADDRESS by thread T3:
#     #0 function_a source.rs:42
#     #1 ...
#   Previous read of size 8 at 0xADDRESS by thread T7:
#     #0 function_b source.rs:87
#     #1 ...
# → Two threads accessing the same memory unsafely
```

### Strategic Delay Injection (When All Else Fails)

When you suspect a race but can't reproduce it:

```bash
# Add usleep() calls at strategic points to widen the race window
# Then run under GDB or TSAN

# In Rust: std::thread::sleep(Duration::from_millis(10));
# In C: usleep(10000);

# Place delays:
# 1. After acquiring a resource but before using it
# 2. Between checking a condition and acting on it (TOCTOU)
# 3. Between allocating and initializing
# 4. In signal handlers (extends the race window)

# After reproducing with delays:
# - Record with rr for deterministic replay
# - Remove delays and verify with TSAN
```

---

## GDB Python Scripting for Agents

GDB's Python API enables automated analysis that goes far beyond what `-ex` commands can do. Write scripts to `/tmp/` and source them in batch mode.

### Thread Categorization Script

```bash
cat > /tmp/categorize_threads.py << 'PYEOF'
import gdb

categories = {
    'epoll_wait': 'IO_WAIT', 'poll_schedule': 'IO_WAIT',
    'futex_wait': 'MUTEX_WAIT', '__lll_lock_wait': 'MUTEX_WAIT',
    'pthread_cond_wait': 'CONDVAR_WAIT', 'pthread_cond_timedwait': 'CONDVAR_WAIT',
    'accept4': 'ACCEPTING', 'accept': 'ACCEPTING',
    'recv': 'RECEIVING', 'recvfrom': 'RECEIVING', 'recvmsg': 'RECEIVING',
    'send': 'SENDING', 'sendto': 'SENDING', 'sendmsg': 'SENDING',
    'nanosleep': 'SLEEPING', 'clock_nanosleep': 'SLEEPING',
    'read': 'READING', 'write': 'WRITING',
}

results = {}
for thread in gdb.selected_inferior().threads():
    thread.switch()
    frame = gdb.newest_frame()
    cat = 'RUNNING'
    f = frame
    depth = 0
    while f and depth < 20:
        name = f.name() or ''
        for pattern, category in categories.items():
            if pattern in name:
                cat = category
                break
        if cat != 'RUNNING':
            break
        f = f.older()
        depth += 1

    tid = thread.ptid[1]
    try:
        tname = open(f'/proc/{gdb.selected_inferior().pid}/task/{tid}/comm').read().strip()
    except:
        tname = '?'

    results.setdefault(cat, []).append(f"  Thread {thread.num} (TID {tid}, {tname}): {frame.name() or '??'}")

print("\n=== THREAD CATEGORIES ===")
for cat in ['RUNNING', 'MUTEX_WAIT', 'CONDVAR_WAIT', 'IO_WAIT', 'ACCEPTING',
            'RECEIVING', 'SENDING', 'READING', 'WRITING', 'SLEEPING']:
    threads = results.get(cat, [])
    if threads:
        print(f"\n{cat} ({len(threads)}):")
        for t in threads:
            print(t)

total = sum(len(v) for v in results.values())
print(f"\nTotal: {total} | Active: {len(results.get('RUNNING', []))} | "
      f"Waiting: {total - len(results.get('RUNNING', []))}")
PYEOF

gdb --batch \
  -ex "set pagination off" \
  -ex "source /tmp/categorize_threads.py" \
  -p $PID 2>&1 | tee /tmp/thread_categories.txt
```

### Mutex Ownership Inspector

```bash
cat > /tmp/mutex_owners.py << 'PYEOF'
import gdb
import re

print("=== MUTEX OWNERSHIP ANALYSIS ===")

# Find all threads blocked on mutexes
for thread in gdb.selected_inferior().threads():
    thread.switch()
    frame = gdb.newest_frame()
    f = frame
    depth = 0
    while f and depth < 15:
        name = f.name() or ''
        if 'pthread_mutex_lock' in name:
            try:
                f.select()
                mutex_val = gdb.parse_and_eval('mutex')
                mutex_addr = int(mutex_val)
                # Read __owner field from pthread_mutex_t
                owner_expr = f'((pthread_mutex_t*){mutex_addr})->__data.__owner'
                owner = int(gdb.parse_and_eval(owner_expr))
                print(f"Thread {thread.num} (TID {thread.ptid[1]}) "
                      f"WAITING for mutex 0x{mutex_addr:x}, held by TID {owner}")
            except Exception as e:
                print(f"Thread {thread.num}: mutex analysis failed: {e}")
            break
        f = f.older()
        depth += 1

print("\nTo prove deadlock: check if any holder is also waiting for a mutex held by a waiter.")
PYEOF

gdb --batch \
  -ex "set pagination off" \
  -ex "source /tmp/mutex_owners.py" \
  -p $PID 2>&1 | tee /tmp/mutex_analysis.txt
```

### Custom Pretty-Printer for Rust Types

```bash
cat > /tmp/rust_helpers.py << 'PYEOF'
import gdb

class RustVecPrinter:
    """Pretty-print a Rust Vec<T>"""
    def __init__(self, val):
        self.val = val
    def to_string(self):
        try:
            buf = self.val['buf']['inner']['ptr']['pointer']['pointer']
            length = int(self.val['len'])
            cap = int(self.val['buf']['inner']['cap']['0'])
            return f"Vec(len={length}, cap={cap}, ptr={buf})"
        except:
            return str(self.val)

class RustStringPrinter:
    """Pretty-print a Rust String"""
    def __init__(self, val):
        self.val = val
    def to_string(self):
        try:
            vec = self.val['vec']
            buf = vec['buf']['inner']['ptr']['pointer']['pointer']
            length = int(vec['len'])
            # Read the actual string bytes
            data = gdb.selected_inferior().read_memory(int(buf), min(length, 200))
            return f'String("{data.tobytes().decode("utf-8", errors="replace")}")'
        except:
            return str(self.val)

def rust_lookup(val):
    t = str(val.type)
    if 'alloc::vec::Vec<' in t:
        return RustVecPrinter(val)
    if t == 'alloc::string::String':
        return RustStringPrinter(val)
    return None

gdb.pretty_printers.append(rust_lookup)
print("Rust pretty-printers loaded (Vec, String)")
PYEOF

# Use with:
gdb --batch \
  -ex "source /tmp/rust_helpers.py" \
  -ex "thread apply all bt full" \
  -p $PID 2>&1
```

---

## Core Dump Forensics

Core dumps capture the complete process state at the moment of death. Deep analysis goes far beyond `bt full`.

### Core Dump Setup

```bash
# Enable core dumps (MUST set before the crash)
ulimit -c unlimited

# Set a useful naming pattern
echo '/tmp/core.%p.%e.%t' | sudo tee /proc/sys/kernel/core_pattern
# %p = PID, %e = executable name, %t = timestamp

# For setuid binaries
sudo sysctl fs.suid_dumpable=2

# Verify
cat /proc/sys/kernel/core_pattern
ulimit -c  # should show "unlimited"

# systemd-coredump (if your system uses it)
coredumpctl list                    # list all recent core dumps
coredumpctl info PID                # details about a specific crash
coredumpctl debug PID               # open in GDB directly
```

### Deep Core Dump Analysis

```bash
BINARY=/path/to/binary
CORE=/tmp/core.12345.binary.1709000000

# === COMPREHENSIVE ANALYSIS ===
gdb --batch \
  -ex "set pagination off" \
  -ex "set print pretty on" \
  \
  -ex "echo === CRASH SIGNAL ===\n" \
  -ex "print \$_siginfo" \
  -ex "print (void*)\$_siginfo._sifields._sigfault.si_addr" \
  \
  -ex "echo === BACKTRACE ===\n" \
  -ex "bt full" \
  \
  -ex "echo === ALL THREADS ===\n" \
  -ex "thread apply all bt" \
  \
  -ex "echo === REGISTERS ===\n" \
  -ex "info registers" \
  \
  -ex "echo === DISASSEMBLY AT CRASH ===\n" \
  -ex "x/10i \$pc" \
  \
  -ex "echo === MEMORY AROUND FAULT ADDRESS ===\n" \
  -ex "x/16gx \$_siginfo._sifields._sigfault.si_addr" \
  \
  -ex "echo === STACK DUMP ===\n" \
  -ex "x/32gx \$rsp" \
  \
  -ex "echo === ADDRESS SPACE ===\n" \
  -ex "info proc mappings" \
  \
  -ex "echo === SHARED LIBRARIES ===\n" \
  -ex "info sharedlibrary" \
  \
  "$BINARY" "$CORE" 2>&1 | tee /tmp/core_analysis.txt
```

### Signal Frame Interpretation

```bash
# The $_siginfo structure tells you exactly what happened:

# SIGSEGV (signal 11):
#   si_code = 1 (SEGV_MAPERR) → Access to unmapped memory (NULL deref, wild pointer)
#   si_code = 2 (SEGV_ACCERR) → Access permission denied (write to read-only, execute non-exec)
#   si_addr = the exact faulting address

# SIGBUS (signal 7):
#   si_code = 1 (BUS_ADRALN) → Unaligned access (rare on x86, common on ARM)
#   si_code = 2 (BUS_ADRERR) → Non-existent physical address

# SIGABRT (signal 6):
#   Usually from abort() — check if ASAN, malloc corruption, or assert() triggered it
#   Look for: __GI_abort → __assert_fail → your_function

# SIGFPE (signal 8):
#   si_code = 1 (FPE_INTDIV) → Integer division by zero
#   si_code = 7 (FPE_FLTINV) → Invalid floating point operation (NaN)

# Quick signal decode:
gdb --batch \
  -ex "print \$_siginfo.si_signo" \
  -ex "print \$_siginfo.si_code" \
  -ex "print (void*)\$_siginfo._sifields._sigfault.si_addr" \
  "$BINARY" "$CORE" 2>&1
```

### Heap State Examination

```bash
# glibc malloc uses chunk headers: [prev_size | size+flags | user_data...]
# The 16 bytes BEFORE the user pointer are the chunk header

gdb --batch \
  -ex "set pagination off" \
  \
  -ex "echo === HEAP INFO ===\n" \
  -ex "info proc mappings" \
  \
  -ex "echo === EXAMINE SUSPICIOUS POINTER ===\n" \
  -ex "x/4gx (0xUSER_PTR - 16)" \
  \
  "$BINARY" "$CORE" 2>&1

# Chunk header interpretation:
# [prev_size] [size | A M P]
# size: includes header (so real usable size = size - 16)
# A (bit 2): belongs to non-main arena
# M (bit 1): mmap'd chunk (large allocation)
# P (bit 0): previous chunk is in use (1) or free (0)
#
# Free chunk: [prev_size] [size] [fd] [bk]
#   fd/bk = forward/backward free list pointers
#   If fd/bk point to clearly invalid addresses → heap corruption

# Common corruption patterns:
# 1. Double free: chunk already in freelist, fd/bk are valid freelist pointers
#    but trying to free it again corrupts the freelist
# 2. Heap buffer overflow: user writes past chunk end, corrupting next chunk's header
#    → crash in free() or malloc() when traversing corrupted chunk list
# 3. Use-after-free: chunk freed, user data overwritten with fd/bk pointers
#    → program reads freelist pointers thinking they're user data
```

---

## Anti-Patterns (Never Do)

| Bad | Why | Do Instead |
|-----|-----|-----------|
| `gdb -p PID` interactively as agent | Blocks your session forever | Always use `--batch` |
| Attach without checking ptrace_scope | Wastes time on "Operation not permitted" | Check & relax first |
| Kill process to "debug" it | Destroys the evidence | Attach GDB, capture state, THEN decide |
| `strace -f -e all` on production | Can slow process 100x | Use `-e trace=network,futex` selectively |
| Attach to wrong PID | Disrupts innocent process | Triple-check PID matches target |
| Forget to detach | Leaves process frozen | Use `--batch` or explicit `detach` |
| Skip thread analysis | Miss the hot thread | Always `ps -Lp` first |
| Ignore socket state | Miss network-level evidence | Always `ss` for network services |
| `LD_PRELOAD=... gdb` in shell env | GDB loads the preload, may deadlock | Use `set env LD_PRELOAD` inside GDB |
| Debug with wrong build profile | Optimization-sensitive bugs vanish | Match debug/release to the failing build |
| GDB stale binary after rebuild | Debugging old code, wasting time | Always rebuild before re-running GDB |
| Skip `timeout` wrapper | GDB hangs forever on stuck process | Always `timeout 30s gdb ...` |
| Use software watchpoints | 1000x slower than hardware | Use `watch` (hw default), check `info watchpoints` |
| Guess at deadlock | Wastes time on wrong theory | Build lock graph, read `__owner` field, prove the cycle |
| Block Tokio runtime thread | Starves all other tasks | Move sync I/O to `spawn_blocking` |
| Use `gdb -ex "run &"` for hangs | Unreliable in batch mode | Background process, sleep, then attach |
| `rr record` in a VM | Usually fails (no HPC) | Check `rr cpufeatures` first |
| Debug race without TSAN/rr | Non-deterministic, wastes time | Use TSAN for detection, rr for reproduction |
| Hold mutex across .await | Async deadlock risk | Drop guard before .await, restructure code |

---

## Checklist (Before Debugging)

- [ ] Target PID confirmed with `ps -p $PID -o pid,comm,args`
- [ ] ptrace_scope checked (`cat /proc/sys/kernel/yama/ptrace_scope`) and relaxed if needed
- [ ] Thread-level `ps -Lp` captured — identified hot threads
- [ ] Socket state captured with `ss` (if network service)
- [ ] Binary location verified (`readlink -f /proc/$PID/exe`) — not `(deleted)`
- [ ] GDB `--batch` mode used (never interactive)
- [ ] `timeout` wrapper around GDB command
- [ ] Output saved to file with `tee /tmp/gdb_bt_$PID.txt`
- [ ] Build profile matches (debug/release) the failing execution
- [ ] For race conditions: considered TSAN or rr before GDB
- [ ] For memory corruption: considered ASAN before manual analysis
- [ ] For containers: verified SYS_PTRACE capability
- [ ] Cleanup plan for orphaned GDB/target processes

---

## Bug Class Decision Tree

```
What symptom?
├── Process crashed (segfault, abort, signal)
│   ├── Reproducible? → GDB run with crash capture
│   │   ├── Memory corruption? → Rebuild with ASAN, run under GDB
│   │   └── Signal analysis → examine $_siginfo, registers, disassembly
│   └── Intermittent? → rr record --chaos, replay to crash
│
├── Process stuck (100% CPU, not responding)
│   ├── ps -Lp → identify hot thread
│   ├── strace hot TID → which syscall is spinning?
│   ├── GDB bt → where in the code?
│   └── Common: accept4/EAGAIN loop, futex spin, infinite recursion
│
├── Process stuck (0% CPU, not responding)
│   ├── GDB bt full → all threads in futex_wait/lll_lock_wait?
│   ├── Build lock graph → prove deadlock cycle
│   ├── Async deadlock? → Workers in epoll_wait but tasks pending
│   └── Channel deadlock? → All senders/receivers blocked
│
├── Process slow
│   ├── perf record → where is time spent?
│   ├── ss → socket queue buildup?
│   ├── Thread contention? → high involuntary context switches
│   └── NUMA misplacement? → numastat -p $PID
│
├── Data corruption (wrong results, garbled output)
│   ├── Data race? → Rebuild with TSAN
│   ├── Memory corruption? → Rebuild with ASAN
│   ├── Who corrupted this memory? → rr reverse watchpoint
│   └── Specific field? → Hardware watchpoint on the address
│
└── Intermittent/heisenbug
    ├── Timing dependent? → rr --chaos (varies scheduling)
    ├── Load dependent? → Increase concurrency, run TSAN
    ├── Disappears under debugger? → rr (near-native recording speed)
    └── Strategy: TSAN for detection, rr for reproduction, then GDB for analysis
```

---

## References

| Need | Reference |
|------|-----------|
| Complete technique catalog (2200+ lines): disassembly, lock analysis, async internals, stripped binaries, core dump forensics | [TECHNIQUES.md](references/TECHNIQUES.md) |
| 20 batch mode recipes: ASAN/TSAN, rr, Python scripts, valgrind, git bisect, watchpoints, thread categorization | [BATCH-MODE-RECIPES.md](references/BATCH-MODE-RECIPES.md) |
| Complementary tools (650+ lines): rr, bpftrace, ltrace, SystemTap, strace deep dive, perf, /proc, ss, addr2line/objdump | [COMPLEMENTARY-TOOLS.md](references/COMPLEMENTARY-TOOLS.md) |
| Advanced debugging (3100+ lines): GDB Python API deep dive, hardware watchpoints, remote debugging, multi-process, JIT, DWARF | [ADVANCED-DEBUGGING.md](references/ADVANCED-DEBUGGING.md) |
| Related skills | `system-performance-remediation`, `extreme-software-optimization` |
