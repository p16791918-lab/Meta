# Breast-cancer incidence extraction log

Method A (within-study IRR = minority age-adjusted rate / NHW rate). Rates are
age-standardized invasive breast-cancer incidence per 100,000. Data go into
`run_meta_analysis_breast.py :: STUDIES`. Primary outcome = overall invasive
incidence; TNBC is a separate subtype stratum.

## ⚠️ Data-integrity caveat

Auto-fetched `fulltext/*.txt` are **not reliable** (md5-identical duplicates +
some unique-but-mismapped files, e.g. 34508608.txt, 35025856.txt). Extract only
from (1) manually-downloaded PDFs, or (2) a `.txt` whose opening content is
verified to match the study's title. Corrupted `.txt` removed in commit d4fc595.
Screening impact of this bug is still to be assessed (publication-grade: plan =
re-verify includes [ongoing] + fix fetch + sample-check Phase-2 exclusions).

## Per-study status

| Study | Source | Status |
|---|---|---|
| 41082230 Ghanaian/US Black | txt (verified) | ✅ EXTRACTED — Black vs NHW (SEER) |
| T_e7879b363303 TNBC trends | PDF (full paper) | ✅ EXTRACTED — Black vs White (TNBC stratum) |
| 39822259 England 329,500 | PDF | ⏳ values pulled; **UK study** — pending US-only vs international decision |
| 33392441 ER status, 6 Asian ethnicities + NHW | PDF | ⏳ has NHW + Asian subgroups; rates are trend figures — need table values |
| T_101456b59470 South Asian California | PDF | ⏳ compares SA vs Asian/PI (+ colon cancer) — verify a NHW breast reference exists |
| 11562110 SES California | PDF (text ok) | ⏳ 181k chars, not yet mined |
| 12115511 Asian-American rising | PDF (SCANNED, no text) | ❗ needs image OCR / Read-tool |
| T_5b207ea405f3 young adults | PDF = ASCO abstract | ❌ EXCLUDED (conference abstract) |
| T_223de2a7d421 | PDF = Value in Health/ISPOR page | ❌ EXCLUDED (off-topic / wrong document) |
| 34508608, 35025856, 36504334, 34861613, 30503975, 40701557, 38426333, 20147696 | needs PDF | ⏳ user downloading (8) |
| 40736150 Persistent Poverty CA | txt (verified) | ⏳ shows all-cancer rates; need breast-specific-by-race |

## Extracted so far (in STUDIES)

**41082230** — SEER 17, 2013–2015, age-std Segi world, women 20–74 (Table 2):
NHB 148.5 (146.4–150.7); NHW 152.9 (151.9–153.8) → Black vs NHW IRR 0.971.
Ghana/GBHS 84.4 excluded (foreign population).

**T_e7879b363303 (TNBC)** — age-adjusted TNBC per 100,000: Black 33.8, White 17.5,
Hispanic 14.7, AIAN 14.7, Asian ~12. Black vs White TNBC **IRR 1.93 (1.88–1.97)**.
(Hispanic/Asian/AIAN vs White IRRs available in the paper — CIs still to pull.)

## Data-inclusion framework (DECIDED)

Hybrid (Cochrane-style). "Strict" means *extract the comparable number from each
study*, not drop studies:
- **Primary pool**: whole-age (or widest adult age) age-adjusted invasive
  incidence, aggregate race categories (Black / Hispanic / Asian / AIAN vs NHW),
  US population registries. Pull each study's most comparable rate.
- **Secondary / sensitivity / subgroup**: age-restricted (e.g. <50), Asian
  ethnic subgroups (Japanese/Filipino/Chinese…), single-state (Hawaii, CA),
  international (England). Not dropped — moved to their own strata.
- Random-effects (DL) handles residual heterogeneity.
- Sparse comparisons (e.g. AIAN — few source studies) are reported as such, not
  forced.

Extraction tooling confirmed working in this env: pdfplumber (tables) and
pypdfium2 page-render → Read (figures).

## 36504334 (Hawaii) — read (age<50 panel, 2010–2014 AAIR /100k)
Japanese American 52.0 (45.6–58.9); NHW 39.8 (34.8–45.1); Native Hawaiian
33.2 (28.7–38.1); Filipino 31.7 (27.4–36.4). → SECONDARY (Hawaii, age<50,
Asian subgroups). All-ages aggregate (Table 2) still to pull if present.

## Open decisions (for "publication-grade" discussion)
- **US-only vs international?** 39822259 is England (UK ethnic categories:
  white / Black African / Black Caribbean / South Asian). Mixing with US
  SEER/NHW is a comparability/heterogeneity call — likely a separate stratum or
  sensitivity analysis, or exclude if US-only.
- Several "included" records are turning out to be **conference abstracts**
  (young-adults ASCO, T_223 ISPOR) → excluded. Expect to find more once the 8
  PDFs arrive; each gets verified on read.

## Next
- Mine 11562110 (text) and 33392441 (Asian subgroups) for table rates.
- OCR/Read 12115511 (scanned).
- Verify T_101456b59470 has a NHW breast reference.
- Extract the 8 incoming PDFs.
- Need ≥2 studies per comparison before any forest plot renders.


## Progress update (extraction ongoing)
Pooled so far (random-effects):
- **Black vs NHW = 0.952 (0.915-0.990)**, p=0.014 — 41082230 + MMWR
- **Asian vs NHW = 0.714 (0.616-0.827)**, p<0.001 — MMWR(A/PI) + Gomez 20147696
- Hispanic vs NHW: MMWR only (need 2nd) ; AIAN vs NHW: MMWR only (need 2nd)
- TNBC Black vs White: T_e7879b363303 (1)

Gomez 20147696 (CA CR 1988-2004, Table 2, age-adj 2000 std): NHW 145.6
(144.6-146.7); US-born Asian 135.9 (129.6-142.4); foreign-born Asian 78.5
(76.6-80.4). Nativity strata available for a secondary analysis.

Re-screen recovered 12 studies (were wrongly excluded on corrupted full text) —
need PDFs: 21351091 39853979 23446808 21301957 15986118 29982593 25214237
33074325 26513636 21473509 31764279 28365834. These fill Hispanic/AIAN + add
Black/Asian.


## 34861613 (Du & Song 2022, SEER) — comprehensive
Table 2 (age-adj 2000 std, per 100k) 2012-2018: NHW 190.5 (189.8-191.2);
NHB 183.1 (181.5-184.8); NHAPI 149.2 (147.7-150.7); AIAN 139.9 (134.5-145.5);
Hispanic 137.0 (135.9-138.2). -> all 4 comparisons.
Table 3 HR status (2000-2018): HR-neg NHAPI 22.3, NHW 28.0, NHB 46.5, AIAN 21.9,
Hispanic 23.3; HR-pos NHAPI 109.5, NHW 146.6, NHB 114.1, AIAN 96.5, Hispanic 97.7.
=> subtype x race data available.

## All-4 pooled (illustrates the OVERLAP problem)
Black 0.955 (0.934-0.976) k=3 I2=88% | Hispanic 0.719 (0.713-0.725) k=2 I2=0%
| Asian 0.736 (0.666-0.814) k=3 I2=99% | AIAN 0.711 (0.662-0.763) k=2 I2=74%.
Hispanic I2=0% because MMWR & DuSong are the SAME SEER data (0.719 vs 0.719) —
concrete evidence that pooling overlapping registry analyses is circular.
DECISION PENDING (after full charting): overall-pool (redundant w/ SEER) vs
disaggregated subgroups/subtype (novel) vs narrative synthesis.


## More charting (this pass)
- TNBC subgroups added (T_e7879b363303): Black 1.93(1.88-1.97); Hispanic 0.84
  (0.82-0.86); Asian 0.69(0.68-0.69); AIAN 0.84(0.75-0.93) vs White. (1 study
  each until subtype studies 33074325/39853979 arrive.)
- 34508608 & 33392441: Table 1 gives COUNTS + woman-years only -> crude rates
  only, age-adjusted rates are in figures. NOT clean age-adjusted -> use for
  ER/subtype narrative + trends, not primary rate pool. (Age-adjusted HR-neg by
  race already captured from DuSong 34861613 Table 3.)
- 39822259 England: White 199.6; Black African 118.2 (111.6-125.1). Kept as a
  UK/international stratum (pending US-only decision), not in primary pool.

## Status: charting of AVAILABLE clean-rate PDFs is essentially complete
Clean age-adjusted rate tables came from MMWR 35025856, DuSong 34861613, Gomez
20147696, 41082230 (+ 36504334 Hawaii secondary, TNBC T_e78). Remaining local
PDFs (33392441, 34508608, 30503975, 12115511) are counts/crude/figure studies
that do not add clean age-adjusted rates. Next data increment = the 12 recovered
PDFs (likely rate-table studies: 26513636, 39853979, 21351091, 33074325, ...).


## Recovered-PDF extraction (12/12 arrived)
- 21351091 (Liu, Int J Cancer 2012, LA County SEER) adj RR vs NHW: Black 0.78
  (0.77-0.79); Hispanic 0.49 (0.48-0.50); Chinese 0.45; Filipina 0.76;
  Japanese 0.68; Korean 0.34. (model-adjusted RR; Asian subgroups = disaggregated)
- 26513636 (DeSantis, BC Statistics 2015, CA Cancer J Clin, NAACCR 2008-2012,
  Fig 1): NHW 128.1; NHB 124.3; AI/AN 91.9; Hispanic 91.9; API 88.3. 4 comparisons,
  NAACCR base = less SEER overlap. Fig 2 subtype% by race (TNBC: NHW 11, NHB 22,
  Hisp 12, API 10 %).
Pools now: Black 0.920 (k5) | Hispanic 0.653 (k4) | Asian 0.724 (k4) | AIAN 0.716
(k3). I2 ~99% (large-N + real population/method differences).
Still to chart from PDFs: 31764279(AIAN), 28365834(Asian CA), 29982593(Black-White),
33074325(subtype JAMA), 39853979(subtype JAMA), 15986118, 23446808, 25214237,
21301957 — mostly figure/trend based.


## Remaining 8 recovered PDFs — charted / characterized
- 33074325 (Zhao, JAMA, SEER18 2010-15): ✅ overall IRR Black 1.04, Hisp 0.79,
  API 0.90, AIAN 0.82; TNBC IRR Black 2.07, Hisp 0.94, API 0.79, AIAN 0.89.
  => TNBC Black now POOLS: 1.997 (1.87-2.14).
- 39853979 (JAMA 2025): incidence TRENDS (APC) line-chart figures; no clean rate
  table. Secondary/trend narrative.
- 15986118 (Joslyn, NAACCR 1994-98): AGE-SPECIFIC rates + Black-White CROSSOVER
  (Black>White <40, reverses >50). Secondary/age-pattern narrative. Hisp/non-Hisp
  RR by age 1.09->0.55.
- 28365834 (Asian CA), 29982593 (Black-White brief 3pp), 23446808 (trend) = APC/
  figure/counts, not clean overall aggregate rates. Trends narrative.
- 25214237 (UK Leicester): South Asian incidence ~45% lower than white
  (international; white ~111.7/128). International/SA subgroup.
- 21301957 (US Indian-Pakistani): South Asian subgroup (small). Disaggregated.

Current primary pools (k): Black 0.939 (0.878-1.004) k6 — CI crosses 1 (Black-White
convergence) | Hispanic 0.678 k5 | Asian 0.756 k5 | AIAN 0.698 k5. All I2~99%.
TNBC Black 1.997 (1.865-2.139) k2. Charting phase COMPLETE (clean-rate data extracted;
remaining are trend/age/figure/international = secondary narrative).
