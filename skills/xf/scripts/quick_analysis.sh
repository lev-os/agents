#!/bin/bash
#
# Quick Analysis — One-command X archive overview using xf
#
# Usage:
#     ./quick_analysis.sh
#
# Output:
#     - Archive health
#     - Content counts by type
#     - Top hashtags
#     - Engagement summary
#     - Recent activity
#
# Requires: xf, jq

set -e

echo "=============================================="
echo "XF QUICK ANALYSIS"
echo "=============================================="
echo ""

# 1. Health check
echo "--- Health Check ---"
if xf doctor 2>/dev/null; then
    echo "Status: OK"
else
    echo "Status: Issues detected (run 'xf doctor' for details)"
fi
echo ""

# 2. Archive overview
echo "--- Archive Overview ---"
xf stats --format json 2>/dev/null | jq '{
    tweets: .tweets,
    likes: .likes,
    dms: .dms,
    grok_messages: .grok_messages,
    followers: .followers,
    following: .following
}' 2>/dev/null || echo "Could not get stats"
echo ""

# 3. Temporal range
echo "--- Activity Range ---"
xf stats --temporal --format json 2>/dev/null | jq '.temporal | {
    first_tweet: .first_tweet,
    last_tweet: .last_tweet,
    active_days: .active_days,
    longest_gap_days: .longest_gap_days
}' 2>/dev/null || echo "Could not get temporal stats"
echo ""

# 4. Top hashtags
echo "--- Top 10 Hashtags ---"
xf export tweets --format json 2>/dev/null \
    | jq -r '.[].text' \
    | grep -oE '#\w+' \
    | sort | uniq -c | sort -rn | head -10 \
    || echo "Could not extract hashtags"
echo ""

# 5. Engagement summary
echo "--- Engagement Summary ---"
xf export tweets --format json 2>/dev/null | jq '{
    total_tweets: length,
    total_likes_received: (map(.favorite_count // 0) | add),
    total_retweets: (map(.retweet_count // 0) | add),
    avg_likes: (map(.favorite_count // 0) | add / length | floor),
    top_tweet_likes: (sort_by(-.favorite_count) | .[0].favorite_count)
}' 2>/dev/null || echo "Could not calculate engagement"
echo ""

# 6. Recent activity (last 7 days of tweeting)
echo "--- Recent Tweet Activity (by month) ---"
xf export tweets --format json 2>/dev/null \
    | jq -r '.[].created_at[:7]' \
    | sort | uniq -c | tail -7 \
    || echo "Could not get activity"
echo ""

# 7. Content type breakdown
echo "--- DM Conversations ---"
DM_COUNT=$(xf stats --format json 2>/dev/null | jq '.dms // 0')
echo "Total DM messages: $DM_COUNT"
if [ "$DM_COUNT" -gt 0 ]; then
    CONV_COUNT=$(xf list conversations --format json 2>/dev/null | jq 'length' 2>/dev/null || echo "?")
    echo "Unique conversations: $CONV_COUNT"
fi
echo ""

# 8. Grok usage
echo "--- Grok AI Usage ---"
GROK_COUNT=$(xf stats --format json 2>/dev/null | jq '.grok_messages // 0')
echo "Total Grok messages: $GROK_COUNT"
if [ "$GROK_COUNT" -gt 0 ]; then
    CHAT_COUNT=$(xf search "" --types grok --format json --limit 10000 2>/dev/null \
        | jq 'group_by(.metadata.chat_id) | length' 2>/dev/null || echo "?")
    echo "Unique Grok chats: $CHAT_COUNT"
fi
echo ""

# 9. Quick tips
echo "--- Next Steps ---"
echo "1. Search tweets:     xf search \"KEYWORD\" --types tweet --format json"
echo "2. Search DMs:        xf search \"KEYWORD\" --types dm --context --format json"
echo "3. Search Grok:       xf search \"KEYWORD\" --types grok --format json"
echo "4. Top tweets:        xf search \"\" --types tweet --sort engagement --limit 10 --format json"
echo "5. Topic deep dive:   ./scripts/topic_miner.py \"TOPIC\""
echo ""
echo "=============================================="
