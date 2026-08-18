# Methods — draft v1

*Racial and Ethnic Differences in Breast Cancer Incidence in the United States: A Systematic Review and Meta-analysis*

Describes only procedures actually carried out. Written per `manuscript/WRITING_GUIDE.md`
and the constraints in `Advice/Feedback` (§2 search, §3 PRISMA, §4 risk of bias, §5 registry
overlap, §6 statistics). Method-guideline citations reuse the supervisor's own reference list
where they overlap (marked ✓reuse); others are flagged for the verification pass (⚠verify).

> **Open items for the study team**
> - **PROSPERO registration is not yet in place** (Feedback §2). The registration sentence
>   below is a placeholder until a record is filed.
> - Screening and extraction were done by a **single reviewer with AI assistance**, not two
>   independent reviewers; this is stated plainly and carried into the limitations.

---

## Methods

### Protocol and reporting
The review followed the Preferred Reporting Items for Systematic Reviews and Meta-Analyses
(PRISMA) 2020 statement.¹³ **[A PROSPERO registration is being prepared; the registration
number will be added here.]** The protocol covered the search, eligibility criteria, the
handling of overlapping registry data, and the planned analyses.

### Search strategy
Four databases were searched on 7 August 2026: MEDLINE via PubMed, Embase (embase.com
Advanced Search), Scopus, and the Web of Science Core Collection. The search combined four
concept blocks with AND—breast cancer, race or ethnicity, incidence or age-adjusted rate, and
the United States—using database-specific controlled vocabulary together with title/abstract
terms, so that race and ethnicity terms were not restricted to the title. Results were limited
to 2000–2026, English, and human studies, with document-type exclusions for reviews, letters,
editorials, notes, and conference abstracts. The four searches returned 9,099 records. The
search was limited to these databases; reference lists were not hand-searched and grey
literature was not sought. Full strings, platforms, dates, and per-database counts are given
in Supplementary Table 1.

### Eligibility criteria
Studies were eligible if they reported invasive breast cancer incidence among women in the
United States for at least one racial or ethnic group relative to a White or non-Hispanic
White (NHW) comparator, either as an incidence rate ratio (IRR) or standardized incidence
ratio (SIR) or as age-standardized rates from which a ratio could be computed. Both aggregate
groups and disaggregated subgroups (Asian American, Native Hawaiian and Pacific Islander,
Hispanic/Latina by origin, and American Indian and Alaska Native [AI/AN] by region) and
receptor-defined molecular subtypes were included. The reference group was recorded as each
study defined it; studies that stratified the reference by Hispanic origin were treated as NHW
and those using an unstratified White reference were labelled accordingly, and both were
retained because the reference and minority rates came from the same source. The review was
limited to U.S.-resident populations: comparable studies from other countries exist but use a
different White reference (e.g., White British), different racial and ethnic categories, and
different standard populations, so their rate ratios are not commensurable with U.S.
estimates. Reviews, editorials, letters, conference abstracts, non-U.S. studies, studies
without a usable incidence comparison, and mortality- or survival-only reports were excluded.

### Study selection and data extraction
Records were de-duplicated across databases (4,306 duplicates removed, leaving 4,793 unique
records). Titles, abstracts, and then full texts were screened by a single reviewer with AI
assistance, and a sample of decisions was checked for accuracy. From each included study we
extracted the cancer registry, geographic coverage, diagnosis period, age range, standard
population, racial or ethnic group and comparator, outcome (overall or subtype), the reported
estimate, and its confidence interval. Each estimate was labelled by provenance—directly
reported IRR or SIR, computed from reported rates (with a reported or Poisson-derived
variance), or read from a figure—and the label was retained for risk-of-bias scoring and for a
provenance-restricted sensitivity analysis.

### Handling of overlapping registry data
Because SEER, NAACCR, the United States Cancer Statistics (USCS) file, and individual state
registries cover overlapping regions and diagnosis periods, the same women can appear in more
than one study. To avoid counting them repeatedly, each estimate was assigned to a registry
"family," and the registry, region, diagnosis period, age range, group, and outcome of every
study were tabulated so that overlaps could be seen (Supplementary Table 5). For the main
analysis a single representative estimate was retained per registry family and outcome, chosen
by coverage, sample size, recency or length of the diagnosis period, a clear age-standardization
method, and a directly reported confidence interval. Overall, disaggregated-subgroup, subtype,
and age-specific results could draw on different studies, but the same registry data were not
entered twice for the same question. Three sensitivity analyses were run: restricting to
Good-rated studies, to directly reported estimates, and to estimates with an NHW (rather than
unstratified White) comparator.

### Risk of bias and certainty of evidence
Risk of bias was assessed with a Newcastle-Ottawa Scale adapted for population-based
descriptive incidence studies,¹⁴ keeping the three-domain structure (selection, comparability,
outcome) and the Good/Fair/Poor rating. Domain items covered the accuracy of racial and ethnic
classification, registry coverage, the use of a comparator drawn from the same source, and
whether the outcome was directly reported or correctly computed with a variance. Certainty of
evidence was rated within a prespecified GRADE-informed framework,¹⁵,¹⁶ with observational
estimates starting at low certainty and moving down for risk of bias, inconsistency, or
imprecision and up for a large effect. Publication bias and small-study effects were not
formally tested with funnel plots or Egger regression. Within each cell the estimates come
largely from the same overlapping registry data rather than from independent studies, which
limits the usefulness of small-study asymmetry tests; population-based registry incidence rates
are also less likely to be affected by the selective reporting these tests are designed to
detect.

### Statistical analysis
Each estimate was expressed as an IRR relative to NHW women. When a study reported
age-standardized rates rather than a ratio, the IRR was computed from the minority and NHW
rates of the same study, standard population, and diagnosis period, and its confidence interval
was propagated from the reported rate intervals by the delta method. Estimates were pooled with
random-effects models; between-study variance (τ²) was estimated by both the DerSimonian–Laird
and the Paule–Mandel (restricted maximum likelihood–equivalent) methods, and confidence
intervals used the Hartung–Knapp–Sidik–Jonkman adjustment¹⁷ rather than a normal
approximation. For cells with fewer than three estimates the Hartung–Knapp interval is
unstable and the results are reported with corresponding caution. Between-study heterogeneity
was summarized with Cochran's Q (and its p value) and with I². I² was high in most pooled
cells; this most likely reflects repeated inclusion of the same registry data rather than
genuine biological heterogeneity, so the interpretation of any pooled estimate is limited and
the one-estimate-per-registry-family main analysis is treated as primary. Analyses were carried
out in Python 3 using SciPy.

---

## References

Method-guideline citations are numbered 13–17 in the **unified reference list**
(`manuscript/References_draft.md`): 13 PRISMA 2020 (Page 2021), 14 Newcastle–Ottawa Scale
(Wells), 15 GRADE (Guyatt 2011), 16 GRADE Handbook (Schünemann 2013), 17 HKSJ (IntHout 2014).
DerSimonian–Laird (1986) and the Paule–Mandel/τ² estimator comparison (Veroniki 2016) are named
in the text; add as numbered references in the verification pass if a formal citation is wanted
for each estimator.
