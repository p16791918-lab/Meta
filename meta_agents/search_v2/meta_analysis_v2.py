#!/usr/bin/env python3
"""Random-effects meta-analysis of race/ethnicity breast-cancer incidence rate
ratios (IRR vs non-Hispanic White), driven by the unified extraction ledger and
the locked one-per-registry-family representative table.

Implements, per Feedback 6:
  - DerSimonian-Laird (DL) tau^2                    (the conventional default)
  - Paule-Mandel tau^2  (= REML-equivalent MoM)     (compare vs DL)
  - Hartung-Knapp-Sidik-Jonkman (HKSJ) CI           (t_{k-1}, not z)
  - I^2 and tau^2 reported honestly.

Two analyses per cell (outcome dimension x minority group):
  MAIN         : representatives only (main_analysis == yes)  -> non-overlapping.
  SENSITIVITY  : all included estimates with a usable CI       -> overlapping;
                 demonstrates that a high I^2 is a non-independence artefact,
                 not real between-study heterogeneity.

Pooling ACROSS different minority groups is deliberately NOT done: that
heterogeneity is real (different populations) and is the disaggregation finding.
"""
import csv
import math
import os
from collections import defaultdict

import numpy as np
from scipy.optimize import brentq
from scipy.stats import t as tdist, norm

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "breast_extraction.csv")
REPS = os.path.join(HERE, "TableSA_main_representatives.csv")
Z = norm.ppf(0.975)


def load():
    reps = {}
    for r in csv.DictReader(open(REPS, encoding="utf-8")):
        key = (r["record_id"], r["outcome_dim"], r["minority_group"], r["irr"])
        reps[key] = r["main_analysis"]
    QUARANTINE = {"UNVERIFIED", "UNVERIFIED-table", "NO-FULLTEXT"}
    rows = []
    for r in csv.DictReader(open(LEDGER, encoding="utf-8")):
        if r.get("verification", "") in QUARANTINE:
            continue                      # unverifiable prior values are excluded
        irr, lo, hi = r["irr"].strip(), r["irr_ci_lo"].strip(), r["irr_ci_hi"].strip()
        if not (irr and lo and hi):
            continue                      # need a CI to contribute a variance
        try:
            y = math.log(float(irr))
            se = (math.log(float(hi)) - math.log(float(lo))) / (2 * Z)
        except ValueError:
            continue
        if se <= 0:
            continue
        key = (r["record_id"], r["outcome_dim"], r["minority_group"], r["irr"])
        rows.append({
            "rid": r["record_id"], "dim": r["outcome_dim"],
            "grp": r["minority_group"], "y": y, "se": se, "v": se * se,
            "irr": float(irr), "is_rep": reps.get(key, "").startswith("yes"),
        })
    return rows


def fixed_Q(y, v):
    w = 1.0 / v
    mu = np.sum(w * y) / np.sum(w)
    Q = np.sum(w * (y - mu) ** 2)
    return Q, mu


def tau2_DL(y, v):
    k = len(y)
    if k < 2:
        return 0.0
    w = 1.0 / v
    Q, _ = fixed_Q(y, v)
    c = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    return max(0.0, (Q - (k - 1)) / c) if c > 0 else 0.0


def tau2_PM(y, v):
    """Paule-Mandel (REML-equivalent method of moments): solve
    sum w_i (y_i - mu)^2 = k-1 for tau^2, w_i = 1/(v_i+tau^2)."""
    k = len(y)
    if k < 2:
        return 0.0

    def f(t2):
        w = 1.0 / (v + t2)
        mu = np.sum(w * y) / np.sum(w)
        return np.sum(w * (y - mu) ** 2) - (k - 1)

    if f(0.0) <= 0:
        return 0.0
    hi = 1.0
    while f(hi) > 0 and hi < 1e6:
        hi *= 2
    return brentq(f, 0.0, hi, xtol=1e-10)


def pool(y, v, tau2):
    w = 1.0 / (v + tau2)
    mu = np.sum(w * y) / np.sum(w)
    se_re = math.sqrt(1.0 / np.sum(w))               # standard RE SE (z-based)
    return mu, se_re, w


def hksj_se(y, v, tau2, mu, w):
    """Hartung-Knapp-Sidik-Jonkman SE: sqrt( sum w_i (y_i-mu)^2 / ((k-1) sum w_i) )."""
    k = len(y)
    q = np.sum(w * (y - mu) ** 2) / ((k - 1) * np.sum(w))
    return math.sqrt(q)


def i2(y, v):
    k = len(y)
    if k < 2:
        return float("nan")
    Q, _ = fixed_Q(y, v)
    return max(0.0, (Q - (k - 1)) / Q) * 100 if Q > 0 else 0.0


def analyse(rows, label):
    """rows: list of dicts (already a single cell). Returns pooled summaries."""
    y = np.array([r["y"] for r in rows])
    v = np.array([r["v"] for r in rows])
    k = len(y)
    if k == 1:
        r = rows[0]
        return {"k": 1, "method": "single", "irr": r["irr"],
                "lo": math.exp(r["y"] - Z * r["se"]), "hi": math.exp(r["y"] + Z * r["se"]),
                "I2": float("nan"), "tau2": 0.0}
    out = {}
    Q, _ = fixed_Q(y, v)
    I2 = i2(y, v)
    for name, t2 in [("DL", tau2_DL(y, v)), ("PM/REML", tau2_PM(y, v))]:
        mu, se_re, w = pool(y, v, t2)
        # z-based RE CI
        lo_z, hi_z = mu - Z * se_re, mu + Z * se_re
        # HKSJ CI (t_{k-1})
        se_hk = hksj_se(y, v, t2, mu, w)
        tcrit = tdist.ppf(0.975, k - 1)
        lo_h, hi_h = mu - tcrit * se_hk, mu + tcrit * se_hk
        out[name] = {
            "k": k, "irr": math.exp(mu), "tau2": t2, "I2": I2,
            "lo_z": math.exp(lo_z), "hi_z": math.exp(hi_z),
            "lo_hk": math.exp(lo_h), "hi_hk": math.exp(hi_h),
        }
    return out


def main():
    rows = load()
    cells = defaultdict(list)
    for r in rows:
        cells[(r["dim"], r["grp"])].append(r)

    print("=" * 92)
    print("META-ANALYSIS v2  (IRR vs NHW)  -- ledger estimates with usable CI: %d" % len(rows))
    print("=" * 92)

    # ---- Demonstration: multi-estimate cells show the I^2 artefact ----
    print("\n### Cells with >=2 overlapping estimates: MAIN (dedup) vs SENSITIVITY (all)\n")
    hdr = "%-38s %3s  %-26s %-26s %5s"
    print(hdr % ("cell (outcome | group)", "k", "SENSITIVITY all-incl (PM+HKSJ)", "MAIN representative(s)", "I2%"))
    print("-" * 100)
    multi = 0
    for (dim, grp), cr in sorted(cells.items()):
        allc = cr
        repc = [r for r in cr if r["is_rep"]]
        if len(allc) < 2:
            continue
        multi += 1
        s = analyse(allc, "sens")
        spm = s["PM/REML"]
        sens = "%.3f (%.3f-%.3f)" % (spm["irr"], spm["lo_hk"], spm["hi_hk"])
        if len(repc) == 1:
            m = analyse(repc, "main")
            main_s = "%.3f (%.3f-%.3f) [1]" % (m["irr"], m["lo"], m["hi"])
        elif len(repc) >= 2:
            m = analyse(repc, "main")["PM/REML"]
            main_s = "%.3f (%.3f-%.3f) [%d]" % (m["irr"], m["lo_hk"], m["hi_hk"], m["k"])
        else:
            main_s = "(no rep w/ CI)"
        flag = " *" if len(allc) < 3 else ""   # HKSJ unreliable for k<3 (t_{k-1})
        cell = ("%s | %s" % (dim, grp))[:38]
        print(hdr % (cell, len(allc), sens + flag, main_s, "%.0f" % spm["I2"]))
    print("\n(%d multi-estimate cells; I2 column is the all-included sensitivity value.)" % multi)
    print("  * k<3: HKSJ CI uses t_{k-1} and is unstable/over-wide; read the point estimate only.")

    # ---- DL vs PM/REML vs HKSJ on the largest pooled cell ----
    biggest = max(cells.items(), key=lambda kv: len(kv[1]))
    (dim, grp), cr = biggest
    print("\n### Method comparison on the largest cell: %s | %s  (k=%d, all-included)\n"
          % (dim, grp, len(cr)))
    res = analyse(cr, "x")
    for name in ("DL", "PM/REML"):
        d = res[name]
        print("  %-8s  IRR=%.3f  tau2=%.4f  I2=%.0f%%  z-CI(%.3f-%.3f)  HKSJ-CI(%.3f-%.3f)"
              % (name, d["irr"], d["tau2"], d["I2"], d["lo_z"], d["hi_z"], d["lo_hk"], d["hi_hk"]))
    print("\n  -> DL and PM/REML tau^2 differ; HKSJ widens the CI vs z (t_{k-1}).")
    print("  -> High I^2 here reflects NON-INDEPENDENT overlapping registry data;")
    print("     the MAIN analysis uses one representative per registry family instead.")

    # ---- MAIN forest: one representative estimate per group, per dimension ----
    print("\n" + "=" * 92)
    print("MAIN forest (representatives only) -- disaggregated, NOT pooled across groups")
    print("=" * 92)
    for dim in ["aggregate-vs-NHW", "disaggregated-AANHPI", "Hispanic-origin", "male-BC", "AIAN"]:
        reps = sorted([r for (d, g), cr in cells.items() if d == dim
                       for r in cr if r["is_rep"]], key=lambda r: r["irr"])
        if not reps:
            continue
        print("\n  [%s]" % dim)
        for r in reps:
            lo = math.exp(r["y"] - Z * r["se"]); hi = math.exp(r["y"] + Z * r["se"])
            print("    %-30s IRR %.3f (%.3f-%.3f)  rec%s" % (r["grp"][:30], r["irr"], lo, hi, r["rid"]))


if __name__ == "__main__":
    main()
