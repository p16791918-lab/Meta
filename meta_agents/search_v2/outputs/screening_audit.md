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

The flagged records included a set of **neighborhood-, segregation-, redlining-, or enclave-focused
studies** (e.g. 2146, 2609, 3730, 340, 566, 1679) whose headline comparison is the exposure rather
than race. Full-text review showed these do not behave uniformly: some carry a race-specific
age-standardized breast-incidence table as a secondary result and are therefore eligible (confirmed
below for 2609 and 2146), while others report incidence only by socioeconomic stratum within each
race and are correctly excluded (3730). The other main group of content-matches were **conference
abstracts** (excluded by the pre-specified document-type rule), some with eligible-looking content —
e.g. 4351 (state variation in TNBC rates by race, NPCR-SEER), 4277 (race- and subtype-specific
incidence, NHB vs NHW), 4032 (Filipino/Chamorro incidence, Guam), 4388 (Asian incidence, Central
Valley), 4031 (AANHPI incidence by enclave); a peer-reviewed full-length version of any of these
would be eligible.

**Two further false negatives were confirmed on full-text review: rec 2609 and rec 2146.**

**rec 2609** (Krieger 2018, JNCI Cancer
Spectrum, PMID 31360840). Although framed as a study of residential segregation, its Table 2 reports
Massachusetts age-standardized (2000 US) breast incidence rates by race with 95% CIs — NHW 140.8,
NHB 113.6, Hispanic 86.9, Asian/PI 90.4, AIAN 64.1 per 100,000 — from which IRRs versus NHW were
computed (NHB 0.81, Hispanic 0.62, Asian/PI 0.64, AIAN 0.46; delta method). It was added to the
quantitative synthesis as a single-state overlap of the national aggregate representatives, changing
no result. **rec 2146** (Wright/Krieger 2022, JNCI Cancer Spectrum, PMID 35603845; Massachusetts
redlining study) likewise reports, in its Table 3, age-standardized MA breast incidence by race
(NHW 146.56, NHB 119.06, Hispanic 83.71, Asian/PI 83.15, AIAN 82.57 per 100 000); IRRs vs NHW
computed (NHB 0.81, Hispanic 0.57, Asian/PI 0.57, AIAN 0.56) and added as single-state overlaps.
All three confirmed misses (3720, 2609, 2146) are neighborhood- or segregation-focused studies that
nonetheless carry a race-specific breast-incidence table — the recurring false-negative pattern. Not
every such study qualifies. Three more were retrieved and checked in full:
- **rec 566** (Schairer 2012, IBC × socioeconomic position, SEER 2000–2007) reports inflammatory
  breast cancer incidence rate ratios by race versus NHW (Black 1.73, Hispanic-White 1.46, Asian/PI
  0.79, AIAN 1.55). It is eligible, but inflammatory breast cancer is a morphological subtype outside
  the receptor-defined quantitative cells, so — like the other IBC reports (259, 3845) — it was added
  to the **narrative synthesis**, not the quantitative synthesis.
- **rec 3730** (Akinyemiju 2015, SES by hormone-receptor subtype) and **rec 1679** (Hernandez 2025,
  social adversity and TNBC among US Black women) were confirmed **correctly excluded**: each reports
  incidence only by socioeconomic stratum — within each race (3730) or within a single race (1679,
  Black women only, reference = lowest-SES group) — with no race-versus-White rate table.

A few more of the qualifying kind may remain; checking the other flagged neighborhood/SES studies
(e.g. 340 Asian enclave, not retrievable here) would settle them, and any would be regional
sensitivity overlaps that do not change a representative. The
remaining flagged records were risk-factor, stage- or mortality-specific, NHW-only,
proportionate-incidence (PIR), conference-abstract, or methodological reports, consistent with their
recorded exclusion reasons.

**Omissions found elsewhere and their follow-up.** Two rounds of source re-verification also found
extractable data missed on first pass, all among *included* reports, and all were corrected:
- six overlapping-registry reports initially deferred were extracted and added to the sensitivity pool;
- four reports first placed in the narrative set were moved to the quantitative synthesis after their
  image-only tables were rendered and read (rec 369, 14, 93, 210).
