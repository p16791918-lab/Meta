# Data cross-check — verify every entered value against the source paper

For each study: the value I entered into `run_meta_analysis_breast.py :: STUDIES`
and **exactly where in the paper** to find it. Open the PDF (`fulltext/<PMID>.pdf`)
and confirm. Tick the box when verified. Flag anything that doesn't match.

Format: **rate** = age-adjusted incidence per 100,000; **IRR/RR** = ratio vs NHW.

---

## PRIMARY — overall invasive incidence

### 41082230 — Ghanaian & US Black Women (SEER 17)
Location: **Table 2**, row **"Overall age-standardized"** (Segi world std, women 20–74, 2013–2015)
- [ ] NHB **148.5** (146.4–150.7)
- [ ] NHW **152.9** (151.9–153.8)
- (Ghana/GBHS 84.4 — deliberately NOT used)

### 35025856 — MMWR 2022 (Ellington), USCS 1999–2018
Location: **the TABLE**, column **"2018 rate"**, rows by race/ethnicity
- [ ] NHW **186.5** · NHB **174.0** · Hispanic **134.0** · A/PI **143.5** · AI/AN **127.3**
- Note: no CIs in source → SE Poisson-approx (values themselves are exact)

### 34861613 — Du & Song 2022 (Cancer Epidemiology), SEER
Location: **Table 2**, column **"2012–2018"**, "Incidence rate (95% CI)"
- [ ] NHW **190.5** (189.8–191.2) · NHB **183.1** (181.5–184.8)
- [ ] NHAPI **149.2** (147.7–150.7) · AIAN **139.9** (134.5–145.5) · Hispanic **137.0** (135.9–138.2)

### 26513636 — DeSantis 2016 (CA Cancer J Clin), NAACCR 2008–2012
Location: **Figure 1** (bar chart, numbers printed above the light-blue "Incidence" bars)
- [ ] NHW **128.1** · NHB **124.3** · AI/AN **91.9** · Hispanic **91.9** · API **88.3**
- Note: no CIs → SE Poisson-approx

### 31764279 — Gopalani 2020 (Epidemiology), IHS-linked 1999–2015
Location: **Table 1**, "Female Breast" section, **"Overall"** row
- [ ] AI/AN **72.7** (71.6–73.8) · NHW **130.4** (130.3–130.6) · RR **0.56** (0.55–0.57)

### 33074325 — Zhao 2020 (JAMA Netw Open), SEER 18 2010–2015
Location (overall): **Results text**, section **"Incidence of Breast Cancer by Race/Ethnicity"** (the IRRs vs NHW)
- [ ] Black **1.04** (1.02–1.05) · Hispanic **0.79** (0.75–0.83) · API **0.90** (0.89–0.92) · AIAN **0.82** (0.81–0.83)
- ⚠️ **FLAG**: text states NHW absolute rate "31.3/100 000" which looks implausibly low (usually ~130). I used only the IRRs (fine); please confirm whether 31.3 is a typo / special denominator.

### 20147696 — Gomez 2010 (Am J Public Health), California CR
Location: **Table 2**, column **"2000–2004"**, "Incidence Rate (95% CI)"
- [ ] NHW **145.6** (144.6–146.7)
- [ ] US-born Asian aggregated **135.9** (129.6–142.4) · Foreign-born Asian aggregated **78.5** (76.6–80.4)
- Note: I entered a **derived combined Asian = 96.4** (person-year-weighted of US-born+foreign-born; cases 1804+6858, PY 3,068,003+6,749,192). Verify the two component rates; the 96.4 is my calculation.

### 21351091 — Liu 2012 (Int J Cancer), LA County SEER — multivariable-adjusted RR
Location: the **multivariable model table**, section **"Race/ethnicity"** (RR, 95% CI; ref = NH white)
- [ ] Black **0.78** (0.77–0.79) · Hispanic **0.49** (0.48–0.50)
- [ ] Chinese **0.45** (0.44–0.47) · Filipina **0.76** (0.73–0.78) · Japanese **0.68** (0.65–0.70) · Korean **0.34** (0.32–0.36)
- Note: adjusted RR (period + age), not ratio-of-rates.

---

## TNBC subtype (vs NHW)

### T_e7879b363303 — TNBC trends paper ⚠️ CITATION TBD
Location: Results text + IRR table (age-adjusted TNBC per 100,000)
- [ ] rates: Black **33.8** · White **17.5** · Hispanic 14.7 · AIAN 14.7 · Asian ~12
- [ ] IRR Black **1.93** (1.88–1.97) · Hispanic **0.84** (0.82–0.86) · Asian **0.69** (0.68–0.69) · AIAN **0.84** (0.75–0.93)
- ⚠️ **FLAG**: this study's full citation is not yet pinned (it came in as a no-PMID `T_` file). Please confirm author/journal/year.

### 33074325 — Zhao 2020, TNBC
Location: **Figure 1, panel D (TNBC subtype)** — IRR vs NHW
- [ ] Black **2.07** (2.01–2.14) · Hispanic **0.94** (0.91–0.98) · API **0.79** (0.75–0.83) · AIAN **0.89** (0.76–1.04)

---

## Entries that are NARRATIVE only (not in STUDIES numbers, but cited)
- 36504334 (Hawaii, age<50): Japanese 52.0, NHW 39.8, Native Hawaiian 33.2, Filipino 31.7 — Fig 1 table
- 30503975 (Hawaii): Fig 1 line chart, no labels — Native Hawaiian > White (narrative)
- 39822259 (England): White 199.6, Black African 118.2 (111.6–125.1) — text/table (UK)
- 34861613 Table 3 (HR status by race), DeSantis Fig 2 (subtype %), 15986118 (age crossover), 12115511 / 33392441 / 34508608 (counts/figures)

---

## Priority flags to check first
1. **33074325 "31.3"** absolute NHW rate (IRRs are fine, but verify the number).
2. **T_e7879b363303** citation (author/journal/year).
3. **Gomez combined Asian 96.4** (my derivation) vs the two published component rates.
4. Figure-read values (**26513636 Fig 1**, **21351091** table) — read off an image, worth a look.
