#!/usr/bin/env python3
"""Build per-agent session inventory + resume-chain detection for one window.

Produces:  <outdir>/claude.json  +  <outdir>/codex.json
Each shape:
  {
    "agent": "claude_code"|"codex",
    "window": ["YYYY-MM-DD","YYYY-MM-DD"],
    "totals": {raw_sessions, chains, captured_chains, orphan_chains},
    "chains": [{chain_id, lineage[], session_paths[], started_at, ended_at,
                msg_total, topic, handoff_refs[], resume_signals[],
                workstream_match|null, status: "captured"|"orphan"}]
  }

Designed to be called per agent. Cursor support deferred (cass workspace
filter broken for cursor — needs sqlite mining, see SKILL.md "known gaps").

Usage:
    python3 inventory.py --agent claude_code --window 2026-04-03 2026-04-27 \
        --workstreams /path/to/.lev/pm/workstreams \
        --output-dir /path/to/inventory
"""
import argparse, json, re, datetime, os
from pathlib import Path

CLAUDE_PROJ_DIR = Path.home() / ".claude" / "projects"
CODEX_SESS_DIR = Path.home() / ".codex" / "sessions"

RESUME_SIGNALS = [
    (re.compile(r"\d{8}-[a-z0-9-]+-session-\d+\.md"), "handoff_filename_ref"),
    (re.compile(r"<persisted-output>"), "session-restore"),
    (re.compile(r"\[LEV SESSION CONTEXT\]"), "lev_session_context"),
    (re.compile(r"^/handoff-resume\b"), "handoff_resume_cmd"),
    (re.compile(r"FIRST STOP CHECKPOINT", re.I), "stop_checkpoint"),
    (re.compile(r"Latest Handoff", re.I), "latest_handoff"),
    (re.compile(r"Context Recovery", re.I), "context_recovery"),
    (re.compile(r"^/work resume\b"), "work_resume"),
    (re.compile(r"^/ws resume\b"), "ws_resume"),
    (re.compile(r"rollout-\d{4}-\d{2}-\d{2}T", re.I), "rollout_file_ref"),
]

CLEAR_SIGNALS = [
    (re.compile(r"^/clear\b"), "clear"),
    (re.compile(r"^/compact\b"), "compact"),
]

HANDOFF_RX = re.compile(r"(\d{8}-[a-z0-9-]+-session-\d+\.md)", re.I)


def in_window(mtime, since, until):
    d = datetime.date.fromtimestamp(mtime)
    return since <= d <= until + datetime.timedelta(days=1)


def parse_jsonl(path, max_lines=None):
    """Yield records from a jsonl file. Handles malformed lines."""
    try:
        with open(path) as f:
            for i, line in enumerate(f):
                if max_lines and i >= max_lines: return
                line = line.strip()
                if not line: continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except (OSError, FileNotFoundError):
        return


def get_text(rec):
    """Extract user-visible text from one record (handles both claude and codex shapes)."""
    msg = rec.get("message") or rec.get("content") or rec
    if isinstance(msg, dict):
        c = msg.get("content")
        if isinstance(c, str): return c
        if isinstance(c, list):
            parts = []
            for p in c:
                if isinstance(p, dict):
                    if p.get("type") == "text": parts.append(p.get("text", ""))
                    elif "text" in p: parts.append(p["text"])
                elif isinstance(p, str): parts.append(p)
            return "\n".join(parts)
    if isinstance(msg, str): return msg
    return ""


def role_of(rec):
    msg = rec.get("message") or {}
    return rec.get("role") or msg.get("role") or rec.get("type")


def scan_session(path, head=30, tail=10):
    """Return: msg_count, first_msg_ts, last_msg_ts, first_user_text, signals."""
    records = list(parse_jsonl(path))
    if not records: return None
    first_ts = records[0].get("timestamp") or records[0].get("created") or records[0].get("ts") or ""
    last_ts = records[-1].get("timestamp") or records[-1].get("created") or records[-1].get("ts") or ""

    first_user_text = ""
    for r in records[:head]:
        if role_of(r) in ("user", "human"):
            t = get_text(r).strip()
            if t and not t.startswith("<system-reminder>"):
                first_user_text = t[:500]
                break

    head_text = "\n".join(get_text(r) for r in records[:head])
    tail_text = "\n".join(get_text(r) for r in records[-tail:])

    signals = []
    for rx, name in RESUME_SIGNALS:
        if rx.search(head_text): signals.append(name)

    handoff_refs = list(set(HANDOFF_RX.findall(head_text)))

    clear_signals = []
    for rx, name in CLEAR_SIGNALS:
        if rx.search(tail_text): clear_signals.append(name)

    return {
        "msg_count": len(records),
        "first_msg_ts": first_ts,
        "last_msg_ts": last_ts,
        "first_user_text": first_user_text,
        "resume_signals": signals,
        "clear_signals": clear_signals,
        "handoff_refs": handoff_refs,
    }


def list_claude_sessions(window_since, window_until):
    """Top-level human-owned only — exclude subagents/, conductor, worktree-suffixed dirs."""
    proj = CLAUDE_PROJ_DIR / "-Users-jean-patricksmith-digital-leviathan"
    if not proj.exists(): return []
    out = []
    for f in proj.glob("*.jsonl"):
        if not in_window(f.stat().st_mtime, window_since, window_until): continue
        out.append({"sid": f.stem, "path": str(f)})
    return out


def list_codex_sessions(window_since, window_until):
    """All codex jsonl in window, filtered to leviathan-touching."""
    out = []
    for year_dir in CODEX_SESS_DIR.iterdir() if CODEX_SESS_DIR.exists() else []:
        if not year_dir.is_dir(): continue
        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir(): continue
            for day_dir in month_dir.iterdir():
                if not day_dir.is_dir(): continue
                for f in day_dir.glob("*.jsonl"):
                    if not in_window(f.stat().st_mtime, window_since, window_until): continue
                    # quick leviathan filter — slurp first 4KB
                    try:
                        head = open(f).read(4096)
                        if "digital/leviathan" not in head: continue
                    except OSError:
                        continue
                    out.append({"sid": f.stem, "path": str(f)})
    return out


def load_workstream_slugs(ws_dir):
    """Return set of registered workstream ids."""
    slugs = set()
    for ws_yaml in Path(ws_dir).glob("*/state/workstream.yaml"):
        text = ws_yaml.read_text()
        m = re.search(r"workstream_id:\s*(\S+)", text)
        if m: slugs.add(m.group(1))
    return slugs


def load_handoff_index(handoffs_dir, window_since, window_until):
    """Map session_id (UUID) → list of handoff paths that mention it.
    Also map handoff filename → workstream slug (parsed from frontmatter)."""
    handoff_to_ws = {}
    sid_to_handoffs = {}
    for h in Path(handoffs_dir).glob("*.md"):
        try:
            text = h.read_text()
        except OSError:
            continue
        ws_m = re.search(r"^workstream:\s*(\S+)", text, re.MULTILINE)
        if ws_m:
            handoff_to_ws[h.name] = ws_m.group(1)
        # find UUID-like session refs
        for sid in re.findall(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", text, re.I):
            sid_to_handoffs.setdefault(sid.lower(), []).append(h.name)
        # codex rollout-style ids
        for sid in re.findall(r"rollout-\d{4}-\d{2}-\d{2}T[^\s\)\]]+", text):
            sid_to_handoffs.setdefault(sid, []).append(h.name)
    return handoff_to_ws, sid_to_handoffs


def match_workstream(meta, handoff_to_ws, sid_to_handoffs, ws_slugs):
    """Return (workstream_match, status) tuple."""
    # 1. session UUID cross-ref
    for sid in meta["lineage"]:
        for h in sid_to_handoffs.get(sid.lower(), []):
            ws = handoff_to_ws.get(h)
            if ws and ws in ws_slugs:
                return ws, "captured"
    # 2. handoff_refs in chain content → workstream
    for href in meta["handoff_refs"]:
        ws = handoff_to_ws.get(href)
        if ws and ws in ws_slugs:
            return ws, "captured"
        # legacy fallback: handoff filename contains slug
        for slug in ws_slugs:
            if slug in href.lower():
                return slug, "captured"
    return None, "orphan"


def build_chains(agent, sessions, handoff_to_ws, sid_to_handoffs, ws_slugs):
    """For now, chains = singletons. Resume-link detection done in merge.py via
    relax pass against handoff_refs cross-references. This keeps inventory.py
    straightforward; richer chain logic can be added here later."""
    chains = []
    for s in sessions:
        meta = scan_session(s["path"])
        if not meta: continue
        # Skip truly trivial (msg_count<3)
        if meta["msg_count"] < 3: continue
        # Drop AGENTS.md/skill stubs in codex
        if agent == "codex" and meta["msg_count"] < 6: continue
        chain = {
            "chain_id": s["sid"],
            "lineage": [s["sid"]],
            "session_paths": [s["path"]],
            "started_at": meta["first_msg_ts"],
            "ended_at": meta["last_msg_ts"],
            "msg_total": meta["msg_count"],
            "topic": meta["first_user_text"],
            "handoff_refs": meta["handoff_refs"],
            "resume_signals": meta["resume_signals"],
        }
        ws, status = match_workstream(chain, handoff_to_ws, sid_to_handoffs, ws_slugs)
        chain["workstream_match"] = ws
        chain["status"] = status
        chains.append(chain)
    return chains


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True, choices=["claude_code", "codex"])
    ap.add_argument("--window", nargs=2, required=True, metavar=("FROM", "TO"))
    ap.add_argument("--workstreams", required=True, help=".lev/pm/workstreams dir")
    ap.add_argument("--handoffs", default=None, help=".lev/pm/handoffs dir (default: sibling of workstreams)")
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    since = datetime.date.fromisoformat(args.window[0])
    until = datetime.date.fromisoformat(args.window[1])
    handoffs = Path(args.handoffs) if args.handoffs else Path(args.workstreams).parent / "handoffs"
    ws_slugs = load_workstream_slugs(args.workstreams)
    handoff_to_ws, sid_to_handoffs = load_handoff_index(handoffs, since, until)

    if args.agent == "claude_code":
        sessions = list_claude_sessions(since, until)
    else:
        sessions = list_codex_sessions(since, until)

    print(f"scanning {len(sessions)} {args.agent} sessions in {since}→{until}…")
    chains = build_chains(args.agent, sessions, handoff_to_ws, sid_to_handoffs, ws_slugs)
    cap = sum(1 for c in chains if c["status"] == "captured")

    out = {
        "agent": args.agent,
        "window": args.window,
        "totals": {
            "raw_sessions": len(sessions),
            "chains": len(chains),
            "captured_chains": cap,
            "orphan_chains": len(chains) - cap,
        },
        "chains": chains,
        "uncaptured_session_ids": [c["chain_id"] for c in chains if c["status"] == "orphan"],
    }

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.agent.replace('_code','')}.json"
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"wrote {out_path}: chains={len(chains)}, captured={cap}/{len(chains)}")


if __name__ == "__main__":
    main()
