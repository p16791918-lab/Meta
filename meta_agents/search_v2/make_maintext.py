#!/usr/bin/env python3
"""Assemble the MAIN-TEXT tables/figures manifest (outputs/_maintext_manifest.json),
rendered to Word by build_maintext_docx.js. Per MANUSCRIPT_VS_SUPPLE.md the main
text is lean: Table 1 (summary IRRs by group x dimension), Table 2 (aggregate
meta-analysis with k / model / pooled IRR / I2 / Cochran's Q p), and the key
figures (PRISMA + the two representative forests). Everything granular stays in
the Supplementary."""
import csv, json, os, re
from collections import defaultdict, OrderedDict
from labels import disp_group

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
M = []


def H(t, l=1): M.append({"type": "heading", "text": t, "level": l})
def P(t, it=False): M.append({"type": "para", "text": t, "italic": it})
def TB(h, rows, w): M.append({"type": "table", "headers": h, "rows": rows, "widths": w})
def IMG(p, w, h): M.append({"type": "image", "path": os.path.join(OUT, p), "w": w, "h": h})
def PB(): M.append({"type": "pagebreak"})
def rd(p): return list(csv.DictReader(open(os.path.join(HERE, p), encoding="utf-8")))
def cite(ay):  # "Gopalani2020_31764279" -> "Gopalani 2020"; "Ellington2022_USCS" -> "Ellington 2022"
    return re.sub(r"(\d{4})", r" \1", ay.split("_")[0]).strip()


# ==== Table 1. Summary of IRRs by racial/ethnic group and analytic dimension ====
H("Table 1. Incidence rate ratios of invasive breast cancer among U.S. racial and "
  "ethnic groups relative to non-Hispanic White women, by analytic dimension", 1)
P("Each value is a representative population-based estimate (a contemporary benchmark) for the "
  "group — the most recent, broadest-coverage registry estimate with an appropriate population "
  "definition and standardization — not a meta-analytic pooled estimate; one estimate is shown "
  "per registry family. Effect "
  "measure is the incidence rate ratio (IRR) unless noted as a standardized incidence "
  "ratio (SIR). Comparisons are versus non-Hispanic White (NHW) women, except where "
  "marked † — the reference in that study was an unstratified White group (not stratified "
  "by Hispanic origin), which may raise the IRR slightly; these estimates are examined in "
  "the NHW-comparator sensitivity analysis (Supplementary Table 6c). Black denotes "
  "non-Hispanic Black (NHB), and the Asian/Pacific Islander aggregate is labeled AANHPI "
  "(Asian American, Native Hawaiian, and Pacific Islander), with the Pacific-Islander "
  "subset shown separately as NHPI. RoB = risk-of-bias rating of the representative "
  "study. Full per-estimate detail, including each study's comparator and standard "
  "population, is in the Supplementary Materials.", True)
# Single Table 1: analytic dimensions are full-width section rows within one table.
t1 = rd("outputs/Table1_main.csv")
TB(["Group", "Effect", "Estimate [95% CI]", "Representative study", "Registry family",
    "RoB"], [], [3050, 1000, 2850, 2650, 2250, 1300])
tbl = M[-1]
cur = None
for r in t1:
    if r["dimension"] != cur:
        cur = r["dimension"]
        tbl["rows"].append({"section": cur})
    tbl["rows"].append([disp_group(r["group"]), r["effect"], r["estimate"],
                        "%s (%s)" % (cite(r["study"]), r["period"]),
                        r.get("registry", ""), r["rob"]])
PB()

# NOTE: no "meta-analysis results" table. Estimates within a group come from
# overlapping registry populations and are not independent, so they were not pooled;
# the analysis reports a representative population-based (benchmark) estimate per
# group (Table 1) and the robustness of that selection (Supplementary Table 6).

# ==== Figures ====
H("Figure 1. PRISMA 2020 flow diagram", 1)
IMG("Fig_PRISMA.png", 680, 578)
PB()
H("Figure 2. Disaggregated Asian American / Native Hawaiian and Pacific Islander "
  "subgroups versus the aggregate (IRR vs non-Hispanic White)", 1)
IMG("Fig_forest_AANHPI.png", 720, 490)
PB()
H("Figure 3. Aggregate racial and ethnic groups, Hispanic origin, American Indian / "
  "Alaska Native region, and Middle Eastern populations (IRR vs non-Hispanic White)", 1)
IMG("Fig_forest_overview.png", 720, 470)
PB()
H("Figure 4. Incidence rate ratio by racial or ethnic group and analytic dimension "
  "(representative estimate vs non-Hispanic White; 1.0 = the NHW rate)", 1)
IMG("Fig_heatmap.png", 760, 429)

json.dump(M, open(os.path.join(OUT, "_maintext_manifest.json"), "w"), ensure_ascii=False)
from collections import Counter
print("main-text manifest:", dict(Counter(m["type"] for m in M)))


if __name__ == "__main__":
    pass
