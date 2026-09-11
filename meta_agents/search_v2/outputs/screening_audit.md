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

**Conclusion (sample).** One eligible study surfaced in the 200-record sample (~0.5%), indicating a
small but non-zero false-negative rate. Single-reviewer screening with model assistance, rather than
independent dual screening, is a limitation. The one study found was moved out of the excluded set.

## Full-pool scan (all 4,551 excluded records)

Because a sampled miss implies others, every excluded record was then scanned at the title+abstract
level for the same signature—breast + incidence/rate + race/ethnicity + a US registry/population
term, minus obvious-exclusion markers (non-US country, mortality/survival, treatment, genetic,
risk-factor, male/transgender, review). This flagged 176 records, whose recorded exclusion reasons
were reviewed and the strongest content-matches read at the abstract level.

**No further clear false negative of the rec-3720 type** (a full-text article directly reporting a
race-versus-White incidence rate ratio, wrongly excluded) was found. The closest content-matches
fall into two correctly-excluded classes:
- **Conference abstracts** (excluded by the pre-specified document-type rule), including some with
  eligible-looking content — e.g. 4351 (state variation in TNBC rates by race, NPCR-SEER), 4277
  (race- and subtype-specific incidence, NHB vs NHW), 4032 (Filipino/Chamorro incidence, Guam), 4388
  (Asian incidence, Central Valley), 4031 (AANHPI incidence by enclave). If a peer-reviewed
  full-length version of any of these exists, it would be eligible.
- **Socioeconomic-, segregation-, redlining-, or enclave-exposure studies** whose comparison is the
  exposure rather than race versus a White reference (e.g. 2146 redlining MA, 2609 segregation ICE
  MA, 3730 SES by subtype, 340 Asian enclave, 566 IBC by SEP, 1679 social adversity in Black women)
  — the same class carried in the narrative synthesis or excluded throughout.

**A second false negative was confirmed on full-text review: rec 2609** (Krieger 2018, JNCI Cancer
Spectrum, PMID 31360840). Although framed as a study of residential segregation, its Table 2 reports
Massachusetts age-standardized (2000 US) breast incidence rates by race with 95% CIs — NHW 140.8,
NHB 113.6, Hispanic 86.9, Asian/PI 90.4, AIAN 64.1 per 100,000 — from which IRRs versus NHW were
computed (NHB 0.81, Hispanic 0.62, Asian/PI 0.64, AIAN 0.46; delta method). It was added to the
quantitative synthesis as a single-state overlap of the national aggregate representatives, changing
no result. Both confirmed misses (3720, 2609) are neighborhood- or segregation-focused studies that
nonetheless report race-specific breast incidence — the recurring false-negative pattern here — so a
few more of that kind may remain in the excluded pool; retrieving and checking the other flagged
neighborhood/SES studies (e.g. 2146 redlining, 3730 SES-by-subtype, 340 Asian enclave) would settle
them, and any would be regional sensitivity overlaps that do not change a representative. The
remaining flagged records were risk-factor, stage- or mortality-specific, NHW-only,
proportionate-incidence (PIR), conference-abstract, or methodological reports, consistent with their
recorded exclusion reasons.

**Omissions found elsewhere and their follow-up.** Two rounds of source re-verification also found
extractable data missed on first pass, all among *included* reports, and all were corrected:
- six overlapping-registry reports initially deferred were extracted and added to the sensitivity pool;
- four reports first placed in the narrative set were moved to the quantitative synthesis after their
  image-only tables were rendered and read (rec 369, 14, 93, 210).
