# Search strategy v2 — expanded, multi-database (sensitivity-oriented)

Per supervisor feedback, and matching the example paper's format, the search
covers three database platforms: **(1) MEDLINE and Embase** (searched together on
the Embase platform, which includes all MEDLINE records — so PubMed/MEDLINE is not
counted separately), **(2) Scopus**, and **(3) Web of Science Core Collection**.
The strategy is **broadened** from the earlier title-anchored design to
**title/abstract/keyword** for the race/ethnicity concept, to raise sensitivity.
Concept blocks joined with AND: breast cancer; race/ethnicity/disparity;
incidence/age-adjusted rate; US-context. Limits: 2000–2025, English, human;
exclude reviews, letters, editorials, notes, conference abstracts at the
record-type level where the database supports it.

Run all on the SAME day; record each platform's hit count for the PRISMA
"Identification" box.

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
ethnicity is the review's central theme, the SEER AANHPI detailed subgroups
(Chinese, Japanese, Korean, Filipino, Vietnamese, Asian Indian, Pakistani,
Cambodian, Hmong, Laotian, Thai, Samoan, Guamanian, Chamorro) are included as
search terms so single-ethnicity studies (e.g., "Korean American breast cancer
incidence") are captured. Trade-off: bare terms like "Chinese"/"Japanese"/"Korean"
also retrieve non-US (Asian-country) incidence studies. Because eligibility is
strictly US and the added country-ethnicity terms would otherwise flood the
screening set with non-US records, a **US-context block is included as a fourth
AND concept**. It is built broadly — country terms + the three national
surveillance systems (SEER, NAACCR, USCS) + all 50 state names — so that it does
not drop eligible US studies: population-based incidence studies always name
their data source (a US registry) or region, so Wisconsin-only (Lepeak),
California-only, Hawaii-only, etc. studies are still captured. This keeps
sensitivity for US studies while cutting the non-US noise the subgroup terms
introduce.

---

## 1. MEDLINE and Embase — searched together on the Embase platform

Per the supervisor's example paper, MEDLINE and Embase are searched as a single
line on the Embase platform (Embase indexes all MEDLINE records, so
"PubMed/MEDLINE" is not counted as a separate database). This is the **primary
screening corpus**. Use the Embase string in §2 below and report the combined
count as "MEDLINE and Embase".

### (Optional) PubMed / MEDLINE — direct, only if you also run PubMed separately

```
("Breast Neoplasms"[Mesh] OR "breast cancer"[tiab] OR "breast carcinoma"[tiab] OR "breast neoplasm*"[tiab])
AND (race[tiab] OR racial[tiab] OR ethnic*[tiab] OR minorit*[tiab] OR disparit*[tiab]
     OR Black[tiab] OR Hispanic[tiab] OR Latin*[tiab] OR White[tiab] OR Asian[tiab]
     OR "African American"[tiab] OR "American Indian*"[tiab] OR "Alaska Nativ*"[tiab]
     OR "Native American*"[tiab] OR indigenous[tiab] OR "Pacific Islander*"[tiab]
     OR "Native Hawaiian*"[tiab] OR "South Asian*"[tiab] OR "Asian American*"[tiab]
     OR Chinese[tiab] OR Japanese[tiab] OR Korean[tiab] OR Filipin*[tiab] OR Vietnamese[tiab]
     OR "Asian Indian*"[tiab] OR Pakistani[tiab] OR Cambodian[tiab] OR Hmong[tiab]
     OR Laotian[tiab] OR Thai[tiab] OR Samoan[tiab] OR Guamanian[tiab] OR Chamorro[tiab]
     OR "Ethnicity"[Mesh] OR "Minority Groups"[Mesh] OR "Health Status Disparities"[Mesh]
     OR "Black or African American"[Mesh] OR "Hispanic or Latino"[Mesh]
     OR "American Indian or Alaska Native"[Mesh]
     OR "Native Hawaiian or Other Pacific Islander"[Mesh] OR "Asian"[Mesh])
AND (incidence[tiab] OR "incidence rate*"[tiab] OR "age-adjusted"[tiab]
     OR "age-standardized"[tiab] OR "age-standardised"[tiab] OR "Incidence"[Mesh])
AND ("United States"[tiab] OR USA[tiab] OR America*[tiab] OR SEER[tiab] OR NAACCR[tiab]
     OR USCS[tiab] OR "United States Cancer Statistics"[tiab]
     OR "United States"[Mesh] OR "SEER Program"[Mesh]
     OR Alabama[tiab] OR Alaska[tiab] OR Arizona[tiab] OR Arkansas[tiab] OR California[tiab]
     OR Colorado[tiab] OR Connecticut[tiab] OR Delaware[tiab] OR Florida[tiab] OR Georgia[tiab]
     OR Hawaii[tiab] OR Idaho[tiab] OR Illinois[tiab] OR Indiana[tiab] OR Iowa[tiab]
     OR Kansas[tiab] OR Kentucky[tiab] OR Louisiana[tiab] OR Maine[tiab] OR Maryland[tiab]
     OR Massachusetts[tiab] OR Michigan[tiab] OR Minnesota[tiab] OR Mississippi[tiab] OR Missouri[tiab]
     OR Montana[tiab] OR Nebraska[tiab] OR Nevada[tiab] OR "New Hampshire"[tiab] OR "New Jersey"[tiab]
     OR "New Mexico"[tiab] OR "New York"[tiab] OR "North Carolina"[tiab] OR "North Dakota"[tiab] OR Ohio[tiab]
     OR Oklahoma[tiab] OR Oregon[tiab] OR Pennsylvania[tiab] OR "Rhode Island"[tiab] OR "South Carolina"[tiab]
     OR "South Dakota"[tiab] OR Tennessee[tiab] OR Texas[tiab] OR Utah[tiab] OR Vermont[tiab]
     OR Virginia[tiab] OR Washington[tiab] OR "West Virginia"[tiab] OR Wisconsin[tiab] OR Wyoming[tiab])
AND (2000:2025[dp]) AND English[lang] AND humans[MeSH]
NOT (review[pt] OR "case reports"[pt] OR editorial[pt] OR comment[pt] OR letter[pt] OR "news"[pt])
```

## 2. MEDLINE and Embase string (run on the Embase platform, MEDLINE included)

```
('breast cancer'/exp OR 'breast cancer':ti,ab OR 'breast carcinoma':ti,ab OR 'breast neoplasm':ti,ab)
AND (race:ti,ab OR racial:ti,ab OR ethnic*:ti,ab OR minorit*:ti,ab OR disparit*:ti,ab
     OR black:ti,ab OR hispanic:ti,ab OR latin*:ti,ab OR white:ti,ab OR asian:ti,ab
     OR 'african american':ti,ab OR 'american indian*':ti,ab OR 'alaska nativ*':ti,ab
     OR 'native american*':ti,ab OR indigenous:ti,ab OR 'pacific islander*':ti,ab
     OR 'native hawaiian*':ti,ab OR 'south asian*':ti,ab OR 'asian american*':ti,ab
     OR chinese:ti,ab OR japanese:ti,ab OR korean:ti,ab OR filipin*:ti,ab OR vietnamese:ti,ab
     OR 'asian indian*':ti,ab OR pakistani:ti,ab OR cambodian:ti,ab OR hmong:ti,ab
     OR laotian:ti,ab OR thai:ti,ab OR samoan:ti,ab OR guamanian:ti,ab OR chamorro:ti,ab
     OR 'ethnic group'/exp OR 'race'/exp OR 'health disparity'/exp
     OR 'American Indian'/exp OR 'Hispanic'/exp OR 'ethnicity'/exp)
AND (incidence:ti,ab OR 'incidence rate':ti,ab OR 'age-adjusted':ti,ab
     OR 'age-standardized':ti,ab OR 'age standardization'/exp)
AND ('united states':ti,ab OR usa:ti,ab OR america*:ti,ab OR seer:ti,ab OR naaccr:ti,ab
     OR uscs:ti,ab OR 'united states cancer statistics':ti,ab OR 'United States'/exp
     OR alabama:ti,ab OR alaska:ti,ab OR arizona:ti,ab OR arkansas:ti,ab OR california:ti,ab
     OR colorado:ti,ab OR connecticut:ti,ab OR delaware:ti,ab OR florida:ti,ab OR georgia:ti,ab
     OR hawaii:ti,ab OR idaho:ti,ab OR illinois:ti,ab OR indiana:ti,ab OR iowa:ti,ab
     OR kansas:ti,ab OR kentucky:ti,ab OR louisiana:ti,ab OR maine:ti,ab OR maryland:ti,ab
     OR massachusetts:ti,ab OR michigan:ti,ab OR minnesota:ti,ab OR mississippi:ti,ab OR missouri:ti,ab
     OR montana:ti,ab OR nebraska:ti,ab OR nevada:ti,ab OR 'new hampshire':ti,ab OR 'new jersey':ti,ab
     OR 'new mexico':ti,ab OR 'new york':ti,ab OR 'north carolina':ti,ab OR 'north dakota':ti,ab OR ohio:ti,ab
     OR oklahoma:ti,ab OR oregon:ti,ab OR pennsylvania:ti,ab OR 'rhode island':ti,ab OR 'south carolina':ti,ab
     OR 'south dakota':ti,ab OR tennessee:ti,ab OR texas:ti,ab OR utah:ti,ab OR vermont:ti,ab
     OR virginia:ti,ab OR washington:ti,ab OR 'west virginia':ti,ab OR wisconsin:ti,ab OR wyoming:ti,ab)
AND [2000-2025]/py AND [english]/lim AND [humans]/lim
NOT ('review'/it OR 'case report'/it OR editorial/it OR note/it OR 'conference abstract'/it)
```

## 3. Scopus (Advanced Search — paste as one query)

```
( TITLE-ABS-KEY ( "breast cancer" OR "breast carcinoma" OR "breast neoplasm*" ) )
AND ( TITLE-ABS-KEY ( race OR racial OR ethnic* OR minorit* OR disparit*
        OR black OR hispanic OR latin* OR white OR asian OR "african american"
        OR "american indian*" OR "alaska nativ*" OR "native american*" OR indigenous
        OR "pacific islander*" OR "native hawaiian*" OR "south asian*" OR "asian american*"
        OR chinese OR japanese OR korean OR filipin* OR vietnamese OR "asian indian*"
        OR pakistani OR cambodian OR hmong OR laotian OR thai OR samoan OR guamanian OR chamorro ) )
AND ( TITLE-ABS-KEY ( incidence OR "incidence rate*" OR "age-adjusted"
        OR "age-standardized" OR "age standardi*ation" ) )
AND ( TITLE-ABS-KEY ( "United States" OR USA OR America* OR SEER OR NAACCR OR USCS
        OR "United States Cancer Statistics"
        OR Alabama OR Alaska OR Arizona OR Arkansas OR California OR Colorado OR Connecticut
        OR Delaware OR Florida OR Georgia OR Hawaii OR Idaho OR Illinois OR Indiana OR Iowa
        OR Kansas OR Kentucky OR Louisiana OR Maine OR Maryland OR Massachusetts OR Michigan
        OR Minnesota OR Mississippi OR Missouri OR Montana OR Nebraska OR Nevada
        OR "New Hampshire" OR "New Jersey" OR "New Mexico" OR "New York" OR "North Carolina"
        OR "North Dakota" OR Ohio OR Oklahoma OR Oregon OR Pennsylvania OR "Rhode Island"
        OR "South Carolina" OR "South Dakota" OR Tennessee OR Texas OR Utah OR Vermont
        OR Virginia OR Washington OR "West Virginia" OR Wisconsin OR Wyoming ) )
AND PUBYEAR > 1999 AND PUBYEAR < 2026
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
        OR Chinese OR Japanese OR Korean OR Filipin* OR Vietnamese OR "Asian Indian*"
        OR Pakistani OR Cambodian OR Hmong OR Laotian OR Thai OR Samoan OR Guamanian OR Chamorro)
AND TS=(incidence OR "incidence rate*" OR "age-adjusted" OR "age-standardized" OR "age standardi?ation")
AND TS=("United States" OR USA OR America* OR SEER OR NAACCR OR USCS OR "United States Cancer Statistics"
        OR Alabama OR Alaska OR Arizona OR Arkansas OR California OR Colorado OR Connecticut
        OR Delaware OR Florida OR Georgia OR Hawaii OR Idaho OR Illinois OR Indiana OR Iowa
        OR Kansas OR Kentucky OR Louisiana OR Maine OR Maryland OR Massachusetts OR Michigan
        OR Minnesota OR Mississippi OR Missouri OR Montana OR Nebraska OR Nevada
        OR "New Hampshire" OR "New Jersey" OR "New Mexico" OR "New York" OR "North Carolina"
        OR "North Dakota" OR Ohio OR Oklahoma OR Oregon OR Pennsylvania OR "Rhode Island"
        OR "South Carolina" OR "South Dakota" OR Tennessee OR Texas OR Utah OR Vermont
        OR Virginia OR Washington OR "West Virginia" OR Wisconsin OR Wyoming)
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
