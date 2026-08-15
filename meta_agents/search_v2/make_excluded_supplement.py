#!/usr/bin/env python3
"""Compile the PRISMA supplementary table of studies EXCLUDED at full-text review,
with reasons (PRISMA 2020 item 16b). Re-runnable — regenerates from current state
as the eligibility assessment progresses.

Sources:
  ft_eligibility.csv  -> rows with ft_decision == 'exclude' (reason + detail)
  ft_unavailable.csv  -> records that could not be obtained = 'Full text unavailable'

Outputs:
  TableS_excluded_fulltext.csv  (machine-readable)
  TableS_excluded_fulltext.md   (manuscript-ready supplementary table)

Each row: record_id, citation (title, year), pmid, doi, exclusion_reason, detail.
Full-text exclusion reason set (locked):
  Did not report the outcome of interest / Ineligible population /
  Overlapping or duplicate dataset / Full text unavailable
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MERGED = os.path.join(HERE, "merged_unique.csv")
ELIG = os.path.join(HERE, "ft_eligibility.csv")
UNAVAIL = os.path.join(HERE, "ft_unavailable.csv")
OUT_CSV = os.path.join(HERE, "TableS_excluded_fulltext.csv")
OUT_MD = os.path.join(HERE, "TableS_excluded_fulltext.md")

REASON_ORDER = [
    "Did not report the outcome of interest",
    "Ineligible population",
    "Overlapping or duplicate dataset",
    "Full text unavailable",
]


def main():
    recs = list(csv.DictReader(open(MERGED, encoding="utf-8")))
    rows = {}  # record_id -> dict

    # Records reclassified to INCLUDE in the eligibility log must never appear as
    # exclusions, even if they were once on the unobtainable list (e.g. 402, later
    # kept as a narrative include). Guards the excluded count against PRISMA drift.
    included = set()

    # 1) explicit full-text exclusions from the eligibility log
    if os.path.exists(ELIG):
        for r in csv.DictReader(open(ELIG, encoding="utf-8")):
            dec = r.get("ft_decision", "").strip()
            rid = int(r["record_id"])
            if dec == "exclude":
                rows[rid] = {"reason": r.get("ft_reason", "").strip(),
                             "detail": r.get("note", "").strip()}
            elif dec.startswith("include"):
                included.add(rid)

    # 2) unobtainable records = Full text unavailable (don't override an explicit
    #    reason, and skip anything now kept as an include)
    if os.path.exists(UNAVAIL):
        for r in csv.DictReader(open(UNAVAIL, encoding="utf-8")):
            rid = int(r["record_id"])
            if rid not in rows and rid not in included:
                rows[rid] = {"reason": "Full text unavailable",
                             "detail": r.get("note", "").strip()}

    out = []
    for rid, info in rows.items():
        rec = recs[rid] if 0 <= rid < len(recs) else {}
        out.append({
            "record_id": rid,
            "citation": "%s (%s)" % (rec.get("title", ""), rec.get("year", "")),
            "pmid": rec.get("pmid", ""),
            "doi": rec.get("doi", ""),
            "exclusion_reason": info["reason"],
            "detail": info["detail"],
        })
    # sort by reason order, then record_id
    out.sort(key=lambda x: (REASON_ORDER.index(x["exclusion_reason"])
                            if x["exclusion_reason"] in REASON_ORDER else 99,
                            x["record_id"]))

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["record_id", "citation", "pmid", "doi",
                                          "exclusion_reason", "detail"])
        w.writeheader()
        w.writerows(out)

    from collections import Counter
    counts = Counter(x["exclusion_reason"] for x in out)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# Table S. Studies excluded at full-text review, with reasons\n\n")
        f.write("Full-text reports assessed and excluded (PRISMA 2020, item 16b). "
                "Total excluded at full text: **%d**.\n\n" % len(out))
        f.write("| Reason | n |\n|---|---|\n")
        for reason in REASON_ORDER:
            if counts.get(reason):
                f.write("| %s | %d |\n" % (reason, counts[reason]))
        f.write("\n")
        f.write("| # | Study (title, year) | PMID | DOI | Exclusion reason | Detail |\n")
        f.write("|---|---|---|---|---|---|\n")
        for i, x in enumerate(out, 1):
            f.write("| %d | %s | %s | %s | %s | %s |\n" % (
                i, x["citation"].replace("|", "/"), x["pmid"], x["doi"],
                x["exclusion_reason"], x["detail"].replace("|", "/")))

    print("excluded-at-full-text: %d" % len(out))
    for reason in REASON_ORDER:
        if counts.get(reason):
            print("  %3d  %s" % (counts[reason], reason))
    print("wrote %s and %s" % (os.path.basename(OUT_CSV), os.path.basename(OUT_MD)))


if __name__ == "__main__":
    main()
