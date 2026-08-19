# Submission checklist — study-team actions before submitting

These are real actions the manuscript depends on. They are deliberately kept OUT of the
manuscript text itself; the draft prose describes only what was done, with no revision-history
or process commentary.

## Must complete before submission
- [ ] **PROSPERO registration.** Not yet filed. Register the protocol and insert the
      registration number in Methods §Protocol and reporting (a bracketed placeholder is there now).
- [ ] **Dual-reviewer process.** Methods states that screening and risk-of-bias appraisal were
      done independently by two reviewers with consensus/third-reviewer adjudication. The team
      must actually carry this out (and record the agreement) before submission.
- [ ] **Reference list — full Vancouver.** `References_draft.md` gives author/year/title/PMID/DOI
      for refs 1–47. Complete journal/volume/pages by importing the PMID block into a reference
      manager (Zotero/EndNote/Mendeley). Two entries have no PMID and are entered manually.

## Optional / conditional
- [ ] **Six topic-matched references** were set aside because their full text was not confirmed
      (DeSantis 2019, Cunningham 2010, Satagopan 2021, Gomez 2013, Miller 2021, Kohler 2015).
      Reinstate any whose full text is read and confirmed relevant.
- [ ] **Overlapping-registry pooling** was removed entirely (not shown even as a supplementary
      sensitivity). If a reviewer asks to see the I²/heterogeneity artefact of pooling
      non-independent registries, it can be added back as a clearly labelled secondary
      consistency analysis (`meta_analysis_v2.py` still produces it).

## Repo housekeeping (not manuscript)
- [ ] `grade_assessment.py` and `forest_pooled.py` are dead code (GRADE removed; pooled forests
      removed). Delete when convenient.
