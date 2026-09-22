#!/usr/bin/env python3
"""record_id -> number in the unified reference list.

The reference list is built in a fixed order (Introduction, Methods, then the
studies that contributed estimates), so the number each study carries can be
recomputed here without touching the network. Table 1 and Supplementary Table 4
name their studies by author and year; adding the number makes each one reachable
from the reference list, which otherwise lists entries the document never points
at.

build_references.load_order() does the ordering and reads no network; only the
metadata fetch that follows it does.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_MAP = None


def ref_map():
    """{record_id: reference number}, built once."""
    global _MAP
    if _MAP is None:
        from build_references import load_order
        order, _ = load_order()
        _MAP = {rec: n for n, _kind, rec, _pmid, _manual in order if rec}
    return _MAP


def cite_ref(record_id):
    """' [N]' for a record in the reference list, '' for one that is not.

    Bracketed rather than superscript: the table cells in the Word builders are
    rendered as plain runs, so a superscript digit there would not be typeset as
    one.
    """
    n = ref_map().get(str(record_id))
    return " [%d]" % n if n else ""


if __name__ == "__main__":
    m = ref_map()
    print("%d records mapped to reference numbers 1-%d" % (len(m), max(m.values())))
