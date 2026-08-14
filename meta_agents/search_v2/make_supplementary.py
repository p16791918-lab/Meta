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
def PB(): M.append({"type": "pagebreak"})
def rd(p): return list(csv.DictReader(open(os.path.join(HERE, p), encoding="utf-8")))


# ---- S1 search strategy ----
H("Supplementary Table S1. Final search strategy for each database", 1)
P("Search conducted 7 August 2026. Concept blocks combined with AND: breast cancer × race/ethnicity × incidence/age-adjusted rate × United States. Limits: 2000–2026, English, human; document-type exclusions.", True)
t = open(os.path.join(HERE, "..", "SEARCH_STRINGS_v2.md"), encoding="utf-8").read()
blocks = re.findall(r"## (\d)\. ([^\n]+)\n+```\n(.*?)```", t, re.S)
meta = [("PubMed/MEDLINE", "PubMed", "1,331"), ("Embase", "Advanced Search", "3,248"),
        ("Scopus", "Advanced Search", "2,438"), ("Web of Science", "Advanced", "2,082")]
TB(["#", "Database", "Platform", "Date", "Records"],
   [[str(i + 1), m[0], m[1], "2026-08-07", m[2]] for i, m in enumerate(meta)] +
   [["", "Total identified", "", "", "9,099"], ["", "Duplicates removed", "", "", "4,306"],
    ["", "Unique screened", "", "", "4,793"]],
   [700, 3200, 3200, 2200, 1500])
for (num, title, code), m in zip(blocks, meta):
    P(f"{m[0]} — {m[1]} — {m[2]} records", True)
    CODE([l.rstrip() for l in code.strip("\n").split("\n")])
PB()

# ---- S2 PRISMA ----
H("Supplementary Figure S2. PRISMA 2020 flow diagram", 1)
IMG("Fig_PRISMA.png", 760, 640)
PB()

# ---- S3 included (author-year via citation; no record_id) ----
H("Supplementary Table S3. Characteristics of included studies (n = 163)", 1)
inc = rd("TableS_included_studies.csv")
rows = [[r["citation"][:78], r.get("data_source", "")[:28], r.get("groups_vs_nhw", "")[:26], r.get("synthesis", "")] for r in inc]
TB(["Study (author, year)", "Data source", "Groups vs NHW", "Synthesis"], rows, [5200, 2700, 2600, 1300])
PB()

# ---- S4 excluded (no record_id) ----
H("Supplementary Table S4. Full-text exclusions with reasons", 1)
exc = rd("TableS_excluded_fulltext.csv")
rows = [[r["citation"][:84], r["exclusion_reason"]] for r in exc]
TB(["Study (author, year)", "Exclusion reason"], rows, [7200, 4500])
PB()

# ---- S5 registry overlap / representatives (author-year, full main_analysis) ----
H("Supplementary Table S5. Registry overlap and representative selection", 1)
P("One representative per registry family per analytic cell for the main analysis; overlapping estimates retained for sensitivity.", True)
rep = rd("TableSA_main_representatives.csv")
rows = []
for r in rep:
    irr = r["irr"]; ci = f" [{r['irr_ci_lo']}, {r['irr_ci_hi']}]" if r['irr_ci_lo'] else ""
    rows.append([r["author_year"][:20], r["outcome_dim"][:20], r["minority_group"][:24],
                 r["registry_family"][:22], r["period"][:12], (irr + ci) if irr else "-",
                 r["main_analysis"]])
TB(["Study", "Dimension", "Group", "Registry family", "Period", "IRR [95% CI]", "Main analysis"],
   rows, [1900, 1800, 2200, 2000, 1200, 2200, 2600])
PB()

# ---- S6 provenance ----
H("Supplementary Note S6. Provenance of estimates and derivation log", 1)
d = open(os.path.join(HERE, "DERIVATIONS.md"), encoding="utf-8").read()
for line in d.split("\n"):
    line = line.rstrip()
    if not line: continue
    if line.startswith("## "): H(line[3:], 2)
    elif line.startswith("# "): pass
    elif line.startswith("- ") or line.startswith("  "): P("• " + line.strip("- ").strip())
    else: P(line)
PB()

# ---- S7 RoB (study = author-year; no record_id) ----
H("Supplementary Table S7. Risk of bias (Newcastle-Ottawa Scale, adapted)", 1)
P("Domains: Selection (max 4), Comparability (max 2), Outcome (max 3). AI-generated first pass; reviewer to spot-check.", True)
rob = rd("outputs/TableS_risk_of_bias.csv")
rows = [[r["study"][:24], r["registry"][:28], r["Selection_/4"], r["Comparability_/2"], r["Outcome_/3"], r["Overall_quality"]] for r in rob]
TB(["Study", "Registry", "Sel/4", "Comp/2", "Out/3", "Quality"], rows, [2900, 3100, 1100, 1200, 1100, 1500])
PB()

# ---- S8 GRADE ----
H("Supplementary Table S8. GRADE certainty of evidence", 1)
P("Observational bodies start Low; downgrade for RoB/inconsistency/imprecision; upgrade for large magnitude (IRR≤0.5 or ≥2.0). AI first pass.", True)
gr = rd("outputs/TableS_GRADE.csv")
rows = [[r["dimension"][:20], r["group"][:24], r["IRR"][:20], r["rob"], r["up_LargeEffect"], r["GRADE"]] for r in gr]
TB(["Dimension", "Group", "IRR [95% CI]", "RoB", "+Large", "GRADE"], rows, [2100, 2500, 2400, 1200, 1100, 1700])
PB()

# ---- S9 heterogeneity + estimator ----
H("Supplementary Table S9. Between-study heterogeneity and estimator comparison", 1)
P("Sensitivity = all overlapping estimates (Paule-Mandel + HKSJ); high I² reflects non-independent registry overlap. Main = one representative per family.", True)
si = rd("outputs/Table_sensitivity_I2.csv")
rows = [[r["dimension"][:18], r["group"][:22], r["k_all"], f"{r['sens_irr']} ({r['sens_lo']}-{r['sens_hi']})", r["I2"] + "%", (f"{r['main_irr']} ({r['main_lo']}-{r['main_hi']})" if r['main_irr'] else "-")] for r in si]
TB(["Dimension", "Group", "k", "Sensitivity IRR (95% CI)", "I²", "Main IRR (95% CI)"], rows, [1900, 2200, 700, 3000, 900, 3300])
P("Estimator comparison on the largest cell (aggregate Black, k=8): DL IRR 0.934 (τ²=0.0011, I²=98%), HKSJ 0.901–0.969; Paule-Mandel/REML IRR 0.935 (τ²=0.0018), HKSJ 0.902–0.969.")
PB()

# ---- S10 sensitivity ----
H("Supplementary Table S10. Sensitivity analyses", 1)
P("S10a. Good-RoB-only (Poor studies dropped): 82 of 90 cells unchanged, 1 changed, 7 dropped — all headline results unchanged.")
s1 = rd("outputs/Sensitivity1_good_rob.csv"); ch1 = [r for r in s1 if r["status"] != "unchanged"]
TB(["Dimension", "Group", "Main IRR", "Sens IRR", "Status"], [[r["dimension"][:20], r["group"][:24], r["main_irr"], r["sens_irr"] or "-", r["status"]] for r in ch1], [2300, 2600, 2000, 2000, 1500])
P("S10b. Directly-reported-only (computed estimates dropped): 51 unchanged, 5 changed, 34 dropped — most disaggregated/subtype cells rely on computed rates (registries report rates, not ratios).")
s2 = rd("outputs/Sensitivity2_directly_reported.csv"); ch2 = [r for r in s2 if r["status"] == "changed"]
TB(["Dimension", "Group", "Main IRR", "Sens IRR", "Status"], [[r["dimension"][:20], r["group"][:24], r["main_irr"], r["sens_irr"] or "-", r["status"]] for r in ch2], [2300, 2600, 2000, 2000, 1500])
PB()

# ---- forest figures ----
H("Supplementary Figure S11. Forest plot — disaggregated Asian/NHPI subgroups", 1)
IMG("Fig_forest_AANHPI.png", 900, 640)
H("Supplementary Figure S12. Forest plot — aggregate groups, Hispanic origin, AI/AN region, MENA", 1)
IMG("Fig_forest_overview.png", 900, 560)

json.dump(M, open(os.path.join(OUT, "_suppl_manifest.json"), "w"), ensure_ascii=False)
from collections import Counter
print("manifest:", dict(Counter(m["type"] for m in M)),
      "| table rows:", sum(len(m["rows"]) for m in M if m["type"] == "table"))
