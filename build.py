#!/usr/bin/env python3
"""
Niladhamma · static site generator (Canopy design system)

Composes the site from data/ plus the page bodies below. No dependencies, no
build toolchain: run `python3 build.py`.

Canopy hard rules enforced here:
  no em-dash anywhere · Figtree (Latin) with a documented Tamil fallback ·
  success = green + check icon + copy · focus ring never suppressed ·
  key-lines are border-bottom, never a shadow · violet reserved for AI ·
  Title Case for English page titles and nav, sentence case elsewhere · Tamil
  strings are never title-cased (Canopy: English reference only).

Paths are root-relative so pages can live in subdirectories. Serve from the
project root; the pages will not resolve over file://.
"""

import collections
import glob
import json
import os
import re
from html.parser import HTMLParser

from content import C, FAQ

ROOT = os.path.dirname(os.path.abspath(__file__))
def _today_ist():
    """Today in Asia/Kolkata. A CI runner is on UTC, and IST is UTC+5:30, so
    using the runner's date would release each story hours early."""
    from datetime import datetime, timedelta, timezone
    return (datetime.now(timezone.utc)
            + timedelta(hours=5, minutes=30)).date().isoformat()


# ND_TODAY overrides the date, so the release gate can be tested without
# waiting for the calendar.
TODAY = os.environ.get("ND_TODAY") or _today_ist()
DATA = os.path.join(ROOT, "data")

BASE = "https://www.niladhamma.co.in"       # canonical origin
SITE = "நிலாதம்மா"
SITE_FULL = "நிலாதம்மா"
SITE_EN = "Niladhamma"
SITE_EN_FULL = "Niladhamma"
TAGLINE = "உனக்கு நீயே ஒளியாய் இரு"
TAGLINE_EN = "Be a light unto yourself"
MOTTO_EN = "Trust in you"
MOTTO_LINE_EN = "One world, one life. Let's celebrate humanity."
MOTTO_TA = "உனக்கு நீ நம்பிக்கை"
MOTTO_LINE_TA = "ஒரே உலகம், ஒரே வாழ்வு. மனிதத்தைக் கொண்டாடுவோம்."
EMAIL = "info@niladhamma.co.in"
VENUE = "அசோக் நகர் புத்த விஹார், சென்னை"
VENUE_EN = "Ashok Nagar Buddha Vihar"
VENUE_STREET = "15, 4th Avenue, Dr Ambedkar Nagar, Brindavan Extension, Ashok Nagar"
VENUE_CITY = "Chennai"
VENUE_PIN = "600083"
VENUE_ADDR_TA = ("15, 4வது அவென்யூ, டாக்டர் அம்பேத்கர் நகர், பிருந்தாவன் "
                 "எக்ஸ்டென்ஷன், அசோக் நகர், சென்னை 600083")
MAPS_URL = ("https://www.google.com/maps/search/?api=1&amp;query="
            "Ashok+Nagar+Buddha+Vihar%2C+15+4th+Avenue%2C+Dr+Ambedkar+Nagar%2C"
            "+Brindavan+Extension%2C+Ashok+Nagar%2C+Chennai+600083")

VENUE_LD = {
    "@type": "Place",
    "@id": BASE + "/#vihar",
    "name": f"{VENUE_EN} ({VENUE})",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": VENUE_STREET,
        "addressLocality": VENUE_CITY,
        "addressRegion": "Tamil Nadu",
        "postalCode": VENUE_PIN,
        "addressCountry": "IN",
    },
    "hasMap": MAPS_URL.replace("&amp;", "&"),
}

SOCIAL = [
    ("https://www.facebook.com/niladhamma/", "Facebook"),
    ("https://www.instagram.com/niladhamma/", "Instagram"),
    ("https://www.youtube.com/@niladhamma", "YouTube"),
    ("https://x.com/niladhamma", "X"),
]

# --------------------------------------------------------------------------
# Icons: stroked line set, 1.8 weight, round caps, 24px box, currentColor.
# Lucide-equivalent shapes, drawn inline (Canopy ships no icon font).
# --------------------------------------------------------------------------
ICONS = {
    "moon": '<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z"/>',
    "wheel": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.5"/>'
             '<path d="M12 3v6.5M12 14.5V21M3 12h6.5M14.5 12H21'
             'M5.6 5.6l4.6 4.6M13.8 13.8l4.6 4.6M18.4 5.6l-4.6 4.6M10.2 13.8l-4.6 4.6"/>',
    "users": '<path d="M16 20v-1.5a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4V20"/>'
             '<circle cx="9" cy="7" r="3.5"/><path d="M22 20v-1.5a4 4 0 0 0-3-3.87"/>'
             '<path d="M16 3.6a4 4 0 0 1 0 6.8"/>',
    "book": '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v15H6.5A2.5 2.5 0 0 0 4 19.5Z"/>'
            '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20v5H6.5A2.5 2.5 0 0 1 4 19.5Z"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
                '<path d="M7 10l5 5 5-5"/><path d="M12 15V3"/>',
    "heart": '<path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 1 0-7.1 7.1l1.7 1.7L12 21.5'
             'l7.1-7.1 1.7-1.7a5 5 0 0 0 0-7.1Z"/>',
    "file": '<path d="M14 2H7a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7Z"/>'
            '<path d="M14 2v5h5"/><path d="M9 13h6M9 17h4"/>',
    "mail": '<rect x="2.5" y="4.5" width="19" height="15" rx="2"/><path d="M3 6.5l9 6 9-6"/>',
    "check": '<path d="M20 6.5L9.5 17 4 11.5"/>',
    "info": '<circle cx="12" cy="12" r="9.5"/><path d="M12 11v5.5M12 7.6v.1"/>',
    "map": '<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="16" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "sparkle": '<path d="M12 3l1.9 5.4L19.5 10l-5.6 1.6L12 17l-1.9-5.4L4.5 10l5.6-1.6Z"/>'
               '<path d="M18.5 15.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8Z"/>',
    "school": '<path d="M12 3 2.5 8 12 13l9.5-5Z"/><path d="M6 10.4V16c0 1.7 2.7 3 6 3s6-1.3 6-3v-5.6"/>'
              '<path d="M21.5 8v6"/>',
    "shield": '<path d="M12 2.8 4.5 6v6c0 4.6 3.2 8.4 7.5 9.3 4.3-.9 7.5-4.7 7.5-9.3V6Z"/>'
              '<path d="M9.2 12.2l2 2 3.6-3.8"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "external": '<path d="M14 4h6v6"/><path d="M20 4l-9 9"/>'
                '<path d="M18 14v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "globe": '<circle cx="12" cy="12" r="9.2"/><path d="M2.9 12h18.2"/>'
             '<path d="M12 2.8a14.5 14.5 0 0 1 0 18.4a14.5 14.5 0 0 1 0-18.4Z"/>',
    "quote": '<path d="M9.5 6C6.5 7.5 5 10 5 13v5h6v-6H8c0-2 .6-3.4 2.4-4.4Z"/>'
             '<path d="M18 6c-3 1.5-4.5 4-4.5 7v5h6v-6h-3c0-2 .6-3.4 2.4-4.4Z"/>',
    "layers": '<path d="M12 2.8 2.5 7.5 12 12.2l9.5-4.7Z"/><path d="M2.5 16.5 12 21.2l9.5-4.7"/>'
              '<path d="M2.5 12 12 16.7l9.5-4.7"/>',
    "clock": '<circle cx="12" cy="12" r="9.2"/><path d="M12 6.8v5.5l3.4 2"/>',
    "image": '<rect x="3" y="4.5" width="18" height="15" rx="2"/>'
             '<circle cx="8.6" cy="10" r="1.7"/><path d="M20.6 15.8 16 11.2 6.5 20.5"/>',
    "link": '<path d="M10.6 13.4a4.2 4.2 0 0 0 6 0l2.6-2.6a4.2 4.2 0 1 0-6-6l-1.5 1.5"/>'
            '<path d="M13.4 10.6a4.2 4.2 0 0 0-6 0l-2.6 2.6a4.2 4.2 0 1 0 6 6l1.5-1.5"/>',
    "close": '<path d="M6.2 6.2 17.8 17.8M17.8 6.2 6.2 17.8"/>',
    "expand": '<path d="M14.5 3.5H20.5V9.5"/><path d="M9.5 20.5H3.5V14.5"/>'
              '<path d="M20.5 3.5 14 10"/><path d="M3.5 20.5 10 14"/>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/>'
            '<path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/>'
            '<path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
    "hands": '<path d="M11 13.5 8.4 10.9a2 2 0 0 0-2.8 2.8L10 18"/>'
             '<path d="M13 13.5l2.6-2.6a2 2 0 0 1 2.8 2.8L14 18"/>'
             '<path d="M12 3.5 9.8 5.7a3 3 0 0 0 0 4.2l2.2 2.2 2.2-2.2a3 3 0 0 0 0-4.2Z"/>',
}


def icon(name, size=20, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (
        f'<svg{c} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
    )


BRAND_MARK = ('<img class="nd-brand__mark" src="/assets/img/logo-96.png" '
              'width="48" height="48" alt="">')
FOOTER_MARK = ('<img src="/assets/img/logo-96.png" width="28" height="28" alt="" '
               'style="border-radius:50%">')

# Primary navigation. The four utility pages sit behind the Resources hub so
# the bar stays at seven destinations and never wraps.
# ---------------------------------------------------------------------------
# Two languages, one tree. Tamil sits at the root because it is the primary
# audience; English mirrors every path under /en/. Keeping the paths identical
# apart from the prefix is what makes hreflang pairing and the switcher exact.
# ---------------------------------------------------------------------------
LANGS = {
    "ta": {"prefix": "", "html": "ta", "og": "ta_IN", "name": "தமிழ்",
           "self": "தமிழ்", "other": "en", "other_name": "English"},
    "en": {"prefix": "/en", "html": "en", "og": "en_IN", "name": "English",
           "self": "English", "other": "ta", "other_name": "தமிழ்"},
}
DEFAULT_LANG = "ta"


def u(path, L):
    """Site path for a canonical path in language L.

    Directory indexes canonicalise to the trailing-slash form, so "/" and
    "/index.html" never both exist as indexable URLs."""
    full = LANGS[L]["prefix"] + path
    if full.endswith("/index.html"):
        full = full[: -len("index.html")]
    elif full == "/index.html":
        full = "/"
    return full or "/"


def tt(d, L):
    """Pick the string for L from a {'ta': ..., 'en': ...} pair."""
    return d[L]


NAV = [
    ("/index.html", "முகப்பு", "Home"),
    ("/about.html", "நம்மைப் பற்றி", "About"),
    ("/kathai/", "கதைகள்", "Dhamma Stories"),
    ("/events.html", "நிகழ்வுகள்", "Events"),
    ("/writings.html", "பதிவுகள்", "Writings"),
    ("/resources.html", "வளங்கள்", "Resources"),
    ("/contact.html", "தொடர்பு", "Contact"),
]

# Shared chrome strings. Page prose lives beside its translation inside each
# build_* function; only the strings reused across pages are collected here.
UI = {
    "skip":        {"ta": "உள்ளடக்கத்திற்குச் செல்", "en": "Skip to content"},
    "menu":        {"ta": "பட்டி", "en": "Menu"},
    "mainnav":     {"ta": "முதன்மை வழிசெலுத்தல்", "en": "Main navigation"},
    "breadcrumb":  {"ta": "தட நெறி", "en": "Breadcrumb"},
    "home":        {"ta": "முகப்பு", "en": "Home"},
    "pages":       {"ta": "பக்கங்கள்", "en": "Pages"},
    "resources":   {"ta": "வளங்கள்", "en": "Resources"},
    "events_nav":  {"ta": "நிகழ்வுகள்", "en": "Events"},
    "contact":     {"ta": "தொடர்பு", "en": "Contact"},
    "lang_label":  {"ta": "மொழி", "en": "Language"},
    "switch_aria": {"ta": "View this page in English",
                    "en": "இப்பக்கத்தைத் தமிழில் படிக்க"},
    "all":         {"ta": "அனைத்தும்", "en": "All"},
    "read_all":    {"ta": "அனைத்தும்", "en": "See all"},
    "search_title":{"ta": "தலைப்பில் தேட", "en": "Search by title"},
    "no_results":  {"ta": "இந்தத் தேடலுக்கு எதுவும் இல்லை.",
                    "en": "Nothing matches that search."},
    "ehi":         {"ta": "&ldquo;ஏஹி பஸ்ஸிகோ&rdquo; &middot; வாருங்கள், வந்து கண்டுணருங்கள்",
                    "en": "&ldquo;Ehipassiko&rdquo; &middot; come and see for yourself"},
    "footer_blurb":{"ta": "நாங்கள் பௌத்தர்கள். சுதந்திரம், சமத்துவம், "
                          "சகோதரத்துவம் காட்டும் தம்மப்பாதையில் பயணிக்கிறோம். "
                          "2012 முதல் ஒவ்வொரு பௌர்ணமியிலும் குடும்பமாகக் "
                          "கூடி வருகிறோம்.",
                    "en": "We are Buddhists. We tread the Dhamma path founded on "
                          "liberty, equality and fraternity. Since 2012 we have "
                          "gathered as families on every full moon day."},
    "footer_kathai":{"ta": "தம்மபதம்: முப்பத்தோர் நாள் &middot; ஒவ்வொரு நாளும் "
                           "ஒரு பௌத்தக் கதை.",
                     "en": "Dhammapada: Thirty-one Days &middot; one Buddhist "
                           "story for each day."},
    "trans_note":  {"ta": "", "en": "This English text is a translation. The "
                                    "Tamil original is authoritative."},
    # A collection can go live before its translation is ready, so the two
    # states need different wording; the old code showed the line above in
    # both, which told readers a Tamil page was an English translation.
    "trans_wait":  {"ta": "", "en": "This has not been translated yet. The "
                                    "text below is the Tamil original."},
    "kathai_title":{"ta": "தம்மபதம்: முப்பத்தோர் நாள்",
                    "en": "Dhammapada: Thirty-one Days"},
    "kathai_short":{"ta": "தம்மக் கதைகள்", "en": "Dhamma Stories"},
    "writings":    {"ta": "பதிவுகள்", "en": "Writings"},
    "day":         {"ta": "நாள்", "en": "Day"},
    "july":        {"ta": "ஜூலை", "en": "July"},
    "insight":     {"ta": "தம்மக்கருத்து", "en": "Dhamma insight"},
    "ambedkar":    {"ta": "அம்பேத்கர் இணைப்பு", "en": "The Ambedkar connection"},
    "source":      {"ta": "ஆதாரம்", "en": "Source"},
    "prev":        {"ta": "முந்தையது", "en": "Previous"},
    "next":        {"ta": "அடுத்தது", "en": "Next"},
    "older":       {"ta": "அடுத்த பழையது", "en": "Older"},
    "newer":       {"ta": "அண்மையது", "en": "Newer"},
    "more_posts":  {"ta": "மேலும் பதிவுகள்", "en": "More writings"},
    "origin":      {"ta": "இப்பதிவின் அசல்", "en": "Originally published at"},
    "related":     {"ta": "தொடர்புடையவை", "en": "Related"},
    "faq":         {"ta": "அடிக்கடி கேட்கப்படும் கேள்விகள்",
                    "en": "Frequently asked questions"},
    "venue":       {"ta": VENUE, "en": f"{VENUE_EN}, Chennai"},
    "venue_addr":  {"ta": VENUE_ADDR_TA,
                    "en": f"{VENUE_STREET}, {VENUE_CITY} {VENUE_PIN}"},
    "directions":  {"ta": "வழி காட்ட", "en": "Get directions"},
    "map":         {"ta": "வரைபடத்தில் பார்க்க", "en": "View on the map"},
    # Archive post furniture: the meta strip, the photograph viewer, the
    # copy-link control. Counts are formatted by the caller.
    "read_min":    {"ta": "நிமிட வாசிப்பு", "en": "min read"},
    "photos":      {"ta": "படங்கள்", "en": "photographs"},
    "photo_one":   {"ta": "படம்", "en": "photograph"},
    "photo_of":    {"ta": "படம் {n} / {t}", "en": "Photograph {n} of {t}"},
    "copy_link":   {"ta": "இணைப்பை நகலெடு", "en": "Copy link"},
    "copied":      {"ta": "நகலெடுக்கப்பட்டது", "en": "Link copied"},
    "viewer":      {"ta": "படக் காட்சி", "en": "Photograph viewer"},
    "close":       {"ta": "மூடு", "en": "Close"},
}


def U(key, L):
    return UI[key][L]


def c(key, L, **fmt):
    """Prose from content.py, with optional {placeholder} substitution."""
    text = C[key][L]
    return text.format(**fmt) if fmt else text


def faq_for(name, L):
    """FAQ pairs for the current language."""
    return [(q[L], a[L]) for q, a in FAQ[name]]

RESOURCES = [
    ("/dana.html", "தானம்", "Dana", "gift",
     "எதைக் கொடுக்கிறோம், யாருக்கு, எப்படி, ஏன்: தானத்தின் வகைகள்.",
     "What is given, to whom, how and why: the kinds of giving."),
    ("/names.html", "பௌத்தப் பெயர்கள்", "Buddhist Names", "users",
     "ஆண், பெண் குழந்தைகளுக்கான பெயர்கள் மற்றும் தேரகதாவின் தேரர் பெயர்கள்.",
     "Names for boys and girls, and the names of the theras of the Theragatha."),
    ("/certificate.html", "சமூகச் சான்றிதழ்", "Community Certificate", "file",
     "பௌத்தமேற்ற பட்டியலினத்தினர் சான்றிதழ் பெறும் வழிமுறை.",
     "How Scheduled Caste Buddhists obtain a community certificate."),
    ("/downloads.html", "தரவிறக்கம்", "Downloads", "download",
     "மின்னூல்கள், ஒலி வடிவங்கள், அம்பேத்கர் தொகுதிகள்.",
     "E-books, audio, and the Ambedkar volumes."),
    ("/matrimony.html", "பௌத்தத் திருமணம்", "Buddhist Matrimony", "heart",
     "மகாமங்கள முறையும், துணை தேடலுக்கான பதிவும்.",
     "The Mahamangala rite, and the register for finding a partner."),
]


def res_items(L):
    """(href, label, icon, description) for the current language."""
    return [(h, ta if L == "ta" else en, ic, sta if L == "ta" else sen)
            for h, ta, en, ic, sta, sen in RESOURCES]


# Addressed by path, not by position. The list used to be indexed, so adding an
# entry at the front would have quietly retitled four other pages.
_RES = {r[0]: r for r in RESOURCES}


def res_title(path, L):
    _h, ta, en, *_r = _RES[path]
    return ta if L == "ta" else en


def res_desc(path, L):
    *_r, sta, sen = _RES[path]
    return sta if L == "ta" else sen


def res_link(path, L):
    """(href, label, description), the shape the related-links strip wants."""
    return (path, res_title(path, L), res_desc(path, L))

# Calendar. Two kinds of observance, kept apart on purpose.
#
# LUNAR: Theravada observances fall on a full moon, so they move each year.
# They are described by lunar month and the Gregorian months they land in,
# never as a fixed date, because asserting one would be wrong.
#
# FIXED: Ambedkarite and Tamil Buddhist anniversaries are solar and do not move.
LUNAR_DAYS = [
    ({"ta": "வைசாக பௌர்ணமி", "en": "Vesak full moon"}, "Vesak / Buddha Purnima",
     {"ta": "ஏப்ரல் &ndash; மே", "en": "April &ndash; May"},
     {"ta": "புத்தரின் பிறப்பு, ஞானம், பரிநிர்வாணம், மூன்றும் இந்நாளோடு "
            "இணைக்கப்படுகின்றன. பௌத்த மரபின் மிகப் பெரிய நாள்.",
      "en": "The Buddha's birth, his awakening and his parinibbana are all "
            "joined to this day. The greatest day of the Buddhist tradition."}),
    ({"ta": "ஆடி (ஆஷாட) பௌர்ணமி", "en": "Asalha full moon"}, "Asalha Puja / Dhamma Day",
     {"ta": "ஜூன் &ndash; ஜூலை", "en": "June &ndash; July"},
     {"ta": "சாரநாத்தில் புத்தர் தம் முதல் உபதேசத்தை, தம்மச் சக்கரத்தை, "
            "உருட்டிய நாள்; சங்கம் பிறந்த நாள். மறுநாள் வஸ்ஸ (மழைக்கால "
            "தங்குதல்) தொடங்குகிறது.",
      "en": "The day the Buddha turned the wheel of Dhamma in his first "
            "discourse at Sarnath, and the day the Sangha was born. Vassa, the "
            "rains retreat, begins the following day."}),
    ({"ta": "ஐப்பசி (அஸ்ஸயுஜ) பௌர்ணமி", "en": "Assayuja full moon"}, "Pavarana",
     {"ta": "அக்டோபர்", "en": "October"},
     {"ta": "மூன்று மாத வஸ்ஸ நிறைவடையும் நாள். இதைத் தொடர்ந்து வரும் "
            "மாதத்தில் கடின சீவரத் தானம்.",
      "en": "The day the three-month Vassa ends. The Kathina robe offering "
            "follows in the month after."}),
    ({"ta": "மாசி (மாக) பௌர்ணமி", "en": "Magha full moon"}, "Magha Puja",
     {"ta": "பிப்ரவரி &ndash; மார்ச்", "en": "February &ndash; March"},
     {"ta": "அழைப்பின்றி 1,250 அரகந்தர்கள் புத்தரிடம் ஒன்றுகூடிய நாள்; "
            "சங்கத்தின் ஒற்றுமையை நினைவுகூரும் நாள்.",
      "en": "The day 1,250 arahants gathered before the Buddha unsummoned; a "
            "day that recalls the unity of the Sangha."}),
    ({"ta": "மார்கழி (உந்துவாப்) பௌர்ணமி", "en": "Unduvap full moon"}, "Sanghamitta Day",
     {"ta": "டிசம்பர்", "en": "December"},
     {"ta": "போதி மர நாற்றுடன் சங்கமித்தை தேரி இலங்கையை அடைந்த நாள்; "
            "பிக்குனி சங்கம் கடல் கடந்த நாள்.",
      "en": "The day Sanghamitta Theri reached Sri Lanka with the Bodhi tree "
            "sapling; the day the bhikkhuni order crossed the sea."}),
    ({"ta": "அசோக விஜயதசமி", "en": "Ashoka Vijayadashami"}, "Ashoka Vijayadashami",
     {"ta": "செப்டம்பர் &ndash; அக்டோபர்", "en": "September &ndash; October"},
     {"ta": "அசோகர் தம்மத்தைத் தழுவிய நாளாக மரபு கொள்வது. 1956இல் "
            "அம்பேத்கர் தம் தீட்சைக்கு இந்நாளையே தேர்ந்தார்.",
      "en": "Held by tradition to be the day Ashoka embraced the Dhamma. "
            "Ambedkar chose this day for his own conversion in 1956."}),
]

FIXED_DAYS = [
    ("01-01", {"ta": "கோரேகான் நினைவு தினம்", "en": "Bhima Koregaon Remembrance"},
     "1818", {"ta": "பீமா கோரேகான் போரின் நினைவு நாள்.",
              "en": "Remembrance of the battle of Bhima Koregaon."},
     "2026-01-03-2"),
    ("03-01", {"ta": "சாவித்திரிபாய் புலே பிறந்த நாள்",
               "en": "Savitribai Phule's birthday"},
     "1831", {"ta": "இந்தியாவின் முதல் பெண் ஆசிரியர்; பெண் கல்விக்கு "
                    "வழிதிறந்தவர்.",
              "en": "India's first woman teacher, who opened the way to "
                    "education for girls."}),
    ("17-01", {"ta": "ரோகித் வெமுலா நினைவு நாள்", "en": "Rohith Vemula Remembrance"},
     "2016", {"ta": "சாதிய ஒடுக்குமுறைக்கு எதிரான நினைவேந்தல்.",
              "en": "A remembrance against caste oppression."}),
    ("26-01", {"ta": "குடியரசு தினம்", "en": "Republic Day"},
     "1950", {"ta": "அம்பேத்கர் தலைமையில் வரையப்பட்ட அரசியலமைப்பு "
                    "நடைமுறைக்கு வந்த நாள்.",
              "en": "The day the Constitution, drafted under Ambedkar's "
                    "chairmanship, came into force."}),
    ("31-01", {"ta": "மூக்நாயக் தொடங்கிய நாள்", "en": "Mooknayak founded"},
     "1920", {"ta": "அம்பேத்கர் தொடங்கிய முதல் இதழ்; ஒடுக்கப்பட்டோரின் "
                    "குரலுக்கான களம்.",
              "en": "Ambedkar's first journal, a platform for the voice of "
                    "the oppressed."}),
    ("02-03", {"ta": "காலாராம் கோயில் நுழைவுப் போராட்டம்",
               "en": "Kalaram temple entry satyagraha"},
     "1930", {"ta": "நாசிக்கில் கோயில் நுழைவு உரிமைக்காக அம்பேத்கர் "
                    "தலைமையில் நடந்த போராட்டம்.",
              "en": "The struggle led by Ambedkar at Nashik for the right of "
                    "entry to the temple."}),
    ("20-03", {"ta": "மகத் சத்தியாகிரகம்", "en": "Mahad Satyagraha"},
     "1927", {"ta": "சவதார் குளத்து நீர் உரிமைக்காக அம்பேத்கர் தலைமையில் "
                    "நடந்த போராட்டம்.",
              "en": "The struggle led by Ambedkar for the right to draw water "
                    "from the Chavdar tank."}),
    ("11-04", {"ta": "ஜோதிராவ் புலே பிறந்த நாள்", "en": "Jyotirao Phule's birthday"},
     "1827", {"ta": "சத்தியசோதக் சமாஜ் நிறுவியவர்; அம்பேத்கர் தம் மூன்று "
                    "குருக்களில் ஒருவராகக் கொண்டவர்.",
              "en": "Founder of the Satyashodhak Samaj, and one of the three "
                    "teachers Ambedkar named as his own."}),
    ("14-04", {"ta": "அம்பேத்கர் பிறந்த நாள்", "en": "Ambedkar's birthday"},
     "1891", {"ta": "பாபாசாகேப் Dr. B. R. அம்பேத்கர் பிறந்த நாள்.",
              "en": "The birthday of Babasaheb Dr B. R. Ambedkar."}),
    ("20-05", {"ta": "அயோத்திதாசப் பண்டிதர் பிறந்த நாள்",
               "en": "Iyothee Thass Pandithar's birthday"},
     "1845", {"ta": "1898இல் சாக்கிய பௌத்தச் சங்கத்தை நிறுவி தமிழகப் பௌத்த "
                    "மறுமலர்ச்சியைத் தொடங்கியவர்.",
              "en": "Founder of the Sakya Buddhist Society in 1898, who began "
                    "the Buddhist revival in Tamil Nadu."}),
    ("05-05", {"ta": "அயோத்திதாசர் நினைவு நாள்",
               "en": "Iyothee Thass remembrance"},
     "1914", {"ta": "தமிழ்ப் பௌத்த மறுமலர்ச்சியின் முன்னோடி; "
                    "'தமிழன்' இதழை நடத்தியவர்.",
              "en": "The forerunner of the Tamil Buddhist revival, and editor "
                    "of the journal Tamilan."}),
    ("17-06", {"ta": "ராவ் பகதூர் M. C. ராஜா பிறந்த நாள்",
               "en": "Rao Bahadur M. C. Rajah's birthday"},
     "1883", {"ta": "ஒடுக்கப்பட்ட மக்களை தேசிய அளவில் முதலில் "
                    "ஒருங்கிணைத்தவர்.",
              "en": "The first to organise the depressed classes at a "
                    "national level."}, "mcraja-on-hindu-identity"),
    ("07-07", {"ta": "ரெட்டமலை சீனிவாசன் பிறந்த நாள்",
               "en": "Rettamalai Srinivasan's birthday"},
     "1859", {"ta": "தேவன் பகதூர்; அயோத்திதாசருடன் பஞ்சமர் மகாஜன சபையை "
                    "நிறுவியவர்; பூனா ஒப்பந்தத்தில் கையெழுத்திட்டவர்.",
              "en": "Dewan Bahadur, who founded the Panchamar Mahajana Sabha "
                    "with Iyothee Thass and signed the Poona Pact."}),
    ("20-07", {"ta": "பகிஷ்கிருத் ஹிதகாரிணி சபை",
               "en": "Bahishkrit Hitakarini Sabha founded"},
     "1924", {"ta": "அம்பேத்கர் மும்பையில் நிறுவிய அமைப்பு. அதன் "
                    "முழக்கமே 'கல்வி கற்போம், போராடுவோம், ஒன்றுபடுவோம்'.",
              "en": "The organisation Ambedkar founded in Bombay. Its motto "
                    "was 'educate, agitate, organise'."}),
    ("29-08", {"ta": "வரைவுக் குழுத் தலைவர்", "en": "Chair of the Drafting Committee"},
     "1947", {"ta": "அரசியலமைப்பு வரைவுக் குழுவின் தலைவராக அம்பேத்கர் "
                    "தேர்ந்தெடுக்கப்பட்ட நாள்.",
              "en": "The day Ambedkar was elected chairman of the committee "
                    "that drafted the Constitution."}),
    ("24-09", {"ta": "பூனா ஒப்பந்தம்", "en": "The Poona Pact"},
     "1932", {"ta": "ஒடுக்கப்பட்டோருக்கான அரசியல் பிரதிநிதித்துவம் குறித்து "
                    "அம்பேத்கருக்கும் காந்திக்கும் இடையே கையெழுத்தான ஒப்பந்தம்.",
              "en": "The pact signed between Ambedkar and Gandhi on political "
                    "representation for the depressed classes."}),
    ("13-10", {"ta": "யேவோலா அறிவிப்பு", "en": "The Yeola declaration"},
     "1935", {"ta": "'நான் இந்துவாகப் பிறந்தேன், அது என் கையில் இல்லை; "
                    "ஆனால் இந்துவாக இறக்கமாட்டேன்' என்று அறிவித்த நாள்.",
              "en": "The day Ambedkar declared: 'I was born a Hindu, that was "
                    "not in my hands; but I will not die a Hindu.'"}),
    ("14-10", {"ta": "தம்மச் சக்கரப் பிரவர்த்தன் தினம்",
               "en": "Dhamma Chakra Pravartan Din"},
     "1956", {"ta": "நாக்பூர் தீட்சாபூமியில் அம்பேத்கர் சுமார் 3,65,000 "
                    "பேருடன் புத்தம், தம்மம், சங்கம் சரணடைந்த நாள்.",
              "en": "The day Ambedkar took refuge in the Buddha, the Dhamma "
                    "and the Sangha at Deekshabhoomi, Nagpur, with about "
                    "365,000 people."}),
    ("25-11", {"ta": "அரசியலமைப்பு அவையில் இறுதி உரை",
               "en": "The final speech to the Constituent Assembly"},
     "1949", {"ta": "'அரசியல் ஜனநாயகத்துடன் நிறுத்திக்கொள்ளக் கூடாது; "
                    "சமூக ஜனநாயகமும் வேண்டும்' என்று அம்பேத்கர் "
                    "எச்சரித்த உரை.",
              "en": "The speech in which Ambedkar warned that political "
                    "democracy is not enough without social democracy."}),
    ("26-11", {"ta": "அரசியலமைப்பு தினம்", "en": "Constitution Day"},
     "1949", {"ta": "அரசியலமைப்பு அவை அரசியலமைப்பை ஏற்றுக்கொண்ட நாள்.",
              "en": "The day the Constituent Assembly adopted the "
                    "Constitution."}, "2025-11-26"),
    ("06-12", {"ta": "மகாபரிநிர்வாண தினம்", "en": "Mahaparinirvan Din"},
     "1956", {"ta": "பாபாசாகேப் அம்பேத்கர் நினைவு நாள்.",
              "en": "The day Babasaheb Ambedkar died."}),
    ("25-12", {"ta": "மனுஸ்மிருதி எரிப்பு நாள்", "en": "Manusmriti Dahan Din"},
     "1927", {"ta": "சாதிய நூலை அம்பேத்கர் பொதுவெளியில் எரித்த நாள்.",
              "en": "The day Ambedkar publicly burned the caste text."}),
    ("26-12", {"ta": "அன்னை மீனாம்பாள் சிவராஜ் பிறந்த நாள்",
               "en": "Annai Meenambal Sivaraj's birthday"},
     "1904", {"ta": "பட்டியலின மக்களின் முதல் பெண் தலைவர்; "
                    "அம்பேத்கருக்கு 'பாபாசாகேப்' என்ற பெயரைச் சூட்டியவர்.",
              "en": "The first woman leader of the Scheduled Castes, who gave "
                    "Ambedkar the name Babasaheb."}, "annai-meenambal-sivaraj"),
]

# The making of the Constitution, as dates and figures. Every number here is
# from the Constituent Assembly's own record.
CONSTITUTION = [
    ("1946-12-09", {"ta": "அரசியலமைப்பு அவையின் முதல் கூட்டம்",
                    "en": "The Constituent Assembly first sits"}),
    ("1947-08-29", {"ta": "வரைவுக் குழு அமைக்கப்பட்டது; அம்பேத்கர் தலைவர்",
                    "en": "The Drafting Committee is formed, with Ambedkar as chairman"}),
    ("1949-11-25", {"ta": "அம்பேத்கரின் இறுதி உரை",
                    "en": "Ambedkar's final speech to the Assembly"}),
    ("1949-11-26", {"ta": "அரசியலமைப்பு ஏற்கப்பட்டது",
                    "en": "The Constitution is adopted"}),
    ("1950-01-26", {"ta": "அரசியலமைப்பு நடைமுறைக்கு வந்தது",
                    "en": "The Constitution comes into force"}),
]

CONST_STATS = [
    ("2 : 11 : 18", {"ta": "ஆண்டு : மாதம் : நாள், அவை எடுத்துக்கொண்ட காலம்",
                     "en": "years : months : days the Assembly took"}),
    ("141", {"ta": "வரைவுக் குழு கூடிய நாட்கள்",
             "en": "days the Drafting Committee sat"}),
    ("395", {"ta": "இறுதி வரைவின் பிரிவுகள்",
             "en": "articles in the final draft"}),
    ("8", {"ta": "அட்டவணைகள்", "en": "schedules"}),
]

BUDDHA_WORD = {"ta": "\u0baa\u0bc1\u0ba4\u0bcd\u0ba4\u0bb0\u0bcd", "en": "the Buddha"}

DEFAULT_OG = "/assets/img/hero/hero-1-dusk.jpg"

# The cover changes each day. Index is day-of-year modulo the set, so it is
# deterministic (same image for every visitor on a given day) and needs no
# rebuild. object-position is per image because the subject sits differently in
# each frame; the scrim is heavy enough on the left that the copy stays legible
# over all of them (measured, see README).
# (file, object-position, alt, what it is, where, photographer + licence)
HEROES = [
    ("/assets/img/hero/hero-1-dusk.jpg", "64% 42%",
     "அந்தி வானுக்கு எதிரே புத்தர் சிலையின் பக்கவாட்டு நிழலுரு",
     "அந்தி வானில் புத்தர்", "பொரோபுதூர், ஜாவா",
     "Photo Dharma &middot; CC BY 2.0"),
    ("/assets/img/hero/hero-2-sanchi.jpg", "58% 55%",
     "சாஞ்சி பெருந்தூபியும் அதன் தோரண வாயிலும்",
     "சாஞ்சி பெருந்தூபி", "மத்தியப் பிரதேசம், கி.மு. 3ஆம் நூற்றாண்டு",
     "Bernard Gagnon &middot; CC BY-SA 3.0"),
    ("/assets/img/hero/hero-3-galvihara.jpg", "62% 45%",
     "பாறையில் செதுக்கப்பட்ட சயன புத்தர் சிலை",
     "கல் விஹாரை, சயன புத்தர்", "பொலன்னறுவை, இலங்கை, 12ஆம் நூற்றாண்டு",
     "Philip Nalangan &middot; CC BY 4.0"),
    ("/assets/img/hero/hero-4-dusk-figures.jpg", "60% 50%",
     "அந்தி வானில் புத்தர் சிலையும் அமர்ந்திருப்பவரும் நிழலுருவாக",
     "அந்தி வேளையில் தியானம்", "புத்தர் சிலைக்கு எதிரே",
     "Enrique Alabort &middot; CC BY 3.0"),
    ("/assets/img/hero/hero-5-ajanta.jpg", "55% 45%",
     "குகைக் கோயிலில் செதுக்கப்பட்ட புத்தர் சிற்பம்",
     "எல்லோரா குகைச் சிற்பம்", "அவுரங்காபாத், மகாராஷ்டிரா",
     "Karthikeyan.pandian &middot; CC BY-SA 3.0"),
]

# The three refuges. Kept as text, not the old 264px banner image, so it stays
# crisp, selectable and readable by assistive technology.
#
# The refuge words end in the Pali niggahita, not a plain Tamil ம். Buddhaṃ is
# said buddhaṅ, so it is written புத்தங். The ordinary Tamil nouns elsewhere on
# the site keep their ம்: this is the recital, and it is spelled as it is said.
TISARANA = [
    ("புத்தங்", "சரணங் கச்சாமி"),
    ("தம்மங்", "சரணங் கச்சாமி"),
    ("சங்கங்", "சரணங் கச்சாமி"),
]


# ==========================================================================
# Chrome
# ==========================================================================

def asset(path):
    """Asset URL with a content fingerprint, so a changed file busts its cache."""
    f = os.path.join(ROOT, path.lstrip("/"))
    try:
        import hashlib
        with open(f, "rb") as fh:
            return f"{path}?v={hashlib.sha1(fh.read()).hexdigest()[:8]}"
    except FileNotFoundError:
        return path


def esc(s):
    """Escape for an HTML attribute. Post titles and bodies contain quotes."""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _nav_active(path, href):
    if href == "/kathai/":
        return path.startswith("/kathai/")
    if href == "/resources.html":
        return path == "/resources.html" or path in [r[0] for r in RESOURCES]
    return path == href


def title_trim(t, limit=58):
    """Keep <title> inside what a result page will actually show."""
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) <= limit:
        return t
    cut = t[:limit].rsplit(" ", 1)[0].rstrip(" ,.;:-")
    return (cut or t[:limit]) + "\u2026"


def head(title, title_alt, desc, path, L, og_image=None, jsonld=None,
         noindex=False, alt_path=None):
    """`path` is the canonical (unprefixed) path; `alt_path` overrides the
    other language's path when it is not a straight mirror."""
    nav = "".join(
        f'<a href="{u(href, L)}"'
        + (' aria-current="page"' if _nav_active(path, href) else "")
        + f">{ta if L == 'ta' else en}</a>"
        for href, ta, en in NAV
    )
    other = LANGS[L]["other"]
    other_path = u(alt_path or path, other)
    switch = (
        f'<a class="nd-lang" href="{other_path}" hreflang="{other}" '
        f'lang="{LANGS[other]["html"]}" aria-label="{U("switch_aria", L)}">'
        f'{icon("globe", 16)}<span>{LANGS[L]["other_name"]}</span></a>'
    )
    alts = "".join(
        f'\n<link rel="alternate" hreflang="{code}" href="{BASE}{u(alt_path or path, code) if code != L else u(path, L)}">'
        for code in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{u(path, DEFAULT_LANG)}">' 
    og = BASE + (og_image or DEFAULT_OG)
    robots = ("noindex, follow" if noindex else
              "index, follow, max-image-preview:large, max-snippet:-1")
    brand = SITE_FULL if L == "ta" else SITE_EN_FULL
    short = esc(title_trim(title))
    desc = esc(desc)
    # the alternate-language label is useful on section pages and only noise on
    # long article titles, where it pushes the brand out of the snippet
    page_title = (f"{short} · {brand}" if title_alt is None
                  else f"{short} · {brand} | {esc(title_alt)}")
    blocks = ""
    for block in (jsonld or []):
        blocks += ('\n<script type="application/ld+json">'
                   + json.dumps(block, ensure_ascii=False, separators=(",", ":"))
                   + "</script>")
    return f"""<!doctype html>
<html lang="{LANGS[L]["html"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}{u(path, L)}">{alts}
<meta name="robots" content="{robots}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{brand}">
<meta property="og:locale" content="{LANGS[L]["og"]}">
<meta property="og:title" content="{title} · {brand}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}{u(path, L)}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} · {brand}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og}">
<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" href="/assets/img/logo-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0c7a43">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{asset("/assets/css/canopy.css")}">
<link rel="stylesheet" href="{asset("/assets/css/nila.css")}">
<noscript><style>.nd-tabs__list{{display:none}}.nd-tabs__panel[hidden]{{display:block}}
.nd-more{{display:table-row!important}}.nd-timeline .nd-more{{display:list-item!important}}</style></noscript>{blocks}
</head>
<body class="cm-root cm-register--employee">
<a class="nd-skip" href="#main">{U("skip", L)}</a>

<header class="nd-topbar">
  <div class="nd-shell nd-topbar__inner">
    <a class="nd-brand" href="{u("/index.html", L)}">
      {BRAND_MARK}
      <span class="nd-brand__text">
        <span class="nd-brand__name">{SITE_FULL if L == "ta" else SITE_EN_FULL}</span>
        <span class="nd-brand__sub">{SITE_EN_FULL if L == "ta" else SITE}</span>
      </span>
    </a>
    <button class="nd-navtoggle" type="button" aria-expanded="false" aria-controls="nd-nav"
            aria-label="{U("menu", L)}" data-navtoggle>
      {icon('menu', 18)} <span>{U("menu", L)}</span>
    </button>
    <nav class="nd-nav" id="nd-nav" aria-label="{U("mainnav", L)}">{nav}</nav>
    {switch}
  </div>
</header>

<main id="main">
"""


def crumbs(trail, L):
    """trail: [(canonical href or None, label)], Home is prepended."""
    full = [("/index.html", U("home", L))] + trail
    parts = []
    for i, (href, label) in enumerate(full):
        last = i == len(full) - 1
        if last or not href:
            parts.append(f'<li><span aria-current="page">{label}</span></li>')
        else:
            parts.append(f'<li><a href="{u(href, L)}">{label}</a></li>')
    return (f'<nav class="nd-breadcrumb" aria-label="{U("breadcrumb", L)}"><ol>'
            + "".join(parts) + "</ol></nav>")


def crumb_ld(trail, L):
    full = [("/index.html", U("home", L))] + trail
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": label,
             **({"item": BASE + u(href, L)} if href else {})}
            for i, (href, label) in enumerate(full)
        ],
    }


ORG_LD = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": BASE + "/#organization",
    "name": SITE_FULL,
    "alternateName": [SITE_EN_FULL, SITE_EN, SITE],
    "url": BASE + "/",
    "logo": {"@type": "ImageObject", "url": BASE + "/assets/img/logo-512.png",
             "width": 512, "height": 512},
    "slogan": f"{MOTTO_EN}. {MOTTO_LINE_EN}",
    "knowsLanguage": ["ta", "en"],
    "email": EMAIL,
    "foundingDate": "2012",
    "areaServed": "Tamil Nadu, India",
    "address": {"@type": "PostalAddress",
                "streetAddress": VENUE_STREET,
                "addressLocality": VENUE_CITY,
                "addressRegion": "Tamil Nadu",
                "postalCode": VENUE_PIN,
                "addressCountry": "IN"},
    "location": VENUE_LD,
    "hasMap": MAPS_URL.replace("&amp;", "&"),
    "sameAs": [u for u, _ in SOCIAL],
    "description": ("சுதந்திரம், சமத்துவம், சகோதரத்துவம் காட்டும் தம்மப்பாதையில் "
                    "பயணிக்கும் பௌத்த சங்கம். 2012 முதல் ஒவ்வொரு பௌர்ணமியிலும் "
                    "சென்னையில் கூடி வருகிறோம்."),
}


def faq_ld(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }


def faq_block(title, pairs, L, note=None):
    items = "".join(
        f'<div class="nd-faq__item"><h3>{q}</h3><p>{a}</p></div>' for q, a in pairs
    )
    extra = (f'<p class="cm-body-sm cm-text-muted" style="margin-top:18px">{note}</p>'
             if note else "")
    return f"""
<section class="nd-section nd-faqband" aria-labelledby="faq-head">
  <div class="nd-shell">
    <div class="nd-sechead"><div><h2 id="faq-head">{title}</h2></div></div>
    <div class="nd-faq nd-reading">{items}</div>{extra}
  </div>
</section>
"""


def related(title, links, L):
    """links: [(href, label, sub)]"""
    cards = "".join(
        f'<a class="cm-card nd-related__card" href="{u(h, L)}">'
        f'<span class="nd-related__label">{lab}</span>'
        f'<span class="nd-related__sub">{sub}</span>'
        f'<span class="nd-related__go">{icon("arrow", 16)}</span></a>'
        for h, lab, sub in links
    )
    return f"""
<section class="nd-section nd-section--tight" aria-labelledby="rel-head">
  <div class="nd-shell">
    <div class="nd-sechead"><div><h2 id="rel-head">{title}</h2></div></div>
    <div class="nd-related">{cards}</div>
  </div>
</section>
"""


def footer(L):
    def col(items):
        return "".join(f'<li><a href="{u(h, L)}">{lab}</a></li>'
                       for h, lab, *_r in items)
    social = "".join(f'<li><a href="{u}" rel="me noopener">{n}</a></li>' for u, n in SOCIAL)
    return f"""</main>

<footer class="nd-footer">
  <div class="nd-shell">
    <div class="nd-footer__grid">
      <div>
        <div class="nd-footer__brand">{FOOTER_MARK}<strong>{SITE_FULL if L == "ta" else SITE_EN_FULL}</strong></div>
        <p class="nd-footer__about">{U("footer_blurb", L)}</p>
        <p class="nd-footer__about" style="margin-top:14px">
          <a href="{u("/kathai/", L)}">{U("kathai_title", L)}</a>
        </p>
      </div>
      <div>
        <h2 class="nd-footer__head">{U("pages", L)}</h2>
        <ul>{col([(h, ta if L == "ta" else en) for h, ta, en in NAV[1:6]])}</ul>
      </div>
      <div>
        <h2 class="nd-footer__head">{U("resources", L)}</h2>
        <ul>{col(res_items(L))}</ul>
      </div>
      <div>
        <h2 class="nd-footer__head">{U("contact", L)}</h2>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>
            <address style="font-style:normal">
              {U("venue", L)}<br>{U("venue_addr", L)}
            </address>
            <a href="{MAPS_URL}" rel="noopener">{U("map", L)}</a>
          </li>
          {social}
        </ul>
      </div>
    </div>
    <div class="nd-footer__bar">
      <span>&copy; 2026 {SITE_FULL} &middot; {SITE_EN_FULL}</span>
      <span>{MOTTO_EN} &middot; {MOTTO_LINE_EN}</span>
      <span class="nd-footer__lang">
        <a href="{u("/index.html", LANGS[L]["other"])}" hreflang="{LANGS[L]["other"]}"
           lang="{LANGS[LANGS[L]["other"]]["html"]}">
          {icon("globe", 14)} {LANGS[L]["other_name"]}</a>
      </span>
    </div>
  </div>
</footer>

<script src="{asset("/assets/js/site.js")}" defer></script>
</body>
</html>
"""


def pagehead(eyebrow, title_ta, lede, trail, L, extra=""):
    return f"""<section class="nd-pagehead">
  <div class="nd-shell">
    {crumbs(trail, L)}
    <p class="nd-eyebrow">{eyebrow}</p>
    <h1>{title_ta}</h1>
    <p>{lede}</p>{extra}
  </div>
</section>
"""


def fpath(path, L):
    """File on disk for a canonical path in language L."""
    full = LANGS[L]["prefix"] + path
    if full.endswith((".html", ".ics", ".xml", ".txt")):
        return full
    return full.rstrip("/") + "/index.html"


WRITTEN = set()


def sweep():
    """Delete generated pages that this run did not write.

    Without this, a story withheld by the release gate would keep being served
    from the previous build. Only generated output is touched: HTML at the
    root and under the generated directories, plus the sitemap and robots.
    Source, data, tools and assets are never considered."""
    roots = ("en", "kathai", "pathivu")
    stale = []
    for f in glob.glob("*.html") + [g for r in roots
                                    for g in glob.glob(f"{r}/**/*.html", recursive=True)]:
        if os.path.abspath(f) not in WRITTEN:
            stale.append(f)
    for f in stale:
        os.remove(f)
    # drop directories the sweep emptied
    for r in roots:
        for d, _, _ in sorted(os.walk(r, topdown=False), reverse=True):
            if os.path.isdir(d) and not os.listdir(d):
                os.rmdir(d)
    return stale


def write(name, html):
    p = os.path.join(ROOT, name.lstrip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    WRITTEN.add(os.path.abspath(p))
    return len(html)


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as f:
        return json.load(f)


TA_MONTHS = ["ஜனவரி", "பிப்ரவரி", "மார்ச்", "ஏப்ரல்", "மே", "ஜூன்",
             "ஜூலை", "ஆகஸ்ட்", "செப்டம்பர்", "அக்டோபர்", "நவம்பர்", "டிசம்பர்"]


EN_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]


def fmt_date(iso, L):
    y, m, d = iso.split("-")
    if L == "ta":
        return f"{int(d)} {TA_MONTHS[int(m) - 1]} {y}"
    return f"{int(d)} {EN_MONTHS[int(m) - 1]} {y}"


def post_title(post, L):
    return post.get("title_en") or post["title"] if L == "en" else post["title"]


def post_text(post, L):
    return post.get("text_en") or post["text"] if L == "en" else post["text"]


def post_desc(post, L):
    """Meta description for a post. Some archive posts are a caption and a
    photograph, so there is not always 155 characters of prose to use."""
    body = excerpt(post_text(post, L), 155).strip()
    if len(body) >= 60:
        return body
    when = fmt_date(post["date"], L)
    lead = post_title(post, L)
    tail = ({"ta": f"{when} அன்று நிலாதம்மா பதிவு செய்த நிகழ்வு. "
                   f"அசோக் நகர் புத்த விஹார், சென்னை.",
             "en": f"An event recorded by Niladhamma on {when}. "
                   f"Ashok Nagar Buddha Vihar, Chennai."})[L]
    return f"{lead}. {body} {tail}".replace("  ", " ").strip()


STRIP_TAGS = re.compile(r"<[^>]+>")
BARE_URL = re.compile(r"(https?://[^\s<>\"]+[^\s<>\".,;:)])")
TAMIL = re.compile(r"[஀-௿]")


# ==========================================================================
# Post bodies
#
# The archive arrives as Blogger markup: loose divs, runs of <br>, empty
# paragraphs left behind by the editor, and every photograph wrapped in a
# one-cell table whose second row is the caption, usually empty. Shipping that
# as-is drew hairlines where the empty caption cells sat and left the pictures
# at whatever width the editor happened to save.
#
# Each body is parsed once into blocks and the page is built from those:
#   ("p",   inline html)
#   ("ul",  [inline html, ...])
#   ("fig", src, caption inline html)
# The Tamil original is the only thing parsed. The English page reuses its
# figures and interleaves them with the translated paragraphs.
# ==========================================================================

INLINE_KEEP = {"a", "b", "strong", "i", "em", "u"}
FLUSH_TAGS = {"p", "div", "tr", "li", "h1", "h2", "h3", "h4", "blockquote"}


class _Blogger(HTMLParser):
    """Blogger body markup to blocks."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.buf, self.items, self.table = [], [], None, 0

    def _flush(self):
        while self.buf and self.buf[-1] == "<br>":
            self.buf.pop()
        s = "".join(self.buf).strip()
        self.buf = []
        if not STRIP_TAGS.sub("", s).replace("\xa0", " ").strip():
            return
        if self.items is not None:
            self.items.append(s)
        elif self.table and self.blocks and self.blocks[-1][0] == "fig" \
                and not self.blocks[-1][2]:
            # The row under a photograph is its caption, not a paragraph.
            self.blocks[-1] = ("fig", self.blocks[-1][1], s)
        else:
            self.blocks.append(("p", s))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "img":
            self._flush()
            if a.get("src"):
                self.blocks.append(("fig", a["src"], ""))
        elif tag == "br":
            # One break is a line inside the paragraph; two end it. Blogger
            # uses both, and the difference is what the writer meant.
            if self.buf and self.buf[-1] == "<br>":
                self._flush()
            elif self.buf:
                self.buf.append("<br>")
        elif tag == "table":
            self._flush()
            self.table += 1
        elif tag in ("ul", "ol"):
            self._flush()
            self.items = []
        elif tag == "a":
            href = a.get("href", "").strip()
            rel = ' rel="nofollow noopener"' if "://" in href else ""
            self.buf.append(f'<a href="{esc(href)}"{rel}>' if href else "<a>")
        elif tag in INLINE_KEEP:
            self.buf.append(f"<{tag}>")
        elif tag in FLUSH_TAGS:
            self._flush()

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in INLINE_KEEP:
            self.buf.append(f"</{tag}>")
        elif tag in ("ul", "ol"):
            self._flush()
            if self.items:
                self.blocks.append(("ul", self.items))
            self.items = None
        elif tag == "table":
            self._flush()
            self.table = max(0, self.table - 1)
        elif tag in FLUSH_TAGS or tag in ("tbody", "td"):
            self._flush()

    def handle_data(self, data):
        self.buf.append(esc(data))


def parse_body(html):
    p = _Blogger()
    p.feed(html)
    p.close()
    p._flush()
    return p.blocks


def compose_en(blocks, paras, caps):
    """The English body: translated prose, the sangha's own photographs.

    Only the words are rewritten. Each picture keeps the share of the post it
    sat at in the original, which is the one measure that survives a rewrite
    with a different paragraph count."""
    paras = [x for x in paras if x.strip()]
    words = [len(x.split()) for x in paras]
    total = sum(words) or 1

    seen, shares = 0, []
    all_words = sum(len(STRIP_TAGS.sub(" ", b[1]).split())
                    for b in blocks if b[0] == "p") or 1
    for b in blocks:
        if b[0] == "fig":
            shares.append((b, seen / all_words))
        elif b[0] == "p":
            seen += len(STRIP_TAGS.sub(" ", b[1]).split())

    at = collections.defaultdict(list)
    for (_, src, cap), share in shares:
        # Tamil captions with no translation are dropped rather than left
        # sitting in the middle of an English page.
        raw = STRIP_TAGS.sub("", cap).replace("\xa0", " ").strip()
        cap_en = caps.get(cap.strip()) or caps.get(raw) or \
            ("" if TAMIL.search(raw) else raw)
        target, run = len(paras), 0
        for i, w in enumerate(words):
            run += w
            if run / total >= share:
                target = i + 1
                break
        at[target].append(("fig", src, esc(cap_en) if cap_en else ""))

    out = []
    for i, para in enumerate(paras):
        out.extend(at.get(i, []))
        text = BARE_URL.sub(r'<a href="\1" rel="nofollow noopener">\1</a>',
                            esc(para))
        out.append(("p", text))
    out.extend(at.get(len(paras), []))
    return out


# ==========================================================================
# Photographs
#
# Every archive image is a local file, so its true pixel size is knowable at
# build time. That single fact does the work here: it fixes the page against
# reflow as the photographs arrive, it sizes the picture rows, and it decides
# which photographs share a row.
# ==========================================================================

TILE_W = 720            # the display copy; the original is what the viewer opens
ARTICLE_W = 748         # the article card's content box, in pixels
GALLERY_GAP = 10
GALLERY_ROW = 296       # the height a row of photographs aims for
FIG_MAX_H = 560         # a standing photograph should not fill the screen

# Measured sizes are cached to data/img_sizes.json and that file is committed.
# The deploy host has no Pillow, and without a size every ratio silently became
# 4:3: portrait photographs rendered cropped to landscape and no image carried
# width or height. Pillow is now a convenience for measuring new photographs
# locally, not something the build depends on.
SIZE_CACHE = "img_sizes.json"
try:
    _sizes = {k: tuple(v) for k, v in load(SIZE_CACHE).items()}
except (FileNotFoundError, ValueError):
    _sizes = {}
_measured = False


def img_size(src):
    """(width, height) of a local image, or None when it cannot be read."""
    global _measured
    if src not in _sizes:
        size = None
        if src.startswith("/"):
            try:
                from PIL import Image
                with Image.open(os.path.join(ROOT, src.lstrip("/"))) as im:
                    size = im.size
            except Exception:
                size = None
        _sizes[src] = size
        _measured = _measured or size is not None
    return _sizes[src]


def save_sizes():
    """Write the cache back when Pillow measured something new."""
    if not _measured:
        return 0
    known = {k: list(v) for k, v in sorted(_sizes.items()) if v}
    with open(os.path.join(DATA, SIZE_CACHE), "w", encoding="utf-8") as fh:
        json.dump(known, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return len(known)


def ratio(src):
    s = img_size(src)
    return (s[0] / s[1]) if s and s[1] else 4 / 3


def tile_src(src):
    """The display copy of a photograph, or the original when there is none.

    A gallery row paints a picture at 190px to 750px. Serving the 1400px
    original for that costs about a quarter of a megabyte each, and a post with
    eight photographs pays it eight times."""
    t = src.replace("/pathivu/", "/pathivu/tile/")
    return t if t != src and os.path.exists(os.path.join(ROOT, t.lstrip("/"))) else src


def make_tiles(posts):
    """Write any missing display copies. Runs once; later builds find them all
    and do nothing. Without Pillow the originals are used and the pages are
    heavier, but nothing breaks."""
    try:
        from PIL import Image
    except ImportError:
        return 0
    out = os.path.join(ROOT, "assets", "img", "pathivu", "tile")
    os.makedirs(out, exist_ok=True)
    made = 0
    for src in sorted({i for p in posts for i in p["imgs"]}):
        if "/pathivu/" not in src:
            continue
        dst = os.path.join(out, os.path.basename(src))
        if os.path.exists(dst):
            continue
        try:
            with Image.open(os.path.join(ROOT, src.lstrip("/"))) as im:
                im = im.convert("RGB")
                if im.width > TILE_W:
                    im = im.resize((TILE_W, round(im.height * TILE_W / im.width)),
                                   Image.LANCZOS)
                im.save(dst, "JPEG", quality=76, optimize=True, progressive=True)
            made += 1
        except Exception:
            continue
    return made


def plain(cap):
    """Caption text with its inline markup removed. Already entity-escaped by
    the parser, so it is safe in an attribute."""
    return STRIP_TAGS.sub("", cap).strip()


def _img(src, cap, sizes, cls=""):
    w, h = img_size(src) or (0, 0)
    tile = tile_src(src)
    srcset = (f' srcset="{tile} {TILE_W}w, {src} {w}w" sizes="{sizes}"'
              if tile != src and w > TILE_W else "")
    dims = f' width="{w}" height="{h}"' if w and h else ""
    klass = f' class="{cls}"' if cls else ""
    return (f'<img{klass} src="{tile}"{srcset}{dims} alt="{plain(cap)}" '
            f'loading="lazy" decoding="async">')


def _shot(src, cap, n, total, L, sizes, style, cls=""):
    """One photograph, as a link to the full picture. Without JavaScript that
    link simply opens it, which is the honest fallback when no viewer loads."""
    return (f'<a class="nd-shot{cls}" href="{src}" style="{style}" data-shot'
            f' data-cap="{plain(cap)}"'
            f' aria-label="{U("photo_of", L).format(n=n, t=total)}">'
            f'{_img(src, cap, sizes, "nd-shot__img")}'
            f'<span class="nd-shot__zoom" aria-hidden="true">'
            f'{icon("expand", 15)}</span></a>')


def _rows(figs):
    """Pack photographs the way a picture desk would: each row fills the
    width, and the aspect ratios decide who gets how much of it.

    Widths are emitted as flex-grow rather than pixels, so the packing that was
    computed at 748px holds its proportions at every screen size."""
    rows, row, span = [], [], 0.0
    for f in figs:
        row.append(f)
        span += ratio(f[1])
        free = ARTICLE_W - GALLERY_GAP * (len(row) - 1)
        if free / span <= GALLERY_ROW or len(row) == 3:
            rows.append((row, 0.0))
            row, span = [], 0.0
    if row:
        # A short last row would stretch its photographs to an absurd height.
        # Grown spacers either side hold it to the height of the rest and keep
        # it centred. They occupy two gaps of their own, hence len(row) + 1.
        free = ARTICLE_W - GALLERY_GAP * (len(row) + 1)
        rows.append((row, max(0.0, free / GALLERY_ROW - span)))
    return rows


def render_figures(figs, L, first, total):
    """A run of uncaptioned photographs becomes a gallery; a captioned one
    stands on its own, because a caption needs a line of its own to read."""
    if len(figs) == 1:
        src, cap = figs[0][1], figs[0][2]
        r = round(ratio(src), 4)
        wide = min(ARTICLE_W, round(FIG_MAX_H * r))
        # A standing photograph would otherwise run past the fold, so the box
        # is capped by height rather than width. The cap sits on the figure so
        # that the caption keeps the same edges as the picture above it.
        shot = _shot(src, cap, first, total, L,
                     f"(max-width: 900px) 92vw, {wide}px",
                     f"--ar:{r}", cls=" nd-shot--solo")
        capt = f"<figcaption>{cap}</figcaption>" if cap else ""
        return (f'<figure class="nd-fig" style="max-width:min(100%,{wide}px)">'
                f'{shot}{capt}</figure>')

    sizes = f"(max-width: 640px) 92vw, {round(ARTICLE_W / 2)}px"
    out, n = [], first
    for row, spacer in _rows(figs):
        # Half the slack on each side, so a short last row sits centred under
        # the full ones rather than hanging off the left edge.
        gap = (f'<i class="nd-gallery__gap" style="flex-grow:'
               f'{round(spacer / 2, 4)}" aria-hidden="true"></i>') if spacer else ""
        cells = [gap]
        for f in row:
            r = round(ratio(f[1]), 4)
            cells.append(_shot(f[1], f[2], n, total, L, sizes,
                               style=f"--ar:{r};flex-grow:{r}"))
            n += 1
        cells.append(gap)
        out.append(f'<div class="nd-gallery__row">{"".join(cells)}</div>')
    return (f'<div class="nd-gallery" role="group" '
            f'aria-label="{U("viewer", L)}">{"".join(out)}</div>')


def render_body(blocks, L):
    """Blocks to page markup. The opening paragraph is set as a standfirst;
    photographs group into rows unless a caption separates them."""
    total = sum(1 for b in blocks if b[0] == "fig")
    out, i, lead, shot = [], 0, True, 1
    while i < len(blocks):
        if blocks[i][0] == "fig":
            j = i
            while j < len(blocks) and blocks[j][0] == "fig" and not blocks[j][2]:
                j += 1
            run = blocks[i:j] if j > i else blocks[i:i + 1]
            out.append(render_figures(run, L, shot, total))
            shot += len(run)
            i += len(run)
            continue
        kind, payload = blocks[i][0], blocks[i][1]
        if kind == "p":
            klass = ' class="nd-prose__lede"' if lead else ""
            out.append(f"<p{klass}>{payload}</p>")
            lead = False
        else:
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in payload) + "</ul>")
        i += 1
    return "".join(out)


def post_body(post, L):
    if L == "en" and post.get("blocks_en"):
        return render_body(post["blocks_en"], L)
    return render_body(post["blocks"], L)


def read_minutes(post, L):
    """Tamil runs fewer, longer words than English; 170 a minute is the figure
    the sangha's own readings come out at."""
    return max(1, round(len(post_text(post, L).split()) / 170))


def story_field(s, key, L, en_data):
    """English where a translation exists, Tamil otherwise. A collection can be
    published before its translation is ready; the page says so."""
    if L == "ta" or not en_data:
        return s[key]
    e = en_data.get("stories", {}).get(str(s["day"]), {})
    return e.get(key, s[key])


def has_en(st, en_data):
    return bool(en_data) and str(st["day"]) in en_data.get("stories", {})


def ta_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {TA_MONTHS[int(m) - 1]} {y}"


def excerpt(text, n=150):
    t = re.sub(r"\s+", " ", text).strip().replace("…", "").strip(" .")
    return (t[:n].rsplit(" ", 1)[0] + "…") if len(t) > n else t





# ==========================================================================
# Pages
# ==========================================================================

def build_index(posts, peek_coll, peek_stories, peek_en, L):
    tisarana = ('<p class="nd-tisarana" lang="pi">'
                + "".join(f'<span><b>{a}</b> {b}</span>' for a, b in TISARANA)
                + "</p>")
    hero_script = (
        "(function(){var H=" + json.dumps([list(h) for h in HEROES], ensure_ascii=False)
        + ";var d=new Date();var doy=Math.floor((d-new Date(d.getFullYear(),0,0))/864e5);"
        "var h=H[doy%H.length];var i=document.getElementById('nd-hero-img');"
        "if(i&&i.getAttribute('src')!==h[0]){i.src=h[0];i.style.objectPosition=h[1];i.alt=h[2];"
        "var cp=document.getElementById('nd-hero-cap');if(cp){"
        "cp.children[0].innerHTML=h[3];cp.children[1].innerHTML=h[4];cp.children[2].innerHTML=h[5];}"
        "}})();")

    cards = "".join(f"""
      <a class="cm-card nd-mediacard" href="{u(post_url(x), L)}">
        <div class="nd-mediacard__media"><img src="{post_thumb(x)}" alt="" loading="lazy"></div>
        <div class="nd-mediacard__body">
          <p class="nd-mediacard__meta">{fmt_date(x['date'], L)}</p>
          <h3>{post_title(x, L)}</h3>
          <p class="nd-mediacard__excerpt">{excerpt(post_text(x, L), 105)}</p>
        </div>
      </a>""" for x in posts[:8])

    peek = "".join(
        f'<a class="nd-kathai__chip" '
        f'href="{u(story_url(peek_coll["slug"], st["day"]), L)}">'
        f'<img src="{st["icon"]}" alt="" loading="lazy" width="40" height="40">'
        f'<span><em>{peek_coll["month"][L]} {st["day"]}</em>'
        f'{story_field(st, "title", L, peek_en)}</span></a>'
        for st in peek_stories
    )
    res = "".join(
        f'<a class="cm-card nd-card" href="{u(h, L)}">'
        f'<div class="nd-card__icon">{icon(ic, 22)}</div><h3>{lab}</h3><p>{sub}</p></a>'
        for h, lab, ic, sub in res_items(L)
    )
    work = [
        ("/events.html", "moon", "work.pournami"),
        ("/matrimony.html", "heart", "work.marriage"),
        ("/about.html", "school", "work.school"),
        ("/events.html", "sparkle", "work.arts"),
        ("/certificate.html", "shield", "work.cert"),
        ("/writings.html", "book", "work.recover"),
    ]
    work_cards = "".join(
        f'<a class="cm-card nd-card" href="{u(href, L)}">'
        f'<div class="nd-card__icon">{icon(ic, 22)}</div>'
        f'<h3>{c(k + ".h", L)}</h3><p>{c(k + ".p", L)}</p></a>'
        for href, ic, k in work
    )

    return head(
        U("home", L), "Home" if L == "ta" else "\u0bae\u0bc1\u0b95\u0baa\u0bcd\u0baa\u0bc1",
        c("home.meta", L), "/index.html", L,
        jsonld=[ORG_LD, {
            "@context": "https://schema.org", "@type": "WebSite",
            "@id": BASE + "/#website", "url": BASE + "/",
            "name": SITE_FULL if L == "ta" else SITE_EN_FULL, "inLanguage": L,
            "publisher": {"@id": BASE + "/#organization"},
        }],
    ) + f"""
<figure class="nd-hero">
  <div class="nd-hero__media">
    <img id="nd-hero-img" src="{HEROES[0][0]}" alt="{HEROES[0][2]}"
         style="object-position:{HEROES[0][1]}" fetchpriority="high">
  </div>
  <figcaption class="nd-hero__cap" id="nd-hero-cap">
    <span class="nd-hero__capwhat">{HEROES[0][3]}</span>
    <span class="nd-hero__capwhere">{HEROES[0][4]}</span>
    <span class="nd-hero__capcredit">{HEROES[0][5]}</span>
  </figcaption>
  <script>{hero_script}</script>
  <div class="nd-hero__scrim"></div>
  <div class="nd-shell nd-hero__inner">
    <div class="nd-hero__id">
      <img class="nd-hero__logo" src="/assets/img/logo-192.png"
           width="88" height="88" alt="">
      <div>
        <h1 class="nd-hero__brandname">{SITE_FULL if L == "ta" else SITE_EN_FULL}</h1>
        <p class="nd-hero__motto">
          <span class="nd-hero__badge">{MOTTO_EN}</span>
          {MOTTO_LINE_EN}
        </p>
      </div>
    </div>
    <p class="nd-hero__quote">&ldquo;{TAGLINE if L == "ta" else TAGLINE_EN}&rdquo;</p>
    <p class="nd-hero__attrib">&ndash; {BUDDHA_WORD[L]} &middot; {TAGLINE_EN if L == "ta" else TAGLINE}</p>
    {tisarana}
    <p class="nd-hero__lede">{c("home.lede", L,
        link=f'<a href="{u("/events.html", L)}">{c("home.lede.link", L)}</a>')}</p>
    <div class="nd-hero__actions">
      <a class="cm-btn cm-btn--primary" href="{u("/kathai/", L)}">
        {c("home.cta1", L)} {icon('arrow', 18)}</a>
      <a class="cm-btn cm-btn--secondary" href="{u("/about.html", L)}">{c("home.cta2", L)}</a>
    </div>
  </div>
</figure>

<section class="nd-section nd-section--tight nd-well-band">
  <div class="nd-shell">
    <div class="nd-grid nd-grid--4">
      <a class="cm-card nd-stat" href="{u("/about.html", L)}">
        <span class="nd-stat__value">2012</span>
        <span class="nd-stat__label">{c("home.stat1", L)}</span>
      </a>
      <a class="cm-card nd-stat" href="{u("/events.html", L)}">
        <span class="nd-stat__value">178</span>
        <span class="nd-stat__label">{c("home.stat2", L)}</span>
      </a>
      <a class="cm-card nd-stat" href="{u("/kathai/", L)}">
        <span class="nd-stat__value">31</span>
        <span class="nd-stat__label">{c("home.stat3", L)}</span>
      </a>
      <a class="cm-card nd-stat" href="{u("/names.html", L)}">
        <span class="nd-stat__value">1,000+</span>
        <span class="nd-stat__label">{c("home.stat4", L)}</span>
      </a>
    </div>
  </div>
</section>

<section class="nd-section" aria-labelledby="kathai-head">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="kathai-head">{U("kathai_title", L)}</h2>
        <p>{c("home.kathai.sub", L)}</p>
      </div>
      <a class="cm-btn cm-btn--ghost cm-btn--sm" href="{u("/kathai/", L)}">
        {c("home.kathai.all", L)} {icon('arrow', 16)}</a>
    </div>
    <div class="nd-kathai__peek">{peek}</div>
  </div>
</section>

<section class="nd-section" aria-labelledby="work-head">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="work-head">{c("home.work.h", L)}</h2>
        <p>{c("home.work.sub", L)}</p>
      </div>
      <a class="cm-btn cm-btn--ghost cm-btn--sm" href="{u("/about.html", L)}">
        {c("home.work.readall", L)} {icon('arrow', 16)}</a>
    </div>
    <div class="nd-grid nd-grid--3">{work_cards}</div>
  </div>
</section>

<section class="nd-section nd-section--tight">
  <div class="nd-shell">
    <div class="cm-card nd-feature">
      <div class="nd-feature__media">
        <img src="/assets/img/full-moon-palm.jpg" alt="{c("home.moon.h", L)}" loading="lazy">
      </div>
      <div class="nd-feature__body">
        <p class="nd-eyebrow">{c("home.moon.eyebrow", L)}</p>
        <h2>{c("home.moon.h", L)}</h2>
        <p>{c("home.moon.p", L,
               link=f'<a href="{u(story_url("july", 6), L)}">{c("home.moon.link", L)}</a>')}</p>
        <p class="nd-row" style="margin-top:24px">
          <a class="cm-btn cm-btn--primary" href="{u("/events.html", L)}">{c("home.moon.cta", L)}</a>
          <a class="cm-btn cm-btn--ghost" href="{u("/writings.html", L)}">
            {U("writings", L)} {icon('arrow', 18)}</a>
        </p>
      </div>
    </div>
  </div>
</section>

<section class="nd-section" aria-labelledby="recent-head">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="recent-head">{c("home.recent.h", L)}</h2>
        <p>{c("home.recent.sub", L)}</p>
      </div>
      <a class="cm-btn cm-btn--ghost cm-btn--sm" href="{u("/writings.html", L)}">
        {U("read_all", L)} {icon('arrow', 16)}</a>
    </div>
    <div class="nd-grid nd-grid--4">{cards}
    </div>
  </div>
</section>

<section class="nd-section nd-well-band" aria-labelledby="res-head">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="res-head">{c("home.res.h", L)}</h2>
        <p>{c("home.res.sub", L)}</p>
      </div>
      <a class="cm-btn cm-btn--ghost cm-btn--sm" href="{u("/resources.html", L)}">
        {U("read_all", L)} {icon('arrow', 16)}</a>
    </div>
    <div class="nd-grid nd-grid--4">{res}</div>
  </div>
</section>
""" + footer(L)


ABOUT_FAQ = [
    ("பௌத்தர்கள் தமிழ்நாட்டில் இருக்கிறார்களா?",
     "இருக்கிறார்கள். நிலாதம்மா 2012 முதல் சென்னையில் ஒவ்வொரு "
     "பௌர்ணமி நாளிலும் குடும்பமாகக் கூடி வருகிறது. நூற்றுக்கணக்கான "
     "குடும்பங்கள் பௌத்தமேற்று, அரசிதழில் பதிவு செய்து, சமூகச் "
     "சான்றிதழ் பெற்று வலிமை பெற்றிருக்கின்றன."),
    ("பௌர்ணமி பௌத்தர்களுக்கானதா?",
     "ஆம். பௌர்ணமி பௌத்த மரபில் உபோசத நாள்; விழிப்புக்கும் தியானத்துக்கும் "
     "உரிய நாள். புத்தரின் பிறப்பு, ஞானம், முதல் உபதேசம், பரிநிர்வாணம் "
     "ஆகிய நிகழ்வுகள் முழுநிலவு நாட்களோடு இணைக்கப்படுகின்றன."),
    ("சங்கக் கூட்டத்தில் யார் பங்கேற்கலாம்?",
     "அனைவரும். முன்பதிவு தேவையில்லை. அசோக் நகர் புத்த விஹாரில் (15, 4வது "
     "அவென்யூ, டாக்டர் அம்பேத்கர் நகர், பிருந்தாவன் எக்ஸ்டென்ஷன், அசோக் "
     "நகர், சென்னை 600083) ஒவ்வொரு பௌர்ணமி நாளும் மாலை 6 மணி முதல் "
     "கூடுகிறோம். விபாசனா கூட்டுத் தியானத்திற்கு மட்டும் முன்பதிவு தேவை."),
    ("சங்கம் என்னென்ன செய்கிறது?",
     "தொடர் பௌர்ணமி கூட்டங்கள், பௌத்த மகாமங்கள திருமணங்கள், பாபாசாகேப் "
     "அம்பேத்கர் இரவுப் பாடசாலைகள், கலைப் பயிற்சிகள், பௌத்தமேற்பு "
     "நிகழ்வுகளை ஒருங்கிணைத்தல், சமூகச் சான்றிதழ் பெறுவதற்கான உதவி."),
]


def build_about(L):
    trail = [(None, NAV[1][1] if L == "ta" else NAV[1][2])]
    gal = [
        ("bodhi-tree-mahabodhi.jpg",
         {"ta": "போதி மரம், மகாபோதி விஹார், புத்தகயா",
          "en": "The Bodhi tree, Mahabodhi Temple, Bodh Gaya"}),
        ("first-sermon-relief.jpg",
         {"ta": "தம்மச் சக்கரம் உருட்டிய முதல் உபதேசம்",
          "en": "The first discourse, turning the wheel of Dhamma"}),
        ("buddhist-flag-dharmachakra.png",
         {"ta": "பௌத்தக் கொடி, தம்மச் சக்கரத்துடன்",
          "en": "The Buddhist flag, with the wheel of Dhamma"}),
        ("buddha-vihar-perambur-chennai.jpg",
         {"ta": "தென்னிந்திய புத்த விஹார், பெரம்பூர், சென்னை",
          "en": "South India Buddha Vihar, Perambur, Chennai"}),
        ("buddha-tamil-nadu-5c.jpg",
         {"ta": "புத்தர் சிலை, தமிழ்நாடு, ஐந்தாம் நூற்றாண்டு",
          "en": "Buddha figure, Tamil Nadu, 5th century"}),
        ("lion-capital-sarnath.jpg",
         {"ta": "அசோகர் சிங்க முகடு, சாரநாத்",
          "en": "The Ashoka lion capital, Sarnath"}),
        ("ambedkar-statue.jpg",
         {"ta": "பாபாசாகேப் Dr. B. R. அம்பேத்கர்",
          "en": "Babasaheb Dr B. R. Ambedkar"}),
        ("buddha-sarnath-park.jpg",
         {"ta": "புத்தர் சிலை, சாரநாத் புத்த பூங்கா",
          "en": "Buddha figure, Sarnath Buddha Park"}),
    ]
    figs = "".join(
        f'<figure><img src="/assets/img/{fn}" alt="{cap[L]}" loading="lazy">'
        f'<figcaption>{cap[L]}</figcaption></figure>' for fn, cap in gal)

    return head(
        NAV[1][1] if L == "ta" else NAV[1][2],
        NAV[1][2] if L == "ta" else NAV[1][1],
        c("about.meta", L), "/about.html", L,
        og_image="/assets/img/buddha-chola-nagapattinam.jpg",
        jsonld=[crumb_ld(trail, L), faq_ld(faq_for("about", L)), {
            "@context": "https://schema.org", "@type": "AboutPage",
            "url": BASE + u("/about.html", L), "inLanguage": L,
            "about": {"@id": BASE + "/#organization"},
        }],
    ) + pagehead(c("about.eyebrow", L), c("about.h1", L), c("about.lede", L),
                 trail, L) + f"""
<section class="nd-section">
  <div class="nd-shell">
    <div class="nd-grid nd-grid--aside">
      <div class="nd-prose">
        <p class="nd-prose__lede">{c("about.p1", L)}</p>
        <p>{c("about.p2", L,
               link=f'<a href="{u("/events.html", L)}">{c("about.p2.link", L)}</a>')}</p>

        <h2>{c("about.h.action", L)}</h2>
        <p>{c("about.p3", L,
               link1=f'<a href="{u("/certificate.html", L)}">{c("about.p3.link1", L)}</a>',
               link2=f'<a href="{u("/matrimony.html", L)}">{c("about.p3.link2", L)}</a>')}</p>

        <h2>{c("about.h.recover", L)}</h2>
        <p>{c("about.p4", L,
               link=f'<a href="{u("/kathai/", L)}">{c("about.p4.link", L)}</a>')}</p>
        <p>{c("about.p5", L)}</p>
        <p>{c("about.p6", L)}</p>
        <blockquote>{c("about.quote", L)}</blockquote>
      </div>

      <aside class="nd-stack-6">
        <div class="cm-card" style="overflow:hidden">
          <img src="/assets/img/buddha-chola-nagapattinam.jpg" loading="lazy"
               alt="{c("about.caption", L)}">
          <div style="padding:14px 16px;border-top:1px solid var(--cm-border-default)">
            <p class="cm-body-sm cm-text-muted" style="margin:0">{c("about.caption", L)}</p>
          </div>
        </div>

        <div class="cm-card nd-card">
          <p class="nd-eyebrow">{c("about.principles", L)}</p>
          <ul class="nd-tick">
            <li>{c("about.pr1", L)}</li>
            <li>{c("about.pr2", L)}</li>
            <li>{c("about.pr3", L)}</li>
            <li>{c("about.pr4", L)}</li>
          </ul>
        </div>

        <div class="nd-alert nd-alert--accent">
          {icon('map', 20)}
          <div>
            <p class="nd-alert__title">{c("about.where", L)}</p>
            <p><strong>{U("venue", L)}</strong><br>{U("venue_addr", L)}<br>
               {c("about.when", L)}</p>
            <p style="margin-top:10px">
              <a href="{MAPS_URL}" rel="noopener">{U("map", L)}</a> &middot;
              <a href="{u("/contact.html", L)}">{c("about.contactlink", L)}</a>
            </p>
          </div>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="nd-section nd-section--tight nd-well-band" aria-labelledby="heritage-head">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="heritage-head">{c("about.heritage.h", L)}</h2>
        <p>{c("about.heritage.sub", L)}</p>
      </div>
    </div>
    <div class="nd-gallery">{figs}</div>
    <p class="cm-body-sm cm-text-muted" style="margin-top:16px">{c("about.credits", L)}</p>
  </div>
</section>
""" + faq_block(U("faq", L), faq_for("about", L), L) + related(
    c("about.readon", L), [
        ("/kathai/", U("kathai_title", L), c("kathai.meta2", L)),
        ("/events.html", NAV[3][1] if L == "ta" else NAV[3][2], c("events.kinds.sub", L)),
        res_link("/certificate.html", L),
    ], L) + footer(L)


# Each month is its own collection under /kathai/. The hub lists them; a
# collection lists its days. Slugs are the month name so the URL says what it is.
COLLECTIONS = [
    {"file": "stories_july.json", "slug": "july", "en_file": "stories_en.json",
     "label": {"ta": "ஜூலை 2026", "en": "July 2026"},
     "month": {"ta": "ஜூலை", "en": "July"}},
    {"file": "stories_august.json", "slug": "august",
     "en_file": "stories_en_august.json",
     "label": {"ta": "ஆகஸ்ட் 2026", "en": "August 2026"},
     "month": {"ta": "ஆகஸ்ட்", "en": "August"}},
]


def coll_url(slug):
    return f"/kathai/{slug}/"


def story_url(slug, day):
    return f"/kathai/{slug}/day-{day:02d}.html"


def post_url(post):
    return f"/pathivu/{post['slug']}.html"


def post_thumb(post):
    """Card-sized crop; falls back to a local plate when a post has no image."""
    if not post["imgs"]:
        return "/assets/img/lion-capital-sarnath.jpg"
    src = post["imgs"][0]
    return src.replace("/pathivu/", "/pathivu/thumb/")


KATHAI_FAQ = [
    ("தம்மபதம்: முப்பத்தோர் நாள் என்றால் என்ன?",
     "ஜூலை 1 முதல் 31 வரை, ஒவ்வொரு நாளுக்கும் ஒரு பௌத்தக் கதை கொண்ட "
     "தமிழ்த் தொகுப்பு. புத்தர், அவர் சீடர்கள், மகாபஜாபதி, அசோகர், "
     "அம்பேத்கர் ஆகியோரின் வாழ்க்கைக் கதைகள். சங்கக் கூட்டத்தில் தினமும் "
     "வாசிக்கத் தொகுக்கப்பட்டது."),
    ("ஒவ்வொரு கதையிலும் என்ன இருக்கும்?",
     "நான்கு பகுதிகள்: கதை, தம்மக்கருத்து, அம்பேத்கர் இணைப்பு, ஆதாரம். "
     "ஒவ்வொரு கதையும் எந்த நூலில் சொல்லப்பட்டுள்ளது என்ற ஆதாரத்துடன் "
     "தரப்படுகிறது."),
    ("இதை யார் படிக்கலாம்?",
     "அனைவரும். சங்கக் கூட்டங்களில் உரக்க வாசிக்கவும், குடும்பமாகப் "
     "படிக்கவும், குழந்தைகளுக்குச் சொல்லவும் ஏற்ற வகையில் எளிய "
     "தமிழில் எழுதப்பட்டுள்ளது."),
    ("கதைகள் வரலாற்று நிகழ்வுகளா?",
     "சில வரலாற்று நிகழ்வுகள்; சில மரபுவழி உருவகக் கதைகள். அம்பேத்கர் "
     "கற்பித்தபடி, கதையின் அற்புதத்தை அல்ல, அதன் கருத்தைக் கவனிக்க "
     "வேண்டும் என்பதே இத்தொகுப்பின் நோக்கம்."),
]


def build_kathai_index(coll, data, en_data, stories, held, L):
    slug = coll["slug"]
    title = data["title"][L]
    trail = [("/kathai/", U("kathai_short", L)), (None, coll["label"][L])]
    month = coll["month"][L]

    def title_of(st):
        return story_field(st, "title", L, en_data)

    cards = "".join(f"""
      <a class="cm-card nd-kathai__card" href="{u(story_url(slug, st['day']), L)}"
         data-title="{esc(title_of(st).lower())}">
        <span class="nd-kathai__medallion">
          <img src="{st['icon']}" alt="" loading="lazy" width="88" height="88">
        </span>
        <span class="nd-kathai__day">{month} {st['day']}</span>
        <span class="nd-kathai__title">{title_of(st)}</span>
        <span class="nd-kathai__insight">{excerpt(story_field(st, "insight", L, en_data), 88)}</span>
      </a>""" for st in stories)

    if en_data:
        intro = en_data["intro"][1:-1] if L == "en" else data["intro"][2:-1]
        salut = en_data["intro"][0] if L == "en" else data["intro"][1]
        sign = en_data["intro"][-1] if L == "en" else data["intro"][-1]
    else:
        intro, salut, sign = data["intro"][2:-1], data["intro"][1], data["intro"][-1]
    intro_html = "".join(f"<p>{x}</p>" for x in intro)

    notes = ""
    if L == "en":
        notes += (f'<p class="nd-transnote">{icon("info", 15)}'
                  f'<span>{U("trans_note" if en_data else "trans_wait", L)}'
                  f'</span></p>')
    if held:
        notes += (f'<p class="nd-transnote nd-transnote--drip">{icon("calendar", 15)}'
                  f'<span>{c("kathai.drip", L, n=len(stories), total=len(stories) + held)}</span></p>')

    total = len(stories) + held
    return head(
        title, coll["label"][L],
        c("kathai.coll.meta", L, label=coll["label"][L], month=month),
        coll_url(slug), L,
        og_image=stories[0]["icon"] if stories else None,
        jsonld=[crumb_ld(trail, L), faq_ld(faq_for("kathai", L)), {
            "@context": "https://schema.org", "@type": "CollectionPage",
            "url": BASE + u(coll_url(slug), L), "inLanguage": L, "name": title,
            "isPartOf": {"@id": BASE + "/#website"},
            "publisher": {"@id": BASE + "/#organization"},
            "mainEntity": {
                "@type": "ItemList", "numberOfItems": len(stories),
                "itemListOrder": "https://schema.org/ItemListOrderAscending",
                "itemListElement": [
                    {"@type": "ListItem", "position": st["day"],
                     "url": BASE + u(story_url(slug, st["day"]), L),
                     "name": title_of(st)} for st in stories],
            },
        }],
    ) + pagehead(
        coll["label"][L], title, c("kathai.lede", L), trail, L,
        extra='<p class="nd-pagehead__meta">'
              f'{icon("calendar", 16)} {month} 1 &ndash; {total}'
              f'<span>{icon("layers", 16)} {len(stories)} / {total}</span>'
              f'<span>{icon("book", 16)} {c("kathai.meta3", L)}</span></p>'
    ) + f"""
{notes}
<section class="nd-section nd-section--tight">
  <div class="nd-shell">
    <div class="cm-card nd-letter">
      <p class="nd-eyebrow">{c("kathai.intro.h", L)}</p>
      <p class="nd-letter__salutation">{salut}</p>
      <div class="nd-prose">{intro_html}</div>
      <p class="nd-letter__sign">{sign}</p>
    </div>
  </div>
</section>

<section class="nd-section" aria-labelledby="days-head">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="days-head">{c("kathai.days.h", L)}</h2>
        <p>{c("kathai.days.sub", L)}</p>
      </div>
      <div class="cm-field" style="max-width:250px;width:100%">
        <label class="nd-sr" for="nd-ksearch">{c("kathai.search", L)}</label>
        <input class="cm-input" id="nd-ksearch" type="search"
               placeholder="{c("kathai.search", L)}" data-ksearch>
      </div>
    </div>
    <div class="nd-kathai" data-klist>{cards}
    </div>
    <p class="cm-body cm-text-muted nd-hidden" data-kempty style="margin-top:28px;text-align:center">
      {c("kathai.empty", L)}
    </p>
  </div>
</section>
""" + faq_block(c("kathai.about.h", L), faq_for("kathai", L), L) + related(
    U("related", L), [
        ("/kathai/", U("kathai_short", L), c("kathai.hub.sub", L)),
        ("/events.html", NAV[3][1] if L == "ta" else NAV[3][2], c("events.k1.h", L)),
        ("/about.html", NAV[1][1] if L == "ta" else NAV[1][2], c("about.lede", L)),
    ], L) + footer(L)


def build_kathai_hub(built, L):
    """built: [(coll, data, live_count, total)] newest first."""
    trail = [(None, U("kathai_short", L))]
    cards = "".join(
        f'<a class="cm-card nd-coll" href="{u(coll_url(cl["slug"]), L)}">'
        f'<span class="nd-coll__month">{cl["label"][L]}</span>'
        f'<span class="nd-coll__title">{dt["title"][L]}</span>'
        f'<span class="nd-coll__meta">{icon("layers", 15)} '
        f'{c("kathai.hub.count", L, n=live, total=total)}</span>'
        f'<span class="nd-coll__go">{icon("arrow", 16)}</span></a>'
        for cl, dt, live, total in built)
    return head(
        U("kathai_title", L), U("kathai_short", L), c("kathai.hub.meta", L),
        "/kathai/", L,
        jsonld=[crumb_ld(trail, L), {
            "@context": "https://schema.org", "@type": "CollectionPage",
            "url": BASE + u("/kathai/", L), "inLanguage": L,
            "name": U("kathai_title", L),
            "publisher": {"@id": BASE + "/#organization"},
            "mainEntity": {"@type": "ItemList", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": dt["title"][L],
                 "url": BASE + u(coll_url(cl["slug"]), L)}
                for i, (cl, dt, _l, _t) in enumerate(built)]},
        }],
    ) + pagehead(U("kathai_short", L), U("kathai_title", L),
                 c("kathai.hub.lede", L), trail, L) + f"""
<section class="nd-section">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2>{c("kathai.hub.h", L)}</h2>
        <p>{c("kathai.hub.sub", L)}</p>
      </div>
    </div>
    <div class="nd-colls">{cards}</div>
  </div>
</section>
""" + faq_block(c("kathai.about.h", L), faq_for("kathai", L), L) + related(
    U("related", L), [
        ("/about.html", NAV[1][1] if L == "ta" else NAV[1][2], c("about.lede", L)),
        ("/events.html", NAV[3][1] if L == "ta" else NAV[3][2], c("events.k1.h", L)),
        ("/downloads.html", c("dl.h1", L), c("dl.amb.sub", L)),
    ], L) + footer(L)


def build_story(st, prev_s, next_s, coll, data, en_data, L):
    f = lambda k: story_field(st, k, L, en_data)
    title = f("title")
    slug, month = coll["slug"], coll["month"][L]
    trail = [("/kathai/", U("kathai_short", L)),
             (coll_url(slug), coll["label"][L]),
             (None, f"{month} {st['day']}")]
    body = "".join(f"<p>{x}</p>" for x in f("body"))
    url = story_url(slug, st["day"])

    def link(other, rel, label, cls=""):
        t = story_field(other, "title", L, en_data)
        arrow = icon("arrow-left", 18) if rel == "prev" else icon("arrow", 18)
        inner = (f'{arrow}<span><em>{label} &middot; {month} {other["day"]}</em>{t}</span>'
                 if rel == "prev" else
                 f'<span><em>{label} &middot; {month} {other["day"]}</em>{t}</span>{arrow}')
        return f'<a class="nd-prevnext__link{cls}" href="{u(story_url(slug, other["day"]), L)}" rel="{rel}">{inner}</a>'

    nav = '<nav class="nd-prevnext" aria-label="{}">'.format(U("kathai_short", L))
    nav += link(prev_s, "prev", U("prev", L)) if prev_s else "<span></span>"
    nav += (link(next_s, "next", U("next", L), " nd-prevnext__link--next")
            if next_s else "<span></span>")
    nav += "</nav>"

    plain = " ".join(f("body"))
    note = (f'<p class="nd-transnote nd-transnote--inline">{icon("info", 15)} '
            f'<span>{U("trans_note" if has_en(st, en_data) else "trans_wait", L)}'
            f'</span></p>' if L == "en" else "")

    return head(
        f"{month} {st['day']}: {title}",
        f"Day {st['day']}" if L == "ta" else f"நாள் {st['day']}",
        excerpt(plain, 155), url, L, og_image=st["icon"],
        jsonld=[crumb_ld(trail, L), {
            "@context": "https://schema.org", "@type": "Article",
            "headline": f"{month} {st['day']}: {title}",
            "name": title, "url": BASE + u(url, L), "inLanguage": L,
            "articleSection": data["title"][L],
            "description": excerpt(plain, 155),
            "image": BASE + st["icon"],
            "author": {"@id": BASE + "/#organization"},
            "publisher": {"@id": BASE + "/#organization"},
            "isPartOf": {"@type": "CollectionPage",
                         "@id": BASE + u(coll_url(slug), L),
                         "name": data["title"][L]},
            "citation": f("source"),
            "position": st["day"],
        }],
    ) + f"""
<article class="nd-story">
  <header class="nd-story__head">
    <div class="nd-shell">
      {crumbs(trail, L)}
      <div class="nd-story__headrow">
        <div class="nd-story__medallion">
          <img src="{st['icon']}" alt="" width="112" height="112" fetchpriority="high">
        </div>
        <div>
          <p class="nd-eyebrow">{coll["label"][L]} &middot; {U('day', L)} {st['day']} / 31</p>
          <h1>{title}</h1>
          <p class="nd-story__date">{icon('calendar', 16)} {month} {st['day']}</p>
        </div>
      </div>
    </div>
  </header>

  <div class="nd-shell">
    <div class="nd-story__grid">
      <div class="nd-prose nd-story__body">
        {note}
        {body}

        <aside class="nd-callout" aria-labelledby="ins-{st['day']}">
          <p class="nd-callout__label" id="ins-{st['day']}">{icon('quote', 18)} {U('insight', L)}</p>
          <p class="nd-callout__text">{f("insight")}</p>
        </aside>

        <section aria-labelledby="amb-{st['day']}">
          <h2 id="amb-{st['day']}">{U('ambedkar', L)}</h2>
          <p>{f("ambedkar")}</p>
        </section>

        <p class="nd-source"><strong>{U('source', L)}:</strong> {f("source")}</p>
      </div>

      <aside class="nd-story__aside nd-stack-4">
        <div class="cm-card nd-card">
          <p class="nd-eyebrow">{coll["label"][L]}</p>
          <p style="margin-top:10px">{c("story.collection", L, n=st['day'],
              link=f'<a href="{u(coll_url(slug), L)}">{data["title"][L]}</a>')}</p>
          <p style="margin-top:16px">
            <a class="cm-btn cm-btn--secondary cm-btn--sm" href="{u(coll_url(slug), L)}">
              {c("story.seeall", L)}
            </a>
          </p>
        </div>
        <div class="nd-alert nd-alert--accent">
          {icon('moon', 20)}
          <div>
            <p class="nd-alert__title">{c("story.at.h", L)}</p>
            <p>{c("story.at.p", L, venue=U("venue", L),
                   link=f'<a href="{u("/events.html", L)}">{c("story.at.link", L)}</a>')}</p>
          </div>
        </div>
      </aside>
    </div>

    {nav}
  </div>
</article>
""" + footer(L)


def build_post(post, prev_p, next_p, related_posts, L):
    trail = [("/writings.html", U("writings", L)),
             (None, fmt_date(post["date"], L))]
    url = post_url(post)
    title = post_title(post, L)
    labels = [x.strip() for lab in post["labels"] for x in lab.split("\n") if x.strip()]
    chips = "".join(f'<span class="nd-tag">{esc(x)}</span>' for x in labels[:8])
    translated = L == "en" and post.get("blocks_en")
    note = (f'<p class="nd-transnote nd-transnote--inline">{icon("info", 15)} '
            f'<span>{U("trans_note", L)}</span></p>') if translated else ""

    def link(other, rel, label, cls=""):
        arrow = icon("arrow-left", 18) if rel == "prev" else icon("arrow", 18)
        t = post_title(other, L)
        inner = (f'{arrow}<span><em>{label}</em>{t}</span>' if rel == "prev"
                 else f'<span><em>{label}</em>{t}</span>{arrow}')
        return (f'<a class="nd-prevnext__link{cls}" href="{u(post_url(other), L)}" '
                f'rel="{rel}">{inner}</a>')

    nav = f'<nav class="nd-prevnext" aria-label="{U("writings", L)}">'
    nav += link(prev_p, "prev", U("older", L)) if prev_p else "<span></span>"
    nav += (link(next_p, "next", U("newer", L), " nd-prevnext__link--next")
            if next_p else "<span></span>")
    nav += "</nav>"

    more = "".join(
        f'<a class="cm-card nd-mediacard" href="{u(post_url(r), L)}">'
        f'<div class="nd-mediacard__media"><img src="{post_thumb(r)}" alt="" loading="lazy"></div>'
        f'<div class="nd-mediacard__body"><p class="nd-mediacard__meta">{fmt_date(r["date"], L)}</p>'
        f'<h3>{post_title(r, L)}</h3></div></a>' for r in related_posts
    )

    # Counted from the blocks, not from post["imgs"]: one post carries more
    # pictures in its body than the feed listed.
    blocks = post["blocks_en"] if L == "en" and post.get("blocks_en") else post["blocks"]
    n = sum(1 for b in blocks if b[0] == "fig")
    shots = (f'<span class="nd-postmeta__item">{icon("image", 15)} {n} '
             f'{U("photos" if n != 1 else "photo_one", L)}</span>') if n else ""

    # two posts in the archive share a title; the date separates them
    seo_title = (title if not post.get(f"title_dup_{L}")
                 else f"{title} ({fmt_date(post['date'], L)})")
    return head(
        seo_title, None,
        post_desc(post, L), url, L,
        og_image=post["imgs"][0] if post["imgs"] else None,
        jsonld=[crumb_ld(trail, L), {
            "@context": "https://schema.org", "@type": "Article",
            "headline": title, "url": BASE + u(url, L), "inLanguage": L,
            "datePublished": post["date"],
            "description": excerpt(post_text(post, L), 155),
            **({"image": [BASE + i for i in post["imgs"][:4]]} if post["imgs"] else {}),
            "author": {"@id": BASE + "/#organization"},
            "publisher": {"@id": BASE + "/#organization"},
            "isPartOf": {"@type": "CollectionPage", "@id": BASE + u("/writings.html", L),
                         "name": U("writings", L)},
            **({"keywords": ", ".join(labels)} if labels else {}),
        }],
    ) + f"""
<article class="nd-post">
  <header class="nd-post__head">
    <div class="nd-shell">
      <div class="nd-article">
        {crumbs(trail, L)}
        <h1>{title}</h1>
        <div class="nd-postmeta">
          <span class="nd-postmeta__item">{icon('calendar', 15)}
            <time datetime="{post['date']}">{fmt_date(post['date'], L)}</time></span>
          <span class="nd-postmeta__item">{icon('clock', 15)}
            {read_minutes(post, L)} {U('read_min', L)}</span>
          {shots}
          <button class="nd-copy" type="button" data-copy
                  data-done="{U('copied', L)}" hidden>
            {icon('link', 15)} <span>{U('copy_link', L)}</span>
          </button>
        </div>
        {f'<div class="nd-tags">{chips}</div>' if chips else ''}
      </div>
    </div>
  </header>

  <div class="nd-shell">
    <div class="nd-post__body nd-prose nd-article">
      {note}
      {post_body(post, L)}
    </div>

    <div class="nd-article">
      <p class="nd-source">
        {icon('external', 15)} {U('origin', L)}:
        <a href="{post['origin']}" rel="noopener nofollow">niladhamma.co.in</a>
      </p>
    </div>

    <div class="nd-article">{nav}</div>
  </div>
</article>

<section class="nd-section nd-section--tight nd-well-band" aria-labelledby="more-head">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div><h2 id="more-head">{U('more_posts', L)}</h2></div>
      <a class="cm-btn cm-btn--ghost cm-btn--sm" href="{u("/writings.html", L)}">
        {U('read_all', L)} {icon('arrow', 16)}</a>
    </div>
    <div class="nd-grid nd-grid--4">{more}</div>
  </div>
</section>
""" + footer(L)


def build_resources(L):
    trail = [(None, c("res.h1", L) if False else U("resources", L))]
    cards = "".join(
        f'<a class="cm-card nd-card" href="{u(h, L)}">'
        f'<div class="nd-card__icon">{icon(ic, 22)}</div>'
        f'<h3>{lab}</h3><p>{sub}</p></a>'
        for h, lab, ic, sub in res_items(L)
    )
    return head(
        U("resources", L), "Resources" if L == "ta" else "வளங்கள்",
        c("res.meta", L), "/resources.html", L,
        jsonld=[crumb_ld(trail, L), {
            "@context": "https://schema.org", "@type": "CollectionPage",
            "url": BASE + u("/resources.html", L), "inLanguage": L,
            "name": U("resources", L),
            "mainEntity": {"@type": "ItemList", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": lab,
                 "url": BASE + u(h, L)}
                for i, (h, lab, *_r) in enumerate(res_items(L))]},
        }],
    ) + pagehead(U("resources", L), c("res.h1", L), c("res.lede", L),
                 trail, L) + f"""
<section class="nd-section" aria-labelledby="res-list">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="res-list">{c("res.list.h", L)}</h2>
        <p>{c("res.list.sub", L)}</p>
      </div>
    </div>
    <div class="nd-grid nd-grid--2">{cards}</div>
  </div>
</section>
""" + related(c("res.alsosee", L), [
        ("/kathai/", U("kathai_title", L), c("kathai.meta1", L)),
        ("/writings.html", U("writings", L), c("writings.all.sub", L)),
        ("/contact.html", U("contact", L), c("contact.lede", L)),
    ], L) + footer(L)


def observed_date(m):
    """The evening the sangha actually gathers.

    The gathering is at 6pm, and the observance follows the tithi current at
    that hour. When the astronomical full moon falls in the small hours, the
    tithi was current the previous evening, so the gathering is the day before.
    Checked against the two dates the sangha has published: the 172nd (full
    moon 2 Feb 2026 03:40 IST, gathered 1 Feb) and the 178th (29 Jul 2026
    20:06 IST, gathered 29 Jul). Both match."""
    from datetime import date, timedelta
    if int(m["time_ist"][:2]) < 6:
        return (date.fromisoformat(m["date"]) - timedelta(days=1)).isoformat()
    return m["date"]


def build_events(posts, moons, ALL_MOONS, L):
    trail = [(None, NAV[3][1] if L == "ta" else NAV[3][2])]
    POURNAMI_ANCHOR, POURNAMI_N = "2026-07-29", 178

    def pournami_no(date):
        return POURNAMI_N + sum(1 for m in ALL_MOONS
                                if POURNAMI_ANCHOR < m["date"] <= date)

    nth = "வது" if L == "ta" else ""

    # One chronological list. The two kinds of observance were in separate
    # tables that never met, so the page never answered "what is next".
    # Full moons are computed; anniversaries are solar and fixed, so their next
    # occurrence is worked out from today rather than printed as a bare 01 / 01.
    def moon_row(m):
        obs = observed_date(m)
        note = f'{c("cal.at6", L)} &middot; {m["time_ist"]} IST'
        if obs != m["date"]:
            note += f' ({c("cal.shifted", L)})'
        return {
            "date": obs,
            "label": (f'<span class="nd-cal__nth cm-tabular">'
                      f'{pournami_no(m["date"])}{nth}</span> {c("cal.gathering", L)}'),
            "when": fmt_date(obs, L), "note": note,
            "kind": "moon", "moon": obs,
        }

    upcoming = [moon_row(m) for m in moons[:18]]

    y = int(TODAY[:4])
    by_slug = {x["slug"]: x for x in posts}
    for row in FIXED_DAYS:
        dd, name, yr, desc = row[:4]
        link = row[4] if len(row) > 4 else None
        d, mo = dd.split("-")
        for yy in (y, y + 1):
            iso = f"{yy}-{mo}-{d}"
            if iso >= TODAY:
                upcoming.append({
                    "date": iso, "label": f"<strong>{name[L]}</strong>",
                    "when": fmt_date(iso, L),
                    "note": (f'{desc[L]} <span class="nd-cal__since">({yr})</span>'
                             + (f' <a href="{u(post_url(by_slug[link]), L)}">'
                                f'{c("cal.read", L)}</a>'
                                if link and link in by_slug else "")),
                    "kind": "mem", "moon": "",
                })
                break
    upcoming.sort(key=lambda x: x["date"])
    horizon = f"{y + 1}-{TODAY[5:]}"
    upcoming = [x for x in upcoming if x["date"] <= horizon]

    up_rows = "".join(
        f'<tr{f" data-moon=\"{x["moon"]}\"" if x["moon"] else ""}>'
        f'<td class="nd-cal__date">{x["when"]}</td>'
        f'<td>{x["label"]}<br><span class="nd-cal__en">{x["note"]}</span></td>'
        f'<td><span class="nd-kind nd-kind--{x["kind"]}">'
        f'{c("cal.kind.moon" if x["kind"] == "moon" else "cal.kind.mem", L)}</span></td></tr>'
        for x in upcoming
    )
    lunar_rows = "".join(
        f'<tr><td><strong>{ta[L]}</strong><br><span class="nd-cal__en">{en}</span></td>'
        f'<td class="nd-cal__when">{when[L]}</td><td>{desc[L]}</td></tr>'
        for ta, en, when, desc in LUNAR_DAYS
    )
    def day_month(dd):
        d, mo = dd.split("-")
        months = TA_MONTHS if L == "ta" else EN_MONTHS
        return f"{int(d)} {months[int(mo) - 1]}"

    fixed_rows = "".join(
        f'<tr><td class="nd-cal__date">{day_month(d)}</td>'
        f'<td><strong>{name[L]}</strong><br><span class="nd-cal__en">{yr}</span></td>'
        f'<td>{desc[L]}</td></tr>'
        for d, name, yr, desc, *_x in FIXED_DAYS
    )

    const_stats = "".join(
        f'<div class="cm-card nd-stat nd-stat--const">'
        f'<span class="nd-stat__value">{v}</span>'
        f'<span class="nd-stat__label">{lab[L]}</span></div>'
        for v, lab in CONST_STATS)
    const_rows = "".join(
        f'<li><p class="nd-timeline__date">{fmt_date(d, L)}</p>'
        f'<p class="nd-timeline__title">{lab[L]}</p></li>'
        for d, lab in CONSTITUTION)

    ev = [x for x in posts if x["date"] >= "2025-01-01"][:20]
    items = "".join(f"""
      <li>
        <a class="nd-timeline__thumb" href="{u(post_url(x), L)}" tabindex="-1" aria-hidden="true">
          <img src="{post_thumb(x)}" alt="" loading="lazy" width="96" height="72">
        </a>
        <p class="nd-timeline__date">{fmt_date(x['date'], L)}</p>
        <p class="nd-timeline__title"><a href="{u(post_url(x), L)}">{post_title(x, L)}</a></p>
        <p class="nd-timeline__body">{excerpt(post_text(x, L), 175)}</p>
      </li>""" for x in ev)

    # Eight identical alt strings help nobody; name what each photograph is of.
    shots = [x for x in posts if x["imgs"]][:8]
    gal = "".join(
        f'<figure><img src="{post_thumb(x)}" '
        f'alt="{esc(post_title(x, L))} &ndash; {fmt_date(x["date"], L)}" loading="lazy">'
        f'<figcaption><a href="{u(post_url(x), L)}">{post_title(x, L)}</a>'
        f'<span>{fmt_date(x["date"], L)}</span></figcaption></figure>'
        for x in shots)

    return head(
        c("events.title", L), NAV[3][2] if L == "ta" else NAV[3][1],
        c("events.meta", L), "/events.html", L,
        og_image="/assets/img/pournami-poster-square.png",
        jsonld=[crumb_ld(trail, L), faq_ld(faq_for("events", L)), {
            "@context": "https://schema.org", "@type": "WebPage",
            "url": BASE + u("/events.html", L), "inLanguage": L,
            "name": c("events.title", L),
            "description": c("events.meta", L),
            "about": VENUE_LD, "publisher": {"@id": BASE + "/#organization"},
            "primaryImageOfPage": {"@type": "ImageObject",
                                   "url": BASE + "/assets/img/pournami-poster-square.png"},
        }],
    ) + pagehead(NAV[3][1] if L == "ta" else NAV[3][2], c("events.h1", L),
                 c("events.lede", L), trail, L) + f"""
<section class="nd-section nd-section--tight" aria-labelledby="at-head">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="at-head">{c("events.at.h", L)}</h2>
        <p>{c("events.at.sub", L)}</p>
      </div>
    </div>
    <div class="nd-grid nd-grid--aside">
      <ol class="nd-steps nd-steps--run">
        <li><p class="nd-steps__title">{c("events.at.1t", L)}</p>
            <p class="nd-steps__body">{c("events.at.1d", L)}</p></li>
        <li><p class="nd-steps__title">{c("events.at.2t", L)}</p>
            <p class="nd-steps__body">{c("events.at.2d", L)}</p></li>
        <li><p class="nd-steps__title">{c("events.at.3t", L)}</p>
            <p class="nd-steps__body">{c("events.at.3d", L)}</p></li>
        <li><p class="nd-steps__title">{c("events.at.4t", L)}</p>
            <p class="nd-steps__body">{c("events.at.4d", L,
                link=f'<a href="{u("/kathai/", L)}">{c("events.at.4l", L)}</a>')}</p></li>
        <li><p class="nd-steps__title">{c("events.at.5t", L)}</p>
            <p class="nd-steps__body">{c("events.at.5d", L)}</p></li>
      </ol>
      <aside>
        <div class="nd-alert nd-alert--success">
          {icon('check', 20)}
          <div>
            <p class="nd-alert__title">{c("events.bring.h", L)}</p>
            <p>{c("events.bring.p", L)}</p>
          </div>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="nd-section nd-section--tight" aria-labelledby="cal-head">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="cal-head">{c("cal.h", L)}</h2>
        <p>{c("cal.sub", L)}</p>
      </div>
      <a class="cm-btn cm-btn--secondary cm-btn--sm" href="{u("/niladhamma.ics", L)}"
         download>{icon('calendar', 16)} {c("cal.sub.file", L)}</a>
    </div>

    <div class="nd-cal__next cm-card" data-nextmoon hidden>
      <div class="nd-cal__nextmark">{icon('moon', 26)}</div>
      <div>
        <p class="nd-eyebrow">{c("cal.next", L)}</p>
        <p class="nd-cal__nextdate" data-nextmoon-date></p>
        <p class="nd-cal__nextmeta" data-nextmoon-meta></p>
      </div>
      <a class="cm-btn cm-btn--primary cm-btn--sm" href="{u("/contact.html", L)}">
        {U("directions", L)}</a>
    </div>

    <div class="cm-card nd-subscribe">
      <div class="nd-subscribe__mark">{icon('calendar', 24)}</div>
      <div>
        <p class="nd-subscribe__h">{c("cal.sub.h", L)}</p>
        <p class="nd-subscribe__p">{c("cal.sub.p", L)}</p>
        <p class="nd-row" style="margin-top:16px">
          <a class="cm-btn cm-btn--primary cm-btn--sm" rel="noopener"
             href="https://calendar.google.com/calendar/r?cid=webcal%3A%2F%2Fwww.niladhamma.co.in{u('/niladhamma.ics', L).replace('/', '%2F')}">
            {c("cal.sub.google", L)}</a>
          <a class="cm-btn cm-btn--secondary cm-btn--sm"
             href="{u("/niladhamma.ics", L)}" download>{c("cal.sub.file", L)}</a>
        </p>
        <p class="nd-subscribe__note">{icon('info', 14)}
          <span>{c("cal.sub.note", L)}
            <code>{BASE}{u("/niladhamma.ics", L)}</code></span></p>
      </div>
    </div>

    <div class="nd-tabs" data-tabs>
      <div class="nd-tabs__list" role="tablist" aria-label="{c("cal.h", L)}">
        <button class="nd-tab" role="tab" id="t-up" aria-controls="p-up"
                aria-selected="true" type="button">{c("cal.up.h", L)}</button>
        <button class="nd-tab" role="tab" id="t-lu" aria-controls="p-lu"
                aria-selected="false" tabindex="-1" type="button">{c("cal.lunar.h", L)}</button>
        <button class="nd-tab" role="tab" id="t-fx" aria-controls="p-fx"
                aria-selected="false" tabindex="-1" type="button">{c("cal.fixed.h", L)}</button>
      </div>

      <div class="nd-tabs__panel" role="tabpanel" id="p-up" aria-labelledby="t-up">
        <p class="nd-cal__lede">{c("cal.up.sub", L)}</p>
        <div class="nd-cal__scroll">
          <table class="cm-table nd-cal" data-more="8">
            <thead><tr><th scope="col">{c("cal.col.date", L)}</th>
              <th scope="col">{c("cal.col.event", L)}</th>
              <th scope="col">{c("cal.col.kind", L)}</th></tr></thead>
            <tbody>{up_rows}</tbody>
          </table>
        </div>
        <p class="nd-cal__note">
          {icon('info', 15)}
          <span>{c("cal.note1", L,
                    link=f'<a href="{u("/writings.html", L)}">{c("cal.note1.link", L)}</a>')}</span>
        </p>
      </div>

      <div class="nd-tabs__panel" role="tabpanel" id="p-lu" aria-labelledby="t-lu" hidden>
        <div class="nd-cal__scroll">
          <table class="cm-table nd-cal">
            <thead><tr><th scope="col">{c("cal.col.festival", L)}</th>
              <th scope="col">{c("cal.col.when", L)}</th>
              <th scope="col">{c("cal.col.note", L)}</th></tr></thead>
            <tbody>{lunar_rows}</tbody>
          </table>
        </div>
        <p class="nd-cal__note">{icon('info', 15)}<span>{c("cal.note2", L)}</span></p>
      </div>

      <div class="nd-tabs__panel" role="tabpanel" id="p-fx" aria-labelledby="t-fx" hidden>
        <div class="nd-cal__scroll">
          <table class="cm-table nd-cal" data-more="8">
            <thead><tr><th scope="col">{c("cal.col.date", L)}</th>
              <th scope="col">{c("cal.col.event", L)}</th>
              <th scope="col">{c("cal.col.note", L)}</th></tr></thead>
            <tbody>{fixed_rows}</tbody>
          </table>
        </div>

        <div class="nd-const">
          <h3 class="nd-const__h">{c("const.h", L)}</h3>
          <p class="nd-const__sub">{c("const.sub", L)}</p>
          <div class="nd-grid nd-grid--4">{const_stats}</div>
          <ul class="nd-timeline nd-timeline--const">{const_rows}</ul>
          <p class="nd-cal__note">{icon('info', 15)}<span>{c("const.note", L)}</span></p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="nd-section nd-section--tight" aria-labelledby="ev-kinds">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="ev-kinds">{c("events.kinds.h", L)}</h2>
        <p>{c("events.kinds.sub", L)}</p>
      </div>
    </div>
    <div class="nd-grid nd-grid--3">
      <div class="cm-card nd-card">
        <div class="nd-card__icon">{icon('moon', 22)}</div>
        <h3>{c("events.k1.h", L)}</h3>
        <p>{c("events.k1.p", L, venue=U("venue", L),
               link=f'<a href="{u("/kathai/", L)}">{c("events.k1.link", L)}</a>')}</p>
      </div>
      <div class="cm-card nd-card">
        <div class="nd-card__icon">{icon('sparkle', 22)}</div>
        <h3>{c("events.k2.h", L)}</h3>
        <p>{c("events.k2.p", L)}</p>
      </div>
      <div class="cm-card nd-card">
        <div class="nd-card__icon">{icon('book', 22)}</div>
        <h3>{c("events.k3.h", L)}</h3>
        <p>{c("events.k3.p", L)}</p>
      </div>
    </div>
  </div>
</section>

<section class="nd-section nd-section--tight">
  <div class="nd-shell">
    <div class="cm-card nd-feature nd-feature--flip">
      <div class="nd-feature__media">
        <img src="/assets/img/alms-giving.jpg" alt="{c("events.dana.h", L)}" loading="lazy">
      </div>
      <div class="nd-feature__body">
        <p class="nd-eyebrow">{c("events.dana.eyebrow", L)}</p>
        <h2>{c("events.dana.h", L)}</h2>
        <p>{c("events.dana.p", L, venue=U("venue", L),
               link=f'<a href="{u(story_url("july", 4), L)}">{c("events.dana.link", L)}</a>')}</p>
      </div>
    </div>
  </div>
</section>

<section class="nd-section">
  <div class="nd-shell">
    <div class="nd-grid nd-grid--aside">
      <div>
        <div class="nd-sechead">
          <div>
            <h2>{c("events.timeline.h", L)}</h2>
            <p>{c("events.timeline.sub", L)}</p>
          </div>
        </div>
        <ul class="nd-timeline" data-more="6">{items}
        </ul>
        <p style="margin-top:28px">
          <a class="cm-btn cm-btn--secondary" href="{u("/writings.html", L)}">
            {c("events.allposts", L)} {icon('arrow', 18)}
          </a>
        </p>
      </div>

      <aside class="nd-stack-6">
        <div class="cm-card" style="overflow:hidden">
          <img src="/assets/img/pournami-poster-square.png" loading="lazy"
               alt="{c("events.poster.cap", L)}">
          <div style="padding:14px 16px;border-top:1px solid var(--cm-border-default)">
            <p class="cm-body-sm cm-text-muted" style="margin:0 0 12px">
              {c("events.poster.cap", L)}
            </p>
            <a class="cm-btn cm-btn--secondary cm-btn--sm"
               href="/assets/img/pournami-poster-a4.png" download>
              {icon('download', 16)} {c("events.poster.dl", L)}
            </a>
          </div>
        </div>
        <div class="cm-card nd-card">
          <div class="nd-card__icon">{icon('map', 22)}</div>
          <h3>{c("contact.place.h", L)}</h3>
          <address class="nd-address">
            <strong>{U("venue", L)}</strong>
            <span>{U("venue_addr", L)}</span>
          </address>
          <p style="margin-top:16px">
            <a class="cm-btn cm-btn--primary cm-btn--sm" href="{MAPS_URL}" rel="noopener">
              {icon('map', 16)} {U("directions", L)}
            </a>
          </p>
        </div>
        <div class="cm-card nd-card">
          <p class="nd-eyebrow">{c("events.join.h", L)}</p>
          <p style="margin-top:12px">{c("events.join.p", L)}</p>
          <p style="margin-top:16px">
            <a class="cm-btn cm-btn--primary cm-btn--sm" href="{u("/contact.html", L)}">
              {c("events.contact", L)}</a>
          </p>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="nd-section nd-well-band" aria-labelledby="gal-head">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="gal-head">{c("events.gallery.h", L)}</h2>
        <p>{c("events.gallery.sub", L)}</p>
      </div>
    </div>
    <div class="nd-gallery">{gal}</div>
  </div>
</section>
""" + faq_block(U("faq", L), faq_for("events", L), L) + related(
    U("related", L), [
        ("/kathai/", U("kathai_short", L), c("events.k1.link", L)),
        res_link("/matrimony.html", L),
        ("/about.html", NAV[1][1] if L == "ta" else NAV[1][2], c("about.lede", L)),
    ], L) + footer(L)


def build_writings(posts, L):
    trail = [(None, U("writings", L))]
    years = sorted({p["date"][:4] for p in posts}, reverse=True)
    chips = ('<button class="nd-chip" type="button" aria-pressed="true" data-year="all">'
             f'{U("all", L)} ({len(posts)})</button>')
    for y in years:
        n = sum(1 for p in posts if p["date"].startswith(y))
        chips += (f'<button class="nd-chip" type="button" aria-pressed="false" '
                  f'data-year="{y}">{y} ({n})</button>')

    cards = ""
    for p in posts:
        cards += f"""
      <a class="cm-card nd-mediacard" href="{u(post_url(p), L)}"
         data-year="{p['date'][:4]}" data-title="{esc(post_title(p, L).lower())}">
        <div class="nd-mediacard__media"><img src="{post_thumb(p)}" alt="" loading="lazy"></div>
        <div class="nd-mediacard__body">
          <p class="nd-mediacard__meta">{fmt_date(p['date'], L)}</p>
          <h3>{post_title(p, L)}</h3>
          <p class="nd-mediacard__excerpt">{excerpt(post_text(p, L), 120)}</p>
        </div>
      </a>"""

    return head(
        U("writings", L), "Writings" if L == "ta" else "பதிவுகள்",
        c("writings.meta", L), "/writings.html", L,
        jsonld=[crumb_ld(trail, L), {
            "@context": "https://schema.org", "@type": "CollectionPage",
            "url": BASE + u("/writings.html", L), "inLanguage": L,
            "name": U("writings", L), "publisher": {"@id": BASE + "/#organization"},
        }],
    ) + pagehead(U("writings", L), c("writings.h1", L), c("writings.lede", L),
                 trail, L) + f"""
<section class="nd-section" aria-labelledby="posts-head">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="posts-head">{c("writings.all.h", L)}</h2>
        <p>{c("writings.all.sub", L)}</p>
      </div>
    </div>
    <div class="nd-row" style="justify-content:space-between;margin-bottom:24px">
      <div class="nd-filters" data-filters>{chips}</div>
      <div class="cm-field" style="max-width:260px;width:100%">
        <label class="nd-sr" for="nd-search">{U("search_title", L)}</label>
        <input class="cm-input" id="nd-search" type="search"
               placeholder="{U("search_title", L)}" data-search>
      </div>
    </div>
    <div class="nd-grid nd-grid--4" data-list>{cards}
    </div>
    <p class="cm-body cm-text-muted nd-hidden" data-empty style="margin-top:32px;text-align:center">
      {c("writings.empty", L)}
    </p>
  </div>
</section>
""" + related(U("related", L), [
        ("/kathai/", U("kathai_title", L), c("kathai.meta2", L)),
        ("/events.html", NAV[3][1] if L == "ta" else NAV[3][2], c("events.timeline.sub", L)),
        ("/downloads.html", c("dl.h1", L), c("dl.lede", L)),
    ], L) + footer(L)


NAMES_FAQ = [
    ("குழந்தைக்குப் பௌத்தப் பெயர் வைப்பது எப்படி?",
     "இப்பக்கத்தில் ஆண் குழந்தைகளுக்கான 254 பெயர்களும், பெண் "
     "குழந்தைகளுக்கான 228 பெயர்களும், திரிபீடகத்தின் தேரகதாவில் "
     "பதிவான 518 தேரர் பெயர்களும் தொகுக்கப்பட்டுள்ளன. தேடல் பெட்டியில் "
     "எழுத்தைத் தட்டச்சு செய்து வடிகட்டலாம்."),
    ("தேரகதா என்றால் என்ன?",
     "திரிபீடகத்தில் இடம்பெறும் ஒரு நூல். பிக்குகள் தம் தம்மானுபவத்தைப் "
     "பாடல்களாகச் சொன்ன கோர்வை. அதில் இடம்பெறும் தேரர்களின் பெயர்கள் "
     "இங்குத் தொகுக்கப்பட்டுள்ளன."),
    ("பௌத்தப் பெயர்களுக்கும் தமிழுக்கும் என்ன தொடர்பு?",
     "பௌத்தம் இம்மண்ணின் அடையாளமாகச் செழித்து வளர்ந்த மதம். அதன் "
     "கொடையால் தமிழுக்கு வரிவடிவம் முதல் இலக்கிய இலக்கணங்களும் "
     "கிடைத்தன. பல ஊர்ப்பெயர்களும் பௌத்தத்தைத் தாங்கியே இன்றும் "
     "நீடிக்கின்றன."),
]


def build_names(names, L):
    trail = [("/resources.html", U("resources", L)),
             (None, res_title("/names.html", L))]

    def li(lst):
        return "".join(f"<li><span>{i}</span>{n}</li>" for i, n in enumerate(lst, 1))

    title = res_title("/names.html", L)
    return head(
        title, res_title("/names.html", LANGS[L]["other"]),
        c("names.meta", L), "/names.html", L,
        jsonld=[crumb_ld(trail, L), faq_ld(faq_for("names", L))],
    ) + pagehead(title, c("names.h1", L), c("names.lede", L), trail, L) + f"""
<section class="nd-section nd-section--tight">
  <div class="nd-shell">
    <div class="nd-prose nd-reading">
      <p>{c("names.p1", L, link=f'<a href="{u("/kathai/", L)}">{c("names.p1.link", L)}</a>')}</p>
    </div>
  </div>
</section>

<section class="nd-section nd-section--tight">
  <div class="nd-shell">
    <div class="nd-row" style="justify-content:space-between;align-items:flex-end;margin-bottom:20px">
      <div class="nd-filters" data-filters>
        <button class="nd-chip" type="button" aria-pressed="true" data-tab="boys">
          {c("names.tab.boys", L)} ({len(names['boys'])})</button>
        <button class="nd-chip" type="button" aria-pressed="false" data-tab="girls">
          {c("names.tab.girls", L)} ({len(names['girls'])})</button>
        <button class="nd-chip" type="button" aria-pressed="false" data-tab="theras">
          {c("names.tab.theras", L)} ({len(names['theras'])})</button>
      </div>
      <div class="cm-field" style="max-width:260px;width:100%">
        <label class="nd-sr" for="nd-nsearch">{c("names.search", L)}</label>
        <input class="cm-input" id="nd-nsearch" type="search"
               placeholder="{c("names.search", L)}" data-namesearch>
      </div>
    </div>

    <div class="cm-card" style="padding:24px 28px">
      <div data-panel="boys">
        <h2 class="nd-eyebrow" style="margin-bottom:16px">{c("names.h.boys", L)}</h2>
        <ul class="nd-names">{li(names['boys'])}</ul>
      </div>
      <div data-panel="girls" class="nd-hidden">
        <h2 class="nd-eyebrow" style="margin-bottom:16px">{c("names.h.girls", L)}</h2>
        <ul class="nd-names">{li(names['girls'])}</ul>
      </div>
      <div data-panel="theras" class="nd-hidden">
        <h2 class="nd-eyebrow" style="margin-bottom:16px">{c("names.h.theras", L)}</h2>
        <ul class="nd-names">{li(names['theras'])}</ul>
      </div>
      <p class="cm-body cm-text-muted nd-hidden" data-nempty style="margin-top:20px">
        {c("names.empty", L)}
      </p>
    </div>
  </div>
</section>
""" + faq_block(c("names.faq.h", L), faq_for("names", L), L) + related(
    U("related", L), [
        res_link("/certificate.html", L),
        res_link("/matrimony.html", L),
        ("/kathai/", U("kathai_short", L), c("names.p1.link", L)),
    ], L) + footer(L)


CERT_FAQ = [
    ("பௌத்தம் ஏற்றால் சமூகச் சான்றிதழ் பறிபோகுமா?",
     "இல்லை. ஒரு பட்டியலினத்தவர் இந்து, சீக்கிய, பௌத்த மதம் ஆகிய "
     "இந்த மூன்றில் எதற்கு மாறினாலும், பின்பற்றினாலும், அவரின் சமூக "
     "உரிமைகளைப் பெறப் பட்டியலினம் (SC) என்றே சான்றிதழ் வழங்கப்படுகிறது."),
    ("சான்றிதழ் பெற எங்கே விண்ணப்பிக்க வேண்டும்?",
     "மற்றவர்கள் சமூகச் சான்றிதழ் பெறுவது போன்றே, இ-சேவை மையம் மூலமே "
     "விண்ணப்பித்துப் பெற்றுக்கொள்ளலாம். பௌத்தர்களுக்குத் தனி "
     "வழிமுறை எதுவும் இல்லை."),
    ("CAN பதிவில் மதம் என்ன தேர்வு செய்வது?",
     "CAN registration அல்லது குடிமக்கள் கணக்கு எண் பதிவு செய்கையில், "
     "மதம் என்ற இடத்தில் Buddhist என்று தேர்வு செய்தால் போதும்."),
    ("புதிய சான்றிதழில் மதம் ஏன் இல்லை?",
     "பழைய சான்றிதழ்களில் மதம் குறிப்பிடப்பட்டு, அதன் பின்னர் உட்சாதி "
     "குறிப்பிடப்பட்டிருக்கும். சமீபத்திய சான்றிதழ்களில் மதம் "
     "குறிப்பிடப்படுவதில்லை; உட்சாதியும் சமூகமும் (SC) மட்டுமே "
     "குறிப்பிடப்படுகிறது."),
    ("அலுவலகத்தில் மறுத்தால் என்ன செய்வது?",
     "நிலாதம்மாவைத் தொடர்பு கொள்ளுங்கள். இதுவரை "
     "நூற்றுக்கணக்கான குடும்பங்கள் இந்தச் செயல்முறையைக் கடந்திருக்கின்றன; "
     "சங்கம் உங்களுடன் உடன் நிற்கும்."),
]


def build_certificate(L):
    trail = [("/resources.html", U("resources", L)),
             (None, res_title("/certificate.html", L))]
    steps_src = [
        ({"ta": "இ-சேவை மையத்தை அணுகவும்", "en": "Go to an e-Sevai centre"},
         {"ta": "மற்றவர்கள் சமூகச் சான்றிதழ் பெறுவது போன்றே, நாமும் இ-சேவை "
                "மையம் மூலமே விண்ணப்பித்துப் பெற்றுக்கொள்ளலாம். தனி வழிமுறை "
                "எதுவும் இல்லை.",
          "en": "Exactly as anyone else obtains a community certificate, we "
                "apply through an e-Sevai centre. There is no separate "
                "procedure."}),
        ({"ta": "CAN பதிவில் மதத்தைத் தேர்வு செய்யவும்",
          "en": "Select the religion in the CAN registration"},
         {"ta": "CAN registration அல்லது குடிமக்கள் கணக்கு எண் பதிவு "
                "செய்கையில், மதம் என்ற இடத்தில் Buddhist என்று தேர்வு "
                "செய்தால் போதும்.",
          "en": "When completing the CAN registration, that is the Citizen "
                "Account Number registration, selecting Buddhist in the "
                "religion field is enough."}),
        ({"ta": "ஆதாரச் சான்றிதழ் இணைக்கவும்",
          "en": "Attach the supporting certificate"},
         {"ta": "பெற்றோரின் சமூகச் (ஜாதிச்) சான்றிதழைப் பொறுத்தோ, அல்லது "
                "விண்ணப்பதாரரின் பழைய சான்றிதழைப் பொறுத்தோ சமூகச் சான்றிதழ் "
                "வழங்கப்படும்.",
          "en": "The community certificate is issued on the basis of the "
                "parents' community certificate, or of the applicant's own "
                "earlier certificate."}),
    ]
    steps = [(t[L], b[L]) for t, b in steps_src]
    steps_html = "".join(
        f'<li><p class="nd-steps__title">{t}</p><p class="nd-steps__body">{b}</p></li>'
        for t, b in steps
    )
    howto = {
        "@context": "https://schema.org", "@type": "HowTo",
        "name": c("cert.h1", L) if L == "en" else
                "பௌத்தமேற்ற பட்டியலினத்தினர் சமூகச் சான்றிதழ் பெறுவது எப்படி",
        "inLanguage": L, "url": BASE + u("/certificate.html", L),
        "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": b}
                 for i, (t, b) in enumerate(steps)],
    }
    title = res_title("/certificate.html", L)
    return head(
        title, res_title("/certificate.html", LANGS[L]["other"]),
        c("cert.meta", L), "/certificate.html", L,
        jsonld=[crumb_ld(trail, L), howto, faq_ld(faq_for("cert", L))],
    ) + pagehead(title, c("cert.h1", L), c("cert.lede", L), trail, L) + f"""
<section class="nd-section">
  <div class="nd-shell">
    <div class="nd-grid nd-grid--aside">
      <div class="nd-prose">
        <div class="nd-alert nd-alert--success" style="margin-bottom:28px">
          {icon('check', 20)}
          <div>
            <p class="nd-alert__title">{c("cert.alert.h", L)}</p>
            <p>{c("cert.alert.p", L)}</p>
          </div>
        </div>

        <p class="nd-prose__lede">{c("cert.p1", L)}</p>
        <p>{c("cert.p2", L)}</p>

        <h2>{c("cert.steps.h", L)}</h2>
        <ol class="nd-steps">{steps_html}</ol>

        <h2>{c("cert.diff.h", L)}</h2>
        <dl class="nd-deflist">
          <div><dt>{c("cert.old.t", L)}</dt><dd>{c("cert.old.d", L)}</dd></div>
          <div><dt>{c("cert.new.t", L)}</dt><dd>{c("cert.new.d", L)}</dd></div>
        </dl>

        <div class="nd-alert nd-alert--info" style="margin-top:28px">
          {icon('info', 20)}
          <div>
            <p class="nd-alert__title">{c("cert.trouble.h", L)}</p>
            <p>{c("cert.trouble.p", L,
                   link=f'<a href="{u("/contact.html", L)}">{c("cert.trouble.link", L)}</a>')}</p>
          </div>
        </div>
      </div>

      <aside class="nd-stack-6">
        <div class="cm-card nd-card">
          <div class="nd-card__icon">{icon('shield', 22)}</div>
          <h3>{c("cert.go.h", L)}</h3>
          <p>{c("cert.go.p", L,
                 link=f'<a href="{u("/writings.html", L)}">{c("cert.go.link", L)}</a>')}</p>
        </div>
        <div class="cm-card" style="overflow:hidden">
          <img src="/assets/img/lion-capital-sarnath.jpg" loading="lazy"
               alt="{c("cert.lion.cap", L)}">
          <div style="padding:14px 16px;border-top:1px solid var(--cm-border-default)">
            <p class="cm-body-sm cm-text-muted" style="margin:0">{c("cert.lion.cap", L)}</p>
          </div>
        </div>
        <div class="cm-card nd-card">
          <p class="nd-eyebrow">{c("cert.help.h", L)}</p>
          <p style="margin-top:12px">{c("cert.help.p", L)}</p>
          <p style="margin-top:16px">
            <a class="cm-btn cm-btn--primary cm-btn--sm" href="{u("/contact.html", L)}">
              {c("events.contact", L)}</a>
          </p>
        </div>
      </aside>
    </div>
  </div>
</section>
""" + faq_block(U("faq", L), faq_for("cert", L), L) + related(
    U("related", L), [
        res_link("/names.html", L),
        res_link("/matrimony.html", L),
        ("/contact.html", U("contact", L), c("cert.help.p", L)),
    ], L) + footer(L)


def build_downloads(L):
    trail = [("/resources.html", U("resources", L)),
             (None, res_title("/downloads.html", L))]
    books = [
        ("The Bhilsa Topes", "Alexander Cunningham"),
        ("Ashoka: The Buddhist Emperor of India", "Vincent A. Smith"),
        ("Buddhist India", "Rhys Davids"),
        ("Notes on the Religious, Moral and Political State of Ancient India", "&ndash;"),
        ("The Life of Princess Yasodhara: Wife and Disciple of The Lord Buddha", "Sunity Devee"),
    ]
    rows = "".join(f"<tr><td>{t}</td><td>{a}</td></tr>" for t, a in books)
    title = res_title("/downloads.html", L)
    return head(
        title, res_title("/downloads.html", LANGS[L]["other"]),
        c("dl.meta", L), "/downloads.html", L, jsonld=[crumb_ld(trail, L)],
    ) + pagehead(title, c("dl.h1", L), c("dl.lede", L), trail, L) + f"""
<section class="nd-section">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2>{c("dl.audio.h", L)}</h2>
        <p>{c("dl.audio.sub", L)}</p>
      </div>
    </div>
    <div class="nd-grid nd-grid--2">
      <div class="cm-card nd-card">
        <div class="nd-card__icon">{icon('book', 22)}</div>
        <h3>{c("dl.a1.h", L)}</h3>
        <p>{c("dl.a1.p", L)}</p>
      </div>
      <div class="cm-card nd-card">
        <div class="nd-card__icon">{icon('sparkle', 22)}</div>
        <h3>{c("dl.a2.h", L)}</h3>
        <p>{c("dl.a2.p", L)}</p>
      </div>
    </div>
  </div>
</section>

<section class="nd-section nd-section--tight nd-well-band">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2>{c("dl.amb.h", L)}</h2>
        <p>{c("dl.amb.sub", L)}</p>
      </div>
    </div>
    <div class="nd-grid nd-grid--2">
      <div class="cm-card nd-card">
        <div class="nd-card__icon">{icon('download', 22)}</div>
        <h3>{c("dl.amb.ta.h", L)}</h3>
        <p>{c("dl.amb.ta.p", L)}</p>
      </div>
      <div class="cm-card nd-card">
        <div class="nd-card__icon">{icon('download', 22)}</div>
        <h3>{c("dl.amb.en.h", L)}</h3>
        <p>{c("dl.amb.en.p", L)}</p>
      </div>
    </div>
  </div>
</section>

<section class="nd-section">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2>{c("dl.books.h", L)}</h2>
        <p>{c("dl.books.sub", L)}</p>
      </div>
    </div>
    <div class="cm-card" style="overflow:hidden">
      <table class="cm-table" style="border:none;border-radius:0">
        <thead><tr><th scope="col">Title</th><th scope="col">Author</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <div class="nd-alert nd-alert--info" style="margin-top:20px">
      {icon('info', 20)}
      <div>
        <p class="nd-alert__title">{c("dl.pending.h", L)}</p>
        <p>{c("dl.pending.p", L,
               link=f'<a href="{u("/kathai/", L)}">{c("dl.pending.link", L)}</a>')}</p>
      </div>
    </div>
  </div>
</section>
""" + related(U("related", L), [
        ("/kathai/", U("kathai_short", L), c("kathai.meta3", L)),
        ("/writings.html", U("writings", L), c("writings.all.sub", L)),
        res_link("/names.html", L),
    ], L) + footer(L)


def build_dana(L):
    """Dana, the kinds of giving.

    A teaching page rather than a utility one, so every classification carries
    the text it comes from. Where a division is commentarial rather than
    canonical, it says so instead of borrowing a sutta number."""
    trail = [("/resources.html", U("resources", L)),
             (None, res_title("/dana.html", L))]
    title = res_title("/dana.html", L)

    def band(key, items, src=None):
        """One classification: a heading, a line of prose, a definition list."""
        rows = "".join(f"<div><dt>{c(f'dana.{t}.t', L)}</dt>"
                       f"<dd>{c(f'dana.{t}.d', L)}</dd></div>" for t in items)
        cite = (f'<p class="nd-cite">{icon("book", 14)} {c(src, L)}</p>'
                if src else "")
        return (f'<h2 id="dana-{key}">{c(f"dana.{key}.h", L)}</h2>'
                f'<p>{c(f"dana.{key}.p", L)}</p>'
                f'<dl class="nd-deflist">{rows}</dl>{cite}')

    why = "".join(f"<li>{c(f'dana.why.{i}', L)}</li>" for i in range(1, 9))
    pure = "".join(f"<li>{c(f'dana.pure.{i}', L)}</li>" for i in range(1, 5))

    return head(
        title, res_title("/dana.html", LANGS[L]["other"]),
        c("dana.meta", L), "/dana.html", L,
        jsonld=[crumb_ld(trail, L), {
            "@context": "https://schema.org", "@type": "Article",
            "headline": c("dana.h1", L), "url": BASE + u("/dana.html", L),
            "inLanguage": L, "description": c("dana.meta", L),
            "author": {"@id": BASE + "/#organization"},
            "publisher": {"@id": BASE + "/#organization"},
            "about": {"@type": "Thing", "name": "Dana",
                      "sameAs": "https://en.wikipedia.org/wiki/D%C4%81na"},
        }, faq_ld(faq_for("dana", L))],
    ) + pagehead(title, c("dana.h1", L), c("dana.lede", L), trail, L) + f"""
<section class="nd-section">
  <div class="nd-shell">
    <div class="nd-grid nd-grid--aside">
      <div class="nd-prose">
        <p class="nd-prose__lede">{c("dana.p1", L)}</p>
        <p>{c("dana.p2", L)}</p>

        {band("what", ["amisa", "abhaya", "dhamma"])}

        <aside class="nd-callout" aria-labelledby="dana-dhp">
          <p class="nd-callout__label" id="dana-dhp">{icon('quote', 18)}
            {c("dana.dhp.src", L)}</p>
          <p class="nd-callout__text">{c("dana.dhp", L)}</p>
        </aside>

        <div class="nd-alert nd-alert--accent" style="margin:28px 0">
          {icon('shield', 20)}
          <div>
            <p class="nd-alert__title">{c("dana.sila.h", L)}</p>
            <p>{c("dana.sila.p", L)}</p>
          </div>
        </div>

        {band("who", ["indiv", "sangha"], "dana.mn142")}
        {band("how", ["dasa", "sahaya", "sami"])}

        <h2 id="dana-why">{c("dana.why.h", L)}</h2>
        <p>{c("dana.why.p", L)}</p>
        <ol class="nd-numlist nd-numlist--marked">{why}</ol>
        <p class="nd-cite">{icon('book', 14)} {c("dana.an833", L)}</p>

        <h2 id="dana-us">{c("dana.us.h", L)}</h2>
        <p class="nd-prose__lede">{c("dana.us.p1", L)}</p>
        <p>{c("dana.us.p2", L)}</p>
        <p>{c("dana.us.p3", L)}</p>
        <p>{c("dana.us.p4", L)}</p>

        <h2 id="dana-six">{c("dana.six.h", L)}</h2>
        <p>{c("dana.six.p", L)}</p>
        <dl class="nd-deflist">
          <div><dt>{c("dana.six.giver", L)}</dt>
               <dd>{c("dana.six.giver.d", L)}</dd></div>
          <div><dt>{c("dana.six.recv", L)}</dt>
               <dd>{c("dana.six.recv.d", L)}</dd></div>
        </dl>

        <h2 id="dana-food">{c("dana.food.h", L)}</h2>
        <p>{c("dana.food.p", L)}</p>

        <h2 id="dana-pure">{c("dana.pure.h", L)}</h2>
        <p>{c("dana.pure.p", L)}</p>
        <ol class="nd-numlist">{pure}</ol>
        <p class="nd-cite">{icon('book', 14)} {c("dana.mn142", L)}</p>

        <h2 id="dana-amb">{c("dana.amb.h", L)}</h2>
        <p>{c("dana.amb.p", L)}</p>
        <p>{c("dana.amb.vow", L)}</p>
      </div>

      <aside class="nd-stack-6">
        <div class="cm-card nd-card">
          <div class="nd-card__icon">{icon('gift', 22)}</div>
          <h3>{c("dana.here.h", L)}</h3>
          <p>{c("dana.here.p", L)}</p>
          <p style="margin-top:16px">
            <a class="cm-btn cm-btn--secondary cm-btn--sm" href="{u("/events.html", L)}">
              {c("dana.here.link", L)} {icon('arrow', 16)}</a>
          </p>
        </div>
        <div class="cm-card nd-card">
          <p class="nd-eyebrow">{c("dana.what.h", L)}</p>
          <ul class="nd-ticks" style="margin-top:12px">
            <li>{c("dana.amisa.t", L)}</li>
            <li>{c("dana.abhaya.t", L)}</li>
            <li>{c("dana.dhamma.t", L)}</li>
          </ul>
        </div>
        <div class="cm-card nd-card">
          <div class="nd-card__icon">{icon('book', 22)}</div>
          <h3>{U("kathai_short", L)}</h3>
          <p>{U("footer_kathai", L)}</p>
          <p style="margin-top:16px">
            <a class="cm-btn cm-btn--secondary cm-btn--sm" href="{u("/kathai/", L)}">
              {U("read_all", L)} {icon('arrow', 16)}</a>
          </p>
        </div>
      </aside>
    </div>
  </div>
</section>
""" + faq_block(U("faq", L), faq_for("dana", L), L) + related(
    U("related", L), [
        ("/events.html", U("events_nav", L), c("dana.here.p", L)),
        res_link("/matrimony.html", L),
        ("/writings.html", U("writings", L), c("writings.all.sub", L)),
    ], L) + footer(L)


MATRIMONY_FAQ = [
    ("பௌத்த மகாமங்கள திருமணம் என்றால் என்ன?",
     "சாதி, சடங்கு, பொருட்செலவு என்ற சுமைகளின்றி, சமத்துவத்தை மையமாகக் "
     "கொண்டு நடத்தப்படும் திருமண முறை. வந்தனை, திரிசரணம், பஞ்சசீலம், "
     "உறுதிமொழி, ஆசி என அமைதியாக நிகழ்கிறது."),
    ("சங்கம் என்ன உதவி செய்யும்?",
     "திருமண நிகழ்வை முழுமையாக ஒருங்கிணைத்தல், பௌத்த முறையிலான "
     "வழிபாட்டு ஒழுங்கை வகுத்தல், அரசிதழில் பதிவு செய்வதற்கான "
     "வழிகாட்டுதல், திருமணச் சான்றிதழ் பெறுவதற்கான உதவி."),
    ("துணை தேடல் பதிவு எப்படி நடக்கிறது?",
     "விவரங்கள் சங்கத்திடம் மட்டுமே இருக்கும்; வெளியில் "
     "வெளியிடப்படுவதில்லை. பொருத்தமான தொடர்புகள் மட்டுமே இருதரப்பு "
     "ஒப்புதலுடன் பகிரப்படும்."),
]


def build_matrimony(L):
    trail = [("/resources.html", U("resources", L)),
             (None, res_title("/matrimony.html", L))]
    title = res_title("/matrimony.html", L)
    return head(
        title, res_title("/matrimony.html", LANGS[L]["other"]),
        c("mat.meta", L), "/matrimony.html", L,
        og_image="/assets/img/buddhist-temple-chennai.jpg",
        jsonld=[crumb_ld(trail, L), faq_ld(faq_for("matrimony", L))],
    ) + pagehead(title, c("mat.h1", L), c("mat.lede", L), trail, L) + f"""
<section class="nd-section">
  <div class="nd-shell">
    <div class="nd-grid nd-grid--aside">
      <div class="nd-prose">
        <p class="nd-prose__lede">{c("mat.p1", L)}</p>

        <h2>{c("mat.does.h", L)}</h2>
        <ul class="nd-tick">
          <li>{c("mat.d1", L)}</li>
          <li>{c("mat.d2", L)}</li>
          <li>{c("mat.d3", L)}</li>
          <li>{c("mat.d4", L)}</li>
          <li>{c("mat.d5", L)}</li>
        </ul>

        <h2>{c("mat.reg.h", L)}</h2>
        <p>{c("mat.reg.p", L,
               link=f'<a href="{u("/contact.html", L)}">{c("mat.reg.link", L)}</a>')}</p>

        <div class="nd-alert nd-alert--info">
          {icon('info', 20)}
          <div>
            <p class="nd-alert__title">{c("mat.priv.h", L)}</p>
            <p>{c("mat.priv.p", L)}</p>
          </div>
        </div>

        <h2>{c("mat.need.h", L)}</h2>
        <dl class="nd-deflist">
          <div><dt>{c("mat.n1.t", L)}</dt><dd>{c("mat.n1.d", L)}</dd></div>
          <div><dt>{c("mat.n2.t", L)}</dt><dd>{c("mat.n2.d", L)}</dd></div>
          <div><dt>{c("mat.n3.t", L)}</dt><dd>{c("mat.n3.d", L)}</dd></div>
          <div><dt>{c("mat.n4.t", L)}</dt><dd>{c("mat.n4.d", L)}</dd></div>
          <div><dt>{c("mat.n5.t", L)}</dt><dd>{c("mat.n5.d", L)}</dd></div>
        </dl>

        <p style="margin-top:28px">
          <a class="cm-btn cm-btn--primary" href="mailto:{EMAIL}?subject=Buddhist%20Matrimony">
            {icon('mail', 18)} {c("mat.send", L)}
          </a>
        </p>
      </div>

      <aside class="nd-stack-6">
        <div class="cm-card" style="overflow:hidden">
          <img src="/assets/img/buddhist-temple-chennai.jpg" loading="lazy"
               alt="{c("mat.vihar.cap", L)}">
          <div style="padding:14px 16px;border-top:1px solid var(--cm-border-default)">
            <p class="cm-body-sm cm-text-muted" style="margin:0">{c("mat.vihar.cap", L)}</p>
          </div>
        </div>
        <div class="cm-card nd-card">
          <div class="nd-card__icon">{icon('heart', 22)}</div>
          <h3>{c("mat.past.h", L)}</h3>
          <p>{c("mat.past.p", L,
                 link=f'<a href="{u("/writings.html", L)}">{c("mat.past.link", L)}</a>')}</p>
        </div>
      </aside>
    </div>
  </div>
</section>
""" + faq_block(c("mat.faq.h", L), faq_for("matrimony", L), L) + related(
    U("related", L), [
        res_link("/certificate.html", L),
        res_link("/names.html", L),
        ("/events.html", NAV[3][1] if L == "ta" else NAV[3][2], c("events.kinds.sub", L)),
    ], L) + footer(L)


def build_contact(L):
    trail = [(None, U("contact", L))]
    social = "".join(
        f'<li><a href="{link}" rel="me noopener">{n} {icon("external", 14)}</a></li>'
        for link, n in SOCIAL
    )
    return head(
        U("contact", L), "Contact" if L == "ta" else "தொடர்பு",
        c("contact.meta", L), "/contact.html", L,
        jsonld=[crumb_ld(trail, L), {
            "@context": "https://schema.org", "@type": "ContactPage",
            "url": BASE + u("/contact.html", L), "inLanguage": L,
            "mainEntity": {"@id": BASE + "/#organization"},
            "about": VENUE_LD,
        }],
    ) + pagehead(U("contact", L), c("contact.h1", L), c("contact.lede", L),
                 trail, L) + f"""
<section class="nd-section" aria-labelledby="contact-ways">
  <div class="nd-shell">
    <div class="nd-sechead">
      <div>
        <h2 id="contact-ways">{c("contact.ways.h", L)}</h2>
        <p>{c("contact.ways.sub", L)}</p>
      </div>
    </div>
    <div class="nd-grid nd-grid--2">
      <div class="cm-card nd-card">
        <div class="nd-card__icon">{icon('mail', 22)}</div>
        <h3>{c("contact.email.h", L)}</h3>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p style="margin-top:16px">
          <a class="cm-btn cm-btn--primary cm-btn--sm" href="mailto:{EMAIL}">{c("contact.write", L)}</a>
        </p>
      </div>
      <div class="cm-card nd-card">
        <div class="nd-card__icon">{icon('map', 22)}</div>
        <h3>{c("contact.place.h", L)}</h3>
        <address class="nd-address">
          <strong>{U("venue", L)}</strong>
          <span>{U("venue_addr", L)}</span>
          <span lang="en">{VENUE_EN}, {VENUE_STREET}, {VENUE_CITY} {VENUE_PIN}</span>
        </address>
        <p class="cm-body-sm cm-text-muted" style="margin-top:12px">{c("about.when", L)}</p>
        <p class="nd-row" style="margin-top:16px">
          <a class="cm-btn cm-btn--primary cm-btn--sm" href="{MAPS_URL}" rel="noopener">
            {icon('map', 16)} {U("directions", L)}
          </a>
          <a class="cm-btn cm-btn--secondary cm-btn--sm" href="{u("/events.html", L)}">
            {NAV[3][1] if L == "ta" else NAV[3][2]}</a>
        </p>
      </div>
      <div class="cm-card nd-card">
        <div class="nd-card__icon">{icon('users', 22)}</div>
        <h3>{c("contact.social.h", L)}</h3>
        <ul class="nd-linklist">{social}</ul>
      </div>
      <div class="cm-card nd-card">
        <div class="nd-card__icon">{icon('book', 22)}</div>
        <h3>{c("contact.vip.h", L)}</h3>
        <p>{c("contact.vip.p", L)}</p>
      </div>
    </div>

    <div class="nd-alert nd-alert--accent" style="margin-top:32px">
      {icon('check', 20)}
      <div>
        <p class="nd-alert__title">{c("contact.welcome.h", L)}</p>
        <p>{c("contact.welcome.p", L,
               link1=f'<a href="{u("/about.html", L)}">{c("contact.welcome.link1", L)}</a>',
               link2=f'<a href="{u("/kathai/", L)}">{c("contact.welcome.link2", L)}</a>')}</p>
      </div>
    </div>
  </div>
</section>
""" + footer(L)


def build_404(L):
    return head(
        c("404.h1", L), "Not Found" if L == "ta" else "404",
        c("404.meta", L), "/404.html", L, noindex=True,
    ) + f"""
<section class="nd-section">
  <div class="nd-shell nd-reading" style="text-align:center;padding:60px 0">
    <p class="nd-eyebrow">404</p>
    <h1 style="font-size:31px;margin-top:10px">{c("404.h1", L)}</h1>
    <p class="cm-body-lg cm-text-muted" style="margin-top:14px">{c("404.p", L)}</p>
    <p class="nd-row" style="justify-content:center;margin-top:28px">
      <a class="cm-btn cm-btn--primary" href="{u("/index.html", L)}">{U("home", L)}</a>
      <a class="cm-btn cm-btn--secondary" href="{u("/kathai/", L)}">{U("kathai_short", L)}</a>
      <a class="cm-btn cm-btn--secondary" href="{u("/writings.html", L)}">{U("writings", L)}</a>
    </p>
  </div>
</section>
""" + footer(L)


# ==========================================================================
# Sitemap / robots
# ==========================================================================


# ==========================================================================
# iCalendar feed
#
# The sangha's Google Calendar is empty, so the page was pointing at nothing.
# This publishes the same events the page shows as a real calendar file, which
# can be imported once or, better, subscribed to by URL: the site rebuilds
# daily, so a subscription stays current on its own.
#
# Times are written in UTC with a Z suffix, which avoids shipping a VTIMEZONE
# block and is unambiguous everywhere. Anniversaries are all-day dates that
# repeat yearly.
# ==========================================================================

def ics_escape(t):
    """RFC 5545 text escaping: backslash, semicolon, comma, newline."""
    t = re.sub(r"<[^>]+>", "", str(t))
    return (t.replace("\\", "\\\\").replace(";", "\\;")
             .replace(",", "\\,").replace("\n", "\\n").strip())


def ics_fold(line):
    """RFC 5545 lines are folded at 75 octets, continued with a leading space."""
    out, cur = [], ""
    for ch in line:
        if len((cur + ch).encode("utf-8")) > 73:
            out.append(cur)
            cur = " " + ch
        else:
            cur += ch
    out.append(cur)
    return out


def build_ics(moons, all_moons, L):
    from datetime import date, datetime, timedelta

    def pournami_no(d):
        return 178 + sum(1 for m in all_moons if "2026-07-29" < m["date"] <= d)

    name = ({"ta": "நிலாதம்மா நாட்காட்டி", "en": "Niladhamma calendar"})[L]
    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0",
        "PRODID:-//Niladhamma//Sangha calendar//" + L.upper(),
        "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
        f"X-WR-CALNAME:{ics_escape(name)}",
        "X-WR-TIMEZONE:Asia/Kolkata",
        f"X-WR-CALDESC:{ics_escape(c('cal.sub', L))}",
        "REFRESH-INTERVAL;VALUE=DURATION:P1D",
        "X-PUBLISHED-TTL:P1D",
    ]
    # a fixed stamp keeps the file byte-identical between builds on the same day
    stamp = TODAY.replace("-", "") + "T000000Z"
    venue = f"{U('venue', L)}, {U('venue_addr', L)}"

    for m in moons[:24]:
        d = observed_date(m)
        y, mo, dd = map(int, d.split("-"))
        # 18:00 IST is 12:30 UTC; the gathering runs about two hours
        start = datetime(y, mo, dd, 12, 30)
        end = start + timedelta(hours=2)
        n = pournami_no(m["date"])
        summ = ({"ta": f"{n}வது தொடர் பௌர்ணமி கூட்டம்",
                 "en": f"Full moon gathering no. {n}"})[L]
        lines += [
            "BEGIN:VEVENT",
            f"UID:pournami-{d}@niladhamma.co.in",
            f"DTSTAMP:{stamp}",
            f"DTSTART:{start:%Y%m%dT%H%M%S}Z",
            f"DTEND:{end:%Y%m%dT%H%M%S}Z",
            f"SUMMARY:{ics_escape(summ)}",
            f"LOCATION:{ics_escape(venue)}",
            f"DESCRIPTION:{ics_escape(c('events.at.sub', L))}",
            f"URL:{BASE}{u('/events.html', L)}",
            "END:VEVENT",
        ]

    for row in FIXED_DAYS:
        dd_mm, nm, yr, desc = row[:4]
        d, mo = dd_mm.split("-")
        first = f"{TODAY[:4]}{mo}{d}"
        lines += [
            "BEGIN:VEVENT",
            f"UID:anniversary-{mo}{d}@niladhamma.co.in",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{first}",
            f"DTEND;VALUE=DATE:{(date(int(TODAY[:4]), int(mo), int(d)) + timedelta(days=1)):%Y%m%d}",
            "RRULE:FREQ=YEARLY",
            f"SUMMARY:{ics_escape(nm[L])} ({yr})",
            f"DESCRIPTION:{ics_escape(desc[L])}",
            f"URL:{BASE}{u('/events.html', L)}",
            "TRANSP:TRANSPARENT",
            "END:VEVENT",
        ]

    lines.append("END:VCALENDAR")
    folded = []
    for ln in lines:
        folded += ics_fold(ln)
    return "\r\n".join(folded) + "\r\n"


def build_sitemap(urls):
    body = "".join(
        f"<url><loc>{BASE}{u}</loc><changefreq>{cf}</changefreq>"
        f"<priority>{pr}</priority></url>"
        for u, cf, pr in urls
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + body + "</urlset>\n")


def build_robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n"


# ==========================================================================

def main():
    posts = load("posts.json")
    names = load("names.json")
    all_moons = load("moons.json")["moons"]
    moons = [x for x in all_moons if x["date"] >= TODAY]

    # Load every collection and apply the release gate. Withholding happens
    # here, at build time: an unreleased story is never written to disk, listed
    # in the sitemap, or present in any page's HTML.
    colls = []
    for cl in COLLECTIONS:
        data = load(cl["file"])
        en_data = load(cl["en_file"]) if cl["en_file"] else None
        every = data["stories"]
        live = [x for x in every if x.get("release", "0000-00-00") <= TODAY]
        colls.append((cl, data, en_data, live, len(every) - len(live)))

    # Blogger markup is parsed once per post; both languages render from the
    # blocks, and the display copies of the photographs are written if missing.
    made = make_tiles(posts)
    for x in posts:
        x["blocks"] = parse_body(x["html"])

    try:
        pen = {x["slug"]: x for x in load("posts_en.json")}
        try:
            caps = load("captions_en.json")
        except FileNotFoundError:
            caps = {}
        for x in posts:
            e = pen.get(x["slug"])
            if not e:
                continue
            x.update({k: v for k, v in e.items() if k in ("title_en", "text_en")})
            if e.get("body_en"):
                x["blocks_en"] = compose_en(x["blocks"], e["body_en"], caps)
                x.setdefault("text_en", " ".join(e["body_en"]))
            elif e.get("html_en"):
                x["blocks_en"] = parse_body(e["html_en"])
    except FileNotFoundError:
        pass

    # Titles collide in one language without colliding in the other, so the
    # date disambiguator is decided per language.
    for L in LANGS:
        seen = collections.Counter(post_title(x, L) for x in posts)
        for x in posts:
            x[f"title_dup_{L}"] = seen[post_title(x, L)] > 1

    print(f"Building Niladhamma (Canopy) · ta + en · today {TODAY} (IST)")
    for cl, _d, _e, live, held in colls:
        line = f"  {cl['slug']:8s} {len(live):2d}/{len(live) + held} live"
        if held:
            nxt = min(x["release"] for x in load(cl["file"])["stories"]
                      if x["release"] > TODAY)
            line += f", {held} held, next on {nxt}"
        print(line)

    # the home page peeks at the newest collection that has anything live
    peek = next(((cl, e, lv) for cl, _d, e, lv, _h in reversed(colls) if lv),
                (colls[0][0], colls[0][2], []))

    urls = []
    for L in LANGS:
        pages = [
            ("/index.html", build_index(posts, peek[0], peek[2][:6], peek[1], L), "weekly", "1.0"),
            ("/about.html", build_about(L), "monthly", "0.9"),
            ("/kathai/index.html",
             build_kathai_hub([(cl, d, len(lv), len(lv) + h)
                               for cl, d, _e, lv, h in reversed(colls)], L),
             "weekly", "0.9"),
            ("/events.html", build_events(posts, moons, all_moons, L), "weekly", "0.8"),
            ("/writings.html", build_writings(posts, L), "weekly", "0.8"),
            ("/resources.html", build_resources(L), "monthly", "0.7"),
            ("/dana.html", build_dana(L), "yearly", "0.7"),
            ("/names.html", build_names(names, L), "yearly", "0.7"),
            ("/certificate.html", build_certificate(L), "yearly", "0.7"),
            ("/downloads.html", build_downloads(L), "yearly", "0.6"),
            ("/matrimony.html", build_matrimony(L), "yearly", "0.6"),
            ("/contact.html", build_contact(L), "yearly", "0.6"),
        ]
        n = 0
        for path, html, cf, pr in pages:
            write(fpath(path, L), html)
            urls.append((u(path, L), cf, pr))
            n += 1

        for cl, data, en_data, live, held in colls:
            slug = cl["slug"]
            write(fpath(coll_url(slug) + "index.html", L),
                  build_kathai_index(cl, data, en_data, live, held, L))
            urls.append((u(coll_url(slug), L), "weekly" if held else "monthly", "0.9"))
            n += 1
            for i, st in enumerate(live):
                prev_s = live[i - 1] if i else None
                next_s = live[i + 1] if i + 1 < len(live) else None
                write(fpath(story_url(slug, st["day"]), L),
                      build_story(st, prev_s, next_s, cl, data, en_data, L))
                urls.append((u(story_url(slug, st["day"]), L), "yearly", "0.7"))
                n += 1

        for i, po in enumerate(posts):
            newer = posts[i - 1] if i else None
            older = posts[i + 1] if i + 1 < len(posts) else None
            # The four nearest posts in date order, and always four: a partial
            # row left a gap under the last card on the newest and oldest posts.
            near = [q for q in posts if q is not po]
            start = min(max(0, i - 2), max(0, len(near) - 4))
            rel = near[start:start + 4]
            write(fpath(post_url(po), L), build_post(po, older, newer, rel, L))
            urls.append((u(post_url(po), L), "yearly", "0.6"))
            n += 1

        write(fpath("/404.html", L), build_404(L))
        print(f"  {LANGS[L]['name']:8s} {n + 1:4d} pages under {LANGS[L]['prefix'] or '/'}")

    for L in LANGS:
        write(fpath("/niladhamma.ics", L), build_ics(moons, all_moons, L))

    write("/sitemap.xml", build_sitemap(urls))
    write("/robots.txt", build_robots())

    removed = sweep()
    if removed:
        print(f"  swept {len(removed)} page(s) no longer published")
    total_live = sum(len(lv) for _c, _d, _e, lv, _h in colls)
    if made:
        print(f"  photographs  {made} display copies written")
    cached = save_sizes()
    if cached:
        print(f"  photographs  {cached} sizes cached for hosts without Pillow")
    print(f"  sitemap.xml  {len(urls)} URLs")
    print(f"Done. {len(posts)} posts, {total_live} stories live, "
          f"{sum(len(v) for v in names.values())} names.")


if __name__ == "__main__":
    main()
