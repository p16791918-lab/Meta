# Search log — v2 (4-database search)

Records identified per database (for the PRISMA "Identification" box and
Supplementary Table 1). All searches use the strings in `../SEARCH_STRINGS_v2.md`
(2000–2026, English, human; document-type exclusions where supported).

| # | Database (platform) | Search date | Records | Export file | Status |
|---|---|---|---|---|---|
| 1 | PubMed/MEDLINE (PubMed) | 2026-08-07 | **1331** | `pubmed_medline_20260807.txt` (MEDLINE tagged) | ✅ received |
| 2 | Embase (embase.com, **Advanced Search**) | 2026-08-07 | **3248** | `embase_20260807_ADVANCED_3248.csv` | ✅ adopted |
| 3 | Scopus (scopus.com) | 2026-08-07 | **2438** | `scopus_20260807.csv` | ⚠️ confirm total |
| 4 | Web of Science Core Collection | 2026-08-07 | **2082** | `wos_20260807_1..3.xls` (3 batches) | ✅ received |
| | **Total identified** | | **9099** | | |
| | Duplicates removed (cross-DB) | | **4306** | `merge_dedup.py` | de-dup only |
| | **Unique records** | | **4793** | `merged_unique.csv` | (no screening yet) |

## Notes
- PubMed export field coverage: 1331 records; 1323 with abstract (8 title-only,
  screened on title); DOI present via LID/AID `[doi]`; PMID present.
- Embase: **3248 adopted** (run in Embase **Advanced Search**). Coverage: 3228
  abstract; 2599 Medline PMID; 2887 DOI; English. The same query in Embase Quick
  Search returns 1703, which is a **strict subset** of the 3248 (all 1691 unique
  titles are contained in the 3248; Advanced adds 1529 more via broader field/Emtree
  and MEDLINE-record handling). Advanced (superset) adopted for sensitivity; the
  Quick-search export is kept as `embase_20260807_QUICK_1703.csv` for the record.
  Report Embase as "Advanced Search, n=3248" in Supplementary Table 1.
- Scopus: 2438 records in one file; **Abstract 100%** (2438/2438), DOI 2319; no
  PubMed ID column (de-dup via DOI + fuzzy title). Confirm 2438 = full Scopus total.
- Embase is the primary screening corpus (encompasses MEDLINE); PubMed/Scopus/WoS
  counts document the multi-database search.
- WoS: 2082 confirmed complete (query returned 2,082; 3 batches 1000+1000+82).
  Coverage: Abstract 2039; DOI 1990; Pubmed Id 2001. Ignore WoS "Did you mean naaccs?"
  spelling suggestion — NAACCR is the correct registry name.
- **De-duplication done (no screening):** 9099 identified → 4306 cross-DB duplicates
  removed → **4793 unique** (`merge_dedup.py` → `merged_unique.csv`). Matched by
  DOI → PMID → normalized title. PubMed/MEDLINE-only = 34 (expected: Embase
  encompasses MEDLINE, so most PubMed records cluster into Embase).
- **Next (BLOCKED on PROSPERO amendment):** two-stage screening (`../SCREENING_PLAN.md`)
  of the 4793 unique records → `tally_prisma.py` for the PRISMA counts. Not started.
