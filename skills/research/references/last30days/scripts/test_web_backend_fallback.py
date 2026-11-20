#!/usr/bin/env python3
"""A rejected web key must not end web search, and unsearched sources must not read as failures.

Run: python3 scripts/test_web_backend_fallback.py
"""
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import grounding, http, quality_nudge

DR = ("2026-10-17", "2026-11-16")
calls = []


def bad_key(name):
    def fn(query, date_range, key):
        calls.append(name)
        raise http.HTTPError("HTTP 422: Unprocessable Entity", status_code=422,
                             body='{"error":{"detail":"The provided API key is invalid."}}')
    return fn


def good(name):
    def fn(query, date_range, key):
        calls.append(name)
        return [{"id": "W1", "url": "https://example.com", "title": "t"}], {"label": name}
    return fn


grounding._enrich_reddit_items = lambda items: items
grounding.brave_search = bad_key("brave")
grounding.exa_search = good("exa")

# 1. Brave key rejected -> auto falls back to the next keyed backend (Exa).
items, artifact = grounding.web_search("q", DR, {"BRAVE_API_KEY": "x", "EXA_API_KEY": "y"})
assert calls == ["brave", "exa"], calls
assert len(items) == 1 and artifact["label"] == "exa", (items, artifact)

# 1b. The rejected key is remembered for the rest of the process.
calls.clear()
grounding.web_search("q", DR, {"BRAVE_API_KEY": "x", "EXA_API_KEY": "y"})
assert calls == ["exa"], calls

# 2. Every keyed backend rejects -> raise an error that names the key problem.
calls.clear()
grounding.exa_search = bad_key("exa")
try:
    grounding.web_search("q", DR, {"BRAVE_API_KEY": "x", "EXA_API_KEY": "y", "LAST30DAYS_NATIVE_SEARCH": "1"})
except RuntimeError as exc:
    msg = str(exc)
    assert "BRAVE_API_KEY" in msg and "EXA_API_KEY" in msg and "rejected" in msg, msg
else:
    raise AssertionError("expected a key error")

grounding._REJECTED_BACKENDS.clear()

# 3. An explicit backend does not fall back (user pinned it).
calls.clear()
try:
    grounding.web_search("q", DR, {"BRAVE_API_KEY": "x", "EXA_API_KEY": "y"}, backend="brave")
except http.HTTPError:
    pass
assert calls == ["brave"], calls

# 4. Instagram not in the plan -> not a "silent" failure.
cfg = {"SCRAPECREATORS_API_KEY": "k"}
assert not quality_nudge._is_instagram_silent_failure(
    cfg, {"instagram_items_count": 0, "planned_sources": ["reddit", "hackernews"]})
assert quality_nudge._is_instagram_silent_failure(
    cfg, {"instagram_items_count": 0, "planned_sources": ["instagram"]})

# 5. YouTube transcripts skipped by design (limit 0) -> not degraded.
assert not quality_nudge._is_youtube_degraded(
    {"youtube_videos_count": 6, "youtube_transcripts_count": 0, "youtube_transcript_limit": 0}, 0.5)
assert quality_nudge._is_youtube_degraded(
    {"youtube_videos_count": 6, "youtube_transcripts_count": 0, "youtube_transcript_limit": 2}, 0.5)

# 6. The completion line lists only planned, returning or failing sources.
import last30days
shown = {}
progress = SimpleNamespace(end_processing=lambda: None, show_promo=lambda *a, **k: None,
                           show_complete=lambda **kw: shown.update(kw))
report = SimpleNamespace(
    query_plan=SimpleNamespace(source_weights={"reddit": 1.0, "x": 1.0, "youtube": 1.0},
                               subqueries=[SimpleNamespace(sources=["reddit", "hackernews"])]),
    items_by_source={"reddit": [1], "youtube": [], "tiktok": [], "hackernews": [1]},
    errors_by_source={"grounding": "HTTP 422"},
)
last30days._show_runtime_ui(report, progress, {"available_sources": ["reddit", "hackernews", "youtube", "tiktok"]})
assert set(shown["display_sources"]) == {"reddit", "hackernews", "grounding"}, shown["display_sources"]
assert "youtube" not in shown["source_counts"], shown["source_counts"]
print("ok")
