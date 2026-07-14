"""
Lightweight resumable cache for expensive LLM stages
====================================================
Each expensive per-study result (Phase 1 / Phase 2 / extraction) is appended to
a JSON-Lines file keyed by PMID. On re-run, already-done studies are skipped, so
a run that is interrupted (terminal closed, rate limit, crash) resumes from where
it left off instead of re-spending tokens.

Cache is namespaced by a run key (hash of the research question) so changing the
PICO / criteria automatically starts a fresh cache.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from typing import Dict, List, Optional


def run_key(*parts) -> str:
    """Short stable hash identifying a specific review configuration."""
    blob = "||".join(str(p) for p in parts)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:12]


def file_key(pmid, title: str = "") -> str:
    """Filesystem-safe key for naming a study's local full-text file.

    Numeric PMID when present, else 'T_' + a title hash. This mirrors the
    pipeline's internal study key ('T:' + the same hash) but with a
    filename-safe separator, so no-PMID records (Embase-only papers,
    conference abstracts) can still be dropped in as  fulltext/<file_key>.pdf
    and be picked up on the next run.
    """
    raw = str(pmid or "").strip()
    m = re.match(r"\d+", raw)
    if m:
        return m.group()
    t = re.sub(r"\W+", " ", str(title).lower()).strip()
    return "T_" + hashlib.sha1(t.encode("utf-8")).hexdigest()[:12]


def cache_dir_for(base: str, key: str) -> str:
    d = os.path.join(base, key)
    os.makedirs(d, exist_ok=True)
    return d


def _path(cache_dir: str, name: str) -> str:
    return os.path.join(cache_dir, name)


def load_done(cache_dir: Optional[str], name: str) -> Dict[str, dict]:
    """Return {pmid: record} from a .jsonl cache file (empty if none)."""
    done: Dict[str, dict] = {}
    if not cache_dir:
        return done
    p = _path(cache_dir, name)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    done[str(r.get("pmid", ""))] = r
                except json.JSONDecodeError:
                    continue
    return done


def append_record(cache_dir: Optional[str], name: str, record: dict) -> None:
    """Append one record to a .jsonl cache (no-op if cache disabled)."""
    if not cache_dir:
        return
    os.makedirs(cache_dir, exist_ok=True)
    with open(_path(cache_dir, name), "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_json(cache_dir: Optional[str], name: str):
    if not cache_dir:
        return None
    p = _path(cache_dir, name)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return None


def save_json(cache_dir: Optional[str], name: str, obj) -> None:
    if not cache_dir:
        return
    os.makedirs(cache_dir, exist_ok=True)
    with open(_path(cache_dir, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
