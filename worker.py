"""Pulls India's most-popular YouTube videos and stores hashtag counts.
Run every 1-6 hours (cron / systemd timer / GitHub Actions).
Env: YOUTUBE_API_KEY, DATABASE_URL
"""
import os, re, sys
from collections import defaultdict
import requests, psycopg

API_KEY = os.environ["YOUTUBE_API_KEY"]
DSN = os.environ["DATABASE_URL"]
REGION = os.environ.get("REGION", "IN")
# YouTube video category ids; "0" means no category filter.
CATEGORIES = {"0": "all", "10": "music", "17": "sports", "20": "gaming",
              "22": "people", "23": "comedy", "24": "entertainment",
              "25": "news", "26": "style", "28": "tech"}
HASHTAG = re.compile(r"#(\w{2,40})", re.UNICODE)
IGNORE = {"shorts", "short", "youtube", "video", "subscribe", "viral", "trending"}

def fetch(category_id):
    params = {"part": "snippet,statistics", "chart": "mostPopular",
              "regionCode": REGION, "maxResults": 50, "key": API_KEY}
    if category_id != "0":
        params["videoCategoryId"] = category_id
    r = requests.get("https://www.googleapis.com/youtube/v3/videos", params=params, timeout=20)
    if r.status_code != 200:   # some categories are unsupported in some regions
        print(f"skip category {category_id}: HTTP {r.status_code}", file=sys.stderr)
        return []
    return r.json().get("items", [])

def count_tags(items):
    agg = defaultdict(lambda: [0, 0])  # tag -> [mentions, views]
    for it in items:
        text = it["snippet"].get("title", "") + " " + it["snippet"].get("description", "")
        views = int(it.get("statistics", {}).get("viewCount", 0))
        for tag in {t.lower() for t in HASHTAG.findall(text)} - IGNORE:
            agg[tag][0] += 1
            agg[tag][1] += views
    return agg

def main():
    rows = []
    for cid, name in CATEGORIES.items():
        for tag, (m, v) in count_tags(fetch(cid)).items():
            rows.append((tag, "youtube", REGION, name, m, v))
    if not rows:
        sys.exit("no data fetched; check API key, quota and region")
    with psycopg.connect(DSN) as conn, conn.cursor() as cur:
        cur.executemany("""INSERT INTO trend_snapshots
            (tag, source, region, category, mentions, total_views)
            VALUES (%s,%s,%s,%s,%s,%s)""", rows)
        cur.execute("DELETE FROM trend_snapshots WHERE captured_at < now() - interval '30 days'")
    print(f"stored {len(rows)} tag rows")

if __name__ == "__main__":
    main()
