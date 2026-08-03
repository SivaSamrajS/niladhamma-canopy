#!/usr/bin/env python3
"""
Niladhamma monthly report.

Builds reports/<month>-<year>-{ta,en}.html from the story data plus the event
log below, and those render to PDF with:

    python3 -m http.server 8347
    "Google Chrome" --headless --no-pdf-header-footer \\
        --print-to-pdf=reports/july-2026-ta.pdf \\
        http://localhost:8347/reports/july-2026-ta.html

The story list is read from data/, never retyped, so the report cannot drift
from what the site published. Events are the part a person has to supply.

Canopy rules as elsewhere: no em-dash, semantic tokens only, border-first
elevation, Tamil authoritative with English beside it.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

MONTH = {"slug": "july-2026", "ta": "ஜூலை 2026", "en": "July 2026"}

# --------------------------------------------------------------------------
# The month's events. Everything else in this report is derived from data/.
# --------------------------------------------------------------------------
EVENTS = [
    {
        "date": "2026-07-05",
        "ta": "ஆம்ஸ்ட்ராங் மாமா நினைவு நிகழ்வு",
        "en": "Armstrong Anna memorial programme",
        "kind": {"ta": "நினைவு நிகழ்வு", "en": "Memorial"},
        "note": {
            "ta": "ஆம்ஸ்ட்ராங் மாமாவின் நினைவாக நடத்தப்பட்ட நிகழ்வு. "
                  "குழந்தைகளும் இளையோரும் நாடகமும் பாட்டுமாக நான்கு "
                  "நிகழ்ச்சிகளை வழங்கினர்.",
            "en": "A programme held in memory of Armstrong Anna. The children "
                  "and young people gave four items, two dramas and two songs.",
        },
        "programme": [
            {"ta": "பாபாசாகிப்பின் பன்முகத் தன்மைகள்",
             "en": "The many sides of Babasaheb",
             "form": {"ta": "நாடகம்", "en": "Drama"}},
            {"ta": "ஆம்ஸ்ட்ராங் மாமா", "en": "Armstrong Anna",
             "form": {"ta": "நாடகம்", "en": "Drama"}},
            {"ta": "எல்லாமே எங்கள் மாமா தான்",
             "en": "Everything is our Anna",
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
        "note": {
            "ta": "பாரதி பிரபு அவர்கள் வழங்கிய நாடகப் பயிற்சி.",
            "en": "A drama training session led by Bharathi Prabu.",
        },
    },
    {
        "date": "2026-07-19",
        "ta": "தந்தை",
        "en": "Father",
        "kind": {"ta": "நிகழ்வு", "en": "Programme"},
        "pending": True,
        "note": {
            "ta": "நிகழ்வின் முழுத் தலைப்பும் விவரமும் உறுதி செய்யப்பட "
                  "வேண்டியுள்ளது.",
            "en": "The full title and description of this programme are still "
                  "to be confirmed.",
        },
    },
    {
        "date": "2026-07-22",
        "ta": "நீட் எதிர்ப்புப் போராட்டம்",
        "en": "Anti-NEET protest",
        "kind": {"ta": "போராட்டம்", "en": "Protest"},
        "note": {
            "ta": "நீலம் மாணவர் இயக்கம் (NSM) நடத்திய நீட் எதிர்ப்புப் "
                  "போராட்டத்தில் நிலாதம்மா குழு உறுப்பினர்கள் தாரகையும் "
                  "சிவ சம்ராஜும் கலந்துகொண்டனர். காகிதக் கசிவு, மாணவர் "
                  "உயிரிழப்புகள், நீட் தேர்வை ரத்து செய்யக் கோரும் "
                  "கோரிக்கை ஆகியவை முன்வைக்கப்பட்டன.",
            "en": "Niladhamma group members Tharagai and Siva Samraj took part "
                  "in the anti-NEET protest held by the Neelam Students "
                  "Movement (NSM). The paper leak, the students lost to the "
                  "examination, and the demand that NEET be scrapped were what "
                  "the evening was about.",
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
]

UI = {
    "title":      {"ta": "மாதாந்திர அறிக்கை", "en": "Monthly report"},
    "org":        {"ta": "நிலாதம்மா", "en": "Niladhamma"},
    "sub":        {"ta": "அசோக் நகர் புத்த விஹார், சென்னை",
                   "en": "Ashok Nagar Buddha Vihar, Chennai"},
    "at_a_glance":{"ta": "ஒரு பார்வையில்", "en": "At a glance"},
    "stat_days":  {"ta": "நாள், {n} கதைகள்", "en": "days, {n} stories"},
    "stat_events":{"ta": "நிகழ்வுகள்", "en": "events"},
    "stat_moon":  {"ta": "பௌர்ணமிக் கூட்டம்", "en": "full moon gathering"},
    "events_h":   {"ta": "நிகழ்வுகள்", "en": "Events"},
    "programme":  {"ta": "நிகழ்ச்சி நிரல்", "en": "Programme"},
    "took_part":  {"ta": "கலந்துகொண்டோர்", "en": "Took part"},
    "stories_h":  {"ta": "தம்மபதம்: முப்பத்தோர் நாள்",
                   "en": "Dhammapada: Thirty-one Days"},
    "stories_sub":{"ta": "ஜூலை 1 முதல் 31 வரை, ஒவ்வொரு நாளும் ஒரு "
                         "பௌத்தக் கதை. அனைத்தும் வெளியிடப்பட்டன.",
                   "en": "One Buddhist story for each day from 1 to 31 July. "
                         "All of them were published."},
    "photos_h":   {"ta": "படங்கள்", "en": "Photographs"},
    "moon_h":     {"ta": "பௌர்ணமி", "en": "Full moon"},
    "moon_p":     {"ta": "ஜூலை மாதப் பௌர்ணமி {d} அன்று, இரவு {t} மணிக்கு.",
                   "en": "July's full moon fell on {d} at {t}."},
    "pending":    {"ta": "உறுதி செய்யப்பட வேண்டியது",
                   "en": "To be confirmed"},
    "footer":     {"ta": "இவ்வறிக்கை நிலாதம்மா தள ({site}) தரவிலிருந்து "
                         "தானாக உருவாக்கப்பட்டது.",
                   "en": "This report is generated from the Niladhamma site "
                         "data ({site})."},
}

TA_MONTHS = ["ஜனவரி", "பிப்ரவரி", "மார்ச்", "ஏப்ரல்", "மே", "ஜூன்", "ஜூலை",
             "ஆகஸ்ட்", "செப்டம்பர்", "அக்டோபர்", "நவம்பர்", "டிசம்பர்"]
EN_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]


def U(key, L, **fmt):
    s = UI[key][L]
    return s.format(**fmt) if fmt else s


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as fh:
        return json.load(fh)


def fmt_date(iso, L):
    y, m, d = (int(x) for x in iso.split("-"))
    return (f"{d} {TA_MONTHS[m - 1]} {y}" if L == "ta"
            else f"{d} {EN_MONTHS[m - 1]} {y}")


def day_num(iso):
    return int(iso.split("-")[2])


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def stories(L):
    """(day, title) for all 31, Tamil from the source, English from the
    translation file. Read, never retyped, so the report cannot disagree with
    what the site published."""
    ta = {s["day"]: s["title"] for s in load("stories_july.json")["stories"]}
    if L == "ta":
        return sorted(ta.items())
    en = load("stories_en.json")["stories"]
    return sorted((d, en.get(str(d), {}).get("title", t)) for d, t in ta.items())


def july_moon():
    for m in load("moons.json")["moons"]:
        if m["date"].startswith("2026-07"):
            return m
    return None


def event_block(ev, L):
    pending = ("" if not ev.get("pending") else
               f'<span class="rp-pending">{U("pending", L)}</span>')
    parts = [
        f'<div class="rp-ev">',
        f'  <div class="rp-ev__when">',
        f'    <span class="rp-ev__day">{day_num(ev["date"])}</span>',
        f'    <span class="rp-ev__kind">{ev["kind"][L]}</span>',
        f'  </div>',
        f'  <div class="rp-ev__body">',
        f'    <h3>{ev[L]}{pending}</h3>',
        f'    <p class="rp-ev__date">{fmt_date(ev["date"], L)}</p>',
        f'    <p>{ev["note"][L]}</p>',
    ]
    if ev.get("programme"):
        parts.append(f'<p class="rp-label">{U("programme", L)}</p>')
        parts.append('<ol class="rp-prog">')
        for item in ev["programme"]:
            parts.append(f'<li><span>{item[L]}</span>'
                         f'<em>{item["form"][L]}</em></li>')
        parts.append("</ol>")
    if ev.get("people"):
        names = ", ".join(p[L] for p in ev["people"])
        parts.append(f'<p class="rp-people"><strong>{U("took_part", L)}:</strong> '
                     f'{names}</p>')
    parts += ["  </div>", "</div>"]
    return "\n".join(parts)


def build(L):
    st = stories(L)
    moon = july_moon()
    rows = "".join(
        f'<tr><td class="rp-d">{d}</td><td>{esc(t)}</td></tr>' for d, t in st
    )
    half = (len(st) + 1) // 2
    col1 = "".join(f'<tr><td class="rp-d">{d}</td><td>{esc(t)}</td></tr>'
                   for d, t in st[:half])
    col2 = "".join(f'<tr><td class="rp-d">{d}</td><td>{esc(t)}</td></tr>'
                   for d, t in st[half:])

    photos = ""
    for ev in EVENTS:
        for p in ev.get("photos", []):
            photos += (
                f'<figure class="rp-shot">'
                f'<img src="{p["src"]}" width="{p["w"]}" height="{p["h"]}" '
                f'alt="{p[L]}" loading="lazy">'
                f'<figcaption>{p[L]}</figcaption></figure>'
            )

    moon_block = ""
    if moon:
        moon_block = (
            f'<section class="rp-sec rp-sec--tight">'
            f'<h2>{U("moon_h", L)}</h2>'
            f'<p>{U("moon_p", L, d=moon[f"label_{L}"], t=moon["time_ist"])}</p>'
            f'</section>'
        )

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
  .rp-sec--tight {{ margin-top: 30px; }}
  .rp-sec > h2 {{ font-size: 20px; padding-bottom: 10px; margin-bottom: 4px;
                  border-bottom: 2px solid var(--cm-border-default); }}
  .rp-sec > .rp-sub {{ margin: 10px 0 0; font-size: 14.5px; color: var(--cm-text-muted); }}

  /* Events: the date is a rail on the left, so a reader scanning the month
     sees the sequence before they read any of it. */
  .rp-ev {{ display: grid; grid-template-columns: 74px minmax(0, 1fr); gap: 20px;
            padding: 22px 0; border-bottom: 1px solid var(--cm-border-default); }}
  .rp-ev:last-child {{ border-bottom: none; }}
  .rp-ev__when {{ text-align: center; }}
  .rp-ev__day {{ display: block; font-size: 30px; font-weight: 700;
                 line-height: 1; color: var(--cm-green-800, #2f6b45);
                 font-variant-numeric: tabular-nums; }}
  .rp-ev__kind {{ display: block; margin-top: 6px; font-size: 11px; font-weight: 600;
                  color: var(--cm-text-muted); }}
  .rp-ev__body h3 {{ font-size: 17px; margin: 0; }}
  .rp-ev__date {{ margin: 5px 0 10px; font-size: 13px; color: var(--cm-text-muted); }}
  .rp-ev__body p {{ font-size: 15px; line-height: 1.75; margin: 0 0 10px;
                    color: var(--cm-text-body); }}
  .rp-pending {{ display: inline-block; margin-inline-start: 9px; padding: 2px 9px;
                 font-size: 11px; font-weight: 600; vertical-align: middle;
                 color: var(--cm-text-body); background: var(--cm-bg-well);
                 border: 1px solid var(--cm-border-strong);
                 border-radius: var(--cm-radius-sm); }}
  .rp-label {{ font-size: 11px !important; font-weight: 700; letter-spacing: 0.06em;
               color: var(--cm-text-muted); margin: 14px 0 6px !important; }}
  .rp-prog {{ margin: 0; padding-left: 20px; }}
  .rp-prog li {{ font-size: 15px; line-height: 1.7; margin-bottom: 5px; }}
  .rp-prog em {{ font-style: normal; margin-inline-start: 8px; font-size: 12px;
                 color: var(--cm-text-muted); }}
  .rp-people {{ font-size: 14.5px !important; }}

  .rp-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
              gap: 0 34px; margin-top: 18px; }}
  .rp-tbl {{ width: 100%; border-collapse: collapse; }}
  .rp-tbl td {{ padding: 7px 0; font-size: 14.5px; line-height: 1.5;
                border-bottom: 1px solid var(--cm-neutral-100, #eef2ef);
                vertical-align: top; }}
  .rp-d {{ width: 30px; color: var(--cm-green-700); font-weight: 700;
           font-variant-numeric: tabular-nums; }}

  .rp-shots {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
               gap: 14px; margin-top: 18px; }}
  .rp-shot {{ margin: 0; }}
  .rp-shot img {{ width: 100%; height: auto; border-radius: var(--cm-radius-lg);
                  border: 1px solid var(--cm-border-default); }}
  .rp-shot figcaption {{ margin-top: 8px; font-size: 12.5px; line-height: 1.55;
                         color: var(--cm-text-muted); }}

  .rp__foot {{ margin-top: 44px; padding-top: 16px;
               border-top: 1px solid var(--cm-border-default);
               font-size: 12.5px; color: var(--cm-text-muted); }}

  @media (max-width: 700px) {{
    .rp-stats, .rp-grid, .rp-shots {{ grid-template-columns: minmax(0, 1fr); }}
    .rp-ev {{ grid-template-columns: 56px minmax(0, 1fr); gap: 14px; }}
  }}

  @media print {{
    @page {{ margin: 14mm 12mm; }}
    body {{ background: #ffffff !important; }}
    .rp {{ max-width: none; padding: 0; }}
    .rp-stat, .rp-shot, .rp-ev, .rp-sec > h2 {{ break-inside: avoid-page; }}
    .rp-sec > h2 {{ break-after: avoid-page; }}
    .rp-shots {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
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

  <section class="rp-stats" aria-label="{U('at_a_glance', L)}">
    <div class="rp-stat"><b>31</b><span>{U("stat_days", L, n=len(st))}</span></div>
    <div class="rp-stat"><b>{len(EVENTS)}</b><span>{U("stat_events", L)}</span></div>
    <div class="rp-stat"><b>1</b><span>{U("stat_moon", L)}</span></div>
  </section>

  <section class="rp-sec">
    <h2>{U("events_h", L)}</h2>
    {"".join(event_block(e, L) for e in EVENTS)}
  </section>

  <section class="rp-sec">
    <h2>{U("photos_h", L)}</h2>
    <div class="rp-shots">{photos}</div>
  </section>

  <section class="rp-sec">
    <h2>{U("stories_h", L)}</h2>
    <p class="rp-sub">{U("stories_sub", L)}</p>
    <div class="rp-grid">
      <table class="rp-tbl"><tbody>{col1}</tbody></table>
      <table class="rp-tbl"><tbody>{col2}</tbody></table>
    </div>
  </section>

  {moon_block}

  <p class="rp__foot">{U("footer", L, site="niladhamma.co.in")}</p>
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
    print(f"Done. {len(EVENTS)} events, {len(stories('ta'))} stories.")


if __name__ == "__main__":
    main()
