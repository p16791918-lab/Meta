# Search strategy — Breast-cancer incidence racial/ethnic disparity review

Four databases: **PubMed, Embase, Scopus, Web of Science Core Collection.**
Same three-concept logic in every database:

- **C1 Breast cancer** (topic/abstract)
- **C2 Race / ethnicity / disparity** — required in the **TITLE** (keeps the set
  focused on disparity papers, as agreed for the precise strategy)
- **C3 Incidence** — in the title, OR an age-adjusted/standardized rate term in
  title/abstract
- **Limits**: 2000–2025, English, exclude reviews / case reports / editorials /
  letters / notes / conference-only where the DB allows.

Run date and hit count must be recorded per database (fill the table at the
bottom) for the PRISMA "Identification" box and the PROSPERO record.

---

## 1. PubMed (already set in `orchestrator.py` PRECISE_PUBMED_QUERY)

```
("Breast Neoplasms"[Mesh] OR "breast cancer"[tiab] OR "breast carcinoma"[tiab])
AND (race[ti] OR racial[ti] OR ethnic*[ti] OR minorit*[ti] OR disparit*[ti]
     OR Black[ti] OR Hispanic[ti] OR White[ti] OR Asian[ti] OR "African American"[ti]
     OR "Racial Groups"[Mesh] OR "Ethnicity"[Mesh] OR "Health Status Disparities"[Mesh])
AND (incidence[ti] OR "incidence rate"[tiab] OR "age-adjusted"[tiab]
     OR "age-standardized"[tiab] OR "Incidence"[Mesh])
AND (2000:2025[dp]) AND English[lang] AND humans[MeSH]
NOT (review[pt] OR "case reports"[pt] OR editorial[pt] OR comment[pt] OR letter[pt])
```
Export: **PubMed → Save → CSV / MEDLINE**. Needed fields: Title, Abstract,
Authors, Year, Journal, PMID, DOI, Publication Type.

## 2. Embase (already exported → `records_tabular.csv`, 501 records)

```
('breast cancer'/exp OR 'breast carcinoma':ti,ab OR 'breast neoplasm':ti,ab)
AND (race:ti OR racial:ti OR ethnic*:ti OR minorit*:ti OR disparit*:ti
     OR black:ti OR hispanic:ti OR white:ti OR asian:ti OR 'african american':ti)
AND (incidence:ti OR 'incidence rate':ti,ab OR 'age-adjusted':ti,ab
     OR 'age-standardized':ti,ab OR 'age standardization'/exp)
AND [2000-2025]/py AND [english]/lim AND [humans]/lim
NOT ('review'/it OR 'case report'/it OR editorial/it OR note/it)
```

## 3. Scopus (Advanced search) — **NEW, run this**

```
( TITLE-ABS-KEY ( "breast cancer" OR "breast carcinoma" OR "breast neoplasm*"
                  OR "breast tumor*" OR "breast tumour*" ) )
AND ( TITLE ( race OR racial OR ethnic* OR minorit* OR disparit* OR black
              OR hispanic OR latina OR white OR asian OR "african american"
              OR "american indian" OR "native american" OR "pacific islander" ) )
AND ( TITLE ( incidence )
      OR TITLE-ABS-KEY ( "incidence rate*" OR "age-adjusted" OR "age adjusted"
                         OR "age-standardi*" OR "age standardi*" ) )
AND PUBYEAR > 1999 AND PUBYEAR < 2026
AND LANGUAGE ( english )
AND ( DOCTYPE ( ar ) OR DOCTYPE ( cp ) )
```
Notes: Scopus has no "humans" limit (screen out non-human at title/abstract
stage). `DOCTYPE(ar)`=article, `(cp)`=conference paper; this excludes reviews
(re), letters (le), editorials (ed), notes (no), short surveys (sh).
**Export → CSV**, tick fields: *Authors, Title, Year, Source title,
Document Type, Abstract, DOI, PubMed ID* (Citation information + Abstract).
Save as `raw_scopus.csv` in this folder.

## 4. Web of Science Core Collection (Advanced Search) — **NEW, run this**

```
(TS=("breast cancer" OR "breast carcinoma" OR "breast neoplasm*"
     OR "breast tumor*" OR "breast tumour*"))
AND (TI=(race OR racial OR ethnic* OR minorit* OR disparit* OR Black OR Hispanic
         OR Latina OR White OR Asian OR "African American" OR "American Indian"
         OR "Native American" OR "Pacific Islander"))
AND (TI=(incidence)
     OR TS=("incidence rate*" OR "age-adjusted" OR "age adjusted"
            OR "age-standardi*" OR "age standardi*"))
AND PY=(2000-2025)
AND LA=(English)
AND DT=(Article OR Proceedings Paper)
```
Notes: `TS=` topic (title+abstract+keywords), `TI=` title, `DT=` document type
(Article / Proceedings Paper excludes Review, Editorial, Letter, Meeting
Abstract-only, etc.). Select **Web of Science Core Collection** as the database,
all editions.
**Export → Tab-delimited or Excel**, record content = **Full Record**
(must include Abstract). Save as `raw_wos.txt` (tab) or `raw_wos.csv`.

---

## Deduplication / merge (after all four exports are in this folder)

```bash
# 1. Normalize Scopus + WoS into the 8-column schema
python convert_scopus_wos.py raw_scopus.csv --source scopus -o records_scopus.csv
python convert_scopus_wos.py raw_wos.txt   --source wos    -o records_wos.csv
# (Embase already in records_tabular.csv; PubMed export -> records_pubmed.csv)

# 2. Merge + dedup all sources, write provenance + PRISMA counts
python merge_all_sources.py
```
Dedup cascade (in `merge_sources.py`): PMID → DOI → fuzzy title+year
(SequenceMatcher ≥ 0.92, ±1 yr). Each surviving record keeps a `SOURCES`
column (e.g. `Embase+Scopus+WoS`) → feeds the PRISMA identification/overlap box.

## Records log (fill after running each search)

| Database | Search date | Records retrieved | Export file |
|----------|-------------|-------------------|-------------|
| PubMed   |             |                   | records_pubmed.csv |
| Embase   | (done)      | 501               | records_tabular.csv |
| Scopus   |             |                   | raw_scopus.csv |
| WoS Core |             |                   | raw_wos.txt |
| **Merged (unique)** | | (auto) | records_merged.csv |
