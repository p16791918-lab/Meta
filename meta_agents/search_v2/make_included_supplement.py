#!/usr/bin/env python3
"""Compile the PRISMA supplementary "Characteristics of included studies" table
(the companion to the excluded-with-reasons table). Re-runnable — regenerates
from ft_eligibility.csv as the eligibility assessment progresses.

Included = ft_decision in {include-quant, include-narrative}. 'include-quant'
means the study contributed extractable NHW-referenced rates/IRRs to quantitative
synthesis; 'include-narrative' means eligible but synthesized narratively.

Outputs:
  TableS_included_studies.csv   (machine-readable)
  TableS_included_studies.md    (manuscript-ready supplementary table)
"""
import csv
import os
import re


def norm_groups(s):
    """Standardize umbrella shorthand in the free-text 'groups vs NHW' coverage note
    to match the analysis labels: API -> AANHPI, AIAN -> AI/AN (word-boundary)."""
    s = re.sub(r"\bAPI\b", "AANHPI", s)
    s = re.sub(r"\bAIAN\b", "AI/AN", s)
    return s

HERE = os.path.dirname(os.path.abspath(__file__))
MERGED = os.path.join(HERE, "merged_unique.csv")
ELIG = os.path.join(HERE, "ft_eligibility.csv")
OUT_CSV = os.path.join(HERE, "TableS_included_studies.csv")
OUT_MD = os.path.join(HERE, "TableS_included_studies.md")


def main():
    recs = list(csv.DictReader(open(MERGED, encoding="utf-8")))
    out = []
    for r in csv.DictReader(open(ELIG, encoding="utf-8")):
        dec = r.get("ft_decision", "").strip()
        if dec not in ("include-quant", "include-narrative"):
            continue
        rid = int(r["record_id"])
        rec = recs[rid] if 0 <= rid < len(recs) else {}
        out.append({
            "record_id": rid,
            "citation": "%s (%s)" % (rec.get("title", ""), rec.get("year", "")),
            "data_source": r.get("registry_family", "").strip(),
            "groups_vs_nhw": norm_groups(r.get("groups_vs_nhw", "").strip()),
            "outcome_measure": r.get("rate_location", "").strip(),
            "synthesis": "quantitative" if dec == "include-quant" else "narrative",
            "note": r.get("note", "").strip(),
            "pmid": rec.get("pmid", ""),
            "doi": rec.get("doi", ""),
        })
    out.sort(key=lambda x: x["record_id"])

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["record_id", "citation", "data_source",
                                          "groups_vs_nhw", "outcome_measure",
                                          "synthesis", "note", "pmid", "doi"])
        w.writeheader()
        w.writerows(out)

    from collections import Counter
    counts = Counter(x["synthesis"] for x in out)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# Table S. Characteristics of included studies\n\n")
        f.write("Studies included after full-text review (PRISMA 2020). "
                "Total included: **%d** (quantitative synthesis: %d; "
                "narrative synthesis: %d).\n\n"
                % (len(out), counts.get("quantitative", 0), counts.get("narrative", 0)))
        f.write("| # | Study (title, year) | Data source / registry | "
                "Racial/ethnic groups (vs NHW) | Outcome measure | Synthesis | "
                "PMID | DOI |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for i, x in enumerate(out, 1):
            f.write("| %d | %s | %s | %s | %s | %s | %s | %s |\n" % (
                i, x["citation"].replace("|", "/"), x["data_source"].replace("|", "/"),
                x["groups_vs_nhw"].replace("|", "/"), x["outcome_measure"].replace("|", "/"),
                x["synthesis"], x["pmid"], x["doi"]))

    print("included studies: %d (quant %d, narrative %d)"
          % (len(out), counts.get("quantitative", 0), counts.get("narrative", 0)))
    print("wrote %s and %s" % (os.path.basename(OUT_CSV), os.path.basename(OUT_MD)))


if __name__ == "__main__":
    main()
