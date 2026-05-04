#!/usr/bin/env python3
"""Merge per-agent inventory (claude.json + codex.json) → canonical coverage.json.

Filters human-rooted, applies 5-min fold rule for parallel fan-outs, embeds
classifier results + workstream registry snapshot, resolves transcript paths
to XDG cache (~/.cache/cass-lev/<project>/<chain>/<sid>.html).

Usage:
    python3 merge.py --window 2026-04-03 2026-04-27 \
        --inputs /path/to/inventory \
        --workstreams /Users/.../.lev/pm/workstreams \
        --classifier /path/to/classifier.json \
        --project leviathan \
        --output coverage.json
"""
import argparse, json, re, datetime, os, socket
from pathlib import Path

NON_HUMAN_PATTERNS = [
    r"^# Task:", r"^# Sub-task:", r"^<local-command-caveat>", r"^<command-message>",
    r"^/[a-z][a-z0-9-]+\b", r"\blev exec\b", r"^DNA[ -]cascade",
    r"^\s*Task:\s", r"^\s*Subtask:\s",
]

FOLD_PATTERNS = [
    (re.compile(r"^\$codex-autoresearch", re.I), "autoresearch"),
    (re.compile(r"^\$lev-intake", re.I), "lev-intake"),
    (re.compile(r"^\$intake", re.I), "intake"),
    (re.compile(r"^CDO Turn", re.I), "cdo-turn"),
    (re.compile(r"^Adaptive CDO", re.I), "cdo-adaptive"),
    (re.compile(r"^Hermes deep dive", re.I), "hermes"),
    (re.compile(r"^You are the (\w+) mode", re.I), "ntm-mode"),
    (re.compile(r"^You are the Discover", re.I), "discover-agent"),
    (re.compile(r"^tCursor Agent v", re.I), "cursor-telemetry"),
]


def is_human(text):
    if not text: return False
    s = text.strip()
    for p in NON_HUMAN_PATTERNS:
        if re.search(p, s, re.I): return False
    return True


def topic_text(c):
    return c.get("topic") or c.get("first_user_text") or ""


def clean_topic(c):
    t = topic_text(c).strip()
    if t.startswith("<command-message>"):
        mc = re.search(r"<command-message>([^<]+)</command-message>", t)
        rest = re.sub(r"<[^>]+>", "", t).strip()
        t = f"/{mc.group(1)} — {rest}" if mc else "(slash command)"
    return t


def short(t, n=60):
    t = re.sub(r"\s+", " ", t).strip()
    return t[:n] + "…" if len(t) > n else t


def fold_key(c):
    topic = topic_text(c).strip()
    for rx, name in FOLD_PATTERNS:
        if rx.search(topic):
            ts = (c.get("started_at") or "")[:16]
            try:
                dt = datetime.datetime.fromisoformat(ts.replace("Z", ""))
                bucket = dt.replace(minute=5 * (dt.minute // 5), second=0, microsecond=0).isoformat(timespec="minutes")
            except Exception:
                bucket = ts
            return (name, bucket)
    return None


def load_workstreams(ws_dir):
    out = []
    for ws_yaml in sorted(Path(ws_dir).glob("*/state/workstream.yaml")):
        text = ws_yaml.read_text()
        wsid = re.search(r"workstream_id:\s*(\S+)", text)
        if not wsid: continue
        title = re.search(r'title:\s*"?(.*?)"?\n', text)
        obj = re.search(r'objective:\s*"?(.*?)"?\n', text)
        status = re.search(r'status:\s*(\S+)', text)
        phase = re.search(r'phase:\s*(\S+)', text)
        out.append({
            "id": wsid.group(1),
            "title": title.group(1) if title else "",
            "objective": obj.group(1) if obj else "",
            "status": status.group(1) if status else "",
            "phase": phase.group(1) if phase else "",
        })
    return out


def load_classifier(path):
    """classifier.json shape (legacy) or inline classification dict."""
    if not path or not Path(path).exists(): return {}
    d = json.load(open(path))
    out = {}
    for bucket, items in d.get("buckets", {}).items():
        for it in items:
            out[it["chain_id"]] = {
                "bucket": bucket,
                "ws": it.get("ws"),
                "score": it.get("score"),
                "alts": it.get("alts", []),
                "hint_ws": it.get("hint_ws"),
                "reason": it.get("reason", ""),
            }
    return out


def transcript_path(project, chain_id):
    """Resolve XDG cache path for chain root transcript."""
    safe = re.sub(r"[^A-Za-z0-9_-]", "", chain_id)
    cache_root = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "cass-lev" / project / safe
    return cache_root


def find_transcript(project, chain_id, root_sid):
    """Return absolute path to baked HTML if it exists, else None."""
    p = transcript_path(project, chain_id) / f"{root_sid}.html"
    return str(p) if p.exists() else None


def enrich(chains, agent, classifier, project):
    out = []
    for c in chains:
        if c.get("msg_total", 0) < 5: continue
        if not is_human(topic_text(c)): continue
        cid = c["chain_id"]
        lineage = c.get("lineage", [cid])
        root_sid = lineage[0] if lineage else cid
        topic = clean_topic(c)
        out.append({
            "id": cid,
            "agent": agent,
            "topic": topic[:200],
            "topic_short": short(topic, 60),
            "msgs": c.get("msg_total", 0),
            "lineage": lineage,
            "n_sessions": len(lineage),
            "started": (c.get("started_at") or "")[:10],
            "ended": (c.get("ended_at") or "")[:10],
            "started_full": c.get("started_at", ""),
            "ws": c.get("workstream_match"),
            "status": c.get("status", "orphan"),
            "session_paths": c.get("session_paths", []),
            "transcript_path": find_transcript(project, cid, root_sid),
            "handoff_refs": c.get("handoff_refs", []) or [],
            "resume_signals": c.get("resume_signals", []) or [],
            "fold_key": fold_key(c),
            "classification": classifier.get(cid),
        })
    return out


def apply_fold(all_chains, project):
    fold_groups = {}
    for c in all_chains:
        if c["fold_key"]:
            fold_groups.setdefault(c["fold_key"], []).append(c)

    folded_in = set()
    parents = []
    for key, members in fold_groups.items():
        if len(members) < 2: continue
        members.sort(key=lambda c: c["started_full"])
        root = members[0]
        name, bucket = key
        fold_id = f"fold:{name}:{bucket}"
        captured_any = any(c["status"] == "captured" for c in members)
        ws_match = next((c["ws"] for c in members if c["ws"]), None)
        parent_topic = f"[{name} fan-out] {root['topic'][:80]} +{len(members)-1} parallel"
        parent = {
            "id": fold_id,
            "agent": root["agent"],
            "topic": parent_topic[:200],
            "topic_short": f"[{name}] {root['topic_short'][:40]} ×{len(members)}",
            "msgs": sum(c["msgs"] for c in members),
            "lineage": [c["id"] for c in members],
            "n_sessions": len(members),
            "started": root["started"], "ended": members[-1]["ended"],
            "started_full": root["started_full"],
            "ws": ws_match,
            "status": "captured" if captured_any else "orphan",
            "session_paths": [p for c in members for p in c["session_paths"]],
            "transcript_path": members[0]["transcript_path"],  # link to first member
            "handoff_refs": list({h for c in members for h in c["handoff_refs"]}),
            "resume_signals": list({s for c in members for s in c["resume_signals"]}),
            "is_fold": True,
            "fold_kind": name,
            "fold_members": [c["id"] for c in members],
            "classification": None,
        }
        parents.append(parent)
        folded_in.update(c["id"] for c in members)

    return [c for c in all_chains if c["id"] not in folded_in] + parents


def stats(chains):
    cap = sum(1 for c in chains if c["status"] == "captured")
    return dict(
        chains=len(chains),
        captured=cap,
        orphan=len(chains) - cap,
        capture_pct=round(100 * cap / max(1, len(chains)), 1),
        multi_session=sum(1 for c in chains if c["n_sessions"] > 1),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", nargs=2, required=True, metavar=("FROM", "TO"))
    ap.add_argument("--inputs", required=True, help="dir containing claude.json + codex.json")
    ap.add_argument("--workstreams", required=True, help=".lev/pm/workstreams dir")
    ap.add_argument("--classifier", default=None, help="optional classifier.json path")
    ap.add_argument("--project", required=True, help="project slug for XDG cache namespacing")
    ap.add_argument("--output", required=True, help="output coverage.json path")
    args = ap.parse_args()

    inputs = Path(args.inputs)
    ws_registry = load_workstreams(args.workstreams)
    classifier = load_classifier(args.classifier)

    claude_in = inputs / "claude.json"
    codex_in = inputs / "codex.json"
    claude = json.load(open(claude_in)) if claude_in.exists() else {"chains": [], "totals": {"raw_sessions": 0, "chains": 0}}
    codex = json.load(open(codex_in)) if codex_in.exists() else {"chains": [], "totals": {"raw_sessions": 0, "chains": 0}}

    claude_h = enrich(claude["chains"], "claude_code", classifier, args.project)
    codex_h = enrich(codex["chains"], "codex", classifier, args.project)

    all_chains = claude_h + codex_h
    final = apply_fold(all_chains, args.project)
    final.sort(key=lambda c: -c["msgs"])

    # drop fold_key (internal)
    for c in final:
        c.pop("fold_key", None)
        if not c.get("is_fold"):
            c["is_fold"] = False

    combined = stats(final)
    combined["fold_count"] = sum(1 for c in final if c.get("is_fold"))
    combined["fold_collapsed"] = sum(c["n_sessions"] for c in final if c.get("is_fold"))
    combined["auto_attribute"] = sum(1 for c in final if c.get("classification") and c["classification"].get("bucket") == "auto_attribute")

    out = {
        "meta": {
            "schema_version": "1.0",
            "project": args.project,
            "machine": socket.gethostname(),
            "window": args.window,
            "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "totals": combined,
        },
        "agents": {
            "claude_code": {
                "raw_sessions": claude["totals"]["raw_sessions"],
                "all_chains": claude["totals"]["chains"],
                "human_rooted": stats(claude_h),
            },
            "codex": {
                "raw_sessions": codex["totals"]["raw_sessions"],
                "all_chains": codex["totals"]["chains"],
                "human_rooted": stats(codex_h),
            },
        },
        "workstreams": ws_registry,
        "chains": final,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)
    size_kb = out_path.stat().st_size // 1024
    print(f"wrote {out_path} ({size_kb} KB)")
    print(f"chains: {combined['chains']} (captured {combined['captured']} / orphan {combined['orphan']} = {combined['capture_pct']}%)")
    print(f"folds: {combined['fold_count']} parents collapsing {combined['fold_collapsed']} sub-runs")
    print(f"auto-attribute: {combined['auto_attribute']}")


if __name__ == "__main__":
    main()
