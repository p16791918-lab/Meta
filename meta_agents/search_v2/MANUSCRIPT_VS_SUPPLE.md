# Main manuscript vs Supplementary — content classification

Mirrors the example paper's split: the main text carries a small number of
summary/results tables and the key figure(s); everything granular
(search, study lists, per-item RoB, GRADE workings, provenance, detailed
forests) lives in the Supplementary. Numbering restarts in each document
(Table 1…, Figure 1…, S Table 1…, S Figure 1…).

## MAIN MANUSCRIPT (to be written)

**Text:** Abstract (Background / Objectives / Methods / Results / Discussion /
Registration / Keywords) → Introduction → Methods → Results → Discussion →
Conclusion → References.

| Item | Content | Source artifact | Mirrors example |
|---|---|---|---|
| **Figure 1** | PRISMA 2020 flow diagram (two-arm) | `Fig_PRISMA.png` | (primary-SR standard; example used a PPTX flow) |
| **Figure 2** | Forest — disaggregated Asian/NHPI subgroups vs the aggregate (the headline finding) | `Fig_forest_AANHPI.png` | Fig 1 (harvest) role |
| **Figure 3** | Forest — aggregate groups, Hispanic origin, AI/AN region, MENA | `Fig_forest_overview.png` | — |
| **Table 1** | Headline IRR by racial/ethnic group × analytic dimension, with representative study, RoB, GRADE | `Table1_main.csv/md` | Table 1 (summary of associations) |
| **Table 2** | Aggregate meta-analysis results: **k · Model (random-effects) · pooled IRR [95% CI] · I² (%) · Cochran's Q p** (+ one-per-family main IRR) | `Table_sensitivity_I2.csv` (aggregate rows) | Table 2 (No. of results / Effect estimate / I²) |

Methods must state: random-effects only (Paule-Mandel/REML τ², Hartung-Knapp
CI); Cochran's Q / I² for heterogeneity; one-estimate-per-registry-family main
analysis with all-included and directly-reported sensitivity analyses; NOS RoB;
GRADE-informed certainty; single-reviewer-with-AI screening; why no funnel plot
(k<10, non-independent census data).

## SUPPLEMENTARY (current single `Supplementary_Materials.docx`)

| Item | Content | Status |
|---|---|---|
| **S Table 1** | Final search strategy per database (platform, date, n, full query) | built |
| **S Table 2** | Characteristics of included studies (n = 163) | built |
| **S Table 3** | Full-text exclusions with reasons (n = 79) | built |
| **S Table 4** | Registry overlap & representative selection (one-per-family + reason) | built |
| **S Table 5** | Risk of bias — Newcastle-Ottawa per-item star grid | built |
| **S Table 6** | Certainty framework — GRADE-informed scoring (Criteria / Descriptions) | built |
| **S Table 7** | GRADE certainty by outcome | built |
| **S Table 8** | Between-study heterogeneity (k, model, I², Q p) + DL vs PM/REML vs HKSJ estimator comparison | built |
| **S Table 9** | Sensitivity analyses (9a good-RoB-only; 9b directly-reported-only) | built |
| **S Note 1** | Provenance of estimates & derivation log | built |
| **S Figure 1** | Pooled forest — aggregate racial/ethnic groups (all-included, RE diamond + weights) | built (`Fig_pool_aggregate.png`) |
| **S Figure 2** | Pooled forest — triple-negative breast cancer | built (`Fig_pool_tnbc.png`) |
| **S Figure 3** | Pooled forest — disaggregated subgroups with ≥2 studies | built (`Fig_pool_disaggregated.png`) |

## Notes on the split
- **Figures moving to main text** (PRISMA, the two representative forests) come
  out of the Supplementary figure section, which then holds only the three
  **pooled** forests (renumbered S Figure 1–3).
- **Table 2 (main)** is the aggregate subset of S Table 8; S Table 8 keeps the
  full per-cell heterogeneity + estimator detail.
- Everything in the Supplementary is generated from `breast_extraction.csv`
  via the pipeline, so the split is a rendering/placement decision, not a
  re-analysis.
