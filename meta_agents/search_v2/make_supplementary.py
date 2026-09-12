#!/usr/bin/env python3
"""Assemble the single Supplementary Materials manifest (outputs/_suppl_manifest.json)
from the pipeline outputs. Reader-facing tables use author-year (not the internal
record_id). Rendered to Word by build_supplementary_docx.js."""
import csv, json, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
M = []


def H(t, l=1): M.append({"type": "heading", "text": t, "level": l})
def P(t, it=False, ind=0): M.append({"type": "para", "text": t, "italic": it, "indent": ind})
def TB(h, rows, w): M.append({"type": "table", "headers": h, "rows": rows, "widths": w})
def IMG(p, w, h): M.append({"type": "image", "path": os.path.join(OUT, p), "w": w, "h": h})
def CODE(lines): M.append({"type": "code", "lines": lines})
def GT(groups, subs, rows, w): M.append({"type": "gtable", "groups": groups, "subs": subs, "rows": rows, "widths": w})
def ST(rows, w): M.append({"type": "stable", "rows": rows, "widths": w})
def PB(): M.append({"type": "pagebreak"})
def rd(p): return list(csv.DictReader(open(os.path.join(HERE, p), encoding="utf-8")))
from labels import disp_group, disp_dim, disp_comparator
def cite(ay): return re.sub(r"\s*(\d{4})", r" \1", ay.split("_")[0]).strip()  # Kohler2015_SEER18 -> Kohler 2015
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
t = open(os.path.join(HERE, "..", "SEARCH_STRINGS_v2.md"), encoding="utf-8").read()
blocks = re.findall(r"## (\d)\. ([^\n]+)\n+```\n(.*?)```", t, re.S)
meta = [("PubMed/MEDLINE", "PubMed", "1,331"), ("Embase", "embase.com (Advanced Search)", "3,248"),
        ("Scopus", "scopus.com (Advanced Search)", "2,438"), ("Web of Science", "Web of Science (Advanced)", "2,082")]
srows = [{"db": m[0], "platform": m[1], "date": "2026-08-07", "records": m[2],
          "query": [l.rstrip() for l in code.strip("\n").split("\n")]}
         for (num, title, code), m in zip(blocks, meta)]
ST(srows, [1700, 2000, 1200, 1000, 8500])
P("Note. Search conducted 7 August 2026. Concept blocks combined with AND: breast cancer × "
  "race/ethnicity × incidence/age-adjusted rate × United States. Limits: 2000–2026, English, human; "
  "document-type exclusions. Total records identified 9,099; duplicate records removed "
  "(cross-database) 4,306; unique records screened 4,793.", True)
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


# Per-study role in the synthesis (extractable? representative vs overlap), for reproducibility:
# tally, per record_id, how many analytic cells each quantitative study represents vs overlaps.
_rep = {}
for rr in rd("TableSA_main_representatives.csv"):
    rid = rr["record_id"]
    d = _rep.setdefault(rid, {"rep": 0, "ov": 0, "sel": set(), "nosel": set()})
    reason = (rr.get("representative_reason", "") or "").lower()
    ma = (rr.get("main_analysis", "") or "").lower()
    if ma.startswith("yes"):
        d["rep"] += 1
        if "sole" in reason:
            d["sel"].add("sole estimate in the cell")
        else:
            d["sel"].add("best in the cell by coverage/recency/comparator")
    else:
        d["ov"] += 1
        if "undercount" in reason or "undercount" in ma:
            d["nosel"].add("unlinked registry (AI/AN undercount) outranked by an IHS-linked source")
        elif "external" in ma or "external" in reason:
            d["nosel"].add("uses an external (out-of-paper) NHW reference")
        elif "no usable irr" in ma:
            d["nosel"].add("reports no usable rate ratio")
        elif "registry-direct" in ma:
            d["nosel"].add("registry-direct anchor, not a screened study")
        else:
            d["nosel"].add("superseded within its registry family by a broader-coverage or more-recent representative")


# Study-specific narrative reasons (why a narrative study was not quantified), from
# ft_eligibility so the reason is explicit per study rather than a blanket label.
_narr = {}
for e in rd("ft_eligibility.csv"):
    if e.get("ft_decision") == "include-narrative":
        rsn = ((e.get("ft_reason", "") or "") + " " + (e.get("note", "") or "")).lower()
        rid = e.get("record_id", "")
        if "trend" in rsn and "poolable" in rsn:
            _narr[rid] = ("Narrative only (a race–NHW breast IRR is reported, but as an annual "
                          "trend, not a single poolable estimate)")
        elif "secondary synthesis" in rsn or "not pooled to avoid" in rsn or "duplicat" in rsn:
            _narr[rid] = ("Narrative only (summary report that re-reports registry incidence already "
                          "quantified from a dedicated primary study for the same registry and period)")


def _role(r):
    g = r.get("synth_group", "")
    if g == "narrative":
        return _narr.get(r.get("record_id", ""), "Narrative only (no recoverable NHW comparison)")
    if g == "quant-eligible":
        return "Quant-eligible; no extractable data"
    c = _rep.get(r.get("record_id", ""))
    if not c:
        return "Quantitative (extractable)"
    if c["rep"]:
        s = "Representative for %d cell%s" % (c["rep"], "s" if c["rep"] > 1 else "")
        if c["sel"]:
            s += " (selected: %s)" % "; ".join(sorted(c["sel"]))
        if c["ov"]:
            s += "; overlap for %d" % c["ov"]
        return s
    s = "Overlap/sensitivity only (%d cell%s)" % (c["ov"], "s" if c["ov"] > 1 else "")
    if c["nosel"]:
        s += " — not selected: %s" % "; ".join(sorted(c["nosel"]))
    return s


_theme_ct = _C(r.get("narr_theme", "") for r in inc if r.get("synth_group") == "narrative")
rows = []
_cur = None
_curtheme = None
for r in inc:
    g = r.get("synth_group", "")
    if g != _cur:
        _cur = g
        _curtheme = None
        rows.append({"section": _SECT.get(g, g)})
    if g == "narrative":
        th = r.get("narr_theme", "") or "Other (subgroup-specific descriptive)"
        if th != _curtheme:
            _curtheme = th
            rows.append({"section": "   Theme: %s (n = %d)" % (th, _theme_ct[th])})
    rows.append([study_cell(r), r.get("study_design", ""), r.get("data_source", ""),
                 _role(r), _ident(r)])
TB(["Study (author, year)", "Study design", "Data source", "Role in synthesis", "PMID / DOI"], rows,
   [3000, 1900, 1800, 2700, 1300])
P("Note. All %d studies are included in the systematic review; not all entered the quantitative "
  "synthesis, and rows are grouped by contribution: %s Study design is classified from the data "
  "source; most are population-based registry/incidence studies rather than cohort studies. A PMID "
  "(or DOI where none exists) is given for every study so each can be located individually."
  % (_ninc, _elig_clause), True)
P("Role in synthesis records, for each study, whether quantitative data were extractable and how the "
  "study was used, with the reason it was or was not selected as a cell representative: “Representative "
  "for N cell(s)” = supplied the main-analysis benchmark for N analytic cells (group × dimension), with "
  "the selection basis in parentheses (sole estimate in the cell, or best in the cell by "
  "coverage/recency/comparator); “overlap for M” = also contributed M overlapping estimates carried only "
  "in the sensitivity re-selection; “Overlap/sensitivity only” = every estimate overlapped a cell already "
  "represented by another study, followed by why it was not selected (superseded within its registry "
  "family by a broader-coverage or more-recent representative; an unlinked registry outranked by an "
  "IHS-linked source for AI/AN; an external out-of-paper NHW reference; or no usable rate ratio); "
  "“Narrative only” = met inclusion but contributed no quantitative estimate, with the reason given per "
  "study — no recoverable NHW comparison (most), a race–NHW breast IRR reported only as an annual trend "
  "(not a single poolable estimate), or a summary report re-reporting registry incidence already "
  "quantified from a dedicated primary study for the same registry and period. One representative is "
  "selected per analytic cell (selection criteria in Methods and Supplementary Table 4).", True)
PB()

# ---- S4 excluded (no record_id) ----
H("Supplementary Table 3. Full-text exclusions with reasons", 1)
exc = rd("TableS_excluded_fulltext.csv")
rows = [[study_cell(r), r["exclusion_reason"]] for r in exc]
TB(["Study (author, year)", "Exclusion reason"], rows, [7200, 4500])
PB()

# ---- S5 registry overlap / representatives (author-year, full main_analysis) ----
H("Supplementary Table 4. Registry overlap and representative selection", 1)
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
P("Note. Each row is the single representative estimate selected for one analytic cell (group × dimension) for the main analysis: the broadest-coverage, most recent source with an appropriate population definition and standardization — a population-based benchmark, not a pooled estimate. Overlapping estimates from nested registries (county ⊂ state ⊂ SEER; SEER and NPCR feed USCS) are not independent and are retained only for the sensitivity re-selection.", True)
P("Comparator: the reference is shown as each source defined it — non-Hispanic White (NHW) where the source stratified by Hispanic origin, or “White (not NH-stratified)” otherwise (concentrated in the receptor-defined subtypes and AI/AN comparisons). The reference and minority rates come from the same source, period, and standard population, so each IRR is internally valid even where the reference is unstratified White; Supplementary Table 6c restricts to NHW-comparator estimates.", True)
P("Standard population: age-standardized to the 2000 U.S. standard unless the “Std pop” column shows otherwise. The rate ratio is formed within a study, so it does not depend on that study's choice of standard population; it does not, however, make estimates from different studies mutually comparable, because their standard populations, periods, and regions still differ.", True)
P("Main-analysis codes: “yes (representative)” = carried into the main analysis as the group's benchmark; “no (overlaps representative)” = an overlapping estimate for the same cell, used only when the representative is re-selected (Table 6); “no (AI/AN undercount)” = an unlinked-registry AI/AN estimate demoted in favour of the IHS-linked representative; “no (registry-direct anchor)” = the SEER-Explorer reference value, not a screened study; “no (external comparator)” = borrows an out-of-paper SEER-Explorer NHW rate, kept only as an overlap record; “no (no usable IRR)” = the source named the subgroup but reported no rate or ratio.", True)
PB()

# ---- S7 RoB (study = author-year; no record_id) ----
H("Supplementary Table 5. Risk of bias (JBI checklist for studies reporting prevalence/incidence data)", 1)
rob = rd("outputs/TableS_risk_of_bias.csv")
def _v(x): return {"Yes": "Y", "No": "N", "Unclear": "U", "NA": "NA"}.get(x.strip(), x.strip())
QC = ["Q1_frame", "Q2_sampling", "Q3_size", "Q4_described", "Q5_coverage",
      "Q6_condition", "Q7_measurement", "Q8_analysis"]
rrows = [[cite(r["study"])] + [_v(r[q]) for q in QC] + [r["Overall_RoB"]] for r in rob]
TB(["Study", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "RoB"],
   rrows, [3200, 620, 620, 620, 620, 620, 620, 620, 620, 1400])
P("Note. Each item is rated Y (Yes), N (No), or U (Unclear); overall risk of bias is Low, Moderate, or High. Item 9 (survey response rate) was not applicable to any study — census-like registry ascertainment has no survey response rate — so it is omitted here and the rating uses the eight applicable items (Q1–Q8).", True)
P("JBI items: Q1 sample frame appropriate to the target population (defined population-based registry); Q2 appropriate sampling (registry ascertains all diagnosed cases — census-like); Q3 adequate sample size for a stable age-adjusted rate; Q4 study subjects and setting described in detail; Q5 sufficient coverage of the identified population (registry completeness); Q6 valid identification of the condition (invasive breast cancer via registry/pathology record linkage); Q7 condition measured in a standard, reliable way for all participants, including race/ethnicity ascertainment (surname recognition or a known AI/AN undercount = No); Q8 appropriate statistical analysis (age-standardized to a stated standard population with a reported or correctly computed variance).", True)
_nlow = sum(1 for r in rob if r["Overall_RoB"] == "Low")
_nmod = sum(1 for r in rob if r["Overall_RoB"] == "Moderate")
_nhigh = sum(1 for r in rob if r["Overall_RoB"] == "High")
P("Overall risk of bias (over the eight applicable items; Q9 = NA excluded): Low = at most one item not met with the two key items (Q7 measurement, Q8 analysis) met; High = three or more items not met; Moderate otherwise. Of %d studies assessed, %d were Low, %d Moderate, and %d High; the Moderate ratings arise chiefly where an estimate was reported as a point value without a variance (Q8) or where race/ethnicity ascertainment was limited (Q7)."
  % (len(rob), _nlow, _nmod, _nhigh), True)
PB()

# ---- S10 sensitivity ----
H("Supplementary Table 6. Sensitivity analyses", 1)
from collections import Counter as _Ctr
s1 = rd("outputs/Sensitivity1_good_rob.csv"); ch1 = [r for r in s1 if r["status"] != "unchanged"]
_c1 = _Ctr(r["status"] for r in s1)
P("Table 6a. Low-risk-of-bias only (Moderate/High-RoB studies dropped): %d of %d cells unchanged, %d changed, %d dropped."
  % (_c1["unchanged"], sum(_c1.values()), _c1["changed"], _c1["dropped"]))
TB(["Dimension", "Group", "Main IRR [95% CI]", "Sens IRR [95% CI]", "Status"], [[disp_dim(r["dimension"]), disp_group(r["group"]), r["main_irr"] + r.get("main_ci", ""), (r["sens_irr"] + r.get("sens_ci", "")) if r["sens_irr"] else "-", r["status"]] for r in ch1], [1800, 2200, 3000, 3000, 900])
s2 = rd("outputs/Sensitivity2_directly_reported.csv"); ch2 = [r for r in s2 if r["status"] == "changed"]
_c2 = _Ctr(r["status"] for r in s2)
P("Table 6b. Directly-reported-only (computed estimates dropped): %d unchanged, %d changed, %d dropped — most disaggregated/subtype cells rely on computed rates (registries report rates, not ratios)."
  % (_c2["unchanged"], _c2["changed"], _c2["dropped"]))
TB(["Dimension", "Group", "Main IRR [95% CI]", "Sens IRR [95% CI]", "Status"], [[disp_dim(r["dimension"]), disp_group(r["group"]), r["main_irr"] + r.get("main_ci", ""), (r["sens_irr"] + r.get("sens_ci", "")) if r["sens_irr"] else "-", r["status"]] for r in ch2], [1800, 2200, 3000, 3000, 900])
s3 = rd("outputs/Sensitivity3_nhw_only.csv"); ch3 = [r for r in s3 if r["status"] != "unchanged"]
_c3 = _Ctr(r["status"] for r in s3)
P("Table 6c. Non-Hispanic White comparator only (unstratified-White comparators dropped): %d of %d cells unchanged, %d changed, %d dropped."
  % (_c3["unchanged"], sum(_c3.values()), _c3["changed"], _c3["dropped"]))
TB(["Dimension", "Group", "Main IRR [95% CI]", "Sens IRR [95% CI]", "Status"], [[disp_dim(r["dimension"]), disp_group(r["group"]), r["main_irr"] + r.get("main_ci", ""), (r["sens_irr"] + r.get("sens_ci", "")) if r["sens_irr"] else "-", r["status"]] for r in ch3], [1800, 2200, 3000, 3000, 900])
s4 = rd("outputs/Sensitivity4_std2000us.csv"); ch4 = [r for r in s4 if r["status"] != "unchanged"]
_c4 = _Ctr(r["status"] for r in s4)
P("Table 6d. 2000 U.S. standard population only (estimates on other standard populations dropped): %d of %d cells unchanged, %d changed, %d dropped."
  % (_c4["unchanged"], sum(_c4.values()), _c4["changed"], _c4["dropped"]))
TB(["Dimension", "Group", "Main IRR [95% CI]", "Sens IRR [95% CI]", "Status"], [[disp_dim(r["dimension"]), disp_group(r["group"]), r["main_irr"] + r.get("main_ci", ""), (r["sens_irr"] + r.get("sens_ci", "")) if r["sens_irr"] else "-", r["status"]] for r in ch4], [1800, 2200, 3000, 3000, 900])
P("Main IRR = representative estimate in the main analysis. Sens IRR = the representative re-selected after applying the sensitivity restriction (low-risk-of-bias only in Table 6a; author-reported IRR/SIR only in Table 6b; NHW-comparator only in Table 6c; 2000 U.S. standard population only in Table 6d). Status: unchanged = same study remains the representative; changed = a different study becomes the representative (its IRR is shown); dropped = no eligible estimate remained for that cell (Sens IRR = “–”). Only changed/dropped cells are listed; the remaining cells were unchanged. A “dropped” cell means no estimate met the restriction, not that the main estimate changed.", True)
PB()

# ==== NOTES (after all tables) ====
H("Supplementary Note 1. Provenance of estimates and derivation log", 1)
# map internal record_id -> readable author-year (reader-facing, like the tables)
_ay = {}
for r in csv.DictReader(open(os.path.join(HERE, "breast_extraction.csv"), encoding="utf-8")):
    if r["record_id"] != "SEER-EXPL":
        _ay.setdefault(r["record_id"], re.sub(r"\s*(\d{4})", r" \1", r["author_year"].split("_")[0]).strip())

def _rec(text):
    text = re.sub(r"rec (\d+)/(\d+)", r"rec \1, rec \2", text)      # expand rec a/b
    text = re.sub(r"rec (\d+)", lambda m: _ay.get(m.group(1), "study " + m.group(1)), text)
    return text.replace("**", "")                                   # strip markdown bold

d = open(os.path.join(HERE, "DERIVATIONS.md"), encoding="utf-8").read()
# DERIVATIONS.md is hand-wrapped markdown: a "- " item can span several physical
# lines, and "  - " marks a nested item. Join wrapped lines into one logical block
# so each list item renders as a single bullet, and render nested items as an
# indented sub-bullet — rather than prefixing every physical line with "•".
_blk = {"lines": [], "lvl": 0}


def _flush():
    if not _blk["lines"]:
        return
    text = " ".join(_blk["lines"]).strip()
    lvl = _blk["lvl"]
    _blk["lines"] = []
    _blk["lvl"] = 0
    if not text:
        return
    if lvl == 1:
        P("•  " + _rec(text), ind=360)
    elif lvl == 2:
        P("–  " + _rec(text), ind=720)
    else:
        P(_rec(text))


for raw in d.split("\n"):
    s = raw.rstrip()
    if not s.strip():
        _flush(); continue
    if s.startswith("## "):
        _flush(); H(_rec(s[3:]), 2); continue
    if s.startswith("# "):
        _flush(); continue
    stripped = s.lstrip()
    indent = len(s) - len(stripped)
    if stripped.startswith("- "):
        _flush()
        _blk["lines"] = [stripped[2:].strip()]
        _blk["lvl"] = 1 if indent == 0 else 2
    elif indent >= 2 and _blk["lines"]:
        _blk["lines"].append(stripped)          # wrapped continuation of the current item
    elif _blk["lines"] and _blk["lvl"] == 0:
        _blk["lines"].append(stripped)          # wrapped continuation of a plain paragraph
    else:
        _flush()
        _blk["lines"] = [stripped]
        _blk["lvl"] = 0
_flush()
PB()

# ---- Supplementary Note 2: screening false-negative audit ----
H("Supplementary Note 2. Screening false-negative audit", 1)
P("Purpose. The large-language-model title and abstract screening was audited for false negatives "
  "— eligible studies wrongly excluded — because the records were screened by a single reviewer with "
  "model assistance rather than by two independent reviewers.", True)
P("Method. From the records the model excluded, a random sample of 200 was drawn (Python "
  "random.seed(42)) and every title and its recorded exclusion reason was read; the 16 whose "
  "eligibility could not be settled from the title were read at the abstract level against the "
  "eligibility criteria. Because a sampled miss implies others, the full excluded set (4,551 records) "
  "was then scanned for the same signature — breast cancer, an incidence or rate term, a race or "
  "ethnicity term, and a U.S. registry or population term, minus obvious-exclusion markers (non-U.S., "
  "mortality or survival, treatment, genetic, risk-factor, male or transgender, review) — and the "
  "flagged records were reviewed against their recorded exclusion reasons, with the strongest content "
  "matches read in full.", True)
P("Result. Three wrongly excluded studies were confirmed, each a neighborhood-, segregation-, or "
  "redlining-focused report whose headline exposure is not race but which carries a secondary "
  "race-specific, age-standardized breast-incidence table: a Louisiana Tumor Registry triple-negative "
  "study (Black versus an unstratified White reference, rate ratio 2.21, 95% CI 1.96–2.48), and two "
  "Massachusetts Cancer Registry reports (Krieger 2018; Wright 2022) giving age-standardized incidence "
  "by race, from which IRRs versus NHW were computed by the delta method. All three were added to the "
  "quantitative synthesis as single-state or regional overlaps of the national representatives, and "
  "none changed a cell representative.", True)
P("Boundary cases. Not every neighborhood or socioeconomic report qualifies. A SEER "
  "inflammatory-breast-cancer study (Schairer 2012) reports incidence by race but for a morphological "
  "subtype outside the receptor-defined quantitative cells, so it was added to the narrative synthesis. "
  "Two socioeconomic-gradient studies (Akinyemiju 2015; Hernandez 2025) were confirmed correctly "
  "excluded because each reports incidence only by socioeconomic stratum — within each race, or within "
  "a single race — with no race-versus-White rate table. The recurring false-negative pattern is thus a "
  "segregation- or neighborhood-focused study that nonetheless tabulates race-specific incidence; a few "
  "more of that kind may remain, and any would be regional sensitivity overlaps that do not change a "
  "representative.", True)
P("Conclusion. The 200-record sample yielded one eligible study (about 0.5%) and the full-pool scan "
  "two more, indicating a small but non-zero residual false-negative rate. Single-reviewer screening "
  "with model assistance is a limitation, recorded in the Discussion.", True)
P("Omissions found on re-verification. Two rounds of source re-verification, which rendered the "
  "source tables of the quantitative reports as page images rather than relying on extracted text "
  "alone, also recovered extractable data missed on first pass, all among included reports: six overlapping-registry reports initially deferred were extracted into the "
  "sensitivity pool, and four reports first placed in the narrative set were moved to the quantitative "
  "synthesis after their image-only tables were read — two national USCS studies giving age-adjusted "
  "IRRs versus NHW women for ages 20–49 and 65 and older, a seven-state Delta-region study giving "
  "age-adjusted subtype IRRs versus NHW women, and a SEER study giving age-adjusted rates by race from "
  "which the NHW comparison was recomputed. All four contributed overlapping or age-specific estimates "
  "rather than displacing the national representatives.", True)
PB()

json.dump(M, open(os.path.join(OUT, "_suppl_manifest.json"), "w"), ensure_ascii=False)
from collections import Counter
print("manifest:", dict(Counter(m["type"] for m in M)),
      "| table rows:", sum(len(m["rows"]) for m in M if m["type"] == "table"))
