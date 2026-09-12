#!/usr/bin/env python3
"""Contamination guard: assert the extraction ledger contains ONLY records that
are include-quant in THIS review's full-text eligibility (search_v2). Prevents
values from any prior/other corpus from entering the analysis.
Exits non-zero and lists offenders if any are found. Import check_ledger() from
the analysis scripts, or run standalone.
"""
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def v2_quant_ids():
    p = os.path.join(HERE, "ft_eligibility.csv")
    return {r["record_id"] for r in csv.DictReader(open(p, encoding="utf-8"))
            if r["ft_decision"] == "include-quant"}

def check_ledger(path=None, allow={"SEER-EXPL"}):
    path = path or os.path.join(HERE, "breast_extraction.csv")
    ok = v2_quant_ids() | allow
    bad = {}
    for r in csv.DictReader(open(path, encoding="utf-8")):
        rid = r["record_id"]
        if rid not in ok:
            bad.setdefault(rid, 0)
            bad[rid] += 1
    return bad

if __name__ == "__main__":
    bad = check_ledger()
    if bad:
        print("CONTAMINATION: non-v2-include-quant records in ledger:")
        for rid, n in sorted(bad.items()):
            print("  record_id=%r : %d rows" % (rid, n))
        sys.exit(1)
    print("OK: every ledger record is a search_v2 include-quant study.")
