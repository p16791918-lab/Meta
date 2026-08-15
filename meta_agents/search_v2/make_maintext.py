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
P("Primary result = the main-analysis IRR, a single representative estimate per "
  "registry family (no pooling, so no k / I² / heterogeneity test apply to it). The "
  "sensitivity analysis pools every overlapping registry estimate for the cell with a "
  "random-effects model (Paule-Mandel/REML τ², Hartung-Knapp-Sidik-Jonkman CI); the "
  "No. of estimates, I², and Cochran's Q p-value below describe THAT pool. Because those "
  "estimates repeatedly include the same nested registries (SEER ⊂ NAACCR ⊂ USCS), they "
  "are not independent — hence the very high I² / small Q p is a non-independence artifact, "
  "not genuine between-study heterogeneity (Supplementary Table 8; GRADE framework, "
  "Table 6). Concordance of the two columns indicates the direction is robust.", True)
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
    main = ("%s (%s-%s)" % (r["main_irr"], r["main_lo"], r["main_hi"])) if r["main_irr"] else "-"
    pooled = "%s (%s-%s)" % (r["sens_irr"], r["sens_lo"], r["sens_hi"])
    rows.append(["%s — %s" % (label[dim], disp_group(grp)), main, pooled,
                 r["k_all"], "Random-effects", r["I2"] + "%", r["p_Q"]])
TB(["Comparison (vs NHW)", "Main IRR (95% CI)\n[primary, one-per-family]",
    "Sensitivity IRR (95% CI)\n[all overlapping]", "No. of estimates", "Model", "I²", "Q p"],
   rows, [2900, 2500, 2500, 1200, 1500, 700, 900])
P("AIAN main analysis uses the Indian Health Service–linked (undercount-corrected) "
  "representative; the higher unlinked SEER value (0.71) enters only the sensitivity pool. "
  "Main and sensitivity estimates agree closely in direction for all groups. No. of "
  "estimates / I² / Q p are properties of the sensitivity pool only.", True)
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
