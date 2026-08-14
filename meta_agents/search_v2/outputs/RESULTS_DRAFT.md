# Results (objective draft — numbers only, for the manuscript)

> Draft of the Results section giving the observed values only, in neutral
> voice. Interpretation belongs in the Discussion. Figures referenced here
> (forest plots) are generated from `Table_main_forest.csv`.

## 1. Study selection (PRISMA 2020)

A systematic search of four databases on 7 August 2026 identified 9,099 records:
PubMed/MEDLINE (n=1,331), Embase (Advanced Search; n=3,248), Scopus (n=2,438),
and Web of Science Core Collection (n=2,082). After removal of 4,306 cross-database
duplicates, 4,793 unique records remained. Title/abstract screening excluded 4,551
records and identified 242 reports for full-text retrieval. Full-text assessment of
the 242 reports excluded 79 and retained 163 studies: 48 provided age-adjusted
invasive female breast-cancer incidence data by race/ethnicity that were eligible
for quantitative synthesis, and 115 contributed to the narrative synthesis only.
Numerical estimates were extracted from 43 of the 48 quantitative-eligible studies;
for the remaining 5, the required rate table could not be obtained, and each of
these overlapped a study already represented for the same analytic cell.

## 2. Study characteristics

The 43 quantitative studies drew on U.S. population-based cancer registries: SEER,
NAACCR/CiNA, USCS (NPCR+SEER), state registries (California, Florida, New Mexico,
Hawaii), Indian Health Service (IHS)-linked and tribal registries (PRCDA counties,
Navajo Nation, Alaska Native Tumour Registry), and California Cancer Registry
sub-registries (Greater Bay Area, Los Angeles County). Diagnosis periods spanned
1988–2023.

Provenance of the 144 extracted estimates was recorded and distinguished (Feedback
item 6): 73 were reported directly by the source study (61 as an incidence rate
ratio, 2 as a standardized incidence ratio, 10 as a race-specific rate), and 71
were computed from published race-specific rates (32 with a confidence interval
propagated from reported rate CIs, 10 with a Poisson standard error derived from
case counts, and 29 as a point estimate only). Age-standardization and derivation
of every computed value are documented in `DERIVATIONS.md`. A confidence interval
usable for variance-weighting was available for 103 of the 144 estimates.

## 3. Risk of bias

Risk of bias was assessed with the Newcastle-Ottawa Scale adapted for
population-based incidence studies (Selection, Comparability, Outcome domains;
Table S, `TableS_risk_of_bias.csv`). Of the 43 studies, 35 were rated Good and 8
Poor; among the 28 studies contributing a main-analysis representative, 24 were
Good and 4 Poor. The Poor ratings arose where only a point estimate without a
confidence interval could be obtained for the relevant group.

## 4. Registry overlap and the primary analysis

Because SEER, NAACCR, and USCS are nested and share cases, overlapping estimates
for the same analytic cell were not treated as independent. One representative was
retained per registry family for each outcome dimension × racial/ethnic group,
selected by coverage, most recent/longest diagnosis period, and clearest
standardization/confidence interval (Table SA). All estimates were retained in a
sensitivity analysis.

Pooling overlapping estimates produced very high between-study heterogeneity
(I² = 98–100% for the aggregate Black, Hispanic, Asian/Pacific Islander, and
American Indian/Alaska Native cells; Table, `Table_sensitivity_I2.csv`). This
value reflects repeated inclusion of overlapping registry data rather than
biological heterogeneity, and the pooled aggregate estimates are therefore
reported with that limitation. On the largest overlapping cell (aggregate Black,
k=8), the DerSimonian–Laird and Paule–Mandel/REML estimators gave τ² = 0.0011 and
0.0018 and pooled IRR = 0.934 and 0.935; the Hartung–Knapp–Sidik–Jonkman interval
(0.902–0.969) was wider than the z-based interval (0.907–0.963)
(`Table_method_comparison.md`).

## 5. Incidence rate ratios versus non-Hispanic White women

### Aggregate racial/ethnic groups (representative estimates)
- American Indian/Alaska Native: IRR 0.56 (0.55–0.57) [IHS-linked; period 1999–2015]
- Hispanic/Latina: IRR 0.72 (0.71–0.73)
- Asian/Pacific Islander (aggregate): IRR 0.77 (0.75–0.79)
- Black/African American: IRR 0.93 (0.92–0.95)

### Disaggregated Asian American, Native Hawaiian and Pacific Islander subgroups
Representative IRRs ranged from 0.16 to 1.21 across subgroups:
Hmong 0.16 (0.12–0.22), Cambodian 0.26 (0.20–0.34), Laotian/Kampuchean 0.39
(0.35–0.43), Vietnamese 0.58 (0.56–0.61), Korean 0.67 (0.65–0.70),
Guamanian/Chamorro/Samoan 0.72 (0.64–0.81), Chinese 0.76 (0.74–0.77), Filipina
0.85 (0.84–0.87), Asian Indian/Pakistani 0.95 (0.93–0.97), Japanese 1.04
(1.00–1.08), Native Hawaiian/Pacific Islander (aggregate) 1.21 (1.16–1.25), and
Native Hawaiian 1.21 (1.12–1.31). The aggregate Asian/Pacific Islander estimate
(0.77) fell within this range.

### Hispanic subgroups by origin (single study, Florida, 1999–2001)
Mexican 0.50 (0.38–0.67), New Latino 0.68 (0.62–0.76), Cuban 0.76 (0.68–0.84),
Puerto Rican 0.82 (0.73–0.92).

### American Indian/Alaska Native by region/tribe
Navajo 0.49 (0.44–0.55); IHS-PRCDA Southern Plains 1.25 (1.11–1.41) and Northern
Plains 1.33 (1.26–1.41) (provisional regional estimates). The Alaska Native
estimate was 1.09 (0.99–1.21) from the directly-reported source.

### Middle Eastern (California, 1988–2004)
Middle Eastern women: IRR 0.86 (0.84–0.88).

### Molecular subtypes (representative estimates)
- Triple-negative: Black 1.95 (1.93–1.98); Hispanic 0.86 (0.84–0.88);
  Asian/Pacific Islander 0.70 (0.68–0.72); American Indian/Alaska Native
  (from the USCS TNBC source).
- HR+/HER2− and other subtypes by race and by Asian subgroup are tabulated in
  `Table_main_forest.csv`.

### Male breast cancer
Black men versus White men: IRR 1.52 (1.44–1.60).

## 6. Sensitivity analysis

Restricting each cell to its one-per-registry-family representative changed the
aggregate point estimates only slightly relative to the all-included pooled values
(e.g., Black 0.933 vs 0.935; Hispanic 0.718 vs 0.734; Asian/PI 0.769 vs 0.795;
AI/AN 0.560 vs 0.693) while removing the non-independence that inflated I²
(`Table_sensitivity_I2.csv`). The larger shift for AI/AN reflects the difference
between IHS-linked and unlinked national registries for that group.
