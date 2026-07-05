"""
Agent 2: Screening Agent
- Phase 1: Title/Abstract screening  (screen_phase1)
- Full-text retrieval                (fetch_fulltext.py, called between phases)
- Phase 2: Full-text screening + RoB (screen_phase2)
- PRISMA flowchart numbers

Use run_screening_2stage() for the correct two-stage PRISMA flow: only studies
that pass abstract screening have their full text retrieved and then assessed.
The legacy screen_studies() (abstract-only, both phases in one pass) is kept
for backward compatibility but should not be used for real reviews.
"""
import json
import os
from typing import List, Dict
from shared.claude_cli import call_claude
from shared.prompts import SCREENING_AGENT_PROMPT
from shared.models import ScreeningDecision, RoBLevel, PICO

_ROB_MAP = {
    "low": RoBLevel.LOW,
    "moderate": RoBLevel.MODERATE,
    "high": RoBLevel.HIGH,
    "critical": RoBLevel.CRITICAL,
}


def screen_studies(
    studies: List[Dict],
    pico: PICO,
    inclusion_criteria: List[str],
    exclusion_criteria: List[str],
    rob_tool: str = "RoB2"
) -> Dict:
    """
    Screen a list of studies and return PRISMA numbers + decisions.

    Returns:
        {
            "decisions": List[ScreeningDecision],
            "prisma": { total_retrieved, phase1_excluded, phase2_excluded, included_final },
            "rob_summary": { low, moderate, high, critical }
        }
    """
    decisions = []

    # Batch studies into groups of 10 to reduce API calls
    batch_size = 10
    batches = [studies[i:i+batch_size] for i in range(0, len(studies), batch_size)]

    print(f"[Agent 2: Screening] Processing {len(studies)} studies in {len(batches)} batches...")

    for batch_idx, batch in enumerate(batches):
        studies_text = json.dumps(batch, indent=2, ensure_ascii=False)

        user_message = f"""
        Screen these studies for a meta-analysis.

        PICO:
        P: {pico.population}
        I: {pico.intervention}
        C: {pico.comparison}
        O: {pico.outcome}

        INCLUSION CRITERIA:
        {chr(10).join(f'- {c}' for c in inclusion_criteria)}

        EXCLUSION CRITERIA:
        {chr(10).join(f'- {c}' for c in exclusion_criteria)}

        ROB TOOL: {rob_tool}

        STUDIES (batch {batch_idx+1}):
        {studies_text}

        For EACH study, return a JSON array of decisions:
        [
          {{
            "pmid": "...",
            "title": "...",
            "phase1_decision": "include|exclude|uncertain",
            "phase1_reason": "brief reason",
            "phase2_decision": "include|exclude|pending_full_text",
            "phase2_reason": "brief reason",
            "rob_overall": "low|moderate|high|critical|not_applicable"
          }},
          ...
        ]

        Return ONLY the JSON array. No explanations.
        """

        raw = call_claude(user_message, system=SCREENING_AGENT_PROMPT)
        clean = raw.replace("```json", "").replace("```", "").strip()

        try:
            batch_decisions = json.loads(clean)
            for d in batch_decisions:
                rob_map = {
                    "low": RoBLevel.LOW,
                    "moderate": RoBLevel.MODERATE,
                    "high": RoBLevel.HIGH,
                    "critical": RoBLevel.CRITICAL
                }
                decisions.append(ScreeningDecision(
                    pmid=d.get("pmid", ""),
                    title=d.get("title", ""),
                    authors="",
                    year=0,
                    phase1_decision=d.get("phase1_decision", "uncertain"),
                    phase1_reason=d.get("phase1_reason", ""),
                    phase2_decision=d.get("phase2_decision"),
                    phase2_reason=d.get("phase2_reason"),
                    rob_tool=rob_tool,
                    rob_overall=rob_map.get(d.get("rob_overall", ""), None)
                ))
        except json.JSONDecodeError as e:
            print(f"[Agent 2: Screening] ⚠ JSON parse error in batch {batch_idx+1}: {e}")

        print(f"[Agent 2: Screening] Batch {batch_idx+1}/{len(batches)} done")

    # PRISMA counts
    phase1_excluded = sum(1 for d in decisions if d.phase1_decision == "exclude")
    phase2_excluded = sum(1 for d in decisions
                         if d.phase1_decision != "exclude"
                         and d.phase2_decision == "exclude")
    included_final = sum(1 for d in decisions if d.phase2_decision == "include")

    rob_summary = {
        "low": sum(1 for d in decisions if d.rob_overall == RoBLevel.LOW),
        "moderate": sum(1 for d in decisions if d.rob_overall == RoBLevel.MODERATE),
        "high": sum(1 for d in decisions if d.rob_overall == RoBLevel.HIGH),
        "critical": sum(1 for d in decisions if d.rob_overall == RoBLevel.CRITICAL),
    }

    print(f"[Agent 2: Screening] ✓ Complete")
    print(f"  ▸ Phase 1 excluded: {phase1_excluded}")
    print(f"  ▸ Phase 2 excluded: {phase2_excluded}")
    print(f"  ▸ Final included:   {included_final}")
    print(f"  ▸ RoB: {rob_summary}")

    return {
        "decisions": decisions,
        "prisma": {
            "total_retrieved": len(studies),
            "phase1_excluded": phase1_excluded,
            "phase2_excluded": phase2_excluded,
            "included_final": included_final
        },
        "rob_summary": rob_summary
    }


def generate_prisma_text(prisma: Dict) -> str:
    """Generate PRISMA flow description for Methods section."""
    total = prisma.get("total_retrieved", 0)
    p1_excl = prisma.get("phase1_excluded", 0)
    sought = prisma.get("reports_sought", total - p1_excl)
    not_retrieved = prisma.get("reports_not_retrieved", 0)
    assessed = prisma.get("fulltext_assessed", sought - not_retrieved)
    return f"""
PRISMA Flow:
- Records identified: {total}
- Records excluded (title/abstract): {p1_excl}
- Reports sought for retrieval: {sought}
- Reports not retrieved (no full text): {not_retrieved}
- Full-text reports assessed for eligibility: {assessed}
- Full-text excluded: {prisma.get('phase2_excluded', 0)}
- Studies included in synthesis: {prisma.get('included_final', 0)}
"""


# ─────────────────────────────────────────────────────────────────────────────
# TWO-STAGE SCREENING (correct PRISMA flow)
# ─────────────────────────────────────────────────────────────────────────────

def _batches(seq, size=10):
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def screen_phase1(
    studies: List[Dict],
    pico: PICO,
    inclusion_criteria: List[str],
    exclusion_criteria: List[str],
) -> List[ScreeningDecision]:
    """
    Phase 1 — title/abstract screening ONLY.
    Decides which studies are worth retrieving the full text for.
    Returns one ScreeningDecision per study (phase1 fields filled).
    """
    decisions: List[ScreeningDecision] = []
    batches = _batches(studies, 10)
    print(f"[Agent 2: Phase 1] Abstract screening {len(studies)} studies "
          f"in {len(batches)} batches...")

    for bi, batch in enumerate(batches):
        studies_text = json.dumps(
            [{k: s.get(k) for k in ("pmid", "title", "abstract", "year")} for s in batch],
            indent=2, ensure_ascii=False,
        )
        user_message = f"""
        Phase 1 screening (TITLE/ABSTRACT ONLY) for a meta-analysis.
        Decide, from the abstract alone, whether each study is worth retrieving
        the full text. Be INCLUSIVE: when unsure, mark "uncertain" (which still
        advances to full-text), never "exclude".

        PICO:
        P: {pico.population}
        I: {pico.intervention}
        C: {pico.comparison}
        O: {pico.outcome}

        INCLUSION CRITERIA:
        {chr(10).join(f'- {c}' for c in inclusion_criteria)}

        EXCLUSION CRITERIA:
        {chr(10).join(f'- {c}' for c in exclusion_criteria)}

        STUDIES (batch {bi + 1}):
        {studies_text}

        Return ONLY a JSON array:
        [
          {{"pmid": "...", "title": "...",
            "phase1_decision": "include|exclude|uncertain",
            "phase1_reason": "brief reason"}}
        ]
        """
        raw = call_claude(user_message, system=SCREENING_AGENT_PROMPT)
        clean = raw.replace("```json", "").replace("```", "").strip()
        try:
            for d in json.loads(clean):
                decisions.append(ScreeningDecision(
                    pmid=str(d.get("pmid", "")),
                    title=d.get("title", ""),
                    authors="", year=0,
                    phase1_decision=d.get("phase1_decision", "uncertain"),
                    phase1_reason=d.get("phase1_reason", ""),
                ))
        except json.JSONDecodeError as e:
            print(f"[Agent 2: Phase 1] ⚠ JSON parse error in batch {bi + 1}: {e}")
        print(f"[Agent 2: Phase 1] Batch {bi + 1}/{len(batches)} done")

    advanced = sum(1 for d in decisions if d.phase1_decision != "exclude")
    print(f"[Agent 2: Phase 1] ✓ {advanced}/{len(decisions)} advance to full-text")
    return decisions


def screen_phase2(
    studies_fulltext: List[Dict],
    pico: PICO,
    inclusion_criteria: List[str],
    exclusion_criteria: List[str],
    rob_tool: str = "NOS",
    allow_abstract_fallback: bool = False,
) -> List[ScreeningDecision]:
    """
    Phase 2 — full-text screening + Risk of Bias, one study per call.
    Only studies with retrieved full text are assessed. Studies without full
    text get phase2_decision="not_retrieved" (unless allow_abstract_fallback).
    """
    decisions: List[ScreeningDecision] = []
    print(f"[Agent 2: Phase 2] Full-text screening {len(studies_fulltext)} studies...")

    for idx, study in enumerate(studies_fulltext):
        pmid = str(study.get("pmid", ""))
        title = study.get("title", "")
        text = study.get("fulltext")
        source = study.get("fulltext_source")

        if not text:
            if allow_abstract_fallback and study.get("abstract"):
                text, source = study["abstract"], "abstract_fallback"
            else:
                decisions.append(ScreeningDecision(
                    pmid=pmid, title=title, authors="", year=0,
                    phase1_decision="include", phase1_reason="passed Phase 1",
                    phase2_decision="not_retrieved",
                    phase2_reason="Full text could not be retrieved "
                                  "(paywalled / not in PMC).",
                    rob_tool=rob_tool,
                ))
                print(f"[Agent 2: Phase 2] ({idx + 1}) PMID {pmid}: NOT RETRIEVED — skipped")
                continue

        user_message = f"""
        Phase 2 screening — assess the FULL TEXT for final eligibility and
        Risk of Bias. Base every judgement on the full text below, not guesses.

        PICO:
        P: {pico.population}
        I: {pico.intervention}
        C: {pico.comparison}
        O: {pico.outcome}

        INCLUSION CRITERIA:
        {chr(10).join(f'- {c}' for c in inclusion_criteria)}
        EXCLUSION CRITERIA:
        {chr(10).join(f'- {c}' for c in exclusion_criteria)}

        ROB TOOL: {rob_tool}

        STUDY (PMID {pmid}) — FULL TEXT [source: {source}]:
        {text}

        Return ONLY a JSON object:
        {{
          "phase2_decision": "include|exclude",
          "phase2_reason": "brief reason grounded in the full text",
          "rob_overall": "low|moderate|high|critical"
        }}
        """
        raw = call_claude(user_message, system=SCREENING_AGENT_PROMPT)
        clean = raw.replace("```json", "").replace("```", "").strip()
        try:
            d = json.loads(clean)
            decisions.append(ScreeningDecision(
                pmid=pmid, title=title, authors="", year=0,
                phase1_decision="include", phase1_reason="passed Phase 1",
                phase2_decision=d.get("phase2_decision", "exclude"),
                phase2_reason=d.get("phase2_reason", ""),
                rob_tool=rob_tool,
                rob_overall=_ROB_MAP.get(d.get("rob_overall", ""), None),
            ))
            print(f"[Agent 2: Phase 2] ({idx + 1}) PMID {pmid}: "
                  f"{d.get('phase2_decision')} [{source}]")
        except json.JSONDecodeError as e:
            print(f"[Agent 2: Phase 2] ⚠ JSON parse error for PMID {pmid}: {e}")

    return decisions


def run_screening_2stage(
    studies: List[Dict],
    pico: PICO,
    inclusion_criteria: List[str],
    exclusion_criteria: List[str],
    rob_tool: str = "NOS",
    fulltext_dir: str = "fulltext",
    use_pmc: bool = True,
    allow_abstract_fallback: bool = False,
) -> Dict:
    """
    Correct PRISMA flow:
      Phase 1 (abstract) → retrieve full text for survivors → Phase 2 (full text).

    Returns:
        {
          "decisions":       merged Phase 1 + Phase 2 decisions,
          "prisma":          dict with reports_sought / reports_not_retrieved / ...,
          "rob_summary":     counts by RoB level,
          "retrieval":       advanced studies annotated with fulltext status,
          "included_fulltext": included studies WITH full text (for extraction),
        }
    """
    from fetch_fulltext import fetch_fulltext

    # ── Phase 1: abstract ──────────────────────────────────────────────────
    p1 = screen_phase1(studies, pico, inclusion_criteria, exclusion_criteria)
    p1_by_pmid = {d.pmid: d for d in p1}

    advanced = [
        s for s in studies
        if p1_by_pmid.get(str(s.get("pmid", "")))
        and p1_by_pmid[str(s.get("pmid", ""))].phase1_decision != "exclude"
    ]

    # ── Full-text retrieval (survivors only) ───────────────────────────────
    retrieval = fetch_fulltext(advanced, fulltext_dir=fulltext_dir, use_pmc=use_pmc)

    # ── Phase 2: full text ─────────────────────────────────────────────────
    p2 = screen_phase2(retrieval, pico, inclusion_criteria, exclusion_criteria,
                        rob_tool, allow_abstract_fallback)
    p2_by_pmid = {d.pmid: d for d in p2}

    # ── Merge decisions (carry Phase 1 result into every record) ───────────
    decisions: List[ScreeningDecision] = []
    for s in studies:
        pmid = str(s.get("pmid", ""))
        d1 = p1_by_pmid.get(pmid)
        d2 = p2_by_pmid.get(pmid)
        if d2 is not None:
            decisions.append(d2)
        elif d1 is not None:
            decisions.append(d1)  # Phase-1 excluded (never sought)

    # ── PRISMA counts ──────────────────────────────────────────────────────
    phase1_excluded = sum(1 for d in p1 if d.phase1_decision == "exclude")
    reports_sought = len(advanced)
    reports_not_retrieved = sum(1 for d in p2 if d.phase2_decision == "not_retrieved")
    fulltext_assessed = reports_sought - reports_not_retrieved
    phase2_excluded = sum(1 for d in p2 if d.phase2_decision == "exclude")
    included_final = sum(1 for d in p2 if d.phase2_decision == "include")

    rob_summary = {
        lvl: sum(1 for d in p2 if d.rob_overall == getattr(RoBLevel, lvl.upper()))
        for lvl in ("low", "moderate", "high", "critical")
    }

    included_pmids = {d.pmid for d in p2 if d.phase2_decision == "include"}
    included_fulltext = [s for s in retrieval if str(s.get("pmid", "")) in included_pmids]

    print(f"[Agent 2] ✓ Two-stage screening complete")
    print(f"  ▸ Phase 1 excluded:        {phase1_excluded}")
    print(f"  ▸ Reports sought:          {reports_sought}")
    print(f"  ▸ Not retrieved (paywall): {reports_not_retrieved}")
    print(f"  ▸ Full-text assessed:      {fulltext_assessed}")
    print(f"  ▸ Phase 2 excluded:        {phase2_excluded}")
    print(f"  ▸ Included in synthesis:   {included_final}")

    return {
        "decisions": decisions,
        "prisma": {
            "total_retrieved": len(studies),
            "phase1_excluded": phase1_excluded,
            "reports_sought": reports_sought,
            "reports_not_retrieved": reports_not_retrieved,
            "fulltext_assessed": fulltext_assessed,
            "phase2_excluded": phase2_excluded,
            "included_final": included_final,
        },
        "rob_summary": rob_summary,
        "retrieval": retrieval,
        "included_fulltext": included_fulltext,
    }
