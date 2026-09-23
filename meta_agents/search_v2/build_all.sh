#!/bin/sh
# Rebuild every deliverable from the ledger, in dependency order.
#
# Table 1 and the figures are drawn by different scripts, so they agree only if
# the intermediates they share are current. Regenerating one script's output by
# hand and not the others is how the figure came to print an interval Table 1 had
# stopped using. Run this instead: it rebuilds in order, then refuses to write the
# documents unless the cross-check passes.
#
# PDF conversion needs LibreOffice with Writer (see build_pdfs.sh).
set -e
cd "$(dirname "$0")"

echo "--- selection and appraisal"
python3 finalize_representatives.py   # ledger -> locked representatives
python3 rob_assessment.py             # representatives + ledger -> risk of bias
python3 sensitivity_analyses.py       # re-selection under each restriction

echo "\n--- tables and figures"
python3 results_tables.py             # -> Table_main_forest.csv, the figures' data
python3 make_table1.py
python3 prisma_flow.py
python3 forest_main.py                # Figure 2, from Table_main_forest.csv
python3 make_heatmap.py               # Figure 3, from the representatives

echo "\n--- supporting supplements"
# make_author_labels.py is deliberately not here: it re-reads the raw database
# exports to reconcile author names, needs xlrd, and its result is already in the
# ledger. It is a search-stage tool, not part of rebuilding the deliverables.
python3 make_included_supplement.py
python3 make_excluded_supplement.py
python3 make_registry_overlap.py

echo "\n--- manuscript and manifests"
python3 make_maintext.py              # figure sizes read from the regenerated PNGs
python3 make_supplementary.py
python3 assemble_manuscript.py
python3 make_changelog.py             # which paragraphs changed this round, and why

echo "\n--- cross-check (gates the document build)"
python3 crosscheck_master.py

echo "\n--- documents"
cd outputs
for b in build_maintext_docx.js build_supplementary_docx.js build_manuscript_docx.js \
         build_feedback5_docx.js build_changelog_docx.js; do
    [ -f "$b" ] && node "$b"
done
cd ..
./build_pdfs.sh
