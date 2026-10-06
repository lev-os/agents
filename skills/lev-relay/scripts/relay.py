#!/usr/bin/env python3
"""Allowed prose from Claude, OmO/Senpi and OMP JSONL. No Codex adapter."""
from __future__ import annotations

import argparse
import base64
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import stat
import sys
import tempfile
import time
from typing import Any

AGENTS = ("claude", "omo", "omp")
MAX_SOURCE = 64 * 1024 * 1024
MAX_FILES = 20000
UTC = dt.timezone.utc


class RelayError(Exception):
    pass


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def stamp(value: float | None = None) -> str:
    return dt.datetime.fromtimestamp(time.time() if value is None else value, UTC).isoformat()


def timestamp(value: Any) -> float | None:
    try:
        if isinstance(value, (int, float)):
            return value / 1000 if value > 1e11 else float(value)
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return (parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)).timestamp()
    except (ValueError, TypeError, OverflowError):
        return None


PRIVATE = re.compile(r"<(thinking|analysis|reasoning|tool[_-]call|tool[_-]result|task-notification|system-reminder)(?:\s[^>]*)?>.*?(?:</\1>|$)", re.I | re.S)
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----.*?(?:-----END (?:[A-Z ]+)?PRIVATE KEY-----|$)", re.S),
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16})\b"),
    re.compile(r"(?i)(\b(?:[A-Z0-9_]*api[_-]?key|access[_-]?token|auth[_-]?token|password|client[_-]?secret)\b[\"']?\s*[=:]\s*)(?:\"[^\"\n]*\"|'[^'\n]*'|[^\s,;]+)"),
    re.compile(r"(?i)(\bBearer\s+)[A-Za-z0-9._~+/-]{12,}=*"),
    re.compile(r"(?i)(https?://)[^\s/@:]+:[^\s/@]+@"),
]


def sanitize(text: str) -> tuple[str, dict[str, int]]:
    omissions = {"private_spans": 0, "secrets": 0}
    text, omissions["private_spans"] = PRIVATE.subn("[omitted private/tool span]", text)
    for pattern in SECRET_PATTERNS:
        def redact(match: re.Match) -> str:
            return (match.group(1) if match.lastindex else "") + "[REDACTED]"
        text, n = pattern.subn(redact, text)
        omissions["secrets"] += n
    return text, omissions


def safe_path(path: str | Path) -> Path:
    result = Path(path).expanduser().resolve()
    if any(part in {".codex", ".ssh", ".aws", "credentials", "auth.json"} for part in result.parts):
        raise RelayError("source denied: protected location (Codex is out of scope)")
    if result.suffix != ".jsonl":
        raise RelayError("source must be an allowed session JSONL; databases are unsupported")
    if not result.is_file():
        raise RelayError("session source is not a regular file")
    if result.stat().st_size > MAX_SOURCE:
        raise RelayError("source exceeds 64 MiB; use a documented bounded export")
    return result


def prose(message: dict) -> tuple[str, dict]:
    content = message.get("content", "")
    omitted = {"non_text_blocks": 0, "private_spans": 0, "secrets": 0}
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        blocks = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text" and isinstance(block.get("text"), str):
                blocks.append(block["text"])
            else:
                omitted["non_text_blocks"] += 1
        text = "".join(blocks)  # No invented whitespace between text blocks.
    else:
        text = ""
        omitted["non_text_blocks"] += 1
    if re.match(r"\s*(?:Tool result\s*\(|Tool output\s*:)", text, re.I):
        omitted["tool_payload_wrappers"] = 1
        return "", omitted
    text, counts = sanitize(text)
    omitted.update(counts)
    return text, omitted


def encode_cursor(identity: dict, record: dict | None, offset: int = 0) -> str:
    data = {"v": 1, "scope": digest(identity), "anchor": record["id"] if record else None,
            "fingerprint": record["fp"] if record else None, "offset": offset}
    return base64.urlsafe_b64encode(json.dumps(data, separators=(",", ":")).encode()).decode().rstrip("=")


def decode_cursor(token: str, identity: dict) -> dict:
    try:
        data = json.loads(base64.urlsafe_b64decode(token + "=" * (-len(token) % 4)))
        if data["v"] != 1 or data["scope"] != digest(identity) or not isinstance(data["offset"], int) or data["offset"] < 0:
            raise ValueError()
        return data
    except (ValueError, KeyError, TypeError):
        raise RelayError("invalid cursor or cursor belongs to another machine/agent/session") from None


def load_session(agent: str, source: str | Path, machine: str, profile: str = "default") -> dict:
    if agent not in AGENTS:
        raise RelayError("unsupported agent; choose claude, omo or omp")
    path = safe_path(source)
    with path.open("rb") as stream:
        raw = stream.read(MAX_SOURCE + 1)
    if len(raw) > MAX_SOURCE:
        raise RelayError("source grew beyond 64 MiB")
    lines = raw.split(b"\n")
    partial = bool(lines[-1])
    lines = lines[:-1]  # An unfinished final JSON record is never consumed.
    session_id = None
    title = "Untitled"
    title_source = "missing"
    cwd = None
    records, seen, times = [], {}, []
    for line_no, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
            if not isinstance(obj, dict):
                raise ValueError()
        except (ValueError, UnicodeDecodeError):
            raise RelayError(f"malformed complete JSONL record at line {line_no}; content withheld") from None
        typ = obj.get("type")
        observed = timestamp(obj.get("timestamp"))
        if observed is not None:
            times.append(observed)
        if agent == "claude":
            sid = obj.get("sessionId")
            if sid:
                if session_id and session_id != sid:
                    raise RelayError("mixed session identities in one source")
                session_id = sid
            cwd = obj.get("cwd", cwd)
            if typ == "custom-title" and isinstance(obj.get("customTitle"), str):
                title, title_source = obj["customTitle"], "custom-title"
            if typ == "ai-title" and isinstance(obj.get("aiTitle"), str) and title_source != "custom-title":
                title, title_source = obj["aiTitle"], "ai-title"
            message = obj.get("message") if typ in {"user", "assistant"} else None
            if obj.get("isSidechain"):
                message = None
            rid = obj.get("uuid")
            parent = obj.get("parentUuid")
        else:
            if typ == "title" and isinstance(obj.get("title"), str):
                title, title_source = obj["title"], "title-slot"
                continue  # Mutable title slot does not invalidate transcript cursors.
            if typ == "session":
                if obj.get("version", 1) not in {1, 2, 3}:
                    raise RelayError("unsupported session format version")
                session_id, cwd = obj.get("id"), obj.get("cwd")
                continue
            if typ in {"session_info", "session-info"} and isinstance(obj.get("name"), str):
                title, title_source = obj["name"], "session-info"
            message = obj.get("message") if typ == "message" else None
            rid, parent = obj.get("id"), obj.get("parentId")
        if not rid and not message:
            continue
        # Entries without UUIDs (legacy exports) get content-addressed identities.
        rid = str(rid or "legacy-" + digest(obj))
        fp = digest(obj)
        if rid in seen:
            if seen[rid] != fp:
                raise RelayError("entry identity changed in source; explicit recovery required")
            continue
        seen[rid] = fp
        role, text, omissions = None, "", {}
        if isinstance(message, dict) and message.get("role") in {"user", "assistant"}:
            role = message["role"]
            text, omissions = prose(message)
        elif message is not None:
            omissions = {"excluded_message": 1}
        records.append({"id": rid, "fp": fp, "parent": parent, "role": role,
                        "text": text, "timestamp": obj.get("timestamp"), "omissions": omissions})
    if not session_id:
        if agent == "claude" and re.fullmatch(r"[a-fA-F0-9-]{32,36}", path.stem):
            session_id = path.stem
        else:
            raise RelayError("source has no verified session ID")
    title, _ = sanitize(title)
    identity = {"machine": machine, "agent": agent, "profile": profile, "session_id": str(session_id)}
    return {"identity": identity, "title": title, "title_source": title_source,
            "project": cwd, "source": str(path), "records": records, "partial_tail": partial,
            "last_activity_epoch": max(times) if times else None,
            "last_activity": stamp(max(times)) if times else None,
            "cursor": encode_cursor(identity, records[-1] if records else None)}


def roots(agent: str, home: Path | None = None) -> list[tuple[str, Path]]:
    home = home or Path.home()
    if agent == "claude":
        return [("default", Path(os.environ.get("CLAUDE_CONFIG_DIR", home / ".claude")) / "projects")]
    if agent == "omo":
        base = next((os.environ[k] for k in ("OMO_CODING_AGENT_DIR", "SENPI_CODING_AGENT_DIR", "PI_CODING_AGENT_DIR") if os.environ.get(k)), str(home / ".omo/agent"))
        return [("default", Path(base) / "sessions")]
    base = os.environ.get("PI_CODING_AGENT_DIR")
    if base:
        return [("default", Path(base) / "sessions")]
    # OMP defines PI_CONFIG_DIR as a directory name joined under home.
    # Node path.join keeps the home prefix even for a leading slash.
    config = home / os.environ.get("PI_CONFIG_DIR", ".omp").lstrip("/")
    found = [("default", config / "agent/sessions")]
    profiles = config / "profiles"
    if profiles.is_dir():
        found.extend((p.name, p / "agent/sessions") for p in sorted(profiles.iterdir()) if p.is_dir())
    if os.environ.get("PI_CODING_AGENT_SESSION_DIR"):
        found.insert(0, ("session-dir", Path(os.environ["PI_CODING_AGENT_SESSION_DIR"])))
    return found


def inventory(agents: list[str], machine: str, since: float | None, query: str = "", extra_roots: list[str] | None = None) -> dict:
    sessions, errors, scanned, root_report = [], [], 0, []
    identities = {}
    for agent in agents:
        locations = roots(agent)
        for entry in extra_roots or []:
            parts = entry.split("=", 1)
            if len(parts) != 2 or parts[0] not in AGENTS:
                raise RelayError("--root must be agent=/allowed/session/root")
            if parts[0] == agent:
                locations.append(("explicit", Path(parts[1]).expanduser()))
        paths = set()
        for profile, root in locations:
            root_report.append({"agent": agent, "profile": profile, "root": str(root), "exists": root.is_dir()})
            if not root.is_dir():
                continue
            # Main sessions only: no Claude subagent histories or private databases.
            for path in root.rglob("*.jsonl"):
                if "extensions" in path.relative_to(root).parts[:-1]:
                    continue  # Extension goal/event histories are not agent sessions.
                if agent == "claude" and any(p in {"subagents", "transcripts", "precompact"} for p in path.relative_to(root).parts[:-1]):
                    continue
                resolved = path.resolve()
                if resolved in paths:
                    continue
                paths.add(resolved)
                scanned += 1
                if scanned > MAX_FILES:
                    raise RelayError("inventory exceeded 20000 files; narrow roots before claiming completeness")
                try:
                    session = load_session(agent, path, machine, profile)
                    epoch = session["last_activity_epoch"]
                    if since is not None and epoch is None:
                        errors.append({"agent": agent, "source": str(path),
                                       "error": "activity timestamp unavailable; recent-window membership unknown"})
                        continue
                    if since is not None and epoch < since:
                        continue
                    if query.casefold() not in (session["title"] + " " + session["identity"]["session_id"] + " " + str(session["project"])).casefold():
                        continue
                    row = {k: v for k, v in session.items() if k not in {"records", "last_activity_epoch"}}
                    key = digest(session["identity"])
                    if key in identities:
                        identities[key]["alternate_sources"] = identities[key].get("alternate_sources", []) + [row["source"]]
                        identities[key]["ambiguous_source"] = True
                    else:
                        identities[key] = row
                        sessions.append(row)
                except (OSError, RelayError) as error:
                    errors.append({"agent": agent, "source": str(path), "error": str(error)})
    sessions.sort(key=lambda s: s["last_activity"] or "", reverse=True)
    return {"machine": machine, "observed_at": stamp(), "since": stamp(since) if since is not None else None,
            "sessions": sessions, "count": len(sessions), "scanned_files": scanned,
            "coverage": "complete_for_reported_roots" if not errors else "incomplete",
            "roots": root_report, "errors": errors}


def delta(session: dict, after: str | None, max_chars: int = 32000) -> dict:
    if max_chars < 1:
        raise RelayError("max-chars must be positive")
    records, identity = session["records"], session["identity"]
    index, offset = 0, 0
    if after:
        cursor = decode_cursor(after, identity)
        if cursor["anchor"]:
            matches = [i for i, r in enumerate(records) if r["id"] == cursor["anchor"]]
            if not matches or records[matches[0]]["fp"] != cursor["fingerprint"]:
                raise RelayError("cursor gap: anchor removed or changed by rotation/truncation; choose explicit replay/rebind")
            index, offset = matches[0], cursor["offset"]
            if offset == 0:
                index += 1
            elif offset > len(records[index]["text"]):
                raise RelayError("cursor continuation is beyond message length")
    messages, omissions, branches, used = [], {}, [], 0
    next_cursor = after or encode_cursor(identity, None)
    ids = {r["id"] for r in records}
    for i in range(index, len(records)):
        record = records[i]
        if i > 0 and record["parent"] in ids and record["parent"] != records[i - 1]["id"]:
            branches.append({"entry_id": record["id"], "parent_id": record["parent"]})
        for key, count in record["omissions"].items():
            omissions[key] = omissions.get(key, 0) + count
        text = record["text"][offset:] if i == index else record["text"]
        if text and record["role"]:
            take = min(len(text), max_chars - used)
            if take <= 0:
                break
            messages.append({"id": record["id"], "role": record["role"], "timestamp": record["timestamp"],
                             "text": text[:take], "continuation": bool(i == index and offset)})
            used += take
            if take < len(text):
                next_cursor = encode_cursor(identity, record, (offset if i == index else 0) + take)
                break
        next_cursor = encode_cursor(identity, record)
        offset = 0
    return {"identity": identity, "messages": messages, "next_cursor": next_cursor,
            "omissions": {k: v for k, v in omissions.items() if v}, "branches": branches,
            "partial_tail_waiting": session["partial_tail"], "last_activity": session["last_activity"]}


def render(batch: dict, mode: str) -> str:
    messages = batch["messages"]
    if mode == "summary":
        # A factual extract for the relay to summarize, not a fabricated semantic status.
        parts = []
        for role in ("user", "assistant"):
            matching = [m for m in messages if m["role"] == role]
            if matching:
                text = matching[-1]["text"]
                parts.append(f"Latest {role} prose ({len(matching)} new message(s)):\n" + text[:800] + ("\n[excerpt clipped]" if len(text) > 800 else ""))
    else:
        parts = [f"### {m['role']} · {m['id']}\n\n" + m["text"] for m in messages]
    if not parts:
        parts = ["No new allowed user/assistant prose."]
    if batch.get("branches"):
        parts.append("[Branch change observed; this is append-order prose, not a claim about the active branch.]")
    if batch.get("omissions"):
        parts.append("[Sanitized output; omissions: " + json.dumps(batch["omissions"], sort_keys=True) + ".]")
    if batch.get("partial_tail_waiting"):
        parts.append("[Incomplete final JSONL record deferred.]")
    return "\n\n".join(parts)


class Store:
    def __init__(self, root: Path, machine: str, relay_id: str):
        self.root = root.expanduser() / digest(machine)[:16]
        self.relay_id, self.machine = relay_id, machine
        self.file = self.root / (digest(relay_id)[:24] + ".json")
        # Prevent accidentally syncing cursors, outboxes, approvals or locks.
        if any(p in {".agents", ".git", "skills"} for p in self.root.resolve().parts):
            raise RelayError("state root must be local and outside synced skill/Git directories")

    @contextlib.contextmanager
    def lock(self):
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.root, 0o700)
        with (self.root / ".lock").open("a") as lock:
            os.chmod(lock.name, 0o600)
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise RelayError("another relay operation owns the local state lock") from None
            yield

    def get(self) -> dict:
        if not self.file.exists():
            return {"v": 1, "relay_id": self.relay_id, "machine": self.machine}
        try:
            data = json.loads(self.file.read_text())
            if data.get("v") != 1 or data.get("relay_id") != self.relay_id or data.get("machine") != self.machine:
                raise ValueError()
            return data
        except (ValueError, OSError):
            raise RelayError("invalid local state; preserve it and recover explicitly") from None

    def save(self, data: dict):
        fd, name = tempfile.mkstemp(prefix=".relay-", dir=self.root)
        try:
            with os.fdopen(fd, "w") as stream:
                json.dump(data, stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, self.file)
        finally:
            if os.path.exists(name):
                os.unlink(name)

    def bind(self, session: dict, replace: bool = False) -> dict:
        data = self.get()
        if data.get("binding") and data["binding"]["identity"] != session["identity"] and not replace:
            raise RelayError("relay already bound; selecting another session requires --replace")
        for file in self.root.glob("*.json"):
            other = json.loads(file.read_text())
            if other.get("relay_id") != self.relay_id and other.get("binding", {}).get("identity") == session["identity"]:
                return {"reused": True, "relay_id": other["relay_id"], "identity": session["identity"]}
        if data.get("binding", {}).get("identity") == session["identity"]:
            # Source relocation must match identity; never reset delivery cursors implicitly.
            data["binding"]["source"] = session["source"]
            self.save(data)
            return {"reused": True, "relay_id": self.relay_id, "identity": session["identity"]}
        if data.get("monitor", {}).get("automation_id") and data.get("monitor", {}).get("status") == "ACTIVE":
            raise RelayError("pause the bound heartbeat through the supported tool before replacing this binding")
        slug = re.sub(r"[^a-z0-9]+", "-", session["title"].lower()).strip("-")[:36] or "session"
        name = f"Lev Proxy {session['identity']['session_id'][:4]}-{slug}-{digest(session['identity'])[:6]}"
        data = {"v": 1, "relay_id": self.relay_id, "machine": self.machine,
                "binding": {k: session[k] for k in ("identity", "source", "title", "project")},
                "optional_child_title": name, "read_cursor": None, "delivery_cursor": None,
                "ack_cursor": None, "last_source_activity": session["last_activity"], "bound_at": stamp()}
        self.save(data)
        return {"reused": False, "relay_id": self.relay_id, "binding": data["binding"], "optional_child_title": name}

    def read(self, mode: str, scheduled: bool = False, now: float | None = None, max_chars: int = 32000) -> dict:
        data = self.get()
        if not data.get("binding"):
            raise RelayError("relay is unbound; list/find then bind an exact agent/session")
        binding = data["binding"]
        identity = binding["identity"]
        session = load_session(identity["agent"], binding["source"], self.machine, identity["profile"])
        if session["identity"] != identity:
            raise RelayError("bound path now contains a different session; refusing to retarget")
        now = time.time() if now is None else now
        monitor = data.get("monitor", {})
        activity = session["last_activity_epoch"]
        if activity is not None:
            data["last_source_activity"] = stamp(activity)
        reason = None
        if monitor:
            if monitor.get("expires_at") and now >= timestamp(monitor["expires_at"]):
                reason = "duration_expired"
            elif activity is None:
                reason = "source_activity_unknown"
            elif activity is not None and now - activity >= 900:
                reason = "source_idle_15_minutes"
            if reason:
                monitor["status"] = "PAUSED"
                monitor["pause_reason"] = reason
            # A user wake reads even while paused. It does not renew a monitoring lease.
        action = {"schedule_action": "pause" if reason else "none", "automation_id": monitor.get("automation_id"),
                  "monitor_status": monitor.get("status", "OFF"), "pause_reason": reason}
        if scheduled and (reason or monitor.get("status") != "ACTIVE"):
            self.save(data)
            return {**action, "quiet": True, "reason": reason or "monitor_not_active"}
        pending = data.get("pending")
        if pending:
            pending = {**pending, "mode": mode, "markdown": render(pending, mode)}
            self.save(data)
            return {**pending, **action, "replayed_pending": True,
                    "requires_delivery_verification": pending["status"] == "prepared"}
        batch = delta(session, data.get("read_cursor"), max_chars)
        data["read_cursor"] = batch["next_cursor"]
        batch_id = digest([identity, data.get("ack_cursor"), batch["next_cursor"]])[:24]
        result = {**batch, **action, "batch_id": batch_id, "status": "prepared", "mode": mode,
                  "markdown": render(batch, mode), "quiet": not batch["messages"] and not batch["omissions"]}
        if batch["next_cursor"] != data.get("ack_cursor") or batch["messages"]:
            data["pending"] = result
        self.save(data)
        return result

    def receipt(self, batch_id: str, receipt: str | None, ack: bool = False) -> dict:
        data = self.get()
        if data.get("last_acked_batch") == batch_id:
            return {"acknowledged": True, "idempotent": True, "batch_id": batch_id}
        pending = data.get("pending")
        if not pending or pending["batch_id"] != batch_id:
            raise RelayError("no matching pending delivery")
        if ack:
            if pending["status"] != "delivered":
                raise RelayError("cannot acknowledge before a verified chat delivery receipt")
            data["ack_cursor"] = pending["next_cursor"]
            data["last_acked_batch"] = batch_id
            del data["pending"]
        else:
            if not receipt:
                raise RelayError("delivery requires a supported chat receipt reference")
            pending["status"] = "delivered"
            pending["receipt"] = receipt
            data["delivery_cursor"] = pending["next_cursor"]
        self.save(data)
        return {"batch_id": batch_id, "acknowledged": ack, "delivery_cursor": data.get("delivery_cursor"),
                "ack_cursor": data.get("ack_cursor")}

    def monitor(self, minutes: int, duration: int | None, mode: str, now: float | None = None) -> dict:
        if minutes < 5 or minutes > 1440:
            raise RelayError("cadence must be 5..1440 minutes; default is 15")
        if duration is not None and duration <= 0:
            raise RelayError("duration must be positive")
        data = self.get()
        if not data.get("binding"):
            raise RelayError("bind a session before monitoring")
        now = time.time() if now is None else now
        old = data.get("monitor", {})
        data["monitor"] = {"status": "REQUESTED", "every_minutes": minutes, "mode": mode,
                           "requested_at": stamp(now), "expires_at": stamp(now + duration * 60) if duration else None,
                           "automation_id": old.get("automation_id"), "destination_thread": self.relay_id}
        self.save(data)
        return {**data["monitor"], "schedule_created": False,
                "next_action": "create/update one supported heartbeat targeting this relay; record confirmed result"}

    def schedule_record(self, automation_id: str, destination: str, status: str) -> dict:
        data = self.get()
        if not data.get("monitor") or destination != self.relay_id:
            raise RelayError("schedule must target the same bound Lev Relay thread")
        data["monitor"].update(automation_id=automation_id, status=status, destination_thread=destination)
        self.save(data)
        return data["monitor"]

    def prepare(self, message: str) -> dict:
        data = self.get()
        if not data.get("binding"):
            raise RelayError("bind before preparing steering")
        if data.get("steering", {}).get("status") in {"sending", "uncertain"}:
            raise RelayError("prior send has no verified receipt; do not retry")
        ticket = digest([data["binding"]["identity"], message, stamp()])[:24]
        proposal = {"ticket": ticket, "message": message, "sha256": hashlib.sha256(message.encode()).hexdigest(),
                    "identity": data["binding"]["identity"], "status": "awaiting_human_approval"}
        data["steering"] = proposal
        self.save(data)
        return {"ticket": ticket, "message_sha256": proposal["sha256"], "status": proposal["status"],
                "next_action": "show exact message; ask the human whether to send; no message has been sent"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--machine", default=socket.gethostname())
    parser.add_argument("--relay-id", default=os.environ.get("LEV_RELAY_ID"))
    parser.add_argument("--state-root", type=Path, default=Path.home() / ".local/state/lev/relay")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("list", "find"):
        p = sub.add_parser(command)
        p.add_argument("query", nargs="?", default="")
        p.add_argument("--agent", action="append", choices=AGENTS)
        p.add_argument("--since-hours", type=float, default=24)
        p.add_argument("--all", action="store_true")
        p.add_argument("--root", action="append")
    p = sub.add_parser("read")
    p.add_argument("--agent", choices=AGENTS)
    p.add_argument("--source")
    p.add_argument("--profile", default="default")
    p.add_argument("--after")
    p.add_argument("--mode", choices=("summary", "trace"), default="summary")
    p.add_argument("--max-chars", type=int, default=32000)
    p = sub.add_parser("bind")
    p.add_argument("--agent", choices=AGENTS, required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--session-id", required=True)
    p.add_argument("--profile", default="default")
    p.add_argument("--replace", action="store_true")
    p = sub.add_parser("wake")
    p.add_argument("--scheduled", action="store_true")
    p.add_argument("--mode", choices=("summary", "trace"), default="summary")
    p.add_argument("--max-chars", type=int, default=32000)
    sub.add_parser("status")
    for command in ("delivered", "ack"):
        p = sub.add_parser(command)
        p.add_argument("--batch-id", required=True)
        if command == "delivered":
            p.add_argument("--receipt", required=True)
    p = sub.add_parser("monitor")
    p.add_argument("--every", type=int, default=15, help="minutes (explicit 5 supported)")
    p.add_argument("--for-minutes", type=int)
    p.add_argument("--mode", choices=("summary", "trace"), default="summary")
    p = sub.add_parser("schedule-record")
    p.add_argument("--automation-id", required=True)
    p.add_argument("--destination-thread", required=True)
    p.add_argument("--status", choices=("ACTIVE", "PAUSED"), required=True)
    p = sub.add_parser("steer-prepare")
    p.add_argument("--message-file", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command in {"list", "find"}:
            since = None if args.all else time.time() - args.since_hours * 3600
            result = inventory(args.agent or list(AGENTS), args.machine, since, args.query, args.root)
        elif args.command == "read" and args.source:
            if not args.agent:
                raise RelayError("stateless --source read also requires --agent")
            result = delta(load_session(args.agent, args.source, args.machine, args.profile), args.after, args.max_chars)
            result["markdown"] = render(result, args.mode)
        else:
            if not args.relay_id:
                raise RelayError("stateful commands require --relay-id with the exact Codex thread ID")
            store = Store(args.state_root, args.machine, args.relay_id)
            with store.lock():
                if args.command == "bind":
                    session = load_session(args.agent, args.source, args.machine, args.profile)
                    if session["identity"]["session_id"] != args.session_id:
                        raise RelayError("session ID does not match source header")
                    result = store.bind(session, args.replace)
                elif args.command in {"read", "wake"}:
                    result = store.read(args.mode, getattr(args, "scheduled", False), max_chars=args.max_chars)
                elif args.command == "status":
                    result = store.get()
                    if result.get("pending"):
                        result["pending"] = {k: result["pending"][k] for k in ("batch_id", "status", "next_cursor")}
                    if result.get("steering"):
                        result["steering"] = {k: result["steering"][k] for k in ("ticket", "sha256", "status")}
                elif args.command in {"delivered", "ack"}:
                    result = store.receipt(args.batch_id, getattr(args, "receipt", None), args.command == "ack")
                elif args.command == "monitor":
                    result = store.monitor(args.every, args.for_minutes, args.mode)
                elif args.command == "schedule-record":
                    result = store.schedule_record(args.automation_id, args.destination_thread, args.status)
                else:
                    result = store.prepare(args.message_file.read_text())
        if args.format == "markdown" and "markdown" in result:
            print(result["markdown"])
            print("\n<!-- next cursor: " + result["next_cursor"] + " -->")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (RelayError, OSError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
