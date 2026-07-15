# Breast-cancer incidence extraction log

Method A (within-study IRR = minority age-adjusted rate / NHW rate). Rates are
age-standardized invasive breast-cancer incidence per 100,000. Data go into
`run_meta_analysis_breast.py :: STUDIES`.

## ⚠️ Data-integrity caveat (important)

The auto-fetched PMC full texts in `fulltext/*.txt` are **not reliable**:
- Many are byte-identical duplicates of one another (md5 collisions), i.e. the
  same article was written to several PMID filenames.
- Even some *unique* files are mis-mapped (e.g. `34508608.txt` is an early-onset
  geographic-trends paper, not the "Decreasing ER-negative BC" study its PMID
  claims; `35025856.txt` is a Japan APC paper, not the MMWR US study).

**Therefore we extract only from sources we can trust:**
1. Manually-downloaded PDFs (the user searched the real title → correct paper).
2. A `.txt` **only after** its opening content is verified to match the study's
   expected title.

Corrupted `.txt` for included studies were deleted (commit d4fc595).

## Per-study status

| Study (PMID / key) | Source | Status |
|---|---|---|
| 41082230 Ghanaian/US Black | txt (content-verified) | ✅ extracted — Black vs NHW |
| 40736150 Persistent Poverty CA | txt (verified title) | ⏳ rates shown are all-cancer; need breast-specific-by-race table |
| 41082230 has NHW+NHB | — | done above |
| 34508608 | txt MISMATCH | ❌ needs PDF (title≠content) |
| 35025856 MMWR US | needs PDF | ⏳ user downloading |
| 36504334 AANHPI | needs PDF | ⏳ user downloading |
| 34861613 Asian ≥20 | needs PDF | ⏳ user downloading |
| 30503975 Hawaii | needs PDF | ⏳ user downloading |
| 40701557 econ segregation | needs PDF | ⏳ user downloading (may be stage, not incidence) |
| 38426333 US cancer mortality | needs PDF | ⏳ user downloading (may be mortality → narrative) |
| 20147696 Hidden Asian | needs PDF | ⏳ user downloading |
| 11562110 SES California | PDF ✅ | ⏳ to read |
| 12115511 Asian-American rising | PDF ✅ | ⏳ to read |
| 33392441 ER status Asian | PDF ✅ | ⏳ to read |
| 39822259 England 329,500 | PDF ✅ | ⏳ to read |
| T_5b207ea405f3 young adults | PDF ✅ | ⏳ to read |
| T_101456b59470 South Asian CA | PDF ✅ | ⏳ to read (classify) |
| T_223de2a7d421 racial disparities invasive | PDF ✅ | ⏳ to read (classify) |
| T_e7879b363303 TNBC trends | PDF ✅ | ⏳ to read (classify) |

## Extracted so far

**41082230** — SEER 17, 2013–2015, age-standardized (Segi world), women 20–74
(full-text Table 2):
- Non-Hispanic Black: 148.5 (146.4–150.7) per 100,000
- Non-Hispanic White: 152.9 (151.9–153.8) per 100,000
- → Black vs NHW IRR = 0.971 (very precise; large SEER sample)
- Ghana/GBHS 84.4 excluded (foreign population, not a US racial minority).

## Next
- Read the 8 available PDFs (11562110, 12115511, 33392441, 39822259, and the
  four T_* files) and extract NHW-referenced rates.
- When the user supplies the 7 needed PDFs, extract those too.
- Re-check 40736150 for a breast-specific-by-race table.
- Need ≥2 studies per minority-vs-NHW comparison before a forest plot renders.
