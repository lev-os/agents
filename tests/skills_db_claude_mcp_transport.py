"""One-agent Claude stdio MCP transport for the skills-db evaluation adapter.

This module records protocol and delivery facts. It does not decide whether a
skill applied, was used, or improved an outcome.
"""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
import hashlib
import io
import json
import math
import os
import queue
import selectors
import signal
import subprocess
import threading
import time
from pathlib import Path
from typing import Any, BinaryIO, Callable

try:
    from skills_db_agent_controller import AdmissionError, BudgetLimits, ProtocolError, SkillsCliProfile, ScriptedSkillsController
except ModuleNotFoundError:  # imported as tests.skills_db_claude_mcp_transport
    from tests.skills_db_agent_controller import AdmissionError, BudgetLimits, ProtocolError, SkillsCliProfile, ScriptedSkillsController


SERVER_NAME = "skills-db"
SERVER_VERSION = "0.1.0"
MAX_FRAME_BYTES = 1_048_576
MAX_PENDING = 8
TOOLS = ("tree", "browse", "discover", "get", "read_path", "read_chunks")
LIVE_RUNTIME_ROOT = Path.home() / ".local/state/lev/skills-db-progressive-discovery/finish-20261017T083107Z/live-agent-coder"


class MCPTransportError(RuntimeError):
    pass


class MCPDeadlineError(MCPTransportError):
    pass


def _no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _encode_frame(value: dict[str, Any]) -> bytes:
    return _json_text(value).encode("utf-8") + b"\n"


class DaemonExecutor:
    """Small bounded dispatcher whose workers cannot hold process shutdown open."""

    def __init__(self, max_workers: int):
        self.max_workers = max_workers
        self.lock = threading.Lock()
        self.threads: set[threading.Thread] = set()
        self.futures: set[Future[Any]] = set()

    def submit(self, function: Callable[..., Any], *args: Any) -> Future[Any]:
        future: Future[Any] = Future()
        with self.lock:
            if sum(thread.is_alive() for thread in self.threads) >= self.max_workers:
                raise RuntimeError("bounded MCP worker limit reached")
            self.futures.add(future)

        def run() -> None:
            if not future.set_running_or_notify_cancel():
                return
            try:
                future.set_result(function(*args))
            except BaseException as error:
                future.set_exception(error)
            finally:
                with self.lock:
                    self.futures.discard(future)

        thread = threading.Thread(target=run, name="skills-db-tool", daemon=True)
        with self.lock:
            self.threads.add(thread)
        thread.start()
        return future

    def shutdown(self, *, wait: bool = False, cancel_futures: bool = True) -> None:
        if cancel_futures:
            with self.lock:
                futures = list(self.futures)
            for future in futures:
                future.cancel()
        if wait:
            with self.lock:
                threads = list(self.threads)
            for thread in threads:
                thread.join()


def _cli_operation_overlap(records: list[dict[str, Any]], operations: set[str], *, profile_mode: str | None = None) -> bool:
    spans: dict[str, list[tuple[float, float]]] = {}
    for item in records:
        start, finish, pid, exit_code = (item.get("started_monotonic"), item.get("finished_monotonic"), item.get("pid"), item.get("exit_code"))
        argv = item.get("argv")
        if (
            isinstance(pid, bool)
            or not isinstance(pid, int)
            or pid <= 0
            or isinstance(exit_code, bool)
            or exit_code != 0
            or item.get("timed_out") is not False
            or item.get("status") != "ok"
            or not isinstance(argv, list)
            or not argv
            or argv[0] not in operations
            or profile_mode is not None and item.get("profile_mode") != profile_mode
            or isinstance(start, bool)
            or not isinstance(start, (int, float))
            or isinstance(finish, bool)
            or not isinstance(finish, (int, float))
            or not math.isfinite(float(start))
            or not math.isfinite(float(finish))
            or finish <= start
        ):
            continue
        spans.setdefault(argv[0], []).append((float(start), float(finish)))
    if len(spans) < 2:
        return False
    for operation, left_spans in spans.items():
        for other, right_spans in spans.items():
            if operation >= other:
                continue
            if any(max(a_start, b_start) < min(a_finish, b_finish) for a_start, a_finish in left_spans for b_start, b_finish in right_spans):
                return True
    return False


def actual_cli_overlap(records: list[dict[str, Any]]) -> bool:
    """Only successful current-public browse/discover process intervals count."""
    return _cli_operation_overlap(records, {"browse", "discover"}, profile_mode="current_public")


def tool_schemas() -> list[dict[str, Any]]:
    def schema(name: str, description: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
        return {
            "name": name,
            "description": description,
            "inputSchema": {"type": "object", "properties": properties, "required": required, "additionalProperties": False},
            "annotations": {"readOnlyHint": True},
            "_meta": {"anthropic/maxResultSizeChars": 262144},
        }

    source = {"source_id": {"type": "string", "minLength": 1}}
    return [
        schema("tree", "List admitted catalog collections or subjects.", {"view": {"type": "string", "enum": ["collections", "subjects"]}, "depth": {"type": "integer", "minimum": 0, "maximum": 20}}, ["view", "depth"]),
        schema("browse", "Browse one observed tree node. Use a small limit and cursor to page large rows.", {"node_id": {"type": "string"}, "limit": {"type": "integer", "minimum": 1, "maximum": 20}, "cursor": {"type": "string"}}, ["node_id"]),
        schema("discover", "Run one public CLI discovery query. Each query is admitted and charged separately.", {"query": {"type": "string", "minLength": 1, "maxLength": 4096}, "limit": {"type": "integer", "minimum": 1, "maximum": 20}}, ["query"]),
        schema("get", "Return a descriptor for one source that was already observed.", source, ["source_id"]),
        schema("read_path", "Read a complete observed source when it fits the reply cap.", source, ["source_id"]),
        schema("read_chunks", "Read an exact UTF-8 byte span from an observed source.", {**source, "start_byte": {"type": "integer", "minimum": 0}, "end_byte": {"type": "integer", "minimum": 1}}, ["source_id", "start_byte", "end_byte"]),
    ]


def build_claude_launch_profile(*, claude_binary: str, claude_sha256: str, claude_version: str, model: str, model_catalog_ref: str, system_prompt: str, task_text: str, mcp_config_path: str, working_directory: str) -> dict[str, Any]:
    """Verify the live binary and return one pinned, single-agent print launch."""
    if not isinstance(model, str) or not model.strip() or not isinstance(model_catalog_ref, str) or not model_catalog_ref.strip():
        raise MCPTransportError("an existing model and its live catalog reference are required")
    if not isinstance(claude_version, str) or not claude_version.strip() or not isinstance(claude_sha256, str) or len(claude_sha256) != 64:
        raise MCPTransportError("Claude binary version and SHA-256 are required")
    binary = Path(claude_binary).expanduser().resolve(strict=True)
    if not binary.is_file() or _sha256_file(binary) != claude_sha256:
        raise MCPTransportError("installed Claude binary does not match its admitted SHA-256")
    if not isinstance(system_prompt, str) or not isinstance(task_text, str):
        raise MCPTransportError("task and instruction must be text")
    schema_bytes = len(_json_text(tool_schemas()).encode("utf-8"))
    if len(system_prompt.encode("utf-8")) + len(task_text.encode("utf-8")) + schema_bytes > BudgetLimits().context_bytes:
        raise MCPTransportError("task, instruction and tool schema exceed the frozen text budget")
    tools_arg = ",".join(f"mcp__{SERVER_NAME}__{name}" for name in TOOLS)
    argv = [
        str(binary), "--print", "--tools", "", "--strict-mcp-config", "--restricted",
        "--mcp-config", mcp_config_path, "--disable-slash-commands", "--no-session-persistence",
        "--output-format", "stream-json", "--verbose", "--permission-prompts", "none",
        "--allowedTools", tools_arg, "--system-prompt", system_prompt, "--model", model,
    ]
    return {
        "mode": "one_claude_print_agent_one_stdio_mcp_server",
        "argv": argv,
        "stdin_text": task_text,
        "tools": list(TOOLS),
        "builtin_tools": [],
        "mcp_config_path": mcp_config_path,
        "model": model,
        "model_catalog_ref": model_catalog_ref,
        "claude_binary": str(binary),
        "claude_sha256": claude_sha256,
        "claude_version": claude_version,
        "working_directory": str(Path(working_directory).resolve()),
        "reasoning_effort": None,
        "provider_fallback": False,
        "model_rng_seed": None,
        "provider_calls": 0,
    }


def load_current_launch_pins() -> dict[str, Any]:
    state_root = Path.home() / ".local/state/lev/skills-db-progressive-discovery/finish-20261017T083107Z"
    selection_path = state_root / "live-subject-selection.json"
    binary_profile_path = state_root / "live-subject-binary.json"
    selection = json.loads(selection_path.read_text(encoding="utf-8"), object_pairs_hook=_no_duplicate_pairs)
    binary = json.loads(binary_profile_path.read_text(encoding="utf-8"), object_pairs_hook=_no_duplicate_pairs)
    expected_launcher = Path.home() / ".local/bin/claude"
    expected_binary = Path.home() / ".local/share/claude/versions/2.1.302"
    if (
        selection.get("status") != "prepared_not_runtime_qualified"
        or selection.get("providerInstanceId") != "claudeAgent"
        or selection.get("model") != "claude-sonnet-5-5"
        or selection.get("requested_cli_effort") is not None
        or selection.get("provider_fallback") is not False
        or selection.get("model_rng_seed") is not None
        or Path(binary.get("launcher", "")).expanduser().resolve() != expected_launcher.resolve()
        or Path(binary.get("resolved_binary", "")).expanduser().resolve() != expected_binary.resolve()
        or binary.get("sha256") != "5262ce9de86243fed0d21edc39b271555d56780d0112e2b194439fe1c6662d37"
        or binary.get("bytes") != 267956720
        or binary.get("version") != "2.1.302 (Claude Code)"
    ):
        raise MCPTransportError("live Claude model or binary profile differs from the admitted subject")
    return {
        "selection_path": str(selection_path),
        "binary_profile_path": str(binary_profile_path),
        "model": selection["model"],
        "model_catalog_ref": str(selection_path) + "#providerInstanceId/model_catalog_entry.id",
        "requested_cli_effort": None,
        "provider_fallback": False,
        "model_rng_seed": None,
        "launcher": str(expected_launcher),
        "binary": str(expected_binary),
        "binary_sha256": binary["sha256"],
        "binary_version": binary["version"],
        "binary_profile_sha256": _sha256_file(binary_profile_path),
        "selection_profile_sha256": _sha256_file(selection_path),
    }


def build_campaign_profile(*, task_text: str, instruction_text: str, backend: str, runtime_root: str | Path, gateway_report_path: str | Path, admitted_at: float, mode: str = "current_public") -> dict[str, Any]:
    if not isinstance(task_text, str) or not isinstance(instruction_text, str) or backend not in {"qmd", "lexical"}:
        raise MCPTransportError("campaign task, instruction or explicit backend is invalid")
    if mode not in {"current_public", "offline_test"}:
        raise MCPTransportError("campaign mode is not admitted")
    if Path(runtime_root).expanduser().resolve() != LIVE_RUNTIME_ROOT.resolve():
        raise MCPTransportError("campaign output is outside the owned runtime directory")
    report_path = Path(gateway_report_path).expanduser().resolve()
    if not _inside(report_path, LIVE_RUNTIME_ROOT.resolve()) or report_path == LIVE_RUNTIME_ROOT.resolve():
        raise MCPTransportError("gateway report path is outside the owned runtime directory")
    if isinstance(admitted_at, bool) or not isinstance(admitted_at, (int, float)) or not math.isfinite(float(admitted_at)) or admitted_at > time.monotonic():
        raise MCPTransportError("campaign admission origin must be finite and no later than now")
    if time.monotonic() - admitted_at >= BudgetLimits().wall_seconds:
        raise MCPTransportError("campaign admission origin is stale")
    schema_bytes = len(_json_text(tool_schemas()).encode("utf-8"))
    initial_bytes = len(task_text.encode("utf-8")) + len(instruction_text.encode("utf-8"))
    if initial_bytes + schema_bytes > BudgetLimits().context_bytes:
        raise MCPTransportError("task, instruction and exposed schemas exceed the frozen text budget")
    return {"task_text": task_text, "instruction_text": instruction_text, "admitted_at": float(admitted_at), "runtime_root": str(LIVE_RUNTIME_ROOT), "backend": backend, "gateway_report_path": str(report_path), "mode": mode}


def build_mcp_config(*, profile_file: str, python_executable: str) -> dict[str, Any]:
    profile_path = Path(profile_file).resolve(strict=False)
    runtime_root = LIVE_RUNTIME_ROOT.resolve()
    if not _inside(profile_path, runtime_root):
        raise MCPTransportError("MCP profile file is outside the owned runtime directory")
    adapter_script = Path(__file__).resolve()
    return {"mcpServers": {SERVER_NAME: {"type": "stdio", "command": python_executable, "args": [str(adapter_script), "serve", "--profile-file", str(profile_path)], "env": {"PYTHONDONTWRITEBYTECODE": "1"}}}}


def _write_private_json(path: Path, value: dict[str, Any], *, replace: bool = False) -> None:
    data = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        view = memoryview(data)
        while view:
            count = os.write(fd, view)
            view = view[count:]
    finally:
        os.close(fd)
    if replace:
        os.replace(temporary, path)
    else:
        os.link(temporary, path)
        temporary.unlink()


class OwnedProcessTree:
    """Retain descendant PIDs and process groups, including children that call setsid."""

    def __init__(self, root_pid: int, *, clock: Callable[[], float] = time.monotonic):
        self.root_pid = root_pid
        self.clock = clock
        self.processes: dict[int, dict[str, int]] = {}
        self.groups: dict[int, dict[str, Any]] = {}
        self.last_scan = 0.0
        self.tracking_error: str | None = None
        self._signal_seen: set[tuple[str, int]] = set()
        self.scan(force=True)

    def scan(self, *, force: bool = False) -> None:
        now = self.clock()
        if not force and now - self.last_scan < 0.1:
            return
        self.last_scan = now
        try:
            result = subprocess.run(["ps", "-axo", "pid=,ppid=,pgid=,sid="], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False, timeout=0.2)
            if result.returncode:
                raise MCPTransportError("ps could not enumerate owned descendants")
            table = {}
            for line in result.stdout.splitlines():
                try:
                    pid, ppid, pgid, sid = (int(item) for item in line.split())
                except (ValueError, TypeError):
                    continue
                table[pid] = {"pid": pid, "ppid": ppid, "pgid": pgid, "sid": sid}
        except (OSError, subprocess.SubprocessError, MCPTransportError) as error:
            self.tracking_error = str(error)[:256]
            return
        try:
            root_group, root_session = os.getpgid(self.root_pid), os.getsid(self.root_pid)
        except OSError:
            root_group = root_session = self.root_pid
        self.processes.setdefault(self.root_pid, {"pid": self.root_pid, "ppid": 0, "pgid": root_group, "sid": root_session, "owner_root": self.root_pid})
        owners = {self.root_pid: self.root_pid}
        changed = True
        while changed:
            changed = False
            for pid, identity in table.items():
                if pid not in owners and identity["ppid"] in owners:
                    owners[pid] = owners[identity["ppid"]]
                    changed = True
        for pid, owner in owners.items():
            identity = table.get(pid) or self.processes.get(pid)
            if identity is None:
                continue
            self.processes[pid] = {**identity, "owner_root": owner}
            group = self.groups.setdefault(identity["pgid"], {"pgid": identity["pgid"], "sid": identity["sid"], "members": set()})
            group["members"].add(pid)

    @staticmethod
    def _alive_pid(pid: int) -> bool:
        try:
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, PermissionError, OSError):
            return False

    @staticmethod
    def _alive_group(pgid: int) -> bool:
        try:
            os.killpg(pgid, 0)
            return True
        except (ProcessLookupError, PermissionError, OSError):
            return False

    def _send_once(self, kind: str, identity: int, sig: int, *, group: bool) -> None:
        marker = (kind, identity)
        if marker in self._signal_seen:
            return
        try:
            if group:
                os.killpg(identity, sig)
            else:
                os.kill(identity, sig)
        except (ProcessLookupError, PermissionError, OSError):
            pass
        self._signal_seen.add(marker)

    def stop_phase(self, stop_started: float, term_grace_seconds: float = 2.0) -> None:
        self.scan()
        elapsed = self.clock() - stop_started
        if elapsed < term_grace_seconds:
            # Signal the owning agent group once. MCP handlers can stop their own
            # CLI children while detached groups remain registered here.
            self._send_once("interrupt", self.root_pid, signal.SIGINT, group=True)
            return
        sig = signal.SIGTERM if elapsed < 2 * term_grace_seconds else signal.SIGKILL
        name = "term" if sig == signal.SIGTERM else "kill"
        for pgid in list(self.groups):
            self._send_once(name, pgid, sig, group=True)

    def observation(self, exit_code: int | None, state: str, *, deadline: float) -> dict[str, Any]:
        self.scan(force=True)
        alive_pids = [pid for pid in self.processes if self._alive_pid(pid)]
        alive_groups = [pgid for pgid in self.groups if self._alive_group(pgid)]
        return {"state": state, "pid": self.root_pid, "exit_code": exit_code, "deadline_monotonic": deadline, "owned_processes": [dict(value) for value in self.processes.values()], "owned_groups": [dict(value, members=sorted(value["members"])) for value in self.groups.values()], "survivor_pids": alive_pids, "survivor_groups": alive_groups, "tracking_error": self.tracking_error}


def supervise_agent_process(proc: Any, *, started_monotonic: float, wall_seconds: float = 300.0, term_grace_seconds: float = 2.0, teardown_seconds: float = 5.0, cancel_event: threading.Event | None = None, clock: Callable[[], float] = time.monotonic) -> dict[str, Any]:
    """Supervise one agent and every retained descendant process group."""
    if isinstance(started_monotonic, bool) or not math.isfinite(float(started_monotonic)) or started_monotonic > clock():
        raise MCPTransportError("agent admission origin must be finite and no later than now")
    if os.getpgid(proc.pid) != proc.pid:
        raise MCPTransportError("agent must start as its own process-group leader")
    tree = OwnedProcessTree(proc.pid, clock=clock)
    deadline = started_monotonic + wall_seconds
    state = "exited"
    while proc.poll() is None and clock() < deadline and not (cancel_event and cancel_event.is_set()):
        tree.scan()
        try:
            proc.wait(timeout=min(0.05, max(0.001, deadline - clock())))
        except subprocess.TimeoutExpired:
            pass
    if cancel_event and cancel_event.is_set():
        state = "cancelled"
    elif clock() >= deadline and proc.poll() is None:
        state = "deadline"
    tree.scan(force=True)
    if proc.poll() is not None and any(tree._alive_group(pgid) for pgid in tree.groups):
        if state == "exited":
            state = "exited_with_owned_descendants"
    if proc.poll() is None or any(tree._alive_group(pgid) for pgid in tree.groups):
        stop_started = clock()
        finish_at = stop_started + teardown_seconds
        while clock() < finish_at:
            tree.stop_phase(stop_started, term_grace_seconds)
            try:
                if proc.poll() is None:
                    proc.wait(timeout=min(0.02, max(0.001, finish_at - clock())))
                else:
                    time.sleep(min(0.02, max(0.0, finish_at - clock())))
            except subprocess.TimeoutExpired:
                pass
            tree.scan()
            if proc.poll() is not None and not any(tree._alive_group(pgid) for pgid in tree.groups):
                break
    return tree.observation(proc.poll(), state, deadline=deadline)


def _owned_group_alive(pid: int) -> bool:
    try:
        os.killpg(pid, 0)
        return True
    except (ProcessLookupError, PermissionError, OSError):
        return False


class ClaudeMCPServer:
    """Concurrent MCP stdio server over the existing campaign meter and callbacks."""

    def __init__(
        self,
        controller: ScriptedSkillsController,
        *,
        task_text: str,
        instruction_text: str,
        admitted_at: float | None = None,
        max_pending: int = MAX_PENDING,
        clock: Callable[[], float] = time.monotonic,
    ):
        self.controller = controller
        self.meter = controller.meter
        self.clock = clock
        self.max_pending = max_pending
        self.meter.begin(task_text, instruction_text, started_at=admitted_at)
        self.initial_text = {"task_bytes": len(task_text.encode("utf-8")), "instruction_bytes": len(instruction_text.encode("utf-8"))}
        self.initialized = False
        self.initialize_seen = False
        self.seen_ids: set[str | int] = set()
        self.pending: dict[str | int, Future[Any]] = {}
        self.pending_lock = threading.Lock()
        self.write_lock = threading.Lock()
        self.delivery_lock = threading.Lock()
        self.deliveries: list[dict[str, Any]] = []
        self.protocol_errors: list[str] = []
        self.frames_received = 0
        self.frame_bytes_received = 0
        self.frame_bytes_sent = 0
        self.deadline_fired = False
        self.stop_event = threading.Event()
        self.stop_started: float | None = None

    def request_stop(self, reason: str) -> None:
        if self.stop_started is None:
            self.stop_started = self.clock()
        self.stop_event.set()
        self.protocol_errors.append(reason[:256])
        self.controller.terminate_active_tools(reason, stop_started=self.stop_started, wait=False)

    def _write(self, writer: BinaryIO, frame: bytes) -> None:
        with self.write_lock:
            try:
                fd = writer.fileno()
            except (AttributeError, OSError, io.UnsupportedOperation):
                written = writer.write(frame)
                if written != len(frame):
                    raise MCPTransportError("in-memory MCP writer made a short write")
                self.frame_bytes_sent += written
                return
            os.set_blocking(fd, False)
            selector = selectors.DefaultSelector()
            selector.register(fd, selectors.EVENT_WRITE)
            view = memoryview(frame)
            try:
                while view:
                    self.meter.ensure_active()
                    ready = selector.select(timeout=min(0.05, self._remaining_seconds()))
                    if not ready:
                        continue
                    try:
                        count = os.write(fd, view)
                    except BlockingIOError:
                        continue
                    if count <= 0:
                        raise BrokenPipeError("MCP stdout closed during frame write")
                    self.frame_bytes_sent += count
                    view = view[count:]
            except AdmissionError as error:
                raise MCPDeadlineError("active deadline stopped MCP frame delivery") from error
            finally:
                selector.close()

    def _remaining_seconds(self) -> float:
        if self.meter.deadline is None:
            raise AdmissionError("campaign has not been admitted")
        remaining = self.meter.deadline - self.clock()
        if remaining <= 0:
            raise AdmissionError("active deadline elapsed during MCP frame delivery")
        return remaining

    def _reserve_and_write(self, writer: BinaryIO, frame: bytes, text: str, recipient: str) -> None:
        self.meter.reserve_reply([{"type": "inputText", "text": text}], recipient=recipient, frame_bytes=len(frame))
        self._write(writer, frame)

    def _send_rpc_error(self, writer: BinaryIO, request_id: Any, code: int, message: str) -> None:
        message = message[:512]
        frame = _encode_frame({"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}})
        try:
            self._reserve_and_write(writer, frame, message, f"agent:mcp-error:{request_id}")
        except AdmissionError:
            self.protocol_errors.append("JSON-RPC error could not fit the remaining text budget")
            self.meter.abort("JSON-RPC error could not be admitted")
            self.stop_event.set()

    def _send_tool_result(
        self,
        writer: BinaryIO,
        request_id: str | int,
        text: str,
        *,
        is_error: bool,
        transfer: dict[str, Any] | None,
        tool_name: str | None = None,
        tool_arguments: dict[str, Any] | None = None,
    ) -> None:
        frame = _encode_frame({"jsonrpc": "2.0", "id": request_id, "result": {"content": [{"type": "text", "text": text}], "isError": is_error}})
        try:
            self._reserve_and_write(writer, frame, text, f"agent:mcp-tool:{request_id}")
            if transfer is not None:
                self.meter.commit_span(transfer["reservation_token"])
                item = {**transfer, "recipient": "agent:mcp", "pipe_write_completed": True, "recipient_completed": False, "delivery_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
                state_lock = getattr(self.controller, "_source_state_lock", self.delivery_lock)
                with state_lock:
                    self.controller.transfers.append(item)
            with self.delivery_lock:
                self.deliveries.append({"request_id": request_id, "tool_name": tool_name, "tool_arguments": tool_arguments, "text": text, "text_bytes": len(text.encode("utf-8")), "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "is_error": is_error, "pipe_write_completed": True, "recipient_completed": False, "source_id": transfer.get("source_id") if transfer else None, "start_byte": transfer.get("start_byte") if transfer else None, "end_byte": transfer.get("end_byte") if transfer else None, "file_size": transfer.get("file_size") if transfer else None, "digest": transfer.get("digest") if transfer else None, "index_revision": transfer.get("index_revision") if transfer else None, "eof": transfer.get("eof") if transfer else None, "reservation_token": transfer.get("reservation_token") if transfer else None})
        except BaseException:
            if transfer is not None:
                self.meter.release_span(transfer["reservation_token"])
            raise

    def _dispatch_tool(self, writer: BinaryIO, request_id: str | int, params: Any) -> None:
        transfer = None
        name = None
        arguments = None
        try:
            if not isinstance(params, dict) or set(params) != {"name", "arguments"}:
                raise ProtocolError("tools/call params must contain name and arguments")
            name, arguments = params["name"], params["arguments"]
            if name not in TOOLS or not isinstance(arguments, dict):
                raise ProtocolError("tool is outside the six read-only skills tools")
            if name in self.controller.CLI_COMMANDS:
                payload = self.controller._run_cli_tool(name, arguments)
                body = payload
            elif name in self.controller.SOURCE_COMMANDS:
                body, transfer = self.controller._read_source(name, arguments)
            else:
                raise ProtocolError("tool is outside the read-only allowlist")
            text = _json_text(body)
            self._send_tool_result(writer, request_id, text, is_error=False, transfer=transfer, tool_name=name, tool_arguments=arguments)
        except Exception as error:
            if transfer is not None:
                self.meter.release_span(transfer["reservation_token"])
            if isinstance(error, MCPDeadlineError):
                self.protocol_errors.append(str(error))
                self.meter.abort("deadline blocked an MCP frame write")
                self.stop_event.set()
                self.controller.terminate_active_tools("writer_deadline")
                return
            # A result above the frozen byte cap is a small explicit failure.
            # Never slice or project the successful payload to make it fit.
            message = ("budget_or_tool_error: " + str(error))[:512]
            try:
                self._send_tool_result(writer, request_id, message, is_error=True, transfer=None, tool_name=name, tool_arguments=arguments)
            except AdmissionError:
                self.protocol_errors.append("tool error could not fit the remaining text budget")
                self.meter.abort("tool error could not be admitted")
                self.stop_event.set()

    def _handle(self, writer: BinaryIO, frame: dict[str, Any], executor: ThreadPoolExecutor) -> bool:
        if not isinstance(frame, dict) or frame.get("jsonrpc") != "2.0" or not isinstance(frame.get("method"), str) or not set(frame) <= {"jsonrpc", "method", "params", "id"}:
            self.meter.admit_attempt(action="malformed_frame")
            self.protocol_errors.append("invalid JSON-RPC request envelope")
            self._send_rpc_error(writer, frame.get("id") if isinstance(frame, dict) else None, -32600, "invalid JSON-RPC request envelope")
            return False
        method = frame["method"]
        request_id = frame.get("id")
        is_notification = "id" not in frame
        is_tool_call = method == "tools/call"
        if is_tool_call:
            try:
                self.meter.admit_attempt(action="mcp_tool_call")
            except AdmissionError as error:
                if not is_notification and isinstance(request_id, (str, int)) and not isinstance(request_id, bool):
                    denied = frame.get("params")
                    denied_name = denied.get("name") if isinstance(denied, dict) else None
                    denied_args = denied.get("arguments") if isinstance(denied, dict) and isinstance(denied.get("arguments"), dict) else None
                    try:
                        self._send_tool_result(writer, request_id, "budget_exhausted: " + str(error), is_error=True, transfer=None, tool_name=denied_name if isinstance(denied_name, str) else None, tool_arguments=denied_args)
                    except AdmissionError:
                        self.protocol_errors.append("budget error could not fit the remaining text budget")
                return False
        if not is_notification:
            if isinstance(request_id, bool) or not isinstance(request_id, (str, int)) or isinstance(request_id, str) and not request_id:
                self.protocol_errors.append("request id must be a unique non-empty string or integer")
                if is_tool_call:
                    self.controller.terminate_active_tools("invalid_request_id")
                    return True
                self._send_rpc_error(writer, None, -32600, "invalid JSON-RPC request id")
                return False
            with self.pending_lock:
                duplicate_id = request_id in self.seen_ids
                if not duplicate_id:
                    self.seen_ids.add(request_id)
            if duplicate_id:
                self.protocol_errors.append("duplicate JSON-RPC id rejected")
                self._send_rpc_error(writer, request_id, -32600, "duplicate JSON-RPC request id")
                self.controller.terminate_active_tools("duplicate_request_id")
                return True
        if method == "notifications/initialized" and is_notification:
            if not getattr(self, "initialize_seen", False):
                self.protocol_errors.append("initialized notification arrived before initialize")
                return True
            self.initialized = True
            return False
        if method == "notifications/cancelled" and is_notification:
            params = frame.get("params", {})
            if not isinstance(params, dict) or set(params) - {"requestId", "reason"} or "requestId" not in params or isinstance(params.get("requestId"), bool) or not isinstance(params.get("requestId"), (str, int)):
                self.protocol_errors.append("cancel notification fields are invalid")
                return True
            self.request_stop("agent_cancelled")
            return False
        if method == "initialize" and not is_notification:
            params = frame.get("params")
            if not isinstance(params, dict) or not isinstance(params.get("protocolVersion"), str):
                self._send_rpc_error(writer, request_id, -32602, "initialize params are invalid")
                return False
            if self.initialize_seen:
                self._send_rpc_error(writer, request_id, -32600, "duplicate initialize request")
                return True
            self.initialize_seen = True
            result = {"jsonrpc": "2.0", "id": request_id, "result": {"protocolVersion": "2025-11-25", "capabilities": {"tools": {"listChanged": False}}, "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}}}
            self._write(writer, _encode_frame(result))
            return False
        if method == "ping" and not is_notification:
            self._write(writer, _encode_frame({"jsonrpc": "2.0", "id": request_id, "result": {}}))
            return False
        if method == "tools/list" and not is_notification:
            if not self.initialized:
                self._send_rpc_error(writer, request_id, -32002, "MCP initialize handshake is incomplete")
                return False
            if frame.get("params", {}) not in ({}, None):
                self._send_rpc_error(writer, request_id, -32602, "tools/list does not accept parameters")
                return False
            schemas = tool_schemas()
            schema_text = _json_text(schemas)
            response = {"jsonrpc": "2.0", "id": request_id, "result": {"tools": schemas}}
            self._reserve_and_write(writer, _encode_frame(response), schema_text, "agent:mcp-tool-schema")
            return False
        if method == "tools/call":
            if is_notification or isinstance(request_id, bool) or not isinstance(request_id, (str, int)) or isinstance(request_id, str) and not request_id:
                self.protocol_errors.append("tools/call requires a unique string or integer id")
                self.controller.terminate_active_tools("invalid_tool_call_id")
                return True
            if not self.initialized:
                params = frame.get("params")
                self._send_tool_result(writer, request_id, "MCP initialize handshake is incomplete", is_error=True, transfer=None, tool_name=params.get("name") if isinstance(params, dict) and isinstance(params.get("name"), str) else None, tool_arguments=params.get("arguments") if isinstance(params, dict) and isinstance(params.get("arguments"), dict) else None)
                return False
            with self.pending_lock:
                if len(self.pending) >= self.max_pending:
                    future = None
                else:
                    future = executor.submit(self._dispatch_tool, writer, request_id, frame.get("params"))
                    self.pending[request_id] = future
            if future is None:
                params = frame.get("params")
                self._send_tool_result(writer, request_id, "pending_request_cap: concurrent tool limit reached", is_error=True, transfer=None, tool_name=params.get("name") if isinstance(params, dict) and isinstance(params.get("name"), str) else None, tool_arguments=params.get("arguments") if isinstance(params, dict) and isinstance(params.get("arguments"), dict) else None)
            else:
                future.add_done_callback(lambda _: self._drop_pending(request_id))
            return False
        if is_notification:
            self.protocol_errors.append("unknown notification rejected")
            return False
        self._send_rpc_error(writer, request_id, -32601, "unsupported MCP method")
        return False

    def _drop_pending(self, request_id: str | int) -> None:
        with self.pending_lock:
            self.pending.pop(request_id, None)

    def serve(self, reader: BinaryIO, writer: BinaryIO) -> dict[str, Any]:
        frames: queue.Queue[bytes | None] = queue.Queue(maxsize=MAX_PENDING + 2)

        def read_frames() -> None:
            while True:
                raw = reader.readline(MAX_FRAME_BYTES + 1)
                if raw == b"":
                    frames.put(None)
                    return
                frames.put(raw)
                if len(raw) > MAX_FRAME_BYTES or not raw.endswith(b"\n"):
                    frames.put(None)
                    return

        reader_thread = threading.Thread(target=read_frames, name="skills-db-mcp-reader", daemon=True)
        reader_thread.start()
        eof = False
        fatal = False
        executor = DaemonExecutor(max_workers=self.max_pending)
        while (not eof or self.pending) and not self.stop_event.is_set():
            if self.meter.deadline is not None and self.clock() >= self.meter.deadline:
                self.deadline_fired = True
                self.request_stop("active_deadline")
                fatal = True
                break
            try:
                raw = frames.get(timeout=0.05)
            except queue.Empty:
                continue
            if raw is None:
                eof = True
                continue
            self.frames_received += 1
            self.frame_bytes_received += len(raw)
            if len(raw) > MAX_FRAME_BYTES or not raw.endswith(b"\n"):
                try:
                    self.meter.admit_attempt(action="malformed_frame")
                except AdmissionError:
                    pass
                self.protocol_errors.append("frame exceeded the byte bound or ended before newline")
                self.request_stop("broken_or_oversized_frame")
                fatal = True
                break
            try:
                value = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicate_pairs)
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
                try:
                    self.meter.admit_attempt(action="malformed_frame")
                except AdmissionError:
                    pass
                self.protocol_errors.append("malformed MCP JSON frame")
                self.request_stop("malformed_json_frame")
                fatal = True
                break
            try:
                if self._handle(writer, value, executor):
                    fatal = True
                    break
            except Exception as error:
                self.protocol_errors.append(("transport dispatch failed: " + str(error))[:512])
                self.request_stop("transport_dispatch_failed")
                fatal = True
                break
        if fatal and not self.stop_event.is_set():
            self.request_stop("protocol_or_deadline_failure")
        # Pending callbacks share one total teardown deadline. Daemon workers
        # cannot keep this process alive if an owner callback fails to stop.
        if self.stop_started is None:
            self.stop_started = self.clock()
        wait_deadline = self.stop_started + self.meter.limits.teardown_seconds
        while self.pending and self.clock() < wait_deadline:
            time.sleep(min(0.01, max(0.0, wait_deadline - self.clock())))
        if self.pending:
            self.protocol_errors.append("pending callbacks exceeded the shared teardown deadline")
            self.meter.abort("pending callbacks exceeded teardown bound")
            fatal = True
        executor.shutdown(wait=False, cancel_futures=True)
        return {
            "terminal": "failed" if fatal or self.stop_event.is_set() else "eof",
            "deadline_fired": self.deadline_fired,
            "initial_text": self.initial_text,
            "frames_received": self.frames_received,
            "frame_bytes_received": self.frame_bytes_received,
            "frame_bytes_sent": self.frame_bytes_sent,
            "deliveries": list(self.deliveries),
            "protocol_errors": list(self.protocol_errors),
            "meter": self.meter.observation(),
            "cli_runs": list(self.controller.cli_runs),
            "source_transfers": list(self.controller.transfers),
            "query_observations": dict(getattr(self.controller, "query_observations", {})),
            "profile": dict(getattr(self.controller, "profile_observation", {})),
        }


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def serve_profile(profile_file: str) -> int:
    runtime_root = LIVE_RUNTIME_ROOT.resolve()
    supplied_path = Path(profile_file)
    path = supplied_path.resolve(strict=True)
    if supplied_path.is_symlink() or not _inside(path, runtime_root) or not path.is_file() or path.stat().st_size > 2_097_152:
        raise MCPTransportError("campaign profile must be a regular file inside the owned runtime directory")
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_no_duplicate_pairs)
    expected = {"task_text", "instruction_text", "admitted_at", "runtime_root", "backend", "gateway_report_path", "mode"}
    if not isinstance(value, dict) or set(value) != expected:
        raise MCPTransportError("campaign profile fields do not match the admitted schema")
    report_path = Path(value["gateway_report_path"]).resolve(strict=False)
    if Path(value["runtime_root"]).resolve() != runtime_root or value["backend"] not in {"qmd", "lexical"} or value["mode"] != "current_public" or not _inside(report_path, runtime_root) or report_path.parent != path.parent:
        raise MCPTransportError("campaign runtime path or discover backend is not admitted")
    admitted_at = value["admitted_at"]
    if isinstance(admitted_at, bool) or not isinstance(admitted_at, (int, float)):
        raise MCPTransportError("campaign admission time is invalid")
    profile = SkillsCliProfile.current_public(backend=value["backend"], runtime_root=runtime_root)
    controller = ScriptedSkillsController(public_profile=profile, lane="live_claude")
    server = ClaudeMCPServer(controller, task_text=value["task_text"], instruction_text=value["instruction_text"], admitted_at=float(admitted_at))

    def stop(signum, _frame):
        server.request_stop("stdio_server_signal_" + signal.Signals(signum).name.lower())

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    observation = server.serve(__import__("sys").stdin.buffer, __import__("sys").stdout.buffer)
    _write_private_json(report_path, observation)
    return 0 if observation.get("terminal") == "eof" and not observation.get("protocol_errors") and not observation.get("meter", {}).get("aborted") else 2


def _canonical_args(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def match_tool_result_event(
    event: dict[str, Any],
    deliveries: list[dict[str, Any]],
    matched_ids: set[str] | None = None,
    tool_uses: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Join observed assistant tool_use and user tool_result to one gateway request."""
    matched = matched_ids if matched_ids is not None else set()
    uses = tool_uses if tool_uses is not None else {}
    message = event.get("message")
    blocks = message.get("content") if isinstance(message, dict) else None
    if not isinstance(blocks, list):
        return []
    event_type = event.get("type")
    if event_type == "assistant":
        for block in blocks:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            use_id, name, arguments = block.get("id"), block.get("name"), block.get("input")
            if not isinstance(use_id, str) or not use_id or use_id in uses or not isinstance(name, str) or not isinstance(arguments, dict):
                raise MCPTransportError("assistant tool_use is malformed or duplicates an observed ID")
            tool = name.rsplit("__", 1)[-1]
            if tool not in TOOLS and name not in {"EndConversation", "mcp__EndConversation"}:
                raise MCPTransportError("assistant requested a foreign tool")
            uses[use_id] = {"name": name, "tool": tool, "arguments": arguments, "terminal_only": tool == "EndConversation"}
        return []
    if event_type != "user":
        return []
    observations = []
    for block in blocks:
        if not isinstance(block, dict) or block.get("type") != "tool_result":
            continue
        tool_use_id = block.get("tool_use_id")
        use = uses.get(tool_use_id) if isinstance(tool_use_id, str) else None
        if not isinstance(tool_use_id, str) or not tool_use_id or tool_use_id in matched or use is None or use.get("terminal_only"):
            raise MCPTransportError("tool_result has a missing, duplicate, or unmapped tool_use_id")
        content = block.get("content")
        if isinstance(content, str):
            text = content
        elif isinstance(content, list) and all(isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str) for item in content):
            text = "".join(item["text"] for item in content)
        else:
            raise MCPTransportError("tool_result content is not a complete text delivery")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        candidates = [
            item for item in deliveries
            if item.get("pipe_write_completed")
            and not item.get("recipient_completed")
            and item.get("tool_name") == use.get("tool")
            and _canonical_args(item.get("tool_arguments")) == _canonical_args(use.get("arguments"))
            and item.get("sha256") == digest
            and item.get("text") == text
        ]
        if len(candidates) != 1:
            raise MCPTransportError("tool_result does not map one-to-one to a unique gateway request")
        candidate = candidates[0]
        candidate["recipient_completed"] = True
        candidate["stream_tool_use_id"] = tool_use_id
        candidate["recipient_receipt"] = {"tool_use_id": tool_use_id, "request_id": candidate.get("request_id"), "sha256": digest, "text_bytes": len(text.encode("utf-8"))}
        matched.add(tool_use_id)
        observations.append({"tool_use_id": tool_use_id, "request_id": candidate.get("request_id"), "tool_name": candidate.get("tool_name"), "sha256": digest, "text_bytes": len(text.encode("utf-8")), "source_id": candidate.get("source_id"), "start_byte": candidate.get("start_byte"), "end_byte": candidate.get("end_byte"), "file_size": candidate.get("file_size"), "eof": candidate.get("eof")})
    return observations


def ensure_complete_tool_results(deliveries: list[dict[str, Any]], tool_uses: dict[str, dict[str, Any]] | None = None) -> None:
    missing = [item.get("request_id") for item in deliveries if item.get("pipe_write_completed") and not item.get("recipient_completed")]
    unmatched_uses = [use_id for use_id, use in (tool_uses or {}).items() if not use.get("terminal_only") and use_id not in {item.get("stream_tool_use_id") for item in deliveries}]
    if missing or unmatched_uses:
        raise MCPTransportError("stream-json receipt coverage incomplete; missing requests=" + ",".join(str(item) for item in missing[:16]) + "; unmatched tool_use IDs=" + ",".join(unmatched_uses[:16]))


def recipient_source_coverage(deliveries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_source: dict[str, list[dict[str, Any]]] = {}
    for item in deliveries:
        if item.get("recipient_completed") and item.get("source_id"):
            by_source.setdefault(item["source_id"], []).append(item)
    complete = []
    for source_id, rows in by_source.items():
        identities = {(row.get("digest"), row.get("index_revision"), row.get("file_size")) for row in rows}
        if len(identities) != 1:
            continue
        digest, revision, size = next(iter(identities))
        spans = sorted((row.get("start_byte"), row.get("end_byte"), row.get("eof")) for row in rows)
        cursor = 0
        valid = isinstance(size, int) and size > 0
        for start, end, eof in spans:
            if isinstance(start, bool) or not isinstance(start, int) or isinstance(end, bool) or not isinstance(end, int) or start != cursor or end <= start or end > size:
                valid = False
                break
            cursor = end
            if bool(eof) != (end == size):
                valid = False
                break
        if valid and cursor == size:
            complete.append({"source_id": source_id, "digest": digest, "index_revision": revision, "file_size": size, "recipient_completed": True, "tool_use_ids": [row.get("stream_tool_use_id") for row in rows]})
    return complete


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["serve"])
    parser.add_argument("--profile-file", required=True)
    args = parser.parse_args()
    serve_profile(args.profile_file)

