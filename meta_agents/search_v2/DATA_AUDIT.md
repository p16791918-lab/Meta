# Data audit — breast_extraction.csv (meta-analysis input)

Audit of the extraction ledger that feeds `meta_analysis_v2.py`. Two layers:
(A) automated internal-consistency checks; (B) source-fidelity spot checks of
the migrated `run_meta` rows (which were NOT re-read from source when imported).

## A. Automated consistency (all 135 rows) — PASS
- CI ordering (lo ≤ IRR ≤ hi): 0 violations.
- IRR = minority_rate / nhw_rate (where both present, ±5%): 0 violations.
- IRR plausibility (0.15–3.5): 0 out of range.
- CI width (log-width < 3): 0 implausibly wide.
- Provenance vs CI: 65 migrated rows were mis-labeled "computed-from-rates"
  though they carry a CI → **corrected** from the run_meta se-function
  (se_from_ci → directly-reported-IRR; se_logirr_from_rate_cis →
  computed-from-rates-with-CI; se_from_rates → Poisson-SE). Final ledger:
  directly-reported-IRR 64, with-CI 45, Poisson-SE 10, no-CI rate-only 9
  (rec 4098/463), directly-reported-rate 6, SIR 1.

## B. Source-fidelity spot checks (verified against fulltext)
- **rec 161 (Loo 2019, Hawaii multiethnic — supplies 26 representatives):**
  VERIFIED. Japanese HR+/HER2- IRR 1.03, Filipina 0.64 / 0.88, Chinese
  0.58 / 0.72 all match the full text. (Note: the flattened OCR mangled the
  Chinese HR+/HER2- CI to "0.46, 0.53" — does not bracket 0.58; the ledger's
  0.528–0.637 is the correct published CI.)
- **rec 169 (MMWR 2022, USCS — aggregate representative):** VERIFIED. 2018
  rates NHW 186.5, NHB 174.0, Hispanic 134.0, A/PI 143.5, AI/AN 127.3 all
  match; IRRs 0.933 / 0.718 / 0.769 / 0.683 are internally exact.
  SCALE NOTE: rec 169 rates are for **women aged ≥20** (2000 US std), so
  absolute rates run ~33% above the all-ages SEER-Explorer scale (NHW 186.5
  vs ~140). IRRs are ratios with a shared internal comparator and are
  therefore unaffected and cross-comparable (Feedback 6).

## Open items (to finish the audit)
- rec 161 "disaggregated overall" rows equal the HR+/HER2- subtype value
  exactly (e.g. Japanese 1.030 in both). Plausible (HR+/HER2- is the majority
  subtype) but the exact identity suggests a migration duplication; these
  rows are OVERLAP (rec 234 is the disaggregated representative) so the MAIN
  analysis is unaffected — verify before using in the sensitivity pool.
- Remaining migrated representative sources to spot-check: rec 210 (Du&Song),
  rec 286 (Zhao), rec 136 (DeSantis), rec 100 (Liu), rec 145 (Lepeak).
- rec 394 (Moran, Asian Indian 0.484) is an outlier vs rec 234 Asian
  Indian/Pakistani 0.952; after label normalization it collapses to an
  overlap (rec 234 is the representative), so it does not drive the forest.
- Age-standard confirmation across all studies (most are 2000 US std; rec
  3398 is 1970 world — flagged; rec 265 std pop to confirm).
