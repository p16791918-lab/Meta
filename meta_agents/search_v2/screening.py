#!/usr/bin/env python3
"""Resumable title/abstract screening harness (Stage TA).

record_id = row index in merged_unique.csv (stable while that file is unchanged).
Decisions are appended to screening_decisions.csv so the process resumes after any
interruption. This harness only *presents* records and *records* decisions — the
include/exclude judgement is made by the reviewer (AI first pass, human-verified),
per SCREENING_PLAN.md. No decision is invented here.

Commands:
  python3 screening.py status
  python3 screening.py next [N]            # print next N undecided records
  python3 screening.py apply <batch.csv>   # append validated decisions
  python3 screening.py tally               # PRISMA TA counts by display category
"""
import csv, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
MERGED = os.path.join(HERE, 'merged_unique.csv')
DEC = os.path.join(HERE, 'screening_decisions.csv')

TA_CATS = [
    "Not relevant to the research question/topic",
    "Not a US population-based/registry study",
    "Editorials, commentaries, letters, or conference abstracts",
]
DEC_FIELDS = ['record_id', 'stage', 'decision', 'display_reason', 'sub_reason', 'title']

def load_merged():
    with open(MERGED, newline='', encoding='utf-8', errors='replace') as f:
        return list(csv.DictReader(f))

def load_decisions():
    if not os.path.exists(DEC):
        return {}
    out = {}
    with open(DEC, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            out[r['record_id']] = r
    return out

def cmd_status():
    m = load_merged(); d = load_decisions()
    print(f'unique records : {len(m)}')
    print(f'decided        : {len(d)}')
    print(f'remaining      : {len(m) - len(d)}')
    if d:
        from collections import Counter
        dec = Counter(v['decision'] for v in d.values())
        print('  by decision  :', dict(dec))

def cmd_next(n):
    m = load_merged(); d = load_decisions()
    shown = 0
    for i, r in enumerate(m):
        rid = str(i)
        if rid in d:
            continue
        ab = (r.get('abstract') or '').replace('\n', ' ')
        if len(ab) > 600:
            ab = ab[:600] + '…'
        print(f'### id={rid} | src={r.get("sources","")} | type={r.get("doctype","")} | year={r.get("year","")}')
        print(f'T: {r.get("title","")}')
        print(f'A: {ab if ab else "(no abstract)"}')
        print()
        shown += 1
        if shown >= n:
            break
    if shown == 0:
        print('*** no undecided records remain ***')

def cmd_apply(path):
    m = load_merged()
    titles = {str(i): r.get('title', '') for i, r in enumerate(m)}
    existing = load_decisions()
    added = 0
    new_file = not os.path.exists(DEC)
    with open(path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    with open(DEC, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=DEC_FIELDS)
        if new_file:
            w.writeheader()
        for r in rows:
            rid = (r.get('record_id') or '').strip()
            dec = (r.get('decision') or '').strip().lower()
            reason = (r.get('display_reason') or '').strip()
            if rid not in titles:
                print(f'[skip] unknown record_id {rid}'); continue
            if rid in existing:
                print(f'[skip] already decided {rid}'); continue
            if dec not in ('include', 'exclude'):
                print(f'[skip] bad decision for {rid}: {dec}'); continue
            if dec == 'exclude' and reason not in TA_CATS:
                print(f'[skip] bad display_reason for {rid}: {reason!r}'); continue
            w.writerow({'record_id': rid, 'stage': 'TA', 'decision': dec,
                        'display_reason': reason if dec == 'exclude' else '',
                        'sub_reason': (r.get('sub_reason') or '').strip(),
                        'title': titles[rid]})
            existing[rid] = True
            added += 1
    print(f'applied {added} decisions -> {DEC}  (total {len(existing)})')

def cmd_tally():
    d = load_decisions()
    from collections import Counter
    inc = sum(1 for v in d.values() if v['decision'] == 'include')
    exc = [v for v in d.values() if v['decision'] == 'exclude']
    print(f'TA screened : {len(d)}')
    print(f'  include   : {inc}  -> full-text stage')
    print(f'  exclude   : {len(exc)}')
    c = Counter(v['display_reason'] for v in exc)
    for cat in TA_CATS:
        print(f'      {cat}  (n={c.get(cat,0)})')

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    if cmd == 'status':
        cmd_status()
    elif cmd == 'next':
        cmd_next(int(sys.argv[2]) if len(sys.argv) > 2 else 50)
    elif cmd == 'apply':
        cmd_apply(sys.argv[2])
    elif cmd == 'tally':
        cmd_tally()
    else:
        print(__doc__)
