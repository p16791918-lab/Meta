# Registry overlap → representative-study selection (supervisor feedback #5)

Overlapping registry studies are **kept at screening** (not excluded). After
full-text review, each included study is characterized in a table; overlap is
identified; and **one representative estimate per registry family** is chosen for
the **primary** analysis. All-studies and overlap-excluded analyses are reported as
sensitivity checks. A Supplementary table records overlap, primary-inclusion, and
the selection reason for every study.

## Step 1 — Supplementary Table S-A: study characterization (overlap detection)
One row per study (split into extra rows if a study reports from >1 registry). This
is the table feedback item 5 (line 30) asks for — it makes overlap visible — and it
also carries the CI-source distinction feedback item 6 (line 42) requires.

| Study (author, year) | Data source / registry | Registry family | Region / coverage | Diagnosis period | Age range | Race/ethnicity groups reported | Outcome(s) reported | Age-standardization (standard population) | Effect measure & CI source¹ | Sample size / person-years |

¹ **CI/effect source** — one of: `directly-reported IRR/RR (95% CI given)` ·
`rate-derived IRR (computed from two age-adjusted rates)` · `figure-extracted` ·
`approximated SE`. (Distinguishing these is required by feedback item 6.)

## Step 2 — Registry families (for detecting overlap)
- **USCS** ⊇ **NAACCR** ⊇ **SEER** (national aggregators; USCS ≈ full US, NAACCR
  ~93%, SEER subset)
- **SEER** ⊇ regional SEER registries (e.g., **Los Angeles County**, **Greater
  California**, **Hawaii**, **Connecticut**)
- **State/regional registries** (e.g., California Cancer Registry ⊇ LA County;
  Wisconsin; Pennsylvania) — may overlap SEER where the state is a SEER site
- **IHS-linked AIAN** analysis — distinct correction layer (kept separately)

Two studies overlap when they draw on the **same underlying registry data for the
same outcome, race/ethnicity group, and an overlapping calendar period**.

## Step 3 — Representative-study selection criteria (per feedback)
Within each set of overlapping studies (for a given outcome × group), pick the ONE
study with, in order of priority:
1. **Most comprehensive coverage** (national/state > regional > county) for that
   question — but the most *specific* source is preferred for disaggregated
   subgroups only available regionally;
2. **Largest sample / person-years**;
3. **Most recent or longest** diagnosis period;
4. **Clear/explicit age-standardization** method (e.g., 2000 US standard);
5. **Directly reported 95% CI** (over computed/approximated).

Different outcomes may use different representative studies (overall incidence,
molecular subtype, age-specific, ethnic subgroup), but the **same registry data
must not be counted twice for the same question**.

## Step 4 — Analyses
- **Primary:** one estimate per registry family (the representatives).
- **Sensitivity A:** all eligible studies included (as-is).
- **Sensitivity B:** exclude studies with high overlap potential (keep only the
  cleanest, non-overlapping sources).
- Compare direction/magnitude across the three.

## Step 5 — Supplementary Table S-B: overlap + representative-study selection
Feedback item 5 (line 34) requires this table to show, for every study: **overlap
potential**, **inclusion in the primary analysis**, and the **selection reason**.
Modeled on the example paper's assessment table (structured per-criterion columns +
an overall decision), the reason is broken into the five selection criteria so the
choice is transparent — not a free-text assertion.

**Unit = one row per question (outcome × race/ethnicity subgroup) × study**, because
the same study can be the representative for one question and excluded for another
(feedback line 32: the same registry data must not be counted twice for the *same*
question).

| Question (outcome × subgroup) | Study (author, year) | Registry family | Region / period (overlap drivers) | Overlap potential² | Overlaps with (study) | C1 coverage | C2 sample | C3 period | C4 age-std | C5 CI direct³ | Included in primary? (Y/N) | In Sens A (all) | In Sens B (overlap-excluded) | Reason for selection / exclusion |

² **Overlap potential** — `None` / `Partial` / `High`, judged from shared registry
family + overlapping region + overlapping calendar period for the same question.
³ **C1–C5** = the five selection criteria (Step 3): most comprehensive coverage,
largest sample/person-years, most recent-or-longest period, clear age-standardization,
directly reported 95% CI. Mark ✓ / – for the chosen representative vs the others so
the winning criterion is visible.

**Mapping to feedback:** 중복 가능성 → *Overlap potential* + *Overlaps with*;
주 분석 포함 여부 → *Included in primary?* (+ Sens A / Sens B membership);
대표연구 선정 이유 → *C1–C5 marks* + *Reason*.

---
**Scope (confirmed):** the review is **US-only**. Non-US studies (e.g., UK) are
**excluded** at screening (codes TA3 / FT4) and are **not** retained as narrative
international comparison. They therefore do not appear in Tables S-A / S-B; they are
counted only in the PRISMA exclusion tally.
