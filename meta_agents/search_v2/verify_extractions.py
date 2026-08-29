#!/usr/bin/env python3
"""Census check of every extracted value in the ledger against its source PDF.

For each ledger row, pull the source PDF text (main + any *_supple), then look for
the value that was actually READ from the source:
  - directly-reported-IRR / -SIR  -> the IRR itself
  - everything else (rates)        -> the minority rate, and the NHW rate when the
                                      paper supplies it (not an external anchor)
Whitespace-insensitive substring search (many tables extract as run-together text).
Output: VERIFIED where the value is found; a FLAG otherwise (no PDF, or value not in
the extractable text = image table / supplement-only / needs a human).
"""
import csv, os, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
FT = os.path.join(HERE, "fulltext")

try:
    import pdfplumber
except ImportError:
    raise SystemExit("pdfplumber required")

_cache = {}
def pdftext(rid):
    if rid in _cache:
        return _cache[rid]
    parts = []
    for path in [os.path.join(FT, "%s.pdf" % rid)] + sorted(glob.glob(os.path.join(FT, "%s_supple*.pdf" % rid))):
        if os.path.exists(path):
            try:
                with pdfplumber.open(path) as p:
                    parts.append("\n".join((pg.extract_text() or "") for pg in p.pages))
            except Exception as e:
                parts.append("")
    t = "\n".join(parts)
    _cache[rid] = t
    return t

def has(text, val):
    """substring match, tolerant of whitespace removed by table extraction."""
    val = (val or "").strip()
    if not val:
        return None
    if val in text:
        return True
    # whitespace-stripped compare
    return val in re.sub(r"\s+", "", text)

EXTERNAL_NHW = ("external", "seer-explorer", "inferred")  # NHW not from this paper

def main():
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "breast_extraction.csv"), encoding="utf-8"))
            if r["record_id"] != "SEER-EXPL"]
    verified, flags = [], []
    for r in rows:
        rid = r["record_id"]
        prov = r.get("provenance", "")
        t = pdftext(rid)
        if not t:
            flags.append((rid, r["author_year"], r["minority_group"], r["outcome_dim"], "NO PDF / unreadable"))
            continue
        # which value(s) prove the extraction?
        checks = []
        if prov in ("directly-reported-IRR", "directly-reported-SIR"):
            checks.append(("IRR", r.get("irr")))
        else:
            checks.append(("min_rate", r.get("minority_rate")))
            note = (r.get("notes", "") + r.get("std_pop", "")).lower()
            if r.get("nhw_rate") and not any(k in note for k in EXTERNAL_NHW):
                checks.append(("nhw_rate", r.get("nhw_rate")))
        results = [(lbl, has(t, v), v) for lbl, v in checks if v]
        if results and all(res is True for _, res, _ in results):
            verified.append(rid)
        else:
            missing = ", ".join("%s=%s" % (lbl, v) for lbl, res, v in results if res is not True)
            flags.append((rid, r["author_year"], r["minority_group"], r["outcome_dim"], "not found: " + missing))
    print("=== EXTRACTION CENSUS: %d rows, %d verified, %d flagged ===" % (len(rows), len(verified), len(flags)))
    print()
    print("FLAGGED (need author / not text-verifiable):")
    # group flags by record for readability
    seen = {}
    for rid, ay, grp, dim, why in flags:
        seen.setdefault((rid, ay, why.split(":")[0]), []).append((grp, dim, why))
    for (rid, ay, _), items in sorted(seen.items(), key=lambda x: int(x[0][0]) if x[0][0].isdigit() else 0):
        why = items[0][2]
        n = len(items)
        print("  rec %-5s %-24s [%d row%s] %s" % (rid, ay[:24], n, "s" if n > 1 else "", why[:70]))

if __name__ == "__main__":
    main()
