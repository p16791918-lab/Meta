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

## 12115511 (Deapen 2002, Int J Cancer, LA County CSP) — NARRATIVE
Asian-American ethnic-subgroup TRENDS in LA County (1972-2000). Qualitative:
Japanese/Filipino ~2x Chinese/Korean; Japanese approaching/surpassing NHW; APC
Asian +6.3%/yr vs NHW +1.5%/yr (>=50y). No clean rate table in abstract/intro
(scan figures/tables only). OVERLAPS 21351091 (Liu, LA County) which already
provides the subgroup RRs (Chinese 0.45, Filipina 0.76, Japanese 0.68, Korean
0.34 - consistent with the "2x" statement). => Use as narrative/supporting
citation for Asian-subgroup heterogeneity; NOT a separate quantitative point
(avoid LA County double-count).

## 30503975 (Loo 2019, Hawaii Tumor Registry) — VERIFIED figure-based
Fig 1 = age-adjusted incidence TREND line chart, 5 groups, 1984-2013, NO printed
data labels -> exact values not extractable (eyeball 2009-2013: Native Hawaiian
~175, White ~150, Japanese ~145, Filipino ~105, Chinese ~90). No rate table.
Key NARRATIVE finding: Native Hawaiian incidence HIGHEST (above White) in Hawaii;
Japanese approaching/exceeding White. Overlaps 36504334 (Hawaii). => narrative
(Native Hawaiian > White) not a precise quantitative point.
33392441 similarly: Table 1 = counts/woman-years only; rates in figures.

---

## Age-stratified extraction (age-crossover / effect modification) — 2026-07-17

**Rationale:** the overall age-adjusted pool converges (Black IRR 0.94, CI crosses 1)
partly because age-standardization masks opposing age-specific patterns. Extracting
age-stratified rates surfaces the crossover that the pooled estimate hides.

### 36504334 — Hawaii SEER (Cancer Causes Control 2023), 2010–2014 AAIR /100k
Double-duty source: age strata × disaggregated API ethnicity. NHW = reference.

| Group | <50y AAIR (95% CI) | IRR | ≥50y AAIR (95% CI) | IRR |
|---|---|---|---|---|
| NHW (ref) | 39.8 (34.8–45.1) | — | 100.7 (94.7–106.9) | — |
| Japanese | 52.0 (45.6–58.9) | 1.31 | 107.1 (100.9–113.4) | 1.06 (ns) |
| Native Hawaiian | 33.2 (28.7–38.1) | 0.83 | 137.6 (128.2–147.4) | **1.37** |
| Filipino | 31.7 (27.4–36.4) | 0.80 | 77.9 (71.8–84.2) | 0.77 |

Computed IRR CIs (rates treated independent) reproduce the paper's reported IRRs
(≥50: NH 1.37, JA 1.06, FA 0.77) → extraction validated.
**Within-API crossover:** Japanese highest when young; Native Hawaiian overtakes
when older. Added to STUDIES as outcomes `invasive_incidence_age_lt50` /
`invasive_incidence_age_ge50` (6 rows). Kept OUT of the main age-adjusted pool.

### Black–White age crossover — NARRATIVE ONLY
No included full-text gives an extractable Black-vs-White rate+CI table by age band
(MMWR 35025856 and Li&Li 39853979 report it as APC trends / figures; DeSantis 26513636
Fig 2 is case-distribution/survival, not age-specific incidence). Documented
qualitatively: DeSantis median age at diagnosis Black 58 vs White 62; established
younger-onset excess in Black women. Not entered as a quantitative meta-analysis row.

**STUDIES now: 59 rows** (was 53) — +6 Hawaii age-stratified.

---

## Full re-sweep of ALL included PDFs — 2026-07-17 (user challenge: "did you read them all?")

Honest answer: I had NOT. Systematically dumped every table + rate-text from all 34
fulltext PDFs. Found substantial extractable data previously missed:

### NEW rows added to STUDIES (+6, now 65)
| Paper | Data | Outcome |
|---|---|---|
| 30503975 Loo 2019 (Hawaii SEER 2010-13) | Japanese 1.03, Native Hawaiian 1.11, Filipina 0.69, Chinese 0.59 (IRR+CI vs White) | invasive_incidence subgroup |
| 21301957 Kakarala 2011 (CA CR) | Asian Indian/Pakistani 72.3 vs NHW 149.5 → IRR 0.48 | invasive_incidence subgroup (NEW: South Asian) |
| 21473509 Lepeak 2011 (Wisconsin CRS) | Black 103.0 vs White 121.2 (state registry, no CI) | invasive_incidence Black (geographic diversity) |

**Consequence:** Chinese/Filipina/Japanese now have k=2 (Liu LA + Hawaii) → POOLABLE.
New disaggregated-subgroup analysis: Korean 0.34 ↔ Native Hawaiian 1.11 = **3.3x spread**.

### NEW descriptive: Black–White age crossover NOW QUANTITATIVE
- **15986118** (NAACCR 1994-98) Table 1 = full age-specific rate + RR + 95% CI for
  Black, AI, API vs White across 14 age bands. Black RR 1.92 (20-24) → 1.02 (40-44,
  crossover) → 0.78-0.84 (60+). API RR monotonic 0.68→0.40. Stored as
  AGE_CROSSOVER_15986118, printed by run_all(). This REPLACES my earlier (wrong)
  claim that Black-White crossover was "narrative only."

### Confirmed figure-only (rates readable off-axis, no CI — NOT extracted as rows)
- Li&Li 39853979 (Fig 2-5: race×subtype×age panels + APC tables)
- MMWR 35025856 (Fig 2 race×age), 23446808 Hou&Huo (Fig 2/4 race×ER trends)
- 33392441, 34508608, 29982593 (ER-subtype / convergence trend figures)
- 28365834 California Asian: Table 1 is STAGE-specific (localized/regional/distant)
  by 7 Asian subgroups incl. Vietnamese/South Asian/SE Asian; Fig 2 age<50/≥50 trends.
  Stage-sum → total invasive derivable (Korean 0.47 … Japanese 0.82) but not yet added.

### Out of US scope (UK studies — international context / narrative only)
- 39822259 (Eur J Surg Oncol 2026, UK: White ASIR 199.6, Indian 134.7)
- 25214237 (Leicester UK South Asian vs White)

### FLAGGED for optional future add (not yet in STUDIES)
- 30503975 subtype × ethnicity (Native Hawaiian TNBC 0.86 / HER2-enriched 1.19 /
  HR+HER2+ 1.35; Japanese TNBC 1.07) — would extend subtype analysis to disaggregated API.
- 28365834 stage-summed total-invasive Asian subgroups (adds Vietnamese, South Asian, SE Asian).

---

## txt-vs-PDF audit (user: "detailed data needs the PDF, not txt") — 2026-07-17

Confirmed the pattern, with one important nuance:
- Of 14 charted studies, only **41082230 has no PDF** (txt only). All others have PDFs.
- BUT 41082230's PMC-sourced .txt keeps Table 2 as **inline text**, so its data IS
  extractable without a PDF. Auditing it revealed ER-status subtype rates I had missed:
  - ER-positive Black 105.4 vs White 128.5 → IRR 0.82  (hrpos_incidence)
  - ER-negative Black 43.1 vs White 24.0 → IRR **1.80** (hrneg_incidence, aggressive)
  Added both → HR/ER-negative Black now pools k=2 (Du&Song 1.66 + Ghana 1.80) = **1.73**.
- General rule going forward: **corrupted or poorly-linearized .txt lose table structure**
  (that caused the earlier false exclusions); **PMC-XML-derived .txt keep tables inline**
  and are usable. When in doubt, prefer the PDF via pdfplumber. STUDIES 65 → 67.

---

## 12115511 (Deapen 2002) recovered from scanned PDF — 2026-07-17

The included study 12115511 ("Rapidly rising breast cancer incidence rates among
Asian-American women", Deapen, Int J Cancer 2002) had a CORRUPTED .txt (a different
article — a lifestyle/nativity survivorship paper) AND a scanned (image-only) PDF that
pdfplumber could not extract. Rendered the scan to PNG (pypdfium2 scale=3) and read
Table I directly. It contains annual age-adjusted invasive BC rates + case counts by
ethnicity for LA County 1988–1997 — a clean quantitative source after all.

Added Asian subgroup rows (Chinese/Japanese/Filipina/Korean) using 10-year mean rate
vs NHW mean (124.3) and Poisson SE from summed case counts (se_logrr_from_counts).
Korean now k=2, Chinese/Filipina/Japanese k=3. Main-race rows (Black/Hispanic/API)
NOT added — LA County overlaps Liu 21351091 (flagged for registry-cluster sensitivity).
STUDIES 83 → 87.

Lesson reinforced: a "figure-only / inaccessible" verdict can be wrong when the txt is
corrupted AND the PDF is a scan — render the scan and look. (Contrast 33392441, checked
same day: genuinely figure-only — its rates live only in trend-line figures, no numeric
rate table, and it is SEER data overlapping sources already pooled → kept narrative.)

---

## FINAL study-level reconciliation — all 27 included studies classified (2026-07-17)

Every included study examined and assigned to quantitative or narrative synthesis.

### Quantitative synthesis (15)
41082230, 35025856, 34861613, 26513636, 31764279, 33074325, 20147696, 21351091,
36504334, 30503975, 21301957, 21473509, 15986118, T_e7879b363303 (TNBC), 12115511.

### Narrative — figure-only trend papers (rates in figures, no CI; mostly SEER overlap) (6)
29982593, 28365834, 23446808, 39853979, 33392441, 34508608.

### Narrative — non-US (PICO is US racial/ethnic disparities) (3)
25214237 (UK Leicester), 39822259 (England), 33006431 (Canada + mortality-to-
incidence RATIO — wrong outcome too; exclude regardless of PICO decision).

### Narrative — US but different design / redundant (3)
40736150 (exposure = persistent-poverty AREA, not race vs NHW: breast IRR 0.79
PPA-vs-nonPPA); 11562110 (Yost — SES-stratified CA incidence, overlaps Gomez/Liu/
Deapen; SES-gradient mechanism); T_101456b59470 (Jain — CA South Asian invasive
breast 75.2 vs NHW 144 → IRR 0.52, no CI, overlaps Kakarala 21301957; corroborates).

Total 15 + 6 + 3 + 3 = 27. Data collection COMPLETE.
Pending analyst decision: US-only PICO → move the 3 non-US to excluded
(included 27→24; add to manual_decisions.csv). 33006431 excluded regardless.
