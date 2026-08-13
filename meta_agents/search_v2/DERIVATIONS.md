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
- **rec 49 (Mills 2005, Hmong-California).** Hmong female breast AAIR 23.8 (39
  cases) vs NHW 145.5; only the Hmong case count (39) is available, so SE(logIRR)
  = 1/sqrt(39) = 0.160 with the large NHW denominator treated as fixed
  (1/D_nhw ~ 0). IRR 0.164 (0.120-0.224). Period mismatch (Hmong 1988-2000 vs
  NHW 1995-1999) flagged in-row. Lowest AANHPI subgroup.
- **rec 3267 (Kem 2007, Cambodian CA+PugetSound).** Author-reported Cambodian/
  White ratio 0.26 (uses the surname-method "high rate" 41.0 / NHW 155.5); the
  high/low rate bracket 34.8-41.0 is an ethnic-identification uncertainty range,
  NOT a 95% CI, so SE(logIRR) = 1/sqrt(58) = 0.131 from the 58 Cambodian cases.
  IRR 0.264 (0.204-0.341).

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
- **rec 51 (ANTR 2021, Alaska Native).** Paper is ANTR-only (Alaska Native
  people), no in-paper NHW. AN female breast 130.8 (116.7-146.0), 2014-2018,
  2000 US std. Paired with SEER-Explorer NHW observed annual mean for the SAME
  window (2014-2018 = 137.4, 2000 US std). IRR 0.952 (0.851-1.065). NOTE: this
  overlaps rec 28 (Nash 2019, same ANTR registry, 2009-2014) which reports a
  DIRECTLY-reported IRR 1.09 (0.99-1.21) vs in-paper US White; rec 28 is the
  cell representative, rec 51 is a sensitivity/overlap estimate (its 0.95 vs
  rec 28's 1.09 reflects the different period and the external NHW denominator).

## 4b. IRR CI from reported standard errors of rates
- **rec 4333 (Wilkinson 2002, Miami-Dade Hispanic).** Table 1 gives invasive
  breast rates with SEs: Hispanic 81.9 (SE 1.2), NHW 125.8 (SE 2.0), 1990-1998.
  IRR = 81.9/125.8 = 0.651; SE(log rate) = SE_rate/rate; SE(logIRR) =
  sqrt((1.2/81.9)^2 + (2.0/125.8)^2) = 0.0216 -> IRR 0.651 (0.624-0.679).
  Regional aggregate Hispanic (Cuban-heavy), collapses with rec 3298 aggregate
  Hispanic (sensitivity/overlap).

## 5b. Author-reported rate ratios taken as directly reported
- **rec 587 (Nasseri 2009, Middle Eastern-California).** Authors print the rate
  ratio and its CI: invasive breast 0.86 (126.2/146.9, 95% CI 0.84-0.88); taken
  as `directly-reported-IRR`. Standard not stated but NHW=146.9 implies 2000 US.
  New MENA analytic cell.
- **rec 955 (Goggins 2009, Asian Indian/Pakistani).** Table 1 prints the female
  breast SIR relative to US White = 0.61 (0.56-0.66); `directly-reported-SIR`.
  Overlaps rec 234 Asian Indian/Pakistani (sensitivity). CONTAMINATION NOTE: the
  uploaded 461.pdf is byte-for-byte this Goggins paper (mis-named); the SIR was
  attributed to its correct record (955), NOT to rec 461 (Northern Plains AI/AN),
  whose correct full text is still unavailable (deferred).

## Contamination / mis-classification catches (this extraction pass)
- **rec 1336** flattened numbers looked like subtype IRRs but rendering showed
  they are mortality HAZARD RATIOS (Cox models) — demoted (not incidence).
- **rec 2548 (Hmong-Minnesota)** comparator is "All Minnesotans"/API (total
  population, both sexes), not NHW women — demoted (incomparable; the clean
  Hmong-vs-NHW female estimate comes from rec 49 instead).
- **rec 461/955 PDF mis-filing** resolved as above.

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
