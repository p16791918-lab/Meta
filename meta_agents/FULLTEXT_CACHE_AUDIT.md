# Full-text cache integrity audit — MUST RESOLVE BEFORE SUBMISSION

**Finding:** the local `fulltext/*.txt` cache is corrupted for a majority of the
checkable included studies — many `.txt` files contain a *different paper* than
the PMID/reference they are named for. This was found by reading the actual first
lines of each file (not keyword scoring) and confirmed for several studies.

The citation identities themselves (all 32 PMIDs/DOIs) are correct and were
verified against PubMed/Crossref (`verify_citations.py`). The problem is the
**stored full-text files**, which means the local cache cannot be used to verify
that each extracted rate came from the paper it is attributed to.

## Corruption map (included studies with a local `.txt`)

| ref | PMID | expected paper | local `.txt` actually contains | status |
|----|------|----------------|-------------------------------|--------|
| 1  | 26513636 | DeSantis, breast cancer statistics 2015 (CA Cancer J Clin) | generic "JNCI / PMC13339151" header | ❌ wrong |
| 2  | 29982593 | Davis Lynn, Black–White trends | Black–White incidence trends text | ✅ match |
| 4  | 33074325 | Kong, subtype incidence by race (JAMA Netw Open) | 3-D tumour volume on DCE-MRI study | ❌ wrong |
| 6  | 15986118 | Joslyn, NAACCR rates by age | Nigeria breast cancer paper | ❌ wrong |
| 8  | 33006431 | Nobel, mortality-to-incidence ratio (US/NYC) | a Canada paper (source of the old "Canada" note) | ❌ wrong |
| 12 | 41082230 | Ghanaian/US Black incidence | sub-Saharan African incidence text | ✅ match |
| 15 | 31764279 | Gopalani, AIAN incidence | AIAN cancer incidence text | ✅ match |
| 16 | 21351091 | Liu, LA detailed race/ethnicity incidence | a China breast cancer paper | ❌ wrong |
| 19 | 21301957 | Moran, Indian-Pakistani clinicopathologic/survival | South Asian **screening/mammography** paper | ❌ wrong |
| 20 | 21473509 | Lepeak, Wisconsin disparities | a Canada paper | ❌ wrong |
| 21 | 28365834 | Gomez, Asian Americans California (Breast Cancer Res Treat) | generic "JNCI / PMC13339151" header | ❌ wrong |
| 22 | 23446808 | Hou & Huo, US trend 2000–2009 | a smoking / breast-cancer-risk paper | ❌ likely wrong |
| 23 | 39853979 | Li & Li, subtype trends (JAMA Netw Open) | generic "JNCI / PMC13339151" header | ❌ wrong |
| 25 | 34508608 | Davis Lynn, ER-negative trends | early-onset BC incidence text | ✅ match |
| 26 | 25214237 | Stotter, South Asian UK | UK breast cancer text | ✅ match |
| 28 | 12115511 | Deapen, Asian-American rising rates | Asian/Hispanic/NHW immigrant text | ✅ match |
| 29 | 40736150 | Movsisyan, persistent-poverty California | California SES disparities text | ✅ match |

`[1]`, `[21]`, `[23]` share the identical "PMC13339151 / JNCI" header → the
download/caching step overwrote several files with the same wrong content.
(Studies with no local `.txt` — refs 3, 5, 7, 9–11, 13, 14, 17, 18, 24, 27, 30 —
could not be checked this way.)

## What this does and does not mean

- **Does NOT mean the citations are wrong.** All 32 PMIDs/DOIs resolve to the
  correct papers (verified).
- **Does mean** the extracted rate values cannot be confirmed against the local
  cache, and at least one value is misattributed: the "Asian Indian/Pakistani
  IRR 0.48" data point is attributed to ref 19 (Moran, a clinicopathologic/
  survival study) whose local file is a screening paper. (That subgroup estimate
  is independently corroborated by ref 31, Jain, ~0.52, so the *direction* is not
  at risk — but the provenance is.)
- The extracted values may still be correct if they were taken from correct PDFs
  during the original extraction and the `.txt` cache was corrupted later (the
  git history shows heavy churn/overwrite of these files). **This cannot be
  assumed; it must be re-verified.**

## Required action before submission

1. In an environment where NCBI/publishers are reachable (the Codespace), obtain
   the **correct** full text for every quantitative study (refs 1, 4, 6, 8→n/a
   excluded, 12–20, and 3, 5, 13, 14, 17, 18 that lack a local file).
2. Re-verify each extracted rate in `DATA_VERIFICATION_CHECKLIST` against the
   correct paper's table/figure. Fix any value that does not match in
   `run_meta_analysis_breast.py`, then regenerate figures, PRISMA counts, and the
   manuscript numbers.
3. Resolve ref 19 specifically: confirm whether Moran (21301957) reports
   population incidence; if not, replace it with the correct source of the South
   Asian estimate or drop that data point (ref 31 still supports the direction).
4. Re-run `verify_citations.py` and re-audit the cache until every included
   study's full text matches its PMID.

**Until steps 1–4 are complete, the quantitative dataset is not independently
verified and the manuscript should not be submitted.**
