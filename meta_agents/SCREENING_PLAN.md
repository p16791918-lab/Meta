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

**Screening — title/abstract** → Records screened (n); Records excluded (n), by reason:
| code | reason (as shown in PRISMA) |
|---|---|
| TA1 | Not breast cancer |
| TA2 | Not an incidence outcome (mortality / survival / prevalence / screening / stage / treatment only) |
| TA3 | Not a US population |
| TA4 | Not reported by race/ethnicity |
| TA5 | Wrong publication type (review, editorial, letter, comment, conference abstract, news) |
| TA6 | Not a primary population-based/registry study |

**Eligibility — full text** → Reports sought (n); not retrieved (n); assessed (n);
Reports excluded (n), by reason:
| code | reason (as shown in PRISMA) |
|---|---|
| FT1 | Outcome not age-adjusted invasive incidence (e.g., mortality-to-incidence ratio, in-situ only, stage-specific only) |
| FT2 | No non-Hispanic White reference group |
| FT3 | No extractable rates or rate ratios (figure-only / annual-percent-change only) |
| FT4 | Non-US study |
| FT5 | Male breast cancer / not female |
| FT6 | Duplicate or overlapping report of an already-included dataset |
| FT7 | Full text unavailable |

**Included** → Studies included in review (n); in quantitative synthesis (n);
narrative synthesis (n).

## Decision log schema (`screening_decisions.csv`)
`record_id, source_db, title, doi, pmid, stage (TA/FT), decision (include/exclude),
reason_code, note`
- One row per record. `reason_code` empty when include.
- Counts per reason_code → the PRISMA numbers, directly.

## Notes tied to supervisor feedback
- **Registry overlap is NOT a PRISMA exclusion.** Overlapping registry studies are
  still "included"; the one-estimate-per-registry-family selection for the primary
  analysis is documented in a separate Supplementary table (feedback item 5), not
  in the PRISMA flow.
- **"Not a US population" (TA3 / FT4):** the review is **US-only (confirmed)**.
  Non-US studies are excluded and counted here — the earlier draft kept some non-US
  as narrative international comparison, but under the confirmed US-only scope they
  are excluded, not retained as narrative.
- The reason lists are fixed **before** screening so tallies are consistent; if a
  new reason is genuinely needed, add a code rather than reusing a vague one.
