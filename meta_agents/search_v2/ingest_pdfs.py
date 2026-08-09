#!/usr/bin/env python3
"""Ingest manually downloaded PDFs into the full-text set.

Drop each manually retrieved PDF into  fulltext_pdf/<record_id>.pdf
(record_id is the first column of manual_download_needed.csv), then run this.
It extracts text and writes fulltext/<record_id>.txt in the same format the
fetch script uses (SOURCE: manual-pdf), so eligibility/extraction is uniform.

Run in the Codespace (needs pypdf) OR in the web session (no network needed —
PDF parsing is local):
    pip install pypdf
    python3 ingest_pdfs.py

Reports which record_ids were ingested, which PDFs failed to parse, and which
manual records still have no PDF.
"""
import csv
import os
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
PDFDIR = os.path.join(HERE, "fulltext_pdf")
OUTDIR = os.path.join(HERE, "fulltext")
MERGED = os.path.join(HERE, "merged_unique.csv")
MANUAL = os.path.join(HERE, "manual_download_needed.csv")


def pdf_to_text(path):
    try:
        import pypdf
        reader = pypdf.PdfReader(path)
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception:
        pass
    try:
        from pdfminer.high_level import extract_text
        return extract_text(path)
    except Exception:
        return None


def main():
    os.makedirs(PDFDIR, exist_ok=True)
    os.makedirs(OUTDIR, exist_ok=True)
    recs = list(csv.DictReader(open(MERGED, encoding="utf-8")))

    # Accept PDFs in either fulltext_pdf/ or directly in fulltext/ (named <id>.pdf).
    pdfs = sorted(set(glob.glob(os.path.join(PDFDIR, "*.pdf"))
                      + glob.glob(os.path.join(OUTDIR, "*.pdf"))))
    if not pdfs:
        print("no PDFs found in %s or %s — save each as <record_id>.pdf and re-run."
              % (PDFDIR, OUTDIR))
        return

    ingested, failed = [], []
    for path in pdfs:
        base = os.path.splitext(os.path.basename(path))[0]
        if not base.isdigit():
            print("skip (name not a record_id): %s" % os.path.basename(path))
            continue
        rid = int(base)
        text = pdf_to_text(path)
        if not text or len(text) < 400:
            failed.append(rid)
            print("FAILED to extract text: %s.pdf (%d chars)" % (rid, len(text or "")))
            continue
        rec = recs[rid] if 0 <= rid < len(recs) else {}
        with open(os.path.join(OUTDIR, "%d.txt" % rid), "w", encoding="utf-8") as f:
            f.write("record_id=%d pmid=%s doi=%s\nSOURCE: manual-pdf\nTITLE: %s\n\n%s\n"
                    % (rid, rec.get("pmid", ""), rec.get("doi", ""), rec.get("title", ""), text))
        ingested.append(rid)
        print("ingested rec %-4d  %6d chars  %s" % (rid, len(text), rec.get("title", "")[:50]))

    print("\n=== summary ===")
    print("ingested : %d" % len(ingested))
    print("failed   : %d  %s" % (len(failed), failed))

    # Which manual records still lack a full text?
    if os.path.exists(MANUAL):
        manual_ids = [int(r["record_id"]) for r in csv.DictReader(open(MANUAL, encoding="utf-8"))]
        have = {int(os.path.splitext(os.path.basename(p))[0])
                for p in glob.glob(os.path.join(OUTDIR, "*.txt"))
                if os.path.splitext(os.path.basename(p))[0].isdigit()}
        still = [i for i in manual_ids if i not in have]
        print("manual records still WITHOUT full text: %d" % len(still))
        if still:
            print("  ", still)


if __name__ == "__main__":
    main()
