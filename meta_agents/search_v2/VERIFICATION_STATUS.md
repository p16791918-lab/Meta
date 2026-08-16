# Source-verification status — extracted estimates

All **43 of 43** extracted studies have their full text (or data supplement) on
hand and every extracted value was cross-checked against the source.

## Method
For each ledger row, the extracted numbers were confirmed to appear in the source
PDF: the reported IRR/SIR for `directly-reported-*` provenance, or the minority
and NHW rates for `computed-from-rates*` provenance (an automated string check
plus manual inspection of the flagged/recovered cases).

## Corrections surfaced by verification (all fixed)
- **95% CIs recovered** for four studies whose CIs were present in the source but
  initially recorded as point-only — Howlader 2014 (eTable 3), Gleason 2012
  (Table 1 CIRW/CIRB), Anderson 2008 (IRR column), Richardson 2016 (MMWR rate
  CIs). All four moved Poor → Good on the Newcastle-Ottawa RoB.
- **rec 234 (Gomez 2026)**: switched to the in-paper NHW comparator from eTable 3
  (139.5, SEER-21 2018–2022) instead of an external SEER-Explorer value; added
  the eTable 3 aggregate estimates as SEER-21 sensitivity/overlap rows.
- **rec 333 (Keegan 2010)**: confirmed overall Hispanic 78.3 / NHW 125.7 (Table 1);
  the earlier 88.3 was a neighborhood-SES tertile, already corrected.
- **rec 203 (Brinton 2008)**: removed aggregate and age≥50 rows whose values did
  not trace to the source (younger-women-only paper).

## Studies verified without a local main-text PDF
- **rec 155 (Sung 2023), rec 286 (Kong 2020)**: verified against their data
  supplements (`155_supple.pdf`, `286_supple.pdf`), from which the estimates were
  extracted.

Author attributions were separately reconciled to the published first author for
all 163 included studies (see `AUTHOR_AUDIT.md`).
