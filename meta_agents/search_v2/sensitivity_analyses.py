#!/usr/bin/env python3
"""Sensitivity analyses requested (Feedback 6):
  #1  Low-RoB-only : keep only studies rated low risk of bias (JBI).
  #2  Directly-reported-only : keep only estimates the source printed as a ratio
      (provenance directly-reported-IRR / -SIR); drop everything we computed.

For every main-analysis cell (outcome_dim x group x registry-family), re-select
the best representative from the filtered rows using the SAME selection rule as
finalize_representatives, and report whether the cell's representative IRR is
unchanged, changed (to a different study), or dropped (no eligible estimate).
"""
import csv
import os
from collections import defaultdict

from finalize_representatives import registry_family, PROV_RANK, period_key, registry_family as _rf

HERE = os.path.dirname(os.path.abspath(__file__))
LED = os.path.join(HERE, "breast_extraction.csv")
ROB = os.path.join(HERE, "outputs", "TableS_risk_of_bias.csv")
OUT = os.path.join(HERE, "outputs")
QUAR = {"UNVERIFIED", "UNVERIFIED-table", "NO-FULLTEXT"}
DIRECT = {"directly-reported-IRR", "directly-reported-SIR"}
# reference groups that are (or are equivalent to) non-Hispanic White
NHW_OK = {"NHW", "White (NH)", "NHW (external SEER-Explorer)"}


def load(qual):
    rows = []
    for r in csv.DictReader(open(LED, encoding="utf-8")):
        if r.get("verification") in QUAR or r["record_id"] == "SEER-EXPL":
            continue
        if "young" in r.get("minority_group", "").lower():
            continue  # match the main analysis, which excludes age-restricted "young" subgroups
        fam, tier, fclass = registry_family(r["registry"])
        r["_tier"] = tier
        r["_cluster"] = "%s|%s|%s" % (r["outcome_dim"], r["minority_group"], fclass)
        r["_qual"] = qual.get(r["record_id"], "NA")
        rows.append(r)
    return rows


def score(r):
    has_irr = 1 if (r.get("irr") or "").strip() else 0
    return (has_irr, r["_tier"], period_key(r["period"]), PROV_RANK.get(r["provenance"], 0))


def best(rows):
    rows = [r for r in rows if (r.get("irr") or "").strip()]
    return max(rows, key=score) if rows else None


def run(rows, keep, mainrep, label):
    # cluster ledger estimates by (dimension, group), matching the main-analysis
    # cells; the baseline representative is the one finalize_representatives chose
    # (mainrep), so the sensitivity assesses exactly the displayed main cells.
    clusters = defaultdict(list)
    for r in rows:
        clusters[(r["outcome_dim"], r["minority_group"])].append(r)
    out = []
    for (dim, grp), rec in mainrep.items():
        members = clusters.get((dim, grp), [])
        base = [r for r in members if r["record_id"] == rec]
        main_rep = base[0] if base else best(members)
        if not main_rep or not (main_rep.get("irr") or "").strip():
            continue
        filt = [r for r in members if keep(r)]
        sens_rep = best(filt)
        if sens_rep is None:
            status, sirr, srec = "dropped", "", ""
        elif sens_rep["record_id"] == main_rep["record_id"]:
            status = "unchanged"
            sirr, srec = sens_rep["irr"], sens_rep["record_id"]
        else:
            status = "changed"
            sirr, srec = sens_rep["irr"], sens_rep["record_id"]
        out.append(dict(dimension=dim, group=grp, family="",
                        main_irr=main_rep["irr"], main_rec=main_rep["record_id"],
                        sens_irr=sirr, sens_rec=srec, status=status,
                        n_all=len(members), n_kept=len(filt)))
    order = {"changed": 0, "dropped": 1, "unchanged": 2}
    out.sort(key=lambda x: (order[x["status"]], x["dimension"], x["group"]))
    return out


def write(out, name, title):
    cols = ["dimension", "group", "family", "main_irr", "main_rec",
            "sens_irr", "sens_rec", "status", "n_all", "n_kept"]
    with open(os.path.join(OUT, name + ".csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
    from collections import Counter
    c = Counter(r["status"] for r in out)
    with open(os.path.join(OUT, name + ".md"), "w", encoding="utf-8") as f:
        f.write("# %s\n\n" % title)
        f.write("Cells: %d total — unchanged %d, changed %d, dropped %d.\n\n"
                % (len(out), c["unchanged"], c["changed"], c["dropped"]))
        f.write("Only cells where the representative CHANGED or DROPPED are shown "
                "in full below; all others are unchanged.\n\n")
        f.write("| Dimension | Group | Main IRR (rec) | Sensitivity IRR (rec) | Status |\n")
        f.write("|----|----|----|----|----|\n")
        for r in out:
            if r["status"] == "unchanged":
                continue
            f.write("| %s | %s | %s (%s) | %s (%s) | **%s** |\n" % (
                r["dimension"], r["group"], r["main_irr"], r["main_rec"],
                r["sens_irr"] or "-", r["sens_rec"] or "-", r["status"]))
    return c


def main():
    qual = {r["record_id"]: r["Overall_RoB"]
            for r in csv.DictReader(open(ROB, encoding="utf-8"))}
    rows = load(qual)
    # baseline main-analysis representatives, exactly as finalize_representatives chose
    # them (one per displayed cell): (dimension, group) -> record_id
    REPS = os.path.join(HERE, "TableSA_main_representatives.csv")
    mainrep = {(r["outcome_dim"], r["minority_group"]): r["record_id"]
               for r in csv.DictReader(open(REPS, encoding="utf-8"))
               if r["main_analysis"].startswith("yes")}
    print("main-analysis cells:", len(mainrep))

    c2 = write(run(rows, lambda r: r["provenance"] in DIRECT, mainrep, "SENS2"),
               "Sensitivity2_directly_reported",
               "Sensitivity #2 — directly-reported IRR/SIR only (computed estimates dropped)")
    print("\n#2 directly-reported-only:", dict(c2))

    c1 = write(run(rows, lambda r: r["_qual"] == "Low", mainrep, "SENS1"),
               "Sensitivity1_good_rob",
               "Sensitivity #1 — low-risk-of-bias studies only (Moderate/High dropped)")
    print("#1 low-RoB-only      :", dict(c1))

    c3 = write(run(rows, lambda r: r.get("comparison_vs", "").strip() in NHW_OK, mainrep, "SENS3"),
               "Sensitivity3_nhw_only",
               "Sensitivity #3 — non-Hispanic White comparator only (unstratified-White comparators dropped)")
    print("#3 NHW-comparator    :", dict(c3))


if __name__ == "__main__":
    main()
