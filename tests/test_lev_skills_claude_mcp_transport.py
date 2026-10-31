from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import hashlib

from skills_db_agent_controller import AdmissionError, BudgetLimits, CampaignMeter, MAX_CLI_STDERR_BYTES, MAX_CLI_STDOUT_BYTES, ProtocolError, SkillsCliProfile, ScriptedSkillsController, SourceError
from skills_db_claude_mcp_transport import ClaudeMCPServer, MCPTransportError, _cli_operation_overlap, actual_cli_overlap, build_campaign_profile, build_claude_launch_profile, build_mcp_config, ensure_complete_tool_results, match_tool_result_event, supervise_agent_process


def frame(method: str, request_id: int | str | None, params: object = None) -> bytes:
    value = {"jsonrpc": "2.0", "method": method}
    if request_id is not None:
        value["id"] = request_id
    if params is not None:
        value["params"] = params
    return json.dumps(value, separators=(",", ":")).encode() + b"\n"


class ControllerStub:
    CLI_COMMANDS = {"tree", "browse", "discover", "get"}
    SOURCE_COMMANDS = {"read_path", "read_chunks"}

    def __init__(self, meter: CampaignMeter, callback=None):
        self.meter = meter
        self.callback = callback
        self.transfers = []
        self.cli_runs = []
        self.full_sources = set()
        self.cancelled = []
        self.calls = []

    def _run_cli_tool(self, name, args):
        self.calls.append((name, args))
        if self.callback:
            return self.callback(name, args)
        return {"status": "ok", "name": name, "args": args}

    def _read_source(self, name, args):
        raise AssertionError("source reads are not expected in this test")

    def _update_full_source(self, source_id):
        self.full_sources.add(source_id)

    def terminate_active_tools(self, reason, *, stop_started=None, wait=True):
        self.cancelled.append(reason)
        self.meter.abort(reason)
        return {"survivor_pids": []}


class ClaudeMCPTransportTest(unittest.TestCase):
    def server(self, controller=None, *, limits=BudgetLimits(), task="task", instruction="instructions", max_pending=8, initialized=True):
        meter = controller.meter if controller else CampaignMeter(limits)
        controller = controller or ControllerStub(meter)
        server = ClaudeMCPServer(controller, task_text=task, instruction_text=instruction, max_pending=max_pending)
        server.initialize_seen = initialized
        server.initialized = initialized
        return server

    def test_single_server_exposes_only_six_read_only_tools_and_dispatches_parallel_calls(self):
        both_running = threading.Event()
        lock = threading.Lock()
        state = {"active": 0, "maximum": 0}

        def callback(name, args):
            with lock:
                state["active"] += 1
                state["maximum"] = max(state["maximum"], state["active"])
                if state["active"] == 2:
                    both_running.set()
            self.assertTrue(both_running.wait(2), "independent MCP calls were serialized")
            with lock:
                state["active"] -= 1
            return {"status": "ok", "query": args.get("query")}

        meter = CampaignMeter()
        controller = ControllerStub(meter, callback)
        server = self.server(controller, initialized=False)
        inbound = b"".join([
            frame("initialize", "init", {"protocolVersion": "2025-11-25"}),
            frame("notifications/initialized", None),
            frame("tools/list", "list"),
            frame("tools/call", "a", {"name": "discover", "arguments": {"query": "one", "limit": 1}}),
            frame("tools/call", "b", {"name": "discover", "arguments": {"query": "two", "limit": 1}}),
        ])
        out = io.BytesIO()
        report = server.serve(io.BytesIO(inbound), out)
        messages = [json.loads(line) for line in out.getvalue().splitlines()]
        listed = next(message for message in messages if message.get("id") == "list")["result"]["tools"]
        self.assertEqual([tool["name"] for tool in listed], ["tree", "browse", "discover", "get", "read_path", "read_chunks"])
        self.assertTrue(all(tool["annotations"]["readOnlyHint"] is True for tool in listed))
        self.assertTrue(all(tool["_meta"]["anthropic/maxResultSizeChars"] == 262144 for tool in listed))
        self.assertEqual(state["maximum"], 2)
        self.assertEqual(report["meter"]["admitted_calls"], 2)
        self.assertEqual(report["meter"]["initial_text_bytes"], len("task") + len("instructions"))
        self.assertGreater(report["meter"]["reply_deliveries"][0]["text_bytes"], 0)  # tool schema was charged

    def test_oversized_success_is_replaced_by_a_small_charged_error_without_truncation(self):
        meter = CampaignMeter()
        controller = ControllerStub(meter, lambda *_: {"status": "ok", "large": "x" * 262145})
        server = self.server(controller)
        out = io.BytesIO()
        report = server.serve(io.BytesIO(frame("tools/call", "large", {"name": "discover", "arguments": {"query": "x"}})), out)
        message = json.loads(out.getvalue())
        content = message["result"]["content"][0]["text"]
        self.assertTrue(message["result"]["isError"])
        self.assertIn("per-reply cap", content)
        self.assertNotIn("x" * 1000, content)
        self.assertTrue(any(denial["kind"] == "reply" and denial["reason"] == "per_response_cap" for denial in report["meter"]["denials"]))

    def test_tool_attempt_161_is_charged_then_denied(self):
        meter = CampaignMeter()
        controller = ControllerStub(meter)
        server = self.server(controller)
        out = io.BytesIO()
        with ThreadPoolExecutor(max_workers=8) as executor:
            for index in range(160):
                server._handle(out, json.loads(frame("tools/call", index, {"name": "discover", "arguments": {"query": "q"}})), executor)
                with server.pending_lock:
                    future = server.pending.get(index)
                if future is not None:
                    future.result(timeout=2)
            server._handle(out, json.loads(frame("tools/call", 160, {"name": "discover", "arguments": {"query": "overflow"}})), executor)
        observation = meter.observation()
        self.assertEqual(observation["attempted_calls"], 161)
        self.assertEqual(observation["admitted_calls"], 160)
        self.assertTrue(any(denial.get("reason") == "call_cap" for denial in observation["denials"]))

    def test_duplicate_id_and_unknown_method_fail_closed(self):
        meter = CampaignMeter()
        controller = ControllerStub(meter)
        server = self.server(controller)
        out = io.BytesIO()
        with ThreadPoolExecutor(max_workers=2) as executor:
            call = json.loads(frame("tools/call", "same", {"name": "discover", "arguments": {"query": "q"}}))
            server._handle(out, call, executor)
            with server.pending_lock:
                first = server.pending.get("same")
            if first:
                first.result(timeout=2)
            self.assertTrue(server._handle(out, call, executor))
        self.assertIn("duplicate JSON-RPC id rejected", server.protocol_errors)
        self.assertEqual(meter.observation()["attempted_calls"], 2)
        with self.assertRaises(AdmissionError):
            meter.ensure_active()

    def test_broken_and_duplicate_json_frames_stop_before_dispatch(self):
        meter = CampaignMeter()
        controller = ControllerStub(meter)
        server = self.server(controller)
        bad = b'{"jsonrpc":"2.0","id":1,"id":2,"method":"tools/call"}\n'
        report = server.serve(io.BytesIO(bad), io.BytesIO())
        self.assertEqual(report["terminal"], "failed")
        self.assertEqual(meter.observation()["admitted_calls"], 1)
        self.assertEqual(controller.transfers, [])

    def test_stream_json_receiver_must_match_exact_admitted_text_and_unique_use_id(self):
        text = '{"source_id":"skills-db/x","text":"all bytes"}'
        deliveries = [{"request_id": 9, "text": text, "sha256": hashlib.sha256(text.encode()).hexdigest(), "pipe_write_completed": True, "tool_name": "get", "tool_arguments": {"source_id": "skills-db/x"}}]
        uses = {"use-1": {"tool": "get", "arguments": {"source_id": "skills-db/x"}}, "use-2": {"tool": "get", "arguments": {"source_id": "skills-db/x"}}}
        event = {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "use-1", "content": text}]}}
        self.assertEqual(match_tool_result_event(event, deliveries, tool_uses=uses)[0]["tool_use_id"], "use-1")
        ensure_complete_tool_results(deliveries)
        truncated = {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "use-2", "content": text[:-1]}]}}
        with self.assertRaises(MCPTransportError):
            match_tool_result_event(truncated, deliveries, tool_uses=uses)
        with self.assertRaises(MCPTransportError):
            ensure_complete_tool_results([{"request_id": "missing", "pipe_write_completed": True}])

    def test_launch_profile_pins_one_agent_and_requires_a_resolved_model(self):
        binary = Path(sys.executable).resolve()
        pins = dict(claude_binary=str(binary), claude_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(), claude_version="fixture", working_directory=tempfile.gettempdir())
        profile = build_claude_launch_profile(**pins, model="claude-model-from-live-catalog", model_catalog_ref="live-model-catalog#selected", system_prompt="instructions", task_text="task", mcp_config_path="/run/mcp.json")
        self.assertEqual(profile["mode"], "one_claude_print_agent_one_stdio_mcp_server")
        self.assertIn("--strict-mcp-config", profile["argv"])
        self.assertIn("--restricted", profile["argv"])
        self.assertNotIn("--bare", profile["argv"])
        self.assertEqual(profile["tools"], ["tree", "browse", "discover", "get", "read_path", "read_chunks"])
        with self.assertRaises(MCPTransportError):
            build_claude_launch_profile(**pins, model="", model_catalog_ref="live-model-catalog#selected", system_prompt="instructions", task_text="task", mcp_config_path="/run/mcp.json")

    def test_owned_campaign_and_mcp_config_profiles_are_bounded(self):
        profile = build_campaign_profile(task_text="task", instruction_text="instructions", backend="qmd", runtime_root="/Users/jean-patricksmith/.local/state/lev/skills-db-progressive-discovery/finish-20261017T083107Z/live-agent-coder", gateway_report_path="/Users/jean-patricksmith/.local/state/lev/skills-db-progressive-discovery/finish-20261017T083107Z/live-agent-coder/gateway.json", admitted_at=time.monotonic(), mode="offline_test")
        self.assertEqual(set(profile), {"task_text", "instruction_text", "admitted_at", "runtime_root", "backend", "gateway_report_path", "mode"})
        config = build_mcp_config(profile_file=profile["runtime_root"] + "/campaign.json", python_executable="/Users/jean-patricksmith/.pyenv/versions/3.13.4/bin/python3")
        server = config["mcpServers"]["skills-db"]
        self.assertEqual(server["type"], "stdio")
        self.assertEqual(server["args"][1:], ["serve", "--profile-file", profile["runtime_root"] + "/campaign.json"])
        self.assertIn("tests/skills_db_claude_mcp_transport.py", server["args"][0])
        with self.assertRaises(MCPTransportError):
            build_mcp_config(profile_file="/tmp/unowned.json", python_executable="python3")
        with self.assertRaises(MCPTransportError):
            build_campaign_profile(task_text="task", instruction_text="instructions", backend="implicit", runtime_root=profile["runtime_root"], gateway_report_path=profile["gateway_report_path"], admitted_at=time.monotonic())

    def test_public_path_load_uses_descriptor_digest_without_hidden_get(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source_root = root / "skills-db"
            source_root.mkdir()
            source = source_root / "example" / "SKILL.md"
            source.parent.mkdir()
            source.write_bytes(b"full source\n")
            pins = []
            for name in ("cli", "wrapper", "bridge", "inventory", "snapshot"):
                path = root / name
                path.write_text(name, encoding="utf-8")
                pins.append(path)
            profile = SkillsCliProfile.offline_test(
                repo_root=root,
                executable=pins[0],
                wrapper_path=pins[1],
                qmd_bridge_path=pins[2],
                inventory_path=pins[3],
                snapshot_path=pins[4],
                runtime_root=root / "run",
            )
            meter = CampaignMeter()
            meter.begin("task", "instruction")
            controller = ScriptedSkillsController(public_profile=profile, meter=meter)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            descriptor = {"source_id": "skills-db/example/SKILL.md", "path": str(source), "realpath": str(source.resolve()), "digest": digest, "index_revision": profile.catalog_revision, "relative_path": "example/SKILL.md", "bundle_id": None, "bundle_revision": None, "bundle_member_source_ids": []}
            controller.descriptors[descriptor["source_id"]] = descriptor
            controller._run_cli = lambda _argv: self.fail("direct path loading must not issue hidden get")
            body, transfer = controller._read_source("read_path", {"source_id": descriptor["source_id"]})
            self.assertEqual(body["text"], "full source\n")
            self.assertTrue(body["eof"])
            self.assertEqual(transfer["digest"], digest)
            self.assertEqual(len(meter.pending_spans), 1)
            self.assertEqual(controller.cli_runs, [])

    def test_public_path_load_rejects_source_digest_drift(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source_root = root / "skills-db"
            source_root.mkdir()
            source = source_root / "skill.md"
            source.write_bytes(b"before")
            pins = []
            for name in ("cli", "wrapper", "bridge", "inventory", "snapshot"):
                path = root / name
                path.write_text(name, encoding="utf-8")
                pins.append(path)
            profile = SkillsCliProfile.offline_test(repo_root=root, executable=pins[0], wrapper_path=pins[1], qmd_bridge_path=pins[2], inventory_path=pins[3], snapshot_path=pins[4], runtime_root=root / "run")
            meter = CampaignMeter()
            meter.begin("task", "instruction")
            controller = ScriptedSkillsController(public_profile=profile, meter=meter)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            descriptor = {"source_id": "skills-db/skill.md", "path": str(source), "realpath": str(source.resolve()), "digest": digest, "index_revision": profile.catalog_revision, "relative_path": "skill.md", "bundle_id": None, "bundle_revision": None, "bundle_member_source_ids": []}
            controller.descriptors[descriptor["source_id"]] = descriptor
            source.write_bytes(b"after")
            with self.assertRaises(SourceError):
                controller._read_source("read_path", {"source_id": descriptor["source_id"]})
            self.assertEqual(meter.pending_spans, {})

    def test_actual_owned_browse_discover_intervals_overlap_and_serial_spans_do_not(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repo = root / "repo"
            (repo / "skills-db").mkdir(parents=True)
            interval_dir = root / "intervals"
            interval_dir.mkdir()
            executable = root / "fake-cli.py"
            executable.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, pathlib, time\n"
                f"d=pathlib.Path({str(interval_dir)!r})\n"
                "start=time.monotonic(); time.sleep(0.2); end=time.monotonic()\n"
                "(d / f'{os.getpid()}.json').write_text(json.dumps({'start':start,'end':end}))\n"
                "print(json.dumps({'status':'ok','index_revision':'offline-test-revision','items':[]}))\n",
                encoding="utf-8",
            )
            executable.chmod(0o755)
            pins = []
            for name in ("wrapper", "bridge", "inventory", "snapshot"):
                path = root / name
                path.write_text(name, encoding="utf-8")
                pins.append(path)
            profile = SkillsCliProfile.offline_test(repo_root=repo, executable=executable, wrapper_path=pins[0], qmd_bridge_path=pins[1], inventory_path=pins[2], snapshot_path=pins[3], runtime_root=root / "run")
            meter = CampaignMeter()
            controller = ScriptedSkillsController(public_profile=profile, meter=meter)
            controller.tree_nodes.add("n")
            server = self.server(controller, initialized=False)
            inbound = b"".join([
                frame("initialize", "i", {"protocolVersion": "2025-11-25"}),
                frame("notifications/initialized", None),
                frame("tools/call", "a", {"name": "browse", "arguments": {"node_id": "n", "limit": 1}}),
                frame("tools/call", "b", {"name": "discover", "arguments": {"query": "q", "limit": 1}}),
            ])
            server.serve(io.BytesIO(inbound), io.BytesIO())
            runs = controller.cli_runs
            self.assertEqual(len(runs), 2)
            self.assertLess(max(run["started_monotonic"] for run in runs), min(run["finished_monotonic"] for run in runs))
            self.assertTrue(_cli_operation_overlap(runs, {"browse", "discover"}))
            self.assertFalse(actual_cli_overlap(runs), "offline fixtures cannot establish a public runtime gate")
            serialized = ScriptedSkillsController(public_profile=profile, meter=CampaignMeter())
            serialized.tree_nodes.add("n")
            cli_lock = threading.Lock()
            original_run_cli = serialized._run_cli
            def run_serially(argv):
                with cli_lock:
                    return original_run_cli(argv)
            serialized._run_cli = run_serially
            serial_server = self.server(serialized, initialized=False)
            serial_server.serve(io.BytesIO(inbound), io.BytesIO())
            self.assertEqual(len(serialized.cli_runs), 2)
            self.assertFalse(_cli_operation_overlap(serialized.cli_runs, {"browse", "discover"}))

    def test_cli_stdout_and_stderr_are_bounded_before_payload_parse(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            repo = root / "repo"
            (repo / "skills-db").mkdir(parents=True)
            executable = root / "fake-cli.py"
            executable.write_text(
                "#!/usr/bin/env python3\n"
                "import os,sys\n"
                f"if sys.argv[2]=='stdout': os.write(1,b'x'*{MAX_CLI_STDOUT_BYTES + 1})\n"
                f"else: os.write(2,b'e'*{MAX_CLI_STDERR_BYTES + 1})\n",
                encoding="utf-8",
            )
            executable.chmod(0o755)
            pins = []
            for name in ("wrapper", "bridge", "inventory", "snapshot"):
                path = root / name
                path.write_text(name, encoding="utf-8")
                pins.append(path)
            profile = SkillsCliProfile.offline_test(repo_root=repo, executable=executable, wrapper_path=pins[0], qmd_bridge_path=pins[1], inventory_path=pins[2], snapshot_path=pins[3], runtime_root=root / "run")
            meter = CampaignMeter()
            meter.begin("task", "instruction")
            controller = ScriptedSkillsController(public_profile=profile, meter=meter)
            for channel in ("stdout", "stderr"):
                with self.assertRaisesRegex(ProtocolError, "exceeded its bounded output size"):
                    controller._run_cli(["tree", channel])
            self.assertEqual(len(controller.cli_runs), 2)
            self.assertTrue(all(run["pid"] and run["finished_monotonic"] >= run["started_monotonic"] for run in controller.cli_runs))

    def test_foreign_tool_name_cannot_dispatch_a_cli_command(self):
        meter = CampaignMeter()
        controller = ControllerStub(meter)
        server = self.server(controller)
        out = io.BytesIO()
        server.serve(io.BytesIO(frame("tools/call", "foreign", {"name": "filesystem.read", "arguments": {"path": "/etc/passwd"}})), out)
        message = json.loads(out.getvalue())
        self.assertTrue(message["result"]["isError"])
        self.assertEqual(controller.calls, [])

    def test_idle_deadline_stops_server_without_a_new_request(self):
        meter = CampaignMeter(BudgetLimits(wall_seconds=0.05))
        controller = ControllerStub(meter)
        server = self.server(controller, limits=meter.limits)
        read_fd, write_fd = os.pipe()
        reader = os.fdopen(read_fd, "rb", buffering=0)
        result = {}
        thread = threading.Thread(target=lambda: result.update(server.serve(reader, io.BytesIO())), daemon=True)
        thread.start()
        thread.join(timeout=1)
        os.close(write_fd)
        reader.close()
        self.assertFalse(thread.is_alive())
        self.assertTrue(result["deadline_fired"])
        self.assertIn("active_deadline", controller.cancelled)

    def test_agent_process_supervisor_sends_term_then_kill_after_grace(self):
        proc = subprocess.Popen(
            [sys.executable, "-c", "import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(10)"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        report = supervise_agent_process(proc, started_monotonic=time.monotonic() - 1, wall_seconds=0.01, term_grace_seconds=0.05, teardown_seconds=0.2)
        self.assertEqual(report["state"], "deadline")
        self.assertIsNotNone(proc.poll())
        self.assertEqual(report["survivor_groups"], [])


if __name__ == "__main__":
    unittest.main()
