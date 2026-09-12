#!/usr/bin/env python3
"""Complete the unified reference list to full Vancouver format using a PubMed
.nbib export (authors, journal abbreviation, year, volume, issue, pages, doi).

Reads the current manuscript/References_draft.md to recover each reference's
number and PMID (order = order of appearance, 1-47), pulls the full record for
each PMID from the .nbib, and rewrites the numbered entries in Vancouver style.
References without a PMID (only #44) keep their existing line and are flagged.
The header note and the PMID import block are preserved.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REFS = os.path.join(HERE, "manuscript", "References_draft.md")


def parse_nbib(path):
    recs = {}
    cur = {}
    field = None
    for line in open(path, encoding="utf-8"):
        if line.strip() == "" and cur:
            recs[cur.get("PMID", "")] = cur
            cur, field = {}, None
            continue
        m = re.match(r"^([A-Z]{2,4})\s*- (.*)$", line.rstrip("\n"))
        if m:
            field, val = m.group(1), m.group(2)
            if field == "AU":
                cur.setdefault("AU", []).append(val)
            else:
                cur[field] = val
        elif field and line.startswith("      "):   # continuation
            if field == "AU":
                cur["AU"][-1] += " " + line.strip()
            else:
                cur[field] = cur.get(field, "") + " " + line.strip()
    if cur:
        recs[cur.get("PMID", "")] = cur
    return recs


def vancouver(r):
    au = r.get("AU", [])
    if au:
        authors = ", ".join(au[:6]) + (", et al." if len(au) > 6 else "")
    else:
        authors = (r.get("CN", "") or "").strip()   # corporate author (e.g., CDC)
    if authors and not authors.endswith("."):
        authors += "."          # close the author list (Vancouver: "Authors. Title.")
    title = (r.get("TI", "") or "").strip()
    title = re.sub(r"\s+", " ", title).rstrip(".") + "."
    journal = (r.get("TA", "") or r.get("JT", "")).strip().rstrip(".")
    ym = re.search(r"(19|20)\d\d", r.get("DP", ""))
    year = ym.group(0) if ym else ""
    vol = (r.get("VI", "") or "").strip()
    issue = (r.get("IP", "") or "").strip()
    pages = (r.get("PG", "") or "").strip()
    doi = ""
    for k in ("LID", "AID"):
        m = re.search(r"(10\.\S+?)\s*\[doi\]", r.get(k, ""))
        if m:
            doi = m.group(1)
            break
    loc = year
    if vol:
        loc += ";" + vol
        if issue:
            loc += "(%s)" % issue
    if pages:
        loc += ":" + pages
    out = "%s %s %s. %s." % (authors, title, journal, loc)
    out = re.sub(r"\s+", " ", out).replace(" .", ".").strip()
    if doi:
        out += " doi:" + doi
    return out


def main(nbib_path):
    recs = parse_nbib(nbib_path)
    lines = open(REFS, encoding="utf-8").read().split("\n")
    out, n_done, n_kept = [], 0, 0
    for l in lines:
        m = re.match(r"^(\d+)\.\s+(.*)$", l)
        if not m:
            out.append(l)
            continue
        num, body = m.group(1), m.group(2)
        pm = re.search(r"PMID:\s*(\d+)", body)
        if pm and pm.group(1) in recs:
            out.append("%s. %s" % (num, vancouver(recs[pm.group(1)])))
            n_done += 1
        else:
            out.append(l + "   [no PMID — complete manually]" if not pm else l)
            n_kept += 1
    open(REFS, "w", encoding="utf-8").write("\n".join(out))
    print("completed to Vancouver: %d | kept (no PMID): %d" % (n_done, n_kept))


if __name__ == "__main__":
    main(sys.argv[1])
