# Screening re-review audit (Feedback4 item 6: review-process reporting)

**Purpose.** Check the large-language-model title/abstract screening for false negatives
(eligible studies wrongly excluded).

**Method (reproducible).** From the records the model excluded at title/abstract, a random sample
of **200** was drawn (Python `random.seed(42)`, `random.sample`). All 200 titles and their recorded
exclusion reasons were read. Of these, 117 concerned breast cancer or race/ethnicity with incidence;
the titles alone settled most as clearly ineligible, and the **16 whose eligibility was not decidable
from the title were read in full at the abstract level** against the eligibility criteria (US,
population-based/registry, female invasive breast cancer incidence by race or ethnicity, with a
recoverable estimate).

**Result — one false negative found (rec 3720).** Reading the 16 ambiguous abstracts identified one
record that had been wrongly excluded:
- **rec 3720** — "Neighborhood social determinants of triple negative breast cancer." A Louisiana
  Tumor Registry study of TNBC diagnosed 2010–2012 that reports, controlling for age, that **African
  American women had 2.21 times the TNBC incidence of European American women** (Table 2, model 1,
  age-adjusted; Black-vs-White RR = 2.21, 95% CI 1.96–2.48; White = reference). This is an eligible
  US population-based incidence-by-race estimate. The full text was subsequently obtained (PMID
  30834239), and the study was **added to the quantitative synthesis** as a regional overlapping
  estimate for the NHB triple-negative cell (excluded count 4,551 → 4,550; included 162 → 163; quant
  52 → 53). As a single-state estimate with an unstratified White reference, it is a sensitivity
  overlap of the national NHB TNBC representative (1.95) and changes no result.

The other 15 ambiguous abstracts were confirmed correctly excluded (imaging/sonographic series;
book chapters and narrative reviews; lab or diet studies; single-institution HER2/FISH; drug
effectiveness; screening-modality comparison; family-history and environmental-chemical
case-control; late-stage/metastasis burden), as were the remaining 101 title-decidable records
(non-US, mortality/survival/outcome, risk-factor, genetic, treatment, male/transgender, editorial,
hospital-based).

**Conclusion.** One eligible study surfaced in the 200-record sample (~0.5%), indicating a small but
non-zero false-negative rate. Single-reviewer screening with model assistance, rather than
independent dual screening, is a limitation. The one study found was moved out of the excluded set.

**Omissions found elsewhere and their follow-up.** Two rounds of source re-verification also found
extractable data missed on first pass, all among *included* reports, and all were corrected:
- six overlapping-registry reports initially deferred were extracted and added to the sensitivity pool;
- four reports first placed in the narrative set were moved to the quantitative synthesis after their
  image-only tables were rendered and read (rec 369, 14, 93, 210).
