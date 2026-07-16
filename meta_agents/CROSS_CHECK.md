# Data cross-check — verify every entered value (numbered 1–46)

Open `fulltext/<PMID>.pdf`, go to the stated location, confirm the value, tick `[x]`.
**rate** = age-adjusted incidence per 100,000; **IRR/RR** = ratio vs NHW.

---

## PRIMARY — overall invasive incidence

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

### 26513636 — DeSantis 2016 (CA Cancer J Clin), NAACCR 2008–2012 · **Figure 1 (labels above "Incidence" bars)**
13. [ ] NHW **128.1**
14. [ ] NHB **124.3**
15. [ ] AI/AN **91.9**
16. [ ] Hispanic **91.9**
17. [ ] API **88.3**

### 31764279 — Gopalani 2020 (Epidemiology), IHS-linked · **Table 1, "Female Breast" → "Overall" row**
18. [ ] AI/AN **72.7** (71.6–73.8)
19. [ ] NHW **130.4** (130.3–130.6)
20. [ ] RR **0.56** (0.55–0.57)

### 33074325 — Zhao 2020 (JAMA Netw Open), SEER 18 · **Results text "Incidence of Breast Cancer by Race/Ethnicity"**
21. [ ] Black IRR **1.04** (1.02–1.05)
22. [ ] Hispanic IRR **0.79** (0.75–0.83)
23. [ ] API IRR **0.90** (0.89–0.92)
24. [ ] AIAN IRR **0.82** (0.81–0.83)
25. [ ] ⚠️ **FLAG** — text says NHW absolute rate "**31.3**/100 000" (looks too low, usually ~130). I used only the IRRs; confirm if 31.3 is a typo / special denominator.

### 20147696 — Gomez 2010 (Am J Public Health), California CR · **Table 2, column "2000–2004"**
26. [ ] NHW **145.6** (144.6–146.7)
27. [ ] US-born Asian aggregated **135.9** (129.6–142.4)
28. [ ] Foreign-born Asian aggregated **78.5** (76.6–80.4)
29. [ ] ⚠️ **MY CALC** — combined Asian **96.4** (person-year-weighted of #27+#28; cases 1804+6858, PY 3,068,003+6,749,192). Verify #27/#28; 96.4 is my derivation.

### 21351091 — Liu 2012 (Int J Cancer), LA County SEER · **multivariable table, "Race/ethnicity" section (adjusted RR vs NH white)**
30. [ ] Black **0.78** (0.77–0.79)
31. [ ] Hispanic **0.49** (0.48–0.50)
32. [ ] Chinese **0.45** (0.44–0.47)
33. [ ] Filipina **0.76** (0.73–0.78)
34. [ ] Japanese **0.68** (0.65–0.70)
35. [ ] Korean **0.34** (0.32–0.36)

---

## TNBC subtype (vs NHW)

### T_e7879b363303 — TNBC trends paper · **Results text + IRR table**
36. [ ] rate Black **33.8**
37. [ ] rate White **17.5**
38. [ ] IRR Black **1.93** (1.88–1.97)
39. [ ] IRR Hispanic **0.84** (0.82–0.86)
40. [ ] IRR Asian **0.69** (0.68–0.69)
41. [ ] IRR AIAN **0.84** (0.75–0.93)
42. [ ] ⚠️ **FLAG** — confirm this study's citation (author/journal/year); came in as no-PMID `T_` file.

### 33074325 — Zhao 2020, TNBC · **Figure 1, panel D (TNBC subtype), IRR vs NHW**
43. [ ] Black **2.07** (2.01–2.14)
44. [ ] Hispanic **0.94** (0.91–0.98)
45. [ ] API **0.79** (0.75–0.83)
46. [ ] AIAN **0.89** (0.76–1.04)

---

## Priority (check these first): #25, #42, #29, then figure-reads #13–17 & #30–35.
