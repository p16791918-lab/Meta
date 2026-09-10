# Screening re-review audit (Feedback4 item 6: review-process reporting)

**Purpose.** Check the large-language-model title/abstract screening for false negatives
(eligible studies wrongly excluded).

**Method (reproducible).** From the 4,551 records the model excluded at title/abstract, a random
sample of **200** was drawn (Python `random.seed(42)`, `random.sample`). All 200 titles and their
recorded exclusion reasons were read. Any title related to breast cancer or to race/ethnicity with
incidence was inspected in full against the eligibility criteria (US, population-based/registry,
female invasive breast cancer incidence by race or ethnicity, with a recoverable estimate).

**Result.** 117 of the 200 titles were breast- or race/ethnicity-related and were inspected in
full; the other 83 were plainly off-topic (other cancers, methods, unrelated topics). **All 200
were judged correctly excluded — 0 false negatives.** The 117 inspected fell into the exclusion
categories the screening applied:
- **Non-US populations** (e.g., Ethiopia 4709, Iran 1952, China 2838/2765, Nigeria 3312, Latin
  America 1279/1041, sub-Saharan Africa 610, Brazil 3679/4605, England 1896, Canada 4399,
  Switzerland/China 4238);
- **Mortality, survival, or outcomes rather than incidence** (290, 1966, 4278, 230, 2454, 502,
  2173, 1197, 3800);
- **Risk-factor / etiology studies** (physical activity 583/3307, diet 2070/3159/881, obesity
  654/2623, alcohol 3148, smoking 3151/2734, pesticides 714, chemicals 932, hypertension 2112,
  hysterectomy 39, deployment 849);
- **Genetics / tumor biology** (BRCA 780/2765/2227, ancestry variants 3666, HER2 polymorphism 904,
  hereditary 343, methylation 2380);
- **Screening, treatment, or reconstruction** (2424, 1421, 600, 1136, 789, 1916, 2546, 3493);
- **Excluded populations** — male or transgender breast cancer (1916, 1889);
- **Editorials, reviews, case reports, or lab studies** (3645, 4105, 2048, 4103, 3913, 2068, 4617);
- **Hospital-based, not population-based** (rec 77 two-hospital NYC series, and its visual-abstract
  duplicate 4103).

A few neighborhood/SES-exposure titles (e.g., 3720 "neighborhood social determinants of TNBC",
502 "color or money") were inspected as borderline and resolved as exclusions, consistent with the
rule that the analytic comparator must be race/ethnicity versus a White reference rather than a
socioeconomic exposure; these are the same grounds on which SES-exposure reports were placed in the
narrative rather than the quantitative synthesis.

**Conclusion.** In this random sample of 200 model-excluded records, no eligible US
population-based breast-cancer-incidence-by-race study was wrongly excluded. This checks the
screening step for false negatives; it does not replace independent dual screening, which was not
performed (a stated limitation).

**Omissions found elsewhere and their follow-up.** Two rounds of source re-verification did find
extractable data missed on first pass, all among *included* reports, and all were corrected:
- six overlapping-registry reports initially deferred were extracted and added to the sensitivity pool;
- four reports first placed in the narrative set were moved to the quantitative synthesis after their
  image-only tables were rendered and read (rec 369, 14, 93, 210).
