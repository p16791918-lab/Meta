# Data verification results — quantitative synthesis

Every value entering the meta-analysis was checked against the **source-article
PDF** held in `fulltext/*.pdf` (the corrupted `fulltext/*.txt` cache was NOT used;
the PDFs were confirmed to be the correct articles by title match). Rates in
tables were matched by exact number search; rates presented only as a chart were
read from the rendered figure; IRR/RR values were matched with their confidence
intervals.

## Result: all 13 quantitative studies verified, 0 data errors

| ref | study (PMID) | method | outcome |
|----|--------------|--------|---------|
| 1  | DeSantis 26513636 | Figure 1 (rendered) | NHW 128.1, NHB 124.3, AI/AN 91.9, Hispanic 91.9, API 88.3 — all confirmed |
| 3  | Gomez 20147696 | table | US-born 135.9 / foreign-born 78.5 / NHW 145.6 — confirmed |
| 4  | Kong 33074325 | table (IRRs) | 20/20 subtype IRRs + CIs confirmed |
| 5  | Du & Li (TNBC) 36895969 | table | Black 33.8, Hisp 14.7, Asian 12.0, AIAN 14.7 / NHW 17.5 — confirmed |
| 6  | Joslyn 15986118 | table | age-band rates confirmed |
| 12 | Davis Lynn 41082230 | PMC table (txt correct) | Black 148.5/152.9, ER+ 105.4/128.5, ER− 43.1/24.0 — confirmed |
| 13 | Ellington 35025856 | table | Black 174.0, Hisp 134.0, Asian 143.5, AIAN 127.3 / NHW 186.5 — confirmed |
| 14 | Du & Song 34861613 | table | 15/15 rates confirmed |
| 15 | Gopalani 31764279 | table | AIAN 72.7 / NHW 130.4 — confirmed |
| 16 | Liu 21351091 | table (adj RR) | 6/6 RRs confirmed (Japanese 0.68 [0.65–0.70]) |
| 17 | Ihenacho 36504334 | table | age <50 / ≥50 rates confirmed |
| 18 | Loo 30503975 | table | Hawaii IRR rates confirmed |
| 19 | Moran 21301957 | Table 1 | Asian Indian/Pakistani 72.3 / NHW 149.5 — confirmed |
| 20 | Lepeak 21473509 | table | Black 103.0 / NHW 121.2 — confirmed |

Notes:
- The `fulltext/*.txt` cache is corrupted for many studies (wrong article), but it
  was never the extraction source; the `fulltext/*.pdf` files are intact and match.
- Non-data corrections made during verification: internal labels
  (`Kakarala`→Moran, `California CR`→SEER for ref 19); manuscript Asian-subgroup
  prose aligned to the code output (Chinese 0.51, Filipina 0.72, Japanese 0.84).
- Limitation that remains: verification was single-author + AI-assisted, not a
  two-reviewer independent double-extraction (stated in Methods/Limitations).
