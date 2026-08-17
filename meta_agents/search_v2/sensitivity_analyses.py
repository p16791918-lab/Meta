#!/usr/bin/env python3
"""Sensitivity analyses requested (Feedback 6):
  #1  Good-RoB-only : drop studies rated Poor on the Newcastle-Ottawa adaptation.
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


def run(rows, keep, label):
    clusters = defaultdict(list)
    for r in rows:
        clusters[r["_cluster"]].append(r)
    out = []
    for cl, members in clusters.items():
        main_rep = best(members)
        if not main_rep:
            continue
        filt = [r for r in members if keep(r)]
        sens_rep = best(filt)
        dim, grp, fclass = cl.split("|")
        if sens_rep is None:
            status, sirr, srec = "dropped", "", ""
        elif sens_rep["record_id"] == main_rep["record_id"]:
            status = "unchanged"
            sirr, srec = sens_rep["irr"], sens_rep["record_id"]
        else:
            status = "changed"
            sirr, srec = sens_rep["irr"], sens_rep["record_id"]
        out.append(dict(dimension=dim, group=grp, family=fclass,
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
    qual = {r["record_id"]: r["Overall_quality"]
            for r in csv.DictReader(open(ROB, encoding="utf-8"))}
    rows = load(qual)
    print("cells assessed:", len(set(r["_cluster"] for r in rows)))

    c2 = write(run(rows, lambda r: r["provenance"] in DIRECT, "SENS2"),
               "Sensitivity2_directly_reported",
               "Sensitivity #2 — directly-reported IRR/SIR only (computed estimates dropped)")
    print("\n#2 directly-reported-only:", dict(c2))

    c1 = write(run(rows, lambda r: r["_qual"] == "Good", "SENS1"),
               "Sensitivity1_good_rob",
               "Sensitivity #1 — Good-RoB studies only (Poor dropped)")
    print("#1 Good-RoB-only     :", dict(c1))

    c3 = write(run(rows, lambda r: r.get("comparison_vs", "").strip() in NHW_OK, "SENS3"),
               "Sensitivity3_nhw_only",
               "Sensitivity #3 — non-Hispanic White comparator only (unstratified-White comparators dropped)")
    print("#3 NHW-comparator    :", dict(c3))


if __name__ == "__main__":
    main()
