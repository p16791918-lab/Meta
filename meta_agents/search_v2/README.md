# search_v2 — active systematic review & meta-analysis

Race/ethnicity differences in US breast-cancer incidence. 4-database search
(PubMed/MEDLINE, Embase, Scopus, Web of Science), 4,793 unique records.

## Pipeline data (top level)
- `merged_unique.csv` ...... 4,793 deduped records (screening input)
- `screening_decisions.csv`  title/abstract decisions (242 include / 4,551 exclude)
- `ft_eligibility.csv` ..... full-text decisions (119 quant / 45 narrative / 78 exclude)
- `breast_extraction.csv` .. THE meta-analysis ledger (v2-only; `verification` column)
- `ft_unavailable.csv` ..... records whose full text could not be obtained

## Scripts
- `screening.py` ........... resumable title/abstract screening harness
- `merge_dedup.py` ......... build merged_unique.csv from raw_search/
- `fetch_fulltext.py` / `ingest_pdfs.py` / `reconcile_coverage.py` — full-text retrieval
- `scan_estimates.py` ...... dump breast x race rate/IRR signal lines for extraction
- `guard_v2_only.py` ....... asserts the ledger holds ONLY v2 include-quant records
- `finalize_representatives.py`  one-representative-per-registry-family selection
- `meta_analysis_v2.py` .... DL / Paule-Mandel-REML / Hartung-Knapp; main vs sensitivity
- `make_*.py` .............. PRISMA supplementary tables

## Outputs / tables
- `TableSA_main_representatives.csv` — locked main-analysis representatives
- `TableSA_registry_overlap.csv` .... registry-overlap table (all includes, PRISMA)
- `TableS_included_studies.*`, `TableS_excluded_fulltext.*`

## Docs
- `DATA_AUDIT.md` .. source-verification audit ; `QUARANTINE.md` .. excluded values
- `EXTRACTION_WORKLIST.csv` .. per-study extraction status (DONE/TODO)
- `SEARCH_LOG.md`, `FULLTEXT_README.md`

## Folders
- `fulltext/` .. per-record full text (gitignored) ; `fulltext_pdf/` .. PDFs
- `seer_explorer/` .. SEER*Explorer comparator exports (NHW / by-race)
- `raw_search/` .. original database export files
- `screening_batches/` .. historical title/abstract batch decision files
