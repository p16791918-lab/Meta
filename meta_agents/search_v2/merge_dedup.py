#!/usr/bin/env python3
"""Cross-database de-duplication ONLY (no screening).

Normalizes the four v2 search exports (PubMed/MEDLINE, Embase, Scopus, WoS) into a
common schema, then removes duplicate records across databases by DOI → PMID →
normalized title. Reports total identified, duplicates removed, and unique records,
and writes `merged_unique.csv`. No eligibility/screening decision is made here — that
step waits until the PROSPERO amendment is registered.

Run:  python3 merge_dedup.py
"""
import csv, re, os, sys, glob
import xlrd

HERE = os.path.dirname(os.path.abspath(__file__))

def norm_title(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())

def norm_doi(s):
    s = (s or '').strip().lower()
    s = re.sub(r'^https?://(dx\.)?doi\.org/', '', s)
    return s.strip()

def norm_pmid(s):
    s = (s or '').strip()
    m = re.search(r'\d+', s)
    return m.group(0) if m else ''

# ── parsers → list of dicts {source,title,year,doi,pmid,abstract,doctype} ──────

def parse_pubmed(path):
    recs, cur, tag = [], {}, None
    def flush():
        if cur:
            recs.append({
                'source': 'PubMed/MEDLINE',
                'title': cur.get('TI', '').strip(' .'),
                'year': (cur.get('DP', '')[:4]),
                'doi': norm_doi(cur.get('_doi', '')),
                'pmid': norm_pmid(cur.get('PMID', '')),
                'abstract': cur.get('AB', '').strip(),
                'doctype': cur.get('PT', '').strip(),
            })
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line.strip():
                flush(); cur, tag = {}, None; continue
            if len(line) > 4 and line[4] == '-':
                tag = line[:4].strip()
                val = line[6:]
                if tag in ('LID', 'AID') and '[doi]' in val:
                    cur['_doi'] = val.replace('[doi]', '').strip()
                cur[tag] = (cur.get(tag, '') + ' ' + val).strip() if tag in cur else val
            else:  # continuation
                if tag:
                    cur[tag] = cur.get(tag, '') + ' ' + line.strip()
    flush()
    return recs

def parse_embase(path):
    recs = []
    for r in csv.DictReader(open(path, newline='', encoding='utf-8-sig', errors='replace')):
        recs.append({
            'source': 'Embase',
            'title': (r.get('Title') or '').strip(),
            'year': str(r.get('Publication Year') or '').strip()[:4],
            'doi': norm_doi(r.get('DOI')),
            'pmid': norm_pmid(r.get('Medline PMID')),
            'abstract': (r.get('Abstract') or '').strip(),
            'doctype': (r.get('Publication Type') or '').strip(),
        })
    return recs

def parse_scopus(path):
    recs = []
    for r in csv.DictReader(open(path, newline='', encoding='utf-8-sig', errors='replace')):
        recs.append({
            'source': 'Scopus',
            'title': (r.get('Title') or '').strip(),
            'year': str(r.get('Year') or '').strip()[:4],
            'doi': norm_doi(r.get('DOI')),
            'pmid': norm_pmid(r.get('PubMed ID')),
            'abstract': (r.get('Abstract') or '').strip(),
            'doctype': (r.get('Document Type') or '').strip(),
        })
    return recs

def parse_wos(paths):
    recs = []
    for path in paths:
        sh = xlrd.open_workbook(path).sheet_by_index(0)
        hdr = [str(sh.cell_value(0, c)) for c in range(sh.ncols)]
        idx = {h: i for i, h in enumerate(hdr)}
        def g(r, name):
            return str(sh.cell_value(r, idx[name])) if name in idx else ''
        for r in range(1, sh.nrows):
            recs.append({
                'source': 'WoS',
                'title': g(r, 'Article Title').strip(),
                'year': g(r, 'Publication Year').strip()[:4],
                'doi': norm_doi(g(r, 'DOI')),
                'pmid': norm_pmid(g(r, 'Pubmed Id')),
                'abstract': g(r, 'Abstract').strip(),
                'doctype': g(r, 'Document Type').strip(),
            })
    return recs

# ── de-duplication (union by DOI, then PMID, then normalized title) ────────────

def dedup(records):
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb

    # give every record a node; link records that share a key
    by_doi, by_pmid, by_title = {}, {}, {}
    for i, r in enumerate(records):
        find(('rec', i))
        if r['doi']:
            k = ('doi', r['doi'])
            if k in by_doi: union(('rec', i), ('rec', by_doi[k]))
            else: by_doi[k] = i
        if r['pmid']:
            k = ('pmid', r['pmid'])
            if k in by_pmid: union(('rec', i), ('rec', by_pmid[k]))
            else: by_pmid[k] = i
        nt = norm_title(r['title'])
        if nt and len(nt) > 10:
            if nt in by_title: union(('rec', i), ('rec', by_title[nt]))
            else: by_title[nt] = i

    clusters = {}
    for i in range(len(records)):
        clusters.setdefault(find(('rec', i)), []).append(i)
    return list(clusters.values())

def main():
    pubmed = parse_pubmed(glob.glob(os.path.join(HERE, 'pubmed_medline_*.txt'))[0])
    embase = parse_embase(os.path.join(HERE, 'embase_20260807_ADVANCED_3248.csv'))
    scopus = parse_scopus(glob.glob(os.path.join(HERE, 'scopus_*.csv'))[0])
    wos = parse_wos(sorted(glob.glob(os.path.join(HERE, 'wos_20260807_*.xls'))))

    all_recs = pubmed + embase + scopus + wos
    per = {'PubMed/MEDLINE': len(pubmed), 'Embase': len(embase),
           'Scopus': len(scopus), 'WoS': len(wos)}
    clusters = dedup(all_recs)

    # choose a representative per cluster: prefer one with abstract, source priority
    prio = {'Embase': 0, 'PubMed/MEDLINE': 1, 'Scopus': 2, 'WoS': 3}
    unique_rows = []
    for cl in clusters:
        members = [all_recs[i] for i in cl]
        rep = sorted(members, key=lambda m: (0 if m['abstract'] else 1, prio.get(m['source'], 9)))[0]
        srcs = ';'.join(sorted({m['source'] for m in members}, key=lambda s: prio.get(s, 9)))
        unique_rows.append({**rep, 'sources': srcs, 'n_copies': len(members)})

    total = len(all_recs)
    uniq = len(clusters)
    print('=' * 60)
    print('  CROSS-DATABASE DE-DUPLICATION (no screening)')
    print('=' * 60)
    for k, v in per.items():
        print(f'  {k:<16} {v:>6}')
    print(f'  {"TOTAL identified":<16} {total:>6}')
    print(f'  {"Duplicates":<16} {total - uniq:>6}  (removed)')
    print(f'  {"UNIQUE records":<16} {uniq:>6}')
    print('-' * 60)
    from collections import Counter
    ov = Counter(r['sources'] for r in unique_rows)
    print('  Unique records by source-combination (top):')
    for combo, c in ov.most_common(12):
        print(f'    {combo:<40} {c:>5}')
    print('=' * 60)

    out = os.path.join(HERE, 'merged_unique.csv')
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['sources', 'n_copies', 'source', 'title',
                                          'year', 'doi', 'pmid', 'doctype', 'abstract'])
        w.writeheader()
        for r in unique_rows:
            w.writerow(r)
    print(f'  wrote {out}  ({uniq} unique records)  — NO screening applied')

if __name__ == '__main__':
    main()
