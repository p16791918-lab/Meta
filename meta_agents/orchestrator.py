"""
Meta-Analysis Orchestrator
===========================
Coordinates all 5 sub-agents in sequence:
  Agent 1 → Search
  Agent 2 → Screening
  Agent 3 → Data Extraction
  Agent 4 → Statistical Analysis
  Agent 5 → Manuscript Writing

Usage:
  cd meta_agents
  python orchestrator.py [mcp|entrez|csv|demo]
"""
import json
import os
import sys
from datetime import datetime
from shared.models import PICO, MetaAnalysisProject
from agent_1_search import (
    run_search_agent, build_search_strategy, gather_sources,
)
from agent_2_screening import run_screening_2stage, generate_prisma_text
from agent_3_extraction import extract_data, to_r_dataframe
from fetch_fulltext import write_retrieval_report
from merge_sources import merge_sources
from cache_utils import run_key, cache_dir_for, load_json, save_json, file_key
from agent_4_analysis import run_analysis_agent, save_r_script
from agent_5_writer import write_full_manuscript, compile_manuscript


def run_meta_analysis(
    title: str,
    pico: PICO,
    inclusion_criteria: list,
    exclusion_criteria: list,
    rob_tool: str = "RoB2",
    target_journal: str = "PLOS ONE",
    protocol_doi: str = None,
    date_range: tuple = ("2000/01/01", "2025/12/31"),
    max_search_results: int = 200,
    # ── Search mode ───────────────────────────────────────────────────────────
    search_mode: str = "pubmed_mcp",
    # search_mode = "pubmed_mcp" : Use PubMed MCP server (recommended)
    # search_mode = "entrez"     : Use biopython Entrez API (no MCP needed)
    # search_mode = "csv"        : Import from CSV files (Embase, etc.)
    # search_mode = "multi"      : Search several databases + dedup (see `sources`)
    # search_mode = "demo"       : Synthetic data for pipeline testing
    mcp_server_url: str = "http://localhost:3000",
    csv_files: dict = None,
    # ── Multi-source (search_mode="multi") ─────────────────────────────────────
    sources: dict = None,
    # sources example — PubMed (live) + Embase (pre-downloaded CSV):
    #   {
    #     "PubMed": {"mode": "entrez"},
    #     "Embase": {"csv": "records_tabular.csv"},
    #   }
    dedup_fuzzy_title: bool = True,
    dedup_title_threshold: float = 0.92,
    pubmed_query_override: str = None,
    # A curated PubMed query string. When set, it replaces the auto-generated
    # query for precision. Changing it also changes the cache key (fresh run).
    # ── Full-text retrieval (Phase 1 → Phase 2 gate) ───────────────────────────
    fulltext_dir: str = "fulltext",
    # fetch full text only for abstract-screened survivors:
    #   - PMC open-access papers are fetched automatically (needs biopython)
    #   - paywalled papers: drop your PDFs into fulltext_dir as <PMID>.pdf
    use_pmc: bool = True,
    allow_abstract_fallback: bool = False,
    # allow_abstract_fallback=True lets Phase 2 fall back to the abstract when no
    # full text is available (used in demo mode; NOT recommended for real reviews)
    # ── Resume / checkpointing ─────────────────────────────────────────────────
    resume: bool = True,
    cache_base: str = ".cache",
    stop_for_manual_pdfs: bool = True,
    # When True, the pipeline STOPS after screening if any papers still need to
    # be obtained by hand (included studies with no full text, or not-retrieved
    # studies that couldn't be screened), lists them, and does NOT run
    # extraction/analysis/writing. Add the PDFs and re-run, or pass proceed to
    # synthesize with only what was retrieved.
    # resume=True caches each screened/extracted study per PMID under
    # cache_base/<review-hash>/, so an interrupted run (terminal closed, rate
    # limit, crash) continues where it stopped instead of re-spending tokens.
    # csv_files example:
    # {
    #   "Embase":   "embase_results.csv",
    #   "Cochrane": "cochrane_results.csv",
    #   "PubMed":   "pubmed_results.csv",  # optional
    # }
) -> MetaAnalysisProject:
    """
    Full pipeline: PICO → manuscript.

    search_mode guide:
      "pubmed_mcp"  Use after installing MCP server. Most convenient.
      "entrez"      Use after: pip install biopython
      "csv"         Pass pre-downloaded CSV files via csv_files dict.
      "demo"        Test the full pipeline with synthetic data.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    mode_label = {
        "pubmed_mcp": "PubMed MCP",
        "entrez":     "PubMed Entrez API",
        "csv":        f"CSV import ({', '.join((csv_files or {}).keys())})",
        "multi":      f"Multi-source ({', '.join((sources or {}).keys())})",
        "demo":       "DEMO (synthetic data)",
    }.get(search_mode, search_mode)

    print("\n" + "="*60)
    print("  META-ANALYSIS AGENT SYSTEM")
    print("="*60)
    print(f"  Title        : {title}")
    print(f"  Journal      : {target_journal}")
    print(f"  Search mode  : {mode_label}")
    print("="*60 + "\n")

    project = MetaAnalysisProject(
        title=title,
        pico=pico,
        protocol_doi=protocol_doi,
        target_journal=target_journal
    )

    # Resumable cache, namespaced by the research question so changing the
    # PICO / criteria automatically starts a fresh cache.
    cache_dir = None
    if resume:
        key = run_key(title, pico.population, pico.intervention,
                      pico.comparison, pico.outcome,
                      inclusion_criteria, exclusion_criteria,
                      pubmed_query_override or "")
        cache_dir = cache_dir_for(cache_base, key)
        print(f"  Resume cache : {cache_dir}/  (delete to force a clean run)")

    # ── AGENT 1: SEARCH ───────────────────────────────────────────────────────
    print("\n[STEP 1/5] Literature Search")

    from shared.models import SearchResult
    studies_raw = None
    search_result = None

    # Reuse a frozen search set if the search already ran once. Live PubMed
    # results shift between runs (relevance sort + result cap), so freezing the
    # merged set keeps the review reproducible AND lets the per-study screening
    # cache line up on resume instead of re-screening a shifted set.
    if cache_dir:
        cached_studies = load_json(cache_dir, "studies.json")
        cached_meta = load_json(cache_dir, "search_meta.json")
        if cached_studies and cached_meta:
            studies_raw = cached_studies
            search_result = SearchResult(
                pico=pico,
                mesh_terms=cached_meta.get("mesh_terms", []),
                pubmed_query=cached_meta.get("pubmed", ""),
                cochrane_query=cached_meta.get("cochrane", ""),
                embase_query=cached_meta.get("embase", ""),
                total_hits=len(cached_studies),
                studies=cached_studies,
            )
            print(f"[STEP 1/5] Using frozen search set from cache: "
                  f"{len(studies_raw)} studies "
                  f"(delete {cache_dir}/studies.json to re-search)")

    if studies_raw is None:
        if search_mode == "demo":
            strategy = build_search_strategy(pico, date_range)
            search_result = SearchResult(
                pico=pico,
                mesh_terms=[t for v in strategy.get("mesh_terms", {}).values() for t in v],
                pubmed_query=strategy["pubmed_query"],
                cochrane_query=strategy["cochrane_query"],
                embase_query=strategy["embase_query"],
                total_hits=0,
                studies=[],
            )
            studies_raw = _generate_demo_studies(pico, n=15)
            print(f"[STEP 1/5] Demo mode: using {len(studies_raw)} synthetic studies")
        elif search_mode == "multi":
            if not sources:
                raise ValueError(
                    "search_mode='multi' requires a `sources` dict, e.g.\n"
                    "  sources={'PubMed': {'mode': 'entrez'}, "
                    "'Embase': {'csv': 'records_tabular.csv'}}"
                )
            source_lists, strategy = gather_sources(
                pico, sources, date_range, max_search_results, mcp_server_url,
                pubmed_query_override=pubmed_query_override,
            )
            studies_raw, dedup_report = merge_sources(
                source_lists,
                fuzzy_title=dedup_fuzzy_title,
                title_threshold=dedup_title_threshold,
            )
            search_result = SearchResult(
                pico=pico,
                mesh_terms=[t for v in strategy.get("mesh_terms", {}).values() for t in v],
                pubmed_query=strategy["pubmed_query"],
                cochrane_query=strategy["cochrane_query"],
                embase_query=strategy["embase_query"],
                total_hits=len(studies_raw),
                studies=studies_raw,
            )
            with open(f"{output_dir}/dedup_report.json", "w", encoding="utf-8") as f:
                json.dump(dedup_report, f, indent=2, ensure_ascii=False)
            print(f"[STEP 1/5] Multi-source: {dedup_report['records_by_source']} → "
                  f"{dedup_report['total_after']} unique "
                  f"({dedup_report['duplicates_removed']} duplicates removed)")
        else:
            search_result = run_search_agent(
                pico,
                mode=search_mode,
                date_range=date_range,
                max_results=max_search_results,
                mcp_server_url=mcp_server_url,
                csv_files=csv_files,
            )
            studies_raw = search_result.studies

        # Freeze the search set so resumed runs reuse it exactly.
        if cache_dir and search_mode != "demo":
            save_json(cache_dir, "studies.json", studies_raw)
            save_json(cache_dir, "search_meta.json", {
                "pubmed": search_result.pubmed_query,
                "cochrane": search_result.cochrane_query,
                "embase": search_result.embase_query,
                "mesh_terms": search_result.mesh_terms,
            })

    project.search_results = search_result

    with open(f"{output_dir}/search_queries.json", "w", encoding="utf-8") as f:
        json.dump({
            "mode":     search_mode,
            "pubmed":   search_result.pubmed_query,
            "cochrane": search_result.cochrane_query,
            "embase":   search_result.embase_query,
            "mesh_terms": search_result.mesh_terms,
            "total_records": len(studies_raw),
        }, f, indent=2, ensure_ascii=False)

    search_result.studies = studies_raw

    # ── AGENT 2: SCREENING (two-stage PRISMA) ─────────────────────────────────
    # Phase 1 (abstract) → retrieve full text for survivors → Phase 2 (full text)
    print("\n[STEP 2/5] Study Screening (PRISMA, two-stage)")
    screening = run_screening_2stage(
        studies_raw,
        pico,
        inclusion_criteria,
        exclusion_criteria,
        rob_tool,
        fulltext_dir=fulltext_dir,
        use_pmc=use_pmc,
        allow_abstract_fallback=allow_abstract_fallback,
        cache_dir=cache_dir,
    )

    project.included_studies = [
        d for d in screening["decisions"]
        if d.phase2_decision == "include"
    ]
    project.prisma_numbers = screening["prisma"]
    project.rob_summary = screening["rob_summary"]

    prisma_text = generate_prisma_text(screening["prisma"])
    with open(f"{output_dir}/prisma_flow.txt", "w") as f:
        f.write(prisma_text)
    print(prisma_text)

    # ── Papers the USER must obtain before final synthesis ────────────────────
    #   (1) included studies with no full text  → needed for accurate extraction
    #   (2) not-retrieved studies (no full text AND no abstract) → couldn't be
    #       screened at all; must be obtained to classify include/exclude
    need_pdf = [s for s in screening["included_fulltext"] if not s.get("fulltext_source")]
    not_retrieved = [
        s for s in screening["retrieval"]
        if not s.get("fulltext_source") and not s.get("abstract")
    ]
    write_retrieval_report(need_pdf, f"{output_dir}/fulltext_needed.csv")

    import csv as _csv
    to_obtain = ([("included: need PDF for extraction", s) for s in need_pdf] +
                 [("not retrieved: need to classify", s) for s in not_retrieved])
    with open(f"{output_dir}/papers_to_obtain.csv", "w", newline="", encoding="utf-8") as f:
        w = _csv.writer(f)
        w.writerow(["reason", "pmid", "title", "year", "journal", "doi", "save_as"])
        for reason, s in to_obtain:
            pmid = str(s.get("pmid", "")).strip()
            fkey = file_key(pmid, s.get("title", ""))
            w.writerow([reason, pmid, s.get("title", ""), s.get("year", ""),
                        s.get("journal", ""), s.get("doi", ""),
                        f"fulltext/{fkey}.pdf"])

    if to_obtain:
        print("\n" + "=" * 64)
        print(f"  PAUSED — {len(to_obtain)} paper(s) must be obtained before synthesis")
        print("=" * 64)
        for reason, s in to_obtain:
            pmid = str(s.get("pmid", "")).strip() or "(no PMID)"
            fkey = file_key(s.get("pmid", ""), s.get("title", ""))
            print(f"  [{reason}]")
            print(f"     {pmid} | {(s.get('title') or '')[:66]}")
            print(f"     → save as: fulltext/{fkey}.pdf")
        print("-" * 64)
        print(f"  Full list : {output_dir}/papers_to_obtain.csv")
        print(f"  Next      : download each PDF → save as {fulltext_dir}/<PMID>.pdf → re-run")
        print(f"  Or        : `python orchestrator.py multi proceed` to synthesize now")
        print(f"              with only the {len(project.included_studies)} retrieved studies")
        print("=" * 64 + "\n")
        if stop_for_manual_pdfs:
            print("[STOP] Skipping extraction / analysis / writing until papers are provided.")
            return project

    # ── AGENT 3: DATA EXTRACTION (from full text) ─────────────────────────────
    print("\n[STEP 3/5] Data Extraction")
    # Extract from the full text of the finally-included studies (not the abstract)
    included_fulltext = screening["included_fulltext"]

    outcome_type = _infer_outcome_type(pico.outcome)
    extracted = extract_data(
        included_fulltext,
        primary_outcome_name=pico.outcome,
        outcome_type=outcome_type,
        cache_dir=cache_dir,
    )
    project.extracted_data = extracted

    r_df_code = to_r_dataframe(extracted)
    with open(f"{output_dir}/data.R", "w") as f:
        f.write(r_df_code)

    # ── AGENT 4: STATISTICAL ANALYSIS ─────────────────────────────────────────
    print("\n[STEP 4/5] Statistical Analysis")
    analysis = run_analysis_agent(
        extracted,
        subgroup_vars=["design", "follow_up_wk"],
        sensitivity_scenarios=["leave-one-out", "high-ROB excluded", "RCT only"]
    )

    project.manuscript_sections["results_narrative"] = analysis.get("results_narrative", "")
    project.manuscript_sections["grade_table"] = str(analysis.get("grade_table", {}))
    project.manuscript_sections["analysis_plan"] = analysis.get("analysis_plan", "")

    save_r_script(analysis.get("r_code", ""), f"{output_dir}/meta_analysis.R")

    # ── AGENT 5: MANUSCRIPT WRITING ───────────────────────────────────────────
    print("\n[STEP 5/5] Manuscript Writing")
    sections = write_full_manuscript(project)
    project.manuscript_sections.update(sections)

    manuscript_path = f"{output_dir}/manuscript.md"
    full_text = compile_manuscript(sections, title, manuscript_path)

    # ── FINAL SUMMARY ─────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("  PIPELINE COMPLETE")
    print("="*60)
    print(f"  Output directory : {output_dir}/")
    print(f"  ├── search_queries.json")
    print(f"  ├── prisma_flow.txt")
    print(f"  ├── data.R                  (study data)")
    print(f"  ├── meta_analysis.R         (full R analysis)")
    print(f"  └── manuscript.md           (draft manuscript)")
    print(f"\n  Studies included : {len(project.included_studies)}")
    total_words = sum(len(v.split()) for v in sections.values())
    print(f"  Manuscript words : ~{total_words}")
    print("="*60 + "\n")

    return project


# ── Helper functions ─────────────────────────────────────────────────────────

def _infer_outcome_type(outcome_str: str) -> str:
    binary_keywords = ["event", "mortality", "death", "incidence", "rate",
                       "mace", "stroke", "mi ", "hospitalization", "odds"]
    tte_keywords = ["survival", "time to", "hazard"]
    outcome_lower = outcome_str.lower()
    if any(k in outcome_lower for k in tte_keywords):
        return "time-to-event"
    if any(k in outcome_lower for k in binary_keywords):
        return "binary"
    return "continuous"


def _generate_demo_studies(pico: PICO, n: int = 15) -> list:
    """Generate synthetic study data for demo/testing purposes."""
    import random
    random.seed(42)
    studies = []
    first_authors = ["Kim", "Park", "Lee", "Choi", "Jung", "Han",
                     "Smith", "Johnson", "Wang", "Chen", "Muller",
                     "Tanaka", "Patel", "Santos", "Rossi"]
    years = range(2010, 2025)

    for i in range(n):
        year = random.choice(years)
        studies.append({
            "pmid": str(10000000 + i),
            "title": f"Effect of {pico.intervention} on {pico.outcome} "
                     f"in {pico.population}: A randomized controlled trial",
            "abstract": (
                f"Background: {pico.intervention} has been proposed as a treatment "
                f"for {pico.population}. "
                f"Methods: This RCT enrolled {random.randint(50, 500)} participants "
                f"randomized to {pico.intervention} (n={random.randint(25, 250)}) "
                f"or {pico.comparison} (n={random.randint(25, 250)}). "
                f"Primary outcome was {pico.outcome} at "
                f"{random.choice([12, 24, 52])} weeks. "
                f"Results: Mean {pico.outcome} was {random.uniform(5, 10):.1f} "
                f"(SD {random.uniform(1, 3):.1f}) vs "
                f"{random.uniform(6, 12):.1f} (SD {random.uniform(1, 3):.1f}). "
                f"Conclusion: {pico.intervention} significantly improved outcomes."
            ),
            "year": year,
            "authors": [f"{first_authors[i % len(first_authors)]} A", "Co-author B"]
        })

    return studies


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # ─────────────────────────────────────────
    # 1) PICO configuration (shared)
    # ─────────────────────────────────────────
    MY_PICO = PICO(
        population="Women in the general population across racial and ethnic groups (Non-Hispanic White, Black/African American, Hispanic/Latina, Asian/Pacific Islander, American Indian/Alaska Native)",
        intervention="Racial/ethnic minority groups (Black, Hispanic, Asian/Pacific Islander, American Indian/Alaska Native)",
        comparison="Non-Hispanic White women",
        outcome="Invasive breast cancer age-adjusted incidence rate by race/ethnicity",
        study_design="Observational studies (cohort, cross-sectional, registry-based, population-based)",
        time_frame="2000-2025"
    )

    INCLUSION = [
        "Observational studies (cohort, cross-sectional, registry-based, population-based)",
        "Human subjects, women",
        "Report invasive breast cancer age-adjusted incidence rates by race/ethnicity",
        "Include at least two racial/ethnic groups for comparison",
        "Published in English",
        "Published 2000-2025"
    ]

    EXCLUSION = [
        "Reviews of any kind (narrative, systematic, scoping), editorials, commentaries, letters",
        "Case reports or case series (n<10)",
        "Studies that do NOT report breast cancer incidence separately by race/ethnicity",
        "Studies reporting only mortality, survival, stage, or treatment outcomes without incidence",
        "Studies reporting only prevalence (no incidence) — handle separately, not pooled",
        "Non-breast cancers; male breast cancer; studies of DCIS/in-situ only",
        "Studies reporting only crude (non-age-adjusted) rates",
        "Single racial/ethnic group only (for the primary within-study IRR analysis)",
        "Animal or in vitro studies",
        "Studies focused solely on awareness, knowledge, screening behavior, or risk-factor exposure",
        "Conference abstracts without full data",
    ]

    # Curated, precise PubMed query — requires the breast-cancer, race/ethnicity,
    # AND incidence concepts to all be central, and drops reviews / case reports
    # at the source. Mirrors the Embase query strength (race/disparity in title).
    PRECISE_PUBMED_QUERY = (
        '('
        '"Breast Neoplasms"[Mesh] OR "breast cancer"[tiab] OR "breast carcinoma"[tiab]'
        ') AND ('
        'race[ti] OR racial[ti] OR ethnic*[ti] OR minorit*[ti] OR disparit*[ti] '
        'OR Black[ti] OR Hispanic[ti] OR White[ti] OR Asian[ti] OR "African American"[ti] '
        'OR "Racial Groups"[Mesh] OR "Ethnicity"[Mesh] OR "Health Status Disparities"[Mesh]'
        ') AND ('
        'incidence[ti] OR "incidence rate"[tiab] OR "age-adjusted"[tiab] '
        'OR "age-standardized"[tiab] OR "Incidence"[Mesh]'
        ') AND (2000:2025[dp]) AND English[lang] AND humans[MeSH] '
        'NOT (review[pt] OR "case reports"[pt] OR comment[pt] OR editorial[pt] OR letter[pt])'
    )

    COMMON = dict(
        pico=MY_PICO,
        inclusion_criteria=INCLUSION,
        exclusion_criteria=EXCLUSION,
        rob_tool="NOS",
        target_journal="PLOS ONE",
        protocol_doi="CRD42025XXXXXX",
        title="Racial and Ethnic Disparities in Breast Cancer Incidence: "
              "A Systematic Review and Meta-Analysis",
    )

    # ─────────────────────────────────────────
    # 2) Select search mode
    #    python orchestrator.py [mcp|entrez|csv|multi|demo]
    # ─────────────────────────────────────────
    mode = sys.argv[1] if len(sys.argv) > 1 else "demo"
    # `proceed` (or `go`) as an extra arg = synthesize now, even if some papers
    # still need to be obtained by hand.
    proceed = any(a in ("proceed", "go", "force") for a in sys.argv[2:])

    if mode == "multi":
        # ── MODE E: Multi-source (PubMed live + Embase CSV) + dedup ────
        # Prerequisites:
        #   pip install biopython
        #   export NCBI_EMAIL="your@email.com"
        # PubMed is searched live; Embase is read from the pre-downloaded CSV.
        project = run_meta_analysis(
            **COMMON,
            search_mode="multi",
            sources={
                "PubMed": {"mode": "entrez"},
                "Embase": {"csv": "records_tabular.csv"},
                # "Cochrane": {"csv": "cochrane.csv"},   # optional
            },
            pubmed_query_override=PRECISE_PUBMED_QUERY,
            max_search_results=700,  # covers the full ~686-result breast query
            # Screen on the abstract when full text can't be retrieved (many
            # eligible Embase / paywalled papers have no PMID/PMC), instead of
            # skipping them. Final included studies still need full text for
            # accurate data extraction — see fulltext_needed.csv.
            allow_abstract_fallback=True,
            stop_for_manual_pdfs=not proceed,
        )

    elif mode == "mcp":
        # ── MODE A: PubMed MCP server ─────────────────────────────────
        # Prerequisites:
        #   pip install pubmed-mcp
        #   pubmed-mcp serve --port 3000   (separate terminal)
        project = run_meta_analysis(
            **COMMON,
            search_mode="pubmed_mcp",
            mcp_server_url="http://localhost:3000",
        )

    elif mode == "entrez":
        # ── MODE B: biopython Entrez API ──────────────────────────────
        # Prerequisites:
        #   pip install biopython
        #   export NCBI_EMAIL="your@email.com"
        project = run_meta_analysis(
            **COMMON,
            search_mode="entrez",
            max_search_results=200,
        )

    elif mode == "csv":
        # ── MODE C: Manual CSV file import ────────────────────────────
        # Prerequisites:
        #   Embase   → https://www.embase.com → search → Export → CSV
        #   Cochrane → https://www.cochranelibrary.com → Export → CSV
        #   Place files in current directory then set paths below
        project = run_meta_analysis(
            **COMMON,
            search_mode="csv",
            csv_files={
                "Embase": "records_tabular.csv",
            },
        )

    else:
        # ── MODE D: Demo (default, pipeline test) ─────────────────────
        # Synthetic studies have no real full text, so skip PMC and let
        # Phase 2 fall back to the abstract just to exercise the pipeline.
        project = run_meta_analysis(
            **COMMON,
            search_mode="demo",
            use_pmc=False,
            allow_abstract_fallback=True,
        )
