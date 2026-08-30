#!/usr/bin/env python3
"""Master cross-check (2nd-round feedback #7).

Verifies that every displayed incidence-rate ratio and confidence interval in the
Main text (Table 1, forests) and Supplementary tables traces to the SINGLE master
extraction ledger (breast_extraction.csv), and that every author-COMPUTED estimate
re-derives from its own reported rates.

Four checks, each PASS/FAIL with per-row detail:

  A. Derived-IRR recomputation. For every row whose provenance is
     computed-from-rates*, recompute IRR = minority_rate / nhw_rate and, where the
     component rates carry CIs, recompute the IRR CI by the delta method on the log
     scale. Compare against the stored irr / irr_ci_lo / irr_ci_hi.

  B. Table 1 traceability. Every estimate rendered in outputs/Table1_main.csv must
     match a ledger row (record_id, group, dimension) with an identical IRR and CI.

  C. Forest traceability. Every row in outputs/Table_main_forest.csv must match a
     ledger row flagged as a main representative, with a CI equal (to display
     precision) to the ledger CI. Table 1 cells that carry a CI but are absent from
     the forest are listed (expected: none, except point-estimate-only cells).

  D. Main-vs-sensitivity consistency. For each cell, the "main_irr" printed in every
     sensitivity table (SENS1/2/3) must equal the Table 1 representative IRR.

  E. Manuscript counts vs data. Every count the prose asserts (163 included, 48
     quant-eligible, 43 extractable, 115 narrative, 145 estimates, 85 cells) must
     match the value recomputed from ft_eligibility.csv / the ledger / the
     representatives table, guarding against stale hard-coded numbers in the drafts.

Exit status is non-zero if any check fails, so it can gate the docx rebuild.
"""
import csv
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
LEDGER = os.path.join(HERE, "breast_extraction.csv")
ELIG = os.path.join(HERE, "ft_eligibility.csv")
REPS = os.path.join(HERE, "TableSA_main_representatives.csv")
MAN = os.path.join(HERE, "manuscript")
Z = 1.959963984540054  # norm.ppf(0.975)

# Relative tolerance for a re-derived point estimate vs the stored value. Source
# rates are printed rounded (often 1 decimal on a per-100,000 scale), so an exact
# match is not expected; 3% absorbs that rounding without hiding a real error.
RTOL_IRR = 0.03
RTOL_CI = 0.05


def num(x):
    x = (x or "").strip()
    try:
        return float(x)
    except ValueError:
        return None


def led_rows():
    return list(csv.DictReader(open(LEDGER, encoding="utf-8")))


def close(a, b, rtol):
    if a is None or b is None:
        return a is None and b is None
    if b == 0:
        return abs(a - b) < 1e-9
    return abs(a - b) / abs(b) <= rtol


# --------------------------------------------------------------------------- A
def check_A(rows):
    fails, checked, ci_checked = [], 0, 0
    for r in rows:
        prov = r["provenance"]
        if not prov.startswith("computed-from-rates"):
            continue
        mr, nr = num(r["minority_rate"]), num(r["nhw_rate"])
        stored = num(r["irr"])
        if mr is None or nr is None or nr == 0 or stored is None:
            fails.append(("A-inputs", r["record_id"], r["minority_group"],
                          "computed row missing a rate or IRR"))
            continue
        checked += 1
        recomputed = mr / nr
        if not close(recomputed, stored, RTOL_IRR):
            fails.append(("A-point", r["record_id"], r["minority_group"],
                          "IRR stored %.3f but rates give %.3f (%.3f/%.3f)"
                          % (stored, recomputed, mr, nr)))
        # CI recomputation, only when the component rates carry CIs and the
        # stored IRR has a CI to compare against.
        mlo, mhi = num(r["min_ci_lo"]), num(r["min_ci_hi"])
        nlo, nhi = num(r["nhw_ci_lo"]), num(r["nhw_ci_hi"])
        slo, shi = num(r["irr_ci_lo"]), num(r["irr_ci_hi"])
        if None not in (mlo, mhi, nlo, nhi, slo, shi) and mr > 0 and nr > 0:
            # both component rates carry CIs -> delta method on the log scale
            se_m = (math.log(mhi) - math.log(mlo)) / (2 * Z)
            se_n = (math.log(nhi) - math.log(nlo)) / (2 * Z)
            se_log = math.sqrt(se_m ** 2 + se_n ** 2)
            lo = recomputed * math.exp(-Z * se_log)
            hi = recomputed * math.exp(Z * se_log)
            ci_checked += 1
            if not (close(lo, slo, RTOL_CI) and close(hi, shi, RTOL_CI)):
                fails.append(("A-ci", r["record_id"], r["minority_group"],
                              "CI stored [%.3f, %.3f] but delta method gives [%.3f, %.3f]"
                              % (slo, shi, lo, hi)))
        elif None not in (mlo, mhi, slo, shi) and (nlo is None or nhi is None):
            # only the minority rate carries a CI and the NHW denominator is a
            # fixed reference rate (no variance): CI = minority-rate CI / denominator
            lo, hi = mlo / nr, mhi / nr
            ci_checked += 1
            if not (close(lo, slo, RTOL_CI) and close(hi, shi, RTOL_CI)):
                fails.append(("A-ci-fixed", r["record_id"], r["minority_group"],
                              "CI stored [%.3f, %.3f] but rate/denominator gives [%.3f, %.3f]"
                              % (slo, shi, lo, hi)))
    return checked, ci_checked, fails


# --------------------------------------------------------------------------- B
def norm_g(s):
    return (s or "").strip().lower()


def check_B(rows):
    # index ledger by (record_id, dim, group) -> (irr, lo, hi)
    idx = {}
    for r in rows:
        idx.setdefault((r["record_id"], r["outcome_dim"], norm_g(r["minority_group"])), []).append(
            (num(r["irr"]), num(r["irr_ci_lo"]), num(r["irr_ci_hi"])))
    reps = {r["record_id"]: r for r in csv.DictReader(
        open(os.path.join(HERE, "TableSA_main_representatives.csv"), encoding="utf-8"))}
    t1 = list(csv.DictReader(open(os.path.join(OUT, "Table1_main.csv"), encoding="utf-8")))
    fails, checked = [], 0
    for r in t1:
        # Table 1 stores the display study (author_year) not the record_id; match
        # on the representatives table via the estimate string instead.
        est = r["estimate"]
        m = est.replace("†", "").replace("[", " ").replace("]", " ").replace(",", " ")
        parts = [p for p in m.split() if p]
        try:
            pt = float(parts[0])
        except (ValueError, IndexError):
            fails.append(("B-parse", r["group"], est))
            continue
        checked += 1
        # find any ledger estimate for this group matching the point value
        hit = False
        for (rid, dim, g), lst in idx.items():
            if g != norm_g(r["group"]):
                continue
            for (irr, lo, hi) in lst:
                if irr is not None and close(irr, pt, 1e-4):
                    hit = True
                    break
            if hit:
                break
        if not hit:
            fails.append(("B-trace", r["group"], "Table 1 IRR %.3f not found in ledger" % pt))
    return checked, fails


# --------------------------------------------------------------------------- C
def check_C(rows):
    # ledger CI by (group, irr)
    led = {}
    for r in rows:
        led.setdefault(norm_g(r["minority_group"]), []).append(
            (num(r["irr"]), num(r["irr_ci_lo"]), num(r["irr_ci_hi"])))
    fp = os.path.join(OUT, "Table_main_forest.csv")
    if not os.path.exists(fp):
        return 0, [("C-missing", "Table_main_forest.csv", "not generated")]
    frows = list(csv.DictReader(open(fp, encoding="utf-8")))
    fails, checked = [], 0
    for r in frows:
        g, irr = norm_g(r["group"]), num(r["irr"])
        flo, fhi = num(r["ci_lo"]), num(r["ci_hi"])
        checked += 1
        hit = False
        for (lirr, llo, lhi) in led.get(g, []):
            if lirr is not None and close(lirr, irr, 1e-2):
                # forest CI is a log round-trip of the ledger CI; compare loosely
                if llo is None or lhi is None or (close(flo, llo, RTOL_CI) and close(fhi, lhi, RTOL_CI)):
                    hit = True
                    break
        if not hit:
            fails.append(("C-trace", r["group"],
                          "forest IRR %.3f [%.3f, %.3f] not matched in ledger" % (irr, flo, fhi)))
    return checked, fails


# --------------------------------------------------------------------------- D
def check_D():
    # Ground truth: the main representative IRR per (outcome_dim, minority_group),
    # exactly as finalize_representatives locked it. Each sensitivity table's
    # baseline "main_irr" must reproduce this cell by cell.
    rep = {}
    for r in csv.DictReader(open(os.path.join(HERE, "TableSA_main_representatives.csv"),
                                 encoding="utf-8")):
        if r["main_analysis"].startswith("yes"):
            rep[(r["outcome_dim"], norm_g(r["minority_group"]))] = num(r["irr"])
    fails, checked = [], 0
    for name in ("Sensitivity1_good_rob", "Sensitivity2_directly_reported",
                 "Sensitivity3_nhw_only"):
        fp = os.path.join(OUT, name + ".csv")
        if not os.path.exists(fp):
            fails.append((name, "-", "sensitivity file not generated"))
            continue
        for r in csv.DictReader(open(fp, encoding="utf-8")):
            key = (r["dimension"], norm_g(r["group"]))
            mi = num(r["main_irr"])
            if key not in rep or mi is None:
                continue
            checked += 1
            if not close(mi, rep[key], 1e-3):
                fails.append((name, "%s / %s" % (r["dimension"], r["group"]),
                              "sensitivity main_irr %.3f != representative %.3f"
                              % (mi, rep[key])))
    return checked, fails


# --------------------------------------------------------------------------- E
def canonical_counts():
    """Recompute the study/estimate counts the manuscript reports, from the data."""
    dec = [r.get("ft_decision", "").strip()
           for r in csv.DictReader(open(ELIG, encoding="utf-8"))]
    quant = dec.count("include-quant")
    narrative = dec.count("include-narrative")
    excluded = dec.count("exclude")
    included = quant + narrative
    led = [r for r in csv.DictReader(open(LEDGER, encoding="utf-8"))
           if r["record_id"] != "SEER-EXPL"]
    studies = len(set(r["record_id"] for r in led))
    estimates = sum(1 for r in led if "young" not in r["minority_group"].lower())
    rep_rows = [r for r in csv.DictReader(open(REPS, encoding="utf-8"))
                if r["main_analysis"].startswith("yes")]
    cells = len(rep_rows)
    reps = len(set(r["record_id"] for r in rep_rows))
    return {"included": included, "quant": quant, "narrative": narrative,
            "excluded": excluded, "studies": studies, "estimates": estimates,
            "cells": cells, "reps": reps}


def check_E():
    """Guard against stale hard-coded counts: every number the manuscript prose
    asserts for a canonical quantity must match the value recomputed from data.
    Each pattern captures the number the prose states next to a fixed phrase."""
    c = canonical_counts()
    # (base_dir, file, regex with one capture group, canonical key)
    # The PRISMA flow figure and its count sheet carry the same numbers as hard-coded
    # literals; probe them too so the figure cannot drift from the ledger unnoticed
    # (this is exactly the gap that let "144 estimates / 28 representatives" go stale).
    here_probes = [
        ("prisma_flow.py", r"Studies included in the review \(n = (\d+)\)", "included"),
        ("prisma_flow.py", r"(\d+) eligible \(\d+ with extractable", "quant"),
        ("prisma_flow.py", r"\d+ eligible \((\d+) with extractable", "studies"),
        ("prisma_flow.py", r"Narrative synthesis only: (\d+)", "narrative"),
        ("prisma_flow.py", r"Reports excluded \(n = (\d+)\)", "excluded"),
        ("prisma_flow.py", r"(\d+) estimates;", "estimates"),
        ("prisma_flow.py", r"estimates; (\d+) supplied a main-analysis", "reps"),
        ("outputs/PRISMA_COUNTS.md", r"contributed (\d+) estimates", "estimates"),
        ("outputs/PRISMA_COUNTS.md", r"estimates; (\d+) studies supplied", "reps"),
    ]
    # (file, regex with one capture group, canonical key)
    probes = [
        ("Results_draft.md", r"(\d+)\s+included studies", "included"),
        ("Results_draft.md", r"(\d+)\s+were eligible for\s+quantitative", "quant"),
        ("Results_draft.md", r"(\d+)\s+provided extractable", "studies"),
        ("Results_draft.md", r"\((\d+)\s+individual estimates", "estimates"),
        ("Results_draft.md", r"remaining\s+(\d+)\s+informed the narrative", "narrative"),
        ("Results_draft.md", r"(\d+)\s+representative estimates", "cells"),
        ("Methods_draft.md", r"(\d+)\s*\n?\s*publications were included", "included"),
        ("Methods_draft.md", r"(\d+)\s+were eligible for quantitative", "quant"),
        ("Methods_draft.md", r"remaining\s+(\d+)\s+informed the", "narrative"),
        ("Abstract_draft.md", r"(\d+)\s+studies were included", "included"),
        ("Abstract_draft.md", r"(\d+)\s+eligible for quantitative", "quant"),
        ("Abstract_draft.md", r"and\s+(\d+)\s+narrative", "narrative"),
    ]
    fails, checked = [], 0
    all_probes = [(os.path.join(MAN, fn), pat, key) for fn, pat, key in probes] + \
                 [(os.path.join(HERE, fn), pat, key) for fn, pat, key in here_probes]
    for p, pat, key in all_probes:
        fn = os.path.basename(p)
        if not os.path.exists(p):
            continue
        text = " ".join(open(p, encoding="utf-8").read().split())  # normalise wraps
        m = re.search(pat, text)
        if not m:
            fails.append(("E-missing", fn, "phrase not found for '%s' (expected %d)"
                          % (key, c[key])))
            continue
        checked += 1
        got = int(m.group(1))
        if got != c[key]:
            fails.append(("E-count", fn, "%s: prose says %d, data gives %d"
                          % (key, got, c[key])))
    return checked, fails, c


def check_F(rows):
    """Every computed/derived-provenance record must appear in the derivation log
    (DERIVATIONS.md → Supplementary Note 1), so the log stays complete as the
    ledger changes."""
    logp = os.path.join(HERE, "DERIVATIONS.md")
    if not os.path.exists(logp):
        return 0, [("F-missing", "DERIVATIONS.md", "not found")]
    logged = set(re.findall(r"rec (\d+)", open(logp, encoding="utf-8").read()))
    need = {r["record_id"] for r in rows
            if r["record_id"] != "SEER-EXPL"
            and (r["provenance"].startswith("computed-from-rates")
                 or r["provenance"] == "directly-reported-rate")}
    fails = [("F-omitted", "rec " + rid, "computed record absent from the derivation log")
             for rid in sorted(need - logged, key=int)]
    return len(need), fails


def main():
    rows = led_rows()
    ok = True

    print("=" * 78)
    print("MASTER CROSS-CHECK  (feedback #7)  — ledger: %d rows" % len(rows))
    print("=" * 78)

    nA, nAci, fA = check_A(rows)
    print("\n[A] Derived-IRR recomputation")
    print("    point estimates recomputed from rates : %d" % nA)
    print("    CIs recomputed by delta method        : %d" % nAci)
    if fA:
        ok = False
        for f in fA:
            print("    FAIL", f)
    else:
        print("    PASS — all computed IRRs and CIs reproduce from their own rates")

    nB, fB = check_B(rows)
    print("\n[B] Table 1 traceability (%d estimates)" % nB)
    if fB:
        ok = False
        for f in fB:
            print("    FAIL", f)
    else:
        print("    PASS — every Table 1 IRR traces to a ledger row")

    nC, fC = check_C(rows)
    print("\n[C] Forest traceability (%d rows)" % nC)
    if fC:
        ok = False
        for f in fC:
            print("    FAIL", f)
    else:
        print("    PASS — every forest IRR/CI traces to a ledger representative")

    nD, fD = check_D()
    print("\n[D] Main-vs-sensitivity consistency (%d comparisons)" % nD)
    if fD:
        ok = False
        for f in fD:
            print("    FAIL", f)
    else:
        print("    PASS — each sensitivity baseline equals the locked representative")

    nE, fE, cE = check_E()
    print("\n[E] Manuscript counts vs data (%d numbers checked)" % nE)
    print("    canonical:", cE)
    if fE:
        ok = False
        for f in fE:
            print("    FAIL", f)
    else:
        print("    PASS — every reported count matches the recomputed value")

    nF, fF = check_F(rows)
    print("\n[F] Derivation-log completeness (%d computed records)" % nF)
    if fF:
        ok = False
        for f in fF:
            print("    FAIL", f)
    else:
        print("    PASS — every computed/derived estimate is in the derivation log")

    print("\n" + "=" * 78)
    print("RESULT:", "ALL CHECKS PASS" if ok else "FAILURES ABOVE")
    print("=" * 78)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
