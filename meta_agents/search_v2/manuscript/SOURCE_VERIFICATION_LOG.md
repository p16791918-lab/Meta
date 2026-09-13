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
