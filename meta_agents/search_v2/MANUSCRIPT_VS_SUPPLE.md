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

**No meta-analysis results table anywhere.** The main analysis selects one
representative per registry family — it does not pool — so no pooled IRR, k, I², or
Cochran's Q p is presented as a result. A naive pool of the all-included
overlapping estimates was examined only as an internal consistency check (its
I² ≈ 99–100% reflects the non-independence of overlapping registry data, which is
exactly why the review does not pool); it is not shown as a finding, per the
round-2 feedback.

Methods state: no pooled random-effects primary estimate; a
one-representative-per-registry-family main analysis with low-risk-of-bias,
directly-reported, and NHW-comparator re-selection sensitivity analyses; JBI risk
of bias (GRADE and Newcastle–Ottawa dropped in round 2); certainty of evidence not
graded; single-reviewer-with-AI screening.

## SUPPLEMENTARY (current single `Supplementary_Materials.docx`)

| Item | Content | Basis (Feedback / reference) |
|---|---|---|
| **S Table 1** | Final search strategy per database (platform, date, n, full query) | Feedback #2 |
| **S Table 2** | Characteristics of included studies (n = 162; study-design column) | Feedback 2nd-#4 |
| **S Table 3** | Full-text exclusions with reasons | round-1 #2 |
| **S Table 4** | Registry overlap & representative selection (one-per-family + reason) | Feedback #5 |
| **S Table 5** | Risk of bias — JBI checklist per item (Q1–Q9, overall) | Feedback 2nd-#2 |
| **S Table 6** | Sensitivity analyses (6a low-RoB; 6b directly-reported; 6c NHW-comparator) | Feedback #5 |
| **S Note 1** | Provenance of estimates & derivation log (directly-reported vs computed-from-rates vs Poisson-SE) | Feedback #6/#7 (distinguish IRR types) |

There are **no GRADE tables and no pooled forest figures** — both were removed in
round 2. The three key figures (PRISMA, aggregate-to-disaggregated forest,
group × dimension heatmap) live in the **main text**, not the Supplementary.

## Notes on the split
- **Supplementary:** search strategy, reasons for exclusion, the registry/
  representative table (Feedback #5), JBI risk of bias, the re-selection
  sensitivity analyses, and the provenance/derivation log.
- **Main text is deliberately lean:** Table 1 (summary IRRs by group × dimension)
  plus Figure 1 (PRISMA), Figure 2 (aggregate-to-disaggregated forest), and
  Figure 3 (group × dimension heatmap). There is no main-text Table 2.
- Everything is generated from `breast_extraction.csv` via the pipeline, so the
  split is a rendering/placement decision, not a re-analysis.
