#!/usr/bin/env python3
"""Persist meta-analysis result tables to outputs/ for the manuscript:
  Table_main_forest.(csv/md)      - representative IRR per group per dimension.
  Table_sensitivity_I2.(csv/md)   - all-included (SENSITIVITY, PM+HKSJ) vs MAIN
                                    representative, with I^2, for multi-estimate cells.
  Table_method_comparison.md      - DL vs PM/REML vs HKSJ on the largest cell.
Reuses the computational functions in meta_analysis_v2.py.
"""
import csv
import math
import os
from collections import defaultdict

import meta_analysis_v2 as M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
os.makedirs(OUT, exist_ok=True)
Z = M.Z

DIM_ORDER = ["aggregate-vs-NHW", "disaggregated-AANHPI", "disaggregated-MENA",
             "Hispanic-origin", "AIAN", "male-BC",
             "subtype-TNBC", "subtype-HRneg-HER2pos", "subtype-HRpos-HER2neg",
             "subtype-HRpos-HER2pos"]


def main():
    from guard_v2_only import check_ledger
    if check_ledger():
        raise SystemExit("CONTAMINATION in ledger")
    rows = M.load()
    cells = defaultdict(list)
    for r in rows:
        cells[(r["dim"], r["grp"])].append(r)

    # ---- MAIN forest ----
    frows = []
    for (dim, grp), cr in cells.items():
        for r in cr:
            if not r["is_rep"]:
                continue
            lo = math.exp(r["y"] - Z * r["se"])
            hi = math.exp(r["y"] + Z * r["se"])
            frows.append(dict(dimension=dim, group=grp, irr=round(r["irr"], 3),
                              ci_lo=round(lo, 3), ci_hi=round(hi, 3), record=r["rid"]))
    dim_rank = {d: i for i, d in enumerate(DIM_ORDER)}
    frows.sort(key=lambda x: (dim_rank.get(x["dimension"], 99), x["irr"]))
    with open(os.path.join(OUT, "Table_main_forest.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["dimension", "group", "irr", "ci_lo", "ci_hi", "record"])
        w.writeheader(); w.writerows(frows)
    with open(os.path.join(OUT, "Table_main_forest.md"), "w", encoding="utf-8") as f:
        f.write("# Table. Main analysis — representative IRR vs non-Hispanic White\n\n")
        f.write("One estimate per registry family; not pooled across groups.\n\n")
        cur = None
        for r in frows:
            if r["dimension"] != cur:
                cur = r["dimension"]
                f.write("\n**%s**\n\n| Group | IRR | 95%% CI | rec |\n|----|----|----|----|\n" % cur)
            f.write("| %s | %.3f | %.3f-%.3f | %s |\n" % (
                r["group"], r["irr"], r["ci_lo"], r["ci_hi"], r["record"]))

    # ---- SENSITIVITY vs MAIN with I^2 ----
    srows = []
    for (dim, grp), cr in sorted(cells.items()):
        if len(cr) < 2:
            continue
        s = M.analyse(cr, "s")["PM/REML"]
        repc = [r for r in cr if r["is_rep"]]
        if len(repc) == 1:
            m = M.analyse(repc, "m")
            main_irr, mlo, mhi, mk = m["irr"], m["lo"], m["hi"], 1
        elif len(repc) >= 2:
            m = M.analyse(repc, "m")["PM/REML"]
            main_irr, mlo, mhi, mk = m["irr"], m["lo_hk"], m["hi_hk"], m["k"]
        else:
            main_irr = mlo = mhi = None; mk = 0
        srows.append(dict(dimension=dim, group=grp, k_all=len(cr),
                          sens_irr=round(s["irr"], 3), sens_lo=round(s["lo_hk"], 3),
                          sens_hi=round(s["hi_hk"], 3), I2=round(s["I2"]),
                          tau2=round(s["tau2"], 4),
                          main_irr=round(main_irr, 3) if main_irr else "",
                          main_lo=round(mlo, 3) if main_irr else "",
                          main_hi=round(mhi, 3) if main_irr else "", main_k=mk,
                          hksj_unstable="yes" if len(cr) < 3 else "no"))
    with open(os.path.join(OUT, "Table_sensitivity_I2.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(srows[0].keys()))
        w.writeheader(); w.writerows(srows)
    with open(os.path.join(OUT, "Table_sensitivity_I2.md"), "w", encoding="utf-8") as f:
        f.write("# Table. Between-study heterogeneity: all-included (sensitivity) "
                "vs one-per-family (main)\n\n")
        f.write("Sensitivity = all overlapping estimates pooled (Paule-Mandel tau2 + "
                "HKSJ CI); high I2 reflects non-independent overlapping registry data. "
                "Main = single representative per registry family.\n\n")
        f.write("| Dimension | Group | k | Sensitivity IRR (95%% CI) | I2%% | Main IRR (95%% CI) | HKSJ unstable (k<3) |\n")
        f.write("|----|----|----|----|----|----|----|\n")
        for r in srows:
            mtxt = ("%.3f (%.3f-%.3f)" % (r["main_irr"], r["main_lo"], r["main_hi"])
                    if r["main_irr"] != "" else "-")
            f.write("| %s | %s | %d | %.3f (%.3f-%.3f) | %d | %s | %s |\n" % (
                r["dimension"], r["group"], r["k_all"], r["sens_irr"], r["sens_lo"],
                r["sens_hi"], r["I2"], mtxt, r["hksj_unstable"]))

    # ---- method comparison on largest cell ----
    biggest = max(cells.items(), key=lambda kv: len(kv[1]))
    (dim, grp), cr = biggest
    res = M.analyse(cr, "x")
    with open(os.path.join(OUT, "Table_method_comparison.md"), "w", encoding="utf-8") as f:
        f.write("# Table. Estimator comparison on the largest overlapping cell: "
                "%s | %s (k=%d, all-included)\n\n" % (dim, grp, len(cr)))
        f.write("| Estimator | IRR | tau2 | I2%% | z-based 95%% CI | HKSJ 95%% CI |\n")
        f.write("|----|----|----|----|----|----|\n")
        for name in ("DL", "PM/REML"):
            d = res[name]
            f.write("| %s | %.3f | %.4f | %.0f | %.3f-%.3f | %.3f-%.3f |\n" % (
                name, d["irr"], d["tau2"], d["I2"], d["lo_z"], d["hi_z"],
                d["lo_hk"], d["hi_hk"]))
        f.write("\nDL and Paule-Mandel/REML tau2 differ; HKSJ widens the CI relative "
                "to the z-based interval. The high I2 is attributable to pooling "
                "non-independent overlapping registry estimates, not to real "
                "biological heterogeneity; the main analysis avoids it by using one "
                "representative per registry family.\n")
    # ---- per-cell estimator comparison (DL vs PM/REML vs HKSJ) ----
    ec = []
    for (dim, grp), cr in cells.items():
        if len(cr) < 2:
            continue
        res = M.analyse(cr, "x")
        dl, pm = res["DL"], res["PM/REML"]
        ec.append(dict(dimension=dim, group=grp, k=len(cr),
                       dl_irr="%.3f" % dl["irr"], dl_ci="%.3f-%.3f" % (dl["lo_z"], dl["hi_z"]),
                       dl_tau2="%.4f" % dl["tau2"], pm_irr="%.3f" % pm["irr"],
                       pm_ci="%.3f-%.3f" % (pm["lo_z"], pm["hi_z"]), pm_tau2="%.4f" % pm["tau2"],
                       hksj_ci="%.3f-%.3f" % (pm["lo_hk"], pm["hi_hk"]), i2="%.0f" % pm["I2"],
                       klt3=("*" if len(cr) < 3 else "")))
    ec.sort(key=lambda x: (x["klt3"] != "", x["dimension"], x["group"]))
    with open(os.path.join(OUT, "Table_estimator_comparison.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(ec[0].keys()))
        w.writeheader(); w.writerows(ec)

    print("wrote outputs/Table_main_forest, Table_sensitivity_I2, Table_method_comparison, Table_estimator_comparison")
    print("main-forest rows:", len(frows), "| multi-estimate cells:", len(srows))


if __name__ == "__main__":
    main()
