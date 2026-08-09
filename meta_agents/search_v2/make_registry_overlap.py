#!/usr/bin/env python3
"""Build the registry-overlap characterization table (Table S-A) for included
studies, so non-independent (overlapping) registry data can be collapsed to one
representative estimate per registry family in the quantitative synthesis.

For each included study (ft_eligibility.csv include-*), extract from the full text:
  - registry system  : SEER version(s), USCS(NPCR+SEER), NAACCR/CiNA, or the
                        state/regional registry named in ft_eligibility.
  - study period      : preferring an explicit "diagnosed from X to/through Y"
                        statement; year-range fallbacks are flagged (verify).
  - US coverage       : "% of the US population" if stated.
SEER version -> geographic scope is a fixed lookup (version defines the registries).

Output: TableSA_registry_overlap.csv  (record_id, citation, registry_family,
        seer_version, study_period, pct_us, coverage_note, verify).
"""
import csv
import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
MERGED = os.path.join(HERE, "merged_unique.csv")
ELIG = os.path.join(HERE, "ft_eligibility.csv")
OUT = os.path.join(HERE, "TableSA_registry_overlap.csv")

# SEER version -> approximate geographic scope (version defines the registry set)
SEER_SCOPE = {
    "9": "SEER9 ~10% US (SF, CT, Detroit, HI, IA, NM, Seattle, UT, Atlanta; 1975+)",
    "12": "SEER12 (+San Jose, LA, rural GA, AK Native)",
    "13": "SEER13 ~14% US (+LA, San Jose-Monterey, rural GA, AK Native; 1992+)",
    "17": "SEER17 ~26% US (+Greater CA, KY, LA, NJ, GA; 2000+)",
    "18": "SEER18 ~28% US (SEER17 + Greater GA)",
    "21": "SEER21 ~37% US (+ID, MA, etc.)",
    "22": "SEER22 ~48% US (expanded)",
}


def scan(rid):
    p = os.path.join(HERE, "fulltext", "%d.txt" % rid)
    if not os.path.isfile(p):
        return None
    t = open(p, encoding="utf-8").read()
    body = t.split("\n\n", 1)[1] if "\n\n" in t else t

    versions = sorted(set(re.findall(r"SEER[\s-]?(\d\d?)\b", body)),
                      key=lambda x: int(x))
    versions = [v for v in versions if v in SEER_SCOPE]  # drop stray numbers
    uscs = bool(re.search(r"\bUSCS\b|U\.?S\.? Cancer Statistics|National Program of Cancer Registries|\bNPCR\b", body))
    naaccr = bool(re.search(r"\bNAACCR\b|\bCiNA\b|North American Association of Central", body))

    # study period: prefer an explicit diagnosis-window statement
    period, verify = "", ""
    m = re.search(r"diagnos\w+[^.]{0,60}?\b(19[7-9]\d|20[0-2]\d)\s*(?:to|through|[–\-—])\s*(20[0-2]\d|19[7-9]\d)\b",
                  body, re.I)
    if not m:
        m = re.search(r"\b(?:from|during|between)\s+(19[7-9]\d|20[0-2]\d)\s*(?:to|through|and|[–\-—])\s*(20[0-2]\d|19[7-9]\d)\b",
                      body, re.I)
    if m:
        period = "%s-%s" % (m.group(1), m.group(2))
    else:
        ranges = Counter("%s-%s" % (a, b) for a, b in
                         re.findall(r"\b(19[7-9]\d|20[0-2]\d)\s*[–\-—]\s*(20[0-2]\d|19[7-9]\d)\b", body))
        if ranges:
            period = ranges.most_common(1)[0][0]
            verify = "period auto-guess - verify"

    pct = re.findall(r"(\d{1,2}(?:\.\d)?)\s*%\s*of the (?:total\s+)?U\.?S\.?(?:\s|-)?population", body, re.I)
    return {
        "seer_version": ",".join("SEER" + v for v in versions),
        "uscs": uscs, "naaccr": naaccr,
        "period": period, "verify": verify,
        "pct_us": pct[0] if pct else "",
        "scope": "; ".join(SEER_SCOPE[v] for v in versions),
    }


def main():
    recs = list(csv.DictReader(open(MERGED, encoding="utf-8")))
    out = []
    for r in csv.DictReader(open(ELIG, encoding="utf-8")):
        if not r.get("ft_decision", "").startswith("include"):
            continue
        rid = int(r["record_id"])
        s = scan(rid)
        if s is None:
            continue
        rec = recs[rid]
        system = s["seer_version"]
        if s["uscs"]:
            system = (system + " + " if system else "") + "USCS(NPCR+SEER ~99%)"
        if s["naaccr"] and "NAACCR" not in system:
            system = (system + " + " if system else "") + "NAACCR/CiNA(~93%)"
        out.append({
            "record_id": rid,
            "citation": "%s (%s)" % (rec.get("title", "")[:70], rec.get("year", "")),
            "registry_family": r.get("registry_family", ""),
            "registry_system_detected": system or "(state/regional - see registry_family)",
            "study_period": s["period"],
            "pct_us": s["pct_us"],
            "coverage_scope": s["scope"],
            "verify": s["verify"],
        })
    out.sort(key=lambda x: (x["registry_family"], x["record_id"]))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["record_id", "citation", "registry_family",
                                          "registry_system_detected", "study_period",
                                          "pct_us", "coverage_scope", "verify"])
        w.writeheader()
        w.writerows(out)
    print("registry-overlap rows: %d -> %s" % (len(out), os.path.basename(OUT)))
    print("need period verification:", sum(1 for x in out if x["verify"]))


if __name__ == "__main__":
    main()
