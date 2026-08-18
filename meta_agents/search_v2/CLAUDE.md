# Project working rules — breast-cancer racial/ethnic incidence SR/MA

**Two standing premises for all manuscript work:**

1. **The supervisor's feedback is the governing premise (대전제).** Two files apply:
   `Advice/Feedback` (1st round) and `Advice/Feedback2.md` (2nd round). Re-read both before
   drafting or revising; if anything conflicts, the feedback wins, and the 2nd round wins over
   the 1st. (2nd round: remove GRADE; RoB via JBI not NOS with ≥2 independent reviewers;
   distinguish 163 included / 48 quant-eligible / 43 extractable; add study-design column and
   stop calling studies "cohort"; overlapping-registry pooling is sensitivity-only, not primary;
   present the representative as a "population-based benchmark", not a pooled estimate; verify all
   derived IRRs from one master dataset.)
2. **Write source-grounded, non-AI-sounding prose per `manuscript/WRITING_GUIDE.md`.** Read the
   source paper before writing a factual sentence; tie every quantitative claim to a reference
   read in full or extracted into the ledger; use concrete figures and named studies; vary
   sentence length; no rhetorical/absolute wording, no LLM clichés, no first-person singular;
   unify terminology (NHW/NHB/AANHPI/NHPI/AI/AN/TNBC).

Key paths: ledger `breast_extraction.csv`; display labels `labels.py`; deliverable generators
`make_*.py` → `outputs/build_*_docx.js`; drafts in `manuscript/`; source PDFs in `fulltext/<rec>.pdf`.
Work on branch `claude/usage-question-q3vm84`; commit and push after each meaningful change.
