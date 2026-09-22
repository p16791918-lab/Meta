#!/bin/sh
# Convert the submission documents to PDF, the form the supervisor reads them in.
# Layout faults show up here and not in the .docx: a figure taller than the page
# is silently clipped rather than moved.
#
# Needs LibreOffice WITH Writer. libreoffice-core alone cannot load a .docx (or
# even a .txt) and fails with "source file could not be loaded":
#   apt-get install -y --no-install-recommends libreoffice-writer
set -e
cd "$(dirname "$0")/outputs"
PROFILE="${TMPDIR:-/tmp}/lo-profile-$$"
for f in Manuscript_Full Main_Text_Tables_Figures Supplementary_Materials Feedback5_Response; do
    [ -f "$f.docx" ] || continue
    soffice --headless --norestore -env:UserInstallation="file://$PROFILE" \
            --convert-to pdf --outdir . "$f.docx" >/dev/null 2>&1
    printf '%-32s %s pages\n' "$f.pdf" "$(pdfinfo "$f.pdf" | awk '/^Pages/{print $2}')"
done
rm -rf "$PROFILE"
