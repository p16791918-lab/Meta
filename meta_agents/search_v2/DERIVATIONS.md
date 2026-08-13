# Derivations log — values NOT directly reported by the source

Transparency record (for the Methods / Supplementary). Every estimate in
`breast_extraction.csv` whose IRR was **not printed as-is by the study** is
listed here with exactly how it was derived, so each is reproducible and
auditable. Rows whose `provenance` is `directly-reported-IRR` / `-SIR` are
taken verbatim from the paper and are NOT in this log.

## 1. Age-standardization from age-specific rates
- **rec 2 (Kohler 2015, Suppl Table 3).** The supplement reports 5-year
  age-specific incidence rates (ages 20–85+) by race × subtype, not a single
  age-adjusted rate. We age-standardized each race's 14 age-specific rates to
  the **2000 US standard population** (Census P25-1130 weights for the 20–85+
  groups): std_rate = Σ(rate_i·w_i)/Σw_i. IRR = minority_std / NHW_std.
  - Alignment verified against printed anchors (HR+/HER2− NHW 45–49 = 128.2,
    75–79 = 342.7; TNBC NHW 35–39 = 9.7).
  - **Point estimates only — no CI** (a proper CI needs age-specific variance
    propagation, not attempted). Provenance = `computed-from-rates`.
  - IRR is invariant to the 20+ vs all-age standard (ages 0–19 contribute ≈0 to
    both numerator and denominator).

## 2. IRR computed from race-specific rates ± CIs
- **rec 4098, 463, 100, 381, 485, 333, 522, 4040, 3398, 3182, 3662** and the
  SEER-Explorer anchor: IRR = minority_rate / NHW_rate. Where both rates carry a
  95% CI, SE(logIRR) = sqrt(SE_min² + SE_nhw²) with SE(log rate) =
  (ln hi − ln lo)/(2·1.96); provenance `computed-from-rates-with-CI`. Where a
  rate lacks a CI, point IRR only; provenance `computed-from-rates`.

## 3. Poisson SE from case counts
- **rec 203, 182.** No ratio CI printed but case counts are. SE(logIRR) =
  sqrt(1/D_min + 1/D_nhw) (D = cases); provenance `computed-from-rates-Poisson-SE`.

## 4. External NHW comparator (study reports minority only)
- **rec 234 (Sung 2026).** Reports disaggregated AANHPI rates but no numeric NHW.
  Paired with the **SEER-Explorer** NHW female-breast rate, same submission
  (Nov 2025), same registry set (SEER-21), same standard (2000 US), same
  period-window handling (non-delay-adjusted, 2018–2022 mean = 140.3). Documented;
  the 2019–2023 pooled value (141.3) agrees as a sensitivity check.
- **rec 3182 (Pinheiro 2009).** Table gives origin rates + rounded IR ratios but
  not the NHW-FL rate; NHW-FL ≈ 143 (2000 US std) was back-derived so computed
  IRRs reproduce the authors' rounded ratios (0.8/0.5/0.8/0.7) — flagged to
  refine if the exact NHW is obtained.

## 5. Direction conversion
- **rec 286 (Kong 2020).** Subtype IRRs are printed minority-vs-NHW (verified from
  "In [minority]… higher/lower than NHW") → taken as-is. The overall Black
  statement is printed NHW-vs-Black (1.04) → would invert to 0.96; left unrecorded
  as ambiguous.

## Open item
- CIs are missing for the rec 2 age-standardized IRRs and for a few rate-only
  rows (rec 4098, 100, 381). These enter the MAIN forest as point estimates and
  the sensitivity/precision-weighted pooling notes this. If exact CIs or case
  counts are later obtained, upgrade provenance and add CIs.
