# Derivations log — values not directly reported by the source

Transparency record. Every estimate whose IRR was **not printed as-is by the study** is listed here
with how it was derived, so each is reproducible. Estimates reported by the source as a ratio
(`directly-reported-IRR` / `-SIR`) are taken verbatim and are not in this log.

## 1. Age-standardization from age-specific rates
- **rec 2 (Suppl Table 3).** The supplement reports 5-year
  age-specific incidence rates (ages 20–85+) by race × subtype, not a single
  age-adjusted rate. Each race's 14 age-specific rates were standardized to
  the **2000 US standard population** (Census P25-1130 weights for the 20–85+
  groups): std_rate = Σ(rate_i·w_i)/Σw_i. IRR = minority_std / NHW_std.
  - Alignment verified against printed anchors (HR+/HER2− NHW 45–49 = 128.2,
    75–79 = 342.7; TNBC NHW 35–39 = 9.7).
  - **95% CIs computed by variance propagation.** Suppl Table 3 reports a 95% CI
    for every age-specific rate. SE per band =
    (hi−lo)/(2·1.96); Var(std_rate) = Σ(w_i/Σw)²·SE_i²; SE(logIRR) =
    √[(SE_min/std_min)² + (SE_nhw/std_nhw)²]. Provenance =
    `computed-from-rates-with-CI` (e.g., TNBC Black 1.82 [1.70, 1.95],
    HR+/HER2− AANHPI 0.69 [0.66, 0.72]).
  - IRR is invariant to the 20+ vs all-age standard (ages 0–19 contribute ≈0 to
    both numerator and denominator).

## 2. IRR computed from race-specific rates ± CIs
IRR = minority_rate / NHW_rate. With both rate CIs: SE(logIRR) =
sqrt(SE_min² + SE_nhw²), SE(log rate) = (ln hi − ln lo)/(2·1.96); provenance
`computed-from-rates-with-CI`. Rate without CI → point IRR only; provenance
`computed-from-rates` (or `directly-reported-rate` where the source printed the rate).
The records in each class:
- **with CI:** rec 10, rec 200, rec 265, rec 333, rec 346, rec 522, rec 2131, rec 3398, rec 4040.
- **point only (no CI):** rec 100, rec 381, rec 463, rec 485, rec 500, rec 4098.
- Handled in other sections: §1 (rec 2), §4 (rec 234, rec 3182, rec 51), §4b (rec 4333), and the Poisson-SE records in §3.
- **rec 10** rates use the **Segi world 1960** standard (ages 20–74), not 2000 US
  — the IRR remains comparable (a ratio); the absolute scale differs (flagged in-row).
- **rec 265/346** use "White"/"Black" not NH-stratified (rec 346 White incl.
  Hispanic); rec 265 is the crossover from printed age-specific rates.
- **rec 500** NHW (130.4) is from the same paper (Gopalani 2020), not external.

## 3. Poisson SE from case counts
Where a study reports rates and annual case counts but no ratio CI, SE(logIRR) =
sqrt(1/D_min + 1/D_nhw) (D = cases); provenance `computed-from-rates-Poisson-SE`.
- **rec 169 (USCS).** Aggregate age-adjusted rates for women aged ≥20
  (USCS, ~99% coverage): Black 174.0, Hispanic 134.0, Asian/PI 143.5, AI/AN 127.3, vs
  NHW 186.5; the paper reports rates, not ratios. IRR = minority / 186.5, with the CI
  from the annual case counts (e.g., Black 0.933 [0.920, 0.946], Hispanic 0.718
  [0.707, 0.731]). This supplies three of the four aggregate overall estimates.
- **rec 203, rec 182.** Rates with case counts but no
  ratio CI; SE(logIRR) from the counts as above.
- **rec 49 (Hmong-California).** Hmong female breast AAIR 23.8 (39
  cases) vs NHW 145.5; only the Hmong case count (39) is available, so SE(logIRR)
  = 1/sqrt(39) = 0.160 with the large NHW denominator treated as fixed
  (1/D_nhw ~ 0). IRR 0.164 (0.120-0.224). Period mismatch (Hmong 1988-2000 vs
  NHW 1995-1999) flagged in-row.
- **rec 3267 (Cambodian CA+PugetSound).** Author-reported Cambodian/
  White ratio 0.26 (surname-method "high rate" 41.0 / NHW 155.5); the
  high/low rate bracket 34.8-41.0 is an ethnic-identification uncertainty range,
  not a 95% CI, so SE(logIRR) = 1/sqrt(58) = 0.131 from the 58 Cambodian cases.
  IRR 0.264 (0.204-0.341).

## 4. External NHW comparator (study reports minority only)
- **rec 234.** Disaggregated AANHPI rates are in the main Table
  (2018–2022, SEER-21); the **in-paper NHW comparator is eTable 3** (Supplement 1):
  Non-Hispanic White 139.5 (139.0–140.0), same registry (SEER-21), same period
  (2018–2022), same standard (2000 US). IRRs = subgroup rate / 139.5 with 95% CIs
  propagated from both rate CIs.
- **rec 3182.** Table 4 gives origin-specific female-breast rates with 95% CIs
  (Cuban 108.0, Mexican 71.9, New Latino 97.8, Puerto Rican 116.9), and the
  non-Hispanic White Florida comparator is reported in Table 2: 140.4 (137.6–143.2),
  same registry (Florida, 1999–2001), same standard (2000 US). IRR = origin rate /
  140.4, with the 95% CI propagated from both rate CIs by the delta method (e.g.,
  Cuban 0.769 [0.688, 0.860]). These reproduce the authors' printed rounded rate
  ratios (0.8/0.5/0.7/0.8).
- **rec 51 (Alaska Native).** Paper is ANTR-only (Alaska Native
  people), no in-paper NHW. AN female breast 130.8 (116.7-146.0), 2014-2018,
  2000 US std. Paired with the SEER-Explorer NHW observed annual mean for the SAME
  window (2014-2018 = 137.4, 2000 US std). IRR 0.952 (0.851-1.065). This
  overlaps rec 28 (same ANTR registry, 2009-2014), which reports a
  directly-reported IRR 1.09 (0.99-1.21) vs an in-paper US White reference; rec 28 is the
  cell representative and rec 51 is a sensitivity/overlap estimate (the 0.95 vs
  1.09 difference reflects the different period and the external NHW denominator).

## 4b. IRR CI from reported standard errors of rates
- **rec 4333 (Miami-Dade Hispanic).** Table 1 gives invasive
  breast rates with SEs: Hispanic 81.9 (SE 1.2), NHW 125.8 (SE 2.0), 1990-1998.
  IRR = 81.9/125.8 = 0.651; SE(log rate) = SE_rate/rate; SE(logIRR) =
  sqrt((1.2/81.9)^2 + (2.0/125.8)^2) = 0.0216 → IRR 0.651 (0.624-0.679).
  Regional aggregate Hispanic (Cuban-heavy); collapses with rec 3298 aggregate
  Hispanic (sensitivity/overlap).

## 5. Author-reported rate ratios taken as directly reported
- **rec 587 (Middle Eastern-California).** The authors print the rate
  ratio and its CI: invasive breast 0.86 (126.2/146.9, 95% CI 0.84-0.88); taken
  as `directly-reported-IRR`. Standard not stated but NHW=146.9 implies 2000 US.
- **rec 955 (Asian Indian/Pakistani).** Table 1 prints the female
  breast SIR relative to US White = 0.61 (0.56-0.66); `directly-reported-SIR`.
  Overlaps rec 234 Asian Indian/Pakistani (sensitivity).

## 6. Direction conversion
- **rec 286.** Subtype IRRs are printed minority-vs-NHW (verified from
  "In [minority]… higher/lower than NHW") and taken as-is. The overall Black
  statement is printed NHW-vs-Black (1.04); it would invert to 0.96 but was left
  unrecorded as ambiguous.

## 7. Overlap studies entered for the sensitivity analysis (not representatives)
These six were read from full text and enter the ledger only as
overlap/sensitivity rows; each collapses to an existing cell representative
(finalize_representatives), so none changes a main-text estimate.
- **rec 236 (Gomez 2010, California Cancer Registry, 1988-2004).** Table 1
  prints age-standardized (2000 US) invasive breast rates: NHW 146.1
  (145.5-146.7); Chinese 73.5 (71.6-75.4), Japanese 102.5 (99.3-105.9), Filipina
  100.4 (98.1-102.8), Korean 46.3 (43.8-49.0), Vietnamese 59.9 (56.7-63.1). IRR =
  rate/146.1 with delta-method CI (e.g. Chinese 0.503, 0.490-0.516). State
  registry (< national SEER-21); overlaps the SEER-21 subgroup reps (rec 234).
- **rec 4027 (Jin 2016, eight-state SEER+NPCR, 2009-2011).** Table 4 (female)
  prints breast rates with CIs: NHW 134.4 (133.8-135.1); Chinese 82.8, Filipina
  111.3, Japanese 127.8, Korean 75.6, South Asian [=Asian Indian/Pakistani]
  106.3, Vietnamese 72.2, Asian aggregate 94.5. IRR = rate/134.4, delta-method
  CI. Eight-state subset (< national SEER-21); overlaps rec 234.
- **rec 461 (Watanabe-Galloway 2015, NE/ND/SD state registries, 2002-2009).**
  Table 2 prints all-ages age-standardized (2000 US) breast rates: AI/AN 134.6,
  NHW 149.3, RR 0.9. IRR = 134.6/149.3 = 0.902. Unlinked state registries
  undercount AI/AN, so this is demoted by the AI/AN-undercount rule below the
  IHS-linked Northern-Plains representative (rec 3662).
- **rec 2137 (Melkonian 2022, urban IHS-linked USCS-AIAD, 2008-2017).** Table 2
  prints all-ages breast rates for urban populations: AI/AN 74.2, NHW 129.6, RR
  0.57. IRR = 74.2/129.6 = 0.573. Urban-restricted IHS subset (< full PRCDA);
  overlaps the AI/AN aggregate representative (rec 500).
- **rec 419 (Amirikia 2011, California Cancer Registry, 1988-2006).** Table 2
  prints age-specific triple-negative rates by race (0-39, 40-49, 50-59, 60-74,
  >=75). These were age-standardized by the review to all ages with 2000 US
  standard-population weights (0.5697/0.1540/0.1112/0.1048/0.0603): NHB 23.6, NHW
  12.6, Hispanic 10.2 per 100,000. IRR(Black)=1.87, IRR(Hispanic)=0.81.
  California registry (< national USCS); overlaps the USCS TNBC rep (rec 155).
- **rec 209 (Zhang 2022, NPCR+SEER/USCS, 2019).** The text (Figure 2A) prints the
  2019 age-adjusted triple-negative rates by race: NHB 25.0, NHW 12.8, Hispanic
  11.5, AI/AN 9.4, AANHPI 9.5 per 100,000. IRR = rate/12.8 (NHB 1.95, Hispanic 0.90,
  AI/AN 0.73, AANHPI 0.74). Single-year 2019 cross-section; overlaps the USCS TNBC
  representative (rec 155, 2015-2019 mean), which is preferred on the longer span.
