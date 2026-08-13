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
IRR = minority_rate / NHW_rate. With both rate CIs: SE(logIRR) =
sqrt(SE_min² + SE_nhw²), SE(log rate) = (ln hi − ln lo)/(2·1.96); provenance
`computed-from-rates-with-CI`. Rate without CI → point IRR only; provenance
`computed-from-rates`. Complete lists (auto-generated from the ledger):
- **with CI:** rec 10, rec 234, rec 522, rec 2131, rec 3182, rec 3398, rec 4040.
- **point only (no CI):** rec 2, rec 100, rec 265, rec 333, rec 346, rec 381,
  rec 463, rec 485, rec 500, rec 4098.
- Elaborated elsewhere: rec 2 (§1), rec 234 & rec 3182 (§4).
- **rec 10** rates use the **Segi world 1960** standard (ages 20–74), not 2000 US
  — IRR still comparable (ratio), absolute scale differs (flagged in-row).
- **rec 265/346** use "White"/"Black" not NH-stratified (rec 346 White incl.
  Hispanic); rec 265 is the crossover from printed age-specific rates, no ratio CI.
- **rec 500** NHW (130.4) is from the same paper (Gopalani 2020), not external.

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
