#!/usr/bin/env python3
"""Per-PDF inclusion-appropriateness check for the 163 included studies.

For each included study that has a source PDF, confirm the full text carries the
eligibility signature — breast + incidence/rate + White + a race/ethnicity term.
Studies without a PDF get verdict AUTHOR (cannot be checked without the full text).
Writes outputs/Inclusion_verification_report.csv, one row per included study.
"""
import csv, os, glob, re
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
FT = os.path.join(HERE, "fulltext")
RACE = ["race", "ethnic", "black", "white", "hispanic", "asian", "american indian",
        "alaska", "native hawaiian", "nhw", "nh white"]

def text(rid):
    parts = []
    for p in [os.path.join(FT, "%s.pdf" % rid)] + sorted(glob.glob(os.path.join(FT, "%s_supple*.pdf" % rid))):
        if os.path.exists(p):
            try:
                with pdfplumber.open(p) as pf:
                    parts.append("\n".join((pg.extract_text() or "") for pg in pf.pages))
            except Exception:
                pass
    return " ".join(parts).lower()

def main():
    inc = list(csv.DictReader(open(os.path.join(HERE, "TableS_included_studies.csv"), encoding="utf-8")))
    out = []
    for r in inc:
        rid = r["record_id"]
        if not os.path.exists(os.path.join(FT, "%s.pdf" % rid)):
            out.append([rid, r.get("pmid", ""), r.get("synth_group", ""), "AUTHOR",
                        "no source PDF (confirm eligibility from full text)", r.get("citation", "")[:80]])
            continue
        t = text(rid)
        sig = {"breast": "breast" in t, "rate": ("incidence" in t or "rate" in t),
               "white": "white" in t, "race": any(k in t for k in RACE)}
        if all(sig.values()):
            out.append([rid, r.get("pmid", ""), r.get("synth_group", ""), "VERIFIED",
                        "eligibility signature present", r.get("citation", "")[:80]])
        else:
            missing = ",".join(k for k, v in sig.items() if not v)
            verdict = "AUTHOR" if not sig["breast"] and not sig["rate"] else "REVIEW"
            out.append([rid, r.get("pmid", ""), r.get("synth_group", ""), verdict,
                        "signature missing: " + missing + " (likely image PDF or narrative-only)", r.get("citation", "")[:80]])
    with open(os.path.join(HERE, "outputs", "Inclusion_verification_report.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["rec_id", "PMID", "synth_group", "verdict", "detail", "citation"])
        w.writerows(out)
    from collections import Counter
    print("inclusion report: %d studies |" % len(out), dict(Counter(x[3] for x in out)))

if __name__ == "__main__":
    main()
