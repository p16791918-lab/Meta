# Response to Reviewers — draft

*Manuscript: "Racial and Ethnic Disparities in Breast Cancer Incidence in the
United States: A Systematic Review and Meta-Analysis Showing That Aggregate
Racial Categories Conceal Ethnic, Molecular-Subtype, and Age-Specific
Disparities."*

We thank the editor and reviewers for their careful reading. Below we respond to
each point; manuscript changes are quoted, with the section indicated. Line/page
numbers refer to the revised manuscript.

---

## 1. Prospective registration (PROSPERO)

**Comment.** The review was not prospectively registered, which some journals
weight heavily for systematic reviews.

**Response.** We acknowledge this and have not concealed it. Prospective
registration was not feasible because data extraction was already complete when
registration was considered, and PROSPERO accepts registrations only up to the
completion of extraction; a retrospective registration would misrepresent the
timeline. We have instead addressed the underlying goal of registration —
protection against undisclosed post-hoc flexibility — through complete public
availability of the protocol (PICO, search strategy, eligibility criteria, and
analysis plan), the full extracted dataset, the value-by-value extraction and
cross-check logs, the screening-decision log, and all analysis code, which
reproduces the entire analysis end-to-end from a clean environment. We describe
these openly available materials in the Methods as an important reproducibility
safeguard notwithstanding the absence of prospective registration (we have
softened the earlier wording so as not to imply that public code supersedes
registration). We are happy to add the completed-protocol document as a
supplementary file if the editor prefers.

> *Methods (Overview):* "It was not prospectively registered in PROSPERO; to
> support transparency the full protocol …, the extracted data, and all analysis
> code are openly available (see Data availability). We regard the complete
> public availability of data and code as a stronger reproducibility guarantee
> than registration alone."

## 2. Extreme heterogeneity (I² ≈ 99–100%)

**Comment.** With heterogeneity this extreme, a pooled estimate may be
meaningless; why retain the meta-analysis?

**Response.** This is the central methodological point of the paper, and we have
sharpened it rather than defended a summary rate. We do **not** offer the
aggregate pooled IRR as a recommended summary effect. On the contrary, the
meta-analytic machinery is retained precisely because its heterogeneity
statistics (I², τ², and 95% prediction intervals) are the instrument that
*quantifies and exposes* the between-stratum variation that is our thesis: the
near-100% I² is direct evidence that the aggregate category is averaging over
real, structured biological and demographic differences (by ethnicity, molecular
subtype, and age), not statistical noise. Accordingly we frame the aggregate
estimates as descriptive and place the inferential weight on the disaggregated
strata. We have made this framing explicit in the Methods and Limitations.

> *Methods (Quantitative synthesis):* "… the aggregate pooled estimates are
> presented to characterize and quantify that heterogeneity rather than as
> recommended summary effects; the disaggregated strata carry the substantive
> findings."
>
> *Limitations:* "The high I² is, in effect, a quantitative indictment of the
> aggregate estimate rather than a flaw in the synthesis."

If the reviewer would nonetheless prefer, we can move the aggregate forest plot
(Fig 1) and the pooled point estimates to the Supplement and lead the Results
with the disaggregated analyses; we have retained them in the main text only
because the paper's argument depends on first presenting the reassuring aggregate
picture and then dissolving it.

## 3. Causal / mechanistic interpretation is too strong

**Comment.** Statements such as the link to West African genetic ancestry were
not directly tested in this study.

**Response.** Agreed. We have softened all mechanistic language to conditional
phrasing and added an explicit statement that the interpretation was not tested
here.

> *Discussion:* "… it suggests that the aggressive-subtype excess **may not** be
> a universal minority phenomenon but **may instead be more consistent with**
> Black-specific etiology — **potentially involving** mechanisms linked to West
> African genetic ancestry and the distinct reproductive and socioeconomic
> exposures more prevalent among Black women — **than with** minority status per
> se. **This mechanistic interpretation was not directly tested in the present
> study and is offered as a hypothesis consistent with the observed pattern.**"

## 4. Some statements are too absolute

**Comment.** e.g., "The aggregate API estimate corresponds to no actual
population."

**Response.** We have replaced the absolute phrasing with an interpretability
claim in both the Results and the Discussion.

> *Results:* "The aggregate API estimate of 0.78 therefore **has limited
> interpretability**: it corresponds to no single constituent population and
> reflects the ethnic composition of the underlying sample rather than the risk
> of any specific community."
>
> *Discussion:* "… the aggregate **is of limited interpretability, corresponding
> to no single constituent population**."

## 5. AI-assisted screening — verification, human-review fraction, reproducibility

**Comment.** How were AI outputs verified? What fraction was human-reviewed? Is
it reproducible?

**Response.** We have expanded the Methods to specify the scope of AI use and the
verification procedure, and we disclose the same in the Declarations. AI
assistance was confined to retrieval, de-duplication, and first-pass
classification. Every full-text inclusion/exclusion decision was reviewed by the
author, and each of the 27 included studies — together with every value
extracted from it — was verified by the author against the primary full text
(100% human verification of included records). The two-stage pipeline, its
per-record decisions, and the value-by-value extraction are fully reproducible
from the openly available code, decision log, and cross-check file.

> *Methods (Study selection):* "AI assistance was confined to retrieval,
> de-duplication, and first-pass classification; every full-text inclusion or
> exclusion was reviewed by the author, and each of the 27 included studies —
> together with all data subsequently extracted from it — was verified by the
> author against the primary full text (100% human verification of included
> records). The two-stage pipeline, its per-record decisions, and the
> value-by-value extraction are fully reproducible from the openly available
> code, decision log, and cross-check file."

---

## 6. Search sensitivity (title-anchored strategy)

**Comment.** The search anchors the race/ethnicity term in the title, which is
highly specific but may have low sensitivity; relevant studies could have been
missed.

**Response.** We agree this is a deliberate specificity-over-sensitivity design,
and we have now justified it actively in the Methods (not only acknowledged it in
the Limitations). Two points bear on the "why title?" question. First, the design
was chosen to retrieve studies whose *primary objective* is racial/ethnic
variation in breast cancer incidence, rather than the far larger literature that
reports race only as a covariate in clinical, treatment, or survival analyses; an
unrestricted all-fields search returns that tangential set in overwhelming volume
with little gain in eligible primary-rate studies. Second, the search was **not**
title-only for the concept: in PubMed the race/ethnicity concept was captured by
title terms *or* the corresponding MeSH descriptors ("Racial Groups",
"Ethnicity", "Health Status Disparities"), and the incidence concept by title,
abstract, or the "Incidence" MeSH, so studies indexed to controlled vocabulary
were retrieved regardless of title wording (the title anchoring was strict only in
Embase). Because the principal US registry systems (SEER, NAACCR, USCS, and the
California and Hawaii registries) are each represented among the included studies,
the major sources of national and regional incidence data are captured; we
nonetheless state plainly that a more sensitive, abstract-wide search could add
further regional analyses. If the editor wishes, we can run and report a
supplementary abstract-wide search to quantify any incremental yield.

> *Limitations:* "… our search was deliberately specific — anchoring the
> race/ethnicity/disparity term in the article title — which favours precision
> over sensitivity and may have missed studies that reported incidence
> disparities only as a secondary result … but we cannot exclude that a more
> sensitive search would add further regional analyses."

## 7. Choice of between-study variance estimator (DerSimonian–Laird)

**Comment.** Why DerSimonian–Laird rather than REML or a Hartung–Knapp
adjustment?

**Response.** We used DerSimonian–Laird as the conventional random-effects
default and have added a justification. Critically, our inference does not depend
on the precise width of the aggregate confidence intervals — we emphasize the
*direction* of effects and the disaggregated strata — so the choice of variance
estimator has negligible bearing on the conclusions. We additionally confirmed
robustness with fixed-effect and one-estimate-per-registry-family analyses.

> *Methods (Quantitative synthesis):* "DerSimonian–Laird was chosen as the
> conventional random-effects default; because our inference rests on the
> direction of effects and on the disaggregated strata rather than on the precise
> width of the aggregate confidence intervals, the choice of between-study
> variance estimator (e.g., restricted maximum likelihood, or a Hartung–Knapp
> adjustment) has negligible bearing on the conclusions …"

## Minor / technical

- **Reference ordering.** In-text citation numbers are in strict order of first
  appearance and correspond one-to-one to the reference list.
- **Reference 27 (Gathani et al., 2026, England).** This is a recent
  article-numbered publication (*Eur J Surg Oncol.* 2026;52:109585); the author
  list was verified from the full text. It is used only as a non-US narrative
  comparison. We will re-verify the final citation details against the journal
  record at proof.
- **Data sparsity.** Subgroup/subtype comparisons resting on as few as two
  sources are now explicitly labeled hypothesis-generating rather than definitive
  population-wide estimates.
- **Publication bias.** Formal funnel/Egger tests were not applicable (<10
  studies per comparison; registry overlap makes funnel asymmetry
  uninterpretable). We added a qualitative assessment: registry data ascertain
  essentially all incident cases and are reported regardless of the direction of
  any race/ethnicity contrast, so selective publication of "positive" findings
  does not operate as in hypothesis-testing studies. Grey literature and
  conference abstracts were not sought because primary age-adjusted rates were
  required; the near-census nature of registry reporting attenuates the
  file-drawer problem.

We believe these revisions address the reviewers' concerns while preserving the
paper's central contribution. We thank the reviewers again for improving the
manuscript.
