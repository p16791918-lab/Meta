# Author-attribution audit — internal author_year vs. published first author

The internal `author_year` shorthand in `breast_extraction.csv` was hand-entered during extraction. Cross-checking each included study against the FIRST AUTHOR of the paper identified by its PMID/DOI (from the raw MEDLINE/Embase/Scopus/WoS search dumps) surfaced the mismatches below.

**RESOLVED.** All 23 were verified against each row's title/registry/period and found to be simple author-label errors (the linked PMID/DOI is correct; only the hand-entered surname/year was wrong — e.g. three Scarlett Lin Gomez California-registry papers were recorded as Sung/Chen/Wu, and the Hendrick↔Xu and Ellington↔Xie pairs were swapped). No wrong-PMID (type-B) cases were found. `breast_extraction.csv author_year` has been corrected to the published first author across all rows, propagating through the representative table, forest plots (`label()`), Note 1 (`DERIVATIONS.md`), Table 1, and GRADE. Supplementary Table 2 independently uses the dump-derived first author. Statistics are unchanged (author labels do not enter any computation). This table is retained as the provenance record of the correction.

Total corrected: **23** of 44 extracted studies.

| rec | internal author_year | published first author (per PMID) | PMID | Title |
|---|---|---|---|---|
| 2 | Kohler2015_SEER18 | Howlader et al. | 24777111 | US incidence of breast cancer subtypes defined by joint hormone receptor and HER2 status (2014) |
| 10 | Jemal2024_SEER17 | Davis Lynn et al. | 41082230 | Breast Cancer Incidence Rates in Ghanaian and US Black Women from 2013 Through 2015 (2025) |
| 12 | 2024_USCS_female | Zhang et al. | 41086189 | Disparities and trends of the incidence and mortality of female-specific cancers in the United States (2025) |
| 51 | ANTR2021 | Nash et al. | 34918619 | The Alaska Native Tumour Registry: fifty years of cancer surveillance data for  Alaska Native people (2022) |
| 66 | Miller2021_SEER9 | Hendrick et al. | 34427920 | Age distributions of breast cancer diagnosis and mortality by race and ethnicity in US women (2021) |
| 107 | Berdahl2021_NM-SEER | Zahrieh et al. | 33705303 | Quantification of Potential Inequities in Breast Cancer Incidence in New Mexico Through Bayesian Disease Mapping (2021) |
| 146 | Hendrick2024_SEER | Xu et al. | 38277147 | Breast Cancer Incidence Among US Women Aged 20 to 49 Years by Race, Stage, and Hormone Receptor Status (2024) |
| 155 | Scott2023_USCS | Sung et al. | 36862439 | State Variation in Racial and Ethnic Disparities in Incidence of Triple-Negative Breast Cancer among US Women (2023) |
| 169 | MMWR2022_USCS | Ellington et al. | 35025856 | Trends in Breast Cancer Incidence, by Race, Ethnicity, and Age Among Women Aged ≥20 Years - United States, 1999-2018 (2022) |
| 182 | MMWR2012_VitalSigns_23151952 | Cronin et al. | 23151952 | Vital signs: Racial disparities in breast cancer severity - United States, 2005-2009 (2012) |
| 199 | Amirikia2008_SEER9 | Baquet et al. | 18507200 | Breast cancer epidemiology in blacks and whites: Disparities in incidence, mortality, survival rates and histology (2008) |
| 200 | Anderson2012_SEER | Gleason et al. | 23166647 | Breast Cancer Incidence in Black and White Women Stratified by Estrogen and Progesterone Receptor Statuses (2012) |
| 203 | Anderson2008_SEER13 | Brinton et al. | 19001605 | Recent trends in breast cancer among younger women in the United States (2008) |
| 234 | Sung2026_SEER21 | Gomez et al. | 42377954 | Breast Cancer Incidence in Asian American, Native Hawaiian, and Pacific Islander Populations, 2000-2022 (2026) |
| 324 | Chen2017_CCR | Gomez et al. | 28365834 | Breast cancer in Asian Americans in California, 1988–2013: increasing incidence trends and recent data on breast cancer subtypes (2017) |
| 346 | MMWR2016_27736827 | Richardson et al. | 27736827 | Patterns and Trends in Age-Specific Black-White Differences in Breast Cancer Incidence and Mortality - United States, 1999-2014 (2016) |
| 463 | Gomez2007_GBACR | Keegan et al. | 17163416 | Recent trends in breast cancer incidence among 6 Asian groups in the Greater Bay Area of Northern California (2007) |
| 485 | Clegg2009_SEER | Harper et al. | 19124489 | Trends in area-socioeconomic and race-ethnic disparities in breast cancer incidence, stage at diagnosis, screening, mortality, and survival among women ages 50 years and over (1987-2005) (2009) |
| 522 | Sangaramoorthy2022_HTR | Ihenacho et al. | 36504334 | Characterizing breast cancer incidence and trends among Asian American, Native Hawaiian, and non-Hispanic White women in Hawaiʻi, 1990-2014 (2023) |
| 1478 | Nihiseah2025_Navajo | Yazzie et al. | 41385397 | Cancer incidence, stage at diagnosis, and trends across the Navajo Nation, 2014–2018 (2025) |
| 2131 | Ellington2022_USCS | Xie et al. | 35699957 | Associations of Obesity, Physical Activity, and Screening With State-Level Trends and Racial and Ethnic Disparities of Breast Cancer Incidence and Mortality in the US (2022) |
| 3298 | Howe2006_multistate | Carozza et al. | 16933057 | Patterns of cancer incidence among US Hispanics/Latinos, 1995-2000 (2006) |
| 3398 | Wu2004_SEERplusCCR | Gomez et al. | 12749722 | Cancer incidence patterns in Koreans in the US and in Kangwha, South Korea (2003) |
