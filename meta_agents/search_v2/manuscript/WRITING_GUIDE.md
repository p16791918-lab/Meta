# Manuscript Writing Guide — standing rules

**Premise (대전제):** the supervisor's `Advice/Feedback` governs everything. When any
instruction here conflicts with that file, the Feedback wins. Re-read `Advice/Feedback`
and `Advice/Manuscript.docx` (flow reference) before drafting a new section.

This guide applies to every section we still have to write (Abstract, Methods, Results,
Discussion) and to any revision of the Introduction. It codifies the method used for the
Introduction rewrite (v9).

---

## A. Source-grounded drafting (do this every time)

1. **Read before writing.** Read the source paper's full text (`fulltext/<rec>.pdf`) or use
   our own extraction. Do **not** write a factual sentence from a title or abstract match.
2. **Tie every quantitative claim to a read/extracted reference.** If we have not confirmed
   the source, either drop the claim or drop the citation — never assert "✅ verified" for a
   study we only screened. Keep a per-reference *Source check* column (full text / extracted /
   screened-only).
3. **Concrete over abstract.** Prefer real figures and named studies
   ("Gomez and colleagues reported 146 vs 83 per 100,000") to smooth multi-citation synthesis
   ("rates differ across groups³⁻⁶").
4. **Distribute citations** to the specific claim each supports; avoid long bundled
   superscripts when a specific attribution is possible.

## B. Tone (the supervisor flagged AI-sounding prose — avoid it)

5. **No rhetorical / loaded verbs:** mask, conceal, obscure, reveal, dissolve, misleading,
   indictment, underscore, highlight, stark, striking, profound, alarming.
6. **No absolutes:** every, all, none, no single study, "did not change any conclusion."
   State only what the results support, hedged ("about", "tended to").
7. **Kill LLM clichés:** "to our knowledge … has not been assembled", "attributed to
   differences in", "differ severalfold", "plays a crucial role", "sheds light on",
   "a growing body of evidence", "it is important to note."
8. **Vary sentence length deliberately** — mix short declaratives with longer sentences.
   Uniform cadence is the main tell.
9. **Voice:** first-person plural **We** or the passive ("Data were extracted",
   "A systematic search was conducted"). Never first-person singular *I*.
10. **Say each point once** in the place it belongs; do not repeat the same claim (e.g. the
    aggregation point) across Abstract/Intro/Results/Discussion.

## C. Terminology (unify to the Abbreviations table)

11. Use **NHW, NHB, AANHPI, NHPI, AI/AN, TNBC, IRR, SIR, SEER, IHS**; define each on first
    use, then use the abbreviation. No deprecated terms (API, Asian/Pacific Islander, bare
    Blacks/Whites). Where a source used a "White" (not NH-stratified) comparator, say so
    plainly rather than smoothing it to NHW.

## D. Statistics & interpretation (Feedback §6 — hard constraints)

12. Do **not** present a pooled random-effects IRR, I², or τ² as a primary result (2nd-round
    feedback §5): estimates within a group come from overlapping/nested registry populations
    and are not independent. The primary result is one representative population-based estimate
    per registry family; any pooling is at most a secondary consistency/sensitivity check.
13. Do **not** describe the representative estimate as a meta-analytic pooled value (2nd-round
    feedback §6): call it a "representative population-based estimate" or "contemporary
    benchmark," and state its selection criteria.
14. Keep provenance explicit: directly-reported IRR vs computed-from-rates vs figure-extracted
    vs approximate SE. Confirm same standard population, period, and comparator before
    computing a rate ratio.
15. Do **not** call age-standardization itself an artefact; say the overall age-standardized
    result may not capture age-specific differences.
16. Do **not** connect observed racial/ethnic differences to genetic ancestry or a specific
    biological mechanism; limit to possible explanation / hypothesis, and only for things the
    included studies actually assessed.

## E. Section structure (Feedback §7)

- **Introduction:** background → limitations of prior work → objective. Concise.
- **Methods:** only what was actually done. Do not defend search/analysis choices at length.
- **Results:** numbers and objective findings, not interpretation.
- **Discussion:** key results → comparison with prior work → possible explanations →
  clinical / public-health meaning → strengths and limitations → conclusion.

## F. Workflow

- Draft in `manuscript/<Section>_draft.md`; commit after each meaningful change; push to the
  working branch; send the file to the user for review.
- Method-guideline citations (PRISMA 2020 and the JBI prevalence/incidence appraisal checklist)
  go in Methods. GRADE and the Newcastle–Ottawa Scale were dropped in the 2nd-round revision.
