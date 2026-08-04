# Search strategy v2 — expanded, 4 databases (sensitivity-oriented)

Per supervisor feedback, the search is expanded from 2 to **4 databases**
(PubMed/MEDLINE, Embase, Scopus, Web of Science Core Collection) and **broadened**
from the earlier title-anchored design to **title/abstract/keyword** for the
race/ethnicity concept, to raise sensitivity. Three concept blocks joined with AND:
(1) breast cancer, (2) race/ethnicity/disparity, (3) incidence/age-adjusted rate.
Limits: 2000–2025, English, human; exclude reviews, letters, editorials, notes,
conference abstracts at the record-type level where the database supports it.

Run all four on the SAME day; record each database's hit count for the PRISMA
"Identification" box.

---

## 1. PubMed / MEDLINE (broadened — race concept now tiab, not ti only)

```
("Breast Neoplasms"[Mesh] OR "breast cancer"[tiab] OR "breast carcinoma"[tiab] OR "breast neoplasm*"[tiab])
AND (race[tiab] OR racial[tiab] OR ethnic*[tiab] OR minorit*[tiab] OR disparit*[tiab]
     OR Black[tiab] OR Hispanic[tiab] OR White[tiab] OR Asian[tiab] OR "African American"[tiab]
     OR "Racial Groups"[Mesh] OR "Ethnicity"[Mesh] OR "Health Status Disparities"[Mesh]
     OR "Minority Groups"[Mesh])
AND (incidence[tiab] OR "incidence rate*"[tiab] OR "age-adjusted"[tiab]
     OR "age-standardized"[tiab] OR "age-standardised"[tiab] OR "Incidence"[Mesh])
AND (2000:2025[dp]) AND English[lang] AND humans[MeSH]
NOT (review[pt] OR "case reports"[pt] OR editorial[pt] OR comment[pt] OR letter[pt] OR "news"[pt])
```

## 2. Embase (Elsevier syntax; race concept now ti,ab)

```
('breast cancer'/exp OR 'breast cancer':ti,ab OR 'breast carcinoma':ti,ab OR 'breast neoplasm':ti,ab)
AND (race:ti,ab OR racial:ti,ab OR ethnic*:ti,ab OR minorit*:ti,ab OR disparit*:ti,ab
     OR black:ti,ab OR hispanic:ti,ab OR white:ti,ab OR asian:ti,ab OR 'african american':ti,ab
     OR 'ethnic group'/exp OR 'race'/exp OR 'health disparity'/exp)
AND (incidence:ti,ab OR 'incidence rate':ti,ab OR 'age-adjusted':ti,ab
     OR 'age-standardized':ti,ab OR 'age standardization'/exp)
AND [2000-2025]/py AND [english]/lim AND [humans]/lim
NOT ('review'/it OR 'case report'/it OR editorial/it OR note/it OR 'conference abstract'/it)
```

## 3. Scopus (Advanced Search — paste as one query)

```
( TITLE-ABS-KEY ( "breast cancer" OR "breast carcinoma" OR "breast neoplasm*" ) )
AND ( TITLE-ABS-KEY ( race OR racial OR ethnic* OR minorit* OR disparit*
        OR black OR hispanic OR white OR asian OR "african american" OR "racial group*" ) )
AND ( TITLE-ABS-KEY ( incidence OR "incidence rate*" OR "age-adjusted"
        OR "age-standardized" OR "age standardi*ation" ) )
AND PUBYEAR > 1999 AND PUBYEAR < 2026
AND ( LIMIT-TO ( LANGUAGE , "English" ) )
AND NOT ( DOCTYPE ( re ) OR DOCTYPE ( le ) OR DOCTYPE ( ed ) OR DOCTYPE ( no ) OR DOCTYPE ( cp ) )
```
Export: CSV with Title, Abstract, Authors, Year, Source, DOI, PubMed ID, Document Type.

## 4. Web of Science Core Collection (Advanced Search; TS = topic)

```
TS=("breast cancer" OR "breast carcinoma" OR "breast neoplasm*")
AND TS=(race OR racial OR ethnic* OR minorit* OR disparit*
        OR Black OR Hispanic OR White OR Asian OR "African American" OR "racial group*")
AND TS=(incidence OR "incidence rate*" OR "age-adjusted" OR "age-standardized" OR "age standardi?ation")
AND PY=(2000-2025)
AND LA=(English)
NOT DT=(Review OR Letter OR Editorial Material OR Note OR Meeting Abstract)
```
Export: "Tab-delimited" or RIS/CSV with Title, Abstract, Authors, Year, Source, DOI, PubMed ID (PM), Document Type (DT).

---

## Processing (what I do with your exports)

Give me the four export files (CSV/RIS/tab). I will:
1. Normalize each to the pipeline schema (title, abstract, authors, year, source, DOI, PMID, doctype).
2. Cross-database de-duplication (DOI first, then fuzzy title) — record duplicates removed and unique n.
3. Feed unique records through the two-stage screening; new candidates not already among the 27 get full-text screened; the previously included studies should re-appear (a sanity check on the old search).
4. Extract any newly eligible studies (author-verified against source PDF, same as before) and re-run the meta-analysis, sensitivity, RoB, GRADE.
5. Update the PRISMA flow (Fig 5), all counts, and the Methods search paragraph + search date.

Expectation: the four-database search should re-capture the existing 27 studies and may add a few regional/older analyses; the headline findings are unlikely to change direction, but the review becomes defensibly comprehensive.
