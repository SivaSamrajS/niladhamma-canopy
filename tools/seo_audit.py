#!/usr/bin/env python3
"""
Full SEO and technical audit of the built site.

    python3 tools/seo_audit.py

Exits non-zero if anything at ERROR level is found, so it can gate a deploy.
WARN items are judgement calls worth reading, not necessarily faults.
"""

import collections
import glob
import html
import json
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.niladhamma.co.in"
os.chdir(ROOT)

errors, warns, notes = [], [], []


def err(page, msg):
    errors.append((page, msg))


def warn(page, msg):
    warns.append((page, msg))


def note(msg):
    notes.append(msg)


# ---------------------------------------------------------------- load pages
pages = sorted(p for p in glob.glob("**/*.html", recursive=True)
               if not p.startswith(("node_modules", "assets")))
doc = {}
for p in pages:
    doc[p] = open(p, encoding="utf-8").read()


def one(pattern, s, group=1):
    m = re.search(pattern, s, re.S | re.I)
    return m.group(group) if m else None


def page_url(p):
    """Canonical site URL a file is served at. Directory indexes use the
    trailing-slash form, matching what build.py emits."""
    path = "/" + p.replace(os.sep, "/")
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    return path or "/"


def canonical_of(p):
    return one(r'<link rel="canonical" href="([^"]+)"', doc[p])


# =========================================================== 1. titles
titles = collections.defaultdict(list)
def lang_of(p):
    return "en" if p.startswith("en/") else "ta"


for p in pages:
    t = one(r"<title>(.*?)</title>", doc[p])
    if not t:
        err(p, "no <title>")
        continue
    t = html.unescape(t).strip()
    titles[(lang_of(p), t)].append(p)
    if len(t) > 70:
        warn(p, f"title {len(t)} chars (over 70): {t[:60]}...")
    if len(t) < 15:
        warn(p, f"title only {len(t)} chars: {t}")
for (lg, t), ps in titles.items():
    if len(ps) > 1:
        err(ps[0], f"duplicate title in {lg} across {len(ps)} pages: {t[:60]}")

# =========================================================== 2. descriptions
descs = collections.defaultdict(list)
for p in pages:
    d = one(r'<meta name="description" content="([^"]*)"', doc[p])
    if d is None:
        err(p, "no meta description")
        continue
    d = html.unescape(d).strip()
    descs[(lang_of(p), d)].append(p)
    if not d:
        err(p, "empty meta description")
    elif len(d) > 170:
        warn(p, f"description {len(d)} chars (over 170)")
    elif len(d) < 70:
        warn(p, f"description only {len(d)} chars")
for (lg, d), ps in descs.items():
    if len(ps) > 1:
        err(ps[0], f"duplicate description in {lg} across {len(ps)} pages")

# =========================================================== 3. canonicals
for p in pages:
    canon = canonical_of(p)
    if not canon:
        err(p, "no canonical")
        continue
    if not canon.startswith("https://"):
        err(p, f"canonical not absolute https: {canon}")
    want = BASE + page_url(p)
    if canon != want:
        err(p, f"canonical {canon} does not match {want}")

# =========================================================== 4. hreflang
alts = {}
for p in pages:
    found = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', doc[p])
    alts[p] = dict(found)
    if not found:
        if "/404" not in p:
            err(p, "no hreflang alternates")
        continue
    codes = [c for c, _ in found]
    if "x-default" not in codes:
        err(p, "no x-default hreflang")
    for c in ("ta", "en"):
        if c not in codes:
            err(p, f"missing hreflang={c}")
    if len(codes) != len(set(codes)):
        err(p, f"duplicate hreflang codes: {codes}")

# reciprocity: if A says B is its English alternate, B must say A is its Tamil one
def local(url):
    return urllib.parse.urlparse(url).path


for p in pages:
    if not alts.get(p):
        continue
    self_lang = "en" if p.startswith("en/") else "ta"
    other = "ta" if self_lang == "en" else "en"
    target = local(alts[p].get(other, ""))
    tfile = target.lstrip("/")
    tfile = tfile + "index.html" if tfile.endswith("/") or tfile == "" else tfile
    if tfile not in doc:
        err(p, f"hreflang={other} points at a page that does not exist: {target}")
        continue
    back = local(alts.get(tfile, {}).get(self_lang, ""))
    mine = local(alts[p].get(self_lang, ""))
    if back != mine:
        err(p, f"hreflang not reciprocal: {tfile} points back to {back}, expected {mine}")
    # self-reference required
    if local(alts[p].get(self_lang, "")) != page_url(p):
        warn(p, f"hreflang={self_lang} does not self-reference ({alts[p].get(self_lang)})")

# =========================================================== 5. robots / index
noindex = set()
for p in pages:
    r = one(r'<meta name="robots" content="([^"]*)"', doc[p]) or ""
    if "noindex" in r:
        noindex.add(p)
    elif "index" not in r:
        warn(p, "no robots meta")

# =========================================================== 6. headings
for p in pages:
    h1 = re.findall(r"<h1[ >]", doc[p])
    if len(h1) != 1:
        err(p, f"{len(h1)} h1 tags (want exactly 1)")
    levels = [int(x) for x in re.findall(r"<h([1-6])[ >]", doc[p])]
    prev = levels[0] if levels else 0
    for lv in levels[1:]:
        if lv > prev + 1:
            err(p, f"heading level skips h{prev} to h{lv}")
            break
        prev = lv

# =========================================================== 7. images
for p in pages:
    for tag in re.findall(r"<img\b[^>]*>", doc[p]):
        if "alt=" not in tag:
            err(p, f"img without alt: {tag[:70]}")
        src = one(r'src="([^"]+)"', tag)
        if src and src.startswith("/") and not os.path.exists(src.split("?")[0].lstrip("/")):
            err(p, f"img src missing on disk: {src}")
        if src and src.startswith("http://"):
            err(p, f"insecure img src: {src}")

# =========================================================== 8. links
linked = set()
for p in pages:
    hrefs = re.findall(r'href="([^"]+)"', doc[p])
    internal = 0
    for h in hrefs:
        if h.startswith("http://"):
            err(p, f"insecure http link: {h}")
        if not h.startswith("/"):
            continue
        internal += 1
        target = h.split("#")[0].split("?")[0].lstrip("/")
        if target.endswith("/") or target == "":
            target += "index.html"
        if target.endswith(".html"):
            if target not in doc:
                err(p, f"broken internal link: {h}")
            else:
                linked.add(target)
        elif not os.path.exists(target):
            err(p, f"broken asset link: {h}")
    if internal < 5 and p not in noindex:
        warn(p, f"only {internal} internal links")

orphans = [p for p in pages if p not in linked and p not in noindex
           and p not in ("index.html", "en/index.html")]
for p in orphans:
    err(p, "orphan: not linked from any page")

# =========================================================== 9. structured data
ld_types = collections.Counter()
ids = set()
refs = set()
for p in pages:
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc[p], re.S)
    if not blocks and p not in noindex:
        warn(p, "no structured data")
    for b in blocks:
        try:
            data = json.loads(b)
        except Exception as e:
            err(p, f"JSON-LD does not parse: {e}")
            continue
        ld_types[data.get("@type")] += 1
        def walk(node):
            if isinstance(node, dict):
                # an @id alongside a @type is a definition; alone it is a reference
                if "@id" in node:
                    (ids if "@type" in node else refs).add(node["@id"])
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)
        walk(data)
        if data.get("@type") == "Article":
            for f in ("headline", "url", "author", "publisher", "inLanguage"):
                if f not in data:
                    err(p, f"Article JSON-LD missing {f}")
        if data.get("@type") == "BreadcrumbList":
            items = data.get("itemListElement", [])
            if len(items) < 2:
                warn(p, "BreadcrumbList with fewer than 2 items")
        if data.get("@type") == "FAQPage":
            for q in data.get("mainEntity", []):
                if not q.get("acceptedAnswer", {}).get("text"):
                    err(p, "FAQPage question with no answer text")

dangling = {r for r in refs if r.startswith(BASE) and r not in ids}
for d in sorted(dangling):
    warn("(schema)", f"@id referenced but never defined: {d}")

# =========================================================== 10. social cards
for p in pages:
    for prop, kind in (("og:title", "property"), ("og:description", "property"),
                       ("og:url", "property"), ("og:image", "property"),
                       ("twitter:card", "name"), ("twitter:image", "name")):
        if f'{kind}="{prop}"' not in doc[p]:
            err(p, f"missing {prop}")
    ogimg = one(r'<meta property="og:image" content="([^"]+)"', doc[p])
    if ogimg:
        if not ogimg.startswith("https://"):
            err(p, f"og:image not absolute: {ogimg}")
        else:
            rel = ogimg[len(BASE):].lstrip("/")
            if not os.path.exists(rel):
                err(p, f"og:image missing on disk: {ogimg}")

# =========================================================== 11. lang
for p in pages:
    lang = one(r'<html lang="([^"]+)"', doc[p])
    want = "en" if p.startswith("en/") else "ta"
    if lang != want:
        err(p, f'html lang="{lang}", expected "{want}"')

# =========================================================== 12. sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
try:
    tree = ET.fromstring(sm)
except Exception as e:
    err("sitemap.xml", f"does not parse: {e}")
    tree = None

if tree is not None:
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    locs = [el.text for el in tree.iter(ns + "loc")]
    if len(locs) != len(set(locs)):
        err("sitemap.xml", "contains duplicate URLs")
    sm_paths = {urllib.parse.urlparse(l).path for l in locs}
    file_paths = set()
    for p in pages:
        if p in noindex:
            continue
        path = page_url(p)
        file_paths.add(path)
    missing = file_paths - sm_paths
    extra = sm_paths - file_paths
    for m in sorted(missing):
        err("sitemap.xml", f"indexable page not listed: {m}")
    for m in sorted(extra):
        err("sitemap.xml", f"lists a URL with no page: {m}")
    for p in noindex:
        if page_url(p) in sm_paths:
            err("sitemap.xml", f"lists a noindex page: {page_url(p)}")
    for l in locs:
        if not l.startswith(BASE):
            err("sitemap.xml", f"URL not on the canonical origin: {l}")
    note(f"sitemap lists {len(locs)} URLs")

# =========================================================== 13. robots.txt
rb = open("robots.txt", encoding="utf-8").read()
if "Sitemap:" not in rb:
    err("robots.txt", "no Sitemap directive")
if f"{BASE}/sitemap.xml" not in rb:
    err("robots.txt", "Sitemap directive does not point at the canonical sitemap")
if re.search(r"^Disallow: /\s*$", rb, re.M):
    err("robots.txt", "disallows the whole site")

# =========================================================== 14. per-language parity
ta_pages = {p for p in pages if not p.startswith("en/")}
en_pages = {p[3:] for p in pages if p.startswith("en/")}
only_ta = ta_pages - en_pages
only_en = en_pages - ta_pages
for p in sorted(only_ta):
    err(p, "no English counterpart")
for p in sorted(only_en):
    err("en/" + p, "no Tamil counterpart")

# ================================================ 15. translation completeness
untranslated = []
for p in pages:
    if not p.startswith("en/"):
        continue
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", doc[p], flags=re.S)
    text = re.sub(r"<[^>]+>", " ", body)
    tamil = len(re.findall(r"[\u0b80-\u0bff]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    if tamil > 200 and tamil > latin:
        untranslated.append(p)
if untranslated:
    note(f"{len(untranslated)} English pages still carry mostly Tamil body text")
    for p in untranslated[:3]:
        warn(p, "English page body is not translated")
    if len(untranslated) > 3:
        warn("(en)", f"... and {len(untranslated) - 3} more untranslated English pages")


# =========================================================== 16. misc
for p in pages:
    if "<html" in doc[p] and 'name="viewport"' not in doc[p]:
        err(p, "no viewport meta")
    if re.search(r"—", doc[p]):
        warn(p, "contains an em-dash")
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", doc[p], flags=re.S)
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    if words < 120 and p not in noindex:
        warn(p, f"thin content: about {words} words")

# =========================================================== report
print("=" * 72)
print(f"SEO AUDIT · {len(pages)} pages "
      f"({len(ta_pages)} ta + {len(en_pages)} en) · origin {BASE}")
print("=" * 72)
for n in notes:
    print(f"  note   {n}")
print(f"  schema types: {dict(ld_types.most_common())}")
print(f"  noindex pages: {sorted(noindex) or 'none'}")
print()

if errors:
    print(f"ERRORS ({len(errors)})")
    grouped = collections.defaultdict(list)
    for p, m in errors:
        grouped[m.split(":")[0]].append((p, m))
    for kind, items in sorted(grouped.items(), key=lambda x: -len(x[1])):
        print(f"  [{len(items):3d}] {kind}")
        for p, m in items[:4]:
            print(f"        {p}  ::  {m}")
        if len(items) > 4:
            print(f"        ... and {len(items) - 4} more")
else:
    print("ERRORS (0)  none")
print()

if warns:
    print(f"WARNINGS ({len(warns)})")
    grouped = collections.defaultdict(list)
    for p, m in warns:
        grouped[m.split(":")[0].split("(")[0].strip()].append((p, m))
    for kind, items in sorted(grouped.items(), key=lambda x: -len(x[1])):
        print(f"  [{len(items):3d}] {kind}")
        for p, m in items[:3]:
            print(f"        {p}  ::  {m}")
        if len(items) > 3:
            print(f"        ... and {len(items) - 3} more")
else:
    print("WARNINGS (0)  none")

print()
print(f"RESULT: {len(errors)} errors, {len(warns)} warnings")
sys.exit(1 if errors else 0)
