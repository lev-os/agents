#!/usr/bin/env python3
"""xapi topic search must not end at 0 posts because the whole topic was one exact phrase.

Run: python3 scripts/test_xapi_phrase_fallback.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import x_api

TWEET = {"id": "1850000000000000000", "text": "rogue AI coup talk", "author_id": "1",
         "created_at": "2026-11-10T12:00:00.000Z", "public_metrics": {}}
queries = []


def fake_get(token, url, params, deadline=None):
    queries.append(params["query"])
    if params["query"].startswith('"'):
        return {"data": [], "meta": {}}  # exact phrase: no hits
    return {"data": [TWEET], "includes": {"users": [{"id": "1", "username": "u"}]}, "meta": {}}


x_api._get = fake_get
result = x_api.search_x("tok", "AI coup rogue AI", "2026-10-17", "2026-11-16", depth="quick")
assert queries[0] == '"AI coup rogue AI" -is:retweet', queries
assert len(result["items"]) == 1, (queries, result)
assert queries[-1] == "AI coup rogue AI -is:retweet", queries

# A one-word topic has no looser form: one request only.
queries.clear()
x_api.search_x("tok", "nothinghere", "2026-10-17", "2026-11-16", depth="quick")
assert len(queries) == 1, queries
print("ok")
