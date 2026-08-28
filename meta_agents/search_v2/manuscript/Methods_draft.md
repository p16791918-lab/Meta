# Methods

*Racial and Ethnic Differences in Breast Cancer Incidence in the United States: A Systematic Review with Quantitative Synthesis*

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
records). Titles and abstracts, and then full texts, were screened independently by two
reviewers, and disagreements were resolved by consensus or a third reviewer. In all, 163
publications were included in the systematic review; of these, 48 were eligible for quantitative
synthesis (43 provided extractable quantitative data) and the remaining 115 informed the
narrative synthesis. Most included studies were population-based registry or incidence
studies (drawing on SEER, NPCR/USCS, NAACCR, state, or IHS-linked registries) rather than cohort
studies (Supplementary Table 2). From each study contributing quantitative data we extracted the
cancer registry, geographic coverage, diagnosis period, age range, standard population, racial
or ethnic group and comparator, outcome (overall or subtype), the reported estimate, and its
confidence interval. Each estimate was labelled by provenance—directly reported IRR or SIR,
computed from reported rates (with a reported or Poisson-derived variance), or read from a
figure—and the label was retained for risk-of-bias scoring and for a provenance-restricted
sensitivity analysis.

### Selection of a representative population-based estimate
Because SEER, NAACCR, the United States Cancer Statistics (USCS) file, and individual state
registries cover overlapping regions and diagnosis periods, the same women can appear in more
than one study; estimates from different publications that draw on the same or nested registry
populations are therefore not statistically independent. Rather than pool such non-independent
estimates, the analytic unit was the **cell** defined by each racial or ethnic group crossed with
each analytic dimension (overall incidence, a receptor-defined subtype, an age band, or nativity),
and one **representative population-based estimate** (a contemporary benchmark) was selected for each
cell. Each estimate was assigned to a registry "family," and the registry, region, diagnosis period,
age range, group, and outcome of each study were tabulated so that overlaps within a cell could be
seen (Supplementary Table 4). Within a cell, the representative was chosen by applying, in order:
the broadest population coverage (USCS > NAACCR > SEER-national > state or regional), then the most
recent and longest diagnosis period, a clearly documented age-standardization, and a directly
reported confidence interval where available.
For American Indian and Alaska Native (AI/AN) populations this order was overridden: an Indian
Health Service–linked (IHS-PRCDA) estimate was preferred over an unlinked national-registry
estimate for the same dimension, because unlinked registries misclassify race and undercount
this population, so the more valid population definition—rather than the broadest coverage—
determined the representative.
Overall, disaggregated-subgroup, subtype, and age-specific results could draw on different
studies, but the same registry data were not entered twice for the same question. The stability
of the selection was checked in three ways: restricting to studies at low risk of bias, to
directly reported (rather than computed) estimates, and to estimates with an NHW (rather than
unstratified White) comparator (Supplementary Table 6).

### Risk of bias
Risk of bias was assessed with the Joanna Briggs Institute (JBI) critical appraisal checklist
for studies reporting prevalence/incidence data,¹⁴ which is designed for population-based
descriptive rate studies (appropriate sampling frame and case ascertainment, valid identification
of the condition, adequate coverage, and appropriate statistical/standardization methods). Two
reviewers applied the checklist independently, and disagreements were resolved by consensus or a
third reviewer. Certainty of evidence was not graded,
because the review describes and compares population-based incidence rather than estimating a
causal effect for which a GRADE-type certainty rating would be appropriate.

### Statistical analysis
Each estimate was expressed as an IRR relative to NHW women. When a study reported
age-standardized rates rather than a ratio, the IRR was computed from the minority and NHW
rates of the same study, standard population, and diagnosis period, and its confidence interval
was propagated from the reported rate intervals by the delta method. Because estimates within a
group are drawn from overlapping registry populations and are not independent, they were not
combined into a pooled random-effects estimate; the primary result for each group is the
representative population-based estimate defined above. The analysis therefore presents the
racial and ethnic differences and the heterogeneity among subgroups within each aggregate
category, displayed group by group rather than summarized as a single pooled value. Studies that met
the inclusion criteria but did not provide a recoverable non-Hispanic White comparison were not
placed on the IRR scale; these were summarized narratively by racial or ethnic group and outcome.
Analyses were carried out in Python 3 using SciPy.

All quantitative results were generated from a single master extraction dataset. Each rate
ratio not reported directly by a source was recomputed from that study's own age-standardized
minority and reference rates, and each such confidence interval was reproduced from the
component rate intervals (by the delta method when both rates carried an interval, or by scaling
the minority-rate interval when the reference rate was a fixed population benchmark without a
reported interval). The main-text table, the forest figures, and the sensitivity tables were all
regenerated from this master dataset and cross-checked so that each displayed estimate and each
sensitivity baseline traces to the same underlying value.

---

## References

Method-guideline citations: 13 PRISMA 2020 (Page 2021) and 14 the JBI critical appraisal
checklist for studies reporting prevalence/incidence data (Munn 2015). Full details are in the
unified reference list (`manuscript/References_draft.md`).
