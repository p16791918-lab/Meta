# Feedback compliance — the governing checklist

The supervisor's feedback (Advice/Feedback) is the **grand principle**; the example
paper (Advice/Manuscript.docx + Supplementary) is the **format to mirror**. This file
tracks every feedback item and every structural element of the example against what we
have built. ✅ done · 🔧 plan fixed, executes after search · ▢ still to do.

---

## Part 1 — Feedback items (Advice/Feedback)

### 1. Whole-text revision (voice, tone, no repetition, rewrite from sources)
🔧 Planned in `MASTER_PLAN.md` (step I). Rules: "We"/passive; delete rhetorical words
("conceal", "reassuring picture dissolves", "quantitative indictment", "artefact");
soften absolutes ("every/all/no single study"); each conclusion once; **rewrite from
re-reading the source papers, not sentence edits**. → executes in the rewrite.
Not started on the manuscript itself (full rewrite comes after the search).

### 2. Literature search (4 DB, labels, Supp table, date, PROSPERO, tiab)
✅ `SEARCH_STRINGS_v2.md` (PubMed/MEDLINE, Embase, Scopus, WoS; race terms in
title/abstract; "PubMed/MEDLINE" label), `SEARCH_DAY_CHECKLIST.md`, full strings go to
**Supplementary Table 1** (platform/date/count), search date recorded on the day.
🔧 PROSPERO via `PROSPERO_AMENDMENT.md` (professor amends the 2023 record → cite CRD).

### 3. PRISMA 2020 flowchart (example + PRISMA 2020 format)
🔧 `SCREENING_PLAN.md` + `tally_prisma.py` produce the counts; two-arm PRISMA 2020 with
per-reason counts. Figure must be **redrawn to match Advice/PRISMA flowchart.pptx**
(step G) — the current fig5 is a placeholder.

### 4. Risk of bias (example tool/items/figure = NOS)
✅ `NOS_PLAN.md` — cohort NOS, example item wording + verbatim Good/Fair/Poor
thresholds, Supplementary Table 3 format + a RoB figure. AI first pass, author verifies
a subset. Poor-excluded sensitivity planned.

### 5. Overlapping registry data
✅ `REGISTRY_OVERLAP_PLAN.md` — characterization table (S-A), one-estimate-per-registry-
family primary, all-studies & overlap-excluded sensitivity, decision table (S-B) with
overlap potential / primary inclusion / selection reason.

### 6. Statistics & interpretation
✅ `STATS_PLAN.md` + code: REML + Hartung–Knapp primary, **DL-vs-REML-vs-HK comparison
table (S-C)** implemented and validated; I²≈99–100% framed as a limit with named
sources + prediction interval; effect-source distinction (directly/rate-derived/figure/
approx) → sensitivity S-1; comparability check (same standard pop/period/comparator).
🔧 Wording fixes (no "artefact"; no genetic-ancestry causation) → in the rewrite.

### 7. Manuscript structure
🔧 Title → shortened professor version; Intro/Methods/Results/Discussion restructured to
the example (see Part 2); each argument once; **terminology unified** — canonical label
set + handling rule in `EXTRACTION_MANUAL.md` (✅ that rule is fixed). Structure executes
in the rewrite.

### 총평 (overall: remove AI-tells; summarize sources in own words; 8-item summary)
🔧 The rewrite is from re-reading sources; the 8-item self-summary (research
question/objectives, databases/strategy, in/exclusion, PRISMA method, RoB method,
overlap handling, statistics, Results/Discussion structure) is the pre-writing step.

---

## Part 2 — Example-paper format to mirror (Advice/Manuscript.docx)

| Example element | Our status |
|---|---|
| **Short title** | ▢ add (e.g., "Breast Cancer Incidence Disparities in the US") |
| **Corresponding authors** | 🔧 placeholders pending approval (2 corresponding professors) |
| **Abstract** | 🔧 rewrite (≤ journal limit, structured) |
| **Systematic review registration: CRD…** | 🔧 add the CRD line once PROSPERO is amended |
| **Introduction** | 🔧 background → gap → aim, concise |
| **Methods → Protocol registration, Search Strategy, Eligibility** | 🔧 regroup to this heading |
| **Methods → Study Selection and Data Extraction** | 🔧 regroup; from `SCREENING_PLAN`/`EXTRACTION_MANUAL` |
| **Methods → Statistical Analysis and Data Harmonization** | 🔧 from `STATS_PLAN` (REML+HK, S-C, overlap) |
| **Results → Selection and Characteristics of Included Studies** | 🔧 PRISMA + characteristics table |
| **Results → [outcome subsections]** | 🔧 neutral headers (aggregate; disaggregated subgroups; subtype; age) — drop rhetorical headers |
| **Results → Publication Bias, Risk of Bias, Certainty (Evidence Class)** | 🔧 combine NOS + GRADE + small-study into one subsection |
| **Discussion** | 🔧 main findings → prior work → explanations → implications → strengths/limitations |
| **Conclusion** (separate) | ▢ add as its own section |
| **Abbreviations** | ▢ add |
| **Declarations →** COI · Data Access · Data Sharing · **Author Contributions** · **Declaration on the Use of Generative AI** | 🔧 expand to these sub-parts (example wording for the AI declaration) |
| **Supporting Information** (Supp Tables 1–3 + Supp Figures) | 🔧 S1 search · S2 exclusion reasons · S3 NOS · S-A/S-B overlap · S-C methods · forest/LOO/sensitivity figures |
| **References** | ✅ `REFERENCES.md` order-of-appearance (re-run after search) |
| **Figure legends** (separate section) | ▢ add |
| **Table 1. Summary of associations** | 🔧 build a summary-of-findings Table 1 like the example |

### Supplementary structure (Advice/Supplementary Materials.docx) → our mapping
- Supp Table 1 = search strategy per database (platform/date/count) ✅ ready
- Supp Table 2 = reasons for exclusion ✅ `SCREENING_PLAN.md` categories
- Supp Table 3 = NOS ✅ `NOS_PLAN.md`
- + Table S-A / S-B (registry overlap), Table S-C (method comparison), forest /
  leave-one-out / poor-excluded sensitivity figures.

---

## Bottom line
Every feedback item is captured and every example element is mapped. What is **done** is
the **methodology/rules + statistics code**; what is **pending** is the **manuscript
rewrite (I)** and three **figures/tables that need the final study set** (PRISMA figure,
characteristics table, Table 1). Nothing in the feedback is currently unaddressed.
`MASTER_PLAN.md` sequences the execution; this file is the compliance record to check
each artifact against before submission.
