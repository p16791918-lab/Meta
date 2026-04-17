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
from agent_1_search import run_search_agent, build_search_strategy
from agent_2_screening import screen_studies, generate_prisma_text
from agent_3_extraction import extract_data, to_r_dataframe
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
    # search_mode = "demo"       : Synthetic data for pipeline testing
    mcp_server_url: str = "http://localhost:3000",
    csv_files: dict = None,
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

    # ── AGENT 1: SEARCH ───────────────────────────────────────────────────────
    print("\n[STEP 1/5] Literature Search")

    if search_mode == "demo":
        strategy = build_search_strategy(pico, date_range)
        from shared.models import SearchResult
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

    # ── AGENT 2: SCREENING ────────────────────────────────────────────────────
    print("\n[STEP 2/5] Study Screening (PRISMA)")
    screening = screen_studies(
        studies_raw,
        pico,
        inclusion_criteria,
        exclusion_criteria,
        rob_tool
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

    # ── AGENT 3: DATA EXTRACTION ──────────────────────────────────────────────
    print("\n[STEP 3/5] Data Extraction")
    included_raw = [
        s for s in studies_raw
        if any(d.pmid == s.get("pmid") and d.phase2_decision == "include"
               for d in screening["decisions"])
    ]

    outcome_type = _infer_outcome_type(pico.outcome)
    extracted = extract_data(
        included_raw,
        primary_outcome_name=pico.outcome,
        outcome_type=outcome_type
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
        population="General population across racial and ethnic groups (Non-Hispanic White, Black/African American, Hispanic/Latino, Asian/Pacific Islander, American Indian/Alaska Native)",
        intervention="Racial/ethnic minority groups (Black, Hispanic, Asian/Pacific Islander, American Indian/Alaska Native)",
        comparison="Non-Hispanic White population",
        outcome="Skin cancer incidence rate or prevalence by race/ethnicity (cutaneous melanoma, basal cell carcinoma, squamous cell carcinoma, non-melanoma skin cancer)",
        study_design="Observational studies (cohort, cross-sectional, registry-based, population-based)",
        time_frame="2000-2025"
    )

    INCLUSION = [
        "Observational studies (cohort, cross-sectional, registry-based, population-based)",
        "Human subjects",
        "Report skin cancer incidence rates or prevalence by race/ethnicity",
        "Include at least two racial/ethnic groups for comparison",
        "Cutaneous malignancies (melanoma, BCC, SCC, NMSC, ALM, keratinocyte carcinoma)",
        "Published in English",
        "Published 2000-2025"
    ]

    EXCLUSION = [
        "Non-cutaneous melanoma (uveal, conjunctival, ocular, mucosal melanoma)",
        "Non-skin cancers (lung, oral cavity, esophageal, penile, paranasal sinus)",
        "Case reports or case series (n<10)",
        "Studies reporting only treatment outcomes without incidence/prevalence data",
        "Studies focused solely on awareness or knowledge surveys",
        "Animal studies or in vitro studies",
        "Conference abstracts without full data"
    ]

    COMMON = dict(
        pico=MY_PICO,
        inclusion_criteria=INCLUSION,
        exclusion_criteria=EXCLUSION,
        rob_tool="NOS",
        target_journal="PLOS ONE",
        protocol_doi="CRD42025XXXXXX",
        title="Racial and Ethnic Disparities in Skin Cancer Incidence and Prevalence: "
              "A Systematic Review and Meta-Analysis",
    )

    # ─────────────────────────────────────────
    # 2) Select search mode
    #    python orchestrator.py [mcp|entrez|csv|demo]
    # ─────────────────────────────────────────
    mode = sys.argv[1] if len(sys.argv) > 1 else "demo"

    if mode == "mcp":
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
        project = run_meta_analysis(
            **COMMON,
            search_mode="demo",
        )
