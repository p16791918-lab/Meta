#!/usr/bin/env python3
"""Assemble the MAIN-TEXT tables/figures manifest (outputs/_maintext_manifest.json),
rendered to Word by build_maintext_docx.js. Per MANUSCRIPT_VS_SUPPLE.md the main
text is lean: Table 1 (summary IRRs by group x dimension) and the key figures
(Figure 1 PRISMA; Figure 2 the aggregate-to-disaggregated heterogeneity forest;
Figure 3 the group x analytic-dimension heatmap). There is no pooled
meta-analysis table in the main text — the analysis selects one representative
per cell rather than pooling. Everything granular stays in the Supplementary."""
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


def IMG_FIT(p, max_w, max_h):
    """Embed a figure at its own aspect ratio, scaled to fit inside max_w x max_h
    (pixels at 96 dpi). The box is the narrower of the Letter and A4 printable
    areas less the heading and the Note, so the page fits either paper size. Reading the size from the file keeps a regenerated figure from being
    stretched, and keeps a tall figure from running off the bottom of the page in
    the PDF conversion."""
    from PIL import Image
    fp = os.path.join(OUT, p)
    iw, ih = Image.open(fp).size
    s = min(max_w / iw, max_h / ih)
    IMG(p, int(round(iw * s)), int(round(ih * s)))
def PB(): M.append({"type": "pagebreak"})
def rd(p): return list(csv.DictReader(open(os.path.join(HERE, p), encoding="utf-8")))
def cite(ay):  # "Gopalani2020_31764279" -> "Gopalani 2020"; "Ellington2022_USCS" -> "Ellington 2022"
    return re.sub(r"(\d{4})", r" \1", ay.split("_")[0]).strip()


# ==== Table 1. Summary of IRRs by racial/ethnic group and analytic dimension ====
H("Table 1. Incidence rate ratios of invasive breast cancer among U.S. racial and "
  "ethnic groups relative to non-Hispanic White women, by analytic dimension", 1)
# Single Table 1: analytic dimensions are full-width section rows within one table.
t1 = rd("outputs/Table1_main.csv")
# No "Effect" column: every representative is an incidence rate ratio, so the
# column carried one value in all 38 rows. The two SIRs are overlaps and appear
# in Supplementary Table 4, not here.
TB(["Group", "Estimate [95% CI]", "Representative study", "Registry family",
    "RoB"], [], [3250, 3000, 2800, 2400, 1600])
tbl = M[-1]
cur = None
for r in t1:
    if r["dimension"] != cur:
        cur = r["dimension"]
        tbl["rows"].append({"section": cur})
    tbl["rows"].append([disp_group(r["group"]), r["estimate"],
                        "%s%s (%s)" % (cite(r["study"]), r.get("ref", ""), r["period"]),
                        r.get("registry", ""), r["rob"]])
# Note placed below the table (analysis method, comparator, symbols, abbreviations only).
P("Note. This table shows 38 of the 85 analytic cells, those covering the principal comparisons; "
  "the rest, chiefly the other receptor-defined subtypes and the age-specific comparisons, are in "
  "Supplementary Table 4. Each cell shows one representative population-based estimate — the most recent, "
  "broadest-coverage registry estimate per analytic cell — not a pooled estimate; the "
  "selection rule and its robustness are given in the Methods and Supplementary Table 6. "
  "Each representative study is followed by its number in the reference list. "
  "The effect measure is the incidence rate ratio (IRR) throughout; comparisons are versus "
  "non-Hispanic White (NHW) women. "
  "† the study's reference was an unstratified White group (not stratified by Hispanic "
  "origin), examined in the NHW-comparator sensitivity analysis (Supplementary Table 6c); "
  "5 of the 19 cells so marked appear in this table. "
  "‡ the 95% confidence interval was computed by the reviewers from published rates rather "
  "than reported in the source. NHB, non-Hispanic Black; AANHPI, Asian American, Native "
  "Hawaiian, and Pacific Islander (NHPI, the Pacific Islander subset, shown separately); "
  "RoB, risk-of-bias rating of the representative study. Full per-estimate detail is in the "
  "Supplementary Materials.", True)
PB()

# NOTE: no "meta-analysis results" table. Estimates within a group come from
# overlapping registry populations and are not independent, so they were not pooled;
# the analysis reports a representative population-based (benchmark) estimate per
# group (Table 1) and the robustness of that selection (Supplementary Table 6).

# ==== Figures ====
H("Figure 1. PRISMA 2020 flow diagram", 1)
IMG_FIT("Fig_PRISMA.png", 634, 780)
PB()
H("Figure 2. Aggregate-to-disaggregated heterogeneity in breast cancer incidence "
  "(representative IRR vs non-Hispanic White, 95% CI): the Asian American, Native Hawaiian "
  "and Pacific Islander (AANHPI), Hispanic/Latina, and American Indian and Alaska Native "
  "(AI/AN) aggregates, each shown with its subgroups", 1)
IMG_FIT("Fig_forest_main.png", 634, 720)
P("Note. Each point is the representative estimate for one analytic cell, drawn from a separate "
  "study; an aggregate and its subgroups differ in registry, region, diagnosis period, and "
  "standard population. Diamonds mark aggregate groups, circles subgroups. A solid bar is a 95% "
  "CI reported in the source; a dashed bar marked ‡ is one computed for this review; a point "
  "without a bar had no interval in its source. † reference was an unstratified White group, not "
  "NHW. Values match Table 1.", True)
PB()
H("Figure 3. Incidence rate ratio by racial or ethnic group and analytic dimension "
  "(representative estimate vs non-Hispanic White; 1.0 = the NHW rate)", 1)
IMG_FIT("Fig_heatmap.png", 634, 780)

json.dump(M, open(os.path.join(OUT, "_maintext_manifest.json"), "w"), ensure_ascii=False)
from collections import Counter
print("main-text manifest:", dict(Counter(m["type"] for m in M)))


if __name__ == "__main__":
    pass
