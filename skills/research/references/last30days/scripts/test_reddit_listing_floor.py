#!/usr/bin/env python3
"""A subreddit feed post that never mentions the topic is not Reddit evidence.

The "AI coup" run resolved r/conspiracy and returned its front page (all dated
today, none about the topic), so weekly counts were impossible.

Run: python3 scripts/test_reddit_listing_floor.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import reddit_keyless as rk


def post(url, rel, title):
    return {"url": url, "title": title, "date": "2026-11-16", "relevance": rel,
            "score": 5, "num_comments": 0, "engagement": {"score": 5, "num_comments": 0}, "metadata": {"post_id": url[-3:]}}


feed = [post(f"https://www.reddit.com/r/conspiracy/comments/x{i:02d}/", 0.0, "pterodactyl") for i in range(6)]
search = [post("https://www.reddit.com/r/news/comments/s01/", 0.0, "body-only hit")]
rk._scored_listings = lambda subs, depth="default", query="", sorts=None: [dict(p) for p in feed]
rk.reddit_rss.search_rss = lambda topic, depth="default", subreddits=None: []
rk.reddit_arctic.fetch_scores = lambda ids: {}
rk._enrich = lambda posts, depth: posts

# 1. Only off-topic feed posts -> empty, so the ScrapeCreators backup can run.
assert rk.search_and_enrich("ai coup", "2026-10-17", "2026-11-16", subreddits=["conspiracy"]) == []

# 2. A zero-overlap keyword-search hit still survives the all-zero fallback.
rk.reddit_rss.search_rss = lambda topic, depth="default", subreddits=None: [dict(p) for p in search]
got = rk.search_and_enrich("ai coup", "2026-10-17", "2026-11-16", subreddits=["conspiracy"])
assert [p["url"] for p in got] == [search[0]["url"]], got

# 3. Dedicated (entity-home) subs stay floor-exempt.
got = rk.search_and_enrich("ai coup", "2026-10-17", "2026-11-16", dedicated_subreddits=["conspiracy"])
assert sum(1 for p in got if p.get("dedicated")) == 6, got

print("ok")
