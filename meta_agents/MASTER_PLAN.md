# Master revision plan — Phase 2 (supervisor feedback)

One place that ties every sub-plan to the feedback, shows current → target state, and
marks **who** does each step and **what it depends on**. Detailed methods live in the
linked files; this is the sequencing/checklist. Statuses: ✅ done · 🔜 ready (waiting
on a trigger) · ⏳ blocked on search · ▢ to build.

**Confirmed decisions:** US-only scope (non-US excluded, not narrative) · single
reviewer + AI (values verified against source) · analysis engine = **Python** ·
RoB tool = **Newcastle–Ottawa Scale** · primary model = **REML + Hartung–Knapp**.

---

## Sequence (what unblocks what)
```
A. Search (4 DB)  ──►  B. De-dup + screening  ──►  C. Full-text + registry-overlap table
      │                                                     │
      └─ ready now                                          ▼
                                              D. Representative selection + extraction
                                                            │
                                                            ▼
                                        E. Re-run stats (REML+HK + method compare)
                                                            │
                              ┌─────────────────────────────┼───────────────┐
                              ▼                              ▼               ▼
                     F. NOS risk of bias        G. PRISMA 2020 figure   H. GRADE
                              └─────────────────────────────┼───────────────┘
                                                            ▼
                                              I. Full manuscript rewrite
                                                            │
                                                            ▼
                                      J. Supplementary + submission package
```
PROSPERO amendment (K) runs in parallel — professor's decision, not on this critical path.

---

## A. Search — 4 databases  🔜 (user runs tomorrow) · feedback #2
- Files: `SEARCH_STRINGS_v2.md`, `SEARCH_DAY_CHECKLIST.md`.
- 4 DB: PubMed/MEDLINE · Embase (primary screening corpus) · Scopus · WoS. All race
  terms in **title/abstract(/keyword)**; US-context block AND-ed in.
- **User:** run all four same day, record counts + date, export all four (Title,
  Abstract, Authors, Year, Source, DOI, PMID, DocType), commit to `search_v2/`.
- Output feeds the PRISMA "Identification" box.

## B. De-duplication + two-stage screening  ⏳ (me, after A) · feedback #2/#3
- File: `SCREENING_PLAN.md`. De-dup (DOI → fuzzy title); log per-record decisions to
  `screening_decisions.csv` with reason codes (TA1–6 / FT1–7) so PRISMA counts are
  automatic. **US-only** enforced here (TA3/FT4). Registry overlap is **not** a
  screening exclusion.

## C. Full-text review + registry-overlap characterization  ⏳ · feedback #5
- File: `REGISTRY_OVERLAP_PLAN.md`. Build **Table S-A** (registry family, region,
  period, age, groups, outcome, age-standard, **CI/effect source**, sample). Detect
  overlap across registry families.

## D. Representative selection + extraction  ⏳ · feedback #5
- Pick one estimate per registry family per question (5 criteria). Build **Table S-B**
  (overlap potential, C1–C5 marks, primary inclusion, Sens A/B membership, reason).
- Extract new eligible studies (value verified against source PDF, as before).

## E. Statistics — re-run  ▢ (me, Python) · feedback #6
- File: `STATS_PLAN.md`. Extend `run_meta_analysis_breast.py`: add **REML** + **Hartung–
  Knapp**; produce **Table S-C** (REML+HK primary vs REML+Wald vs DL) — compare, don't
  assert. Report I² with τ² + **prediction interval**; frame high I² as a limit.
  Sensitivity: primary = one-per-family; A = all studies; B = overlap-excluded;
  S-1 = directly-reported effects only. Comparability check before any rate-derived IRR.

## F. Risk of bias — Newcastle–Ottawa  ▢ · feedback #4
- Replace the custom scheme in `rob_assessment.py` with **NOS** (Selection /
  Comparability / Outcome domains, star system) matching `Advice/Risk of bias…docx`
  Supp Table 3 format. AI does first pass; a few checked by hand. → Table S-D + figure.

## G. PRISMA 2020 flow diagram  ▢ · feedback #3
- Redraw as the two-arm PRISMA 2020 (databases/registers + other methods) with
  per-stage exclusion reasons + counts, matching `Advice/PRISMA flowchart.pptx`.
  Numbers come straight from B.

## H. GRADE certainty  🔜 (script exists) · same as example paper
- `grade_assessment.py` present; re-run on the final pooled set. (AMSTAR-2 is **not**
  used — that is for umbrella reviews; ours includes primary studies → NOS.)

## I. Manuscript rewrite  ▢ (biggest item) · feedback #1/#7
- File to rewrite: `MANUSCRIPT.md`.
- **Title →** "Racial and Ethnic Differences in Breast Cancer Incidence in the United
  States: A Systematic Review and Meta-Analysis" (drop the long conclusory subtitle).
- **Voice:** "We" / passive ("A systematic search was conducted", "Data were
  extracted"); remove first-person singular.
- **De-rhetoric:** delete "conceal / reassuring picture dissolves / quantitative
  indictment / artefact"; soften absolutes (every / all / no single study); state each
  conclusion **once** in the right section.
- **Rewrite from sources, not edits:** re-read the included papers and summarize in own
  words (professor's explicit instruction — item 1 line 8 / 총평).
- **Structure per example:** tight Introduction (background → gap → aim); Methods =
  what was actually done (no long defensive justifications); Results = numbers first;
  Discussion in order **main findings → prior work → possible explanations →
  clinical/public-health implications → strengths & limitations → conclusion**.
- **Terminology:** unify Black vs non-Hispanic Black, White vs NHW, API vs named
  subgroups to each source's definitions (item 7 line 58).
- **Section headers:** replace the current rhetorical headers (e.g. "Aggregate racial
  comparisons conceal…", "reveals a 3-fold spread", "convergence is an age crossover")
  with neutral ones.
- **Declarations:** Generative-AI statement in the example paper's form (supporting
  role, outputs verified, did not determine results); authors as placeholders pending
  approval.

## J. Supplementary + submission package  ▢
- Assemble: S-1 search strategies per DB (platform/date/count) · S-A characterization ·
  S-B overlap/selection · S-C method comparison · S-D NOS · GRADE table. Rebuild figures
  (`make_figures.py`) incl. new PRISMA. Refresh `REFERENCES.md` order-of-appearance.

## K. PROSPERO  🔜 (professor) · feedback #2 · parallel
- File: `PROSPERO_AMENDMENT.md`. Professor amends the lab's 2023 record (CRD kept) to
  the current protocol; 3 decisions pending (reviewer model, scope refinement,
  NRF funding). Cite CRD in Methods once amended.

---

## Division of labor
- **User (tomorrow):** A (search + export) → then hand me the files. Professor: K.
- **Me (after exports):** B → C → D → E → F → G → H → I → J, committing each to the
  branch for your review.
- **You review** each artifact as it lands (this file is the map).

## Open items to confirm
1. Search date (goes in Methods + PROSPERO) — set on search day.
2. Second reviewer? (currently single + AI; affects PROSPERO field + Methods.)
3. NRF-Korea funding — real or "no specific funding"? (aligns paper + PROSPERO.)
4. Author list / order — currently placeholders pending your + professors' approval.
