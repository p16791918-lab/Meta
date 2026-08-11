#!/usr/bin/env python3
"""Audit the local full-text cache against authoritative PubMed records.

For every included study with a PMID, this fetches the authoritative title and
abstract from NCBI (works where NCBI is reachable, e.g. a Codespace) and:
  * flags whether the local fulltext/<pmid>.txt matches that title, and
  * prints the abstract + study type hint, so misattributed caches (a paper
    whose stored text is a *different* article) are caught and the correct
    source can be re-obtained.

Run in the Codespace:
    export NCBI_API_KEY=...   NCBI_EMAIL=you@example
    python3 audit_fulltext_cache.py

Reads PMIDs from REFERENCES.md; no key stored in this file.
"""
import os, re, urllib.request, urllib.parse
import xml.etree.ElementTree as ET

API_KEY=os.environ.get('NCBI_API_KEY',''); EMAIL=os.environ.get('NCBI_EMAIL','')
EFETCH='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
STOP=set('the a an of and or in to by for with from on among versus vs as at be is are '
         'women united states us breast cancer incidence rates rate race ethnicity racial '
         'ethnic study analysis trends'.split())

def refs():
    out={}
    for line in open('REFERENCES.md',encoding='utf-8'):
        m=re.match(r'^(\d+)\.\s+(.*)',line)
        if not m: continue
        pm=re.search(r'PMID:\s*(\d+)',m.group(2))
        if pm: out[int(m.group(1))]=pm.group(1)
    return out

def fetch(pmids):
    p={'db':'pubmed','id':','.join(pmids),'retmode':'xml','tool':'cache-audit','email':EMAIL}
    if API_KEY: p['api_key']=API_KEY
    with urllib.request.urlopen(EFETCH+'?'+urllib.parse.urlencode(p),timeout=60) as r:
        root=ET.fromstring(r.read())
    meta={}
    for art in root.findall('.//PubmedArticle'):
        pmid=art.findtext('.//MedlineCitation/PMID')
        title=' '.join((art.findtext('.//Article/ArticleTitle') or '').split())
        abst=' '.join(t.text or '' for t in art.findall('.//Article/Abstract/AbstractText'))
        abst=' '.join(abst.split())
        meta[pmid]=(title,abst)
    return meta

def kw(t): return {w for w in re.findall(r'[a-z]+',t.lower()) if w not in STOP and len(w)>3}

def main():
    R=refs(); meta=fetch(list(R.values()))
    bad=[]
    for num,pmid in sorted(R.items()):
        title,abst=meta.get(pmid,('',''))
        path=f'fulltext/{pmid}.txt'
        line=f"[{num}] PMID {pmid} — {title[:70]}"
        if os.path.exists(path):
            body=open(path,encoding='utf-8',errors='ignore').read()[:4000].lower()
            kt=kw(title); hit=(sum(1 for w in kt if w in body)/len(kt)) if kt else 1
            status='MATCH' if hit>=0.5 else 'CACHE-MISMATCH'
            if hit<0.5: bad.append(num)
            line+=f"\n     local cache: {status} ({hit*100:.0f}% title words in file)"
        else:
            line+="\n     local cache: (none)"
        # incidence-study hint from abstract
        inc = bool(re.search(r'per 100|incidence rate|age-adjusted|age-standardi', abst, re.I))
        line+=f"\n     abstract reports incidence rates? {'yes-ish' if inc else 'no clear rate language'}"
        print(line); print()
    print('='*60)
    print('CACHE-MISMATCH refs (local file is the wrong paper):', bad or 'none')

if __name__=='__main__':
    if not API_KEY: import sys; print('warn: set NCBI_API_KEY',file=sys.stderr)
    main()
