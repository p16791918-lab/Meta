# Main manuscript vs Supplementary — content classification

Placement follows two professor references plus the Feedback:
- **Manuscript.docx** (mobile-phone umbrella review) — main text = a summary
  figure + summary/results tables (No. of results / Effect estimate / I²).
- **"Risk of bias, search strategy 참고.docx"** (maternal-smoking meta-analysis)
  — explicitly puts Search strategy, Reasons for exclusion, Newcastle-Ottawa
  RoB, and ALL forest plots + leave-one-out in the **Supplementary**.
- **Feedback** — full search string → Supplementary Table (#2); registry
  overlap / representative selection → Supplementary Table (#5); RoB → follow
  the reference format (#4); IRR-provenance distinction → present separately (#6).

So the main text stays lean (summary + aggregate results table + PRISMA, and
optionally the one headline forest); everything granular is Supplementary.
Numbering restarts in each document (Table 1…, Figure 1…, S Table 1…, S Figure 1…).

## MAIN MANUSCRIPT (to be written)

**Text:** Abstract (Background / Objectives / Methods / Results / Discussion /
Registration / Keywords) → Introduction → Methods → Results → Discussion →
Conclusion → References.

| Item | Content | Source artifact | Basis |
|---|---|---|---|
| **Table 1** | Headline IRR by racial/ethnic group × analytic dimension (one unified table, dimensions as section rows), with representative study and RoB | `Table1_main.csv/md` | Manuscript Table 1 (summary of associations) |
| **Figure 1** | PRISMA 2020 flow diagram (two-arm) | `Fig_PRISMA.png` | primary-SR standard (Feedback #3) |
| **Figure 2** | Aggregate-to-disaggregated heterogeneity forest — AANHPI, Hispanic/Latina, and AI/AN, each an aggregate estimate with its subgroups and 95% CIs | `Fig_forest_main.png` | Feedback #11 (visual synthesis of heterogeneity) |
| **Figure 3** | Heatmap — IRR by racial/ethnic group × analytic dimension (overall, age, receptor subtypes, TNBC) | `Fig_heatmap.png` | Feedback #11 (pattern shifts by dimension) |

**No main-text "meta-analysis results" (k / I² / Q p) table.** The main analysis
selects one representative per registry family — it does not pool — so k, I², and
Cochran's Q p apply only to the all-included *sensitivity* pool, which lives in
**Supplementary Table 8** with the pooled forests (S Figures 1–3). Putting a
pooled table in the main text would misrepresent the non-pooling main analysis.

Methods must state: random-effects only (Paule-Mandel/REML τ², Hartung-Knapp
CI); Cochran's Q / I² for heterogeneity; one-estimate-per-registry-family main
analysis with all-included and directly-reported sensitivity analyses; NOS RoB;
GRADE-informed certainty; single-reviewer-with-AI screening; why no funnel plot
(k<10, non-independent census data).

## SUPPLEMENTARY (current single `Supplementary_Materials.docx`)

| Item | Content | Basis (Feedback / reference) |
|---|---|---|
| **S Table 1** | Final search strategy per database (platform, date, n, full query) | Feedback #2 + RoB-ref S Table 1 |
| **S Table 2** | Characteristics of included studies (n = 163) | Manuscript supp (characteristics) |
| **S Table 3** | Full-text exclusions with reasons (n = 79) | RoB-ref S Table 2 (Reasons for exclusion) |
| **S Table 4** | Registry overlap & representative selection (one-per-family + reason) | Feedback #5 |
| **S Table 5** | Risk of bias — Newcastle-Ottawa per-item star grid | Feedback #4 + RoB-ref S Table 3 |
| **S Table 6** | Certainty framework — GRADE-informed scoring (Criteria / Descriptions) | Manuscript supp (GRADE framework) |
| **S Table 7** | GRADE certainty by outcome | GRADE synthesis |
| **S Table 8** | Between-study heterogeneity (k, model, I², Q p) + DL vs PM/REML vs HKSJ estimator comparison | Feedback #6 (estimator comparison) |
| **S Table 9** | Sensitivity analyses (9a good-RoB-only; 9b directly-reported-only) | Feedback #5 (sensitivity) |
| **S Note 1** | Provenance of estimates & derivation log (directly-reported vs computed-from-rates vs Poisson-SE) | Feedback #6 (distinguish IRR types) |
| **S Figure 1** | Forest — aggregate groups, Hispanic origin, AI/AN region, MENA | RoB-ref keeps forests in Supplementary |
| **S Figure 2** | Pooled forest — aggregate racial/ethnic groups (all-included, RE diamond + weights) | RoB-ref (forest + sensitivity in supp) |
| **S Figure 3** | Pooled forest — triple-negative breast cancer | " |
| **S Figure 4** | Pooled forest — disaggregated subgroups with ≥2 studies | " |

*(If the headline disaggregated forest `Fig_forest_AANHPI` is NOT promoted to
main Figure 2, it becomes S Figure 1 and the others shift down.)*

## Notes on the split
- **Confirmed Supplementary by Feedback + the RoB reference:** search strategy,
  reasons for exclusion, Newcastle-Ottawa RoB, registry/representative table,
  estimator comparison, sensitivity, provenance — and, per the RoB reference,
  the **forest plots** as well.
- **Main text is deliberately lean:** the summary IRR table (Table 1), the
  aggregate meta-analysis results table with k/model/I²/Q p (Table 2), and the
  PRISMA diagram (Figure 1). Promoting the single headline forest to main
  Figure 2 is optional — the RoB reference would keep it in the Supplementary.
- **Table 2 (main)** is the aggregate subset of S Table 8; S Table 8 keeps the
  full per-cell heterogeneity + estimator detail.
- Everything is generated from `breast_extraction.csv` via the pipeline, so the
  split is a rendering/placement decision, not a re-analysis.
