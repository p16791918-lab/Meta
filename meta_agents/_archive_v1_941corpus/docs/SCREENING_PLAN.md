# Screening plan — exclusion reasons & counts for the PRISMA 2020 flow

Modeled on the example PRISMA (Advice/PRISMA flowchart.pptx), every excluded
record is tagged with **one reason category** so the flow diagram shows
"reason (n=…)". Screening is two-stage; each stage has its own reason list.
Decisions are written to a log (`screening_decisions.csv`) so counts are automatic
and author-verifiable.

## PRISMA boxes we must fill

**Identification**
- Records identified per database: PubMed/MEDLINE (n), Embase (n), Scopus (n),
  Web of Science (n) — total (n)
- Records removed before screening: duplicate records removed (n)
  *(and, if applicable, records removed by document-type filter (n))*

The PRISMA figure shows a **short list of reasons** like the example
(Advice/PRISMA flowchart.pptx), which collapses everything off-topic into
"Not relevant to the research question/topic." We do the same: the figure uses the
**display categories** below, while the decision log keeps a **fine sub-reason** for
each record (traceability), and the fine reasons roll up into the display category.

**Screening — title/abstract** → Records screened (n); Records excluded (n), by reason:
| display category (shown in PRISMA) | fine sub-reasons rolled up (log only) |
|---|---|
| **Not relevant to the research question/topic** | not breast cancer · not an incidence outcome (mortality/survival/prevalence/screening/stage/treatment) · not reported by race/ethnicity |
| **Not a US population-based/registry study** | non-US population · not a primary population-based/registry study |
| **Editorials, commentaries, letters, or conference abstracts** | review · editorial · letter · comment · conference abstract · news |

**Eligibility — full text** → Reports sought (n); not retrieved (n); assessed (n);
Reports excluded (n), by reason:
| display category (shown in PRISMA) | fine sub-reasons rolled up (log only) |
|---|---|
| **Did not report the outcome of interest** | outcome not age-adjusted invasive incidence (mortality-to-incidence ratio, in-situ only, stage-specific only) · no non-Hispanic White reference group · no extractable rates or rate ratios (figure-/APC-only) |
| **Ineligible population** | non-US study · male breast cancer / not female |
| **Overlapping or duplicate dataset** | duplicate/overlapping report of an already-included dataset |
| **Full text unavailable** | report not retrievable in full text |

**Included** → Studies included in review (n); in quantitative synthesis (n);
narrative synthesis (n).

## Decision log schema (`screening_decisions.csv`)
`record_id, source_db, title, doi, pmid, stage (TA/FT), decision (include/exclude),
display_reason, sub_reason, note`
- One row per record. `display_reason`/`sub_reason` empty when include.
- `display_reason` ∈ the categories above → drives the PRISMA figure counts.
- `sub_reason` is the fine detail → keeps the decision auditable without cluttering
  the figure.
- `decision` also accepts `dup` for records removed as duplicates before screening
  (counted in the "duplicate records removed" box, not screened).

**Auto-tally:** `python3 tally_prisma.py screening_decisions.csv` reads this log and
prints every PRISMA number — per-database identification, duplicates removed,
records screened/excluded with per-category counts (TA), reports assessed/excluded
with per-category counts (FT), and studies included — and flags any `display_reason`
that isn't one of the fixed categories. So the counts fall out of the log
automatically; they are not tallied by hand. (Like the example paper, only these
aggregate counts go in the flowchart; the per-record log stays as internal,
author-verifiable backing.)

## Notes tied to supervisor feedback
- **Registry overlap is NOT a PRISMA exclusion.** Overlapping registry studies are
  still "included"; the one-estimate-per-registry-family selection for the primary
  analysis is documented in a separate Supplementary table (feedback item 5), not
  in the PRISMA flow. ("Overlapping or duplicate dataset" at full text means a
  *duplicate report of the same study/dataset*, e.g. a re-publication — not two
  distinct studies that happen to share registry data.)
- **US-only scope (confirmed):** non-US records are excluded — at title/abstract they
  fall under "Not a US population-based/registry study," at full text under
  "Ineligible population." The earlier draft kept some non-US as narrative
  international comparison; under the confirmed US-only scope they are excluded, not
  retained as narrative.
- The display categories and their roll-up are fixed **before** screening so tallies
  are consistent; if a genuinely new sub-reason appears, add it under the right
  display category rather than inventing a vague new bucket.
