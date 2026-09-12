# Archive — v1 (941-record PubMed+Embase corpus)

Superseded first-pass systematic review and meta-analysis, kept for provenance
only. **Do not use in the current review.** The active work is in
`meta_agents/search_v2/` (the 4-database, 4,793-record corpus).

- `code/`       — v1 pipeline (agent_*.py, orchestrator.py, run_meta_analysis*.py, helpers, shared/)
- `data/`       — v1 raw/merged records (part1/2.csv, records_tabular.csv, manual_decisions.csv)
- `docs/`       — v1 plans, logs, checklists, reviewer responses
- `manuscript/` — v1 manuscript + submission package + figures
- `outputs/`    — v1 timestamped run outputs
- `fulltext_v1/`— v1 full-text cache (gitignored)

NOTE: run_meta_analysis_breast.py here is the source of the earlier "migrated"
values. Those were purged from the current ledger; the current analysis
extracts every estimate directly from search_v2 source (see search_v2/DATA_AUDIT.md).
