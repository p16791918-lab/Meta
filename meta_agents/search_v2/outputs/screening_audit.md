# Screening re-review audit (Feedback4 item 6: review-process reporting)

**Purpose.** Check the large-language-model title/abstract screening for false negatives
(eligible studies wrongly excluded).

**Method (reproducible).** From the 4,551 records the model excluded at title/abstract, a random
sample of **200** was drawn (Python `random.seed(42)`, `random.sample`) and re-screened against the
eligibility criteria. Records whose title mentioned breast cancer *and* a race/ethnicity term *and*
incidence/rate/epidemiology were flagged for full manual inspection.

**Result.** 11 of the 200 were flagged; on inspection **all 11 were correctly excluded** — none was
an eligible US population-based breast-cancer-incidence-by-race study:
- non-US populations (China 2838; Brazil 3679; Africa protocol 2138);
- treatment/survival or risk-factor studies, not population incidence (herbal medicine survival 2028;
  chemo side effects 1960; physical-activity cohort 583; breastfeeding 4415; contralateral mastectomy
  trends 600; BRCA mutation incidence 780);
- hospital-based, not registry (rec 77, "Asian American women in NYC" — two-hospital
  presentation/screening series, sub-reason recorded at screening; its visual-abstract duplicate 4103).

**Conclusion.** 0 of 200 sampled exclusions were false negatives. The screening step is consistent
with the eligibility criteria for this sample.

**Omissions found elsewhere and their follow-up.** Two rounds of source re-verification did find
extractable data missed on first pass, all among *included* reports, and all were corrected:
- six overlapping-registry reports initially deferred were extracted and added to the sensitivity pool;
- four reports first placed in the narrative set were moved to the quantitative synthesis after their
  image-only tables were rendered and read (rec 369, 14, 93, 210).
