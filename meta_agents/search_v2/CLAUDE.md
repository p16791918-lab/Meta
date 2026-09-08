# Project working rules — breast-cancer racial/ethnic incidence SR/MA

**Two standing premises for all manuscript work:**

1. **The supervisor's feedback is the governing premise (대전제).** Four files apply:
   `Advice/Feedback` (1st round), `Advice/Feedback2.md` (2nd round), `Advice/Feedback3.md`
   (3rd round), and `Advice/Feedback4.md` (4th round). Re-read all before drafting or revising;
   if anything conflicts, the feedback wins, and a later round wins over an earlier one.
   (2nd round: remove GRADE; RoB via JBI not NOS with ≥2 independent reviewers;
   distinguish 163 included / 48 quant-eligible / 43 extractable; add study-design column and
   stop calling studies "cohort"; overlapping-registry pooling is sensitivity-only, not primary;
   present the representative as a "population-based benchmark", not a pooled estimate; verify all
   derived IRRs from one master dataset. 3rd round: systematic review with quantitative synthesis
   not meta-analysis; analytic cell = group × dimension; RoB↔sensitivity consistency; unify
   study-selection (single-reviewer + AI); drop male BC; NHW vs unstratified White; provenance
   tiers; 43/5/115 classification; AI/AN undercount vs selection-rule wording; simplify
   Discussion; strengthen Figs 2–3. 4th round: fix AI/AN source classification (Gopalani 2020 =
   CDC WONDER/USCS, not IHS-PRCDA) and re-verify representatives/RoB/sensitivity; consistent
   inclusion/assignment/selection rules with per-study extractable+selection log; re-verify
   comparator/period/age/effect-measure against sources; reconsider Poisson-CI on
   age-standardized ratios; fix "standard population largely cancels" and "contemporary
   benchmark"; complete narrative-synthesis themes and review-process reporting (LLM role,
   PROSPERO status, JBI Q9); state the review's contribution; de-AI the docx formatting
   (black headings, plain styles, no decorative table fills, move blurbs to a Note).)
2. **Write source-grounded, non-AI-sounding prose per `manuscript/WRITING_GUIDE.md`.** Read the
   source paper before writing a factual sentence; tie every quantitative claim to a reference
   read in full or extracted into the ledger; use concrete figures and named studies; vary
   sentence length; no rhetorical/absolute wording, no LLM clichés, no first-person singular;
   unify terminology (NHW/NHB/AANHPI/NHPI/AI/AN/TNBC).

Key paths: ledger `breast_extraction.csv`; display labels `labels.py`; deliverable generators
`make_*.py` → `outputs/build_*_docx.js`; drafts in `manuscript/`; source PDFs in `fulltext/<rec>.pdf`.
Work on branch `claude/usage-question-q3vm84`; commit and push after each meaningful change.
