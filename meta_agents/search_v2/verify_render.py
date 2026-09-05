#!/usr/bin/env python3
"""Batch-verify each extracted record's key values against its PDF text (pymupdf)."""
import csv, os, sys
import pymupdf

reps = set()
for r in csv.DictReader(open('TableSA_main_representatives.csv')):
    if r['main_analysis'].startswith('yes'):
        reps.add(r['record_id'])

byrec = {}
for r in csv.DictReader(open('breast_extraction.csv')):
    if r['record_id'] == 'SEER-EXPL':
        continue
    byrec.setdefault(r['record_id'], []).append(r)

done = {'3298', '28', '265', '161', '2510', '286', '587', '522', '324', '485'}


def norm(t):
    return t.replace(',', '').replace(' ', '').replace('\n', '')


def check_val(full, fn, v):
    v = (v or '').strip()
    if not v:
        return None
    if v in full or norm(v) in fn:
        return True
    try:
        f = float(v)
        for cand in ['%.1f' % f, '%.2f' % f, '%.3f' % f, str(round(f, 2)), str(round(f, 1))]:
            if cand in full or norm(cand) in fn:
                return True
    except ValueError:
        pass
    return False


mode = sys.argv[1] if len(sys.argv) > 1 else 'rep'
if mode == 'rep':
    targets = [rid for rid in byrec if rid in reps and rid not in done]
elif mode == 'ovl':
    targets = [rid for rid in byrec if rid not in reps and rid not in done]
else:
    targets = [r for r in sys.argv[1:] if r in byrec]

for rid in sorted(targets, key=int):
    if not os.path.exists('fulltext/%s.pdf' % rid):
        print('rec %s: PDF 없음 (skip)' % rid)
        continue
    doc = pymupdf.open('fulltext/%s.pdf' % rid)
    full = ' '.join(p.get_text() for p in doc)
    fn = norm(full)
    ay = byrec[rid][0]['author_year'][:20]
    miss = []
    for r in byrec[rid]:
        parts = []
        for label, val in [('irr', r['irr']), ('min', r['minority_rate']), ('nhw', r['nhw_rate'])]:
            res = check_val(full, fn, val)
            if res is None:
                continue
            mark = 'OK' if res else 'MISS'
            parts.append('%s=%s[%s]' % (label, val.strip(), mark))
            if not res:
                miss.append((r['minority_group'], r['outcome_dim'], label, val.strip()))
        grp = '%s/%s' % (r['minority_group'][:16], r['outcome_dim'][:14])
        print('  %-34s %s' % (grp, ' '.join(parts)))
    flag = '  <-- MISS 있음' if miss else ''
    print('=== rec %s (%s) done%s' % (rid, ay, flag))
