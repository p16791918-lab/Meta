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
from labels import disp_group, disp_dim, disp_comparator
def cite(ay): return re.sub(r"(\d{4})", r" \1", ay.split("_")[0]).strip()  # Kohler2015_SEER18 -> Kohler 2015
# First-author labels for the included studies, derived offline from the raw
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


# ---- Abbreviations (front matter) ----
H("Abbreviations", 1)
ABBR = [
    ("AANHPI", "Asian American, Native Hawaiian, and Pacific Islander"),
    ("AI/AN", "American Indian and Alaska Native"),
    ("ANTR", "Alaska Native Tumor Registry"),
    ("CI", "confidence interval"),
    ("HER2", "human epidermal growth factor receptor 2"),
    ("HR", "hormone receptor"),
    ("IHS", "Indian Health Service"),
    ("IRR", "incidence rate ratio"),
    ("JBI", "Joanna Briggs Institute"),
    ("NAACCR", "North American Association of Central Cancer Registries"),
    ("NHB", "non-Hispanic Black"),
    ("NHPI", "Native Hawaiian and Pacific Islander"),
    ("NHW", "non-Hispanic White"),
    ("NPCR", "National Program of Cancer Registries"),
    ("PRCDA", "Purchased/Referred Care Delivery Area (IHS)"),
    ("PRISMA", "Preferred Reporting Items for Systematic Reviews and Meta-Analyses"),
    ("RoB", "risk of bias"),
    ("SEER", "Surveillance, Epidemiology, and End Results Program"),
    ("SIR", "standardized incidence ratio"),
    ("TNBC", "triple-negative breast cancer"),
    ("USCS", "United States Cancer Statistics (NPCR + SEER)"),
]
TB(["Abbreviation", "Definition"], [[a, d] for a, d in ABBR], [2200, 9000])
PB()

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
inc = rd("TableS_included_studies.csv")
from collections import Counter as _C
_gc = _C(r.get("synth_group", "") for r in inc)
_next, _nelig, _nnarr = _gc["quant-extracted"], _gc["quant-eligible"], _gc["narrative"]
_ninc = _next + _nelig + _nnarr          # total included (recomputed, not hard-coded)
H("Supplementary Table 2. Characteristics of included studies (n = %d)" % _ninc, 1)
if _nelig:
    _elig_clause = ("%d were eligible for quantitative synthesis (of these, %d provided extractable "
                    "quantitative data and entered the analysis, and %d were eligible but provided no "
                    "extractable data), and the remaining %d contributed to the narrative synthesis only "
                    "(%d = %d + %d + %d)." % (_next + _nelig, _next, _nelig, _nnarr, _ninc, _next, _nelig, _nnarr))
else:
    _elig_clause = ("%d were eligible for quantitative synthesis and all provided extractable quantitative "
                    "data that entered the analysis, and the remaining %d contributed to the narrative "
                    "synthesis only (%d = %d + %d)." % (_next, _nnarr, _ninc, _next, _nnarr))
P("The %d studies are all publications included in the systematic review; not all entered the "
  "quantitative synthesis. They are grouped below by how each contributed: %s Study design is classified "
  "from the data source; most included studies are population-based registry/incidence studies "
  "rather than cohort studies. A PMID (or DOI where no PMID exists) is given for every study so "
  "that each of the %d included studies—including the %d in the narrative synthesis—can be "
  "located individually."
  % (_ninc, _elig_clause, _ninc, _nnarr),
  True)
_SECT = {
    "quant-extracted": "Quantitative synthesis — data extracted (n = %d)" % _next,
    "quant-eligible": "Quantitative synthesis — eligible, no extractable data (n = %d)" % _nelig,
    "narrative": "Narrative synthesis only (n = %d)" % _nnarr,
}


def _ident(r):
    p, d = r.get("pmid", "").strip(), r.get("doi", "").strip()
    if p:
        return "PMID " + p
    return ("doi:" + d) if d else ""


rows = []
_cur = None
for r in inc:
    g = r.get("synth_group", "")
    if g != _cur:
        _cur = g
        rows.append({"section": _SECT.get(g, g)})
    rows.append([study_cell(r), r.get("study_design", ""), r.get("data_source", ""),
                 r.get("groups_vs_nhw", ""), _ident(r)])
TB(["Study (author, year)", "Study design", "Data source", "Groups vs NHW", "PMID / DOI"], rows,
   [3400, 2400, 2100, 2400, 1900])
PB()

# ---- S4 excluded (no record_id) ----
H("Supplementary Table 3. Full-text exclusions with reasons", 1)
exc = rd("TableS_excluded_fulltext.csv")
rows = [[study_cell(r), r["exclusion_reason"]] for r in exc]
TB(["Study (author, year)", "Exclusion reason"], rows, [7200, 4500])
PB()

# ---- S5 registry overlap / representatives (author-year, full main_analysis) ----
H("Supplementary Table 4. Registry overlap and representative selection", 1)
P("One representative population-based estimate (contemporary benchmark) per registry family per analytic cell for the main analysis — the most recent, broadest-coverage estimate with an appropriate population definition and standardization, not a pooled estimate; overlapping estimates are retained only for the sensitivity re-selection.", True)
rep = rd("TableSA_main_representatives.csv")
rows = []
for r in rep:
    irr = r["irr"]; ci = f" [{r['irr_ci_lo']}, {r['irr_ci_hi']}]" if r['irr_ci_lo'] else ""
    rows.append([cite(r["author_year"]), disp_dim(r["outcome_dim"]), disp_group(r["minority_group"]),
                 disp_comparator(r.get("comparison_vs", "")), r["registry_family"], r["period"],
                 (r.get("std_pop", "") or "—"), (irr + ci) if irr else "-",
                 r["main_analysis"]])
TB(["Study", "Dimension", "Group", "Comparator", "Registry family", "Period", "Std pop",
    "IRR [95% CI]", "Main analysis"],
   rows, [1500, 1450, 1700, 1700, 1550, 1050, 1150, 1750, 2050])
P("Registries are nested (county ⊂ state ⊂ SEER ⊂ NAACCR ⊂ USCS), so overlapping estimates for the same analytic cell are not independent; one representative was kept per registry family per cell (selection criteria in Methods).", True)
P("Main analysis: “yes (representative)” = the estimate carried into the main analysis as the group’s benchmark; “no (overlaps representative)” = an overlapping estimate for the same cell, used only when the representative is re-selected in the sensitivity analyses (Table 6); “no (AI/AN undercount)” = an unlinked national-registry AI/AN estimate demoted in favour of the IHS-linked representative; “no (registry-direct anchor)” = the SEER-Explorer reference value, not a screened study.", True)
P("Comparator: the reference group is shown as each source defined it — non-Hispanic White (NHW) where the source stratified by Hispanic origin, or “White (not NH-stratified)” otherwise (the latter concentrated in the receptor-defined subtypes and AI/AN comparisons). Because the reference rate and the minority rate come from the same source, period, and standard population, the incidence rate ratio is internally valid even where the reference is unstratified White; a sensitivity analysis restricted to NHW-comparator estimates is reported in Supplementary Table 6c.", True)
P("Standard population: age-standardization is to the 2000 U.S. standard unless the “Std pop” column shows otherwise. Because the rate ratio is formed within each study, the standard population largely cancels; the few non-2000 estimates are flagged in the “Std pop” column.", True)
PB()

# ---- S7 RoB (study = author-year; no record_id) ----
H("Supplementary Table 5. Risk of bias (JBI checklist for studies reporting prevalence/incidence data)", 1)
P("Nine JBI items rated Y (Yes) / N (No) / U (Unclear); overall risk of bias is summarized as Low, Moderate, or High. The checklist was applied to each study by the author (a single assessor) with large-language-model assistance.", True)
rob = rd("outputs/TableS_risk_of_bias.csv")
def _v(x): return {"Yes": "Y", "No": "N", "Unclear": "U"}.get(x.strip(), x.strip())
QC = ["Q1_frame", "Q2_sampling", "Q3_size", "Q4_described", "Q5_coverage",
      "Q6_condition", "Q7_measurement", "Q8_analysis", "Q9_response"]
rrows = [[cite(r["study"])] + [_v(r[q]) for q in QC] + [r["Overall_RoB"]] for r in rob]
TB(["Study", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "RoB"],
   rrows, [3200, 620, 620, 620, 620, 620, 620, 620, 620, 620, 1400])
P("JBI items: Q1 sample frame appropriate to the target population (defined population-based registry); Q2 appropriate sampling (registry ascertains all diagnosed cases — census-like); Q3 adequate sample size for a stable age-adjusted rate; Q4 study subjects and setting described in detail; Q5 sufficient coverage of the identified population (registry completeness); Q6 valid identification of the condition (invasive breast cancer via registry/pathology record linkage); Q7 condition measured in a standard, reliable way for all participants, including race/ethnicity ascertainment (surname recognition or a known AI/AN undercount = No); Q8 appropriate statistical analysis (age-standardized to a stated standard population with a reported or correctly computed variance); Q9 response rate — not applicable to census-like registry ascertainment.", True)
_nlow = sum(1 for r in rob if r["Overall_RoB"] == "Low")
_nmod = sum(1 for r in rob if r["Overall_RoB"] == "Moderate")
_nhigh = sum(1 for r in rob if r["Overall_RoB"] == "High")
P("Overall risk of bias: Low = at most one item not met with the two key items (Q7 measurement, Q8 analysis) met; High = three or more items not met; Moderate otherwise. Of %d studies assessed, %d were Low, %d Moderate, and %d High; the Moderate ratings arise chiefly where an estimate was reported as a point value without a variance (Q8) or where race/ethnicity ascertainment was limited (Q7)."
  % (len(rob), _nlow, _nmod, _nhigh), True)
PB()

# ---- S10 sensitivity ----
H("Supplementary Table 6. Sensitivity analyses", 1)
from collections import Counter as _Ctr
s1 = rd("outputs/Sensitivity1_good_rob.csv"); ch1 = [r for r in s1 if r["status"] != "unchanged"]
_c1 = _Ctr(r["status"] for r in s1)
P("Table 6a. Low-risk-of-bias only (Moderate/High-RoB studies dropped): %d of %d cells unchanged, %d changed, %d dropped. The changed and dropped cells were concentrated in the disaggregated AANHPI subgroups (with a few age-specific and Middle Eastern cells), whose representatives are computed estimates from moderate-risk-of-bias sources; the AI/AN representatives are unchanged because the IHS-linked estimates preferred in the main analysis are themselves low risk of bias."
  % (_c1["unchanged"], sum(_c1.values()), _c1["changed"], _c1["dropped"]))
TB(["Dimension", "Group", "Main IRR [95% CI]", "Sens IRR [95% CI]", "Status"], [[disp_dim(r["dimension"]), disp_group(r["group"]), r["main_irr"] + r.get("main_ci", ""), (r["sens_irr"] + r.get("sens_ci", "")) if r["sens_irr"] else "-", r["status"]] for r in ch1], [1800, 2200, 3000, 3000, 900])
s2 = rd("outputs/Sensitivity2_directly_reported.csv"); ch2 = [r for r in s2 if r["status"] == "changed"]
_c2 = _Ctr(r["status"] for r in s2)
P("Table 6b. Directly-reported-only (computed estimates dropped): %d unchanged, %d changed, %d dropped — most disaggregated/subtype cells rely on computed rates (registries report rates, not ratios)."
  % (_c2["unchanged"], _c2["changed"], _c2["dropped"]))
TB(["Dimension", "Group", "Main IRR [95% CI]", "Sens IRR [95% CI]", "Status"], [[disp_dim(r["dimension"]), disp_group(r["group"]), r["main_irr"] + r.get("main_ci", ""), (r["sens_irr"] + r.get("sens_ci", "")) if r["sens_irr"] else "-", r["status"]] for r in ch2], [1800, 2200, 3000, 3000, 900])
s3 = rd("outputs/Sensitivity3_nhw_only.csv"); ch3 = [r for r in s3 if r["status"] != "unchanged"]
_c3 = _Ctr(r["status"] for r in s3)
P("Table 6c. Non-Hispanic White comparator only (unstratified-White comparators dropped): %d of %d cells unchanged, %d changed, %d dropped. The aggregate, disaggregated-AANHPI, and Hispanic-origin cells are unchanged because they already use an NHW comparator; the dropped cells are those whose only representative used an unstratified White reference — the receptor-defined subtype set (Loo 2019), the ER/PR subtypes (Gleason 2012), and the two age-specific Black cells — confirming which findings depend on the unstratified-White comparator."
  % (_c3["unchanged"], sum(_c3.values()), _c3["changed"], _c3["dropped"]))
TB(["Dimension", "Group", "Main IRR [95% CI]", "Sens IRR [95% CI]", "Status"], [[disp_dim(r["dimension"]), disp_group(r["group"]), r["main_irr"] + r.get("main_ci", ""), (r["sens_irr"] + r.get("sens_ci", "")) if r["sens_irr"] else "-", r["status"]] for r in ch3], [1800, 2200, 3000, 3000, 900])
P("Main IRR = representative estimate in the main analysis. Sens IRR = the representative re-selected after applying the sensitivity restriction (low-risk-of-bias only in Table 6a; author-reported IRR/SIR only in Table 6b; NHW-comparator only in Table 6c). Status: unchanged = same study remains the representative; changed = a different study becomes the representative (its IRR is shown); dropped = no eligible estimate remained for that cell (Sens IRR = “–”). Only changed/dropped cells are listed; the remaining cells were unchanged. A “dropped” cell means no estimate met the restriction, not that the main estimate changed.", True)
PB()

# ==== NOTES (after all tables) ====
H("Supplementary Note 1. Provenance of estimates and derivation log", 1)
# map internal record_id -> readable author-year (reader-facing, like the tables)
_ay = {}
for r in csv.DictReader(open(os.path.join(HERE, "breast_extraction.csv"), encoding="utf-8")):
    if r["record_id"] != "SEER-EXPL":
        _ay.setdefault(r["record_id"], re.sub(r"(\d{4})", r" \1", r["author_year"].split("_")[0]).strip())

def _rec(text):
    text = re.sub(r"rec (\d+)/(\d+)", r"rec \1, rec \2", text)      # expand rec a/b
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

json.dump(M, open(os.path.join(OUT, "_suppl_manifest.json"), "w"), ensure_ascii=False)
from collections import Counter
print("manifest:", dict(Counter(m["type"] for m in M)),
      "| table rows:", sum(len(m["rows"]) for m in M if m["type"] == "table"))
