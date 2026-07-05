"""
Multi-source record merging & deduplication
============================================
Combines search results from several databases (PubMed, Embase, Cochrane, ...)
into one deduplicated record set, tracking which database(s) each record came
from (provenance) for the PRISMA "Identification" box.

Cascading duplicate key (most reliable first):
  1. PMID           exact match
  2. DOI            normalized match
  3. Title + Year   normalized title, within year_tolerance, similarity >= threshold
                    (only when fuzzy_title=True)

Records with neither PMID nor DOI (e.g. Embase-unique papers) fall through to
title matching; if nothing matches they are kept as distinct studies.
"""
from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# Normalization helpers
# ─────────────────────────────────────────────────────────────────────────────

def _norm_pmid(v) -> str:
    s = re.sub(r"\D", "", str(v or ""))
    return s


def _norm_doi(v) -> str:
    s = str(v or "").strip().lower()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s)
    s = re.sub(r"^doi:\s*", "", s)
    return s


def _norm_title(v) -> str:
    s = re.sub(r"\W+", " ", str(v or "").lower()).strip()
    return re.sub(r"\s+", " ", s)


def _year(v) -> int:
    m = re.search(r"\d{4}", str(v or ""))
    return int(m.group()) if m else 0


def _completeness(rec: dict) -> int:
    """Higher = more complete; used to pick the record to keep on merge."""
    score = 0
    if rec.get("abstract"):
        score += 2
    if _norm_pmid(rec.get("pmid")):
        score += 1
    if _norm_doi(rec.get("doi")):
        score += 1
    if rec.get("journal"):
        score += 1
    return score


# ─────────────────────────────────────────────────────────────────────────────
# Merge
# ─────────────────────────────────────────────────────────────────────────────

def merge_sources(
    source_lists: Dict[str, List[dict]],
    fuzzy_title: bool = True,
    title_threshold: float = 0.92,
    year_tolerance: int = 1,
) -> Tuple[List[dict], dict]:
    """
    Merge and deduplicate records from multiple databases.

    Args:
        source_lists:   {"PubMed": [study, ...], "Embase": [study, ...]}
        fuzzy_title:    also match on normalized title + year when no PMID/DOI
        title_threshold: SequenceMatcher ratio required for a fuzzy title match
        year_tolerance:  allowed |year difference| for a fuzzy title match

    Returns:
        (merged_records, report)

        Each merged record gains "sources": sorted list of database labels.
        report = {
          "records_by_source", "total_before", "duplicates_removed",
          "total_after", "overlap"
        }
    """
    merged: List[dict] = []
    pmid_index: Dict[str, int] = {}
    doi_index: Dict[str, int] = {}
    # parallel arrays for fuzzy title matching
    titles: List[str] = []
    years: List[int] = []

    def _find(rec_pmid: str, rec_doi: str, rec_title: str, rec_year: int) -> Optional[int]:
        if rec_pmid and rec_pmid in pmid_index:
            return pmid_index[rec_pmid]
        if rec_doi and rec_doi in doi_index:
            return doi_index[rec_doi]
        if fuzzy_title and rec_title:
            for idx, (t, y) in enumerate(zip(titles, years)):
                if not t:
                    continue
                if year_tolerance >= 0 and rec_year and y and abs(rec_year - y) > year_tolerance:
                    continue
                if t == rec_title or SequenceMatcher(None, t, rec_title).ratio() >= title_threshold:
                    return idx
        return None

    records_by_source: Dict[str, int] = {}

    for label, studies in source_lists.items():
        records_by_source[label] = len(studies)
        for s in studies:
            p = _norm_pmid(s.get("pmid"))
            d = _norm_doi(s.get("doi"))
            t = _norm_title(s.get("title"))
            y = _year(s.get("year"))

            idx = _find(p, d, t, y)
            if idx is None:
                rec = dict(s)
                rec["sources"] = [label]
                merged.append(rec)
                new_idx = len(merged) - 1
                titles.append(t)
                years.append(y)
                if p:
                    pmid_index[p] = new_idx
                if d:
                    doi_index[d] = new_idx
            else:
                rec = merged[idx]
                if label not in rec["sources"]:
                    rec["sources"].append(label)
                # keep the more complete record's scalar fields
                if _completeness(s) > _completeness(rec):
                    sources = rec["sources"]
                    merged[idx] = {**s, "sources": sources}
                    rec = merged[idx]
                else:
                    # fill any blanks from the duplicate
                    for k in ("pmid", "doi", "abstract", "journal", "year"):
                        if not rec.get(k) and s.get(k):
                            rec[k] = s[k]
                # (re)register identifiers that may now be present
                np, nd = _norm_pmid(rec.get("pmid")), _norm_doi(rec.get("doi"))
                if np:
                    pmid_index[np] = idx
                if nd:
                    doi_index[nd] = idx
                titles[idx] = _norm_title(rec.get("title")) or titles[idx]

    total_before = sum(records_by_source.values())
    total_after = len(merged)

    # overlap breakdown (e.g. PubMed_only / Embase_only / both)
    overlap: Dict[str, int] = {}
    for rec in merged:
        key = "+".join(sorted(rec["sources"])) if len(rec["sources"]) > 1 \
            else f"{rec['sources'][0]}_only"
        overlap[key] = overlap.get(key, 0) + 1

    report = {
        "records_by_source": records_by_source,
        "total_before": total_before,
        "duplicates_removed": total_before - total_after,
        "total_after": total_after,
        "overlap": overlap,
    }

    for rec in merged:
        rec["sources"] = sorted(rec["sources"])

    print(f"[Merge] {records_by_source} → {total_after} unique "
          f"({report['duplicates_removed']} duplicates removed)")
    print(f"[Merge] Overlap: {overlap}")
    return merged, report
