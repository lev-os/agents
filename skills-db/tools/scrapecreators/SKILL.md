---
name: scrapecreators
description: "Unified social media API — 27+ platforms via single key. Reddit, Twitter/X, TikTok, Instagram, YouTube, LinkedIn, Facebook, Threads, Bluesky, Truth Social. No rate limits."
skill_type: tool
category: process-research-social
metadata:
  openclaw:
    emoji: "🕷️"
    requires:
      env:
        - SCRAPECREATORS_API_KEY
    homepage: https://docs.scrapecreators.com
    tags: [social-media, reddit, twitter, tiktok, instagram, youtube, linkedin, osint, scraping, api]
---

# ScrapeCreators — Unified Social Media API

27+ platforms. Single API key. No rate limits. ~$0.001/request at scale.

## Authentication

```bash
# Header for all requests
x-api-key: $SCRAPECREATORS_API_KEY
```

Base URL: `https://api.scrapecreators.com`

## Key Endpoints

### Reddit
```bash
# Global search
curl -s "https://api.scrapecreators.com/v1/reddit/search?query=TOPIC&sort=relevance&timeframe=month" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"

# Subreddit search
curl -s "https://api.scrapecreators.com/v1/reddit/subreddit/search?subreddit=SUBREDDIT&query=TOPIC&sort=relevance&timeframe=month" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"

# Post comments
curl -s "https://api.scrapecreators.com/v1/reddit/post/comments?url=REDDIT_URL" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"

# Subreddit details
curl -s "https://api.scrapecreators.com/v1/reddit/subreddit/details?subreddit=NAME" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

### Twitter/X
```bash
# Search tweets
curl -s "https://api.scrapecreators.com/v1/twitter/search/tweets?query=TOPIC&sort_by=relevance" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"

# User tweets
curl -s "https://api.scrapecreators.com/v1/twitter/user-tweets?username=HANDLE" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"

# Tweet details
curl -s "https://api.scrapecreators.com/v1/twitter/tweet?tweet_id=ID" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"

# Profile
curl -s "https://api.scrapecreators.com/v1/twitter/profile?username=HANDLE" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

### YouTube
```bash
# Search
curl -s "https://api.scrapecreators.com/v1/youtube/search?query=TOPIC" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"

# Video transcript
curl -s "https://api.scrapecreators.com/v1/youtube/video/transcript?video_id=ID" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"

# Video comments
curl -s "https://api.scrapecreators.com/v1/youtube/video/comments?video_id=ID" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

### TikTok
```bash
# Keyword search
curl -s "https://api.scrapecreators.com/v1/tiktok/search/keyword?query=TOPIC&sort_by=relevance" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"

# Video transcript
curl -s "https://api.scrapecreators.com/v1/tiktok/video/transcript?video_id=ID" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

### Instagram
```bash
# Reels search
curl -s "https://api.scrapecreators.com/v2/instagram/reels/search?query=TOPIC" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"

# Post comments
curl -s "https://api.scrapecreators.com/v2/instagram/post/comments?shortcode=CODE" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

### LinkedIn
```bash
# Profile
curl -s "https://api.scrapecreators.com/v1/linkedin/profile?url=LINKEDIN_URL" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"

# Company posts
curl -s "https://api.scrapecreators.com/v1/linkedin/company/posts?url=COMPANY_URL" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

## Platform Coverage

| Platform | Search | Profiles | Content | Comments | Transcripts |
|----------|--------|----------|---------|----------|-------------|
| Reddit | Global + subreddit | — | Posts | Comments | — |
| Twitter/X | Tweets | Profiles | Tweets, threads | — | Video transcripts |
| YouTube | Search + hashtag | Channels | Videos | Comments | Transcripts |
| TikTok | Keyword, hashtag, top | Profiles | Videos | Comments | Transcripts |
| Instagram | Reels | Profiles | Posts, reels | Comments | Transcripts |
| LinkedIn | — | Profiles, companies | Posts | — | — |
| Facebook | — | — | Ad library | — | — |
| Threads | — | Profiles | Posts | — | — |
| Bluesky | — | Profiles | Posts | — | — |
| Truth Social | — | Profiles | Posts | — | — |

## Pricing

1 request = 1 credit. Credits never expire.

| Tier | Price | Credits | $/1k requests |
|------|-------|---------|---------------|
| Free Trial | $0 | 100 | — |
| Freelance | $47 | 25,000 | $1.88 |
| Business | $497 | 500,000 | $0.99 |

## Advantages Over Alternatives

- **No rate limits** — unlimited concurrent requests
- **Single key** — covers all 27+ platforms
- **Solves Firecrawl's Reddit block** — ScrapeCreators has full Reddit API access
- **Transcript extraction** — video transcripts across TikTok, Instagram, YouTube, Twitter
- **Comment threads** — full comment trees for Reddit and YouTube

## Related

- `lev-social` — uses Bird CLI + PostCrawl; ScrapeCreators covers both
- `lev-research` — route through timetravel's ScrapeCreators adapter
- `last30days` — uses ScrapeCreators as its primary backend
