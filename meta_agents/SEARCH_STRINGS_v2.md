# Search strategy v2 — expanded, multi-database (sensitivity-oriented)

Per supervisor feedback, the search covers **four databases: (1) PubMed/MEDLINE,
(2) Embase, (3) Scopus, (4) Web of Science Core Collection.** Note (per feedback):
PubMed and MEDLINE are the same database and are written as **"PubMed/MEDLINE"**
(one entry), searched via PubMed — not counted as two. The strategy is
**broadened** from the earlier title-anchored design to **title/abstract/keyword**
for the race/ethnicity concept, to raise sensitivity. Concept blocks joined with
AND: breast cancer; race/ethnicity/disparity; incidence/age-adjusted rate;
US-context. Limits: 2000–2026, English, human; exclude reviews, letters,
editorials, notes, conference abstracts at the record-type level where the
database supports it.

Run all four on the SAME day; record each database's hit count for the PRISMA
"Identification" box. **Embase is the primary screening corpus** (it encompasses
MEDLINE), per the supervisor; Scopus and WoS document comprehensiveness.

**Screening strategy (per supervisor):** all four databases are searched to
demonstrate a multi-database search, but the **primary screening corpus is
Embase**, because Embase encompasses MEDLINE (so PubMed/MEDLINE is covered).
Scopus and Web of Science are run to document comprehensiveness (report their
counts); their unique records are not separately screened. This makes the
**Embase string the critical one** — it must be comprehensive, which is why the
race/ethnicity block below is expanded to cover disaggregated groups (American
Indian/Alaska Native, Native Hawaiian/Pacific Islander, South Asian, etc.) that
the earlier title-only search could miss.

**Note on term coverage:** the race/ethnicity block was expanded beyond the
aggregate terms because this review's included studies specifically cover AIAN
(Gopalani) and Native Hawaiian/Pacific Islander (Loo, Ihenacho) and South Asian
(Jain) populations; a paper titled only "American Indian breast cancer incidence"
would be missed by aggregate-only terms.

**Detailed Asian/Pacific Islander subgroups.** Because disaggregated Asian
ethnicity is the review's central theme, the major US-reported subgroups
(Chinese, Japanese, Korean, Filipino, Vietnamese, Asian Indian) are included as
search terms so single-ethnicity studies (e.g., "Korean American breast cancer
incidence") are captured. Rarer subgroups (Pakistani, Cambodian, Hmong, Laotian,
Thai, Samoan, Guamanian, Chamorro) are not listed individually — they are seldom
reported separately in US breast-cancer incidence studies and are covered by the
umbrella terms already present (South Asian, Pacific Islander, Native Hawaiian,
Asian, Asian American). Trade-off: bare terms like "Chinese"/"Japanese"/"Korean"
also retrieve non-US (Asian-country) incidence studies. Because eligibility is
strictly US and the added country-ethnicity terms would otherwise flood the
screening set with non-US records, a **US-context block is included as a fourth
AND concept**: country terms (United States / USA / America*) + the three national
surveillance systems (SEER, NAACCR, USCS) + the **SEER registry states**
(Connecticut, Iowa, New Mexico, Utah, Hawaii, Georgia, Michigan, Washington,
California, Kentucky, Louisiana, New Jersey). The full 50-state list was trimmed to
these SEER sites because (i) national registries (NPCR/NAACCR/USCS) already cover
every other state through the system terms, (ii) very long term lists are rejected
or truncated by Web of Science / Scopus, and (iii) **US-only eligibility is enforced
at screening (TA3/FT4) regardless**, so the block only needs to avoid dropping
US studies, not to be exhaustive. Population-based incidence studies name their data
source (a US registry) or region, so single-state SEER-site studies are still
captured; any US study named only by a non-SEER state is recovered via the country/
system terms or the other databases and confirmed at screening.

---

## 1. PubMed/MEDLINE  (searched via PubMed — one database, not two)

```
("Breast Neoplasms"[Mesh] OR "breast cancer"[tiab] OR "breast carcinoma"[tiab] OR "breast neoplasm*"[tiab])
AND (race[tiab] OR racial[tiab] OR ethnic*[tiab] OR minorit*[tiab] OR disparit*[tiab]
     OR Black[tiab] OR Hispanic[tiab] OR Latin*[tiab] OR White[tiab] OR Asian[tiab]
     OR "African American"[tiab] OR "American Indian*"[tiab] OR "Alaska Nativ*"[tiab]
     OR "Native American*"[tiab] OR indigenous[tiab] OR "Pacific Islander*"[tiab]
     OR "Native Hawaiian*"[tiab] OR "South Asian*"[tiab] OR "Asian American*"[tiab]
     OR Chinese[tiab] OR Japanese[tiab] OR Korean[tiab] OR Filipin*[tiab] OR Vietnamese[tiab]
     OR "Asian Indian*"[tiab]
     OR "Ethnicity"[Mesh] OR "Minority Groups"[Mesh] OR "Health Status Disparities"[Mesh]
     OR "Black or African American"[Mesh] OR "Hispanic or Latino"[Mesh]
     OR "American Indian or Alaska Native"[Mesh]
     OR "Native Hawaiian or Other Pacific Islander"[Mesh] OR "Asian"[Mesh])
AND (incidence[tiab] OR "incidence rate*"[tiab] OR "age-adjusted"[tiab]
     OR "age-standardized"[tiab] OR "age-standardised"[tiab] OR "Incidence"[Mesh])
AND ("United States"[tiab] OR USA[tiab] OR America*[tiab] OR SEER[tiab] OR NAACCR[tiab]
     OR USCS[tiab] OR "United States Cancer Statistics"[tiab]
     OR "United States"[Mesh] OR "SEER Program"[Mesh]
     OR Connecticut[tiab] OR Iowa[tiab] OR "New Mexico"[tiab] OR Utah[tiab] OR Hawaii[tiab]
     OR Georgia[tiab] OR Michigan[tiab] OR Washington[tiab] OR California[tiab]
     OR Kentucky[tiab] OR Louisiana[tiab] OR "New Jersey"[tiab])
AND (2000:2026[dp]) AND English[lang] AND humans[MeSH]
NOT (review[pt] OR "case reports"[pt] OR editorial[pt] OR comment[pt] OR letter[pt] OR "news"[pt])
```

## 2. Embase  (Elsevier syntax — primary screening corpus)

```
('breast cancer'/exp OR 'breast cancer':ti,ab OR 'breast carcinoma':ti,ab OR 'breast neoplasm':ti,ab)
AND (race:ti,ab OR racial:ti,ab OR ethnic*:ti,ab OR minorit*:ti,ab OR disparit*:ti,ab
     OR black:ti,ab OR hispanic:ti,ab OR latin*:ti,ab OR white:ti,ab OR asian:ti,ab
     OR 'african american':ti,ab OR 'american indian*':ti,ab OR 'alaska nativ*':ti,ab
     OR 'native american*':ti,ab OR indigenous:ti,ab OR 'pacific islander*':ti,ab
     OR 'native hawaiian*':ti,ab OR 'south asian*':ti,ab OR 'asian american*':ti,ab
     OR chinese:ti,ab OR japanese:ti,ab OR korean:ti,ab OR filipin*:ti,ab OR vietnamese:ti,ab
     OR 'asian indian*':ti,ab
     OR 'ethnic group'/exp OR 'race'/exp OR 'health disparity'/exp
     OR 'American Indian'/exp OR 'Hispanic'/exp OR 'ethnicity'/exp)
AND (incidence:ti,ab OR 'incidence rate':ti,ab OR 'age-adjusted':ti,ab
     OR 'age-standardized':ti,ab OR 'age standardization'/exp)
AND ('united states':ti,ab OR usa:ti,ab OR america*:ti,ab OR seer:ti,ab OR naaccr:ti,ab
     OR uscs:ti,ab OR 'united states cancer statistics':ti,ab OR 'United States'/exp
     OR connecticut:ti,ab OR iowa:ti,ab OR 'new mexico':ti,ab OR utah:ti,ab OR hawaii:ti,ab
     OR georgia:ti,ab OR michigan:ti,ab OR washington:ti,ab OR california:ti,ab
     OR kentucky:ti,ab OR louisiana:ti,ab OR 'new jersey':ti,ab)
AND [2000-2026]/py AND [english]/lim AND [humans]/lim
NOT ('review'/it OR 'case report'/it OR editorial/it OR note/it OR 'conference abstract'/it)
```

## 3. Scopus (Advanced Search — paste as one query)

```
( TITLE-ABS-KEY ( "breast cancer" OR "breast carcinoma" OR "breast neoplasm*" ) )
AND ( TITLE-ABS-KEY ( race OR racial OR ethnic* OR minorit* OR disparit*
        OR black OR hispanic OR latin* OR white OR asian OR "african american"
        OR "american indian*" OR "alaska nativ*" OR "native american*" OR indigenous
        OR "pacific islander*" OR "native hawaiian*" OR "south asian*" OR "asian american*"
        OR chinese OR japanese OR korean OR filipin* OR vietnamese OR "asian indian*" ) )
AND ( TITLE-ABS-KEY ( incidence OR "incidence rate*" OR "age-adjusted"
        OR "age-standardized" OR "age standardi*ation" ) )
AND ( TITLE-ABS-KEY ( "United States" OR USA OR America* OR SEER OR NAACCR OR USCS
        OR "United States Cancer Statistics"
        OR Connecticut OR Iowa OR "New Mexico" OR Utah OR Hawaii
        OR Georgia OR Michigan OR Washington OR California OR Kentucky OR Louisiana OR "New Jersey" ) )
AND PUBYEAR > 1999 AND PUBYEAR < 2027
AND ( LIMIT-TO ( LANGUAGE , "English" ) )
AND NOT ( DOCTYPE ( re ) OR DOCTYPE ( le ) OR DOCTYPE ( ed ) OR DOCTYPE ( no ) OR DOCTYPE ( cp ) )
```
Export: CSV with Title, Abstract, Authors, Year, Source, DOI, PubMed ID, Document Type.

## 4. Web of Science Core Collection (Advanced Search; TS = topic)

```
TS=("breast cancer" OR "breast carcinoma" OR "breast neoplasm*")
AND TS=(race OR racial OR ethnic* OR minorit* OR disparit*
        OR Black OR Hispanic OR Latin* OR White OR Asian OR "African American"
        OR "American Indian*" OR "Alaska Nativ*" OR "Native American*" OR indigenous
        OR "Pacific Islander*" OR "Native Hawaiian*" OR "South Asian*" OR "Asian American*"
        OR Chinese OR Japanese OR Korean OR Filipin* OR Vietnamese OR "Asian Indian*")
AND TS=(incidence OR "incidence rate*" OR "age-adjusted" OR "age-standardized" OR "age standardi?ation")
AND TS=("United States" OR USA OR America* OR SEER OR NAACCR OR USCS OR "United States Cancer Statistics"
        OR Connecticut OR Iowa OR "New Mexico" OR Utah OR Hawaii
        OR Georgia OR Michigan OR Washington OR California OR Kentucky OR Louisiana OR "New Jersey")
AND PY=(2000-2026)
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
