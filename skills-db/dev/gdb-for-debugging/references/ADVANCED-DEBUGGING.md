# Advanced Debugging Techniques

Deep-dive reference for expert-level debugging with GDB, rr, sanitizers, and
related tooling. Every section is written for autonomous AI coding agents that
need to diagnose real failures without human hand-holding.

---

## 1. Reverse Debugging with rr

### What rr Is

rr is a record/replay debugger created by Mozilla. It records the **complete
execution** of a program -- every syscall return value, every signal, every
scheduling decision -- into a trace directory. You can then replay that trace
inside a GDB-compatible interface and **step backwards** through execution.
Because the replay is deterministic, the exact same sequence of events happens
every time you replay, which makes it possible to debug race conditions,
heisenbugs, and any other timing-dependent failure.

rr is not a sampling profiler or an approximation. It captures the full causal
history of the process.

### Installation

```bash
# Ubuntu/Debian
sudo apt install rr

# Fedora
sudo dnf install rr

# From source (latest features, needed for newer kernels)
git clone https://github.com/rr-debugger/rr.git
cd rr
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
sudo make install
```

Verify the installation and check for hardware support:

```bash
rr --version
# If this fails with "perf_event_open failed", you need:
echo 1 | sudo tee /proc/sys/kernel/perf_event_paranoid
# Or permanently in /etc/sysctl.d/10-rr.conf:
# kernel.perf_event_paranoid = 1
```

### Recording a Session

```bash
# Basic recording
rr record ./binary arg1 arg2

# Record with chaos mode -- intentionally varies scheduling to expose races
rr record --chaos ./binary arg1 arg2

# Record with environment variables
rr record env RUST_BACKTRACE=1 ./binary

# Record a test suite (each test process is recorded separately)
rr record cargo test --release

# Record with output capture for agent analysis
rr record --chaos ./binary 2>&1 | tee /tmp/rr_record.log
echo "rr exit code: $?" >> /tmp/rr_record.log
```

The trace is stored in `~/.local/share/rr/` by default. Each recording gets its
own directory named `binary-N` where N is an incrementing counter.

**Chaos mode** (`--chaos`) is particularly valuable for agents. It intentionally
introduces scheduling perturbations that make race conditions manifest more
reliably. If you suspect a race condition, always record with `--chaos` and run
the recording multiple times. A failure that occurs only 1% of the time under
normal execution may occur 30-50% of the time under chaos mode.

### Replaying a Session

```bash
# Replay most recent recording (opens GDB-compatible interface)
rr replay

# Replay a specific trace
rr replay ~/.local/share/rr/binary-5

# Replay with GDB commands (batch mode for agents)
rr replay -- -ex "bt full" -ex "thread apply all bt" 2>&1 | tee /tmp/rr_replay.log

# Replay and run to crash, then get full state
rr replay -ex "continue" -ex "bt full" -ex "info registers" -ex "info locals" \
    -ex "thread apply all bt full" -ex "quit" 2>&1 | tee /tmp/rr_replay.log
```

### Key Reverse Execution Commands

Once inside an rr replay session (or via `-ex` flags), all standard GDB
commands work, plus:

| Command | Effect |
|---------|--------|
| `reverse-continue` (`rc`) | Run backwards until a breakpoint/watchpoint fires |
| `reverse-step` (`rs`) | Step one source line backwards (into functions) |
| `reverse-next` (`rn`) | Step one source line backwards (over functions) |
| `reverse-finish` | Run backwards until the current function's caller is reached |
| `reverse-stepi` | Step one machine instruction backwards |
| `when` | Show the current event number in the trace |
| `run N` | Jump to event number N (forward or backward) |
| `checkpoint` | Save a named position in the trace |
| `restart N` | Return to checkpoint N |

### When Marks and Navigation

rr's trace is a linear sequence of events. The `when` command shows where you
are:

```
(rr) when
Current event: 15234
```

You can jump to any event:

```
(rr) run 10000
(rr) when
Current event: 10000
```

This is invaluable for binary-searching through a trace. If you know the bug
manifests between events 10000 and 20000, you can jump to 15000 and check
whether the corruption has happened yet, then narrow down further.

### Checkpoints

Checkpoints are like bookmarks in the trace:

```
(rr) checkpoint
Checkpoint 1 at event 15234
(rr) # ... navigate around ...
(rr) restart 1
# Back at event 15234
```

Use checkpoints to mark interesting points: "corruption not yet visible",
"corruption visible", "last known good state".

### Watchpoints with Reverse Execution

This is the killer combination. The workflow for finding memory corruption:

1. Run forward to the crash/corruption point
2. Identify the corrupted memory address
3. Set a hardware watchpoint on that address
4. `reverse-continue` -- rr runs backwards through the trace until something
   **wrote** to that address
5. `bt` shows exactly who corrupted the memory

```
(rr) continue
# ... program crashes with SIGSEGV accessing 0x55a3f000 ...
(rr) # The struct at 0x55a3f000 has a corrupted vtable pointer
(rr) watch *(void**)0x55a3f000
Hardware watchpoint 1: *(void**)0x55a3f000
(rr) reverse-continue
# rr stops at the exact instruction that wrote the bad value
Hardware watchpoint 1: *(void**)0x55a3f000
Old value = 0xdeadbeef
New value = 0x7f3a2b001234   # <-- the correct value, before corruption
(rr) bt
#0  corrupt_function (ptr=0x55a3f000) at bug.c:42
#1  process_request (req=0x55a3e800) at server.c:187
#2  worker_thread (arg=0x0) at server.c:301
```

This is **deterministic**. You can replay this exact sequence as many times as
you need.

### Conditional Reverse Breakpoints

You can reverse-continue until a condition becomes false, which finds exactly
when an invariant broke:

```
(rr) # We know list->size should never exceed list->capacity
(rr) break check_invariant if list->size > list->capacity
(rr) reverse-continue
# Stops at the first point going backwards where the invariant was violated
```

Alternatively, use a watchpoint on the size field and check the condition
manually each time rr stops.

### Full Batch-Mode Recipes for Agents

**Recipe 1: Record and replay to crash with full diagnostics**

```bash
#!/bin/bash
set -euo pipefail

BINARY="$1"
shift
TRACE_LOG="/tmp/rr_record_$(date +%s).log"
REPLAY_LOG="/tmp/rr_replay_$(date +%s).log"

# Record -- chaos mode for race conditions
echo "=== Recording ===" | tee "$TRACE_LOG"
rr record --chaos "$BINARY" "$@" 2>&1 | tee -a "$TRACE_LOG"
RECORD_EXIT=$?
echo "=== Record exit code: $RECORD_EXIT ===" | tee -a "$TRACE_LOG"

if [ $RECORD_EXIT -ne 0 ]; then
    echo "=== Replaying to crash ===" | tee "$REPLAY_LOG"
    rr replay \
        -ex "continue" \
        -ex "bt full" \
        -ex "info registers" \
        -ex "info locals" \
        -ex "thread apply all bt full" \
        -ex "info threads" \
        -ex "quit" \
        2>&1 | tee -a "$REPLAY_LOG"
fi

echo "=== Record log: $TRACE_LOG ==="
echo "=== Replay log: $REPLAY_LOG ==="
```

**Recipe 2: Replay with watchpoint to find corruption source**

```bash
#!/bin/bash
# Usage: ./find_corruption.sh ADDRESS
# ADDRESS is the memory address that was corrupted (from crash analysis)

ADDRESS="$1"
REPLAY_LOG="/tmp/rr_watchpoint_$(date +%s).log"

rr replay \
    -ex "continue" \
    -ex "watch *(void**)${ADDRESS}" \
    -ex "reverse-continue" \
    -ex "bt full" \
    -ex "info locals" \
    -ex "info registers" \
    -ex "list" \
    -ex "quit" \
    2>&1 | tee "$REPLAY_LOG"
```

**Recipe 3: Replay with automated checkpoint search**

```bash
#!/bin/bash
# Replay and check a condition at different event points
REPLAY_LOG="/tmp/rr_search_$(date +%s).log"

# First, find the total number of events
rr replay \
    -ex "continue" \
    -ex "when" \
    -ex "quit" \
    2>&1 | tee "$REPLAY_LOG"
```

### Why rr Is THE Tool for Heisenbugs and Race Conditions

Traditional debugging of race conditions follows this doomed pattern:

1. Observe failure in production
2. Try to reproduce -- fail, because timing is different
3. Add logging -- fail, because logging changes timing
4. Add sleeps to "widen the race window" -- sometimes works, usually doesn't
5. Stare at code and guess

rr breaks this cycle because:

- **Deterministic replay**: once recorded, the failure replays identically every
  time. No more "works on my machine".
- **Chaos mode**: actively tries different scheduling orders to surface races
  that only manifest 0.1% of the time.
- **Reverse execution**: instead of "why did it crash?", you ask "what wrote
  this bad value?" and get an exact answer.
- **Zero instrumentation overhead on replay**: the recording has 1.5-5x
  overhead, but replay analysis is as fast as you can navigate.

### Limitations

- **Single-machine only**: rr records on one machine and replays on that same
  machine (or one with a compatible CPU). No distributed tracing.
- **Performance overhead during recording**: 1.5-5x slowdown. Not suitable for
  always-on production recording, but fine for test runs and reproduction
  attempts.
- **Hardware perf counters required**: rr uses `perf_event_open` which requires
  hardware performance counters. This means:
  - Does not work inside most VMs (unless nested virtualization exposes PMU)
  - Does not work inside Docker unless you pass `--privileged` or bind-mount
    the perf subsystem
  - Cloud instances: works on bare-metal and some VM types (AWS
    metal instances, GCP C2 instances)
- **Linux only**: no macOS, no Windows.
- **x86_64 and aarch64**: x86_64 is mature; aarch64 support is newer and less
  battle-tested.
- **Single-threaded recording constraint**: rr records one thread at a time on
  a single core. Multi-threaded programs still work, but rr serializes their
  execution during recording, which may hide some race conditions (mitigated
  somewhat by `--chaos`).

### Integration with GDB

rr replay speaks GDB's MI (Machine Interface) protocol. This means:

- Every GDB command works: breakpoints, watchpoints, `print`, `x/`, `info`,
  `thread apply all`, all of it.
- GDB Python scripts work inside rr replay sessions.
- Conditional breakpoints work (and combined with reverse execution).
- Pretty-printers work.
- The only additions are the reverse-* commands and the `when`/`run`/`checkpoint`
  commands.

---

## 2. GDB Python Scripting for Automated Analysis

GDB embeds a Python interpreter that has full access to the debugger's state.
This makes it possible to write sophisticated analysis scripts that an agent can
load and execute in batch mode.

### Basics: Loading and Running Python in GDB

```bash
# Run a Python script inside GDB
gdb --batch -ex "source /tmp/analysis.py" -p $PID

# Run a Python script during replay
rr replay -ex "source /tmp/analysis.py" -ex "quit"

# Inline Python in -ex commands (short snippets only)
gdb --batch -ex "python print(gdb.selected_inferior().pid)" -p $PID
```

### Core API Reference

**Accessing the inferior (debugged process):**

```python
import gdb

inferior = gdb.selected_inferior()
pid = inferior.pid
threads = inferior.threads()
```

**Reading memory and evaluating expressions:**

```python
# Evaluate a C/Rust expression in the debuggee's context
val = gdb.parse_and_eval("my_variable")
print(f"my_variable = {val}")

# Read raw memory
mem = inferior.read_memory(address, length)
# Returns a memoryview object; convert to bytes:
raw_bytes = bytes(mem)
```

**Frame walking:**

```python
frame = gdb.newest_frame()  # innermost (most recent) frame
while frame is not None:
    print(f"  {frame.name()} at {frame.pc():#x}")
    try:
        frame = frame.older()  # move toward caller
    except gdb.error:
        break
```

**Type inspection:**

```python
t = gdb.lookup_type("struct my_struct")
print(f"Size: {t.sizeof}")
for field in t.fields():
    print(f"  {field.name}: {field.type} at offset {field.bitpos // 8}")
```

**Thread iteration:**

```python
for thread in gdb.selected_inferior().threads():
    thread.switch()  # make this thread current
    frame = gdb.newest_frame()
    print(f"Thread {thread.num} ({thread.name}): {frame.name()}")
```

### Creating Custom GDB Commands

```python
import gdb

class ThreadSummary(gdb.Command):
    """Summarize all threads with their current function."""

    def __init__(self):
        super().__init__("thread-summary", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        for thread in gdb.selected_inferior().threads():
            thread.switch()
            frame = gdb.newest_frame()
            name = frame.name() if frame else "<unknown>"
            print(f"Thread {thread.num:3d} [{thread.name or 'unnamed'}]: {name}")

ThreadSummary()
```

Save to a file, load with `source /path/to/file.py`, then run `thread-summary`.

### Complete Script: Thread Categorizer

This script walks all threads and categorizes them by what they're doing:
running user code, waiting on a mutex, sleeping, doing I/O, etc.

```python
#!/usr/bin/env python3
"""
Thread categorizer for GDB.
Groups threads by state: running, mutex-wait, condvar-wait, IO-wait, sleeping, other.

Usage:
    gdb --batch -ex "source /tmp/thread_categorizer.py" -p PID 2>&1 | tee /tmp/threads.log
"""

import gdb
import json
import sys

# Patterns that identify thread states by function names in the backtrace
MUTEX_WAIT_FUNCS = {
    "__lll_lock_wait", "__GI___pthread_mutex_lock", "pthread_mutex_lock",
    "__pthread_mutex_timedlock", "futex_wait", "__lll_lock_wait_private",
    "parking_lot_core::thread_parker", "std::sync::mutex::Mutex",
    "__rust_mutex_lock",
}

CONDVAR_WAIT_FUNCS = {
    "pthread_cond_wait", "pthread_cond_timedwait", "__pthread_cond_wait",
    "std::sync::condvar::Condvar",
}

IO_WAIT_FUNCS = {
    "epoll_wait", "epoll_pwait", "poll", "ppoll", "select", "pselect",
    "read", "__read", "write", "__write", "recvfrom", "sendto",
    "accept", "accept4", "connect", "__libc_accept", "__libc_read",
    "io_uring_enter", "aio_suspend",
    "mio::poll::Poll", "tokio::runtime",
}

SLEEP_FUNCS = {
    "nanosleep", "clock_nanosleep", "__clock_nanosleep",
    "usleep", "sleep", "pause", "sigsuspend", "sigwaitinfo",
    "std::thread::sleep",
}

SIGNAL_WAIT_FUNCS = {
    "sigwait", "sigtimedwait", "rt_sigtimedwait",
}


def categorize_thread(thread):
    """Walk the backtrace and categorize this thread."""
    thread.switch()
    frames = []
    categories = set()

    try:
        frame = gdb.newest_frame()
    except gdb.error:
        return "unknown", []

    while frame is not None:
        name = frame.name() or "<unknown>"
        frames.append(name)

        # Check against each category
        for func in MUTEX_WAIT_FUNCS:
            if func in name:
                categories.add("mutex-wait")
        for func in CONDVAR_WAIT_FUNCS:
            if func in name:
                categories.add("condvar-wait")
        for func in IO_WAIT_FUNCS:
            if func in name:
                categories.add("io-wait")
        for func in SLEEP_FUNCS:
            if func in name:
                categories.add("sleeping")
        for func in SIGNAL_WAIT_FUNCS:
            if func in name:
                categories.add("signal-wait")

        try:
            frame = frame.older()
        except gdb.error:
            break

    if not categories:
        category = "running"
    elif "mutex-wait" in categories:
        category = "mutex-wait"
    elif "condvar-wait" in categories:
        category = "condvar-wait"
    elif "io-wait" in categories:
        category = "io-wait"
    elif "sleeping" in categories:
        category = "sleeping"
    elif "signal-wait" in categories:
        category = "signal-wait"
    else:
        category = "other"

    return category, frames


def main():
    categories = {}
    thread_details = []

    for thread in gdb.selected_inferior().threads():
        try:
            category, frames = categorize_thread(thread)
        except Exception as e:
            category = "error"
            frames = [str(e)]

        if category not in categories:
            categories[category] = []
        categories[category].append(thread.num)

        thread_details.append({
            "thread_num": thread.num,
            "thread_name": thread.name or "unnamed",
            "category": category,
            "top_frames": frames[:8],
        })

    # Print summary
    total = len(thread_details)
    print(f"\n{'='*60}")
    print(f"THREAD CATEGORIZATION SUMMARY ({total} threads)")
    print(f"{'='*60}")

    for cat in ["running", "mutex-wait", "condvar-wait", "io-wait",
                 "sleeping", "signal-wait", "other", "error"]:
        if cat in categories:
            threads = categories[cat]
            print(f"\n  {cat.upper()} ({len(threads)} threads):")
            for tnum in threads:
                detail = next(d for d in thread_details if d["thread_num"] == tnum)
                top = detail["top_frames"][0] if detail["top_frames"] else "?"
                print(f"    Thread {tnum:3d} [{detail['thread_name']:20s}] -> {top}")

    # Write structured JSON for programmatic consumption
    output_path = "/tmp/thread_categories.json"
    with open(output_path, "w") as f:
        json.dump({
            "summary": {cat: len(threads) for cat, threads in categories.items()},
            "threads": thread_details,
        }, f, indent=2)
    print(f"\nStructured output written to {output_path}")


main()
```

### Complete Script: Mutex Waiter Graph Builder

This script identifies which threads are waiting on which mutexes and which
threads hold those mutexes, then builds a lock dependency graph and checks for
deadlock cycles.

```python
#!/usr/bin/env python3
"""
Mutex waiter graph builder and deadlock detector for GDB.
Builds a directed graph of lock dependencies and detects cycles (deadlocks).

Usage:
    gdb --batch -ex "source /tmp/mutex_graph.py" -p PID 2>&1 | tee /tmp/deadlock.log
"""

import gdb
import json


def get_futex_address(thread):
    """
    If a thread is blocked in a futex call, extract the futex address
    (first argument = the mutex address).
    """
    thread.switch()
    try:
        frame = gdb.newest_frame()
    except gdb.error:
        return None

    while frame is not None:
        name = frame.name() or ""
        if "futex" in name or "__lll_lock_wait" in name:
            # The futex address is typically the first argument.
            # In __lll_lock_wait, the mutex pointer is passed as the first arg.
            # Try to read it from the frame's arguments or from rdi (x86_64).
            try:
                # Try reading the first argument
                block = frame.block()
                for sym in block:
                    if sym.is_argument:
                        val = sym.value(frame)
                        addr = int(val) if val.type.code == gdb.TYPE_CODE_INT else int(val.cast(gdb.lookup_type("long")))
                        if addr > 0x1000:  # sanity check -- not a small integer
                            return addr
            except (gdb.error, RuntimeError, StopIteration):
                pass

            # Fallback: read rdi register (first arg in System V ABI)
            try:
                rdi = frame.read_register("rdi")
                addr = int(rdi)
                if addr > 0x1000:
                    return addr
            except (gdb.error, ValueError):
                pass

        try:
            frame = frame.older()
        except gdb.error:
            break

    return None


def get_held_locks(thread):
    """
    Heuristic: scan the backtrace for functions that acquire locks.
    This is imperfect -- a proper implementation would instrument
    pthread_mutex_lock to track acquisitions. For post-mortem analysis,
    we look for mutexes in local variables.
    """
    thread.switch()
    held = []

    try:
        frame = gdb.newest_frame()
    except gdb.error:
        return held

    while frame is not None:
        try:
            # Look for local variables that look like mutex pointers
            block = frame.block()
            for sym in block:
                if sym.is_variable or sym.is_argument:
                    name_lower = sym.name.lower()
                    if "mutex" in name_lower or "lock" in name_lower or "mtx" in name_lower:
                        try:
                            val = sym.value(frame)
                            # If it's a pointer, get the address it points to
                            if val.type.code == gdb.TYPE_CODE_PTR:
                                addr = int(val)
                                if addr > 0x1000:
                                    held.append(addr)
                            elif hasattr(val, 'address') and val.address:
                                addr = int(val.address)
                                if addr > 0x1000:
                                    held.append(addr)
                        except (gdb.error, RuntimeError):
                            pass
        except (gdb.error, RuntimeError):
            pass

        try:
            frame = frame.older()
        except gdb.error:
            break

    return held


def detect_cycles(graph):
    """
    Detect cycles in a directed graph.
    graph: dict mapping node -> list of neighbors
    Returns list of cycles found.
    """
    visited = set()
    rec_stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)

        path.pop()
        rec_stack.discard(node)

    for node in graph:
        if node not in visited:
            dfs(node, [])

    return cycles


def main():
    threads = list(gdb.selected_inferior().threads())

    print(f"\n{'='*60}")
    print(f"MUTEX WAITER GRAPH ANALYSIS ({len(threads)} threads)")
    print(f"{'='*60}")

    # Step 1: Find which threads are waiting on which futex/mutex
    waiters = {}  # thread_num -> futex_address
    for thread in threads:
        try:
            addr = get_futex_address(thread)
            if addr is not None:
                waiters[thread.num] = addr
                print(f"  Thread {thread.num:3d} [{thread.name or 'unnamed':20s}] WAITING on lock @ {addr:#x}")
        except Exception as e:
            print(f"  Thread {thread.num:3d} [{thread.name or 'unnamed':20s}] ERROR: {e}")

    # Step 2: Find which threads hold which locks
    holders = {}  # thread_num -> [lock_addresses]
    for thread in threads:
        try:
            held = get_held_locks(thread)
            if held:
                holders[thread.num] = held
                for addr in held:
                    print(f"  Thread {thread.num:3d} [{thread.name or 'unnamed':20s}] HOLDS lock @ {addr:#x}")
        except Exception as e:
            pass

    # Step 3: Build wait-for graph
    # Edge: thread A -> thread B means "A is waiting for a lock that B holds"
    wait_for_graph = {}
    lock_to_holder = {}

    # Map each lock to its holder thread(s)
    for tnum, locks in holders.items():
        for lock_addr in locks:
            lock_to_holder[lock_addr] = tnum

    # For each waiting thread, find who holds the lock it's waiting for
    for waiter_tnum, lock_addr in waiters.items():
        if lock_addr in lock_to_holder:
            holder_tnum = lock_to_holder[lock_addr]
            if waiter_tnum not in wait_for_graph:
                wait_for_graph[waiter_tnum] = []
            wait_for_graph[waiter_tnum].append(holder_tnum)
            print(f"\n  DEPENDENCY: Thread {waiter_tnum} --waits-for--> Thread {holder_tnum} (lock @ {lock_addr:#x})")

    # Step 4: Detect cycles
    cycles = detect_cycles(wait_for_graph)

    print(f"\n{'='*60}")
    if cycles:
        print(f"DEADLOCK DETECTED! {len(cycles)} cycle(s) found:")
        for i, cycle in enumerate(cycles):
            print(f"\n  Cycle {i+1}: {' -> '.join(f'Thread {t}' for t in cycle)}")
            print(f"  This is a PROVEN deadlock -- circular wait among these threads.")
    else:
        if waiters:
            print("No deadlock cycle detected, but some threads are waiting on locks.")
            print("The lock holders may be busy (not deadlocked) or the held-lock")
            print("detection heuristic may have missed some locks.")
        else:
            print("No threads appear to be waiting on mutexes.")
    print(f"{'='*60}")

    # Write structured output
    output = {
        "waiters": {str(k): f"0x{v:x}" for k, v in waiters.items()},
        "holders": {str(k): [f"0x{a:x}" for a in v] for k, v in holders.items()},
        "wait_for_graph": {str(k): v for k, v in wait_for_graph.items()},
        "cycles": cycles,
        "deadlock_detected": len(cycles) > 0,
    }
    output_path = "/tmp/mutex_graph.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nStructured output written to {output_path}")


main()
```

### Complete Script: Statistical Profiler

This script repeatedly samples backtraces and aggregates frame frequency to
identify hot functions -- useful when `perf` is not available (e.g., inside
containers without perf_event access).

```python
#!/usr/bin/env python3
"""
Statistical profiler using GDB.
Repeatedly samples backtraces and reports the most frequent frames.

Usage:
    gdb --batch -ex "source /tmp/gdb_profiler.py" -p PID 2>&1 | tee /tmp/profile.log

Caveats: this is EXTREMELY slow compared to perf. It stops the process for each
sample. Use only when perf/bpftrace are unavailable.
"""

import gdb
import time
import json
from collections import defaultdict

NUM_SAMPLES = 50         # Number of backtrace samples to collect
SAMPLE_INTERVAL_MS = 100  # Milliseconds between samples (approximate)


def sample_all_threads():
    """Take one backtrace sample from all threads."""
    samples = []
    for thread in gdb.selected_inferior().threads():
        try:
            thread.switch()
            frames = []
            frame = gdb.newest_frame()
            depth = 0
            while frame is not None and depth < 30:
                name = frame.name() or f"<unknown@{frame.pc():#x}>"
                frames.append(name)
                try:
                    frame = frame.older()
                except gdb.error:
                    break
                depth += 1
            samples.append(frames)
        except gdb.error:
            pass
    return samples


def main():
    frame_counts = defaultdict(int)
    stack_counts = defaultdict(int)
    total_samples = 0

    print(f"\n{'='*60}")
    print(f"GDB STATISTICAL PROFILER")
    print(f"Collecting {NUM_SAMPLES} samples at ~{SAMPLE_INTERVAL_MS}ms intervals")
    print(f"{'='*60}")

    for i in range(NUM_SAMPLES):
        # Continue briefly then interrupt
        try:
            gdb.execute("continue &", to_string=True)
            time.sleep(SAMPLE_INTERVAL_MS / 1000.0)
            gdb.execute("interrupt", to_string=True)
            time.sleep(0.01)  # Let GDB settle
        except gdb.error:
            pass

        samples = sample_all_threads()
        for frames in samples:
            total_samples += 1
            # Count each unique frame in this sample
            seen = set()
            for func_name in frames:
                if func_name not in seen:
                    frame_counts[func_name] += 1
                    seen.add(func_name)
            # Count the full stack signature
            stack_key = " -> ".join(frames[:5])  # Top 5 frames as signature
            stack_counts[stack_key] += 1

        if (i + 1) % 10 == 0:
            print(f"  ... {i+1}/{NUM_SAMPLES} samples collected ({total_samples} thread-samples)")

    # Report
    print(f"\n{'='*60}")
    print(f"PROFILE RESULTS ({total_samples} thread-samples)")
    print(f"{'='*60}")

    print(f"\nTop 20 functions by sample frequency:")
    print(f"{'Samples':>8s}  {'%':>6s}  Function")
    print(f"{'-'*8}  {'-'*6}  {'-'*40}")

    sorted_frames = sorted(frame_counts.items(), key=lambda x: -x[1])
    for name, count in sorted_frames[:20]:
        pct = 100.0 * count / total_samples if total_samples > 0 else 0
        print(f"{count:8d}  {pct:5.1f}%  {name}")

    print(f"\nTop 10 stack signatures:")
    sorted_stacks = sorted(stack_counts.items(), key=lambda x: -x[1])
    for stack, count in sorted_stacks[:10]:
        pct = 100.0 * count / total_samples if total_samples > 0 else 0
        print(f"\n  [{count} samples, {pct:.1f}%]")
        for func in stack.split(" -> "):
            print(f"    {func}")

    # Write structured output
    output_path = "/tmp/gdb_profile.json"
    with open(output_path, "w") as f:
        json.dump({
            "total_samples": total_samples,
            "frame_counts": dict(sorted_frames[:50]),
            "stack_counts": dict(sorted_stacks[:20]),
        }, f, indent=2)
    print(f"\nStructured output written to {output_path}")


main()
```

### Complete Script: Memory Region Dumper

Examines heap metadata and memory regions for corruption analysis.

```python
#!/usr/bin/env python3
"""
Memory region dumper and heap metadata inspector for GDB.
Reads /proc/PID/maps and examines glibc malloc chunk headers.

Usage:
    gdb --batch -ex "source /tmp/memory_dumper.py" -p PID 2>&1 | tee /tmp/memory.log
"""

import gdb
import json
import re


def read_proc_maps():
    """Read /proc/PID/maps to understand the memory layout."""
    pid = gdb.selected_inferior().pid
    maps = []
    try:
        with open(f"/proc/{pid}/maps", "r") as f:
            for line in f:
                parts = line.strip().split(None, 5)
                if len(parts) >= 5:
                    addr_range = parts[0].split("-")
                    maps.append({
                        "start": int(addr_range[0], 16),
                        "end": int(addr_range[1], 16),
                        "perms": parts[1],
                        "offset": parts[2],
                        "dev": parts[3],
                        "inode": parts[4],
                        "name": parts[5] if len(parts) > 5 else "",
                    })
    except (IOError, OSError) as e:
        print(f"WARNING: Cannot read /proc/{pid}/maps: {e}")
    return maps


def classify_region(region):
    """Classify a memory region by its name/properties."""
    name = region["name"].strip()
    perms = region["perms"]

    if "[heap]" in name:
        return "heap"
    elif "[stack]" in name:
        return "stack"
    elif "[vdso]" in name or "[vvar]" in name or "[vsyscall]" in name:
        return "kernel"
    elif name.endswith(".so") or ".so." in name:
        return "shared-lib"
    elif name and not name.startswith("["):
        return "file-mapped"
    elif perms == "---p":
        return "guard-page"
    elif "x" in perms:
        return "executable"
    else:
        return "anonymous"


def examine_malloc_chunk(address):
    """
    Examine a glibc malloc chunk header at the given address.
    Chunk layout (64-bit):
        offset -16: prev_size (8 bytes) -- size of previous chunk if free
        offset  -8: size (8 bytes) -- size of this chunk | flags in low 3 bits
        offset   0: user data starts here (this is what malloc returns)

    Flags in size field:
        bit 0 (PREV_INUSE): previous chunk is in use
        bit 1 (IS_MMAPPED): chunk was allocated via mmap
        bit 2 (NON_MAIN_ARENA): chunk belongs to a non-main arena
    """
    result = {}
    try:
        inferior = gdb.selected_inferior()
        # Read 16 bytes before the user pointer (chunk header)
        header_addr = address - 16
        header_bytes = bytes(inferior.read_memory(header_addr, 16))

        prev_size = int.from_bytes(header_bytes[0:8], byteorder='little')
        size_field = int.from_bytes(header_bytes[8:16], byteorder='little')

        chunk_size = size_field & ~0x7  # Mask out flag bits
        prev_inuse = bool(size_field & 0x1)
        is_mmapped = bool(size_field & 0x2)
        non_main_arena = bool(size_field & 0x4)

        result = {
            "address": f"0x{address:x}",
            "header_address": f"0x{header_addr:x}",
            "prev_size": prev_size,
            "chunk_size": chunk_size,
            "flags": {
                "PREV_INUSE": prev_inuse,
                "IS_MMAPPED": is_mmapped,
                "NON_MAIN_ARENA": non_main_arena,
            },
            "raw_size_field": f"0x{size_field:x}",
        }

        # Sanity checks
        issues = []
        if chunk_size == 0:
            issues.append("CORRUPT: chunk size is zero")
        if chunk_size > 0x100000000:  # > 4GB is suspicious
            issues.append(f"SUSPICIOUS: chunk size {chunk_size} is very large")
        if chunk_size % 16 != 0:
            issues.append(f"CORRUPT: chunk size {chunk_size} is not 16-byte aligned")
        result["issues"] = issues

        # Read first 64 bytes of user data
        try:
            user_data = bytes(inferior.read_memory(address, 64))
            result["user_data_hex"] = user_data.hex()
            # Check if it looks like freed memory (glibc fills with fd/bk pointers)
            ptr1 = int.from_bytes(user_data[0:8], byteorder='little')
            ptr2 = int.from_bytes(user_data[8:16], byteorder='little')
            if not prev_inuse:
                result["free_list"] = {
                    "fd": f"0x{ptr1:x}",
                    "bk": f"0x{ptr2:x}",
                }
        except gdb.MemoryError:
            result["user_data_hex"] = "<unreadable>"

    except gdb.MemoryError as e:
        result["error"] = f"Cannot read memory at 0x{address:x}: {e}"
    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    pid = gdb.selected_inferior().pid

    print(f"\n{'='*60}")
    print(f"MEMORY REGION ANALYSIS (PID {pid})")
    print(f"{'='*60}")

    # Read and classify memory regions
    maps = read_proc_maps()
    region_summary = {}

    for region in maps:
        category = classify_region(region)
        if category not in region_summary:
            region_summary[category] = {"count": 0, "total_size": 0, "regions": []}
        size = region["end"] - region["start"]
        region_summary[category]["count"] += 1
        region_summary[category]["total_size"] += size
        region_summary[category]["regions"].append({
            "range": f"0x{region['start']:x}-0x{region['end']:x}",
            "size": size,
            "perms": region["perms"],
            "name": region["name"].strip(),
        })

    print(f"\nMemory region summary:")
    for category in sorted(region_summary.keys()):
        info = region_summary[category]
        total_mb = info["total_size"] / (1024 * 1024)
        print(f"  {category:15s}: {info['count']:3d} regions, {total_mb:8.1f} MB total")

    # Find heap region(s) and examine some chunks
    heap_regions = [r for r in maps if "[heap]" in r["name"]]
    if heap_regions:
        heap = heap_regions[0]
        heap_size = heap["end"] - heap["start"]
        print(f"\nHeap region: 0x{heap['start']:x} - 0x{heap['end']:x} ({heap_size / 1024:.0f} KB)")

        # Sample a few chunks from the start of the heap
        # The first chunk typically starts at the heap base + some offset
        print(f"\nSampling malloc chunks from heap start:")
        addr = heap["start"] + 16  # Skip to first user data pointer
        for i in range(5):
            if addr >= heap["end"] - 32:
                break
            chunk = examine_malloc_chunk(addr)
            print(f"\n  Chunk at {chunk.get('address', '?')}:")
            if "error" in chunk:
                print(f"    ERROR: {chunk['error']}")
                break
            print(f"    Size: {chunk.get('chunk_size', '?')} bytes")
            print(f"    Flags: {chunk.get('flags', {})}")
            if chunk.get("issues"):
                for issue in chunk["issues"]:
                    print(f"    *** {issue} ***")
            if chunk.get("free_list"):
                print(f"    Free list: fd={chunk['free_list']['fd']}, bk={chunk['free_list']['bk']}")

            # Move to next chunk
            size = chunk.get("chunk_size")
            if isinstance(size, int) and size > 0 and size < 0x100000:
                addr += size
            else:
                break

    # Write structured output
    output_path = "/tmp/memory_regions.json"
    with open(output_path, "w") as f:
        json.dump({
            "pid": pid,
            "region_summary": {k: {"count": v["count"], "total_size": v["total_size"]}
                               for k, v in region_summary.items()},
            "heap_regions": [{"start": f"0x{r['start']:x}", "end": f"0x{r['end']:x}",
                              "size": r["end"] - r["start"]} for r in heap_regions],
        }, f, indent=2)
    print(f"\nStructured output written to {output_path}")


main()
```

### Error Handling in GDB Python Scripts

GDB Python scripts run in a fragile environment. The debuggee might be in any
state, frames might be corrupt, memory might be unreadable. Always wrap frame
walks and memory reads:

```python
def safe_frame_walk(max_depth=50):
    """Walk frames with comprehensive error handling."""
    frames = []
    try:
        frame = gdb.newest_frame()
    except gdb.error as e:
        return [f"<cannot get newest frame: {e}>"]

    depth = 0
    while frame is not None and depth < max_depth:
        try:
            name = frame.name() or f"<unknown@{frame.pc():#x}>"
        except gdb.error:
            name = "<error reading frame>"

        try:
            sal = frame.find_sal()
            if sal.symtab:
                location = f"{sal.symtab.filename}:{sal.line}"
            else:
                location = f"<no source info>"
        except gdb.error:
            location = "<error>"

        frames.append(f"{name} at {location}")

        try:
            frame = frame.older()
        except gdb.error:
            frames.append("<corrupted stack beyond this point>")
            break

        depth += 1

    if depth >= max_depth:
        frames.append(f"<truncated at {max_depth} frames>")

    return frames
```

### Writing Pretty Printers

Pretty printers make complex types readable in GDB output. Useful for Rust's
`Vec`, `HashMap`, `String`, and custom types.

```python
import gdb

class RustVecPrinter:
    """Pretty-print a Rust Vec<T>."""

    def __init__(self, val):
        self.val = val

    def to_string(self):
        try:
            buf = self.val["buf"]
            ptr = buf["ptr"]["pointer"]["pointer"]
            length = int(self.val["len"])
            capacity = int(buf["cap"]["0"])
            return f"Vec(len={length}, cap={capacity}, ptr={ptr})"
        except gdb.error as e:
            return f"Vec(<error: {e}>)"

    def children(self):
        try:
            ptr = self.val["buf"]["ptr"]["pointer"]["pointer"]
            length = int(self.val["len"])
            element_type = ptr.type.target()
            for i in range(min(length, 20)):  # Cap at 20 elements
                yield f"[{i}]", (ptr + i).dereference()
            if length > 20:
                yield "...", f"({length - 20} more elements)"
        except gdb.error:
            pass


def rust_type_lookup(val):
    """Register pretty printers for Rust types."""
    type_name = str(val.type.tag or val.type.name or "")
    if "Vec<" in type_name:
        return RustVecPrinter(val)
    return None


gdb.pretty_printers.append(rust_type_lookup)
```

---

## 3. Hardware Watchpoints

### What They Are

Hardware watchpoints use the CPU's debug registers (DR0-DR3 on x86_64) to
monitor memory accesses without any software overhead. When the CPU accesses a
watched address, it triggers a hardware exception that GDB catches. This is
fundamentally different from software breakpoints (which replace an instruction
with INT3) -- hardware watchpoints operate at the memory bus level.

### Limits

x86_64 provides exactly **4 hardware debug registers** (DR0-DR3). This means
you can have at most 4 hardware watchpoints simultaneously. Each can watch 1, 2,
4, or 8 bytes.

When you exceed 4 hardware watchpoints, GDB silently falls back to **software
watchpoints**, which single-step every instruction and check whether the watched
memory changed. This is roughly **1000x slower** and makes the program
essentially unusable.

### Watch Types

| Command | Triggers on | Use case |
|---------|------------|----------|
| `watch EXPR` | Write to EXPR | "Who changed this value?" |
| `rwatch EXPR` | Read from EXPR | "Who's reading stale data?" |
| `awatch EXPR` | Any access (read or write) | "Who touches this memory at all?" |

### Setting Watchpoints by Address

```
# Watch a global variable
(gdb) watch global_counter
Hardware watchpoint 1: global_counter

# Watch a specific memory address (cast to appropriate type)
(gdb) watch *(int*)0x7fff5fbff8a0
Hardware watchpoint 2: *(int*)0x7fff5fbff8a0

# Watch a larger region (up to 8 bytes on x86_64)
(gdb) watch *(long*)0x7fff5fbff8a0
Hardware watchpoint 3: *(long*)0x7fff5fbff8a0

# Watch a struct field
(gdb) watch obj->status
Hardware watchpoint 4: obj->status

# Watch with a condition
(gdb) watch global_counter if global_counter > 1000
```

### rwatch for Finding Stale Data Readers

`rwatch` is rarely used but invaluable in specific scenarios. If you know a
piece of memory contains stale or corrupt data and you want to find **who reads
it** (and therefore acts on bad data):

```
# Trigger when anything reads from this address
(gdb) rwatch *(long*)0x55a3f000
Hardware read watchpoint 5: *(long*)0x55a3f000
```

Note: not all architectures support read watchpoints. x86_64 does.

### Batch Mode for Data Corruption

The canonical pattern for finding who corrupts a variable:

```bash
# Step 1: Find the address of the variable
gdb --batch \
    -ex "break main" \
    -ex "run" \
    -ex "print &global_var" \
    -ex "quit" \
    --args ./binary

# Step 2: Set a watchpoint on that address and let it run
gdb --batch \
    -ex "watch *(int*)&global_var" \
    -ex "commands 1" \
    -ex "  bt 10" \
    -ex "  print global_var" \
    -ex "  continue" \
    -ex "end" \
    -ex "run" \
    --args ./binary 2>&1 | tee /tmp/watchpoint.log
```

This logs every write to `global_var` with a backtrace, without stopping.

### Watchpoints for Heap Corruption

When a program crashes due to heap corruption, the corrupted address is usually
visible in the crash dump. The workflow:

1. Run the program, observe the crash. Note the corrupted address.
2. Re-run under GDB with a hardware watchpoint on that address.
3. GDB stops at the exact instruction that wrote the bad value.

```bash
# From the crash, we know the corrupted chunk is at 0x55a3f000
# The chunk header (prev_size + size) is at 0x55a3eff0
gdb --batch \
    -ex "watch *(long*)0x55a3eff0" \
    -ex "commands 1" \
    -ex "  bt full" \
    -ex "  print/x *(long[4]*)0x55a3eff0" \
    -ex "  continue" \
    -ex "end" \
    -ex "run" \
    --args ./binary 2>&1 | tee /tmp/heap_corruption.log
```

**Caveat**: The heap address may differ between runs due to ASLR. Solutions:

- Disable ASLR: `echo 0 | sudo tee /proc/sys/kernel/randomize_va_space`
- Or: set a breakpoint early, use `print &variable` to find the address
  dynamically, then set the watchpoint.

### Watchpoints on Struct Fields with Exact Offsets

When you need to watch a specific field deep inside a struct:

```
(gdb) # Find the offset
(gdb) print (int)&((struct connection*)0)->state
$1 = 48

(gdb) # Watch that field on a specific instance
(gdb) print &my_conn
$2 = (struct connection *) 0x55a3f100
(gdb) watch *(int*)(0x55a3f100 + 48)
Hardware watchpoint 1: *(int*)(0x55a3f100 + 48)
```

### Checking Watchpoint Type

Always verify that your watchpoint is actually hardware-backed:

```
(gdb) info watchpoints
Num     Type           Disp Enb Address            What
1       hw watchpoint  keep y                      *(int*)0x55a3f100
2       watchpoint     keep y                      big_array[500]
```

Watchpoint 1 is `hw watchpoint` (hardware) -- good, no overhead.
Watchpoint 2 is just `watchpoint` (software) -- this will be extremely slow.

If you see a software watchpoint, reduce the number of watchpoints to 4 or
fewer, or narrow the watched region.

### Software vs Hardware Watchpoint Performance

| Type | Mechanism | Overhead | Max count |
|------|-----------|----------|-----------|
| Hardware | CPU debug registers | ~0% (no overhead) | 4 on x86_64 |
| Software | Single-step every instruction | ~1000x slowdown | Unlimited |

GDB does not warn you when it falls back to software watchpoints. You must check
with `info watchpoints`.

---

## 4. Memory Corruption Analysis

### Sanitizer Overview

The compiler-based sanitizers are the first line of defense. They instrument the
binary at compile time to detect memory errors at runtime with moderate overhead.

| Sanitizer | Flag | Detects | Overhead |
|-----------|------|---------|----------|
| ASAN | `-fsanitize=address` | Use-after-free, buffer overflow (heap/stack/global), double-free, memory leaks | 2-3x slower, 2-3x more memory |
| MSAN | `-fsanitize=memory` | Reads of uninitialized memory | 3x slower |
| TSAN | `-fsanitize=thread` | Data races | 5-15x slower, 5-10x more memory |
| LSAN | `-fsanitize=leak` | Memory leaks (standalone or integrated with ASAN) | Minimal (runs at exit) |
| UBSAN | `-fsanitize=undefined` | Undefined behavior (signed overflow, null deref, alignment) | 1.1-1.5x slower |

**Critical limitation**: ASAN and MSAN cannot be combined. ASAN and TSAN cannot
be combined. You must build separate binaries for each sanitizer.

### Using ASAN with GDB

By default, ASAN prints an error report and calls `_exit()`, which means GDB
never sees a signal. To make ASAN abort (so GDB catches it):

```bash
# Build with ASAN
gcc -fsanitize=address -g -O1 -fno-omit-frame-pointer -o binary source.c
# or for Rust
RUSTFLAGS="-Zsanitizer=address" cargo +nightly build --target x86_64-unknown-linux-gnu

# Run under GDB with ASAN configured to abort
ASAN_OPTIONS=abort_on_error=1:halt_on_error=1 \
    gdb --batch \
    -ex "run" \
    -ex "bt full" \
    -ex "info locals" \
    -ex "thread apply all bt" \
    -ex "quit" \
    --args ./binary 2>&1 | tee /tmp/asan.log
```

The ASAN report is printed to stderr before the abort, and then GDB catches
SIGABRT. The backtrace shows both the ASAN runtime frames and the application
frames.

### Rust-Specific Sanitizer Usage

```bash
# ASAN for Rust
RUSTFLAGS="-Zsanitizer=address" \
    cargo +nightly build --target x86_64-unknown-linux-gnu

# TSAN for Rust (catches data races in unsafe code)
RUSTFLAGS="-Zsanitizer=thread" \
    cargo +nightly build --target x86_64-unknown-linux-gnu

# MSAN for Rust (requires all dependencies to also be MSAN-instrumented, which
# is very hard in practice -- prefer Valgrind for uninitialized memory checks)
RUSTFLAGS="-Zsanitizer=memory" \
    cargo +nightly build --target x86_64-unknown-linux-gnu

# Run ASAN-instrumented Rust binary under GDB
ASAN_OPTIONS=abort_on_error=1 \
    gdb --batch -ex "run" -ex "bt full" -ex "quit" \
    --args target/x86_64-unknown-linux-gnu/debug/binary
```

### Heap Analysis Without Sanitizers

When you can't rebuild with sanitizers (e.g., production binary, third-party
library), you can examine glibc's malloc metadata directly in GDB.

**glibc malloc chunk layout (64-bit):**

```
Address:        Content:
chunk_ptr + 0:  prev_size  (8 bytes) -- size of previous chunk if PREV_INUSE is 0
chunk_ptr + 8:  size       (8 bytes) -- chunk size | flags
chunk_ptr + 16: user data starts here (this is what malloc() returns)

Size field flags (low 3 bits):
  bit 0 (0x1) PREV_INUSE:      previous chunk is allocated
  bit 1 (0x2) IS_MMAPPED:      chunk was mmap'd (not from sbrk heap)
  bit 2 (0x4) NON_MAIN_ARENA:  chunk from a thread-local arena
```

**Examining a chunk in GDB:**

```
(gdb) # ptr is what malloc returned (user data pointer)
(gdb) # To see the chunk header, go back 16 bytes
(gdb) x/4gx ptr-16
0x55a3eff0: 0x0000000000000000  0x0000000000000051   # prev_size=0, size=0x50|PREV_INUSE
0x55a3f000: 0x4141414141414141  0x4141414141414141   # user data

# Decode: chunk size = 0x50 & ~0x7 = 0x50 = 80 bytes
# Flags: PREV_INUSE=1, IS_MMAPPED=0, NON_MAIN_ARENA=0
# Next chunk is at 0x55a3eff0 + 0x50 = 0x55a3f040
```

**Signs of corruption:**

```
# Corrupted size field:
(gdb) x/2gx ptr-16
0x55a3eff0: 0x0000000000000000  0x4141414141414141   # size = 'AAAAAAAA' -- buffer overflow from previous chunk

# Double-free / use-after-free (free list pointers visible):
(gdb) x/4gx ptr-16
0x55a3eff0: 0x0000000000000000  0x0000000000000051   # size looks ok
0x55a3f000: 0x00007f3a2b000010  0x00007f3a2b000020   # fd and bk pointers -- this chunk is free!
# If code is still using ptr, it's a use-after-free
```

**Walking the free list:**

```
(gdb) # main_arena is a global in glibc
(gdb) print main_arena
(gdb) # Or find it:
(gdb) info address main_arena
# Examine fastbins, unsorted bin, smallbins, largebins in main_arena
(gdb) print main_arena.fastbinsY
(gdb) print main_arena.bins[0]  # unsorted bin
```

### Valgrind + GDB Integration

Valgrind can run a GDB server that lets you debug with full Valgrind error
detection:

```bash
# Terminal 1: Start Valgrind with GDB server
valgrind --vgdb=yes --vgdb-error=0 ./binary

# Terminal 2: Connect GDB
gdb ./binary -ex "target remote | vgdb"

# Or in a single batch command (connect to already-running valgrind):
gdb --batch \
    -ex "target remote | vgdb" \
    -ex "continue" \
    -ex "bt full" \
    -ex "quit" \
    ./binary
```

`--vgdb-error=0` means Valgrind stops at startup before the program runs
(useful for setting breakpoints). `--vgdb-error=1` stops on the first error.

Inside GDB connected to Valgrind, you get special commands:

```
(gdb) monitor leak_check full reachable any
# Runs a full leak check right now

(gdb) monitor who_points_at 0x55a3f000
# Shows what still points to this address (useful for understanding leaks)

(gdb) monitor block_list 100
# Shows the 100 largest allocated blocks
```

### Double-Free Detection in GDB

When ASAN is not available, you can catch double-frees manually:

```bash
gdb --batch \
    -ex "break free" \
    -ex "commands 1" \
    -ex "  silent" \
    -ex "  set \$addr = (void*)\$rdi" \
    -ex "  printf \"free(%p) from thread %d\\n\", \$addr, \$_thread" \
    -ex "  bt 5" \
    -ex "  continue" \
    -ex "end" \
    -ex "run" \
    --args ./binary 2>&1 | tee /tmp/free_log.log
```

Then search the log for duplicate addresses:

```bash
grep "^free(" /tmp/free_log.log | sort | uniq -d
```

Any address that appears twice was double-freed.

### Stack Smashing Analysis

When GCC's stack protector fires (`*** stack smashing detected ***`):

```bash
# Break on the stack check failure handler
gdb --batch \
    -ex "break __stack_chk_fail" \
    -ex "run" \
    -ex "bt full" \
    -ex "info locals" \
    -ex "quit" \
    --args ./binary 2>&1 | tee /tmp/stack_smash.log
```

The backtrace at `__stack_chk_fail` shows which function had its canary
overwritten. Examine the local variables in that function to find the buffer
that overflowed.

### Signal Frame Analysis

When SIGSEGV arrives, decode the faulting address:

```
(gdb) # After SIGSEGV stops execution:
(gdb) print $_siginfo._sifields._sigfault.si_addr
$1 = (void *) 0x0
# Faulting address is 0x0 -- NULL pointer dereference

(gdb) print $_siginfo.si_signo
$2 = 11   # SIGSEGV

(gdb) print $_siginfo.si_code
$3 = 1    # SEGV_MAPERR (address not mapped) vs 2 = SEGV_ACCERR (permission denied)
```

In batch mode:

```bash
gdb --batch \
    -ex "run" \
    -ex "print \$_siginfo._sifields._sigfault.si_addr" \
    -ex "print \$_siginfo.si_code" \
    -ex "bt full" \
    -ex "info registers" \
    -ex "x/5i \$pc" \
    -ex "quit" \
    --args ./binary 2>&1 | tee /tmp/sigsegv.log
```

---

## 5. Lock Graph Construction and Deadlock Proof

### Why Backtraces Alone Are Not Enough

When you see a hung program with threads in `futex_wait`, the natural instinct
is to say "looks like a deadlock." But that is not proof. Threads might be:

- Waiting on a legitimately slow operation
- Waiting for a resource that is held by a thread doing I/O
- In a priority inversion scenario (not a deadlock)
- Waiting for an external event (network, timer, signal)

To **prove** a deadlock, you must demonstrate a **cycle** in the wait-for graph.
This is the difference between a guess and a diagnosis.

### Step-by-Step Lock Graph Construction

**Step 1: Identify every thread that is waiting on a lock.**

From `thread apply all bt`, look for threads blocked in:
- `__lll_lock_wait` (glibc mutex)
- `futex_wait` / `futex_wait_queue_me` (kernel futex)
- `pthread_mutex_lock` / `pthread_rwlock_wrlock` / `pthread_rwlock_rdlock`
- `parking_lot_core::park` (Rust parking_lot)
- `std::sync::mutex::Mutex::lock` (Rust stdlib)

```
Thread 3 (LWP 12345):
#0  __lll_lock_wait () at lowlevellock.S:135
#1  pthread_mutex_lock (mutex=0x55a3f100) at pthread_mutex_lock.c:80
#2  process_request (ctx=0x7fff5000) at server.c:150
```

Thread 3 is waiting on mutex at `0x55a3f100`.

**Step 2: For each waiting thread, identify which locks it already holds.**

This is the harder part. Options:

a) Look at the frames above the lock acquisition -- local variables or arguments
   that are mutex pointers indicate locks being held.

b) If the code uses RAII lock guards (Rust's `MutexGuard`, C++'s
   `std::lock_guard`), look for guard variables in `info locals` for frames
   above the current lock wait.

c) Examine the mutex's `__data.__owner` field (glibc):

```
(gdb) print *(pthread_mutex_t*)0x55a3f100
$1 = {
  __data = {
    __lock = 2,           # 0 = unlocked, 1 = locked, 2 = locked with waiters
    __count = 0,
    __owner = 12344,      # <-- LWP of the thread holding this mutex
    __nusers = 1,
    __kind = 0,           # PTHREAD_MUTEX_DEFAULT
    ...
  }
}
```

Now you know: thread 3 (LWP 12345) is waiting for mutex at `0x55a3f100`, which
is held by LWP 12344 (thread 2).

**Step 3: Build the directed graph.**

```
Thread 2 (LWP 12344) --holds--> mutex 0x55a3f100 <--waits-- Thread 3 (LWP 12345)
Thread 3 (LWP 12345) --holds--> mutex 0x55a3f200 <--waits-- Thread 2 (LWP 12344)
```

**Step 4: Find the cycle.**

```
Thread 2 --waits-for-lock-held-by--> Thread 3 --waits-for-lock-held-by--> Thread 2
```

This is a cycle. Deadlock proven.

### Extracting Lock Owner from glibc Mutex

The most reliable way to find who holds a mutex:

```
(gdb) # Given mutex address 0x55a3f100
(gdb) set $mtx = (pthread_mutex_t*)0x55a3f100
(gdb) print $mtx->__data.__owner
$1 = 12344
(gdb) # This is the LWP (kernel thread ID)
(gdb) # Find which GDB thread this corresponds to:
(gdb) info threads
  Id   Target Id              Frame
  1    Thread 0x7f3a (LWP 12343) main
  2    Thread 0x7f3b (LWP 12344) __lll_lock_wait  # <-- this one holds it
  3    Thread 0x7f3c (LWP 12345) __lll_lock_wait
```

### Futex-Based Analysis

When you don't have debug symbols for the mutex type, you can work from the
syscall level. In `__lll_lock_wait`, the futex address is the first argument:

```
(gdb) thread 3
(gdb) frame 0
#0  __lll_lock_wait () at lowlevellock.S:135
(gdb) info registers rdi
rdi            0x55a3f100       # This is the futex/mutex address
```

Cross-reference this address across all threads to find who holds it and who
else is waiting.

### Batch Mode Deadlock Analysis

```bash
#!/bin/bash
# Comprehensive deadlock analysis
PID=$1
LOG="/tmp/deadlock_analysis_$(date +%s).log"

gdb --batch \
    -ex "thread apply all bt full" \
    -ex "python
import gdb, json
result = {'threads': []}
for t in gdb.selected_inferior().threads():
    t.switch()
    f = gdb.newest_frame()
    frames = []
    while f:
        frames.append(f.name() or '<unknown>')
        try: f = f.older()
        except: break
    waiting_on = None
    if frames and ('lll_lock_wait' in frames[0] or 'futex_wait' in frames[0]):
        try:
            waiting_on = hex(int(gdb.newest_frame().read_register('rdi')))
        except: pass
    result['threads'].append({
        'num': t.num, 'lwp': t.ptid[1],
        'top_frame': frames[0] if frames else '?',
        'waiting_on_futex': waiting_on
    })
with open('/tmp/deadlock_threads.json', 'w') as f:
    json.dump(result, f, indent=2)
print('Thread analysis written to /tmp/deadlock_threads.json')
" \
    -ex "quit" \
    -p "$PID" 2>&1 | tee "$LOG"
```

### Priority Inversion

Priority inversion is not a deadlock, but it can look like one:

- High-priority thread H waits for mutex held by low-priority thread L
- Medium-priority thread M preempts L (because M has higher priority than L)
- H is effectively blocked by M, even though M and H share no locks

Symptoms: H appears hung, L appears to make no progress, but there is no cycle
in the lock graph.

Solution: priority inheritance mutexes (`PTHREAD_PRIO_INHERIT`), or `rt_mutex`
in the kernel.

### RwLock Deadlocks

Read-write locks have a subtle deadlock mode:

```
Thread 1: holds read lock, tries to upgrade to write lock
Thread 2: holds read lock, tries to upgrade to write lock
```

Neither can get the write lock because the other still holds a read lock.
Neither will release its read lock because it's waiting for the write lock.
Deadlock.

Another variant:

```
Thread 1: holds read lock on A, requests write lock on A (upgrade)
           -> blocks because Thread 2 holds read lock on A
Thread 2: holds read lock on A, requests write lock on A (upgrade)
           -> blocks because Thread 1 holds read lock on A
```

In GDB, RwLock deadlocks show up as threads blocked in `pthread_rwlock_wrlock`
with the lock's reader count > 0.

### Async Runtime "Deadlocks"

In async Rust (Tokio, async-std), deadlocks can occur without any visible mutex
contention. All worker threads show `epoll_wait` (idle), but tasks are not
making progress.

The "lock" is implicit: task A is awaiting a channel message that task B should
send, but task B is awaiting something that task A should produce. This is a
cycle in the task dependency graph.

**How to diagnose in GDB**: you cannot see the task dependency graph from
backtraces. Instead:

1. Use `tokio-console` if the binary was built with the `console` feature.
2. Look at channel states: find the mpsc/oneshot channel objects in memory and
   check if data is queued.
3. If a tokio-runtime-worker thread is **not** in `epoll_wait` but in
   `futex_wait` or a blocking syscall, that thread is blocking the runtime --
   this is the most common cause of async "deadlock."

---

## 6. Async Runtime Debugging (Tokio/async-std)

### How Async Rust Works at the Machine Level

When you write `async fn`, the compiler transforms the function body into a
state machine implemented as an enum. Each `.await` point becomes a variant of
that enum. The state machine implements the `Future` trait with a `poll` method
that the runtime calls.

In GDB, an async function's local state is stored in the future's enum variant.
The backtrace typically shows:

```
#0  epoll_wait (...)
#1  mio::poll::Poll::poll (...)
#2  tokio::runtime::io::driver::Driver::turn (...)
#3  tokio::runtime::driver::Driver::park (...)
#4  tokio::runtime::scheduler::multi_thread::worker::Context::park (...)
#5  tokio::runtime::scheduler::multi_thread::worker::run (...)
```

This is a **healthy** worker thread waiting for I/O events. The actual
application code is not visible because the worker is idle.

When a worker is executing a task, the backtrace shows the future's poll chain:

```
#0  my_app::handle_request::{{closure}} (...)
#1  <my_app::handle_request::{{closure}} as core::future::future::Future>::poll (...)
#2  tokio::runtime::task::harness::poll_future (...)
#3  tokio::runtime::scheduler::multi_thread::worker::Context::run_task (...)
```

### Thread Naming Conventions

| Thread name | What it does |
|-------------|-------------|
| `tokio-runtime-worker` | Core executor thread, runs async tasks |
| `tokio-runtime-worker-N` | Same, with an index |
| `blocking-N` | Thread from `spawn_blocking()` pool, allowed to block |
| `actix-rt:worker:N` | Actix-web worker (also Tokio-based) |

### Diagnosing Task Starvation

If all `tokio-runtime-worker` threads are in `epoll_wait` but pending requests
are not being processed, tasks are starved. Common causes:

1. **Blocking call on a runtime thread**: a task called a blocking function
   (file I/O, DNS resolution, `std::sync::Mutex::lock`) without using
   `spawn_blocking()`.

2. **CPU-intensive computation**: a task performs a long computation without
   yielding.

3. **Too many tasks**: the runtime's queue is full and tasks can't be scheduled.

**How to find blocking calls in GDB:**

```bash
gdb --batch \
    -ex "thread apply all bt" \
    -p PID 2>&1 | tee /tmp/async_debug.log
```

Look for `tokio-runtime-worker` threads that are NOT in `epoll_wait`:

```
Thread 5 "tokio-runtime-w" (LWP 54321):
#0  __lll_lock_wait () at lowlevellock.S:135
#1  pthread_mutex_lock (...)
#2  std::sys::sync::mutex::pthread_mutex::PthreadMutex::lock (...)
#3  std::sync::mutex::Mutex<T>::lock (...)
#4  my_app::database::get_connection (...)  # <-- BUG: blocking mutex on async thread
```

This is a bug. The `std::sync::Mutex::lock` call blocks the entire runtime
thread. The fix is to use `tokio::sync::Mutex` or move the blocking call to
`spawn_blocking()`.

### Interpreting Async Backtraces

The state machine enum variants encode which `.await` point the future is at:

```
(gdb) print *future
$1 = my_app::handle_request::{{closure}}::variant3 {
    __awaitee = tokio::time::sleep::{{closure}}::variant1 { ... },
    request = Request { ... },
    response_builder = ResponseBuilder { ... },
}
```

`variant3` means the future is at the 3rd `.await` point in the function body.
The `__awaitee` field shows what it's currently awaiting.

### Channel Debugging

Tokio channels (`mpsc`, `oneshot`, `broadcast`) have internal state you can
examine:

```
(gdb) # For an mpsc channel, find the sender/receiver objects
(gdb) # The internal state includes:
(gdb) #   - Message queue (how many messages are buffered)
(gdb) #   - Whether sender/receiver are dropped
(gdb) #   - Waker state

# For a oneshot channel:
(gdb) print *oneshot_receiver
# Look for the state field: Empty, Filled, or Closed
```

### Naming Tasks for Debugging

Naming tasks makes GDB output much more useful:

```rust
// Instead of:
tokio::spawn(handle_request(req));

// Use:
tokio::task::Builder::new()
    .name(&format!("handle-req-{}", req.id))
    .spawn(handle_request(req));
```

### Tokio Console

`tokio-console` provides real-time introspection of the Tokio runtime. It
requires the `console-subscriber` crate and the `tokio_unstable` cfg flag:

```bash
# In Cargo.toml:
# [dependencies]
# console-subscriber = "0.1"

# Build with tokio_unstable:
RUSTFLAGS="--cfg tokio_unstable" cargo build

# In main():
# console_subscriber::init();

# Then run:
tokio-console
```

This shows all tasks, their states, poll times, and waker statistics. For
production debugging, it is often more useful than GDB for async issues.

### Timer Debugging

Tokio stores timers in a hierarchical timing wheel. If a timer is created but
never fires, it may be because:

1. The runtime's time driver is not being polled (blocked runtime thread)
2. The timer was created with an incorrect duration
3. The timer's future was dropped before it completed

In GDB, you can find the timer wheel in the runtime's driver state and examine
registered timers, but this requires deep knowledge of Tokio internals and
varies by version. The `tokio-console` approach is usually more practical.

### Complete Async Debugging Workflow

```bash
#!/bin/bash
# Async Rust debugging workflow
PID=$1
LOG="/tmp/async_debug_$(date +%s).log"

echo "=== Async Runtime Debug ===" | tee "$LOG"

# 1. Get all thread backtraces
gdb --batch \
    -ex "thread apply all bt" \
    -p "$PID" 2>&1 | tee -a "$LOG"

# 2. Categorize threads with Python
gdb --batch \
    -ex "python
import gdb
workers_idle = []
workers_busy = []
blocking = []
other = []
for t in gdb.selected_inferior().threads():
    t.switch()
    f = gdb.newest_frame()
    name = t.name or ''
    top = f.name() if f else '?'
    if 'runtime-worker' in name or 'runtime-w' in name:
        if 'epoll_wait' in (top or ''):
            workers_idle.append((t.num, name, top))
        else:
            workers_busy.append((t.num, name, top))
    elif 'blocking' in name:
        blocking.append((t.num, name, top))
    else:
        other.append((t.num, name, top))

print(f'\\nIdle workers: {len(workers_idle)}')
print(f'Busy workers: {len(workers_busy)}')
print(f'Blocking pool: {len(blocking)}')
print(f'Other: {len(other)}')
if workers_busy:
    print(f'\\n*** BUSY WORKERS (potential blockers): ***')
    for num, name, top in workers_busy:
        print(f'  Thread {num} [{name}]: {top}')
" \
    -ex "quit" \
    -p "$PID" 2>&1 | tee -a "$LOG"
```

---

## 7. Container and Namespace Debugging

### Docker: Enabling ptrace

By default, Docker's seccomp profile blocks `ptrace()`, which GDB requires.
You must explicitly enable it:

```bash
# Option 1: Add SYS_PTRACE capability (recommended)
docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined myimage

# Option 2: Run privileged (grants ALL capabilities -- use only for debugging)
docker run --privileged myimage

# Option 3: Custom seccomp profile that allows ptrace
# (create a JSON seccomp profile with ptrace whitelisted)
```

### Debugging Inside a Running Container

```bash
# Install GDB inside the container (if not present)
docker exec -it CONTAINER bash -c "apt-get update && apt-get install -y gdb"

# Attach to the main process (PID 1 inside the container)
docker exec -it CONTAINER gdb --batch \
    -ex "thread apply all bt" \
    -p 1 2>&1 | tee /tmp/container_debug.log

# If process is not PID 1, find it first:
docker exec -it CONTAINER ps aux
docker exec -it CONTAINER gdb --batch \
    -ex "thread apply all bt full" \
    -p TARGET_PID
```

### Debugging from the Host with nsenter

`nsenter` enters the namespaces of a containerized process, letting you run
GDB from the host system without installing anything inside the container:

```bash
# Step 1: Find the container's PID on the host
CONTAINER_PID=$(docker inspect --format '{{.State.Pid}}' CONTAINER_NAME)
echo "Container PID on host: $CONTAINER_PID"

# Step 2: Enter its namespaces and run GDB
# -m: mount namespace (see container's filesystem)
# -u: UTS namespace (hostname)
# -i: IPC namespace
# -n: network namespace
# -p: PID namespace
nsenter -t $CONTAINER_PID -m -u -i -n -p \
    gdb --batch \
    -ex "thread apply all bt" \
    -p 1

# Or: attach from host directly (no namespace entry needed for ptrace,
# but you need the HOST PID, not the container PID)
gdb --batch \
    -ex "thread apply all bt" \
    -p $CONTAINER_PID
```

### PID Namespace Confusion

A process has different PIDs in different namespaces:

```bash
# Inside the container:
$ ps aux
PID 1    my_server

# On the host:
$ docker inspect --format '{{.State.Pid}}' mycontainer
45678

# Verify with NSpid field:
$ cat /proc/45678/status | grep NSpid
NSpid:  45678   1
#       ^host   ^container
```

When using GDB from the host, use the host PID (45678).
When using GDB inside the container, use the container PID (1).

### Kubernetes Debugging

**Option 1: Add SYS_PTRACE capability in the pod spec**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: debug-pod
spec:
  containers:
  - name: app
    image: myimage
    securityContext:
      capabilities:
        add: ["SYS_PTRACE"]
```

**Option 2: Ephemeral debug container (Kubernetes 1.23+)**

This attaches a new container to a running pod. The debug container shares the
process namespace of the target container:

```bash
# Attach a debug container with GDB
kubectl debug -it POD_NAME \
    --image=ubuntu:22.04 \
    --target=CONTAINER_NAME \
    -- bash

# Inside the debug container:
apt-get update && apt-get install -y gdb
# Find the process:
ps aux
# Attach:
gdb --batch -ex "thread apply all bt" -p TARGET_PID
```

**Option 3: kubectl exec (if GDB is in the image)**

```bash
kubectl exec -it POD_NAME -c CONTAINER_NAME -- \
    gdb --batch -ex "thread apply all bt" -p 1
```

### Rootless Containers

Rootless containers (Podman rootless, Docker rootless) block ptrace entirely
by default. Options:

```bash
# Podman rootless with ptrace
podman run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined myimage

# If that doesn't work, you may need:
podman run --privileged myimage
```

### /proc Access Without ptrace

Many useful debugging operations work through `/proc` without needing ptrace:

```bash
# Memory maps (no ptrace needed)
cat /proc/PID/maps

# Open file descriptors
ls -la /proc/PID/fd/

# Stack trace (if /proc/PID/stack is readable)
cat /proc/PID/stack

# Syscall being executed
cat /proc/PID/syscall

# Process status, threads, etc.
cat /proc/PID/status
ls /proc/PID/task/

# Memory usage breakdown
cat /proc/PID/smaps_rollup
```

### Complete Container Debug Recipe

```bash
#!/bin/bash
# Debug a process inside a Docker container
CONTAINER="$1"
PROCESS="${2:-1}"  # Default to PID 1

echo "=== Container Debug: $CONTAINER, PID $PROCESS ==="

# Get host PID
HOST_PID=$(docker inspect --format '{{.State.Pid}}' "$CONTAINER")
echo "Host PID: $HOST_PID"

# Check if ptrace is allowed
if nsenter -t "$HOST_PID" -m -p cat /proc/1/status > /dev/null 2>&1; then
    echo "nsenter access: OK"
else
    echo "ERROR: Cannot enter container namespace. Is SYS_PTRACE enabled?"
    exit 1
fi

# Get thread backtraces
echo "=== Thread Backtraces ==="
nsenter -t "$HOST_PID" -m -u -i -n -p \
    gdb --batch \
    -ex "thread apply all bt" \
    -p "$PROCESS" 2>&1

# Get memory maps
echo "=== Memory Maps ==="
cat /proc/"$HOST_PID"/maps

# Get open files
echo "=== Open Files ==="
ls -la /proc/"$HOST_PID"/fd/ 2>/dev/null
```

---

## 8. Disassembly Analysis for Optimized Code

### When You Need This

Release-mode binaries (Rust's `--release`, C's `-O2`/`-O3`) apply aggressive
optimizations: function inlining, loop unrolling, dead code elimination, link-time
optimization (LTO). This means:

- Backtraces show `??` for inlined functions
- Frame names are misleading (the "function" shown may be an inliner)
- Variables are optimized out: `(gdb) print x` -> `<optimized out>`
- Source line information is approximate

In these cases, you must read the assembly to understand what actually happened.

### Essential GDB Commands

```
# Disassemble the current function
(gdb) disas
# or with source interleaved (if debug info available):
(gdb) disas /s

# Disassemble N instructions from a specific address
(gdb) x/20i $pc           # 20 instructions from current position
(gdb) x/20i $pc-40        # context around crash point (before and after)
(gdb) x/50i function_name  # disassemble a named function

# Show current instruction with surrounding context
(gdb) x/5i $pc-10
(gdb) x/5i $pc

# Disassemble a specific address range
(gdb) disas 0x401000, 0x401100
```

### x86_64 System V ABI (Calling Convention)

Understanding the calling convention is essential for reading disassembly:

**Argument passing (integer/pointer arguments):**

| Argument # | Register |
|------------|----------|
| 1st | `rdi` |
| 2nd | `rsi` |
| 3rd | `rdx` |
| 4th | `rcx` |
| 5th | `r8` |
| 6th | `r9` |
| 7th+ | stack |

**Floating-point arguments**: `xmm0` through `xmm7`

**Return value**: `rax` (and `rdx` for 128-bit returns)

**Callee-saved registers** (function must preserve these): `rbx`, `rbp`, `r12`,
`r13`, `r14`, `r15`

**Caller-saved registers** (function may clobber these): `rax`, `rcx`, `rdx`,
`rsi`, `rdi`, `r8`, `r9`, `r10`, `r11`

**Stack pointer**: `rsp` (16-byte aligned before `call` instruction)

### Reading Crash Disassembly

**NULL pointer dereference:**

```
=> 0x401234: mov    (%rax),%rdx
```

If `rax = 0`, this is a NULL pointer dereference. The instruction tries to load
the value at the address in `rax` (which is 0) into `rdx`.

```
(gdb) info registers rax
rax    0x0    0
```

**Use-after-free:**

```
=> 0x401234: mov    0x10(%rax),%rdx
```

`rax` points to freed memory. The instruction loads from offset `0x10` into the
struct, but the struct has been freed and the memory may be reused.

```
(gdb) info registers rax
rax    0x55a3f000    # Points to freed heap memory
(gdb) x/4gx 0x55a3f000
# May show free list pointers instead of valid struct data
```

**Vtable / function pointer corruption:**

```
=> 0x401234: call   *%rax
```

An indirect call through `rax`. If `rax` contains garbage, this is a corrupted
function pointer or vtable entry.

```
(gdb) info registers rax
rax    0x4141414141414141    # 'AAAAAAAA' -- obvious buffer overflow
```

**Buffer overflow detection in assembly:**

```
# Stack canary check (GCC -fstack-protector):
mov    %fs:0x28,%rax       # Load canary from TLS
mov    %rax,-0x8(%rbp)     # Store on stack
... (function body) ...
mov    -0x8(%rbp),%rax     # Reload canary
xor    %fs:0x28,%rax       # Compare with original
jne    __stack_chk_fail    # If different, stack was smashed
```

### Finding Source from Addresses

```bash
# addr2line: map addresses to source lines
addr2line -e ./binary -f 0x401234
# Output:
# function_name
# /path/to/source.c:42

# With inlined function chain:
addr2line -e ./binary -f -i 0x401234
# Shows the full inline chain

# For Rust binaries with debug info:
addr2line -e target/debug/binary -f -i 0x401234
```

### objdump for Offline Analysis

```bash
# Full disassembly with source interleaving (requires debug info)
objdump -d -S ./binary | less

# Just disassembly, no source
objdump -d ./binary | less

# Disassemble a specific section
objdump -d -j .text ./binary

# Show all symbols
objdump -t ./binary | sort

# Show dynamic symbols (shared library imports)
objdump -T ./binary
```

### Split Debug Info

Many distributions and build systems separate debug info from the binary:

```bash
# Check if binary has debug info
objdump -h ./binary | grep debug
# If no output, debug info is not embedded

# Find separate debug file
# Method 1: .gnu_debuglink section
objdump -s -j .gnu_debuglink ./binary
# Shows the filename of the separate debug file

# Method 2: build-id
readelf -n ./binary | grep "Build ID"
# Build ID: 0x1234abcd...
# Debug file location: /usr/lib/debug/.build-id/12/34abcd....debug

# Method 3: search standard locations
find /usr/lib/debug/ -name "$(basename ./binary).debug" 2>/dev/null

# Load separate debug info in GDB
(gdb) set debug-file-directory /usr/lib/debug
# GDB searches this directory automatically

# Or manually:
(gdb) symbol-file /path/to/binary.debug
```

### Rust-Specific Disassembly Notes

Rust function names are mangled. Use `rustfilt` to demangle:

```bash
# Demangle Rust symbols in objdump output
objdump -d ./binary | rustfilt | less

# Or in GDB:
(gdb) set print demangle on
(gdb) set print asm-demangle on
```

Rust's `Option` and `Result` are compiled as enums with discriminants. In
optimized code, `Option<&T>` uses NULL as the `None` discriminant (niche
optimization), so a NULL pointer in the assembly might actually be a legitimate
`None` value rather than a bug.

### Batch Mode Disassembly at Crash

```bash
gdb --batch \
    -ex "run" \
    -ex "bt" \
    -ex "x/10i \$pc-20" \
    -ex "x/10i \$pc" \
    -ex "info registers" \
    -ex "print/x \$_siginfo._sifields._sigfault.si_addr" \
    -ex "quit" \
    --args ./binary 2>&1 | tee /tmp/crash_disas.log
```

---

## 9. Multi-Process Debugging

### Following Forks

By default, GDB follows the parent when a process forks. To follow the child:

```
(gdb) set follow-fork-mode child
(gdb) run
# GDB now attaches to the child process after fork()
```

### Debugging Both Parent and Child

```
(gdb) set detach-on-fork off
(gdb) run
# After fork(), both processes are controlled by GDB
# The parent is paused, child is running (or vice versa depending on follow-fork-mode)

(gdb) info inferiors
  Num  Description       Connection           Executable
* 1    process 12345     1 (native)           /path/to/binary
  2    process 12346     1 (native)           /path/to/binary

(gdb) inferior 2    # Switch to child
(gdb) bt           # See child's backtrace
(gdb) inferior 1    # Switch back to parent
```

### Fork + Exec Debugging

When a process forks and then execs a different binary:

```
(gdb) set follow-fork-mode child
(gdb) set follow-exec-mode new
# After exec(), GDB creates a new inferior for the exec'd program

# Or to stop at exec:
(gdb) catch exec
(gdb) run
# GDB stops when exec() is called
```

### Batch Mode with Forks

Following forks in batch mode is tricky because you cannot interactively switch
inferiors. The best approach is usually to attach separate GDB instances:

```bash
# Strategy 1: Follow child in batch mode
gdb --batch \
    -ex "set follow-fork-mode child" \
    -ex "run" \
    -ex "bt full" \
    -ex "quit" \
    --args ./server 2>&1 | tee /tmp/child_debug.log

# Strategy 2: Use the parent GDB to find the child PID, then attach separately
# In terminal 1:
gdb --batch \
    -ex "set detach-on-fork off" \
    -ex "catch fork" \
    -ex "run" \
    -ex "quit" \
    --args ./server 2>&1 | tee /tmp/fork_pid.log
# Note: GDB prints the child PID in its "catch fork" output, e.g.:
#   "Catchpoint 1 (forked process 12345)"

# Then in terminal 2:
CHILD_PID=$(grep -oP 'forked process \K[0-9]+' /tmp/fork_pid.log)
gdb --batch -ex "bt full" -p $CHILD_PID
```

### Real Use Case: Debugging a Forking Server

Many servers (nginx, Apache, PostgreSQL) fork worker processes:

```bash
# Debug the master process:
gdb --batch \
    -ex "break accept" \
    -ex "run" \
    -ex "bt" \
    -ex "quit" \
    --args ./server

# Debug a worker after it's been forked:
# Step 1: Start the server normally
./server &
SERVER_PID=$!

# Step 2: Find worker PIDs
pgrep -P $SERVER_PID

# Step 3: Attach to a specific worker
gdb --batch \
    -ex "thread apply all bt" \
    -p WORKER_PID
```

---

## 10. Remote Debugging with gdbserver

### When to Use

- The target system doesn't have a full GDB installation (embedded, minimal
  containers, IoT devices)
- You need to debug with symbols that are only available on the host
- The target system has limited storage/memory for a full GDB

### Starting gdbserver

```bash
# Start a new process under gdbserver
gdbserver :9999 ./binary arg1 arg2

# Attach to a running process
gdbserver --attach :9999 $PID

# Use a named pipe instead of TCP (for local debugging)
gdbserver /tmp/gdb.pipe ./binary

# Multi-process mode (keeps listening for new connections)
gdbserver --multi :9999
```

### Connecting from GDB

```bash
# On the host machine:
gdb ./binary
(gdb) target remote TARGET_HOST:9999
(gdb) continue
# ... debugging session ...

# For batch mode:
gdb --batch \
    -ex "target remote TARGET_HOST:9999" \
    -ex "continue" \
    -ex "bt full" \
    -ex "thread apply all bt" \
    -ex "detach" \
    ./binary 2>&1 | tee /tmp/remote_debug.log
```

### SSH Tunneling

If the target is behind a firewall:

```bash
# On the host: create an SSH tunnel
ssh -L 9999:localhost:9999 user@target_host

# On the target: start gdbserver on localhost only (for security)
gdbserver localhost:9999 ./binary

# On the host: connect through the tunnel
gdb --batch \
    -ex "target remote localhost:9999" \
    -ex "continue" \
    -ex "bt full" \
    -ex "detach" \
    ./binary
```

### gdbserver in Docker

Useful for debugging inside containers from a host GDB with full symbol
resolution:

```bash
# Inside the container: start gdbserver
docker exec -d CONTAINER gdbserver :9999 --attach 1

# On the host: connect with full symbols
gdb --batch \
    -ex "set sysroot /path/to/container/rootfs" \
    -ex "target remote CONTAINER_IP:9999" \
    -ex "thread apply all bt" \
    -ex "detach" \
    ./binary_with_debug_symbols

# Or use Docker's port mapping:
docker run -p 9999:9999 --cap-add=SYS_PTRACE myimage \
    gdbserver :9999 ./binary
```

### Symbol Resolution for Remote Debugging

The host GDB needs access to the same binary and shared libraries as the target.
Options:

```
(gdb) set sysroot /path/to/target/rootfs
# GDB looks for shared libraries relative to this path

(gdb) set solib-search-path /path/to/target/libs
# Additional search paths for shared libraries

(gdb) symbol-file /path/to/binary.debug
# Load symbols from a separate file
```

### Batch Remote Debugging Recipe

```bash
#!/bin/bash
# Remote debug a process on a target machine
TARGET_HOST="$1"
TARGET_PID="$2"
BINARY_PATH="$3"  # Local path to the binary with debug symbols

LOG="/tmp/remote_debug_$(date +%s).log"

# Start gdbserver on the target
ssh "$TARGET_HOST" "gdbserver :9999 --attach $TARGET_PID &" &
sleep 2

# Connect and debug
gdb --batch \
    -ex "target remote ${TARGET_HOST}:9999" \
    -ex "thread apply all bt full" \
    -ex "info threads" \
    -ex "thread apply all info locals" \
    -ex "detach" \
    "$BINARY_PATH" 2>&1 | tee "$LOG"

echo "Debug log: $LOG"
```

---

## 11. Race Condition Systematic Diagnosis

### Why Races Are Hard

Race conditions are the hardest class of bugs because:

1. They depend on timing, which changes between runs
2. Adding instrumentation (logging, printf) changes timing, potentially hiding
   the race
3. Running under GDB changes timing (GDB adds overhead, changes scheduling)
4. They may only manifest under specific load patterns

### Systematic Approach

Do not guess. Follow this systematic process:

**Phase 1: Detection with TSAN**

```bash
# Build with ThreadSanitizer
gcc -fsanitize=thread -g -O1 -o binary source.c
# or
RUSTFLAGS="-Zsanitizer=thread" cargo +nightly build --target x86_64-unknown-linux-gnu

# Run normally -- TSAN reports data races
./binary 2>&1 | tee /tmp/tsan_report.log
```

TSAN catches most data races at the source level. It reports:
- The two conflicting accesses (with backtraces)
- Whether they are reads or writes
- The thread IDs involved

**Phase 2: Reliable Reproduction with rr**

If TSAN finds a race, or if you have a symptom without TSAN:

```bash
# Record with chaos mode to vary scheduling
for i in $(seq 1 20); do
    rr record --chaos ./binary 2>&1 | tee /tmp/rr_attempt_$i.log
    if [ $? -ne 0 ]; then
        echo "Failure reproduced on attempt $i"
        break
    fi
done
```

Chaos mode introduces scheduling perturbations that make races more likely to
manifest.

**Phase 3: Root Cause Analysis with rr Replay**

```bash
# Replay the recorded failure
rr replay \
    -ex "continue" \
    -ex "watch *(long*)CONTESTED_ADDRESS" \
    -ex "reverse-continue" \
    -ex "bt full" \
    -ex "info locals" \
    -ex "quit" 2>&1 | tee /tmp/rr_analysis.log
```

With the watchpoint at the contested address, `reverse-continue` finds both
writers. Examine each writer's context to understand the access pattern.

**Phase 4: Design the Fix**

Based on the access pattern:
- **Unprotected shared state**: add a mutex or use atomics
- **Missing synchronization on initialization**: use `std::sync::Once` / `pthread_once`
- **Lock ordering violation**: establish and document a global lock ordering
- **Incorrect atomic ordering**: strengthen the memory ordering (e.g., `Relaxed` to `AcqRel`)

### GDB-Specific Techniques

**Scheduler-locking: freeze all threads except current**

```
(gdb) set scheduler-locking on
# Only the current thread runs when you step
(gdb) step    # steps one thread, all others frozen
(gdb) set scheduler-locking off
# All threads resume when you continue
```

This is invaluable for race reproduction: manually interleave thread execution
to trigger the race.

**Thread-specific breakpoints:**

```
(gdb) break critical_function thread 3
# This breakpoint only fires for thread 3

(gdb) break update_state thread 2 if counter > 100
# Fires only for thread 2 when counter > 100
```

**Non-stop mode:**

```
(gdb) set non-stop on
(gdb) set target-async on
# Now when one thread hits a breakpoint, other threads continue
# This is closer to the real scheduling behavior
(gdb) interrupt -a  # Stop all threads
```

### The "Schedule-Locked Step" Technique

To reproduce a race manually:

1. Set breakpoints at both racing code paths
2. Run until one thread hits a breakpoint
3. Enable scheduler-locking
4. Step that thread to just before the write
5. Switch to the other thread
6. Step it to just before its write
7. Now alternate steps between threads to trigger the race in a controlled way

```
(gdb) break writer_a thread 2
(gdb) break writer_b thread 3
(gdb) continue
# Thread 2 hits breakpoint

(gdb) set scheduler-locking on
(gdb) next   # advance thread 2 one step
(gdb) thread 3
(gdb) next   # advance thread 3 one step
# Now thread 2 and thread 3 are both at their critical sections
(gdb) thread 2
(gdb) next   # thread 2 writes
(gdb) thread 3
(gdb) next   # thread 3 writes -- race triggered!
```

### Complete Race Diagnosis Workflow Script

```bash
#!/bin/bash
# Systematic race condition diagnosis
BINARY="$1"
shift

echo "=== Phase 1: TSAN Analysis ==="
# Build with TSAN (assumes Makefile or similar)
TSAN_BINARY="${BINARY}.tsan"
gcc -fsanitize=thread -g -O1 -o "$TSAN_BINARY" $(find . -name "*.c") -lpthread
if [ $? -eq 0 ]; then
    "$TSAN_BINARY" "$@" 2>&1 | tee /tmp/tsan_report.log
    echo "TSAN report: /tmp/tsan_report.log"
fi

echo ""
echo "=== Phase 2: rr Record (chaos mode, up to 10 attempts) ==="
for i in $(seq 1 10); do
    timeout 60 rr record --chaos "$BINARY" "$@" 2>&1 | tee "/tmp/rr_attempt_$i.log"
    EXIT=$?
    if [ $EXIT -ne 0 ] && [ $EXIT -ne 124 ]; then
        echo "Failure on attempt $i"
        echo ""
        echo "=== Phase 3: rr Replay ==="
        rr replay \
            -ex "continue" \
            -ex "bt full" \
            -ex "thread apply all bt full" \
            -ex "info threads" \
            -ex "quit" \
            2>&1 | tee /tmp/rr_replay.log
        echo "Replay log: /tmp/rr_replay.log"
        break
    fi
done
```

---

## 12. Performance-Sensitive Debugging

### Understanding GDB's Overhead

When GDB attaches to a process, it:

1. Sends `SIGSTOP` to all threads (they freeze for 10-100ms typically)
2. Reads `/proc/PID/maps` and loads symbol tables
3. Each command that reads memory (`bt`, `print`, `info locals`) issues
   `ptrace(PTRACE_PEEKDATA, ...)` calls, each of which is a context switch

**Minimize overhead:**

```bash
# Fast: minimal backtrace (only top 5 frames, no local variables)
gdb --batch -ex "thread apply all bt 5" -p PID -ex "detach"

# Slow: full backtrace with all locals (reads entire stack for every thread)
gdb --batch -ex "thread apply all bt full" -p PID -ex "detach"

# Very slow: info locals for all threads (reads all stack variables)
gdb --batch -ex "thread apply all info locals" -p PID -ex "detach"
```

For production systems, prefer `bt 5` or `bt 10` over `bt full`. Only use
`bt full` or `info locals` when you need the extra detail and can tolerate
the pause.

### perf + GDB Correlation

Use `perf` to find the hot spot, then use GDB to examine it:

```bash
# Step 1: Profile to find hot functions
perf record -g -p PID -- sleep 10
perf report --stdio | head -50
# Output shows: 35% cpu in process_request()

# Step 2: Set targeted GDB breakpoint only at the hot function
gdb --batch \
    -ex "break process_request if iteration_count > 1000000" \
    -ex "commands 1" \
    -ex "  bt 5" \
    -ex "  info locals" \
    -ex "  detach" \
    -ex "end" \
    -ex "continue" \
    -p PID
```

### eBPF/bpftrace: Zero-Overhead Alternative

bpftrace can trace function calls without stopping the process:

```bash
# Trace a specific function's arguments (no stop, no ptrace)
bpftrace -e 'uprobe:/path/to/binary:process_request {
    printf("called with arg1=%d, arg2=%s\n", arg0, str(arg1));
}'

# Count how many times each function is called (sampling)
bpftrace -e 'uprobe:/path/to/binary:* {
    @calls[func] = count();
}'

# Measure function latency
bpftrace -e '
uprobe:/path/to/binary:process_request { @start[tid] = nsecs; }
uretprobe:/path/to/binary:process_request {
    if (@start[tid]) {
        @latency_us = hist((nsecs - @start[tid]) / 1000);
        delete(@start[tid]);
    }
}'

# Trace all malloc calls over 1MB
bpftrace -e 'uprobe:/lib/x86_64-linux-gnu/libc.so.6:malloc /arg0 > 1048576/ {
    printf("malloc(%d) from:\n", arg0);
    print(ustack);
}'
```

bpftrace advantages over GDB for performance debugging:
- Does not stop the process
- Near-zero overhead for simple probes
- Can aggregate data (histograms, counts) in-kernel
- Works in production

bpftrace disadvantages:
- Cannot inspect complex data structures
- Cannot modify program state
- Requires root (or CAP_BPF + CAP_PERFMON)
- Probe expressions are limited compared to GDB's Python scripting

### perf probe for Dynamic Tracing

`perf probe` creates tracepoints at arbitrary locations without GDB:

```bash
# Add a probe at function entry
perf probe -x ./binary 'process_request'

# Add a probe with argument capture
perf probe -x ./binary 'process_request size=%di'

# Add a probe at a specific source line
perf probe -x ./binary 'source.c:42'

# Record events from the probe
perf record -e probe_binary:process_request -p PID -- sleep 10
perf script  # Show all captured events

# Remove the probe
perf probe -d probe_binary:process_request
```

### SystemTap for Kernel + Userspace Analysis

When you need to correlate kernel events with userspace behavior:

```bash
# Trace all write() syscalls from a specific process with backtraces
stap -e '
probe process("/path/to/binary").function("write_data") {
    printf("write_data called from:\n%s\n", sprint_ubacktrace())
}
probe kernel.function("vfs_write") {
    if (pid() == target()) {
        printf("vfs_write: fd=%d, count=%d\n", $fd, $count)
    }
}
' -x PID
```

### Choosing the Right Tool

| Scenario | Tool | Why |
|----------|------|-----|
| Crash analysis | GDB | Full state inspection |
| Memory corruption | ASAN + GDB | ASAN finds it, GDB examines it |
| Race conditions | TSAN + rr | TSAN detects, rr reproduces |
| Performance profiling | perf | Lowest overhead sampling |
| Function tracing | bpftrace | Zero-stop overhead |
| Deadlock analysis | GDB + Python scripts | Need to inspect lock state |
| Post-mortem (core dump) | GDB | Full state preserved in core |
| Production monitoring | bpftrace / perf | Cannot stop production |
| Reverse debugging | rr | Only tool that does this |
| Container debugging | GDB + nsenter | Namespace-aware attachment |

### Combining Tools in a Debugging Session

A real-world debugging session often chains multiple tools:

```bash
# 1. perf says 40% of CPU in process_request
perf record -g -p PID -- sleep 30
perf report --stdio 2>&1 | tee /tmp/perf.log

# 2. bpftrace shows the slow calls have arg1 > 10000
bpftrace -e 'uprobe:./binary:process_request /arg0 > 10000/ {
    @slow = count();
    printf("slow call: arg0=%d\n", arg0);
}' 2>&1 | tee /tmp/bpf.log

# 3. GDB examines the state during a slow call
gdb --batch \
    -ex "break process_request if request_size > 10000" \
    -ex "commands 1" \
    -ex "  bt 10" \
    -ex "  info locals" \
    -ex "  continue" \
    -ex "end" \
    -ex "continue" \
    -p PID 2>&1 | tee /tmp/gdb_slow.log

# 4. Found a quadratic algorithm -- profile confirms with perf annotate
perf annotate process_request 2>&1 | tee /tmp/perf_annotate.log
```

---

## Cross-Reference: Technique Integration

The techniques in this document are most powerful when combined. Here is how
they interconnect:

| Starting Point | Next Step | Tool Chain |
|----------------|-----------|------------|
| Crash in production | Get core dump, analyze | GDB batch → core dump analysis → disassembly |
| Intermittent crash | Record and replay | rr record --chaos → rr replay → watchpoint → reverse-continue |
| Data race suspected | Detect then reproduce | TSAN build → rr record --chaos → rr replay → watchpoint |
| Deadlock | Prove it | GDB attach → thread backtraces → Python mutex graph → cycle detection |
| Performance regression | Profile then inspect | perf record → bpftrace → GDB conditional breakpoint |
| Memory corruption | Sanitize then trace | ASAN build → GDB with abort_on_error → heap metadata inspection |
| Container issue | Namespace-aware debug | nsenter/kubectl debug → GDB batch → thread categorization |
| Optimized binary crash | Assembly analysis | GDB disas → addr2line → split debug info → register analysis |
| Async starvation | Runtime inspection | GDB thread categorize → find blocked workers → channel state |

Every diagnostic session should start with the lowest-overhead tool that can
answer the immediate question, and escalate to more invasive tools only when
needed. perf and bpftrace for understanding the shape of the problem; GDB and
rr for understanding the exact cause.
