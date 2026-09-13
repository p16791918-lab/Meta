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
