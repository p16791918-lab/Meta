"""
Agent 1: Literature Search Agent
=================================
Supports 3 search modes:

  MODE A - pubmed_mcp  : PubMed MCP server (recommended)
  MODE B - entrez      : biopython Entrez API (fallback if no MCP)
  MODE C - csv         : Manual CSV file import (Embase, etc.)

See run_search_agent() docstring for usage.
"""

from __future__ import annotations

import csv
import json
import os
import re
from pathlib import Path
from typing import Literal, Optional

import anthropic

from shared.models import PICO, SearchResult
from shared.prompts import SEARCH_AGENT_PROMPT

# ── Supported search modes ───────────────────────────────────────────────────
SearchMode = Literal["pubmed_mcp", "entrez", "csv"]


# ── CSV column mapping (varies by database export format) ────────────────────
_CSV_COLUMN_MAP = {
    "pmid":     ["PMID", "PubMed ID", "Accession Number", "pubmed_id", "pmid"],
    "title":    ["Title", "Article Title", "title", "TI"],
    "abstract": ["Abstract", "abstract", "AB", "Author Abstract"],
    "year":     ["Year", "Publication Year", "PY", "year", "Cover Date"],
    "authors":  ["Authors", "Author Names", "AU", "authors", "Author(s)"],
    "journal":  ["Source title", "Journal", "SO", "Publication Title"],
    "doi":      ["DOI", "Digital Object Identifier", "doi"],
}


def _find_col(header: list, candidates: list) -> Optional[str]:
    """Return the first matching column name from candidates list."""
    h_lower = {h.lower(): h for h in header}
    for c in candidates:
        if c.lower() in h_lower:
            return h_lower[c.lower()]
    return None


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1-A  Build search strategy (Claude API - common to all modes)
# ─────────────────────────────────────────────────────────────────────────────

def build_search_strategy(
    pico: PICO,
    date_range: tuple = ("2000/01/01", "2025/12/31"),
) -> dict:
    """
    Use Claude API to generate PICO → MeSH terms + search queries.
    Called by all modes before fetching actual literature.
    """
    client = anthropic.Anthropic()

    user_message = f"""
    Please create a comprehensive search strategy for this meta-analysis:

    PICO:
    - Population: {pico.population}
    - Intervention: {pico.intervention}
    - Comparison: {pico.comparison}
    - Outcome: {pico.outcome}
    - Study Design filter: {pico.study_design or 'RCT preferred'}
    - Date range: {date_range[0]} to {date_range[1]}

    Generate:
    1. MeSH terms for each PICO element
    2. Free-text synonyms
    3. Full PubMed search string (with Boolean operators, ready to paste)
    4. Cochrane Library search string
    5. Embase (Ovid) search string

    Return ONLY valid JSON:
    {{
      "mesh_terms": {{"P": [...], "I": [...], "C": [...], "O": [...]}},
      "free_text":  {{"P": [...], "I": [...], "C": [...], "O": [...]}},
      "pubmed_query":   "...",
      "cochrane_query": "...",
      "embase_query":   "...",
      "estimated_results": integer,
      "notes": "..."
    }}
    """

    print("[Agent 1: Search] Generating search strategy via Claude...")
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=SEARCH_AGENT_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = response.content[0].text.strip()
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


# ─────────────────────────────────────────────────────────────────────────────
# MODE A: PubMed MCP server
# ─────────────────────────────────────────────────────────────────────────────
#
# Setup (run in Claude Code terminal):
#
# Option 1) Community pubmed-mcp (pip):
#   pip install pubmed-mcp
#   pubmed-mcp serve --port 3000
#
# Option 2) npx-based server:
#   npx -y @joshuarileydev/pubmed-mcp-server
#
# [claude_code_config.json registration example]
# {
#   "mcpServers": {
#     "pubmed": {
#       "command": "pubmed-mcp",
#       "args": ["serve"],
#       "env": { "NCBI_EMAIL": "your@email.com", "NCBI_API_KEY": "optional" }
#     }
#   }
# }

def fetch_via_pubmed_mcp(
    query: str,
    max_results: int = 200,
    mcp_server_url: str = "http://localhost:3000",
) -> list:
    """
    Fetch literature via PubMed MCP server.
    Automatically falls back to Entrez on failure.
    """
    client = anthropic.Anthropic()
    print(f"[Agent 1: Search] Trying PubMed MCP @ {mcp_server_url} ...")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            system=(
                "You are a PubMed search assistant. "
                "Use the available PubMed MCP tools to search for articles. "
                "Return results as a JSON array with fields: "
                "pmid, title, abstract, year, authors, journal, doi. "
                "Return ONLY the JSON array, no other text."
            ),
            messages=[{
                "role": "user",
                "content": (
                    f"Search PubMed for: {query}\n"
                    f"Retrieve up to {max_results} results.\n"
                    "Return as JSON array only."
                )
            }],
            mcp_servers=[{
                "type": "url",
                "url": mcp_server_url,
                "name": "pubmed",
            }],
        )

        studies = []

        for block in response.content:
            if getattr(block, "type", "") == "mcp_tool_result":
                raw = ""
                if block.content:
                    raw = block.content[0].text
                try:
                    data = json.loads(raw)
                    if isinstance(data, list):
                        studies.extend(data)
                    elif isinstance(data, dict) and "articles" in data:
                        studies.extend(data["articles"])
                except json.JSONDecodeError:
                    pass

            elif getattr(block, "type", "") == "text":
                raw = block.text.strip().replace("```json", "").replace("```", "").strip()
                try:
                    data = json.loads(raw)
                    if isinstance(data, list):
                        studies.extend(data)
                except json.JSONDecodeError:
                    pass

        if studies:
            print(f"[Agent 1: Search] ✓ PubMed MCP → {len(studies)} articles")
            return [_normalize_study(s, source="pubmed_mcp") for s in studies[:max_results]]

        print("[Agent 1: Search] ⚠ MCP returned 0 results → fallback to Entrez")
        return fetch_via_entrez(query, max_results)

    except Exception as e:
        print(f"[Agent 1: Search] ⚠ MCP error: {e} → fallback to Entrez")
        return fetch_via_entrez(query, max_results)


# ─────────────────────────────────────────────────────────────────────────────
# MODE B: biopython Entrez (fallback)
# ─────────────────────────────────────────────────────────────────────────────

def fetch_via_entrez(query: str, max_results: int = 200) -> list:
    """
    Search PubMed via biopython Bio.Entrez.
    Env vars: NCBI_EMAIL (recommended), NCBI_API_KEY (optional, 10 req/s)
    Install: pip install biopython
    """
    try:
        from Bio import Entrez

        Entrez.email   = os.getenv("NCBI_EMAIL",   "researcher@example.com")
        Entrez.api_key = os.getenv("NCBI_API_KEY",  "")
        print(f"[Agent 1: Search] Querying PubMed via Entrez (max {max_results})...")

        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()
        pmids = record["IdList"]

        if not pmids:
            print("[Agent 1: Search] ⚠ No PMIDs returned")
            return []

        handle = Entrez.efetch(db="pubmed", id=pmids, rettype="abstract", retmode="xml")
        records = Entrez.read(handle)
        handle.close()

        studies = []
        for article in records.get("PubmedArticle", []):
            medline = article["MedlineCitation"]
            art     = medline["Article"]
            abstract_parts = art.get("Abstract", {}).get("AbstractText", [""])
            abstract_text  = " ".join(str(a) for a in abstract_parts)

            pub_date = (art.get("Journal", {})
                           .get("JournalIssue", {})
                           .get("PubDate", {}))
            year_str = pub_date.get("Year") or pub_date.get("MedlineDate", "0")[:4]
            try:
                year = int(year_str)
            except (ValueError, TypeError):
                year = 0

            doi = next(
                (str(loc) for loc in art.get("ELocationID", [])
                 if loc.attributes.get("EIdType") == "doi"),
                ""
            )

            studies.append({
                "pmid":     str(medline["PMID"]),
                "title":    str(art.get("ArticleTitle", "")),
                "abstract": abstract_text,
                "year":     year,
                "authors":  [
                    f"{a.get('LastName', '')} {a.get('Initials', '')}"
                    for a in art.get("AuthorList", [])
                ],
                "journal":  str(art.get("Journal", {}).get("Title", "")),
                "doi":      doi,
                "source":   "pubmed_entrez",
            })

        print(f"[Agent 1: Search] ✓ Entrez → {len(studies)} articles")
        return studies

    except ImportError:
        print("[Agent 1: Search] ✗ biopython not installed: pip install biopython")
        return []
    except Exception as e:
        print(f"[Agent 1: Search] ✗ Entrez error: {e}")
        return []


# ─────────────────────────────────────────────────────────────────────────────
# MODE C: Manual CSV import
# ─────────────────────────────────────────────────────────────────────────────

def load_from_csv(
    csv_path,
    source_label: str = "manual_csv",
    encoding: str = "utf-8-sig",   # BOM-aware for Embase CSV
) -> list:
    """
    Load manually downloaded CSV export files.

    Supported databases (auto-detects columns):
      - Embase  (Elsevier → Export → CSV)
      - PubMed  (Send to → File → Format: CSV)
      - Scopus  (Export → CSV)
      - Web of Science (Export → Tab-delimited → .csv)
      - Cochrane (Export → CSV)

    Args:
        csv_path:     Path to CSV file (str or Path)
        source_label: Database name for tracking (e.g. "Embase")
        encoding:     Default utf-8-sig (handles BOM files)

    Returns:
        List of normalized study dicts
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path.resolve()}")

    rows, header = [], []
    for enc in [encoding, "utf-8", "cp1252", "latin-1"]:
        try:
            with open(path, newline="", encoding=enc) as f:
                reader = csv.DictReader(f)
                rows   = list(reader)
                header = list(reader.fieldnames or [])
            break
        except (UnicodeDecodeError, LookupError):
            continue
    else:
        raise ValueError(f"Cannot decode {path} with common encodings.")

    print(f"\n[Agent 1: Search] Loading CSV → {path.name}")
    print(f"  Encoding : {enc} | Rows : {len(rows)} | Columns : {len(header)}")

    col = {field: _find_col(header, candidates)
           for field, candidates in _CSV_COLUMN_MAP.items()}

    if not col.get("title"):
        print(f"  ⚠ 'Title' column not found. Available: {header}")

    studies = []
    for i, row in enumerate(rows):
        def get(field):
            c = col.get(field)
            return row.get(c, "").strip() if c else ""

        authors_raw = get("authors")
        authors = [a.strip() for a in re.split(r"[;,]", authors_raw) if a.strip()]

        m = re.search(r"\d{4}", get("year"))
        year = int(m.group()) if m else 0

        study = {
            "pmid":     get("pmid"),
            "title":    get("title"),
            "abstract": get("abstract"),
            "year":     year,
            "authors":  authors,
            "journal":  get("journal"),
            "doi":      get("doi"),
            "source":   source_label,
        }

        if not study["title"]:
            continue

        studies.append(study)

    print(f"  ✓ {len(studies)} valid records loaded from {source_label}")
    return studies


def load_multiple_csv(csv_files: dict) -> list:
    """
    Load CSVs from multiple databases and deduplicate by title.

    Args:
        csv_files: {"Embase": "embase.csv", "Cochrane": "cochrane.csv", ...}
    """
    all_studies = []

    for source_label, csv_path in csv_files.items():
        try:
            studies = load_from_csv(csv_path, source_label=source_label)
            all_studies.extend(studies)
        except FileNotFoundError as e:
            print(f"[Agent 1: Search] ⚠ Skipping {source_label}: {e}")

    seen: set = set()
    deduped = []
    for s in all_studies:
        norm = re.sub(r"\W+", " ", s["title"].lower()).strip()
        if norm and norm not in seen:
            seen.add(norm)
            deduped.append(s)

    removed = len(all_studies) - len(deduped)
    print(f"\n[Agent 1: Search] Deduplication: {len(all_studies)} → {len(deduped)} "
          f"({removed} duplicates removed)")
    return deduped


def _normalize_study(s: dict, source: str = "") -> dict:
    """Normalize dict from external sources to standard format."""
    return {
        "pmid":     str(s.get("pmid") or s.get("PubMed ID", "")),
        "title":    str(s.get("title") or s.get("Title", "")),
        "abstract": str(s.get("abstract") or s.get("Abstract", "")),
        "year":     int(s.get("year") or s.get("Year", 0) or 0),
        "authors":  s.get("authors") or s.get("Authors", []),
        "journal":  str(s.get("journal") or s.get("Journal", "")),
        "doi":      str(s.get("doi") or s.get("DOI", "")),
        "source":   source or s.get("source", "unknown"),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────────────────────────────────────

def run_search_agent(
    pico: PICO,
    mode: str = "pubmed_mcp",
    date_range: tuple = ("2000/01/01", "2025/12/31"),
    max_results: int = 200,
    mcp_server_url: str = "http://localhost:3000",
    csv_files: Optional[dict] = None,
) -> SearchResult:
    """
    Main search agent function.

    Args:
        pico:           PICO object
        mode:           "pubmed_mcp" | "entrez" | "csv"
        date_range:     Search date range tuple
        max_results:    Max records to retrieve (ignored for csv mode)
        mcp_server_url: PubMed MCP server URL (for mode="pubmed_mcp")
        csv_files:      {"DBName": "filepath"} (for mode="csv")

    Examples:
        # MCP mode (requires PubMed MCP server)
        result = run_search_agent(pico, mode="pubmed_mcp")

        # Entrez mode (requires biopython only)
        result = run_search_agent(pico, mode="entrez")

        # CSV mode (manually downloaded exports)
        result = run_search_agent(
            pico,
            mode="csv",
            csv_files={
                "Embase":   "embase_results.csv",
                "Cochrane": "cochrane_results.csv",
                "PubMed":   "pubmed_results.csv",
            }
        )
    """
    strategy = build_search_strategy(pico, date_range)

    all_mesh = []
    for terms in strategy.get("mesh_terms", {}).values():
        all_mesh.extend(terms)

    search_result = SearchResult(
        pico=pico,
        mesh_terms=all_mesh,
        pubmed_query=strategy["pubmed_query"],
        cochrane_query=strategy["cochrane_query"],
        embase_query=strategy["embase_query"],
        total_hits=strategy.get("estimated_results", 0),
        studies=[],
    )

    print(f"\n[Agent 1: Search] Mode → {mode.upper()}")

    if mode == "pubmed_mcp":
        studies = fetch_via_pubmed_mcp(strategy["pubmed_query"], max_results, mcp_server_url)

    elif mode == "entrez":
        studies = fetch_via_entrez(strategy["pubmed_query"], max_results)

    elif mode == "csv":
        if not csv_files:
            raise ValueError(
                "mode='csv' requires csv_files dict.\n"
                "Example: csv_files={'Embase': 'embase.csv', 'PubMed': 'pubmed.csv'}"
            )
        studies = load_multiple_csv(csv_files)

    else:
        raise ValueError(f"Unknown mode: '{mode}'. Use 'pubmed_mcp', 'entrez', or 'csv'.")

    search_result.studies = studies
    search_result.total_hits = len(studies)

    print(f"[Agent 1: Search] ✓ Total records: {len(studies)}")
    return search_result


# Backwards-compatibility alias
fetch_pubmed_results = fetch_via_entrez


# ─────────────────────────────────────────────────────────────────────────────
# Standalone test
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    test_pico = PICO(
        population="Type 2 diabetes mellitus patients",
        intervention="SGLT2 inhibitors",
        comparison="Placebo",
        outcome="Major adverse cardiovascular events (MACE)",
        study_design="Randomized controlled trial",
    )

    test_mode = sys.argv[1] if len(sys.argv) > 1 else "entrez"

    if test_mode == "csv":
        sample_csv = "sample_embase.csv"
        with open(sample_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Title", "Abstract", "Year", "Authors", "PMID", "DOI", "Source title"])
            w.writerow([
                "SGLT2 inhibitors in T2DM: a RCT",
                "Background: SGLT2 inhibitors reduce cardiovascular events...",
                "2022", "Kim J; Park S", "35000001", "10.1000/test", "NEJM"
            ])
        result = run_search_agent(test_pico, mode="csv",
                                  csv_files={"Embase_test": sample_csv})
    else:
        result = run_search_agent(test_pico, mode=test_mode)

    print(f"\nPubMed query : {result.pubmed_query[:120]}")
    print(f"Embase query : {result.embase_query[:120]}")
    print(f"Records      : {len(result.studies)}")
