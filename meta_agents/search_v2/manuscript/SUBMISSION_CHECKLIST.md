# Submission checklist — study-team actions before submitting

These are real actions the manuscript depends on. They are deliberately kept OUT of the
manuscript text itself; the draft prose describes only what was done, with no revision-history
or process commentary.

## Must complete before submission
- [ ] **PROSPERO registration.** Not yet filed. Register the protocol and insert the
      registration number in Methods §Protocol and reporting (a bracketed placeholder is there now).
- [x] **Reviewer process — described as actually performed.** Methods now states that screening,
      full-text selection, extraction, and risk-of-bias appraisal were done by a single reviewer
      (the author) with large-language-model assistance, and that every included study's full text
      was read for the inclusion decision and every extracted estimate verified against its source;
      the absence of a second independent reviewer is stated as a limitation in Methods and the
      Discussion. If a second independent reviewer is added before submission, update this wording
      and report the inter-reviewer agreement.
- [ ] **Reference list — full Vancouver.** `References_draft.md` gives author/year/title/PMID/DOI
      for refs 1–47. Complete journal/volume/pages by importing the PMID block into a reference
      manager (Zotero/EndNote/Mendeley). Two entries have no PMID and are entered manually.

## Optional / conditional
- [x] **Deferred overlap candidates — resolved.** The topic-matched studies previously set aside
      for unconfirmed full text (recs 209, 236, 419, 461, 2137, 4027) were retrieved, extracted,
      and entered in the ledger this round as overlap estimates; the deferred bucket is now empty.
      (An earlier draft of this line named six studies by pre-correction author labels; two of
      those — "Kohler 2015" and "Miller 2021" — are the internal mislabels for Howlader 2014 and
      Hendrick 2021, already included as refs 2 and 3, and the other four are not records in the
      current dataset. See AUTHOR_AUDIT.md.)
- [ ] **Overlapping-registry pooling** was removed entirely (not shown even as a supplementary
      sensitivity). If a reviewer asks to see the I²/heterogeneity artefact of pooling
      non-independent registries, it can be added back as a clearly labelled secondary
      consistency analysis (`meta_analysis_v2.py` still produces it).

## Repo housekeeping (not manuscript)
- [x] `grade_assessment.py`, `forest_pooled.py`, and `outputs/TableS_GRADE.csv/md` deleted
      (GRADE removed in round 2; those files still carried GRADE and the "AI-generated first
      pass" wording, both of which the feedback said to drop).
