#!/usr/bin/env python3
"""
Niladhamma monthly report.

Builds reports/<month>-{ta,en}.html, and those render to PDF with:

    python3 -m http.server 8347
    "Google Chrome" --headless --no-pdf-header-footer \\
        --print-to-pdf=reports/july-2026-ta.pdf \\
        http://localhost:8347/reports/july-2026-ta.html

Everything that the site already knows is read from data/, never retyped: the
story titles, the full moon date and time, and for any event that was written
up on the site, its photographs and the address of the post. An event only
needs hand-entering where the archive has no record of it.

Canopy rules as elsewhere: no em-dash, semantic tokens only, border-first
elevation, Tamil authoritative with English beside it.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

SITE = "https://www.niladhamma.co.in"
MONTH = {"slug": "july-2026", "ta": "ஜூலை 2026", "en": "July 2026", "n": 7,
         "year": 2026}

# --------------------------------------------------------------------------
# The month's events.
#
# "posts" names the archive entries that recorded the event. The generator
# pulls the photographs and the link from those, so nothing here duplicates
# what the site already holds. "photos" is only for pictures that never went
# onto the site.
# --------------------------------------------------------------------------
EVENTS = [
    {
        "date": "2026-07-05",
        "ta": "சமத்துவத் தலைவர் ஆம்ஸ்ட்ராங் இரண்டாம் ஆண்டு நினைவேந்தல்",
        "en": "Second year memorial for Armstrong, the Equality Leader",
        "kind": {"ta": "நினைவேந்தல்", "en": "Memorial"},
        "posts": ["2026-07-06-3", "2026-07-06", "2026-07-06-2"],
        "body": {
            "ta": [
                "சமத்துவத் தலைவரின் இரண்டாம் ஆண்டு நினைவேந்தல் நிகழ்வில் "
                "நிலாதம்மா குழு கலை நிகழ்ச்சிகளை வழங்கியது. குழந்தைகளும் "
                "இளையோரும் சேர்ந்து இரண்டு நாடகங்களும் இரண்டு பாட்டுகளும் "
                "மேடையேற்றினர்.",
                "மேடையில் நிகழ்ச்சி நிகழ்த்தியதற்காக நிலாதம்மா குழுவிற்குத் "
                "திருமதி பொற்கொடி ஆம்ஸ்ட்ராங் அண்ணி நினைவுப் பரிசு "
                "வழங்கினார். நினைவிடத்தில் குழு புகைப்படமும் "
                "எடுக்கப்பட்டது.",
                "நாடகமும் பாட்டும் நிலாதம்மாவின் நிலையான வேலைமுறை. "
                "கலைகளைச் சமத்துவக் கருவியாக்கி இயங்குவது என்பது "
                "சங்கம் தொடக்கத்திலிருந்தே செய்துவரும் ஒன்று; இந்த "
                "நிகழ்வும் அதன் ஒரு பகுதியே.",
            ],
            "en": [
                "The Niladhamma group gave the arts programme at the second "
                "year memorial for the Equality Leader. The children and the "
                "young people together staged two dramas and two songs.",
                "Mrs Porkodi Armstrong presented the group with a memento for "
                "the performance, and a group photograph was taken at the "
                "memorial site.",
                "Drama and song are how this sangha works. Making the arts an "
                "instrument of equality is something it has done from the "
                "beginning, and this programme was part of that.",
            ],
        },
        "programme": [
            {"ta": "பாபாசாகிப்பின் பன்முகத் தன்மைகள்",
             "en": "The many sides of Babasaheb",
             "form": {"ta": "நாடகம்", "en": "Drama"}},
            {"ta": "ஆம்ஸ்ட்ராங் மாமா", "en": "Armstrong Maama",
             "form": {"ta": "நாடகம்", "en": "Drama"}},
            {"ta": "எல்லாமே எங்கள் மாமா தான்",
             "en": "Everything is our Maama",
             "form": {"ta": "பாட்டு", "en": "Song"}},
            {"ta": "உழைக்கும் மக்கள் தலைவன் யார்",
             "en": "Who is the leader of the working people",
             "form": {"ta": "பாட்டு", "en": "Song"}},
        ],
    },
    {
        "date": "2026-07-12",
        "ta": "பாரதி பிரபு நாடகப் பயிற்சி",
        "en": "Drama training with Bharathi Prabu",
        "kind": {"ta": "பயிற்சி", "en": "Training"},
        "body": {
            "ta": [
                "பாரதி பிரபு அவர்கள் நிலாதம்மாக் குழுவினருக்கு நாடகப் "
                "பயிற்சி வழங்கினார்.",
                "நினைவேந்தல் மேடையில் ஏறிய அதே குழந்தைகளுக்கும் "
                "இளையோருக்கும் இது தொடர்ச்சியான பயிற்சி. நிகழ்ச்சிக்கு "
                "ஒரு முறை ஒத்திகை பார்ப்பதோடு நிற்காமல், நடிப்பையும் "
                "மேடை நடத்தையையும் தொடர்ந்து கற்பது என்பது சங்கத்தின் "
                "வழக்கம்.",
            ],
            "en": [
                "Bharathi Prabu led a drama training session for the "
                "Niladhamma group.",
                "This is continuing work with the same children and young "
                "people who went on stage at the memorial. The sangha's "
                "practice is not to rehearse once for a programme but to keep "
                "learning performance and stagecraft between them.",
            ],
        },
    },
    {
        "date": "2026-07-19",
        "ta": "அருட்தந்தை ஜான் சுரேஷ் நிகழ்வு",
        "en": "Programme for Father John Suresh",
        "kind": {"ta": "நிகழ்வு", "en": "Programme"},
        "body": {
            "ta": ["சிறுசேரி மகிழ்ச்சி இல்லத்தில் நடைபெற்ற நிகழ்வு. "
                   "நிலாதம்மாக் குழுவினர் அனைவரும் கலந்துகொண்டனர்.",
                   "இம்மாதத்தில் தளத்தில் பதிவாகாத ஒரே நிகழ்வு இதுவே."],
            "en": ["A programme held at Magizhchi Illam in Siruseri. Every "
                   "member of the Niladhamma group took part.",
                   "This is the one event of the month that was not written up "
                   "on the site."],
        },
    },
    {
        "date": "2026-07-22",
        "ta": "நீட் எதிர்ப்புப் போராட்டம்",
        "en": "Anti-NEET protest",
        "kind": {"ta": "போராட்டம்", "en": "Protest"},
        "body": {
            "ta": [
                "நீலம் மாணவர் இயக்கம் (NSM) நடத்திய நீட் எதிர்ப்புப் "
                "போராட்டத்தில் நிலாதம்மாக் குழு உறுப்பினர்கள் தாரகையும் "
                "சிவ சம்ராஜும் கலந்துகொண்டனர்.",
                "தேர்வுத் தாள் கசிவு, நீட் தேர்வை ரத்து செய்யக் கோரும் "
                "கோரிக்கை, சிறைப்படுத்தப்பட்ட மாணவர்களுக்கு ஆதரவு "
                "ஆகியவை போராட்டத்தில் முன்வைக்கப்பட்டன.",
                "கல்வி வாய்ப்பு என்பது சமத்துவப் பிரச்சினை. நுழைவுத் "
                "தேர்வு எந்த மாணவரைத் தடுக்கிறது என்பதைக் கேட்பது "
                "அம்பேத்கரிய வேலையின் நேரடித் தொடர்ச்சி; அதனால்தான் "
                "இது சங்கத்தின் மாதாந்திரப் பதிவில் இடம்பெறுகிறது.",
            ],
            "en": [
                "Niladhamma group members Tharagai and Siva Samraj took part "
                "in the anti-NEET protest held by the Neelam Students "
                "Movement (NSM).",
                "The examination paper leak, the demand that NEET be scrapped, "
                "and support for the students who had been detained were what "
                "the evening put forward.",
                "Access to education is a question of equality. Asking which "
                "students an entrance examination keeps out is a direct "
                "continuation of Ambedkarite work, and that is why it belongs "
                "in the sangha's record of the month.",
            ],
        },
        "people": [
            {"ta": "தாரகை", "en": "Tharagai"},
            {"ta": "சிவ சம்ராஜ்", "en": "Siva Samraj"},
        ],
        "photos": [
            {"src": "img/neet-speech.jpg", "w": 1050, "h": 1400,
             "ta": "நீலம் மாணவர் இயக்கப் போராட்ட மேடையில் உரை",
             "en": "Addressing the Neelam Students Movement protest"},
            {"src": "img/neet-placard.jpg", "w": 1050, "h": 1400,
             "ta": "&ldquo;காகிதக் கசிவு. நீட்டை இப்போதே ரத்து செய்&rdquo;",
             "en": "&ldquo;Paper leak. Ban NEET now&rdquo;"},
            {"src": "img/neet-crowd.jpg", "w": 1050, "h": 1400,
             "ta": "போராட்டத் திடலில் ஊடகங்களுக்கு அளிக்கப்பட்ட பேட்டி",
             "en": "Speaking to the media at the protest ground"},
        ],
    },
    {
        "date": "2026-07-29",
        "ta": "ஆடிப் பௌர்ணமி அழைப்பு",
        "en": "The Aadi full moon invitation",
        "kind": {"ta": "அழைப்பு", "en": "Invitation"},
        "posts": ["2026-07-29"],
        "body": {
            "ta": [
                "பௌர்ணமி பௌத்த மரபில் உபோசத நாள்; விழிப்புக்கும் "
                "தியானத்துக்கும் உரிய நாள்.",
                "ஆடி மாத முழுநிலவுக்குத் தனிச் சிறப்பு உண்டு. புத்தர் "
                "சாரநாத்தில் தம் முதல் உபதேசத்தை நிகழ்த்தி தம்மச் "
                "சக்கரத்தை உருட்டிய நாள், சங்கம் பிறந்த நாள் என்று "
                "மரபு அதனை இணைக்கிறது.",
                "அதே கதைதான் இம்மாதத் தொகுப்பின் ஆறாம் நாள் கதையாகவும் "
                "வெளியானது; அதை அழைப்புப் பதிவே ஒரு அழகான தற்செயல் "
                "என்று குறிப்பிடுகிறது.",
            ],
            "en": [
                "A full moon day is an uposatha day in the Buddhist "
                "tradition, a day given to wakefulness and to meditation.",
                "The Aadi full moon carries a particular weight. Tradition "
                "ties it to the day the Buddha gave his first discourse at "
                "Sarnath and set the wheel of the Dhamma turning, and to the "
                "day the Sangha came into being.",
                "That same story went out as day six of this month's "
                "collection, a coincidence the invitation itself stops to "
                "notice.",
            ],
        },
    },
    {
        "date": "2026-07-30",
        "ta": "பௌர்ணமி விழா",
        "en": "The full moon gathering",
        "kind": {"ta": "கூட்டம்", "en": "Gathering"},
        "posts": ["2026-07-30"],
        "body": {
            "ta": [
                "அசோக் நகர் புத்த விஹாரில் நடைபெற்ற பௌர்ணமி விழா. "
                "2012 முதல் ஒவ்வொரு பௌர்ணமியிலும் குடும்பமாகக் கூடும் "
                "வழக்கத்தின் தொடர்ச்சி.",
                "வந்தனை, திரிசரணம், பஞ்சசீலம், தியானம், தம்மக் கதை, "
                "தானம் என்று கூட்டம் அமைதியாக நடக்கிறது. குழந்தைகள் "
                "முதல் பெரியவர்கள் வரை அனைவரும் கலந்துகொண்டனர்.",
            ],
            "en": [
                "The full moon gathering at Ashok Nagar Buddha Vihar, "
                "continuing the practice of meeting as families on every full "
                "moon day since 2012.",
                "Homage, the three refuges, the five precepts, meditation, a "
                "Dhamma story and dana: the evening runs quietly through "
                "them. Everyone from the children to the elders took part.",
            ],
        },
    },
]

UI = {
    "title":      {"ta": "மாதாந்திர அறிக்கை", "en": "Monthly report"},
    "org":        {"ta": "நிலாதம்மா", "en": "Niladhamma"},
    "sub":        {"ta": "அசோக் நகர் புத்த விஹார், சென்னை",
                   "en": "Ashok Nagar Buddha Vihar, Chennai"},
    "stat_days":  {"ta": "நாள், {n} கதைகள்", "en": "days, {n} stories"},
    "stat_events":{"ta": "நிகழ்வுகள்", "en": "events"},
    "stat_photos":{"ta": "படங்கள் பதிவு செய்யப்பட்டன",
                   "en": "photographs recorded"},
    "events_h":   {"ta": "நிகழ்வுகள்", "en": "Events"},
    "programme":  {"ta": "நிகழ்ச்சி நிரல்", "en": "Programme"},
    "took_part":  {"ta": "கலந்துகொண்டோர்", "en": "Took part"},
    "recorded":   {"ta": "தளத்தில் பதிவு", "en": "Recorded on the site"},
    "stories_h":  {"ta": "தம்மபதம்: முப்பத்தோர் நாள்",
                   "en": "Dhammapada: Thirty-one Days"},
    "stories_sub":{"ta": "ஜூலை 1 முதல் 31 வரை, ஒவ்வொரு நாளும் ஒரு "
                         "பௌத்தக் கதை. முப்பத்தொன்றும் வெளியிடப்பட்டன.",
                   "en": "One Buddhist story for each day from 1 to 31 July. "
                         "All thirty one were published."},
    "moon_note":  {"ta": "ஜூலை மாதப் பௌர்ணமி {d}, இரவு {t} மணிக்கு.",
                   "en": "July's full moon fell on {d} at {t}."},
    "pending":    {"ta": "உறுதி செய்யப்பட வேண்டியது",
                   "en": "To be confirmed"},
    "footer":     {"ta": "இவ்வறிக்கை நிலாதம்மா தளத்தின் தரவிலிருந்து "
                         "உருவாக்கப்பட்டது. கதைத் தலைப்புகளும் "
                         "பௌர்ணமி நேரமும் நிகழ்வுப் படங்களும் "
                         "தளத்தில் வெளியானவையே.",
                   "en": "This report is generated from the Niladhamma site "
                         "data. The story titles, the full moon time and the "
                         "event photographs are the ones the site published."},
}

TA_MONTHS = ["ஜனவரி", "பிப்ரவரி", "மார்ச்", "ஏப்ரல்", "மே", "ஜூன்", "ஜூலை",
             "ஆகஸ்ட்", "செப்டம்பர்", "அக்டோபர்", "நவம்பர்", "டிசம்பர்"]
EN_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]

STRIP = re.compile(r"<[^>]+>")


def U(key, L, **fmt):
    s = UI[key][L]
    return s.format(**fmt) if fmt else s


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as fh:
        return json.load(fh)


POSTS = {p["slug"]: p for p in load("posts.json")}
POSTS_EN = {p["slug"]: p for p in load("posts_en.json")}
SIZES = load("img_sizes.json")


def fmt_date(iso, L):
    y, m, d = (int(x) for x in iso.split("-"))
    return (f"{d} {TA_MONTHS[m - 1]} {y}" if L == "ta"
            else f"{d} {EN_MONTHS[m - 1]} {y}")


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def stories(L):
    """(day, title) for all 31. Read from the data the site publishes, so the
    report cannot disagree with what actually went out."""
    ta = {s["day"]: s["title"] for s in load("stories_july.json")["stories"]}
    if L == "ta":
        return sorted(ta.items())
    en = load("stories_en.json")["stories"]
    return sorted((d, en.get(str(d), {}).get("title", t)) for d, t in ta.items())


def july_moon():
    for m in load("moons.json")["moons"]:
        if m["date"].startswith(f"{MONTH['year']}-{MONTH['n']:02d}"):
            return m
    return None


def post_title(slug, L):
    if L == "en" and POSTS_EN.get(slug, {}).get("title_en"):
        return POSTS_EN[slug]["title_en"]
    return POSTS[slug]["title"].strip()


def event_photos(ev, limit=3):
    """Photographs for an event: the ones its archive posts carry, else the
    ones supplied by hand. Tiles rather than originals, because a report is
    read at a fraction of the size a viewer opens."""
    if ev.get("photos"):
        return [dict(p, src=p["src"]) for p in ev["photos"][:limit]]
    out = []
    for slug in ev.get("posts", []):
        for src in POSTS[slug]["imgs"]:
            w, h = SIZES.get(src, [4, 3])
            tile = src.replace("/pathivu/", "/pathivu/tile/")
            out.append({"src": tile, "w": w, "h": h, "ta": "", "en": ""})
            if len(out) >= limit:
                return out
    return out


def event_block(ev, L):
    pending = ("" if not ev.get("pending") else
               f'<span class="rp-pending">{U("pending", L)}</span>')
    body = "".join(f"<p>{p}</p>" for p in ev["body"][L])

    extra = ""
    if ev.get("programme"):
        items = "".join(f'<li><span>{i[L]}</span><em>{i["form"][L]}</em></li>'
                        for i in ev["programme"])
        extra += (f'<p class="rp-label">{U("programme", L)}</p>'
                  f'<ol class="rp-prog">{items}</ol>')
    if ev.get("people"):
        names = ", ".join(p[L] for p in ev["people"])
        extra += (f'<p class="rp-meta"><strong>{U("took_part", L)}:</strong> '
                  f"{names}</p>")
    if ev.get("posts"):
        links = ", ".join(
            f'<a href="{SITE}{"" if L == "ta" else "/en"}/pathivu/{s}.html">'
            f"{esc(post_title(s, L))}</a>" for s in ev["posts"])
        extra += (f'<p class="rp-meta"><strong>{U("recorded", L)}:</strong> '
                  f"{links}</p>")

    shots = event_photos(ev)
    gallery = ""
    if shots:
        cells = "".join(
            f'<figure class="rp-shot"><img src="{s["src"]}" width="{s["w"]}" '
            f'height="{s["h"]}" alt="{s.get(L, "")}" loading="lazy">'
            + (f'<figcaption>{s[L]}</figcaption>' if s.get(L) else "")
            + "</figure>" for s in shots)
        gallery = f'<div class="rp-shots">{cells}</div>'

    return (
        f'<article class="rp-ev">'
        f'  <div class="rp-ev__when">'
        f'    <span class="rp-ev__day">{int(ev["date"].split("-")[2])}</span>'
        f'    <span class="rp-ev__kind">{ev["kind"][L]}</span>'
        f"  </div>"
        f'  <div class="rp-ev__body">'
        f"    <h3>{ev[L]}{pending}</h3>"
        f'    <p class="rp-ev__date">{fmt_date(ev["date"], L)}</p>'
        f"    {body}{extra}{gallery}"
        f"  </div>"
        f"</article>"
    )


def build(L):
    st = stories(L)
    moon = july_moon()
    shot_count = sum(len(POSTS[s]["imgs"]) for e in EVENTS
                     for s in e.get("posts", [])) + sum(
        len(e.get("photos", [])) for e in EVENTS)

    # One table, two stories per row, rather than two tables side by side.
    # Side by side they broke at different points and stranded a row of each
    # on a page of its own; paired in a single row they break as a unit.
    half = (len(st) + 1) // 2
    rows = ""
    for i in range(half):
        d, t = st[i]
        rows += f'<tr><td class="rp-d">{d}</td><td>{esc(t)}</td>'
        if i + half < len(st):
            d2, t2 = st[i + half]
            rows += f'<td class="rp-d rp-d--2">{d2}</td><td>{esc(t2)}</td>'
        else:
            rows += '<td colspan="2"></td>'
        rows += "</tr>"

    moon_line = ""
    if moon:
        moon_line = (f'<p class="rp-sub">'
                     f'{U("moon_note", L, d=moon[f"label_{L}"], t=moon["time_ist"])}'
                     f"</p>")

    return f"""<!doctype html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{U("org", L)} · {MONTH[L]} {U("title", L)}</title>
<link rel="stylesheet" href="/assets/css/canopy.css">
<link rel="stylesheet" href="/assets/css/nila.css">
<style>
  /* Report layer. Reads Canopy semantic tokens like the rest of the site;
     nothing here defines a colour of its own. */
  body {{ background: var(--nd-field); }}
  .rp {{ max-width: 900px; margin: 0 auto; padding: 40px 28px 64px; }}
  .rp__head {{ padding-bottom: 22px; border-bottom: 2px solid var(--cm-green-700); }}
  .rp__org {{ font-size: 12px; font-weight: 700; letter-spacing: 0.08em;
              text-transform: uppercase; color: var(--cm-text-accent); margin: 0; }}
  .rp__org:lang(ta) {{ text-transform: none; letter-spacing: 0.02em; }}
  .rp__h1 {{ font-size: 34px; line-height: 1.2; letter-spacing: -0.02em; margin: 10px 0 6px; }}
  .rp__sub {{ margin: 0; font-size: 14.5px; color: var(--cm-text-muted); }}

  .rp-stats {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
               gap: 14px; margin: 26px 0 0; }}
  .rp-stat {{ background: var(--nd-surface); border: 1px solid var(--cm-border-default);
              border-radius: var(--cm-radius-lg); padding: 16px 18px; }}
  .rp-stat b {{ display: block; font-size: 27px; line-height: 1.1;
                color: var(--cm-text-primary); }}
  .rp-stat span {{ display: block; margin-top: 5px; font-size: 13px;
                   line-height: 1.5; color: var(--cm-text-muted); }}

  .rp-sec {{ margin-top: 40px; }}
  .rp-sec > h2 {{ font-size: 20px; padding-bottom: 10px; margin-bottom: 4px;
                  border-bottom: 2px solid var(--cm-border-default); }}
  .rp-sub {{ margin: 10px 0 0; font-size: 14.5px; color: var(--cm-text-muted); }}

  /* Events: the date is a rail on the left, so a reader scanning the month
     sees the sequence before they read any of it. */
  .rp-ev {{ display: grid; grid-template-columns: 74px minmax(0, 1fr); gap: 20px;
            padding: 24px 0; border-bottom: 1px solid var(--cm-border-default); }}
  .rp-ev:last-child {{ border-bottom: none; }}
  .rp-ev__when {{ text-align: center; }}
  .rp-ev__day {{ display: block; font-size: 30px; font-weight: 700;
                 line-height: 1; color: var(--cm-green-800, #2f6b45);
                 font-variant-numeric: tabular-nums; }}
  .rp-ev__kind {{ display: block; margin-top: 6px; font-size: 11px; font-weight: 600;
                  color: var(--cm-text-muted); }}
  .rp-ev__body h3 {{ font-size: 17.5px; line-height: 1.35; margin: 0; }}
  .rp-ev__date {{ margin: 5px 0 12px !important; font-size: 13px;
                  color: var(--cm-text-muted); }}
  .rp-ev__body p {{ font-size: 15px; line-height: 1.78; margin: 0 0 11px;
                    color: var(--cm-text-body); max-width: 62ch; }}
  .rp-pending {{ display: inline-block; margin-inline-start: 9px; padding: 2px 9px;
                 font-size: 11px; font-weight: 600; vertical-align: middle;
                 color: var(--cm-text-body); background: var(--cm-bg-well);
                 border: 1px solid var(--cm-border-strong);
                 border-radius: var(--cm-radius-sm); }}
  .rp-label {{ font-size: 11px !important; font-weight: 700; letter-spacing: 0.06em;
               color: var(--cm-text-muted); margin: 16px 0 7px !important; }}
  .rp-prog {{ margin: 0 0 4px; padding-left: 20px; }}
  .rp-prog li {{ font-size: 15px; line-height: 1.7; margin-bottom: 5px; }}
  .rp-prog em {{ font-style: normal; margin-inline-start: 8px; font-size: 12px;
                 color: var(--cm-text-muted); }}
  .rp-meta {{ font-size: 14px !important; color: var(--cm-text-muted) !important; }}
  .rp-meta strong {{ color: var(--cm-text-body); }}
  .rp-meta a {{ color: var(--cm-text-accent); }}

  .rp-shots {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
               gap: 12px; margin-top: 14px; }}
  .rp-shot {{ margin: 0; }}
  .rp-shot img {{ width: 100%; height: auto; aspect-ratio: 4 / 3; object-fit: cover;
                  border-radius: var(--cm-radius-md, 8px);
                  border: 1px solid var(--cm-border-default); }}
  .rp-shot figcaption {{ margin-top: 7px; font-size: 12px; line-height: 1.5;
                         color: var(--cm-text-muted); }}

  .rp-tbl {{ width: 100%; border-collapse: collapse; margin-top: 18px;
             table-layout: fixed; }}
  .rp-tbl td {{ padding: 7px 0; font-size: 14.5px; line-height: 1.5;
                border-bottom: 1px solid var(--cm-neutral-100, #eef2ef);
                vertical-align: top; }}
  .rp-d {{ width: 30px; color: var(--cm-green-700); font-weight: 700;
           font-variant-numeric: tabular-nums; }}
  /* The right-hand pair needs a gutter, or the two columns read as one run. */
  .rp-tbl--pairs td:nth-child(2) {{ padding-right: 30px; }}
  .rp-d--2 {{ padding-left: 4px; }}
  @media (max-width: 700px) {{
    .rp-tbl--pairs, .rp-tbl--pairs tbody, .rp-tbl--pairs tr {{ display: block; }}
    .rp-tbl--pairs td {{ display: inline-block; border-bottom: none; }}
    .rp-tbl--pairs td:nth-child(2) {{ width: calc(100% - 40px); padding-right: 0; }}
    .rp-tbl--pairs td:nth-child(4) {{ width: calc(100% - 40px); }}
  }}

  .rp__foot {{ margin-top: 44px; padding-top: 16px;
               border-top: 1px solid var(--cm-border-default);
               font-size: 12.5px; line-height: 1.6; color: var(--cm-text-muted); }}

  @media (max-width: 700px) {{
    .rp-stats {{ grid-template-columns: minmax(0, 1fr); }}
    .rp-ev {{ grid-template-columns: 56px minmax(0, 1fr); gap: 14px; }}
  }}

  @media print {{
    @page {{ margin: 14mm 12mm; }}
    body {{ background: #ffffff !important; }}
    .rp {{ max-width: none; padding: 0; }}
    .rp-sec {{ margin-top: 26px; }}
    .rp-ev {{ padding: 18px 0; }}

    /* Hold together the things that lose their meaning when split: a heading
       from the text under it, a photograph from its caption, a numbered
       programme. A long event is allowed to run across a page break, because
       forbidding that left half of page one blank while the event waited for
       room it did not need. */
    .rp-sec > h2, .rp-ev__body h3, .rp-ev__date {{ break-after: avoid-page; }}
    .rp-shots, .rp-prog, .rp-shot, .rp-stat, .rp-tbl tr {{ break-inside: avoid-page; }}
    .rp-ev__body p {{ orphans: 2; widows: 2; }}
    .rp-meta a {{ color: inherit; text-decoration: none; }}

    .rp-shots {{ margin-top: 10px; }}
    /* Tightened just enough that the thirty one titles finish on the page
       they start on rather than spilling two rows onto one of their own. */
    .rp-tbl td {{ padding: 5px 0; }}
    .rp__foot {{ margin-top: 14px; padding-top: 10px; break-before: avoid-page; }}
    .rp-sec {{ margin-top: 20px; }}
    .rp-sub {{ margin-top: 8px; }}
  }}
</style>
</head>
<body class="cm-root">
<main class="rp">
  <header class="rp__head">
    <p class="rp__org" lang="{L}">{U("org", L)}</p>
    <h1 class="rp__h1">{MONTH[L]} {U("title", L)}</h1>
    <p class="rp__sub">{U("sub", L)}</p>
  </header>

  <section class="rp-stats">
    <div class="rp-stat"><b>31</b><span>{U("stat_days", L, n=len(st))}</span></div>
    <div class="rp-stat"><b>{len(EVENTS)}</b><span>{U("stat_events", L)}</span></div>
    <div class="rp-stat"><b>{shot_count}</b><span>{U("stat_photos", L)}</span></div>
  </section>

  <section class="rp-sec">
    <h2>{U("events_h", L)}</h2>
    {"".join(event_block(e, L) for e in EVENTS)}
  </section>

  <section class="rp-sec rp-sec--stories">
    <h2>{U("stories_h", L)}</h2>
    <p class="rp-sub">{U("stories_sub", L)}</p>
    {moon_line}
    <table class="rp-tbl rp-tbl--pairs"><tbody>{rows}</tbody></table>
  </section>

  <p class="rp__foot">{U("footer", L)}</p>
</main>
</body>
</html>
"""


def main():
    out = os.path.join(ROOT, "reports")
    os.makedirs(out, exist_ok=True)
    for L in ("ta", "en"):
        path = os.path.join(out, f"{MONTH['slug']}-{L}.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(build(L))
        print(f"  wrote reports/{MONTH['slug']}-{L}.html")
    linked = sum(len(e.get("posts", [])) for e in EVENTS)
    print(f"Done. {len(EVENTS)} events ({linked} drawn from the archive), "
          f"{len(stories('ta'))} stories.")


if __name__ == "__main__":
    main()
