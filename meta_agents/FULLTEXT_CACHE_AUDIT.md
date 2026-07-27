# Full-text cache integrity audit

**Finding:** the local `fulltext/*.txt` cache is corrupted for a majority of the
checkable included studies — many `.txt` files contain a *different paper* than
the PMID/reference they are named for. This was found by reading the actual first
lines of each file (not keyword scoring) and confirmed for several studies.
**However** (see the correction below) the extracted values came from
manually-obtained PDFs, not this cache, so the practical impact is limited to
one citation fix (ref 19) plus an advisable cache refresh.

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

## Important correction — the cache is NOT the extraction source

An initial read of this audit over-stated the problem. `EXTRACTION_LOG.md`
documents that the **values were extracted from manually-obtained PDFs**
(pdfplumber for tables, pypdfium2 page-render → Read for figures), and that a
**full re-sweep of all included PDFs** was done on 2026-07-17. The log's
txt-vs-PDF audit records: *"Of 14 charted studies, only 41082230 has no PDF (txt
only); all others have PDFs … prefer the PDF."* And 41082230's `.txt` is one of
the ✅-matching files.

So the corrupted `.txt` cache is a **later artifact** (the files were overwritten
after extraction — see the heavy churn in git history); it did **not** feed the
dataset. It breaks convenient *local* re-checking, not the original provenance.

## What this does and does not mean

- **Citations** — all 32 PMIDs/DOIs resolve correctly (verified). ✅
- **Extraction provenance** — per the log, from verified PDFs with a full
  re-sweep; the corrupted `.txt` cache did not supply the values. Human
  double-checking was partial (as the manuscript states), so a value-level
  re-check is still worthwhile but is **not** invalidated by the cache issue.
- **One genuine outstanding item — ref 19.** The value "Asian Indian/Pakistani
  72.3 vs NHW 149.5 → IRR 0.48" was logged as "Kakarala 2011 (CA CR)", but the
  attached identifier PMID 21301957 is **Moran** (a clinicopathologic/survival
  study). The PMID↔study identification is wrong. The subgroup estimate is
  independently corroborated by ref 31 (Jain, ~0.52), so no conclusion is at
  risk, but the citation must be corrected or the data point dropped.

## Recommended action before submission (scoped)

1. **Resolve ref 19**: find the true source of the South Asian IRR (likely a real
   Kakarala et al. SEER/CA paper) and correct its PMID/citation, or drop the
   data point and rely on ref 31 (Jain). Update `run_meta_analysis_breast.py`,
   `REFERENCES.md`, figures, and counts accordingly.
2. **Optional but advisable**: refresh the corrupted `.txt` cache from the
   correct PDFs and spot-re-check a sample of extracted rates against them (use
   `DATA_VERIFICATION_CHECKLIST`), so local provenance is clean and re-checkable.
3. Re-run `audit_fulltext_cache.py` until every included study's stored text
   matches its PMID.

The corrupted cache alone does not block submission; **ref 19 should be fixed**
first, and the partial-verification caveat already stated in the manuscript
remains accurate.

## UPDATE — ref 19 kept pending author PDF verification (not removed)

An earlier commit removed the ref-19 data point on inference (PubMed title +
corrupted `.txt`) without checking the source PDF. That was premature and has
been **reverted**: ref 19 is restored to the quantitative pool (counts back to
14 quantitative / 13 narrative) and flagged in `REFERENCES.md` as PENDING author
verification. The author will confirm, against the actual source PDF, whether
PMID 21301957 is the correct citation and whether the "Asian Indian/Pakistani
IRR 0.48" value comes from it — then correct the citation or move it to narrative
as the evidence dictates. Do not re-remove until that check is done.

Separately, the manuscript's Asian-subgroup prose was aligned to the code output
(Chinese 0.47→0.51, Filipina 0.71→0.72, Japanese 0.78→0.84) so text matches
Fig 2; the underlying input rates for those subgroups are part of the author's
PDF verification.
