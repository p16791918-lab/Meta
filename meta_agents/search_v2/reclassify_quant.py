#!/usr/bin/env python3
"""Triage the include-quant studies by their DOMINANT reported metric, to
separate truly poolable (numeric IRR/RR/SIR or race-specific rates with CI vs
NHW) from narrative-only (APC/EAPC trends, %-proportions, figure-only, or a
non-NHW comparator). First-pass automated signal; each flip is confirmed by
hand before ft_eligibility is changed.
"""
import csv, os, re
HERE = os.path.dirname(os.path.abspath(__file__))

def signals(rid, extracted):
    p = os.path.join(HERE, "fulltext", "%s.txt" % rid)
    pdf = os.path.join(HERE, "fulltext", "%s.pdf" % rid)
    if rid in extracted:
        return "POOLABLE(extracted)"
    if not os.path.exists(p):
        return "NO-TEXT(pdf only)" if os.path.exists(pdf) else "NO-SOURCE"
    t = open(p, encoding="utf-8").read()
    low = t.lower()
    # numeric race-specific IRR / RR / SIR with a CI
    has_irr = bool(re.search(r"(black|white|hispanic|asian|native|indian|hawaiian|filipin|japanese|korean|chinese|nhb|nhw|ai/an)[^\n]{0,45}(irr|rate ratio|incidence rate ratio|\brr\b|\bsir\b)\s*[=:(]?\s*\d\.\d\d", low))
    # race-specific rate (2-3 digit) with CI near race
    has_rate_ci = bool(re.search(r"(black|white|hispanic|asian|native|hawaiian|nhb|nhw)[^\n]{0,40}\d{2,3}\.\d\s*[\[(]\s*(?:95)?", low))
    apc = bool(re.search(r"\b(apc|eapc|aapc|annual percent)\b", low))
    pir = bool(re.search(r"\bpir\b|proportional incidence", low))
    if has_irr or has_rate_ci:
        return "POOLABLE(has numeric IRR/rate+CI in text)"
    if pir:
        return "NARRATIVE(PIR/non-standard)"
    if apc and not (has_irr or has_rate_ci):
        return "NARRATIVE?(APC/trend-dominant)"
    return "CHECK(no clear numeric IRR in text - table/figure?)"

def main():
    elig = list(csv.DictReader(open(os.path.join(HERE, "ft_eligibility.csv"), encoding="utf-8")))
    extracted = {r["record_id"] for r in csv.DictReader(open(os.path.join(HERE, "breast_extraction.csv"), encoding="utf-8"))}
    iq = [r for r in elig if r["ft_decision"] == "include-quant"]
    from collections import Counter
    cats = Counter()
    rows = []
    for r in iq:
        s = signals(r["record_id"], extracted)
        cats[s.split("(")[0]] += 1
        rows.append((r["record_id"], s))
    print("include-quant triage (%d studies):" % len(iq))
    for k, v in cats.most_common():
        print("  %-12s %d" % (k, v))
    # write proposal
    with open(os.path.join(HERE, "RECLASSIFY_PROPOSAL.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["record_id", "triage_signal"])
        for rid, s in sorted(rows, key=lambda x: x[1]): w.writerow([rid, s])
    print("\nwrote RECLASSIFY_PROPOSAL.csv")

if __name__ == "__main__":
    main()
