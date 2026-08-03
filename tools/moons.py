#!/usr/bin/env python3
"""
Compute full moon instants (Meeus, Astronomical Algorithms ch. 49) and write
data/moons.json for the calendar page.

    python3 tools/moons.py 2026 2028

Accuracy is well under an hour, which is far tighter than we need: the page
shows the calendar date in IST. Observance in the Theravada tradition follows a
local lunar reckoning that can differ from the astronomical instant by a day, so
the page says so rather than presenting these as ritual dates.
"""

import json
import math
import os
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IST = timezone(timedelta(hours=5, minutes=30))

# Tamil month a full moon most often falls in, keyed by Gregorian month. Used
# only as a label; the authoritative field is the date.
TA_MONTHS = ["ஜனவரி", "பிப்ரவரி", "மார்ச்", "ஏப்ரல்", "மே", "ஜூன்",
             "ஜூலை", "ஆகஸ்ட்", "செப்டம்பர்", "அக்டோபர்", "நவம்பர்", "டிசம்பர்"]
EN_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]


def jde_full_moon(k):
    """Julian Ephemeris Day of the full moon for lunation index k + 0.5."""
    k = k + 0.5
    T = k / 1236.85
    jde = (2451550.09766 + 29.530588861 * k
           + 0.00015437 * T ** 2 - 0.000000150 * T ** 3 + 0.00000000073 * T ** 4)
    E = 1 - 0.002516 * T - 0.0000074 * T ** 2
    r = math.radians
    M = r((2.5534 + 29.10535670 * k - 0.0000014 * T ** 2 - 0.00000011 * T ** 3) % 360)
    Mp = r((201.5643 + 385.81693528 * k + 0.0107582 * T ** 2
            + 0.00001238 * T ** 3 - 0.000000058 * T ** 4) % 360)
    F = r((160.7108 + 390.67050284 * k - 0.0016118 * T ** 2
           - 0.00000227 * T ** 3 + 0.000000011 * T ** 4) % 360)
    O = r((124.7746 - 1.56375588 * k + 0.0020672 * T ** 2 + 0.00000215 * T ** 3) % 360)

    c = (-0.40614 * math.sin(Mp)
         + 0.17302 * E * math.sin(M)
         + 0.01614 * math.sin(2 * Mp)
         + 0.01043 * math.sin(2 * F)
         + 0.00734 * E * math.sin(Mp - M)
         - 0.00515 * E * math.sin(Mp + M)
         + 0.00209 * E * E * math.sin(2 * M)
         - 0.00111 * math.sin(Mp - 2 * F)
         - 0.00057 * math.sin(Mp + 2 * F)
         + 0.00056 * E * math.sin(2 * Mp + M)
         - 0.00042 * math.sin(3 * Mp)
         + 0.00042 * E * math.sin(M + 2 * F)
         + 0.00038 * E * math.sin(M - 2 * F)
         - 0.00024 * E * math.sin(2 * Mp - M)
         - 0.00017 * math.sin(O)
         - 0.00007 * math.sin(Mp + 2 * M))

    A = [(299.77 + 0.107408 * k - 0.009173 * T ** 2, 0.000325),
         (251.88 + 0.016321 * k, 0.000165), (251.83 + 26.651886 * k, 0.000164),
         (349.42 + 36.412478 * k, 0.000126), (84.66 + 18.206239 * k, 0.000110),
         (141.74 + 53.303771 * k, 0.000062), (207.14 + 2.453732 * k, 0.000060),
         (154.84 + 7.306860 * k, 0.000056), (34.52 + 27.261239 * k, 0.000047),
         (207.19 + 0.121824 * k, 0.000042), (291.34 + 1.844379 * k, 0.000040),
         (161.72 + 24.198154 * k, 0.000037), (239.56 + 25.513099 * k, 0.000035),
         (331.55 + 3.592518 * k, 0.000023)]
    add = sum(amp * math.sin(r(ang % 360)) for ang, amp in A)
    return jde + c + add


def jd_to_utc(jd):
    return datetime(2000, 1, 1, 12, tzinfo=timezone.utc) + timedelta(days=jd - 2451545.0)


def full_moons(y0, y1):
    out = []
    k0 = int((y0 - 2000) * 12.3685) - 2
    for k in range(k0, k0 + (y1 - y0 + 2) * 13):
        utc = jd_to_utc(jde_full_moon(k))
        ist = utc.astimezone(IST)
        if y0 <= ist.year <= y1:
            out.append(ist)
    return sorted(out)


def main():
    y0 = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
    y1 = int(sys.argv[2]) if len(sys.argv) > 2 else y0 + 2
    rows = []
    for d in full_moons(y0, y1):
        rows.append({
            "date": d.strftime("%Y-%m-%d"),
            "time_ist": d.strftime("%H:%M"),
            "label_ta": f"{d.day} {TA_MONTHS[d.month - 1]} {d.year}",
            "label_en": f"{d.day} {EN_MONTHS[d.month - 1]} {d.year}",
        })
    with open(os.path.join(ROOT, "data", "moons.json"), "w", encoding="utf-8") as f:
        json.dump({"generated_for": [y0, y1], "moons": rows}, f,
                  ensure_ascii=False, indent=1)
    print(f"wrote data/moons.json · {len(rows)} full moons {y0}-{y1}")
    for r in rows[:4]:
        print(f"  {r['date']} {r['time_ist']} IST")


if __name__ == "__main__":
    main()
