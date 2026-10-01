import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("relay", Path(__file__).parents[1] / "scripts/relay.py")
relay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(relay)
NOW = 1790816400.0


class RelayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "session.jsonl"
        self.store = relay.Store(self.root / "state", "fixture-host", "relay-A")

    def tearDown(self):
        self.temp.cleanup()

    def write(self, entries, agent="omo", sid="abcd1111", title=None):
        header = {"type": "session", "version": 3, "id": sid, "cwd": "/fixture", "timestamp": relay.stamp(NOW - 86400 * 3)}
        rows = [header] if agent != "claude" else []
        if title is not None:
            rows.insert(0, {"type": "title", "v": 1, "title": title})
        for i, e in enumerate(entries):
            obj = {"type": "message", "id": f"m{i}", "parentId": f"m{i-1}" if i else None,
                   "timestamp": relay.stamp(NOW), "message": {"role": "user", "content": "hello"}}
            obj.update(e)
            if agent == "claude":
                obj.update(type=obj["message"]["role"], uuid=obj.pop("id"), sessionId=sid)
            rows.append(obj)
        self.source.write_text("".join(json.dumps(o) + "\n" for o in rows))
        return relay.load_session(agent, self.source, "fixture-host")

    def bound(self, entries=None):
        session = self.write(entries or [{}, {"message": {"role": "assistant", "content": "done"}}])
        with self.store.lock():
            self.store.bind(session)
        return session

    def confirm(self, batch):
        self.store.receipt(batch["batch_id"], "relay-A/verified-turn")
        return self.store.receipt(batch["batch_id"], None, ack=True)

    def test_discovery_uses_activity_not_creation_or_mtime(self):
        self.write([{}])
        os.utime(self.source, (NOW - 86400 * 4, NOW - 86400 * 4))
        with patch.object(relay, "roots", return_value=[("default", self.root)]):
            result = relay.inventory(["omo"], "fixture-host", NOW - 86400)
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["sessions"][0]["last_activity"], relay.stamp(NOW))
        self.assertNotIn("hello", json.dumps(result))

    def test_old_activity_not_in_recent_inventory_even_fresh_mtime(self):
        self.write([{"timestamp": relay.stamp(NOW - 86401)}])
        with patch.object(relay, "roots", return_value=[("default", self.root)]):
            self.assertEqual(relay.inventory(["omo"], "fixture-host", NOW - 86400)["count"], 0)

    def test_find_title_and_full_id(self):
        self.write([{}], title="Exact title")
        with patch.object(relay, "roots", return_value=[("default", self.root)]):
            self.assertEqual(relay.inventory(["omp"], "fixture-host", None, "abcd1111")["count"], 1)
            self.assertEqual(relay.inventory(["omp"], "fixture-host", None, "exact title")["count"], 1)

    def test_bind_and_discover_reuse(self):
        session = self.bound()
        self.assertTrue(self.store.bind(session)["reused"])
        other = relay.Store(self.root / "state", "fixture-host", "relay-B")
        result = other.bind(session)
        self.assertTrue(result["reused"])
        self.assertEqual(result["relay_id"], "relay-A")
        self.assertFalse(other.file.exists())

    def test_short_id_collision_has_distinct_names(self):
        first = self.write([{}], sid="abcd1111", title="same")
        with self.store.lock():
            a = self.store.bind(first)
        second = self.write([{}], sid="abcd2222", title="same")
        b = self.store.bind(second, replace=True)
        self.assertNotEqual(a["optional_child_title"], b["optional_child_title"])

    def test_rebind_requires_explicit_selection(self):
        self.bound()
        other = self.write([{}], sid="different")
        with self.assertRaises(relay.RelayError):
            self.store.bind(other)

    def test_cursor_delta_and_exact_once_ack(self):
        self.bound()
        batch = self.store.read("trace")
        self.assertEqual([m["text"] for m in batch["messages"]], ["hello", "done"])
        replay = self.store.read("trace")
        self.assertEqual(batch["batch_id"], replay["batch_id"])
        self.assertIsNone(self.store.get()["ack_cursor"])
        self.confirm(batch)
        self.assertTrue(self.store.receipt(batch["batch_id"], None, ack=True)["idempotent"])
        self.assertEqual(self.store.read("trace")["messages"], [])

    def test_cannot_ack_before_delivery(self):
        self.bound()
        b = self.store.read("trace")
        with self.assertRaises(relay.RelayError):
            self.store.receipt(b["batch_id"], None, ack=True)

    def test_delivery_and_ack_cursors_are_distinct(self):
        self.bound()
        b = self.store.read("trace")
        self.store.receipt(b["batch_id"], "verified-reference")
        state = self.store.get()
        self.assertEqual(state["read_cursor"], state["delivery_cursor"])
        self.assertIsNone(state["ack_cursor"])

    def test_trace_preserves_unicode_spaces_and_blocks(self):
        text = "  α\n\n你好\t "
        s = self.write([{"message": {"role": "assistant", "content": [
            {"type": "text", "text": text[:4]}, {"type": "text", "text": text[4:]}]}}])
        self.assertEqual(relay.delta(s, None)["messages"][0]["text"], text)

    def test_character_pagination_does_not_lose_or_add_text(self):
        original = " αβ\n🎉  hello " * 10
        s = self.write([{"message": {"role": "assistant", "content": original}}, {}])
        cursor, strings = None, []
        for _ in range(100):
            b = relay.delta(s, cursor, max_chars=7)
            strings.extend(m["text"] for m in b["messages"])
            if b["next_cursor"] == cursor:
                break
            cursor = b["next_cursor"]
        self.assertEqual("".join(strings), original + "hello")

    def test_summary_is_labeled_excerpt_trace_full(self):
        s = self.write([{"message": {"role": "assistant", "content": "x" * 1000}}])
        b = relay.delta(s, None)
        self.assertIn("excerpt clipped", relay.render(b, "summary"))
        self.assertIn("x" * 1000, relay.render(b, "trace"))

    def test_default_15_override_5_bounded_2_hours(self):
        self.bound()
        self.assertEqual(self.store.monitor(15, None, "summary", NOW)["every_minutes"], 15)
        plan = self.store.monitor(5, 120, "trace", NOW)
        self.assertEqual(plan["expires_at"], relay.stamp(NOW + 7200))
        self.assertFalse(plan["schedule_created"])

    def test_schedule_destination_must_be_same_relay(self):
        self.bound()
        self.store.monitor(15, None, "summary", NOW)
        with self.assertRaises(relay.RelayError):
            self.store.schedule_record("schedule", "parent", "ACTIVE")
        self.assertEqual(self.store.schedule_record("schedule", "relay-A", "ACTIVE")["destination_thread"], "relay-A")

    def test_expiry_inclusive_pauses_scheduled_read(self):
        self.bound()
        self.store.monitor(5, 120, "trace", NOW)
        self.store.schedule_record("schedule", "relay-A", "ACTIVE")
        self.assertEqual(self.store.read("trace", scheduled=True, now=NOW+7200)["pause_reason"], "duration_expired")

    def test_idle_15_pause_and_wake_catchup_without_resume(self):
        self.bound()
        self.store.monitor(5, 120, "trace", NOW)
        self.store.schedule_record("schedule", "relay-A", "ACTIVE")
        paused = self.store.read("trace", scheduled=True, now=NOW+900)
        self.assertTrue(paused["quiet"])
        self.assertEqual(paused["pause_reason"], "source_idle_15_minutes")
        woke = self.store.read("trace", scheduled=False, now=NOW+901)
        self.assertEqual(len(woke["messages"]), 2)
        self.assertEqual(woke["monitor_status"], "PAUSED")

    def test_partial_tail_deferred_until_complete(self):
        s = self.write([{}])
        anchor = s["cursor"]
        with self.source.open("a") as f:
            f.write('{"type":"message","id":"next"')
        b = relay.delta(relay.load_session("omo", self.source, "fixture-host"), anchor)
        self.assertEqual(b["messages"], [])
        self.assertTrue(b["partial_tail_waiting"])
        with self.source.open("a") as f:
            f.write(',"message":{"role":"assistant","content":"new"}}\n')
        self.assertEqual(relay.delta(relay.load_session("omo", self.source, "fixture-host"), anchor)["messages"][0]["text"], "new")

    def test_malformed_complete_record_fails_without_payload(self):
        self.write([{}])
        with self.source.open("a") as f:
            f.write('secret-private-payload\n')
        with self.assertRaises(relay.RelayError) as caught:
            relay.load_session("omo", self.source, "fixture-host")
        self.assertNotIn("secret-private-payload", str(caught.exception))

    def test_rotation_reanchors_unchanged_id(self):
        s = self.write([{}])
        anchor = s["cursor"]
        old = self.source.read_text()
        self.source.unlink()
        self.source.write_text(old + json.dumps({"type":"message","id":"new","message":{"role":"assistant","content":"rotated"}}) + "\n")
        self.assertEqual(relay.delta(relay.load_session("omo", self.source, "fixture-host"), anchor)["messages"][0]["text"], "rotated")

    def test_title_slot_rewrite_keeps_cursor(self):
        s = self.write([{}], agent="omp", title="before")
        anchor = s["cursor"]
        self.source.write_text(self.source.read_text().replace('"before"', '"after"'))
        self.assertEqual(relay.delta(relay.load_session("omp", self.source, "fixture-host"), anchor)["messages"], [])

    def test_truncation_or_changed_anchor_explicit_gap(self):
        s = self.write([{}, {}])
        anchor = s["cursor"]
        self.write([{}])
        with self.assertRaisesRegex(relay.RelayError, "cursor gap"):
            relay.delta(relay.load_session("omo", self.source, "fixture-host"), anchor)

    def test_branch_change_is_disclosed(self):
        s = self.write([{}, {}, {"parentId":"m0"}])
        self.assertEqual(relay.delta(s, None)["branches"][0]["entry_id"], "m2")

    def test_private_tool_secret_filtering(self):
        secret = "sk-ant-" + "f" * 30
        s = self.write([{"message":{"role":"assistant","content":[
            {"type":"thinking","thinking":"NEVER-REASONING"},
            {"type":"toolCall","arguments":{"text":"NEVER-TOOL"}},
            {"type":"text","text":"visible <analysis>NEVER-PRIVATE</analysis> api_key='fixture value' " + secret}]}},
            {"message":{"role":"toolResult","content":"NEVER-RESULT"}}])
        b = relay.delta(s, None)
        out = relay.render(b, "trace")
        for forbidden in ("NEVER-REASONING", "NEVER-TOOL", "NEVER-PRIVATE", "NEVER-RESULT", "fixture value", secret):
            self.assertNotIn(forbidden, out)
        self.assertIn("Sanitized output", out)

    def test_plain_user_tool_wrappers_and_notifications_excluded(self):
        s = self.write([
            {"message":{"role":"user","content":"Tool result (fixture, id=tool): NEVER-PAYLOAD"}},
            {"message":{"role":"user","content":"<task-notification>NEVER-BACKGROUND</task-notification>"}},
            {"message":{"role":"assistant","content":"<system-reminder>NEVER-SYSTEM</system-reminder>allowed"}}])
        out = relay.render(relay.delta(s,None),"trace")
        for text in ['NEVER-PAYLOAD','NEVER-BACKGROUND','NEVER-SYSTEM']:
            self.assertNotIn(text,out)
        self.assertIn('allowed',out)
        self.assertIn('tool_payload_wrappers',out)

    def test_claude_main_roles_and_exact_uuid(self):
        s = self.write([{}, {"message":{"role":"assistant","content":[{"type":"text","text":"exact"}]}}], agent="claude", sid="full-id")
        self.assertEqual(s["identity"]["session_id"], "full-id")
        self.assertEqual(relay.delta(s, None)["messages"][1]["id"], "m1")

    def test_claude_metadata_title_never_uses_prose(self):
        self.write([{}], agent="claude")
        with self.source.open("a") as stream:
            stream.write(json.dumps({"type":"ai-title","sessionId":"abcd1111","aiTitle":"Recorded title"}) + "\n")
        session = relay.load_session("claude", self.source, "fixture-host")
        self.assertEqual(session["title"], "Recorded title")
        self.assertEqual(session["title_source"], "ai-title")

    def test_timestamp_negative_offset_is_respected(self):
        self.assertEqual(relay.timestamp("2026-10-01T00:00:00-04:00"), relay.timestamp("2026-10-01T04:00:00Z"))

    def test_mode_switch_can_show_full_pending_trace(self):
        self.bound([{"message":{"role":"assistant","content":"x"*1000}}])
        self.assertIn("excerpt clipped", self.store.read("summary")["markdown"])
        self.assertIn("x"*1000, self.store.read("trace")["markdown"])

    def test_cross_machine_cursor_rejected(self):
        s = self.write([{}])
        wrong = relay.load_session("omo", self.source, "different-host")
        with self.assertRaises(relay.RelayError):
            relay.delta(wrong, s["cursor"])

    def test_denied_codex_path_and_symlink_cannot_be_read(self):
        denied = self.root / ".codex"
        denied.mkdir()
        file = denied / "session.jsonl"
        file.write_text("{}\n")
        link = self.root / "link.jsonl"
        link.symlink_to(file)
        for path in (file, link):
            with self.assertRaises(relay.RelayError):
                relay.safe_path(path)

    def test_local_state_modes_and_no_synced_state(self):
        self.bound()
        self.assertEqual(self.store.file.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.store.root.stat().st_mode & 0o777, 0o700)
        with self.assertRaises(relay.RelayError):
            relay.Store(self.root / ".agents/skills/lev-relay", "fixture-host", "relay-A")

    def test_overlapping_operation_refused(self):
        with self.store.lock():
            with self.assertRaises(relay.RelayError):
                with self.store.lock():
                    pass

    def test_prepare_steering_never_sends(self):
        self.bound()
        before = self.source.read_bytes()
        proposal = self.store.prepare("exact approved later\n")
        self.assertEqual(proposal["status"], "awaiting_human_approval")
        self.assertEqual(self.source.read_bytes(), before)
        self.assertEqual(self.store.get()["steering"]["message"], "exact approved later\n")


if __name__ == "__main__":
    unittest.main()
