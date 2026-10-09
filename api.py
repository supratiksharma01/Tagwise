"""Tagwise API.
  GET  /v1/trending?region=IN&category=all&limit=30
  POST /v1/generate   {"caption": "...", "count": 5|10}
Env: DATABASE_URL, ANTHROPIC_API_KEY, ALLOWED_ORIGIN (your site, e.g. https://tagwise.vercel.app),
     optional MODEL (default claude-sonnet-5-5), RATE_LIMIT_PER_HOUR (default 10)
"""
import os, json, re, time
from collections import defaultdict
import psycopg
from anthropic import Anthropic
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DSN = os.environ["DATABASE_URL"]
MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
LIMIT = int(os.environ.get("RATE_LIMIT_PER_HOUR", "10"))
client = Anthropic()  # reads ANTHROPIC_API_KEY

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=[os.environ.get("ALLOWED_ORIGIN", "*")],
                   allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

WINDOW = """SELECT tag, SUM(mentions), SUM(total_views) FROM trend_snapshots
            WHERE region=%s AND category=%s
              AND captured_at > now() - interval '{lo}' AND captured_at <= now() - interval '{hi}'
            GROUP BY tag"""

def trending_rows(region="IN", category="all"):
    with psycopg.connect(DSN) as conn, conn.cursor() as cur:
        cur.execute(WINDOW.format(lo="24 hours", hi="0 hours"), (region, category))
        now = {t: (int(m), int(v)) for t, m, v in cur.fetchall()}
        cur.execute(WINDOW.format(lo="48 hours", hi="24 hours"), (region, category))
        prev = {t: int(m) for t, m, _ in cur.fetchall()}
    out = [{"tag": "#" + t, "mentions": m, "views": v,
            "momentum": round((m - prev.get(t, 0)) / max(prev.get(t, 0), 1), 2),
            "new": t not in prev} for t, (m, v) in now.items()]
    out.sort(key=lambda x: (x["mentions"], x["views"]), reverse=True)
    return out

@app.get("/v1/trending")
def trending(region: str = "IN", category: str = "all", limit: int = 30):
    return {"region": region, "category": category, "source": "youtube",
            "items": trending_rows(region, category)[:limit]}

hits = defaultdict(list)
def check_rate(request: Request):
    ip = (request.headers.get("x-forwarded-for") or request.client.host).split(",")[0].strip()
    now = time.time()
    hits[ip] = [t for t in hits[ip] if now - t < 3600]
    if len(hits[ip]) >= LIMIT:
        raise HTTPException(429, "Hourly limit reached. Try again later.")
    hits[ip].append(now)

class GenReq(BaseModel):
    caption: str = Field(min_length=3, max_length=2000)
    count: int = Field(default=5, ge=3, le=10)

@app.post("/v1/generate")
def generate(req: GenReq, request: Request):
    check_rate(request)
    trend = trending_rows()[:60]
    known = {t["tag"].lower(): t for t in trend}
    prompt = f"""You help Indian social media creators pick hashtags.
Caption: \"\"\"{req.caption}\"\"\"
Tags trending now on YouTube India (tag, trending videos using it): {json.dumps([[t['tag'], t['mentions']] for t in trend])}
Return ONLY a JSON array of {req.count + 5} objects, best first, no markdown. Each:
{{"tag":"#x","tier":"mega|mid|niche","why":"max 12 words"}}.
Rules: the first {req.count} must mix reach tiers (at most 1 mega, 2 mid, rest niche) and describe the post precisely, not generic reach tags.
Use a trending tag only when it truly fits the post. Other tags may be new: lowercase, no spaces. If the caption uses Hindi, Bengali or Hinglish, include 1-2 matching tags in that style. Never state post counts."""
    try:
        msg = client.messages.create(model=MODEL, max_tokens=1200,
                                     messages=[{"role": "user", "content": prompt}])
        text = re.sub(r"```json|```", "", msg.content[0].text).strip()
        arr = json.loads(text)
    except Exception as e:
        raise HTTPException(502, f"AI request failed: {type(e).__name__}")
    items = []
    for a in arr[: req.count + 5]:
        tag = str(a.get("tag", "")).lower()
        if not tag.startswith("#"):
            tag = "#" + tag
        k = known.get(tag)
        items.append({"tag": tag, "tier": a.get("tier") if a.get("tier") in ("mega", "mid", "niche") else "niche",
                      "why": a.get("why", ""), "trending": bool(k), "mentions": k["mentions"] if k else None})
    return {"items": items, "count": req.count, "trend_data": bool(trend)}
