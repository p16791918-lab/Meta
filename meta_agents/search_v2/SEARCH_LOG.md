# Search log — v2 (4-database search)

Records identified per database (for the PRISMA "Identification" box and
Supplementary Table 1). All searches use the strings in `../SEARCH_STRINGS_v2.md`
(2000–2026, English, human; document-type exclusions where supported).

| # | Database (platform) | Search date | Records | Export file | Status |
|---|---|---|---|---|---|
| 1 | PubMed/MEDLINE (PubMed) | 2026-08-07 | **1331** | `pubmed_medline_20260807.txt` (MEDLINE tagged) | ✅ received |
| 2 | Embase (embase.com) | 2026-08-07 | **3248**¹ | `embase_20260807_records_1.csv` | ⚠️ confirm total |
| 3 | Scopus (scopus.com) | | | | ▢ pending |
| 4 | Web of Science Core Collection | | | | ▢ pending |
| | **Total identified** | | | | |
| | Duplicates removed (cross-DB) | | | | (after all four) |
| | **Unique records** | | | | |

## Notes
- PubMed export field coverage: 1331 records; 1323 with abstract (8 title-only,
  screened on title); DOI present via LID/AID `[doi]`; PMID present.
- ¹ Embase file is named `records_1.csv` (possible batch). Coverage: 3248 records;
  3228 abstract; 2599 Medline PMID; 2887 DOI; English. **Confirm the Embase total
  hit count and whether more batch files exist (records_2, …).**
- Embase is the primary screening corpus (encompasses MEDLINE); PubMed/Scopus/WoS
  counts document the multi-database search.
- Next: on receiving Embase (+ Scopus, WoS), normalize all → cross-database
  de-duplicate (DOI then fuzzy title) → two-stage screening (`../SCREENING_PLAN.md`)
  → `tally_prisma.py` for the PRISMA counts.
