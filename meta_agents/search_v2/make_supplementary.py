#!/usr/bin/env python3
"""Assemble the single Supplementary Materials manifest (outputs/_suppl_manifest.json)
from the pipeline outputs. Reader-facing tables use author-year (not the internal
record_id). Rendered to Word by build_supplementary_docx.js."""
import csv, json, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
M = []


def H(t, l=1): M.append({"type": "heading", "text": t, "level": l})
def P(t, it=False): M.append({"type": "para", "text": t, "italic": it})
def TB(h, rows, w): M.append({"type": "table", "headers": h, "rows": rows, "widths": w})
def IMG(p, w, h): M.append({"type": "image", "path": os.path.join(OUT, p), "w": w, "h": h})
def CODE(lines): M.append({"type": "code", "lines": lines})
def GT(groups, subs, rows, w): M.append({"type": "gtable", "groups": groups, "subs": subs, "rows": rows, "widths": w})
def ST(rows, w): M.append({"type": "stable", "rows": rows, "widths": w})
def PB(): M.append({"type": "pagebreak"})
def rd(p): return list(csv.DictReader(open(os.path.join(HERE, p), encoding="utf-8")))
from labels import disp_group
def cite(ay): return re.sub(r"(\d{4})", r" \1", ay.split("_")[0]).strip()  # Kohler2015_SEER18 -> Kohler 2015
# First-author labels for the 163 included studies, derived offline from the raw
# search dumps (MEDLINE FAU / Embase / Scopus / WoS), keyed by record_id. Used to
# put a real author on the "Study (author, year)" column instead of title-only.
AUTHORS = json.load(open(os.path.join(HERE, "author_labels.json"), encoding="utf-8"))
def study_cell(r):
    # "Study (author, year)" column: title, then (author, year) in parentheses —
    # e.g. "Breast Cancer Incidence in Asian American ... (Gomez et al., 2026)".
    au = AUTHORS.get(r["record_id"], "").strip()
    cit = r["citation"].strip()
    ym = re.search(r"\s*\((\d{4})\)\s*$", cit)
    year = ym.group(1) if ym else ""
    title = cit[:ym.start()].strip() if ym else cit
    if au and year:
        return "%s (%s, %s)" % (title, au, year)
    if year:
        return "%s (%s)" % (title, year)
    return cit


# ---- S1 search strategy ----
H("Supplementary Table 1. Final search strategy for each database", 1)
P("Search conducted 7 August 2026. Concept blocks combined with AND: breast cancer × race/ethnicity × incidence/age-adjusted rate × United States. Limits: 2000–2026, English, human; document-type exclusions.", True)
t = open(os.path.join(HERE, "..", "SEARCH_STRINGS_v2.md"), encoding="utf-8").read()
blocks = re.findall(r"## (\d)\. ([^\n]+)\n+```\n(.*?)```", t, re.S)
meta = [("PubMed/MEDLINE", "PubMed", "1,331"), ("Embase", "embase.com (Advanced Search)", "3,248"),
        ("Scopus", "scopus.com (Advanced Search)", "2,438"), ("Web of Science", "Web of Science (Advanced)", "2,082")]
srows = [{"db": m[0], "platform": m[1], "date": "2026-08-07", "records": m[2],
          "query": [l.rstrip() for l in code.strip("\n").split("\n")]}
         for (num, title, code), m in zip(blocks, meta)]
ST(srows, [1700, 2000, 1200, 1000, 8500])
P("Total records identified 9,099; duplicate records removed (cross-database) 4,306; unique records screened 4,793.", True)
PB()

# ---- S3 included (author-year via citation; no record_id) ----
H("Supplementary Table 2. Characteristics of included studies (n = 163)", 1)
inc = rd("TableS_included_studies.csv")
rows = [[study_cell(r), r.get("data_source", ""), r.get("groups_vs_nhw", ""), r.get("synthesis", "")] for r in inc]
TB(["Study (author, year)", "Data source", "Groups vs NHW", "Synthesis"], rows, [5200, 2700, 2600, 1300])
PB()

# ---- S4 excluded (no record_id) ----
H("Supplementary Table 3. Full-text exclusions with reasons", 1)
exc = rd("TableS_excluded_fulltext.csv")
rows = [[study_cell(r), r["exclusion_reason"]] for r in exc]
TB(["Study (author, year)", "Exclusion reason"], rows, [7200, 4500])
PB()

# ---- S5 registry overlap / representatives (author-year, full main_analysis) ----
H("Supplementary Table 4. Registry overlap and representative selection", 1)
P("One representative per registry family per analytic cell for the main analysis; overlapping estimates retained for sensitivity.", True)
rep = rd("TableSA_main_representatives.csv")
rows = []
for r in rep:
    irr = r["irr"]; ci = f" [{r['irr_ci_lo']}, {r['irr_ci_hi']}]" if r['irr_ci_lo'] else ""
    rows.append([cite(r["author_year"]), r["outcome_dim"], disp_group(r["minority_group"]),
                 r["registry_family"], r["period"], (irr + ci) if irr else "-",
                 r["main_analysis"]])
TB(["Study", "Dimension", "Group", "Registry family", "Period", "IRR [95% CI]", "Main analysis"],
   rows, [1900, 1800, 2200, 2000, 1200, 2200, 2600])
P("Registries are nested (county ⊂ state ⊂ SEER ⊂ NAACCR ⊂ USCS), so overlapping estimates for the same analytic cell are not independent. For each cell (outcome dimension × group) one representative was kept per registry family, selected by (i) an IRR being computable, (ii) coverage (USCS > NAACCR > SEER-national > state/regional), (iii) most recent end-year then longest span, and (iv) clearest standardization / directly-reported CI.", True)
P("Main analysis: “yes (representative)” = the estimate carried into the main analysis; “no (overlaps representative)” = collapses to the cell representative and is used only in the all-included sensitivity analysis; “no (AI/AN undercount)” = an unlinked national-registry AI/AN estimate demoted in favour of the IHS-linked representative; “no (registry-direct anchor)” = the SEER-Explorer reference value, not a screened study.", True)
P("Terminology: comparisons are versus non-Hispanic White (NHW); “non-Hispanic Black (NHB)” and NHW denote non-Hispanic categories. Five older sources did NOT stratify by Hispanic origin — Anderson 2008 and Brinton 2008 (age-specific), Gleason 2012 (ER/PR subtypes), and Cronin 2012 and Richardson 2016 (aggregate, sensitivity/overlap only) — so their Black/White groups are non-stratified; none is a main-analysis representative for the headline (aggregate/TNBC) cells (Note 1).", True)
PB()

# ---- S7 RoB (study = author-year; no record_id) ----
H("Supplementary Table 5. Risk of bias (Newcastle-Ottawa Scale, adapted)", 1)
P("Each cell shows 1 where the item was met (blank = not met). Selection (max 4): S1–S4; Comparability (max 2): C1–C2; Outcome (max 3): O1–O3. AI-generated first pass; reviewer to spot-check.", True)
rob = rd("outputs/TableS_risk_of_bias.csv")
def _s(v): return "1" if v.strip() == "1" else ""
rrows = [[cite(r["study"]), _s(r["S1_representative"]), _s(r["S2_samplesize"]), _s(r["S3_race_ascertain"]),
          _s(r["S4_completeness"]), _s(r["C1_agestd"]), _s(r["C2_comparable"]),
          _s(r["O1_outcome"]), _s(r["O2_stats_CI"]), _s(r["O3_analysis"]), r["Overall_quality"]] for r in rob]
GT([["Study", 1, True], ["Selection", 4, False], ["Comparability", 2, False], ["Outcome", 3, False], ["Quality", 1, True]],
   [None, "S1", "S2", "S3", "S4", "C1", "C2", "O1", "O2", "O3", None],
   rrows, [3600, 700, 700, 700, 700, 700, 700, 700, 700, 700, 2100])
P("Sel = Selection (max 4 stars): (1) representativeness — defined population-based registry; (2) sample size — adequate case count for a stable age-adjusted rate (national/multi-registry or ≥50 cases); (3) ascertainment of race/ethnicity — standard registry coding or IHS/tribal linkage (surname-based or national AI/AN undercount loses the star); (4) case ascertainment completeness (high-completeness registry).", True)
P("Comp = Comparability (max 2 stars): (1) age-standardization to a stated standard population (e.g., 2000 US); (2) minority and non-Hispanic White comparator from the same standard, diagnosis period and registry (externally-paired comparator loses the star).", True)
P("Out = Outcome (max 3 stars): (1) outcome assessment — invasive breast cancer via registry/pathology record linkage; (2) statistical reporting — 95% CI or SE reported; (3) appropriate analysis — age-adjusted IRR directly reported or correctly computed with a variance (point-only computation loses the star).", True)
P("Overall quality (AHRQ thresholds): Good = Selection 3–4 AND Comparability 1–2 AND Outcome 2–3; Fair = Selection 2 AND Comparability 1–2 AND Outcome 2–3; Poor = Selection 0–1 OR Comparability 0 OR Outcome 0–1. The 8 Poor ratings arise where only a point estimate without a confidence interval was available (Outcome = 1). Assessment is an AI-generated first pass for reviewer verification.", True)
PB()

# ---- Table 6: GRADE-informed scoring framework (like supervisor Table 2) ----
H("Supplementary Table 6. Certainty of evidence assessment using a GRADE-informed scoring framework", 1)
framework = [
    ["Baseline certainty", "All outcomes are bodies of observational, population-based cancer-registry evidence and therefore start at Low (baseline score = 0)."],
    ["Risk of bias", "Based on the adapted Newcastle-Ottawa Scale (Table 5). Downgraded by −1 when the representative study for the outcome was rated Poor."],
    ["Inconsistency", "Downgraded by −1 when overlapping estimates for the same cell disagreed in the direction of effect. The very high I² among overlapping registry estimates was NOT treated as inconsistency, because it reflects repeated inclusion of non-independent, nested registry data rather than genuine between-study heterogeneity."],
    ["Indirectness", "Downgraded by −1 when the population, exposure, comparator, or outcome did not directly correspond to the review question. Judged not serious: U.S. population-based registries directly measure age-adjusted invasive breast-cancer incidence by race/ethnicity versus non-Hispanic White."],
    ["Imprecision", "Downgraded by −1 when the 95% confidence interval included the null (IRR = 1.0) for a near-null estimate, or when only a point estimate without a confidence interval was available."],
    ["Publication bias", "Judged not serious: registry data reflect near-complete (census-like) case ascertainment and are not subject to selective publication of significant results; funnel-plot / Egger assessment is not applicable."],
    ["Strength of association", "Upgraded for a large magnitude of effect: +1 when IRR ≤ 0.50 or ≥ 2.00; +2 when IRR ≤ 0.20 or ≥ 5.00, provided residual bias is unlikely to account for it."],
    ["Dose–response / confounding", "Not applied: these descriptive incidence studies do not assess an exposure gradient, and residual-confounding upgrades were not used."],
    ["Scoring rules", "Final certainty from the Low baseline: High (total score ≥ 2), Moderate (1), Low (0), Very low (≤ −1). Per-outcome scores are given in Table 7. Assessment is an AI-generated first pass for reviewer verification."],
]
TB(["Criteria", "Descriptions"], framework, [3000, 11400])
PB()

# ---- Table 7: GRADE results by outcome ----
H("Supplementary Table 7. GRADE certainty of evidence by outcome", 1)
P("Certainty derived with the framework in Table 6. RoB = Newcastle-Ottawa rating of the representative study (Table 5); +Large = large-magnitude upgrade (+1 if IRR ≤ 0.50 or ≥ 2.00; +2 if ≤ 0.20 or ≥ 5.00).", True)
gr = rd("outputs/TableS_GRADE.csv")
rows = [[r["dimension"], disp_group(r["group"]), r["IRR"], r["rob"], r["up_LargeEffect"], r["GRADE"]] for r in gr]
TB(["Dimension", "Group", "IRR [95% CI]", "RoB", "+Large", "GRADE"], rows, [2100, 2500, 2400, 1200, 1100, 1700])
PB()

# ---- S9 heterogeneity + estimator ----
H("Supplementary Table 8. Between-study heterogeneity and estimator comparison", 1)
P("Sensitivity = all overlapping estimates (Paule-Mandel + HKSJ); high I² reflects non-independent registry overlap. Main = one representative per family.", True)
si = rd("outputs/Table_sensitivity_I2.csv")
rows = [[r["dimension"], disp_group(r["group"]), r["k_all"], "Random-effects",
         f"{r['sens_irr']} ({r['sens_lo']}-{r['sens_hi']})", r["I2"] + "%", r["p_Q"],
         (f"{r['main_irr']} ({r['main_lo']}-{r['main_hi']})" if r['main_irr'] else "-")] for r in si]
TB(["Dimension", "Group", "k", "Model", "Sensitivity IRR (95% CI)", "I²", "Q p", "Main IRR (95% CI)"],
   rows, [1700, 1950, 500, 1500, 2500, 750, 850, 2300])
P("k = number of overlapping estimates pooled. Model = random-effects for every cell (Paule-Mandel/REML τ² with a Hartung-Knapp-Sidik-Jonkman confidence interval); no fixed-effect model was used. Sensitivity IRR = all k estimates pooled. I² and Q p = the between-study heterogeneity of the all-included (sensitivity) pool; Q p is the p-value of Cochran's Q (χ² with k−1 df). The very high I² / small Q p here reflect repeated inclusion of non-independent, overlapping registry data rather than genuine between-study heterogeneity — which is why it is NOT treated as inconsistency in the GRADE framework (Table 6) and why the main analysis collapses to one representative per registry family. Main IRR = that single representative, which removes the non-independence. For cells with k < 3 the HKSJ interval (t with k−1 df) is unstable and over-wide, so read the point estimate rather than the interval. Only cells with ≥ 2 overlapping estimates appear here.", True)
P("Estimator comparison (τ² method and confidence-interval method) for every cell "
  "with ≥2 overlapping estimates. Cells marked * have k < 3, where the "
  "Hartung-Knapp interval (t with k−1 df) is unstable; read the point estimate.", True)
ec = rd("outputs/Table_estimator_comparison.csv")
ecrows = [[f"{disp_group(r['group'])}{r['klt3']}", r["k"],
           f"{r['dl_irr']} ({r['dl_ci']})", r["dl_tau2"],
           f"{r['pm_irr']} ({r['pm_ci']})", r["pm_tau2"],
           r["hksj_ci"], r["i2"] + "%"] for r in ec]
TB(["Group", "k", "DerSimonian-Laird IRR (95% CI)", "DL τ²",
    "Paule-Mandel / REML IRR (95% CI)", "PM τ²", "HKSJ 95% CI", "I²"],
   ecrows, [2400, 600, 2900, 900, 2900, 900, 1900, 700])
P("Across the four cells with ≥3 estimates (Black, Hispanic, Asian/Pacific Islander, "
  "American Indian/Alaska Native), the DerSimonian-Laird and Paule-Mandel/REML pooled "
  "IRRs differ by ≤0.001, and the Hartung-Knapp interval is wider than the z-based "
  "interval; the pooled estimate is therefore robust to the choice of τ² estimator and "
  "interval method. The main analysis nonetheless relies on one representative per "
  "registry family rather than these pooled values, because the estimates are not "
  "independent.", True)
PB()

# ---- S10 sensitivity ----
H("Supplementary Table 9. Sensitivity analyses", 1)
P("Table 9a. Good-RoB-only (Poor studies dropped): 82 of 90 cells unchanged, 1 changed, 7 dropped — all headline results unchanged.")
s1 = rd("outputs/Sensitivity1_good_rob.csv"); ch1 = [r for r in s1 if r["status"] != "unchanged"]
TB(["Dimension", "Group", "Main IRR", "Sens IRR", "Status"], [[r["dimension"], disp_group(r["group"]), r["main_irr"], r["sens_irr"] or "-", r["status"]] for r in ch1], [2300, 2600, 2000, 2000, 1500])
P("Table 9b. Directly-reported-only (computed estimates dropped): 51 unchanged, 5 changed, 34 dropped — most disaggregated/subtype cells rely on computed rates (registries report rates, not ratios).")
s2 = rd("outputs/Sensitivity2_directly_reported.csv"); ch2 = [r for r in s2 if r["status"] == "changed"]
TB(["Dimension", "Group", "Main IRR", "Sens IRR", "Status"], [[r["dimension"], disp_group(r["group"]), r["main_irr"], r["sens_irr"] or "-", r["status"]] for r in ch2], [2300, 2600, 2000, 2000, 1500])
P("Main IRR = representative estimate in the main analysis. Sens IRR = the representative re-selected after applying the sensitivity restriction (Good-RoB-only in Table 9a; author-reported IRR/SIR only in Table 9b). Status: unchanged = same study remains the representative; changed = a different study becomes the representative (its IRR is shown); dropped = no eligible estimate remained for that cell (Sens IRR = “–”). Only changed/dropped cells are listed; all others were unchanged, indicating the main results are robust.", True)
PB()

# ==== NOTES (after all tables) ====
H("Supplementary Note 1. Provenance of estimates and derivation log", 1)
# map internal record_id -> readable author-year (reader-facing, like the tables)
_ay = {}
for r in csv.DictReader(open(os.path.join(HERE, "breast_extraction.csv"), encoding="utf-8")):
    if r["record_id"] != "SEER-EXPL":
        _ay.setdefault(r["record_id"], re.sub(r"(\d{4})", r" \1", r["author_year"].split("_")[0]).strip())
_ay.update({"461": "the Northern Plains AI/AN study",
            "1336": "the npj Breast Cancer 2026 mortality study",
            "2548": "Oyenuga 2018 (Hmong-Minnesota)"})

def _rec(text):
    text = re.sub(r"rec (\d+)/(\d+)", r"rec \1, rec \2", text)      # expand rec a/b
    text = re.sub(r"rec \d+ (\()", r"\1", text)                     # drop prefix if author-year follows in ()
    text = re.sub(r"rec (\d+)", lambda m: _ay.get(m.group(1), "study " + m.group(1)), text)
    return text.replace("**", "")                                   # strip markdown bold

d = open(os.path.join(HERE, "DERIVATIONS.md"), encoding="utf-8").read()
for line in d.split("\n"):
    line = line.rstrip()
    if not line: continue
    if line.startswith("## "): H(_rec(line[3:]), 2)
    elif line.startswith("# "): pass
    elif line.startswith("- ") or line.startswith("  "): P("• " + _rec(line.strip("- ").strip()))
    else: P(_rec(line))
PB()

# ==== FIGURES (portrait section, grouped at the end, like the example paper) ====
# PRISMA and the two representative forests are promoted to the main text
# (Main Figures 1-3); the Supplementary keeps only the pooled (all-included)
# forests, which carry the per-study weights and random-effects diamonds.
H("Supplementary Figure 1. Pooled forest plots — aggregate racial/ethnic groups", 1)
P("Every contributing study per group with the random-effects pooled diamond "
  "(Paule-Mandel/REML + Hartung-Knapp) and I². The high I² reflects non-independent "
  "overlapping registry data (all-included / sensitivity pooling); the main analysis "
  "instead uses one representative per registry family (Table 4).", True)
IMG("Fig_pool_aggregate.png", 602, 880)
PB()
H("Supplementary Figure 2. Pooled forest plots — triple-negative breast cancer", 1)
IMG("Fig_pool_tnbc.png", 680, 466)
PB()
H("Supplementary Figure 3. Pooled forest plots — disaggregated subgroups with ≥2 studies", 1)
IMG("Fig_pool_disaggregated.png", 680, 591)

json.dump(M, open(os.path.join(OUT, "_suppl_manifest.json"), "w"), ensure_ascii=False)
from collections import Counter
print("manifest:", dict(Counter(m["type"] for m in M)),
      "| table rows:", sum(len(m["rows"]) for m in M if m["type"] == "table"))
