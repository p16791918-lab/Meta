#!/usr/bin/env python3
"""Dump candidate breast-cancer race/ethnicity IRR / rate / RR signal lines from
a study's full text, to drive manual extraction into breast_extraction.csv.
Usage: python3 scan_estimates.py <record_id> [<record_id> ...]
"""
import re
import sys
import os

RACE = (r"non-Hispanic [Ww]hite|NHW|NHB|non-Hispanic [Bb]lack|African American|"
        r"Hispanic|Latina|[Bb]lack|[Ww]hite|Asian|Chinese|Japanese|Korean|Filipin|"
        r"Vietnamese|Hmong|Cambodian|Laotian|South Asian|Asian Indian|Pakistani|"
        r"Native Hawaiian|Hawaiian|Chamorro|Samoan|Pacific Islander|American Indian|"
        r"Alaska Native|AI/AN|AIAN|Navajo|Cuban|Mexican|Puerto Rican")
NUM = r"\d\.\d\d?|\d{1,3}\.\d"


def scan(rid):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fulltext", "%s.txt" % rid)
    if not os.path.isfile(p):
        print("## %s : NO FULLTEXT" % rid)
        return
    t = open(p, encoding="utf-8").read()
    title = t.split("\n", 1)[0]
    print("\n" + "#" * 70)
    print("## rec %s  (%d chars)\n%s" % (rid, len(t), title[:120]))
    # method signals
    for kw in ["age-adjust", "standard population", "2000 US", "1970", "per 100 000",
               "per 100,000", "incidence rate ratio", "\brate ratio\b", "\bSIR\b", "\bIRR\b",
               "diagnosed", "SEER", "NAACCR", "USCS", "Registry"]:
        m = re.search(kw, t, re.I)
        if m:
            print("  [method:%s] ...%s..." % (kw.strip("\\b"),
                  t[m.start()-20:m.start()+55].replace("\n", " ").strip()[:80]))
    print("  --- signal lines (breast + race + number) ---")
    seen = set()
    for m in re.finditer(r"[^\n.]{0,80}(?:%s)[^\n.]{0,120}" % RACE, t):
        seg = m.group(0).replace("\n", " ").strip()
        if re.search(NUM, seg) and re.search(r"breast|IRR|RR|rate ratio|SIR|per 100|incidence", seg, re.I):
            key = seg[:60]
            if key not in seen:
                seen.add(key)
                print("   ::", seg[:200])


if __name__ == "__main__":
    for rid in sys.argv[1:]:
        scan(rid)
