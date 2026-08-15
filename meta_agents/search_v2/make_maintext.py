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
P("One representative estimate per group (one estimate per registry family). Effect "
  "measure is the incidence rate ratio (IRR) unless noted as a standardized incidence "
  "ratio (SIR). RoB = Newcastle-Ottawa rating of the representative study; GRADE = "
  "certainty of evidence. Full per-estimate detail is in the Supplementary Materials.", True)
# Single Table 1: analytic dimensions are full-width section rows within one table.
t1 = rd("outputs/Table1_main.csv")
TB(["Group", "Effect", "Estimate [95% CI]", "Representative study", "RoB", "GRADE"],
   [], [3200, 1100, 3000, 3400, 1400, 1300])
tbl = M[-1]
cur = None
for r in t1:
    if r["dimension"] != cur:
        cur = r["dimension"]
        tbl["rows"].append({"section": cur})
    tbl["rows"].append([disp_group(r["group"]), r["effect"], r["estimate"],
                        "%s (%s)" % (cite(r["study"]), r["period"]), r["rob"], r["grade"]])
PB()

# ==== Table 2. Aggregate meta-analysis results (k, model, IRR, I2, Q p) ====
H("Table 2. Aggregate meta-analysis of invasive breast cancer incidence by "
  "racial and ethnic group", 1)
P("Random-effects meta-analysis (Paule-Mandel/REML τ² with Hartung-Knapp-"
  "Sidik-Jonkman confidence interval); no fixed-effect model was used. k = number of "
  "estimates pooled in the all-included (sensitivity) analysis; I² and Cochran's Q "
  "p-value describe that pool. The main analysis uses one estimate per registry family "
  "to remove non-independence; the very high I² reflects overlapping registry data "
  "rather than genuine between-study heterogeneity (see Supplementary Table 8 and the "
  "GRADE framework).", True)
si = {(r["dimension"], r["group"]): r for r in rd("outputs/Table_sensitivity_I2.csv")}
order = [("aggregate-vs-NHW", "Black"), ("aggregate-vs-NHW", "Hispanic"),
         ("aggregate-vs-NHW", "Asian/PI (aggregate)"), ("aggregate-vs-NHW", "AIAN"),
         ("subtype-TNBC", "Black")]
rows = []
label = {"aggregate-vs-NHW": "Overall invasive breast cancer", "subtype-TNBC": "Triple-negative"}
for dim, grp in order:
    r = si.get((dim, grp))
    if not r:
        continue
    pooled = "%s (%s-%s)" % (r["sens_irr"], r["sens_lo"], r["sens_hi"])
    main = ("%s (%s-%s)" % (r["main_irr"], r["main_lo"], r["main_hi"])) if r["main_irr"] else "-"
    rows.append(["%s — %s" % (label[dim], disp_group(grp)), r["k_all"], "Random-effects",
                 pooled, r["I2"] + "%", r["p_Q"], main])
TB(["Comparison (vs NHW)", "k", "Model", "Pooled IRR (95% CI)", "I²", "Q p",
    "Main IRR (one-per-family)"], rows, [3400, 700, 1900, 2700, 800, 1000, 2900])
P("AIAN main analysis uses the Indian Health Service–linked (undercount-corrected) "
  "representative; the higher unlinked SEER value (0.71) appears only in the sensitivity "
  "pool. Pooled and main IRRs agree closely for all other groups.", True)
PB()

# ==== Figures ====
H("Figure 1. PRISMA 2020 flow diagram", 1)
IMG("Fig_PRISMA.png", 680, 578)
PB()
H("Figure 2. Disaggregated Asian American / Native Hawaiian and Pacific Islander "
  "subgroups versus the aggregate (IRR vs non-Hispanic White)", 1)
IMG("Fig_forest_AANHPI.png", 720, 470)
PB()
H("Figure 3. Aggregate racial and ethnic groups, Hispanic origin, American Indian / "
  "Alaska Native region, and Middle Eastern populations (IRR vs non-Hispanic White)", 1)
IMG("Fig_forest_overview.png", 720, 470)

json.dump(M, open(os.path.join(OUT, "_maintext_manifest.json"), "w"), ensure_ascii=False)
from collections import Counter
print("main-text manifest:", dict(Counter(m["type"] for m in M)))


if __name__ == "__main__":
    pass
