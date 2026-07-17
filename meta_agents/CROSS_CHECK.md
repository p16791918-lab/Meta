# Data cross-check — by PMID (descending), items 1–74

Open `fulltext/<PMID>.pdf`, go to the stated location, confirm the value, tick `[x]`.
**rate** = age-adjusted incidence per 100,000; **IRR/RR** = ratio vs NHW.

---

### 41082230 — Ghanaian & US Black (SEER 17) · **Table 2, "Overall age-standardized" row** (Segi std, 20–74y, 2013–2015)
1. [ ] NHB **148.5** (146.4–150.7)
2. [ ] NHW **152.9** (151.9–153.8)

### 35025856 — MMWR 2022 (Ellington), USCS · **the TABLE, column "2018 rate"**
3. [ ] NHW **186.5**
4. [ ] NHB **174.0**
5. [ ] Hispanic **134.0**
6. [ ] A/PI **143.5**
7. [ ] AI/AN **127.3**

### 34861613 — Du & Song 2022 (Cancer Epidemiology), SEER · **Table 2, column "2012–2018"**
8. [ ] NHW **190.5** (189.8–191.2)
9. [ ] NHB **183.1** (181.5–184.8)
10. [ ] NHAPI **149.2** (147.7–150.7)
11. [ ] AIAN **139.9** (134.5–145.5)
12. [ ] Hispanic **137.0** (135.9–138.2)

### 33074325 — Zhao 2020 (JAMA Netw Open), SEER 18 2010–2015
**Overall · Results text "Incidence of Breast Cancer by Race/Ethnicity" (IRR vs NHW)**
13. [ ] Black **1.04** (1.02–1.05)
14. [ ] Hispanic **0.79** (0.75–0.83)
15. [ ] API **0.90** (0.89–0.92)
16. [ ] AIAN **0.82** (0.81–0.83)
17. [ ] ⚠️ **FLAG** — NHW absolute rate "**31.3**/100 000" looks too low (usually ~130); I used only the IRRs — confirm typo / special denominator.
**TNBC · Figure 1 panel D (IRR vs NHW)**
18. [ ] Black **2.07** (2.01–2.14)
19. [ ] Hispanic **0.94** (0.91–0.98)
20. [ ] API **0.79** (0.75–0.83)
21. [ ] AIAN **0.89** (0.76–1.04)

### 31764279 — Gopalani 2020 (Epidemiology), IHS-linked · **Table 1, "Female Breast" → "Overall" row**
22. [ ] AI/AN **72.7** (71.6–73.8)
23. [ ] NHW **130.4** (130.3–130.6)
24. [ ] RR **0.56** (0.55–0.57)

### 26513636 — DeSantis 2016 (CA Cancer J Clin), NAACCR 2008–2012 · **Figure 1 (labels above "Incidence" bars)**
25. [ ] NHW **128.1**
26. [ ] NHB **124.3**
27. [ ] AI/AN **91.9**
28. [ ] Hispanic **91.9**
29. [ ] API **88.3**

### 21351091 — Liu 2012 (Int J Cancer), LA County SEER · **multivariable table, "Race/ethnicity" section (adjusted RR vs NH white)**
30. [ ] Black **0.78** (0.77–0.79)
31. [ ] Hispanic **0.49** (0.48–0.50)
32. [ ] Chinese **0.45** (0.44–0.47)
33. [ ] Filipina **0.76** (0.73–0.78)
34. [ ] Japanese **0.68** (0.65–0.70)
35. [ ] Korean **0.34** (0.32–0.36)

### 20147696 — Gomez 2010 (Am J Public Health), California CR · **Table 2, column "2000–2004"**
36. [ ] NHW **145.6** (144.6–146.7)
37. [ ] US-born Asian aggregated **135.9** (129.6–142.4)
38. [ ] Foreign-born Asian aggregated **78.5** (76.6–80.4)
39. [ ] ⚠️ **MY CALC** — combined Asian **96.4** (PY-weighted of #37+#38; cases 1804+6858, PY 3,068,003+6,749,192). Verify #37/#38; 96.4 is my derivation.

### (no PMID) T_e7879b363303 — TNBC trends paper · **Results text + IRR table**
40. [ ] rate Black **33.8**
41. [ ] rate White **17.5**
42. [ ] IRR Black **1.93** (1.88–1.97)
43. [ ] IRR Hispanic **0.84** (0.82–0.86)
44. [ ] IRR Asian **0.69** (0.68–0.69)
45. [ ] IRR AIAN **0.84** (0.75–0.93)
46. [ ] ⚠️ **FLAG** — confirm citation (author/journal/year); came in as no-PMID `T_` file.

---

## Priority first: #17, #46, #39, then figure/table image-reads #25–29 & #30–35.

---

## 33074325 — additional molecular subtypes (Figure 1, panels A–C) · items 47–58
All IRR vs NHW (NHW=1 reference). #17-resolved: the "31.3" is NHW's rate; Black=1.04×it; we use the ratio.

**A. HR+/ERBB2- (Fig 1A)**
47. [ ] Black **0.86** (0.84–0.87)
48. [ ] Hispanic **0.78** (0.76–0.79)
49. [ ] API **0.87** (0.85–0.88)
50. [ ] AIAN **0.74** (0.69–0.79)

**B. HR+/ERBB2+ (Fig 1B)**
51. [ ] Black **1.12** (1.08–1.16)
52. [ ] Hispanic **0.91** (0.88–0.94)
53. [ ] API **1.04** (1.00–1.08)
54. [ ] AIAN **0.94** (0.81–1.09)

**C. HR-/ERBB2+ HER2-enriched (Fig 1C)**
55. [ ] Black **1.46** (1.38–1.54)
56. [ ] Hispanic **1.05** (0.99–1.11)
57. [ ] API **1.41** (1.33–1.49)
58. [ ] AIAN **1.04** (0.82–1.31)

---

## 34861613 (Du & Song) — HR-status subtypes (Table 3, age-adj rates) · items 59–66
**HR-negative (aggressive)** rates /100k
59. [ ] NHW **28.0** (27.9–28.2)
60. [ ] NHB **46.5** (46.0–47.1)
61. [ ] NHAPI **22.3** (21.9–22.7) · AIAN **21.9** (20.5–23.3) · Hispanic **23.3** (22.9–23.6)
**HR-positive** rates /100k
62. [ ] NHW **146.6** (146.2–147.0)
63. [ ] NHB **114.1** (113.3–115.0)
64. [ ] NHAPI **109.5** (108.7–110.4)
65. [ ] AIAN **96.5** (93.5–99.5)
66. [ ] Hispanic **97.7** (97.0–98.4)

---

## 36504334 (Hawaii SEER, Cancer Causes Control 2023) — AGE-STRATIFIED · items 67–74
2010–2014 AAIR /100k, invasive BC. Reference = Non-Hispanic White. Age crossover:
Japanese highest when young → Native Hawaiian overtakes when older.

**Age <50 years · Results text p.4 (para "Among young women, the 2010–2014…") + Table 2**
67. [ ] NHW (ref) **39.8** (34.8–45.1)
68. [ ] Japanese **52.0** (45.6–58.9) → IRR 1.31
69. [ ] Native Hawaiian **33.2** (28.7–38.1) → IRR 0.83
70. [ ] Filipino **31.7** (27.4–36.4) → IRR 0.80

**Age ≥50 years · Results text p.5 + Table 2 (older-women panel)**
71. [ ] NHW (ref) **100.7** (94.7–106.9)
72. [ ] Native Hawaiian **137.6** (128.2–147.4) → IRR **1.37** (paper-reported 1.37, 1.25–1.49)
73. [ ] Japanese **107.1** (100.9–113.4) → IRR 1.06 (paper 1.06, 0.98–1.15; ns)
74. [ ] Filipino **77.9** (71.8–84.2) → IRR 0.77 (paper 0.77, 0.70–0.85)

**Black–White age crossover** = narrative only (no extractable rate+CI table in included
full-texts): DeSantis 26513636 p.3 — median age at diagnosis Black **58** vs White **62**;
well-established younger-onset excess in Black women. Not entered as a quantitative row.
