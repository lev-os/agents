#!/usr/bin/env python3
"""A query word matches only whole words and real inflections, never a longer word.

Run: python3 scripts/test_relevance_whole_word.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.relevance import token_overlap_relevance as rel

Q = "ai coup"
on_topic = rel(Q, "Inside the AI coup at Nvidia")

# Prefix matches score as if "coup" were absent (only "ai" matched).
ai_only = rel(Q, "AI-created love story")
couple = rel(Q, "AI-created love story", ["AICouple", "AIVideo", "CoupleGoals"])
assert couple <= ai_only, (couple, ai_only)
assert rel(Q, "spin that ai couple like what") == rel(Q, "spin that ai banana like what")
assert rel(Q, "ai coupon codes") == rel(Q, "ai banana codes")
assert couple < on_topic, (couple, on_topic)

# Real inflections still count, in text and in hashtags.
assert rel(Q, "AI coups are coming") > ai_only
assert rel(Q, "the ai couped board") > ai_only
assert rel(Q, "video", ["AICoup"]) > rel(Q, "video", ["AIVideo"])
assert rel(Q, "video", ["AICoups"]) > rel(Q, "video", ["AIVideo"])

# Concatenated query words in a hashtag still split ("claudecode").
assert rel("claude code", "new video", ["claudecode"]) > 0.8

print("ok")
