#!/usr/bin/env python3
"""Risk-of-bias assessment for the included population-based incidence studies.

Tool: Newcastle-Ottawa Scale adapted for cross-sectional / population-based
descriptive incidence studies (same 3-domain structure and Good/Fair/Poor rubric
as the reference paper's NOS table, but with items appropriate to registry
incidence studies rather than case-control/cohort designs).

Domains and star items (max 9):
  SELECTION (max 4)
    S1 Representativeness of the sample : population-based registry covering a
       defined geographic population (SEER/NAACCR/USCS/state/IHS/ANTR/Navajo/CCR).
    S2 Sample size / case stability     : adequate case count for a stable
       age-adjusted rate (national/multi-registry, or >=50 cases in the group).
    S3 Ascertainment of race/ethnicity  : standard registry race coding or
       IHS/tribal linkage (validated); surname-only or known national AIAN
       misclassification loses the star.
    S4 Case ascertainment completeness  : high-completeness registry (SEER/
       NAACCR/USCS ~93-99%); undocumented/partial coverage loses the star.
  COMPARABILITY (max 2)
    C1 Age-standardization              : rates standardized to a stated standard
       population (2000 US, 1970 US, world).
    C2 Comparable standard/period/group : minority and NHW comparator drawn from
       the same standard population, diagnosis period and registry (in-paper
       comparator); externally-paired NHW loses the star.
  OUTCOME (max 3)
    O1 Outcome assessment               : invasive breast cancer via registry/
       pathology record linkage (objective).
    O2 Statistical reporting            : 95% CI or SE reported for the estimate.
    O3 Appropriate analysis             : age-adjusted IRR/rate directly reported
       or correctly computed with a variance; point-only computation loses star.

Rubric (per reference paper / AHRQ):
  Good : Selection 3-4 AND Comparability 1-2 AND Outcome 2-3
  Fair : Selection 2   AND Comparability 1-2 AND Outcome 2-3
  Poor : Selection 0-1 OR  Comparability 0   OR Outcome 0-1

NOTE: this is an AI-generated first-pass to be spot-checked by the reviewer
(per feedback item 4). Each star carries a short justification.
"""
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
LED = os.path.join(HERE, "breast_extraction.csv")
REPS = os.path.join(HERE, "TableSA_main_representatives.csv")
OUT_CSV = os.path.join(HERE, "outputs", "TableS_risk_of_bias.csv")
OUT_MD = os.path.join(HERE, "outputs", "TableS_risk_of_bias.md")


def study_facts():
    led = list(csv.DictReader(open(LED, encoding="utf-8")))
    st = {}
    for r in led:
        rid = r["record_id"]
        if rid == "SEER-EXPL":
            continue
        s = st.setdefault(rid, dict(rid=rid, author=r["author_year"],
                                    registry=r["registry"], period=r["period"],
                                    std=r["std_pop"], provs=set(), cis=0, n=0,
                                    notes=" ".join([]), groups=set()))
        s["provs"].add(r["provenance"])
        s["n"] += 1
        s["groups"].add(r["minority_group"])
        if r["irr_ci_lo"].strip() and r["irr_ci_hi"].strip():
            s["cis"] += 1
        s["notes"] += " " + (r["notes"] or "")
        s["comparison"] = r["comparison_vs"]
    return st


def score(s):
    reg = s["registry"].lower()
    notes = s["notes"].lower()
    provs = s["provs"]
    j = {}
    # ---- SELECTION ----
    S1 = 1
    j["S1"] = "population-based registry"
    S2 = 1
    j["S2"] = "national/multi-registry or adequate cases"
    # small-count / provisional / single-region small subgroup
    m = re.search(r"(\d+)\s*cases", notes)
    ncase = int(m.group(1)) if m else None
    if (ncase is not None and ncase < 45) or "provisional" in notes:
        S2 = 0
        j["S2"] = "small case count / provisional estimate (rate unstable)"
    S3 = 1
    j["S3"] = "standard registry race coding"
    if "surname" in notes:
        S3 = 0
        j["S3"] = "race/ethnicity by surname recognition (misclassification risk)"
    elif ("ihs" in reg or "prcda" in reg or "navajo" in reg or "antr" in reg
          or "alaska native tumo" in reg):
        j["S3"] = "IHS/tribal registry linkage (validated AI/AN classification)"
    elif "aian undercount" in notes or "undercount" in notes:
        S3 = 0
        j["S3"] = "unlinked national registry undercounts AI/AN"
    S4 = 1
    j["S4"] = "high-completeness registry"
    if not re.search(r"seer|naaccr|uscs|npcr|ihs|prcda|california|florida|"
                     r"new mexico|hawaii|navajo|alaska|bay area|puget|atlanta|"
                     r"la county|multi-state|50-state|national", reg):
        S4 = 0
        j["S4"] = "coverage/completeness not documented"
    sel = S1 + S2 + S3 + S4
    # ---- COMPARABILITY ----
    C1 = 1 if re.search(r"2000 us|1970|world|segi|standard", s["std"].lower()) else 0
    j["C1"] = ("standardized to %s" % s["std"]) if C1 else "standardization not stated"
    ext = ("external" in notes or "seer-explorer" in notes
           or "back-derived" in notes or s.get("comparison", "").lower().find("external") >= 0)
    C2 = 0 if ext else 1
    j["C2"] = "externally-paired NHW comparator" if ext else "in-paper NHW comparator, same registry/period/standard"
    comp = C1 + C2
    # ---- OUTCOME ----
    O1 = 1
    j["O1"] = "invasive breast cancer via registry/pathology linkage"
    O2 = 1 if s["cis"] > 0 else 0
    j["O2"] = "95% CI / SE reported" if O2 else "point estimate only (no CI)"
    direct = any(p.startswith("directly") for p in provs)
    withvar = any(("with-CI" in p or "Poisson" in p) for p in provs)
    O3 = 1 if (direct or withvar) else 0
    j["O3"] = ("directly reported / computed with variance" if O3
               else "age-adjusted IRR computed as point only (no variance)")
    out = O1 + O2 + O3
    # ---- rubric ----
    if sel >= 3 and 1 <= comp <= 2 and 2 <= out <= 3:
        q = "Good"
    elif sel == 2 and 1 <= comp <= 2 and 2 <= out <= 3:
        q = "Fair"
    else:
        q = "Poor"
    return dict(S1=S1, S2=S2, S3=S3, S4=S4, C1=C1, C2=C2, O1=O1, O2=O2, O3=O3,
                sel=sel, comp=comp, out=out, quality=q, j=j)


def main():
    st = study_facts()
    reps = set()
    for r in csv.DictReader(open(REPS, encoding="utf-8")):
        if r["main_analysis"].startswith("yes"):
            reps.add(r["record_id"])
    rows = []
    for rid in sorted(st, key=lambda x: int(x)):
        s = st[rid]
        sc = score(s)
        rows.append((s, sc, rid in reps))
    cols = ["record_id", "study", "registry", "period", "in_main_analysis",
            "S1_representative", "S2_samplesize", "S3_race_ascertain",
            "S4_completeness", "C1_agestd", "C2_comparable",
            "O1_outcome", "O2_stats_CI", "O3_analysis",
            "Selection_/4", "Comparability_/2", "Outcome_/3", "Overall_quality",
            "justification"]
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for s, sc, isrep in rows:
            j = sc["j"]
            just = "; ".join("%s:%s" % (k, j[k]) for k in
                             ["S1", "S2", "S3", "S4", "C1", "C2", "O1", "O2", "O3"])
            w.writerow([s["rid"], s["author"], s["registry"], s["period"],
                        "yes" if isrep else "sensitivity-only",
                        sc["S1"], sc["S2"], sc["S3"], sc["S4"], sc["C1"], sc["C2"],
                        sc["O1"], sc["O2"], sc["O3"],
                        sc["sel"], sc["comp"], sc["out"], sc["quality"], just])
    # markdown summary
    from collections import Counter
    qc = Counter(sc["quality"] for _, sc, _ in rows)
    qc_rep = Counter(sc["quality"] for _, sc, isrep in rows if isrep)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# Table S. Risk of bias — Newcastle-Ottawa Scale "
                "(adapted for population-based incidence studies)\n\n")
        f.write("Domains: Selection (max 4), Comparability (max 2), Outcome (max 3). "
                "Quality per AHRQ thresholds (see rob_assessment.py header). "
                "**AI-generated first pass — reviewer to spot-check.**\n\n")
        f.write("Overall (43 studies): %s. Main-analysis representatives (28): %s\n\n"
                % (dict(qc), dict(qc_rep)))
        f.write("| Rec | Study | Registry | Period | Main | Sel/4 | Comp/2 | Out/3 | Quality |\n")
        f.write("|----|----|----|----|----|----|----|----|----|\n")
        for s, sc, isrep in rows:
            f.write("| %s | %s | %s | %s | %s | %d | %d | %d | **%s** |\n" % (
                s["rid"], s["author"], s["registry"][:30], s["period"][:16],
                "Y" if isrep else "s", sc["sel"], sc["comp"], sc["out"], sc["quality"]))
    print("wrote %s (%d studies)" % (OUT_CSV, len(rows)))
    print("overall quality:", dict(qc))
    print("representatives  :", dict(qc_rep))


if __name__ == "__main__":
    main()
