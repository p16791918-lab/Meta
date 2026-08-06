# Data-extraction coding manual (supervisor feedback #6, #7)

Rules fixed **before** extraction so coding is consistent and the numbers are
reproducible. One reviewer extracts with AI first-pass support; **every value is
verified against the source article** (table/figure + page recorded). The extracted
sheet feeds `STUDIES` in `run_meta_analysis_breast.py`.

---

## 1. Extraction fields (per estimate) — mirrors the example Appendix
One row per **study × outcome × race/ethnicity group × (registry/period)** estimate:

| Field | Notes |
|---|---|
| Lead author, year · PMID/DOI | provenance |
| Data source / registry · **registry family** | SEER / NAACCR / USCS / state (→ overlap table) |
| Region / coverage | national / state / county |
| Diagnosis period | calendar years |
| **Standard population** | e.g., 2000 US standard (see §4) |
| Outcome | invasive incidence / subtype (TNBC, HR±/HER2±) / age-band / nativity |
| Exposure group (as reported) → **harmonized group** | see §2 |
| Comparator (as reported) → harmonized | must resolve to NHW (see §2) |
| Age group | all-ages age-adjusted / specific band |
| Model | crude vs age-adjusted vs further-adjusted (see §3) |
| Effect type | IRR / RR (age-adjusted rate ratio) |
| Minority rate; NHW rate (per 100,000) | with each rate's 95% CI if given |
| Estimate (95% CI) | as reported |
| Case counts / person-years | if given (for SE) |
| **CI / effect source** | directly-reported / rate-derived / figure-extracted / approximated (→ §5, Table S-A) |
| Source location | table/figure no. + page |

---

## 2. Terminology unification (feedback #7, line 58)
"Unify" means two things at once: **(a)** use **one canonical label set** consistently
throughout the manuscript, tables, and figures (defined once in Methods), and **(b)**
map each study to a canonical label **by what the study actually measured** — never
relabel a study into a category its definition does not fit. So a mismatch is not just
flagged and left; the flag triggers a **handling rule** (below) and the handling is
part of the unification.

### Canonical vocabulary (defined once, used everywhere)
- **NHW** = non-Hispanic White — the reference group.
- **NH Black** = non-Hispanic Black.
- **Hispanic** = Hispanic/Latino/Latina/Latinx (of any race).
- **Asian/PI (aggregate)** — and, kept **separate**, the disaggregated subgroups:
  Chinese, Japanese, Korean, Filipino, Vietnamese, Asian Indian, Native Hawaiian,
  other Pacific Islander.
- **AIAN** = American Indian/Alaska Native, with **IHS-linked / misclassification-
  corrected** vs **registry-only** kept as distinct sub-labels.
- **Nativity:** US-born vs foreign-born kept separate from the pooled group.

The manuscript uses **only these labels** — no switching between "Black" and
"non-Hispanic Black", "White"/"NHW", or "API"/subgroup synonyms within the text.

### Mapping + handling when a study's definition does not match the canonical one
For each reported group, map to the canonical label by the study's true definition.
When the definition does **not** match (e.g., the study's "White" includes Hispanic
White, or its "Black" includes Hispanic Black):
1. **Prefer a conforming version from the same study.** If the study also reports the
   canonical version (e.g., non-Hispanic White rates), **use that** and map cleanly.
   *(This resolves most cases.)*
2. **Otherwise do not relabel it into the canonical category.** Instead either:
   - (a) keep it under an **honest distinct label** (e.g., "White, incl. Hispanic")
     and **do not pool it** with NHW-referenced estimates; or
   - (b) **exclude it from the primary pool** and report it in a **sensitivity
     analysis / narratively**.
3. **Record the decision** (which option, and why) in the row.

### Rules that always hold
- **Reference must be NHW.** A comparator that is not non-Hispanic White is handled by
  the rule above, not silently treated as NHW.
- **Asian/PI aggregate and its subgroups are never pooled together**, and a subgroup
  is never merged into the aggregate within one pool — that separation is the review's
  central point. Record whether an aggregate includes Pacific Islanders.

A harmonization key (raw label → canonical label · match? · handling decision) is
saved with the extraction sheet so every mapping is auditable.

---

## 3. Estimate-selection rules (when a study reports more than one)
Only **one estimate per study × outcome × group enters a given pool** (no double
counting). Choose, in order:
1. **Age-adjusted invasive incidence** over crude or non-age-adjusted. Do **not** mix
   crude and age-adjusted estimates in the same pool.
2. **Directly reported IRR/RR (with 95% CI)** over a rate-derived one, when both exist.
3. If multiple **calendar periods**: use the **most recent complete period** for the
   primary analysis; earlier periods enter only a trend/sensitivity view, never the
   same pool.
4. If multiple **registries/regions** within one study: apply the registry-family
   rule (most comprehensive coverage) — see `REGISTRY_OVERLAP_PLAN.md`.
5. If both **crude and model-adjusted** are given: the estimand is age-standardized
   incidence, so use the **age-adjusted** rate; note any further adjustment under
   Comparability (NOS), do not pool adjusted with unadjusted.

Every choice (and the rejected alternatives) is noted in the row so it is auditable.

---

## 4. Standard-population & comparability check (feedback #6, line 43)
Before computing or pooling a rate ratio, confirm the minority and NHW figures share:
- the **same standard population** (e.g., 2000 US standard) — record it;
- an **overlapping diagnosis period**;
- the **same registry/source**.

If a study mixes standard populations, periods, or comparator definitions, **flag it**
and, where it affects the estimate, **exclude that rate ratio in a sensitivity check**
rather than pooling it silently. (Feeds Table S-A "age-standardization" column.)

---

## 5. Effect measure & SE-derivation rules (feedback #6, line 42)
Pooling is on the **log rate-ratio** scale. Each estimate is tagged by **how it was
obtained**, and the SE is derived by the matching rule (function names are the ones in
`run_meta_analysis_breast.py`):

| CI / effect source | Rule | Function |
|---|---|---|
| **Directly reported IRR/RR + 95% CI** | SE from the reported CI | `se_from_ci(irr, lo, hi)` |
| **Rate-derived** (two age-adjusted rates, each with its own 95% CI) | IRR = minority÷NHW rate; SE propagated from both rate CIs | `irr_from_rates` + `se_logirr_from_rate_cis` |
| **Rates without CI** (only point rates) | Poisson SE approximated from rates/person-years | `se_from_rates` — **flag "approximated"** |
| **Case counts available** | SE of log-RR from counts | `se_logrr_from_counts` |
| **Figure-only** (read off a plot) | extract value; **flag "figure-extracted"** | (record read method) |

- The tag is recorded in the **CI/effect source** field (→ Table S-A) and drives
  **sensitivity S-1** (restrict to directly-reported effects only).
- Rates are per **100,000 person-years**; keep units consistent.

---

## 6. Process & provenance
- **Single reviewer + AI first pass**; the reviewer verifies **every value** against
  the source PDF (table/figure + page recorded in the row and in `EXTRACTION_LOG.md`).
- Rules in this manual are fixed before extraction; if a genuinely new situation
  arises, add a rule here rather than deciding ad hoc.
- The completed sheet is transcribed into `STUDIES` (one `Study(...)` per row), so the
  analysis code and the extraction sheet stay in one-to-one correspondence.
