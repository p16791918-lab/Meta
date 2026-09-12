# Risk of bias — Newcastle–Ottawa Scale (supervisor feedback #4)

Risk of bias of the included observational studies is assessed with the
**Newcastle–Ottawa Scale (NOS)**, following the format of the example paper
(Advice/Risk of bias, search strategy 참고.docx, Supplementary Table 3): three
domains (**Selection / Comparability / Outcome**), a star system, and the standard
Good / Fair / Poor thresholds quoted verbatim below.

## Which scale applies (answer to "both scales?")
The example uses **two** NOS variants because it included both cohort and
case–control studies. Our included studies are **population-based cancer-registry
incidence studies**, which map to the **cohort NOS**. So:
- **Primary: the cohort NOS is applied to every included study** (all are
  population-based registry/incidence designs).
- The **case–control NOS** is kept defined here only as a fallback: if screening
  turns up a genuine case–control design, that study is scored on the case–control
  scale instead. We expect this not to occur.
- Each study's table row records which scale was used.

Maximum stars (cohort NOS): **Selection ★★★★ · Comparability ★★ · Outcome ★★★**
(9 total).

---

## Cohort NOS — operationalized for registry incidence-by-race studies
"Exposed cohort" = a racial/ethnic **minority** group; "non-exposed cohort" = the
**non-Hispanic White (NHW)** reference group; "outcome" = incident invasive breast
cancer.

### Selection (max ★★★★)
| # | NOS item (example wording) | ★ awarded when (our operationalization) |
|---|---|---|
| S1 | **Representativeness of the exposed cohort** — truly/somewhat representative of the average population in the community | Minority group drawn from a **population-based cancer registry** (SEER, NAACCR, USCS, or a state/regional registry) covering a defined population. **✗** if single-institution, clinic, or convenience sample. |
| S2 | **Selection of the non-exposed cohort** — drawn from the same community as the exposed cohort | NHW comparator drawn from the **same registry/population and period** as the minority group. **✗** if the reference rate comes from a different source/population. |
| S3 | **Ascertainment of exposure** (race/ethnicity) — secure records or structured classification | Race/ethnicity from **self-identification or the registry's standard NAACCR/SEER coding**. **✗** if surrogate only (surname/geocoding) or high missingness/imputation without validation. |
| S4 | **Outcome not present at start of study** | Cases are **incident** (first primary) invasive breast cancers, as registries capture new diagnoses. **✗** if prevalent/mixed cases or unclear. |

### Comparability (max ★★) — of the exposed vs non-exposed cohort on design/analysis
| ★ | ★ awarded when |
|---|---|
| ★ (1st) | Rates are **age-standardized** (age-adjusted to a standard population, e.g., 2000 US standard) — controls for age, the most important confounder. |
| ★★ (2nd) | **Additionally** either (i) both groups use the **same standard population, diagnosis period, and registry** (internally comparable rate ratio), **or** (ii) the study adjusts for/stratifies by a further key factor (e.g., stage, SES, nativity). |

*(Pre-specifying the 2nd star this way keeps scoring consistent across reviewers.)*

### Outcome (max ★★★)
| # | NOS item (example wording) | ★ awarded when |
|---|---|---|
| O1 | **Assessment of outcome** — independent blind assessment or record linkage | Outcome ascertained by **population-based cancer-registry linkage** (pathologically confirmed incident cancer). **✗** if self-report/unverified. |
| O2 | **Follow-up long enough for outcomes to occur** | A **defined diagnosis/observation period** sufficient for stable rates (e.g., ≥1 full registry year or a multi-year window). **✗** if a very short/partial period. |
| O3 | **Adequacy of follow-up** | Registry **case completeness** high (e.g., SEER/NAACCR completeness standards, typically ≥95%) or completeness reported/described. **✗** if completeness poor or unreported with concern. |

---

## Quality thresholds (quoted from the example, AHRQ standard)
- **Good quality:** 3 or 4 ★ in **Selection** AND 1 or 2 ★ in **Comparability** AND
  2 or 3 ★ in **Outcome**.
- **Fair quality:** 2 ★ in **Selection** AND 1 or 2 ★ in **Comparability** AND
  2 or 3 ★ in **Outcome**.
- **Poor quality:** 0 or 1 ★ in **Selection** OR 0 ★ in **Comparability** OR
  0 or 1 ★ in **Outcome**.

## Case–control NOS (fallback only — kept for completeness)
If a case–control study is included, score it on the case–control scale instead:
Selection (case definition adequate · representativeness of cases · selection of
controls · definition of controls), Comparability (as above), Exposure
(ascertainment of exposure · same method for cases and controls · non-response
rate). Same Good/Fair/Poor thresholds (Outcome→Exposure domain).

---

## Reporting (Supplementary Table 3, example format)
One row per study; a star (★) in each earned cell:

| Study (author, year) | Scale | S1 | S2 | S3 | S4 | Comparability | O1 | O2 | O3 | Total ★ | Quality |
|---|---|---|---|---|---|---|---|---|---|---|---|

Plus a NOS traffic-light / summary figure mirroring the example's risk-of-bias
figure.

## Process (feedback #4, line 25)
AI performs the **first-pass** NOS coding from each study's full text; the author
then **verifies a subset** (a few studies across the quality range) against the
source to confirm the coding, and spot-checks any borderline Good/Fair/Poor calls.
Scoring rules above are fixed **before** assessment so ratings are reproducible.
A **sensitivity analysis excluding "Poor"-quality studies** is reported (as in the
example paper).
