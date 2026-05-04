#!/usr/bin/env python3
"""Heuristic classifier — score each big orphan chain (msg_total ≥ 50) against
the workstream registry. Reads a coverage.json (or per-agent inventory + ws dir)
and writes classifier.json.

Buckets:
  auto_attribute  score ≥ 7  (high confidence)
  needs_review    score 4-6.99
  archive         score < 4
  bot_dispatch    topic starts with $skill / # Task / <command-message>

Scoring:  keyword overlap between (topic + handoff_refs) and (workstream id + title + objective).
Boost: literal slug hit in topic = +2; handoff filename contains slug = +3.

Usage:
    python3 classify.py --coverage coverage.json --output classifier.json
        OR
    python3 classify.py --inputs <dir> --workstreams <ws-dir> --output classifier.json
"""
import argparse, json, re, datetime
from pathlib import Path

STOP = set("the a an and or to of for in on at by with from as is are be it this that we i you our they them via through using uses based like one each per all not no so but if then which who what when how why".split())

BOT_PREFIXES = (
    r"\$codex-autoresearch", r"\$lev-intake", r"\$intake", r"\$research",
    r"^# Task:", r"^# Sub-task:", r"^<command-message>", r"^<local-command-caveat>",
)


def tokenize(s):
    if not s: return set()
    s = re.sub(r"[^a-z0-9]+", " ", s.lower())
    return {t for t in s.split() if t and len(t) > 2 and t not in STOP}


def is_bot(topic):
    if not topic: return False
    for p in BOT_PREFIXES:
        if re.search(p, topic.strip(), re.I): return True
    return False


def load_workstreams_from_yaml(ws_dir):
    out = {}
    for ws_yaml in sorted(Path(ws_dir).glob("*/state/workstream.yaml")):
        text = ws_yaml.read_text()
        wsid = re.search(r"workstream_id:\s*(\S+)", text)
        title = re.search(r'title:\s*"?(.*?)"?\n', text)
        obj = re.search(r'objective:\s*"?(.*?)"?\n', text)
        if not wsid: continue
        blob = " ".join(filter(None, [
            wsid.group(1), title.group(1) if title else "", obj.group(1) if obj else ""
        ]))
        out[wsid.group(1)] = tokenize(blob) | {wsid.group(1).replace("-", " ")}
    return out


def workstreams_from_coverage(cov):
    out = {}
    for ws in cov.get("workstreams", []):
        wsid = ws.get("id")
        if not wsid: continue
        blob = " ".join(filter(None, [wsid, ws.get("title", ""), ws.get("objective", "")]))
        out[wsid] = tokenize(blob) | {wsid.replace("-", " ")}
    return out


def score_chain(c, ws_corpus):
    text = " ".join(filter(None, [c.get("topic", ""), " ".join(c.get("handoff_refs", []) or [])]))
    tokens = tokenize(text)
    text_low = text.lower()
    scores = []
    for ws, ws_tokens in ws_corpus.items():
        overlap = tokens & ws_tokens
        slug_hit = 2 if (ws in text_low or ws.replace("-", " ") in text_low) else 0
        s = len(overlap) + slug_hit
        for href in (c.get("handoff_refs", []) or []):
            if ws.replace("-", " ") in href.replace("-", " ").lower():
                s += 3
        scores.append((s, ws))
    scores.sort(reverse=True)
    return scores


def hint_from_handoff(c, ws_corpus):
    for href in (c.get("handoff_refs", []) or []):
        for ws in ws_corpus:
            if ws in href.lower():
                return ws
    return None


def classify(chains, ws_corpus, msg_threshold=50):
    big = [c for c in chains if c.get("msgs", c.get("msg_total", 0)) >= msg_threshold and c.get("status") == "orphan"]
    buckets = {"auto_attribute": [], "needs_review": [], "archive": [], "bot_dispatch": []}
    ws_count = {}

    for c in big:
        topic = c.get("topic") or ""
        cid = c.get("id") or c.get("chain_id")
        agent = c.get("agent") or ("codex" if cid.startswith("codex-chain") else "claude_code")
        msgs = c.get("msgs", c.get("msg_total", 0))
        base = {
            "chain_id": cid, "agent": agent, "msgs": msgs,
            "n_sessions": c.get("n_sessions", len(c.get("lineage", []))),
            "topic": topic[:200],
        }
        if is_bot(topic):
            buckets["bot_dispatch"].append({**base, "hint_ws": hint_from_handoff(c, ws_corpus), "reason": "bot/skill dispatch — attribute via invoker"})
            continue
        scored = score_chain(c, ws_corpus)
        if not scored:
            buckets["archive"].append({**base, "reason": "no workstreams loaded"})
            continue
        top = scored[:3]
        best_score, best_ws = top[0]
        if best_score >= 7: bucket = "auto_attribute"
        elif best_score >= 4: bucket = "needs_review"
        else: bucket = "archive"
        buckets[bucket].append({
            **base, "ws": best_ws, "score": best_score,
            "alts": [{"ws": w, "score": s} for s, w in top[1:] if s > 0],
            "reason": f"top match {best_ws} (score {best_score})",
        })
        ws_count[best_ws] = ws_count.get(best_ws, 0) + 1

    return buckets, ws_count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--coverage", help="coverage.json (preferred — uses embedded ws registry)")
    ap.add_argument("--inputs", help="dir with claude.json + codex.json (legacy)")
    ap.add_argument("--workstreams", help="workstream YAML dir (used with --inputs)")
    ap.add_argument("--output", required=True)
    ap.add_argument("--update-coverage", action="store_true",
                    help="if --coverage given, also write classification back into coverage.json chains[].classification")
    args = ap.parse_args()

    if args.coverage:
        cov = json.load(open(args.coverage))
        chains = cov["chains"]
        ws_corpus = workstreams_from_coverage(cov)
    else:
        if not args.inputs or not args.workstreams:
            ap.error("--coverage OR (--inputs + --workstreams) required")
        ws_corpus = load_workstreams_from_yaml(args.workstreams)
        chains = []
        for fname in ("claude.json", "codex.json"):
            p = Path(args.inputs) / fname
            if p.exists():
                d = json.load(open(p))
                # shape inventory chains as classify-ready (has chain_id/topic/handoff_refs/msg_total)
                for c in d["chains"]:
                    chains.append({**c, "id": c["chain_id"], "msgs": c.get("msg_total", 0), "agent": "codex" if c["chain_id"].startswith("codex-chain") else "claude_code"})

    buckets, ws_count = classify(chains, ws_corpus)
    out = {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "workstreams_evaluated": len(ws_corpus),
        "orphans_classified": sum(len(v) for v in buckets.values()),
        "buckets": buckets,
        "summary_by_ws": dict(sorted(ws_count.items(), key=lambda x: -x[1])),
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(args.output, "w"), indent=2, ensure_ascii=False)
    print(f"wrote {args.output}")
    print("buckets:", {k: len(v) for k, v in buckets.items()})

    if args.update_coverage and args.coverage:
        cov = json.load(open(args.coverage))
        # Index classifications by chain_id
        cls_by_id = {}
        for bucket, items in buckets.items():
            for it in items:
                cls_by_id[it["chain_id"]] = {
                    "bucket": bucket, "ws": it.get("ws"), "score": it.get("score"),
                    "alts": it.get("alts", []), "hint_ws": it.get("hint_ws"),
                    "reason": it.get("reason", ""),
                }
        for c in cov["chains"]:
            if c["id"] in cls_by_id:
                c["classification"] = cls_by_id[c["id"]]
        # Recompute auto_attribute total
        cov["meta"]["totals"]["auto_attribute"] = sum(
            1 for c in cov["chains"] if c.get("classification") and c["classification"].get("bucket") == "auto_attribute"
        )
        json.dump(cov, open(args.coverage, "w"), indent=2, ensure_ascii=False)
        print(f"updated {args.coverage} chains[].classification")


if __name__ == "__main__":
    main()
