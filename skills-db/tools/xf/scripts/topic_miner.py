#!/usr/bin/env python3
"""
Topic Miner — Deep dive analysis of a topic across your X archive.

Usage:
    ./topic_miner.py "machine learning"
    ./topic_miner.py "rust" --since "2024-01"
    ./topic_miner.py "distributed systems" --output report.json

Output:
    - Tweet count and engagement
    - Liked content on topic
    - DM mentions
    - Grok conversations
    - Related hashtags
    - Timeline

Requires: xf, jq
"""

import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime


def run_xf(args: list[str]) -> dict | list | None:
    """Run xf command and return parsed JSON."""
    try:
        result = subprocess.run(
            ["xf"] + args,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout) if result.stdout.strip() else None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None


def search(query: str, types: str = None, limit: int = 100, since: str = None) -> list:
    """Search X archive."""
    args = ["search", query, "--format", "json", "--limit", str(limit)]
    if types:
        args.extend(["--types", types])
    if since:
        args.extend(["--since", since])
    result = run_xf(args)
    return result if isinstance(result, list) else []


def extract_hashtags(results: list) -> Counter:
    """Extract hashtags from results."""
    hashtags = Counter()
    for r in results:
        text = r.get("text", "")
        for word in text.split():
            if word.startswith("#"):
                tag = word.lower().strip("#.,!?")
                if tag:
                    hashtags[tag] += 1
    return hashtags


def extract_mentions(results: list) -> Counter:
    """Extract @mentions from results."""
    mentions = Counter()
    for r in results:
        text = r.get("text", "")
        for word in text.split():
            if word.startswith("@"):
                mention = word.lower().strip("@.,!?")
                if mention:
                    mentions[mention] += 1
    return mentions


def analyze_engagement(tweets: list) -> dict:
    """Analyze tweet engagement."""
    if not tweets:
        return {"count": 0}

    likes = []
    rts = []
    for t in tweets:
        meta = t.get("metadata", {})
        likes.append(meta.get("favorite_count", 0) or 0)
        rts.append(meta.get("retweet_count", 0) or 0)

    return {
        "count": len(tweets),
        "total_likes": sum(likes),
        "total_retweets": sum(rts),
        "avg_likes": round(sum(likes) / len(tweets), 1) if tweets else 0,
        "max_likes": max(likes) if likes else 0,
        "top_tweets": sorted(
            [{"text": t["text"][:100], "likes": t.get("metadata", {}).get("favorite_count", 0)}
             for t in tweets],
            key=lambda x: x["likes"],
            reverse=True
        )[:5]
    }


def analyze_timeline(results: list) -> dict:
    """Analyze timeline distribution."""
    months = Counter()
    years = Counter()

    for r in results:
        created = r.get("created_at", "")
        if len(created) >= 7:
            months[created[:7]] += 1
        if len(created) >= 4:
            years[created[:4]] += 1

    return {
        "by_month": dict(sorted(months.items())),
        "by_year": dict(sorted(years.items()))
    }


def mine_topic(topic: str, since: str = None) -> dict:
    """Comprehensive topic mining."""
    print(f"Mining topic: {topic}")
    print("-" * 50)

    report = {
        "topic": topic,
        "generated_at": datetime.now().isoformat(),
        "since": since,
    }

    # 1. Your tweets
    print("Searching tweets...")
    tweets = search(topic, types="tweet", limit=500, since=since)
    report["tweets"] = analyze_engagement(tweets)
    print(f"  Found {len(tweets)} tweets")

    # 2. Liked content
    print("Searching likes...")
    likes = search(topic, types="like", limit=500, since=since)
    report["likes"] = {
        "count": len(likes),
        "samples": [l["text"][:100] for l in likes[:5]]
    }
    print(f"  Found {len(likes)} liked tweets")

    # 3. DM mentions
    print("Searching DMs...")
    dms = search(topic, types="dm", limit=200, since=since)
    conv_ids = set(d.get("metadata", {}).get("conversation_id", "") for d in dms)
    report["dms"] = {
        "message_count": len(dms),
        "conversation_count": len(conv_ids - {""})
    }
    print(f"  Found {len(dms)} DM messages in {len(conv_ids)} conversations")

    # 4. Grok conversations
    print("Searching Grok...")
    grok = search(topic, types="grok", limit=200, since=since)
    chat_ids = set(g.get("metadata", {}).get("chat_id", "") for g in grok)
    user_msgs = [g for g in grok if g.get("metadata", {}).get("sender") == "user"]
    report["grok"] = {
        "message_count": len(grok),
        "chat_count": len(chat_ids - {""}),
        "user_questions": len(user_msgs),
        "sample_questions": [g["text"][:100] for g in user_msgs[:5]]
    }
    print(f"  Found {len(grok)} Grok messages in {len(chat_ids)} chats")

    # 5. Related hashtags (from tweets)
    print("Extracting hashtags...")
    hashtags = extract_hashtags(tweets)
    # Remove the search term itself if it's a hashtag
    topic_tag = topic.lower().strip("#")
    if topic_tag in hashtags:
        del hashtags[topic_tag]
    report["related_hashtags"] = dict(hashtags.most_common(20))
    print(f"  Found {len(hashtags)} unique hashtags")

    # 6. Related mentions
    print("Extracting mentions...")
    mentions = extract_mentions(tweets)
    report["related_mentions"] = dict(mentions.most_common(10))
    print(f"  Found {len(mentions)} unique mentions")

    # 7. Timeline
    print("Analyzing timeline...")
    all_results = tweets + likes + dms + grok
    report["timeline"] = analyze_timeline(all_results)

    print("-" * 50)
    return report


def print_report(report: dict):
    """Print human-readable report."""
    print("\n" + "=" * 60)
    print(f"TOPIC REPORT: {report['topic']}")
    print("=" * 60)

    # Tweets
    tweets = report.get("tweets", {})
    print(f"\n📝 YOUR TWEETS: {tweets.get('count', 0)}")
    if tweets.get("count", 0) > 0:
        print(f"   Total likes: {tweets.get('total_likes', 0)}")
        print(f"   Avg likes: {tweets.get('avg_likes', 0)}")
        print(f"   Top tweet: {tweets.get('max_likes', 0)} likes")
        if tweets.get("top_tweets"):
            print("   Top content:")
            for i, t in enumerate(tweets["top_tweets"][:3], 1):
                print(f"     {i}. [{t['likes']} ❤️] {t['text'][:60]}...")

    # Likes
    likes = report.get("likes", {})
    print(f"\n❤️ LIKED CONTENT: {likes.get('count', 0)}")
    if likes.get("samples"):
        print("   Samples:")
        for sample in likes["samples"][:3]:
            print(f"     - {sample[:60]}...")

    # DMs
    dms = report.get("dms", {})
    print(f"\n💬 DM DISCUSSIONS: {dms.get('message_count', 0)} messages in {dms.get('conversation_count', 0)} conversations")

    # Grok
    grok = report.get("grok", {})
    print(f"\n🤖 GROK Q&A: {grok.get('message_count', 0)} messages in {grok.get('chat_count', 0)} chats")
    if grok.get("sample_questions"):
        print("   Your questions:")
        for q in grok["sample_questions"][:3]:
            print(f"     - {q[:60]}...")

    # Hashtags
    hashtags = report.get("related_hashtags", {})
    if hashtags:
        print("\n#️⃣ RELATED HASHTAGS:")
        for tag, count in list(hashtags.items())[:10]:
            print(f"   #{tag}: {count}")

    # Timeline
    timeline = report.get("timeline", {})
    by_year = timeline.get("by_year", {})
    if by_year:
        print("\n📅 ACTIVITY BY YEAR:")
        for year, count in sorted(by_year.items()):
            print(f"   {year}: {count}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Deep dive analysis of a topic across your X archive."
    )
    parser.add_argument("topic", help="Topic to mine")
    parser.add_argument("--since", help="Filter from date (e.g., '2024-01', 'last month')")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--json", action="store_true", help="Output JSON only")

    args = parser.parse_args()

    # Check xf is available
    try:
        subprocess.run(["xf", "doctor"], capture_output=True, timeout=5)
    except FileNotFoundError:
        print("Error: 'xf' command not found. Please install xf first.", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: xf health check timed out.", file=sys.stderr)
        sys.exit(1)

    # Mine the topic
    report = mine_topic(args.topic, since=args.since)

    # Output
    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to: {args.output}")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
