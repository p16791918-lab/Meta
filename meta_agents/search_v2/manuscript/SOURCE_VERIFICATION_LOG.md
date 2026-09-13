# Source-verification log — representative estimates (full-text)

Full-text re-verification of all 24 representative studies (83 analytic-cell
estimates) against their original papers: data system/coverage, diagnosis
period, comparator, and the reported value (and CI). Prompted by the discovery
that Zhang 2025 had been mislabelled USCS when its source is SEER-22.

## Scope and method
- 24 distinct representative studies; source held for all (23 PDF + rec 155 as
  extracted text with eTable1 verified).
- Coverage/registry: matched each ledger `registry` and author-label source
  token against the paper's stated data system.
- Period: matched each ledger `period` against the paper's stated diagnosis
  years / table caption.
- Comparator: NHW vs unstratified White confirmed against the paper.
- Value: for directly-reported cells, the IRR and its 95% CI string were located
  in the source; for computed cells, the component minority and NHW rates were
  located; point estimates (no CI) matched on the value.

## Corrections made (metadata; none changed a representative or a headline value)
- **rec 12 Zhang 2025** — source is SEER 22-registry (~47.9% of US), not USCS;
  author_year `..._USCS`→`..._SEER22`, registry `US national`→`SEER 22 (~48%)`
  (tier 1→6). Stays an overlap (USCS Ellington outranks it); no headline change.
- **rec 265 Anderson 2008** — period `2008` (pub year) → **1975-2004** (SEER data
  range per Methods). Black age-lt40/age-ge40.
- **rec 485 Harper 2009** — period `2004` → **1997-2001** (SEER diagnosis years).
  age-ge50.
- **rec 161 Loo 2019** — period `2000-2016` → **2010-2013** (Table 1 caption; the
  years receptor/HER2 classification was available). 14 receptor-subtype cells.

## Values confirmed against source (no value error found)
- Headline aggregates (rec 169 Ellington, USCS): Black 174.0/186.5=0.933,
  Hispanic 134.0/186.5=0.718, Asian/PI 143.5/186.5=0.769, AIAN 127.3/186.5 —
  all five rates present in source; IRRs reproduce.
- AI/AN national + regional (rec 2510 Melkonian 2019): breast RR 0.87 and the
  IHS-region values (Northern Plains 1.05, Southern Plains via rec 3662 1.33,
  etc.) located in the source table.
- NHB TNBC (rec 155 Sung 2023): national rates Black 25.2 / White 12.9 → 1.95;
  IRR and CI [1.93,1.98] from eTable1 (28,710 Black TNBC cases → narrow CI legit).
- The eight crosscheck [G] "narrow-CI" warnings (rec 2406 Sung 2020 ×3, rec 286
  Kong 2020 ×3, rec 10 Davis Lynn ×1, rec 155 ×1) were each matched cell-by-cell
  to the source table; all are large national-registry (USCS/SEER-18/17) strata
  whose narrow CIs are legitimate. Not errors.
- All remaining representative cells: directly-reported IRR+CI located in source,
  or component rates located, or point-estimate value located. Zero not-found.

## Automated guards
- crosscheck A–H all PASS (A recomputes computed IRRs/CIs; H flags any
  author-label vs registry-classification mismatch — the Zhang error class).

## Honest depth note
Coverage, period, comparator: full-text checked for all 24. Values: headline and
all [G]-flagged cells confirmed against the source *table cell*; the remaining
cells confirmed by presence of the reported value/CI or component rates in the
source text plus internal recomputation (crosscheck A). No value discrepancy was
found at this depth.

## Under-extraction found and corrected (existing source, missed cells)
Full-text re-reading of Kong 2020 (rec 286, SEER-18, NHW reference) showed it
reports the complete 4-race x 4-subtype matrix, but only a subset had been
extracted. The missing cells were added:
- **New cells** (AI/AN had no estimate in these subtype dimensions):
  AI/AN HR+/HER2+ 0.94 (0.81-1.09) and AI/AN HR-/HER2+ 1.04 (0.82-1.31).
- **Overlaps** added for sensitivity: AI/AN TNBC 0.89 (0.76-1.04); Asian/PI
  HR+/HER2+ 1.04 (1.00-1.08); Hispanic HR-/HER2+ 1.05 (0.99-1.11).
Because Kong (2010-2015) is more recent than Howlader 2014 (2010 data) at equal
SEER-national coverage and NHW comparator, Kong's Asian/PI HR+/HER2+ and Hispanic
HR-/HER2+ correctly displaced Howlader as those two cells' representatives
(Asian/PI HR+/HER2+ 0.85->1.04; Hispanic HR-/HER2+ 0.84->1.05); Howlader (rec 2)
is now an overlap. Effect on counts: analytic cells 83->85, extracted estimates
206->211, representative studies 24->23, sensitivity-only studies 31->32,
corroborated cells 36->38 of the (now) 85. Prose, PRISMA counts, figures, and
docx regenerated; crosscheck A-H all pass. AI/AN subtype cells remain unlinked
(undercount caveat already in the Discussion).

## Overlap-completeness pass (all remaining extractable overlap cells)
A study-by-study re-reading of the multi-subgroup overlap sources for any
group x dimension the source reports but the ledger had skipped. Findings:
- **Gomez 2010 (rec 236, CCR) — one cell added.** The source reports all six
  Asian populations (Chinese, Japanese, Filipina, Korean, Vietnamese, **South
  Asian**); only five had been extracted. Added South Asian (labelled Asian
  Indian/Pakistani per the ledger convention; source "South Asian" = Asian
  Indian/Pakistani/Sri Lankan/Bangladeshi): rate 77.0 (72.1-82.1) vs NHW 146.1
  (145.5-146.7) -> IRR 0.527 (0.494-0.562), computed-from-rates-with-CI (method
  reproduces the study's Chinese cell exactly). Overlap only: the Asian
  Indian/Pakistani representative stays rec 234 (SEER-21, 0.958); the cell was
  already corroborated (rec 234 + rec 4027 Jin), so the corroboration split is
  unchanged. Extracted estimates 211->212; representatives, cells (85), and all
  sensitivity splits unchanged. crosscheck A-H all pass.
- **Zahnd 2019 (rec 93) — nothing to add.** The Hispanic HR-/HER2+ cell is
  suppressed at source (Table 4: ***, based on <16 cases) and cannot be
  extracted; the "Unknown subtype" column is not an analytic dimension of this
  review. Every Hispanic and NHB dimension the source reports a usable ratio for
  is already in the ledger (an earlier working note that misread the 0.74
  HR+/HER2+ value as HR-/HER2+ was wrong).
- **McCracken 2007 (rec 4098, CCR) — one aggregate cell added; no missed
  subgroup.** A page-image render of Table 3 resolved the column layout: the
  columns are Chinese, Filipino, Vietnamese, Korean, Japanese, **Total
  Asian/Pacific Islander**, and Non-Hispanic White. There is no South Asian
  column (an earlier text-only read had mistaken the aggregate column for one),
  so the five disaggregated subgroups already extracted are the only ones the
  table breaks out. The sixth column is the Total Asian/Pacific Islander
  aggregate; its female-breast rate 89.9 vs NHW 152.9 -> IRR 0.588 was added as
  an AANHPI-aggregate overlap (computed-from-rates, no CI in source). Overlap
  only: the aggregate representative stays rec 169 (Ellington USCS, 0.769) and
  the cell was already heavily corroborated, so representatives and the
  corroboration split are unchanged.
## Narrative-only pool re-verification (targeted, source-checked)
Prompted by the two quant-table under-extractions above, the narrative->quant
boundary was re-checked at the source for the highest-risk records — those whose
ft_eligibility row shows a vs-NHW comparison and an age-adjusted/standardized
rate or IRR (not PIR/SIR/OR/cohort/trend-only), prioritising the thinnest cells
(Middle Eastern, South Asian, NHPI). Findings confirm the existing
classification; no record was upgraded and no cell was added.
- **rec 3275 (Middle Eastern, CCR) — correctly narrative (duplicate).** Its
  female-breast row (ME 126.16 vs NHW 146.89 -> RR 0.86 [0.84-0.88]) is
  numerically identical to the MENA representative rec 587 (Nasseri 2009, CCR
  1988-2004, 126.2/146.9, 0.86 [0.84-0.88]) — the same ME-California population,
  so extracting it would double-count rec 587.
- **rec 3322 (South Asian, CCR 1988-2000) — correctly narrative (overlap).**
  Its Table 3 compares SA/API/NHW California rates in four sub-periods (a
  time-trend design), drawing on the same California registry as rec 236
  (Gomez 2010 CCR 1988-2004 South Asian) that already carries the CCR South
  Asian overlap; it adds no independent registry family.
- **Group-coverage cross-check.** The 31 quant-covered minority groups were
  matched against every narrative record's group: no narrative-only study
  uniquely covers a group x dimension that lacks a representative. The unusual
  narrative groups (USAPI, Somali, African-born vs US-born Black, Arab-American
  by immigrant generation, single tribes such as Seneca) are nativity strata or
  use a non-NHW comparator (US total, general population, PIR/SIR), not new
  analytic cells.
Conclusion: unlike the incomplete extraction found *within* already-included
quant tables, the narrative/quant classification itself holds on re-verification.

- Other comprehensive Asian sources confirmed complete for the review's cells:
  Jin 2016 (rec 4027) reports six Asian subgroups + aggregate, all extracted
  (smaller Hmong/Kampuchean/Laotian/Thai were aggregated and "too small to be
  included" at source); the single-/dual-subgroup studies (rec 100 Liu,
  324 Gomez2017, 49, 955, 3267, 3398, 4040) are focused reports whose other
  subgroups are figure-only or out of scope.
