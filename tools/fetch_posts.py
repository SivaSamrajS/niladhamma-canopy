#!/usr/bin/env python3
"""
Pull every post from the Blogger Atom feed, sanitise the body HTML, and mirror
each image into assets/img/pathivu/ so nothing on the rebuilt site depends on
blogger.googleusercontent.com staying up.

    python3 tools/fetch_posts.py

Writes data/posts.json. Images already on disk are skipped, so re-runs are cheap.
"""

import hashlib
import html
import json
import os
import re
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGDIR = os.path.join(ROOT, "assets", "img", "pathivu")
FEED = ("https://www.niladhamma.co.in/feeds/posts/default"
        "?alt=json&max-results=500")
UA = {"User-Agent": "niladhamma-site/1.0 (sam@culturemonkey.io)"}

# Tags we keep in post bodies. Everything else is unwrapped to its text.
ALLOWED = {"p", "br", "b", "strong", "i", "em", "u", "ul", "ol", "li",
           "h2", "h3", "h4", "blockquote", "a", "img", "div", "span",
           "table", "tr", "td", "th", "tbody", "thead"}


def slugify(url, date, seen):
    tail = urllib.parse.unquote(url.rstrip("/").split("/")[-1]).replace(".html", "").strip()
    if re.fullmatch(r"blog-post(_\d+)?", tail) or not tail:
        base = date
    else:
        base = re.sub(r"[^a-z0-9]+", "-", tail.lower()).strip("-")[:60] or date
    s, n = base, 2
    while s in seen:
        s, n = f"{base}-{n}", n + 1
    seen.add(s)
    return s


def local_name(src):
    ext = ".png" if src.lower().split("?")[0].endswith(".png") else ".jpg"
    return "p" + hashlib.sha1(src.encode()).hexdigest()[:14] + ext


def fetch_image(src):
    """Return the site-root path, or None if the image could not be fetched."""
    path = os.path.join(IMGDIR, local_name(src))
    rel = "/assets/img/pathivu/" + local_name(src)
    if os.path.exists(path) and os.path.getsize(path) > 800:
        return src, rel
    # ask Blogger for a large render rather than the thumbnail in the feed
    big = re.sub(r"/(s\d+|w\d+-h\d+)/", "/s1600/", src)
    for cand in (big, src):
        try:
            req = urllib.request.Request(cand, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            if len(data) > 800:
                with open(path, "wb") as f:
                    f.write(data)
                return src, rel
        except Exception:
            continue
    if os.path.exists(path):
        os.remove(path)
    return src, None


def clean_html(body, imgmap):
    b = re.sub(r"<(script|style|iframe|ins)[^>]*>.*?</\1>", "", body, flags=re.S | re.I)
    b = re.sub(r"<(script|style|iframe|ins)[^>]*/?>", "", b, flags=re.I)
    b = re.sub(r"<a[^>]*>(\s*<img[^>]*>)\s*</a>", r"\1", b, flags=re.S | re.I)

    def fiximg(m):
        rel = imgmap.get(m.group(1))
        return f'<img src="{rel}" alt="" loading="lazy">' if rel else ""

    b = re.sub(r'<img[^>]*?src="([^"]+)"[^>]*>', fiximg, b, flags=re.I)
    b = re.sub(r'\s(style|width|height|class|id|border|align|data-[a-z-]+)="[^"]*"',
               "", b, flags=re.I)
    b = re.sub(r"</?([a-z0-9]+)[^>]*>",
               lambda m: m.group(0) if m.group(1).lower() in ALLOWED else "", b, flags=re.I)
    b = re.sub(r"<div[^>]*>", "<div>", b, flags=re.I)
    b = re.sub(r"<div>\s*</div>", "", b)
    b = re.sub(r"(<br\s*/?>\s*){3,}", "<br><br>", b, flags=re.I)
    return re.sub(r"\n{3,}", "\n\n", b).strip()


def main():
    os.makedirs(IMGDIR, exist_ok=True)
    feed = json.load(urllib.request.urlopen(
        urllib.request.Request(FEED, headers=UA)))["feed"]
    entries = feed["entry"]

    every = []
    for e in entries:
        every += re.findall(r'<img[^>]+src="([^"]+)"', e.get("content", {}).get("$t", ""))
    every = sorted(set(every))
    print(f"{len(entries)} posts, {len(every)} distinct images")

    with ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(fetch_image, every))
    imgmap = {s: rel for s, rel in results if rel}
    print(f"mirrored {len(imgmap)} / {len(every)} "
          f"({len(every) - len(imgmap)} no longer resolve upstream)")

    posts, seen = [], set()
    for e in entries:
        url = [l["href"] for l in e["link"] if l["rel"] == "alternate"][0]
        date = e["published"]["$t"][:10]
        raw = e.get("content", {}).get("$t", "")
        body = clean_html(raw, imgmap)
        plain = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))).strip()
        mine = [imgmap[s] for s in dict.fromkeys(re.findall(r'<img[^>]+src="([^"]+)"', raw))
                if s in imgmap]
        posts.append({
            "slug": slugify(url, date, seen),
            "title": e["title"]["$t"].strip(),
            "date": date,
            "origin": url,
            "labels": [t["term"] for t in e.get("category", [])],
            "html": body,
            "text": plain,
            "imgs": mine,
        })

    with open(os.path.join(ROOT, "data", "posts.json"), "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=1)

    noimg = [p["slug"] for p in posts if not p["imgs"]]
    print(f"wrote data/posts.json · {len(posts)} posts · "
          f"{sum(len(p['imgs']) for p in posts)} image refs")
    print(f"posts with no usable image: {len(noimg)}")


if __name__ == "__main__":
    main()
