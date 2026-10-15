"""Connected scripted-fixture tests for the S06 controller boundary."""

from __future__ import annotations

from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import threading
import time
from typing import Any
import unittest
import skills_db_agent_controller as controller_module

from skills_db_agent_controller import (
    AdmissionError,
    BudgetLimits,
    CampaignMeter,
    DEFAULT_LIMITS,
    ProtocolError,
    RUN_ROOT,
    ScriptedSkillsController,
    SourceError,
)
import test_lev_skills_cli as cli_fixtures


QUERY = "controllerneedle"
MAIN_TEXT = "---\nname: bundle-target\ndescription: controllerneedle package source\n---\n# Bundle 🌊\n\nQuoted: \"read this\"\\path\n"
ASSET_BYTES = "# Required local note\nUnicode: 雪 and quotes: \"kept\"\n".encode("utf-8")
KNOWN_SERVER_REQUEST_METHODS = (
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
)


POSITIVE_PEER = r'''import json, os, sys, time

log_path = os.environ["S06_PEER_LOG"]
def log(value):
    with open(log_path, "a", encoding="utf-8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n")
def receive():
    raw = sys.stdin.buffer.readline()
    if not raw:
        raise EOFError("controller closed stdio")
    value = json.loads(raw.decode("utf-8"))
    log({"direction": "controller_to_peer", "frame": value})
    return value
def send(value):
    sys.stdout.write(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()
def reply(request, result):
    send({"id": request["id"], "result": result})
def thread_value():
    cwd = os.getcwd()
    return {
        "id": "thread-fixture-1", "environments": None, "extra": None, "sessionId": "session-fixture-1",
        "forkedFromId": None, "parentThreadId": None, "preview": "scripted fixture", "ephemeral": True,
        "section": None, "sectionEnteredAt": None, "projectId": None, "historyMode": "legacy",
        "modelProvider": "scripted_fixture", "model": "scripted_fixture", "reasoningEffort": None,
        "createdAt": 1, "updatedAt": 1, "recencyAt": None, "status": {"type": "idle"},
        "path": None, "cwd": cwd, "cliVersion": "fixture", "originator": None, "source": "unknown",
        "canAcceptDirectInput": True, "threadSource": "scripted_fixture", "agentNickname": None,
        "agentRole": None, "gitInfo": None, "name": None, "daybreakEnabled": None, "turns": [],
    }
def turn_value(status="inProgress"):
    return {"id": "turn-fixture-1", "rootTurnId": None, "items": [], "itemsView": "full",
            "status": status, "error": None, "startedAt": 1, "completedAt": 2 if status == "completed" else None,
            "durationMs": 1 if status == "completed" else None}

initialize = receive()
reply(initialize, {"userAgent": "codex-app-server/fixture", "codexHome": os.getcwd(),
                   "platformFamily": "unix", "platformOs": "test"})
initialized = receive()
thread_request = receive()
log({"dynamic_tools": thread_request["params"].get("dynamicTools")})
reply(thread_request, {
    "thread": thread_value(), "model": "scripted_fixture", "modelProvider": "scripted_fixture",
    "serviceTier": None, "disabledPluginIds": [], "cwd": os.getcwd(), "runtimeWorkspaceRoots": [],
    "instructionSources": [], "approvalPolicy": "never", "approvalsReviewer": "user",
    "sandbox": {"type": "readOnly", "networkAccess": False}, "activePermissionProfile": None,
    "reasoningEffort": None, "multiAgentMode": "explicitRequestOnly",
})
turn_request = receive()
task_text = turn_request["params"]["input"][0]["text"]
log({"task_text": task_text, "developer_instructions": thread_request["params"]["developerInstructions"]})
reply(turn_request, {"turn": turn_value()})
thread_id, turn_id = "thread-fixture-1", "turn-fixture-1"

def call(request_id, call_id, tool, arguments):
    frame = {"method": "item/tool/call", "id": request_id, "params": {
        "threadId": thread_id, "turnId": turn_id, "callId": call_id,
        "namespace": "skills_db", "tool": tool, "arguments": arguments,
    }}
    log({"direction": "peer_to_controller", "frame": frame})
    send(frame)
def read_replies(expected):
    replies = {}
    while expected - set(replies):
        frame = receive()
        if frame.get("id") not in expected or "result" not in frame:
            raise RuntimeError("unexpected callback response frame")
        replies[frame["id"]] = frame["result"]
        log({"direction": "peer_received_reply", "id": frame["id"], "result": frame["result"]})
    return replies
def text_result(result):
    assert result["success"] is True
    return result["contentItems"][0]["text"]

# Two concurrently outstanding callbacks must be observed and independently metered.
call("rpc-query-a", "call-query-a", "discover", {"query": "controllerneedle"})
call("rpc-query-b", "call-query-b", "discover", {"query": "controllerneedle"})
query_replies = read_replies({"rpc-query-a", "rpc-query-b"})
query_payload = json.loads(text_result(query_replies["rpc-query-a"]))
matches = query_payload["matches"]
descriptor = next(item for item in matches if item["skill_name"] == "bundle-target")
source_id = descriptor["source_id"]
asset = next(item for item in descriptor["bundle"]["members"] if item["relative_path"].endswith("assets/reference.md"))
if os.path.basename(__file__).startswith("peer-digest"):
    ready = os.path.join(os.path.dirname(__file__), "descriptor-ready")
    proceed = os.path.join(os.path.dirname(__file__), "allow-read")
    with open(ready, "w", encoding="utf-8") as stream:
        stream.write(source_id)
    while not os.path.exists(proceed):
        time.sleep(0.01)
    call("rpc-digest", "call-digest", "read_path", {"source_id": source_id})
    digest_result = read_replies({"rpc-digest"})["rpc-digest"]
    log({"digest_rejection": digest_result})
    send({"method": "turn/completed", "params": {"threadId": thread_id, "turn": turn_value("completed")}})
    sys.exit(0)
if os.path.basename(__file__).startswith("peer-gap"):
    call("rpc-gap", "call-gap", "read_chunks", {"source_id": source_id, "start_byte": 1, "end_byte": GAP_END})
    gap_result = json.loads(text_result(read_replies({"rpc-gap"})["rpc-gap"]))
    log({"received_gap": gap_result})
    send({"method": "turn/completed", "params": {"threadId": thread_id, "turn": turn_value("completed")}})
    sys.exit(0)

call("rpc-tree", "call-tree", "tree", {"view": "collections", "depth": 20})
tree_result = read_replies({"rpc-tree"})["rpc-tree"]
tree = json.loads(text_result(tree_result))
def flatten(nodes):
    for node in nodes:
        yield node
        yield from flatten(node.get("children", []))
node = next(item for item in flatten(tree["items"]) if item["id"] == "source.collection.skills-db.testing")
call("rpc-browse", "call-browse", "browse", {"node_id": node["id"], "limit": 20})
browse = json.loads(text_result(read_replies({"rpc-browse"})["rpc-browse"]))
assert any(item["source_id"] == source_id for item in browse["items"])

call("rpc-get", "call-get", "get", {"source_id": source_id})
get_payload = json.loads(text_result(read_replies({"rpc-get"})["rpc-get"]))
assert get_payload["items"][0]["content_delivery"] == {"mode": "descriptor_only", "content_loaded": False}

call("rpc-read-main", "call-read-main", "read_path", {"source_id": source_id})
main_body = json.loads(text_result(read_replies({"rpc-read-main"})["rpc-read-main"]))
asset_size = len("# Required local note\nUnicode: 雪 and quotes: \"kept\"\n".encode("utf-8"))
asset_parts = []
for index, (start, end) in enumerate(((0, 10), (10, 30), (30, asset_size))):
    request_id = "rpc-read-asset-" + str(index)
    call(request_id, "call-read-asset-" + str(index), "read_chunks", {"source_id": asset["source_id"], "start_byte": start, "end_byte": end})
    asset_parts.append(json.loads(text_result(read_replies({request_id})[request_id])) )
asset_body = dict(asset_parts[-1])
asset_body["start_byte"] = 0
asset_body["text"] = "".join(item["text"] for item in asset_parts)
log({"received_source": main_body})
log({"received_source": asset_body})

hostile = [
    ("rpc-alias", "get", {"source_key": source_id}),
    ("rpc-unknown-id", "read_path", {"source_id": "gold/fake"}),
    ("rpc-raw-path", "read_path", {"source_id": source_id, "path": "/etc/passwd"}),
    ("rpc-forged-query", "discover", {"query": "controllerneedle", "evaluated": True, "predicate_fingerprint": "f" * 64}),
    ("rpc-ranking-only", "pick", {"query": "controllerneedle"}),
    ("rpc-overlap-span", "read_chunks", {"source_id": asset["source_id"], "start_byte": 0, "end_byte": 1}),
]
for request_id, tool, arguments in hostile:
    call(request_id, "call-" + request_id, tool, arguments)
hostile_replies = read_replies({item[0] for item in hostile})
log({"hostile_results_are_failures": all(not item["success"] for item in hostile_replies.values())})

# Peer claims in a protocol terminal are deliberately false and must be ignored.
send({"method": "turn/completed", "params": {"threadId": thread_id, "turn": turn_value("completed"),
      "usage": {"totalTokens": 999999}, "evaluatedPredicates": 999,
      "loadedSourceIds": ["gold/fake"], "outcome": "perfect"}})
'''


DEADLINE_PEER = r'''import json, os, signal, subprocess, sys, time
def receive():
    return json.loads(sys.stdin.buffer.readline().decode("utf-8"))
def send(value):
    sys.stdout.write(json.dumps(value) + "\n"); sys.stdout.flush()
def reply(request, result):
    send({"id": request["id"], "result": result})
signal.signal(signal.SIGTERM, signal.SIG_IGN)
initialize = receive()
reply(initialize, {"userAgent":"fixture", "codexHome":os.getcwd(), "platformFamily":"unix", "platformOs":"test"})
receive()
thread_request = receive()
cwd = os.getcwd()
thread = {"id":"thread-fixture-1", "environments":None, "extra":None, "sessionId":"session-fixture-1",
"forkedFromId":None, "parentThreadId":None, "preview":"fixture", "ephemeral":True, "section":None,
"sectionEnteredAt":None, "projectId":None, "historyMode":"legacy", "modelProvider":"scripted_fixture",
"model":"scripted_fixture", "reasoningEffort":None, "createdAt":1, "updatedAt":1, "recencyAt":None,
"status":{"type":"idle"}, "path":None, "cwd":cwd, "cliVersion":"fixture", "originator":None,
"source":"unknown", "canAcceptDirectInput":True, "threadSource":"scripted_fixture", "agentNickname":None,
"agentRole":None, "gitInfo":None, "name":None, "daybreakEnabled":None, "turns":[]}
reply(thread_request, {"thread":thread, "model":"scripted_fixture", "modelProvider":"scripted_fixture", "serviceTier":None,
"disabledPluginIds":[], "cwd":cwd, "runtimeWorkspaceRoots":[], "instructionSources":[], "approvalPolicy":"never",
"approvalsReviewer":"user", "sandbox":{"type":"readOnly", "networkAccess":False}, "activePermissionProfile":None,
"reasoningEffort":None, "multiAgentMode":"explicitRequestOnly"})
turn_request = receive()
reply(turn_request, {"turn":{"id":"turn-fixture-1", "rootTurnId":None, "items":[], "itemsView":"full",
"status":"inProgress", "error":None, "startedAt":1, "completedAt":None, "durationMs":None}})
pid_path = os.path.join(os.path.dirname(__file__), "child.pid")
child = subprocess.Popen([sys.executable, "-I", "-c", "import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(30)"])
open(pid_path, "w").write(str(child.pid))
time.sleep(30)
'''


BROKEN_PIPE_PEER = r'''import json, os, sys
def receive(): return json.loads(sys.stdin.buffer.readline().decode("utf-8"))
def send(value): sys.stdout.write(json.dumps(value) + "\n"); sys.stdout.flush()
def reply(request, result): send({"id":request["id"], "result":result})
initialize=receive(); reply(initialize,{"userAgent":"fixture","codexHome":os.getcwd(),"platformFamily":"unix","platformOs":"test"})
receive(); thread_request=receive(); cwd=os.getcwd()
thread={"id":"thread-fixture-1","environments":None,"extra":None,"sessionId":"session-fixture-1","forkedFromId":None,
"parentThreadId":None,"preview":"fixture","ephemeral":True,"section":None,"sectionEnteredAt":None,"projectId":None,
"historyMode":"legacy","modelProvider":"scripted_fixture","model":"scripted_fixture","reasoningEffort":None,"createdAt":1,
"updatedAt":1,"recencyAt":None,"status":{"type":"idle"},"path":None,"cwd":cwd,"cliVersion":"fixture","originator":None,
"source":"unknown","canAcceptDirectInput":True,"threadSource":"scripted_fixture","agentNickname":None,"agentRole":None,"gitInfo":None,
"name":None,"daybreakEnabled":None,"turns":[]}
reply(thread_request,{"thread":thread,"model":"scripted_fixture","modelProvider":"scripted_fixture","serviceTier":None,"disabledPluginIds":[],
"cwd":cwd,"runtimeWorkspaceRoots":[],"instructionSources":[],"approvalPolicy":"never","approvalsReviewer":"user",
"sandbox":{"type":"readOnly","networkAccess":False},"activePermissionProfile":None,"reasoningEffort":None,"multiAgentMode":"explicitRequestOnly"})
turn=receive(); reply(turn,{"turn":{"id":"turn-fixture-1","rootTurnId":None,"items":[],"itemsView":"full","status":"inProgress","error":None,"startedAt":1,"completedAt":None,"durationMs":None}})
send({"method":"item/tool/call","id":"rpc-broken","params":{"threadId":"thread-fixture-1","turnId":"turn-fixture-1","callId":"call-broken","namespace":"skills_db","tool":"discover","arguments":{"query":"controllerneedle"}}})
os.close(0)
os._exit(0)
'''


NONREADING_PEER = r'''import json, os, sys, time
def receive(): return json.loads(sys.stdin.buffer.readline().decode("utf-8"))
def send(value): sys.stdout.write(json.dumps(value) + "\n"); sys.stdout.flush()
initialize=receive()
send({"id":initialize["id"],"result":{"userAgent":"fixture","codexHome":os.getcwd(),"platformFamily":"unix","platformOs":"test"}})
receive() # initialized
time.sleep(30) # deliberately never read thread/start or later frames
'''


class S06ControllerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = cli_fixtures.PublicLevSkillsCliTest("runTest")
        self.fixture.setUp()
        self.fixture.install_taxonomy()
        self.source = self.fixture.write_skill(
            "bundle-target",
            category="testing",
            description="controllerneedle package source",
            body="# Bundle 🌊\n\nQuoted: \"read this\"\\path\n",
        )
        self.asset = self.fixture.write_flat_markdown(
            "testing/bundle-target/assets/reference.md",
            ASSET_BYTES.decode("utf-8"),
        )
        self.rows = self.fixture.rebuild()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def write_peer(self, source: str, name: str = "peer.py") -> Path:
        path = self.fixture.output / name
        path.write_text(source, encoding="utf-8")
        return path

    def preserve_fixture(self, label: str) -> Path:
        root = RUN_ROOT / "tmpfixtures" / label
        root.mkdir(parents=True, exist_ok=True)
        for source in sorted((self.fixture.repo / "skills-db").rglob("*")):
            if source.is_file():
                destination = root / source.relative_to(self.fixture.repo / "skills-db")
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
        return root

    def read_peer_log(self, path: Path) -> list[dict]:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

    def test_connected_rpc_real_cli_and_received_complete_bundle_bytes(self) -> None:
        peer = self.write_peer(POSITIVE_PEER)
        controller = ScriptedSkillsController(self.fixture, lane="positive")
        instruction = "Use only the attached read-only skills-db tools.\n" + ("i" * 1_048_576)
        original_write = controller_module._write_pipe
        short_writes: list[tuple[int, int]] = []
        def short_write(fd: int, payload: memoryview) -> int:
            offered = len(payload)
            written = original_write(fd, payload[:min(4096, offered)])
            short_writes.append((offered, written))
            return written
        controller_module._write_pipe = short_write
        try:
            observation = controller.run_scripted_peer(
                peer,
                task_text="Find controllerneedle and read the complete local package.",
                instruction_text=instruction,
            )
        finally:
            controller_module._write_pipe = original_write
        log = self.read_peer_log(controller.peer_log)
        received_frames = [item["frame"] for item in log if item.get("direction") == "controller_to_peer"]
        methods = [frame.get("method") for frame in received_frames]
        self.assertIn("initialize", methods)
        self.assertIn("initialized", methods)
        self.assertIn("thread/start", methods)
        self.assertIn("turn/start", methods)
        self.assertTrue(any(item.get("dynamic_tools") for item in log))
        self.assertEqual(observation["run_kind"], "scripted_fixture")
        self.assertGreater(observation["budget"]["initial_text_bytes"], 1_048_576)
        self.assertTrue(any(offered > written for offered, written in short_writes))
        self.assertTrue(any(item["frame_bytes"] > 1_048_576 for item in observation["protocol_out"]))
        self.assertEqual(observation["terminal"]["peer_exit_code"], 0)
        self.assertTrue(observation["terminal"]["cleanup"]["reader_threads_stopped"])
        self.assertIsNone(observation["terminal"]["failure"])

        commands = [item["argv"][0] for item in observation["cli_runs"]]
        self.assertEqual(commands.count("discover"), 2)
        for run in observation["cli_runs"]:
            if run["argv"][0] == "discover":
                self.assertIn("--no-cache", run["argv"])
                self.assertEqual(run["exit_code"], 0)
                self.assertEqual(run["index_revision"], observation["query_observations"][0]["index_revision"])
        self.assertEqual(set(commands), {"discover", "tree", "browse", "get"})
        self.assertEqual(len(observation["query_observations"]), 1)
        self.assertTrue(all(item["evaluation_origin"] == "cli_evaluation" for item in observation["query_observations"]))
        self.assertTrue(observation["query_observations"][0]["evaluated"])
        self.assertIn(observation["query_observations"][0]["status"], {"ok", "empty"})
        self.assertEqual(len(observation["query_observations"][0]["predicate_fingerprint"]), 64)
        self.assertEqual(len(observation["query_observations"][0]["request_fingerprint"]), 64)
        query_callbacks = [item for item in observation["callback_observations"] if item["tool"] == "discover" and item["state"] == "delivered"]
        self.assertEqual({item["request_id"] for item in query_callbacks}, {"rpc-query-a", "rpc-query-b"})
        self.assertTrue(all(isinstance(item["call_id"], str) and item["duration_ms"] >= 0 for item in query_callbacks))
        peer_events = [item.get("direction") for item in log]
        first_reply = peer_events.index("peer_received_reply")
        self.assertLess(peer_events.index("peer_to_controller"), first_reply)
        self.assertEqual(sum(item == "peer_to_controller" for item in peer_events[:first_reply]), 2)
        self.assertEqual(observation["budget"]["attempted_calls"], observation["budget"]["admitted_calls"])
        self.assertEqual(len(observation["callback_rejections"]), 6)
        self.assertTrue(any(item.get("hostile_results_are_failures") for item in log))

        peer_replies = [item["result"] for item in log if item.get("direction") == "peer_received_reply"]
        read_bodies = [json.loads(result["contentItems"][0]["text"]) for result in peer_replies if result.get("success") is True and json.loads(result["contentItems"][0]["text"]).get("source_id")]
        main = next(item for item in read_bodies if item["source_id"] == controller.descriptors[next(key for key, value in controller.descriptors.items() if value["relative_path"] == "testing/bundle-target/SKILL.md")]["source_id"] and item["text"].startswith("---"))
        asset_source_id = next(key for key, value in controller.descriptors.items() if value["relative_path"] == "testing/bundle-target/assets/reference.md")
        asset_parts = sorted((item for item in read_bodies if item["source_id"] == asset_source_id), key=lambda item: item["start_byte"])
        asset_text = "".join(item["text"] for item in asset_parts)
        self.assertEqual(main["text"].encode("utf-8"), self.source.read_bytes())
        self.assertEqual(asset_text.encode("utf-8"), self.asset.read_bytes())
        self.assertEqual(main["digest"], cli_fixtures.file_digest(self.source))
        self.assertEqual(asset_parts[0]["digest"], cli_fixtures.file_digest(self.asset))
        self.assertTrue(all(item["complete_after_written_transfers"] for item in observation["bundle_delivery"]))
        self.assertTrue(any(item["eof"] for item in observation["source_transfers"]))
        self.assertEqual(observation["terminal"]["cleanup"]["process_groups_gone"], [True])
        self.assertTrue(observation["peer_claims_used_as_evidence"] is False)
        self.assertNotIn("999999", json.dumps(observation["query_observations"]))
        self.assertFalse(any("fake" in item["source_id"] for item in observation["source_transfers"]))
        self.assertEqual(observation["budget"]["cumulative_text_bytes"], observation["budget"]["initial_text_bytes"] + sum(item["text_bytes"] for item in observation["budget"]["reply_deliveries"]))
        self.assertGreater(sum(item["frame_bytes"] for item in observation["budget"]["reply_deliveries"]), sum(item["text_bytes"] for item in observation["budget"]["reply_deliveries"]))
        self.preserve_fixture("connected-positive")

    def test_clean_eof_without_matching_completed_turn_is_incomplete(self) -> None:
        prefix = POSITIVE_PEER.split('thread_id, turn_id = "thread-fixture-1", "turn-fixture-1"', 1)[0]
        peer = self.write_peer(prefix + "\nsys.exit(0)\n", "peer-early-exit.py")
        controller = ScriptedSkillsController(self.fixture, lane="early-eof")
        observation = controller.run_scripted_peer(peer, task_text="task", instruction_text="instructions")
        self.assertEqual(observation["terminal"]["peer_exit_code"], 0)
        self.assertTrue(observation["terminal"]["stdout_eof_observed"])
        self.assertEqual(observation["terminal"]["state"], "incomplete")
        self.assertIn("without one matching completed turn", observation["terminal"]["failure"])
        self.assertEqual(observation["terminal"]["protocol_terminal_notifications"], [])
        self.assertEqual(observation["budget"]["admitted_calls"], 0)

    def test_terminal_frames_require_matching_well_formed_completed_status(self) -> None:
        def make_controller() -> ScriptedSkillsController:
            controller = ScriptedSkillsController(self.fixture, lane="terminal-shape")
            controller._thread_id = "thread-fixture-1"
            controller._turn_id = "turn-fixture-1"
            return controller

        def frame(*, thread_id="thread-fixture-1", turn_id="turn-fixture-1", status="completed", omit=None):
            turn = {"id": turn_id, "rootTurnId": None, "items": [], "itemsView": "full", "status": status,
                    "error": None, "startedAt": 1, "completedAt": 2, "durationMs": 1}
            if omit:
                turn.pop(omit)
            return {"method": "turn/completed", "params": {"threadId": thread_id, "turn": turn}}

        accepted = make_controller()
        accepted._observe_incoming(frame())
        self.assertTrue(accepted._has_one_matching_completed_turn())
        cases = [
            frame(thread_id="other-thread"),
            frame(turn_id="other-turn"),
            frame(omit="completedAt"),
            frame(status="failed"),
            frame(status="interrupted"),
        ]
        for terminal in cases:
            with self.subTest(terminal=terminal):
                candidate = make_controller()
                candidate._observe_incoming(terminal)
                self.assertFalse(candidate._has_one_matching_completed_turn())
                self.assertIsNotNone(candidate._terminal_fact_error)
        duplicate = make_controller()
        duplicate._observe_incoming(frame())
        duplicate._observe_incoming(frame(status="failed"))
        self.assertFalse(duplicate._has_one_matching_completed_turn())
        self.assertIn("duplicate or contradictory", duplicate._terminal_fact_error)

    def test_server_request_envelopes_fail_before_dispatch(self) -> None:
        prefix = POSITIVE_PEER.split('# Two concurrently outstanding callbacks')[0]
        params = {"threadId": "thread-fixture-1", "turnId": "turn-fixture-1",
                  "callId": "envelope-call", "namespace": "skills_db",
                  "tool": "discover", "arguments": {"query": QUERY}}
        cases = [{"method": "item/tool/call", "id": value, "params": params}
                 for value in ({"bad": "id"}, [], None, True, 1.5, 2**63, -(2**63)-1)]
        self.assertEqual(len(KNOWN_SERVER_REQUEST_METHODS), 11)
        cases.extend({"method": method, "params": params} for method in KNOWN_SERVER_REQUEST_METHODS)
        cases.append({"method": "item/commandExecution/requestApproval", "id": 7,
                      "params": {"kind": "command", "threadId": "thread-fixture-1",
                                 "turnId": "turn-fixture-1", "itemId": "fixture-command",
                                 "startedAtMs": 1, "environmentId": "fixture-environment"}})
        cases.append({"method": [], "id": 7, "params": params})
        for frame in cases:
            with self.subTest(frame=frame):
                peer = self.write_peer(prefix + '\nsend(' + repr(frame) + ')\n'
                                       + 'send({"method":"turn/completed","params":{"threadId":thread_id,"turn":turn_value("completed")}})\n',
                                       'peer-invalid-envelope.py')
                candidate = ScriptedSkillsController(self.fixture, lane="invalid-envelope")
                dispatch_calls: list[dict[str, Any]] = []
                dispatch = candidate._dispatch_callback
                def track_dispatch(request_params: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None]:
                    dispatch_calls.append(request_params)
                    return dispatch(request_params)
                candidate._dispatch_callback = track_dispatch
                observation = candidate.run_scripted_peer(peer, task_text="t", instruction_text="i")
                self.assertNotEqual(observation["terminal"]["state"], "completed")
                self.assertEqual(dispatch_calls, [])
                self.assertEqual(candidate.cli_runs, [])
                self.assertEqual(candidate.transfers, [])
                self.assertEqual(observation["budget"]["attempted_calls"], 1)
                self.assertEqual(observation["budget"]["admitted_calls"], 1)
                self.assertTrue(observation["budget"]["aborted"])
                self.assertTrue(observation["terminal"]["cleanup"]["callbacks_stopped"])

    def test_valid_string_and_int64_request_ids_dispatch(self) -> None:
        prefix = POSITIVE_PEER.split('# Two concurrently outstanding callbacks')[0]
        for request_id in ("valid-id", 7, -(2**63), 2**63-1):
            with self.subTest(request_id=request_id):
                peer = self.write_peer(prefix + '\ncall(' + repr(request_id)
                                       + ', "valid-call", "discover", {"query":"controllerneedle"})\n'
                                       + 'text_result(read_replies({' + repr(request_id) + '})[' + repr(request_id) + '])\n'
                                       + 'send({"method":"turn/completed","params":{"threadId":thread_id,"turn":turn_value("completed")}})\n',
                                       'peer-valid-envelope.py')
                candidate = ScriptedSkillsController(self.fixture, lane="valid-envelope")
                observation = candidate.run_scripted_peer(peer, task_text="t", instruction_text="i")
                self.assertEqual(observation["terminal"]["state"], "completed")
                self.assertEqual(len(candidate.cli_runs), 1)
                self.assertEqual(candidate.callback_observations[0]["request_id"], request_id)

    def test_unread_peer_stdin_write_stops_at_active_deadline(self) -> None:
        peer = self.write_peer(NONREADING_PEER, "peer-nonreading.py")
        limits = replace(DEFAULT_LIMITS, wall_seconds=0.25)
        controller = ScriptedSkillsController(self.fixture, meter=CampaignMeter(limits), lane="write-block")
        instruction = "x" * 1_048_576
        started = time.monotonic()
        observation = controller.run_scripted_peer(peer, task_text="t", instruction_text=instruction)
        elapsed = time.monotonic() - started
        self.assertIn("deadline", observation["terminal"]["failure"])
        self.assertLess(elapsed, limits.wall_seconds + limits.term_grace_seconds + limits.teardown_seconds + 1)
        self.assertTrue(observation["terminal"]["cleanup"]["process_groups_gone"] == [True])
        self.assertTrue(controller.write_failures)
        failure = controller.write_failures[0]
        self.assertLess(failure["bytes_written"], failure["frame_bytes"])
        self.assertEqual(observation["write_failures"], controller.write_failures)
        self.assertTrue(observation["budget"]["aborted"])

    def test_initial_input_over_cap_fails_before_peer_spawn(self) -> None:
        peer = self.write_peer("raise SystemExit(0)\n")
        controller = ScriptedSkillsController(self.fixture)
        with self.assertRaises(AdmissionError):
            controller.run_scripted_peer(
                peer,
                task_text="x" * (DEFAULT_LIMITS.context_bytes + 1),
                instruction_text="",
            )
        self.assertIsNone(controller.proc)
        self.assertEqual(controller.meter.admitted_calls, 0)
        self.assertEqual(controller.meter.denials[0]["kind"], "initial_text")

    def test_evidence_identity_is_unique_even_for_repeated_lane_names(self) -> None:
        first = ScriptedSkillsController(self.fixture, lane="same-lane")
        first_path = first.write_evidence()
        first_bytes = first_path.read_bytes()
        second = ScriptedSkillsController(self.fixture, lane="same-lane")
        second_path = second.write_evidence()
        self.assertNotEqual(first_path, second_path)
        self.assertEqual(first_path.read_bytes(), first_bytes)
        self.assertEqual(json.loads(first_bytes)["lane"], "same-lane")
        self.assertEqual(json.loads(second_path.read_text(encoding="utf-8"))["lane"], "same-lane")

    def test_shared_last_call_race_and_reply_byte_boundaries(self) -> None:
        meter = CampaignMeter()
        meter.begin("", "")
        barrier = threading.Barrier(161)
        results: list[bool] = []
        result_lock = threading.Lock()

        def attempt() -> None:
            barrier.wait()
            try:
                meter.admit_attempt(action="discover")
                accepted = True
            except AdmissionError:
                accepted = False
            with result_lock:
                results.append(accepted)

        workers = [threading.Thread(target=attempt) for _ in range(161)]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(timeout=5)
        self.assertTrue(all(not worker.is_alive() for worker in workers))
        self.assertEqual(sum(results), 160)
        self.assertEqual(meter.admitted_calls, 160)
        self.assertEqual(meter.attempted_calls, 161)

        same_reply = CampaignMeter()
        same_reply.begin("", "")
        with self.assertRaises(AdmissionError):
            same_reply.reserve_reply(
                [{"type": "inputText", "text": "a" * (200 * 1024)}, {"type": "inputText", "text": "b" * (200 * 1024)}],
                recipient="one-reply",
                frame_bytes=400 * 1024 + 80,
            )
        self.assertEqual(same_reply.context_bytes, 0)
        self.assertEqual(same_reply.denials[-1]["reason"], "per_response_cap")

        separate_replies = CampaignMeter()
        separate_replies.begin("", "")
        body = "x" * (200 * 1024)
        body_bytes = len(body.encode("utf-8"))
        separate_replies.reserve_reply([{"type": "inputText", "text": body}], recipient="control", frame_bytes=body_bytes + 100)
        separate_replies.reserve_reply([{"type": "inputText", "text": body}], recipient="candidate", frame_bytes=body_bytes + 100)
        self.assertEqual(separate_replies.context_bytes, 2 * body_bytes)
        self.assertEqual(separate_replies.context_bytes, 400 * 1024)
        self.assertEqual([item["recipient"] for item in separate_replies.reply_bytes], ["control", "candidate"])

        equality = CampaignMeter()
        equality.begin("", "")
        exact = "x" * DEFAULT_LIMITS.per_response_bytes
        for index in range(DEFAULT_LIMITS.context_bytes // DEFAULT_LIMITS.per_response_bytes):
            equality.reserve_reply([{"type": "inputText", "text": exact}], recipient=f"copy-{index}", frame_bytes=len(exact) + 64)
        self.assertEqual(equality.context_bytes, DEFAULT_LIMITS.context_bytes)
        with self.assertRaises(AdmissionError):
            equality.reserve_reply([{"type": "inputText", "text": "diagnostic"}], recipient="no-free-diagnostic", frame_bytes=100)
        self.assertEqual(equality.context_bytes, DEFAULT_LIMITS.context_bytes)

    def test_concurrent_identical_source_spans_reserve_before_delivery(self) -> None:
        controller = ScriptedSkillsController(self.fixture, lane="span-race")
        controller.meter.begin("task", "instructions")
        controller._thread_id = "thread-fixture-1"
        controller._turn_id = "turn-fixture-1"
        payload = controller._run_cli_tool("discover", {"query": QUERY})
        source_id = next(item["source_id"] for item in payload["matches"] if item.get("skill_name") == "bundle-target")
        delivery_barrier = threading.Barrier(2)
        starts = threading.Barrier(2)
        delivered: list[dict[str, Any]] = []
        def wait_for_both_frames(frame: dict[str, Any]) -> None:
            delivery_barrier.wait(timeout=3)
            delivered.append(frame)
        controller._send_frame = wait_for_both_frames

        def request(index: int) -> None:
            starts.wait(timeout=3)
            controller._serve_tool_request({
                "method": "item/tool/call", "id": f"rpc-span-{index}", "params": {
                    "threadId": "thread-fixture-1", "turnId": "turn-fixture-1", "callId": f"call-span-{index}",
                    "namespace": "skills_db", "tool": "read_chunks",
                    "arguments": {"source_id": source_id, "start_byte": 0, "end_byte": 10},
                },
            })

        workers = [threading.Thread(target=request, args=(index,)) for index in range(2)]
        for worker in workers: worker.start()
        for worker in workers: worker.join(timeout=5)
        self.assertTrue(all(not worker.is_alive() for worker in workers))
        self.assertEqual([frame["result"]["success"] for frame in delivered].count(True), 1)
        self.assertEqual([frame["result"]["success"] for frame in delivered].count(False), 1)
        self.assertEqual(len(controller.transfers), 1)
        self.assertEqual(controller.meter.observation()["pending_span_reservations"], 0)
        self.assertEqual(controller.meter.observation()["committed_source_spans"], 1)
        self.assertEqual(len(controller.callback_rejections), 1)
        controller.write_evidence()

    def test_source_digest_change_and_descriptor_escape_are_rejected(self) -> None:
        peer = self.write_peer(POSITIVE_PEER, "peer-digest.py")
        controller = ScriptedSkillsController(self.fixture, lane="digest")
        result: dict[str, Any] = {}
        def run_controller() -> None:
            try:
                result["observation"] = controller.run_scripted_peer(peer, task_text="read it", instruction_text="read only")
            except BaseException as error:
                result["error"] = error
        runner = threading.Thread(target=run_controller)
        runner.start()
        ready = peer.parent / "descriptor-ready"
        proceed = peer.parent / "allow-read"
        try:
            until = time.monotonic() + 5
            while not ready.exists() and time.monotonic() < until:
                time.sleep(0.01)
            self.assertTrue(ready.exists(), "scripted peer did not expose the real descriptor before timeout")
            source_id = ready.read_text(encoding="utf-8")
            self.assertTrue(source_id in controller.descriptors)
            self.source.write_bytes(self.source.read_bytes() + b"post-descriptor mutation\n")
        finally:
            proceed.write_text("continue", encoding="utf-8")
            runner.join(timeout=10)
        self.assertFalse(runner.is_alive())
        self.assertNotIn("error", result)
        observation = result["observation"]
        self.assertIsNone(observation["terminal"]["failure"])
        self.assertEqual(observation["terminal"]["peer_exit_code"], 0)
        self.assertEqual(len(observation["callback_rejections"]), 1)
        self.assertEqual(observation["callback_rejections"][0]["tool"], "read_path")
        self.assertIn("current CLI index", observation["callback_rejections"][0]["message"])
        self.assertEqual(observation["source_transfers"], [])
        self.assertEqual(controller.full_sources, set())
        log = self.read_peer_log(controller.peer_log)
        rejection = next(item["digest_rejection"] for item in log if "digest_rejection" in item)
        self.assertFalse(rejection["success"])

        outside = self.fixture.output / "outside.txt"
        outside.write_text("fixture-only outside path", encoding="utf-8")
        forged = dict(controller.descriptors[source_id])
        forged["path"] = str(outside)
        forged["local_path"] = str(outside)
        with self.assertRaisesRegex(SourceError, "escaped"):
            controller._validate_descriptor(forged)

    def test_gapped_source_span_is_received_but_never_gets_full_bundle_credit(self) -> None:
        end = len(self.source.read_bytes()) - 1
        peer = self.write_peer(POSITIVE_PEER.replace("GAP_END", str(end)), "peer-gap.py")
        controller = ScriptedSkillsController(self.fixture, lane="gap")
        observation = controller.run_scripted_peer(peer, task_text="read a partial span", instruction_text="fixture only")
        transfer = observation["source_transfers"][0]
        self.assertEqual(transfer["start_byte"], 1)
        self.assertEqual(transfer["end_byte"], end)
        self.assertFalse(transfer["eof"])
        self.assertNotIn(transfer["source_id"], controller.full_sources)
        self.assertTrue(all(not item["complete_after_written_transfers"] for item in observation["bundle_delivery"]))
        log = self.read_peer_log(controller.peer_log)
        received = next(item["received_gap"] for item in log if "received_gap" in item)
        self.assertEqual(received["text"].encode("utf-8"), self.source.read_bytes()[1:end])

    def test_cached_real_cli_result_does_not_earn_predicate_credit(self) -> None:
        first = self.fixture.run_json(["discover", QUERY, "--json"])
        cached = self.fixture.run_json(["discover", QUERY, "--json"])
        self.assertTrue(first["query_groups"][0]["evaluated"])
        self.assertEqual(cached["evaluation_origin"], "cache")
        self.assertFalse(cached["query_groups"][0]["evaluated"])
        self.assertEqual(cached["query_groups"][0]["evaluation_origin"], "cache")

        controller = ScriptedSkillsController(self.fixture)
        cached_observation = {
            "record": {
                "exit_code": 0,
                "timed_out": False,
                "argv": ["discover", "--query", QUERY, "--namespace", "skills-db", "--json", "--no-cache"],
                "index_revision": cached["index_revision"],
                "started_monotonic": 1.0,
                "finished_monotonic": 2.0,
            }
        }
        controller._record_query_outcomes(cached_observation, cached)
        self.assertEqual(controller.query_observations, {})

        too_many_terms = " ".join(["needle"] * 33)
        failure = self.fixture.run_cli(["discover", "--query", too_many_terms, "--namespace", "skills-db", "--json", "--no-cache"])
        self.assertEqual(failure.returncode, 1)
        failed_payload = json.loads(failure.stdout)
        failed_observation = {
            "record": {
                "exit_code": failure.returncode,
                "timed_out": False,
                "argv": ["discover", "--query", too_many_terms, "--namespace", "skills-db", "--json", "--no-cache"],
                "index_revision": failed_payload.get("index_revision"),
                "started_monotonic": 1.0,
                "finished_monotonic": 2.0,
            }
        }
        controller._record_query_outcomes(failed_observation, failed_payload)
        self.assertEqual(controller.query_observations, {})

    def test_failed_real_cli_result_does_not_earn_predicate_credit(self) -> None:
        controller = ScriptedSkillsController(self.fixture)
        too_many_terms = " ".join(["needle"] * 33)
        failure = self.fixture.run_cli(["discover", "--query", too_many_terms, "--namespace", "skills-db", "--json", "--no-cache"])
        self.assertEqual(failure.returncode, 1)
        failed_payload = json.loads(failure.stdout)
        failed_observation = {
            "record": {
                "exit_code": failure.returncode,
                "timed_out": False,
                "argv": ["discover", "--query", too_many_terms, "--namespace", "skills-db", "--json", "--no-cache"],
                "index_revision": failed_payload.get("index_revision"),
                "started_monotonic": 1.0,
                "finished_monotonic": 2.0,
            }
        }
        controller._record_query_outcomes(failed_observation, failed_payload)
        self.assertEqual(controller.query_observations, {})

    def test_deadline_terminates_owned_peer_group_after_term_grace(self) -> None:
        peer = self.write_peer(DEADLINE_PEER, "peer-deadline.py")
        limits = replace(DEFAULT_LIMITS, wall_seconds=0.2)
        meter = CampaignMeter(limits)
        controller = ScriptedSkillsController(self.fixture, meter=meter, lane="deadline")
        started = time.monotonic()
        observation = controller.run_scripted_peer(peer, task_text="wait", instruction_text="fixture only")
        elapsed = time.monotonic() - started
        child_pid_path = self.fixture.output / "child.pid"
        self.assertTrue(child_pid_path.exists())
        child_pid = int(child_pid_path.read_text(encoding="utf-8"))
        self.assertIn("active deadline", observation["terminal"]["failure"])
        self.assertEqual(observation["terminal"]["peer_exit_code"], -signal.SIGKILL)
        self.assertEqual(observation["terminal"]["cleanup"]["process_groups_gone"], [True])
        self.assertGreaterEqual(observation["terminal"]["cleanup"]["elapsed_ms"], 1900)
        self.assertLessEqual(observation["terminal"]["cleanup"]["elapsed_ms"], 5000)
        self.assertLess(elapsed, limits.wall_seconds + limits.term_grace_seconds + limits.teardown_seconds + 1.0)
        self.assertFalse(self._pid_running(child_pid), f"owned process-group child {child_pid} survived cleanup")

    def test_late_callback_and_native_mode_are_rejected_before_cli_dispatch(self) -> None:
        now = [10.0]
        clock = lambda: now[0]
        meter = CampaignMeter(replace(DEFAULT_LIMITS, wall_seconds=1), clock)
        meter.begin("task", "instructions", started_at=10.0)
        controller = ScriptedSkillsController(self.fixture, meter=meter, clock=clock)
        controller._thread_id = "thread-fixture-1"
        controller._turn_id = "turn-fixture-1"
        now[0] = 11.0
        controller._serve_tool_request({
            "method": "item/tool/call", "id": "late", "params": {
                "threadId": "thread-fixture-1", "turnId": "turn-fixture-1", "callId": "late-call",
                "namespace": "skills_db", "tool": "discover", "arguments": {"query": QUERY},
            },
        })
        self.assertEqual(controller.cli_runs, [])
        self.assertEqual(meter.admitted_calls, 0)
        with self.assertRaises(ProtocolError):
            ScriptedSkillsController(self.fixture).run_scripted_peer(
                self.write_peer("raise SystemExit(0)\n", "peer-native.py"),
                task_text="task",
                instruction_text="instructions",
                run_kind="native_codex",
            )

    def test_broken_pipe_preserves_terminal_failure_and_charges_attempt(self) -> None:
        peer = self.write_peer(BROKEN_PIPE_PEER, "peer-broken.py")
        controller = ScriptedSkillsController(self.fixture, lane="broken-pipe")
        observation = controller.run_scripted_peer(peer, task_text="query", instruction_text="fixture")
        self.assertEqual(observation["budget"]["admitted_calls"], 1)
        self.assertTrue(observation["terminal"]["failure"] is not None)
        self.assertIsNotNone(observation["terminal"]["peer_exit_code"])
        self.assertTrue(observation["terminal"]["stdout_eof_observed"])
        self.assertTrue(observation["terminal"]["cleanup"]["reader_threads_stopped"])

    @staticmethod
    def _pid_running(pid: int) -> bool:
        try:
            result = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True, timeout=2, check=False)
        except (OSError, subprocess.TimeoutExpired):
            return True
        state = result.stdout.strip()
        return bool(state) and not state.startswith("Z")


if __name__ == "__main__":
    unittest.main()
