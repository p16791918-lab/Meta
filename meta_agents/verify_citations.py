#!/usr/bin/env python3
"""Citation-integrity check: does each PMID in REFERENCES.md actually resolve to
the paper we cite?

Fetches authoritative metadata from NCBI E-utilities (PubMed) and compares the
first-author surname, publication year, and title against what REFERENCES.md
stores. Flags any mismatch. Also does a Crossref check for entries that carry a
DOI but no PMID.

Run in an environment where NCBI is reachable (e.g. GitHub Codespace):

    export NCBI_API_KEY=...        # your key
    export NCBI_EMAIL=you@example  # your email
    python3 verify_citations.py

Writes citation_verification_report.txt and prints a summary. No network key is
stored in this file.
"""
import os, re, json, time, sys, urllib.request, urllib.parse
import xml.etree.ElementTree as ET

API_KEY = os.environ.get('NCBI_API_KEY', '')
EMAIL   = os.environ.get('NCBI_EMAIL', '')
EFETCH  = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
CROSSREF = 'https://api.crossref.org/works/'

STOP = set('the a an of and or in on for by to with from between among vs versus '
           'among rates rate trends trend incidence breast cancer women united '
           'states us study analysis by race ethnicity racial ethnic'.split())


def parse_references(path='REFERENCES.md'):
    refs = []
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^(\d+)\.\s+(.*)', line)
        if not m:
            continue
        num, text = int(m.group(1)), m.group(2)
        pmid = re.search(r'PMID:\s*(\d+)', text)
        doi = re.search(r'doi:\s*([^\s.]+(?:\.[^\s,;]+)*)', text, re.I)
        first_author = re.match(r'([A-Z][A-Za-z\'\-]+)', text)
        year = re.search(r'\b(19|20)\d{2}\b', text)
        refs.append({
            'num': num, 'text': text,
            'pmid': pmid.group(1) if pmid else None,
            'doi': (doi.group(1).rstrip('.') if doi else None),
            'first_author': first_author.group(1) if first_author else '',
            'year': year.group(0) if year else '',
        })
    return refs


def efetch(pmids):
    params = {'db': 'pubmed', 'id': ','.join(pmids), 'retmode': 'xml',
              'tool': 'citation-verify', 'email': EMAIL}
    if API_KEY:
        params['api_key'] = API_KEY
    url = EFETCH + '?' + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return ET.fromstring(r.read())


def pubmed_meta(root):
    out = {}
    for art in root.findall('.//PubmedArticle'):
        pmid = art.findtext('.//MedlineCitation/PMID')
        title = ' '.join((art.findtext('.//Article/ArticleTitle') or '').split())
        journal = art.findtext('.//Article/Journal/ISOAbbreviation') or ''
        year = (art.findtext('.//Article/Journal/JournalIssue/PubDate/Year') or
                (art.findtext('.//Article/Journal/JournalIssue/PubDate/MedlineDate') or '')[:4])
        a1 = art.find('.//Article/AuthorList/Author')
        surname = a1.findtext('LastName') if a1 is not None else ''
        vol = art.findtext('.//Article/Journal/JournalIssue/Volume') or ''
        pages = art.findtext('.//Article/Pagination/MedlinePgn') or ''
        doi = ''
        for aid in art.findall('.//ArticleIdList/ArticleId'):
            if aid.get('IdType') == 'doi':
                doi = aid.text
        out[pmid] = dict(title=title, journal=journal, year=year,
                         surname=surname or '', vol=vol, pages=pages, doi=doi or '')
    return out


def token_overlap(claimed_text, real_title):
    rt = {w for w in re.findall(r'[a-z]+', real_title.lower()) if w not in STOP and len(w) > 3}
    ct = set(re.findall(r'[a-z]+', claimed_text.lower()))
    if not rt:
        return 1.0
    return len(rt & ct) / len(rt)


def crossref_check(ref):
    try:
        url = CROSSREF + urllib.parse.quote(ref['doi'])
        req = urllib.request.Request(url, headers={'User-Agent': f'citation-verify (mailto:{EMAIL})'})
        with urllib.request.urlopen(req, timeout=30) as r:
            msg = json.load(r)['message']
        real_first = (msg.get('author', [{}])[0].get('family', '') if msg.get('author') else '')
        real_year = str((msg.get('issued', {}).get('date-parts', [[None]])[0] or [None])[0] or '')
        title = (msg.get('title') or [''])[0]
        author_ok = real_first.lower() in ref['text'].lower() if real_first else None
        year_ok = (real_year in ref['text']) if real_year else None
        return dict(source='crossref', real_first=real_first, real_year=real_year,
                    title=title, author_ok=author_ok, year_ok=year_ok,
                    title_ok=token_overlap(ref['text'], title) >= 0.5)
    except Exception as e:
        return dict(source='crossref', error=str(e))


def main():
    refs = parse_references()
    with_pmid = [r for r in refs if r['pmid']]
    root = efetch([r['pmid'] for r in with_pmid])
    meta = pubmed_meta(root)

    lines, flags = [], []
    for r in sorted(refs, key=lambda x: x['num']):
        n = r['num']
        if r['pmid']:
            m = meta.get(r['pmid'])
            if not m:
                lines.append(f"[{n}] PMID {r['pmid']}: NOT RETURNED by PubMed  <-- CHECK")
                flags.append(n); continue
            author_ok = m['surname'].lower() in r['text'].lower() if m['surname'] else False
            year_ok = m['year'] in r['text'] if m['year'] else False
            title_ok = token_overlap(r['text'], m['title']) >= 0.5
            ok = author_ok and year_ok and title_ok
            mark = 'OK ' if ok else '!! '
            if not ok:
                flags.append(n)
            lines.append(
                f"{mark}[{n}] PMID {r['pmid']}  author:{'Y' if author_ok else 'N'} "
                f"year:{'Y' if year_ok else 'N'} title:{'Y' if title_ok else 'N'}\n"
                f"      PubMed: {m['surname']} … {m['year']} {m['journal']} {m['vol']}:{m['pages']} "
                f"doi:{m['doi']}\n      Title : {m['title']}")
        elif r['doi']:
            c = crossref_check(r); time.sleep(0.2)
            if 'error' in c:
                lines.append(f"?? [{n}] no PMID; Crossref error: {c['error']}")
                flags.append(n)
            else:
                ok = bool(c.get('author_ok')) and bool(c.get('year_ok')) and bool(c.get('title_ok'))
                if not ok:
                    flags.append(n)
                lines.append(
                    f"{'OK ' if ok else '!! '}[{n}] DOI {r['doi']} (Crossref)  "
                    f"author:{'Y' if c.get('author_ok') else 'N'} year:{'Y' if c.get('year_ok') else 'N'} "
                    f"title:{'Y' if c.get('title_ok') else 'N'}\n      Crossref: {c.get('real_first')} "
                    f"{c.get('real_year')} — {c.get('title')}")
        else:
            lines.append(f"-- [{n}] no PMID and no DOI — verify manually: {r['text'][:80]}…")
            flags.append(n)

    report = '\n'.join(lines)
    open('citation_verification_report.txt', 'w', encoding='utf-8').write(report + '\n')
    print(report)
    print('\n' + '=' * 60)
    if flags:
        print(f"NEEDS REVIEW ({len(flags)}): {sorted(set(flags))}")
    else:
        print("ALL PMID/DOI references matched (author + year + title).")
    print("full report -> citation_verification_report.txt")


if __name__ == '__main__':
    if not API_KEY:
        print("warning: NCBI_API_KEY not set; PubMed may rate-limit or 403.", file=sys.stderr)
    main()
