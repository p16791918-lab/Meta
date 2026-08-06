# Statistical analysis plan (supervisor feedback item 6)

Feedback item 6 asks for four things, not just a change of estimator:
(1) **compare** the heterogeneity method against alternatives rather than asserting
robustness; (2) interpret the very high I² as a *limit on the pooled estimate*, with
named sources; (3) **distinguish** how each effect size was obtained (directly
reported vs rate-derived vs figure-extracted vs approximated SE); (4) confirm
studies share a standard population / period / comparator before computing rate
ratios. This file fixes the analysis so all four are addressed.

---

## 1. Heterogeneity-method comparison (the "compare, don't assert" requirement)

Do **not** run one estimator and claim the result is unaffected. Report the pooled
within-study log-IRR under several estimator × CI-method combinations, side by side,
and state whether the point estimate and CI **materially change**.

**Supplementary Table S-C — method-comparison (per pooled outcome):**

| Model | τ² estimator | CI / test method | Pooled IRR (95% CI) | τ² | I² | 95% prediction interval |
|---|---|---|---|---|---|---|
| **Primary** | REML | **Hartung–Knapp** | … | … | … | … |
| REML (Wald) | REML | z (Wald) | … | … | … | … |
| DerSimonian–Laird | DL | z (Wald) | … | … | … | … |
| Paule–Mandel *(optional)* | PM | z (Wald) | … | … | … | … |

- **Primary model = REML + Hartung–Knapp** (more conservative CI under few/hetero-
  geneous studies). DL is reported *for comparison*, because the earlier draft used
  DL — this directly answers "DL를 REML/HK와 비교하지 않고 단정하지 말 것."
- In the text: report that the direction/magnitude is (un)changed across methods, and
  where HK **widens** the CI, say so — do not claim "no effect on conclusions" without
  showing this table.
- Run the same comparison for every pooled estimate (overall and each subgroup pool).

## 2. Interpreting I² ≈ 99–100% (feedback line 40)

- State **first** that near-total heterogeneity **limits interpretation of any single
  pooled estimate**; the pooled IRR is descriptive, not a precise common effect.
- Then attribute heterogeneity to concrete sources: **registry family, region,
  diagnosis period, age-standardization/standard population, and race/ethnicity
  subgroup** — the same axes that motivate the one-estimate-per-registry-family
  primary analysis and the subgroup analyses. Report τ² and a **95% prediction
  interval** alongside I², since a PI conveys the spread better than I² alone.
- Do **not** call heterogeneity "not a statistical weakness / not noise" (the earlier
  draft's phrasing).

## 3. Distinguish how each effect size was obtained (feedback line 42)

Every effect entering the synthesis is tagged (already a column in Table S-A):
`directly-reported IRR/RR (95% CI given)` · `rate-derived IRR (two age-adjusted
rates divided)` · `figure-extracted` · `approximated SE`.

- **Sensitivity analysis S-1:** restrict to **directly reported** IRR/RR only (drop
  rate-derived, figure-extracted, approximated) and compare with the primary pool.
- For rate-derived IRRs, the SE is propagated from both rates' CIs
  (`se_logirr_from_rate_cis`); state this in Methods rather than treating it as a
  reported SE.
- Flag figure-extracted values (e.g., DeSantis Figure 1) explicitly in the forest
  plot / table footnote.

## 4. Comparability check before computing a rate ratio (feedback line 43)

Before dividing two age-adjusted rates into an IRR, confirm the minority and NHW
rates share:
- the **same standard population** (e.g., 2000 US standard) — record it in Table S-A;
- an **overlapping diagnosis period**;
- the **same comparator definition** (non-Hispanic White, not "White" including
  Hispanic — reconcile terminology per feedback item 7, line 58).

If a study mixes standard populations or comparator definitions, note it and, where
it matters, exclude that rate ratio in a sensitivity check rather than silently
pooling it.

## 5. Wording constraints tied to the stats (feedback lines 44–45) — for the rewrite

- Do **not** describe age-standardization itself as an "artefact." Say instead that a
  single age-standardized summary **may not capture age-specific differences**;
  present age-band-specific rate ratios where studies report them.
- Do **not** link observed racial/ethnic differences to genetic ancestry or a specific
  biological mechanism. Restrict such content to **possible explanations / hypotheses**
  not directly assessed by the included studies.

---

## Software note
Whichever tool is chosen (pending decision: Python / R `metafor` / Stata), the
method-comparison table above is the deliverable. `metafor::rma()` makes it one line
per row (`method="REML"/"DL"/"PM"`, `test="knha"/"z"`), which is why it is the
recommended engine; Python results can be cross-checked against it.
