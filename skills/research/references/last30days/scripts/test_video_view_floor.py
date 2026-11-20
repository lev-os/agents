#!/usr/bin/env python3
"""A 38-view TikTok must not survive the 1000-view floor.

The "Anthropic rogue agents" run ranked first a 38-view TikTok that pastes a
research prompt. The pipeline prunes each source stream on its own, so every
batch held one source and the "sole source" exemption switched the view
floor off for every run.

Run: python3 scripts/test_video_view_floor.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import schema, signals


def tiktok(url, views, rel):
    return schema.SourceItem(
        item_id=url, source="tiktok", title="t", body="", url=url,
        engagement={"views": views, "likes": 2, "shares": 1, "comments": 0},
        local_relevance=rel,
    )


prompt = tiktok("https://www.tiktok.com/@x/video/1", 38, 0.40)
viral = tiktok("https://www.tiktok.com/@y/video/2", 149_643, 0.30)

# 1. One TikTok stream: the low-view item drops when a peer meets the floor.
got = [i.url for i in signals.prune_low_relevance([prompt, viral])]
assert got == [viral.url], got

# 2. No TikTok meets the floor: the stream is kept, never emptied.
quiet = tiktok("https://www.tiktok.com/@z/video/3", 500, 0.30)
got = [i.url for i in signals.prune_low_relevance([prompt, quiet])]
assert got == [prompt.url, quiet.url], got

print("ok")
