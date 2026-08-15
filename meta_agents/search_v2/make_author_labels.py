#!/usr/bin/env python3
"""Derive a first-author label ("Surname" or "Surname et al.") for every included
study, entirely offline from the raw search-export dumps captured at search time
(no network / PubMed calls). Keyed by record_id. Written to author_labels.json and
consumed by make_supplementary.py to populate the "Study (author, year)" column.

Resolution order per record (first hit wins):
  1. MEDLINE dump  by PMID  (FAU field; exact author count -> et al. decision)
  2. Embase/WoS    by PMID  (Author Names / AU; multi-author from the list length)
  3. Embase/Scopus/WoS by DOI
  4. breast_extraction.csv author_year surname (last-resort fallback)

Note: the label reflects the FIRST AUTHOR of the paper identified by the row's
PMID/DOI, which is authoritative for Supplementary Table 2. It may differ from the
internal author_year shorthand in breast_extraction.csv; those differences are
audited separately (see AUTHOR_AUDIT.md) and are not silently reconciled here.
"""
import csv, json, os, re
import xlrd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw_search")


def strip_initials(first):
    # "Englum B.R." / "Gram I.T." -> "Englum" / "Gram"
    return re.sub(r"\s+[A-Z]\.?([- ]?[A-Z]\.?)*\s*$", "", first).strip() or first


def build_maps():
    pmid_sn, pmid_n = {}, {}          # MEDLINE: surname + author count
    pmid_sn2, pmid_multi = {}, {}     # Embase/WoS by PMID
    doi_sn, doi_multi = {}, {}        # Embase/Scopus/WoS by DOI

    # 1) MEDLINE
    pmid, cnt, first = None, 0, None

    def flush():
        if pmid and first is not None:
            pmid_sn[pmid] = first
            pmid_n[pmid] = cnt

    med = os.path.join(RAW, "pubmed_medline_20260807.txt")
    if os.path.exists(med):
        for line in open(med, encoding="utf-8", errors="replace"):
            if line.startswith("PMID- "):
                flush(); pmid = line[6:].strip(); cnt = 0; first = None
            elif line.startswith("FAU - "):
                cnt += 1
                if first is None:
                    first = line[6:].split(",")[0].strip()
            elif line.startswith("AU  - ") and first is None:
                cnt += 1; first = line[6:].split(",")[0].strip()
        flush()

    # 2) Embase (PMID + DOI)
    for f in ["embase_20260807_ADVANCED_3248.csv", "embase_20260807_QUICK_1703.csv"]:
        p = os.path.join(RAW, f)
        if not os.path.exists(p):
            continue
        for r in csv.DictReader(open(p, encoding="utf-8", errors="replace")):
            au = r.get("Author Names", "").strip()
            if not au:
                continue
            parts = re.split(r",\s(?=[A-Z][a-zA-Z'-]+\s)", au)
            sn = strip_initials(parts[0]); multi = len(parts) > 1
            pm = (r.get("Medline PMID") or "").strip()
            di = (r.get("DOI") or "").strip().lower()
            if pm:
                pmid_sn2.setdefault(pm, sn); pmid_multi.setdefault(pm, multi)
            if di:
                doi_sn.setdefault(di, sn); doi_multi.setdefault(di, multi)

    # 3) Scopus (DOI)
    sp = os.path.join(RAW, "scopus_20260807.csv")
    if os.path.exists(sp):
        sr = csv.DictReader(open(sp, encoding="utf-8", errors="replace"))
        akey = [c for c in sr.fieldnames if c.strip('﻿"').lower() == "authors"][0]
        for r in sr:
            au = r.get(akey, "").strip(); di = (r.get("DOI") or "").strip().lower()
            if au and di:
                parts = au.split(";")
                doi_sn.setdefault(di, strip_initials(parts[0].strip()))
                doi_multi.setdefault(di, len(parts) > 1)

    # 4) WoS (PMID + DOI)
    for f in ["wos_20260807_1.xls", "wos_20260807_2.xls"]:
        p = os.path.join(RAW, f)
        if not os.path.exists(p):
            continue
        sh = xlrd.open_workbook(p).sheet_by_index(0)
        hdr = {str(sh.cell_value(0, c)).strip(): c for c in range(sh.ncols)}
        cau, cpm, cdi = hdr.get("Authors"), hdr.get("Pubmed Id"), hdr.get("DOI")
        for rr in range(1, sh.nrows):
            au = str(sh.cell_value(rr, cau)).strip() if cau is not None else ""
            if not au:
                continue
            parts = au.split(";"); sn = parts[0].split(",")[0].strip(); multi = len(parts) > 1
            if cpm is not None:
                pm = str(sh.cell_value(rr, cpm)).strip().replace(".0", "")
                if pm:
                    pmid_sn2.setdefault(pm, sn); pmid_multi.setdefault(pm, multi)
            if cdi is not None:
                di = str(sh.cell_value(rr, cdi)).strip().lower()
                if di:
                    doi_sn.setdefault(di, sn); doi_multi.setdefault(di, multi)

    return pmid_sn, pmid_n, pmid_sn2, pmid_multi, doi_sn, doi_multi


def main():
    pmid_sn, pmid_n, pmid_sn2, pmid_multi, doi_sn, doi_multi = build_maps()

    rec_sn = {}
    for r in csv.DictReader(open(os.path.join(HERE, "breast_extraction.csv"), encoding="utf-8")):
        m = re.match(r"([A-Za-z]+)", r["author_year"])
        if m:
            rec_sn.setdefault(r["record_id"], m.group(1))

    def resolve(rid, pm, di):
        pm = pm.strip(); di = di.strip().lower()
        if pm in pmid_sn:
            return pmid_sn[pm], (pmid_n.get(pm, 2) > 1)
        if pm in pmid_sn2:
            return pmid_sn2[pm], pmid_multi.get(pm, True)
        if di in doi_sn:
            return doi_sn[di], doi_multi.get(di, True)
        if rid in rec_sn:
            return rec_sn[rid], True
        return None, None

    inc = list(csv.DictReader(open(os.path.join(HERE, "TableS_included_studies.csv"), encoding="utf-8")))
    out, miss = {}, []
    for r in inc:
        sn, multi = resolve(r["record_id"], r["pmid"], r["doi"])
        if sn is None:
            miss.append(r["record_id"]); continue
        out[r["record_id"]] = ("%s et al." % sn) if multi else sn

    json.dump(out, open(os.path.join(HERE, "author_labels.json"), "w"), ensure_ascii=False, indent=0)
    print("author labels: %d / %d resolved" % (len(out), len(inc)))
    if miss:
        print("  unresolved:", miss)


if __name__ == "__main__":
    main()
