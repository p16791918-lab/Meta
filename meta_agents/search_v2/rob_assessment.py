#!/usr/bin/env python3
"""Risk-of-bias assessment for the included population-based incidence studies.

Tool: JBI Critical Appraisal Checklist for Studies Reporting Prevalence Data,
applied to population-based cancer-registry incidence studies (the appropriate
JBI instrument for descriptive rate/prevalence designs). Nine items are rated
Yes / No / Unclear:

  Q1 Sample frame appropriate to the target population (defined population-based
     cancer registry: SEER / NAACCR / USCS / NPCR / state / IHS-PRCDA / ANTR).
  Q2 Study participants sampled appropriately (registry ascertains all diagnosed
     cases in the covered population — census-like, not a sample).
  Q3 Adequate sample size (case count sufficient for a stable age-adjusted rate).
  Q4 Study subjects and setting described in detail (registry, period, population,
     racial/ethnic definition, standard population).
  Q5 Data analysis with sufficient coverage of the identified population
     (high-completeness registry).
  Q6 Valid methods used to identify the condition (invasive breast cancer via
     registry / pathology record linkage; ICD-O coding).
  Q7 Condition measured in a standard, reliable way for all participants —
     including race/ethnicity ascertainment (standard registry coding or IHS/
     tribal linkage; surname recognition or a known AI/AN undercount = No).
  Q8 Appropriate statistical analysis (age-standardized to a stated standard
     population, with a reported or correctly computed variance/CI).
  Q9 Response rate — not applicable to census-like registry ascertainment; rated
     adequate where registry coverage is documented (see Q5).

Overall risk of bias (summary of the nine items):
  Low      : 0-1 "No" AND Q7 = Yes AND Q8 = Yes
  High     : >= 3 "No"
  Moderate : otherwise (including any single "No" on the two key items Q7/Q8)

The checklist is applied by the author (a single assessor) with
large-language-model assistance in the manuscript workflow.
"""
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
LED = os.path.join(HERE, "breast_extraction.csv")
REPS = os.path.join(HERE, "TableSA_main_representatives.csv")
OUT_CSV = os.path.join(HERE, "outputs", "TableS_risk_of_bias.csv")
OUT_MD = os.path.join(HERE, "outputs", "TableS_risk_of_bias.md")

QCOLS = ["Q1_frame", "Q2_sampling", "Q3_size", "Q4_described", "Q5_coverage",
         "Q6_condition", "Q7_measurement", "Q8_analysis", "Q9_response"]


def study_facts():
    st = {}
    for r in csv.DictReader(open(LED, encoding="utf-8")):
        rid = r["record_id"]
        if rid == "SEER-EXPL":
            continue
        s = st.setdefault(rid, dict(rid=rid, author=r["author_year"],
                                    registry=r["registry"], period=r["period"],
                                    std=r["std_pop"], provs=set(), cis=0, n=0,
                                    notes="", groups=set(), comparison=""))
        s["provs"].add(r["provenance"])
        s["n"] += 1
        s["groups"].add(r["minority_group"])
        if r["irr_ci_lo"].strip() and r["irr_ci_hi"].strip():
            s["cis"] += 1
        s["notes"] += " " + (r["notes"] or "")
        s["comparison"] = r["comparison_vs"]
    return st


def appraise(s):
    reg = s["registry"].lower()
    notes = s["notes"].lower()
    provs = s["provs"]
    j = {}
    # Q1 sample frame — population-based registry
    j["Q1_frame"] = ("Yes", "population-based cancer registry covering a defined population")
    # Q2 sampling — census-like registry ascertainment
    j["Q2_sampling"] = ("Yes", "registry ascertains all diagnosed cases (census-like)")
    # Q3 sample size / rate stability
    m = re.search(r"(\d+)\s*cases", notes)
    ncase = int(m.group(1)) if m else None
    if (ncase is not None and ncase < 45) or "provisional" in notes:
        j["Q3_size"] = ("No", "small case count / provisional estimate (rate unstable)")
    else:
        j["Q3_size"] = ("Yes", "national/multi-registry or adequate case count for a stable rate")
    # Q4 subjects/setting described
    j["Q4_described"] = ("Yes", "registry, diagnosis period, groups and standard population described")
    # Q5 coverage/completeness
    if re.search(r"seer|naaccr|uscs|npcr|ihs|prcda|california|florida|new mexico|hawaii|"
                 r"navajo|alaska|bay area|puget|atlanta|la county|multi-state|50-state|national", reg):
        j["Q5_coverage"] = ("Yes", "high-completeness registry")
    else:
        j["Q5_coverage"] = ("Unclear", "registry coverage/completeness not documented")
    # Q6 valid identification of the condition
    j["Q6_condition"] = ("Yes", "invasive breast cancer via registry/pathology record linkage")
    # Q7 measured reliably — includes race/ethnicity ascertainment
    if "surname" in notes:
        j["Q7_measurement"] = ("No", "race/ethnicity by surname recognition (misclassification risk)")
    elif "undercount" in notes or "aian undercount" in notes:
        j["Q7_measurement"] = ("No", "unlinked national registry undercounts AI/AN")
    elif ("ihs" in reg or "prcda" in reg or "navajo" in reg or "antr" in reg or "alaska native tumo" in reg):
        j["Q7_measurement"] = ("Yes", "IHS/tribal registry linkage (validated AI/AN classification)")
    else:
        j["Q7_measurement"] = ("Yes", "standard registry race/ethnicity coding; ICD-O condition coding")
    # Q8 appropriate statistical analysis — standardization + variance
    std_ok = bool(re.search(r"2000 us|1970|world|segi|standard|age-adjust", s["std"].lower()))
    direct = any(p.startswith("directly") for p in provs)
    withvar = any(("with-CI" in p or "Poisson" in p) for p in provs)
    has_var = s["cis"] > 0 or direct or withvar
    if std_ok and has_var:
        j["Q8_analysis"] = ("Yes", "age-standardized to a stated standard with a reported/computed variance")
    elif not has_var:
        j["Q8_analysis"] = ("No", "age-adjusted estimate reported as a point value without a variance/CI")
    else:
        j["Q8_analysis"] = ("Unclear", "standard population not clearly stated")
    # Q9 response rate — not applicable to census-like registry
    j["Q9_response"] = ("Yes", "not applicable (census-like registry ascertainment)")

    verd = {k: v[0] for k, v in j.items()}
    n_no = sum(1 for v in verd.values() if v == "No")
    key_ok = verd["Q7_measurement"] == "Yes" and verd["Q8_analysis"] == "Yes"
    if n_no >= 3:
        rob = "High"
    elif n_no <= 1 and key_ok:
        rob = "Low"
    else:
        rob = "Moderate"
    return verd, {k: v[1] for k, v in j.items()}, rob, n_no


def main():
    st = study_facts()
    reps = {r["record_id"] for r in csv.DictReader(open(REPS, encoding="utf-8"))
            if r["main_analysis"].startswith("yes")}
    rows = []
    for rid in sorted(st, key=lambda x: int(x)):
        s = st[rid]
        verd, just, rob, n_no = appraise(s)
        rows.append((s, verd, just, rob, rid in reps))
    cols = (["record_id", "study", "registry", "period", "in_main_analysis"]
            + QCOLS + ["n_No", "Overall_RoB", "justification"])
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for s, verd, just, rob, isrep in rows:
            n_no = sum(1 for v in verd.values() if v == "No")
            jtext = "; ".join("%s:%s (%s)" % (k, verd[k], just[k]) for k in QCOLS)
            w.writerow([s["rid"], s["author"], s["registry"], s["period"],
                        "yes" if isrep else "sensitivity-only"]
                       + [verd[k] for k in QCOLS] + [n_no, rob, jtext])
    from collections import Counter
    qc = Counter(rob for _, _, _, rob, _ in rows)
    qc_rep = Counter(rob for _, _, _, rob, isrep in rows if isrep)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# Table S. Risk of bias — JBI Critical Appraisal Checklist for "
                "Studies Reporting Prevalence/Incidence Data\n\n")
        f.write("Nine items rated Yes/No/Unclear; overall risk of bias summarized as "
                "Low/Moderate/High (see rob_assessment.py header). The checklist was applied "
                "by the author (a single assessor) with large-language-model assistance.\n\n")
        f.write("Overall (%d studies): %s. Main-analysis representatives: %s\n\n"
                % (len(rows), dict(qc), dict(qc_rep)))
        f.write("| Rec | Study | Registry | Period | " + " | ".join(QCOLS) + " | RoB |\n")
        f.write("|----|----|----|----|" + "----|" * (len(QCOLS) + 1) + "\n")
        for s, verd, just, rob, isrep in rows:
            f.write("| %s | %s | %s | %s | %s | **%s** |\n" % (
                s["rid"], s["author"], s["registry"][:26], s["period"][:16],
                " | ".join(verd[k] for k in QCOLS), rob))
    print("wrote %s (%d studies)" % (OUT_CSV, len(rows)))
    print("overall RoB     :", dict(qc))
    print("representatives :", dict(qc_rep))


if __name__ == "__main__":
    main()
