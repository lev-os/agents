"""Test-local, scripted app-server bridge for the S06 skills-db slice.

This module only admits ``scripted_fixture`` runs. It is deliberately not a
native Codex adapter or an evaluation verdict surface.
"""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import asdict, dataclass
import hashlib
import json
import os
from pathlib import Path
import queue
import selectors
import signal
import subprocess
import sys
import threading
import time
from typing import Any, Callable
import uuid


READINESS_ROOT = Path(
    "/Users/jean-patricksmith/.local/state/lev/skills-db-progressive-discovery/20261014T055617Z/s06-readiness"
)
RUN_ROOT = Path(
    "/Users/jean-patricksmith/.local/state/lev/skills-db-progressive-discovery/20261014T055617Z/s06-writer"
)
BUDGET_FILE = READINESS_ROOT / "frozen-budget-only.json"
EXPECTED_BUDGET_SHA256 = "b62097524f02e3bae375c99de758550eaec294066fe8dd3594f68c4783792453"
EXPECTED_CLI_SHA256 = "349b185c118d8e0c4dc63172c0aad5341bf01a31022d0a214c9c6760e0affc88"


class AdmissionError(RuntimeError):
    """An attempt or byte delivery did not fit the frozen shared allowance."""


class ProtocolError(RuntimeError):
    """The peer used an unsupported or malformed app-server frame."""


class SourceError(RuntimeError):
    """A returned source descriptor failed the local source boundary."""


@dataclass(frozen=True)
class BudgetLimits:
    calls: int = 160
    context_bytes: int = 2_097_152
    per_response_bytes: int = 262_144
    wall_seconds: float = 300.0
    term_grace_seconds: float = 2.0
    teardown_seconds: float = 5.0


DEFAULT_LIMITS = BudgetLimits()


def frozen_limits() -> BudgetLimits:
    """Read only the approved budget extract and reject drift before use."""
    raw = BUDGET_FILE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_BUDGET_SHA256:
        raise RuntimeError("approved S06 budget extract digest changed")
    value = json.loads(raw.decode("utf-8"))["runtime_budget_contract"]
    limits = BudgetLimits(
        calls=value["calls"],
        context_bytes=value["context_bytes"],
        per_response_bytes=value["per_response_bytes"],
        wall_seconds=value["wall_seconds"],
        term_grace_seconds=value["term_grace_seconds"],
        teardown_seconds=value["local_teardown_seconds"],
    )
    if limits != DEFAULT_LIMITS:
        raise RuntimeError("approved S06 budget values differ from the frozen defaults")
    return limits


class CampaignMeter:
    """Atomic, non-refundable counters shared by every lane in a campaign."""

    def __init__(self, limits: BudgetLimits = DEFAULT_LIMITS, clock: Callable[[], float] = time.monotonic):
        self.limits = limits
        self.clock = clock
        self.lock = threading.Lock()
        self.deadline: float | None = None
        self.attempted_calls = 0
        self.admitted_calls = 0
        self.context_bytes = 0
        self.initial_bytes = 0
        self.initial_deliveries: list[dict[str, Any]] = []
        self.reply_bytes: list[dict[str, Any]] = []
        self.denials: list[dict[str, Any]] = []
        self.aborted = False
        self.abort_reason: str | None = None
        self.pending_spans: dict[str, tuple[str, str, str, int, int]] = {}
        self.committed_spans: list[tuple[str, str, str, int, int]] = []

    def begin(self, task_text: str, instruction_text: str, *, started_at: float | None = None) -> None:
        if not isinstance(task_text, str) or not isinstance(instruction_text, str):
            raise TypeError("initial task and instruction must be text")
        started = self.clock() if started_at is None else started_at
        task_bytes = len(task_text.encode("utf-8"))
        instruction_bytes = len(instruction_text.encode("utf-8"))
        requested = task_bytes + instruction_bytes
        with self.lock:
            if self.deadline is None:
                self.deadline = started + self.limits.wall_seconds
            elif self.clock() >= self.deadline:
                raise AdmissionError("active deadline elapsed before lane admission")
            if self.context_bytes + requested > self.limits.context_bytes:
                self.denials.append({"kind": "initial_text", "bytes": requested})
                raise AdmissionError("initial task and instruction exceed the context cap")
            self.context_bytes += requested
            self.initial_bytes += requested
            self.initial_deliveries.append({"task_bytes": task_bytes, "instruction_bytes": instruction_bytes})

    def ensure_active(self) -> None:
        with self.lock:
            if self.deadline is None:
                raise AdmissionError("campaign has not been admitted")
            if self.aborted:
                raise AdmissionError("campaign aborted: " + (self.abort_reason or "unspecified"))
            if self.clock() >= self.deadline:
                raise AdmissionError("active deadline elapsed")

    def abort(self, reason: str) -> None:
        with self.lock:
            self.aborted = True
            if self.abort_reason is None:
                self.abort_reason = reason[:512]

    def reserve_span(self, token: str, source_id: str, digest: str, index_revision: str, start: int, end: int) -> None:
        span = (source_id, digest, index_revision, start, end)
        with self.lock:
            if self.aborted:
                raise AdmissionError("campaign aborted before source-span admission")
            if self.deadline is None or self.clock() >= self.deadline:
                raise AdmissionError("active deadline elapsed before source-span admission")
            for existing in [*self.committed_spans, *self.pending_spans.values()]:
                if existing[:3] == span[:3] and max(start, existing[3]) < min(end, existing[4]):
                    raise AdmissionError("overlapping source span is already pending or delivered")
            self.pending_spans[token] = span

    def commit_span(self, token: str) -> None:
        with self.lock:
            span = self.pending_spans.pop(token, None)
            if span is None:
                raise AdmissionError("source span reservation was lost before frame commit")
            self.committed_spans.append(span)

    def release_span(self, token: str) -> None:
        with self.lock:
            self.pending_spans.pop(token, None)

    def admit_attempt(self, *, action: str) -> int:
        """Charge before validation/dispatch. Denied 161st attempt is not admitted."""
        with self.lock:
            self.attempted_calls += 1
            if self.aborted:
                self.denials.append({"kind": "attempt", "action": action, "reason": "aborted"})
                raise AdmissionError("campaign aborted before tool dispatch")
            if self.deadline is None or self.clock() >= self.deadline:
                self.denials.append({"kind": "attempt", "action": action, "reason": "deadline"})
                raise AdmissionError("active deadline elapsed before tool dispatch")
            if self.admitted_calls >= self.limits.calls:
                self.denials.append({"kind": "attempt", "action": action, "reason": "call_cap"})
                raise AdmissionError("shared tool attempt cap exhausted")
            self.admitted_calls += 1
            return self.admitted_calls

    def reserve_reply(self, items: list[dict[str, Any]], *, recipient: str, frame_bytes: int) -> int:
        text_bytes = 0
        for item in items:
            if not isinstance(item, dict) or item.get("type") != "inputText" or not isinstance(item.get("text"), str):
                raise ProtocolError("only typed inputText reply items are admitted by this fixture bridge")
            text_bytes += len(item["text"].encode("utf-8"))
        with self.lock:
            if self.deadline is None or self.clock() >= self.deadline:
                self.denials.append({"kind": "reply", "recipient": recipient, "bytes": text_bytes, "reason": "deadline"})
                raise AdmissionError("active deadline elapsed before delivery")
            if self.aborted:
                self.denials.append({"kind": "reply", "recipient": recipient, "bytes": text_bytes, "reason": "aborted"})
                raise AdmissionError("campaign aborted before delivery")
            if text_bytes > self.limits.per_response_bytes:
                self.denials.append({"kind": "reply", "recipient": recipient, "bytes": text_bytes, "reason": "per_response_cap"})
                raise AdmissionError("sum of text items exceeds the per-reply cap")
            if self.context_bytes + text_bytes > self.limits.context_bytes:
                self.denials.append({"kind": "reply", "recipient": recipient, "bytes": text_bytes, "reason": "context_cap"})
                raise AdmissionError("shared campaign text cap exhausted")
            self.context_bytes += text_bytes
            self.reply_bytes.append({
                "recipient": recipient,
                "text_bytes": text_bytes,
                "frame_bytes": frame_bytes,
                "frame_overhead_bytes": max(0, frame_bytes - text_bytes),
            })
            return text_bytes

    def observation(self) -> dict[str, Any]:
        with self.lock:
            return {
                "limits": asdict(self.limits),
                "attempted_calls": self.attempted_calls,
                "admitted_calls": self.admitted_calls,
                "initial_text_bytes": self.initial_bytes,
                "initial_deliveries": list(self.initial_deliveries),
                "cumulative_text_bytes": self.context_bytes,
                "reply_deliveries": list(self.reply_bytes),
                "denials": list(self.denials),
                "aborted": self.aborted,
                "abort_reason": self.abort_reason,
                "pending_span_reservations": len(self.pending_spans),
                "committed_source_spans": len(self.committed_spans),
                "deadline_monotonic": self.deadline,
            }


_EOF = object()


def _write_pipe(fd: int, payload: memoryview) -> int:
    """Single nonblocking pipe write; callers must handle partial success."""
    return os.write(fd, payload)


def _json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _decode_json_frame(raw: bytes) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ProtocolError(f"invalid UTF-8 JSON frame: {error}") from error
    if not isinstance(value, dict):
        raise ProtocolError("stdio frame must be a JSON object")
    return value


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


class ScriptedSkillsController:
    """One local fixture controller owning one scripted stdio process group."""

    SERVER_REQUEST_METHODS = frozenset(
        {
            "item/commandExecution/requestApproval",
            "item/fileChange/requestApproval",
            "item/tool/requestUserInput",
            "mcpServer/elicitation/request",
            "item/permissions/requestApproval",
            "item/tool/call",
            "account/chatgptAuthTokens/refresh",
            "attestation/generate",
            "currentTime/read",
            "applyPatchApproval",
            "execCommandApproval",
        }
    )

    TOOL_NAMESPACE = "skills_db"
    CLI_COMMANDS = {"tree", "browse", "discover", "get"}
    SOURCE_COMMANDS = {"read_path", "read_chunks"}

    def __init__(
        self,
        fixture: Any,
        *,
        meter: CampaignMeter | None = None,
        lane: str = "scripted",
        clock: Callable[[], float] = time.monotonic,
    ):
        self.fixture = fixture
        self.clock = clock
        self.meter = meter or CampaignMeter(frozen_limits(), clock)
        self.lane = lane
        self.approved_root = (Path(fixture.repo) / "skills-db").resolve()
        self.fixture_root = Path(fixture.output).resolve()
        self.cli_sha256 = hashlib.sha256(Path(fixture.script).read_bytes()).hexdigest()
        if self.cli_sha256 != EXPECTED_CLI_SHA256:
            raise RuntimeError("copied skills-db CLI differs from the admitted read-only source")
        self.proc: subprocess.Popen[bytes] | None = None
        self._frames: queue.Queue[Any] = queue.Queue()
        self._reader: threading.Thread | None = None
        self._stderr_reader: threading.Thread | None = None
        self._stderr = bytearray()
        self._write_lock = threading.Lock()
        self._cli_lock = threading.Lock()
        self._active_tools: dict[int, subprocess.Popen[bytes]] = {}
        self._active_tools_lock = threading.Lock()
        self._callback_futures: set[Future[Any]] = set()
        self._callback_futures_lock = threading.Lock()
        self._request_id = 0
        self.run_id: str | None = None
        self._evidence_path: Path | None = None
        self._thread_id: str | None = None
        self._turn_id: str | None = None
        self.peer_log: Path | None = None
        self.protocol_out: list[dict[str, Any]] = []
        self.write_failures: list[dict[str, Any]] = []
        self.protocol_in: list[dict[str, Any]] = []
        self.notifications: list[dict[str, Any]] = []
        self.protocol_terminals: list[dict[str, Any]] = []
        self._terminal_fact_error: str | None = None
        self._terminal_frame_seen = False
        self.callback_rejections: list[dict[str, Any]] = []
        self.callback_observations: list[dict[str, Any]] = []
        self.cli_runs: list[dict[str, Any]] = []
        self.query_observations: dict[str, dict[str, Any]] = {}
        self.descriptors: dict[str, dict[str, Any]] = {}
        self.tree_nodes: set[str] = set()
        self.bundle_specs: dict[str, dict[str, Any]] = {}
        self.transfers: list[dict[str, Any]] = []
        self.full_sources: set[str] = set()
        self.failed: str | None = None
        self.terminal: dict[str, Any] = {"state": "not_started"}
        self.stderr_text = ""

    @staticmethod
    def dynamic_tools() -> list[dict[str, Any]]:
        def tool(name: str, description: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
            return {
                "type": "function",
                "name": name,
                "description": description,
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                    "additionalProperties": False,
                },
            }

        return [
            {
                "type": "namespace",
                "name": ScriptedSkillsController.TOOL_NAMESPACE,
                "description": "Read-only local skills-db fixture discovery and source delivery.",
                "tools": [
                    tool("tree", "Read an installed skills-db navigation tree.", {"view": {"type": "string"}, "depth": {"type": "integer"}}, ["view", "depth"]),
                    tool("browse", "Browse a node returned by tree.", {"node_id": {"type": "string"}, "limit": {"type": "integer"}}, ["node_id", "limit"]),
                    tool("discover", "Run an uncached query through the copied CLI.", {"query": {"type": "string"}}, ["query"]),
                    tool("get", "Return a descriptor for an already observed source ID.", {"source_id": {"type": "string"}}, ["source_id"]),
                    tool("read_path", "Deliver the complete UTF-8 bytes for an observed descriptor.", {"source_id": {"type": "string"}}, ["source_id"]),
                    tool("read_chunks", "Deliver a non-overlapping byte span for an observed descriptor.", {"source_id": {"type": "string"}, "start_byte": {"type": "integer"}, "end_byte": {"type": "integer"}}, ["source_id", "start_byte", "end_byte"]),
                ],
            }
        ]

    def run_scripted_peer(
        self,
        peer_script: Path,
        *,
        task_text: str,
        instruction_text: str,
        run_kind: str = "scripted_fixture",
    ) -> dict[str, Any]:
        """Admit initial text before starting the fixed-argv scripted peer."""
        if run_kind != "scripted_fixture":
            raise ProtocolError("this component only admits scripted_fixture runs")
        if self.run_id is not None:
            raise ProtocolError("controller instances admit only one scripted campaign")
        peer_script = Path(peer_script).resolve()
        if not peer_script.is_file() or not _within(peer_script, self.fixture_root):
            raise ProtocolError("scripted peer must be a file inside the isolated fixture root")
        started = self.clock()
        self.run_id = f"{time.time_ns()}-{os.getpid()}-{uuid.uuid4().hex[:12]}"
        self.meter.begin(task_text, instruction_text, started_at=started)
        self.peer_log = peer_script.parent / "peer-observed.jsonl"
        self.peer_log.unlink(missing_ok=True)
        env = self.fixture.env({
            "PYTHONDONTWRITEBYTECODE": "1",
            "XDG_CACHE_HOME": str(self.fixture_root / "xdg-cache"),
            "XDG_CONFIG_HOME": str(self.fixture_root / "xdg-config"),
            "S06_PEER_LOG": str(self.peer_log),
        })
        argv = [sys.executable, "-I", str(peer_script)]
        try:
            self.proc = subprocess.Popen(
                argv,
                cwd=str(self.fixture.repo),
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
                start_new_session=True,
                close_fds=True,
                bufsize=0,
            )
        except Exception as error:
            self.terminal = {"state": "spawn_failed", "error": type(error).__name__}
            self.write_evidence()
            raise
        assert self.proc.stdout is not None and self.proc.stderr is not None
        self._reader = threading.Thread(target=self._read_frames, name="s06-peer-stdout", daemon=True)
        self._stderr_reader = threading.Thread(target=self._drain_stderr, name="s06-peer-stderr", daemon=True)
        self._reader.start()
        self._stderr_reader.start()
        try:
            initialized = self._client_request(
                "initialize",
                {"clientInfo": {"name": "s06-scripted-fixture", "title": "S06 fixture", "version": "1"},
                 "capabilities": {"experimentalApi": False, "requestAttestation": False}},
            )
            self._require_keys(initialized, {"userAgent", "codexHome", "platformFamily", "platformOs"}, "initialize response")
            self._send_frame({"method": "initialized"})
            thread = self._client_request(
                "thread/start",
                {
                    "cwd": str(Path(self.fixture.repo).resolve()),
                    "ephemeral": True,
                    "allowProviderModelFallback": False,
                    "developerInstructions": instruction_text,
                    "dynamicTools": self.dynamic_tools(),
                },
            )
            thread_value = thread.get("thread") if isinstance(thread, dict) else None
            if not isinstance(thread_value, dict) or not isinstance(thread_value.get("id"), str):
                raise ProtocolError("thread/start response omitted the typed thread id")
            self._thread_id = thread_value["id"]
            turn = self._client_request(
                "turn/start",
                {"threadId": self._thread_id, "input": [{"type": "text", "text": task_text, "text_elements": []}]},
            )
            turn_value = turn.get("turn") if isinstance(turn, dict) else None
            if not isinstance(turn_value, dict) or not isinstance(turn_value.get("id"), str):
                raise ProtocolError("turn/start response omitted the typed turn id")
            self._turn_id = turn_value["id"]
            self._serve_requests()
        except (AdmissionError, ProtocolError, BrokenPipeError, EOFError, OSError, TimeoutError) as error:
            self.failed = type(error).__name__ + ": " + str(error)
            self.meter.abort(self.failed)
        finally:
            self._cleanup_owned_processes()
            if self.proc is not None:
                completed_turn = self._has_one_matching_completed_turn()
                clean_exit = self.proc.returncode == 0 and self.terminal.get("stdout_eof_observed", False)
                if self.failed is not None:
                    state = "failed"
                elif completed_turn and clean_exit:
                    state = "completed"
                else:
                    state = "incomplete"
                failure = self.failed or self._terminal_fact_error
                self.terminal = {
                    "state": state,
                    "peer_pid": self.proc.pid,
                    "peer_exit_code": self.proc.returncode,
                    "stdout_eof_observed": self.terminal.get("stdout_eof_observed", False),
                    "protocol_terminal_notifications": list(self.protocol_terminals),
                    "cleanup": self.terminal.get("cleanup", {}),
                    "failure": failure,
                }
            self.stderr_text = bytes(self._stderr).decode("utf-8", errors="replace")
            self.write_evidence()
        return self.observation()

    def _read_frames(self) -> None:
        assert self.proc is not None and self.proc.stdout is not None
        try:
            while True:
                raw = self.proc.stdout.readline()
                if not raw:
                    self._frames.put(_EOF)
                    return
                self._frames.put(raw)
        except Exception as error:
            self._frames.put(error)

    def _drain_stderr(self) -> None:
        assert self.proc is not None and self.proc.stderr is not None
        try:
            while True:
                chunk = self.proc.stderr.read(4096)
                if not chunk:
                    return
                self._stderr.extend(chunk)
        except Exception:
            return

    def _next_frame(self) -> dict[str, Any]:
        self.meter.ensure_active()
        deadline = self.meter.deadline
        assert deadline is not None
        try:
            value = self._frames.get(timeout=max(0.001, deadline - self.clock()))
        except queue.Empty as error:
            raise TimeoutError("active campaign deadline elapsed while awaiting peer frame") from error
        if value is _EOF:
            self.terminal["stdout_eof_observed"] = True
            raise EOFError("scripted peer closed stdout")
        if isinstance(value, Exception):
            raise ProtocolError(f"stdout reader failed: {value}") from value
        raw = bytes(value).rstrip(b"\r\n")
        frame = _decode_json_frame(raw)
        self.protocol_in.append({"frame_bytes": len(bytes(value)), "method": frame.get("method"), "id": frame.get("id"), "received_monotonic": self.clock()})
        return frame

    def _send_frame(self, frame: dict[str, Any]) -> None:
        self.meter.ensure_active()
        if self.proc is None or self.proc.stdin is None:
            raise BrokenPipeError("peer stdin is unavailable")
        encoded = json.dumps(frame, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"
        deadline = self.meter.deadline
        assert deadline is not None
        if not self._write_lock.acquire(timeout=max(0.0, deadline - self.clock())):
            self.meter.abort("write lock acquisition exceeded active deadline")
            self.write_failures.append({"frame_bytes": len(encoded), "bytes_written": 0, "reason": "write_lock_deadline"})
            raise TimeoutError("deadline expired while waiting for peer stdin write lock")
        written = 0
        try:
            self.meter.ensure_active()
            fd = self.proc.stdin.fileno()
            os.set_blocking(fd, False)
            view = memoryview(encoded)
            with selectors.DefaultSelector() as selector:
                selector.register(fd, selectors.EVENT_WRITE)
                while written < len(encoded):
                    self.meter.ensure_active()
                    remaining = deadline - self.clock()
                    if remaining <= 0:
                        raise TimeoutError("active deadline expired during peer stdin frame write")
                    if not selector.select(remaining):
                        raise TimeoutError("peer stdin stayed unread through the active deadline")
                    try:
                        with self.meter.lock:
                            if self.meter.aborted or self.clock() >= deadline:
                                raise TimeoutError("peer stdin frame write reached the deadline or campaign abort")
                            amount = _write_pipe(fd, view[written:])
                            if self.clock() >= deadline:
                                raise TimeoutError("peer stdin frame write completed after the active deadline")
                    except BlockingIOError:
                        continue
                    if amount <= 0:
                        raise BrokenPipeError("peer stdin accepted zero bytes")
                    written += amount
            self.protocol_out.append({"frame_bytes": len(encoded), "method": frame.get("method"), "id": frame.get("id")})
        except (BrokenPipeError, OSError, TimeoutError, AdmissionError) as error:
            self.meter.abort(type(error).__name__ + ": " + str(error))
            self.write_failures.append({"frame_bytes": len(encoded), "bytes_written": written, "reason": type(error).__name__})
            raise
        finally:
            self._write_lock.release()

    def _client_request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        self._request_id += 1
        request_id = self._request_id
        self._send_frame({"method": method, "id": request_id, "params": params})
        while True:
            frame = self._next_frame()
            if frame.get("id") == request_id and ("result" in frame or "error" in frame):
                if "error" in frame:
                    raise ProtocolError(f"peer rejected {method}: {frame['error']}")
                result = frame.get("result")
                if not isinstance(result, dict):
                    raise ProtocolError(f"peer returned non-object result for {method}")
                return result
            self._observe_incoming(frame)

    @staticmethod
    def _require_keys(value: dict[str, Any], required: set[str], label: str) -> None:
        if not required.issubset(value):
            raise ProtocolError(f"{label} omitted required generated-schema fields")

    def _serve_requests(self) -> None:
        executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="s06-callback")
        pending: set[Future[Any]] = set()
        eof = False
        try:
            while not eof or pending:
                self.meter.ensure_active()
                for future in list(pending):
                    if future.done():
                        pending.remove(future)
                        with self._callback_futures_lock:
                            self._callback_futures.discard(future)
                        try:
                            future.result()
                        except Exception as error:
                            self.failed = self.failed or (type(error).__name__ + ": " + str(error))
                            self.meter.abort(self.failed)
                if eof:
                    if not pending:
                        break
                    time.sleep(0.005)
                    continue
                deadline = self.meter.deadline
                assert deadline is not None
                try:
                    value = self._frames.get(timeout=min(0.05, max(0.001, deadline - self.clock())))
                except queue.Empty:
                    if self.proc is not None and self.proc.poll() is not None:
                        # Drain the final EOF marker on the next iteration.
                        continue
                    continue
                if value is _EOF:
                    self.terminal["stdout_eof_observed"] = True
                    eof = True
                    continue
                if isinstance(value, Exception):
                    raise ProtocolError(f"stdout reader failed: {value}") from value
                raw = bytes(value)
                frame = _decode_json_frame(raw.rstrip(b"\r\n"))
                record = {"frame_bytes": len(raw), "method": frame.get("method"), "id": frame.get("id"), "received_monotonic": self.clock()}
                if frame.get("method") == "item/tool/call" and isinstance(frame.get("params"), dict):
                    record.update({key: frame["params"].get(key) for key in ("callId", "threadId", "turnId", "tool")})
                self.protocol_in.append(record)
                if (
                    isinstance(frame.get("method"), str)
                    and frame["method"] in self.SERVER_REQUEST_METHODS
                ) or ("method" in frame and "id" in frame):
                    if self._terminal_frame_seen:
                        raise ProtocolError("tool callback arrived after a terminal turn frame")
                    future = executor.submit(self._serve_tool_request, frame)
                    pending.add(future)
                    with self._callback_futures_lock:
                        self._callback_futures.add(future)
                else:
                    self._observe_incoming(frame)
            if not self._has_one_matching_completed_turn() and self._terminal_fact_error is None:
                self._terminal_fact_error = "clean stdout EOF without one matching completed turn"
                self.meter.abort(self._terminal_fact_error)
        except (AdmissionError, TimeoutError) as error:
            self.failed = type(error).__name__ + ": " + str(error)
            self.meter.abort(self.failed)
            raise
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

    def _observe_incoming(self, frame: dict[str, Any]) -> None:
        method = frame.get("method")
        if method == "turn/completed":
            self._record_turn_terminal(frame)
        # The fake peer may report any usage, time, load, or outcome. Only the
        # method name and frame size are retained; its claims never enter proof.
        self.notifications.append({"method": method, "frame_bytes": self.protocol_in[-1]["frame_bytes"] if self.protocol_in else 0})

    def _record_turn_terminal(self, frame: dict[str, Any]) -> None:
        self._terminal_frame_seen = True
        params = frame.get("params")
        turn = params.get("turn") if isinstance(params, dict) else None
        status = turn.get("status") if isinstance(turn, dict) else None
        turn_id = turn.get("id") if isinstance(turn, dict) else None
        required = {"id", "rootTurnId", "items", "itemsView", "status", "error", "startedAt", "completedAt", "durationMs"}
        well_formed = (
            isinstance(params, dict)
            and params.get("threadId") == self._thread_id
            and isinstance(turn, dict)
            and required.issubset(turn)
            and turn_id == self._turn_id
            and (turn.get("rootTurnId") is None or isinstance(turn.get("rootTurnId"), str))
            and isinstance(turn.get("items"), list)
            and turn.get("itemsView") in {"notLoaded", "summary", "full"}
            and status in {"completed", "failed", "interrupted"}
            and (turn.get("error") is None or isinstance(turn.get("error"), dict))
            and (turn.get("startedAt") is None or isinstance(turn.get("startedAt"), (int, float)))
            and (turn.get("completedAt") is None or isinstance(turn.get("completedAt"), (int, float)))
            and (turn.get("durationMs") is None or isinstance(turn.get("durationMs"), (int, float)))
        )
        if status == "completed" and isinstance(turn, dict):
            well_formed = well_formed and turn.get("completedAt") is not None
        record = {
            "method": "turn/completed",
            "thread_id": params.get("threadId") if isinstance(params, dict) else None,
            "turn_id": turn_id,
            "status": status,
            "well_formed_and_matching": bool(well_formed),
            "observed_monotonic": self.clock(),
        }
        self.protocol_terminals.append(record)
        if len(self.protocol_terminals) > 1:
            self._terminal_fact_error = "duplicate or contradictory turn terminal frames"
        elif not well_formed:
            self._terminal_fact_error = "turn terminal frame is malformed or has wrong thread/turn IDs"
        elif status != "completed":
            self._terminal_fact_error = "turn terminal status was " + str(status)
        if self._terminal_fact_error is not None:
            self.meter.abort(self._terminal_fact_error)

    def _has_one_matching_completed_turn(self) -> bool:
        return (
            len(self.protocol_terminals) == 1
            and self.protocol_terminals[0]["well_formed_and_matching"]
            and self.protocol_terminals[0]["status"] == "completed"
            and self._terminal_fact_error is None
        )

    def _serve_tool_request(self, frame: dict[str, Any]) -> None:
        request_id = frame.get("id")
        params = frame.get("params")
        call_id = params.get("callId") if isinstance(params, dict) else None
        action = params.get("tool") if isinstance(params, dict) else "malformed"
        started = self.clock()
        callback_record: dict[str, Any] = {
            "request_id": request_id,
            "call_id": call_id,
            "thread_id": params.get("threadId") if isinstance(params, dict) else None,
            "turn_id": params.get("turnId") if isinstance(params, dict) else None,
            "tool": action,
            "recipient": self.lane,
            "started_monotonic": started,
            "state": "started",
        }
        transfer: dict[str, Any] | None = None
        reservation_token: str | None = None
        envelope_valid = False
        try:
            self.meter.admit_attempt(action=str(action))
            # RequestId's generated JSON schema is string | int64. Python bool
            # is an int subclass, so exact types matter at this dispatch seam.
            valid_id = type(request_id) is str or (
                type(request_id) is int and -(2**63) <= request_id < 2**63
            )
            if set(frame) != {"method", "id", "params"} or not valid_id:
                raise ProtocolError("server request has an invalid RequestId or envelope")
            if frame["method"] != "item/tool/call":
                raise ProtocolError("unsupported server request method")
            envelope_valid = True
            tool_result, transfer = self._dispatch_callback(params)
            reservation_token = transfer.get("reservation_token") if transfer is not None else None
            items = tool_result["contentItems"]
            callback_record["response_items"] = [
                {"text_bytes": len(item["text"].encode("utf-8")), "sha256": hashlib.sha256(item["text"].encode("utf-8")).hexdigest()}
                for item in items
            ]
            response = {"id": request_id, "result": tool_result}
            frame_bytes = len(json.dumps(response, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) + 1
            self.meter.reserve_reply(items, recipient=self.lane, frame_bytes=frame_bytes)
            self._send_frame(response)
            if transfer is not None and reservation_token is not None:
                self.meter.commit_span(reservation_token)
                transfer.pop("reservation_token", None)
                reservation_token = None
            callback_record["state"] = "delivered" if tool_result["success"] else "rejected"
            callback_record["response_frame_bytes"] = frame_bytes
            if transfer is not None:
                transfer["call_id"] = call_id
                transfer["recipient"] = self.lane
                transfer["write_completed"] = True
                self.transfers.append(transfer)
                self._update_full_source(transfer["source_id"])
        except (AdmissionError, BrokenPipeError, OSError, ProtocolError, SourceError, TimeoutError) as error:
            if reservation_token is not None:
                self.meter.release_span(reservation_token)
            callback_record["state"] = "delivery_failed" if isinstance(error, (BrokenPipeError, OSError, TimeoutError)) else "rejected"
            callback_record["error"] = type(error).__name__
            callback_record["message"] = str(error)[:512]
            if not envelope_valid or isinstance(error, (BrokenPipeError, OSError, TimeoutError)) or (
                isinstance(error, AdmissionError) and (
                    "deadline" in str(error) or "cap exhausted" in str(error) or "campaign aborted" in str(error)
                )
            ):
                self.failed = self.failed or (type(error).__name__ + ": " + str(error))
                self.meter.abort(self.failed)
            else:
                self.callback_rejections.append({"call_id": call_id, "tool": action, "error": type(error).__name__, "message": str(error)[:512]})
            # If admission still allows it, return a charged error text. If not,
            # stop without a free diagnostic allowance.
            if not isinstance(error, AdmissionError) or "tool attempt cap" not in str(error):
                try:
                    text = _json_text({"error": type(error).__name__, "message": str(error)[:512]})
                    items = [{"type": "inputText", "text": text}]
                    response = {"id": request_id, "result": {"contentItems": items, "success": False}}
                    frame_bytes = len(json.dumps(response, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) + 1
                    self.meter.reserve_reply(items, recipient=self.lane, frame_bytes=frame_bytes)
                    self._send_frame(response)
                    callback_record["response_items"] = [{"text_bytes": len(text.encode("utf-8")), "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}]
                    callback_record["response_frame_bytes"] = frame_bytes
                except (AdmissionError, BrokenPipeError, OSError):
                    callback_record["state"] = "no_response_budget_or_pipe"
        finally:
            callback_record["finished_monotonic"] = self.clock()
            callback_record["duration_ms"] = max(0, int((callback_record["finished_monotonic"] - started) * 1000))
            self.callback_observations.append(callback_record)

    def _dispatch_callback(self, params: Any) -> tuple[dict[str, Any], dict[str, Any] | None]:
        if not isinstance(params, dict):
            raise ProtocolError("item/tool/call params must be an object")
        required = {"threadId", "turnId", "callId", "namespace", "tool", "arguments"}
        if set(params) != required:
            raise ProtocolError("item/tool/call params do not match DynamicToolCallParams")
        if params["threadId"] != self._thread_id or params["turnId"] != self._turn_id:
            raise ProtocolError("callback belongs to a different observed thread or turn")
        if not isinstance(params["callId"], str) or not params["callId"]:
            raise ProtocolError("DynamicToolCallParams.callId must be a non-empty string")
        if params["namespace"] != self.TOOL_NAMESPACE:
            raise ProtocolError("unsupported dynamic tool namespace")
        tool = params["tool"]
        args = params["arguments"]
        if not isinstance(tool, str) or not isinstance(args, dict):
            raise ProtocolError("dynamic tool name and arguments have invalid types")
        if tool in self.CLI_COMMANDS:
            payload = self._run_cli_tool(tool, args)
            text = _json_text(payload)
            return {"contentItems": [{"type": "inputText", "text": text}], "success": True}, None
        if tool in self.SOURCE_COMMANDS:
            body, transfer = self._read_source(tool, args)
            text = _json_text(body)
            return {"contentItems": [{"type": "inputText", "text": text}], "success": True}, transfer
        raise ProtocolError("tool is outside the read-only tree/browse/discover/get/read_path/read_chunks allowlist")

    def _run_cli_tool(self, tool: str, args: dict[str, Any]) -> dict[str, Any]:
        if tool == "tree":
            self._exact_keys(args, {"view", "depth"})
            view, depth = args["view"], args["depth"]
            if view not in {"collections", "subjects"} or isinstance(depth, bool) or not isinstance(depth, int) or not 0 <= depth <= 20:
                raise ProtocolError("invalid tree request")
            argv = ["tree", "--view", view, "--depth", str(depth), "--json"]
        elif tool == "browse":
            self._exact_keys(args, {"node_id", "limit"})
            node_id, limit = args["node_id"], args["limit"]
            if not isinstance(node_id, str) or node_id not in self.tree_nodes:
                raise ProtocolError("browse node must have been observed from tree")
            if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 100:
                raise ProtocolError("invalid browse limit")
            argv = ["browse", "--node", node_id, "--limit", str(limit), "--json"]
        elif tool == "discover":
            self._exact_keys(args, {"query"})
            query = args["query"]
            if not isinstance(query, str) or not query.strip() or "\x00" in query or len(query.encode("utf-8")) > 4096:
                raise ProtocolError("query must be non-empty UTF-8 text up to 4096 bytes")
            # Every query is uncached; the value is a single argv element.
            argv = ["discover", "--query", query, "--namespace", "skills-db", "--json", "--no-cache", "--limit=20"]
        else:
            self._exact_keys(args, {"source_id"})
            source_id = args["source_id"]
            if not isinstance(source_id, str) or source_id not in self.descriptors:
                raise SourceError("get accepts only a source ID observed in a real CLI descriptor")
            argv = ["get", source_id, "--json"]

        observation = self._run_cli(argv)
        payload = observation["payload"]
        if tool == "tree":
            self._register_tree_nodes(payload.get("items", []))
        elif tool == "discover":
            self._record_query_outcomes(observation, payload)
        if tool in {"browse", "discover", "get"}:
            descriptors = payload.get("items", []) if tool != "discover" else payload.get("matches", [])
            if not isinstance(descriptors, list):
                raise SourceError("CLI descriptor collection is malformed")
            for descriptor in descriptors:
                self._register_descriptor(descriptor)
        if tool == "get":
            for descriptor in payload.get("items", []):
                delivery = descriptor.get("content_delivery", {}) if isinstance(descriptor, dict) else {}
                if delivery != {"mode": "descriptor_only", "content_loaded": False}:
                    raise SourceError("get must remain descriptor-only")
        return payload

    @staticmethod
    def _exact_keys(value: dict[str, Any], expected: set[str]) -> None:
        if set(value) != expected:
            raise ProtocolError("tool arguments contain missing or unsupported fields")

    def _run_cli(self, argv: list[str]) -> dict[str, Any]:
        if not argv or argv[0] not in self.CLI_COMMANDS:
            raise ProtocolError("CLI argv is outside the fixed read-only command set")
        if hashlib.sha256(Path(self.fixture.script).read_bytes()).hexdigest() != EXPECTED_CLI_SHA256:
            raise ProtocolError("copied skills-db CLI changed after controller admission")
        if any(not isinstance(arg, str) or "\x00" in arg for arg in argv):
            raise ProtocolError("CLI argv contains an invalid argument")
        self.meter.ensure_active()
        started = self.clock()
        command = [sys.executable, str(Path(self.fixture.script).resolve()), *argv]
        env = self.fixture.env({
            "PYTHONDONTWRITEBYTECODE": "1",
            "XDG_CACHE_HOME": str(self.fixture_root / "xdg-cache"),
            "XDG_CONFIG_HOME": str(self.fixture_root / "xdg-config"),
        })
        proc: subprocess.Popen[bytes] | None = None
        record: dict[str, Any] = {"argv": list(argv), "started_monotonic": started, "pid": None, "exit_code": None}
        try:
            with self._active_tools_lock:
                self.meter.ensure_active()
                proc = subprocess.Popen(
                    command,
                    cwd=str(self.fixture.repo),
                    env=env,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=False,
                    start_new_session=True,
                    close_fds=True,
                )
                record["pid"] = proc.pid
                self._active_tools[proc.pid] = proc
            while True:
                self.meter.ensure_active()
                remaining = self._remaining()
                try:
                    stdout, stderr = proc.communicate(timeout=min(0.05, remaining))
                    break
                except subprocess.TimeoutExpired:
                    continue
            self.meter.ensure_active()
            record["exit_code"] = proc.returncode
            record["stderr_bytes"] = len(stderr)
            if proc.returncode != 0:
                raise ProtocolError(f"read-only CLI exited {proc.returncode}: {stderr.decode('utf-8', errors='replace')[:512]}")
            try:
                payload = json.loads(stdout.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise ProtocolError(f"read-only CLI returned invalid JSON: {error}") from error
            if not isinstance(payload, dict):
                raise ProtocolError("read-only CLI returned a non-object JSON value")
            record["index_revision"] = payload.get("index_revision")
            record["status"] = payload.get("status")
            record["timed_out"] = False
            return {"payload": payload, "record": record}
        finally:
            record["finished_monotonic"] = self.clock()
            record["duration_ms"] = max(0, int((record["finished_monotonic"] - started) * 1000))
            self.cli_runs.append(record)
            if proc is not None:
                self._terminate_tool_group(proc)
                with self._active_tools_lock:
                    self._active_tools.pop(proc.pid, None)

    def _terminate_tool_group(self, proc: subprocess.Popen[bytes]) -> None:
        term_deadline = self.clock() + self.meter.limits.term_grace_seconds
        self._signal_group(proc, signal.SIGTERM)
        while self.clock() < term_deadline:
            try:
                os.killpg(proc.pid, 0)
            except (ProcessLookupError, PermissionError, OSError):
                break
            time.sleep(min(0.01, max(0.0, term_deadline - self.clock())))
        try:
            os.killpg(proc.pid, 0)
            group_alive = True
        except (ProcessLookupError, PermissionError, OSError):
            group_alive = False
        if group_alive:
            self._signal_group(proc, signal.SIGKILL)
        teardown_deadline = self.clock() + self.meter.limits.teardown_seconds
        while group_alive and self.clock() < teardown_deadline:
            try:
                os.killpg(proc.pid, 0)
            except (ProcessLookupError, PermissionError, OSError):
                group_alive = False
                break
            time.sleep(min(0.01, max(0.0, teardown_deadline - self.clock())))
        if group_alive:
            self.meter.abort("owned CLI process group survived TERM and KILL")
        if proc.poll() is None:
            try:
                proc.wait(timeout=max(0.0, teardown_deadline - self.clock()))
            except subprocess.TimeoutExpired:
                self.meter.abort("owned CLI process survived TERM and KILL")

    def _remaining(self) -> float:
        self.meter.ensure_active()
        deadline = self.meter.deadline
        assert deadline is not None
        return max(0.001, deadline - self.clock())

    @staticmethod
    def _signal_group(proc: subprocess.Popen[bytes], sig: int) -> None:
        try:
            os.killpg(proc.pid, sig)
        except (ProcessLookupError, PermissionError, OSError):
            pass

    def _register_tree_nodes(self, items: list[Any]) -> None:
        for item in items:
            if not isinstance(item, dict):
                continue
            node_id = item.get("id")
            if isinstance(node_id, str):
                self.tree_nodes.add(node_id)
            self._register_tree_nodes(item.get("children", []))

    def _register_descriptor(self, descriptor: Any) -> None:
        if not isinstance(descriptor, dict):
            raise SourceError("CLI returned a non-object source descriptor")
        source_id = descriptor.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            raise SourceError("source descriptor has no source ID")
        validated = self._validate_descriptor(descriptor)
        self._store_descriptor(validated, complete="bundle" in descriptor)
        bundle = descriptor.get("bundle")
        if isinstance(bundle, dict):
            bundle_id = bundle.get("bundle_id")
            revision = bundle.get("revision")
            members = bundle.get("members")
            ids = descriptor.get("bundle_member_source_ids")
            if not isinstance(bundle_id, str) or not isinstance(revision, str) or not isinstance(members, list) or not isinstance(ids, list):
                raise SourceError("bundle closure descriptor is incomplete")
            if descriptor.get("bundle_revision") != revision:
                raise SourceError("bundle revision fields disagree")
            member_ids = []
            for member in members:
                member_valid = self._validate_descriptor(member)
                member_ids.append(member_valid["source_id"])
                self._store_descriptor(member_valid, complete=False)
            if len(member_ids) != len(set(member_ids)) or set(member_ids) != set(ids) or len(member_ids) != bundle.get("member_count"):
                raise SourceError("bundle members do not match the required source-ID closure")
            self.bundle_specs[bundle_id] = {"revision": revision, "member_ids": sorted(member_ids)}

    def _store_descriptor(self, descriptor: dict[str, Any], *, complete: bool) -> None:
        source_id = descriptor["source_id"]
        current = self.descriptors.get(source_id)
        if current is None:
            self.descriptors[source_id] = descriptor
            return
        core = ("source_id", "path", "realpath", "digest", "index_revision", "relative_path")
        if any(current.get(key) != descriptor.get(key) for key in core):
            raise SourceError("source ID was returned with conflicting index/path/digest descriptors")
        current_complete = current.get("bundle_id") is not None and bool(current.get("bundle_member_source_ids"))
        if complete or not current_complete:
            self.descriptors[source_id] = descriptor

    def _validate_descriptor(self, descriptor: dict[str, Any]) -> dict[str, Any]:
        source_id = descriptor.get("source_id")
        path_value = descriptor.get("path")
        real_value = descriptor.get("realpath")
        digest = descriptor.get("digest")
        revision = descriptor.get("index_revision")
        if not isinstance(source_id, str) or not isinstance(path_value, str) or not isinstance(real_value, str):
            raise SourceError("descriptor is missing source ID/path/realpath")
        if not isinstance(digest, str) or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise SourceError("descriptor digest is not lower-case SHA-256")
        if not isinstance(revision, str) or not revision:
            raise SourceError("descriptor omitted index revision")
        source_path = Path(path_value)
        real_path = Path(real_value)
        try:
            resolved = source_path.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            raise SourceError("descriptor path does not resolve to a local file") from error
        if not resolved.is_file() or str(resolved) != str(real_path) or not _within(resolved, self.approved_root):
            raise SourceError("descriptor path escaped or disagrees with the approved source root")
        if descriptor.get("local_path", path_value) != path_value:
            raise SourceError("local_path and path descriptor fields disagree")
        if descriptor.get("content_revision", digest) != digest:
            raise SourceError("descriptor content revision disagrees with its digest")
        source_record = descriptor.get("source_record")
        if isinstance(source_record, dict):
            if source_record.get("real_path") != real_value or source_record.get("relative_path") != descriptor.get("source_scope", {}).get("relative_path"):
                raise SourceError("source record does not match descriptor path scope")
            if source_record.get("sha256") not in {None, digest}:
                raise SourceError("source record digest disagrees with the descriptor")
        return {
            "source_id": source_id,
            "path": str(resolved),
            "realpath": str(real_path),
            "digest": digest,
            "index_revision": revision,
            "relative_path": descriptor.get("relative_path") or descriptor.get("source_scope", {}).get("relative_path"),
            "bundle_id": descriptor.get("bundle_id"),
            "bundle_revision": descriptor.get("bundle_revision"),
            "bundle_member_source_ids": list(descriptor.get("bundle_member_source_ids", [])),
        }

    def _read_source(self, tool: str, args: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        source_id = args.get("source_id")
        descriptor = self.descriptors.get(source_id) if isinstance(source_id, str) else None
        if descriptor is None:
            raise SourceError("source reads require an ID from a real returned descriptor")
        if tool == "read_path":
            self._exact_keys(args, {"source_id"})
            start, end = 0, None
        else:
            self._exact_keys(args, {"source_id", "start_byte", "end_byte"})
            start, end = args["start_byte"], args["end_byte"]
            if isinstance(start, bool) or isinstance(end, bool) or not isinstance(start, int) or not isinstance(end, int):
                raise SourceError("byte spans require integer start/end offsets")
        path = Path(descriptor["path"]).resolve(strict=True)
        if str(path) != descriptor["realpath"] or not _within(path, self.approved_root):
            raise SourceError("source realpath changed or escaped the approved fixture root")
        file_size = path.stat().st_size
        if end is None:
            end = file_size
        if not (0 <= start < end <= file_size):
            raise SourceError("source span is empty, reversed, or outside the current file")
        reservation_token = uuid.uuid4().hex
        self.meter.reserve_span(
            reservation_token,
            source_id,
            descriptor["digest"],
            descriptor["index_revision"],
            start,
            end,
        )
        try:
            try:
                current = self._run_cli(["get", source_id, "--json"])["payload"]
            except ProtocolError as error:
                raise SourceError("source ID is no longer admitted by the current CLI index") from error
            current_items = current.get("items")
            if (
                current.get("status") != "ok"
                or not isinstance(current_items, list)
                or len(current_items) != 1
                or not isinstance(current_items[0], dict)
                or current_items[0].get("content_delivery") != {"mode": "descriptor_only", "content_loaded": False}
            ):
                raise SourceError("current CLI get did not return one descriptor-only source")
            current_descriptor = self._validate_descriptor(current_items[0])
            if current_descriptor != descriptor:
                changed = {key: [descriptor.get(key), current_descriptor.get(key)] for key in descriptor if descriptor.get(key) != current_descriptor.get(key)}
                raise SourceError("source ID/index/path/digest changed after descriptor admission: " + _json_text(changed))
            raw = path.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            if len(raw) != file_size or digest != descriptor["digest"]:
                raise SourceError("source size or digest changed after descriptor admission")
            body = raw[start:end]
            try:
                text = body.decode("utf-8")
            except UnicodeDecodeError as error:
                raise SourceError("source bytes are not a lossless UTF-8 text representation") from error
            if text.encode("utf-8") != body:
                raise SourceError("source text changed during UTF-8 round trip")
            eof = end == len(raw)
            transfer = {
                "source_id": source_id,
                "path": str(path),
                "digest": digest,
                "index_revision": descriptor["index_revision"],
                "start_byte": start,
                "end_byte": end,
                "file_size": len(raw),
                "eof": eof,
                "text_bytes": len(body),
                "reservation_token": reservation_token,
            }
            return {
                "source_id": source_id,
                "digest": digest,
                "index_revision": descriptor["index_revision"],
                "start_byte": start,
                "end_byte": end,
                "file_size": len(raw),
                "eof": eof,
                "text": text,
            }, transfer
        except BaseException:
            self.meter.release_span(reservation_token)
            raise

    def _record_query_outcomes(self, observation: dict[str, Any], payload: dict[str, Any]) -> None:
        record = observation["record"]
        groups = payload.get("query_groups")
        if (
            record.get("exit_code") != 0
            or record.get("timed_out") is not False
            or not isinstance(record.get("argv"), list)
            or not record["argv"]
            or record["argv"][0] != "discover"
            or "--no-cache" not in record["argv"]
            or payload.get("evaluation_origin") != "cli_evaluation"
            or payload.get("index_revision") != record.get("index_revision")
            or not isinstance(groups, list)
        ):
            return
        for group in groups:
            if not isinstance(group, dict):
                continue
            predicate = group.get("predicate_fingerprint")
            request = group.get("request_fingerprint")
            if (
                group.get("kind") != "query"
                or group.get("evaluated") is not True
                or group.get("evaluation_origin") != "cli_evaluation"
                or group.get("duplicate_of") is not None
                or group.get("status") not in {"ok", "empty"}
                or not isinstance(predicate, str)
                or len(predicate) != 64
                or any(character not in "0123456789abcdef" for character in predicate)
                or not isinstance(request, str)
                or len(request) != 64
                or any(character not in "0123456789abcdef" for character in request)
            ):
                continue
            self.query_observations.setdefault(
                predicate,
                {
                    "predicate_fingerprint": predicate,
                    "request_fingerprint": request,
                    "index_revision": record.get("index_revision"),
                    "argv": list(record["argv"]),
                    "evaluated": True,
                    "status": group["status"],
                    "duplicate_of": None,
                    "controller_started_monotonic": record["started_monotonic"],
                    "controller_finished_monotonic": record["finished_monotonic"],
                    "cli_exit_code": record["exit_code"],
                    "evaluation_origin": "cli_evaluation",
                },
            )

    def _bundle_completion(self) -> list[dict[str, Any]]:
        output = []
        for bundle_id, spec in sorted(self.bundle_specs.items()):
            member_ids = spec["member_ids"]
            complete = bool(member_ids) and all(source_id in self.full_sources for source_id in member_ids)
            output.append({"bundle_id": bundle_id, "revision": spec["revision"], "member_source_ids": member_ids, "complete_after_written_transfers": complete})
        return output

    def _update_full_source(self, source_id: str) -> None:
        descriptor = self.descriptors.get(source_id)
        if descriptor is None:
            return
        try:
            file_size = Path(descriptor["path"]).stat().st_size
        except OSError:
            return
        spans = sorted(
            (item["start_byte"], item["end_byte"])
            for item in self.transfers
            if item["source_id"] == source_id and item["write_completed"]
        )
        cursor = 0
        for start, end in spans:
            if start != cursor:
                return
            cursor = end
        if cursor == file_size and file_size > 0:
            self.full_sources.add(source_id)

    def _cleanup_owned_processes(self) -> None:
        started = self.clock()
        if self.failed is not None:
            self.meter.abort(self.failed)
        processes: list[subprocess.Popen[bytes]] = []
        if self.proc is not None:
            processes.append(self.proc)
        with self._active_tools_lock:
            processes.extend(self._active_tools.values())
        processes = list({proc.pid: proc for proc in processes}.values())
        with self._callback_futures_lock:
            callback_futures = list(self._callback_futures)
        for future in callback_futures:
            future.cancel()
        grace = self.meter.limits.term_grace_seconds
        term_deadline = started + grace
        for proc in processes:
            self._signal_group(proc, signal.SIGTERM)
        for proc in processes:
            try:
                remaining = max(0.0, term_deadline - self.clock())
                if remaining:
                    proc.wait(timeout=remaining)
            except subprocess.TimeoutExpired:
                pass
        # Wait on the group, not only its leader, for the whole TERM grace.
        # A peer may exit while a child still holds its stdout pipe.
        while self.clock() < term_deadline:
            alive = False
            for proc in processes:
                try:
                    os.killpg(proc.pid, 0)
                    alive = True
                except (ProcessLookupError, PermissionError, OSError):
                    pass
            if not alive:
                break
            time.sleep(min(0.01, max(0.0, term_deadline - self.clock())))
        # Killing the leader does not prove its process group is gone. Send KILL
        # to any remaining members after the full TERM grace for the group.
        for proc in processes:
            try:
                os.killpg(proc.pid, 0)
            except (ProcessLookupError, PermissionError, OSError):
                continue
            self._signal_group(proc, signal.SIGKILL)
        teardown_deadline = started + grace + self.meter.limits.teardown_seconds
        for proc in processes:
            try:
                proc.wait(timeout=max(0.0, teardown_deadline - self.clock()))
            except subprocess.TimeoutExpired:
                self.failed = self.failed or "TimeoutError: owned child survived TERM and KILL"
        for stream in (self.proc.stdin, self.proc.stdout, self.proc.stderr) if self.proc is not None else ():
            if stream is not None:
                try:
                    stream.close()
                except OSError:
                    pass
        for future in callback_futures:
            try:
                future.result(timeout=max(0.0, teardown_deadline - self.clock()))
            except (TimeoutError, Exception):
                pass
        for thread in (self._reader, self._stderr_reader):
            if thread is not None:
                thread.join(timeout=max(0.0, teardown_deadline - self.clock()))
        groups_gone = []
        for proc in processes:
            try:
                os.killpg(proc.pid, 0)
                groups_gone.append(False)
            except (ProcessLookupError, PermissionError, OSError):
                groups_gone.append(True)
        if not all(groups_gone):
            self.failed = self.failed or "TimeoutError: owned process group survived cleanup"
        callbacks_stopped = all(future.done() for future in callback_futures)
        reader_threads_stopped = all(thread is None or not thread.is_alive() for thread in (self._reader, self._stderr_reader))
        if not callbacks_stopped:
            self.failed = self.failed or "TimeoutError: callback worker survived local teardown"
        if not reader_threads_stopped:
            self.failed = self.failed or "TimeoutError: stdio reader survived local teardown"
        self.terminal["cleanup"] = {
            "term_grace_seconds": grace,
            "teardown_seconds": self.meter.limits.teardown_seconds,
            "owned_processes": [{"pid": proc.pid, "returncode": proc.poll()} for proc in processes],
            "process_groups_gone": groups_gone,
            "reader_threads_stopped": reader_threads_stopped,
            "callbacks_stopped": callbacks_stopped,
            "elapsed_ms": max(0, int((self.clock() - started) * 1000)),
        }

    def observation(self) -> dict[str, Any]:
        return {
            "schema": "s06.scripted-controller-observation.v1",
            "run_kind": "scripted_fixture",
            "campaign_id": self.run_id,
            "lane": self.lane,
            "cli_sha256": self.cli_sha256,
            "thread_id": self._thread_id,
            "turn_id": self._turn_id,
            "budget": self.meter.observation(),
            "protocol_out": list(self.protocol_out),
            "protocol_in": list(self.protocol_in),
            "write_failures": list(self.write_failures),
            "notifications": list(self.notifications),
            "callback_rejections": list(self.callback_rejections),
            "callback_observations": list(self.callback_observations),
            "cli_runs": list(self.cli_runs),
            "query_observations": list(self.query_observations.values()),
            "source_descriptors_observed": sorted(self.descriptors),
            "source_transfers": list(self.transfers),
            "bundle_delivery": self._bundle_completion(),
            "terminal": dict(self.terminal),
            "peer_stderr": self.stderr_text,
            "peer_claims_used_as_evidence": False,
        }

    def write_evidence(self) -> Path:
        if self._evidence_path is not None:
            return self._evidence_path
        evidence_root = RUN_ROOT / "evidence"
        evidence_root.mkdir(parents=True, exist_ok=True)
        if self.run_id is None:
            self.run_id = f"offline-{time.time_ns()}-{os.getpid()}-{uuid.uuid4().hex[:12]}"
        run_dir = evidence_root / self.run_id
        run_dir.mkdir(parents=False, exist_ok=False)
        path = run_dir / "controller.json"
        path.write_text(json.dumps(self.observation(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self._evidence_path = path
        return self._evidence_path
